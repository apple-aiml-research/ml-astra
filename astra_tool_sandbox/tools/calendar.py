# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""A collection of tools which simulates common functions used for calendars."""

import copy
import datetime
import functools
from typing import Any, Dict, List, Literal, Optional, Union, cast
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
    lt_eq_filter_dataframe,
    register_as_tool,
    sorted_unique,
    sublist_filter_dataframe,
    sublist_partial_filter_dataframe,
    substring_or_fuzzy_match_filter_dataframe,
)
from astra_tool_sandbox.common.validators import (
    typechecked,
    validate_if_iso8601_str,
    validate_iso8601,
)
from astra_tool_sandbox.tools.contact import (
    get_full_name_by_person_id,
    get_participants_full_name_by_person_id,
    get_participants_person_id_or_name,
    get_person_id_by_email_or_phonenumber,
    get_person_id_by_full_name,
)


# Define a warning class for overlapping events
class ConflictCalendarEventWarning(UserWarning):
    pass


# Define an error class for overlapping events
class ConflictCalendarEventError(Exception):
    pass


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def create_calendar_event(
    creation_datetime_iso: str,
    start_datetime_iso: str,
    calendar_event_name: str = "New Event",
    calendar_name: str = "personal",
    reminder_time_ahead: str = "15 minutes",
    end_datetime_iso: Optional[str] = None,
    invitees: Optional[List[str]] = None,
    location: Optional[str] = None,
    organizer: Optional[str] = None,
    meeting_url: Optional[str] = None,
    notes: Optional[str] = None,
) -> str:
    """Create a new calendar event and return its unique identifier.

    Args:
        creation_datetime_iso:      ISO 8601 formatted timestamp indicating when the event was created.
        start_datetime_iso:         ISO 8601 formatted start time of the event.
        end_datetime_iso:           (Optional) ISO 8601 formatted end time of the event. If not provided, defaults to 30 minutes after the start time.
        calendar_event_name:        Title of the event. Defaults to "New Event".
        calendar_name:              Name of the calendar to add the event to (e.g., "personal", "work"). Defaults to "personal".
        invitees:                   (Optional) List of full names, emails, or phone numbers of the invited participants.
        location:                   (Optional) Physical or virtual location where the event will take place.
        reminder_time_ahead:        Time before the event to trigger a reminder (e.g., "15 minutes"). Defaults to "15 minutes".
        organizer:                  (Optional) Name or contact info of the event organizer. If not provided, defaults to the current user.
        meeting_url:                (Optional) Link to a virtual meeting (e.g., Zoom, Google Meet).
        notes:                      (Optional) Additional description or notes about the event.
    Returns:
        A unique string identifier for the created calendar event, which can be used
        to reference or update the event in other operations.
    """
    validate_iso8601(time_string=creation_datetime_iso)
    current_context = get_current_context()
    # get contact_db
    contact_db = copy.deepcopy(
        current_context.get_database(namespace=DatabaseNamespace.CONTACT)
    )
    organizer_id: Optional[str] = None

    if isinstance(organizer, str):
        organizer_id = get_person_id_by_full_name(
            organizer, contact_db
        ) or get_person_id_by_email_or_phonenumber(organizer, contact_db)

    else:
        # if no organizer provided, use the protagonist themselves as organizer
        organizer_id = contact_db.filter(pl.col("is_self"))[0, "person_id"]
        organizer = contact_db.filter(pl.col("is_self"))[0, "full_name"]

    # get invitees person id if possible
    invitees_ids: Optional[List[Any]] = None
    invitees_names: Optional[List[Any]] = None

    if isinstance(invitees, list):
        invitees_ids = get_participants_person_id_or_name(invitees, contact_db)
        invitees_names = get_participants_full_name_by_person_id(
            invitees_ids, contact_db
        )

    if not isinstance(end_datetime_iso, str):
        # if no end_datetime_iso provided
        end_datetime_iso = (
            datetime.datetime.fromisoformat(start_datetime_iso)
            + datetime.timedelta(minutes=30)
        ).isoformat()

    # creation_datetime_iso = datetime.datetime.now().isoformat(),

    calendar_event_id = f"calendar-{str(uuid4())}"
    current_context.add_to_database(
        namespace=DatabaseNamespace.CALENDAR,
        rows=[
            {
                "calendar_event_id": calendar_event_id,
                "calendar_name": calendar_name,
                "calendar_event_name": calendar_event_name,
                "creation_datetime_iso": creation_datetime_iso,
                "start_datetime_iso": start_datetime_iso,
                "end_datetime_iso": end_datetime_iso,
                "attendees_ids": sorted_unique((invitees_ids or []) + ([organizer_id])),
                "attendees_names": sorted_unique((invitees_names or []) + [organizer]),
                "location": location,
                "reminder_time_ahead": reminder_time_ahead,
                "organizer_id": organizer_id,
                "organizer_name": organizer,
                "meeting_url": meeting_url,
                "notes": notes,
            }
        ],
    )
    return calendar_event_id


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def remove_calendar_event(calendar_event_id: str) -> None:
    """Remove an existing calendar event of the calendar database.

    Args:
        calendar_event_id:      String format unique identifier of the calendar event to be deleted

    Returns:

    Raises:
        NoDataError:    If the provided event_id was not found
    """

    current_context = get_current_context()
    current_context.remove_from_database(
        namespace=DatabaseNamespace.CALENDAR,
        predicate=pl.col("calendar_event_id") == calendar_event_id,
    )


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def modify_calendar_event(
    calendar_event_id: str,
    creation_datetime_iso: str,
    calendar_name: Union[str, NotGiven] = NOT_GIVEN,
    start_datetime_iso: Union[str, NotGiven] = NOT_GIVEN,
    end_datetime_iso: Union[str, NotGiven] = NOT_GIVEN,
    calendar_event_name: Union[str, NotGiven] = NOT_GIVEN,
    attendees: Union[List[str], NotGiven] = NOT_GIVEN,
    location: Union[str, NotGiven] = NOT_GIVEN,
    reminder_time_ahead: Union[str, NotGiven] = NOT_GIVEN,
    organizer: Union[str, NotGiven] = NOT_GIVEN,
    meeting_url: Union[str, NotGiven] = NOT_GIVEN,
    notes: Union[str, NotGiven] = NOT_GIVEN,
) -> str:
    """Create a new calendar event and return its unique identifier.

    Args:
        calendar_event_id:      String format unique identifier of the calendar to be modified
        creation_datetime_iso:  Creation time in ISO 8601 of the current date and time.
        start_datetime_iso:     ISO 8601 formatted start timestamp of the event.
        calendar_event_name:    Optional. The name or title of the calendar event.
        end_datetime_iso:       Optional. ISO 8601 formatted end timestamp of the event. Defaults set to 30 minutes after start_datetime_iso.
        calendar_name:          Optional. Name of the calendar (e.g., 'personal', 'work'). Defaults to 'personal'.
        attendees:              Optional. List of person attends the event. Can be unique contact person id or full name.
        location:               Optional. Physical or virtual location of the event.
        reminder_time_ahead:    Optional. Time ahead of the event to trigger a reminder. Defaults set to '15 minutes'.
        organizer:              Optional. Individual organizing or creating the event. By default is None.
        meeting_url:            Optional. URL to an associated virtual meeting (e.g., Zoom, Google Meet).
        notes:                  Optional. Additional text or description for the event.
    Raises:
        ValueError:     When all arguments were None
        NoDataError:    When the reminder_id cannot be found in database
        DuplicateError: When multiple entries with the same id were found
    Return:

        A unique string identifier for the modified calendar event.
    """
    if all(
        x is NOT_GIVEN
        for x in [
            calendar_name,
            calendar_event_name,
            start_datetime_iso,
            end_datetime_iso,
            attendees,
            organizer,
            location,
            notes,
            meeting_url,
            reminder_time_ahead,
        ]
    ):
        raise ValueError(
            "No update information given. At least one new field should be provided among "
            "[calendar_name, calendar_event_name, start_datetime_iso, end_datetime_iso, invitees, location, notes, reminder_time_ahead] in order to modify the calendar event"
        )

    current_context = get_current_context()
    # get contact_db
    contact_db = copy.deepcopy(
        current_context.get_database(namespace=DatabaseNamespace.CONTACT)
    )
    calendar_database = current_context.get_database(DatabaseNamespace.CALENDAR)
    # Check if entry exists
    target_entry = calendar_database.filter(
        pl.col("calendar_event_id") == calendar_event_id
    )
    if target_entry.is_empty():
        raise NoDataError(f"No db entry matching {calendar_event_id=} found")
    # Check if entry is unique
    target_entry_dicts = target_entry.to_dicts()
    if len(target_entry_dicts) > 1:
        raise DuplicateError(f"More than 1 entry with {calendar_event_id=} found")
    target_entry_dict = target_entry_dicts[0]

    # Define a helper function to get the appropriate value or default
    def get_value_or_default(
        value: Optional[Union[str, None, NotGiven]] = None,
        default: Optional[Union[str, None, NotGiven]] = None,
    ) -> Optional[Union[str, None, NotGiven]]:
        return value if isinstance(value, str) else default

    updated_start_datetime_iso = get_value_or_default(
        start_datetime_iso, target_entry_dict["start_datetime_iso"]
    )
    updated_end_datetime_iso = get_value_or_default(
        end_datetime_iso, target_entry_dict["end_datetime_iso"]
    )

    if cast(str, updated_start_datetime_iso) > cast(str, updated_end_datetime_iso):
        raise ValueError(
            f"Provided new time is invalid with start_datetime_iso: {start_datetime_iso} and end_datetime_iso: {end_datetime_iso}"
        )

    # update invitees/organizers
    if isinstance(organizer, str):
        organizer_id = get_person_id_by_full_name(
            organizer, contact_db
        ) or get_person_id_by_email_or_phonenumber(organizer, contact_db)
        organizer_name = get_full_name_by_person_id(organizer_id, contact_db)
    else:
        # if no organizer provided, use the protagonist themselves as organizer
        organizer_id = target_entry_dict["organizer_id"]
        organizer_name = target_entry_dict["organizer_name"]

    # get invitees person id if possible
    attendees_ids: Optional[List[Any]] = None
    if isinstance(attendees, list):
        attendees_ids = get_participants_person_id_or_name(attendees, contact_db)
        if organizer_id not in attendees_ids:
            # update attendees ids and names if organizer changes
            attendees_ids.append(organizer_id)
        attendees_names = get_participants_full_name_by_person_id(
            attendees_ids, contact_db
        )

    else:
        attendees_ids = target_entry_dict["attendees_ids"]
        attendees_names = target_entry_dict["attendees_names"]

    # Create updated entry
    new_entry = target_entry_dict.copy()

    for name, value in [
        ("calendar_name", calendar_name),
        ("calendar_event_name", calendar_event_name),
        ("start_datetime_iso", updated_start_datetime_iso),
        ("end_datetime_iso", updated_end_datetime_iso),
        ("attendees_ids", sorted(attendees_ids or [])),
        ("attendees_names", sorted(attendees_names or [])),
        ("organizer_id", organizer_id),
        ("organizer_name", organizer_name),
        ("location", location),
        ("meeting_url", meeting_url),
        ("reminder_time_ahead", reminder_time_ahead),
        ("notes", notes),
    ]:
        if value is not NOT_GIVEN:
            new_entry[name] = value

    # Validate keys before deleting anything
    allowed_fields = {
        "calendar_event_id",
        "attendees_names",
        "calendar_name",
        "calendar_event_name",
        "creation_datetime_iso",
        "start_datetime_iso",
        "end_datetime_iso",
        "attendees_ids",
        "attendees_names",
        "organizer_id",
        "organizer_name",
        "location",
        "meeting_url",
        "reminder_time_ahead",
        "notes",
    }
    unknown_fields = set(new_entry) - allowed_fields
    if unknown_fields:
        raise KeyError(f"Unknown fields: {unknown_fields}")

    # Update database
    current_context.remove_from_database(
        namespace=DatabaseNamespace.CALENDAR,
        predicate=pl.col("calendar_event_id") == calendar_event_id,
    )
    # get current timestamp for a new creation time
    new_entry["creation_datetime_iso"] = creation_datetime_iso
    current_context.add_to_database(
        namespace=DatabaseNamespace.CALENDAR,
        rows=[new_entry],
    )
    return calendar_event_id


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def search_calendar_events(
    calendar_event_id: Union[str, NotGiven] = NOT_GIVEN,
    creation_datetime_iso_lowerbound: Union[str, NotGiven] = NOT_GIVEN,
    creation_datetime_iso_upperbound: Union[str, NotGiven] = NOT_GIVEN,
    start_datetime_iso_lowerbound: Union[str, NotGiven] = NOT_GIVEN,
    start_datetime_iso_upperbound: Union[str, NotGiven] = NOT_GIVEN,
    end_datetime_iso_lowerbound: Union[str, NotGiven] = NOT_GIVEN,
    end_datetime_iso_upperbound: Union[str, NotGiven] = NOT_GIVEN,
    calendar_event_name: Union[str, NotGiven] = NOT_GIVEN,
    calendar_name: Union[str, NotGiven] = NOT_GIVEN,
    attendees: Union[List[str], NotGiven] = NOT_GIVEN,
    location: Union[str, NotGiven] = NOT_GIVEN,
    reminder_time_ahead: Union[str, NotGiven] = NOT_GIVEN,
    organizer: Union[str, NotGiven] = NOT_GIVEN,
    meeting_url: Union[str, NotGiven] = NOT_GIVEN,
    notes: Union[str, NotGiven] = NOT_GIVEN,
) -> List[
    Dict[
        Literal[
            "calendar_event_id",
            "creation_datetime_iso",
            "start_datetime_iso",
            "end_datetime_iso",
            "calendar_event_name",
            "calendar_name",
            "attendees_ids",
            "attendees_names",
            "location",
            "reminder_time_ahead",
            "organizer_id",
            "organizer_name",
            "meeting_url",
            "notes",
        ],
        str,
    ]
]:
    """Search for calendar events based on provided criteria.

    Supports a range of match types for different fields, including:
    1. Exact value matching for identifiers and string fields
    2. Fuzzy matching for event names and notes
    3. Range-based datetime filtering (for creation, start, and end times)
    4. Partial list matching for invitees

    Args:
        calendar_event_id:               Unique ID of the calendar event. Exact match.
        creation_datetime_iso_lowerbound:  Lower bound of creation time in ISO 8601 format.
        creation_datetime_iso_upperbound:  Upper bound of creation time in ISO 8601 format.
        start_datetime_iso_lowerbound:     Lower bound of start time in ISO 8601 format.
        start_datetime_iso_upperbound:     Upper bound of start time in ISO 8601 format.
        end_datetime_iso_lowerbound:       Lower bound of end time in ISO 8601 format.
        end_datetime_iso_upperbound:       Upper bound of end time in ISO 8601 format.
        calendar_event_name:             Name of the calendar event. Fuzzy match.
        calendar_name:                   Name of the calendar the event belongs to. Exact match.
        attendees:                       List of attendees full names or unique contact person IDs. Partial match.
        location:                        Event location. Fuzzy match.
        reminder_time_ahead:            Reminder lead time (e.g., '30 minutes'). Exact match.
        organizer:                       Name or ID of the event organizer. Exact match.
        meeting_url:                     URL to the associated virtual meeting. Exact match.
        notes:                           Additional notes or description. Fuzzy match.

    Returns:
        A list of matching calendar event entries. Returns an empty list if no matches are found.

    Raises:
        ValueError: If no valid search criteria were provided.
    """
    current_context = get_current_context()
    calendar_db = current_context.get_database(namespace=DatabaseNamespace.CALENDAR)
    contact_db = current_context.get_database(namespace=DatabaseNamespace.CONTACT)
    # validate strings
    validate_if_iso8601_str(
        creation_datetime_iso_lowerbound, "creation_datetime_iso_lowerbound"
    )
    validate_if_iso8601_str(
        creation_datetime_iso_upperbound, "creation_datetime_iso_upperbound"
    )
    validate_if_iso8601_str(
        start_datetime_iso_lowerbound, "start_datetime_iso_lowerbound"
    )
    validate_if_iso8601_str(
        start_datetime_iso_upperbound, "start_datetime_iso_upperbound"
    )
    validate_if_iso8601_str(end_datetime_iso_lowerbound, "end_datetime_iso_lowerbound")
    validate_if_iso8601_str(end_datetime_iso_upperbound, "end_datetime_iso_upperbound")

    # update invitees/organizers
    organizer_id: Union[str, NotGiven] = NOT_GIVEN
    if isinstance(organizer, str):
        organizer_id = get_person_id_by_full_name(
            organizer, contact_db
        ) or get_person_id_by_email_or_phonenumber(organizer, contact_db)
    elif isinstance(organizer, NotGiven):
        # if no organizer provided, use the protagonist themselves as organizer
        organizer_id = NOT_GIVEN

    # get invitees person id if possible
    attendees_ids: Union[List[Any], NotGiven] = NOT_GIVEN
    if isinstance(attendees, List):
        attendees_ids = get_participants_person_id_or_name(attendees, contact_db)
    elif isinstance(attendees, NotGiven):
        attendees_ids = NOT_GIVEN

    # Filtering criteria
    calendar_dataframe = filter_dataframe(
        dataframe=current_context.get_database(namespace=DatabaseNamespace.CALENDAR),
        filter_criteria=[
            ("calendar_event_id", calendar_event_id, exact_match_filter_dataframe),
            ("calendar_name", calendar_name, exact_match_filter_dataframe),
            (
                "calendar_event_name",
                calendar_event_name,
                functools.partial(
                    substring_or_fuzzy_match_filter_dataframe, threshold=80
                ),
            ),
            ("attendees_ids", attendees_ids, sublist_filter_dataframe),
            (
                "attendees_names",
                attendees,
                functools.partial(sublist_partial_filter_dataframe, threshold=80),
            ),
            ("organizer_id", organizer_id, exact_match_filter_dataframe),
            (
                "notes",
                notes,
                functools.partial(fuzzy_match_filter_dataframe, threshold=30),
            ),
            # These three were accepted by the signature and documented above with their
            # intended matchers, but were missing here — so passing only one of them raised
            # "No search criteria are given", punishing an agent for using a documented
            # parameter. Matchers follow the docstring: location fuzzy, the other two exact.
            (
                "location",
                location,
                functools.partial(
                    substring_or_fuzzy_match_filter_dataframe, threshold=80
                ),
            ),
            ("meeting_url", meeting_url, exact_match_filter_dataframe),
            (
                "reminder_time_ahead",
                reminder_time_ahead,
                exact_match_filter_dataframe,
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
                "start_datetime_iso",
                start_datetime_iso_lowerbound,
                gt_eq_filter_dataframe,
            ),
            (
                "start_datetime_iso",
                start_datetime_iso_upperbound,
                lt_eq_filter_dataframe,
            ),
            (
                "end_datetime_iso",
                end_datetime_iso_lowerbound,
                gt_eq_filter_dataframe,
            ),
            (
                "end_datetime_iso",
                end_datetime_iso_upperbound,
                lt_eq_filter_dataframe,
            ),
        ],
    )

    return cast(
        List[
            Dict[
                Literal[
                    "calendar_event_id",
                    "creation_datetime_iso",
                    "start_datetime_iso",
                    "end_datetime_iso",
                    "calendar_event_name",
                    "calendar_name",
                    "attendees_ids",
                    "attendees_names",
                    "location",
                    "reminder_time_ahead",
                    "organizer_id",
                    "organizer_name",
                    "meeting_url",
                    "notes",
                ],
                str,
            ]
        ],
        calendar_dataframe.to_dicts(),
    )


@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def get_all_calendars() -> (
    List[
        Dict[
            Literal[
                "calendar_event_id",
                "creation_datetime_iso",
                "start_datetime_iso",
                "end_datetime_iso",
                "calendar_event_name",
                "calendar_name",
                "attendees_ids",
                "attendees_names",
                "location",
                "reminder_time_ahead",
                "organizer_id",
                "organizer_name",
                "meeting_url",
                "notes",
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
    calendar_dataframe = current_context.get_database(DatabaseNamespace.CALENDAR)
    return cast(
        List[
            Dict[
                Literal[
                    "calendar_event_id",
                    "creation_datetime_iso",
                    "start_datetime_iso",
                    "end_datetime_iso",
                    "calendar_event_name",
                    "calendar_name",
                    "attendees_ids",
                    "attendees_names",
                    "location",
                    "reminder_time_ahead",
                    "organizer_id",
                    "organizer_name",
                    "meeting_url",
                    "notes",
                ],
                str,
            ]
        ],
        calendar_dataframe.to_dicts(),
    )
