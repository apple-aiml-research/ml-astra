# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
# Auto-generated scenario extensions
import json
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
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_tool_trace_partial_arguments_similarity,
    column_word_contains_any_similarity,
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


def get_TAG_DAWEI_SHEN_pilot_plot_9(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="DAWEI_SHEN_9_3aa04b37-7566-4055-a6c0-c0ca39a53e71_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_9",
                "fix_add_missing_milestone_event_time_retrival",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T08:00:00-08:00",
            is_read_time="2024-12-10T08:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to see the address for the Tech Panel. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the address for the panel and tell me what time it starts.",
                },
            ],
            reasoning="The user wants to see the address and start time for the Tech Panel. I will search the calendar, locate the event named “Tech Panel Hosted by Jeff Bing,” which starts at 9:00 AM (2024-12-10T09:00:00-08:00) today. I will then tell the user the address (Tech Hub Conference Center) and confirm the 9:00 AM start time.",
            success_conditions=[
                {
                    "input_text": 'The assistant shows the user the address "Tech Hub Conference Center".',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "The assistant tells the user that the Tech Panel starts at 9:00 AM.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent looks up information about the event
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
                # Milestone 1 – The tool output contains the specific Tech Panel event
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
                                                "value": "Tech Panel Hosted by Jeff Bing",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-10T09:00:00-08:00",
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
                # Milestone 2 – The user is shown the Tech Panel address and inform user of the event's start time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Tech Hub Conference Center",
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
                                    "content": [
                                        ("9:00", "9 o'clock", "9 am", "9am", "9 a.m.")
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
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_9_0ebb0ed8-74e4-47a5-b714-2ecd6413b598_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_9",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T12:05:00-08:00",
            is_read_time="2024-12-06T12:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know how many events you have on in the morning next week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I'd like to know how many events I have in the morning next week",
                },
            ],
            reasoning='The user wants to know how many events they have on "in the morning next week".\n\nOkay, firstly, I\'ll check their calendar just to see how many events they have on next week.\n\nGreat, so the user only has two events next week, both starting in the morning. I would say they both begin "early in the morning", with the first event, "Tech Panel Hosted by Jeff Bing" starting at 09:00 on Tuesday, December 10th 2024, and the second event, "Team Review Meeting" starting at 10:00 on Friday, December 13th 2024. \n\nI will inform the user of this now.',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that they have two events that startin the morning next week: "Tech Panel Hosted by Jeff Bing", starting at 09:00 on Tuesday, December 10th 2024 and "Team Review Meeting", starting at 10:00 on Friday, December 13th 2024.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent looks up next week’s calendar events
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
                # Milestone 1 – The user is informed about the two early-morning events next week
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
                                                "value": "Tech Panel Hosted by Jeff Bing",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-10T09:00:00-08:00",
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
                # Milestone 2 – The agent looks up next week’s calendar events
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
                # Milestone 3 – The user is informed about the two early-morning events next week
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
                                                "value": "Team Review Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-13T10:00:00-08:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=2,
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
                # Milestone 4 – The user is informed about the two early-morning events next week
                Milestone(
                    snapshot_constraints=[
                        # Message states that there are two events (accepts either “two” or “2”)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("two", "2")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity,
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (2, 3), (1, 4), (3, 4)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_9_29b5ee11-2f46-41ec-8f9c-6285061a7d25_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_9",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T11:00:00-08:00",
            is_read_time="2024-12-08T11:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You are really excited for the tech panel that Jeff is hosting.       You want to know how many days are left until the panel. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How many days left until the Tech Panel hosted by Jeff Bing?",
                },
            ],
            reasoning="The user wants to know how many days remain until the event. I will look up their calendar, find the Tech Panel Hosted by Jeff Bing scheduled for 9:00 AM on December 10, 2024. Since today is December 8, 2024, the event is in two days. I will tell the user it is in 2 days.",
            success_conditions=[
                {
                    "input_text": "The assistant tells the user that the Tech Panel Hosted by Jeff Bing is in 2 days.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – agent looks up calendar events
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
                # Milestone 1 – The user is informed about the two early-morning events next week
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
                                                "value": "Tech Panel Hosted by Jeff Bing",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-10T09:00:00-08:00",
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
                # Milestone 2 – user is informed how many days remain (should be 2)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("2 days", "two days")],
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
                (0, 1),  # Look up event
                (1, 2),  # inform user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_9_29b5ee11-2f46-41ec-8f9c-6285061a7d25_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_9",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T11:00:00-08:00",
            is_read_time="2024-12-08T11:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You are really excited for the tech panel that Jeff is hosting.       You want to know how many days are left until the panel. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How many days until that electronics talk?",
                },
            ],
            reasoning="The user wants to know how many days are left until an event. First, determine which event they mean: the Tech Panel Hosted by Jeff Bing on December 10, 2024, which matches the description of an electronics talk. Today is December 8, 2024, so the event is in two days. Inform the user that the event is in 2 days.",
            success_conditions=[
                {
                    "input_text": "The assistant replies that the Tech Panel Hosted by Jeff Bing is in 2 days.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent queries the calendar to find the event
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
                # Milestone 1 – The returned calendar search results include Jeff’s Tech Panel
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
                                                "value": "Tech Panel Hosted by Jeff Bing",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-10T09:00:00-08:00",
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
                # Milestone 2 – The agent informs the user how many days remain (should be 2)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("2 days", "two days")],
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
            name="DAWEI_SHEN_9_0ebb0ed8-74e4-47a5-b714-2ecd6413b598_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_9",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T12:05:00-08:00",
            is_read_time="2024-12-06T12:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know how many events you have on early in the morning next week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I'd like to know if I have any early morning events next week please, how many",
                },
            ],
            reasoning='The user wants to know if they have any "early morning" events next week and the count.\n\nI will look at their calendar for next week. There are two events, both of which begin in the morning: "Tech Panel Hosted by Jeff Bing" at 09:00 on Tuesday, December 10 2024, and "Team Review Meeting" at 10:00 on Friday, December 13 2024. Because those are early-morning times, the correct yes/no reply is: "No, your early mornings are not free next week; you have two events …". I will answer with that information.',
            success_conditions=[
                {
                    "input_text": 'The assistant replies: "You have two events in the morning next week"',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Calendar information is retrieved with an appropriate tool
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
                # Milestone 1 – The user is informed about the two early-morning events next week
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
                                                "value": "Tech Panel Hosted by Jeff Bing",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-10T09:00:00-08:00",
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
                # Milestone 2 – Calendar information is retrieved with an appropriate tool
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
                # Milestone 3 – The user is informed about the two early-morning events next week
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
                                                "value": "Team Review Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-13T10:00:00-08:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=2,
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
                # Milestone 4 – The user is informed about the two early-morning events next week
                Milestone(
                    snapshot_constraints=[
                        # Message states that there are two events (accepts either “two” or “2”)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("two", "2")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity,
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (2, 3), (1, 4), (3, 4)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_9_19eeff08-0463-4b8a-a529-3939580f8982_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T08:00:00-08:00",
            is_read_time="2024-12-10T08:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to delete your event 'Tech Panel Hosted by Jeff Bing' as you feel too unwell to go. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my first event on today.",
                },
            ],
            reasoning="The user wants to delete their first event of the day. Looking at today’s calendar, the first event is “Tech Panel Hosted by Jeff Bing,” which starts at 09:00. I will delete this event and confirm the deletion to the user.",
            success_conditions=[
                {
                    "input_text": "The event 'Tech Panel Hosted by Jeff Bing' on December 10th starting at 09:00 is deleted.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up calendar events (to locate the one that must be deleted)
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
                                                "value": "Tech Panel Hosted by Jeff Bing",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-10T09:00:00-08:00",
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
                # Milestone 2 – The “Tech Panel Hosted by Jeff Bing” event is removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Tech Panel Hosted by Jeff Bing",
                                    "start_datetime_iso": "2024-12-10T09:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ],
                ),
                # Milestone 3 – The agent tells the user the event has been deleted
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Tech Panel",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,  # look for confirmation mentioning the event
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # After searching calendar,
                (1, 2),  # the event should be removed
                (2, 3),  # user should be informed
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_9_372d1b59-9ca9-4095-a434-5d418b1c9d5e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "email",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T10:12:00-08:00",
            is_read_time="2024-12-06T10:12:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        'You\'d like to send a reply to the email "Invitation: Tech Panel Discussion on December 10" and cc Theo.       Also add Theo Appleseed as an attendee to the corresponding calendar event. '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want you to reply to Jeff's email with: \"Hi Jeff, thank you so much for the invite, I'm really looking forward to it.\" CC Theo Appleseed on the reply, and go ahead and send him a shadow calendar invite too.",
                },
            ],
            reasoning='The user asked me to do two things. First, they want me to reply to the email titled "Invitation: Tech Panel Discussion on December 10"—I found that message in their inbox (received on Dec 6 2024 at 10:10). I will reply with the exact text: "Hi Jeff, thank you so much for the invite, I\'m really looking forward to it." and CC Theo Appleseed (theo.appleseed@orchardtech.com).\n\nSecond, they want me to send Theo a shadow calendar invite for the corresponding event. I searched their contacts and located Theo Appleseed’s email. Then I looked up the calendar event "Tech Panel Hosted by Jeff Bing" scheduled for Tuesday, 10 Dec 2024, 09:00–11:00. I will create another event with same details but add Theo Appleseed as the only invitee so he receives the shadow invite.',
            success_conditions=[
                {
                    "input_text": 'A reply to the email "Invitation: Tech Panel Discussion on December 10" received on December 6th 2024 at 10:10 is sent. The email reads: "Hi Jeff, thank you so much for the invite, I\'m really looking forward to it." and CCs Theo Appleseed (theo.appleseed@orchardtech.com).',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": 'A new calendar event with key word "Tech Panel" with Theo Appleseed as the only invitee created for Tuesday 10th December 2024 at 09:00-11:00, a shadow version of "Tech Panel Hosted by Jeff Bing".',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "send_email",
                "search_emails",
                "get_all_emails",
                "search_contacts",
                "get_all_contacts",
                "create_calendar_event",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # M0: search emails
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
                                        "search_emails",
                                        "get_all_emails",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # M1 the email found
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
                                            "subject": {
                                                "value": "Invitation: Tech Panel Discussion on December 10",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-06T10:10:00-08:00",
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
                # M2: search for Theo
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
                # Milestone 3 – Theo Appleseed’s contact information was actually returned
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
                            reference_milestone_node_index=2,  # parse the results of the search done in milestone 2
                        )
                    ],
                ),
                # Milestone 4 – reply action triggered
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "tool_trace": json.dumps(
                                        {
                                            "tool_name": "send_email",
                                            "arguments": {
                                                "email_action": "send",
                                                "email_id_referred": "place_holder",  # must send email with a thread id to reply an email
                                                "email_id_referred_action": "reply",
                                                "cc_recipients_addresses": [
                                                    "theo.appleseed@orchardtech.com"
                                                ],
                                            },
                                        },
                                        ensure_ascii=False,
                                    )
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": column_tool_trace_partial_arguments_similarity
                            },
                        ),
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
                # Milestone 5 – A reply email to Jeff Bing has been sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["jeff.bing@bingelectronics.com"]
                                    ],
                                    "cc_addresses": [
                                        ["theo.appleseed@orchardtech.com"]
                                    ],
                                    "status": "sent",
                                    "subject": "Re",
                                    "body": "looking forward",
                                    "creation_datetime_iso": "2024-12-06T10:12:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "status": column_exact_match_similarity,
                                "body": column_contains_similarity,  # contains the key phrase
                                "subject": column_contains_similarity,  # Reply the email,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        ),
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
                # Milestone 6 – The agent looks up calendar events (to locate the one that to be shadowed)
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
                # M7: found the calendar events
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
                                                "value": "Tech Panel Hosted by Jeff Bing",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-10T09:00:00-08:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=6,
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
                # Milestone 8 – Theo Appleseed has been sent a shadow invite
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Tech Panel",
                                    "attendees_names": [
                                        ["Dawei Shen", "Theo Appleseed"]
                                    ],
                                    "organizer_name": "Dawei Shen",
                                    "creation_datetime_iso": "2024-12-06T10:12:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
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
                (0, 1),  # Find the email
                (2, 3),  # Search for Theo
                (6, 7),  # Found the calendar events
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_9_3aa04b37-7566-4055-a6c0-c0ca39a53e71_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T08:00:00-08:00",
            is_read_time="2024-12-10T08:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to see the address for the Tech Panel. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the address for the panel.",
                },
            ],
            reasoning="The user wants to see the address for the “Tech Panel Hosted by Jeff Bing” on Dec 10, 2024 (09:00–11:00). I will look up the event in the calendar, retrieve its location (“Tech Hub Conference Center”), and reply to the user with that address.",
            success_conditions=[
                {
                    "input_text": "1. The address linked to the calendar event Tech Panel Hosted by Jeff Bing is presented.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # TODO: Add OR correlations to the Milestones, aka either path will work
                # Milestone 0 – A calendar (or email) lookup tool is invoked to retrieve information about the Tech Panel
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
                # Milestone 1 – The “Tech Panel Hosted by Jeff Bing” event (09:00-11:00, 10 Dec 2024) was retrieved
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
                                                "value": "Tech Panel Hosted by Jeff Bing",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-10T09:00:00-08:00",
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
                # # Milestone 2 – An email lookup tool is invoked to retrieve information about the Tech Panel
                # Milestone(
                #     snapshot_constraints=[
                #         SnapshotConstraint(
                #             database_namespace=DatabaseNamespace.SANDBOX,
                #             snapshot_constraint=snapshot_similarity,
                #             target_dataframe=pl.DataFrame(
                #                 {
                #                     "sender": RoleType.EXECUTION_ENVIRONMENT,
                #                     "recipient": RoleType.AGENT,
                #                     "tool_trace": "",
                #                 }
                #             ),
                #             column_similarity_measure={
                #                 "tool_trace": partial(
                #                     column_tool_trace_matches_tool_names,
                #                     target_tools=[
                #                         "search_emails",
                #                         "get_all_emails",
                #                     ],
                #                 )
                #             },
                #         )
                #     ],
                # ),
                # # Milestone 3: The email found
                # Milestone(
                #     snapshot_constraints=[
                #         SnapshotConstraint(
                #             database_namespace=DatabaseNamespace.SANDBOX,
                #             snapshot_constraint=partial(
                #                 tool_trace_dependant_similarity,
                #                 fill_to="content",
                #                 extractor=cast(
                #                     ToolTraceExtractorType,
                #                     partial(
                #                         result_list_match_existence_extractor,
                #                         match_conditions={
                #                             "subject": {
                #                                 "value": "Invitation: Tech Panel Discussion on December 10",
                #                                 "partial": False,
                #                             },
                #                             "creation_datetime_iso": {
                #                                 "value": "2024-12-06T10:10:00-08:00",
                #                                 "partial": False,
                #                             },
                #                         },
                #                     ),
                #                 ),
                #             ),
                #             reference_milestone_node_index=2,
                #             target_dataframe=pl.DataFrame(
                #                 {
                #                     "sender": RoleType.EXECUTION_ENVIRONMENT,
                #                     "recipient": RoleType.AGENT,
                #                     "content": "{matched}",
                #                 }
                #             ),
                #             column_similarity_measure={
                #                 "content": column_one_similarity
                #             },
                #         )
                #     ],
                # ),
                # Milestone 4 – The user receives the address / location of the Tech Panel
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Either phrase should appear in the reply
                                    "content": "Tech Hub Conference Center",
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
                (0, 1),  # check for calendars
                (1, 2),  # reply given calendar
                # (2, 3), # check for emails
                # (3, 4), # Reply given email
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_9_98e4f047-c9b5-4602-ad90-6deda8736685_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T14:30:00-08:00",
            is_read_time="2024-12-09T14:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to check the time of the tech panel you are attending tomorrow. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "when's that tech panel?",
                },
            ],
            reasoning="The user wants to know when the tech panel is. Checking the calendar, I find an event called 'Tech Panel Hosted by Jeff Bing' scheduled for tomorrow, 10 December 2024, from 09:00 to 11:00. I will inform the user of the event name, date, and time range.",
            success_conditions=[
                {
                    "input_text": "The user is informed that 'Tech Panel Hosted by Jeff Bing' is at 09:00-11:00 on 10 December 2024.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
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
                # Milestone 1 – The “Tech Panel Hosted by Jeff Bing” event (09:00-11:00, 10 Dec 2024) was retrieved
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
                                                "value": "Tech Panel Hosted by Jeff Bing",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-10T09:00:00-08:00",
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
                # Milestone 2 – The user is informed of the correct event name, date, and time range
                Milestone(
                    snapshot_constraints=[
                        # Start time mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        ("9:00", "9 o'clock", "9 am", "9am", "9 a.m.")
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
            name="DAWEI_SHEN_9_98e4f047-c9b5-4602-ad90-6deda8736685_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T14:30:00-08:00",
            is_read_time="2024-12-09T14:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to check the time of the tech panel you are attending tomorrow. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When's Jeff's tech panel?",
                },
            ],
            reasoning="The user wants to know When Jeff's tech panel is. What do they mean by Jeff's tech panel? When looking at the calendar I found an event called Tech Panel Hosted by Jeff Bing. this must be what they're referring to. The runtime for that is 09:00-11:00. I will inform the user now of this.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. the user is informed that 'Tech Panel Hosted by Jeff Bing' is at 09:00-11:00 on 10 December 2024. ",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent queried the calendar
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
                # Milestone 1 – The “Tech Panel Hosted by Jeff Bing” event (09:00-11:00, 10 Dec 2024) was retrieved
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
                                                "value": "Tech Panel Hosted by Jeff Bing",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-10T09:00:00-08:00",
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
                # Milestone 2 – User is informed of event name, date, and time
                Milestone(
                    snapshot_constraints=[
                        # Must mention the date 10 December 2024 (allow either order)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "December 10",
                                            "Dec 10",
                                            "10 December",
                                            "10th of December",
                                            "12/10",
                                            "12-10",
                                            "the 10th",
                                            "Tue",
                                            "Tuesday",
                                            "tomorrow",
                                            "2024-12-10T09:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                        # Must mention the time range 09:00-11:00 (allow 9:00)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        ("9:00", "9 o'clock", "9 am", "9am", "9 a.m.")
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
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_9_372d1b59-9ca9-4095-a434-5d418b1c9d5e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "email",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T10:12:00-08:00",
            is_read_time="2024-12-06T10:12:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        'You\'d like to send a reply to the email "Invitation: Tech Panel Discussion on December 10" and cc Theo.       Also add Theo Appleseed as an attendee to the corresponding calendar event. '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want you to reply to the email with: "Hi Jeff, thank you so much for the invite, I\'m really looking forward to it." Also send a shadow invite to Theo for the event, and CC him on the thread.',
                },
            ],
            reasoning='The user needs two actions completed:\n1) Send a reply to the email with subject "Invitation: Tech Panel Discussion on December 10" that arrived at 10:10 AM on 2024-12-06.  The reply body must be exactly: "Hi Jeff, thank you so much for the invite, I\'m really looking forward to it."  The reply must be sent in-thread to Jeff Bing and CC Theo Appleseed (theo.appleseed@orchardtech.com).\n2) Locate the related calendar event, "Tech Panel Hosted by Jeff Bing," scheduled for Tuesday 2024-12-10 from 09:00 to 11:00 (UTC-08:00), and create another calendar event with key word "Tech Panel" and Theo Appleseed as the only invitee so he receives a shadow invite.',
            success_conditions=[
                {
                    "input_text": 'A reply is sent to the email "Invitation: Tech Panel Discussion on December 10", addressed to Jeff Bing and CC\'ing Theo Appleseed, with the body: "Hi Jeff, thank you so much for the invite, I\'m really looking forward to it."',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": 'A new calendar event with key word "Tech Panel" with Theo Appleseed as the only invitee created for Tuesday 10th December 2024 at 09:00-11:00, a shadow version of "Tech Panel Hosted by Jeff Bing".',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "send_email",
                "search_emails",
                "get_all_emails",
                "search_contacts",
                "get_all_contacts",
                "create_calendar_event",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # M0: search emails
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
                                        "search_emails",
                                        "get_all_emails",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # M1 the email found
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
                                            "subject": {
                                                "value": "Invitation: Tech Panel Discussion on December 10",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-06T10:10:00-08:00",
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
                # M2: search for Theo
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
                # Milestone 3 – Theo Appleseed’s contact information was actually returned
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
                            reference_milestone_node_index=2,  # parse the results of the search done in milestone 2
                        )
                    ],
                ),
                # Milestone 4 – A reply email to Jeff Bing has been sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "tool_trace": json.dumps(
                                        {
                                            "tool_name": "send_email",
                                            "arguments": {
                                                "email_action": "send",
                                                "email_id_referred": "place_holder",  # must send email with a thread id to reply an email
                                                "email_id_referred_action": "reply",
                                                "cc_recipients_addresses": [
                                                    "theo.appleseed@orchardtech.com"
                                                ],
                                            },
                                        },
                                        ensure_ascii=False,
                                    )
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": column_tool_trace_partial_arguments_similarity
                            },
                        ),
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
                # Milestone 5 – A reply email to Jeff Bing has been sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["jeff.bing@bingelectronics.com"]
                                    ],
                                    "cc_addresses": [
                                        ["theo.appleseed@orchardtech.com"]
                                    ],
                                    "status": "sent",
                                    "subject": "Re",
                                    "body": "looking forward",
                                    "creation_datetime_iso": "2024-12-06T10:12:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "status": column_exact_match_similarity,
                                "body": column_contains_similarity,  # contains the key phrase
                                "subject": column_contains_similarity,  # Reply the email,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        ),
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
                # Milestone 6 – The agent looks up calendar events (to locate the one that to be shadowed)
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
                # M7: found the calendar events
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
                                                "value": "Tech Panel Hosted by Jeff Bing",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-10T09:00:00-08:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=6,
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
                # Milestone 8 – Theo Appleseed has been sent a shadow invite
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Tech Panel",
                                    "attendees_names": [
                                        ["Dawei Shen", "Theo Appleseed"]
                                    ],
                                    "organizer_name": "Dawei Shen",
                                    "creation_datetime_iso": "2024-12-06T10:12:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
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
                (0, 1),  # Find the email
                (2, 3),  # Search for Theo
                (6, 7),  # Found the calendar events
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_9_27590c4b-e5c6-4567-900d-8f5ceb51d383_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T11:00:00-08:00",
            is_read_time="2024-12-06T11:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know the location of the tech panel that Jeff Bing has invited you to "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where is the event Jeff invited me to taking place",
                },
            ],
            reasoning="So the user wants to know the location of an event Jeff has invited them to. I will search their emails for Jeff Bing’s invitation. The email titled “Invitation: Tech Panel Discussion on December 10” contains the details, including that the Tech Panel is being held at the Tech Hub Conference Center. I will respond to the user with that location.",
            success_conditions=[
                {
                    "input_text": "The assistant tells the user that the Tech Panel will take place at the Tech Hub Conference Center.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – An email lookup tool is invoked to retrieve information about the Tech Panel
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
                                        "search_emails",
                                        "get_all_emails",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1: The email found
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
                                            "subject": {
                                                "value": "Invitation: Tech Panel Discussion on December 10",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-06T10:10:00-08:00",
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
                # Milestone 2 – The user receives the address / location of the Tech Panel
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Either phrase should appear in the reply
                                    "content": "Tech Hub Conference Center",
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
                (0, 1),  # check for email
                (1, 2),  # reply given email
            ],
        ),
    ]
