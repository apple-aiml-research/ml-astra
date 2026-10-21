# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Unit tests for astra_tool_sandbox.tools.messaging"""

import uuid
from typing import Any, Dict, Iterator, List, Optional, Union, cast

import polars as pl
import pytest

from astra_tool_sandbox.common.execution_context import (
    DatabaseNamespace,
    ExecutionContext,
    get_current_context,
    new_context,
)
from astra_tool_sandbox.common.scenario import label_and_filter_messages
from astra_tool_sandbox.common.utils import load_str_time_to_datetime_iso_8601
from astra_tool_sandbox.scenarios.astra_v1.load_astra_v1_entities import (
    astra_v1_to_contact,
    astra_v1_to_messages,
    convert_empty_values_to_none,
)
from astra_tool_sandbox.tools.messaging import (
    get_all_messages,
    remove_message_or_conversation,
    search_messages,
    send_message,
)


@pytest.fixture
def device_context() -> Dict[str, Any]:
    """Provide a test device info

    Returns:

    """
    return {
        "device_id": "my phone",
        "cellular": True,
        "wifi": True,
        "location_service": True,
        "low_battery_mode": False,
        "latitude": 37.334606,
        "longitude": -122.009102,
    }


@pytest.fixture
def self_contact() -> Dict[str, Any]:
    """Provide a test contact info for self

    Returns:

    """
    contact_json = {
        "person_id": str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name=__name__)),
        "first_name": "Dawei",
        "last_name": "Shen",
        "cell": "+1 555-123-4567-8901",
        "email": "dawei.shen@orchardtech.com",
        "alias": "Dawei",
        "address": "123 Tech Lane, Orchard County, CA 94022, USA",
        "company": "Orchard Tech",
        "job_title": "Data Science Manager",
        "is_self": True,
        "relationship": "Self",
        "birthday": "1994-05-14",
    }
    return astra_v1_to_contact(**convert_empty_values_to_none(contact_json))


@pytest.fixture
def new_contact() -> Dict[str, Any]:
    """Provide a test contact info for self

    Returns:

    """
    contact_json = {
        "person_id": str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name=__name__)),
        "first_name": "Yuting",
        "last_name": "Tao",
        "cell": "+86 234-567-8901-2345",
        "email": "yuting.tao@retired.cn",
        "alias": "Mom",
        "address": "88 Innovation Blvd, Shanghai, China",
        "company": "",
        "job_title": "",
        "is_self": False,
        "relationship": "Mother",
        "birthday": "1967-07-08",
    }
    return astra_v1_to_contact(**convert_empty_values_to_none(contact_json))


@pytest.fixture
def new_contacts() -> List[Dict[str, str]]:
    """Provide test contact info for new person

    Returns:
        name, phone number and relationship for test contact
    """
    contact_jsons = [
        {
            "person_id": str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name="vick")),
            "first_name": "Vick",
            "last_name": "Li",
            "cell": "+1 555-890-1234-5678",
            "email": "vick.li@techpals.com",
            "alias": "Vick",
            "address": "123 Tech Lane, Orchard County, CA 94022, USA",
            "company": "Tech Pals",
            "job_title": "Software Engineer",
            "is_self": False,
            "relationship": "College Friend",
            "birthday": "1994-07-22",
        },
        {
            "person_id": str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name="lukas")),
            "first_name": "Lukas",
            "last_name": "Hürholz",
            "cell": "+44 123-456-7890-1234",
            "email": "lukas.hurholz@londonbanking.co.uk",
            "alias": "Lukas",
            "address": "456 Finance St, London, UK",
            "company": "London Banking",
            "job_title": "Banker",
            "is_self": False,
            "relationship": "High School Friend",
            "birthday": "1994-12-31",
        },
        {
            "person_id": str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name="charles")),
            "first_name": "Charles",
            "last_name": "Wilde",
            "cell": "+1 555-234-5678-9012",
            "email": "charles.wilde@orchardtheater.com",
            "alias": "Charles",
            "address": "789 Culture St, Orchard County, CA 94022, USA",
            "company": "Orchard Theater",
            "job_title": "Actor",
            "is_self": False,
            "relationship": "Theater Friend",
            "birthday": "1988-08-08",
        },
    ]

    output_jsons = [
        astra_v1_to_contact(**convert_empty_values_to_none(json_))
        for json_ in contact_jsons
    ]
    # person_id = output_json.pop('person_id', None)
    # is_self = output_json.pop('is_self', None)
    return output_jsons


