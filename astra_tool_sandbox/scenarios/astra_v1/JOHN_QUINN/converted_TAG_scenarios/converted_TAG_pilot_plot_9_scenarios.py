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
    column_list_tuple_contains_similarity,
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_any_similarity,
    not_contains_presence_similarity,
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


def get_TAG_JOHN_QUINN_pilot_plot_9(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="JOHN_QUINN_9_ded2d765-0ed2-4ae0-a427-8da862ddbf27_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T10:30:00-07:00",
            is_read_time="2024-07-23T10:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You have a strained relationship with your coworker, Bronson Chunk, and prefer to keep all communications strictly professional and within official channels. You find his private messages intrusive."
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Bronson just texted my personal cell again. Can you ask him how he even got my number and tell him to stop messaging me here? I want to be clear that I'm not okay with this.",
                },
            ],
            reasoning="User wants to reply to Bronson Chunk regarding an intrusive text. I locate Bronson Chunk in the contacts list. Since the user has already provided the specific intent and tone in the prompt, I will proceed to send the message asking how he got the number and stating that the private messaging is not okay.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A message is sent to Bronson Chunk asking how he got the number and telling him to stop messaging the personal cell because the user is not okay with it.",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent tries to locate Bronson’s prior message / contact info
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
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – Confirm the retrieval returned Bronson’s conversation
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
                                            "conversation_name": {
                                                "value": "Bronson Chunk",
                                                "partial": False,
                                            },
                                            # Accept either the name or the email in participants
                                            "participants_addresses": {
                                                "value": "bronson.chunk@palantir.com",
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
                    ]
                ),
                # Milestone 2 – A new outbound message is sent to Bronson with the required content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [
                                            (
                                                "bronson.chunk@palantir.com",
                                                "408-555-0130",
                                            ),
                                            (
                                                "john.quinn@palantir.com",
                                                "1234-5678-9108",
                                            ),
                                        ]
                                    ],
                                    "content": "Bronson, how did you get my personal number? I am not okay with you messaging me here. Please stop using this number and keep all future communication to official work channels only.",
                                    "creation_datetime_iso": "2024-07-23T10:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
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
            name="JOHN_QUINN_9_9a0cb664-cd0a-4ed4-9bab-c4d52aa66137_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T10:35:00-07:00",
            is_read_time="2024-07-23T10:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You decide you need to cancel your doctors appointment as Bronson has asked you to keep your week clear for urgent meetings "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my doctor's appointment next week",
                },
            ],
            reasoning="The user wants me to delete their doctors appointment next week. The first thing I need to do is check the user's calendar, specifically the 29th to the 4th of July. I can see one event named \"Doctor's Appointment with Dr. Emilia Jackson\". That must be the event they are referring to. I will delete it and inform the user. ",
            success_conditions=[
                {
                    "input_text": '1. The event "Doctor\'s Appointment with Dr. Emilia Jackson" at 15:00-16:00 on July 30 2024 is deleted',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up calendar events for next week
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
                # Milestone 1 – Confirms the doctor’s appointment was retrieved in the previous tool call
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
                # Milestone 2 – The doctor’s appointment is deleted from the calendar
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
                            reference_milestone_node_index=-1,  # compare with initial snapshot
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
            name="JOHN_QUINN_9_261641c7-0bea-4204-98ed-50082012c103_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-28T14:15:00-07:00",
            is_read_time="2024-07-28T14:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know what time to expect the visit from your Japanese colleagues tomorrow. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What's the start time for the first day of the international visit?",
                },
            ],
            reasoning='The user wants to know the start time for the first day of the international visit. I\'d better take a look at their calendar to figure out what event they\'d like to know about.\n\nI can see upcoming events on Monday to Friday this week (2024-07-29 to 2024-08-02) named Visit from Palantir Japan - Day 1 through to Day 5. The mention of "Japan" and "Visit" lead me to deduce that these events must be the "international visit" the user mentioned.\n\nNext, I should identify the first day of the visit. 2024-07-29 is the first day on which a "Visit from Palantir Japan" event appears, and the event title also includes "Day 1". The time of this event is 09:00 to 17:00.\n\nGreat, now I can let the user know that the start time for the first day of the international visit is 09:00 tomorrow.',
            success_conditions=[
                {
                    "input_text": "1. Start time of calendar event Visit from Palantir Japan - Day 1 on 2024-07-29 at 09:00-17:00 is presented to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent looks up calendar information
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
                # Milestone 1 – The expected “Visit from Palantir Japan – Day 1” event with the correct start time was returned
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
                                                "value": "Visit from Palantir Japan - Day 1",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T09:00:00-07:00",
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
                # Milestone 2 – The agent’s reply to the user includes the 09:00 start time
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
                                            "09:00",
                                            "9:00",
                                            "9 am",
                                            "9am",
                                            "09:00 AM",
                                            "09:00 am",
                                            "9 a.m.",
                                            "09:00 a.m.",
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
            milestone_edge_list=[
                (0, 1),  # Calendar lookup → verify correct event retrieved
                (1, 2),  # Event found → reply to user with start time
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_15136fdd-1f78-4d2e-b4a3-4734c8a7c0a6_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
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
                        "Your project manager just informed you that some of your Japanese colleagues will be visiting to begin a discussion about the situation in Peru.  You want to know when is the first meeting with the Palantir Japan team is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is my first visit with Palantir Japan scheduled for?",
                },
            ],
            reasoning="Okay so, the user is looking for their \"first visit\" event with Palantir Japan. I can check their calendar and can see there are a few events corresponding with Palantir Japan.... These must be the events that the user is referring to. I can see that the first event, 'Visit from Palantir Japan - Day 1' is scheduled for 29 July 2024 from 09:00 to 17:00 with John Quinn, Julie Patterson and Robin Selmoure. I am confident this is the event the user is asking for so I can display to them the time and date information to them.",
            success_conditions=[
                {
                    "input_text": "1. The date and time for the event 'Visit from Palantir Japan - Day 1' scheduled for 29 July 2024 from 09:00 to 17:00 with John Quinn, Julie Patterson and Robin Selmoure is displayed to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent looks up calendar information
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
                # Milestone 1 – Confirm the expected event was present in the tool output from Milestone 0
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
                                                "value": "Visit from Palantir Japan - Day 1",
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
                # Milestone 2 – Agent answers the user with the correct date and start time
                Milestone(
                    snapshot_constraints=[
                        # Date mention
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "July 29",
                                            "Jul 29",
                                            "29 July",
                                            "7-29",
                                            "07-29",
                                            "7/29",
                                            "07/29",
                                            "the 29th",
                                            "Monday",
                                            "2024-07-29T09:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity,
                            },
                        ),
                        # Time mention (start time of the meeting)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "09:00",
                                            "9:00",
                                            "9 am",
                                            "9am",
                                            "09:00 am",
                                            "9 a.m.",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Tool call → confirm event retrieved
                (1, 2),  # Event retrieved → answer to user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_f3d0704b-118d-41cf-b949-d1e0aebe415c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
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
                        "You want to cancel the doctor's appointment you've waited months for because a scheduling conflict at work has arisen. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete Doctor's Appointment with Dr. Emilia Jackson\n2024.07.30 03:00 pm - 04:00 pm\nEndomore Clinic, 450 Medical Plaza, San José, CA from my calendar. ",
                },
            ],
            reasoning="User wants to delete a calendar event from calendart and has provided me with all the necessary information to know which one. I shall delete the specified event from user's calendar. ",
            success_conditions=[
                {
                    "input_text": "1. Doctor's Appointment with Dr. Emilia Jackson\n2024.07.30 03:00 pm - 04:00 pm\nEndomore Clinic, 450 Medical Plaza, San José, CA is located on calendar. ",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. Doctor's Appointment with Dr. Emilia Jackson\n2024.07.30 03:00 pm - 04:00 pm\nEndomore Clinic, 450 Medical Plaza, San José, CA is removed form calendar. ",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (information-retrieval step)
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
                # Milestone 1 – Doctor’s appointment has been removed from the calendar
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
                                    "location": "Endomore Clinic, 450 Medical Plaza, San José, CA",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_51021406-b5de-4f60-955e-f67f115e344e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T18:00:00-07:00",
            is_read_time="2024-07-27T18:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want check the time of your upcoming event 'Visit from Palantir Japan - Day 1' as you want to be prepared for it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is the visit from Palantir Japan on Monday?",
                },
            ],
            reasoning="The user wants to know the time of the visit from Palantir Japan on Monday. I should check their Calendar for an event with that name occurring this Monday. Okay, I see one event 'Visit from Palantir Japan - Day 1' on Monday the 29th of July at 9:00 to 17:00. They must mean that event. I'll share the time of that event with the user now. ",
            success_conditions=[
                {
                    "input_text": "1. The time of the event 'Visit from Palantir Japan - Day 1' on Monday, July 29th 2024 from 09:00 to 17:00 is shared with the user. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent looks up calendar events
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
                # Milestone 1 – Confirm the desired Monday event was found in the tool output
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
                                                "value": "Visit from Palantir Japan - Day 1",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T09:00:00-07:00",
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
                            reference_milestone_node_index=0,  # parse tool outcome from milestone 0
                        ),
                    ],
                ),
                # Milestone 2 – Agent tells the user the correct time window
                Milestone(
                    snapshot_constraints=[
                        # Check that start time (around 9 AM) is mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "09:00",
                                            "9:00",
                                            "9 am",
                                            "9 a.m.",
                                            "9am",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
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
            name="JOHN_QUINN_9_fb9e29cd-8bac-4948-8290-c691f1880fbb_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "email",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
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
                    "content": "I need you to erase my physical event from my calendar next week.",
                },
            ],
            reasoning="The user wants to remove an event from the calendar. I need to figure out which event to delete. They're asking about a physical event next week. Let me look at events on their calendar for next week, so between 28 July and 3 August. The only thing that looks similar to a physical is an event named Doctor's Appointment with Dr. Emilia Jackson on 30 July from 15:00-16:00. The description of the event says \"Annual check-up and consultation\" and a physical exam is like an annual check-up, so this must be the event the user wants me to remove from the calendar. I'll delete it.",
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
                # Milestone 0 – Agent uses calendar tools to find the appointment ("physical") next week
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
                # Milestone 1 – Confirms the specific doctor's appointment event was retrieved from calendar
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
                            reference_milestone_node_index=0,  # based on the calendar lookup in milestone 0
                        ),
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
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # calendar lookup → confirm correct event identified
                (1, 2),  # identified event → event removed
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_518d814d-1764-46a2-8751-8e36ea0c982b_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T18:00:00-07:00",
            is_read_time="2024-07-27T18:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want check the time of your upcoming event 'Visit from Palantir Japan - Day 1' as you want to be prepared for it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is the first meeting with the Japanese branch?",
                },
            ],
            reasoning="The user wants to know the time of the first meeting with the Japanese branch. I should check their Calendar for an upcoming event with that name. I can't see an event with that name in the user's calendar. However, I see an event called 'Visit from Palantir Japan - Day 1' on Monday the 29th of July at 9:00 to 17:00. This sounds like it could be the event they're referring to because it mentions Palantir Japan. There are other events with this title but the user wants the first one, so I'll tell them the start and end time of 09:00-17:00 for the first event on Monday the 29th of July.",
            success_conditions=[
                {
                    "input_text": "1. The time of the event 'Visit from Palantir Japan - Day 1' on Monday, July 29th 2024 from 09:00 to 17:00 is shared with the user. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent consults the calendar to locate the meeting
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
                # Milestone 1 – The expected event was returned in the previous tool call
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
                                                "value": "Visit from Palantir Japan - Day 1",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T09:00:00-07:00",
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
                # Milestone 2 – The user is informed of the correct meeting time
                Milestone(
                    snapshot_constraints=[
                        # Confirm the agent's reply contains the event name (or a clear reference)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Palantir Japan",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Confirm the agent's reply includes the 9 AM start time in some reasonable format
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "09:00",
                                            "9:00",
                                            "9 am",
                                            "9am",
                                            "9 a.m.",
                                            "9 AM",
                                            "9 A.M.",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # retrieve calendar → confirm event retrieved
                (1, 2),  # event found → inform user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_fb9e29cd-8bac-4948-8290-c691f1880fbb_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "email",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
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
                    "content": "Delete Doctor's Appointment with Dr. Emilia Jackson from my calendar. ",
                },
            ],
            reasoning="User wants to delete a calendar event named \"Doctor's Appointment with Dr. Emilia Jackson\". I see it's currently scheduled for 30 July 2024 from 15:00-16:00 so I shall delete the specified event from user's calendar. ",
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
                # Milestone 0 – Agent searches or lists calendar events to find the doctor's appointment
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
                # Milestone 1 – Confirm the specific doctor's appointment event was retrieved from the calendar
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
                        ),
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
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # calendar search/list → confirm correct event retrieved
                (1, 2),  # confirmed event → event removed
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_51021406-b5de-4f60-955e-f67f115e344e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T18:00:00-07:00",
            is_read_time="2024-07-27T18:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want check the time of your upcoming event 'Visit from Palantir Japan - Day 1' as you want to be prepared for it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is the meeting with the Japanese branch?",
                },
            ],
            reasoning="The user wants to know the time of the meeting with the Japanese branch. I should check their Calendar for an upcoming event with that name. I can't see an event with that name in the user's calendar. However, I see an event called 'Visit from Palantir Japan - Day 1' on Monday the 29th of July at 9:00 to 17:00. This sounds like it could be that event. There are other events with a similar title but I assume the user is referring to the earliest event.  I'll share the event with the user to confirm that this is the correct event information they want and then share the time of that event with the user. ",
            success_conditions=[
                {
                    "input_text": "1. The time of the event 'Visit from Palantir Japan - Day 1' on Monday, July 29th 2024 from 09:00 to 17:00 is shared with the user. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent looks at the calendar
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
                # Milestone 1 – The expected event is found in the calendar tool output
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
                                                "value": "Visit from Palantir Japan - Day 1",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T09:00:00-07:00",
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
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – Agent tells the user the start and end time of the meeting
                Milestone(
                    snapshot_constraints=[
                        # Start time present
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "9:00",
                                            "09:00",
                                            "9 am",
                                            "9am",
                                            "9 a.m.",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # calendar lookup -> confirmation event exists
                (1, 2),  # event found -> inform user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_f3d0704b-118d-41cf-b949-d1e0aebe415c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "misinformation_no",
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
                        "You want to cancel the doctor's appointment you've waited months for because a scheduling conflict at work has arisen. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need you to erase my endocrine appointment. ",
                },
            ],
            reasoning="User wants to delete an endocrine appointment. I see user has a doctor appointment on calendar. I also see from email that this is an appointment with an edocrinologist. I shall delete this appointment from user's calendar. ",
            success_conditions=[
                {
                    "input_text": "1. Doctor's Appointment with Dr. Emilia Jackson\n2024.07.30 03:00 pm - 04:00 pm\nEndomore Clinic, 450 Medical Plaza, San José, CA is located on calendar. ",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. Doctor's Appointment with Dr. Emilia Jackson\n2024.07.30 03:00 pm - 04:00 pm\nEndomore Clinic, 450 Medical Plaza, San José, CA is removed form calendar. ",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events to locate the appointment
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
                # Milestone 1 – The appointment has been removed from the calendar
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
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar search precedes removal
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_15136fdd-1f78-4d2e-b4a3-4734c8a7c0a6_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "misinformation_no",
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
                        "Your project manager just informed you that some of your Japanese colleagues will be visiting to begin a discussion about the situation in Peru.  You want to know when is the first meeting with the Palantir Japan team is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is the first event on my calendar for next week with the visitors?",
                },
            ],
            reasoning="Right so, the user is asking for the first event on their calendar with the visitors for next week. Next week begins on 29th July 2024. On that day I can see two events scheduled, 'Visit from Palantir Japan - Day 1' scheduled from 09:00 to 17:00 with John Quinn, Julie Patterson and Robin Selmoure and 'Daily Stand-up: Security Updates' scheduled from 09:00 to 09:30 with John Quinn, Robin Selmoure and Julie Patterson. As both these events begin at the same time, it should be the 'Visit from Palantir Japan - Day 1' since it's related to visitors. I will display to them the time and date information to them.",
            success_conditions=[
                {
                    "input_text": "1. The date and time for the event 'Visit from Palantir Japan - Day 1' scheduled for 29 July 2024 from 09:00 to 17:00 with John Quinn, Julie Patterson and Robin Selmoure is displayed to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – the agent looks up next-week calendar events
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
                # Milestone 1 – the event “Visit from Palantir Japan – Day 1” is present in the tool output
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
                                                "value": "Visit from Palantir Japan - Day 1",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T09:00:00-07:00",
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
                # Milestone 2 – the agent tells the user the correct date (July 29) and mentions the visitors’ meeting
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
                                            "July 29",
                                            "Jul 29",
                                            "29 July",
                                            "7-29",
                                            "07-29",
                                            "7/29",
                                            "07/29",
                                            "the 29th",
                                            "Monday",
                                            "2024-07-29T09:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Palantir Japan",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
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
            name="JOHN_QUINN_9_261641c7-0bea-4204-98ed-50082012c103_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-28T14:15:00-07:00",
            is_read_time="2024-07-28T14:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know what time to expect the visit from your Japanese colleagues tomorrow. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is the Palantir Japan visit starting tomorrow?",
                },
            ],
            reasoning="The user wants to know what time the Palantir Japan visit is starting tomorrow. First I'd better check their calendar to see what they have scheduled tomorrow.\n\nI found an event named Visit from Palantir Japan - Day 1 scheduled for 09:00-17:00 tomorrow (2024-07-29). I'll go ahead and let the user know that this event starts at 09:00.",
            success_conditions=[
                {
                    "input_text": "1. Start time of calendar event Visit from Palantir Japan - Day 1 on 2024-07-29 at 09:00-17:00 is presented to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent consults the calendar to look for tomorrow’s visit
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
                # Milestone 1 – Confirm the desired calendar event was actually returned
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
                                                "value": "Visit from Palantir Japan - Day 1",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T09:00:00-07:00",
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
                # Milestone 2 – The agent tells the user the event starts at 09:00
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
                                            "09:00",
                                            "9:00",
                                            "9 am",
                                            "9am",
                                            "09:00 am",
                                            "09:00 AM",
                                            "9 a.m.",
                                            "09:00 a.m.",
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
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_9a0cb664-cd0a-4ed4-9bab-c4d52aa66137_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T10:35:00-07:00",
            is_read_time="2024-07-23T10:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You decide you need to cancel your doctors appointment as Bronson has asked you to keep your week clear for urgent meetings "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my doctor's appointment on the 30th please",
                },
            ],
            reasoning="The user wants me to delete their doctors appointment on the 30th. The first thing I need to do is check the user's calendar, specifically the 30th of July. There are three events on this day, one of these is named \"Doctor's Appointment with Dr. Emilia Jackson\". That must be the event they are referring to. I will delete it and inform the user",
            success_conditions=[
                {
                    "input_text": '1. The event "Doctor\'s Appointment with Dr. Emilia Jackson" at 15:00-16:00 on July 30 2024 is deleted',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (information-retrieval step)
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
                                ),
                            },
                        )
                    ],
                ),
                # Milestone 1 – Verify that the doctor’s appointment on July 30 was returned by the lookup
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
                                "content": column_one_similarity,
                            },
                        )
                    ],
                ),
                # Milestone 2 – Doctor’s appointment has been removed from the calendar (state change)
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
                            reference_milestone_node_index=-1,  # compare with pre-task snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # lookup → verify event found
                (1, 2),  # event found → event removed
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_889c50d8-e5e0-4896-b81a-7039f026adb6_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T10:30:00-07:00",
            is_read_time="2024-07-23T10:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to schedule a meeting with your coworkers to start preparations for the Palantir Japan visit. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I need you to message my coworkers, not my boss, to say "We need to meet to discuss the visit next week."',
                },
            ],
            reasoning="The user wants to message their coworkers — but not their boss — to say \"We need to meet to discuss the visit next week.\". I first check the user's Contacts to find their coworkers. At Palantir there are three coworkers: Bronson Chunk (Project Manager), Julie Patterson (Data Analyst) and Robin Selmoure (Software Engineer). Since the user said 'not my boss', I should exclude the manager, Bronson Chunk, and message the other two coworkers, Julie Patterson and Robin Selmoure. The user has provided the content of the message so I will use that in the draft, then present it to the user for their approval before I send it. ",
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Julie Patterson and Robin Selmoure saying "We need to meet to discuss the visit next week."',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up coworkers in the contact list
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
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – Julie Patterson is found in the search result from Milestone 0
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
                                                "value": "Julie Patterson",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "408-555-0131",
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
                # Milestone 2 – Agent looks up coworkers in the contact list
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
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 3 – Robin Selmoure is found in the search result from Milestone 0
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
                                                "value": "Robin Selmoure",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "408-555-0132",
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
                        )
                    ]
                ),
                # Milestone 4 – A group message is created containing Julie & Robin with correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [
                                            (
                                                "julie.patterson@palantir.com",
                                                "408-555-0131",
                                            ),
                                            (
                                                "robin.selmoure@palantir.com",
                                                "408-555-0132",
                                            ),
                                            (
                                                "john.quinn@palantir.com",
                                                "1234-5678-9108",
                                            ),
                                        ]
                                    ],
                                    "content": "We need to meet to discuss the visit next week.",
                                    "creation_datetime_iso": "2024-07-23T10:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (2, 3),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_18f82ccf-b5fe-4d2f-93fb-1974dc7f93ac_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T10:05:00-07:00",
            is_read_time="2024-07-23T10:05:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to delete your scheduled doctors appointment "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Delete the event called "Doctor\'s Appointment with Dr. Emilia Jackson" from my calendar.',
                },
            ],
            reasoning="The user wants to delete the appointment. I must determine what appointment the user is referring to. Looking through the user's calendar I can see they have a Doctor's Appointment with Dr. Emilia Jackson scheduled for next week. This is the only appointment in their calendar so I can assume this is what they are referring to. I'll ask the user for confirmation and then delete the appointment from their calendar.",
            success_conditions=[
                {
                    "input_text": '1. Calendar Event "Doctor\'s Appointment with Dr. Emilia Jackson" is deleted from the calendar ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events to locate the doctor appointment
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
                # Milestone 1 – Confirm that the doctor appointment event was actually retrieved
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
                # Milestone 2 – Verify the calendar event has been deleted
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Doctor's Appointment with Dr. Emilia Jackson",
                                    "start_datetime_iso": "2024-07-30T15:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_exact_match_similarity,
                            },
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # event search → confirmation of correct event found
                (1, 2),  # confirmation → deletion verified
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_744b4672-87c2-4311-a9d9-1e0d7d6aaf4a_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "misinformation_no",
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
                        "You were made aware of an unexpected work visit, you want to know when the first day of it is. . "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When are the asian work guests first coming?",
                },
            ],
            reasoning="The user is asking about a scheduled event.\nFirst, I should consult their calendar and determine the event they are referring to.\nI cannot see any exact matches for the user query. Searching through their calendar I can see a number of potential matches. The user has mentioned guests from asia. This may be referring to the series of events titled Visit from Palantir Japan. The first of these, Visit from Palantir Japan - Day 1 is scheduled for July 29 2024 09:00-17:00. As I can see no other matches, and the user has referred to the guests 'first coming', I am confident that this is the event being referred to.\nI should inform the user of the dates for the scheduled event.",
            success_conditions=[
                {
                    "input_text": "1. Date of event Visit from Palantir Japan - Day 1 scheduled for July 29 2024 09:00-17:00 is confirmed as July 29 2024.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent looks up calendar events
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
                # Milestone 1 – Returned calendar data includes the Day-1 visit event
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
                                                "value": "Visit from Palantir Japan - Day 1",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T09:00:00-07:00",
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
                # Milestone 2 – Agent tells the user the correct first-day date
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
                                        ("July 29", "29 July", "Jul 29", "2024-07-29")
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
            milestone_edge_list=[
                (0, 1),  # calendar lookup → confirm event exists
                (1, 2),  # confirmation of event → inform user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_744b4672-87c2-4311-a9d9-1e0d7d6aaf4a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
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
                        "You were made aware of an unexpected work visit, you want to know when the first day of it is. . "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What date is the visit from Palantir Japan - Day 1?",
                },
            ],
            reasoning="The user is asking about the date of a scheduled event.\nFirst, I should consult their calendar and find the event being referred to.\nI see an exact match for the user's query. \nThe event Visit from Palantir Japan - Day 1 is scheduled for July 29 2024 09:00-17:00. \nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Date of event Visit from Palantir Japan - Day 1 scheduled for July 29 2024 09:00-17:00 is confirmed as July 29 2024.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent checks the calendar for the requested visit
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
                # Milestone 1 – The returned calendar data contains the correct event
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
                                                "value": "Visit from Palantir Japan - Day 1",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T09:00:00-07:00",
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
                # Milestone 2 – The agent informs the user of the correct date
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("July 29", "2024-07-29", "Jul 29")],
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
                (0, 1),  # Calendar search → confirm event retrieved
                (1, 2),  # Event found → inform user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_18f82ccf-b5fe-4d2f-93fb-1974dc7f93ac_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T10:05:00-07:00",
            is_read_time="2024-07-23T10:05:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to delete your scheduled doctors appointment "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Remove "Doctor\'s Appointment with Dr. Emilia Jackson"',
                },
            ],
            reasoning='The user wants to remove "Doctor\'s Appointment with Dr. Emilia Jackson" from their calendar. I can see it is scheduled for July 30th at 3:00 pm. I will remove this event from the calendar and inform the user.',
            success_conditions=[
                {
                    "input_text": '1. Calendar Event "Doctor\'s Appointment with Dr. Emilia Jackson" is deleted from the calendar ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent searches the calendar for the doctor’s appointment
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
                # Milestone 1 – Confirm the desired event appears in the tool output from Milestone 0
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
                # Milestone 2 – The calendar event is removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Doctor's Appointment with Dr. Emilia Jackson",
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
            name="JOHN_QUINN_9_889c50d8-e5e0-4896-b81a-7039f026adb6_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T10:30:00-07:00",
            is_read_time="2024-07-23T10:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to schedule a meeting with your coworkers to start preparations for the Palantir Japan visit. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a message to Julie and Robin saying "We need to meet to discuss the visit next week."',
                },
            ],
            reasoning='The user wants to send a message to Julie and Robin saying "We need to meet to discuss the visit next week.". I should first figure out who these people are. I should check the user\'s Contacts for any contacts with these names. \n\nHmm, looks like the user only has one Julie, Julie Patterson, and one Robin, Robin Selmoure, in their Contacts so these must be who the user was talking about. \n\nI will now draft a message to these contacts, using the content the user has already provided as the contents. I will present it to the user to make sure they approve before I send it. ',
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Julie Patterson and Robin Selmoure saying "We need to meet to discuss the visit next week."',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up contacts (Julie & Robin)
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
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Julie Patterson is found in the contact lookup
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
                                                "value": "Julie Patterson",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "julie.patterson@palantir.com",
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
                # Milestone 2 – Agent looks up coworkers in the contact list
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
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 3 – Robin Selmoure is found in the contact lookup
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
                                                "value": "Robin Selmoure",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "robin.selmoure@palantir.com",
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
                        )
                    ],
                ),
                # Milestone 4 – Message sent to Julie & Robin with the correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [
                                            (
                                                "julie.patterson@palantir.com",
                                                "408-555-0131",
                                            ),
                                            (
                                                "robin.selmoure@palantir.com",
                                                "408-555-0132",
                                            ),
                                        ]
                                    ],
                                    "content": "We need to meet to discuss the visit next week.",
                                    "creation_datetime_iso": "2024-07-23T10:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (2, 3),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_6bcb5a0c-9874-405e-9e68-ebdb336ea03d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_9",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T10:30:00-07:00",
            is_read_time="2024-07-23T10:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to dictate a reply to Bronson saying that you will be nowhere near the office for the Palantir meetings "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a message reply to my boss saying "I\'m not gonna be anywhere near the office for those Palantir visits".',
                },
            ],
            reasoning='The user wants to dictate a reply to their boss\n\nI should locate the message history with this contact by searching their name in the user\'s Messages and then start a draft reply. I can\'t find by that name but have found one named "Bronson Chunk" who\'s alias is "Boss".\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly',
            success_conditions=[
                {
                    "input_text": '1. A message reply saying "I\'m not gonna be anywhere near the office for those Palantir visits" is sent to Bronson Chunk',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent looks through messages to find the conversation with Bronson
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
                # Milestone 1 – Result of the search contains the conversation with Bronson Chunk
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
                                            "conversation_name": {
                                                "value": "Bronson Chunk",
                                                "partial": False,
                                            }
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
                # Milestone 2 – A reply message is sent to Bronson containing the dictated text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [
                                            (
                                                "bronson.chunk@palantir.com",
                                                "408-555-0130",
                                            ),
                                            (
                                                "john.quinn@palantir.com",
                                                "1234-5678-9108",
                                            ),
                                        ]
                                    ],
                                    "content": "not gonna be anywhere near",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-23T10:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_1ae2ba96-8cbd-4943-b8c1-4abb67d4e524_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "contact",
                "calendar",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-28T18:45:00-07:00",
            is_read_time="2024-07-28T18:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You need to cancel some events because you are feeling unwell.  You need to email Robin Selmoure and Julie Patterson together to let them know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete Visit from Palantir Japan and Daily Stand-up from tomorrow's schedule and tell Robin & Julie I have to cancel, I have an awful fever via email.",
                },
            ],
            reasoning="The user wants to delete two named events from tomorrow's calendar so I'll delete the events that they have mentioned, Visit from Palantir Japan - Day 1 scheduled for July 29 2024 09:00-17:00 and Daily Stand-up: Security Updates scheduled for July 29 2024 09:00-09:30. They also want to send out messages to Robin Selmoure and Julie Patterson to notify them of the change. I'll send those messages now.",
            success_conditions=[
                {
                    "input_text": "1. Delete the calendar event Visit from Palantir Japan - Day 1 scheduled July 29 2024 from 09:00 to 17:00.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. Delete the calendar event Daily Stand-up: Security Updates scheduled July 29 2024 from 09:00 to 09:30.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. Send Robin Selmoure and Julie Patterson an email saying something like 'I have to cancel, I have an awful fever.'",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
                "get_all_contacts",
                "search_contacts",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Agent looks up tomorrow’s calendar events
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
                # Milestone 1 – The “Visit from Palantir Japan – Day 1” event has been removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Visit from Palantir Japan - Day 1",
                                    "start_datetime_iso": "2024-07-29T09:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T17:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                    ],
                ),
                # Milestone 2 – The “Daily Stand-up: Security Updates” event has been removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Daily Stand-up: Security Updates",
                                    "start_datetime_iso": "2024-07-29T09:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T09:30:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                    ],
                ),
                # Milestone 3 – Agent looks up contacts (Julie & Robin)
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
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 4 – Julie Patterson is found in the contact lookup
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
                                                "value": "Julie Patterson",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "julie.patterson@palantir.com",
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
                            reference_milestone_node_index=3,
                        )
                    ],
                ),
                # Milestone 5 – Agent looks up coworkers in the contact list
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
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 6 – Robin Selmoure is found in the contact lookup
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
                                                "value": "Robin Selmoure",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "robin.selmoure@palantir.com",
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
                            reference_milestone_node_index=5,
                        )
                    ],
                ),
                # Milestone 7 – An email was sent to Robin  and Julie explaining the cancellation
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        [
                                            "julie.patterson@palantir.com",
                                            "robin.selmoure@palantir.com",
                                        ]
                                    ],
                                    "body": "awful fever",
                                    "creation_datetime_iso": "2024-07-28T18:45:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "body": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR,
                    ],
                ),
            ],
            milestone_edge_list=[(3, 4), (5, 6)],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_3fd3c3c2-3f29-4a5a-a1fc-81f29d829f80_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_9",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T11:15:00-07:00",
            is_read_time="2024-07-23T11:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to dictate a reply to Bronson Chunk saying that you will be 45 minutes late to the meeting. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a message reply to Bronson Chunk saying "Hi Bronson I will be 45 minutes late to the meeting sorry about that".',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Bronson Chunk.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.\n",
            success_conditions=[
                {
                    "input_text": '1. A reply message is sent to Bronson Chunk saying "Hi Bronson I will be 45 minutes late to the meeting sorry about that.".',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages", "send_message"],
            milestones=[
                # Milestone 0 – The agent tries to locate the relevant conversation (information-retrieval)
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
                    ]
                ),
                # Milestone 1 – Verify the conversation with Bronson Chunk was actually found
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
                                            "conversation_name": {
                                                "value": "Bronson Chunk",
                                                "partial": False,
                                            },
                                            # At least be sure Bronson’s email is in the thread
                                            "participants_addresses": {
                                                "value": "bronson.chunk@palantir.com",
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
                    ]
                ),
                # Milestone 2 – A reply message containing “45 minutes late” was sent to Bronson
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Both participants should appear in the conversation
                                    "participants_addresses": [
                                        [
                                            (
                                                "bronson.chunk@palantir.com",
                                                "408-555-0130",
                                            ),
                                            (
                                                "john.quinn@palantir.com",
                                                "1234-5678-9108",
                                            ),
                                        ]
                                    ],
                                    "content": "45 minutes late",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-23T11:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial DB state
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # tool call → confirm target conversation found
                (1, 2),  # conversation found → message sent
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_3fd3c3c2-3f29-4a5a-a1fc-81f29d829f80_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T11:15:00-07:00",
            is_read_time="2024-07-23T11:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to dictate a reply to Bronson Chunk saying that you will be 45 minutes late to the meeting. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to the last person who text me and say "Hi Bronson I will be 45 minutes late to the meeting sorry about that.".',
                },
            ],
            reasoning='The user wants to reply to the last person who text them to say "Hi Bronson I will be 45 minutes late to the meeting sorry about that.".\n\nFirst I need to find who messaged the user last. I need to check the timestamps of the user\'s massages to see what the last text was and who it was sent by. \n\nLooks like the last message was received from Bronson Chunk at 10:27 on the 23 July and read "Hi John, we have an urgent visit scheduled next week from our colleagues at Palantir Japan. They need to discuss the situation in Peru. Please keep your entire week clear for meetings and preparations.".\n\nI will now send a reply to this message, using the content the user provided. ',
            success_conditions=[
                {
                    "input_text": '1. A reply message is sent to Bronson Chunk saying "Hi Bronson I will be 45 minutes late to the meeting sorry about that.".',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages", "send_message"],
            milestones=[
                # Milestone 0 – the agent looks up recent messages to determine who texted last
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
                # Milestone 1 – a reply message is sent to Bronson containing “45 minutes late”
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Ensure Bronson is among the participants
                                    "participants_addresses": [
                                        [("bronson.chunk@palantir.com", "408-555-0130")]
                                    ],
                                    # Ensure the key information about being 45 minutes late is in the body
                                    "content": "45 minutes late",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-23T11:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_1ae2ba96-8cbd-4943-b8c1-4abb67d4e524_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "contact",
                "calendar",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-28T18:45:00-07:00",
            is_read_time="2024-07-28T18:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You need to cancel some events because you are feeling unwell.  You need to email the attendees together but not your manager to let them know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Clear work events from tomorrow's calendar and tell my relevant coworkers, not my manager, I have to cancel tomorrow, I have an awful fever via email.",
                },
            ],
            reasoning="The user would like to clear all work events from tomorrow's calendar, so I'll check the calendar now. I can see that the user has 3 events scheduled but only two are work related, so I'll just delete Visit from Palantir Japan - Day 1 scheduled for July 29 2024 09:00-17:00 and Daily Stand-up: Security Updates scheduled for July 29 2024 09:00-09:30.\n Before I do though, the user has said to tell the relevant coworkers but not his manager. I'll check the events for any other attendees other than the user. There are two for both events, Robin Selmoure and Julie Patterson and the organizer Bronson Chunk. Then via contact search, Bronson is the project manager so I will not include him in the email. I'll send an email to them. Now I can permanently delete the calendar events.",
            success_conditions=[
                {
                    "input_text": "1. Delete the calendar event Visit from Palantir Japan - Day 1 scheduled July 29 2024 from 09:00 to 17:00.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. Delete the calendar event Daily Stand-up: Security Updates scheduled July 29 2024 from 09:00 to 09:30.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. Send Robin Selmoure and Julie Patterson an email saying 'I have to cancel tomorrow, I have an awful fever.'",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
                "get_all_contacts",
                "search_contacts",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Agent looks up work event
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
                # Milestone 1 – The “Visit from Palantir Japan – Day 1” event has been removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Visit from Palantir Japan - Day 1",
                                    "start_datetime_iso": "2024-07-29T09:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T17:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                    ],
                ),
                # Milestone 2 – The “Daily Stand-up: Security Updates” event has been removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Daily Stand-up: Security Updates",
                                    "start_datetime_iso": "2024-07-29T09:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T09:30:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                    ],
                ),
                # Milestone 3 – Agent looks up contacts (Julie & Robin)
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
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 4 – Julie Patterson is found in the contact lookup
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
                                                "value": "Julie Patterson",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "julie.patterson@palantir.com",
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
                            reference_milestone_node_index=3,
                        )
                    ],
                ),
                # Milestone 5 – Agent looks up coworkers in the contact list
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
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 6 – Robin Selmoure is found in the contact lookup
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
                                                "value": "Robin Selmoure",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "robin.selmoure@palantir.com",
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
                            reference_milestone_node_index=5,
                        )
                    ],
                ),
                # Milestone 7 – Agent looks up coworkers in the contact list
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
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 8 – Bronson is found in the contact lookup
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
                                                "value": "Bronson Chunk",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "bronson.chunk@palantir.com",
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
                            reference_milestone_node_index=7,
                        )
                    ],
                ),
                # Milestone 9 – An email was sent to Robin  and Julie explaining the cancellation
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        [
                                            "julie.patterson@palantir.com",
                                            "robin.selmoure@palantir.com",
                                        ]
                                    ],
                                    "body": "awful fever",
                                    "creation_datetime_iso": "2024-07-28T18:45:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "body": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR,
                    ],
                ),
            ],
            milestone_edge_list=[(3, 4), (5, 6), (7, 8)],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_6bcb5a0c-9874-405e-9e68-ebdb336ea03d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_9",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T10:30:00-07:00",
            is_read_time="2024-07-23T10:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to dictate a reply to Bronson saying that you will be nowhere near the office for the Palantir meetings "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a message reply to Bronson Chunk saying "I\'m not gonna be anywhere near the office for those Palantir visits".',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Bronson Chunk\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly",
            success_conditions=[
                {
                    "input_text": '1. A message reply saying "I\'m not gonna be anywhere near the office for those Palantir visits" is sent to Bronson Chunk',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the existing conversation / messages with Bronson
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
                # Milestone 1 – Confirm that the retrieved result actually contains the Bronson Chunk conversation
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
                                            "conversation_name": {
                                                "value": "Bronson Chunk",
                                                "partial": False,
                                            }
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
                # Milestone 2 – A new outgoing message is actually sent to Bronson with the dictated content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Both John and Bronson must be in the thread
                                    "participants_addresses": [
                                        [
                                            (
                                                "bronson.chunk@palantir.com",
                                                "408-555-0130",
                                            ),
                                            (
                                                "john.quinn@palantir.com",
                                                "1234-5678-9108",
                                            ),
                                        ]
                                    ],
                                    "content": "not gonna be anywhere near the office",
                                    "creation_datetime_iso": "2024-07-23T10:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_32931812-8549-4995-ac08-367d839a81cc_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_9",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T10:30:00-07:00",
            is_read_time="2024-07-23T10:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want Bronson Chunk's message read aloud to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read the text message from Bronson.",
                },
            ],
            reasoning="The user wants me to read Bronson's text message. Bronson Chunk is the only contact by that name, so I will look for the last message from Bronson Chunk.\n\nI can see a text message from Bronson Chunk received at 10:27:38 on July 23rd 2024 that says 'Hi John, we have an urgent visit scheduled next week from our colleagues at Palantir Japan. They need to discuss the situation in Peru. Please keep your entire week clear for meetings and preparations.' I will read this out to the user.",
            success_conditions=[
                {
                    "input_text": "1. The text message from 408-555-0130 sent at 10:27 on July 23rd 2024 with the text 'Hi John, we have an urgent visit scheduled next week from our colleagues at Palantir Japan. They need to discuss the situation in Peru. Please keep your entire week clear for meetings and preparations.' is read aloud.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
            milestones=[
                # Milestone 0 – the agent queries the messages database
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
                # Milestone 1 – confirm the Bronson message was returned by the tool in Milestone 0
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
                                            "conversation_name": {
                                                "value": "Bronson Chunk",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "urgent visit scheduled next week",
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
                # Milestone 2 – the agent reads the message aloud to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "urgent visit",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_c08c826c-72a7-4501-a21d-9d8d71170592_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T12:30:00-07:00",
            is_read_time="2024-07-23T12:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to see if you need to reschedule any events due to the visit by your Japanese colleagues. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I might have to reschedule a few things in my calendar due to the meetings with colleagues from overseas. Can you tell me what events I have that clash with that?",
                },
            ],
            reasoning="The user wants me to check for clashes in their calendar. The events they want to check for clashes with events based around 'colleagues from overseas'. Looking at the user's calendar, I see the event \"Daily Stand-up: Security Updates\" that mentions Peru in the notes, but it just says the meeting is to address the security situation, so it doesn't sound like anyone is visiting. I see multiple events with \"visit from Palantir Japan\" in the title. Palantir is where the user works, so Palantir Japan must be the branch that their overseas colleagues work at. I'll assume this series of meetings is what the user is talking about. To start, I have found 5 events with for that visit from Palantir Japan taking place between 09:00 and 17:00 daily from Monday 29th July to Friday 2nd August 2024. Now I need to tell the user which other events in their calendar overlap with the Visit from Palantir Japan events. \nI will check these time ranges for clashes. I have found a daily clash at 09:00 called Daily Stand-up: Security Updates. This clash lasts 30 minutes every morning. \nThere is one more clash on Tuesday 30th July from 15:00 to 16:00 called Doctor's Appointment with Dr. Emilia Jackson.\nI inform the user of these clashes.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The user is informed that one event, "Daily Stand-up: Security Updates" from 9:00-9:30 on 29 July 2024, overlaps with the event "Visit from Palantir Japan - Day 1"',
                },
                {
                    "input_text": '2. The user is informed that two events overlap with the event "Visit from Palantir Japan - Day 2" event on 30 July 2024: "Daily Stand-up: Security Updates" from 9:00-9:30, and "Doctor\'s Appointment with Dr. Emilia Jackson" from 15:00-16:00',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": '3. The user is informed that one event, "Daily Stand-up: Security Updates" from 9:00-9:30 on 31 July 2024, overlaps with the event "Visit from Palantir Japan - Day 3"',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": '4. The user is informed that one event, "Daily Stand-up: Security Updates" from 9:00-9:30 on 1 August 2024, overlaps with the event "Visit from Palantir Japan - Day 4"',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": '5. The user is informed that one event, "Daily Stand-up: Security Updates" from 9:00-9:30 on 2 August 2024, overlaps with the event "Visit from Palantir Japan - Day 5',
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent looks up calendar data to determine overlaps
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
                # Milestone 1 – The user is informed of every required overlap
                Milestone(
                    snapshot_constraints=[
                        # Day-1 clash
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Visit from Palantir Japan",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Daily Stand-up: Security Updates",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # # Day-2 clashes (stand-up + doctor)
                        # SnapshotConstraint(
                        #     database_namespace=DatabaseNamespace.SANDBOX,
                        #     snapshot_constraint=snapshot_similarity,
                        #     target_dataframe=pl.DataFrame(
                        #         {
                        #             "sender": RoleType.AGENT,
                        #             "recipient": RoleType.USER,
                        #             "content": "Visit from Palantir Japan - Day 2",
                        #         }
                        #     ),
                        #     column_similarity_measure={
                        #         "content": column_contains_similarity
                        #     },
                        # ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Doctor",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # # Day-3 clash
                        # SnapshotConstraint(
                        #     database_namespace=DatabaseNamespace.SANDBOX,
                        #     snapshot_constraint=snapshot_similarity,
                        #     target_dataframe=pl.DataFrame(
                        #         {
                        #             "sender": RoleType.AGENT,
                        #             "recipient": RoleType.USER,
                        #             "content": "Visit from Palantir Japan - Day 3",
                        #         }
                        #     ),
                        #     column_similarity_measure={
                        #         "content": column_contains_similarity
                        #     },
                        # ),
                        # # Day-4 clash
                        # SnapshotConstraint(
                        #     database_namespace=DatabaseNamespace.SANDBOX,
                        #     snapshot_constraint=snapshot_similarity,
                        #     target_dataframe=pl.DataFrame(
                        #         {
                        #             "sender": RoleType.AGENT,
                        #             "recipient": RoleType.USER,
                        #             "content": "Visit from Palantir Japan - Day 4",
                        #         }
                        #     ),
                        #     column_similarity_measure={
                        #         "content": column_contains_similarity
                        #     },
                        # ),
                        # # Day-5 clash
                        # SnapshotConstraint(
                        #     database_namespace=DatabaseNamespace.SANDBOX,
                        #     snapshot_constraint=snapshot_similarity,
                        #     target_dataframe=pl.DataFrame(
                        #         {
                        #             "sender": RoleType.AGENT,
                        #             "recipient": RoleType.USER,
                        #             "content": "Visit from Palantir Japan - Day 5",
                        #         }
                        #     ),
                        #     column_similarity_measure={
                        #         "content": column_contains_similarity
                        #     },
                        # ),
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_518d814d-1764-46a2-8751-8e36ea0c982b_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T18:00:00-07:00",
            is_read_time="2024-07-27T18:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want check the time of your upcoming event 'Visit from Palantir Japan - Day 1' as you want to be prepared for it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is the longer of my two events two days from now?",
                },
            ],
            reasoning='The user wants to know the time of an event. I need to determine which event on their calendar they\'re talking about. The event is one of two events happening two days from now. Two days from today, July 27th, is July 29th. The two events happening on July 29th are "Visit from Palantir Japan - Day 1" from 09:00-17:00 and "Daily Stand-up: Security Updates" from 09:00-9:30. So I need to find the longer event between these two, and that\'s the event the user wants more information about. The former is 8 hours long because 17 minus 9 is 8. The latter is .5 hours long because 9:30 minus 9:00 is 30 minutes, or a half hour. So when the user says "the longer of my two events" they are referring to the event named "Visit from Palantir Japan - Day 1". So they want to know what time that event is happening. I\'ll tell them it starts at 9:00 and ends at 17:00 on July 29th.',
            success_conditions=[
                {
                    "input_text": "1. The time of the event 'Visit from Palantir Japan - Day 1' on Monday, July 29th 2024 from 09:00 to 17:00 is shared with the user. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent’s reply to the user includes the event **start time**
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Accept any reasonable phrasing of 09:00 / 9 am
                                    "content": [
                                        (
                                            "09:00",
                                            "9:00",
                                            "9 am",
                                            "9am",
                                            "09:00 am",
                                            "09:00am",
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
                # Milestone 1 – Agent’s reply to the user includes the event **end time**
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Accept any reasonable phrasing of 17:00 / 5 pm
                                    "content": [
                                        (
                                            "17:00",
                                            "5:00",
                                            "5 pm",
                                            "5pm",
                                            "17:00 pm",
                                            "17:00pm",
                                            "5 p.m.",
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
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_9_c08c826c-72a7-4501-a21d-9d8d71170592_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_9",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T12:30:00-07:00",
            is_read_time="2024-07-23T12:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to see if you need to reschedule any events due to the visit by your Japanese colleagues. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Are there any clashes in my calendar with the 'Visit from Palantir Japan' events?",
                },
            ],
            reasoning="The user wants me to check for clashes in their calendar. The events they want to check for clashes with have 'Visit from Palantir Japan' in their title. I have found 5 events with that in their title taking place between 09:00 and 17:00 daily from Monday 29th July to Friday 2nd August 2024.\nI will check these time ranges for clashes. I have found a daily clash at 09:00 called Daily Stand-up: Security Updates. This clash lasts 30 minutes every morning. \nThere is one more clash on Tuesday 30th July from 15:00 to 16:00 called Doctor's Appointment with Dr. Emilia Jackson.\nI inform the user of these clashes.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The user is informed that one event, "Daily Stand-up: Security Updates" from 9:00-9:30 on 29 July 2024, overlaps with the event "Visit from Palantir Japan - Day 1"',
                },
                {
                    "input_text": '2. The user is informed that two events overlap with the event "Visit from Palantir Japan - Day 2" event on 30 July 2024: "Daily Stand-up: Security Updates" from 9:00-9:30, and "Doctor\'s Appointment with Dr. Emilia Jackson" from 15:00-16:00',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": '3. The user is informed that one event, "Daily Stand-up: Security Updates" from 9:00-9:30 on 31 July 2024, overlaps with the event "Visit from Palantir Japan - Day 3"',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": '4. The user is informed that one event, "Daily Stand-up: Security Updates" from 9:00-9:30 on 1 August 2024, overlaps with the event "Visit from Palantir Japan - Day 4"',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": '5. The user is informed that one event, "Daily Stand-up: Security Updates" from 9:00-9:30 on 2 August 2024, overlaps with the event "Visit from Palantir Japan - Day 5',
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0  –  The agent queries the calendar to look for potential clashes
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
                # Milestone 1  –  The user is informed about every required clash
                # We only check that the agent’s reply to the user mentions each overlapping pair/event
                Milestone(
                    snapshot_constraints=[
                        # Overlap for Day 1
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Visit from Palantir Japan",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Daily Stand-up",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # # Overlap for Day 2  (includes the doctor’s appointment)
                        # SnapshotConstraint(
                        #     database_namespace=DatabaseNamespace.SANDBOX,
                        #     snapshot_constraint=snapshot_similarity,
                        #     target_dataframe=pl.DataFrame(
                        #         {
                        #             "sender": RoleType.AGENT,
                        #             "recipient": RoleType.USER,
                        #             "content": "Visit from Palantir Japan - Day 2",
                        #         }
                        #     ),
                        #     column_similarity_measure={
                        #         "content": column_contains_similarity
                        #     },
                        # ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Doctor",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # # Overlap for Day 3
                        # SnapshotConstraint(
                        #     database_namespace=DatabaseNamespace.SANDBOX,
                        #     snapshot_constraint=snapshot_similarity,
                        #     target_dataframe=pl.DataFrame(
                        #         {
                        #             "sender": RoleType.AGENT,
                        #             "recipient": RoleType.USER,
                        #             "content": "Visit from Palantir Japan - Day 3",
                        #         }
                        #     ),
                        #     column_similarity_measure={
                        #         "content": column_contains_similarity
                        #     },
                        # ),
                        # # Overlap for Day 4
                        # SnapshotConstraint(
                        #     database_namespace=DatabaseNamespace.SANDBOX,
                        #     snapshot_constraint=snapshot_similarity,
                        #     target_dataframe=pl.DataFrame(
                        #         {
                        #             "sender": RoleType.AGENT,
                        #             "recipient": RoleType.USER,
                        #             "content": "Visit from Palantir Japan - Day 4",
                        #         }
                        #     ),
                        #     column_similarity_measure={
                        #         "content": column_contains_similarity
                        #     },
                        # ),
                        # # Overlap for Day 5
                        # SnapshotConstraint(
                        #     database_namespace=DatabaseNamespace.SANDBOX,
                        #     snapshot_constraint=snapshot_similarity,
                        #     target_dataframe=pl.DataFrame(
                        #         {
                        #             "sender": RoleType.AGENT,
                        #             "recipient": RoleType.USER,
                        #             "content": "Visit from Palantir Japan - Day 5",
                        #         }
                        #     ),
                        #     column_similarity_measure={
                        #         "content": column_contains_similarity
                        #     },
                        # ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
    ]
