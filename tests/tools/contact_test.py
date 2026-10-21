# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Unit tests for astra_tool_sandbox.tools.contact"""

import uuid
from typing import Any, Dict, Iterator

import polars as pl
import pytest
from polars.exceptions import DuplicateError, NoDataError

from astra_tool_sandbox.common.constants import GLOBAL_TIME_ISO
from astra_tool_sandbox.common.execution_context import (
    DatabaseNamespace,
    ExecutionContext,
    get_current_context,
    new_context,
)
from astra_tool_sandbox.scenarios.astra_v1.load_astra_v1_entities import (
    astra_v1_to_contact,
    convert_empty_values_to_none,
)
from astra_tool_sandbox.tools.contact import (
    add_contact,
    get_participants_id_by_name_or_phone_or_email,
    get_participants_person_id_or_name,
    lookup_contact_value,
    match_names_in_contact,
    modify_contact,
    remove_contact,
    search_contacts,
)


@pytest.fixture
def self_contact() -> Dict[str, Any]:
    """Provide a test contact info for self

    Returns:

    """
    theo_json = {
        "person_id": f"contacts-{uuid.uuid5(namespace=uuid.NAMESPACE_URL, name=__name__)}",
        "first_name": "Theo",
        "last_name": "Appleseed",
        "cell": "1234-5678-9101",
        "email": "theo.appleseed@example.com",
        "alias": "Theo",
        "address": "123 Orchard Lane, Orchard County, CA",
        "company": "Innovative Tech Solutions",
        "job_title": "Applied Researcher",
        "is_self": True,
        "relationship": "Self",
        "birthday": "1999-05-15",
    }
    return astra_v1_to_contact(**convert_empty_values_to_none(theo_json))


@pytest.fixture
def new_contact() -> Dict[str, str]:
    """Provide test contact info for new person

    Returns:
        name, phone number and relationship for test contact
    """
    theo_json = {
        "first_name": "John",
        "last_name": "Appleseed",
        "cell": "1234-5678-9102",
        "email": "john.appleseed@example.com",
        "alias": "Dad",
        "address": "321 Rural Route, Neighboring Town, CA",
        "company": "Nearby University",
        "job_title": "Professor of Theoretical Physics",
        "is_self": False,
        "relationship": "Father",
        "birthday": "1965-03-22",
        "creation_time": "2024-12-12",
    }

    output_json = astra_v1_to_contact(**convert_empty_values_to_none(theo_json))
    person_id = output_json.pop("person_id", None)
    is_self = output_json.pop("is_self", None)
    return output_json


@pytest.fixture(scope="function", autouse=True)
def execution_context(self_contact: dict[str, Any]) -> Iterator[None]:
    """Autouse fixture which will setup and teardown execution context before and after each test function

    Returns:

    """
    test_context = ExecutionContext()
    test_context.add_to_database(
        namespace=DatabaseNamespace.CONTACT, rows=[self_contact]
    )
    with new_context(test_context):
        yield


def test_add_contact(new_contact: dict[str, str]) -> None:
    add_contact(**new_contact)
    current_context = get_current_context()
    contact_database = current_context.get_database(namespace=DatabaseNamespace.CONTACT)
    for k, v in new_contact.items():
        if isinstance(v, str):
            assert contact_database[k][1].lower() == v.lower()
        else:
            assert contact_database[k][1] == v
    with pytest.raises(DuplicateError):
        add_contact(**new_contact, is_self=True)


def test_modify_contact(new_contact: dict[str, str]) -> None:
    current_context = get_current_context()
    person_id = f"contacts-{uuid.uuid5(namespace=uuid.NAMESPACE_URL, name='person_0')}"

    current_context.add_to_database(
        namespace=DatabaseNamespace.CONTACT,
        rows=[{**new_contact, "person_id": person_id, "is_self": False}],
    )
    modify_contact(
        person_id=person_id,
        first_name="Fred",
        phone_number="1123-4567-8901",
        relationship="coworker",
        creation_datetime_iso=GLOBAL_TIME_ISO,
    )
    assert (
        current_context.get_database(namespace=DatabaseNamespace.CONTACT)
        .filter(pl.col("person_id") == person_id)["first_name"][-1]
        .lower()
        == "fred"
    )
    assert (
        current_context.get_database(namespace=DatabaseNamespace.CONTACT).filter(
            pl.col("person_id") == person_id
        )["phone_number"][-1]
        == "1123-4567-8901"
    )
    assert (
        current_context.get_database(namespace=DatabaseNamespace.CONTACT).filter(
            pl.col("person_id") == person_id
        )["relationship"][-1]
        == "coworker"
    )
    with pytest.raises(ValueError):
        modify_contact(person_id=person_id, creation_datetime_iso=GLOBAL_TIME_ISO)
    with pytest.raises(NoDataError):
        modify_contact(
            person_id="fake id",
            first_name="Freddy",
            creation_datetime_iso=GLOBAL_TIME_ISO,
        )
    with pytest.raises(DuplicateError):
        modify_contact(
            person_id=person_id, is_self=True, creation_datetime_iso=GLOBAL_TIME_ISO
        )
    current_context.add_to_database(
        namespace=DatabaseNamespace.CONTACT,
        rows=[{**new_contact, "person_id": person_id, "is_self": False}],
    )
    with pytest.raises(DuplicateError):
        modify_contact(
            person_id=person_id,
            first_name="Freddy",
            creation_datetime_iso=GLOBAL_TIME_ISO,
        )


