# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Unit tests for astra_tool_sandbox.tools.messaging"""

import uuid
from typing import Any, Dict, Iterator, List, Optional, Union, cast

import polars as pl
import pytest
from polars.exceptions import NoDataError

from astra_tool_sandbox.common.execution_context import (
    DatabaseNamespace,
    ExecutionContext,
    get_current_context,
    new_context,
)
from astra_tool_sandbox.common.scenario import label_and_filter_emails
from astra_tool_sandbox.common.utils import load_str_time_to_datetime_iso_8601
from astra_tool_sandbox.scenarios.astra_v1.load_astra_v1_entities import (
    astra_v1_to_contact,
    astra_v1_to_emails,
    convert_empty_values_to_none,
)

# from astra_tool_sandbox.tools.messaging import get_all_messages, search_messages, send_message
from astra_tool_sandbox.tools.email import (
    NotEditableError,
    get_all_emails,
    modify_draft_email,
    remove_email_or_thread,
    search_emails,
    send_email,
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
            "cell": "+1 555-789-0123-4567",
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
            "person_id": str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name="kevin")),
            "first_name": "Kevin",
            "last_name": "Chen",
            "cell": "+1 555-890-1234-5678",
            "email": "kevin.chen@orchardtech.com",
            "alias": "Kevin",
            "address": "123 Tech Lane, Orchard County, CA 94022, USA",
            "company": "Orchard Tech",
            "job_title": "Team Lead",
            "is_self": False,
            "relationship": "Coworker",
            "birthday": "1980-04-05",
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
def new_emails_jsons() -> List[Dict[str, Any]]:
    """Provide test messages

    Returns:
        Rows of new messages
    """
    emails_jsons = [
        {
            "subject": "Revised Draft for Virtual Assistant Algorithm",
            "sender": "michelle.barnes@orchardtech.com",
            "recipients": "dawei.shen@orchardtech.com",
            "cc": "theo.appleseed@orchardtech.com",
            "bcc": "",
            "creation_time": "2024-12-02T09:00:00",
            "body": "Hi Dawei, I've attached the revised draft for the virtual assistant algorithm. Please review and let us know your thoughts. Best, Michelle",
            "attachment": "Revised_Algorithm_Draft.pdf",
            "email_id": "email-0",
        },
        {
            "subject": "Re: Revised Draft for Virtual Assistant Algorithm",
            "sender": "theo.appleseed@orchardtech.com",
            "recipients": "dawei.shen@orchardtech.com, michelle.barnes@orchardtech.com",
            "cc": "",
            "bcc": "",
            "creation_time": "2024-12-02T09:15:00",
            "body": "Hi all, I suggest adding an additional improvement to the section on user interaction. I've noted this in the draft attached. Cheers, Theo",
            "attachment": "Revised_Algorithm_Draft_with_Comments.pdf",
        },
        {
            "subject": "Re: Revised Draft for Virtual Assistant Algorithm",
            "sender": "dawei.shen@orchardtech.com",
            "recipients": "michelle.barnes@orchardtech.com, theo.appleseed@orchardtech.com",
            "cc": "",
            "bcc": "",
            "creation_time": "2024-12-02T09:30:00",
            "body": "Thanks, Michelle and Theo. I've reviewed the draft and your comments. I approve the changes. Let's schedule a meeting for Wednesday to discuss further. Best, Dawei",
            "attachment": "",
        },
        {
            "subject": "Dataset Update for Machine Learning Model",
            "sender": "michelle.barnes@orchardtech.com",
            "recipients": "dawei.shen@orchardtech.com",
            "cc": "",
            "bcc": "",
            "creation_time": "2024-12-09T08:00:00",
            "body": "Hi Dawei,\n\nI hope this email finds you well. I am writing to share the latest updates on the dataset we've been working on for our machine-learning model. Attached you'll find the updated files along with a few key questions that we need to address:\n\n1. How do we intend to handle the increasing volume of unstructured data?\n2. Are there specific algorithms you suggest we explore for better accuracy?\n3. What are your thoughts on the timeline for the next phase of testing?\n\nLooking forward to discussing these during our team sync.\n\nBest regards,\nMichelle",
            "attachment": "Updated_Dataset_Questions.pdf",
        },
        {
            "subject": "Action Items from Team Review",
            "sender": "dawei.shen@orchardtech.com",
            "recipients": "michelle.barnes@orchardtech.com",
            "cc": "kevin.chen@orchardtech.com",
            "bcc": "",
            "creation_time": "2024-12-13T10:05:00",
            "body": "Hi Michelle, Following our team review today, I'm assigning you the task of analyzing the latest data trends for our upcoming project. Please prepare a detailed report by next Friday. Let me know if you need any specific data sets or further clarifications. Best, Dawei",
            "attachment": "",
        },
        {
            "subject": "Action Items from Team Review",
            "sender": "dawei.shen@orchardtech.com",
            "recipients": "kevin.chen@orchardtech.com",
            "cc": "michelle.barnes@orchardtech.com",
            "bcc": "",
            "creation_time": "2024-12-13T10:10:00",
            "body": "Hi Kevin, As discussed in today's review, please schedule a time next week to go over the development needs for the new features we're planning to implement. I would like to ensure we're on track with the project timeline. Regards, Dawei",
            "attachment": "",
        },
        {
            "subject": "Re: Action Items from Team Review",
            "sender": "michelle.barnes@orchardtech.com",
            "recipients": "dawei.shen@orchardtech.com",
            "cc": "kevin.chen@orchardtech.com",
            "bcc": "",
            "creation_time": "2024-12-13T10:15:00",
            "body": "Hello Dawei, I've received the action items and will start working on the data analysis report. I'll reach out if I need any additional data. Thanks, Michelle",
            "attachment": "",
        },
    ]
    return emails_jsons


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
    new_emails_jsons: list[dict[str, Optional[Union[float, str]]]],
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
    new_emails = astra_v1_to_emails(
        [convert_empty_values_to_none(email_json) for email_json in new_emails_jsons],
        contact_db=contact_db,
    )

    email_db_updated = label_and_filter_emails(
        email_db=pl.DataFrame(new_emails),
        self_person_id=contact_db.filter(pl.col("is_self"))[0, "person_id"],
        reference_time=reference_time,
        is_read_time=is_read_time,
    )
    test_context.add_to_database(
        namespace=DatabaseNamespace.EMAIL,
        rows=email_db_updated.to_dicts(),
    )
    with new_context(test_context):
        yield


