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
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    not_contains_presence_similarity,
    removal_similarity,
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


def get_TAG_THEO_APPLESEED_pilot_plot_22(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="THEO_APPLESEED_22_1e912474-400d-4e61-ab91-7e8c70747756_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T13:50:00-07:00",
            is_read_time="2024-07-29T13:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know how much time there is between the events client presentation preparation and weekly team meeting.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How much time do I have between client presentation and the other meeting I have with the same folks later today?",
                },
            ],
            reasoning="The user wants to know how much time there is between \"client presentation\" and the meeting they have with the same folks later.\n\nOkay, first of all, I need to go to the user's Calendar to see if they have any upcoming events that correspond to these descriptions. \n\nOkay, right, there's Client Presentation Preparation at 14:00-15:00, participants are Kevin, Stefan, Michelle and Dawei. After that, from 16:00 - 17:00, July 29th there's a Weekly Team Meeting and its participants are also Kevin, Stefan, Michelle and Dawei. \n\nI will let the user know that they have 1 hour in between. ",
            success_conditions=[
                {
                    "input_text": '1. The time between the events named "Client Presentation Preparation" and "Weekly Team Meeting" is presented to the user: 1 hour. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent uses calendar tools to look up relevant events
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
                # Milestone 1 – Confirm both specific events exist in calendar tool output
                Milestone(
                    snapshot_constraints=[
                        # Check "Client Presentation Preparation" event was retrieved
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
                                                "value": "Client Presentation Preparation",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T14:00:00-07:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-07-29T15:00:00-07:00",
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
                # Milestone 2 – Agent uses calendar tools to look up relevant events
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
                # Milestone 3 – Confirm both specific events exist in calendar tool output
                Milestone(
                    snapshot_constraints=[
                        # Check "Weekly Team Meeting" event was retrieved
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
                                                "value": "Weekly Team Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T16:00:00-07:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-07-29T17:00:00-07:00",
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
                # Milestone 4 – Agent tells user the correct time gap (1 hour)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Accept any phrasing that clearly conveys "1 hour"
                                    "content": [("1 hour", "one hour")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Use calendar tools → confirm both events retrieved
                (2, 3),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_467b72b5-b421-4fbb-931a-35fae58e645d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:45:00-07:00",
            is_read_time="2024-07-29T10:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You notice that you have double booked yourself today.   You decide to move one of the clashing events. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need you to move the follow-up sync one hour later.",
                },
            ],
            reasoning="The user is asking me to move an event.\nI should find the event in the user's calendar.\nI have found the queried event, Follow-up Sync with Michelle and Dawei scheduled for July 29, 2024 11:00-12:00.\nThe user has asked me to move the start time of this event one hour later.\nI cannot see any possible clashes as a result of this.\nI will go ahead and move the event.\nFollow-up Sync with Michelle and Dawei is now scheduled for July 29, 2024 12:00-13:00.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. The event named 'Follow-up Sync with Michelle and Dawei', originally scheduled for 29 July 2024 from 11:00-12:00, is moved to 29 July 2024 from 12:00-13:00.",
                },
                {
                    "input_text": "2. The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "modify_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – The agent looks up today’s calendar to locate the conflicting event
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
                    ],
                ),
                # Milestone 1 – Confirm the correct event (“Follow-up Sync with Michelle and Dawei”) was returned
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
                                                "value": "Follow-up Sync with Michelle and Dawei",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T11:00:00-07:00",
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
                    ],
                ),
                # Milestone 2 – The calendar event has been updated to one hour later (12:00-13:00)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Follow-up Sync with Michelle and Dawei",
                                    "start_datetime_iso": "2024-07-29T12:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T13:00:00-07:00",
                                    "creation_datetime_iso": "2024-07-29T10:45:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_a3c3b16e-62f5-4841-86ac-e42879f6eabd_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T13:50:00-07:00",
            is_read_time="2024-07-29T13:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know how much time there is between the events client presentation preparation and weekly team meeting. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to know how much time there is between the client presentation and the team meeting please ",
                },
            ],
            reasoning='The user wants to know how much time there is between "the client presentation" and "the team meeting".\n\nOkay, first of all, I need to go to the user\'s Calendar to see if they have any upcoming events that correspond to these descriptions.\n\nGreat, okay, I can see that they have one event named "Client Presentation Preparation" that\'s happening from 14:00 - 15:00, July 29th, 2024, and another named "Weekly Team Meeting", taking place from 16:00 - 17:00, July 29th, 2024.\n\nThe later of the two meetings starts at 16:00, and the earlier of the two meetings ends at 15:00, so I calculate the time between these two events is 1 hour. \n\nI will now inform the user of this. ',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the amount of time between the events named "Client Presentation Preparation" and "Weekly Team Meeting" is 1 hour. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent consulted calendar data
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
                    ],
                ),
                # Milestone 1 – Agent told the user the gap is one hour
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
                                            "1 hour",
                                            "one hour",
                                            "1-hour",
                                            "1 hr",
                                            "one hr",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_1cbc0460-3f90-4203-827a-41b907ba1982_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:30:00-07:00",
            is_read_time="2024-07-29T07:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to set a reminder to take time to reset in your free time as your schedule is quite busy today.  You see you have a free spot in your calendar so you decide that that would be the best time to chill out. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Create an event "Reset" for the free hour I have at 15:00 today ',
                },
            ],
            reasoning='Okay, so the user wants to create an event "Reset" for the free hour they have at 15:00 today. I\'m going to need to double check the user\'s calendar for the time frame the user requested to avoid scheduling conflicts. Looking at the calendar, there does appear to be a free hour from 15:00-16:00 ,so I will put the event there as requested. With the user\'s confirmation, I create the event "Reset" at 15:00-16:00 on 29 July 2024. ',
            success_conditions=[
                {
                    "input_text": '1. The event "Reset" is created at 15:00-16:00 on 29 July 2024. ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – confirm that a new calendar event called “Reset” was added for the correct
                # one-hour slot on 29 July 2024.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Reset",
                                    "start_datetime_iso": "2024-07-29T15:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T16:00:00-07:00",
                                    "creation_datetime_iso": "2024-07-29T07:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            # default exact-match behaviour is fine for these fields
                            reference_milestone_node_index=-1,  # compare against initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_5f0f6536-3481-4308-a300-4d2e28ef4a99_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T08:00:00-07:00",
            is_read_time="2024-07-29T08:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You'll need more time to prepare for the weekly team meeting. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to move my Weekly Team Meeting, push it back by half an hour please.",
                },
            ],
            reasoning="User says they need to move their meeting. Let's see if there's an event named Weekly Team Meeting. I see there is; it's scheduled for today at 16:00-17:00. The user wants to move it back half an hour, which means I must reschedule it for half an hour later than originally planned, so starting at 16:30, and leave all other details the same. I will now inform the user that 'Weekly Team Meeting' has been rescheduled and will now take place from 16:30-17:30 on 29th July 2024. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. The event Weekly Team Meeting is rescheduled to July 29, 2024 - 16:30-17:30, all other details remain the same.",
                },
                {
                    "input_text": "2. The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "modify_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up existing calendar events
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
                    ],
                ),
                # Milestone 1 – Confirm that the “Weekly Team Meeting” event (original 16:00-17:00 slot) was found
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
                                                "value": "Weekly Team Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T16:00:00-07:00",
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
                    ],
                ),
                # Milestone 2 – The calendar event is updated to start 16:30 and end 17:30 on the same date
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Weekly Team Meeting",
                                    "start_datetime_iso": "2024-07-29T16:30:00-07:00",
                                    "end_datetime_iso": "2024-07-29T17:30:00-07:00",
                                    "creation_datetime_iso": "2024-07-29T08:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_5f0f6536-3481-4308-a300-4d2e28ef4a99_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T14:30:00-07:00",
            is_read_time="2024-07-29T14:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You'll need more time to prepare for the weekly team meeting. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Push my next meeting back half an hour. ",
                },
            ],
            reasoning="Ok so the user wants to Push their next meeting back half an hour. First I will establish what they mean by 'next meeting.' Currently at 14:30 they appear to be in their 'Client Presentation Preparation' so I'm assuming is is not this one. The next event on the calendar is 'Weekly Team Meeting.' Next I will reschedule 'Weekly Team Meeting' so it is 'pushed back' half an hour, meaning it starts half an hour later. The new runtime for this event would be 16:30-17:30. I will now inform the user that 'Weekly Team Meeting' has been rescheduled and will now take place from 16:30-17:30 on 29th July 2024.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. The event Weekly Team Meeting is rescheduled to July 29, 2024 - 16:30-17:30, all other details remain the same.",
                },
                {
                    "input_text": "2. The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "modify_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the existing calendar events to figure out which one is the “next meeting”.
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
                # Milestone 1 – The “Weekly Team Meeting” is rescheduled 30 minutes later (single logical update).
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Weekly Team Meeting",
                                    "start_datetime_iso": "2024-07-29T16:30:00-07:00",
                                    "end_datetime_iso": "2024-07-29T17:30:00-07:00",
                                    "creation_datetime_iso": "2024-07-29T14:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_ba499c2c-ae8d-4cfa-ab26-2b25d87baf85_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T11:00:00-07:00",
            is_read_time="2024-07-29T11:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        'You want to delete your event called Dentist Appointment" at 13:00pm on 29 July 2024 due to your schedule being packed. '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Remove the Dentist event",
                },
            ],
            reasoning="The user needs to delete a specific calendar event. The user has presented this event as 'Dentist' event. I see the user's calendar has an event named 'Dentist Appointment' at 13:00-14:00 today 29 July 2024. From here I will remove the event from the calendar and confirm to the user.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The event "Dentist Appointment" at 13:00 on 29th July 2024 is removed from the calendar.',
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events to locate the dentist appointment
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
                    ],
                ),
                # Milestone 1 – Confirm that the returned search results include the correct dentist event
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
                                                "value": "Dentist Appointment",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T13:00:00-07:00",
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
                    ],
                ),
                # Milestone 2 – Verify the dentist appointment has been removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dentist Appointment",
                                    "start_datetime_iso": "2024-07-29T13:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T14:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Must locate the event before confirming its presence
                (1, 2),  # After confirming the correct event, verify it was removed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_1cbc0460-3f90-4203-827a-41b907ba1982_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:30:00-07:00",
            is_read_time="2024-07-29T07:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to set a reminder to take time to reset in your free time this afternoon as your schedule is quite busy today.  You see you have a free spot in your calendar so you decide that that would be the best time to chill out. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Find a one-hour block in my calendar to reset this afternoon, name it 'Reset'. ",
                },
            ],
            reasoning="Okay, so the user wants to create an event for today at 15:00-16:00. They didn't give me a specific name for the event, so by default I'll call it \"Reset\". \n\nNext, I need to check the user's calendar to confirm availability for the requested time. They said they have an hour free between 13:00 and 17:00. I found that the time slot 15:00-16:00 is free because there are no scheduled events during that time, so I will create the event for this time as requested. With the user's confirmation, I will create the event \"Reset\" at 15:00-16:00 on 29 July 2024. ",
            success_conditions=[
                {
                    "input_text": '1. The event "Reset" is created at 15:00-16:00 on 29 July 2024. ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent inspects the existing calendar to confirm availability
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
                    ],
                ),
                # Milestone 1 – A new calendar event “Reset” from 15:00-16:00 on 2024-07-29 has been created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Reset",
                                    "start_datetime_iso": "2024-07-29T15:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T16:00:00-07:00",
                                    "creation_datetime_iso": "2024-07-29T07:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_24aa34d2-a2a2-421f-9406-012430104919_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T09:00:00-07:00",
            is_read_time="2024-07-29T09:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to cancel your dentist appointment because you have too many work appointments on for the day and are traveling to Chicago the next day. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "My calendar is full on July 29th 2024, I need to cancel my dentist appointment because I am going to Chicago the next day. ",
                },
            ],
            reasoning="The user wants to cancel their dentist appointment. I see an event named 'Dentist Appointment' in their calendar booked today, 29 July 2024, from 13:00 to 14:00 at the Downtown Dental Clinic. I will delete this event from the calendar. ",
            success_conditions=[
                {
                    "input_text": "1. Dentist appointment is canceled for July 29th 2024. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (must query the calendar)
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
                    ],
                ),
                # Milestone 1 – Verify the dentist appointment was actually found in the previous lookup
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
                                                "value": "Dentist Appointment",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T13:00:00-07:00",
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
                            reference_milestone_node_index=0,  # refer to tool results from Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – Dentist appointment is removed (canceled) from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dentist Appointment",
                                    "start_datetime_iso": "2024-07-29T13:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial DB state
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_a3c3b16e-62f5-4841-86ac-e42879f6eabd_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T13:50:00-07:00",
            is_read_time="2024-07-29T13:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know how much time there is between the events client presentation preparation and weekly team meeting. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How much time between presentation practice and my team meeting? reply in hours",
                },
            ],
            reasoning='The user wants to know how much time there is between their "presentation practice" and their "team meeting".\n\nI go to the user\'s Calendar to find the events these refer to. I can see one event named "Client Presentation Preparation" on July 29th, 2024, from 14:00 - 15:00, which is their presentation practice, and one event named "Weekly Team Meeting", from 16:00 - 17:00, July 29th, 2024, which is their team meeting.\n\nThe later of the two meetings starts at 16:00, and the earlier of the two meetings ends at 15:00, so I calculate the time between these two events is 1 hour.\n\nI will now inform the user of this. ',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the amount of time between the events named "Client Presentation Preparation" and "Weekly Team Meeting" is 1 hour.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent looks up calendar events to determine the gap
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
                    ],
                ),
                # Milestone 1 – Agent tells the user the time difference is one hour
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("1 hour", "1 hr", "one hour")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_467b72b5-b421-4fbb-931a-35fae58e645d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:45:00-07:00",
            is_read_time="2024-07-29T10:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You notice that you have double booked yourself today.  You decide to move one of the clashing events. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need you to move the event in Conference room B to start at 12:00.",
                },
            ],
            reasoning="The user has asked me to move an event.\nI should look through the user's calendar to find the queried event.\nThe user has provided me with the location set for this event of 'Conference room B'. This will narrow my search.\nI can see only one upcoming event with a relevant location: Follow-up Sync with Michelle and Dawei scheduled for July 29, 2024 11:00-12:00, the location of this event is set as Conference Room B, Innovative Tech Solutions.\nI cannot see any potential clashes that may come about as a result of me adjusting the start time of this event.\nFollow-up Sync with Michelle and Dawei is now scheduled for July 29, 2024 12:00-13:00.\nI should inform the user.\n",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. The event named 'Follow-up Sync with Michelle and Dawei', originally scheduled for 29 July 2024 from 11:00-12:00, is moved to 29 July 2024 from 12:00-13:00.",
                },
                {
                    "input_text": "2. The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "modify_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events so it can identify the meeting to reschedule
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
                    ],
                ),
                # Milestone 1 - Find the calendar event that takes place in Conference Room B
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
                                                "value": "Follow-up Sync with Michelle and Dawei",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Conference Room B",
                                                "partial": True,
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
                    ],
                ),
                # Milestone 2 – The calendar event has been updated to 12:00-13:00 on July 29, 2024
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Follow-up Sync with Michelle and Dawei",
                                    "start_datetime_iso": "2024-07-29T12:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T13:00:00-07:00",
                                    "creation_datetime_iso": "2024-07-29T10:45:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial calendar state
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_1e912474-400d-4e61-ab91-7e8c70747756_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_22",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T13:50:00-07:00",
            is_read_time="2024-07-29T13:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know how much time there is between the events client presentation preparation and weekly team meeting.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to know how much time there is between the client presentation and the team meeting please ",
                },
            ],
            reasoning='The user wants to know how much time there is between "the client presentation" and "the team meeting".\n\nOkay, first of all, I need to go to the user\'s Calendar to see if they have any upcoming events that correspond to these descriptions.\n\nGreat, okay, I can see that they have one event named "Client Presentation Preparation" that\'s happening from 14:00 - 15:00, July 29th, 2024, and another named "Weekly Team Meeting", taking place from 16:00 - 17:00, July 29th, 2024.\n\nI calculate the time between these two events is 1 hour. \n\nI will now inform the user of this. ',
            success_conditions=[
                {
                    "input_text": '1. The time between the events named "Client Presentation Preparation" and "Weekly Team Meeting" is presented to the user: 1 hour. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent looks up calendar information (optional but expected for retrieval tasks)
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
                # Milestone 1 – User is informed that there is 1 hour between the two events
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Any phrasing that clearly communicates "1 hour" is acceptable
                                    "content": [("1 hour", "one hour")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar lookup precedes answering the user
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_c2c76c6b-086d-4551-90b1-f7ab69cabff2_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T12:30:00-07:00",
            is_read_time="2024-07-29T12:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        'You want to see the location of "Dentist Appointment" '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the location of my dentist appointment",
                },
            ],
            reasoning='The user wants to know the location of their calendar event named "Dentist Appointment". I have found a calendar event with this name in the user\'s schedule for today at 13:00-14:00 with the location listed as "Downtown Dental Clinic", so I will tell that information to the user. ',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the location of the event named "Dentist Appointment", scheduled for 13:00-14:00 on 29 July 2024, is the Downtown Dental Clinic.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent uses a calendar-reading tool to look up events
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
                # Milestone 1 – Confirm the dentist appointment was returned from the calendar lookup
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
                                                "value": "Dentist Appointment",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Downtown Dental Clinic",
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
                # Milestone 2 – Agent tells the user where the appointment is
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Downtown Dental Clinic",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_5277aad9-f0dd-4acb-ba6d-1d1d123a4381_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:30:00-07:00",
            is_read_time="2024-07-29T07:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to set a reminder to take time to reset in your free time as your schedule is quite busy today.  You see you have a free spot in your calendar for 15:00-16:00 and so you decide that that would be the best time to chill out. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Put it in my calendar to reset from 15:00-16:00 this afternoon. ",
                },
            ],
            reasoning="Okay, so the user wants to create an event for today at 15:00-16:00. They didn't give me a specific name for the event, so by default I'll call it \"Reset\". \n\nNext, I need to check the user's calendar to confirm availability for the requested time. I found that the time slot 15:00-16:00 is free, so I will create the event for this time as requested. With the user's confirmation, I will create the event \"Reset\" at 15:00-16:00 on 29 July 2024. ",
            success_conditions=[
                {
                    "input_text": "1. An event is created at 15:00-16:00 on 29 July 2024. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – A new calendar event from 15:00-16:00 on July 29 2024 is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "start_datetime_iso": "2024-07-29T15:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T16:00:00-07:00",
                                    "creation_datetime_iso": "2024-07-29T07:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # Allow case-insensitive or phrasing variation on the event name
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_ecb87370-0d88-4b70-8ffa-357f9b0eb164_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:40:00-07:00",
            is_read_time="2024-07-29T07:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want a summary of the events you have in the day ahead. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you tell me about my events for today?",
                },
            ],
            reasoning="The user wants to know about today's events. First I'll need to check their calendar for events scheduled today, 2024/07/29.\n\nI found seven events on the user's calendar today: Project Sync Meeting (08:00-09:00), Data Analysis Review (09:30-10:30), Follow-up Sync with Michelle and Dawei (11:00-12:00), Brainstorming Session (11:00-12:00), Dentist Appointment (13:00-14:00), Client Presentation Preparation (14:00-15:00), and Weekly Team Meeting (16:00-17:00).\n\nGreat, now I can tell the user about their events.",
            success_conditions=[
                {
                    "input_text": "1. A summary of the events scheduled on 2024/07/29 is provided to the user: Project Sync Meeting (08:00-09:00), Data Analysis Review (09:30-10:30), Follow-up Sync with Michelle and Dawei (11:00-12:00), Brainstorming Session (11:00-12:00), Dentist Appointment (13:00-14:00), Client Presentation Preparation (14:00-15:00), and Weekly Team Meeting (16:00-17:00).",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent retrieves today’s calendar events
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
                # Milestone 1 – Confirm at least one expected event was returned from the calendar lookup
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
                                                "value": "Project Sync Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T08:00:00-07:00",
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
                # Milestone 2 – The user receives a summary containing all seven events
                Milestone(
                    snapshot_constraints=[
                        # Project Sync Meeting
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Project Sync Meeting",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Data Analysis Review
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Data Analysis Review",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Follow-up Sync with Michelle and Dawei
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Follow-up Sync with Michelle and Dawei",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Brainstorming Session
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Brainstorming Session",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Dentist Appointment
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Dentist Appointment",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Client Presentation Preparation
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Client Presentation Preparation",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Weekly Team Meeting
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Weekly Team Meeting",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_1dfc4067-52c8-4520-929f-7070f14a7b39_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:50:00-07:00",
            is_read_time="2024-07-29T10:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "Your day is too busy and you want to cancel your dentist appointment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete this afternoon's Dentist Appointment.",
                },
            ],
            reasoning="The user wants to delete this afternoon's Dentist Appointment. I'll check their calendar for today.\n\nI found a matching event: Dentist Appointment at 13:00-14:00 today (2024-07-29). I'll go ahead and delete it.",
            success_conditions=[
                {
                    "input_text": "1. Dentist Appointment at 13:00-14:00 on 2024-07-29 is deleted.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – the agent tries to locate the dentist appointment in the calendar
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
                    ],
                ),
                # Milestone 1 – confirm the returned calendar event is the 1 pm Dentist Appointment
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
                                                "value": "Dentist Appointment",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T13:00:00-07:00",
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
                    ],
                ),
                # Milestone 2 – the dentist appointment has been removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dentist Appointment",
                                    "start_datetime_iso": "2024-07-29T13:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T14:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # found event → confirm correct event
                (1, 2),  # confirmed event → event removed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_104d2354-2a88-4a4b-91b2-924c4b5aaae9_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-30T11:20:00-07:00",
            is_read_time="2024-07-30T11:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You are no longer going to Chicago so want to remove the train journey from your Calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete Train Trip to Chicago from my calendar. ",
                },
            ],
            reasoning="The user wants to delete their Train Trip to Chicago. I should look in their Calendar for this. Looks like they have one event with that name on 30 July 2024 from 15:07-20:00. I will delete it and let the user know. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. Train Trip to Chicago at 15:07-20:00 on 30 July 2024 is deleted.",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent tries to locate calendar event(s) (information-retrieval step)
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
                    ],
                ),
                # Milestone 1 – Verify the Chicago train trip is removed from the Calendar DB
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Train Trip to Chicago",
                                    "start_datetime_iso": "2024-07-30T15:07:00-07:00",
                                    "end_datetime_iso": "2024-07-30T20:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Must have located the event before removing it
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_bc4637c8-00df-425e-b9bc-cb84c751c260_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T18:40:00-07:00",
            is_read_time="2024-07-29T18:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to schedule in a massage in the evening today after a long day at work. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Create a new event called massage appointment at 18:40.",
                },
            ],
            reasoning="Right so, the user wants me to create a new event named 'Massage Appointment'. To that end, I should explore the user's calendar for Monday 29th July 2024 to make sure there are no conflictive events. After checking the user is available the time they want to schedule the massage, I can create an event called \"Massage Appointment\" for 18:40 based on their request. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A new event 'Massage Appointment' is scheduled for 29th July 2024 at 18:40.",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – A new calendar event “Massage Appointment” at 18:40 on 2024-07-29 was created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Massage Appointment",
                                    "start_datetime_iso": "2024-07-29T18:40:00-07:00",
                                    "creation_datetime_iso": "2024-07-29T18:40:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            # Only need to match the critical identifying fields; defaults are fine for others
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_104d2354-2a88-4a4b-91b2-924c4b5aaae9_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T11:20:00-07:00",
            is_read_time="2024-07-29T11:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You are no longer going to Chicago so want to remove the train journey from your Calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my travel event. ",
                },
            ],
            reasoning=" The user wants to delete their travel event. I should check their Calendar. Hmm looks like there is no travel event. However, there is an event called Train Trip to Chicago from 15:07-20:00 on 30 July 2024. Trains are a mode of travel so this must be what the user meant. I will delete this one and let the user know. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. Train Trip to Chicago at 15:07-20:00 on 30 July 2024 is deleted.",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (discovery step)
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
                    ],
                ),
                # Milestone 1 – Verify that the Chicago train trip was surfaced in the tool output
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
                                                "value": "Train Trip to Chicago",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-30T15:07:00-07:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-07-30T20:00:00-07:00",
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
                    ],
                ),
                # Milestone 2 – Event has been removed from the calendar database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Train Trip to Chicago",
                                    "start_datetime_iso": "2024-07-30T15:07:00-07:00",
                                    "end_datetime_iso": "2024-07-30T20:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # tool call -> confirm event found
                (1, 2),  # event confirmed -> event removed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_1dfc4067-52c8-4520-929f-7070f14a7b39_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:50:00-07:00",
            is_read_time="2024-07-29T10:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "Your day is too busy and you want to cancel your dentist appointment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I can't go to the dentist this week.",
                },
            ],
            reasoning="The user says they can't go to the dentist this week. Let's check their calendar to see if they were supposed to go to the dentist this week.\n\nI found an event called Dentist Appointment today (2024-07-29) from 13:00 to 14:00. There are no other dentist events on the calendar for this week, so I can deduce that the user wants me to delete this event. I will now delete it and inform the user I have done so.",
            success_conditions=[
                {
                    "input_text": "1. Dentist Appointment at 13:00-14:00 on 2024-07-29 is deleted.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (either searches or retrieves all)
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
                    ],
                ),
                # Milestone 1 – Verify the Dentist Appointment event was surfaced from the previous lookup
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
                                                "value": "Dentist Appointment",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T13:00:00-07:00",
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
                    ],
                ),
                # Milestone 2 – Dentist appointment is removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dentist Appointment",
                                    "start_datetime_iso": "2024-07-29T13:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial state
                        ),
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar lookup → verify event found
                (1, 2),  # Event found → event removed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_ecb87370-0d88-4b70-8ffa-357f9b0eb164_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:40:00-07:00",
            is_read_time="2024-07-29T07:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want a summary of the events you have in the day ahead. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read today's event information out loud.",
                },
            ],
            reasoning="The user wants today's event information to be read out to them. I'll check their calendar for events scheduled today, 2024/07/29.\n\nI found seven events on the user's calendar today: Project Sync Meeting (08:00-09:00), Data Analysis Review (09:30-10:30), Follow-up Sync with Michelle and Dawei (11:00-12:00), Brainstorming Session (11:00-12:00), Dentist Appointment (13:00-14:00), Client Presentation Preparation (14:00-15:00), and Weekly Team Meeting (16:00-17:00).\n\nI'll go ahead and inform the user about their events.",
            success_conditions=[
                {
                    "input_text": "1. A summary of the events scheduled on 2024/07/29 is provided to the user: Project Sync Meeting (08:00-09:00), Data Analysis Review (09:30-10:30), Follow-up Sync with Michelle and Dawei (11:00-12:00), Brainstorming Session (11:00-12:00), Dentist Appointment (13:00-14:00), Client Presentation Preparation (14:00-15:00), and Weekly Team Meeting (16:00-17:00).",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent queries the calendar for today’s events
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
                    ],
                ),
                # Milestone 1 – Confirm at least one expected event (Project Sync Meeting) is found in the
                #               calendar-query result from Milestone 0
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
                                                "value": "Project Sync Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T08:00:00-07:00",
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
                    ],
                ),
                # Milestone 2 – The user receives a summary that mentions all seven events
                Milestone(
                    snapshot_constraints=[
                        # Project Sync Meeting
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Project Sync Meeting",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Data Analysis Review
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Data Analysis Review",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Follow-up Sync with Michelle and Dawei
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Follow-up Sync",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Brainstorming Session
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Brainstorming Session",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Dentist Appointment
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Dentist Appointment",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Client Presentation Preparation
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Client Presentation Preparation",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Weekly Team Meeting
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Weekly Team Meeting",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Tool call → confirmation event retrieved
                (1, 2),  # Confirmation of retrieval → user-facing summary
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_9ab96ab5-cbef-458d-a01c-9338b349e05d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:40:00-07:00",
            is_read_time="2024-07-29T07:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to clear your schedule for today except for your dentist appointment "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Get rid of everything today except the tooth cleaning",
                },
            ],
            reasoning="The user is asking me to delete multiple events.\nI should look at the user's calendar.\nThe user has asked me to delete all but one event.\nFirst, I should identify which event they want to keep. The user has mentioned a tooth fixing person, I cannot see any exact matches. However, I can see a Dentist Appointment, this is related to the tooth mentioned by the user. I will ensure this event is not deleted.\nI will go ahead and delete the following events from July 29, 2024: Project Sync Meeting 08:00-08:30, Dara Analysis Review 09:30-10:30, Brainstorming Session 11:00-12:00, Follow-up Sync with Michelle and Dawei 11:00-12:00, Client Presentation Preparation 14:00-15:00, Weekly Team Meeting 16:00-17:00.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. The event Project Sync Meeting on 29 July 2024 at 8:00-9:00 is deleted from the calendar",
                },
                {
                    "input_text": "2. The event Data Analysis Review on 29 July 2024 at 9:30-10:30 is deleted from the calendar",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The event Brainstorming Session on 29 July 2024 at 11:00-12:00 is deleted from the calendar",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "4. The event Follow-up Sync with Michelle and Dawei on 29 July 2024 at 11:00-12:00 is deleted from the calendar",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "5. The event client presentation preparation on 29 July 2024 at 14:00-15:00 is deleted from the calendar",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "6. The event Weekly Team Meeting on 29 July 2024 at 16:00-17:00 is deleted from the calendar",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The assistant looks at today’s calendar to figure out what to delete
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
                # ---------- Removals ----------
                # Milestone 1 – Project Sync Meeting removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Project Sync Meeting",
                                    "start_datetime_iso": "2024-07-29T08:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
                # Milestone 2 – Data Analysis Review removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Data Analysis Review",
                                    "start_datetime_iso": "2024-07-29T09:30:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
                # Milestone 3 – Brainstorming Session removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Brainstorming Session",
                                    "start_datetime_iso": "2024-07-29T11:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
                # Milestone 4 – Follow-up Sync with Michelle and Dawei removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Follow-up Sync with Michelle and Dawei",
                                    "start_datetime_iso": "2024-07-29T11:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
                # Milestone 5 – Client Presentation Preparation removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Client Presentation Preparation",
                                    "start_datetime_iso": "2024-07-29T14:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
                # Milestone 6 – Weekly Team Meeting removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Weekly Team Meeting",
                                    "start_datetime_iso": "2024-07-29T16:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_745080bf-e1d8-43e7-a56d-f396f7cfd32e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:35:00-07:00",
            is_read_time="2024-07-29T07:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to cancel your dentist appointment today because your schedule is too full. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Cancel the event Dentist Appointment scheduled for 29 July 2024 at 13:00 to 14:00.",
                },
            ],
            reasoning="The user wants me to show them the event called dentist appointment which is happening today. Now they would like to cancel the appointment so I'll go ahead and delete that and then notify them that I done so.",
            success_conditions=[
                {
                    "input_text": '1. The event "Dentist Appointment" scheduled for 29 July 2024 at 13:00 to 14:00 is cancelled. ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (optional but recommended information-gathering step)
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
                    ],
                ),
                # Milestone 1 – Confirm the dentist appointment appears in the tool output from Milestone 0
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
                                                "value": "Dentist Appointment",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T13:00:00-07:00",
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
                            reference_milestone_node_index=0,  # parse tool output from Milestone 0
                        ),
                    ],
                ),
                # Milestone 2 – The dentist appointment has been cancelled (removed)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dentist Appointment",
                                    "start_datetime_iso": "2024-07-29T13:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T14:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_4d78ce1a-b8d7-4403-ab77-11ec8deb98cd_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:35:00-07:00",
            is_read_time="2024-07-29T07:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to schedule time to go to the sauna after work today, after the last meeting "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I'm going to be tired after today can you schedule a sauna session for me later tonight right after work?",
                },
            ],
            reasoning='The user wants to schedule a sauna session for later tonight as they\'re going to be tired after work. The user said they want it to be scheduled "right after work". Their last meeting of the day is "Weekly Team Meeting" from 16:00-17:00, so it needs to be some time right after 17:00, I\'ll add a new calendadr event named "Sauna Session" for 17:00 today July 29th 2024.',
            success_conditions=[
                {
                    "input_text": '1. A calendar event "Sauna Session" is scheduled at 17:00 on July 29',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks at the existing calendar to understand today’s schedule
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
                    ],
                ),
                # Milestone 1 – Confirm that one of today’s known events (e.g. the 4 pm Weekly Team Meeting) was returned
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
                                                "value": "Weekly Team Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T16:00:00-07:00",
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
                    ],
                ),
                # Milestone 2 – A new calendar entry for a sauna session at 5 pm is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Sauna",  # we’ll use a substring match below
                                    "start_datetime_iso": "2024-07-29T17:00:00-07:00",
                                    "creation_datetime_iso": "2024-07-29T07:35:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                # start_datetime_iso will default to exact-match which is desired,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_4d78ce1a-b8d7-4403-ab77-11ec8deb98cd_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:35:00-07:00",
            is_read_time="2024-07-29T07:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to schedule time to go to the sauna after work today, two hours after work "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I'm going to be tired after today, can you schedule a sauna session for me 2 hours after my last meeting today ends?",
                },
            ],
            reasoning='The user wants to schedule a sauna session 2 hours after their last meeting today ends, since they will be tired after the workday. Looking at their calendar for today, 29 July, their meetings are: Project Sync Meeting from 8:00-9:00, Data Analysis Review from 9:30-10:30, Follow-up Sync with Michelle and Dawei from 11:00-12:00, Brainstorming Session from 11:00-12:00, Client Presentation Preparation from 14:00-15:00, and Weekly Team Meeting from 16:00-17:00. The last meeting of the day is the Weekly Team Meeting, which ends at 17:00. Two hours after 17:00 is 19:00, so I create an event named "Sauna Session" for 19:00-19:30 today 29 July 2024.',
            success_conditions=[
                {
                    "input_text": '1. A calendar event "Sauna Session" is scheduled at 19:00 on July 29',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent inspects today’s calendar to locate the coworker sync
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
                    ],
                ),
                # Milestone 1 – A new calendar entry “Sauna Session” starting at 19:00 on 2024-07-29 exists
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Sauna Session",
                                    "start_datetime_iso": "2024-07-29T19:00:00-07:00",
                                    "creation_datetime_iso": "2024-07-29T07:35:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            # event name and exact start time are critical; default exact matching is fine
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore SANDBOX traces when checking CALENDAR change
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_05b86e4a-9f8c-40af-90b8-baae9ff20ac7_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:35:00-07:00",
            is_read_time="2024-07-29T07:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        'You realised that you accidentally double-booked yourself today at 11:00, where you have two meetings scheduled in your calendar - "Follow-up Sync with Michelle and Dawei" and "Brainstorming Session", and you definitely will not be able to attend both.   You need to ask the assistant to delete the "Follow-up Sync with Michelle and Dawei". '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I will have to ask you to delete the follow-up event I have in my calendar today for 11:00",
                },
            ],
            reasoning='The user has asked me to delete the "follow-up" event for today from their calendar.  There isn\'t an event in the calendar that has that exact name, but thankfully they gave me a time that I can use to cross-reference. They said it is an event at 11:00 - I found two events scheduled in the calendar - "Follow-up Sync with Michelle and Dawei" and "Brainstorming Session". One of them contains the phrase "follow-up" which the user said earlier, so they must be wanting to delete the "Follow-up Sync with Michelle and Dawei" event. I can proceed accordingly once I get confirmation from the user that this is the correct event.',
            success_conditions=[
                {
                    "input_text": "1. The system must check for events that are occurring on July 29th 2024 (today) at 11:00.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": '2 The event "Follow-up Sync with Michelle and Dawei" on July 29th 2024 (today) at 11:00 will be deleted from the user\'s calendar.',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – The agent looks up today’s 11:00 events
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
                        ),
                    ],
                ),
                # Milestone 1 – Confirms that the 11:00 “Follow-up Sync with Michelle and Dawei” event was returned
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
                                                "value": "Follow-up Sync with Michelle and Dawei",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T11:00:00-07:00",
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
                    ],
                ),
                # Milestone 2 – The event is removed from the calendar database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Follow-up Sync with Michelle and Dawei",
                                    "start_datetime_iso": "2024-07-29T11:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_22_9ab96ab5-cbef-458d-a01c-9338b349e05d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_22",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:40:00-07:00",
            is_read_time="2024-07-29T07:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to clear your schedule for today except for your dentist appointment "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Clear today except dentist",
                },
            ],
            reasoning="The user is asking me to delete multiple events.\nI should look at the user's calendar.\nThe user has asked me to delete all but one event, Dentist Appointment 13:00-14:00.\nI will go ahead and delete the following events from July 29, 2024: Project Sync Meeting 08:00-08:30, Dara Analysis Review 09:30-10:30, Brainstorming Session 11:00-12:00, Follow-up Sync with Michelle and Dawei 11:00-12:00, Client Presentation Preparation 14:00-15:00, Weekly Team Meeting 16:00-17:00.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. The event Project Sync Meeting on 29 July 2024 at 8:00-9:00 is deleted from the calendar",
                },
                {
                    "input_text": "2. The event Data Analysis Review on 29 July 2024 at 9:30-10:30 is deleted from the calendar",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The event Brainstorming Session on 29 July 2024 at 11:00-12:00 is deleted from the calendar",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "4. The event Follow-up Sync with Michelle and Dawei on 29 July 2024 at 11:00-12:00 is deleted from the calendar",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "5. The event client presentation preparation on 29 July 2024 at 14:00-15:00 is deleted from the calendar",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "6. The event Weekly Team Meeting on 29 July 2024 at 16:00-17:00 is deleted from the calendar",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Project Sync Meeting deleted
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Project Sync Meeting",
                                    "start_datetime_iso": "2024-07-29T08:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
                # Milestone 1 – Data Analysis Review deleted
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Data Analysis Review",
                                    "start_datetime_iso": "2024-07-29T09:30:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
                # Milestone 2 – Brainstorming Session deleted
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Brainstorming Session",
                                    "start_datetime_iso": "2024-07-29T11:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
                # Milestone 3 – Follow-up Sync with Michelle and Dawei deleted
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Follow-up Sync with Michelle and Dawei",
                                    "start_datetime_iso": "2024-07-29T11:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
                # Milestone 4 – Client Presentation Preparation deleted
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Client Presentation Preparation",
                                    "start_datetime_iso": "2024-07-29T14:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
                # Milestone 5 – Weekly Team Meeting deleted
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Weekly Team Meeting",
                                    "start_datetime_iso": "2024-07-29T16:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=[],
        ),
    ]
