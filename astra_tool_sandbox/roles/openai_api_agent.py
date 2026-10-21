# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Agent role for any model that conforms to OpenAI tool use API"""

import logging
import os
from typing import Any, Iterable, List, Literal, Optional, Union, cast

import openai
from dotenv import load_dotenv
from openai import NOT_GIVEN, NotGiven
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessageFunctionToolCall,
    ChatCompletionMessageParam,
    ChatCompletionToolParam,
)
from requests.exceptions import HTTPError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from astra_tool_sandbox.common.execution_context import RoleType, get_current_context
from astra_tool_sandbox.common.message_conversion import (
    Message,
    openai_tool_call_to_python_code,
    to_openai_messages,
)
from astra_tool_sandbox.common.tool_conversion import convert_to_openai_tools
from astra_tool_sandbox.common.utils import all_logging_disabled
from astra_tool_sandbox.roles.base_role import BaseRole

LOGGER = logging.getLogger(__name__)


class OpenAIAPIAgent(BaseRole):
    """Agent role for any model that conforms to OpenAI tool use API"""

    role_type: RoleType = RoleType.AGENT
    model_name: str

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        # We set the `base_url` explicitly here to avoid picking up the
        # `OPENAI_BASE_URL` environment variable that may be set for serving models as
        # OpenAI API compatible servers.

        # Load environment variables from .env file
        load_dotenv()

        if model_name is not None:
            self.model_name = model_name

        # An explicit `base_url` means the caller is pointing this role at one specific
        # OpenAI-compatible endpoint -- a locally hosted open-source model, for
        # instance. Honour it verbatim instead of falling through to the public OpenAI
        # defaults below. The api_key fallback matters because such a server usually
        # ignores the value but the OpenAI client still refuses a None.
        if base_url is not None:
            self.openai_client = openai.OpenAI(
                api_key=api_key or "EMPTY",
                base_url=base_url,
                timeout=300,
            )
            return

        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.openai_client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1",
            timeout=300,
        )

    def respond(self, ending_index: Optional[int] = None) -> None:
        """Reads a List of messages and attempt to respond with a Message

        Specifically, interprets system, user, execution environment messages and sends out NL response to user, or
        code snippet to execution environment.

        Message comes from current context, the last k messages should be directed to this role type
        Response are written to current context as well. n new messages, addressed to appropriate recipient
        k != n when dealing with parallel function call and responses. Parallel function call are expanded into
        individual messages, parallel function call responses are combined as 1 OpenAI API request

        Args:
            ending_index:   Optional index. Will respond to message located at ending_index instead of most recent one
                            if provided. Utility for processing system message, which could contain multiple entries
                            before each was responded to

        Raises:
            KeyError:   When the last message is not directed to this role
        """
        messages: List[Message] = self.get_messages(ending_index=ending_index)
        response_messages: List[Message] = []
        self.messages_validation(messages=messages)
        # Keeps only relevant messages
        messages = self.filter_messages(messages=messages)
        # Does not respond to System
        if messages[-1].sender == RoleType.SYSTEM:
            return
        # Get OpenAI tools if most recent message is from user
        available_tools = self.get_available_tools()
        available_tool_names = set(available_tools.keys())
        openai_tools = cast(
            Union[Iterable[ChatCompletionToolParam], NotGiven],
            (
                convert_to_openai_tools(available_tools)
                if messages[-1].sender == RoleType.USER
                or messages[-1].sender == RoleType.EXECUTION_ENVIRONMENT
                else NOT_GIVEN
            ),
        )
        # We need a cast here since `convert_to_openai_tool` returns a plain dict, but
        # `ChatCompletionToolParam` is a `TypedDict`.
        # openai_tools = cast(
        #     Union[Iterable[ChatCompletionToolParam], NotGiven],
        #     openai_tools,
        # )

        # Convert to OpenAI messages.
        current_context = get_current_context()
        openai_messages, _ = to_openai_messages(messages)
        # Call model
        response = self.model_inference(
            openai_messages=openai_messages, openai_tools=openai_tools
        )
        # Parse response
        openai_response_message = response.choices[0].message
        # Reasoning token count, when the model reports one. Read defensively:
        # `usage`, `completion_tokens_details` and `reasoning_tokens` are each
        # absent on non-reasoning models and on some OpenAI-compatible proxies.
        reasoning_token_count = getattr(
            getattr(
                getattr(response, "usage", None), "completion_tokens_details", None
            ),
            "reasoning_tokens",
            None,
        )
        # Message contains no tool call, aka addressed to user
        if openai_response_message.tool_calls is None:
            assert openai_response_message.content is not None
            response_messages = [
                Message(
                    sender=self.role_type,
                    recipient=RoleType.USER,
                    content=openai_response_message.content,
                    reasoning_token_count=reasoning_token_count,
                )
            ]
        else:
            assert openai_tools is not NOT_GIVEN
            for tool_call in openai_response_message.tool_calls:
                if not isinstance(tool_call, ChatCompletionMessageFunctionToolCall):
                    continue
                # The response contains the agent facing tool name so we need to get
                # the execution facing tool name when creating the Python code.
                execution_facing_tool_name = (
                    current_context.get_execution_facing_tool_name(
                        tool_call.function.name
                    )
                )
                response_messages.append(
                    Message(
                        sender=self.role_type,
                        recipient=RoleType.EXECUTION_ENVIRONMENT,
                        content=openai_tool_call_to_python_code(
                            tool_call,
                            available_tool_names,
                            execution_facing_tool_name=execution_facing_tool_name,
                        ),
                        openai_tool_call_id=tool_call.id,
                        openai_function_name=tool_call.function.name,
                        # Parallel tool calls all come from one API response, so
                        # only the first message carries the count. Otherwise
                        # summing a trajectory would multiply-count one response.
                        reasoning_token_count=(
                            reasoning_token_count if not response_messages else None
                        ),
                    )
                )
        self.add_messages(response_messages)

    @retry(
        wait=wait_random_exponential(multiplier=1, max=40),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(HTTPError),
    )
    def model_inference(
        self,
        openai_messages: list[
            dict[
                Literal["role", "content", "tool_call_id", "name", "tool_calls"],
                Any,
            ]
        ],
        openai_tools: Union[Iterable[ChatCompletionToolParam], NotGiven],
    ) -> ChatCompletion:
        """Run OpenAI model inference

        Args:
            openai_messages:    List of OpenAI API format messages
            openai_tools:       List of OpenAI API format tools definition

        Returns:
            OpenAI API chat completion object
        """
        with all_logging_disabled():
            create_kwargs: dict[str, Any] = {
                "model": self.model_name,
                "messages": cast(list[ChatCompletionMessageParam], openai_messages),
                "tools": openai_tools,
            }
            return cast(
                ChatCompletion,
                self.openai_client.chat.completions.create(**create_kwargs),
            )


