# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Simulated user role for any model that conforms to OpenAI tool use API"""

import os
from logging import getLogger
from typing import Any, Dict, Iterable, List, Literal, Optional, Union, cast

import openai
from dotenv import load_dotenv
from openai import NOT_GIVEN, NotGiven, OpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessageFunctionToolCall,
    ChatCompletionMessageParam,
    ChatCompletionToolParam,
)
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from astra_tool_sandbox.common.execution_context import RoleType
from astra_tool_sandbox.common.message_conversion import (
    Message,
    openai_tool_call_to_python_code,
)
from astra_tool_sandbox.common.tool_conversion import convert_to_openai_tool
from astra_tool_sandbox.common.utils import all_logging_disabled
from astra_tool_sandbox.roles.base_role import BaseRole

LOGGER = getLogger(__name__)


class OpenAIAPIUser(BaseRole):
    """Simulated user role for any model that conforms to OpenAI tool use API"""

    role_type: RoleType = RoleType.USER
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

        # See OpenAIAPIAgent.__init__ for what an explicit base_url means and why the
        # api_key needs a placeholder fallback.
        if base_url is not None:
            self.openai_client = OpenAI(
                api_key=api_key or "EMPTY",
                base_url=base_url,
                timeout=300,
            )
            return

        # Access the API keys
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.openai_client = OpenAI(base_url="https://api.openai.com/v1")

    def respond(self, ending_index: Optional[int] = None) -> None:
        """Reads a List of messages and attempt to respond with a Message

        Specifically, interprets system & agent messages, sends out valid followup responses back to agent

        Comparing to agents and execution environments. Users and user simulators have a unique challenge. Agents and
        execution environments passively accept messages from other roles, execute them and respond. However, a user
        has the autonomy to decide when to stop the conversation. It must be able to, otherwise the conversation is
        never going to stop.

        The current idea is to instruct the user simulator to issue structured responses indicating end of conversation,
        1 such approach could be, we offer a tool to user simulator. The simulator could issue
        tool call to in order to terminate the conversation. This will be interpreted, and sent to execution env to
        execute.

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
        # Get OpenAI tools if most recent turn is from Agent (again, to terminate the conversation if needed)
        available_tools = self.get_available_tools()
        available_tool_names = set(available_tools.keys())
        # openai_tools = (
        #     [convert_to_openai_tool(tool) for tool in available_tools.values()]
        #     if messages[-1].sender == RoleType.AGENT
        #     else NOT_GIVEN
        # )
        # # We need a cast here since `convert_to_openai_tool` returns a plain dict, but
        # # `ChatCompletionToolParam` is a `TypedDict`.
        # openai_tools = cast(
        #     Union[Iterable[ChatCompletionToolParam], NotGiven],
        #     openai_tools,
        # )
        openai_tools = cast(
            Union[Iterable[ChatCompletionToolParam], NotGiven],
            (convert_to_openai_tool(tool) for tool in available_tools.values())
            if messages[-1].sender == RoleType.AGENT
            else NOT_GIVEN,
        )
        # Convert to OpenAI messages
        openai_messages = self.to_openai_messages(messages=messages)
        # Call model
        response = self.model_inference(
            openai_messages=openai_messages, openai_tools=openai_tools
        )
        # Parse response
        openai_response_message = response.choices[0].message

        # Message contains no tool call, aka addressed to agent
        if openai_response_message.tool_calls is None:
            # Not sure why the content field `ChatCompletionMessage` has a type of
            # `str | None`.
            assert openai_response_message.content is not None
            response_messages = [
                Message(
                    sender=self.role_type,
                    recipient=RoleType.AGENT,
                    content=openai_response_message.content,
                )
            ]
        else:
            assert openai_tools is not NOT_GIVEN
            for tool_call in openai_response_message.tool_calls:
                if not isinstance(tool_call, ChatCompletionMessageFunctionToolCall):
                    continue
                response_messages.append(
                    Message(
                        sender=self.role_type,
                        recipient=RoleType.EXECUTION_ENVIRONMENT,
                        content=openai_tool_call_to_python_code(
                            tool_call,
                            available_tool_names,
                            execution_facing_tool_name=None,
                            # The simulator shares the allow list and this code path, but
                            # its calls are not the agent's hallucinations.
                            requested_by=RoleType.USER,
                        ),
                    )
                )
        self.add_messages(response_messages)

    @retry(
        wait=wait_random_exponential(multiplier=0.1, max=60),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type(openai.RateLimitError),
    )
    def model_inference(
        self,
        openai_messages: list[dict[Literal["role", "content"], str]],
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

    @staticmethod
    def to_openai_messages(
        messages: List[Message],
    ) -> List[Dict[Literal["role", "content"], str]]:
        """Converts a list of Tool Sandbox messages to OpenAI API messages, from the perspective of a simulated user

        Args:
            messages:   A list of Tool Sandbox messages

        Returns:
            A list of OpenAI API messages
        """
        openai_messages: List[Dict[Literal["role", "content"], str]] = []
        for message in messages:
            if message.sender == RoleType.SYSTEM and message.recipient == RoleType.USER:
                openai_messages.append({"role": "system", "content": message.content})
            elif (
                message.sender == RoleType.AGENT and message.recipient == RoleType.USER
            ):
                # The roles are in reverse
                # We are the user simulator, simulated response from OpenAI assistant role is the simulated user message
                # which means agent dialog is OpenAI user role
                openai_messages.append({"role": "user", "content": message.content})
            elif (
                message.sender == RoleType.USER and message.recipient == RoleType.AGENT
            ):
                openai_messages.append(
                    {"role": "assistant", "content": message.content}
                )
            elif (
                message.sender == RoleType.USER
                and message.recipient == RoleType.EXECUTION_ENVIRONMENT
            ) or (
                message.sender == RoleType.EXECUTION_ENVIRONMENT
                and message.recipient == RoleType.USER
            ):
                # These pairs are ignored.
                pass
            else:
                raise ValueError(
                    f"Unrecognized sender recipient pair {(message.sender, message.recipient)}"
                )
        return openai_messages


class GPT_4_o_2024_11_20_User(OpenAIAPIUser):
    model_name = "gpt-4o-2024-11-20"


class GPT_4_1_2025_04_14_User(OpenAIAPIUser):
    model_name = "gpt-4.1-2025-04-14"
