# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Unit tests for astra_tool_sandbox.roles.execution_environment"""

import json
import textwrap
from typing import Iterator, Optional

import pytest

from astra_tool_sandbox.common.execution_context import (
    DatabaseNamespace,
    ExecutionContext,
    RoleType,
    get_current_context,
    new_context,
)
from astra_tool_sandbox.common.message_conversion import Message
from astra_tool_sandbox.common.utils import deterministic_uuid
from astra_tool_sandbox.roles.execution_environment import ExecutionEnvironment


@pytest.fixture(scope="function", autouse=True)
def execution_context() -> Iterator[None]:
    """Autouse fixture which will setup and teardown execution context before and after each test function

    Returns:

    """
    with new_context(ExecutionContext()):
        yield


@pytest.fixture
def execution_environment() -> ExecutionEnvironment:
    """Execution environment object used for testing

    Returns:
        An execution environment object
    """
    return ExecutionEnvironment()


def test_execution_environment_syntax_error(
    execution_environment: ExecutionEnvironment,
) -> None:
    execution_environment.add_messages(
        [
            Message(
                sender=RoleType.AGENT,
                recipient=RoleType.EXECUTION_ENVIRONMENT,
                content="improt math",
            )
        ]
    )
    execution_environment.respond()
    last_message = execution_environment.get_messages()[-1]
    # The exact rendering of a SyntaxError differs across supported Python
    # versions: 3.11+ (PEP 657, fine-grained error locations) widens the caret
    # underline from a single "^" to span the whole offending token (e.g.
    # "^^^^"). Assert on the stable parts of the captured error rather than
    # matching the interpreter's output verbatim, so the test holds on 3.9-3.12.
    assert last_message.sender == RoleType.EXECUTION_ENVIRONMENT
    assert last_message.recipient == RoleType.AGENT
    assert last_message.conversation_active is True
    assert last_message.content is not None
    assert 'File "<input>", line 1' in last_message.content
    assert "improt math" in last_message.content
    assert "SyntaxError: invalid syntax" in last_message.content
    # The captured exception text is surfaced back to the agent verbatim.
    assert last_message.tool_call_exception == last_message.content


def test_execution_environment_raise_error(
    execution_environment: ExecutionEnvironment,
) -> None:
    execution_environment.add_messages(
        [
            Message(
                sender=RoleType.AGENT,
                recipient=RoleType.EXECUTION_ENVIRONMENT,
                content='raise ValueError("This is a test error")',
            )
        ]
    )
    execution_environment.respond()
    content = "ValueError: This is a test error"
    assert execution_environment.get_messages()[-1] == Message(
        sender=RoleType.EXECUTION_ENVIRONMENT,
        recipient=RoleType.AGENT,
        content=content,
        conversation_active=True,
        tool_call_exception=content,
    )


def test_execution_environment_incomplete_command(
    execution_environment: ExecutionEnvironment,
) -> None:
    message = Message(
        sender=RoleType.AGENT,
        recipient=RoleType.EXECUTION_ENVIRONMENT,
        content="if True:",  # < incomplete code
    )
    execution_environment.add_messages([message])
    execution_environment.respond()
    content = (
        "Error: The given code was incomplete and could not be executed: "
        f"'{message.content}'"
    )
    assert execution_environment.get_messages()[-1] == Message(
        sender=RoleType.EXECUTION_ENVIRONMENT,
        recipient=RoleType.AGENT,
        content=content,
        conversation_active=True,
        tool_call_exception=content,
    )


def test_execution_environment_successful_execution(
    execution_environment: ExecutionEnvironment,
) -> None:
    execution_environment.add_messages(
        [
            Message(
                sender=RoleType.AGENT,
                recipient=RoleType.EXECUTION_ENVIRONMENT,
                content="a = 1\nb = 2\nc = a + b\nprint(c)",
            )
        ]
    )
    execution_environment.respond()
    content = "3"
    assert execution_environment.get_messages()[-1] == Message(
        sender=RoleType.EXECUTION_ENVIRONMENT,
        recipient=RoleType.AGENT,
        content=textwrap.dedent(content),
        conversation_active=True,
    )


