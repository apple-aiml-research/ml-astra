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
    column_datetime_window_similarity,
    column_exact_match_similarity,
    column_list_tuple_contains_similarity,
    column_one_similarity,
    column_tool_trace_matches_tool_names,
    removal_similarity,
    snapshot_similarity,
    tool_trace_dependant_similarity,
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


def get_TAG_JOHN_QUINN_challenging_scenarios(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="JOHN_QUINN_4_b7816c79-6f90-4b35-92a7-b62dc79bfe3e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_4",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T16:15:00-07:00",
            is_read_time="2024-07-22T16:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to dictate a reply to Robin Selmour asking if she wants to meet to talk about the Peru crisis. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to Robin\'s text from ten minutes ago and say "Do you want to meet tomorrow to talk about the Peru crisis?".',
                },
            ],
            reasoning="The user wants to reply to Robin's text. There's only one Robin in their contacts, Robin Selmoure. Robin's most recent message says \"Understood, John. If you ever feel like sharing, you know where to find me!' and it was delivered at 16:08. But the user wants to reply to a message received ten minutes ago, and 16:08 was only seven minutes ago. I suppose the user was making an approximation when they said ten minutes, because this is the only message they could respond to. I'll craft the reply \"Do you want to meet tomorrow to talk about the Peru crisis?\" and send it.",
            success_conditions=[
                {
                    "input_text": "1. A reply text message is sent to Robin Selmour on 22 July 2024 at 16:15 saying 'Do you want to meet tomorrow to talk about the Peru crisis?'.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["search_messages", "get_all_messages", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up recent messages (or conversations) to find Robin's last text to reply to
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
                                        "search_messages",
                                        "get_all_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – confirm the retrieved results include the correct last message from Robin Selmoure
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
                                                "value": "robin.selmoure@palantir.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Understood, John. If you ever feel like sharing, you know where to find me!",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-22T16:08:00-07:00",
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
                                "content": column_one_similarity,
                            },
                            reference_milestone_node_index=0,  # depend on retrieval in milestone 0
                        )
                    ],
                ),
                # Milestone 2 – A message is sent to Robin with the requested content, as a reply around the target time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Participants: John and Robin, identified by their email addresses
                                    "participants_addresses": [
                                        [
                                            (
                                                "john.quinn@palantir.com",
                                                "1234-5678-9108",
                                            ),
                                            (
                                                "robin.selmoure@palantir.com",
                                                "408-555-0132",
                                            ),
                                        ]
                                    ],
                                    "content": "Do you want to meet tomorrow to talk about the Peru crisis?",
                                    "status": "sent",
                                    # Creation time on July 22, 2024 at ~16:15, allow approximate match
                                    "creation_datetime_iso": "2024-07-22T16:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieve messages
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_fb9e29cd-8bac-4948-8290-c691f1880fbb_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "email",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T11:00:00-07:00",
            is_read_time="2024-07-23T11:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to cancel the doctor's appointment you've waited months for because a scheduling conflict at work has arisen.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my Doctor's Appointment with Dr. Emilia Jackson next Monday.",
                },
            ],
            reasoning="User wants to delete a calendar event named \"Doctor's Appointment with Dr. Emilia Jackson\". They claimed it's next Monday, which would be 29 July, but I see on the user's calendar this event is currently scheduled for 30 July 2024 from 15:00-16:00. Even though the user said Monday, this is the only event with that name happening that week, so I shall delete the specified event from user's calendar and let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. The event named \"Doctor's Appointment with Dr. Emilia Jackson\" on 30 July 2024 from 15:00-16:00 is removed from the user's calendar. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "remove_calendar_event",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – Agent searches calendar to find the doctor's appointment event
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
                # Milestone 1 – Confirms that the specific doctor's appointment on July 30, 2024 was retrieved
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
                                                "value": "Doctor's Appointment with Dr. Emilia Jackson",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-30T15:00:00-07:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-07-30T16:00:00-07:00",
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
                # Milestone 2 – The doctor's appointment event has been removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Doctor's Appointment with Dr. Emilia Jackson",
                                    "start_datetime_iso": "2024-07-30T15:00:00-07:00",
                                    "end_datetime_iso": "2024-07-30T16:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar search → confirm correct event retrieved
                (1, 2),  # Event identified → event removed
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_fb9e29cd-8bac-4948-8290-c691f1880fbb_single_turn_3",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "email",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_yes",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T11:00:00-07:00",
            is_read_time="2024-07-23T11:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to cancel the doctor's appointment you've waited months for because a scheduling conflict at work has arisen."
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the event that I confirmed after the Endomore Clinic Team emailed me about it.",
                },
            ],
            reasoning="The user wants to delete an event. They said it's an event that the Endomore Clinic Team emailed them about. To figure out which event that is, let me look at the user's emails. I see two emails with the content ending with a signature from The Endomore Clinic Team, from appointments@endomoreclinic.com. One is \"Reminder: Upcoming Appointment with Dr. Emilia Jackson\" from today at 9:00, and another is \"Confirmation of Your Appointment with Dr. Emilia Jackson\" from today at 10:00. Both mention the appointment on 30 July 2024 at 15:00, but the user did not reply to either of them or show confirmation in any way, so I don't have a way to verify that the user confirmed the appointment, but I can be sure these emails will point me to the event the user is referring to. Let me look at the calendar on the date mentioned in the email, 30 July 2024. I see an event named \"Doctor's Appointment with Dr. Emilia Jackson\" scheduled for 15:00-16:00, so I'll ask the user's confirmation and delete this one.",
            success_conditions=[
                {
                    "input_text": "1. The event named \"Doctor's Appointment with Dr. Emilia Jackson\" on 30 July 2024 from 15:00-16:00 is removed from the user's calendar. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "remove_calendar_event",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – Agent uses a calendar lookup tool to find the referenced appointment event
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
                # Milestone 1 – Confirms the specific doctor's appointment event was retrieved
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
                                                "value": "Doctor's Appointment with Dr. Emilia Jackson",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-30T15:00:00-07:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-07-30T16:00:00-07:00",
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
                                "content": column_one_similarity,
                            },
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – The doctor's appointment event is removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Doctor's Appointment with Dr. Emilia Jackson",
                                    "start_datetime_iso": "2024-07-30T15:00:00-07:00",
                                    "end_datetime_iso": "2024-07-30T16:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # calendar lookup → confirm correct event retrieved
                (1, 2),  # correct event identified → event removed
            ],
        ),
    ]
