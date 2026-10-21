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
    column_rouge_l_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
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


def get_TAG_THEO_APPLESEED_pilot_plot_16(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="THEO_APPLESEED_16_733386a1-3d65-4053-91f3-e1644bafbb07_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:35:00-07:00",
            is_read_time="2024-07-27T11:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to see the last message John Quinn sent you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me John Quinn's last message.",
                },
            ],
            reasoning="The user wants to see John Quinn's last message. Let me look for him in contacts. I will look for the last message he sent. I will show it to the user.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. The user is shown the last text message ,'For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.', sent by John Quinn on July 27th 2024 at 11:15.",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent invokes a message-retrieval tool
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
                # Milestone 1 – Returned tool output contains John Quinn’s last message
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
                                                "value": "For sure. Speaking of creativity",
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
                # Milestone 2 – Agent shows the user the correct last message text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "For sure. Speaking of creativity",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
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
            name="THEO_APPLESEED_16_7ed91374-0874-46fb-a3e7-47b521ed526b_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:35:00-07:00",
            is_read_time="2024-07-27T11:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to shoot a quick message to John and see if he's mad at you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you text my pal John Quinn for me to ask him if he's mad at me?",
                },
            ],
            reasoning='The user wants to text John Quinn and say "Are you mad at me?".  \n\nAs the user has told me everything I need to know so I will draft up the message and send it. \n\nI will now let the user know I have sent the message. ',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A message is sent to John Quinn that says "Are you mad at me?".',
                }
            ],
            tool_allow_list=["send_message", "get_all_contacts", "search_contacts"],
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
                # Milestone 1 – The contact lookup returned John Quinn
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
                            reference_milestone_node_index=0,  # depends on tool outcome of Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – A message was sent to John asking if he is mad
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
                                                "1234-5678-9108",
                                                "john.quinn@palantir.com",
                                            )
                                        ]
                                    ],
                                    "content": "mad at me",
                                    "creation_datetime_iso": "2024-07-27T11:35:00-07:00",
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
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # contact lookup -> confirm John
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_7ed91374-0874-46fb-a3e7-47b521ed526b_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:35:00-07:00",
            is_read_time="2024-07-27T11:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You were terribly late for today's hike and want to shoot a quick message to John and see if he's mad at you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I was terribly late this morning, text John saying "Are you mad at me?".',
                },
            ],
            reasoning="The user wants to text John saying \"Are you mad at me?\", given the context that they were terribly late this morning. I should first figure out who John is. \n\nLooking at the user's Contacts they have 2 Johns so I must narrow down which John they meant. I should check other apps to try and narrow it down. \n\nHmm, looking at the user's Calendar they have just came from a hike with John Quinn, and I see nothing with John Appleseed so the user must mean John Quinn.\n\nAs the user has already told me the contents of the message I will write up and send it.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A message is sent to John Quinn that says "Are you mad at me?".',
                }
            ],
            tool_allow_list=[
                "send_message",
                "get_all_contacts",
                "search_contacts",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – Agent looks up John in contacts
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
                # Milestone 1 – John Quinn is found in the tool output
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
                # Milestone 2 – Agent looks up calendar events
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
                # Milestone 3 – Hiking trip is found
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
                                            "start_datetime_iso": {
                                                "value": "2024-07-27T06:00:00-07:00",
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
                # Milestone 4 – Message sent to John with the correct content
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
                                    "content": "Are you mad at me?",
                                    "creation_datetime_iso": "2024-07-27T11:35:00-07:00",
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
                (0, 1),  # contact lookup → validate John found
                (2, 3),  # hiking trip found
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_34e21972-225f-4b72-869b-90e8015fd0f3_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "contact",
                "calendar",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T10:40:00-07:00",
            is_read_time="2024-07-27T10:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want send a message to thank John for accompanying you on the hike and suggest you plan another one soon. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you text John and say hey John, thank you for joining me on the hike and that we should plan another one soon. ",
                },
            ],
            reasoning="I need to text John to thank him for joining the user on a hike, so I must first figure out the intended contact. The user has two contacts named John: John Quinn and John Appleseed. Based on the fact that the content they told me to include their text message mentions a hike, I'll see which John went on a hike with the user. I found the event Hiking Trip in the calendar with John Quinn as an attendee, so that must be who the user wants to text. \n\nI have searched the user's contacts and have found a 'John Quinn', who is also listed as an attendee in the Hiking Trip event form the user's schedule this morning. I can safely assume that 'John Quinn' is the intended contact. ",
            success_conditions=[
                {
                    "input_text": 'A message is sent to John Quinn that says "Hey John, thank you for joining me on the Hike. We should plan another hike soon."',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent looks up which “John” to text
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
                # Milestone 1 – Confirm John Quinn was one of the contacts returned
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
                                "content": column_one_similarity,
                            },
                            reference_milestone_node_index=0,
                        ),
                    ],
                ),
                # Milestone 2 – A new outgoing message to John Quinn was created with the correct intent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # John’s phone must appear in the participant list
                                    "participants_addresses": [
                                        [("john.quinn@palantir.com", "1234-5678-9108")]
                                    ],
                                    # Message body should contain the user’s thanks / hike reference
                                    "content": "thank you",  # substring check below,
                                    "creation_datetime_iso": "2024-07-27T10:40:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to the initial state
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
            name="THEO_APPLESEED_16_5a6bad52-4901-4fda-a5b3-5ed12b2db4dd_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:30:00-07:00",
            is_read_time="2024-07-27T11:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to create a reminder to go pick up that book John recommended you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Create an event "John\'s Book Recommendation" for 15:00-15:30 today.',
                },
            ],
            reasoning='Ok so the user wants to create an event "John\'s Book Recommendation" for 15:00-15:30 today. First is the event name which was given to me by the user. as "John\'s Book Recommendation." Next is the timeframe which was also given to me by the user as 15:00-15:30 today.  I will now create the event "John\'s Book Recommendation" for 15:00-15:30 on 27 July 2024.',
            success_conditions=[
                {
                    "input_text": '1. The event "John\'s Book Recommendation" is created for 15:00-15:30 on 27 July 2024. ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["create_calendar_event"],
            milestones=[
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Book Recommendation",
                                    "start_datetime_iso": "2024-07-27T15:00:00-07:00",
                                    "end_datetime_iso": "2024-07-27T15:30:00-07:00",
                                    "creation_datetime_iso": "2024-07-27T11:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against pre-task snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_80d5f72e-6c40-4ffd-885d-da35bf10ed67_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T23:55:00-07:00",
            is_read_time="2024-07-27T23:55:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send John Quinn a text message about the sci-fi book he mentioned. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a text to my college friend at Palantir, 'I just started reading the book you recommended, really enjoying it!'.",
                },
            ],
            reasoning="Okay, the user wants to send a text message saying 'I just started reading the book you recommended, really enjoying it!' to their 'college friend at Palantir'. I can see no contacts named that in their contact list. Although I can see 'John Quinn' labelled as 'College Friend' and his email address corresponds to @palantir.com. This is all evidence that whom the user wants to send a message to is John Quinn. I can confirm with the user prior to sending the message then to double check.",
            success_conditions=[
                {
                    "input_text": "1. An SMS message will be sent to John Quinn on the 27th July 2024 at 23:55 saying 'I just started reading the book you recommended, really enjoying it!'.\n",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up the “college friend at Palantir”
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
                # Milestone 1 – Confirm the contact found is John Quinn
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
                        ),
                    ]
                ),
                # Milestone 2 – SMS message is sent to John Quinn with the correct content and timestamp
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Ensure John’s phone number is one of the participants; allow self or others in the conversation
                                    "participants_addresses": [
                                        [("1234-5678-9108", "john.quinn@palantir.com")]
                                    ],
                                    "content": "I just started reading the book you recommended, really enjoying it!",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-27T23:55:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
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
            name="THEO_APPLESEED_16_2ebf89ad-df86-4fc0-aa8e-9aa6a2d21fc1_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T10:50:00-07:00",
            is_read_time="2024-07-27T10:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know if John messaged you about the hike. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did John Quinn message me?",
                },
            ],
            reasoning="Ok so the user wants to know if John Quinn has messaged them. First I will establish who John Quinn is. The name John Quinn corresponds with the contact of the same name. Next I will look at the message logs with John Quinn. The user has most recently contacted John through text so I will look there. It seems the user has received a message from John 5 minutes ago. I will now inform the user that they received a message from John Quinn at 10:45 on 27 July 2024. ",
            success_conditions=[
                {
                    "input_text": "1. Messages are checked for the latest message from John Quinn about a hike and the message received on July 27th at 10:45 is shown to the user. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – The agent uses a message-retrieval tool
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
                # Milestone 1 – The returned messages include the one from John Quinn at 10:45 AM on 27-Jul-2024
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
                                                "value": "2024-07-27T10:45:00-07:00",
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
                # Milestone 2 – The agent communicates this information to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Absolutely, Theo!",
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
            name="THEO_APPLESEED_16_2ebf89ad-df86-4fc0-aa8e-9aa6a2d21fc1_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "calendar",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T10:50:00-07:00",
            is_read_time="2024-07-27T10:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know if John messaged you about the hike. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did John message about the hike? ",
                },
            ],
            reasoning="The user wants to know if John messaged about their hike. I'm not sure which John it is since they have two contacts called John, John Appleseed and John Quinn. I should check their calendar to see if there is a hiking event with John as a participant. I see the 'Hiking Trip' event at 6:00 today July 27th with John Quinn. It must be that John, so I'll check for messages from today with John Quinn. I see one new message from John today at 10:45 in response to a message from Theo about the hike. I'll show the user that message ",
            success_conditions=[
                {
                    "input_text": "1. Messages are checked for the latest message from John Quinn about a hike and the message received on July 27th at 10:45 is shown to the user. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks up recent messages (from John)
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
                # Milestone 1 – Verify the returned tool output contains John Quinn’s 10:45 am hike-related message
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
                                            # A distinctive snippet from the message body
                                            "content": {
                                                "value": "great way to start the day",
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
                # Milestone 2 – Agent informs the user, mentioning (a snippet of) John’s message
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
                                            "Absolutely",
                                            "great way to start the day",
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
            name="THEO_APPLESEED_16_80d5f72e-6c40-4ffd-885d-da35bf10ed67_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T23:55:00-07:00",
            is_read_time="2024-07-27T23:55:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send John Quinn a text message about the sci-fi book he mentioned. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send my contact John Quinn the following via SMS messaging: 'I just started reading the book you recommended, really enjoying it!'.",
                },
            ],
            reasoning="Okay, the user wants to send an SMS message saying 'I just started reading the book you recommended, really enjoying it!' to their 'college friend at Palantir' to their contact 'John Quinn'. I can see that the user only has one contact corresponding to that name. I can confidently assume that that is whom the user wants to message. I can then confirm with the user before sending the message.",
            success_conditions=[
                {
                    "input_text": "1. An SMS message will be sent to John Quinn on the 27th July 2024 at 23:55 saying 'I just started reading the book you recommended, really enjoying it!'.\n",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent tries to locate John Quinn in the contacts list
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
                # Milestone 1 – John Quinn’s contact record was indeed returned from the lookup in Milestone 0
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
                # Milestone 2 – A new SMS message to John Quinn containing the requested text exists
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
                                    "content": "I just started reading the book you recommended, really enjoying it!",
                                    "creation_datetime_iso": "2024-07-27T23:55:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # John’s number must be among the participants; extra addresses (e.g., self) are allowed
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
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
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_5cfda922-360a-4dba-aaca-80a046743856_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:40:00-07:00",
            is_read_time="2024-07-27T11:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to dictate a reply to John saying that he left his sunglasses in your car. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a message reply to John Quinn saying "Hi John just to say you left your sunglasses in my car, do you want me to drop them off?"',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called John Quinn.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A reply message is sent to John Quinn saying that he left his sunglasses in your car.",
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
                # Milestone 0 – Agent looks up John or the conversation via a read-only tool
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
                # Milestone 1 – A reply message to John Quinn was actually sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Must include John’s address (allowing additional participants such as self)
                                    "participants_addresses": [
                                        [("john.quinn@palantir.com", "1234-5678-9108")]
                                    ],
                                    # Message body must reference the sunglasses
                                    "content": "sunglasses",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-27T11:40:00-07:00",
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
                        ),
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_5a6bad52-4901-4fda-a5b3-5ed12b2db4dd_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:30:00-07:00",
            is_read_time="2024-07-27T11:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to create a reminder to go pick up that book John recommended you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Remind me to pick up John's book recommendation around three today on calendar and put his full name in the calendar title. ",
                },
            ],
            reasoning="Ok so the user wants a reminder to pick up John's book recommendation around three today, and they want John's full name in the title. First I will create a name for the event based off of the information given to me. John's full name is John Quinn, so I will name the event \"John Quinn's Book Recommendation\". Next I will set the timeframe. The user wants it to start at 15:00 but doesn't set an end time. I will use the default of half an hour as this event mainly serves as a reminder. I will now create the event \"John Quinn's Book Recommendation\" for 15:00 on 27 July 2024.",
            success_conditions=[
                {
                    "input_text": '1. The event "John Quinn\'s Book Recommendation" is created for 15:00 on 27 July 2024. ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "create_calendar_event",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – Agent uses a messages retrieval tool (directly or via a helper) to find latest messages
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
                # Milestone 1 – Confirm that the specific latest message from John Quinn exists in the tool output
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
                                            "sender_address": {
                                                "value": "john.quinn@palantir.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-27T11:15:00-07:00",
                                                "partial": False,
                                            },
                                            "status": {
                                                "value": "read",
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
                # Milestone 2 – Confirm the new reminder event exists with the correct time window
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "John Quinn",  # title should at least mention John
                                    "start_datetime_iso": "2024-07-27T15:00:00-07:00",
                                    "creation_datetime_iso": "2024-07-27T11:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                # default exact-match measures for the two datetime fields,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_7928a858-fa42-4d49-be2d-d674cdf2a997_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:40:00-07:00",
            is_read_time="2024-07-27T11:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send a message to John Quinn saying 'how about next week?' "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to John Quinn saying 'how about next week?'",
                },
            ],
            reasoning="The user wants to send a message to John Quinn. I'll check the user's contacts for a contact under this name. There is a contact under that name so I'll pull up that number. Next I'll ask the user what they'd like to say. Okay, now that I have the content of the message I can send it and notify the user.",
            success_conditions=[
                {
                    "input_text": "1. A message is sent to John Quinn saying 'how about next week?'",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up John Quinn in the contacts database
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
                        ),
                    ],
                ),
                # Milestone 1 – Verify that John Quinn’s contact information was returned from the search in Milestone 0
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
                                            # Either phone or email may appear – we just need to see one of them
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
                # Milestone 2 – A new message has been sent to John with the requested content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Confirm John is among the participants
                                    "participants_addresses": [
                                        [("john.quinn@palantir.com", "1234-5678-9108")]
                                    ],
                                    "content": "how about next week?",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-27T11:40:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare against initial state
                        ),
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → confirm John Quinn found
                (1, 2),  # Contact confirmed → message sent
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_f026f171-ed93-41ff-9da3-1350cb3ce84e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:20:00-07:00",
            is_read_time="2024-07-27T11:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You feel like you and John really hit it off at your hike this morning, and you're beginning to see him in a different light.   You want to try asking him out for coffee, so you send him a text. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I\'m going to need you to text John back and write "Not yet.... Maybe you can tell me a little about it over coffee at some point?". Ready to send?',
                },
            ],
            reasoning="The user asked me to send a text for them, to John. So there are two Johns in the user's contact, John Quinn and John Appleseed. I'm not exactly sure which John they want me to message. I'm going to check the user's message history with both of these Johns. There is no message history with John Appleseed from what I can see, but there are very recent texts from an active conversation with John Quinn from today, as recent as 5 minutes ago. The user also said to text 'back', so they must want to reply to John Quinn's messages.\n\n\nWith the user's confirmation, I will send the message \"Not yet.... Maybe you can tell me a little about it over coffee at some point?\" to John Quinn.",
            success_conditions=[
                {
                    "input_text": '1. The system will send the following message to John Quinn: "Not yet.... Maybe you can tell me a little about it over coffee at some point?".',
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
                # Milestone 0 ─ The agent tries to locate the relevant conversation / contact
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
                # Milestone 1 ─ A new message is sent to John Quinn with the requested text
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
                                                "theo.appleseed@example.com",
                                                "1234-5678-9101",
                                            ),  # Theo
                                        ]
                                    ],
                                    "sender_address": "theo.appleseed@example.com",
                                    "content": "Not yet.... Maybe you can tell me a little about it over coffee at some point?",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-27T11:20:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_contains_similarity,  # look for “Not yet” etc.
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox chatter
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # retrieval precedes sending the message
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_7aec669b-514c-4a5a-b3bc-1e711b1539a8_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:40:00-07:00",
            is_read_time="2024-07-27T11:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to delete the last message you sent to John Quinn. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I don't want to see the message I sent about recommendation and planning another hike soon anymore.",
                },
            ],
            reasoning="The user no longer wants to see the message they sent about recommendation and planning another hike soon. I'll have to look through the user's messaging history to find this message.\n\nI found a message sent to John Quinn at 11:30 on 2024-07-27 that says \"Not yet, but it's next on my list. Thanks for the recommendation! Let's plan another hike soon?\" This must be the message the user is referring to.\n\nSince they don't want to see the message anymore, I will delete the message and inform the user that I've done so.",
            success_conditions=[
                {
                    "input_text": "1. Message sent to John Quinn at 11:30 on 2024-07-27 saying \"Not yet, but it's next on my list. Thanks for the recommendation! Let's plan another hike soon?\" is deleted.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "remove_message_or_conversation",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent uses a message-retrieval tool to locate the message
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
                # Milestone 1 – Confirm that the retrieved results include the specific message the user wants removed
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
                                            "content": {
                                                "value": "Let's plan another hike soon",
                                                "partial": True,
                                            },
                                            "participants_addresses": {
                                                "value": [
                                                    "john.quinn@palantir.com",
                                                    "theo.appleseed@example.com",
                                                ],
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
                # Milestone 2 – Verify the message was actually deleted from the MESSAGING database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [
                                            (
                                                "john.quinn@palantir.com",
                                                "1234-5678-9108",
                                            ),  # John Quinn
                                            (
                                                "theo.appleseed@example.com",
                                                "1234-5678-9101",
                                            ),  # Theo
                                        ]
                                    ],
                                    "content": "Let's plan another hike soon",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_contains_similarity,
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # retrieval → confirmation
                (1, 2),  # confirmation → deletion
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_a5022fe9-61bf-442b-98bc-daee0728222d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T13:15:00-07:00",
            is_read_time="2024-07-24T13:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "Cookie is feeling sick so has cancelled your dinner date.   You now want to remove it from your Calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my dinner with Cookie tonight. ",
                },
            ],
            reasoning="The user wants to delete their dinner with Cookie tonight. I should check their Calendar. Hmm looks like they have an event called Dinner with Cookie from 19:00-21:00 on 24 July 2024. I will delete this and let the user know I've deleted it. ",
            success_conditions=[
                {
                    "input_text": "1. Dinner with Cookie from 19:00-21:00 on 24 July 2024 is removed from Calendar. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar to find the event to delete
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
                # Milestone 1 – Verify that the “Dinner with Cookie” event was actually returned from the lookup
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
                                                "value": "Dinner with Cookie",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-24T19:00:00-07:00",
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
                # Milestone 2 – Event is removed from the calendar database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dinner with Cookie",
                                    "start_datetime_iso": "2024-07-24T19:00:00-07:00",
                                    "end_datetime_iso": "2024-07-24T21:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ]
                ),
                # Milestone 3 – Agent confirms to the user that the dinner was deleted
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Dinner with Cookie",
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
                (0, 1),  # lookup → verify event retrieved
                (1, 2),  # verification → event removed
                (2, 3),  # removal → user confirmation
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_66b81ffd-0375-4dd6-8b5b-3c2598d56fa5_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
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
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to get a time stamp off a text message. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When did the last text from John come in.",
                },
            ],
            reasoning="The user wants the time stamp of a text message. The sender of the message is John, I can deduce he means John Quinn as they were having a conversation earlier that day. see the message and shall relay its datestamp to user. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "The user is dictated the time stamp of a text message.",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – The agent looks up messages (from John)
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
                # Milestone 1 – The retrieved messages include John’s 11:15 am, July 27 2024 text
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
                                                "value": "2024-07-27T11:15:00-07:00",
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
                # Milestone 2 – The agent tells the user the correct timestamp
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "11:15",
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
                (0, 1),  # Retrieve messages → confirm John’s message exists
                (1, 2),  # After confirming, respond to user
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_17d491d7-1fb1-4af9-a417-53903795eb76_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "contact",
                "messaging",
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
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to get a time stamp off a text message. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When did the last text from John come in.",
                },
            ],
            reasoning="The user wants the time stamp of a text message. The sender of the message is John. I see the user has two contacts named John: John Appleseed and John Quinn. I can deduce the user means John Quinn as they were having a text conversation earlier today, and there are no text messages from John Appleseed in the user's threads. The last text that John Quinn sent to the user was today 27 July 2024 at 11:15 and it said \"For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.\". I'll communicate the timestamp of 11:15 to the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The user is informed that the most recently delivered text message from John Quinn, with the content "For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you\'d like it.", was delivered at 11:15 on 27 July 2024.',
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – Agent uses a messages retrieval tool to look for John's texts
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
                # Milestone 1 – Confirms the specific last message from John Quinn was retrieved with correct timestamp and content
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
                                            "sender_address": {
                                                "value": "john.quinn@palantir.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-27T11:15:00-07:00",
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
                # Milestone 2 – Agent informs the user of the correct timestamp for the last text from John
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We just need the essential info: date and time; wording can vary.
                                    "content": "11:15",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Ensure the date is also communicated (any phrasing that includes the date string)
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "July 27",
                                            "Jul 27",
                                            "27 July",
                                            "27 Jul",
                                            "7-27",
                                            "07-27",
                                            "7/27",
                                            "07/27",
                                            "the 27th",
                                            "27th of July",
                                            "today",
                                            "2024-07-27T11:15",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity,
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (
                    0,
                    1,
                ),  # messages retrieval → confirm the correct John Quinn message and timestamp
                (1, 2),  # confirmed retrieval → inform user with the timestamp
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_a5022fe9-61bf-442b-98bc-daee0728222d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T13:15:00-07:00",
            is_read_time="2024-07-24T13:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "Cookie is feeling sick so has cancelled your dinner date.   You now want to remove it from your Calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my event tonight. ",
                },
            ],
            reasoning="The user wants to delete their event tonight. I should check their Calendar. Looks like they only have one event left today, Dinner with Cookie from 19:00-21:00 on 24 July 2024. This must be the event the user meant. I will delete it and tell the user it is deleted. ",
            success_conditions=[
                {
                    "input_text": "1. Dinner with Cookie from 19:00-21:00 on 24 July 2024 is removed from Calendar. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events for “tonight”
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
                # Milestone 1 – Verify the “Dinner with Cookie” event appears in the tool result
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
                                                "value": "Dinner with Cookie",
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
                # Milestone 2 – Event is removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dinner with Cookie",
                                    "start_datetime_iso": "2024-07-24T19:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with pre-task snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Event lookup → confirm correct event
                (1, 2),  # Confirmation → removal
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_7aec669b-514c-4a5a-b3bc-1e711b1539a8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:40:00-07:00",
            is_read_time="2024-07-27T11:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to delete the last message you sent to John Quinn. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the last message I sent to John.",
                },
            ],
            reasoning="The user wants to delete the last message they sent to John. I'll check the user's contacts first.\n\nI found two Johns: John Quinn and John Appleseed. I'm not sure which one the user is referring to, so I'll check their messages with both contacts.\n\nThe user has no recent message history with John Appleseed, but I did find messages with John Quinn today (2024-07-27). The last one, with content \"Not yet, but it's next on my list. Thanks for the recommendation! Let's plan another hike soon?\", was sent by the user at 11:30. I'll delete this message and let the user know.",
            success_conditions=[
                {
                    "input_text": "1. Message sent to John Quinn at 11:30 on 2024-07-27 saying \"Not yet, but it's next on my list. Thanks for the recommendation! Let's plan another hike soon?\" is deleted.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "remove_message_or_conversation",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – The agent searches the message database for John Quinn's conversation
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
                # Milestone 1 – Confirm the correct message was found in the tool output from Milestone 0
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
                                            "content": {
                                                "value": "Not yet, but it's next on my list.",
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
                # Milestone 2 – Verify the message has been removed from the MESSAGING database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "John Quinn",
                                    "content": "Not yet, but it's next on my list.",  # key substring
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                                "conversation_name": column_exact_match_similarity,
                            },
                            reference_milestone_node_index=-1,  # compare to initial state
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Search → confirm correct message retrieved
                (1, 2),  # Confirm retrieval → verify deletion
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_8e491896-7731-4bdb-9f29-cd35d1a68034_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:25:00-07:00",
            is_read_time="2024-07-27T11:25:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know if John has responded to your last message. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has John Quinn responded to my last message? Yes or no.",
                },
            ],
            reasoning="The user is asking if they have received a reply.\nI should consult their conversation with the named contact. The last message from the user to John Quinn was at 11:00, and I see one new message from John, received at 11:15 on July 27, 2024. It is now 11:25, and that is the most recent message in the thread, so there are no messages left un-replied for the user; John has responded to every single one.\nI should inform the user with yes.",
            success_conditions=[
                {
                    "input_text": "1) The user has been informed with yes, as John Quinn sent the last message.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "get_all_calendars",
                "search_calendar_events",
            ],
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
                # Milestone 1 – Verify that a message from John Quinn was indeed returned
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
                # Milestone 2 – Agent informs the user whether John has replied
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("responded", "replied", "yes")],
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
                (0, 1),  # Tool call → confirm John’s message is found
                (1, 2),  # Confirmation → user-facing response
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_60efdeb3-2a0e-461a-9820-17f10ac8c1dd_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "calendar",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:25:00-07:00",
            is_read_time="2024-07-27T11:25:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what did John say as you're texting him but can't use your hands at the moment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read out what John said just there?",
                },
            ],
            reasoning="Okay, the user wants to know what John has just said. I can see two Johns are in the user's contact list, John Quinn and John Appleseed, but the one they've been texting more recently today is John Quinn. I can then read out John's message that says  'For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.' to the user.",
            success_conditions=[
                {
                    "input_text": "1. The latest message received from John Quinn at 11:15 on the 27th July 2024 saying 'For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.' is read out to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent uses a messages retrieval tool to figure out what John "just said"
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
                # Milestone 1 – Confirms the latest message from John Quinn with the correct content was retrieved
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
                                            # Make sure it's John Quinn in the conversation participants
                                            "participants_addresses": {
                                                "value": ["john.quinn@palantir.com"],
                                                "partial": True,  # allow Theo's address etc. alongside
                                            },
                                            # And that the content of his message matches the target text
                                            "content": {
                                                "value": "For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.",
                                                "partial": False,
                                            },
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
                            reference_milestone_node_index=0,  # validate based on the retrieval in milestone 0
                        ),
                    ],
                ),
                # Milestone 2 – The agent tells the user what John said, including the key parts of the message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Only check that the core of John's message is conveyed
                                    "content": "new sci-fi book",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_rouge_l_similarity
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieval call → confirm correct John Quinn message found
                (1, 2),  # Correct message identified → user informed with that content
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_32895c84-da1a-44f9-b410-c93e8c01605e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
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
            reference_time="2024-07-27T15:35:00-07:00",
            is_read_time="2024-07-27T15:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You hiked with John Quinn this morning, but he seemed annoyed during the hike.   He also hasn't replied to your text for four hours, so you want to ask if he's mad at you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Text John saying "Are you mad at me?".',
                },
            ],
            reasoning="The user wants to text John saying \"Are you mad at me?\". I should first figure out who John is. \n\nLooking at the user's Contacts they have 2 Johns so I must narrow down which John they meant. I should check other apps to try and narrow it down. \n\nHmm, looking at the user's Calendar they have just came from a hike with John Quinn. John Quinn also hasn't replied to their latest text message they sent four hours ago, so maybe that's why they're worried he's mad.\n\nAs the user has already told me the contents of the message I will write up a draft real quick and send it to John Quinn.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A message is sent to John Quinn that says "Are you mad at me?".',
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
                # Milestone 0 – Agent looks up John in contacts
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
                # Milestone 1 – Confirm that John Quinn was retrieved from the contact search
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
                # Milestone 2 – Verify a message was sent to John that says "Are you mad at me?"
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
                                    "content": "Are you mad at me?",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-27T15:35:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare with initial state
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
            name="THEO_APPLESEED_16_0f9f5d4e-c6a1-4c44-ad68-8df08ac5e6c4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:25:00-07:00",
            is_read_time="2024-07-27T11:25:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what did John say as you're texting him but can't use your hands at the moment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read out what John said just there?",
                },
            ],
            reasoning="Okay, the user wants to know what John has just said. I can see two Johns are in the user's contact list but the one they've been speaking to today is John Quinn. I can then read out John's message that says  'For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.' to the user.",
            success_conditions=[
                {
                    "input_text": "1. The latest message received from John Quinn at 11:15 on the 27th July 2024 saying 'For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.' is read out to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_messages",
                "get_all_messages",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent tries to retrieve recent messages
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
                # Milestone 1 – Confirm the expected John Quinn message was found in the result of milestone 0
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
                                                "value": "For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.",
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
                                    "content": "For sure. Speaking of creativity",
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
                (0, 1),  # messages retrieved -> verify correct message included
                (1, 2),  # message found -> tell the user
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_817234ef-fdf1-4301-818c-08a2798358b9_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:25:00-07:00",
            is_read_time="2024-07-27T11:25:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to view John's message about the sci-fi book again. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the message from John about the novel please ",
                },
            ],
            reasoning='The user wants to view "the message from John about the novel".\n\nOkay, firstly, I need to go to the user\'s Messages to see if they\'ve received any from "John".\n\nAlright, so I can see they\'ve been messaging a "John Quinn". I will now parse through these messages to see if there are any that correspond to the above description.\n\nRight, so, there aren\'t any exact matches, but they did receive a message at 11:15:00 on July 28th, 2024 with the content "For sure. Speaking of creativity, have you read that new sci-fi books I mentioned last time. Think you\'d like it". \n\nI surmise that this is the message the user is referring to, as book and novel are literal synonyms of each other.\n\nI will now present this message to the user. ',
            success_conditions=[
                {
                    "input_text": '1. The user is presented with the message received from John Quinn at 11:15:00 on July 27th, 2024 with the content "For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you\'d like it."',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
            milestones=[
                # Milestone 0 – Agent invokes a message-retrieval tool
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
                # Milestone 1 – Confirm the expected message from John Quinn was returned
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
                                                "value": "sci-fi",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-27T11:15:00-07:00",
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
                    ]
                ),
                # Milestone 2 – Agent shows the user the message content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "new sci-fi book",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,  # allow paraphrasing but must include the message text
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
            name="THEO_APPLESEED_16_21e46ebc-c4a1-4262-92e2-8fc981ccb851_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T20:45:00-07:00",
            is_read_time="2024-07-27T20:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to ask John what the name of that book he recommended is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a message to the last person I texted that says "Hey man, what was the name of the book you were on about earlier?"',
                },
            ],
            reasoning='The user is asking me to send a message.\nFirst, I need to identify the intended recipient. The user has specified that this should be the last person they texted. Looking through their messages, the most recent communication was with John Quinn, culminating with a message received July 27, 2024, 11:30.\nI am confident that John Quinn is the intended recipient. I will draft the message as instructed.\nA message stating "Hey man, what was the name of the book you were on about earlier?" will be sent to John Quinn.',
            success_conditions=[
                {
                    "input_text": '1. A message is sent to John Quinn asking " Hey man, what was the name of the book you were on about earlier?"',
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
                # Milestone 0 – Agent looks up the last conversation / messages
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
                # Milestone 1 – Verify that John Quinn’s address appeared in the tool output from Milestone 0
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
                                            # We only need to see that John’s address shows up
                                            "participants_addresses": {
                                                "value": "john.quinn@palantir.com",
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
                # Milestone 2 – A new outgoing message is sent to John that contains the requested text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At minimum, John must be in the participants list
                                    "participants_addresses": [
                                        [("john.quinn@palantir.com", "1234-5678-9108")]
                                    ],
                                    "content": "what was the name of the book",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-27T20:45:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Tool usage to find last message → verify John found
                (1, 2),  # After confirming recipient → message is sent
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_eb99d637-00d3-414e-b698-bea26e14fc72_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:35:00-07:00",
            is_read_time="2024-07-27T11:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send John a follow-up message about your last hiking trip. John's pace was incredibly fast."
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send this message to the person I just texted: "It’s hard for me to keep up with your pace! What’s your training plan for it?".',
                },
            ],
            reasoning='The user wants to send a message.\nFirst I should determine who they want to send it to.\nThe user has indicated that the recipient should be the person who they have most recently sent a message to.\nLooking through the user\'s message history I can see that the only message sent today was sent to John Quinn at 11:30 on July 27, 2024. I am confident that this is the correct recipient.\nI will compose the message as prompted.\nA message with the content "It’s hard for me to keep up with your pace! What’s your training plan for it?" will be sent to John Quinn.\n',
            success_conditions=[
                {
                    "input_text": '1. A message is sent to John Quinn stating "It’s hard for me to keep up with your pace! What’s your training plan for it?".',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_messages", "send_message", "search_messages"],
            milestones=[
                # Milestone 0 – Agent looks at recent messages to figure out who was texted last
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
                # Milestone 1 – The tool result used in Milestone 0 contains a thread with John Quinn
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
                                            # We just need to see John’s address in the participants list
                                            "participants_addresses": {
                                                "value": "john.quinn@palantir.com",
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
                # Milestone 2 – A new message has been sent to John containing the requested text
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
                                    "content": "hard for me",
                                    "creation_datetime_iso": "2024-07-27T11:35:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_21e46ebc-c4a1-4262-92e2-8fc981ccb851_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T20:45:00-07:00",
            is_read_time="2024-07-27T20:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to ask John what the name of that book he recommended is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a message to John Quinn that says "Hey man, what was the name of the book you were on about earlier?"',
                },
            ],
            reasoning="The user is asking me to send a message. \nI must find John Quinn's contact details. I'll search the users contacts. I found John Quinn's contact details. I will set that as the recipient of the message.\nI draft the message with what the user has requested.The user requested the message to say \"Hey man, what was the name of the book you were on about earlier?\" I wait for confirmation from the user that this is correct and then send the message on receipt.",
            success_conditions=[
                {
                    "input_text": '1. A message is sent to John Quinn asking " Hey man, what was the name of the book you were on about earlier?"',
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
                # Milestone 0 – Agent looks up John Quinn’s contact information
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
                # Milestone 1 – John Quinn is found in the contact-search result from Milestone 0
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
                # Milestone 2 – A new message is sent to John with the requested text
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
                                    "content": "Hey man, what was the name of the book you were on about earlier?",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-27T20:45:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # John must be among the participants; extra (self) participant allowed
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                # Verify the key phrase appears in the message body (case-insensitive)
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
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
                (0, 1),  # Contact lookup → confirm John found
                (1, 2),  # John confirmed → message sent
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_28725a3a-8fe9-4e79-83a3-9341160b3670_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T12:00:00-07:00",
            is_read_time="2024-07-27T12:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You ask John if he would like to go on another Hike next week same time and place and can you bring your friend Cookie Watson. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to John Quinn saying, I had a great hike trip with John today and want to do another next week on Saturday. I would also like to bring my friend Cookie Watson on the trip if he doesn't mind.",
                },
            ],
            reasoning="User wants to create another hiking trip for the following week August 3rd at 06:00 and bring a guest named Cookie Watson. \n\nWill message John Quinn and ask if he would like to attend another hike on Saturday the 3rd of August and if he doesn't mind Cookie Watson joining them on the hike. ",
            success_conditions=[
                {
                    "input_text": "1. Message sent to John Quinn inquiring if he would like to go on another hike next Saturday and asking if you can bring your friend Cookie Watson.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up John Quinn in the contacts
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
                # Milestone 1 – Confirm that the contact returned in Milestone 0 is John Quinn
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
                # Milestone 2 – A new message to John Quinn asking about another hike and bringing Cookie Watson
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Accept either John’s phone or email as the identifier, but no one else
                                    "participants_addresses": [
                                        [("1234-5678-9108", "john.quinn@palantir.com")]
                                    ],
                                    "content": "Cookie",
                                    "creation_datetime_iso": "2024-07-27T12:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_contains_similarity,
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
            name="THEO_APPLESEED_16_817234ef-fdf1-4301-818c-08a2798358b9_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:25:00-07:00",
            is_read_time="2024-07-27T11:25:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to view John's message about the sci-fi book again. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you show me John's message about the sci-fi book again please?",
                },
            ],
            reasoning='The user wants to view "John\'s message about the sci-fi book again".\n\nOkay, firstly I need to go to the user\'s Messages to see if they\'ve received any from "John".\n\nOkay, great, I can see they\'ve just received a message from "John Quinn" at 11:15:00 on July 27th, 2024 with the content "For sure. Speaking of creativity, have you read that new sci-fi books I mentioned last time. Think you\'d like it". This must be the message the user is referring to.\n\nI will present it to them right now. ',
            success_conditions=[
                {
                    "input_text": '1. The user is presented with the message received from John Quinn at 11:15:00 on July 27th, 2024 with the content "For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you\'d like it."',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
            milestones=[
                # Milestone 0 – Agent looks up messages (must invoke a message-retrieval tool)
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
                # Milestone 1 – Returned tool output contains John’s sci-fi book message
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
                                                "value": "For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.",
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
                # Milestone 2 – Agent shows the user the requested message content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "sci-fi book",
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
                (0, 1),  # Tool invocation → verify correct message found
                (1, 2),  # After confirming retrieval → verify user-facing response
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_0f9f5d4e-c6a1-4c44-ad68-8df08ac5e6c4_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:25:00-07:00",
            is_read_time="2024-07-27T11:25:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what did John say as you're texting him but can't use your hands at the moment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read to me my latest message.",
                },
            ],
            reasoning="Right so, the user wants their latest received message read out to them. From their message threads I can see that the latest message received was from John Quinn on the 27th July 2024 at 11:15 saying ' 'For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.'. I can then read this information out to the user.",
            success_conditions=[
                {
                    "input_text": "1. The latest message received from John Quinn at 11:15 on the 27th July 2024 saying 'For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.' is read out to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_messages",
                "get_all_messages",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent invokes a message-retrieval tool
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
                # Milestone 1 – The retrieved result set contains John’s latest message
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
                                                "value": (
                                                    "For sure. Speaking of creativity, have you "
                                                    "read that new sci-fi book I mentioned last time? "
                                                    "Think you'd like it."
                                                ),
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
                # Milestone 2 – Agent tells the user the contents of that message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": (
                                        "For sure. Speaking of creativity, have you read that new sci-fi book"
                                    ),
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
                (0, 1),  # Retrieval tool call → verify correct message in output
                (1, 2),  # After verifying, agent responds to user
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_32895c84-da1a-44f9-b410-c93e8c01605e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
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
            reference_time="2024-07-27T15:35:00-07:00",
            is_read_time="2024-07-27T15:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You hiked with John Quinn this morning, but he seemed annoyed during the hike.   He also hasn't replied to your text for four hours, so you want to ask if he's mad at you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you text my pal John Quinn for me to ask him if he's mad at me?",
                },
            ],
            reasoning='The user wants to text John Quinn and say "Are you mad at me?".  \n\nAs the user has told me everything I need to know so I will draft up the message and send it. \n\nI will now let the user know I have sent the message. ',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A message is sent to John Quinn that says "Are you mad at me?".',
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
                # Milestone 1 – John Quinn’s contact entry was returned from the search in Milestone 0
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
                                "content": column_one_similarity,
                            },
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – A new message asking if John is mad has been sent to the conversation with John Quinn
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
                                    "content": "mad",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-27T15:35:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare against the initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # contact search → verify John found
                (1, 2),  # verified contact → message sent
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_60efdeb3-2a0e-461a-9820-17f10ac8c1dd_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "calendar",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:25:00-07:00",
            is_read_time="2024-07-27T11:25:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what did John say as you're texting him but can't use your hands at the moment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read to me my latest message.",
                },
            ],
            reasoning="Right so, the user wants their latest received message read out to them. From their message threads I can see that the latest message received was from John Quinn on the 27th July 2024 at 11:15 saying ' 'For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.'. I can then read this information out to the user.",
            success_conditions=[
                {
                    "input_text": "1. The latest message received from John Quinn at 11:15 on the 27th July 2024 saying 'For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.' is read out to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent uses a messages retrieval tool (directly or via a helper) to find latest messages
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
                # Milestone 1 – Confirm that the specific latest message from John Quinn exists in the tool output
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
                                            "sender_address": {
                                                "value": "john.quinn@palantir.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-27T11:15:00-07:00",
                                                "partial": False,
                                            },
                                            "status": {
                                                "value": "read",
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
                # Milestone 2 – Agent reads out the message content (or close paraphrase) to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We only require that the key sentence from the message appears;
                                    # phrasing around it ("John said:", etc.) is flexible.
                                    "content": "new sci-fi book",
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
                (0, 1),  # Retrieve messages → confirm correct latest message exists
                (1, 2),  # Have correct message identified → read that content to user
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_8e491896-7731-4bdb-9f29-cd35d1a68034_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:25:00-07:00",
            is_read_time="2024-07-27T11:25:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know if John has responded to your last message. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has my hiking buddy responded to my last message yet? Yes or no.",
                },
            ],
            reasoning="The user is asking if they have received a reply.\nFirst, I need to determine which contact they are referring to. I cannot see anyone tagged as hiking buddy in the contact list. \nI should search the user's conversations and calendar and see if they yield any results.\nI can see one potential match, the user's recent Hiking Trip event has John Quinn as a participant.\nI should consult their conversation with the named contact. The last message from the user to John Quinn was at 11:00, and I see one new message from John, received at 11:15 July 27, 2024. It is now 11:25, and that is the most recent message in the thread, so there are no messages left un-replied for the user; John has responded to every single one.\nI should inform the user with yes.",
            success_conditions=[
                {
                    "input_text": "1) The user has been informed with yes, as messages checked for reply from John Quinn and he has replied.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "get_all_calendars",
                "search_calendar_events",
            ],
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
                # Milestone 1 – The retrieved message list contains at least one recent message from John Quinn
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
                                            # We do not need to verify timestamps/content here;
                                            # presence of a message from John is sufficient for task logic
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
                # Milestone 2 – Agent informs the user that John has responded
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
                                            "yes",
                                            "has responded",
                                            "he responded",
                                            "john replied",
                                            "john has",
                                            "he has",
                                            "he replied",
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
                (0, 1),  # message search → confirm John’s message present
                (1, 2),  # confirmation of John’s message → inform user
            ],
        ),
    ]
