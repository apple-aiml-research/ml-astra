# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Unit tests for astra_tool_sandbox.roles.cli_role"""

import json
from typing import Any, Iterator

import pytest

from astra_tool_sandbox.common.execution_context import (
    ExecutionContext,
    RoleType,
    get_current_context,
    new_context,
)
from astra_tool_sandbox.common.message_conversion import Message, to_openai_messages
from astra_tool_sandbox.roles.cli_role import CliAgent
from astra_tool_sandbox.roles.execution_environment import ExecutionEnvironment


@pytest.fixture(scope="function", autouse=True)
def execution_context() -> Iterator[None]:
    with new_context(ExecutionContext()):
        get_current_context().tool_allow_list = ["search_contacts"]
        CliAgent.add_messages(
            [
                Message(
                    sender=RoleType.USER,
                    recipient=RoleType.AGENT,
                    content="Find Paul's contact.",
                )
            ]
        )
        yield


def _agent_tool_call(monkeypatch: pytest.MonkeyPatch, *typed: str) -> Any:
    """Feed `typed` to a CliAgent turn, execute the call, and return the
    serialized OpenAI tool call."""
    inputs = iter(typed)
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))
    CliAgent().respond()
    ExecutionEnvironment().respond()
    openai_messages, _ = to_openai_messages(CliAgent.get_messages())
    (tool_call,) = openai_messages[-2]["tool_calls"]
    assert openai_messages[-1]["role"] == "tool"
    assert openai_messages[-1]["tool_call_id"] == tool_call["id"]
    return tool_call


def test_cli_agent_tool_call_serializes(monkeypatch: pytest.MonkeyPatch) -> None:
    tool_call = _agent_tool_call(
        monkeypatch, "tool", "search_contacts(contact_name='Paul')"
    )
    assert tool_call["function"]["name"] == "search_contacts"
    assert json.loads(tool_call["function"]["arguments"]) == {"contact_name": "Paul"}


def test_cli_agent_tool_call_binds_positional_args(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tool_call = _agent_tool_call(monkeypatch, "tool", "search_contacts('person-1')")
    assert json.loads(tool_call["function"]["arguments"]) == {"person_id": "person-1"}


def test_cli_agent_reprompts_on_unparseable_tool_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tool_call = _agent_tool_call(
        monkeypatch,
        "tool",
        "search_contacts(contact_name='Paul'",
        "search_contacts(contact_name=Paul)",
        "search_contacts(contact_name='Paul')",
    )
    assert json.loads(tool_call["function"]["arguments"]) == {"contact_name": "Paul"}