def test_remove_contact(self_contact: dict[str, Any]) -> None:
    # Failure
    with pytest.raises(NoDataError):
        remove_contact(person_id="wrong id")
    # Success
    remove_contact(person_id=self_contact["person_id"])
    current_context = get_current_context()
    contact_database = current_context.get_database(namespace=DatabaseNamespace.CONTACT)
    assert contact_database.is_empty()


def test_search_contacts(self_contact: dict[str, Any]) -> None:
    # Exact matching uuid
    assert [self_contact] == search_contacts(person_id=self_contact["person_id"])
    # Fuzzy match name
    assert [self_contact] == search_contacts(
        contact_name="Theo"
    )  # , last_name="Appleseed"
    assert [self_contact] == search_contacts(
        contact_name="Theos"
    )  # , last_name="Appleseed"
    assert [self_contact] == search_contacts(
        contact_name="Appleseed"
    )  # , last_name="Appleseed"

    # Exact match phone number
    assert [self_contact] == search_contacts(phone_number=self_contact["phone_number"])
    # Fuzzy match relationship
    assert [self_contact] == search_contacts(relationship="myself")
    # Exact match is_self
    assert [self_contact] == search_contacts(is_self=True)
    # Range search birthday
    assert [self_contact] == search_contacts(
        birthday_lowerbound="1999-05-14",
        birthday_upperbound="1999-05-16",
    )
    # No arguments
    with pytest.raises(ValueError):
        search_contacts()
    # Exact matching failure
    assert (
        len(
            search_contacts(
                person_id=str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name="wrong id"))
            )
        )
        == 0
    )
    # Fuzzy matching failure
    assert len(search_contacts(relationship="friend")) == 0


# ---------- regex-injection regression: phone/email inputs in name lookups ----------


PHONE_WITH_PLUS = "+1 555-890-1234-5678"
EMAIL = "alice@example.com"


def _regex_contact_df() -> pl.DataFrame:
    """Small standalone contact frame for regex-injection regression tests.

    Built directly rather than via fixtures so these cases don't depend on
    the `execution_context` setup used by the CRUD tests above.
    """
    return pl.DataFrame(
        [
            {
                "person_id": "p1",
                "first_name": "Alice",
                "last_name": "Smith",
                "full_name": "Alice Smith",
                "phone_number": PHONE_WITH_PLUS,
                "email": EMAIL,
            },
            {
                "person_id": "p2",
                "first_name": "J.R.R.",
                "last_name": "Tolkien",
                "full_name": "J.R.R. Tolkien",
                "phone_number": "+1 555-000-0000",
                "email": "tolkien@example.com",
            },
        ]
    )


def test_lookup_by_full_name_with_phone_input_does_not_crash() -> None:
    """Prior bug: '+' in phone number produced invalid regex `(?i)+1 ...`."""
    df = _regex_contact_df()
    result = lookup_contact_value(
        val=PHONE_WITH_PLUS,
        contact_db=df,
        target_col="person_id",
        match_col="full_name",
    )
    # strict=False returns the input value on no-match (existing contract).
    assert result == PHONE_WITH_PLUS


def test_lookup_by_full_name_with_phone_input_strict_returns_empty() -> None:
    df = _regex_contact_df()
    result = lookup_contact_value(
        val=PHONE_WITH_PLUS,
        contact_db=df,
        strict=True,
        target_col="person_id",
        match_col="full_name",
    )
    assert result == ""


def test_lookup_by_full_name_with_email_input_does_not_crash() -> None:
    df = _regex_contact_df()
    result = lookup_contact_value(
        val=EMAIL,
        contact_db=df,
        strict=True,
        target_col="person_id",
        match_col="full_name",
    )
    assert result == ""


