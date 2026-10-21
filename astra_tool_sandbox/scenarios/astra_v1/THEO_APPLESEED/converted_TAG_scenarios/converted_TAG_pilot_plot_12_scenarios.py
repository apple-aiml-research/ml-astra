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
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_str_contains_all_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
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


def get_TAG_THEO_APPLESEED_pilot_plot_12(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="THEO_APPLESEED_12_987d99b7-fb66-463e-b6e2-5e6c0f44d9a6_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:01:00-07:00",
            is_read_time="2024-07-25T20:01:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "Someone has just texted you and you want to know who it was. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Was John the person who texted me most recently?",
                },
            ],
            reasoning="The user is asking me to identify the sender of a message.\nI should look at their message history and determine the most recently received message.\nI can see that the user received a message from John Quinn, received at 20:00 on July 25, 2024, this is the most recent message.\nI should confirm for the user that John Quinn was the most recent sender.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that John Quinn is the person who texted them most recently, at 20:00 on July 25, 2024",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – Agent retrieves recent messages
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
                # Milestone 1 – Tool output includes the message from John Quinn at the expected time
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
                                                "value": "john.quinn@palantir.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-25T20:00:00-07:00",
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
                # Milestone 2 – Agent informs the user that John (Quinn) was the most recent sender
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("John", "John Quinn")],
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
            name="THEO_APPLESEED_12_f97d8f39-add6-4a32-a3f9-06ca1058d857_single_turn_3",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:15:00-07:00",
            is_read_time="2024-07-25T20:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to make a last minute request ahead of your hiking trip with your friend to pack a first aid kit. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to the text about snacks and say "bring a first aid kit too"',
                },
            ],
            reasoning="The user wants to reply to a text about snacks. I need to determine which text they are talking about. I'll start by looking at texts that the user has received in the last fifteen minutes, so since 20:00, then expand my query field after that if I don't find anything. I only see one text that has come in in the last fifteen minutes, from John Quinn at 20:08. It says \"Awesome! I'll pack some snacks. See you Saturday!\" so that mentions snacks. Because it's from John Quinn, I'll craft the reply to John Quinn saying \"bring a first aid kit too\".",
            success_conditions=[
                {
                    "input_text": '1. A message reply is sent to John Quinn saying "bring a first aid kit too"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks through recent messages to locate the snack conversation
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
                # Milestone 2 – Tool output includes the message from John Quinn at the expected time
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
                                                "value": "john.quinn@palantir.com",
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
                # Milestone 2 – A reply is sent to John Quinn that asks to bring a first-aid kit
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require that both John Quinn and Theo Appleseed are in the conversation
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
                                        ]
                                    ],
                                    # Key phrase confirming the request
                                    "content": "first aid kit",
                                    "creation_datetime_iso": "2024-07-25T20:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial state
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
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_12_f97d8f39-add6-4a32-a3f9-06ca1058d857_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:15:00-07:00",
            is_read_time="2024-07-25T20:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to make a last minute request ahead of your hiking trip with your friend to pack a first aid kit. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a text to the person coming on my Hiking Trip saying "bring a first aid kit too"',
                },
            ],
            reasoning='The user wants to send a text to the person coming on their hiking trip. First I\'ll look for an event with that name and then I\'ll look at the invitees to see who the recipient of this text should be. I see an event named "Hiking Trip" on Saturday 27 July from 6:00-10:00. I see John Quinn is an invitee on that event. So I\'ll text John Quinn saying "bring a first aid kit too".',
            success_conditions=[
                {
                    "input_text": '1. A message reply is sent to John Quinn saying "bring a first aid kit too"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up relevant information (contact or calendar)
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
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – A new message is sent to John Quinn with the required content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least John Quinn’s identifier must be present among the participants.
                                    "participants_addresses": [
                                        [
                                            (
                                                "john.quinn@palantir.com",
                                                "1234-5678-9108",
                                            )
                                        ]
                                    ],
                                    "content": "bring a first aid kit too",
                                    "creation_datetime_iso": "2024-07-25T20:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieval precedes sending the message
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_12_987d99b7-fb66-463e-b6e2-5e6c0f44d9a6_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:01:00-07:00",
            is_read_time="2024-07-25T20:01:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "Someone has just texted you and you want to know who it was. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who was my most recent message from?",
                },
            ],
            reasoning="The user is asking about the sender of a message.\nI should look through their conversations and identify the most recent sender.\nI can see that the user received a message from John Quinn, received at 20:00 on July 25, 2024.\nLooking at the timestamps of all the other texts in the user's messages, this one from 20:00 on 25 July 2024 is closest to the current time of 20:01 on 25 July 2024. This is the most recent message.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that John Quinn is the person who texted them most recently, at 20:00 on July 25, 2024",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – Agent looks up recent messages
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
                # Milestone 1 – The tool output from Milestone 0 shows a message from John Quinn
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
                                                "value": "john.quinn@palantir.com",
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
                # Milestone 2 – Agent tells the user the last message was from John Quinn
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "John Quinn",
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
            name="THEO_APPLESEED_12_00686794-f2fc-4117-83c0-f2a979df794f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:10:00-07:00",
            is_read_time="2024-07-25T20:10:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to ask John Quinn to bring some sauerkraut to the hiking trip. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to John Quinn saying 'Bring a jar of sauerkraut.'",
                },
            ],
            reasoning="The user wants to send a message to John Quinn. The user has already confirmed what they'd like to say to be 'Bring a jar of sauerkraut' so I can send the message now.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A message is sent to John Quinn saying 'Bring a jar of sauerkraut'.",
                }
            ],
            tool_allow_list=["send_message", "search_contacts", "get_all_contacts"],
            milestones=[
                # Milestone 0 – Agent tries to locate John Quinn in contacts
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
                # Milestone 1 – Verify John Quinn appeared in the contact-search result
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
                                                "value": "John Quinn",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9108",
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
                # Milestone 2 – A new message is sent that tells John to bring sauerkraut
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Must at least include John Quinn; extra participants (e.g., self) are allowed
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9108",
                                                "john.quinn@palantir.com",
                                            )
                                        ]
                                    ],
                                    "content": "Bring a jar of sauerkraut",
                                    "creation_datetime_iso": "2024-07-25T20:10:00-07:00",
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
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_12_2ef715fc-36d7-4cd6-bb83-7ea50ddeb9f4_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:45:00-07:00",
            is_read_time="2024-07-25T20:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know when to leave home for your meeting tomorrow morning; you need 30 minutes to commute and 15 minutes to walk to your office. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When do I need to leave the house tomorrow morning? I need 30 minutes to commute and 15 minutes to walk to my office.",
                },
            ],
            reasoning="The user wants to know when to leave the house for their meeting tomorrow morning. Tomorrow is 26 July 2024; the only morning event that day is the 'Project Review Meeting' at 09:00 in Conference Room B at the office. The user needs 30 minutes to commute plus 15 minutes to walk to the office — 45 minutes of travel — so they must leave home 45 minutes before 09:00, at 08:15. I will tell the user to leave the house at 08:15.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed they need to leave the house at 08:15 (45 minutes before the 09:00 Project Review Meeting on 26 July 2024).",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (tomorrow’s hike)
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
                # Milestone 1 – Returned calendar data includes tomorrow's Project Review Meeting (09:00)
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
                                                "value": "Project Review Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-26T09:00:00-07:00",
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
                # Milestone 2 – Agent tells the user when to leave the house (08:15)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "8:15",
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
                (0, 1),  # Calendar lookup → verify event found
                (1, 2),  # Event found → user informed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_12_31ee6b4f-85f3-46a2-8111-9b2a72fc8987_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_12",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:00:00-07:00",
            is_read_time="2024-07-25T20:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know who just texted you.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who just texted me? ",
                },
            ],
            reasoning="The user wants to know who just texted them. I should check their messages to the most recent message and who the sender was. I see one message from John Quinn received at 20:00. This must be the message they mean. I'll show the user the message from John. ",
            success_conditions=[
                {
                    "input_text": "1. Messages are checked for the most recent text message. ",
                    "statefullness": "Stateless",
                },
                {
                    "statefullness": "Stateless",
                    "input_text": "2. The message received from John Quinn on July 25th at 20:00 is read aloud to the user. ",
                },
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
            milestones=[
                # Milestone 0 – Agent checks messages to find the most recent text message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,  # tool call traces
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",
                                }
                            ),
                            column_similarity_measure={
                                # Allow either a direct "get all" or a targeted search over messages
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "get_all_messages",
                                        "search_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Confirms that the John Quinn message on 2024-07-25T20:00:00-07:00 exists in the retrieved messages
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
                                        # Check key fields for the most recent message
                                        match_conditions={
                                            "conversation_name": {
                                                "value": "John Quinn",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "john.quinn@palantir.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-25T20:00:00-07:00",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Hey Theo! Are you up for a hike this Saturday? Thinking of hitting the Big Rock Mountain Trail.",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,  # validate based on the messages retrieval in Milestone 0
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
                # Milestone 2 – Agent informs the user who texted and reads the message content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,  # user-facing reply
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Must mention the sender and convey the message text
                                    "content": [("John", "hike")],
                                }
                            ),
                            column_similarity_measure={
                                # Require both the sender's name and some form of the message content
                                "content": column_str_contains_all_similarity,
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # messages retrieval → confirm correct latest message
                (1, 2),  # confirmed message → user notified with sender and content
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_12_b5e0309f-0e25-48f3-8cb0-2eaa7119e000_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:15:00-07:00",
            is_read_time="2024-07-25T20:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send Cookie a text inviting her to join you on your hike this weekend "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Ask Cookie if she'd like to join John Quinn and I on our hiking trip this weekend saying, Hey Cookie my friend John and I are going on a hiking trip this weekend, would you like to join?",
                },
            ],
            reasoning="The user would like to ask Cookie if she'd like to join them and John Quinn on their hiking trip this weekend. The user only has one contact named Cookie: Cookie Watson. I shall use the message content provided and send 'Hey Cookie my friend John and I are going on a hiking trip this weekend, would you like to join?' to Cookie Watson.\n",
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Cookie Watson saying "Hey Cookie my friend John and I are going on a hiking trip this weekend, would you like to join?"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up Cookie’s contact information
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
                # Milestone 1 – Confirm that Cookie Watson is found in the contact-search result from Milestone 0
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
                                                "value": "Cookie Watson",
                                                "partial": False,
                                            },
                                            # Either phone or email proves it’s the right contact
                                            "phone_number": {
                                                "value": "1234-5678-9107",
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
                # Milestone 2 – A new outgoing message to Cookie containing the hiking invite is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Verify Cookie is among the conversation participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9107",  # Cookie’s phone
                                                "cookie.watson@example.com",  # or Cookie’s email
                                            )
                                        ]
                                    ],
                                    "content": "hiking trip",  # key phrase expected in the body,
                                    "creation_datetime_iso": "2024-07-25T20:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                    # No need to exclude other DBs; only one addition expected
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                # Milestone 2 is independent (uses reference_milestone_node_index=-1)
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_12_f97d8f39-add6-4a32-a3f9-06ca1058d857_single_turn_4",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:15:00-07:00",
            is_read_time="2024-07-25T20:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to make a last minute request ahead of your hiking trip with your friend to pack a first aid kit. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to the text that came in less than ten minutes ago saying "bring a first aid kit too"',
                },
            ],
            reasoning="The user wants to reply to a text. I need to determine which text they are talking about before I can send it. They said the text to reply to is one that came in less than ten minutes ago. It's 20:15 right now, meaning ten minutes ago was 20:05, so I need to find all the texts that the user has received with a time stamp after 20:05. I only see one text that has come in since 20:05, a message from John Quinn at 20:08. Because it's from John Quinn, he will be the recipient of the user's text \"bring a first aid kit too\", so I'll send that now.",
            success_conditions=[
                {
                    "input_text": '1. A message reply is sent to John Quinn saying "bring a first aid kit too"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – The agent looks up recent messages to identify the one that arrived <10 minutes ago
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
                # Milestone 1 – Confirm the message from John Quinn was found in the previous tool output
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
                                                "value": "john.quinn@palantir.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                # We only need to know the agent located John’s last message
                                                "value": "Awesome! I'll pack some snacks",
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
                # Milestone 2 – A reply message has been sent to John Quinn that asks to bring a first-aid kit
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
                                                "theo.appleseed@example.com",
                                                "1234-5678-9101",
                                            ),
                                        ]
                                    ],
                                    "content": "first aid kit",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-25T20:15:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare with initial DB snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Tool call → confirm John's message present
                # Milestone 2 is independent (uses reference_milestone_node_index=-1)
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_12_c1cac399-3bec-4f1b-9b2b-aa95fe930ee4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:00:00-07:00",
            is_read_time="2024-07-25T20:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know who just texted you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who just texted me? ",
                },
            ],
            reasoning='The user wants to know who just texted them. I should check their messages to the most recent message and who the sender was. I see one message from John Quinn received at 20:00 that says "Hey Theo! Are you up for a hike this Saturday? Thinking of hitting the Big Rock Mountain Trail.". This must be the message they mean. I\'ll show the user the message from John. ',
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The user is informed that John Quinn sent them a message saying "Hey Theo! Are you up for a hike this Saturday? Thinking of hitting the Big Rock Mountain Trail." at 20:00 on 25 July 2024. ',
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – The agent queries the message database to see who texted
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
                                        "get_all_messages",
                                        "search_messages",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – Confirm the returned result includes the recent message from John Quinn
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
                                                "value": "john.quinn@palantir.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "hike",
                                                "partial": True,  # only needs to mention hike
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
                # Milestone 2 – The agent tells the user that John texted (and optionally what he said)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("John Quinn", "Johnny", "John")],
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
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_12_2ef715fc-36d7-4cd6-bb83-7ea50ddeb9f4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:45:00-07:00",
            is_read_time="2024-07-25T20:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know the location of your hike in the morning. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where is my hiking trip?",
                },
            ],
            reasoning="The user wants to know where there hiking trip is. I should check their Calendar. Looking at their Calendar they only have one event named Hiking Trip, from 06:00-10:00 on 27 July 2024. This event says the hike is taking place at Big Rock Mountain Trail, Orchard County, CA. I will tell the user this.",
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the location of the event named "Hiking Trip" happening on 27 July 2024 from 06:00-10:00 is "Big Rock Mountain Trail, Orchard County, CA".',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 — Calendar lookup performed
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
                # Milestone 1 — The hiking trip event with the correct location is returned
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
                                                "value": "Hiking Trip",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Big Rock Mountain Trail",
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
                # Milestone 2 — Agent informs the user of the hike location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Big Rock Mountain Trail",
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
                (0, 1),  # Calendar lookup -> verify event details
                (1, 2),  # Event found -> user informed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_12_fc4d1659-d198-4f67-9d1d-a31199b85b25_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:30:00-07:00",
            is_read_time="2024-07-25T20:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to dictate a reply to John saying that you will bring the sleeping bags for the hiking trip. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a message reply to John Quinn saying "Hi John just to say I\'ll bring the sleeping bags on the hike just in case."',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called John Quinn.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nThe user wants to say \"I'll bring the sleeping bags on the hike just in case.\" so I'll send that message to John Quinn.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A reply message is sent to John Quinn saying "I\'ll bring the sleeping bags on the hike just in case." ',
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "send_message",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent invokes a contact or message retrieval tool
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
                                        "search_messages",
                                        "get_all_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Verify that John Quinn’s contact (or conversation) was actually retrieved
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
                                                "value": "John Quinn",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "john.quinn@palantir.com",
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
                # Milestone 2 – A reply message is sent to John Quinn mentioning the sleeping bags
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
                                                "theo.appleseed@example.com",
                                                "1234-5678-9101",
                                            ),
                                        ]
                                    ],
                                    "content": "sleeping bags",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-25T20:30:00-07:00",
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
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieval tool used → verify John's info returned
                # Milestone 2 is independent (uses reference_milestone_node_index=-1)
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_12_c1fa0952-ac51-4f60-92c1-77fe8b2c5e8a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T21:00:00-07:00",
            is_read_time="2024-07-26T21:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You need to take care of your niece so you need to tell your friend you're canceling your hiking plans "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you send John a thing saying \"I can't go hiking anymore, sorry something has come up, my niece has gotten pretty sick so I wanna be around in case she needs me. Let's reschedule for next week maybe?\"",
                },
            ],
            reasoning="The user wants to communicate with someone named John. First let me figure out how they want to communicate, and then figure out who they mean by John. They want to send John a 'thing'. Since they've dictated some content to send, I'll formulate a text message. Now, They have two Johns in their contacts - John Quinn and John Appleseed. The text they're asking me to send mentions hiking, so let me see if either John is in the user's calendar events. I see an event named 'Hiking Trip' on 27 July 2024 at 6:00-10:00 with John Quinn as an invitee, so I'll assume that's who the user wants to text. What's more, looking at their previous texts, I can see they were talking to John Quinn about hiking, so that gives me even more confidence that John Quinn is the right John to contact. I'll send the message the user dictated, \"I can't go hiking anymore, sorry something has come up, my niece has gotten pretty sick so I wanna be around in case she needs me. Let's reschedule for next week maybe?\". ",
            success_conditions=[
                {
                    "input_text": "1. A message is sent to John Quinn with the text \"I can't go hiking anymore, sorry something has come up, my niece has gotten pretty sick so I wanna be around in case she needs me. Let's reschedule for next week maybe?\"",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_message",
                "search_messages",
                "get_all_messages",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – Agent looks up John Quinn in contacts
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
                # Milestone 1 – Verify the contact search returned John Quinn
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
                                                "value": "John Quinn",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9108",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "john.quinn@palantir.com",
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
                # Milestone 2 – Agent looks up which John in the personal context
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
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 3 – A new outgoing message to John Quinn with the correct content has been created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [("john.quinn@palantir.com", "1234-5678-9108")]
                                    ],
                                    "content": "I can't go hiking anymore",
                                    "creation_datetime_iso": "2024-07-26T21:00:00-07:00",
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
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact search → confirm John Quinn found
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_12_4061e11c-3a93-4151-aea8-d8a55ac40b6f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:10:00-07:00",
            is_read_time="2024-07-25T20:10:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You're getting exciting about your upcoming hiking trip and have been texting your friend about it.  You want to remind him to bring his power bank. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to John and say See ya there! Don't forget your power bank.",
                },
            ],
            reasoning="Ok so the user want's to reply to someone named John. They have two contacts named John: John Appleseed and John Quinn. Since they said they want to reply to John, let me see which John send them a message more recently. There are no texts from John Appleseed. John Quinn's most recent text is from two minutes ago at 20:08 and it says \"Awesome! I'll pack some snacks. See you Saturday!\". I'll assume the user wants to reply to John Quinn because that's the only person named John who has sent them a text they can even reply to. I will send the text to John Quinn saying \"See ya there! Don't forget your power bank.\"",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A message is sent to John Quinn saying "See ya there! Don\'t forget your power bank."',
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "send_message",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks up John Quinn in contacts
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
                # Milestone 1 – Verify the contact search returned John Quinn
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
                                                "value": "John Quinn",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9108",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "john.quinn@palantir.com",
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
                # Milestone 2 – Agent looks up which John in the personal context
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
                # Milestone 3 – Verify a new outgoing message was created to John Quinn that reminds him
                # to bring a power bank.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Both John and Theo must be represented by at least one of their
                                    # known identifiers (email or phone).  No restriction on ordering and
                                    # additional identifiers are allowed.
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
                                        ]
                                    ],
                                    # Message body should mention the power bank (key user instruction).
                                    "content": "power bank",
                                    "creation_datetime_iso": "2024-07-25T20:10:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            # Compare against the state before the agent acted
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_12_373036fe-cd10-40e9-8f04-43e3aac6715f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:05:00-07:00",
            is_read_time="2024-07-25T20:05:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what John has said as you are messaging him but need to be hands-free at the moment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What did John say? Read it out.",
                },
            ],
            reasoning='Okay so, the user wants to know what John has said. I can see two contacts named John, John Quinn and John Appleseed. There are no messages from John Appleseed and there is an active message thread with John Quinn, with the most recent message from him received one minute ago at 20:04 saying "How about we start early? Meet at 6 AM?". So this is the John the user is referring to. I can then read out John Quinn\'s latest message to the user.',
            success_conditions=[
                {
                    "input_text": "1. The message received from John Quinn on the 25th July 2024 at 20:04 saying 'How about we start early? Meet at 6 AM?' is read out to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent tries to retrieve John’s recent message(s)
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
                # Milestone 1 – Confirm the retrieved results include John Quinn’s 25-Jul-2024 20:04 message
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
                                                "value": "john.quinn@palantir.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "How about we start early? Meet at 6 AM?",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-25T20:04:00-07:00",
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
                            reference_milestone_node_index=0,  # parse the tool output of milestone 0
                        ),
                    ],
                ),
                # Milestone 2 – The agent tells the user what John said
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "How about we start early",
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
            name="THEO_APPLESEED_12_373036fe-cd10-40e9-8f04-43e3aac6715f_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:05:00-07:00",
            is_read_time="2024-07-25T20:05:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what John has said as you are messaging him but need to be hands-free at the moment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read out my latest message. ",
                },
            ],
            reasoning="Right so, the user wants their latest message read out. I need to see, among all the user's received texts, which one came in most recently, so which one came in closest to the current time of 20:05. From their message log I can see that the last person they were messaging was John Quinn. I can then read out John Quinn's latest message received at 20:04 on the 25th July 2024 which says 'How about we start early? Meet at 6 AM?'.",
            success_conditions=[
                {
                    "input_text": "1. The message received from John Quinn on the 25th July 2024 at 20:04 saying 'How about we start early? Meet at 6 AM?' is read out to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – The agent must invoke a tool to retrieve the latest messages
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
                # Milestone 1 – Confirm the tool’s output contained John Quinn’s latest message
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
                                                "value": "john.quinn@palantir.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "How about we start early? Meet at 6 AM?",
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
                # Milestone 2 – The agent read the message out to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "How about we start early",
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
            name="THEO_APPLESEED_12_c1fa0952-ac51-4f60-92c1-77fe8b2c5e8a_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T21:00:00-07:00",
            is_read_time="2024-07-26T21:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You need to take care of your niece so you need to tell your friend you're canceling your hiking plans "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send the dude I'm hiking with this message: \"I can't go hiking anymore, sorry something has come up, my niece has gotten pretty sick so I wanna be around in case they need me. Let's reschedule for next week maybe?\"",
                },
            ],
            reasoning="The user wants to send a message to someone they are hiking with. Let me see if there are any events in the calendar that mention hiking. I see an event named 'Hiking Trip' on 27 July 2024 at 6:00-10:00 with John Quinn as an invitee, so I'll assume that's the \"dude\" they're hiking with and thus that's who the user wants to text. What's more, looking at their previous texts, I can see they were talking to John Quinn about hiking, so that gives me even more confidence that John Quinn is the right person to send a message to. I'll send the message the user dictated, \"I can't go hiking anymore, sorry something has come up, my niece has gotten pretty sick so I wanna be around in case they need me. Let's reschedule for next week maybe?\".",
            success_conditions=[
                {
                    "input_text": "1. A message is sent to John Quinn with the text \"I can't go hiking anymore, sorry something has come up, my niece has gotten pretty sick so I wanna be around in case they need me. Let's reschedule for next week maybe?\"",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_message",
                "search_calendar_events",
                "get_all_calendars",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks up John Quinn’s contact information
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
                # Milestone 1 – Confirm that the contact retrieved in Milestone 0 matches John Quinn
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
                                                "value": "John Quinn",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9108",
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
                # Milestone 2 – The agent looks up John Quinn’s contact information
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
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 2 – A message is sent to John Quinn with the expected apology / reschedule text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least one of these identifiers for John must appear in the new conversation’s participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9108",
                                                "john.quinn@palantir.com",
                                            )
                                        ]
                                    ],
                                    # Check that the core part of the apology / reschedule text is present
                                    "content": "I can't go hiking anymore",
                                    "creation_datetime_iso": "2024-07-26T21:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # Compare against initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # Ignore sandbox tool-trace rows when validating message addition
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → verify John Quinn found
                # Milestone 2 is independent (uses reference_milestone_node_index=-1)
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_12_f97d8f39-add6-4a32-a3f9-06ca1058d857_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:15:00-07:00",
            is_read_time="2024-07-25T20:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to make a last minute request ahead of your hiking trip with your friend to pack a first aid kit. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to John\'s text saying "bring a first aid kit too"',
                },
            ],
            reasoning="First, I'll need to figure out who the user wants to text. They said they want to text John, but there are two Johns in their contacts: John Appleseed and John Quinn. Let me look at their text messages with both of these contacts. I don't see any messages between the user and John Appleseed. I do see a text from John Quinn today at 20:08 saying \"Awesome! I'll pack some snacks. See you Saturday!\". Looking at the user's calendar, there is an event named \"Hiking Trip\" on Saturday 27 July from 6:00-10:00, and John Quinn is an invitee on that event. Knowing that John Quinn is already packing some snacks for Saturday, likely for this hiking trip event, it would make sense that the user wants to tell John other things to bring, like this first aid kit they're asking me to text about. Taking all that information into consideration, I'll assume John Quinn is the right John to send the text \"bring a first aid kit too\" to.",
            success_conditions=[
                {
                    "input_text": '1. A message reply is sent to John Quinn saying "bring a first aid kit too"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the correct John / conversation
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
                # Milestone 1 – Confirm that the John Quinn conversation found
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
                                                "value": "John Quinn",
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
                # Milestone 2 – A reply message to John Quinn has been created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # must include John Quinn; extras (e.g., the user's address) are allowed
                                    "participants_addresses": [
                                        [
                                            (
                                                "john.quinn@palantir.com",
                                                "1234-5678-9108",
                                            )
                                        ]
                                    ],
                                    "content": "first aid kit",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-25T20:15:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare with pre-task snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # information retrieval precedes sending the message
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_12_f97d8f39-add6-4a32-a3f9-06ca1058d857_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:15:00-07:00",
            is_read_time="2024-07-25T20:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to make a last minute request ahead of your hiking trip with your friend to pack a first aid kit. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to John Quinn saying "bring a first aid kit too"',
                },
            ],
            reasoning='The user wants to reply to a contact named John Quinn to say "bring a first aid kit too" so I\'ll do that.',
            success_conditions=[
                {
                    "input_text": '1. A message reply is sent to John Quinn saying "bring a first aid kit too"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – The agent tries to locate John Quinn (either via contacts or existing messages)
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
                                        "search_messages",
                                        "get_all_messages",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – A new outbound message to John Quinn that asks to bring a first-aid kit
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Ensure John Quinn is in the conversation participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "john.quinn@palantir.com",
                                                "1234-5678-9108",
                                            )
                                        ]
                                    ],
                                    "content": "first aid kit",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-25T20:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,  # must mention first aid kit
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against pre-task state
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieval precedes sending the message
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_12_21289da1-c7ba-4abf-832a-f853bc155a19_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T20:15:00-07:00",
            is_read_time="2024-07-25T20:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to make a last minute request ahead of your hiking trip with John Quinn to pack a first aid kit. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to my friend John saying bring a first aid kit too on upcoming hiking trip for July 27, 2024.",
                },
            ],
            reasoning='The user wants to reply to their friend John to say "bring a first aid kit too". There are two contacts named John — John Quinn (College Friend) and John Appleseed (Father). Since the user means their friend, that is John Quinn, so I reply to him.',
            success_conditions=[
                {
                    "input_text": '1. A message reply is sent to John Quinn saying "bring a first aid kit too"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "send_message",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks up John in the contacts database
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
                # Milestone 1 – John Quinn’s contact information is returned from the lookup in Milestone 0
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
                                                "value": "John Quinn",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "john.quinn@palantir.com",
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
                # Milestone 2 – A new outgoing message to John Quinn that asks to bring a first-aid kit
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
                                                "theo.appleseed@example.com",
                                                "1234-5678-9101",
                                            ),
                                        ]
                                    ],
                                    "content": "first aid kit",
                                    "creation_datetime_iso": "2024-07-25T20:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # Both participants must be present and no one else
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                # Message content must mention the first-aid kit
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → confirm John found
                # Milestone 2 is independent (uses reference_milestone_node_index=-1)
            ],
        ),
    ]
