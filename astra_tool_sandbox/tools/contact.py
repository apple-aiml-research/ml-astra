# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""A collection of tools which simulates common functions used for contact book."""

import functools
import re
from functools import partial, reduce
from logging import getLogger
from typing import Dict, List, Literal, Optional, Union, cast
from uuid import uuid4

import polars as pl
from polars.exceptions import DuplicateError, NoDataError
from typing_extensions import Protocol

from astra_tool_sandbox.common.execution_context import (
    DatabaseNamespace,
    RoleType,
    get_current_context,
)
from astra_tool_sandbox.common.utils import (
    NOT_GIVEN,
    NotGiven,
    exact_match_filter_dataframe,
    exact_match_filter_dataframe_case_insensitive,
    filter_dataframe,
    fuzzy_match_filter_dataframe,
    gt_eq_filter_dataframe,
    is_email_address,
    is_phone_number,
    load_str_time_to_datetime_iso_8601,
    lt_eq_filter_dataframe,
    normalize_phone_number,
    normalize_phone_number_filter,
    register_as_tool,
)
from astra_tool_sandbox.common.validators import (
    typechecked,
    validate_iso8601,
    validate_type,
)

LOGGER = getLogger(__name__)


def is_ascii_only(s: str) -> bool:
    """Checks if a string contains only ASCII characters."""
    return all(ord(c) < 128 for c in s)


def is_latin_name(s: str) -> bool:
    """Checks if the name is composed only of Latin letters and common separators."""
    return bool(re.fullmatch(r"[A-Za-z \-']+", s)) and is_ascii_only(s)


def is_cjk(s: str) -> bool:
    """Checks if the string contains any CJK (Chinese, Japanese, Korean) characters."""
    return any(
        "\u4e00" <= c <= "\u9fff"  # Chinese
        or "\u3040" <= c <= "\u309f"  # Hiragana
        or "\u30a0" <= c <= "\u30ff"  # Katakana
        or "\uac00" <= c <= "\ud7af"  # Hangul
        for c in s
    )


