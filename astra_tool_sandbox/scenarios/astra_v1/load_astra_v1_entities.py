# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
import json
import re
from itertools import chain
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

import polars as pl

from astra_tool_sandbox.common.constants import GLOBAL_TIME_PRESET
from astra_tool_sandbox.common.utils import (
    load_str_time_to_datetime_iso_8601,
    parse_duration_to_hms,
    sorted_unique,
)
from astra_tool_sandbox.common.validators import (
    #     clean_and_sort_names,
    #     validate_calendar_event_time,
    #     validate_email_opera,
    #     validate_phone_number_opera,
    #     validate_range,
    validate_iso8601,
)
from astra_tool_sandbox.tools.contact import (
    compose_full_name,
    get_participants_id_by_name_or_phone_or_email,
    get_participants_person_id_or_name,
    get_person_id_by_email_or_phonenumber,
    get_person_id_by_full_name,
)

# contact_is_self, search_contacts_with_dataframe


def load_and_concatenate_json_files(
    file_paths: list[Path], plot_ids: Optional[List[Any]] = None
) -> List[Dict[str, Any]]:
    output_jsons = []
    PLOT_IDs = []

    for file_path in file_paths:
        with open(file_path, "r") as file:
            data = json.load(file)
            if isinstance(data, dict):
                if not isinstance(plot_ids, list):
                    output_jsons_ = list(chain.from_iterable(data.values()))
                    PLOT_IDs.extend(list(data.keys()))
                else:
                    output_jsons_ = [
                        item for key in plot_ids for item in data.get(key, [])
                    ]
            else:
                output_jsons_ = data
            output_jsons.extend(output_jsons_)

    return output_jsons


def time_string_to_minutes(time_string: str) -> int:
    # Define a pattern to match the numbers and time units
    pattern = r"(\d+)\s*(day|days|hour|minute|hours|minutes)?"
    matches = re.findall(pattern, time_string.lower())

    # Initialize total minutes
    total_minutes = 0

    # Iterate over all matched parts
    for quantity, unit in matches:
        quantity = int(quantity)  # Convert the quantity to an integer

        if ("hour" in unit) or ("hr" in unit):
            total_minutes += quantity * 60  # Convert hours to minutes
        elif "day" in unit:
            total_minutes += quantity * 1440  # convert days to minutes
        elif "minute" in unit or unit == "":
            total_minutes += quantity  # Add minutes directly

    return total_minutes


def convert_empty_values_to_none(data_dict: Dict[str, Any]) -> Dict[str, Any]:
    return {
        key: None if isinstance(value, str) and not value.strip() else value
        for key, value in data_dict.items()
    }