def test_valid_parallel_tool_call(
    execution_environment: ExecutionEnvironment,
) -> None:
    # Set up the environment by adding a system message that specifies which tools to
    # import.
    execution_environment.add_messages(
        [
            Message(
                sender=RoleType.AGENT,
                recipient=RoleType.EXECUTION_ENVIRONMENT,
                content=(
                    "import json\n"
                    "from astra_tool_sandbox.tools.contact import search_contacts\n"
                ),
                conversation_active=True,
            )
        ]
    )
    execution_context = get_current_context()
    execution_context.add_to_database(
        DatabaseNamespace.CONTACT,
        rows=[
            {
                "person_id": deterministic_uuid(payload="Tomas Haake"),
                "full_name": "Tomas Haake",
                "phone_number": "+11233344455",
                "relationship": "self",
                "is_self": True,
            },
            {
                "person_id": deterministic_uuid(payload="Fredrik Thordendal"),
                "full_name": "Fredrik Thordendal",
                "phone_number": "+12453344098",
                "relationship": "friend",
                "is_self": False,
            },
        ],
    )
    execution_environment.respond()

    # Agents can issue parallel tool calls. The expectation is that these are
    # independent and can thus be executed in any order. This is true for the tool calls
    # defined below.
    execution_environment.add_messages(
        [
            Message(
                sender=RoleType.AGENT,
                recipient=RoleType.EXECUTION_ENVIRONMENT,
                content="call_ucWrTNIM4Prh1KlK77k1Zjeu_parameters = {'contact_name': 'Tomas Haake'}\ncall_ucWrTNIM4Prh1KlK77k1Zjeu_response = search_contacts(**call_ucWrTNIM4Prh1KlK77k1Zjeu_parameters)\nprint(repr(call_ucWrTNIM4Prh1KlK77k1Zjeu_response))",
                conversation_active=True,
                openai_tool_call_id="call_ucWrTNIM4Prh1KlK77k1Zjeu",
                openai_function_name="search_contacts",
            ),
            Message(
                sender=RoleType.AGENT,
                recipient=RoleType.EXECUTION_ENVIRONMENT,
                content="call_e60fwDpTW2yecfBg2BQPNy88_parameters = {'contact_name': 'Fredrik Thordendal'}\ncall_e60fwDpTW2yecfBg2BQPNy88_response = search_contacts(**call_e60fwDpTW2yecfBg2BQPNy88_parameters)\nprint(repr(call_e60fwDpTW2yecfBg2BQPNy88_response))",
                conversation_active=True,
                openai_tool_call_id="call_e60fwDpTW2yecfBg2BQPNy88",
                openai_function_name="search_contacts",
            ),
        ]
    )

    execution_environment.respond()

    # Without setting `get_all_history_snapshots` we only get the latest tool call back.
    df = get_current_context().get_database(
        DatabaseNamespace.SANDBOX, get_all_history_snapshots=True
    )
    assert RoleType.EXECUTION_ENVIRONMENT == df[-2]["sender"][0]
    assert RoleType.AGENT == df[-2]["recipient"][0]
    assert "search_contacts" == df[-2]["openai_function_name"][0]
    # If all possible orderings of the tool calls succeed then the response should match
    # the original requests.
    assert "Tomas Haake" in df[-2]["content"][0]

    assert RoleType.EXECUTION_ENVIRONMENT == df[-1]["sender"][0]
    assert RoleType.AGENT == df[-1]["recipient"][0]
    assert "search_contacts" == df[-1]["openai_function_name"][0]
    assert "Fredrik Thordendal" in df[-1]["content"][0]


