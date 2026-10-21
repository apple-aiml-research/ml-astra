# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""A collection of tools which simulates common functions used for messaging."""

import copy
import functools
import warnings
from typing import Dict, List, Literal, Optional, Union, cast
from uuid import uuid4

import polars as pl
from polars.exceptions import DuplicateError, NoDataError

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
    lt_eq_filter_dataframe,
    register_as_tool,
    sublist_filter_dataframe,
)
from astra_tool_sandbox.common.validators import (
    typechecked,
    validate_iso8601,
)
from astra_tool_sandbox.tools.contact import (
    get_participants_id_by_name_or_phone_or_email,
    get_person_id_by_email_or_phonenumber,
)


class NotEditableError(Exception):
    """Raised when an attempt is made to modify a non-editable email (e.g., not in draft status)."""

    pass


def safe_get_participants_id(
    value: Union[list[str], NotGiven, None], contact_db: pl.DataFrame
) -> Union[list[str], NotGiven, None]:
    if isinstance(value, list):
        return get_participants_id_by_name_or_phone_or_email(value, contact_db)
    return value


def safe_get_person_id(
    value: Union[str, NotGiven, None], contact_db: pl.DataFrame
) -> Union[str, NotGiven, None]:
    if isinstance(value, str):
        return get_person_id_by_email_or_phonenumber(value, contact_db)
    return value


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def send_email(
    creation_datetime_iso: str,
    email_action: str = "draft",
    draft_email_id_to_send: Optional[str] = None,
    email_id_referred: Optional[str] = None,
    email_id_referred_action: Optional[str] = None,
    recipients_addresses: Optional[List[str]] = None,
    email_subject: Optional[str] = None,
    email_body: Optional[str] = None,
    cc_recipients_addresses: Optional[List[str]] = None,
    bcc_recipients_addresses: Optional[List[str]] = None,
    attachment_files: Optional[List[str]] = None,
) -> str:
    """
    Compose and optionally send an email with structured metadata.

    Args:
        creation_datetime_iso: Required. ISO 8601 formatted timestamp indicating when the email was created or drafted.
        email_action: Action to perform, e.g., 'draft', 'send'. Defaults to 'draft'.
        draft_email_id_to_send: Optional. If provided, sends an existing draft email identified by its unique ID without modifying its subject, body, recipients, or attachments.
        email_id_referred: Optional. ID of an existing email, if replying to or forwarding a message.
        email_id_referred_action: Optional. Action to perform on the referred email, e.g., 'reply' or 'forward'.
        recipients_addresses: (Optional) List of primary recipient email addresses.
        email_subject: (Optional) Subject line of the email.
        email_body: (Optional) Main content of the email body.
        cc_recipients_addresses: (Optional) List of carbon copy (CC) recipient email addresses.
        bcc_recipients_addresses: (Optional) List of blind carbon copy (BCC) recipient email addresses.
        attachment_files: (Optional) List of file paths, filenames, or identifiers for attachments.

    Returns:
        str: A unique identifier string for the drafted or sent message.

    Raises:
        ValueError: If required inputs are missing or invalid.
        ConnectionError: If there is no connectivity to the backend service or email server.
    """
    if email_action and email_action not in ("send", "draft"):
        raise ValueError("email_action can only be send or draft")

    if email_id_referred_action and email_id_referred_action not in (
        "forward",
        "reply",
    ):
        raise ValueError("email_id_referred_action can only be forward or reply")

    validate_iso8601(creation_datetime_iso)
    current_context = get_current_context()
    # get contact_db
    contact_db = copy.deepcopy(
        current_context.get_database(namespace=DatabaseNamespace.CONTACT)
    )
    # get sender self person id
    self_person_id = contact_db.filter(pl.col("is_self")).select("person_id").row(0)[0]
    self_email = contact_db.filter(pl.col("is_self")).select("email").row(0)[0]

    # get email_db
    email_db = copy.deepcopy(
        current_context.get_database(namespace=DatabaseNamespace.EMAIL)
    )

    # send an existing draft email
    if draft_email_id_to_send:
        if email_action != "send":
            raise ValueError(
                f"email action {email_action} is not compatiable when draft_email_id_to_send provided, only 'send' is allowed."
            )
        existing_draft_email = email_db.filter(
            pl.col("email_id") == draft_email_id_to_send
        )
        if existing_draft_email.is_empty():
            raise NoDataError(
                f"No draft email with email_id={draft_email_id_to_send} found"
            )
        if existing_draft_email[0, "status"] != "draft":
            raise NotEditableError(
                f"Email with id '{draft_email_id_to_send}' cannot be sent because its status is '{existing_draft_email[0, 'status']}' (only 'draft' emails can be sent with email_id provided)."
            )

        target_entry_dict = existing_draft_email.to_dicts()[0]

        if all(
            x is NOT_GIVEN
            for x in [
                target_entry_dict.get("recipients_addresses"),
                target_entry_dict.get("cc_addresses"),
                target_entry_dict.get("bcc_addresses"),
            ]
        ):
            raise ValueError(
                "No recipients given in the draft email. Provide recipients addresses with modify_draft_email tool and then call send_email with corresponding email_id to send it."
            )

        target_entry_dict["status"] = "sent"
        current_context.remove_from_database(
            namespace=DatabaseNamespace.EMAIL,
            predicate=pl.col("email_id") == draft_email_id_to_send,
        )
        current_context.add_to_database(
            namespace=DatabaseNamespace.EMAIL,
            rows=[target_entry_dict],
        )
        return draft_email_id_to_send

    if (email_id_referred_action in ("forward", "reply")) and not email_id_referred:
        raise ValueError(
            f"Cannot perform {email_id_referred_action} when no email_id_referred provided"
        )

    if email_id_referred and isinstance(email_id_referred, str):
        # check if provided email thread id is valid
        try:
            assert email_id_referred in email_db.select("email_id").unique().to_series()
        except AssertionError:
            # print(email_db.to_dicts())
            raise ValueError(f"Email id {email_id_referred} provided does not exist")

        if (not email_id_referred_action) or (
            email_id_referred_action not in ("forward", "reply")
        ):
            raise ValueError(
                "With email_thread_id provided, need to provide email_id_referred_action from ('reply', 'forward')"
            )

        if (email_id_referred_action == "forward") and not recipients_addresses:
            warnings.warn(
                "No recipients addresses provided for a forwarding action. Will be saved to draft",
                category=UserWarning,
            )
            email_action = "draft"

        existing_email_referred = email_db.filter(
            pl.col("email_id") == email_id_referred
        ).sort("creation_datetime_iso", descending=True)
        email_thread_id = existing_email_referred[0, "thread_id"]

        if not email_subject:
            prev_subject = existing_email_referred[0, "subject"]
            if email_id_referred_action == "forward":
                email_subject = (
                    f"Fwd: {prev_subject}"
                    if "Fwd: " not in prev_subject
                    else prev_subject
                )
            elif email_id_referred_action == "reply":
                email_subject = (
                    f"Re: {prev_subject}"
                    if "Re: " not in prev_subject
                    else prev_subject
                )
            else:
                email_subject = prev_subject

        if email_id_referred_action == "forward":
            # if thread action is forwarding, will keep the original content and attachments
            prev_content = existing_email_referred[0, "body"]
            prev_attachment = existing_email_referred[0, "attachments"]

            if not email_body:
                email_body = "Begin forwarded message: \n" + prev_content
            else:
                email_body += "Begin forwarded message: \n" + prev_content

            if not attachment_files:
                attachment_files = prev_attachment
            else:
                attachment_files.extend(prev_attachment)

        def get_filtered_non_self_email_addresses(
            column_to_match: str, recipients_addresses_: Optional[List[str]]
        ) -> Optional[List[str]]:
            if not recipients_addresses_:
                recipients_addresses_ = existing_email_referred.select(
                    column_to_match
                ).row(0)[0]
                if column_to_match == "recipients_addresses":
                    # add sender to the recipients list
                    if isinstance(recipients_addresses_, list):
                        recipients_addresses_.append(
                            existing_email_referred.select("sender_address").row(0)[0]
                        )
                    else:
                        recipients_addresses_ = [
                            existing_email_referred.select("sender_address").row(0)[0]
                        ]

            if recipients_addresses_:
                return [
                    email_address_
                    for email_address_ in recipients_addresses_
                    if email_address_ != self_email
                ]
            else:
                return recipients_addresses_

        if email_id_referred_action == "reply":
            # using previous email recipients as the target when thread action set to reply
            recipients_addresses = get_filtered_non_self_email_addresses(
                "recipients_addresses", recipients_addresses
            )
            cc_recipients_addresses = get_filtered_non_self_email_addresses(
                "cc_addresses", cc_recipients_addresses
            )
            bcc_recipients_addresses = get_filtered_non_self_email_addresses(
                "bcc_addresses", bcc_recipients_addresses
            )

    # get recipiends person ids
    def find_recipients_ids_by_email_address(
        recipients_addresses_: Optional[List[str]],
    ) -> Optional[List[str]]:
        if recipients_addresses_:
            # check if provided addresses are email
            try:
                assert len(recipients_addresses_) == sum(
                    [
                        1
                        for recipient_ in recipients_addresses_
                        if is_email_address(recipient_)
                    ]
                )
            except AssertionError:
                raise AssertionError(
                    "At least one recipient address provided is not a valid email"
                )
            recipients_ids = get_participants_id_by_name_or_phone_or_email(
                recipients_addresses_, contact_db
            )
        else:
            recipients_ids = None
        return recipients_ids

    recipients_ids = find_recipients_ids_by_email_address(recipients_addresses)
    cc_ids = find_recipients_ids_by_email_address(cc_recipients_addresses)
    bcc_ids = find_recipients_ids_by_email_address(bcc_recipients_addresses)

    # Create email uuid
    email_id = f"email-{str(uuid4())}"
    email_thread_id = None
    # By default save as draft
    status = "draft"
    if email_action == "send":
        if recipients_ids:
            if not email_subject:
                warnings.warn(
                    "Attempting to send an email without subject. Are you sure?",
                    category=UserWarning,
                )
            status = "sent"
        else:
            warnings.warn(
                "Attempting to send an email without any recipients. Email will be saved as draft.",
                category=UserWarning,
            )
            status = "draft"

    current_context.add_to_database(
        namespace=DatabaseNamespace.EMAIL,
        rows=[
            {
                "thread_id": f"thread-{str(uuid4())}"
                if not email_thread_id
                else email_thread_id,
                "email_id": email_id,
                "subject": email_subject,
                "sender_id": self_person_id,
                "sender_address": self_email,
                "recipients_ids": recipients_ids,
                "recipients_addresses": recipients_addresses,
                "cc_ids": cc_ids,
                "cc_addresses": cc_recipients_addresses,
                "bcc_ids": bcc_ids,
                "bcc_addresses": bcc_recipients_addresses,
                "creation_datetime_iso": creation_datetime_iso,
                "body": email_body,
                "attachments": attachment_files,
                "status": status,
            }
        ],
    )
    return email_id


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def remove_email_or_thread(
    email_id: Optional[str] = None, email_thread_id: Optional[str] = None
) -> None:
    """Remove an existing email or an email thread of the email database.

    Args:
        email_id:      String format unique identifier of the email to be deleted
        email_thread_id:  String format unique identifier of the email thread to be deleted
    Returns:

    Raises:
        NoDataError:    If the provided event_id was not found
    """
    if all(x is None for x in [email_id, email_thread_id]):
        raise ValueError(
            "No email id or email thread id given. At least one new field should be provided among "
            "[email_id, email_thread_id] in order to delete email(s)"
        )
    current_context = get_current_context()
    if isinstance(email_thread_id, str):
        current_context.remove_from_database(
            namespace=DatabaseNamespace.EMAIL,
            predicate=pl.col("thread_id") == email_id,
        )
    if isinstance(email_id, str):
        current_context.remove_from_database(
            namespace=DatabaseNamespace.EMAIL,
            predicate=pl.col("email_id") == email_id,
        )


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def modify_draft_email(
    email_id: str,
    creation_datetime_iso: str,
    subject: Union[str, NotGiven] = NOT_GIVEN,
    recipients_addresses: Union[List[str], NotGiven] = NOT_GIVEN,
    cc_recipients_addresses: Union[List[str], NotGiven] = NOT_GIVEN,
    bcc_recipients_addresses: Union[List[str], NotGiven] = NOT_GIVEN,
    body: Union[str, NotGiven] = NOT_GIVEN,
    attachments: Union[List[str], NotGiven] = NOT_GIVEN,
) -> str:
    """Modify an existing draft email entity and return its unique identifier.

    Args:
        email_id: Unique identifier of the email to be modified.
        creation_datetime_iso: ISO 8601 formatted string of the current date and time.
        subject: Optional. Subject of the email.
        recipients_addresses: Optional. List of recipients (full names or emails).
        cc_recipients_addresses: Optional. List of CC'd contacts.
        bcc_recipients_addresses: Optional. List of BCC'd contacts.
        body: Optional. The email message body.
        attachments: Optional. List of attachment identifiers or file names.

    Raises:
        ValueError: When all optional arguments are NOT_GIVEN.
        NoDataError: When the email_id is not found.
        DuplicateError: When multiple entries match the email_id.

    Returns:
        A string identifier of the modified email.
    """
    if all(
        x is NOT_GIVEN
        for x in [
            subject,
            recipients_addresses,
            cc_recipients_addresses,
            bcc_recipients_addresses,
            body,
            attachments,
        ]
    ):
        raise ValueError(
            "No update information given. Provide at least one field to modify."
        )

    current_context = get_current_context()
    contact_db = copy.deepcopy(
        current_context.get_database(namespace=DatabaseNamespace.CONTACT)
    )
    email_database = current_context.get_database(DatabaseNamespace.EMAIL)

    # Lookup existing email
    target_entry = email_database.filter(pl.col("email_id") == email_id)
    if target_entry.is_empty():
        raise NoDataError(f"No entry with email_id={email_id} found")
    if target_entry[0, "status"] != "draft":
        raise NotEditableError(
            f"Email with id '{email_id}' cannot be edited because its status is '{target_entry[0, 'status']}' (only 'draft' emails are editable)."
        )
    target_entry_dicts = target_entry.to_dicts()

    if len(target_entry_dicts) > 1:
        raise DuplicateError(f"Multiple entries with email_id={email_id} found")

    target_entry_dict = target_entry_dicts[0]
    recipients_ids = safe_get_participants_id(recipients_addresses, contact_db)
    cc_ids = safe_get_participants_id(cc_recipients_addresses, contact_db)
    bcc_ids = safe_get_participants_id(bcc_recipients_addresses, contact_db)

    updated_values = {
        "subject": subject,
        "recipients_ids": recipients_ids,
        "recipients_addresses": recipients_addresses,
        "cc_ids": cc_ids,
        "cc_addresses": cc_recipients_addresses,
        "bcc_ids": bcc_ids,
        "bcc_addresses": bcc_recipients_addresses,
        "body": body,
        "attachments": attachments,
    }

    for key, value in updated_values.items():
        if value is not NOT_GIVEN:
            target_entry_dict[key] = value

    target_entry_dict["creation_datetime_iso"] = creation_datetime_iso

    current_context.remove_from_database(
        namespace=DatabaseNamespace.EMAIL,
        predicate=pl.col("email_id") == email_id,
    )
    current_context.add_to_database(
        namespace=DatabaseNamespace.EMAIL,
        rows=[target_entry_dict],
    )
    return email_id


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def search_emails(
    email_id: Union[str, NotGiven] = NOT_GIVEN,
    thread_id: Union[str, NotGiven] = NOT_GIVEN,
    subject: Union[str, NotGiven] = NOT_GIVEN,
    sender_address: Union[str, NotGiven] = NOT_GIVEN,
    recipients_addresses: Union[List[str], NotGiven] = NOT_GIVEN,
    cc_recipients_addresses: Union[List[str], NotGiven] = NOT_GIVEN,
    bcc_recipients_addresses: Union[List[str], NotGiven] = NOT_GIVEN,
    body: Union[str, NotGiven] = NOT_GIVEN,
    creation_datetime_iso_lowerbound: Union[str, NotGiven] = NOT_GIVEN,
    creation_datetime_iso_upperbound: Union[str, NotGiven] = NOT_GIVEN,
    status: Union[str, NotGiven] = NOT_GIVEN,
    attachments: Union[List[str], NotGiven] = NOT_GIVEN,
) -> List[
    Dict[
        Literal[
            "email_id",
            "thread_id",
            "subject",
            "sender_id",
            "sender_address",
            "recipients_ids",
            "recipients_addresses",
            "cc_ids",
            "cc_addresses",
            "bcc_ids",
            "bcc_addresses",
            "body",
            "creation_datetime_iso",
            "status",
            "attachments",
        ],
        str,
    ]
]:
    """Search for an email based on provided arguments.

    Args:
        email_id:                       Unique email ID. Exact match.
        thread_id:                      ID of the thread the email belongs to. Exact match.
        subject:                        Subject of the email. Fuzzy match
        sender_address:                 Email address of the sender. Exact match.
        recipients_addresses:           List of recipient email addresses. Partial match.
        cc_recipients_addresses:        List of CC email addresses. Partial match.
        bcc_recipients_addresses:       List of BCC email addresses. Partial match.
        body:                           Email body content. Fuzzy match.
        creation_datetime_iso_lowerbound: Lower bound (inclusive) of creation datetime in ISO format.
        creation_datetime_iso_upperbound: Upper bound (inclusive) of creation datetime in ISO format.
        status:                         Email status (e.g., 'sent', 'read', 'unread', 'draft'). Exact match.
        attachments:                    List of attachment names or IDs. Partial match.

    Returns:
        A list of matching email entries. Empty list if none match.

    Raises:
        ValueError: If datetime bounds are incorrectly formatted.
    """
    if isinstance(creation_datetime_iso_lowerbound, str):
        validate_iso8601(creation_datetime_iso_lowerbound)
    if isinstance(creation_datetime_iso_upperbound, str):
        validate_iso8601(creation_datetime_iso_upperbound)

    current_context = get_current_context()
    contact_db = copy.deepcopy(
        current_context.get_database(namespace=DatabaseNamespace.CONTACT)
    )

    email_dataframe = filter_dataframe(
        dataframe=current_context.get_database(namespace=DatabaseNamespace.EMAIL),
        filter_criteria=[
            ("email_id", email_id, exact_match_filter_dataframe),
            ("thread_id", thread_id, exact_match_filter_dataframe),
            (
                "subject",
                subject,
                functools.partial(fuzzy_match_filter_dataframe, threshold=50),
            ),
            (
                "sender_id",
                safe_get_person_id(sender_address, contact_db),
                exact_match_filter_dataframe,
            ),
            (
                "recipients_ids",
                safe_get_participants_id(recipients_addresses, contact_db),
                sublist_filter_dataframe,
            ),
            (
                "cc_ids",
                safe_get_participants_id(cc_recipients_addresses, contact_db),
                sublist_filter_dataframe,
            ),
            (
                "bcc_ids",
                safe_get_participants_id(bcc_recipients_addresses, contact_db),
                sublist_filter_dataframe,
            ),
            (
                "body",
                body,
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
            ("attachments", attachments, sublist_filter_dataframe),
        ],
    )

    return cast(
        List[
            Dict[
                Literal[
                    "email_id",
                    "thread_id",
                    "subject",
                    "sender_id",
                    "sender_address",
                    "recipients_ids",
                    "recipients_addresses",
                    "cc_ids",
                    "cc_addresses",
                    "bcc_ids",
                    "bcc_addresses",
                    "body",
                    "creation_datetime_iso",
                    "status",
                    "attachments",
                ],
                str,
            ]
        ],
        email_dataframe.to_dicts(),
    )


@register_as_tool(visible_to=(RoleType.AGENT,))
def get_all_emails() -> (
    List[
        Dict[
            Literal[
                "email_id",
                "thread_id",
                "subject",
                "sender_id",
                "sender_address",
                "recipients_ids",
                "recipients_addresses",
                "cc_ids",
                "cc_addresses",
                "bcc_ids",
                "bcc_addresses",
                "body",
                "creation_datetime_iso",
                "status",
                "attachments",
            ],
            str,
        ]
    ]
):
    """Return all Emails
    Args:
        None
    Returns:
        A List of all emails. An empty List if no emails were found

    """
    current_context = get_current_context()
    emails_dataframe = current_context.get_database(DatabaseNamespace.EMAIL)
    return cast(
        List[
            Dict[
                Literal[
                    "email_id",
                    "thread_id",
                    "subject",
                    "sender_id",
                    "sender_address",
                    "recipients_ids",
                    "recipients_addresses",
                    "cc_ids",
                    "cc_addresses",
                    "bcc_ids",
                    "bcc_addresses",
                    "body",
                    "creation_datetime_iso",
                    "status",
                    "attachments",
                ],
                str,
            ]
        ],
        emails_dataframe.to_dicts(),
    )