def test_send_email(
    new_contact: dict[str, str], self_contact: dict[str, Any], reference_time: str
) -> None:
    send_email(
        recipients_addresses=[new_contact["email"]],
        email_body="Test",
        creation_datetime_iso=reference_time,
    )
    current_context = get_current_context()
    email_database = current_context.get_database(namespace=DatabaseNamespace.EMAIL)
    assert email_database["sender_id"][-1] == self_contact["person_id"]
    assert new_contact["person_id"] in email_database["recipients_ids"][-1]
    assert email_database["body"][-1] == "Test"
    assert email_database["creation_datetime_iso"][-1] == reference_time
    assert email_database["status"][-1] == "draft"

    with pytest.raises(ValueError):
        send_email(
            recipients_addresses=[new_contact["email"]],
            email_id_referred="fake-id",
            email_body="Test",
            creation_datetime_iso=reference_time,
            email_id_referred_action="reply",
        )

    with pytest.raises(ValueError):
        send_email(
            recipients_addresses=[new_contact["email"]],
            email_body="Test",
            creation_datetime_iso=reference_time,
            email_id_referred_action="reply",
        )

    email_id_referred = email_database.filter(
        pl.col("subject") == "Dataset Update for Machine Learning Model"
    )[0, "email_id"]

    send_email(
        email_id_referred=email_id_referred,
        email_body="thanks",
        creation_datetime_iso=reference_time,
        email_action="send",
        email_id_referred_action="reply",
    )
    current_context = get_current_context()
    email_database = current_context.get_database(namespace=DatabaseNamespace.EMAIL)
    assert email_database["body"][-1] == "thanks"
    assert (
        email_database["subject"][-1] == "Re: Dataset Update for Machine Learning Model"
    )
    assert (
        "michelle.barnes@orchardtech.com" in email_database["recipients_addresses"][-1]
    )

    send_email(
        recipients_addresses=[new_contact["email"]],
        email_id_referred=email_id_referred,
        email_body="Test",
        creation_datetime_iso=reference_time,
        email_id_referred_action="forward",
    )
    current_context = get_current_context()
    email_database = current_context.get_database(namespace=DatabaseNamespace.EMAIL)
    assert (
        email_database["subject"][-1]
        == "Fwd: Dataset Update for Machine Learning Model"
    )
    assert "Begin forwarded message" in email_database["body"][-1]


