# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Agent role for any model that conforms to DeepSeek tool use API"""

import os
from typing import Any, Iterable, List, Literal, Optional, Union, cast

import openai
from dotenv import load_dotenv
from openai import NOT_GIVEN, NotGiven, OpenAI

# , OpenAI
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


class DeepSeekAPIAgent(BaseRole):
    """Agent role for any model that conforms to DeepSeek tool use API"""

    role_type: RoleType = RoleType.AGENT
    model_name: str

    def __init__(self) -> None:
        # Load environment variables from .env file
        load_dotenv()

        # Access the API keys
        api_key = os.getenv("DEEPSEEK_API_KEY")

        self.deepseek_client: OpenAI = openai.OpenAI(
            api_key=api_key, base_url="https://api.deepseek.com"
        )

    def respond(self, ending_index: Optional[int] = None) -> None:
        """Reads a List of messages and attempt to respond with a Message

        Specifically, interprets system, user, execution environment messages and sends out NL response to user, or
        code snippet to execution environment.

        Message comes from current context, the last k messages should be directed to this role type
        Response are written to current context as well. n new messages, addressed to appropriate recipient
        k != n when dealing with parallel function call and responses. Parallel function call are expanded into
        individual messages, parallel function call responses are combined as 1 API request

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
        # Get DeepSeek compatible tools if most recent message is from user
        available_tools = self.get_available_tools()
        available_tool_names = set(available_tools.keys())
        deepseek_tools = cast(
            Union[Iterable[ChatCompletionToolParam], NotGiven],
            (
                convert_to_openai_tools(available_tools)
                if messages[-1].sender == RoleType.USER
                or messages[-1].sender == RoleType.EXECUTION_ENVIRONMENT
                else NOT_GIVEN
            ),
        )
        # Convert to DeepSeek messages.
        current_context = get_current_context()
        deepseek_messages, _ = to_openai_messages(messages)
        # Call model
        response = self.model_inference(
            deepseek_messages=deepseek_messages, deepseek_tools=deepseek_tools
        )
        # Parse response
        deepseek_response_message = response.choices[0].message
        # Message contains no tool call, aka addressed to user
        if deepseek_response_message.tool_calls is None:
            assert deepseek_response_message.content is not None
            response_messages = [
                Message(
                    sender=self.role_type,
                    recipient=RoleType.USER,
                    content=deepseek_response_message.content,
                )
            ]
        else:
            assert deepseek_tools is not NOT_GIVEN
            for tool_call in deepseek_response_message.tool_calls:
                if not isinstance(tool_call, ChatCompletionMessageFunctionToolCall):
                    continue
                tool_call.id = tool_call.id.replace("-", "_")
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
        deepseek_messages: list[
            dict[
                Literal["role", "content", "tool_call_id", "name", "tool_calls"],
                Any,
            ]
        ],
        deepseek_tools: Union[Iterable[ChatCompletionToolParam], NotGiven],
    ) -> ChatCompletion:
        """Run DeepSeek model inference

        Args:
            messages:    List of OpenAI client format messages
            tools:       List of OpenAI client format tools definition

        Returns:
            DeepSeek API chat completion object
        """
        with all_logging_disabled():
            create_kwargs: dict[str, Any] = {
                "model": self.model_name,
                "messages": cast(list[ChatCompletionMessageParam], deepseek_messages),
                "tools": deepseek_tools,
            }
            response = cast(
                ChatCompletion,
                self.deepseek_client.chat.completions.create(**create_kwargs),
            )

            # Debug: Check if response is unexpectedly a string
            if isinstance(response, str):
                print(
                    "ERROR: DeepSeek API returned string instead of ChatCompletion object:"
                )
                print(f"Response: {response[:500]}...")  # Print first 500 chars
                raise RuntimeError(f"DeepSeek API returned string: {response[:200]}")

            return response


class DeepSeekChatAgent(DeepSeekAPIAgent):
    model_name = "deepseek-chat"