@pytest.fixture()
def reference_time() -> str:
    return cast(str, load_str_time_to_datetime_iso_8601("2024-12-08T20:10:00"))


@pytest.fixture()
def is_read_time() -> str:
    return cast(str, load_str_time_to_datetime_iso_8601("2024-12-08T09:16:00"))


@pytest.fixture()
def new_messages_jsons() -> List[Dict[str, Any]]:
    """Provide test messages

    Returns:
        Rows of new messages
    """
    messages_jsons = [
        {
            "conversation_name": "Vick Li",
            "participants": ["dawei.shen@orchardtech.com", "vick.li@techpals.com"],
            "messages": [
                {
                    "sender": "dawei.shen@orchardtech.com",
                    "sender_name": "Dawei Shen",
                    "content": "Hey Vick, just checking in for our cycling trip at Napa Valley. I'm on my way to the café now. See you there!",
                    "creation_time": "2024-12-01T06:00:00",
                    "status": "",
                },
                {
                    "sender": "vick.li@techpals.com",
                    "sender_name": "Vick Li",
                    "content": "Morning Dawei! Thanks for the heads up. I'll be there on time. Looking forward to it!",
                    "creation_time": "2024-12-01T06:05:00",
                    "status": "",
                },
            ],
        },
        {
            "conversation_name": "Lukas Hürholz",
            "participants": ["+1 555-123-4567-8901", "+44 123-456-7890-1234"],
            "messages": [
                {
                    "sender": "+44 123-456-7890-1234",
                    "sender_name": "Lukas Hürholz",
                    "content": "Hey Dawei, I'll be in California next weekend for work. Would love to catch up over dinner if you're free!",
                    "creation_time": "2024-12-08T09:00:00",
                    "status": "",
                },
                {
                    "sender": "+1 555-123-4567-8901",
                    "sender_name": "Dawei Shen",
                    "content": "Awesome, Lukas! How about dinner next Saturday? Vick will join us too.",
                    "creation_time": "2024-12-08T09:15:00",
                    "status": "",
                },
                {
                    "sender": "+44 123-456-7890-1234",
                    "sender_name": "Lukas Hürholz",
                    "content": "Perfect! See you both next Saturday.",
                    "creation_time": "2024-12-08T09:20:00",
                    "status": "",
                },
            ],
        },
        {
            "conversation_name": "Vick Li",
            "participants": ["+1 555-123-4567-8901", "+1 555-890-1234-5678"],
            "messages": [
                {
                    "sender": "+1 555-123-4567-8901",
                    "sender_name": "Dawei Shen",
                    "content": "Lukas will be in town next weekend. Thinking of setting up dinner plans. Are you in?",
                    "creation_time": "2024-12-08T09:05:00",
                    "status": "",
                },
                {
                    "sender": "+1 555-890-1234-5678",
                    "sender_name": "Vick Li",
                    "content": "Sounds great! Count me in. Let me know the details.",
                    "creation_time": "2024-12-08T09:10:00",
                    "status": "",
                },
            ],
        },
        {
            "conversation_name": "Local Dinner on Dec 14th",
            "conversation_id": str(
                uuid.uuid5(namespace=uuid.NAMESPACE_URL, name="dinner")
            ),
            "participants": [
                "+1 555-123-4567-8901",
                "+44 123-456-7890-1234",
                "+1 555-890-1234-5678",
            ],
            "messages": [
                {
                    "sender": "+44 123-456-7890-1234",
                    "sender_name": "Lukas Hürholz",
                    "content": "Hey all, very looking forward to our outing on 12/14.",
                    "creation_time": "2024-12-08T09:00:00",
                    "status": "",
                },
            ],
        },
        {
            "conversation_name": "Charles Wilde",
            "conversation_id": str(
                uuid.uuid5(namespace=uuid.NAMESPACE_URL, name="charlesconv")
            ),
            "participants": ["+1 555-123-4567-8901", "+1 555-234-5678-9012"],
            "messages": [
                {
                    "sender": "+1 555-234-5678-9012",
                    "sender_name": "Charles Wilde",
                    "content": "Hey Dawei, heads up, we need to adjust tonight's rehearsal schedule. Can we start at 7 PM instead?",
                    "creation_time": "2024-12-08T17:50:00",
                    "status": "",
                },
                {
                    "sender": "+1 555-123-4567-8901",
                    "sender_name": "Dawei Shen",
                    "content": "Got it, Charles. Updating our calendar now.",
                    "creation_time": "2024-12-08T17:51:00",
                    "status": "",
                },
            ],
        },
    ]
    return messages_jsons


