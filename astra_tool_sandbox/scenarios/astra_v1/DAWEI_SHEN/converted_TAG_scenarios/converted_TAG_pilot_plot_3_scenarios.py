# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
# Auto-generated scenario extensions
from functools import partial
from typing import Optional, cast

import polars as pl

from astra_tool_sandbox.common.evaluation import (
    Milestone,
    SnapshotConstraint,
    addition_similarity,
    column_contains_similarity,
    column_datetime_window_similarity,
    column_exact_match_similarity,
    column_list_exact_match_similarity,
    column_list_subset_match_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    contains_presence_similarity,
    snapshot_similarity,
    tool_trace_dependant_similarity,
    update_similarity,
)
from astra_tool_sandbox.common.execution_context import DatabaseNamespace, RoleType
from astra_tool_sandbox.common.scenario import Scenario, ScenarioExtension
from astra_tool_sandbox.common.tool_trace_extractors import (
    ToolTraceExtractorType,
    result_list_match_existence_extractor,
)
from astra_tool_sandbox.scenarios.astra_v1.protagonist_simulator_few_shot_examples import (
    USER_INSTRUCTION_SINGLE_TURN,
)


def get_TAG_DAWEI_SHEN_pilot_plot_3(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="DAWEI_SHEN_3_3a88cb84-6602-473d-90fd-c75fd55fd798_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_3",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_high",
                "contact",
                "email",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-04T20:00:00-08:00",
            is_read_time="2024-12-04T20:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to e-mail everyone who attended today's virtual assistant discussion saying you found today's meeting very productive and you also want to schedule another meeting for Friday "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send an e-mail to Michelle and Theo saying I found our meeting today to be very productive and then schedule another meeting with the same title for this Friday at the same time.",
                },
            ],
            reasoning="The user wants to send an email to Michelle and Theo saying they found their meeting today to be very productive, so first I must determine who is meant by Michelle and Theo.\n\nLooking through the user's calendar I found a meeting in today's schedule with a Michelle Barnes and Theo Appleseed listed as invitees and they are both in the user's contacts so I assume they are who the user is referring to.\n\nI will compose a message like \"I found our meeting today to be very productive.\" and ask the user if it's ok to send.\n\nThe user also wants me to schedule another meeting for this Friday. The user has confirmed this means copying the details of today's meeting with Michelle and Theo to Friday's schedule as well. I will therefore schedule another \"Discussion on Virtual Assistant Algorithm Updates\" for Friday 6 December 2024 at 10:00 – 11:00 (same time as today) in Conference Room B, Orchard Tech, Orchard County, CA with Dawei Shen, Michelle Barnes and Theo Appleseed listed as attendees.",
            success_conditions=[
                {
                    "input_text": "1. An e-mail is sent to michelle.barnes@orchardtech.com and theo.appleseed@orchardtech.com saying you found today's meeting very productive.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. An event "Discussion on Virtual Assistant Algorithm Updates" is scheduled for Friday 6 December 2024 at 10:00 - 11:00 in Conference Room B, Orchard Tech, Orchard County, CA with Dawei Shen, Michelle Barnes and Theo Appleseed as invitees.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_email",
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0: agent search contacts
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "get_all_contacts",
                                        "search_contacts",
                                    ],
                                ),
                            },
                        )
                    ]
                ),
                # Milestone 1: Michelle Found
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "full_name": {
                                                "value": "Michelle Barnes",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "michelle.barnes@orchardtech.com",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        ),
                    ]
                ),
                # Milestone 2: agent search contacts
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "get_all_contacts",
                                        "search_contacts",
                                    ],
                                ),
                            },
                        )
                    ]
                ),
                # Milestone 3: Theo Found
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "full_name": {
                                                "value": "Theo Appleseed",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "theo.appleseed@orchardtech.com",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=2,
                        ),
                    ]
                ),
                # 4: search for calendar
                Milestone(
                    snapshot_constraints=[
                        # 1. Tool usage to search calendar events
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # 5. Ensure calendar event with 'Discussion on Virtual Assistant Algorithm Updates' is retrieved
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "calendar_event_name": {
                                                "value": "Discussion on Virtual Assistant Algorithm Updates",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-04T10:00:00-08:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=4,
                        )
                    ]
                ),
                # Milestone 6: An outgoing email to Michelle and Theo was sent, containing the word "productive"
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        [
                                            "michelle.barnes@orchardtech.com",
                                            "theo.appleseed@orchardtech.com",
                                        ]
                                    ],
                                    "body": "I found our meeting today to be very productive",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-04T20:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "body": column_contains_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
                # Milestone 7: A calendar event for Friday, Dec 6, 2024 at 10-11 AM with the correct title/location/attendees was added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Discussion on Virtual Assistant Algorithm Updates",
                                    "start_datetime_iso": "2024-12-06T10:00:00-08:00",
                                    "end_datetime_iso": "2024-12-06T11:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "Dawei Shen",
                                            "Michelle Barnes",
                                            "Theo Appleseed",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-04T20:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.EMAIL],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # search for Michelle and Theo's contact
                (2, 3),  # search for Theo's contact
                (4, 5),  # get information about today's meeting
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_3_507dab9e-b669-4e4c-a3e9-36fb79827895_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_3",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T11:00:00-08:00",
            is_read_time="2024-12-05T11:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to arrange another meeting with the Virtual Assistant Algorithm team at the same time next week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need another meeting about the virtual assistant project at the same time next week.",
                },
            ],
            reasoning="The user wants to hold another meeting about the virtual assistant project at the usual time next week, so I need to first find this meeting.\nUser has a meeting titled Discussion on Virtual Assistant Algorithm Updates.\nThis meeting took place on Wednesday 4 December 2024 from 10:00 to 11:00, I will regard this time as the usual time referenced by the user and will schedule this meeting again on Wednesday 11 December 2024 from 10:00 to 11:00.\nThe attendees of the original meeting were the user, Michelle Barnes, and Theo Appleseed, so I will add these contacts to the new meeting on 11 December 2024.",
            success_conditions=[
                {
                    "input_text": "1. Event titled with keyword Virtual Assistant is created from 10:00 to 11:00 on 11 December 2024, Michelle Barnes and Theo Appleseed are added as attendees.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0: The agent looks up the existing meeting information
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # 1. the event was found
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "calendar_event_name": {
                                                "value": "Discussion on Virtual Assistant Algorithm Updates",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-04T10:00:00-08:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
                # Milestone 2: The calendar event is actually added to the CALENDAR database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Virtual Assistant",
                                    "start_datetime_iso": "2024-12-11T10:00:00-08:00",
                                    "end_datetime_iso": "2024-12-11T11:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "Dawei Shen",
                                            "Michelle Barnes",
                                            "Theo Appleseed",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-05T11:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "attendees_names": column_list_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            # default similarity works for provided columns
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_3_4e253690-f28c-4b59-a075-86eb6f756f7f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_3",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-04T09:35:00-08:00",
            is_read_time="2024-12-04T09:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        'You are quite busy so you want to delay the "Discussion on Virtual Assistant Algorithm Updates" event by 30 minutes '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you push back the start time of that discussion at 10am for 30 minutes later? I'm too busy.",
                },
            ],
            reasoning='So the user wants me to reschedule his discussion at 10. I will start by looking through the calendar and see if any events are on today. There is an event titled "Discussion on Virtual Assistant Algorithm Updates" starting at 10:00 so that must be what the user is referring to. I will update the start time and end time of this event to be 10:30 and 11:30 respectively. I will then present this information to the user',
            success_conditions=[
                {
                    "input_text": '1. The start time of the "Discussion on Virtual Assistant Algorithm Updates" event is updated to 10:30',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "create_calendar_event",
                "get_all_calendars",
                "modify_calendar_event",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0: The calendar event start time has been updated to 10:30
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Discussion on Virtual Assistant Algorithm Updates",
                                    "start_datetime_iso": "2024-12-04T10:30:00-08:00",
                                    "end_datetime_iso": "2024-12-04T11:30:00-08:00",
                                    "creation_datetime_iso": "2024-12-04T09:35:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_3_507dab9e-b669-4e4c-a3e9-36fb79827895_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_3",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T11:00:00-08:00",
            is_read_time="2024-12-05T11:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to arrange another meeting with the Virtual Assistant Algorithm team at the same time next week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Schedule the VA team meeting to the same time next week.",
                },
            ],
            reasoning="The user wants to schedule the VA team meeting for the same time next week, so I need to locate the existing meeting first.\nThere is an existing meeting titled Virtual Assistant Algorithm Team Meeting (VA) that occurred on Wednesday, 4 December 2024 from 10:00 – 11:00.\nI will create a new event titled “Virtual Assistant Algorithm Team Meeting” on Wednesday, 11 December 2024 from 10:00 – 11:00, with attendees Dawei Shen, Michelle Barnes, and Theo Appleseed.",
            success_conditions=[
                {
                    "input_text": "An event titled with keyword 'Virtual Assistant' is created from 10:00 to 11:00 on 11 December 2024 with attendees Dawei Shen, Michelle Barnes, and Theo Appleseed.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "create_calendar_event",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 ------------------------------------------------------------
                # Agent looks up the existing meeting – it should call either
                # `search_calendar_events` or `get_all_calendars`.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # 1. the event was found
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "calendar_event_name": {
                                                "value": "Discussion on Virtual Assistant Algorithm Updates",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-04T10:00:00-08:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
                # Milestone 2 ------------------------------------------------------------
                # Verify the new calendar event was created with correct key details.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Virtual Assistant",
                                    "start_datetime_iso": "2024-12-11T10:00:00-08:00",
                                    "end_datetime_iso": "2024-12-11T11:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "Dawei Shen",
                                            "Michelle Barnes",
                                            "Theo Appleseed",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-05T11:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "attendees_names": column_list_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with original state
                        )
                    ],
                    # We only care about CALENDAR mutation here.
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.WHATSAPP,
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_3_3a88cb84-6602-473d-90fd-c75fd55fd798_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_3",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-04T20:00:00-08:00",
            is_read_time="2024-12-04T20:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to e-mail everyone who attended today's virtual assistant discussion saying you found today's meeting very productive and you also want to schedule another meeting for Friday "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send an e-mail to Michelle Barnes and Theo Appleseed saying that I found our meeting today to be very productive and then schedule another meeting copying today's meeting's details for this Friday.",
                },
            ],
            reasoning="The user wants to immediately send an email to Michelle Barnes and Theo Appleseed saying that they found today’s meeting very productive. Next, the user wants another meeting scheduled for this Friday that mirrors today’s “Discussion on Virtual Assistant Algorithm Updates” session.\n\nI will:\n1. Look up Michelle Barnes and Theo Appleseed in contacts.\n2. Compose and send an email to them stating that today’s meeting was very productive.\n3. Locate today’s calendar event titled “Discussion on Virtual Assistant Algorithm Updates” (10:00 – 11:00 on 4 Dec 2024).\n4. Create a new event with the same title, attendees, and details for Friday, 6 Dec 2024, 10:00 – 11:00.\n\nThese steps satisfy the user’s request.",
            success_conditions=[
                {
                    "input_text": "1. An e-mail is sent to michelle.barnes@orchardtech.com and theo.appleseed@orchardtech.com saying you found today's meeting very productive.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. An event "Discussion on Virtual Assistant Algorithm Updates" is scheduled for Friday 6 December at 10:00 – 11:00 in Conference Room B, Orchard Tech, Orchard County, CA with Michelle Barnes and Theo Appleseed as invitees.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "send_email",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0: agent search contacts
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "get_all_contacts",
                                        "search_contacts",
                                    ],
                                ),
                            },
                        )
                    ]
                ),
                # Milestone 1: Michelle Found
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "full_name": {
                                                "value": "Michelle Barnes",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "michelle.barnes@orchardtech.com",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        ),
                    ]
                ),
                # Milestone 2: agent search contacts
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "get_all_contacts",
                                        "search_contacts",
                                    ],
                                ),
                            },
                        )
                    ]
                ),
                # Milestone 3: Theo Found
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "full_name": {
                                                "value": "Theo Appleseed",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "theo.appleseed@orchardtech.com",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=2,
                        ),
                    ]
                ),
                # 4: search for calendar
                Milestone(
                    snapshot_constraints=[
                        # 1. Tool usage to search calendar events
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # 5. Ensure calendar event with 'Discussion on Virtual Assistant Algorithm Updates' is retrieved
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "calendar_event_name": {
                                                "value": "Discussion on Virtual Assistant Algorithm Updates",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-04T10:00:00-08:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=4,
                        )
                    ]
                ),
                # Milestone 6 – a new e-mail addressed to Michelle and Theo was actually sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        [
                                            "michelle.barnes@orchardtech.com",
                                            "theo.appleseed@orchardtech.com",
                                        ]
                                    ],
                                    "status": "sent",
                                    "body": "productive",
                                    "creation_datetime_iso": "2024-12-04T20:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "body": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
                # Milestone 7 – a new Friday meeting was added with the correct details
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Discussion on Virtual Assistant Algorithm Updates",
                                    "start_datetime_iso": "2024-12-06T10:00:00-08:00",
                                    "end_datetime_iso": "2024-12-06T11:00:00-08:00",
                                    "attendees_names": [
                                        ["Michelle Barnes", "Theo Appleseed"]
                                    ],
                                    "creation_datetime_iso": "2024-12-04T20:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.EMAIL],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # need to find michelle's contact
                (2, 3),  # need to find theo's contact
                (4, 5),  # need to find today's meeting
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_3_132660c3-8547-40d9-8a9a-40f49262b19d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_3",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T17:00:00-08:00",
            is_read_time="2024-12-03T17:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You remember you promised your mother you would help her harvest her cabbage on Wednesday at 1000, so you need to move the meeting with Michelle and Theo to 1100. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Move the meeting I have on my calendar for Wednesday the 4th of December at 10:00 to 11:00. ",
                },
            ],
            reasoning="The user wants to move the meeting on Wednesday the 4th of December from 1000 to 1100. I see a meeting at that time called Discussion on Virtual Assistant Algorithm Updates scheduled for 2024-12-04T10:00:00-08:00. I will move it from that slot to start at 2024-12-04T11:00:00-08:00 instead (ending at 12:00).",
            success_conditions=[
                {
                    "input_text": "1. The Discussion on Virtual Assistant Algorithm Updates calendar event is shifted later to 1100. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "create_calendar_event",
                "get_all_calendars",
                "modify_calendar_event",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # 0: search for calendar
                Milestone(
                    snapshot_constraints=[
                        # 1. Tool usage to search calendar events
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # 1. Ensure calendar event with 'Discussion on Virtual Assistant Algorithm Updates' is retrieved
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "calendar_event_name": {
                                                "value": "Discussion on Virtual Assistant Algorithm Updates",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-04T10:00:00-08:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
                # Milestone 2 – Calendar event start time is updated to 11:00
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Discussion on Virtual Assistant Algorithm Updates",
                                    "start_datetime_iso": "2024-12-04T11:00:00-08:00",
                                    "end_datetime_iso": "2024-12-04T12:00:00-08:00",
                                    "creation_datetime_iso": "2024-12-03T17:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to baseline before any actions
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_3_d844cd6d-5632-4934-a225-9f96db683eb9_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_3",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T07:00:00-08:00",
            is_read_time="2024-12-01T07:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to see how long your cycling trip with Vick will last. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How long am I spending on that biking thing",
                },
            ],
            reasoning='The user wants to know how long the "biking thing" will take. I assume they are referring to the calendar event titled "Cycling Trip with Vick." I will search the calendar (using tools like get_all_calendars and search_calendar_events) to locate that event, compute the time difference between its start and end times (which is 3 hours), and then tell the user that the trip lasts about 3 hours.',
            success_conditions=[
                {
                    "input_text": "The assistant tells the user that the cycling trip with Vick will last about 3 hours.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0: The agent queries the calendar for events (tool usage check)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1: Confirm that the cycling trip event is included in the tool results
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "calendar_event_name": {
                                                "value": "Cycling Trip with Vick",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                        )
                    ]
                ),
                # Milestone 2: The agent tells the user the duration (≈3 hours)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "3 hours",
                                            "three hours",
                                            "3-hour",
                                            "three-hour",
                                            "3 hrs",
                                            "3hrs",
                                            "180 minutes",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_3_24f4d54c-1803-4383-8dde-f83a7e532f30_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_3",
                "email",
                "misinformation_no",
                "insufficient_context_no",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T10:35:00-08:00",
            is_read_time="2024-12-02T10:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to reply to Theo's email saying that the improvement looks good. Thank you! "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Draft a reply to Theo\'s last email saying "the improvement looks good. Thank you!" and then send it.',
                },
            ],
            reasoning='First, the user wants me to draft a reply to the last email from Theo. I will ask them what they want to say in the draft. They want to say "the improvement looks good. Thank you!". I will create the draft.\n\nNext they want me to send it.I will confirm this with them. I will send the email.',
            success_conditions=[
                {
                    "input_text": '1. An email is sent in response to the last email from theo.appleseed@orchardtech.com. saying something like "the improvement looks good. Thank you!"',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "modify_draft_email",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Agent looks up Theo's last email (or inbox) to reply
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    # Agent can either search specifically or list emails, both are acceptable
                                    target_tools=["search_emails", "get_all_emails"],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1: Confirm that the Theo's email found
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "sender_address": {
                                                "value": "theo.appleseed@orchardtech.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-02T09:15:00",
                                                "partial": True,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                        )
                    ]
                ),
                # Milestone 2 – A draft email is created as a reply to Theo's last email
                #   Content should indicate the improvement looks good and thank Theo.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Reply should be addressed to Theo
                                    "recipients_addresses": [
                                        ["theo.appleseed@orchardtech.com"]
                                    ],
                                    "status": "sent",
                                    # Body must capture both "looks good" and "thank you" sentiment
                                    "body": [("looks good", "looks great", "thank")],
                                    "creation_datetime_iso": "2024-12-02T10:35:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_subset_match_similarity,
                                "status": column_exact_match_similarity,
                                # Require both core ideas: approval and thanks
                                "body": column_str_contains_any_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        ),
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Email lookup → create draft reply
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_3_d844cd6d-5632-4934-a225-9f96db683eb9_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_3",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T07:00:00-08:00",
            is_read_time="2024-12-01T07:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to see how long your cycling trip with Vick will last. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Check up how long my Cycling Trip with Vick calendar event is scheduled for.",
                },
            ],
            reasoning="The user wants to know the duration of the “Cycling Trip with Vick” calendar event, which starts at 07:00 on 2024-12-01. I should locate that event in the user’s calendar and compute the difference between its start and end times (expected to be about 3 hours). I will then tell the user the duration (≈ 3 hours).",
            success_conditions=[
                {
                    "input_text": "The assistant tells the user that the Cycling Trip with Vick lasts about 3 hours.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0: The agent queries the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1: The returned results include the “Cycling Trip with Vick” event
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "calendar_event_name": {
                                                "value": "Cycling Trip with Vick",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-01T07:00:00-08:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                        )
                    ]
                ),
                # Milestone 2: The user is told the duration (≈ 3 hours) of the cycling trip
                Milestone(
                    snapshot_constraints=[
                        # Duration is mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "3 hours",
                                            "three hours",
                                            "3-hour",
                                            "three-hour",
                                            "3 hrs",
                                            "3hrs",
                                            "180 minutes",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_3_f7a50c59-aa93-499f-ab54-5dc5ee27e212_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_3",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-04T07:30:00-08:00",
            is_read_time="2024-12-04T07:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "you have had a hectic few weeks so the time the Discussion on Virtual Assistant Algorithm Updates starts has slipped your mind.       you ask your assistant for a reminder. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is today's discussion?",
                },
            ],
            reasoning="Ok, the user wants to know when today's discussion is. when looking at the calendar I found an event titled 'Discussion on Virtual Assistant Algorithm Updates'. I believe this is the discussion they are referring to. I will inform them that the event starts at 10:00 today. ",
            success_conditions=[
                {
                    "input_text": "1. user is informed the start time of 'Discussion on Virtual Assistant Algorithm Updates' is 10:00 on 4th of December 2024",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent queries the calendar for the meeting time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1: the correct discussion meeting got brought up
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "calendar_event_name": {
                                                "value": "Discussion on Virtual Assistant Algorithm Updates",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-04T10:00:00-08:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                        )
                    ]
                ),
                # Milestone 2 – User receives a response mentioning the correct start time and date
                Milestone(
                    snapshot_constraints=[
                        # Check mention of the correct time
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("10:00", "10 am", "10am")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_3_4ff0be69-2ec7-4472-b7f3-8684b2ca578d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_3",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T15:00:00-08:00",
            is_read_time="2024-12-02T15:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "Having gone through the draft from Michelle you decide that you need another check in meeting to stay on target.       You take it upon yourself to schedule these. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "We need another discussion with Theo and Michelle same time next week.",
                },
            ],
            reasoning="The user indicates that they may need me to schedule a new event or copy an existing one.\nFirst, I should determine which event they mean. I cannot find an event name which matches the query. Looking through scheduled event details I can see that Theo and Michelle are present as participants in the event Discussion on Virtual Assistant Algorithm Updates occurring 10:00 - 11:00 on December 4th 2024. They do not appear to be present in any other scheduled events.\nI can assume that this is the event being referred to.\nI can assume that the user is asking for an existing event to be copied over.\nThe user has indicated that the new event should be next week, at the same time. Before copying it over I should confirm that there are no events scheduled for the proposed date to prevent clashes.\nI can see no potential clashes, I will copy the event.\nI have now copied the event, the new event Discussion on Virtual Assistant Algorithm Updates now occurs on December 11th 2024 and has a start time of 10:00 and an end time of 11:00.",
            success_conditions=[
                {
                    "input_text": "An event titled 'Discussion on Virtual Assistant Algorithm Updates' is created for December 11th 2024 from 10:00 to 11:00 with Theo and Michelle as attendees.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "create_calendar_event",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # 0: search for calendar
                Milestone(
                    snapshot_constraints=[
                        # 1. Tool usage to search calendar events
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # 1. Ensure calendar event with 'Discussion on Virtual Assistant Algorithm Updates' is retrieved
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "calendar_event_name": {
                                                "value": "Discussion on Virtual Assistant Algorithm Updates",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-04T10:00:00-08:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
                # Milestone 2 – next week's meeting was added with the correct details
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Discussion on Virtual Assistant Algorithm Updates",
                                    "start_datetime_iso": "2024-12-11T10:00:00-08:00",
                                    "end_datetime_iso": "2024-12-11T11:00:00-08:00",
                                    "attendees_names": [
                                        ["Michelle Barnes", "Theo Appleseed"]
                                    ],
                                    "creation_datetime_iso": "2024-12-02T15:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_3_4ff0be69-2ec7-4472-b7f3-8684b2ca578d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_3",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T15:00:00-08:00",
            is_read_time="2024-12-02T15:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "Having gone through the draft from Michelle you decide that you need another check in meeting to stay on target.       You take it upon yourself to schedule these. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Copy the virtual assistant discussion to next Wednesday.",
                },
            ],
            reasoning='The user wants me to copy the calendar event titled "Discussion on Virtual Assistant Algorithm Updates." I find the existing event on December 4 2024 that runs from 10:00 a.m. to 11:00 a.m. Because the user asked to copy it to next Wednesday (December 11 2024) without changing the time, I create a duplicate event for December 11 2024 from 10:00 a.m. to 11:00 a.m. There are no conflicting events, so the copy is added successfully.',
            success_conditions=[
                {
                    "input_text": 'A new calendar event named "Discussion on Virtual Assistant Algorithm Updates" is created for December 11 2024 from 10:00 a.m. to 11:00 a.m. with same attendees including Michelle Barnes and Theo Appleseed',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0: The agent looked up the existing calendar event
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # 1. Ensure calendar event with 'Discussion on Virtual Assistant Algorithm Updates' is retrieved
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "calendar_event_name": {
                                                "value": "Discussion on Virtual Assistant Algorithm Updates",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-04T10:00:00-08:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
                # Milestone 2: A new calendar event for 10–11 a.m. on 11 Dec 2024 is added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Discussion on Virtual Assistant Algorithm Updates",
                                    "start_datetime_iso": "2024-12-11T10:00:00-08:00",
                                    "end_datetime_iso": "2024-12-11T11:00:00-08:00",
                                    "attendees_names": [
                                        ["Michelle Barnes", "Theo Appleseed"]
                                    ],
                                    "creation_datetime_iso": "2024-12-02T15:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_3_f7a50c59-aa93-499f-ab54-5dc5ee27e212_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_3",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-04T07:30:00-08:00",
            is_read_time="2024-12-04T07:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "you have had a hectic few weeks so the time the Discussion on Virtual Assistant Algorithm Updates starts has slipped your mind.       you ask your assistant for a reminder. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time are we talking algorithm updates today?",
                },
            ],
            reasoning="The user is asking for the time of the “Discussion on Virtual Assistant Algorithm Updates” meeting. After checking the calendar, I see the event is scheduled for 10:00 AM on December 4, 2024. I will reply with that start time (10 AM on Dec 4).",
            success_conditions=[
                {
                    "input_text": "user is informed the start time of 'Discussion on Virtual Assistant Algorithm Updates' is 10:00 on 4th of December 2024",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent checks calendar (either searches or lists)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – Tool result contains the correct meeting with correct start time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "calendar_event_name": {
                                                "value": "Discussion on Virtual Assistant Algorithm Updates",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-04T10:00:00-08:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                        )
                    ]
                ),
                # Milestone 2 – User is informed of the correct start time/date
                Milestone(
                    snapshot_constraints=[
                        # Time mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "10",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
    ]
