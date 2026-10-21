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
    astra_v1_to_whatsapp_messages,
    convert_empty_values_to_none,
)

# from astra_tool_sandbox.tools.messaging import get_all_messages, search_messages, send_message
from astra_tool_sandbox.tools.whatsapp_messaging import (
    get_all_whatsapp_messages,
    search_whatsapp_messages,
    send_whatsapp_message,
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
        "person_id": str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name="michelle")),
        "first_name": "Michelle",
        "last_name": "Barnes",
        "cell": "+1 555-012-3456-7890",
        "email": "michelle.barnes@orchardtech.com",
        "alias": "Michelle",
        "address": "123 Tech Lane, Orchard County, CA 94022, USA",
        "company": "Orchard Tech",
        "job_title": "Research Analyst",
        "is_self": False,
        "relationship": "Coworker",
        "birthday": "1990-06-25",
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
            "person_id": str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name="theo")),
            "first_name": "Theo",
            "last_name": "Appleseed",
            "cell": "+1 555-789-0123-4568",
            "email": "theo.appleseed@orchardtech.com",
            "alias": "Theo",
            "address": "123 Tech Lane, Orchard County, CA 94022, USA",
            "company": "Orchard Tech",
            "job_title": "Research Scientist",
            "is_self": False,
            "relationship": "Coworker",
            "birthday": "1985-12-20",
        },
        {
            "person_id": str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name="jess")),
            "first_name": "Jess",
            "last_name": "Zimmer",
            "cell": "+1 555-123-4567-8902",
            "email": "jess.zimmer@fintechstartup.com",
            "alias": "Jess",
            "address": "456 Fintech Drive, Orchard County, CA 94022, USA",
            "company": "Fintech Startup",
            "job_title": "Product Manager",
            "is_self": False,
            "relationship": "Girlfriend",
            "birthday": "1994-02-14",
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
    return cast(str, load_str_time_to_datetime_iso_8601("2024-12-15T20:10:00"))


@pytest.fixture()
def is_read_time() -> str:
    return cast(str, load_str_time_to_datetime_iso_8601("2024-12-15T09:16:00"))


@pytest.fixture()
def new_whatsapp_jsons() -> List[Dict[str, Any]]:
    """Provide test messages

    Returns:
        Rows of new messages
    """
    whatsapp_jsons = [
        {
            "sender": "+1 555-234-5678-9012",
            "sender_name": "Charles Wilde",
            "recipient": "dawei.shen@orchardtech.com",
            "recipient_name": "Dawei Shen",
            "group_name": "Theater Group",
            "message": "Hey Dawei, heads up, we need to adjust tonight's rehearsal schedule. Can we start at 7 PM instead?",
            "creation_time": "2024-12-08T17:50:00",
            "status": "",
        },
        {
            "sender": "dawei.shen@orchardtech.com",
            "sender_name": "Dawei Shen",
            "recipient": "+1 555-234-5678-9012",
            "recipient_name": "Charles Wilde",
            "group_name": "Theater Group",
            "message": "Got it, Charles. Updating our calendar now.",
            "creation_time": "2024-12-08T17:51:00",
            "status": "",
        },
        {
            "sender": "jess.zimmer@fintechstartup.com",
            "sender_name": "Jess Zimmer",
            "recipient": "dawei.shen@orchardtech.com",
            "recipient_name": "Dawei Shen",
            "group_name": "",
            "message": "Here are the tickets for our theater night! 🎭",
            "creation_time": "2024-12-05T17:05:00",
            "status": "",
        },
    ]
    return whatsapp_jsons


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
    new_whatsapp_jsons: list[dict[str, Optional[Union[float, str]]]],
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
    new_whatsapp_messages = astra_v1_to_whatsapp_messages(
        new_whatsapp_jsons,
        self_full_name=f"{self_contact['first_name']} {self_contact['last_name']}",
        self_email=self_contact["email"],
        self_phone_number=self_contact["phone_number"],
    )

    whatsapp_db_updated = label_and_filter_messages(
        message_db=pl.DataFrame(new_whatsapp_messages),
        self_person_identifier=contact_db.filter(pl.col("is_self"))[0, "full_name"],
        self_person_identifier_colname="sender_name",
        reference_time=reference_time,
        is_read_time=is_read_time,
    )
    test_context.add_to_database(
        namespace=DatabaseNamespace.WHATSAPP,
        rows=whatsapp_db_updated.to_dicts(),
    )
    with new_context(test_context):
        yield