@pytest.fixture()
def contact_db(
    self_contact: Dict[str, str],
    new_contacts: List[Dict[str, Optional[Union[float, str]]]],
) -> pl.DataFrame:
    contact_db = pl.DataFrame([self_contact] + new_contacts)
    return contact_db


@pytest.fixture(scope="function", autouse=True)
def execution_context(
    self_contact: dict[str, Any],
    device_context: dict[str, Any],
    new_contact: dict[str, Any],
    new_contacts: List[Dict[str, Any]],
    new_messages_jsons: list[dict[str, Optional[Union[float, str]]]],
    contact_db: pl.DataFrame,
    reference_time: str,
    is_read_time: str,
) -> Iterator[None]:
    """Autouse fixture which will setup and teardown execution context before and after each test function

    Returns:

    """
    # Set test context
    test_context = ExecutionContext()
    test_context.add_to_database(
        namespace=DatabaseNamespace.SETTING,
        rows=[device_context],
    )
    test_context.add_to_database(
        namespace=DatabaseNamespace.CONTACT,
        rows=[self_contact] + [new_contact] + new_contacts,
    )
    new_messages = astra_v1_to_messages(
        [
            convert_empty_values_to_none(messaging_json)
            for messaging_json in new_messages_jsons
        ],
        contact_db=contact_db,
    )

    message_db_updated = label_and_filter_messages(
        message_db=pl.DataFrame(new_messages),
        self_person_identifier=contact_db.filter(pl.col("is_self"))[0, "person_id"],
        self_person_identifier_colname="sender_person_id",
        reference_time=reference_time,
        is_read_time=is_read_time,
    )
    test_context.add_to_database(
        namespace=DatabaseNamespace.MESSAGING,
        rows=message_db_updated.to_dicts(),
    )
    with new_context(test_context):
        yield


def test_send_message(
    new_contact: dict[str, str], self_contact: dict[str, Any], reference_time: str
) -> None:
    send_message(
        recipients_addresses=[new_contact["phone_number"]],
        content="Test",
        creation_datetime_iso=reference_time,
    )
    current_context = get_current_context()
    messaging_database = current_context.get_database(
        namespace=DatabaseNamespace.MESSAGING
    )
    assert messaging_database["sender_person_id"][-1] == self_contact["person_id"]
    assert messaging_database["sender_address"][-1] == self_contact["phone_number"]
    assert messaging_database["conversation_name"][-1] == "Yuting Tao"
    assert new_contact["person_id"] in messaging_database["participants_ids"][-1]
    assert (
        new_contact["phone_number"] in messaging_database["participants_addresses"][-1]
    )
    assert self_contact["person_id"] in messaging_database["participants_ids"][-1]
    assert messaging_database["content"][-1] == "Test"
    assert messaging_database["creation_datetime_iso"][-1] == reference_time


