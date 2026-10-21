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
    is_email_address,
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
    get_email_by_full_name,
    get_full_name_by_email_or_phonenumber,
    get_participants_full_name_by_email_or_phonenumber,
    get_phonenumber_by_full_name,
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
def send_whatsapp_message(
    recipients: List[str], content: str, creation_datetime_iso: str
) -> str:
    """Send a whatsapp message to recipients

    Args:
        recipients:     recipients full name or addresses.
        content:        Message payload text
        creation_datetime_iso:  ISO8601 format of current time

    Returns:
        String format unique identifier for the message, this can be passed to other functions
        which require a unique identifier for this message

    Raises:
        ValueError:         If less than or more than 1 self entry was found
        ConnectionError:    If cellular service is not on

    """
    validate_iso8601(creation_datetime_iso)
    current_context = get_current_context()
    # get contact_db
    contact_db = copy.deepcopy(
        current_context.get_database(namespace=DatabaseNamespace.CONTACT)
    )
    # get sender self full_name
    self_full_name = contact_db.filter(pl.col("is_self"))[0, "full_name"]
    self_email = contact_db.filter(pl.col("is_self"))[0, "email"]
    # get participants names for conversation finding purposes
    self_phone_number = contact_db.filter(pl.col("is_self"))[0, "phone_number"]

    recipients_addresses = []
    recipients_names = []
    for recipient in recipients:
        recipient_address, recipient_name = None, None
        if is_email_address(recipient) or is_phone_number(recipient):
            recipient_address = recipient
            recipient_name = get_full_name_by_email_or_phonenumber(
                val=recipient, contact_db=contact_db, strict=False
            )
        else:
            recipient_name = recipient
            recipient_address = get_email_by_full_name(
                val=recipient, contact_db=contact_db, strict=True
            ) or get_phonenumber_by_full_name(
                val=recipient, contact_db=contact_db, strict=True
            )
            if not recipient_address:
                raise ValueError(
                    f"{recipient} contact information not found, cannot send whatsapp messages"
                )

        recipients_addresses.append(recipient_address)
        recipients_names.append(recipient_name)

    participants_addresses = sorted([self_phone_number] + recipients_addresses)
    participants_names = sorted([self_full_name] + recipients_names)

    # find conversation id to find conversation name
    whatsapp_db = copy.deepcopy(
        current_context.get_database(namespace=DatabaseNamespace.WHATSAPP)
    )

    # Normalize participant addresses for comparison
    existing_conversations = whatsapp_db.with_columns(
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
        == normalize_participants_addresses(participants_addresses)
    )

    if not filter_conversation_db.is_empty():
        group_name = filter_conversation_db[0, "conversation_name"]
        group_id = filter_conversation_db[0, "conversation_id"]

    else:
        # check if only got one recipients
        if len(recipients_addresses) == 1:
            group_name = get_full_name_by_email_or_phonenumber(
                val=recipients_addresses[0], contact_db=contact_db
            )
        else:
            group_name = " & ".join(
                get_participants_full_name_by_email_or_phonenumber(
                    recipients_addresses,
                    contact_db=contact_db,
                )
            )
        group_id = f"whatsapp-group-{str(uuid4())}"

    # Create message uuid
    message_id = f"whatsapp-message-{str(uuid4())}"

    current_context.add_to_database(
        namespace=DatabaseNamespace.WHATSAPP,
        rows=[
            {
                "conversation_name": group_name,
                "conversation_id": group_id,
                "participants_names": participants_names,
                "participants_addresses": participants_addresses,
                "message_id": message_id,
                "sender_name": self_full_name,
                "sender_address": self_phone_number,
                "creation_datetime_iso": creation_datetime_iso,
                "content": content,
                "status": "sent",
            }
        ],
    )
    return message_id


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def search_whatsapp_messages(
    conversation_id: Union[str, NotGiven] = NOT_GIVEN,
    conversation_name: Union[str, NotGiven] = NOT_GIVEN,
    participants_names: Union[List[str], NotGiven] = NOT_GIVEN,
    participants_addresses: Union[List[str], NotGiven] = NOT_GIVEN,
    message_id: Union[str, NotGiven] = NOT_GIVEN,
    sender_name: Union[str, NotGiven] = NOT_GIVEN,
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
            "participants_names",
            "participants_addresses",
            "message_id",
            "sender_name",
            "sender_address",
            "content",
            "creation_datetime_iso",
            "status",
        ],
        str,
    ]
]:
    """Search for a whatsapp message based on provided arguments

    Each field has a search criteria of one of the below
    1. Exact value matching
    2. Fuzzy string matching with a predefined threshold
    3. Range matching datetime iso with upperbound or lowerbound
    4. Partial matching if the search string is a sublist
    Search results contains all contact entries that matched all criteria

    Args:
        conversation_id:                   Unique ID of the conversation. Exact match.
        conversation_name:                 Name of the conversation. Fuzzy match.
        participants_names:                List of participant full names. Partial Match.
        participants_addresses:            List of participant addresses. Partial Match.
        message_id:                        Unique identifier for the message. Exact match.
        sender_name:                       Full name of the sender. Exact match.
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
        dataframe=current_context.get_database(namespace=DatabaseNamespace.WHATSAPP),
        filter_criteria=[
            ("message_id", message_id, exact_match_filter_dataframe),
            ("sender_name", sender_name, exact_match_filter_dataframe),
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
                "participants_names",
                participants_names,
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
                functools.partial(fuzzy_match_filter_dataframe, threshold=10),
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
                    "participants_names",
                    "participants_addresses",
                    "message_id",
                    "sender_name",
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
def get_all_whatsapp_messages() -> (
    List[
        Dict[
            Literal[
                "conversation_id",
                "conversation_name",
                "participants_names",
                "participants_addresses",
                "message_id",
                "sender_name",
                "sender_address",
                "content",
                "creation_datetime_iso",
                "status",
            ],
            str,
        ]
    ]
):
    """Return all WhatsApp Messages
    Args:
        None
    Returns:
        A List of all whatsapp messages. An empty List if no whatsapp messages were found

    """
    current_context = get_current_context()
    message_dataframe = current_context.get_database(DatabaseNamespace.WHATSAPP)
    return cast(
        List[
            Dict[
                Literal[
                    "conversation_id",
                    "conversation_name",
                    "participants_names",
                    "participants_addresses",
                    "message_id",
                    "sender_name",
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


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def remove_whatsapp_message_or_conversation(
    message_id: Optional[str] = None, conversation_id: Optional[str] = None
) -> None:
    """
    Remove a specific message or an entire conversation from the whatsapp messaging database.

    Args:
        message_id:        Unique identifier of the individual message to be deleted.
        conversation_id:   Unique identifier of the conversation thread to be deleted.

    Raises:
        ValueError:        If neither message_id nor conversation_id is provided.
    """
    if all(x is None for x in [message_id, conversation_id]):
        raise ValueError(
            "No message id or message conversation id given. At least one new field should be provided among "
            "[message_id, conversation_id] in order to delete whatsapp messages"
        )
    current_context = get_current_context()
    if isinstance(conversation_id, str):
        current_context.remove_from_database(
            namespace=DatabaseNamespace.WHATSAPP,
            predicate=pl.col("conversation_id") == conversation_id,
        )
    if isinstance(message_id, str):
        current_context.remove_from_database(
            namespace=DatabaseNamespace.WHATSAPP,
            predicate=pl.col("message_id") == message_id,
        )