def compose_full_name(
    first_name: Optional[Union[str, None, NotGiven]],
    last_name: Optional[Union[str, None, NotGiven]],
) -> Union[str, None, NotGiven]:
    """Compose full name with guessed order based on character type."""
    if not isinstance(first_name, str) and not isinstance(last_name, str):
        return first_name
    elif not isinstance(first_name, str) or not isinstance(last_name, str):
        return first_name or last_name

    # If both are Latin/ASCII, assume Western order
    if is_latin_name(first_name) and is_latin_name(last_name):
        return f"{first_name} {last_name}"

    # If either has CJK characters, assume Eastern order
    if is_cjk(first_name) or is_cjk(last_name):
        return f"{last_name}{first_name}"  # No space

    # Fallback to Western order
    return f"{first_name} {last_name}"


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def add_contact(
    creation_datetime_iso: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    full_name: Optional[str] = None,
    alias: Optional[str] = None,
    phone_number: Optional[str] = None,
    email: Optional[str] = None,
    relationship: Optional[str] = None,
    address: Optional[str] = None,
    company: Optional[str] = None,
    job_title: Optional[str] = None,
    is_self: bool = False,
    birthday: Optional[str] = None,
) -> str:
    """Add a new contact person to contact database. Entries with identical information are allowed,
    and will be assigned different person_ids.

    Args:
        creation_datetime_iso: Required. ISO 8601 formatted timestamp indicating when the contact was created.
        first_name:     Optional. First Name of contact person
        last_name:      Optional. Last Name of contact person
        full_name:      Optional. Full Name of contact person if both first and last name not provided
        alias:          Optional. Alias of contact person
        phone_number:   Optional. Phone number of contact person
        email:          Optional. Email of contact person
        relationship:   Optional. Relationship between user and this contact
        address:        Optional. addresss of contact person
        company:        Optional. company of contact person
        job_title:      Optional. job title of contact person
        is_self:        Optional. Defaults to False. Should be set to True if the contact corresponds to the current user.
        birthday:       Optional. Birthday of contact person in "YYYY-MM-DD".


    Returns:
        String format unique identifier for the contact person, this can be passed to other functions
        which require a unique identifier for this contact person

    Raises:
        DuplicateError:     When self entry already exists, and we are adding a new one

    """
    # Validate phone number
    # validate_phone_number(phone_number)
    person_id = f"contacts-{str(uuid4())}"
    current_context = get_current_context()
    if is_self and search_contacts(is_self=True):
        raise DuplicateError("Self entry already exists. Cannot add another one.")

    birthday_datetime_iso = load_str_time_to_datetime_iso_8601(birthday)
    current_context.add_to_database(
        namespace=DatabaseNamespace.CONTACT,
        rows=[
            {
                "person_id": person_id,
                "first_name": first_name,
                "last_name": last_name,
                "full_name": compose_full_name(
                    first_name=first_name, last_name=last_name
                )
                if not isinstance(full_name, str)
                else full_name,
                "phone_number": phone_number,
                "alias": alias,
                "email": email,
                "relationship": relationship,
                "address": address,
                "company": company,
                "job_title": job_title,
                "is_self": is_self,
                "birthday": birthday_datetime_iso,
                "creation_datetime_iso": creation_datetime_iso,
            }
        ],
    )
    return person_id


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def modify_contact(
    person_id: str,
    creation_datetime_iso: str,
    first_name: Union[str, NotGiven] = NOT_GIVEN,
    last_name: Union[str, NotGiven] = NOT_GIVEN,
    full_name: Union[str, NotGiven] = NOT_GIVEN,
    alias: Union[str, NotGiven] = NOT_GIVEN,
    phone_number: Union[str, NotGiven] = NOT_GIVEN,
    email: Union[str, NotGiven] = NOT_GIVEN,
    relationship: Union[str, NotGiven] = NOT_GIVEN,
    address: Union[str, NotGiven] = NOT_GIVEN,
    company: Union[str, NotGiven] = NOT_GIVEN,
    job_title: Union[str, NotGiven] = NOT_GIVEN,
    is_self: Union[bool, NotGiven] = NOT_GIVEN,
    birthday: Union[str, NotGiven] = NOT_GIVEN,
) -> str:
    """Modify a contact entry with new information provided

    Args:
        person_id:      String unique identifier for the contact person
        creation_datetime_iso: ISO 8601 formatted string of the current date and time.
        first_name:     Optional. New First Name of contact person
        last_name:      Optional. New Last Name of contact person
        full_name:      Optional. New Full name of contact person
        alias:          Optional. New Alias of contact person
        phone_number:   Optional. New Phone number of contact person
        email:          Optional. New Email of contact person
        relationship:   Optional, New relationship between user and this contact
        address:        Optional. New addresss of contact person
        company:        Optional. New company of contact person
        job_title:      Optional. New job_title of contact person
        is_self:        Optional. Defaults to False. Should be set to True if the contact corresponds to the current user.
        birthday:       Optional. New Birth day of contact person in "YYYY-MM-DD"

    Returns:

    Raises:
        ValueError:     When all arguments were None
        NoDataError:    When the person_id cannot be found in database
        DuplicateError: When multiple entries with the same id were found
                        or when modifying an entry to self with existing self

    """
    if all(
        x is NOT_GIVEN
        for x in [
            first_name,
            last_name,
            full_name,
            alias,
            phone_number,
            email,
            relationship,
            address,
            company,
            job_title,
            is_self,
            birthday,
        ]
    ):
        raise ValueError(
            "No update information given. At least one new field should be provided among "
            "[name, phone_number, relationship, is_self] in order to modify contact"
        )
    # Make sure there won't be duplicate self
    self_entries = search_contacts(is_self=True)
    if self_entries and is_self and self_entries[0]["person_id"] != person_id:
        raise DuplicateError("Self entry already exists. Cannot add another one.")
    current_context = get_current_context()
    contact_database = current_context.get_database(DatabaseNamespace.CONTACT)
    # Check if entry exists
    target_entry = contact_database.filter(pl.col("person_id") == person_id)
    if target_entry.is_empty():
        raise NoDataError(f"No db entry matching {person_id=} found")
    # Check if entry is unique
    target_entry_dicts = target_entry.to_dicts()
    if len(target_entry_dicts) > 1:
        raise DuplicateError(f"More than 1 entry with {person_id=} found")
    target_entry_dict = target_entry_dicts[0]

    birthday_datetime_iso = (
        load_str_time_to_datetime_iso_8601(birthday)
        if isinstance(birthday, str)
        else NOT_GIVEN
    )

    # Create updated entry
    for name, value in [
        ("first_name", first_name),
        ("last_name", last_name),
        (
            "full_name",
            compose_full_name(first_name=first_name, last_name=last_name)
            if not isinstance(full_name, str)
            else full_name,
        ),
        ("alias", alias),
        ("phone_number", phone_number),
        ("email", email),
        ("relationship", relationship),
        ("address", address),
        ("company", company),
        ("job_title", job_title),
        ("is_self", is_self),
        ("birthday", birthday_datetime_iso),
    ]:
        if value is not NOT_GIVEN:
            target_entry_dict[name] = value

    target_entry_dict["creation_datetime_iso"] = creation_datetime_iso

    # Update database
    current_context.remove_from_database(
        namespace=DatabaseNamespace.CONTACT,
        predicate=pl.col("person_id") == person_id,
    )
    current_context.add_to_database(
        namespace=DatabaseNamespace.CONTACT,
        rows=[target_entry_dict],
    )
    return person_id


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def remove_contact(person_id: str) -> None:
    """Remove an existing contact person to contact database.

    Args:
        person_id:      String format unique identifier of the person to be deleted

    Returns:

    Raises:
        NoDataError:    If the provided person_id was not found
    """
    validate_type(person_id, "person_id", str)

    current_context = get_current_context()
    current_context.remove_from_database(
        namespace=DatabaseNamespace.CONTACT, predicate=pl.col("person_id") == person_id
    )


