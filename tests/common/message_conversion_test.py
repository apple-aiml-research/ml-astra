# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Unit tests for astra_tool_sandbox.roles.message_conversion"""

from typing import Any, Tuple

import pytest
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)

from astra_tool_sandbox.common.execution_context import RoleType
from astra_tool_sandbox.common.message_conversion import (
    Message,
    openai_tool_call_to_python_code,
    python_code_to_openai_tool_call,
    to_openai_messages,
)


@pytest.fixture
def python_code_and_openai_too_call() -> Tuple[str, ChatCompletionMessageToolCall]:
    """Contains test datapoint for OpenAI tool call and python code conversion

    Returns:
        A tuple of ChatCompletionMessageToolCall and corresponding python code
    """
    tool_id = "call_1293YXHD"
    name = "test"
    arguments = '{"a": 42}'
    return (
        "call_1293YXHD_parameters = {'a': 42}\n"
        "call_1293YXHD_response = test(**call_1293YXHD_parameters)\n"
        "print(repr(call_1293YXHD_response))"
    ), ChatCompletionMessageToolCall(
        id=tool_id,
        type="function",
        function=Function(name=name, arguments=arguments),
    )


def test_openai_tool_call_to_python_code(
    python_code_and_openai_too_call: Tuple[str, ChatCompletionMessageToolCall],
) -> None:
    python_code, tool_call = python_code_and_openai_too_call
    assert (
        openai_tool_call_to_python_code(
            tool_call, {"test"}, execution_facing_tool_name=None
        )
        == python_code
    )


def test_python_code_to_openai_tool_call(
    python_code_and_openai_too_call: Tuple[str, ChatCompletionMessageToolCall],
) -> None:
    python_code, tool_call = python_code_and_openai_too_call
    assert python_code_to_openai_tool_call(python_code, None) == tool_call


def test_message_construction() -> None:
    message = Message(sender="AGENT", recipient="USER", content="Hi")
    # Test sender recipient converter
    assert isinstance(message.sender, RoleType)
    assert isinstance(message.recipient, RoleType)
    # Test Message post init hook
    assert message.visible_to == [RoleType.AGENT, RoleType.USER]
    # Test visible_to converter
    message = Message(
        sender=RoleType.AGENT,
        recipient=RoleType.USER,
        content="Hi",
        visible_to=[RoleType.USER],
    )
    assert message.visible_to == [RoleType.USER]


# --- Regression: Vertex/Gemini tool_call.id sanitization -------


def test_openai_tool_call_to_python_code_sanitizes_hyphenated_id() -> None:
    """Some OpenAI-compat translators return
    ``function-call-<uuid>`` shaped ids, which are illegal Python identifiers.
    They must be sanitized (dash → underscore) in the generated code.
    """
    tool_call = ChatCompletionMessageToolCall(
        id="function-call-274e7d8f-9a16-4176-9fae-b4e447756f28",
        type="function",
        function=Function(name="test", arguments='{"a": 42}'),
    )
    code = openai_tool_call_to_python_code(
        tool_call, {"test"}, execution_facing_tool_name=None
    )
    # No hyphens in the Python identifiers.
    assert "-" not in code.split("_parameters")[0]
    # The sanitized stem is used consistently across the three references.
    stem = "function_call_274e7d8f_9a16_4176_9fae_b4e447756f28"
    assert code.count(stem) == 4  # _parameters, _response, tool call, print
    # And the generated code parses as valid Python.
    compile(code, "<test>", "exec")


def test_openai_tool_call_to_python_code_sanitizes_leading_digit_id() -> None:
    """Vertex sometimes emits short, digit-prefixed ids like ``3xa0lqg5``.
    Python identifiers can't start with a digit — the sanitizer must prefix
    an underscore.
    """
    tool_call = ChatCompletionMessageToolCall(
        id="3xa0lqg5",
        type="function",
        function=Function(name="test", arguments='{"a": 42}'),
    )
    code = openai_tool_call_to_python_code(
        tool_call, {"test"}, execution_facing_tool_name=None
    )
    stem = "_3xa0lqg5"
    assert code.count(stem) == 4
    compile(code, "<test>", "exec")