def test_send_message_with_conversation_id(
    new_contact: dict[str, str], self_contact: dict[str, Any], reference_time: str
) -> None:
    send_message(
        conversation_id=str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name="dinner")),
        content="Test",
        creation_datetime_iso=reference_time,
    )
    current_context = get_current_context()
    messaging_database = current_context.get_database(
        namespace=DatabaseNamespace.MESSAGING
    )
    assert messaging_database["sender_person_id"][-1] == self_contact["person_id"]
    assert messaging_database["sender_address"][-1] == self_contact["phone_number"]
    assert messaging_database["conversation_name"][-1] == "Local Dinner on Dec 14th"
    assert len(messaging_database["participants_ids"][-1]) == 3


def test_search_messages(
    contact_db: pl.DataFrame,
    new_messages_jsons: list[dict[str, Optional[Union[float, str]]]],
) -> None:
    # new_messages = astra_v1_to_messages(
    #     [
    #         convert_empty_values_to_none(messaging_json)
    #         for messaging_json in new_messages_jsons
    #     ],
    #     contact_db=contact_db,
    # )
    assert 4 == len(search_messages(conversation_name="Vick Li"))
    assert 1 == len(search_messages(conversation_name="Lukas Hürholz", status="unread"))


def test_get_all_messages() -> None:
    all_messages = get_all_messages()
    assert 9 == len(
        all_messages
    )  # since Dawei's last message to Charles is after is_read_time which is impossible


def test_phone_number_normalization_search() -> None:
    """Test that searching with different phone number formats finds the same messages."""
    # Search using the exact format from test data - Charles Wilde's number
    results_exact = search_messages(sender_address="+1 555-234-5678-9012")

    # Search using normalized format (digits only) - correct digit count
    results_normalized = search_messages(sender_address="155523456789012")

    # Search using different formatting with same digits
    results_formatted = search_messages(sender_address="1(555) 234-5678-9012")

    # All should return the same results
    assert len(results_exact) == len(results_normalized) == len(results_formatted)
    assert len(results_exact) > 0  # Should find at least one message

    # Verify the content is the same
    exact_ids = {msg["message_id"] for msg in results_exact}
    normalized_ids = {msg["message_id"] for msg in results_normalized}
    formatted_ids = {msg["message_id"] for msg in results_formatted}

    assert exact_ids == normalized_ids == formatted_ids


def test_phone_number_normalization_participants_search() -> None:
    """Test that searching participants with different phone number formats works."""
    # Search using exact format
    results_exact = search_messages(participants_addresses=["+1 555-234-5678-9012"])

    # Search using different format
    results_formatted = search_messages(participants_addresses=["155523456789012"])

    # Should return same results
    assert len(results_exact) == len(results_formatted)
    assert len(results_exact) > 0

    exact_ids = {msg["message_id"] for msg in results_exact}
    formatted_ids = {msg["message_id"] for msg in results_formatted}
    assert exact_ids == formatted_ids


def test_search_messages_accepts_scalar_participant() -> None:
    # A scalar (str) for a list param must not TypeError and must behave like a
    # one-element list.
    scalar = search_messages(participants_ids="p1")
    assert isinstance(scalar, list)
    assert scalar == search_messages(participants_ids=["p1"])


def test_remove_message_only() -> None:
    """Removing by message_id deletes just that one message."""
    all_messages = get_all_messages()
    target = all_messages[0]

    remove_message_or_conversation(message_id=target["message_id"])

    remaining = get_all_messages()
    assert len(remaining) == len(all_messages) - 1
    assert target["message_id"] not in {msg["message_id"] for msg in remaining}