@register_as_tool(visible_to=(RoleType.AGENT,))
def search_contacts(
    person_id: Union[str, NotGiven] = NOT_GIVEN,
    contact_name: Union[str, NotGiven] = NOT_GIVEN,
    alias: Union[str, NotGiven] = NOT_GIVEN,
    phone_number: Union[str, NotGiven] = NOT_GIVEN,
    email: Union[str, NotGiven] = NOT_GIVEN,
    relationship: Union[str, NotGiven] = NOT_GIVEN,
    address: Union[str, NotGiven] = NOT_GIVEN,
    company: Union[str, NotGiven] = NOT_GIVEN,
    job_title: Union[str, NotGiven] = NOT_GIVEN,
    is_self: Union[bool, NotGiven] = NOT_GIVEN,
    birthday_upperbound: Union[str, NotGiven] = NOT_GIVEN,  # "YYYY-MM-DD"
    birthday_lowerbound: Union[str, NotGiven] = NOT_GIVEN,  # "YYYY-MM-DD"
) -> List[
    Dict[
        Literal[
            "person_id",
            "first_name",
            "last_name",
            "full_name",
            "alias",
            "phone_number",
            "email",
            "relationship",
            "address",
            "company",
            "job_title",
            "is_self",
            "birthday",
        ],
        str,
    ]
]:
    # TODO: Merge first_name, last_name, full_name as contact name
    # Use `contact_name` to match a person's first name, last name, or full name. This field supports partial and fuzzy matching.
    """Search for contacts which contains all contact entries that matched all criteria

    Args:
        person_id:              Str format unique id for the contact person, exact matched
        contact_name:           The person's first name, last name, or full name. This field supports partial and fuzzy matching.
        alias:                  fuzzy matched
        phone_number:           exact matched
        email:                  exact matched
        relationship:           Relationship to the current user, fuzzy matched
        address:                fuzzy matched
        company:                fuzzy matched
        job_title:              fuzzy matched
        is_self:                Indicates if searching for the current user, exact matched
        birthday_upperbound:    Upperbound of the birthday in YYYY-MM-DD to search.
        birthday_lowerbound:    Lowerbound of the birthday in YYYY-MM-DD to search.

    Returns:
        A List of matching contacts. An empty List if no matching contacts were found

    Raises:
        ValueError: When all arguments were not provided

    """
    if all(
        x is NOT_GIVEN
        for x in [
            person_id,
            contact_name,
            alias,
            phone_number,
            email,
            relationship,
            address,
            company,
            job_title,
            is_self,
            birthday_lowerbound,
            birthday_upperbound,
        ]
    ):
        raise ValueError(
            "No update information given. At least one new field should be provided among "
            "[contact_name, alias, phone_number, email, relationship, address, company, job_title, is_self, birthday_lowerbound, birthday_upperbound] in order to search for a contact"
        )
    current_context = get_current_context()
    contact_db = current_context.get_database(namespace=DatabaseNamespace.CONTACT)

    # Validate timestamp fields
    if isinstance(birthday_lowerbound, str):
        validate_iso8601(birthday_lowerbound)
    if isinstance(birthday_upperbound, str):
        validate_iso8601(birthday_upperbound)

    # Step 1: Handle contact_name logic separately
    if contact_name is not NOT_GIVEN:
        name_matches = []
        for col in ["first_name", "last_name", "full_name"]:
            name_matches.append(
                fuzzy_match_filter_dataframe(
                    dataframe=contact_db,
                    column_name=col,
                    value=contact_name,
                )
            )
        # Union all name matches and drop duplicates
        contact_name_matched = pl.concat(name_matches).unique()

        if contact_name_matched.is_empty() or all(
            x is NOT_GIVEN
            for x in [
                person_id,
                alias,
                phone_number,
                email,
                relationship,
                address,
                company,
                job_title,
                is_self,
                birthday_lowerbound,
                birthday_upperbound,
            ]
        ):
            return cast(
                List[
                    Dict[
                        Literal[
                            "person_id",
                            "first_name",
                            "last_name",
                            "full_name",
                            "alias",
                            "phone_number",
                            "email",
                            "relationship",
                            "address",
                            "company",
                            "job_title",
                            "is_self",
                            "birthday",
                        ],
                        str,
                    ]
                ],
                contact_name_matched.to_dicts(),
            )
    else:
        contact_name_matched = contact_db

    # Step 2: Filter the remaining criteria
    contacts_dataframe = filter_dataframe(
        dataframe=contact_name_matched,
        filter_criteria=[
            ("person_id", person_id, exact_match_filter_dataframe),
            ("alias", alias, fuzzy_match_filter_dataframe),
            ("email", email, exact_match_filter_dataframe_case_insensitive),
            ("phone_number", phone_number, normalize_phone_number_filter),
            (
                "birthday",
                birthday_lowerbound,
                gt_eq_filter_dataframe,
            ),
            (
                "birthday",
                birthday_upperbound,
                lt_eq_filter_dataframe,
            ),
            (
                "relationship",
                relationship,
                functools.partial(fuzzy_match_filter_dataframe, threshold=90),
            ),
            (
                "address",
                address,
                functools.partial(fuzzy_match_filter_dataframe, threshold=90),
            ),
            ("company", company, fuzzy_match_filter_dataframe),
            ("job_title", job_title, fuzzy_match_filter_dataframe),
            ("is_self", is_self, exact_match_filter_dataframe),
        ],
    )
    return cast(
        List[
            Dict[
                Literal[
                    "person_id",
                    "first_name",
                    "last_name",
                    "full_name",
                    "alias",
                    "phone_number",
                    "email",
                    "relationship",
                    "address",
                    "company",
                    "job_title",
                    "is_self",
                    "birthday",
                ],
                str,
            ]
        ],
        contacts_dataframe.to_dicts(),
    )


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def get_all_contacts() -> (
    List[
        Dict[
            Literal[
                "person_id",
                "first_name",
                "last_name",
                "full_name",
                "alias",
                "phone_number",
                "email",
                "relationship",
                "address",
                "company",
                "job_title",
                "is_self",
                "birthday",
            ],
            str,
        ]
    ]
):
    """Return all Contacts
    Args:
        None
    Returns:
        A List of all contacts. An empty List if no contacts were found

    """
    current_context = get_current_context()
    contacts_dataframe = current_context.get_database(DatabaseNamespace.CONTACT)
    return cast(
        List[
            Dict[
                Literal[
                    "person_id",
                    "first_name",
                    "last_name",
                    "full_name",
                    "alias",
                    "phone_number",
                    "email",
                    "relationship",
                    "address",
                    "company",
                    "job_title",
                    "is_self",
                    "birthday",
                ],
                str,
            ]
        ],
        contacts_dataframe.to_dicts(),
    )


