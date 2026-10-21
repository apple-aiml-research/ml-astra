# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Interactive CLI user/agent role for human interfacing."""

import ast
import inspect
import json
import uuid
from dataclasses import dataclass
from logging import getLogger
from typing import Any, Callable, List, Optional

from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)

from astra_tool_sandbox.common.execution_context import RoleType, get_current_context
from astra_tool_sandbox.common.message_conversion import (
    Message,
    openai_tool_call_to_python_code,
)
from astra_tool_sandbox.roles.base_role import BaseRole

LOGGER = getLogger(__name__)


@dataclass
class InteractiveMessage:
    content: Optional[str] = None
    tool_call: Optional[str] = None


class CliRole(BaseRole):
    """Interactive CLI user/agent role for a real human."""

    role_type: RoleType
    model_name: str

    def __init__(self) -> None:
        print(f"Interactive role '{self.role_type}'.")

    def respond(self, ending_index: Optional[int] = None) -> None:
        """Reads a List of messages and attempt to respond with a Message

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
        # Agent does not respond to System
        if self.role_type == RoleType.AGENT and messages[-1].sender == RoleType.SYSTEM:
            return
        # Get tools.
        available_tools = self.get_available_tools()

        print("*" * 80)
        for msg in messages:
            print(f" [{msg.sender}] -> [{msg.recipient}]: {msg.content}")
        print("-" * 80)
        # Ask user for input.
        response = self.user_input()

        # Parse response
        if response.tool_call is None:
            # Message contains no tool call, aka addressed to agent
            assert response.content is not None
            recipient_role = (
                RoleType.AGENT if self.role_type == RoleType.USER else RoleType.USER
            )
            response_messages = [
                Message(
                    sender=self.role_type,
                    recipient=recipient_role,
                    content=response.content,
                )
            ]
        else:
            assert response.tool_call is not None
            response_messages = [
                self.tool_call_message(response.tool_call, available_tools)
            ]
        self.add_messages(response_messages)

    def user_input(self) -> InteractiveMessage:
        """Get the user input from the CLI and return a message.

        Returns:
          A message containing the plain text or tool call information.
        """
        available_tool_names = self.get_available_tools().keys()
        text = input(f" [{self.role_type}] > ")
        if (
            (text.lower() == "end")
            or (text.lower() == "end_conversation")
            or (text.lower() == "end conversation")
        ) and "end_conversation" in available_tool_names:
            return InteractiveMessage(tool_call="end_conversation()")
        if text != "tool":
            return InteractiveMessage(content=text)
        # Tool call, show available options.
        tool_names_sigs = [
            (f.__name__, inspect.signature(f))
            for f in self.get_available_tools().values()
        ]
        tools_fmtd = "\n".join([f" - {name}{sig}" for name, sig in tool_names_sigs])
        print(f"Tool options: \n {tools_fmtd}.")
        tool_name = input(f" [{self.role_type}] Tool function call > ")
        return InteractiveMessage(tool_call=tool_name)

    def user_tool_call_to_python_code(
        self, tool_call: str, available_tool_names: set[str]
    ) -> str:
        """Convert a tool call into an execution environment command."""
        return f"print(repr({tool_call}))"

    def tool_call_message(
        self, tool_call: str, available_tools: dict[str, Callable[..., Any]]
    ) -> Message:
        """Build the message sending a typed tool call to the execution environment."""
        return Message(
            sender=self.role_type,
            recipient=RoleType.EXECUTION_ENVIRONMENT,
            content=self.user_tool_call_to_python_code(
                tool_call, set(available_tools.keys())
            ),
        )


def parse_tool_call(
    tool_call: str, available_tools: dict[str, Callable[..., Any]]
) -> tuple[str, dict[str, Any]]:
    """Parse a typed call like `search_contacts(contact_name='Paul')`.

    Returns:
        The tool name and its keyword arguments. Positional arguments are bound to
        parameter names using the tool's signature.

    Raises:
        ValueError: If the text is not a call with literal arguments.
    """
    try:
        call = ast.parse(tool_call.strip(), mode="eval").body
    except SyntaxError as exception:
        raise ValueError(f"invalid syntax: {exception.msg}") from exception
    if not isinstance(call, ast.Call) or not isinstance(call.func, ast.Name):
        raise ValueError("expected a call like tool_name(arg=value)")
    if any(keyword.arg is None for keyword in call.keywords):
        raise ValueError("**kwargs is not supported")
    try:
        args = [ast.literal_eval(arg) for arg in call.args]
        arguments = {
            str(keyword.arg): ast.literal_eval(keyword.value)
            for keyword in call.keywords
        }
    except ValueError as exception:
        raise ValueError(
            "arguments must be Python literals, e.g. quote strings"
        ) from exception
    name = call.func.id
    if args:
        if name not in available_tools:
            raise ValueError(
                f"unknown tool {name!r}, positional arguments need a known tool"
            )
        try:
            arguments = dict(
                inspect.signature(available_tools[name])
                .bind_partial(*args, **arguments)
                .arguments
            )
        except TypeError as exception:
            raise ValueError(str(exception)) from exception
    return name, arguments


class CliUser(CliRole):
    role_type: RoleType = RoleType.USER
    model_name = "cli_user"


class CliAgent(CliRole):
    role_type: RoleType = RoleType.AGENT
    model_name = "cli_agent"

    def tool_call_message(
        self, tool_call: str, available_tools: dict[str, Callable[..., Any]]
    ) -> Message:
        """Build the tool call the same way the API agents do, so the trajectory can
        be serialized to OpenAI messages for evaluation. Re-prompts until the typed
        call parses.
        """
        while True:
            try:
                name, arguments = parse_tool_call(tool_call, available_tools)
                arguments_json = json.dumps(arguments)
                break
            except (ValueError, TypeError) as exception:
                print(f"Could not parse tool call: {exception}")
                tool_call = input(f" [{self.role_type}] Tool function call > ")
        tool_call_id = f"call_{uuid.uuid4().hex}"
        openai_tool_call = ChatCompletionMessageToolCall(
            id=tool_call_id,
            type="function",
            function=Function(name=name, arguments=arguments_json),
        )
        return Message(
            sender=self.role_type,
            recipient=RoleType.EXECUTION_ENVIRONMENT,
            content=openai_tool_call_to_python_code(
                openai_tool_call,
                set(available_tools.keys()),
                execution_facing_tool_name=get_current_context().get_execution_facing_tool_name(
                    name
                ),
            ),
            openai_tool_call_id=tool_call_id,
            openai_function_name=name,
        )