def astra_v1_to_contact(
    first_name: str,
    last_name: Optional[str] = None,
    alias: Optional[str] = None,
    cell: Optional[str] = None,
    email: Optional[str] = None,
    relationship: Optional[str] = None,
    address: Optional[str] = None,
    company: Optional[str] = None,
    job_title: Optional[str] = None,
    is_self: bool = False,
    birthday: Optional[str] = None,
    person_id: Optional[str] = None,
    creation_time: Optional[str] = None,
    time_zone_info: str = "America/Los_Angeles",
) -> Dict[str, Any]:
    """Add a new contact person to contact database. Entries with identical information are allowed,
    and will be assigned different person_ids.
    Args:
        first_name:     First Name of contact person
        last_name:      Optional. Last Name of contact person
        alias:          Optional. Alias of contact person
        cell:           Optional. Phone number of contact person
        email:          Optional. Email of contact person
        relationship:   Optional, relationship between user and this contact
        address:        Optional. addresss of contact person
        company:        Optional. company of contact person
        job_title:      Optional. job_title of contact person
        is_self:        Optional. Defaults to False. Should be set to True if the contact corresponds to the current user.
        birthday:       Optional. Birth day of contact person
        person_id:      Optional. If not provided will be generated on the run
        creation_time:  Optional. If not provided will use global preset time
        time_zone_info  Optional. If not provided, by default is PST
    Returns:
        String format unique identifier for the contact person, this can be passed to other functions
        which require a unique identifier for this contact person
    Raises:
        DuplicateError:     When self entry already exists, and we are adding a new one
    """
    # Validate phone number
    # validate_phone_number(phone_number)
    if not person_id:
        person_id = f"contacts-{str(uuid4())}"
    ## TO DO: add duplicate error for same name
    birthday_datetime_iso = load_str_time_to_datetime_iso_8601(
        birthday, time_zone_info=time_zone_info
    )
    if birthday_datetime_iso:
        validate_iso8601(birthday_datetime_iso)

    if creation_time:
        creation_datetime_iso = load_str_time_to_datetime_iso_8601(
            creation_time, time_zone_info=time_zone_info
        )
    else:
        creation_datetime_iso = load_str_time_to_datetime_iso_8601(
            GLOBAL_TIME_PRESET, time_zone_info=time_zone_info
        )

    full_name = compose_full_name(first_name=first_name, last_name=last_name)

    return {
        "person_id": person_id,
        "first_name": first_name,
        "last_name": last_name,
        "full_name": full_name,
        "phone_number": cell,
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


def astra_v1_to_messages(
    messaging_jsons: List[Dict[str, Any]], contact_db: pl.DataFrame
) -> List[Dict[str, Any]]:
    conversations: Dict[str, Dict[str, Any]] = {}

    for cur_msg in messaging_jsons:
        participants = cur_msg.get("participants", [])
        participants_ids = get_participants_id_by_name_or_phone_or_email(
            participants, contact_db
        )
        participants_key = "_".join(participants_ids)

        # update messages to follow the schema
        updates_messages = [
            {
                "message_id": msg.get("message_id") or f"messages-{uuid4()}",
                "sender_person_id": get_person_id_by_email_or_phonenumber(
                    val=msg.get("sender"), contact_db=contact_db
                ),
                "sender_address": msg.get("sender"),
                "content": msg.get("content"),
                "creation_time_iso": load_str_time_to_datetime_iso_8601(
                    msg.get("creation_time", None)
                ),
                "status": msg.get("status"),
            }
            for msg in cur_msg["messages"]
        ]

        # Use setdefault
        convo = conversations.setdefault(
            participants_key,
            {
                "conversation_id": cur_msg.get(
                    "conversation_id", f"conversation-{uuid4()}"
                ),
                "conversation_name": cur_msg.get("conversation_name"),
                "participants_ids": participants_ids,
                "participants_addresses": participants,
                "messages": [],
            },
        )

        # Extend messages and update participants in case it changed
        convo["messages"].extend(updates_messages)
        convo["participants_ids"] = (
            participants_ids  # This line is still necessary if participants can change
        )

    # Sort by creation_time
    for convo in conversations.values():
        convo["messages"].sort(key=lambda msg: msg["creation_time_iso"])

    return [
        {
            "conversation_id": convo["conversation_id"],
            "conversation_name": convo["conversation_name"],
            "participants_ids": convo["participants_ids"],
            "participants_addresses": convo["participants_addresses"],
            "message_id": msg["message_id"],
            "sender_person_id": msg["sender_person_id"],
            "sender_address": msg["sender_address"],
            "content": msg["content"],
            "creation_datetime_iso": msg["creation_time_iso"],
            "status": msg["status"],
        }
        for convo in conversations.values()
        for msg in convo["messages"]
    ]


def astra_v1_to_calendar_event(
    contact_db: pl.DataFrame,
    calendar_name: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    location: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    invitees: Optional[List[str]] = None,
    reminder: Optional[str] = None,
    organizer: Optional[str] = None,
    meeting_url: Optional[str] = None,
    creation_time: Optional[str] = None,
    calendar_event_id: Optional[str] = None,
    time_zone_info: str = "America/Los_Angeles",
) -> Dict[str, Any]:
    """Convert a raw calendar event into the standardized calendar schema format.

    Args:
        calendar_name:         Name of the calendar to which the event belongs (e.g. 'personal', 'work').
        title:                 Title or name of the calendar event.
        description:           Optional. Notes or description of the event.
        location:              Optional. Location where the event takes place.
        start_time:            ISO 8601 formatted start time of the event.
        end_time:              ISO 8601 formatted end time of the event.
        invitees:              Optional. List of names of individuals invited to the event.
        reminder:              Optional. Time ahead of the event to send a reminder (e.g. '60 minutes').
        organizer:             Optional. Name of the event organizer.
        meeting_url:           Optional. URL for a virtual meeting associated with the event.
        creation_time:         Optional. ISO 8601 formatted timestamp of when the event was created.
        calendar_event_id:     Optional. Unique identifier for the calendar event. If not provided, it will be generated.

    Returns:
        A dictionary formatted according to the standardized calendar schema, with required fields transformed
        and validated as needed.

    Notes:
        - The `calendar_event_id` will be auto-generated if not supplied.
        - Times must be in ISO 8601 format.
        - Invitees list is optional but recommended for events with attendees.
    """
    if not calendar_event_id:
        calendar_event_id = f"calendar-{str(uuid4())}"
    ## TO DO: add duplicate error for same name
    start_datetime_iso = load_str_time_to_datetime_iso_8601(
        start_time, time_zone_info=time_zone_info
    )
    end_datetime_iso = load_str_time_to_datetime_iso_8601(
        end_time, time_zone_info=time_zone_info
    )
    creation_datetime_iso = load_str_time_to_datetime_iso_8601(
        creation_time, time_zone_info=time_zone_info
    )
    # get invitees person id if possible
    if isinstance(invitees, List):
        invitees_ids = get_participants_person_id_or_name(invitees, contact_db)
    else:
        invitees_ids = []

    if isinstance(organizer, List):
        if len(organizer) > 1:
            raise ValueError("Orgaznizer is more than one")
        else:
            organizer = organizer[0]

    organizer_id = (
        get_person_id_by_full_name(organizer, contact_db)
        if isinstance(organizer, str)
        else organizer
    )

    return {
        "calendar_name": calendar_name,
        "calendar_event_id": calendar_event_id,
        "calendar_event_name": title,
        "start_datetime_iso": start_datetime_iso,
        "end_datetime_iso": end_datetime_iso,
        "attendees_ids": sorted_unique((invitees_ids or []) + ([organizer_id])),
        "attendees_names": sorted_unique((invitees or []) + [organizer]),
        "location": location,
        "reminder_time_ahead": reminder,
        "organizer_id": organizer_id,
        "organizer_name": organizer,
        "meeting_url": meeting_url,
        "creation_datetime_iso": creation_datetime_iso,
        "notes": description,
    }


def split_email_addresses(email_str: Optional[Union[str, None]]) -> Optional[List[str]]:
    if isinstance(email_str, str):
        separators = [",", ";"]
        for sep in separators:
            if sep in email_str:
                email_list = [
                    item.strip()
                    for item in email_str.split(sep)
                    if "@" in item and item.strip()
                ]
                return email_list if email_list else None
        # Handle single email (or empty string)
        single = email_str.strip()
        if "@" in single:
            return [single]
    return None


def split_str_to_list(long_str: Optional[Union[str, None]]) -> Optional[List[str]]:
    if isinstance(long_str, str):
        separators = [",", ";"]
        for sep in separators:
            if sep in long_str:
                long_list = [
                    item.strip() for item in long_str.split(sep) if item.strip()
                ]
                return long_list if long_list else None
        single = long_str.strip()
        return [single] if single else None
    return None


def convert_astra_v1_email_schema(
    contact_db: pl.DataFrame,
    email_id: Optional[str] = None,
    subject: Optional[str] = None,
    sender: Optional[str] = None,
    recipients: Optional[str] = None,
    cc: Optional[str] = None,
    bcc: Optional[str] = None,
    creation_time: Optional[str] = None,
    body: Optional[str] = None,
    attachment: Optional[str] = None,
) -> Dict[str, Any]:
    if not isinstance(email_id, str):
        email_id = f"email-{str(uuid4())}"
    recipients_list = split_email_addresses(recipients)
    cc_list = split_email_addresses(cc)
    bcc_list = split_email_addresses(bcc)

    if creation_time:
        creation_datetime_iso = load_str_time_to_datetime_iso_8601(creation_time)
    else:
        creation_datetime_iso = None
    return {
        # "mailbox": None,
        "thread_id": None,
        "email_id": email_id,
        "subject": subject,
        "sender_id": get_person_id_by_email_or_phonenumber(
            sender, contact_db=contact_db
        )
        if sender
        else sender,
        "sender_address": sender,
        "recipients_ids": get_participants_id_by_name_or_phone_or_email(
            recipients_list, contact_db=contact_db
        )
        if recipients_list
        else None,
        "recipients_addresses": recipients_list,
        "cc_ids": get_participants_id_by_name_or_phone_or_email(
            cc_list, contact_db=contact_db
        )
        if cc_list
        else None,
        "cc_addresses": cc_list,
        "bcc_ids": get_participants_id_by_name_or_phone_or_email(
            bcc_list, contact_db=contact_db
        )
        if bcc_list
        else None,
        "bcc_addresses": bcc_list,
        "creation_datetime_iso": creation_datetime_iso,
        "body": body,
        "attachments": split_str_to_list(attachment)
        if isinstance(attachment, str)
        else None,
        "status": None,
    }


def astra_v1_to_emails(
    email_jsons: List[Dict[str, Any]], contact_db: pl.DataFrame
) -> List[Dict[str, Any]]:
    email_list = [
        convert_astra_v1_email_schema(**email_json, contact_db=contact_db)
        for email_json in email_jsons
    ]
    for idx1, email1 in enumerate(email_list):
        if not email1.get("thread_id"):
            email1["thread_id"] = f"email-thread-{str(uuid4())}"
        else:
            continue
        email1_thread_id = email1.get("thread_id")
        subject = email1.get("subject")
        sender_id = email1.get("sender_id")
        participants = (
            [sender_id]
            + (email1.get("recipients_ids") or [])
            + (email1.get("cc_ids") or [])
            + (email1.get("bcc_ids") or [])
        )
        for email2 in email_list[(idx1 + 1) :]:
            if (
                not email2.get("thread_id")
                and subject in email2.get("subject", "")
                and email2.get("sender_id", "") in participants
                # and email2.get("creation_datetime_iso") >= email1.get("creation_datetime_iso")
            ):
                # if not labeled a thread_id
                # subject can be matched
                # print(f"thread {email1_thread_id} detected for email {email2['email_id']}")
                email2["thread_id"] = email1_thread_id
            else:
                continue

    return email_list


def convert_to_whatsapp_schema(
    self_full_name: str,
    self_email: str,
    self_phone_number: str,
    sender: str,
    sender_name: str,
    recipient: str,
    recipient_name: str,
    message_id: Optional[str] = None,
    creation_time: Optional[str] = None,
    message: Optional[str] = None,
    status: Optional[str] = None,
    group_name: Optional[str] = None,
) -> Dict[str, Any]:
    if not isinstance(message_id, str):
        message_id = f"whatsapp-message-{str(uuid4())}"

    if creation_time:
        creation_datetime_iso = load_str_time_to_datetime_iso_8601(creation_time)
    else:
        creation_datetime_iso = None

    participants_names = [sender_name, recipient_name]
    participants_addresses = [sender, recipient]

    non_self_participants = [
        full_name
        for idx, full_name in enumerate(participants_names)
        if participants_addresses[idx] not in (self_phone_number, self_email)
    ]
    if len(participants_names) > 2:
        if not group_name:
            group_name = " & ".join(non_self_participants)
    elif len(participants_names) == 2:
        group_name = non_self_participants[0]

    participants_names = sorted([sender_name, recipient_name])
    participants_addresses = sorted([sender, recipient])

    return {
        "conversation_name": group_name,
        "participants_names": participants_names,
        "participants_addresses": participants_addresses,
        "message_id": message_id,
        "sender_name": sender_name,
        "sender_address": sender,
        "creation_datetime_iso": creation_datetime_iso,
        "content": message,
        "status": None,
    }


def astra_v1_to_whatsapp_messages(
    whatsapp_jsons: List[Dict[str, Any]],
    self_full_name: str,
    self_email: str,
    self_phone_number: str,
) -> List[Dict[str, Any]]:
    whatsapp_messages = [
        convert_to_whatsapp_schema(
            **convert_empty_values_to_none(whatsapp_json),
            self_full_name=self_full_name,
            self_email=self_email,
            self_phone_number=self_phone_number,
        )
        for whatsapp_json in whatsapp_jsons
    ]

    group_by_participants = {}
    group_name_id_pair = {}
    for whatsapp_message in whatsapp_messages:
        cur_group_name = whatsapp_message.get("conversation_name")
        if cur_group_name not in group_by_participants:
            cur_group_id = f"whatsapp-group-{str(uuid4())}"
            whatsapp_message.update({"conversation_id": cur_group_id})
            group_by_participants.update({cur_group_name: [whatsapp_message]})
            group_name_id_pair.update({cur_group_name: cur_group_id})
        else:
            cur_group_id = group_name_id_pair[cur_group_name]
            whatsapp_message.update({"conversation_id": cur_group_id})
            group_by_participants[cur_group_name].append(whatsapp_message)

    return [
        whatsapp_msg
        for group_name_, whatsapp_msgs in group_by_participants.items()
        for whatsapp_msg in sorted(
            whatsapp_msgs, key=lambda x: x["creation_datetime_iso"]
        )
    ]


def astra_v1_to_phonecall(
    contact_db: pl.DataFrame,
    call_type: Optional[str] = None,
    caller: Optional[str] = None,
    receiver: Optional[str] = None,
    creation_time: Optional[str] = None,
    duration: Optional[str] = None,
    voice_mail_trasnscription: Optional[str] = None,
    phonecall_id: Optional[str] = None,
    time_zone_info: str = "America/Los_Angeles",
) -> Dict[str, Any]:
    """Convert a raw calendar event into the standardized calendar schema format.

    Args:
        calendar_name:         Name of the calendar to which the event belongs (e.g. 'personal', 'work').
        title:                 Title or name of the calendar event.
        description:           Optional. Notes or description of the event.
        location:              Optional. Location where the event takes place.
        start_time:            ISO 8601 formatted start time of the event.
        end_time:              ISO 8601 formatted end time of the event.
        invitees:              Optional. List of names of individuals invited to the event.
        reminder:              Optional. Time ahead of the event to send a reminder (e.g. '60 minutes').
        organizer:             Optional. Name of the event organizer.
        meeting_url:           Optional. URL for a virtual meeting associated with the event.
        creation_time:         Optional. ISO 8601 formatted timestamp of when the event was created.
        calendar_event_id:     Optional. Unique identifier for the calendar event. If not provided, it will be generated.

    Returns:
        A dictionary formatted according to the standardized calendar schema, with required fields transformed
        and validated as needed.

    Notes:
        - The `calendar_event_id` will be auto-generated if not supplied.
        - Times must be in ISO 8601 format.
        - Invitees list is optional but recommended for events with attendees.
    """
    if not phonecall_id:
        phonecall_id = f"phone-{str(uuid4())}"

    ## TO DO: add duplicate error for same name
    creation_datetime_iso = load_str_time_to_datetime_iso_8601(
        creation_time, time_zone_info=time_zone_info
    )
    # get invitees person id if possible
    if isinstance(caller, str):
        caller_id = get_person_id_by_email_or_phonenumber(
            caller, contact_db, strict=True
        )
    else:
        caller_id = None

    if isinstance(receiver, str):
        receiver_id = get_person_id_by_email_or_phonenumber(
            receiver, contact_db, strict=True
        )
    else:
        receiver_id = None

    if isinstance(duration, str):
        duration_hms = parse_duration_to_hms(duration)

    self_person_id = contact_db.filter(pl.col("is_self"))[0, "person_id"]

    if caller_id == self_person_id:
        call_type = "outgoing"

    return {
        "phone_call_id": phonecall_id,
        "call_type": call_type,
        "caller_address": caller,
        "caller_id": caller_id,
        "receiver_address": receiver,
        "receiver_id": receiver_id,
        "voice_mail_transcription": voice_mail_trasnscription,
        "creation_datetime_iso": creation_datetime_iso,
        "duration_in_hms": duration_hms,
    }
