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
    contains_presence_similarity,
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


def get_TAG_LUCAS_GARCIA_pilot_plot_13(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="LUCAS_GARCIA_13_1ca7255c-8b3f-496b-87eb-a07896b2aa58_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_13",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T12:40:00-08:00",
            is_read_time="2024-12-08T12:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know what your last message from Megan Johnson says. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What’s that last message?\n",
                },
            ],
            reasoning="The user wants to know what their last message was, so I will find the message, tell the user who it is from and then read it out. I can see the user just received a message from Megan Johnson and because this is the most recent message received on the user’s phone, I can assume this is the message the user referred to. \n",
            success_conditions=[
                {
                    "input_text": "1. The last message received from Megan Johnson is read out loud to the user. \n",
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
                # Milestone 0 – Agent uses a messages-retrieval tool
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
                # Milestone 1 – Confirm the retrieved message is the one from Megan Johnson
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
                                                "value": "megan.johnson@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Will do, Lucas.",
                                                "partial": True,  # allow substring match
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
                # Milestone 2 – Agent tells the user what the last message says
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Will do",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity  # check key phrase from the message
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # tool invocation → verify correct message retrieved
                (1, 2),  # message retrieved → user is informed
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_13_3b653b05-058a-444e-8530-1cb3e94567b5_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_13",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T08:10:00-08:00",
            is_read_time="2024-12-08T08:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know who is attending the online fitness class this week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who's attending my online fitness class today?",
                },
            ],
            reasoning="Right so, the user is looking for the list of attendees to their 'online fitness class'. From checking the user's calendar, I can see one event matching this name, 'Online Fitness Class with Megan and Participants'. It is scheduled for today, 8 December 2024 from 10:00 to 11:00. The attendees listed are 'Megan Johnson, Alex Martin, Olivia Clark and Jessica Lin'. Now that I have found the requested information I can read this out to the user.",
            success_conditions=[
                {
                    "input_text": "1. The attendees, 'Megan Johnson, Alex Martin, Olivia Clark and Jessica Lin', for 'Online Fitness Class with Megan and Participants' scheduled for 8 December 2024 from 10:00 to 11:00 are confirmed to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent looks up the calendar to find today’s online fitness class
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
                # Milestone 1 – Verify that the expected calendar event was retrieved from the tool call in Milestone 0
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
                                                "value": "Online Fitness Class with Megan and Participants",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-08T10:00:00-08:00",
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
                            reference_milestone_node_index=0,  # Depends on calendar tool invocation
                        )
                    ]
                ),
                # Milestone 2 – The agent informs the user of all attendees
                Milestone(
                    snapshot_constraints=[
                        # Check that Megan Johnson is mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Megan Johnson",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Check that Alex Martin is mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Alex Martin",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Check that Olivia Clark is mentioned
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
                        ),
                        # Check that Jessica Lin is mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Jessica Lin",
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
            name="LUCAS_GARCIA_13_97f0f3dd-33a8-4c0e-9459-16d8f38149cd_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_13",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T10:00:00-08:00",
            is_read_time="2024-12-09T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know what time your online fitness class was at yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time was my event on yesterday?",
                },
            ],
            reasoning="The user wants to know what time their event was at yesterday. Today is the 9 December 2024 so yesterday was 8 December 2024. I should check the user's Calendar for any events on this date. \nLooks like there was only one, the Online Fitness Class with Megan and Participants from 10:00-11:00, so this must be the event the user meant. \nI will let the user know it ran from 10:00-11:00. ",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their 'Online Fitness Class with Megan and Participants' ran on December 8th from 10:00-11:00.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent fetches calendar information (either listing all events or searching)
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
                # Milestone 1 – Confirm that the calendar tool’s output contained the correct event
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
                                                "value": "Online Fitness Class with Megan and Participants",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-08T10:00:00-08:00",
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
                # Milestone 2 – Agent informs the user of the event time window
                Milestone(
                    snapshot_constraints=[
                        # Check the start time (10 am / 10:00)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        ("10:00", "10 am", "10am", "10 a.m.", "10 am")
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
                (0, 1),  # Calendar retrieval → confirm event presence
                (1, 2),  # Event found → inform user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_13_97f0f3dd-33a8-4c0e-9459-16d8f38149cd_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_13",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T10:00:00-08:00",
            is_read_time="2024-12-09T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know what time your online fitness class was at yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time was my 'Online Fitness Class with Megan and Participants' yesterday?",
                },
            ],
            reasoning="The user wants to know what time their event 'Online Fitness Class with Megan and Participants' was on at yesterday.\nToday is the 9 December 2024 so yesterday was 8 December 2024.  I should check the user's Calendar for any events on this date. \nLooks like there was only one, the Online Fitness Class with Megan and Participants from 10:00-11:00, so this must be the event the user meant. \nI will let the user know it ran from 10:00-11:00. ",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their 'Online Fitness Class with Megan and Participants' ran on December 8th from 10:00-11:00.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent looks up the calendar to find yesterday’s class
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
                # Milestone 1 – The returned calendar results include the fitness class on Dec-08 at 10:00
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
                                                "value": "Online Fitness Class with Megan and Participants",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-08T10:00:00-08:00",
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
                # Milestone 2 – The agent tells the user the class was from 10:00-11:00
                Milestone(
                    snapshot_constraints=[
                        # Must mention the start time (10 a.m.)
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
                                            "10 AM",
                                            "10 am",
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
            name="LUCAS_GARCIA_13_3b653b05-058a-444e-8530-1cb3e94567b5_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_13",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T08:10:00-08:00",
            is_read_time="2024-12-08T08:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know who is attending the online fitness class this week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who's coming to my event at 10:00?",
                },
            ],
            reasoning="Okay so, the user is looking for the attendees to their event beginning at 10:00. From looking at the user's calendar, I can see one event which will begin at 10:00 today, 8 December 2024, titled 'Online Fitness Class with Megan and Participants'. The attendees listed are 'Megan Johnson, Alex Martin, Olivia Clark and Jessica Lin'. Now that I have found the requested information I can read this out to the user.",
            success_conditions=[
                {
                    "input_text": "1. The attendees, 'Megan Johnson, Alex Martin, Olivia Clark and Jessica Lin', for 'Online Fitness Class with Megan and Participants' scheduled for 8 December 2024 from 10:00 to 11:00 are confirmed to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent tries to look up the 10:00 event in the calendar
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
                # Milestone 1 – The returned calendar results include the correct fitness-class event at 10:00
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
                                                "value": "Online Fitness Class with Megan and Participants",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-08T10:00:00-08:00",
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
                # Milestone 2 – The agent tells the user who is attending (all four names must appear)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Megan Johnson",
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
                                    "content": "Alex Martin",
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
                                    "content": "Olivia Clark",
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
                                    "content": "Jessica Lin",
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
            name="LUCAS_GARCIA_13_1ca7255c-8b3f-496b-87eb-a07896b2aa58_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_13",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T12:40:00-08:00",
            is_read_time="2024-12-08T12:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know what your last message from Megan Johnson says. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you read Megan's last message please",
                },
            ],
            reasoning="OK so the user wants me to read the last message from someone called Megan. I will first go to contacts to see who Megan is. As there are no other Megans, I can assume that Megan is Megan Johnson. Hmmmm, I will now go to Messages. Hmmmm I see so individual messages from Megan. Maybe she is in a chat? I will confirm with the user. Ahh ok Megan is part of there online Fitness Class Feedback group. I will open it. Aha, I see a message from her received on the 8th of December 2024 at 12:40. I will read it for the user.",
            success_conditions=[
                {
                    "input_text": "1. The last message received from Megan Johnson is read out loud to the user. \n",
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
                # Milestone 0 – The agent looks up the user’s messages
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
                # Milestone 1 – The retrieved tool output contains the last message from Megan Johnson
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
                                                "value": "megan.johnson@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Thanks for all the energy and dedication you bring to each class",
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
                # Milestone 2 – The agent’s reply to the user contains (reads out) Megan’s last message content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Thanks for all the energy",
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
            name="LUCAS_GARCIA_13_cfbadf51-5d16-4721-a0fa-e85db6b627aa_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_13",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T12:50:00-08:00",
            is_read_time="2024-12-08T12:50:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to respond to the last text from Megan Johnson in the group chat called Online Fitness Class Feedback. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send Megasaurus a text in the group chat called Online Fitness Class Feedback saying: Yeah, sure, whatever. Chat soon. ",
                },
            ],
            reasoning="User Lucas Garcia wants to send a text to a person called Megasurus in the group chat Online Fitness Class Feedback. As the only other participant in the chat is Megan Johnson, I am confident the true identity of Megasaurus is clear. I shall draft the text reply to Megan Johnson in the designated chat and show it to user Lucas Garcia for approval. Then I will send it.",
            success_conditions=[
                {
                    "input_text": "1.A text is sent in reply to the last text from Megan Johnson in the group chat called Online Fitness Class Feedback saying, Yeah, sure, whatever. Chat soon. ",
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
                # Milestone 0 – Agent looks up the conversation in the message store
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
                # Milestone 1 – Verify that the conversation “Online Fitness Class Feedback” was found
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
                                                "value": "Online Fitness Class Feedback",
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
                # Milestone 2 – A new message is sent in the target conversation with the expected content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Online Fitness Class Feedback",
                                    "participants_addresses": [
                                        [
                                            (
                                                "lucas.garcia@example.com",
                                                "+1 12345-6789-1000-1234",
                                            ),  # Lucas Garcia
                                            (
                                                "megan.johnson@example.com",
                                                "+1 12345-6789-1000-3210",
                                            ),  # Megan Johnson
                                        ]
                                    ],
                                    "content": "Yeah, sure, whatever. Chat soon.",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-08T12:50:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Must find the conversation before confirming it exists
                (1, 2),  # Once confirmed, send the reply
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_13_c4e530c2-bafc-4d85-923a-38a373c59927_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_13",
                "email",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T22:00:00-08:00",
            is_read_time="2024-12-08T22:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to make sure you sent the email recapping the online fitness class to everyone "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'What email addresses did I send the email with the subject line "Recap And Video from December 8th Online Fitness Class" to today?',
                },
            ],
            reasoning='The user wants to know what email addresses they sent the email with the subject line "Recap And Video from December 8th Online Fitness Class" to today. The user only sent one email with that subject line. \n\nI\'ll inform the user that the email addresses included in the recipients are megan.johnson@example.com, olivia.clark@example.com, and alex.martin@example.com.',
            success_conditions=[
                {
                    "input_text": '1. The recipients of the email with the subject line "Recap And Video from December 8th Online Fitness Class" received on December 8 2024 at 11:30 are given',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – The agent looked through email data
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
                                    target_tools=["search_emails", "get_all_emails"],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – The email with the correct subject & timestamp was found
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
                                                "value": "Recap and Video from December 8th Online Fitness Class",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-08T11:30:00-08:00",
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
                # Milestone 2 – The user-facing reply includes every recipient address
                Milestone(
                    snapshot_constraints=[
                        # check for Megan
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "megan.johnson@example.com",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # check for Olivia
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "olivia.clark@example.com",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # check for Alex
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "alex.martin@example.com",
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
                (0, 1),  # email search → confirm correct email found
                (
                    1,
                    2,
                ),  # confirmation of email → user-facing reply contains all addresses
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_13_47da5b7c-9aa1-4d74-bd74-2eea37e288d4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_13",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
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
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You just hosted a great fitness class for some of your students.  You want to check when you started the class. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When did the online class start? Felt like it flew by!",
                },
            ],
            reasoning='Ok so the user wants to know when the online class started. First I will establish what event they are referring to. I will look for past events that have the keywords online class or similar terms. I have found the event "Online Fitness Class with Megan and Participants" this must be what the user is referring to. I will now check the start time of this event. I will now inform the user that the event "Online Fitness Class with Megan and Participants" started at 10:00 on 8 December 2024. \n',
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The user is informed that the event "Online Fitness Class with Megan and Participants" started at 10:00 on December 8th 2024. ',
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent looks up the calendar to find the online class
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
                # Milestone 1 – The expected event is found in the tool output of Milestone 0
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
                                                "value": "Online Fitness Class with Megan and Participants",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-08T10:00:00-08:00",
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
                        ),
                    ],
                ),
                # Milestone 2 – The agent’s reply to the user contains BOTH the correct date and time
                Milestone(
                    snapshot_constraints=[
                        # Check that the time is mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        ("10:00", "10 am", "10am", "10 a.m.", "10 am")
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
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_13_5f5e30c3-7fa8-42f2-8664-62f44f38fc2b_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_13",
                "messaging",
                "whatsapp_messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T12:15:00-08:00",
            is_read_time="2024-12-08T12:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You can't remember if you included the link in the message to Megan. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I send Megan the link to the practice recording?",
                },
            ],
            reasoning="The user wants to know if they sent Megan the link to the practice recording? I should first figure out who Megan is. \nFirst I will check the user's Contacts for a Megan. Looks like there is only one, Megan Johnson, so this must be who the user means. Next I will check for any messages to Megan. Hmm, I don't see any texts with Megan in Messages I should check WhatsApp. Hmm, I don't see any there either. \nIn Megan's contact card the alias is set as online class student. I saw a group chat in Messages called Online Fitness Class Feedback. I should check that for any messages to Megan. There is one sent at 12:10 on the 8 December 2024 that says 'Sure thing! Here's the link: https://www.youtube.com/watch?v=FITNESSSESSION123. Feel free to share it with your friends too. I'm eager to hear your feedback.'\nI will let the user know they have sent the link to Megan. ",
            success_conditions=[
                {
                    "input_text": "1. User is informed they sent the link to Megan Johnson.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks through existing messages to determine whether a link was sent
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – Agent informs the user that the link was indeed sent
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
                                            "you sent the link",
                                            "you already sent",
                                            "yes, you sent",
                                            "looks like you sent",
                                            "you did send",
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
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_13_5f5e30c3-7fa8-42f2-8664-62f44f38fc2b_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_13",
                "messaging",
                "whatsapp_messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T12:15:00-08:00",
            is_read_time="2024-12-08T12:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You can't remember if you included the link in the message to Megan. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I send my online class student a link to the recording of the practice?",
                },
            ],
            reasoning="The user wants to know if they sent their online class student a link to the recording of the practice. I should first figure out who that is. \nFirst I will check the user's Contacts for an online class student. Hmm, I don't see a contact with that name. However, Megan Johnson has her alias set as online class student so this must be who the user meant. \nNext I will check for any messages to Megan. Hmm, I don't see any texts with Megan in Messages I should check WhatsApp. Hmm, I don't see any there either but I saw a group chat in Messages called Online Fitness Class Feedback. I should check that for any messages to Megan. There is one sent at 12:10 on the 8 December 2024 that says 'Sure thing! Here's the link: https://www.youtube.com/watch?v=FITNESSSESSION123. Feel free to share it with your friends too. I'm eager to hear your feedback.'\nI will let the user know they have sent the link to Megan. ",
            success_conditions=[
                {
                    "input_text": "1. User is informed they sent the link to Megan Johnson.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks through past messages for the answer
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
                # Milestone 1 – Confirm the retrieved message actually contains the YouTube link
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
                                            # Message should contain the YouTube link
                                            "content": {
                                                "value": "https://www.youtube.com",
                                                "partial": True,
                                            },
                                            # And be part of the conversation with Megan
                                            "participants_addresses": {
                                                "value": "megan.johnson@example.com",
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
                # Milestone 2 – Agent informs the user that the link was already sent
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
                                            "you already sent",
                                            "you have sent",
                                            "yes, you sent",
                                            "you did send",
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
            milestone_edge_list=[
                (0, 1),  # Tool invocation → verify correct message found
                (1, 2),  # Evidence found → inform user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_13_47da5b7c-9aa1-4d74-bd74-2eea37e288d4_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_13",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
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
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You just hosted a great fitness class for some of your students.  You want to check when you started the class. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'When did "Online Fitness Class with Megan and Participants" start?',
                },
            ],
            reasoning='Ok so the user wants to know when "Online Fitness Class with Megan and Participants" started. First I will search for the given event in the calendar. now I have found the event next I will check the start time of the event. I will now inform the user that the event "Online Fitness Class with Megan and Participants" started at 10:00 on 8 December 2024. ',
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The user is informed that the event "Online Fitness Class with Megan and Participants" started at 10:00 on December 8th 2024. ',
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent consults the Calendar
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
                # Milestone 1 – The expected event is found in the tool output of Milestone 0
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
                                                "value": "Online Fitness Class with Megan and Participants",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-08T10:00:00-08:00",
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
                        ),
                    ],
                ),
                # Milestone 2 – Agent tells the user the correct start date & time
                Milestone(
                    snapshot_constraints=[
                        # Check date mention
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "December 8",
                                            "Dec 8",
                                            "8 December",
                                            "12-8",
                                            "12-08",
                                            "12/8",
                                            "12/08",
                                            "the 8th",
                                            "8th of December",
                                            "today",
                                            "this morning",
                                            "2024-12-08T10:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity,
                            },
                        ),
                        # Check time mention
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        ("10:00", "10 am", "10am", "10 a.m.", "10 AM")
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_13_c4e530c2-bafc-4d85-923a-38a373c59927_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_13",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T22:00:00-08:00",
            is_read_time="2024-12-08T22:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to make sure you sent the email recapping the online fitness class to everyone "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What email addresses did I send the email about the online fitness class to today?",
                },
            ],
            reasoning="The user wants to know what email addresses they sent the email about the online fitness class to today. I need to find the email the user was is referring to. I'll check their mail. \n\nI can see an email the user sent today with the subject line \"Recap And Video from December 8th Online Fitness Class\". This must be the email the user was referring to.\n\nThe user asked who they sent it to, which includes both the To and cc recipients. I'll inform the user that the recipients were megan.johnson@example.com, olivia.clark@example.com, and alex.martin@example.com (To), cc'd to jessica.lin@example.com and theo.appleseed@example.com.",
            success_conditions=[
                {
                    "input_text": '1. The recipients (including cc recipients) of the email with the subject line "Recap and Video from December 8th Online Fitness Class" received on December 8 2024 at 11:30 are given',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – The agent looks up emails to locate the fitness-class recap
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
                                    target_tools=["search_emails", "get_all_emails"],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – Confirm the email with the correct subject was returned
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
                                                "value": "Recap and Video from December 8th Online Fitness Class",
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
                # Milestone 2 – The agent’s reply to the user includes all three recipient addresses
                Milestone(
                    snapshot_constraints=[
                        # Check for Megan Johnson’s address
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "megan.johnson@example.com",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Check for Olivia Clark’s address
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "olivia.clark@example.com",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Check for Alex Martin’s address
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "alex.martin@example.com",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Check for Jessica Lin's cc address
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "jessica.lin@example.com",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Check for Theo Appleseed's cc address
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "theo.appleseed@example.com",
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
            name="LUCAS_GARCIA_13_cfbadf51-5d16-4721-a0fa-e85db6b627aa_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_13",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T12:50:00-08:00",
            is_read_time="2024-12-08T12:50:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to respond to the last text from Megan Johnson in the group chat called Online Fitness Class Feedback. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send Megan Johnson a text in the group chat called Online Fitness Class Feedback saying: Yeah, sure, whatever. Chat soon. ",
                },
            ],
            reasoning="User Lucas Garcia wants to send a text to a person called Megan Johnson. I have found this user in Contacts and have identified the group chat in Messages. I shall draft the text reply to Megan Johnson in the designated chat and show it to user Lucas Garcia for approval. Then I will send it.",
            success_conditions=[
                {
                    "input_text": "1.A text is sent in reply to the last text from Megan Johnson in the group chat called Online Fitness Class Feedback saying, Yeah, sure, whatever. Chat soon. ",
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
                # Milestone 0 – The agent looks for the correct conversation in the Messages database
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
                # Milestone 1 – Confirm that the conversation “Online Fitness Class Feedback” was returned
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
                                                "value": "Online Fitness Class Feedback",
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
                # Milestone 2 – A new outgoing message is added to the conversation with the correct text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Online Fitness Class Feedback",
                                    "participants_addresses": [
                                        [
                                            (
                                                "lucas.garcia@example.com",
                                                "+1 12345-6789-1000-1234",
                                            ),
                                            (
                                                "megan.johnson@example.com",
                                                "+1 12345-6789-1000-3210",
                                            ),
                                        ]
                                    ],
                                    "content": "Yeah, sure, whatever. Chat soon.",
                                    "creation_datetime_iso": "2024-12-08T12:50:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_13_1cf630f6-2b06-48c7-8fa9-81abd11eaf13_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_13",
                "contact",
                "calendar",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T12:00:00-08:00",
            is_read_time="2024-12-08T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You just hosted an online fitness class and it went really well.  You want to host another one next week, but you don't want your youtube subscriber to come because you just want it to be people you know well. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Copy my event named "Online Fitness Class with Megan and Participants" to next Sunday at 10:00-11:00, but exclude Alex. Then text them together "Hey everyone, I\'m excited for our next session!"',
                },
            ],
            reasoning='The user wants to copy the event "Online Fitness Class with Megan and Participants" to next Sunday 15 December 2024 from 10:00-11:00. So I\'ll copy the event and make sure only Jessica Lin, Olivia Clark, and Megan Johnson are invited. Now the user wants me to send a text to those invitees. So I\'ll text Jessica Lin, Olivia Clark, and Megan Johnson saying "Hey everyone, I\'m excited for our next session!"',
            success_conditions=[
                {
                    "input_text": '1. The event named "Online Fitness Class with Megan and Participants" is copied to 15 December 2024 at 10:00-11:00, with ONLY Jessica Lin, Olivia Clark, and Megan Johnson as invitees\n',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. A text message is sent to Jessica Lin, Olivia Clark, and Megan Johnson in a group message saying "Hey everyone, I\'m excited for our next session!"',
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
                "create_calendar_event",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the original calendar event
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
                # Milestone 1 – Confirm that the event “Online Fitness Class with Megan and Participants” was returned
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
                                                "value": "Online Fitness Class with Megan and Participants",
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
                # Milestone 2 – A new calendar event is created for next Sunday with only the requested invitees
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Online Fitness Class with Megan and Participants",
                                    "start_datetime_iso": "2024-12-15T10:00:00-08:00",
                                    "end_datetime_iso": "2024-12-15T11:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "Jessica Lin",
                                            "Olivia Clark",
                                            "Megan Johnson",
                                            "Lucas Garcia",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-08T12:00:00-08:00",
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
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
                # Milestone 3 – A text message is sent to the three invitees
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
                                                "+1 12345-6789-1000-3690",
                                                "jessica.lin@example.com",
                                            ),
                                            (
                                                "+1 12345-6789-1000-7531",
                                                "olivia.clark@example.com",
                                            ),
                                            (
                                                "+1 12345-6789-1000-3210",
                                                "megan.johnson@example.com",
                                            ),
                                        ]
                                    ],
                                    "content": "Hey everyone, I'm excited for our next session!",
                                    "creation_datetime_iso": "2024-12-08T12:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Event lookup ➜ new event creation
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_13_f49acbbb-e5ad-4f66-a289-3e557bc498f5_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_13",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T13:45:00-08:00",
            is_read_time="2024-12-08T13:45:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        'You want to dictate a reply message to Megan Johnson saying "Hey Megan just wondering if you managed to fill in the feedback form yet, let me know if you have any problems with it!". '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a message to the online student saying"Hey Megan just wondering if you managed to fill in the feedback form yet, let me know if you have any problems with it!".',
                },
            ],
            reasoning="The user wants to send a message to the online student. I check for a contact that that matches. I can't find an exact match but I found something close, a contact called Megan Johnson , whose alias is 'Online Class Student' . Taking context from the users requested message the name Megan appears so I must be correct here .\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": '1. A reply message is sent to Megan Johnson saying "Hey Megan just wondering if you managed to fill in the feedback form yet, let me know if you have any problems with it!".',
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
                # Milestone 0 – Agent looks up the contact information for Megan Johnson
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
                # Milestone 1 – Verify the contact returned from Milestone 0 includes Megan Johnson
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
                                                "value": "Megan Johnson",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "megan.johnson@example.com",
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
                # Milestone 2 – A new message is sent to Megan containing the feedback-form reminder
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
                                                "megan.johnson@example.com",
                                                "+1 12345-6789-1000-3210",
                                            ),
                                            (
                                                "lucas.garcia@example.com",
                                                "+1 12345-6789-1000-1234",
                                            ),
                                        ]
                                    ],
                                    "content": "feedback form",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-08T13:45:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
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
                (0, 1),  # Contact lookup → confirm Megan found
                (1, 2),  # Megan confirmed → message sent
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_13_1cf630f6-2b06-48c7-8fa9-81abd11eaf13_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_13",
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
            reference_time="2024-12-08T12:00:00-08:00",
            is_read_time="2024-12-08T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You just hosted an online fitness class and it went really well.  You want to host another one next week, but you don't want your youtube subscriber to come because you just want it to be people you know well. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Copy my event named "Online Fitness Class with Megan and Participants" to next Sunday at the same time, and invite everyone except my youtube follower. Then text the invitees together "Hey everyone, I\'m excited for our next session!"',
                },
            ],
            reasoning='The user wants to copy the event "Online Fitness Class with Megan and Participants." It happened at 10:00-11:00 today, and the user wants to copy it to next Sunday at the same time, so 15 December 2024 from 10:00-11:00. \n\nNow, the user mentioned that they wanted to invite all the same people except for one person. They don\'t want to invite their youtube follower. On the original calendar invite from today, the invitees were Megan Johnson, Alex Martin, Olivia Clark, and Jessica Lin. So I need to determine who among these people is a youtube follower of the user. Let me look in the user\'s contacts at their relationship with these four people. I see Alex Martin is listed with a relationship type of "youtube follower" so that must be who the user is talking about; they don\'t want Alex Martin to be invited to the new event.\n\nSo I\'ll copy the event "Online Fitness Class with Megan and Participants" so it\'s scheduled for next Sunday 15 December 2024 at 10:00-11:00 and make sure only Jessica Lin, Olivia Clark, and Megan Johnson are invited. Now the user wants me to send a text to those invitees. So I\'ll text Jessica Lin, Olivia Clark, and Megan Johnson saying "Hey everyone, I\'m excited for our next session!"',
            success_conditions=[
                {
                    "input_text": '1. The event named "Online Fitness Class with Megan and Participants" is copied to 15 December 2024 at 10:00-11:00, with ONLY Jessica Lin, Olivia Clark, and Megan Johnson as invitees\n',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. A text message is sent to Jessica Lin, Olivia Clark, and Megan Johnson via group message saying "Hey everyone, I\'m excited for our next session!"',
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
                "create_calendar_event",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent tries to locate the original event in the calendar
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
                # Milestone 1 – Verify the calendar search actually returned the correct event
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
                                                "value": "Online Fitness Class with Megan and Participants",
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
                # Milestone 2 – The new event for next Sunday is created with the correct attendees
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Online Fitness Class with Megan and Participants",
                                    "start_datetime_iso": "2024-12-15T10:00:00-08:00",
                                    "end_datetime_iso": "2024-12-15T11:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "Jessica Lin",
                                            "Megan Johnson",
                                            "Olivia Clark",
                                            "Lucas Garcia",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-08T12:00:00-08:00",
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
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
                # Milestone 3 – A text is sent that includes Jessica Lin
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [
                                            (
                                                "jessica.lin@example.com",
                                                "+1 12345-6789-1000-3690",
                                            ),
                                            (
                                                "olivia.clark@example.com",
                                                "+1 12345-6789-1000-7531",
                                            ),
                                            (
                                                "megan.johnson@example.com",
                                                "+1 12345-6789-1000-3210",
                                            ),
                                        ]
                                    ],
                                    "content": "excited for our next session",
                                    "creation_datetime_iso": "2024-12-08T12:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # search → verify retrieved event
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_13_1cf630f6-2b06-48c7-8fa9-81abd11eaf13_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_13",
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
            reference_time="2024-12-08T12:00:00-08:00",
            is_read_time="2024-12-08T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You just hosted an online fitness class and it went really well.  You want to host another one next week, but you don't want your youtube subscriber to come because you just want it to be people you know well. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Copy my exercise instructing session from earlier this morning to next Sunday at the same time, and invite everyone except my youtube follower. Then text the invitees together "Hey everyone, I\'m excited for our next session!"',
                },
            ],
            reasoning='The user wants to copy an event, and I need to figure out which one. They said it\'s the "exercise instructing session" and that it happened "earlier this morning". So I need to look for events on their calendar that already happened today, 8 December 2024, whose title is reminiscent of an exercise instructing session. There\'s only one on the calendar from earlier today, "Online Fitness Class with Megan and Participants." It doesn\'t have "exercise instructing session" in the name, but a fitness class is a synonym for an exercise instructing session, so this must be the event the user means. It happened at 10:00-11:00 today, and the user wants to copy it to next Sunday at the same time, so 15 December 2024 from 10:00-11:00. \n\nNow, the user mentioned that they wanted to invite all the same people except for one person. They don\'t want to invite their youtube follower. On the original calendar invite from today, the invitees were Megan Johnson, Alex Martin, Olivia Clark, and Jessica Lin. So I need to determine who among these people is a youtube follower of the user. Let me look in the user\'s contacts at their relationship with these four people. I see Alex Martin is listed with a relationship type of "youtube follower" so that must be who the user is talking about; they don\'t want Alex Martin to be invited to the new event.\n\nSo I\'ll copy the event "Online Fitness Class with Megan and Participants" so it\'s scheduled for next Sunday 15 December 2024 at 10:00-11:00 and make sure only Jessica Lin, Olivia Clark, and Megan Johnson are invited. Now the user wants me to send a text to those invitees. So I\'ll text Jessica Lin, Olivia Clark, and Megan Johnson saying "Hey everyone, I\'m excited for our next session!"',
            success_conditions=[
                {
                    "input_text": '1. The event named "Online Fitness Class with Megan and Participants" is copied to 15 December 2024 at 10:00-11:00, with ONLY Jessica Lin, Olivia Clark, and Megan Johnson as invitees\n',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. A text message is sent to Jessica Lin, Olivia Clark, and Megan Johnson saying "Hey everyone, I\'m excited for our next session!" via group chat',
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
                "create_calendar_event",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent tries to locate the original event in the calendar
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
                # Milestone 1 – Verify the calendar search actually returned the correct event
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
                                                "value": "Online Fitness Class with Megan and Participants",
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
                # Milestone 2 – The new event for next Sunday is created with the correct attendees
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Online Fitness Class with Megan and Participants",
                                    "start_datetime_iso": "2024-12-15T10:00:00-08:00",
                                    "end_datetime_iso": "2024-12-15T11:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "Jessica Lin",
                                            "Megan Johnson",
                                            "Olivia Clark",
                                            "Lucas Garcia",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-08T12:00:00-08:00",
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
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
                # Milestone 3 – A text is sent that includes Jessica Lin
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [
                                            (
                                                "jessica.lin@example.com",
                                                "+1 12345-6789-1000-3690",
                                            ),
                                            (
                                                "olivia.clark@example.com",
                                                "+1 12345-6789-1000-7531",
                                            ),
                                            (
                                                "megan.johnson@example.com",
                                                "+1 12345-6789-1000-3210",
                                            ),
                                        ]
                                    ],
                                    "content": "excited for our next session",
                                    "creation_datetime_iso": "2024-12-08T12:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # search → verify retrieved event
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_13_f49acbbb-e5ad-4f66-a289-3e557bc498f5_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_13",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T13:45:00-08:00",
            is_read_time="2024-12-08T13:45:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        'You want to dictate a reply message to Megan Johnson saying "Hey Megan just wondering if you managed to fill in the feedback form yet, let me know if you have any problems with it!". '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a reply message to Megan Johnson saying "Hey Megan just wondering if you managed to fill in the feedback form yet, let me know if you have any problems with it!".',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Megan Johnson.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": '1. A reply message is sent to Megan Johnson saying "Hey Megan just wondering if you managed to fill in the feedback form yet, let me know if you have any problems with it!".',
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
                # Milestone 0 – Agent looks up the existing conversation or contact information
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
                    ],
                ),
                # Milestone 1 – A new outgoing message to Megan Johnson is added with the correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require both Megan and Lucas to appear (by email or phone)
                                    "participants_addresses": [
                                        [
                                            (
                                                "megan.johnson@example.com",
                                                "+1 12345-6789-1000-3210",
                                            ),
                                            (
                                                "lucas.garcia@example.com",
                                                "+1 12345-6789-1000-1234",
                                            ),
                                        ]
                                    ],
                                    # Key phrase from dictated message
                                    "content": "managed to fill in the feedback form yet",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-08T13:45:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
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
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_13_c755fc44-8021-4486-bef7-fc17036e1d32_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_13",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T12:50:00-08:00",
            is_read_time="2024-12-08T12:50:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are wondering what time you sent in your last email to Megan, Olivia and Alex "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I send that last email regarding to the Online Class Recap?",
                },
            ],
            reasoning='The user wants to know when they sent their last email regarding to regarding to the Online Class Recap. First thing I need to do is search the user\'s emails. Ok I found an email sent to megan.johnson@example.com,\nolivia.clark@example.com and alex.martin@example.com with title "Recap and Video from December 8th Online Fitness Class". That must be the email the user is referring to. Ok now that I have that I will retrieve the time of the email and inform the user',
            success_conditions=[
                {
                    "input_text": '1. The time of the email sent by the user on December 08, 2024 at 11:30 with title "Recap and Video from December 8th Online Fitness Class" is presented to the user',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – Agent looks through the email database
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
                                    target_tools=["search_emails", "get_all_emails"],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – The expected recap email (with correct time) is present in the retrieved results
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
                                                "value": "Recap and Video from December 8th Online Fitness Class",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-08T11:30:00-08:00",
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
                # Milestone 2 – Agent tells the user the correct time (11:30)
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
                                            "11:30",
                                            "11:30am",
                                            "11:30 am",
                                            "11:30 AM",
                                            "11:30a.m.",
                                            "11:30 a.m.",
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
                (0, 1),  # email search → confirm correct email found
                (1, 2),  # correct email found → agent informs user
            ],
        ),
    ]
