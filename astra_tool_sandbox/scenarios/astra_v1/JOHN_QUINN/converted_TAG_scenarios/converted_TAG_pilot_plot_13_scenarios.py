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
    column_list_tuple_contains_similarity,
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_any_similarity,
    column_word_contains_similarity,
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


def get_TAG_JOHN_QUINN_pilot_plot_13(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="JOHN_QUINN_13_dd4eb766-ff48-4ebd-9a8c-c5afa23e5295_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_13",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T11:15:00-07:00",
            is_read_time="2024-07-24T11:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to reply Robin's message and tell her that it's ok and suggest that she can meet up with them after if she likes "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": " Reply to Robin Selmoure's last message and say That's ok maybe you can meet up with us after the hike if you like",
                },
            ],
            reasoning="The user wants to reply to Robin Selmoure's last message. First I need to look through their conversations to find one with Robin Selmoure. Now that I have found that I will reply to the most recent message. I will now draft the message with the given text and ask the user if it is ready to be sent",
            success_conditions=[
                {
                    "input_text": '1. A message that says "That\'s ok maybe you can meet up with us after the hike if you like" is sent to Robin Selmoure',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up the recent conversation with Robin
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
                # Milestone 1 – New outgoing message to Robin containing the requested text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Include at least Robin in the participants list
                                    "participants_addresses": [
                                        [
                                            (
                                                "408-555-0132",
                                                "robin.selmoure@palantir.com",
                                            )
                                        ]
                                    ],
                                    "content": "maybe you can meet up with us after the hike",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-24T11:15:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare to initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_13_8a417111-a51f-459f-8966-7b01df4cc578_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_13",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-02T22:00:00-07:00",
            is_read_time="2024-08-02T22:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to double-check the duration of your upcoming group hike tomorrow, as you're wondering how many snacks you should bring. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can I get the event duration of tomorrow's hike?",
                },
            ],
            reasoning="The user wants to know the event duration of tomorrow's hike. I wonder what event they're talking about. I should check the user's calendar to figure it out. I see that user has one event called 'Group Hike at Batteries to Bluffs Trail', tomorrow, Saturday, August 3rd 2024 at 8:00-14:00. This must be the event. Okay, I'll give them the details of that event now, including the duration of 6 hours. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The duration of the event, 'Group Hike at Batteries to Bluffs Trail', on Saturday, August 3rd at 8:00-14:00 is shown to the user. ",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 — Agent looks up tomorrow’s hike event in the calendar
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
                # Milestone 1 — Agent tells the user the duration (≈6 hours) of the hike
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
                                            "6 hours",
                                            "six hours",
                                            "6hrs",
                                            "6 hrs",
                                            "6-hour",
                                            "six-hour",
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
            name="JOHN_QUINN_13_0e7a4f75-4bda-43d6-a8f1-92d3ef5df946_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_13",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T10:55:00-07:00",
            is_read_time="2024-07-24T10:55:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to make sure you have next weekend after the coming ones free before you invite your friends on a hike. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you tell me if I have any plans for the next weekend? Not the immediate one. Reply with the exact dates and Yes or No.",
                },
            ],
            reasoning="The user is trying to figure out their availability for next weekend not the immediate one, which is August 3rd and 4th. I have all the referenced details I need to carry out my task. First, I will search their calendar. I can see that they have no plans for the Saturday and Sunday, so I will relay this back to them. ",
            success_conditions=[
                {
                    "input_text": "1. Calendar is searched for any events that may be taking place on Saturday 3 August and Sunday 4 August. ",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. User is informed with 'No', as there're currently no plans for that weekend with exact dates August 3rd and 4th.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
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
                    ]
                ),
                # Milestone 1 – The agent tells the user about August 3rd-4th
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("August", "Aug", "08")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        )
                    ]
                ),
                # Milestone 2 – The agent tells the user they do not have any plans
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "No",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_similarity
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
            name="JOHN_QUINN_13_3d33237b-d3ca-4f66-aa8f-5a7af5f992ae_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_13",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T11:15:00-07:00",
            is_read_time="2024-07-24T11:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to reply to the Hiking Group to confirm receipt of everyones messages. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply in Hiking Group and say excellent, see you all then",
                },
            ],
            reasoning='The user wants to reply to their Hiking Group chat with the text "excellent, see you all then". First I\'ll find the group chat by looking through messages for a chat with this name, and with this I can compose the reply and confirm that the user is happy to send it.',
            success_conditions=[
                {
                    "input_text": '1. A reply is sent to the Hiking Group message group saying "excellent, see you all then”',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up existing message threads
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
                # Milestone 1 – The Hiking Group conversation is returned in the tool output
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
                                                "value": "Hiking Group",
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
                        ),
                    ],
                ),
                # Milestone 2 – A reply is sent in the Hiking Group thread
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Hiking Group",
                                    "content": "see you all",  # we will use substring matching below
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-24T11:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,  # checks substring, case-insensitive
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial state
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
            name="JOHN_QUINN_13_8a417111-a51f-459f-8966-7b01df4cc578_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_13",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-02T22:00:00-07:00",
            is_read_time="2024-08-02T22:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to double-check the duration of your upcoming group hike tomorrow, as you're wondering how many snacks you should bring. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can I get the event duration of Group Hike at Batteries to Bluffs Trail?",
                },
            ],
            reasoning="The user wants to know the event duration of 'Group Hike at Batteries to Bluffs Trail'. I'll search the user's calendar for that event now. I see that user has one event called 'Group Hike at Batteries to Bluffs Trail', tomorrow, Saturday, August 3rd 2024 at 8:00-14:00. This must be the event. Okay, I'll give them the details of that event now, including the duration of 6 hours. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The duration of the event, 'Group Hike at Batteries to Bluffs Trail', on Saturday, August 3rd at 8:00-14:00 is shown to the user. ",
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
                # Milestone 1 – Confirm the expected hike event was returned from the calendar lookup
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
                                                "value": "Group Hike at Batteries to Bluffs Trail",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-08-03T08:00:00-07:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-08-03T14:00:00-07:00",
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
                # Milestone 2 – The user-facing reply includes the duration information
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("6 hours", "six hours", "6 hrs")],
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
                (0, 1),  # Calendar lookup → confirm hike event details
                (1, 2),  # Event confirmed → user is told the duration
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_13_dd4eb766-ff48-4ebd-9a8c-c5afa23e5295_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_13",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T11:15:00-07:00",
            is_read_time="2024-07-24T11:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to reply Robin's message and tell her that it's ok and suggest that she can meet up with them after if she likes "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": " Reply to Robin's last message and say That's ok maybe you can meet up with us after the hike if you like",
                },
            ],
            reasoning='The user wants to reply to Robin\'s last message. First I need to look through their conversations to find a Robin. There are two conversations with Robin however since the user mentioned the "last", meaning most recent message I will choose the most recent conversation and reply to that message. I will now draft the message with the given text and ask the user if it is ready to be sent',
            success_conditions=[
                {
                    "input_text": '1. A message that says "That\'s ok maybe you can meet up with us after the hike if you like" is sent to Robin Selmoure',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up Robin’s previous message / conversation
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
                # Milestone 1 – A new outgoing message to Robin with the requested content is created
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
                                                "john.quinn@palantir.com",
                                                "1234-5678-9108",
                                            ),  # John Quinn
                                            (
                                                "robin.selmoure@palantir.com",
                                                "408-555-0132",
                                            ),  # Robin Selmoure
                                        ]
                                    ],
                                    "content": "maybe you can meet up with us after the hike",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-24T11:15:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieval precedes sending the reply
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_13_482afd1a-e9ed-4492-afb2-f597eebd8d11_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_13",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T17:00:00-07:00",
            is_read_time="2024-07-24T17:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know what time your hike is on August 3rd. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is my group hike at?",
                },
            ],
            reasoning="The user wants to know what time their group hike is at. Let me look for group hikes in their calendar and messages. I think they are referring to this event named 'Group Hike at Batteries to Bluffs Trail'.\n\nOk I have found it. I will inform the user that their event 'Group Hike at Batteries to Bluffs Trail' at Batteries to Bluffs Trail, San Francisco, CA will take place from 08:00 - 14:00 on August 3rd.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their event 'Group Hike at Batteries to Bluffs Trail' at Batteries to Bluffs Trail, San Francisco, CA will take place from 08:00 - 14:00 on August 3rd.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
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
                        ),
                    ],
                ),
                # Milestone 1 – Calendar event for the hike is present in the tool results
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
                                                "value": "Group Hike at Batteries to Bluffs Trail",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-08-03T08:00:00-07:00",
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
                # Milestone 2 – User is informed of the correct date and time
                Milestone(
                    snapshot_constraints=[
                        # Check the time reference
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        ("8:00", "08:00", "8 am", "8am", "8 a.m.")
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        # Check the date reference
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "August 3",
                                            "08/03",
                                            "Aug. 3",
                                            "Aug 3",
                                            "the 3rd",
                                            "Saturday",
                                            "3 August",
                                            "2024-08-03",
                                            "2024-08-03T08:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar lookup → Verify hike event returned
                (1, 2),  # Event found → Inform the user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_13_0097246c-3ecf-4c2a-837c-800c4f556003_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_13",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T11:15:00-07:00",
            is_read_time="2024-07-24T11:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to try and convince Robin to come to the hike. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a message to Robin saying "Hey, don\'t make up excuses. Come on! Join us!"',
                },
            ],
            reasoning="The user wants to send a message to a contact called Robin Selmoure. I find the contact details in the user's contacts. I set it as the recipient of the message.\nI draft the message \"Hey, don't make up excuses. Come on! Join us!\" as per the users request. I await confirmation and send the message after receiving it.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A message is sent to Robin Selmoure saying "Hey, don\'t make up excuses. Come on! Join us!"',
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
                # Milestone 0 – Agent looks up Robin’s contact information
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
                # Milestone 1 – Robin Selmoure is confirmed in the contact-search results
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
                                            "phone_number": {
                                                "value": "408-555-0132",
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
                # Milestone 2 – Message to Robin has been sent
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
                                                "robin.selmoure@palantir.com",
                                                "408-555-0132",
                                            )
                                        ]
                                    ],
                                    "content": "Hey, don't make up excuses. Come on! Join us!",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-24T11:15:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare to initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → verify Robin found
                (1, 2),  # Robin verified → message sent
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_13_cb0c841b-00b4-43c2-b087-0b1965bdd2ba_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_13",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T11:30:00-07:00",
            is_read_time="2024-07-24T11:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to change the time of the hike to 9 am for the next trip with the hiking group. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to move the hike Batteries to Bluffs trail with group Theo, Cookie, and Akira next Saturday to 9 am. Messaged the group and see if that is acceptable with everyone.",
                },
            ],
            reasoning="The user would like to move the hike to Batteries to Bluffs trail  moved from 8am to 9am and needs to confirm with the rest of the Hiking group they are acceptable to this change. \n\nI will message the hiking group and to see with they will accept the planned hike on the Saturday be moved up one hour from 8 to 9 am.",
            success_conditions=[
                {
                    "input_text": "1. Message is sent to hiking group friends Cookie Watson, Akira Muramoto and Theo Appleseed to move the next hike to 9:00 am from 8:00 am. ",
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
                "search_messages",
                "get_all_messages",
                "send_message",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the existing hiking-group conversation
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
                # Milestone 1 – Confirm that the Hiking Group thread was actually returned from the search
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
                                                "value": "Hiking Group",
                                                "partial": False,
                                            }
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,  # parse output of the search in Milestone 0
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
                # Milestone 2 – A new message is sent to Theo, Cookie, and Akira proposing 9 AM
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require that each participant (and John himself) is present in any valid identifier form.
                                    "participants_addresses": [
                                        [
                                            (
                                                "john.quinn@palantir.com",
                                                "1234-5678-9108",
                                            ),
                                            (
                                                "theo.appleseed@example.com",
                                                "1234-5678-9101",
                                            ),
                                            (
                                                "cookie.watson@mckinley.com",
                                                "1234-5678-9107",
                                            ),
                                            (
                                                "akira.muramoto@sportsfan.com",
                                                "408-555-0135",
                                            ),
                                        ]
                                    ],
                                    # Content must mention “9 am/9am/9 a.m./9” (any phrasing).
                                    "content": [
                                        (
                                            "9 am",
                                            "9am",
                                            "9 a.m.",
                                            "09:00",
                                            "9:00 am",
                                        )
                                    ],
                                    "creation_datetime_iso": "2024-07-24T11:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_str_contains_any_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                    # Ignore unrelated database changes while evaluating this addition
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_13_d67ef9b3-9997-433a-a5a5-cb34210aad40_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_13",
                "contact",
                "messaging",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-03T07:00:00-07:00",
            is_read_time="2024-08-03T07:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to send a group message to your trekking friends saying 'Don't forget to bring tons of water and light clothes, it is going to be very warm today!' an hour before your group hike starts. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Write a message to my trekking friends saying "Don\'t forget to bring tons of water and light clothes, it is going to be very warm today!" and send it.',
                },
            ],
            reasoning="The user wants to send a message to their trekking friends. I am not sure what the user means by this. However, the request is made on Saturday August 3 at 7:00, one hour before a 'Group Hike' event on the same day. I can therefore make the connection between trekking friends and group hike. Going through the user apps, I see there is a message group called 'Hiking Group', so it seems reasonable to send the message using this group message chat. Now that I have identified the recipient of the message, I will write the message saying \"Don't forget to bring tons of water and light clothes, it is going to be very warm today!\" and send it to the group chat. I can also assume the pronoun \"it\" is referring to the message the user wants to send. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A message saying 'Don't forget to bring tons of water and light clothes, it is going to be very warm today!' is sent to the Hiking Group an hour before the group hike starts. ",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "search_messages",
                "get_all_messages",
                "send_message",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looks up existing message threads to locate the hiking group chat
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
                # Milestone 1 – Confirm that the Hiking Group thread was actually returned from the search
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
                                                "value": "Hiking Group",
                                                "partial": False,
                                            }
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,  # parse output of the search in Milestone 0
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
                # Milestone 2 – A new message is sent to the Hiking Group with the reminder text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Hiking Group",
                                    "content": "Don't forget to bring tons of water and light clothes, it is going to be very warm today!",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-08-03T07:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial state
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
            name="JOHN_QUINN_13_7e3921a1-14f1-49b1-9453-264a45de9fe9_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_13",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T11:15:00-07:00",
            is_read_time="2024-07-24T11:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to reply Robin's message and tell her that it's ok and suggest that she can meet up with them after if she likes "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to Robin's last message and say That's ok maybe you can meet up with us after the hike if you like",
                },
            ],
            reasoning='The user wants to reply to Robin\'s last message. First I need to look through their conversations to find a Robin. There are two conversations with Robin however since the user mentioned the "last", meaning most recent message I will choose the most recent conversation and reply to that message. I will now draft the message with the given text and ask the user if it is ready to be sent',
            success_conditions=[
                {
                    "input_text": '1. A message that says "That\'s ok maybe you can meet up with us after the hike if you like" is sent to Robin Selmoure',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up the existing conversation / messages
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
                # Milestone 1 – A new outgoing message to Robin is created with the right content
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
                                                "john.quinn@palantir.com",
                                                "1234-5678-9108",
                                            ),
                                            (
                                                "robin.selmoure@palantir.com",
                                                "408-555-0132",
                                            ),
                                        ]
                                    ],
                                    "content": "maybe you can meet up with us after the hike",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-24T11:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # make sure both John and Robin are the only participants, no extras
                                "participants_addresses": column_list_tuple_contains_similarity,
                                # Verify the essence of the reply text is present
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against the initial state
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieval of conversation precedes sending the reply
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_13_0097246c-3ecf-4c2a-837c-800c4f556003_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_13",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T11:15:00-07:00",
            is_read_time="2024-07-24T11:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to try and convince Robin to come to the hike. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to my friend who won't come hiking with us saying \"Hey, don't make up excuses. Come on! Join us!\"",
                },
            ],
            reasoning="The user wants to send a message to a friend who won't go on the hike. I search the users recent messages for the correct contact.I found one called Robin Selmoure who just refused the hiking invitation. I set it as the recipient of the message.\nI draft the message \"Hey, don't make up excuses. Come on! Join us!\" as per the users request. I await confirmation and send the message after receiving it.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A message is sent to Robin Selmoure saying "Hey, don\'t make up excuses. Come on! Join us!"',
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
                # Milestone 0 – The agent looks up Robin’s contact information
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
                # Milestone 1
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
                                                "value": "Robin Selmoure",
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
                # Milestone 2 – A new message to Robin containing the requested text was sent
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
                                                "robin.selmoure@palantir.com",
                                                "408-555-0132",
                                            )
                                        ]
                                    ],
                                    "content": "Hey, don't make up excuses. Come on! Join us!",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-24T11:15:00-07:00",
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
            milestone_edge_list=[
                (0, 1),  # message search → verify who refused the invitation
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_13_482afd1a-e9ed-4492-afb2-f597eebd8d11_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_13",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T17:00:00-07:00",
            is_read_time="2024-07-24T17:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know what time your hike is on August 3rd. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is my Group Hike on August 3rd at?",
                },
            ],
            reasoning="The user wants to know what time their event Group Hike on August 3rd is at. Let me look for it in Calendar. Ok I have found it. I will inform the user that their event 'Group Hike at Batteries to Bluffs Trail' at Batteries to Bluffs Trail, San Francisco, CA will take place from 08:00 - 14:00 on August 3rd.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their event 'Group Hike at Batteries to Bluffs Trail' at Batteries to Bluffs Trail, San Francisco, CA will take place from 08:00 - 14:00 on August 3rd.",
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
                        ),
                    ],
                ),
                # Milestone 1 – The returned tool output contains the Group Hike event on Aug-03 starting 08:00
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
                                            # Flexible name match
                                            "calendar_event_name": {
                                                "value": "Group Hike",
                                                "partial": True,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-08-03T08:00:00-07:00",
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
                # Milestone 2 – The agent’s reply to the user includes the correct date and time window
                Milestone(
                    snapshot_constraints=[
                        # Start time (08:00 / 8 am)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "08:00",
                                            "8:00",
                                            "8 am",
                                            "8am",
                                            "8 a.m.",
                                            "08:00 AM",
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
            name="JOHN_QUINN_13_a8f575e3-a2a0-4c3f-b4b5-942c0f636149_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_13",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T11:15:00-07:00",
            is_read_time="2024-07-24T11:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to dictate a reply to Theo Appleseed saying that you will be a little late to the group hike because you need to walk the dog. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a message reply to Theo Appleseed saying "Hi Theo I will be a little late to the group hike because I need to walk the dog sorry about that."',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Theo Appleseed.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": '1. A reply message is sent to Theo Appleseed that includes "I will be a little late to the group hike because I need to walk the dog."',
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
                # Milestone 0 – The agent looks up the conversation or messages with Theo
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
                # Milestone 1 – Verify that the returned search result (from Milestone 0) contains the thread with Theo
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
                                                "value": "Theo Appleseed",
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
                # Milestone 2 – A new outgoing message is sent to Theo with the correct content
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
                                                "theo.appleseed@example.com",
                                                "1234-5678-9101",
                                            ),
                                        ]
                                    ],
                                    "content": "walk the dog",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-24T11:15:00-07:00",
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
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_13_3525d1f6-a914-4116-9ea3-ef9c062e0381_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_13",
                "contact",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-02T16:40:00-07:00",
            is_read_time="2024-08-02T16:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You have broken your ankle and need to cancel your hike. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my event with Cookie, Theo and Akira.",
                },
            ],
            reasoning="The user wants to delete their event with Cookie, Theo and Akira. First I should figure out who they are. I will check the user's Contacts for these names. \n\nI have found only one Contact that matches these names, Theo Appleseed, Cookie Watson and Akira Muramoto so these must be the people the user meant. \n\nNext I will check the user's Calendar for an event with all these people as invitees. Hmm, looks like there is only one, on 3 August 2024, from 8:00-14:00 called Group Hike at Batteries to Bluffs Trail. \n\nNow I will delete this event and let the user know it has been deleted. ",
            success_conditions=[
                {
                    "input_text": "1. Group Hike at Batteries to Bluffs Trail from 8:00-14:00 on 3 August 2024 is deleted. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent tries to look up the calendar event (either by searching or listing all)
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
                # Milestone 1 – The hike event has been removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Group Hike at Batteries to Bluffs Trail",
                                    "start_datetime_iso": "2024-08-03T08:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_13_7200c330-9951-414e-8576-1a98f3548322_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_13",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T14:00:00-07:00",
            is_read_time="2024-07-24T14:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know if your hiking buddies have replied to your message. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has my message gotten any replies in the Hiking Group?",
                },
            ],
            reasoning="The user is asking about replies to a message.\nFirst, I should try and find the mentioned group chat. I have found the group being referred to. I see three new messages in reply to the user's one. \nA message from Theo Appleseed on July 24, 2024 at 11:12.\nA message from Cookie Watson on July 24, 2024 at 11:13.\nA message from Akira Muramoto on July 24, 2024 at 11:14.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Hiking Group is checked for recent replies to the user's message from all members.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
            milestones=[
                # Milestone 0 – The agent looks up messages to check for replies in the “Hiking Group”
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
                # Milestone 1 – A reply from Theo Appleseed in the Hiking Group was found
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
                                                "value": "Hiking Group",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "theo.appleseed@example.com",
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
                # Milestone 2 – The agent looks up messages to check for replies in the “Hiking Group”
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
                # Milestone 3 – A reply from Cookie Watson in the Hiking Group was found
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
                                                "value": "Hiking Group",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "cookie.watson@mckinley.com",
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
                # Milestone 4 – The agent looks up messages to check for replies in the “Hiking Group”
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
                # Milestone 5 – A reply from Akira Muramoto in the Hiking Group was found
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
                                                "value": "Hiking Group",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "akira.muramoto@sportsfan.com",
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
                    ],
                ),
                # Milestone 6 – The agent informs the user that replies were received from all three friends
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Theo",
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
                                    "content": "Cookie",
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
                                    "content": "Akira",
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
                (2, 3),
                (4, 5),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_13_8e45ad1e-ebb9-467a-b20f-7867cc399a1e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_13",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T11:15:00-07:00",
            is_read_time="2024-07-24T11:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to reply to Robin's last message saying, That's ok,  maybe next time.  Just be sure to send me  pics of how your grooming goes – I'd love to see your little cutey-pie! "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text in reply to my one refusal saying, That's ok,  maybe next time. Just be sure to send me  pics of how your grooming goes –I'd love to see your little cutey-pie!",
                },
            ],
            reasoning="User John Quinn wants to send a textual reply. He mentions a refusal and a grooming. I see in user John Quinn's texts that one correspondent, co-worker Robin Selmoure, refused the user's hiking invitation on the grounds of a conflicting grooming session. I shall draft the reply of user John Quinn to co-worker Robin Selmoure and present it for approval. ",
            success_conditions=[
                {
                    "input_text": "1.A text is sent in reply to Robin Selmoure saying, That's ok,  maybe next time. Just be sure to send me  pics of how your grooming goes –I'd love to see your little cutey-pie!",
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
                # Milestone 0 – Agent looks up Robin’s previous conversation or messages
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
                # Milestone 1 – New outgoing reply message to Robin is created
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
                                                "408-555-0132",
                                                "robin.selmoure@palantir.com",
                                            )
                                        ]
                                    ],
                                    "content": "maybe next time",
                                    "creation_datetime_iso": "2024-07-24T11:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,  # ensure phrase like “maybe next time” appears,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial DB snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_13_7200c330-9951-414e-8576-1a98f3548322_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_13",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T14:00:00-07:00",
            is_read_time="2024-07-24T14:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know if your hiking buddies have replied to your message. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Have I gotten any replies to my message about trails in the group?",
                },
            ],
            reasoning="The user is asking about replies to a message.\nFirst, I should try and find the mentioned group chat. \nThe user has indicated the content of the message being referred to, I should search their messages for the keyword 'trail'\nI see only one potential match, a message sent by the user in the group chat Hiking Group on July 24, 2024 at 11:10.\nI have found the group being referred to. I see three new messages in reply to the user's one. \nA message from Theo Appleseed on July 24, 2024 at 11:12.\nA message from Cookie Watson on July 24, 2024 at 11:13.\nA message from Akira Muramoto on July 24, 2024 at 11:14.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Hiking Group is checked for recent replies to the user's message from all members.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
            milestones=[
                # Milestone 0 – the agent looks through the user’s messages
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
                # Milestone 1 – the agent answers the user and mentions every friend who replied
                Milestone(
                    snapshot_constraints=[
                        # Must mention Theo
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Theo",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Must mention Cookie
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Cookie",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Must mention Akira
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Akira",
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
                (0, 1),  # Tool-use precedes informing the user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_13_3525d1f6-a914-4116-9ea3-ef9c062e0381_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_13",
                "contact",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-02T16:40:00-07:00",
            is_read_time="2024-08-02T16:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You have broken your ankle and need to cancel your hike. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the group hike. ",
                },
            ],
            reasoning="The user wants to delete the group hike. I should first go the user's Calendar and find the event. \n\nThe user has an event called Group Hike at Batteries to Bluffs Trail on 3 August 2024 from 8:00-14:00, so this must be the event the user meant. \n\nI will delete this event and let the user know.",
            success_conditions=[
                {
                    "input_text": "1. Group Hike at Batteries to Bluffs Trail from 8:00-14:00 on 3 August 2024 is deleted. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (either via direct list or search)
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
                # Milestone 1 – The hike event is removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Group Hike at Batteries to Bluffs Trail",
                                    "start_datetime_iso": "2024-08-03T08:00:00-07:00",
                                    "end_datetime_iso": "2024-08-03T14:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieval precedes deletion
            ],
        ),
    ]
