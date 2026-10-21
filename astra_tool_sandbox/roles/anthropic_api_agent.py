# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Agent role for any Anthropic model via the public Anthropic API.

Uses the **native Anthropic API** at ``api.anthropic.com`` (not the
OpenAI-compat translator), so features like extended thinking and prompt
caching stay first-class. Auth uses ``ANTHROPIC_API_KEY``.
"""

import ast
import dataclasses
import logging
import re
from typing import Any, Iterable, Optional, Union, cast

import anthropic
from anthropic import Anthropic
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
    unavailable_tool_call_code,
)
from astra_tool_sandbox.roles._anthropic_compat import (
    MessageParam,
    ResponseMessage,
    TextBlock,
    TextBlockParam,
    ToolParam,
    ToolResultBlockParam,
    ToolUseBlock,
    messages_create,
)
from astra_tool_sandbox.roles.anthropic_tool_utils import convert_to_anthropic_tool
from astra_tool_sandbox.roles.base_role import BaseRole

LOGGER = logging.getLogger(__name__)


def tool_use_block_to_python_code(
    execution_facing_tool_name: str,
    tool_use_block: ToolUseBlock,
    available_tool_names: set[str],
) -> str:
    """Converts Anthropic tool use block to Python code for calling the function.

    A tool the agent was not offered yields code that fails at execution time rather
    than raising here — see `unavailable_tool_call_code`.
    """
    agent_facing_tool_name = tool_use_block.name
    if agent_facing_tool_name not in available_tool_names:
        return unavailable_tool_call_code(
            tool_use_block.id,
            agent_facing_tool_name,
            available_tool_names,
            tool_use_block.input,
        )
    tool_id = tool_use_block.id
    function_call_code = (
        f"{tool_id}_parameters = {tool_use_block.input}\n"
        f"{tool_id}_response = {execution_facing_tool_name}(**{tool_id}_parameters)\n"
        f"print(repr({tool_id}_response))"
    )
    return function_call_code


def to_tool_call_message(
    tool_use_block: ToolUseBlock,
    sender: RoleType,
    execution_facing_tool_name: str,
    available_tool_names: set[str],
) -> Message:
    """Convert a tool use block to the tool sandbox message format."""
    assert tool_use_block.type == "tool_use", (
        "This function must only be called with content blocks of type 'tool_use', but "
        f"got '{tool_use_block.type}'."
    )
    return Message(
        sender=sender,
        recipient=RoleType.EXECUTION_ENVIRONMENT,
        content=tool_use_block_to_python_code(
            execution_facing_tool_name, tool_use_block, available_tool_names
        ),
        openai_tool_call_id=tool_use_block.id,
        openai_function_name=tool_use_block.name,
    )


def response_to_messages(
    response: ResponseMessage,
    sender: RoleType,
    available_tool_names: set[str],
    agent_to_execution_facing_tool_name: dict[str, str],
) -> list[Message]:
    """Convert an Anthropic API response to messages in the tool sandbox format."""
    assert response.stop_reason is not None

    if response.stop_reason == "tool_use":
        assert len(response.content) > 0 and any(
            isinstance(content_block, ToolUseBlock)
            for content_block in response.content
        ), "At least 1 ToolUseBlock content element is needed for tool use, but got 0."
        return [
            to_tool_call_message(
                content_block,
                sender,
                # A hallucinated name is absent from this mapping. Fall back to the
                # name itself so the unavailable-tool path in
                # `tool_use_block_to_python_code` is reachable — subscripting here
                # would raise KeyError first and abort the scenario.
                execution_facing_tool_name=agent_to_execution_facing_tool_name.get(
                    content_block.name, content_block.name
                ),
                available_tool_names=available_tool_names,
            )
            for content_block in response.content
            if isinstance(content_block, ToolUseBlock)
        ]

    assert (
        len(response.content) == 1
    ), f"Only a single content element is supported, but got {len(response.content)}."
    text_block = response.content[0]
    assert isinstance(
        text_block, TextBlock
    ), f"Expected content element to be a `TextBlock`, but got {type(text_block)}."
    return [
        Message(
            sender=sender,
            recipient=RoleType.USER,
            content=text_block.text,
        )
    ]


@dataclasses.dataclass(frozen=True)
class AnthropicMessageCollection:
    """Collection of messages and system prompt in the Anthropic API format."""

    messages: list[MessageParam]
    system_prompt: Union[str, anthropic.NotGiven]


def has_tool_result_block(
    anthropic_message: MessageParam,
) -> bool:
    return isinstance(anthropic_message, dict) and any(
        isinstance(block, dict) and block.get("type", "") == "tool_result"
        for block in anthropic_message["content"]
    )


def to_anthropic_tool_result_block(
    message: Message,
) -> ToolResultBlockParam:
    assert message.openai_tool_call_id is not None
    assert message.openai_function_name is not None
    return ToolResultBlockParam(
        tool_use_id=message.openai_tool_call_id,
        type="tool_result",
        content=[TextBlockParam(text=message.content, type="text")],
        is_error=message.tool_call_exception is not None,
    )


def has_tool_use_block(
    anthropic_message: MessageParam,
) -> bool:
    return isinstance(anthropic_message, dict) and any(
        isinstance(block, ToolUseBlock) for block in anthropic_message["content"]
    )


def to_anthropic_tool_use_block(
    message: Message,
) -> ToolUseBlock:
    pattern = r"^(?P<tool_id>.+)_parameters = (?P<arguments>[^\n]+)\n(?P=tool_id)_response = (?P<name>[^\(]+)"
    match = re.match(pattern=pattern, string=message.content)
    assert match is not None
    assert message.openai_tool_call_id is not None
    assert message.openai_function_name is not None
    return ToolUseBlock(
        id=message.openai_tool_call_id,
        input=ast.literal_eval(match.group("arguments")),
        name=message.openai_function_name,
        type="tool_use",
    )


def to_anthropic_message_collection(
    messages: list[Message],
) -> AnthropicMessageCollection:
    """Converts a list of Tool Sandbox messages to Anthropic API messages."""
    anthropic_messages: list[MessageParam] = []
    system_prompt: Union[str, anthropic.NotGiven] = anthropic.NOT_GIVEN

    for message in messages:
        if message.sender == RoleType.SYSTEM and message.recipient == RoleType.AGENT:
            if system_prompt is anthropic.NOT_GIVEN:
                system_prompt = message.content
            else:
                assert isinstance(system_prompt, str)
                system_prompt = system_prompt + "\n\n" + message.content
        elif message.sender == RoleType.USER and message.recipient == RoleType.AGENT:
            anthropic_messages.append(
                MessageParam(content=message.content, role="user")
            )
        elif (
            message.sender == RoleType.EXECUTION_ENVIRONMENT
            and message.recipient == RoleType.AGENT
        ):
            tool_result_block = to_anthropic_tool_result_block(message)
            if len(anthropic_messages) > 0 and has_tool_result_block(
                anthropic_messages[-1]
            ):
                assert isinstance(anthropic_messages[-1]["content"], list)
                anthropic_messages[-1]["content"].append(tool_result_block)
            else:
                anthropic_messages.append(
                    MessageParam(content=[tool_result_block], role="user")
                )
        elif (
            message.sender == RoleType.AGENT
            and message.recipient == RoleType.EXECUTION_ENVIRONMENT
        ):
            tool_use_block = to_anthropic_tool_use_block(message)
            if len(anthropic_messages) > 0 and has_tool_use_block(
                anthropic_messages[-1]
            ):
                assert isinstance(anthropic_messages[-1]["content"], list)
                anthropic_messages[-1]["content"].append(tool_use_block)
            else:
                anthropic_messages.append(
                    MessageParam(content=[tool_use_block], role="assistant")
                )
        elif message.sender == RoleType.AGENT and message.recipient == RoleType.USER:
            anthropic_messages.append(
                MessageParam(content=message.content, role="assistant")
            )
        else:
            raise ValueError(
                "Unrecognized sender recipient pair "
                f"{(message.sender, message.recipient)}"
            )

    return AnthropicMessageCollection(
        messages=anthropic_messages, system_prompt=system_prompt
    )


class AnthropicAPIAgent(BaseRole):
    """Agent role for any Anthropic tool-use model via the public API."""

    role_type: RoleType = RoleType.AGENT
    #: Bare Anthropic model id (e.g. ``"claude-opus-4-8"``), used verbatim on
    #: the ``api.anthropic.com`` path.
    model_name: str
    #: Optional class-attribute override. Concrete subclasses can set to enable
    #: extended thinking on Claude 4.x. ``None`` means thinking is off.
    thinking_budget_tokens: Optional[int] = None

    def __init__(self) -> None:
        self.client = Anthropic()
        httpx_logger = logging.getLogger("httpx")
        httpx_logger.setLevel(logging.WARNING)

    def respond(self, ending_index: Optional[int] = None) -> None:
        """Reads a List of messages and attempt to respond with a Message."""
        messages: list[Message] = self.get_messages(ending_index=ending_index)
        self.messages_validation(messages=messages)
        messages = self.filter_messages(messages=messages)
        if messages[-1].sender == RoleType.SYSTEM:
            return

        available_tools = self.get_available_tools()
        anthropic_tools = cast(
            Union[
                Iterable[ToolParam],
                anthropic.NotGiven,
            ],
            (
                [
                    convert_to_anthropic_tool(name, tool)
                    for name, tool in available_tools.items()
                ]
                if messages[-1].sender == RoleType.USER
                or messages[-1].sender == RoleType.EXECUTION_ENVIRONMENT
                else anthropic.NOT_GIVEN
            ),
        )
        message_collection = to_anthropic_message_collection(messages=messages)
        response = self.model_inference(
            anthropic_messages=message_collection.messages,
            system=message_collection.system_prompt,
            anthropic_tools=anthropic_tools,
        )

        available_tool_names = set(available_tools.keys())
        agent_to_execution_tool_name = (
            get_current_context().get_agent_to_execution_facing_tool_name()
        )
        response_messages = response_to_messages(
            response,
            sender=self.role_type,
            available_tool_names=available_tool_names,
            agent_to_execution_facing_tool_name=agent_to_execution_tool_name,
        )
        self.add_messages(response_messages)

    @retry(
        wait=wait_random_exponential(multiplier=1, max=40),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(HTTPError),
    )
    def model_inference(
        self,
        anthropic_messages: list[MessageParam],
        system: Union[str, anthropic.NotGiven],
        anthropic_tools: Union[Iterable[ToolParam], anthropic.NotGiven],
    ) -> ResponseMessage:
        """Call Anthropic's native tools API via the public endpoint."""
        LOGGER.debug("Anthropic agent processes these messages: %s", anthropic_messages)

        create_kwargs: dict[str, Any] = {
            "model": self.model_name,
            "system": system,
            "messages": anthropic_messages,
            "tools": anthropic_tools,
            "max_tokens": 1024,
        }
        if self.thinking_budget_tokens is not None:
            # Extended thinking on Claude 4.x. Anthropic requires temperature=1
            # when thinking is enabled.
            create_kwargs["thinking"] = {
                "type": "enabled",
                "budget_tokens": self.thinking_budget_tokens,
            }
            create_kwargs["temperature"] = 1
        else:
            create_kwargs["temperature"] = 0

        response = messages_create(self.client, **create_kwargs)
        assert isinstance(response, ResponseMessage)
        return response


