# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""A collection of tools which simulates common functions used for messaging."""

import copy
import functools
from typing import Dict, List, Literal, Optional, Union, cast
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
    gt_eq_filter_dataframe,
    is_phone_number,
    lt_eq_filter_dataframe,
    normalize_phone_number,
    normalize_phone_number_filter,
    normalize_phone_numbers_in_list_filter,
    register_as_tool,
    sublist_filter_dataframe,
)
from astra_tool_sandbox.common.validators import (
    typechecked,
    validate_iso8601,
)
from astra_tool_sandbox.tools.contact import (
    get_full_name_by_email_or_phonenumber,
    get_participants_full_name_by_email_or_phonenumber,
    get_person_id_by_email_or_phonenumber,
)


def normalize_participants_addresses(addresses: List[str]) -> List[str]:
    """Normalize phone numbers in a list of participant addresses.

    Args:
        addresses: List of participant addresses (emails or phone numbers)

    Returns:
        List of addresses with phone numbers normalized
    """
    normalized = []
    for address in addresses:
        if is_phone_number(address):
            normalized.append(normalize_phone_number(address))
        else:
            normalized.append(address)
    return normalized


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def send_message(
    content: str,
    creation_datetime_iso: str,
    recipients_addresses: Optional[List[str]] = None,
    conversation_id: Optional[str] = None,
) -> str:
    """Send a message to recipients

    Args:
        content:        Message payload text
        creation_datetime_iso:  ISO8601 format of current time
        recipients_addresses:   Optional. A list of recipient addresses to send the message to.
        conversation_id:        Optional. The ID of an existing conversation to which this message is a reply.

    Returns:
        String format unique identifier for the message, this can be passed to other functions
        which require a unique identifier for this message

    Raises:
        ValueError:         If less than or more than 1 self entry was found
        ConnectionError:    If cellular service is not on

    """
    if all(x is None for x in [recipients_addresses, conversation_id]):
        raise ValueError(
            "No recipients information given. Provide at least a list recipients addresses or conversation_id."
        )

    validate_iso8601(creation_datetime_iso)
    current_context = get_current_context()
    # get contact_db
    contact_db = copy.deepcopy(
        current_context.get_database(namespace=DatabaseNamespace.CONTACT)
    )
    # get sender self person id
    self_person_id = contact_db.filter(pl.col("is_self"))[0, "person_id"]

    # get message_db
    message_db = copy.deepcopy(
        current_context.get_database(namespace=DatabaseNamespace.MESSAGING)
    )

    self_address = contact_db.filter(pl.col("is_self"))[0, "phone_number"]

    conversation_name, found_participants_addresses, found_participants_ids = (
        None,
        None,
        None,
    )
    if conversation_id:
        # check if provided message conversation id is valid
        try:
            assert (
                conversation_id
                in message_db.select("conversation_id").unique().to_series()
            )
        except AssertionError:
            # print(email_db.to_dicts())
            raise ValueError(f"Email id {conversation_id} provided does not exist")

        found_conversation_db = message_db.filter(
            pl.col("conversation_id") == conversation_id
        ).sort("creation_datetime_iso", descending=True)
        conversation_name = found_conversation_db[0, "conversation_name"]
        found_participants_addresses = found_conversation_db[
            0, "participants_addresses"
        ].to_list()
        found_participants_ids = found_conversation_db[0, "participants_ids"].to_list()

    participants_ids = found_participants_ids or None
    participants_addresses = found_participants_addresses or None

    if recipients_addresses:
        # Check the input
        recipients_ids = []
        recipients_addresses_cleaned = []
        for recipient_address in recipients_addresses:
            if "contacts-" in recipient_address:
                # Check if recipient_address exists in contact_db["person_id"]
                if (
                    not contact_db.select("person_id")
                    .to_series()
                    .eq(recipient_address)
                    .any()
                ):
                    raise ValueError(
                        f"Provided {recipient_address} is not a valid contact person id"
                    )
                else:
                    recipients_ids.append(recipient_address)
                    phone_number = contact_db.filter(
                        pl.col("person_id") == recipient_address
                    )[0, "phone_number"]
                    recipients_addresses_cleaned.append(phone_number)

            else:
                recipients_ids.append(
                    get_person_id_by_email_or_phonenumber(recipient_address, contact_db)
                )
                recipients_addresses_cleaned.append(recipient_address)

        # get participants ids for conversation finding purposes
        participants_ids = sorted({self_person_id, *recipients_ids})

        if found_participants_ids:
            try:
                # TODO: Allow changing participants
                assert participants_ids == found_participants_ids
            except AssertionError:
                raise ValueError(
                    f"Provided conversation {conversation_id} and recipients {recipients_addresses} do not match"
                )

            # If the conversation id found and participants id matched
            participants_addresses = found_participants_addresses
            self_address = (
                contact_db.filter(pl.col("is_self"))[0, "phone_number"]
                if participants_addresses
                and contact_db.filter(pl.col("is_self"))[0, "phone_number"]
                in participants_addresses
                else contact_db.filter(pl.col("is_self"))[0, "email"]
            )
        else:
            participants_addresses = sorted(
                [contact_db.filter(pl.col("is_self"))[0, "phone_number"]]
                + recipients_addresses_cleaned
            )

    if not conversation_id and recipients_addresses:
        # if conversation id not provided to find conversation name
        # Normalize participant addresses for comparison
        normalized_participants_addresses = normalize_participants_addresses(
            participants_addresses or []
        )

        # Find existing conversations by checking normalized participant addresses
        existing_conversations = message_db.with_columns(
            [
                pl.col("participants_addresses")
                .map_elements(
                    lambda x: normalize_participants_addresses(x)
                    if x is not None and len(x) > 0
                    else [],
                    return_dtype=pl.List(pl.Utf8),
                )
                .alias("normalized_participants_addresses")
            ]
        )

        filter_conversation_db = existing_conversations.filter(
            pl.col("normalized_participants_addresses")
            == normalized_participants_addresses
        )

        if not filter_conversation_db.is_empty():
            conversation_id, conversation_name = (
                filter_conversation_db[0, "conversation_id"],
                filter_conversation_db[0, "conversation_name"],
            )
        else:
            # check if only got one recipients
            if len(recipients_addresses) == 1:
                conversation_name = get_full_name_by_email_or_phonenumber(
                    val=recipients_addresses[0], contact_db=contact_db
                )
            else:
                conversation_name = " & ".join(
                    get_participants_full_name_by_email_or_phonenumber(
                        recipients_addresses,
                        contact_db=contact_db,
                    )
                )

            conversation_id = f"conversation-{uuid4()}"

    # Create message uuid
    message_id = f"messages-{str(uuid4())}"

    current_context.add_to_database(
        namespace=DatabaseNamespace.MESSAGING,
        rows=[
            {
                "conversation_id": conversation_id,
                "conversation_name": conversation_name,
                "participants_ids": participants_ids,
                "participants_addresses": participants_addresses,
                "message_id": message_id,
                "sender_person_id": self_person_id,
                "sender_address": self_address,
                "content": content,
                "creation_datetime_iso": creation_datetime_iso,
                "status": "sent",
            }
        ],
    )
    return message_id


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def search_messages(
    conversation_id: Union[str, NotGiven] = NOT_GIVEN,
    conversation_name: Union[str, NotGiven] = NOT_GIVEN,
    participants_ids: Union[List[str], NotGiven] = NOT_GIVEN,
    participants_addresses: Union[List[str], NotGiven] = NOT_GIVEN,
    message_id: Union[str, NotGiven] = NOT_GIVEN,
    sender_person_id: Union[str, NotGiven] = NOT_GIVEN,
    sender_address: Union[str, NotGiven] = NOT_GIVEN,
    content: Union[str, NotGiven] = NOT_GIVEN,
    creation_datetime_iso_lowerbound: Union[str, NotGiven] = NOT_GIVEN,
    creation_datetime_iso_upperbound: Union[str, NotGiven] = NOT_GIVEN,
    status: Union[str, NotGiven] = NOT_GIVEN,
) -> List[
    Dict[
        Literal[
            "conversation_id",
            "conversation_name",
            "participants_ids",
            "participants_addresses",
            "message_id",
            "sender_person_id",
            "sender_address",
            "content",
            "creation_datetime_iso",
            "status",
        ],
        str,
    ]
]:
    """Search for a message based on provided arguments

    Each field has a search criteria of one of the below
    1. Exact value matching
    2. Fuzzy string matching with a predefined threshold
    3. Range matching datetime iso with upperbound or lowerbound
    4. Partial matching if the search string is a sublist
    Search results contains all contact entries that matched all criteria

    Args:
        conversation_id:                   Unique ID of the conversation. Exact match.
        conversation_name:                 Name of the conversation. Fuzzy match.
        participants_ids:                  List of Unique participant contact identifiers. Partial Match.
        participants_addresses:            List of participant addresses. Partial Match.
        message_id:                        Unique identifier for the message. Exact match.
        sender_person_id:                  Unique identifier for the sender. Exact match.
        sender_address:                    Sender's address (e.g. email or phone). Exact match.
        content:                           Message content. Fuzzy match.
        creation_datetime_iso_lowerbound:  Lower bound (inclusive) of message creation time in ISO 8601 format.
        creation_datetime_iso_upperbound:  Upper bound (inclusive) of message creation time in ISO 8601 format.
        status:                            Status of the message (e.g. 'sent', 'unread', 'read'). Exact match.


    Returns:
        A List of matching messages. An empty List if no matching contacts were found

    Raises:
        ValueError: When all arguments were not provided

    """
    # Validate search time range
    if isinstance(creation_datetime_iso_lowerbound, str):
        validate_iso8601(creation_datetime_iso_lowerbound)
    if isinstance(creation_datetime_iso_upperbound, str):
        validate_iso8601(creation_datetime_iso_upperbound)

    current_context = get_current_context()
    messaging_dataframe = filter_dataframe(
        dataframe=current_context.get_database(namespace=DatabaseNamespace.MESSAGING),
        filter_criteria=[
            ("message_id", message_id, exact_match_filter_dataframe),
            ("sender_person_id", sender_person_id, exact_match_filter_dataframe),
            (
                "sender_address",
                sender_address,
                functools.partial(normalize_phone_number_filter),
            ),
            ("conversation_id", conversation_id, exact_match_filter_dataframe),
            (
                "conversation_name",
                conversation_name,
                functools.partial(fuzzy_match_filter_dataframe, threshold=50),
            ),
            (
                "participants_ids",
                participants_ids,
                sublist_filter_dataframe,
            ),
            (
                "participants_addresses",
                participants_addresses,
                functools.partial(normalize_phone_numbers_in_list_filter),
            ),
            (
                "content",
                content,
                functools.partial(fuzzy_match_filter_dataframe, threshold=20),
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
            ("status", status, exact_match_filter_dataframe),
        ],
    )
    return cast(
        List[
            Dict[
                Literal[
                    "conversation_id",
                    "conversation_name",
                    "participants_ids",
                    "participants_addresses",
                    "message_id",
                    "sender_person_id",
                    "sender_address",
                    "content",
                    "creation_datetime_iso",
                    "status",
                ],
                str,
            ]
        ],
        messaging_dataframe.to_dicts(),
    )


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def remove_message_or_conversation(
    message_id: Optional[str] = None, conversation_id: Optional[str] = None
) -> None:
    """
    Remove a specific message or an entire conversation from the messaging database.

    Exactly one deletion is performed per call. The two arguments are mutually
    exclusive: if both are provided, message_id takes precedence and only that
    single message is removed (the conversation is left intact).

    Args:
        message_id:        Unique identifier of the individual message to be deleted.
                           Takes precedence over conversation_id when both are given.
        conversation_id:   Unique identifier of the conversation thread to be deleted.
                           Used only when message_id is not provided; deletes every
                           message in the thread.

    Raises:
        ValueError:        If neither message_id nor conversation_id is provided.
    """
    if all(x is None for x in [message_id, conversation_id]):
        raise ValueError(
            "No message id or message conversation id given. At least one new field should be provided among "
            "[message_id, conversation_id] in order to delete messages"
        )
    current_context = get_current_context()
    if isinstance(message_id, str):
        current_context.remove_from_database(
            namespace=DatabaseNamespace.MESSAGING,
            predicate=pl.col("message_id") == message_id,
        )
    elif isinstance(conversation_id, str):
        current_context.remove_from_database(
            namespace=DatabaseNamespace.MESSAGING,
            predicate=pl.col("conversation_id") == conversation_id,
        )


@register_as_tool(visible_to=(RoleType.AGENT,))
def get_all_messages() -> (
    List[
        Dict[
            Literal[
                "conversation_id",
                "conversation_name",
                "participants_ids",
                "participants_addresses",
                "message_id",
                "sender_person_id",
                "sender_address",
                "content",
                "creation_datetime_iso",
                "status",
            ],
            str,
        ]
    ]
):
    """Return all Messages
    Args:
        None
    Returns:
        A List of all messages. An empty List if no messages were found

    """
    current_context = get_current_context()
    message_dataframe = current_context.get_database(DatabaseNamespace.MESSAGING)
    return cast(
        List[
            Dict[
                Literal[
                    "conversation_id",
                    "conversation_name",
                    "participants_ids",
                    "participants_addresses",
                    "message_id",
                    "sender_person_id",
                    "sender_address",
                    "content",
                    "creation_datetime_iso",
                    "status",
                ],
                str,
            ]
        ],
        message_dataframe.to_dicts(),
    )