class ParticipantResolver(Protocol):
    def __call__(self, val: str, contact_db: pl.DataFrame) -> str: ...


def match_names_in_contact(
    name_list: list[str],
    contact_df: pl.DataFrame,
    name_columns: list[str] = ["first_name", "last_name", "full_name"],
) -> pl.DataFrame:
    """
    Return rows from contact_df where any of the specified name_columns
    (e.g., 'first_name', 'last_name', 'full_name') contains any name in name_list.
    Matching is case-insensitive and uses whole word regex.
    """
    # Sanity check: only include columns that exist in DataFrame
    valid_cols = [col for col in name_columns if col in contact_df.columns]

    if not valid_cols or not name_list:
        return contact_df[0:0]  # Return empty result if nothing to search

    filters = []
    for name in name_list:
        # Phone numbers and emails can be passed here (invitee lists mix all
        # three identifier types). They cannot match a name column, and the
        # leading '+' on international phone numbers is an invalid regex
        # repetition operator — skip so the caller's fallback path handles
        # them.
        if is_phone_number(name) or is_email_address(name):
            continue
        pattern = rf"(?i)\b{re.escape(name)}\b"
        col_exprs = [
            pl.col(col).cast(str).str.contains(pattern, literal=False).fill_null(False)
            for col in valid_cols
        ]
        filters.append(
            pl.fold(acc=pl.lit(False), function=lambda acc, x: acc | x, exprs=col_exprs)
        )

    if not filters:
        return contact_df[0:0]

    # Combine all name-based filters using OR
    combined_filter = pl.fold(
        acc=pl.lit(False), function=lambda acc, x: acc | x, exprs=filters
    )

    return contact_df.filter(combined_filter)