def test_send_whatsapp_messages(
    new_contact: dict[str, str], self_contact: dict[str, Any], reference_time: str
) -> None:
    send_whatsapp_message(
        recipients=[new_contact["email"]],
        content="Test",
        creation_datetime_iso=reference_time,
    )
    current_context = get_current_context()
    whatsapp_database = current_context.get_database(
        namespace=DatabaseNamespace.WHATSAPP
    )
    assert whatsapp_database["sender_name"][-1] == self_contact["full_name"]
    assert new_contact["full_name"] in whatsapp_database["participants_names"][-1]
    assert whatsapp_database["content"][-1] == "Test"
    assert whatsapp_database["creation_datetime_iso"][-1] == reference_time
    assert whatsapp_database["status"][-1] == "sent"

    with pytest.raises(ValueError):
        send_whatsapp_message(
            recipients=["not existed"],
            content="Test",
            creation_datetime_iso=reference_time,
        )

    send_whatsapp_message(
        recipients=["Jess Zimmer"],
        content="like the rehearsal",
        creation_datetime_iso=reference_time,
    )
    current_context = get_current_context()
    whatsapp_database = current_context.get_database(
        namespace=DatabaseNamespace.WHATSAPP
    )
    assert whatsapp_database["content"][-1] == "like the rehearsal"
    assert whatsapp_database["conversation_name"][-1] == "Jess Zimmer"

    send_whatsapp_message(
        recipients=["Theo Appleseed"],
        content="test theo",
        creation_datetime_iso=reference_time,
    )
    current_context = get_current_context()
    whatsapp_database = current_context.get_database(
        namespace=DatabaseNamespace.WHATSAPP
    )
    assert whatsapp_database["conversation_name"][-1] == "Theo Appleseed"


def test_search_whatsapp_messages() -> None:
    assert 2 == len(search_whatsapp_messages(conversation_name="Charles Wilde"))


def test_get_all_whatsapp_messages() -> None:
    all_messages = get_all_whatsapp_messages()
    assert 3 == len(all_messages)


def test_phone_number_normalization_search() -> None:
    """Test that searching with different phone number formats finds the same messages."""
    # First, let's debug what's actually in the database
    all_messages = get_all_whatsapp_messages()
    print(f"Total messages in DB: {len(all_messages)}")
    if all_messages:
        for i, msg in enumerate(all_messages[:3]):
            print(
                f"Message {i+1}: sender='{msg.get('sender_address', 'N/A')}', content='{msg.get('content', 'N/A')[:50]}...'"
            )
    # Search using the exact format from test data - Charles Wilde's number
    results_exact = search_whatsapp_messages(sender_address="+1 555-234-5678-9012")
    print(f"Exact format search results: {len(results_exact)}")

    # Search using normalized format (digits only) - correct digit count
    results_normalized = search_whatsapp_messages(sender_address="155523456789012")
    print(f"Normalized format search results: {len(results_normalized)}")

    # Search using different formatting with same digits
    results_formatted = search_whatsapp_messages(sender_address="1(555) 234-5678-9012")
    print(f"Formatted search results: {len(results_formatted)}")
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
    results_exact = search_whatsapp_messages(
        participants_addresses=["+1 555-234-5678-9012"]
    )

    # Search using different format
    results_formatted = search_whatsapp_messages(
        participants_addresses=["155523456789012"]
    )

    # Should return same results
    assert len(results_exact) == len(results_formatted)
    assert len(results_exact) > 0

    exact_ids = {msg["message_id"] for msg in results_exact}
    formatted_ids = {msg["message_id"] for msg in results_formatted}
    assert exact_ids == formatted_ids


def test_phone_number_conversation_grouping() -> None:
    """Test that messages with different phone number formats get grouped into the same conversation."""
    # Send first message with exact format from test data
    msg1_id = send_whatsapp_message(
        recipients=["+1 555-234-5678-9012"],
        content="First message with exact format",
        creation_datetime_iso="2024-12-05T18:00:00-08:00",
    )

    # Send second message with different format to same person
    msg2_id = send_whatsapp_message(
        recipients=["155523456789012"],  # Different format, same number
        content="Second message with normalized format",
        creation_datetime_iso="2024-12-05T18:01:00-08:00",
    )

    # Get all messages to check conversation grouping
    all_messages = get_all_whatsapp_messages()

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
    results1 = search_whatsapp_messages(
        participants_addresses=["+1 555-234-5678-9012", "dawei.shen@orchardtech.com"]
    )

    # Search with phone number in different format but same email
    results2 = search_whatsapp_messages(
        participants_addresses=["155523456789012", "dawei.shen@orchardtech.com"]
    )

    # Should find the same messages
    assert len(results1) == len(results2)

    ids1 = {msg["message_id"] for msg in results1}
    ids2 = {msg["message_id"] for msg in results2}
    assert ids1 == ids2