class AnthropicAPIThinkingAgent(AnthropicAPIAgent):
    """Anthropic agent variant with extended thinking enabled.

    Subclasses should set ``model_name`` to a Claude 4.x model that supports
    thinking (e.g. ``claude-opus-4-5-20251101``).
    """

    thinking_budget_tokens = 1024


# A high-level summary of the Claude 3 model family from
# https://docs.anthropic.com/claude/docs/models-overview#claude-3-a-new-generation-of-ai :
# - Opus:   Our most powerful model
# - Sonnet: Balanced between intelligence and speed
# - Haiku:  Fastest and most compact model


class ClaudeOpusAgent(AnthropicAPIAgent):
    model_name = "claude-3-opus-20240229"


class ClaudeSonnetAgent(AnthropicAPIAgent):
    model_name = "claude-3-sonnet-20240229"


class ClaudeHaikuAgent(AnthropicAPIAgent):
    model_name = "claude-3-haiku-20240307"


class Claude_3_5_Sonnet_Agent(AnthropicAPIAgent):
    model_name = "claude-3-5-sonnet-20241022"


class Claude_4_5_Opus_Agent(AnthropicAPIAgent):
    model_name = "claude-opus-4-5-20251101"  # Claude Opus 4.5


class Claude_4_5_Haiku_Agent(AnthropicAPIAgent):
    model_name = "claude-haiku-4-5-20251001"  # Claude Haiku 4.5