def lookup_contact_value(
    val: str,
    contact_db: pl.DataFrame,
    strict: bool = False,
    *,
    target_col: Literal["person_id", "full_name", "phone_number", "email"],
    match_col: Literal["person_id", "full_name", "email_or_phone"],
    verbal: bool = False,
) -> str:
    """
    Generalized contact lookup helper with phone number normalization support.
    """
    if match_col == "person_id":
        filtered = contact_db.filter(pl.col("person_id") == val)
    elif match_col == "email_or_phone":
        # Handle phone number normalization for email_or_phone matching
        phone_exprs = []
        email_exprs = []

        # Check if val is a phone number for normalized matching
        if is_phone_number(val):
            normalized_val = normalize_phone_number(val)
            phone_exprs = [
                pl.col("phone_number").map_elements(
                    lambda x: normalize_phone_number(x)
                    if isinstance(x, str) and is_phone_number(x)
                    else x,
                    return_dtype=pl.Utf8,
                )
                == normalized_val
            ]
        else:
            phone_exprs = [pl.col("phone_number") == val]

        # Always check email with exact match
        email_exprs = [pl.col("email") == val]

        # Combine phone and email expressions with OR
        combined_expr = pl.fold(
            acc=pl.lit(False),
            function=lambda acc, x: acc | x,
            exprs=phone_exprs + email_exprs,
        )
        filtered = contact_db.filter(combined_expr)
    else:  # match_col == "full_name"
        # Phone numbers / emails cannot match a name column, and unescaped
        # '+' from an international phone number is an invalid regex
        # repetition operator. Short-circuit so the caller's OR fallback
        # (email_or_phone lookup) can handle these inputs.
        if is_phone_number(val) or is_email_address(val):
            filtered = contact_db[0:0]
        else:
            pattern = rf"(?i){re.escape(val)}"
            exprs = [
                pl.col(col)
                .cast(str)
                .str.contains(pattern, literal=False)
                .fill_null(False)
                for col in contact_db.columns
            ]
            filtered = contact_db.filter(reduce(lambda a, b: a | b, exprs))

    if filtered.is_empty():
        if not strict:
            if verbal:
                print(
                    f"Contact {val} Got No matches contact found in the database. Using input value instead"
                )
            return val
        if strict:
            return ""

    return str(filtered[0, target_col])