def test_tool_call_id_round_trip_matches_within_message_list() -> None:
    """When the agent's tool call and the paired tool response are converted
    back to OpenAI messages, the ``assistant.tool_calls[0].id`` must equal
    the ``tool.tool_call_id`` — otherwise the API rejects the request.

    Regression for the Vertex/Gemini case where the ID contains
    hyphens. We sanitize only inside
    the Python code identifier; the wire IDs restore the raw model-provided
    form via ``message.openai_tool_call_id`` so logs / provider-side traces
    show the original string.
    """
    raw_id = "function-call-274e7d8f-9a16-4176-9fae-b4e447756f28"
    tool_call = ChatCompletionMessageToolCall(
        id=raw_id,
        type="function",
        function=Function(name="test", arguments='{"a": 42}'),
    )
    code = openai_tool_call_to_python_code(
        tool_call, {"test"}, execution_facing_tool_name=None
    )
    messages = [
        # System prompt (required by to_openai_messages contract).
        Message(
            sender=RoleType.SYSTEM,
            recipient=RoleType.AGENT,
            content="you are helpful",
        ),
        # Kickoff user turn.
        Message(sender=RoleType.USER, recipient=RoleType.AGENT, content="hi"),
        # Agent tool call: content is the (sanitized) python code, but the
        # unsanitized raw id is preserved on the Message field.
        Message(
            sender=RoleType.AGENT,
            recipient=RoleType.EXECUTION_ENVIRONMENT,
            content=code,
            openai_tool_call_id=raw_id,
            openai_function_name="test",
        ),
        # Tool response.
        Message(
            sender=RoleType.EXECUTION_ENVIRONMENT,
            recipient=RoleType.AGENT,
            content="42",
            openai_tool_call_id=raw_id,
            openai_function_name="test",
        ),
    ]
    openai_messages, _ = to_openai_messages(messages)
    assistant = next(m for m in openai_messages if m.get("role") == "assistant")
    tool = next(m for m in openai_messages if m.get("role") == "tool")
    # Wire IDs match each other AND preserve the raw model-provided form.
    assert assistant["tool_calls"][0]["id"] == tool["tool_call_id"] == raw_id


# --- Unknown tool calls must be recoverable, not fatal -----------------------------
#
# Naming a tool outside the provided schema is a model error. Raising aborts the
# scenario, discarding every turn the agent already got right and leaving the LLM
# judge nothing to look at. These pin the alternative: failing code that the
# execution environment converts into an observation the agent can react to.

import code as _code  # noqa: E402
import json  # noqa: E402

from astra_tool_sandbox.common.message_conversion import (  # noqa: E402
    UNAVAILABLE_TOOL_SHIM,
    UNAVAILABLE_TOOL_SHIM_NAME,
)
from astra_tool_sandbox.roles.execution_environment import (  # noqa: E402
    respond_to_single_message,
)


def _tool_call(name: str, arguments: str = "{}") -> ChatCompletionMessageToolCall:
    return ChatCompletionMessageToolCall(
        id="call_abc",
        type="function",
        function=Function(name=name, arguments=arguments),
    )


def _console_with_shim(**namespace: Any) -> _code.InteractiveConsole:
    """A REPL seeded the way create_base_scenario seeds the real one."""
    console = _code.InteractiveConsole(locals=dict(namespace))
    console.runcode(compile(UNAVAILABLE_TOOL_SHIM, "<shim>", "exec"))
    return console


def _run(console: _code.InteractiveConsole, python_code: str) -> Message:
    response = respond_to_single_message(
        interactive_console=console,
        message=Message(
            sender=RoleType.AGENT,
            recipient=RoleType.EXECUTION_ENVIRONMENT,
            content=python_code,
            openai_tool_call_id="call_abc",
            openai_function_name="x",
        ),
        role_type=RoleType.EXECUTION_ENVIRONMENT,
    )
    assert response is not None
    return response


def test_unknown_tool_does_not_raise_and_routes_through_the_shim() -> None:
    code_str = openai_tool_call_to_python_code(
        _tool_call("search_notes"), {"search_emails"}, execution_facing_tool_name=None
    )
    assert UNAVAILABLE_TOOL_SHIM_NAME in code_str


def test_unknown_tool_code_round_trips_with_the_true_name_and_arguments() -> None:
    """The agent's next turn re-parses its own history; that must not break."""
    code_str = openai_tool_call_to_python_code(
        _tool_call("search_notes", '{"query": "x"}'),
        {"search_emails"},
        execution_facing_tool_name=None,
    )
    restored = python_code_to_openai_tool_call(code_str, "search_notes")
    assert restored.function.name == "search_notes"
    assert json.loads(restored.function.arguments) == {"query": "x"}


def test_disallowed_but_existing_tool_still_fails() -> None:
    """The regression that matters: every tool is in the REPL namespace regardless of
    the scenario's tool_allow_list, so a disallowed tool must not simply execute."""
    executed: list[Any] = []
    console = _console_with_shim(search_contacts=lambda **kw: executed.append(kw))

    response = _run(
        console,
        openai_tool_call_to_python_code(
            _tool_call("search_contacts"),
            {"search_emails"},
            execution_facing_tool_name=None,
        ),
    )

    assert executed == [], "a disallowed tool was executed — allow list not enforced"
    assert response.tool_call_exception is not None
    assert "search_contacts" in response.tool_call_exception


def test_unknown_tool_error_reaches_the_agent_with_the_available_list() -> None:
    response = _run(
        _console_with_shim(),
        openai_tool_call_to_python_code(
            _tool_call("search_notes"),
            {"search_emails", "get_all_emails"},
            execution_facing_tool_name=None,
        ),
    )
    assert response.recipient == RoleType.AGENT
    assert response.tool_call_exception is not None
    assert "search_notes" in response.tool_call_exception
    assert "search_emails" in response.tool_call_exception


def test_malformed_json_arguments_are_recoverable_too() -> None:
    response = _run(
        _console_with_shim(),
        openai_tool_call_to_python_code(
            _tool_call("search_emails", "{not json"),
            {"search_emails"},
            execution_facing_tool_name=None,
        ),
    )
    assert response.tool_call_exception is not None
    assert "search_emails" in response.tool_call_exception