def test_remove_conversation_only() -> None:
    """Removing by conversation_id deletes every message in that thread."""
    all_messages = get_all_messages()
    conversation_id = all_messages[0]["conversation_id"]
    conversation_size = sum(
        1 for msg in all_messages if msg["conversation_id"] == conversation_id
    )
    assert conversation_size >= 2  # need a multi-message thread for a meaningful test

    remove_message_or_conversation(conversation_id=conversation_id)

    remaining = get_all_messages()
    assert len(remaining) == len(all_messages) - conversation_size
    assert conversation_id not in {msg["conversation_id"] for msg in remaining}


def test_remove_with_both_ids_removes_only_the_message() -> None:
    """Passing both conversation_id and message_id must delete only the single
    message, not wipe the whole conversation.

    Regression test: previously the conversation_id branch ran first and deleted
    the entire thread, then the message_id branch found no matching row and raised
    polars NoDataError -- crashing after a destructive full-conversation delete.
    """
    all_messages = get_all_messages()
    # Pick a message from a conversation that has more than one message so we can
    # verify the rest of the thread survives.
    conversation_sizes: Dict[str, int] = {}
    for msg in all_messages:
        conversation_sizes[msg["conversation_id"]] = (
            conversation_sizes.get(msg["conversation_id"], 0) + 1
        )
    target = next(
        msg for msg in all_messages if conversation_sizes[msg["conversation_id"]] >= 2
    )

    # Must not raise, and must delete only the targeted message.
    remove_message_or_conversation(
        conversation_id=target["conversation_id"],
        message_id=target["message_id"],
    )

    remaining = get_all_messages()
    assert len(remaining) == len(all_messages) - 1
    assert target["message_id"] not in {msg["message_id"] for msg in remaining}
    # The rest of the conversation is untouched.
    assert target["conversation_id"] in {msg["conversation_id"] for msg in remaining}


def test_remove_with_no_ids_raises() -> None:
    """At least one identifier is required."""
    with pytest.raises(ValueError):
        remove_message_or_conversation()


def test_phone_number_conversation_grouping() -> None:
    """Test that messages with different phone number formats get grouped into the same conversation."""
    # Send first message with exact format from test data
    msg1_id = send_message(
        recipients_addresses=["+1 555-234-5678-9012"],
        content="First message with exact format",
        creation_datetime_iso="2024-12-05T18:00:00-08:00",
    )

    # Send second message with different format to same person
    msg2_id = send_message(
        recipients_addresses=["155523456789012"],  # Different format, same number
        content="Second message with normalized format",
        creation_datetime_iso="2024-12-05T18:01:00-08:00",
    )

    # Get all messages to check conversation grouping
    all_messages = get_all_messages()

    # Find our test messages
    test_messages = [
        msg for msg in all_messages if msg["message_id"] in [msg1_id, msg2_id]
    ]
    assert len(test_messages) == 2

    # Both messages should have the same conversation_id (grouped together)
    conversation_ids = {msg["conversation_id"] for msg in test_messages}
    assert (
        len(conversation_ids) == 1
    ), f"Expected 1 conversation, got {len(conversation_ids)}: {conversation_ids}"

    # Both should have the same conversation_name (Charles Wilde)
    conversation_names = {msg["conversation_name"] for msg in test_messages}
    assert len(conversation_names) == 1
    assert "Charles Wilde" in list(conversation_names)[0]


def test_mixed_format_participant_search() -> None:
    """Test searching with mixed phone number and email formats in participants."""
    # Search with phone number in one format
    results1 = search_messages(
        participants_addresses=["+1 555-234-5678-9012", "dawei.shen@orchardtech.com"]
    )

    # Search with phone number in different format but same email
    results2 = search_messages(
        participants_addresses=["155523456789012", "dawei.shen@orchardtech.com"]
    )

    # Should find the same messages
    assert len(results1) == len(results2)

    ids1 = {msg["message_id"] for msg in results1}
    ids2 = {msg["message_id"] for msg in results2}
    assert ids1 == ids2
