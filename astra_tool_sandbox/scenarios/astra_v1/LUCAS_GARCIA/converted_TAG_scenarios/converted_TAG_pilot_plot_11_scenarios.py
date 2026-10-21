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
    column_list_subset_match_similarity,
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_rouge_l_similarity,
    column_str_contains_any_similarity,
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


def get_TAG_LUCAS_GARCIA_pilot_plot_11(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="LUCAS_GARCIA_11_106941a0-d0c1-4e06-8a80-c62cc0e02f85_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_11",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T17:00:00-08:00",
            is_read_time="2024-12-08T17:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know where your motivational talk was on yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where was my talk event located yesterday?",
                },
            ],
            reasoning="The user wants to know where their talk event was located at yesterday. Let me look in their Calendar to see what talk event they had yesterday. Ok, it must be the event 'Motivational Talk at Local Gym'. I will inform them that this event on December 7th from 09:00-10:00 was located at Orchard County Fitness Center.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their event 'Motivational Talk at Local Gym' on December 7th from 09:00-10:00 was located at Orchard County Fitness Center.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent looks up yesterday’s talk event in the calendar
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
                # Milestone 1 – Confirm the correct calendar event with its location was retrieved
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
                                                "value": "Motivational Talk at Local Gym",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Orchard County Fitness Center",
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
                # Milestone 2 – Agent informs the user of the correct location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Orchard County Fitness Center",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar lookup → verify correct event
                (1, 2),  # Event verified → user informed
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_11_f6896bb2-0910-48f7-855a-c6bb92082438_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "messaging",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T11:35:00-08:00",
            is_read_time="2024-12-07T11:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You did a good job with the motivational talk at the gym and have been asked to do it again at the same time next week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Copy the event 'Motivational Talk at Local Gym' that took place at 09:00 on 7th December 2024 to 09:00 on December 14th 2024.",
                },
            ],
            reasoning="The user wants me to copy an event that took place at 09:00 on December 7th 2024 called 'Motivational Talk at Local Gym'. I copied the event. They wish for it to be copied to December 14th at 09:00-10:00. I'll copy all other information over to the new event, as well, such as the invitee Olivia Clark, and the location of Orchard County Fitness Center. I'll place the event in that slot on the users calendar and let them know that the event has been created.",
            success_conditions=[
                {
                    "input_text": "1. The calendar event 'Motivational Talk at Local Gym' is copied to Saturday 14th December 2024 9:00-10:00 with all other information remaining unchanged.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – Agent uses calendar tools to find or reference the original event to be copied
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
                # Milestone 1 – Confirm the original "Motivational Talk at Local Gym" event on Dec 7, 2024 09:00 was retrieved
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
                                                "value": "Motivational Talk at Local Gym",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T09:00:00-08:00",
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
                # Milestone 2 – New copied event created on Dec 14, 2024 09:00–10:00 with same details
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Motivational Talk at Local Gym",
                                    "start_datetime_iso": "2024-12-14T09:00:00-08:00",
                                    "end_datetime_iso": "2024-12-14T10:00:00-08:00",
                                    "attendees_names": [
                                        ["Lucas Garcia", "Olivia Clark"]
                                    ],
                                    "location": "Orchard County Fitness Center",
                                    "organizer_name": "Lucas Garcia",
                                    "creation_datetime_iso": "2024-12-07T11:35:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
                                "location": column_exact_match_similarity,
                                "organizer_name": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
                # Milestone 3 – User is informed that the new event was created on the correct date and time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Mention event name and the new date & time window
                                    "content": [
                                        (
                                            "Motivational Talk at Local Gym",
                                            "December 14",
                                            "14th",
                                            "09:00",
                                            "9:00",
                                            "9 am",
                                        )
                                    ],
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
                (0, 1),  # Calendar search → confirm original event found
                (1, 2),  # Original event confirmed → new copied event created
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_11_4dfb8b73-1163-4d6f-9d5b-583488e2d02e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_11",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T16:45:00-08:00",
            is_read_time="2024-12-05T16:45:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are worried that you have scheduled your motivational talk at the local gym for the wrong time so you decide to check the time "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you tell me what time I scheduled the motivational talk at the local gym for",
                },
            ],
            reasoning='The user wants to know what time they scheduled their motivational talk at the local gym for. First thing I need to do is look at the user\'s calendar and see if there are any events that match that name. Ok I found one named "Motivational Talk at Local Gym" on December 07, 2024 at 09:00-10:00 This must be the event the user is referring to. Now that I have found it I can retrieve the time it is scheduled for and inform the user',
            success_conditions=[
                {
                    "input_text": '1. The time of the event "Motivational Talk at Local Gym" on December 07, 2024 at 09:00-10:00 is presented to the user',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent uses a calendar-lookup tool
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
                # Milestone 1 – The desired calendar event is present in the tool output
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
                                                "value": "Motivational Talk at Local Gym",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T09:00:00-08:00",
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
                # Milestone 2 – Agent tells the user the correct time
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
                                            "9 am",
                                            "9am",
                                            "9:00",
                                            "09:00",
                                            "9 a.m.",
                                            "9:00 am",
                                            "9 AM",
                                            "9:00 AM",
                                            "09:00 AM",
                                        )
                                    ],
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
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_11_49625308-ba0c-41e7-a39c-b9c37934ee77_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T10:30:00-08:00",
            is_read_time="2024-12-07T10:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You did a good job with the motivational talk at the gym and have been asked to do it again at the same time next week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Copy the event 'Motivational Talk at Local Gym' that took place at 09:00 on 7th December 2024 to 09:00 on December 14th 2024.",
                },
            ],
            reasoning="The user wants me to copy an event that took place at 09:00 on December 7th 2024 called 'Motivational Talk at Local Gym'. I copied the event. They wish for it to be copied to December 14th at 09:00. I create the event and inform the user.\n",
            success_conditions=[
                {
                    "input_text": "1. The calendar event 'Motivational Talk at Local Gym' is copied to Saturday 14th December 2024 with all other information remaining unchanged.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent tries to locate the existing calendar event
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
                # Milestone 1 – Confirm the sought-after event was actually returned
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
                                                "value": "Motivational Talk at Local Gym",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T09:00:00-08:00",
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
                # Milestone 2 – A new calendar event has been created for 14 Dec 2024 at 09:00
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Motivational Talk at Local Gym",
                                    "start_datetime_iso": "2024-12-14T09:00:00-08:00",
                                    "end_datetime_iso": "2024-12-14T10:00:00-08:00",
                                    "attendees_names": [
                                        ["Lucas Garcia", "Olivia Clark"]
                                    ],
                                    "location": "Orchard County Fitness Center",
                                    "creation_datetime_iso": "2024-12-07T10:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
                                "location": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Must find the event before confirming it
                (1, 2),  # Event retrieval precedes creation of the new one
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_11_49625308-ba0c-41e7-a39c-b9c37934ee77_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T10:30:00-08:00",
            is_read_time="2024-12-07T10:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You did a good job with the motivational talk at the gym and have been asked to do it again at the same time next week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Copy my last calendar event to the same time next week.",
                },
            ],
            reasoning="The user wants me to copy an event to a different date for them. They specified their last calendar event. I will check their calendar for the most recently completed event. I found one called 'Motivational Talk at Local Gym' so I will copy this one.\nThe user the event to be copied to the same time next week. Today is 7th December 2024. Next week would be 14th December 2024 so I will place it on that date. They wish for me to keep the time the same so it'll take place between 09:00 and 10:00. I place the event in that slot on the users calendar and let them know that the event has been created. ",
            success_conditions=[
                {
                    "input_text": "1. The calendar event 'Motivational Talk at Local Gym' is copied to Saturday 14th December 2024 with all other information remaining unchanged.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the existing calendar events
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
                # Milestone 1 – Confirm that the correct original event was found
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
                                                "value": "Motivational Talk at Local Gym",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T09:00:00-08:00",
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
                # Milestone 2 – A new calendar event one week later has been created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Motivational Talk at Local Gym",
                                    "start_datetime_iso": "2024-12-14T09:00:00-08:00",
                                    "end_datetime_iso": "2024-12-14T10:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "Lucas Garcia",
                                            "Olivia Clark",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-07T10:30:00-08:00",
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
            milestone_edge_list=[
                (0, 1),  # Look up events → verify correct event found
                (1, 2),  # Verified event → new event created
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_11_4dfb8b73-1163-4d6f-9d5b-583488e2d02e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T16:45:00-08:00",
            is_read_time="2024-12-05T16:45:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are worried that you have scheduled your motivational talk at the local gym for the wrong time so you decide to check the time "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you tell me what time I scheduled my motivational speech for",
                },
            ],
            reasoning='The user wants to know what time they scheduled their motivational speech for. First thing I need to do is look at the user\'s calendar and see if there are any events that match that name. Ok none match that but I did find one named "Motivational Talk at Local Gym" on December 07, 2024 at 09:00-10:00 This must be the event the user is referring to. Now that I have found it I can retrieve the time it is scheduled for and inform the user',
            success_conditions=[
                {
                    "input_text": '1. The time of the event "Motivational Talk at Local Gym" on December 07, 2024 at 09:00-10:00 is presented to the user',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent uses a calendar-reading tool to look up the event
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
                # Milestone 1 – Agent tells the user the scheduled time (9 am)
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
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar lookup precedes informing the user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_11_f6896bb2-0910-48f7-855a-c6bb92082438_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "messaging",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T11:35:00-08:00",
            is_read_time="2024-12-07T11:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You did a good job with the motivational talk at the gym and have been asked to do it again at the same time next week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Copy my last calendar event to the same time next week.",
                },
            ],
            reasoning="The user wants me to copy an event to a different date for them. They specified their last calendar event. I will check their calendar for the most recently completed event. I found one called 'Motivational Talk at Local Gym' from today at 9:00-10:00 so I will copy this one.\nThe user wants the event to be copied to the same time next week. Today is Saturday 7th December 2024. One week from now would be Saturday 14th December 2024 so I will place it on that date. They wish for me to keep the time the same so it'll take place between 09:00 and 10:00. I'll copy all other information over to the new event, as well, such as the invitee Olivia Clark, and the location of Orchard County Fitness Center. I'll place the event in that slot on the users calendar and let them know that the event has been created. ",
            success_conditions=[
                {
                    "input_text": "1. The calendar event 'Motivational Talk at Local Gym' is copied to Saturday 14th December 2024 9:00-10:00 with all other information remaining unchanged.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events to identify the "last calendar event"
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
                # Milestone 1 – Confirms the gym motivational talk event was retrieved as the reference event
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
                                                "value": "Motivational Talk at Local Gym",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T09:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-07T10:00:00-08:00",
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
                # Milestone 2 – New calendar event created for the same time next week with unchanged details
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Motivational Talk at Local Gym",
                                    "start_datetime_iso": "2024-12-14T09:00:00-08:00",
                                    "end_datetime_iso": "2024-12-14T10:00:00-08:00",
                                    "location": "Orchard County Fitness Center",
                                    "attendees_names": [
                                        ["Lucas Garcia", "Olivia Clark"]
                                    ],
                                    "organizer_name": "Lucas Garcia",
                                    "creation_datetime_iso": "2024-12-07T11:35:00-08:00",
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
            milestone_edge_list=[
                (0, 1),  # calendar lookup → confirm correct source event
                (1, 2),  # source event identified → create copied event next week
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_11_106941a0-d0c1-4e06-8a80-c62cc0e02f85_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_11",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T17:00:00-08:00",
            is_read_time="2024-12-08T17:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know where your motivational talk was on yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where was my event 'Motivational Talk at Local Gym' on yesterday?",
                },
            ],
            reasoning="The user wants to know where their event 'Motivational Talk at Local Gym' was located at yesterday. Let me look for this event in their Calendar. I will inform them that this event on December 7th from 09:00-10:00 was located at Orchard County Fitness Center.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their event 'Motivational Talk at Local Gym' on December 7th from 09:00-10:00 was located at Orchard County Fitness Center.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent consults the calendar
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
                # Milestone 1 – The expected event with the correct location is present in the returned tool output
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
                                                "value": "Motivational Talk at Local Gym",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Orchard County Fitness Center",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T09:00:00-08:00",
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
                # Milestone 2 – The agent tells the user where the event was held
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Orchard County Fitness Center",
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
            name="LUCAS_GARCIA_11_065aa190-bd0c-45d4-86e6-73613443e437_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T13:00:00-08:00",
            is_read_time="2024-12-07T13:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You message Olivia to see if she and some others may be interested in a outdoor motivational hike. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to arrange a group hike with everyone that attended my motivational speech but first I want to run the idea past my friend Olivia Clark.",
                },
            ],
            reasoning="The user wants to send a message back to a person named Olivia that suggests that they create and attend a hike that follows up on the recent motivational talk at Local Gym that the user has in the calendar from December 7 2024. \n\nLooking at recent conversations from user with a person named Olivia I see that he means Olivia Clark from contacts that was involved with recent motivational talk at local gym. I will message her first if she would be interested in going on a Hike with user and then I will follow up with user if they would like to create a group and send more invite messages.",
            success_conditions=[
                {
                    "input_text": "1. A message is sent to Olivia Clark inquiring if she would like to go on a outdoor hike soon.",
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
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require that Olivia (by either email or phone) is among the conversation
                                    "participants_addresses": [
                                        [
                                            (
                                                "olivia.clark@example.com",
                                                "+1 12345-6789-1000-7531",
                                            )
                                        ]
                                    ],
                                    # Message body should mention a hike
                                    "content": "hike",
                                    "creation_datetime_iso": "2024-12-07T13:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        ),
                    ],
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_11_d74a291b-618b-4009-bfd4-d471e798a6da_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T11:18:00-08:00",
            is_read_time="2024-12-07T11:18:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are occupied at the moment and want to know what Olivia has text back. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read out what Olivia said.",
                },
            ],
            reasoning="Okay so, the user is looking to know what 'Olivia' said. Checking their contacts, I can see only one matching 'Olivia', 'Olivia Clark'. Checking the message thread next between her and the user I can see they were messaging today, 7 December 2024 and the last message received from Olivia was at 11:15 saying 'Hi Lucas! It was fantastic, truly motivating. I particularly appreciated the segment on maintaining mental resilience. It was just what I needed to hear.'. Now that I have found the requested message I can read it out to the user.",
            success_conditions=[
                {
                    "input_text": "1. The text message received from Olivia Clark on 7 December 2024 at 11:15 saying 'Hi Lucas! It was fantastic, truly motivating. I particularly appreciated the segment on maintaining mental resilience. It was just what I needed to hear.' is read out to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – agent invokes a tool to look for the relevant text message(s)
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
                # Milestone 1 – confirm that the returned message includes Olivia’s 11:15 am text
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
                                                "value": "olivia.clark@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Hi Lucas! It was fantastic, truly motivating. I particularly appreciated the segment on maintaining mental resilience. It was just what I needed to hear.",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-07T11:15:00-08:00",
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
                # Milestone 2 – agent’s reply to the user contains the core content of Olivia’s message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "It was fantastic, truly motivating.",
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
        ScenarioExtension(
            name="LUCAS_GARCIA_11_d74a291b-618b-4009-bfd4-d471e798a6da_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T11:18:00-08:00",
            is_read_time="2024-12-07T11:18:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are occupied at the moment and want to know what Olivia has text back. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What did the person I was last messaging say?",
                },
            ],
            reasoning="Right so, the user is wanting to know what the last person they were messaging is saying. Checking the user's message thread, the last person they messaged was an 'Olivia Clark'. This must be who the user is referring to. The last message received from Olivia was at 11:!5 on 7 December 2024 saying 'Hi Lucas! It was fantastic, truly motivating. I particularly appreciated the segment on maintaining mental resilience. It was just what I needed to hear.'. Now that I have found the requested message, I can read this out to the user.",
            success_conditions=[
                {
                    "input_text": "1. The text message received from Olivia Clark on 7 December 2024 at 11:15 saying 'Hi Lucas! It was fantastic, truly motivating. I particularly appreciated the segment on maintaining mental resilience. It was just what I needed to hear.' is read out to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – the agent uses a message-retrieval tool to look up recent texts
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
                # Milestone 1 – the agent tells the user what Olivia said (any key phrase from the message)
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
                                            "fantastic",
                                            "truly motivating",
                                            "mental resilience",
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
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_11_e8f8ca74-06b5-4a28-addd-67ea0df535bb_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_11",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T14:55:00-08:00",
            is_read_time="2024-12-08T14:55:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You can't remember who attended your motivational talk yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who was in attendance at the first event I had yesterday?",
                },
            ],
            reasoning="The user wants to know who was in attendance at the first event they had yesterday. I'll start by figuring out which event they mean.\n\nLooking at the user's calendar for yesterday (2024-12-07), I can see they had two events: Motivational Talk at Local Gym at 09:00-10:00, and Triathlon Strategy Meeting with Brian and Team at 15:00-16:00. They're asking about the first event they had yesterday, so that would be the Motivational Talk at Local Gym.\n\nI can see that Olivia Clark was an attendee at this event, so I will inform the user of this.",
            success_conditions=[
                {
                    "input_text": "1. User is informed that Olivia Clark attended their event Motivational Talk at Local Gym at 09:00-10:00 on 2024-12-07.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent uses a calendar-retrieval tool to look up yesterday’s events
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
                # Milestone 1 – Verify the “Motivational Talk at Local Gym” event (09:00 2024-12-07) is found in the tool output
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
                                                "value": "Motivational Talk at Local Gym",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T09:00:00-08:00",
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
                # Milestone 2 – Agent’s response to the user mentions attendee “Olivia Clark”
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Olivia Clark",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
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
            name="LUCAS_GARCIA_11_9cd07ab2-03ef-4276-9aa7-9ed3ba19747a_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_11",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T06:20:00-08:00",
            is_read_time="2024-12-07T06:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to arrange brunch with your parents but first need to know what time you are finished with the motivational talk. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is the motivation event later today?",
                },
            ],
            reasoning="The user wants to know what time the event later today will be over at. I should check their Calendar for any events later today, as the request is being made on Saturday, December 7, 2024, at  06:20. \n\nHmm, looks like the user has two events tomorrow. The Motivational Talk at Local Gym from 9:00-10:00 on the 7 December 2024 and the Triathlon Strategy Meeting with Brian and Team from 15:00-16:00 on the 7 December 2024. In the query, the user says 'motivation event', which can clearly refer to the event titled: \"Motivational Talk at Local Gym\". \n\nOkay the user wants to know the end time of the motivational talk. I will check the event details for the end time. Looks like it finishes at 10:00. I will let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. User is informed the Motivational Talk at Local Gym from 9:00-10:00 on the 7 December 2024 finishes at 10:00. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent looks up today’s calendar events (expects a calendar-search related tool call)
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
                # Milestone 1 – Confirm the motivational talk ending at 10:00 was contained in the tool output of Milestone 0
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
                                                "value": "Motivational Talk at Local Gym",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-07T10:00:00-08:00",
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
                # Milestone 2 – Agent’s reply to the user includes the correct end time (10 am / 10:00)
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
                                            "10:00",
                                            "10 am",
                                            "10am",
                                            "10 a.m.",
                                            "10 o'clock",
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
            name="LUCAS_GARCIA_11_5691207b-5247-4c52-a7eb-c152c91ff72d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T08:00:00-08:00",
            is_read_time="2024-12-07T08:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You need to cancel the motivational talk later this morning as you're feeling under the weather "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Cancel the talk later as I'm too sick",
                },
            ],
            reasoning="The user wants to cancel the talk later as they're too sick. I need to determine which talk the user is referring to. The user has two events scheduled in their calendar. One of them is titled \"Motivational Talk at Local Gym\". I can assume this is the event the user is referring to so I'll cancel it.",
            success_conditions=[
                {
                    "input_text": '1. "Motivational Talk at Local Gym" is removed from the calendar ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up today’s calendar events
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
                # Milestone 1 – The correct event (“Motivational Talk at Local Gym”) appears in the tool results
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
                                                "value": "Motivational Talk at Local Gym",
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
                # Milestone 2 – Event is removed (cancellation)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Motivational Talk at Local Gym",
                                }
                            ),
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
            name="LUCAS_GARCIA_11_9cd07ab2-03ef-4276-9aa7-9ed3ba19747a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T06:20:00-08:00",
            is_read_time="2024-12-07T06:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to arrange brunch with your parents but first need to know what time you are finished with the motivational talk. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When am I done sharing my words of wisdom later this morning?",
                },
            ],
            reasoning='The user wants to know when they will be done sharing their words of wisdom later today. \n\nLet me first figure out what they mean by later today. The request is being made on Saturday, December 7, 2024, at  06:20. I explore the user calendar, and I see there is an event starting at 09:00 titled "Motivational Talk at Local Gym". This can be a different way to refer to "words of wisdom", thinking of how "words" and "talk" are related terms. The Motivational Talk at Local Gym takes place from 9:00 to 10:00 on December 7 2024. Therefore, it looks like the talk finishes at 10:00. I will let the user know. ',
            success_conditions=[
                {
                    "input_text": "1. User is informed the Motivational Talk at Local Gym from 9:00-10:00 on the 7 December 2024 finishes at 10:00. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent looks at the calendar to find the relevant event
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
                # Milestone 1 – Agent tells the user the talk ends at 10 am
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
                                            "10:00",
                                            "10 am",
                                            "10am",
                                            "10 a.m.",
                                            "10 o'clock",
                                        )
                                    ],
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
                (0, 1),  # Calendar lookup precedes the user-facing answer
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_11_e8f8ca74-06b5-4a28-addd-67ea0df535bb_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T14:55:00-08:00",
            is_read_time="2024-12-08T14:55:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You can't remember who attended your motivational talk yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who came to my motivational talk yesterday?",
                },
            ],
            reasoning="The user wants to know who came to their motivational talk yesterday. I'll have a look for this event in their calendar.\n\nI found the event the user is interested in: Motivational Talk at Local Gym at 09:00-10:00 on 2024-12-07. I can see that Olivia Clark is listed as an attendee for this event.\n\nNow I can go ahead and let the user know that Olivia Clark came to their motivational talk yesterday.",
            success_conditions=[
                {
                    "input_text": "1. User is informed that Olivia Clark attended their event Motivational Talk at Local Gym at 09:00-10:00 on 2024-12-07.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 — The agent looks up calendar information
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
                # Milestone 1 — Confirm the calendar query returned the motivational talk with Olivia Clark
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
                                                "value": "Motivational Talk at Local Gym",
                                                "partial": False,
                                            },
                                            "attendees_names": {
                                                "value": "Olivia Clark",
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
                    ],
                ),
                # Milestone 2 — The agent informs the user that Olivia Clark attended
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Olivia Clark",
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
                (0, 1),  # Calendar lookup → confirm event retrieved
                (1, 2),  # Event retrieved → inform user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_11_ea627d69-7aef-4cb7-ba7e-a571a4deb077_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T10:55:00-08:00",
            is_read_time="2024-12-07T10:55:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to thank Olivia for attending your talk, you just can't find her number in your phone. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Give me Olivia Clark's number.",
                },
            ],
            reasoning="The user is asking me for a phone number.\nFirst, I should find the named contact in the user's contacts list.\nI have found Olivia Clark. Olivia Clark's phone number is saved as +1 12345-6789-1000-7531\nI should provide this to the user.",
            success_conditions=[
                {
                    "input_text": "1. Phone number of Olivia Clark is given to the user as +1 12345-6789-1000-7531",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts"],
            milestones=[
                # Milestone 0 – Agent looks up contacts
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
                # Milestone 1 – Verify Olivia Clark with correct phone number appeared in the contact search result
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
                                                "value": "Olivia Clark",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 12345-6789-1000-7531",
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
                # Milestone 2 – Agent replies to the user with Olivia's phone number
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "12345-6789-1000-7531",
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
                (0, 1),  # Contact lookup → verify Olivia found
                (1, 2),  # Olivia found → reply to user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_11_e5c5b64a-dc6d-4190-a254-a2d1e2568135_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T11:17:00-08:00",
            is_read_time="2024-12-07T11:17:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You have a little bit of a crush on Olivia, who attends the same gym as you and also goes to your motivational talks.  You texted her earlier asking for her thoughts on your talk today.  You're eager to hear her response and get back to her as soon as she responds. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did Olivia reply?",
                },
            ],
            reasoning="The user wants to know if Olivia replied. I wonder who that is. I'll check their contacts to try and figure it out. I see one contact with that name, Olivia Clark. It must be here. I'll check the user's messages for new messages from Olivia. I see one new message from Olivia Clark, received on December 7th, 2024, at 11:15. I'll show that message to the user now. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The message from Olivia Clark, received on December 7th, 2024, at 11:15 is shown to the user. ",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent tries to locate Olivia’s message using a messages-related read tool
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
                # Milestone 1 – Verify that the tool output from Milestone 0 contained Olivia’s reply
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
                                                "value": "olivia.clark@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "fantastic",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-07T11:15:00-08:00",
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
                # Milestone 2 – Agent’s response to the user includes Olivia’s message/confirmation
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "fantastic",
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
            name="LUCAS_GARCIA_11_66809e1b-f01c-49db-bb86-9364e3a889c2_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T12:00:00-08:00",
            is_read_time="2024-12-07T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to set aside time to workshop the ideas that Olivia gave you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set aside an hour around 6 today to workshop ideas. ",
                },
            ],
            reasoning='Ok so the user wants to set aside an hour around 6 today to workshop ideas. First I\'ll start with the name of the event. I will take this from what the user intends to do so the meaning is clear. I will call the event "Workshop Ideas." Next is the runtime of the event which is given by the user. I will now create the event "Workshop Ideas" or 18:00-19:00 on 7 December 2024. ',
            success_conditions=[
                {
                    "input_text": '1. The event "Workshop Ideas" is created for 18:00-19:00 on 7 December at 12:00 on 7 December 2024. ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["create_calendar_event"],
            milestones=[
                # Milestone 0 – A new calendar event for “Workshop Ideas” from 18:00–19:00 on 7 Dec 2024 exists
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Workshop Ideas",
                                    "start_datetime_iso": "2024-12-07T18:00:00",
                                    "end_datetime_iso": "2024-12-07T19:00:00",
                                    "creation_datetime_iso": "2024-12-07T12:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_rouge_l_similarity,  # must mention “Workshop”
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to pre-task snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_11_f6896bb2-0910-48f7-855a-c6bb92082438_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "messaging",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T11:35:00-08:00",
            is_read_time="2024-12-07T11:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You did a good job with the motivational talk at the gym and have been asked to do it again at the same time next week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Copy the hands-on workshop that Olivia attended this morning to the 14th at the same time.",
                },
            ],
            reasoning='The user wants me to copy an event. I need to first figure out which event they\'re talking about. They said it was a "hands-on workshop" from this morning. The only event on the user\'s calendar this morning was "Motivational Talk at Local Gym" that took place at 9:00-10:00. That doesn\'t sound like a hands-on workshop. The user mentioned Olivia attended it. I see Olivia Clark on the invitation, so maybe the user and Olivia were talking more about the event over text. Let me look at their texts. I see they debriefed about how the motivational talk event went. I do see the term "hands-on workshop" in a text from Olivia from 11:30. It says "Honestly, I think you\'ve covered everything very well. Maybe a hands-on workshop next time? Something interactive might engage people even more.". So in reflecting on the motivational talk, she\'s saying a hands-on workshop should happen some time in the future. This must be where the user got the hands-on workshop part from. So it\'s safe to still assume the event they\'re asking me to copy is "Motivational Talk at Local Gym" especially because it happened this morning and Olivia attended it. They wish for it to be copied to December 14th at 09:00-10:00. I\'ll copy all other information over to the new event, as well, such as the invitee Olivia Clark, and the location of Orchard County Fitness Center. I\'ll place the event in that slot on the users calendar and let them know that the event has been created.',
            success_conditions=[
                {
                    "input_text": "1. The calendar event 'Motivational Talk at Local Gym' is copied to Saturday 14th December 2024 9:00-10:00 with all other information remaining unchanged.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – The agent searches calendar to find the referenced event ("this morning" with Olivia)
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
                # Milestone 1 – Confirm the "Motivational Talk at Local Gym" event on Dec 7, 2024, 09:00–10:00 was retrieved
                # This ties the user's "hands-on workshop Olivia attended this morning" request to the concrete calendar entry.
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
                                                "value": "Motivational Talk at Local Gym",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T09:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-07T10:00:00-08:00",
                                                "partial": False,
                                            },
                                            "attendees_names": {
                                                "value": [
                                                    "Lucas Garcia",
                                                    "Olivia Clark",
                                                ],
                                                "partial": True,  # allow extra attendees if any
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
                # Milestone 2 – New calendar event created on Dec 14, 2024, 09:00–10:00 copying details from the Dec 7 event
                # We only check the fields required by success conditions: same name, time range on the 14th, and unchanged other info.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Motivational Talk at Local Gym",
                                    "start_datetime_iso": "2024-12-14T09:00:00-08:00",
                                    "end_datetime_iso": "2024-12-14T10:00:00-08:00",
                                    "attendees_names": [
                                        ["Lucas Garcia", "Olivia Clark"]
                                    ],
                                    "location": "Orchard County Fitness Center",
                                    "organizer_name": "Lucas Garcia",
                                    "creation_datetime_iso": "2024-12-07T11:35:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # attendees must at least include Lucas and Olivia; allow extras but ensure those two are present
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # calendar search → confirm correct source event
                (
                    1,
                    2,
                ),  # confirmed source event → copied event created on Dec 14 at same time
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_11_66809e1b-f01c-49db-bb86-9364e3a889c2_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T12:00:00-08:00",
            is_read_time="2024-12-07T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to set aside time to workshop the ideas that Olivia gave you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Create an event "Workshop Ideas" for 18:00-19:00 this evening. ',
                },
            ],
            reasoning='Ok so the user wants to create an event "Workshop Ideas" for 18:00-19:00 this evening. First I\'ll name the event which is given by the user. Next is the runtime which is given by the user. I will now create the event "Workshop Ideas" or 18:00-19:00 on 7 December 2024. ',
            success_conditions=[
                {
                    "input_text": '1. The event "Workshop Ideas" is created for 18:00-19:00 on 7 December at 12:00 on 7 December 2024. ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["create_calendar_event"],
            milestones=[
                # Milestone 0 – verify the new calendar entry was added for the correct day and time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Workshop Ideas",
                                    "start_datetime_iso": "2024-12-07T18:00",
                                    "end_datetime_iso": "2024-12-07T19:00",
                                    "creation_datetime_iso": "2024-12-07T12:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Title must match exactly
                                "calendar_event_name": column_exact_match_similarity,
                                # Allow any timezone offset by matching only the date-time portion
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ]
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_11_e5c5b64a-dc6d-4190-a254-a2d1e2568135_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T11:17:00-08:00",
            is_read_time="2024-12-07T11:17:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You have a little bit of a crush on Olivia, who attends the same gym as you and also goes to your motivational talks.  You texted her earlier asking for her thoughts on your talk today.  You're eager to hear her response and get back to her as soon as she responds. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did Liv reply?",
                },
            ],
            reasoning="The user wants to know if Liv replied. I wonder who that is. I'll check their contacts to try and figure it out. I don't see a contact with that name. However, I see one contact with the name, Olivia Clark. I know that Liv can be used to refer to someone called Olivia. It must be her. I'll check the user's messages for new messages from Olivia. I see one new message from Olivia Clark, received on December 7th, 2024, at 11:15. I'll show that message to the user now. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The message from Olivia Clark, received on December 7th, 2024, at 11:15 is shown to the user. ",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent tries to find if “Liv/Olivia” replied by looking at the messages database
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
                # Milestone 1 – Confirm the retrieved messages include the reply from Olivia Clark
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
                                                "value": "olivia.clark@example.com",
                                                "partial": False,
                                            },
                                            # Only need a snippet of the content to confirm it is the correct reply
                                            "content": {
                                                "value": "It was fantastic",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-07T11:15:00-08:00",
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
                            reference_milestone_node_index=0,  # Parse output of Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – The agent tells the user that Olivia (Liv) replied and relays her message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "It was fantastic, truly motivating",
                                }
                            ),
                            column_similarity_measure={
                                # Check that the user-facing answer quotes or paraphrases Olivia’s reply
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
            name="LUCAS_GARCIA_11_ea627d69-7aef-4cb7-ba7e-a571a4deb077_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_11",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T10:55:00-08:00",
            is_read_time="2024-12-07T10:55:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to thank Olivia for attending your talk, you just can't find her number in your phone. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Give me that one gym member's phone number.",
                },
            ],
            reasoning="The user is looking for a contact's phone number.\nFirst, I should identify the queried contact. The user has referred to a gym member, I will look for people tagged this. I see only one potential match, Olivia Clark, who is tagged as Local gym member.\nOlivia Clark's phone number is saved as +1 12345-6789-1000-7531.\nI should provide this to the user.",
            success_conditions=[
                {
                    "input_text": "1. Phone number of Olivia Clark is given to the user as +1 12345-6789-1000-7531",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts"],
            milestones=[
                # Milestone 0 – A contact-retrieval tool is invoked
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
                # Milestone 1 – The tool output includes Olivia Clark with the correct phone number
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
                                                "value": "Olivia Clark",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 12345-6789-1000-7531",
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
                # Milestone 2 – The agent tells the user Olivia’s phone number
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "12345-6789-1000-7531",
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
    ]