class GPT_4_o_mini_2024_07_18_Agent(OpenAIAPIAgent):
    model_name = "gpt-4o-mini-2024-07-18"


class GPT_4_o_2024_05_13_Agent(OpenAIAPIAgent):
    model_name = "gpt-4o-2024-05-13"


class GPT_4_o_2024_11_20_Agent(OpenAIAPIAgent):
    model_name = "gpt-4o-2024-11-20"


class GPT_o_3_2025_04_16_Agent(OpenAIAPIAgent):
    model_name = "o3-2025-04-16"


class GPT_4_1_2025_04_14_Agent(OpenAIAPIAgent):
    # non-reasoning model
    model_name = "gpt-4.1-2025-04-14"


class GPT_5_2025_08_07_Agent(OpenAIAPIAgent):
    model_name = "gpt-5-2025-08-07"


class GPT_5_1_2025_11_13_Agent(OpenAIAPIAgent):
    model_name = "gpt-5.1-2025-11-13"


# class GPT_5_minimal_2025_08_07_Agent(OpenAIAPIAgent):
#     model_name = "gpt-5"

#     @retry(
#         wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_attempt(3)
#     )
#     def model_inference(
#         self,
#         openai_messages: list[
#             dict[
#                 Literal["role", "content", "tool_call_id", "name", "tool_calls"],
#                 Any,
#             ]
#         ],
#         openai_tools: Union[Iterable[ChatCompletionToolParam], NotGiven],
#     ) -> ChatCompletion:
#         """Run OpenAI model inference with minimal reasoning effort using responses API"""
#         with all_logging_disabled():
#             # Convert messages to responses API format
#             input_messages = self._convert_to_responses_input(openai_messages)