get_full_name_by_person_id = partial(
    lookup_contact_value, target_col="full_name", match_col="person_id"
)


get_full_name_by_email_or_phonenumber = partial(
    lookup_contact_value, target_col="full_name", match_col="email_or_phone"
)

get_person_id_by_full_name = partial(
    lookup_contact_value, target_col="person_id", match_col="full_name"
)

get_person_id_by_email_or_phonenumber = partial(
    lookup_contact_value, target_col="person_id", match_col="email_or_phone"
)

get_email_by_full_name = partial(
    lookup_contact_value, target_col="email", match_col="full_name"
)

get_phonenumber_by_full_name = partial(
    lookup_contact_value, target_col="phone_number", match_col="full_name"
)


def check_phonecall_or_email_match_person_id(
    *,
    person_id: Optional[str],
    person_e_address: Optional[str],
    contact_db: pl.DataFrame,
) -> None:
    if not isinstance(person_id, str) or not isinstance(person_e_address, str):
        # One or both fields are missing; nothing to validate
        return

    actual_id = get_person_id_by_email_or_phonenumber(
        person_e_address, contact_db, strict=True
    )

    if person_id != actual_id:
        raise ValueError(
            f"Mismatch: provided person_id '{person_id}' does not match "
            f"the ID '{actual_id}' found for address '{person_e_address}'."
        )


def resolve_participants(
    participants: List[str],
    contact_db: pl.DataFrame,
    resolver: ParticipantResolver,
) -> List[str]:
    """
    Generic helper to resolve participant identifiers (names or IDs).

    Args:
        participants: list of raw participant inputs
        contact_db: contact dataframe
        resolver: function to resolve one participant

    Returns:
        Sorted list of resolved strings (e.g. person_ids or full_names)
    """
    return sorted(
        [
            resolved
            for p in participants
            if (resolved := resolver(p, contact_db)) is not None
        ]
    )


get_participants_full_name_by_person_id = partial(
    resolve_participants, resolver=get_full_name_by_person_id
)

get_participants_id_by_name_or_phone_or_email = partial(
    resolve_participants,
    # strict=True on the first resolver so no-match returns "" (falsy) and the
    # `or` actually falls through to the fallback. Default strict=False on the
    # fallback preserves the "unknown participant -> raw input" contract.
    resolver=lambda p, db: get_person_id_by_email_or_phonenumber(p, db, strict=True)
    or get_person_id_by_full_name(p, db),
)

get_participants_full_name_by_email_or_phonenumber = partial(
    resolve_participants,
    resolver=get_full_name_by_email_or_phonenumber,
)

get_participants_person_id_or_name = partial(
    resolve_participants,
    # strict=True on the first resolver so no-match returns "" (falsy) and the
    # `or` actually falls through to the fallback. Default strict=False on the
    # fallback preserves the "unknown participant -> raw input" contract.
    resolver=lambda p, db: get_person_id_by_full_name(p, db, strict=True)
    or get_full_name_by_email_or_phonenumber(p, db),
)
