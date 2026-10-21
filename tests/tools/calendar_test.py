# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Unit tests for astra_tool_sandbox.tools.calendar"""

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
from astra_tool_sandbox.common.scenario import (
    filter_contexts_by_reference_time,
)
from astra_tool_sandbox.common.utils import load_str_time_to_datetime_iso_8601
from astra_tool_sandbox.scenarios.astra_v1.load_astra_v1_entities import (
    astra_v1_to_calendar_event,
    astra_v1_to_contact,
    convert_empty_values_to_none,
)
from astra_tool_sandbox.tools.calendar import (
    create_calendar_event,
    get_all_calendars,
    modify_calendar_event,
    remove_calendar_event,
    search_calendar_events,
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
        "person_id": f"contact-{str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name=__name__))}",
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
def new_contacts() -> List[Dict[str, str]]:
    """Provide test contact info for new person

    Returns:
        name, phone number and relationship for test contact
    """
    contact_jsons = [
        {
            "person_id": f"contact-{uuid.uuid5(namespace=uuid.NAMESPACE_URL, name='yuting')}",
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
        },
        {
            "person_id": f"contact-{uuid.uuid5(namespace=uuid.NAMESPACE_URL, name='vick')}",
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
            "person_id": f"contact-{uuid.uuid5(namespace=uuid.NAMESPACE_URL, name='lukas')}",
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
def new_calendar_json() -> Dict[str, Any]:
    return {
        "calendar_name": "personal",
        # "calendar_event_name": "Dinner with Lukas and Vick",
        "notes": "Dinner plans with Lukas and Vick at a local restaurant.",
        "location": "Local Restaurant, Orchard County, CA",
        "start_datetime_iso": "2024-12-14T19:00:00-8:00",
        "end_datetime_iso": "2024-12-14T21:00:00-8:00",
        "invitees": [
            "Dawei Shen",
            "Lukas Hürholz",
            "Vick Li",
            "theo.appleseed@tech.com",
        ],
        "reminder_time_ahead": "1 day",
    }


@pytest.fixture()
def new_calendar_jsons() -> List[Dict[str, Any]]:
    """Provide test calendar events

    Returns:
        Rows of new calendar events
    """
    calendar_jsons = [
        {
            "calendar_event_id": f"calendar-{uuid.uuid5(namespace=uuid.NAMESPACE_URL, name='event1')}",
            "calendar_name": "personal",
            "title": "Cycling Trip with Vick",
            "description": "Starting the day with a cycling trip at a local café in Napa Valley.",
            "location": "Local Café, Napa Valley, CA",
            "start_time": "2024-12-01T07:00:00",
            "end_time": "2024-12-01T10:00:00",
            "invitees": ["Dawei Shen", "Vick Li"],
            "reminder": "60 minutes",
            "organizer": "Dawei Shen",
            "meeting_url": "",
            "creation_time": "2024-11-30T12:00:00",
        },
        {
            "calendar_event_id": f"calendar-{uuid.uuid5(namespace=uuid.NAMESPACE_URL, name='event2')}",
            "calendar_name": "work",
            "title": "Discussion on Virtual Assistant Algorithm Updates",
            "description": "Meeting to discuss further updates on the virtual assistant algorithm based on the recent feedback.",
            "location": "Conference Room B, Orchard Tech, Orchard County, CA",
            "start_time": "2024-12-04T10:00:00",
            "end_time": "2024-12-04T11:00:00",
            "invitees": ["Dawei Shen", "Michelle Barnes", "Theo Appleseed"],
            "reminder": "30 minutes",
            "organizer": "Dawei Shen",
            "meeting_url": "",
            "creation_time": "2024-12-02T09:35:00",
        },
        {
            "calendar_event_id": f"calendar-{uuid.uuid5(namespace=uuid.NAMESPACE_URL, name='event3')}",
            "calendar_name": "work",
            "title": "Tech Panel Hosted by Jeff Bing",
            "description": "Attending a tech panel discussion hosted by Jeff Bing on upcoming trends in consumer electronics.",
            "location": "Tech Hub Conference Center, Orchard County, CA",
            "start_time": "2024-12-10T09:00:00",
            "end_time": "2024-12-10T11:00:00",
            "invitees": ["Dawei Shen"],
            "reminder": "1 day",
            "organizer": "Jeff Bing",
            "meeting_url": "",
            "creation_time": "2024-12-06T10:05:00",
        },
    ]
    return calendar_jsons


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
    new_contacts: List[Dict[str, Any]],
    new_calendar_jsons: list[dict[str, Any]],
    contact_db: pl.DataFrame,
    reference_time: str,
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
        rows=[self_contact] + new_contacts,
    )
    new_calendar_events = [
        astra_v1_to_calendar_event(
            **convert_empty_values_to_none(calendar_json), contact_db=contact_db
        )
        for calendar_json in new_calendar_jsons
    ]

    calendar_db_updated = filter_contexts_by_reference_time(
        dataframe=pl.DataFrame(new_calendar_events),
        reference_time=reference_time,
    )
    test_context.add_to_database(
        namespace=DatabaseNamespace.CALENDAR,
        rows=calendar_db_updated.to_dicts(),
    )
    with new_context(test_context):
        yield


def test_create_calendar_event(
    new_calendar_json: dict[str, str], reference_time: str, contact_db: pl.DataFrame
) -> None:
    create_calendar_event(**new_calendar_json, creation_datetime_iso=reference_time)
    current_context = get_current_context()
    calendar_database = current_context.get_database(
        namespace=DatabaseNamespace.CALENDAR
    )
    assert (
        calendar_database["organizer_id"][-1]
        == contact_db.filter(pl.col("is_self"))[0, "person_id"]
    )
    assert (
        f"contact-{uuid.uuid5(namespace=uuid.NAMESPACE_URL, name='lukas')}"
        in calendar_database["attendees_ids"][-1]
    )
    assert len(calendar_database["attendees_ids"][-1]) == 4
    assert len(calendar_database["attendees_names"][-1]) == 4
    assert "theo.appleseed@tech.com" in calendar_database["attendees_ids"][-1]
    assert calendar_database["creation_datetime_iso"][-1] == reference_time


def test_remove_calendar_event(new_calendar_jsons: list[dict[str, Any]]) -> None:
    # Failure
    with pytest.raises(NoDataError):
        remove_calendar_event(calendar_event_id=str("aaaaa"))
    # Success
    remove_calendar_event(calendar_event_id=new_calendar_jsons[0]["calendar_event_id"])
    remove_calendar_event(calendar_event_id=new_calendar_jsons[1]["calendar_event_id"])
    remove_calendar_event(calendar_event_id=new_calendar_jsons[2]["calendar_event_id"])

    current_context = get_current_context()
    contact_database = current_context.get_database(
        namespace=DatabaseNamespace.CALENDAR
    )
    assert contact_database.is_empty()


def test_modify_calendar(reference_time: str) -> None:
    calendar_event_id = (
        f"calendar-{uuid.uuid5(namespace=uuid.NAMESPACE_URL, name='event1')}"
    )
    current_context = get_current_context()

    modify_calendar_event(
        calendar_event_id=calendar_event_id,
        creation_datetime_iso=reference_time,
        calendar_event_name="Cycling Trip",
        organizer="Vick Li",
        notes="just relax",
    )
    assert (
        current_context.get_database(namespace=DatabaseNamespace.CALENDAR).filter(
            pl.col("calendar_event_id") == calendar_event_id
        )["calendar_event_name"][-1]
        == "Cycling Trip"
    )
    assert (
        len(
            current_context.get_database(namespace=DatabaseNamespace.CALENDAR).filter(
                pl.col("calendar_event_id") == calendar_event_id
            )["attendees_ids"][-1]
        )
        == 2
    )
    assert (
        current_context.get_database(namespace=DatabaseNamespace.CALENDAR).filter(
            pl.col("calendar_event_id") == calendar_event_id
        )["organizer_id"][-1]
        == f"contact-{uuid.uuid5(namespace=uuid.NAMESPACE_URL, name='vick')}"
    )
    with pytest.raises(ValueError):
        modify_calendar_event(
            calendar_event_id=calendar_event_id,
            creation_datetime_iso=reference_time,
            end_datetime_iso="2024-12-01T06:00:00-8:00",
        )
    with pytest.raises(NoDataError):
        modify_calendar_event(
            calendar_event_id="aaa",
            creation_datetime_iso=reference_time,
            end_datetime_iso="2024-12-01T09:00:00-8:00",
        )

    modify_calendar_event(
        calendar_event_id=calendar_event_id,
        creation_datetime_iso=reference_time,
        calendar_event_name="Cycling Trip",
        organizer=f"contact-{str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name=__name__))}",
        notes="just relax",
    )
    assert (
        current_context.get_database(namespace=DatabaseNamespace.CALENDAR).filter(
            pl.col("calendar_event_id") == calendar_event_id
        )["organizer_id"][-1]
        == f"contact-{str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name=__name__))}"
    )


def test_search_calendar_events(new_calendar_jsons: list[dict[str, Any]]) -> None:
    # Exact matching uuid
    assert (
        new_calendar_jsons[0]["title"]
        == search_calendar_events(
            calendar_event_id=f"calendar-{uuid.uuid5(namespace=uuid.NAMESPACE_URL, name='event1')}"
        )[0]["calendar_event_name"]
    )

    assert (
        new_calendar_jsons[0]["title"]
        == search_calendar_events(
            start_datetime_iso_lowerbound="2024-12-01T06:00:00-08:00",
            start_datetime_iso_upperbound="2024-12-01T08:00:00-08:00",
        )[0]["calendar_event_name"]
    )

    assert (
        new_calendar_jsons[0]["title"]
        == search_calendar_events(calendar_event_name="Cycling Trip")[0][
            "calendar_event_name"
        ]
    )


def test_search_calendar_by_keyword_substring() -> None:
    # Short keyword: "Tech" is a substring of "Tech Panel Hosted by Jeff Bing" but
    # WRatio@90 scales short queries below threshold and misses it today.
    results = search_calendar_events(calendar_event_name="Tech")
    names = [r["calendar_event_name"] for r in results]
    assert "Tech Panel Hosted by Jeff Bing" in names


def test_search_calendar_by_keyword_fuzzy_typo() -> None:
    results = search_calendar_events(calendar_event_name="Cyclng Trip")  # typo
    names = [r["calendar_event_name"] for r in results]
    assert "Cycling Trip with Vick" in names


def test_search_calendar_keyword_precision_guard() -> None:
    # A nonsense term must NOT match anything
    assert search_calendar_events(calendar_event_name="zzzqqxnothing") == []


def test_search_calendar_by_attendee_first_name() -> None:
    results = search_calendar_events(attendees=["Vick"])  # first name only
    names = [r["calendar_event_name"] for r in results]
    assert "Cycling Trip with Vick" in names


def test_search_calendar_by_attendee_full_name_still_works() -> None:
    results = search_calendar_events(attendees=["Vick Li"])
    names = [r["calendar_event_name"] for r in results]
    assert "Cycling Trip with Vick" in names


def test_search_calendar_attendee_precision_guard() -> None:
    assert search_calendar_events(attendees=["Zzznobody"]) == []


def test_get_all_messages() -> None:
    all_calendars = get_all_calendars()
    assert 3 == len(all_calendars)


def test_search_calendar_events_by_location_alone() -> None:
    results = search_calendar_events(location="Napa Valley")
    names = [r["calendar_event_name"] for r in results]
    assert "Cycling Trip with Vick" in names
    # Must actually filter, not fall through to "return everything".
    assert "Tech Panel Hosted by Jeff Bing" not in names


def test_search_calendar_events_by_reminder_time_ahead_alone() -> None:
    results = search_calendar_events(reminder_time_ahead="1 day")
    names = [r["calendar_event_name"] for r in results]
    assert ["Tech Panel Hosted by Jeff Bing"] == names


def test_search_calendar_events_by_meeting_url_alone(reference_time: str) -> None:
    create_calendar_event(
        creation_datetime_iso=reference_time,
        start_datetime_iso="2024-12-20T09:00:00-08:00",
        calendar_event_name="Remote Sync",
        meeting_url="https://example.com/j/12345",
    )
    results = search_calendar_events(meeting_url="https://example.com/j/12345")
    assert ["Remote Sync"] == [r["calendar_event_name"] for r in results]


def test_search_calendar_events_location_precision_guard() -> None:
    assert [] == search_calendar_events(location="zzzqqxnowhere")