#             response = self.openai_client.responses.create(
#                 model=self.model_name,
#                 input=input_messages,
#                 reasoning={"effort": "minimal"},
#             )

#             # Convert response back to ChatCompletion format
#             return self._convert_response_to_chat_completion(response)

#     def _convert_to_responses_input(self, messages):
#         """Convert OpenAI messages format to responses API input format"""
#         input_messages = []
#         for msg in messages:
#             role = msg.get("role", "")
#             content = msg.get("content", "")

#             # Skip empty messages
#             if not content:
#                 continue

#             # Convert role names if needed
#             if role in ["system", "user", "assistant"]:
#                 input_messages.append({"role": role, "content": content})
#         return input_messages

#     def _convert_response_to_chat_completion(self, response):
#         """Convert responses API response to ChatCompletion format"""
#         from openai.types.chat import ChatCompletion, ChatCompletionMessage
#         from openai.types.chat.chat_completion import Choice

#         # Extract content from response
#         content = (
#             response.output_text if hasattr(response, "output_text") else str(response)
#         )

#         message = ChatCompletionMessage(
#             role="assistant", content=content, tool_calls=None
#         )

#         choice = Choice(index=0, message=message, finish_reason="stop")

#         return ChatCompletion(
#             id=getattr(response, "id", f"resp-{hash(content) % 10000}"),
#             choices=[choice],
#             created=getattr(response, "created_at", 0),
#             model=self.model_name,
#             object="chat.completion",
#         )


# class GPT_5_low_2025_08_07_Agent(GPT_5_minimal_2025_08_07_Agent):
#     model_name = "gpt-5"

#     @retry(
#         wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_attempt(3)
#     )
#     def model_inference(
#         self,
#         openai_messages: list[
#             dict[
#                 Literal["role", "content", "tool_call_id", "name", "tool_calls"],
#                 Any,
#             ]
#         ],
#         openai_tools: Union[Iterable[ChatCompletionToolParam], NotGiven],
#     ) -> ChatCompletion:
#         """Run OpenAI model inference with low reasoning effort using responses API"""
#         with all_logging_disabled():
#             input_messages = self._convert_to_responses_input(openai_messages)

#             response = self.openai_client.responses.create(
#                 model=self.model_name, input=input_messages, reasoning={"effort": "low"}
#             )

#             return self._convert_response_to_chat_completion(response)


# class GPT_5_high_2025_08_07_Agent(GPT_5_minimal_2025_08_07_Agent):
#     model_name = "gpt-5"

#     @retry(
#         wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_attempt(3)
#     )
#     def model_inference(
#         self,
#         openai_messages: list[
#             dict[
#                 Literal["role", "content", "tool_call_id", "name", "tool_calls"],
#                 Any,
#             ]
#         ],
#         openai_tools: Union[Iterable[ChatCompletionToolParam], NotGiven],
#     ) -> ChatCompletion:
#         """Run OpenAI model inference with high reasoning effort using responses API"""
#         with all_logging_disabled():
#             input_messages = self._convert_to_responses_input(openai_messages)

#             response = self.openai_client.responses.create(
#                 model=self.model_name,
#                 input=input_messages,
#                 reasoning={"effort": "high"},
#             )

#             return self._convert_response_to_chat_completion(response)