def test_parallel_tool_call_answers_every_call_when_one_fails(
    execution_environment: ExecutionEnvironment,
) -> None:
    """Every tool call in a parallel batch must get a response, even when one raises.

    An assistant turn whose `tool_calls` are not all answered is an invalid conversation and
    providers reject it outright — observed as `RetryError[BadRequestError]` (Vertex 400,
    deterministic across all 3 retries) on JOHN_QUINN_19, which issued 4 parallel
    `search_calendar_events` calls and got back only 3 results.

    The trigger is subtle: a raising tool records no trace of its own, but the code reads
    `tool_trace` off the newest SANDBOX row, which by then is the *previous* sibling's response
    message and still carries that sibling's trace. So the failing call looks like
    "traces collected but no response" and used to hit a branch that emitted one placeholder
    and returned, abandoning the rest of the batch.
    """
    execution_environment.add_messages(
        [
            Message(
                sender=RoleType.AGENT,
                recipient=RoleType.EXECUTION_ENVIRONMENT,
                content=(
                    "import json\n"
                    "from astra_tool_sandbox.tools.contact import search_contacts\n"
                ),
                conversation_active=True,
            )
        ]
    )
    get_current_context().add_to_database(
        DatabaseNamespace.CONTACT,
        rows=[
            {
                "person_id": deterministic_uuid(payload="Tomas Haake"),
                "full_name": "Tomas Haake",
                "phone_number": "+11233344455",
                "relationship": "self",
                "is_self": True,
            }
        ],
    )
    # Every real scenario runs with tracing on (`base_scenario.py:52`), and the bug only
    # manifests when a trace exists to leak between siblings.
    get_current_context().trace_tool = True
    execution_environment.respond()

    # Three parallel calls: the first succeeds (and so records a tool trace), the second
    # raises, the third would previously never be answered at all.
    execution_environment.add_messages(
        [
            Message(
                sender=RoleType.AGENT,
                recipient=RoleType.EXECUTION_ENVIRONMENT,
                content="call_ok1_response = search_contacts(**{'contact_name': 'Tomas Haake'})\nprint(repr(call_ok1_response))",
                conversation_active=True,
                openai_tool_call_id="call_ok1",
                openai_function_name="search_contacts",
            ),
            Message(
                sender=RoleType.AGENT,
                recipient=RoleType.EXECUTION_ENVIRONMENT,
                # No search criteria -> ValueError.
                content="call_bad_response = search_contacts(**{})\nprint(repr(call_bad_response))",
                conversation_active=True,
                openai_tool_call_id="call_bad",
                openai_function_name="search_contacts",
            ),
            Message(
                sender=RoleType.AGENT,
                recipient=RoleType.EXECUTION_ENVIRONMENT,
                content="call_ok2_response = search_contacts(**{'contact_name': 'Tomas Haake'})\nprint(repr(call_ok2_response))",
                conversation_active=True,
                openai_tool_call_id="call_ok2",
                openai_function_name="search_contacts",
            ),
        ]
    )
    execution_environment.respond()

    df = get_current_context().get_database(
        DatabaseNamespace.SANDBOX, get_all_history_snapshots=True
    )
    answered = [
        df[i]["openai_tool_call_id"][0]
        for i in range(len(df))
        if df[i]["sender"][0] == RoleType.EXECUTION_ENVIRONMENT
        and df[i]["recipient"][0] == RoleType.AGENT
        # Skip the response to the import message, which carries no tool call id.
        and df[i]["openai_tool_call_id"][0] is not None
    ]
    assert ["call_ok1", "call_bad", "call_ok2"] == answered

    # The agent must see the real error, not a placeholder, or it cannot self-correct the way
    # it does from a NameError.
    bad = next(
        df[i]
        for i in range(len(df))
        if df[i]["sender"][0] == RoleType.EXECUTION_ENVIRONMENT
        and df[i]["openai_tool_call_id"][0] == "call_bad"
    )
    assert "ValueError" in bad["content"][0]
    assert "in order to search for a contact" in bad["content"][0]
    assert bad["tool_call_exception"][0] is not None


def _setup_traced_contacts(execution_environment: ExecutionEnvironment) -> None:
    """Import `search_contacts`, add two contacts and turn tool tracing on."""
    execution_environment.add_messages(
        [
            Message(
                sender=RoleType.AGENT,
                recipient=RoleType.EXECUTION_ENVIRONMENT,
                content="from astra_tool_sandbox.tools.contact import search_contacts\n",
                conversation_active=True,
            )
        ]
    )
    get_current_context().add_to_database(
        DatabaseNamespace.CONTACT,
        rows=[
            {
                "person_id": deterministic_uuid(payload="Tomas Haake"),
                "full_name": "Tomas Haake",
                "phone_number": "+11233344455",
                "relationship": "self",
                "is_self": True,
            },
            {
                "person_id": deterministic_uuid(payload="Fredrik Thordendal"),
                "full_name": "Fredrik Thordendal",
                "phone_number": "+12453344098",
                "relationship": "friend",
                "is_self": False,
            },
        ],
    )
    get_current_context().trace_tool = True
    execution_environment.respond()


