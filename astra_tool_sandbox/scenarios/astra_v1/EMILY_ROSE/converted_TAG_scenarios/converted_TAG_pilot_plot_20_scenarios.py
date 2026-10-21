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
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_any_similarity,
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


def get_TAG_EMILY_ROSE_pilot_plot_20(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="EMILY_ROSE_20_19d00cac-e46a-4354-b2a9-e8bff6fd03b8_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_20",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T14:00:00-08:00",
            is_read_time="2024-12-16T14:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "The event you coordinated with Linda went extremely well! The school is asking if you could try to plan another one in January after the holidays.   If you use the same format and just adapt some things you can reuse your preparation - so you'll add a new event for this in your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I\'d like to add the event "EA Coordination Round 2" to the calendar for January 14th 2025 and put it to start at the same time as the event I just had',
                },
            ],
            reasoning='The user asked me to make a new event, "EA Coordination Round 2" to the calendar for January 14th 2025. But they gave me a really vague description of the time I need to set it at. They told me to "put it to start at the same time as the event they just had". So I\'m going to need to check the user\'s calendar for the most recent event they had... I found the event "Educational Activities Coordination Meeting" which occurred earlier today at 09:00. Is it possible that the user wants the new event time to begin at 09:00? \n\nWith the user\'s confirmation, I\'ll create the new event "EA Coordination Round 2" for January 14th 2025 at 09:00.',
            success_conditions=[
                {
                    "input_text": '1. The event "EA Coordination Round 2" is created for January 14th 2025 at 09:00 in the user\'s calendar.',
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
                # Milestone 0 – Agent queries the calendar to figure out the time of the previous event
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
                # Milestone 1 – The earlier event with the 09:00 start time is indeed found
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
                                                "value": "Educational Activities Coordination Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-16T09:00:00-08:00",
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
                # Milestone 2 – A new calendar event is added at the right date and time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "EA Coordination Round 2",
                                    "start_datetime_iso": "2025-01-14T09:00:00-08:00",
                                    "creation_datetime_iso": "2024-12-16T14:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_exact_match_similarity,
                                "start_datetime_iso": column_contains_similarity,
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
            name="EMILY_ROSE_20_19d00cac-e46a-4354-b2a9-e8bff6fd03b8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_20",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T14:00:00-08:00",
            is_read_time="2024-12-16T14:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "The event you coordinated with Linda went extremely well! The school is asking if you could try to plan another one in January after the holidays.   If you use the same format and just adapt some things you can reuse your preparation - so you'll add a new event for this in your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I\'d like to add another one to my calendar called "EA Coordination Round 2" for January 14th 2025 at 09:00.',
                },
            ],
            reasoning='The user is asking me to add "another one to their calendar". I\'m not fully sure what the user means, but the full utterance looks like they want me to add a new event to their calendar. If this is so, I have the date, time and event title that I can use to create the event. \n\nWith the user\'s confirmation, I\'ll add "EA Coordination Round 2" to the calendar for January 14th 2025 at 09:00.',
            success_conditions=[
                {
                    "input_text": '1. The event "EA Coordination Round 2" is created for January 14th 2025 at 09:00 in the user\'s calendar.',
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
                # Milestone 0 – Verify that a new calendar event titled
                # “EA Coordination Round 2” starting on 2025-01-14 at 09:00 was added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "EA Coordination Round 2",
                                    "start_datetime_iso": "2025-01-14T09:00:00-08:00",
                                    "creation_datetime_iso": "2024-12-16T14:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_20_003e80dc-8467-40bf-8d1d-1471cb360da5_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_20",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T08:15:00-08:00",
            is_read_time="2024-12-16T08:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know the location of your 'Educational Activities Coordination Meeting' to beat the traffic. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where is my activities coordination meeting\ntaking place?",
                },
            ],
            reasoning="Right so, the user is wanting to know the location of their 'activities coordination meeting'. I can see from their calendar that there is one event matching titled 'Educational Activities Coordination Meeting' which is scheduled on 16 December 2024 from 09:00 to 10:00. I can see the event is taking place at the 'Orchard County Community Center'. I can then read this out to the user.",
            success_conditions=[
                {
                    "input_text": "1. The location of 'Educational Activities Coordination Meeting', 'Orchard County Community Center', which is scheduled on 16 December 2024 from 09:00 to 10:00 is read out to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent uses a calendar-reading tool to locate the meeting
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
                # Milestone 1 – Returned calendar data contains the correct event and location
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
                                                "value": "Educational Activities Coordination Meeting",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Orchard County Community Center",
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
                    ],
                ),
                # Milestone 2 – Agent tells the user the meeting location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Orchard County Community Center",
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
            name="EMILY_ROSE_20_003e80dc-8467-40bf-8d1d-1471cb360da5_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_20",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T08:15:00-08:00",
            is_read_time="2024-12-16T08:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know the location of your 'Educational Activities Coordination Meeting' to beat the traffic. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What's the location of my next event?",
                },
            ],
            reasoning="Okay so, the user is looking for the location of their next event. Checking their calendar I can see that their next event is on today, 16 December 2024 from 09:00 to 10:00, titled 'Educational Activities Coordination Meeting' with Linda Kim. The location is listed as 'Orchard County Community Center' and I can read this out to the user.",
            success_conditions=[
                {
                    "input_text": "1. The location of 'Educational Activities Coordination Meeting', 'Orchard County Community Center', which is scheduled on 16 December 2024 from 09:00 to 10:00 is read out to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent receives calendar data via a calendar-retrieval tool call
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
                # Milestone 1 – Confirm the expected meeting and its location appear in the tool output
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
                                                "value": "Educational Activities Coordination Meeting",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Orchard County Community Center",
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
                # Milestone 2 – The agent tells the user the meeting location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Orchard County Community Center",
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
                (0, 1),  # Tool call → verify returned event
                (1, 2),  # Verified event → user informed
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_20_beda73f9-e0ad-4a8c-9679-89c000a2bd7c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_20",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T13:00:00-08:00",
            is_read_time="2024-12-16T13:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know what was the location of your event 'Educational Activities Coordination Meeting' as you're forgetful. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where was my event held earlier today?",
                },
            ],
            reasoning="The user wants to know where their event was held earlier today. Let me look in Calendar to see what event they had on earlier today. I can see an event that took place today, 16 December 2024 from 09:00 to 10:00 titled 'Educational Activities Coordination Meeting', with Linda Kim as an attendee. The event was held at 'Orchard County Community Center'. I will inform them of this.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their event 'Educational Activities Coordination Meeting' on December 16th 2024 from 09:00 to 10:00 was located at Orchard County Community Center.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent uses a calendar-reading tool to look up today's events
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
                # Milestone 1 – The returned calendar data contains the correct meeting
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
                                                "value": "Educational Activities Coordination Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-16T09:00:00-08:00",
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
                # Milestone 2 – The agent’s reply to the user includes the correct location information
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Orchard County Community Center",
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
                (0, 1),  # Tool use → verify correct event found
                (1, 2),  # Correct event found → user informed
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_20_beda73f9-e0ad-4a8c-9679-89c000a2bd7c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_20",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T13:00:00-08:00",
            is_read_time="2024-12-16T13:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know what was the location of your event 'Educational Activities Coordination Meeting' as you're forgetful. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where was the event 'Educational Activities Coordination Meeting' located?",
                },
            ],
            reasoning="The user wants to know where their event 'Educational Activities Coordination Meeting' was held. Let me look in Calendar. I can see one event matching which took place earlier today, 16 December 2024 from 09:00 to 10:00 with Linda Kim as an attendee. The location is noted as'Orchard County Community Center'. I will inform them of this.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their event 'Educational Activities Coordination Meeting' on December 16th 2024 from 09:00 to 10:00 was located at Orchard County Community Center.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent queries calendar data
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
                # Milestone 1 – The expected meeting with the correct location is found
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
                                                "value": "Educational Activities Coordination Meeting",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Orchard County Community Center",
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
                    ],
                ),
                # Milestone 2 – Agent informs the user of the meeting location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Orchard County Community Center",
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
                (0, 1),  # Calendar query → verify meeting found
                (1, 2),  # Meeting found → user informed
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_20_48ab1ac1-a24d-41ec-9d9a-780dd198a19d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_20",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T10:15:00-08:00",
            is_read_time="2024-12-16T10:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You feel like the event you were just at took forever and want to see how long it was. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'How long was "Educational Activities Coordination Meeting?"',
                },
            ],
            reasoning='OK so the user wants to know how long was "Educational Activities Coordination Meeting." First I will find the event given by the user. Now that I have found it I will look at the runtime of the event. I will now inform the user that the event "Educational Activities Coordination Meeting" ran from 09:00-10:00 on 16 December 2024; therefore had a runtime of one hour. ',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the event "Educational Activities Coordination Meeting" ran from 09:00-10:00 on 16 December 2024; therefore had a runtime of one hour. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – the agent tries to locate the calendar event
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
                # Milestone 1 – the user is informed about the meeting duration
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Accept any phrasing that clearly conveys the one-hour duration
                                    "content": [("one hour", "1 hour", "60 minutes")],
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
            name="EMILY_ROSE_20_e573ec90-667d-46d1-90d1-7fd60be738b5_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_20",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T11:00:00-08:00",
            is_read_time="2024-12-16T11:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to schedule another meeting with Linda Kim for the same time on Thursday "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Copy this morning's meeting, 'Educational Activities Coordination Meeting', to Thursday at the same time",
                },
            ],
            reasoning="The user wants to copy the morning's meeting 'Educational Activities Coordination Meeting', to Thursday at the same time. I will do this in Calendar and show the user.",
            success_conditions=[
                {
                    "input_text": '1. The calendar event "Educational Activities Coordination Meeting" is copied to December 19 at 9:00 am.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the existing calendar event
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
                # Milestone 1 – Confirm the correct meeting was retrieved from Milestone 0
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
                                                "value": "Educational Activities Coordination Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-16T09:00:00-08:00",
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
                # Milestone 2 – A new calendar event has been created for Thursday at the same time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Educational Activities Coordination Meeting",
                                    "start_datetime_iso": "2024-12-19T09:00:00-08:00",
                                    "end_datetime_iso": "2024-12-19T10:00:00-08:00",
                                    "attendees_names": [["Linda Kim", "Emily Rose"]],
                                    "creation_datetime_iso": "2024-12-16T11:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
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
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_20_669dbeb2-993b-4966-aa46-a895b63a1358_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_20",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T08:55:00-08:00",
            is_read_time="2024-12-16T08:55:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to summarise the education activities event. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Summarise this morning's event",
                },
            ],
            reasoning='The user has asked for a summary of an event, but has not provided much information about it. I will start by searching events within the time frame provided. I have searched the user\'s scheduled events for this morning, and the only one I see is an event called "Educational Activities Coordination Meeting". I can assume this is the intended event. I will summarise the information for the user. ',
            success_conditions=[
                {
                    "input_text": "1. Information for the Educational Activities Coordination Meeting event is summarised for the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent looks up calendar events (today / this morning)
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
                # Milestone 1 – Confirm the correct calendar event was included in the tool result
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
                                                "value": "Educational Activities Coordination Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-16T09:00:00-08:00",
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
                            reference_milestone_node_index=0,  # check output of Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – The agent’s response to the user contains a summary of the event
                Milestone(
                    snapshot_constraints=[
                        # Check the event name is in the reply
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Educational Activities Coordination Meeting",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Check Linda Kim (key attendee) is mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Linda Kim",
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
                (0, 1),  # event lookup -> verify event retrieved
                (1, 2),  # event retrieved -> user summary response
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_20_669dbeb2-993b-4966-aa46-a895b63a1358_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_20",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T08:55:00-08:00",
            is_read_time="2024-12-16T08:55:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to summarise the education activities event. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want you to summarise information for the calendar event called Educational Activities Coordination Meeting.",
                },
            ],
            reasoning="The user wants me to summarise the event called Educational Activities Coordination Meeting.\n\nI should locate the event by searching for it in the user's Calendar.\n\nI will then show the following event information to the user:\nEducational Activities Coordination Meeting\nDecember 16, 2024 - 09:00\nOrchard County Community Center",
            success_conditions=[
                {
                    "input_text": "1. Information for the Educational Activities Coordination Meeting event is summarised for the user.",
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
                # Milestone 1 – Confirm the desired event was returned by the lookup
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
                                                "value": "Educational Activities Coordination Meeting",
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
                # Milestone 2 – User receives a summary that includes key details
                Milestone(
                    snapshot_constraints=[
                        # Check the event name is in the response
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Educational Activities Coordination Meeting",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        ),
                        # Check the date (any reasonable phrasing) is in the response
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "December 16",
                                            "Dec 16",
                                            "Dec. 16",
                                            "16 December",
                                            "16 Dec",
                                            "12-16",
                                            "12/16",
                                            "the 16th",
                                            "today",
                                            "2024-12-16T09:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity,
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
            name="EMILY_ROSE_20_e573ec90-667d-46d1-90d1-7fd60be738b5_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_20",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T11:00:00-08:00",
            is_read_time="2024-12-16T11:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to schedule another meeting with Linda Kim for the same time on Thursday "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Copy this morning's meeting to Thursday at the same time",
                },
            ],
            reasoning="The user wants to copy this morning's meeting to Thursday at the same time. I'll look at the user's calendar to see if they had any meetings this morning. I found an event titled \"Educational Activities Coordination Meeting\" which took place this morning at 9:00 am. I can assume this is the event the user wants to copy. I will copy the meeting to 9:00 on December 19 and inform the user.",
            success_conditions=[
                {
                    "input_text": '1. The calendar event "Educational Activities Coordination Meeting" is copied to December 19 at 9:00 am.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent searches calendar to locate “this morning’s meeting”
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
                # Milestone 1 – Confirm the correct calendar event (Dec 16, 2024 09:00) was returned
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
                                                "value": "Educational Activities Coordination Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-16T09:00:00-08:00",
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
                # Milestone 2 – A new calendar event has been created for Thursday, Dec 19 2024 09:00
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Educational Activities Coordination Meeting",
                                    "start_datetime_iso": "2024-12-19T09:00:00-08:00",
                                    "end_datetime_iso": "2024-12-19T10:00:00-08:00",
                                    "attendees_names": [["Emily Rose", "Linda Kim"]],
                                    "creation_datetime_iso": "2024-12-16T11:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
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
            name="EMILY_ROSE_20_48ab1ac1-a24d-41ec-9d9a-780dd198a19d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_20",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T10:15:00-08:00",
            is_read_time="2024-12-16T10:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You feel like the event you were just at took forever and want to see how long it was. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How long was that last meeting? It seemed to drag on and on. ",
                },
            ],
            reasoning='OK so the user wants to know how long the last meeting ran for. First is establishing which event they\'re referring to. I will look at events that just happened with the keyword meeting to help refine the search. I have found the event "Educational Activities Coordination Meeting" which must be it. Next I will check the runtime of this event. I will now inform the user that the event "Educational Activities Coordination Meeting" ran from 09:00-10:00 on 16 December 2024; therefore had a runtime of one hour. \n',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the event "Educational Activities Coordination Meeting" ran from 09:00-10:00 on 16 December 2024; therefore had a runtime of one hour. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 — The agent looks up calendar events
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
                # Milestone 1 — The returned calendar data includes the correct meeting
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
                                                "value": "Educational Activities Coordination Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-16T09:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-16T10:00:00-08:00",
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
                # Milestone 2 — The agent’s reply to the user contains start time, end time, and duration
                Milestone(
                    snapshot_constraints=[
                        # Duration
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        ("one hour", "1 hour", "60 minute", "an hour")
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
                (0, 1),  # calendar lookup → verify meeting found
                (1, 2),  # meeting verified → user informed
            ],
        ),
    ]
