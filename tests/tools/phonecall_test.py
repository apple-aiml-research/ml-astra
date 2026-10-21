# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Unit tests for astra_tool_sandbox.tools.phone_call"""

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
from astra_tool_sandbox.common.scenario import (
    filter_contexts_by_reference_time,
)
from astra_tool_sandbox.common.utils import load_str_time_to_datetime_iso_8601
from astra_tool_sandbox.scenarios.astra_v1.load_astra_v1_entities import (
    astra_v1_to_contact,
    astra_v1_to_phonecall,
    convert_empty_values_to_none,
)
from astra_tool_sandbox.tools.phone_call import (
    create_outgoing_call,
    search_phonecall_logs,
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
            "cell": "+86 123-456-7890-1234",
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
            "cell": "+1 555-789-0123-4567",
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
    # return cast(str, load_str_time_to_datetime_iso_8601("2024-12-01T20:10:00"))


@pytest.fixture()
def is_read_time() -> str:
    return cast(str, load_str_time_to_datetime_iso_8601("2024-12-08T09:16:00"))


@pytest.fixture()
def new_phonecall_jsons() -> List[Dict[str, Any]]:
    """Provide test calendar events

    Returns:
        Rows of new calendar events
    """
    phonecall_jsons = [
        {
            "call_type": "incoming",
            "caller": "+1 555-678-9012-3456",
            "receiver": "+1 555-123-4567-8901",
            "creation_time": "2024-12-03T07:00:00",
            "duration": "5 minutes",
        },
        {
            "call_type": "incoming",
            "caller": "+86 123-456-7890-1234",
            "receiver": "+1 555-123-4567-8901",
            "creation_time": "2024-12-03T20:00:00",
            "duration": "30 minutes",
        },
        {
            "call_type": "incoming",
            "caller": "+1 555-789-0123-4567",
            "receiver": "+1 555-123-4567-8901",
            "creation_time": "2024-12-06T10:00:00",
            "duration": "5 minutes",
        },
    ]
    return phonecall_jsons


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
    new_phonecall_jsons: list[dict[str, Any]],
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
    new_phonecalls = [
        astra_v1_to_phonecall(
            **convert_empty_values_to_none(phonecall_json), contact_db=contact_db
        )
        for phonecall_json in new_phonecall_jsons
    ]

    phonecall_db_updated = filter_contexts_by_reference_time(
        dataframe=pl.DataFrame(new_phonecalls),
        reference_time=reference_time,
    )
    test_context.add_to_database(
        namespace=DatabaseNamespace.PHONE,
        rows=phonecall_db_updated.to_dicts(),
    )
    with new_context(test_context):
        yield


def test_create_outgoing_call(reference_time: str, contact_db: pl.DataFrame) -> None:
    create_outgoing_call(
        receiver_address="+86 123-456-7890-1234", creation_datetime_iso=reference_time
    )
    current_context = get_current_context()
    phonecall_database = current_context.get_database(namespace=DatabaseNamespace.PHONE)
    assert (
        phonecall_database["caller_id"][-1]
        == contact_db.filter(pl.col("is_self"))[0, "person_id"]
    )
    assert (
        phonecall_database["receiver_id"][-1]
        == f"contact-{uuid.uuid5(namespace=uuid.NAMESPACE_URL, name='yuting')}"
    )
    with pytest.raises(ValueError):
        create_outgoing_call(
            receiver_address="Yuting Tao", creation_datetime_iso=reference_time
        )

    assert phonecall_database.shape[0] == 4


def test_create_outgoing_call_empty_databse(
    reference_time: str, contact_db: pl.DataFrame
) -> None:
    current_context = get_current_context()


def test_search_phonecall_logs(new_phonecall_jsons: list[dict[str, Any]]) -> None:
    # Exact matching uuid
    assert 2 == len(
        search_phonecall_logs(
            duration_in_hms_lowerbound="00:04:00", duration_in_hms_upperbound="00:06:00"
        )
    )

    assert (
        new_phonecall_jsons[1]["caller"]
        == search_phonecall_logs(
            caller_id=f"contact-{uuid.uuid5(namespace=uuid.NAMESPACE_URL, name='yuting')}"
        )[0]["caller_address"]
    )