def test_lookup_by_full_name_escapes_regex_metachars() -> None:
    """'J.R.R.' should match literal 'J.R.R. Tolkien', not treat '.' as wildcard."""
    df = _regex_contact_df()
    result = lookup_contact_value(
        val="J.R.R.",
        contact_db=df,
        strict=True,
        target_col="person_id",
        match_col="full_name",
    )
    assert result == "p2"

    # Wildcard-style input must no longer match anything unrelated.
    result_wild = lookup_contact_value(
        val="JXRXRX",
        contact_db=df,
        strict=True,
        target_col="person_id",
        match_col="full_name",
    )
    assert result_wild == ""


def test_lookup_by_full_name_plain_name_still_works() -> None:
    df = _regex_contact_df()
    result = lookup_contact_value(
        val="Alice",
        contact_db=df,
        strict=True,
        target_col="person_id",
        match_col="full_name",
    )
    assert result == "p1"


def test_lookup_by_email_or_phone_still_normalizes() -> None:
    """The email_or_phone path is unchanged — fix only touches full_name branch."""
    df = _regex_contact_df()
    result = lookup_contact_value(
        val=PHONE_WITH_PLUS,
        contact_db=df,
        strict=True,
        target_col="person_id",
        match_col="email_or_phone",
    )
    assert result == "p1"


def test_match_names_skips_phone_number_input() -> None:
    df = _regex_contact_df()
    matched = match_names_in_contact([PHONE_WITH_PLUS, "Alice"], contact_df=df)
    assert matched["person_id"].to_list() == ["p1"]


def test_match_names_skips_email_input() -> None:
    df = _regex_contact_df()
    matched = match_names_in_contact([EMAIL, "Tolkien"], contact_df=df)
    assert matched["person_id"].to_list() == ["p2"]


def test_match_names_all_phone_returns_empty() -> None:
    """When every input is filtered out we return an empty frame — no fold-empty crash."""
    df = _regex_contact_df()
    matched = match_names_in_contact(
        [PHONE_WITH_PLUS, "+1 555-000-0000"], contact_df=df
    )
    assert matched.height == 0


def test_match_names_escapes_regex_metachars() -> None:
    df = _regex_contact_df()
    # 'J.R.R' (no trailing dot) sits inside 'J.R.R. Tolkien'. The dots must be
    # escaped — otherwise they'd be interpreted as regex wildcards. Note we
    # don't use a trailing dot because match_names_in_contact wraps the
    # pattern in `\b...\b`, and `\b` cannot fire between two non-word chars.
    matched = match_names_in_contact(["J.R.R"], contact_df=df)
    assert matched["person_id"].to_list() == ["p2"]

    matched_wild = match_names_in_contact(["JXRXR"], contact_df=df)
    assert matched_wild.height == 0


# ---------- broken OR-fallback in participant resolvers ----------


def test_get_participants_person_id_or_name_resolves_phone_via_fallback() -> None:
    """The OR-fallback was previously short-circuited on the first (name)
    call because strict=False returned the raw val (truthy). With strict=True
    on the primary, phone-number invitees now resolve to the person's full
    name via the email_or_phone fallback."""
    df = _regex_contact_df()
    resolved = get_participants_person_id_or_name([PHONE_WITH_PLUS], df)
    assert resolved == ["Alice Smith"]


def test_get_participants_person_id_or_name_resolves_email_via_fallback() -> None:
    df = _regex_contact_df()
    resolved = get_participants_person_id_or_name([EMAIL], df)
    assert resolved == ["Alice Smith"]


def test_get_participants_person_id_or_name_resolves_name_via_primary() -> None:
    df = _regex_contact_df()
    resolved = get_participants_person_id_or_name(["Alice Smith"], df)
    # First resolver (get_person_id_by_full_name, target_col="person_id")
    # matches, so we get the person_id — not the full name.
    assert resolved == ["p1"]


def test_get_participants_person_id_or_name_unknown_returns_raw_input() -> None:
    """When neither the name nor the email/phone matches, the fallback
    resolver (strict=False) returns the raw input. This preserves the
    'unknown participant -> raw value passthrough' contract."""
    df = _regex_contact_df()
    resolved = get_participants_person_id_or_name(["Ghost Person"], df)
    assert resolved == ["Ghost Person"]


def test_get_participants_id_by_name_or_phone_or_email_phone_first() -> None:
    """The other OR-partial — email_or_phone tried first, name as fallback.
    Phone-number invitee resolves to person_id (not raw string)."""
    df = _regex_contact_df()
    resolved = get_participants_id_by_name_or_phone_or_email([PHONE_WITH_PLUS], df)
    assert resolved == ["p1"]


def test_get_participants_id_by_name_or_phone_or_email_name_fallback() -> None:
    df = _regex_contact_df()
    resolved = get_participants_id_by_name_or_phone_or_email(["Alice Smith"], df)
    assert resolved == ["p1"]