def test_remove_email_or_thread() -> None:
    # Failure
    with pytest.raises(NoDataError):
        remove_email_or_thread(email_id=str("aaaaa"))
    with pytest.raises(NoDataError):
        remove_email_or_thread(email_thread_id=str("aaaaa"))
    # # Success
    remove_email_or_thread(email_id="email-0")
    # remove_calendar_event(calendar_event_id=new_calendar_jsons[1]["calendar_event_id"])
    # remove_calendar_event(calendar_event_id=new_calendar_jsons[2]["calendar_event_id"])

    # current_context = get_current_context()
    # contact_database = current_context.get_database(
    #     namespace=DatabaseNamespace.CALENDAR
    # )
    # assert contact_database.is_empty()


def test_modify_draft_email(
    new_contact: dict[str, str], reference_time: str, self_contact: dict[str, Any]
) -> None:
    send_email(
        recipients_addresses=[new_contact["email"]],
        email_body="Test",
        creation_datetime_iso=reference_time,
        email_action="draft",
    )

    current_context = get_current_context()
    email_database = current_context.get_database(namespace=DatabaseNamespace.EMAIL)
    email_id = email_database["email_id"][-1]
    # print(email_id)
    modify_draft_email(
        email_id=email_id,
        creation_datetime_iso=reference_time,
        recipients_addresses=[f"test-{new_contact['email']}"],
        subject="Discussion about algorithm",
    )

    current_context = get_current_context()
    email_database = current_context.get_database(namespace=DatabaseNamespace.EMAIL)
    assert email_database["subject"][-1] == "Discussion about algorithm"
    assert email_database["sender_id"][-1] == self_contact["person_id"]
    assert email_database["sender_address"][-1] == self_contact["email"]

    assert (
        email_database["recipients_ids"][-1][0] == [f'test-{new_contact["email"]}'][0]
    )

    # modify a read email
    email_id = email_database["email_id"][-2]
    with pytest.raises(NotEditableError):
        modify_draft_email(
            email_id=email_id,
            creation_datetime_iso=reference_time,
            subject="Discussion about algorithm",
        )


def test_send_draft_email(
    new_contact: dict[str, str], reference_time: str, self_contact: dict[str, Any]
) -> None:
    send_email(
        recipients_addresses=[new_contact["email"]],
        email_body="Test",
        creation_datetime_iso=reference_time,
        email_action="draft",
    )

    current_context = get_current_context()
    email_database = current_context.get_database(namespace=DatabaseNamespace.EMAIL)
    email_id = email_database["email_id"][-1]
    # print(email_id)
    send_email(
        draft_email_id_to_send=email_id,
        creation_datetime_iso=reference_time,
        email_action="send",
    )

    current_context = get_current_context()
    email_database = current_context.get_database(namespace=DatabaseNamespace.EMAIL)
    # assert email_database["subject"][-1] == "Discussion about algorithm"
    assert email_database["sender_id"][-1] == self_contact["person_id"]
    assert email_database["sender_address"][-1] == self_contact["email"]
    assert email_database["status"][-1] == "sent"
    assert email_database["email_id"][-1] == email_id

    assert (
        email_database["recipients_ids"][-1][0]
        == [f'{str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name="michelle"))}'][0]
    )

    # send a non-draft email
    email_id = email_database["email_id"][-2]
    with pytest.raises(NotEditableError):
        send_email(
            draft_email_id_to_send=email_id,
            creation_datetime_iso=reference_time,
            email_action="send",
        )


def test_search_emails() -> None:
    current_context = get_current_context()
    email_database = current_context.get_database(namespace=DatabaseNamespace.EMAIL)
    # print(email_database.to_dicts())
    # assert get_person_id_by_email_or_phonenumber("dawei.shen@orchardtech.com", contact_db) =="5efe1691-ae46-5fc1-b800-2185f21d5073"

    # assert safe_get_person_id("dawei.shen@orchardtech.com", contact_db) =="5efe1691-ae46-5fc1-b800-2185f21d5073"
    assert 3 == len(
        search_emails(sender_address="5efe1691-ae46-5fc1-b800-2185f21d5073")
    )
    assert 3 == len(search_emails(sender_address="dawei.shen@orchardtech.com"))

    assert 3 == len(search_emails(subject="Action Items from Team Review"))


def test_get_all_emails() -> None:
    all_emails = get_all_emails()
    assert 7 == len(all_emails)


def test_search_emails_accepts_scalar_recipient() -> None:
    # A single address (str) instead of a list must not TypeError and must behave
    # identically to a one-element list.
    addr = "dawei.shen@orchardtech.com"
    scalar = search_emails(recipients_addresses=addr)
    listed = search_emails(recipients_addresses=[addr])
    assert scalar == listed
    assert len(scalar) >= 1
