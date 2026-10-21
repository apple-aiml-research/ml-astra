# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""A collection of tools which simulates common functions used for phone calls."""

import copy
import functools
from typing import Dict, List, Literal, Union, cast
from uuid import uuid4

import polars as pl

from astra_tool_sandbox.common.execution_context import (
    DatabaseNamespace,
    RoleType,
    get_current_context,
)
from astra_tool_sandbox.common.utils import (
    NOT_GIVEN,
    NotGiven,
    exact_match_filter_dataframe,
    filter_dataframe,
    fuzzy_match_filter_dataframe,
    gt_eq_duration_filter_dataframe,
    gt_eq_filter_dataframe,
    is_email_address,
    is_phone_number,
    lt_eq_duration_filter_dataframe,
    lt_eq_filter_dataframe,
    normalize_notgiven,
    parse_duration_to_hms,
    register_as_tool,
)
from astra_tool_sandbox.common.validators import (
    typechecked,
    validate_if_iso8601_str,
    validate_iso8601,
)
from astra_tool_sandbox.tools.contact import (
    check_phonecall_or_email_match_person_id,
    get_person_id_by_email_or_phonenumber,
)


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def create_outgoing_call(creation_datetime_iso: str, receiver_address: str) -> str:
    """Create an outgoing call and return its unique identifier.

    Args:
        creation_datetime_iso:      ISO 8601 formatted timestamp indicating when the outgoing call was created.
        receiver_address:                   Phone numbers or email address of the receiver.
    Returns:
        A unique string identifier for the created calendar event, which can be used
        to reference or update the event in other operations.
    """
    if (not is_phone_number(receiver_address)) and (
        not is_email_address(receiver_address)
    ):
        raise ValueError(
            "Provided receiver address is invalid, it needs to be either phone number or email address"
        )

    validate_iso8601(time_string=creation_datetime_iso)

    current_context = get_current_context()
    # get contact_db
    contact_db = copy.deepcopy(
        current_context.get_database(namespace=DatabaseNamespace.CONTACT)
    )
    caller_id = contact_db.filter(pl.col("is_self"))[0, "person_id"]
    caller_address = contact_db.filter(pl.col("is_self"))[0, "phone_number"]

    receiver_id = get_person_id_by_email_or_phonenumber(receiver_address, contact_db)

    phonecall_id = f"phone-{str(uuid4())}"
    current_context.add_to_database(
        namespace=DatabaseNamespace.PHONE,
        rows=[
            {
                "phone_call_id": phonecall_id,
                "call_type": "outgoing",
                "caller_address": caller_address,
                "caller_id": caller_id,
                "receiver_address": receiver_address,
                "receiver_id": receiver_id,
                "voice_mail_transcription": None,
                "creation_datetime_iso": creation_datetime_iso,
                "duration_in_hms": None,
            }
        ],
    )
    return phonecall_id


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def remove_phone_call_logs(phone_call_id: str) -> None:
    """Remove an existing phone call logs of the PHONE database.

    Args:
        phone_call_id:      String format unique identifier of the phone call logs to be deleted

    Returns:

    Raises:
        NoDataError:    If the provided phone_call_id was not found
    """

    current_context = get_current_context()
    current_context.remove_from_database(
        namespace=DatabaseNamespace.PHONE,
        predicate=pl.col("phone_call_id") == phone_call_id,
    )


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def search_phonecall_logs(
    phone_call_id: Union[str, NotGiven] = NOT_GIVEN,
    creation_datetime_iso_lowerbound: Union[str, NotGiven] = NOT_GIVEN,
    creation_datetime_iso_upperbound: Union[str, NotGiven] = NOT_GIVEN,
    duration_in_hms_lowerbound: Union[str, NotGiven] = NOT_GIVEN,
    duration_in_hms_upperbound: Union[str, NotGiven] = NOT_GIVEN,
    caller_id: Union[str, NotGiven] = NOT_GIVEN,
    caller_address: Union[str, NotGiven] = NOT_GIVEN,
    receiver_id: Union[str, NotGiven] = NOT_GIVEN,
    receiver_address: Union[str, NotGiven] = NOT_GIVEN,
    call_type: Union[str, NotGiven] = NOT_GIVEN,
    voice_mail_transcription: Union[str, NotGiven] = NOT_GIVEN,
) -> List[
    Dict[
        Literal[
            "phone_call_id",
            "call_type",
            "caller_address",
            "caller_id",
            "receiver_address",
            "receiver_id",
            "voice_mail_transcription",
            "creation_datetime_iso",
            "duration_in_hms",
        ],
        str,
    ]
]:
    """
    Search for phone call logs based on provided criteria.

    Supports a range of match types for different fields, including:
    1. Exact value matching for identifiers and addresses
    2. Fuzzy matching for voicemail transcription content
    3. Range-based filtering for call creation time and duration

    Args:
        phone_call_id:                  Unique ID of the phone call log. Exact match.
        creation_datetime_iso_lowerbound:  Lower bound of call creation time (ISO 8601).
        creation_datetime_iso_upperbound:  Upper bound of call creation time (ISO 8601).
        duration_in_hms_lowerbound:     Lower bound of call duration in 'HH:mm:ss' or natural language (e.g., '2 minutes').
        duration_in_hms_upperbound:     Upper bound of call duration in 'HH:mm:ss' or natural language (e.g., '5m 30s').
        caller_id:                      ID of the caller. Exact match. Must be consistent with caller_address if both provided.
        caller_address:                 Email or phone number of the caller. Exact match.
        receiver_id:                    ID of the receiver. Exact match. Must be consistent with receiver_address if both provided.
        receiver_address:               Email or phone number of the receiver. Exact match.
        call_type:                      Type of the call (e.g., 'incoming', 'outgoing', 'missed'). Exact match.
        voice_mail_transcription:      Transcribed voicemail content. Fuzzy match.

    Returns:
        A list of matching phone call log entries. Returns an empty list if no matches are found.

    Raises:
        ValueError: If input formats are invalid (e.g., malformed datetime or mismatched person ID/address).
    """
    current_context = get_current_context()
    phonecall_db = current_context.get_database(namespace=DatabaseNamespace.PHONE)
    contact_db = current_context.get_database(namespace=DatabaseNamespace.CONTACT)
    # validate strings
    validate_if_iso8601_str(
        creation_datetime_iso_lowerbound, "creation_datetime_iso_lowerbound"
    )
    validate_if_iso8601_str(
        creation_datetime_iso_upperbound, "creation_datetime_iso_upperbound"
    )
    if isinstance(duration_in_hms_lowerbound, str):
        duration_in_hms_lowerbound = parse_duration_to_hms(duration_in_hms_lowerbound)
    if isinstance(duration_in_hms_upperbound, str):
        duration_in_hms_upperbound = parse_duration_to_hms(duration_in_hms_upperbound)

    check_phonecall_or_email_match_person_id(
        person_id=normalize_notgiven(caller_id),
        person_e_address=normalize_notgiven(caller_address),
        contact_db=contact_db,
    )
    check_phonecall_or_email_match_person_id(
        person_id=normalize_notgiven(receiver_id),
        person_e_address=normalize_notgiven(receiver_address),
        contact_db=contact_db,
    )

    # Filtering criteria
    phonecall_dataframe = filter_dataframe(
        dataframe=phonecall_db,
        filter_criteria=[
            ("phone_call_id", phone_call_id, exact_match_filter_dataframe),
            ("call_type", call_type, exact_match_filter_dataframe),
            ("caller_address", caller_address, exact_match_filter_dataframe),
            ("caller_id", caller_id, exact_match_filter_dataframe),
            ("receiver_address", receiver_address, exact_match_filter_dataframe),
            ("receiver_id", receiver_id, exact_match_filter_dataframe),
            (
                "voice_mail_transcription",
                voice_mail_transcription,
                functools.partial(fuzzy_match_filter_dataframe, threshold=50),
            ),
            (
                "creation_datetime_iso",
                creation_datetime_iso_lowerbound,
                gt_eq_filter_dataframe,
            ),
            (
                "creation_datetime_iso",
                creation_datetime_iso_upperbound,
                lt_eq_filter_dataframe,
            ),
            (
                "duration_in_hms",
                duration_in_hms_lowerbound,
                gt_eq_duration_filter_dataframe,
            ),
            (
                "duration_in_hms",
                duration_in_hms_upperbound,
                lt_eq_duration_filter_dataframe,
            ),
        ],
    )

    return cast(
        List[
            Dict[
                Literal[
                    "phone_call_id",
                    "call_type",
                    "caller_address",
                    "caller_id",
                    "receiver_address",
                    "receiver_id",
                    "voice_mail_transcription",
                    "creation_datetime_iso",
                    "duration_in_hms",
                ],
                str,
            ]
        ],
        phonecall_dataframe.to_dicts(),
    )


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def get_all_phone_calls() -> (
    List[
        Dict[
            Literal[
                "phone_call_id",
                "call_type",
                "caller_address",
                "caller_id",
                "receiver_address",
                "receiver_id",
                "voice_mail_transcription",
                "creation_datetime_iso",
                "duration_in_hms",
            ],
            str,
        ]
    ]
):
    """Return all Calendar Events
    Args:
        None
    Returns:
        A List of all calendar events. An empty List if no calendar events were found

    """
    current_context = get_current_context()
    phonecall_dataframe = current_context.get_database(DatabaseNamespace.PHONE)
    return cast(
        List[
            Dict[
                Literal[
                    "phone_call_id",
                    "call_type",
                    "caller_address",
                    "caller_id",
                    "receiver_address",
                    "receiver_id",
                    "voice_mail_transcription",
                    "creation_datetime_iso",
                    "duration_in_hms",
                ],
                str,
            ]
        ],
        phonecall_dataframe.to_dicts(),
    )