class Claude_4_5_Opus_Thinking_Agent(AnthropicAPIThinkingAgent):
    model_name = "claude-opus-4-5-20251101"


class Claude_4_5_Haiku_Thinking_Agent(AnthropicAPIThinkingAgent):
    model_name = "claude-haiku-4-5-20251001"


# Newer Claude 4.6/4.7/4.8/Sonnet-5 models. ``model_name`` is the public
# ``api.anthropic.com`` model id.


class Claude_4_6_V1_Opus_Agent(AnthropicAPIAgent):
    model_name = "claude-opus-4-6-v1"


class Claude_4_6_Sonnet_Agent(AnthropicAPIAgent):
    model_name = "claude-sonnet-4-6"


class Claude_4_7_Opus_Agent(AnthropicAPIAgent):
    model_name = "claude-opus-4-7"


class Claude_4_8_Opus_Agent(AnthropicAPIAgent):
    model_name = "claude-opus-4-8"


class Claude_Sonnet_5_Agent(AnthropicAPIAgent):
    model_name = "claude-sonnet-5"


# Thinking variants for the new models.


class Claude_4_6_V1_Opus_Thinking_Agent(AnthropicAPIThinkingAgent):
    model_name = "claude-opus-4-6-v1"


class Claude_4_6_Sonnet_Thinking_Agent(AnthropicAPIThinkingAgent):
    model_name = "claude-sonnet-4-6"


class Claude_4_7_Opus_Thinking_Agent(AnthropicAPIThinkingAgent):
    model_name = "claude-opus-4-7"


class Claude_4_8_Opus_Thinking_Agent(AnthropicAPIThinkingAgent):
    model_name = "claude-opus-4-8"


class Claude_Sonnet_5_Thinking_Agent(AnthropicAPIThinkingAgent):
    model_name = "claude-sonnet-5"