def _search_contacts_call(call_id: str, arguments: str) -> Message:
    return Message(
        sender=RoleType.AGENT,
        recipient=RoleType.EXECUTION_ENVIRONMENT,
        content=f"{call_id}_response = search_contacts(**{arguments})\nprint(repr({call_id}_response))",
        conversation_active=True,
        openai_tool_call_id=call_id,
        openai_function_name="search_contacts",
    )


def _traced_contact_names_by_call_id() -> dict[str, Optional[list[str]]]:
    """Map each answered tool call id to the `contact_name` arguments in its response's trace."""
    df = get_current_context().get_database(
        DatabaseNamespace.SANDBOX, get_all_history_snapshots=True
    )
    result: dict[str, Optional[list[str]]] = {}
    for i in range(len(df)):
        if (
            df[i]["sender"][0] == RoleType.EXECUTION_ENVIRONMENT
            and df[i]["recipient"][0] == RoleType.AGENT
            and df[i]["openai_tool_call_id"][0] is not None
        ):
            trace = df[i]["tool_trace"][0]
            result[df[i]["openai_tool_call_id"][0]] = (
                None
                if trace is None
                else [
                    json.loads(t)["arguments"].get("contact_name", "<none>")
                    for t in trace.to_list()
                ]
            )
    return result


def test_parallel_tool_call_keeps_trace_when_last_call_fails(
    execution_environment: ExecutionEnvironment,
) -> None:
    """A successful call's trace must survive a later sibling raising.

    Seen on THEO_APPLESEED_9: `search_contacts(...)` and `search_messages()` were one batch,
    the second raised, and the first call's trace was discarded as "unrelated", so a
    `column_tool_trace_matches_tool_names` milestone on `search_contacts` never matched.
    """
    _setup_traced_contacts(execution_environment)
    execution_environment.add_messages(
        [
            _search_contacts_call("call_ok", "{'contact_name': 'Tomas Haake'}"),
            # No search criteria -> ValueError.
            _search_contacts_call("call_bad", "{}"),
        ]
    )
    execution_environment.respond()

    assert {
        "call_ok": ["Tomas Haake"],
        "call_bad": None,
    } == _traced_contact_names_by_call_id()


def test_parallel_tool_call_keeps_trace_when_middle_call_fails(
    execution_environment: ExecutionEnvironment,
) -> None:
    _setup_traced_contacts(execution_environment)
    execution_environment.add_messages(
        [
            _search_contacts_call("call_ok1", "{'contact_name': 'Tomas Haake'}"),
            _search_contacts_call("call_bad", "{}"),
            _search_contacts_call("call_ok2", "{'contact_name': 'Fredrik Thordendal'}"),
        ]
    )
    execution_environment.respond()

    assert {
        "call_ok1": ["Tomas Haake"],
        "call_bad": None,
        "call_ok2": ["Fredrik Thordendal"],
    } == _traced_contact_names_by_call_id()


def test_parallel_tool_call_all_succeed_trace_placement(
    execution_environment: ExecutionEnvironment,
) -> None:
    """Pin current behaviour: in an all-succeed batch every trace lands on the last response.

    Each call appends its trace to the newest SANDBOX row, which after the first response is
    that response; `respond` then moves the accumulated list onto the next response.
    """
    _setup_traced_contacts(execution_environment)
    execution_environment.add_messages(
        [
            _search_contacts_call("call_1", "{'contact_name': 'Tomas Haake'}"),
            _search_contacts_call("call_2", "{'contact_name': 'Fredrik Thordendal'}"),
        ]
    )
    execution_environment.respond()

    assert {
        "call_1": None,
        "call_2": ["Tomas Haake", "Fredrik Thordendal"],
    } == _traced_contact_names_by_call_id()
