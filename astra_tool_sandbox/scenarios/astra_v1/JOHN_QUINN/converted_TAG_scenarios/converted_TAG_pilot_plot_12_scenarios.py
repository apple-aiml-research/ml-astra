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
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
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


def get_TAG_JOHN_QUINN_pilot_plot_12(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="JOHN_QUINN_12_b1828c69-7cae-473d-9c16-69826b453410_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_12",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T15:00:00-07:00",
            is_read_time="2024-07-24T15:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want a reminder of the name of the supplement Akira mentioned to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What supplement did Akira message me about yesterday?",
                },
            ],
            reasoning="The user wants to know what supplement Akira messaged them about yesterday. I'll see if I can find any mention of a supplement in the user's messages. I found a message from Akira Muramoto about a supplement. I'll inform the user the name of the supplement is 'Green' by Soylent ",
            success_conditions=[
                {
                    "input_text": "1. Akira Muramoto's message containing the name of a supplement is summarised ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – Agent uses a message-retrieval tool to look for Akira’s message
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
                # Milestone 1 – Confirm that the retrieved message is Akira’s and mentions the supplement “Green”
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
                                                "value": "akira.muramoto@sportsfan.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Green",
                                                "partial": True,  # just needs to contain the word
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
                # Milestone 2 – Agent tells the user the supplement name (“Green” by Soylent)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("Green", "Soylent")],
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
                (0, 1),  # Retrieval tool call → confirm correct message found
                (1, 2),  # Correct message found → inform user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_12_9d14b412-d986-4909-b9e4-86d439774583_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_12",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T20:30:00-07:00",
            is_read_time="2024-07-23T20:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You are searching the web to find a new food supplement and are trying to find the one Akira recommended. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'What did the message from Akira Muramoto say about "by solvent"?\n',
                },
            ],
            reasoning='User wants to know shay someone said so I\'ll ask who, they tell me Akira, I see only one contact with this name so I know to check this contact conversation, and they mention a phrase to search for - "By solvent". I find a message corresponding to this and offer it to user.',
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The message containing the phrase "by Soylent"',
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – Agent looks up Akira’s message
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
                # Milestone 1 – Confirm the retrieved message contains “by Soylent” and is from Akira
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
                                                "value": "by Soylent",
                                                "partial": True,
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
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – Agent tells the user what the message said including the key phrase
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "by Soylent",
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
                (0, 1),  # message search → confirm correct message
                (1, 2),  # confirmed retrieval → user-facing answer
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_12_20ba6332-6627-474e-bf9a-16b3564bcaf4_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_12",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T19:30:00-07:00",
            is_read_time="2024-07-23T19:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "Akira is coming to pick up the tent tonight. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Create an event "Akira Visit" at 20:00-20:30 tonight. ',
                },
            ],
            reasoning='Ok so the user wants to create an event "Akira Visit" at 20:00-20:30 tonight. First is the name which is given by the user. Next is the time which is given by the user. I will now create the event "Akira Visit" is created at 20:00-20:30 on 23 July 2024. ',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The event "Akira Visit" is created at 20:00-20:30 on 23 July 2024. ',
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
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
                                    "calendar_event_name": "Akira Visit",
                                    "start_datetime_iso": "2024-07-23T20:00",
                                    "end_datetime_iso": "2024-07-23T20:30",
                                    "creation_datetime_iso": "2024-07-23T19:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_exact_match_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against the initial snapshot
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_12_cf1c30e7-60f7-43ab-ab92-7a1832013ade_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_12",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T19:40:00-07:00",
            is_read_time="2024-07-23T19:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You need to clean your apartment before Akira comes over, you want to check when the last time he messaged was. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When did I get the last message from my sports nutritionist school friend?",
                },
            ],
            reasoning="The user is asking when a contact last messaged them.\nI should find the named contact in the user's contacts. The user has given me a number of key terms to search for. I can see that multiple people have the 'school friend' tag, however only one of these is saved as being a sports nutritionist, Akira Muramoto.\nNext, I can find their conversation. The last message from Akira Muramoto was received on July 23 2024 at 19:24, which said 'Thanks! It definitely will. Take care, John.'.  I can now confirm the time of this message to the user.",
            success_conditions=[
                {
                    "input_text": "1. Time of last message received from Akira Muramoto which said 'Thanks! It definitely will. Take care, John.' is confirmed as 19:24 on July 23, 2024.",
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
                # Milestone 0 – The agent consults the messaging database
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
                # Milestone 1 – The tool output contained the expected last message from Akira
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
                                                "value": "akira.muramoto@sportsfan.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Take care, John",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-23T19:24:00-07:00",
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
                # Milestone 2 – The agent tells the user the correct date/time
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
                                            "July 23",
                                            "23 July",
                                            "Jul 23",
                                            "2024-07-23",
                                            "today",
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
                (0, 1),  # Message lookup → confirm message found
                (1, 2),  # Confirmed message → inform user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_12_d43fb873-b336-41ae-8bd5-2c93b007eaeb_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_12",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T19:45:00-07:00",
            is_read_time="2024-07-23T19:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You are curious about what time you last sent Akira a text message "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I send that last message to Akira",
                },
            ],
            reasoning="The user wants to know what time they sent the last message to Akira. I will first need to find the user's conversation with Akira. Now that I have found that I can retrieve the time of the most recent message and inform the user ",
            success_conditions=[
                {
                    "input_text": '1. The time of the message sent to Akira Muramoto on July 23, 2024 at 19:26 with the text "See you soon, Akira!" is presented to the user.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
            milestones=[
                # Milestone 0 – The agent looks up the message history
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
                # Milestone 1 – Confirm the correct “See you soon, Akira!” message (19:26) was returned
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
                                                "value": "See you soon, Akira!",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-23T19:26:00-07:00",
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
                # Milestone 2 – The agent tells the user the correct time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Accept either 24-hour or 12-hour mention of 7:26 PM / 19:26
                                    "content": [("19:26", "7:26")],
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
            name="JOHN_QUINN_12_0a2ef96a-ec1a-490d-af9f-04d35071fe4b_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_12",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T19:30:00-07:00",
            is_read_time="2024-07-23T19:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to message Akira to let him know that you can't find the tent you promised to have ready for the evening. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Write a message to my sports nutritionist friend to say I can't find the tent, sorry",
                },
            ],
            reasoning='The user is asking to send a message.\nFirst, I should identify the intended recipient. The user has mentioned a sports nutritionist, looking through their contacts I can see that Akira Muramoto is the only person tagged this way, this must be who the user is referring to.\nNext, I will draft the message as requested.\nA message saying "I can\'t find the tent, sorry" will be sent to Akira Muramoto.',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A message is sent to Akira Muramoto saying \"I can't find the tent, sorry” ",
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
                # Milestone 0 – Agent looks up the contact info (either lists or searches contacts)
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
                # Milestone 1 – Akira Muramoto is found in the search/list output of Milestone 0
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
                                                "value": "Akira Muramoto",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "akira.muramoto@sportsfan.com",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "408-555-0135",
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
                # Milestone 2 – A new message is added addressed to Akira that apologises for not finding the tent
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
                                                "akira.muramoto@sportsfan.com",
                                                "408-555-0135",
                                            )
                                        ]
                                    ],
                                    "content": "can't find the tent",
                                    "creation_datetime_iso": "2024-07-23T19:30:00-07:00",
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
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_12_0a2ef96a-ec1a-490d-af9f-04d35071fe4b_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_12",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T19:30:00-07:00",
            is_read_time="2024-07-23T19:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to message Akira to let him know that you can't find the tent you promised to have ready for the evening. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Message Akira and say I can't find the tent, sorry",
                },
            ],
            reasoning="The user would like to send a message to a contact named Akira, containing the text \"I can't find the tent, sorry\". I'll need to find the named contact via their contact list and or messages, and once I've located the contact in question I can compose the message and seek confirmation to send it.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A message is sent to Akira Muramoto saying \"I can't find the tent, sorry” ",
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
                # Milestone 0 – The agent looks up Akira in contacts
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
                # Milestone 1 – Akira Muramoto’s contact information was found
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
                                                "value": "Akira Muramoto",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "408-555-0135",
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
                            reference_milestone_node_index=0,  # depends on Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – A message was sent to Akira saying the tent can’t be found
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require Akira to be among the participants (other participants like the user are allowed)
                                    "participants_addresses": [
                                        [
                                            (
                                                "408-555-0135",
                                                "akira.muramoto@sportsfan.com",
                                            )
                                        ]
                                    ],
                                    "content": [
                                        ("can't find the tent", "cannot find the tent")
                                    ],
                                    "creation_datetime_iso": "2024-07-23T19:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_str_contains_any_similarity,
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
                (0, 1),  # Contact lookup ⇒ verify Akira found
                (1, 2),  # Akira found  ⇒ message sent
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_12_2d8d619f-ea53-4d77-b9c8-b5dbe978d710_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_12",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T19:35:00-07:00",
            is_read_time="2024-07-23T19:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to send a message to Akira not to come over as something has come up and you will bring the tent to work tomorrow. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Cancel my meet up with Akira Muramoto tonight and tell him to come see me a work tomorrow the 24th of July and he can borrow my tent. ",
                },
            ],
            reasoning="The user wants to message back to Akira Muramoto that he no longer wishes to have Akira come over this evening and would prefer a meeting tomorrow the 24th that would be a preferable time to collect the tent that user has agreed to lend to Akira Muramoto. \n\nI will message back Akira Muramoto at akira.muramoto@sportsfan.com that user would prefer that the tent be collected at his place of employment on the 24th of July rather this evening.",
            success_conditions=[
                {
                    "input_text": "1. Send a message to Akira Muramoto not to come over tonight and that I will bring the tent in to work and he can collect it there. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up Akira’s contact information
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
                # Milestone 1 – Confirm Akira Muramoto’s contact appeared in the previous lookup
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
                                                "value": "Akira Muramoto",
                                                "partial": False,
                                            },
                                            "email": {
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
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
                # Milestone 2 – A new outgoing message to Akira cancelling tonight and arranging tomorrow
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
                                                "408-555-0135",
                                                "akira.muramoto@sportsfan.com",
                                            )
                                        ]
                                    ],
                                    "content": "tent",
                                    "creation_datetime_iso": "2024-07-23T19:35:00-07:00",
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
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup -> Confirm Akira found
                (1, 2),  # Akira found -> Send cancellation message
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_12_cf1c30e7-60f7-43ab-ab92-7a1832013ade_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_12",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T19:40:00-07:00",
            is_read_time="2024-07-23T19:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You need to clean your apartment before Akira comes over, you want to check when the last time he messaged was. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did Akira last text me?",
                },
            ],
            reasoning="The user is asking when a contact last messaged them.\nI should find the named contact in the user's contacts. I can see Akira Muramoto is present in the user's contacts list. \nNext, I can find their conversation. The last message from Akira Muramoto was received on July 23, 2024 at 19:24 which said 'Thanks! It definitely will. Take care, John.'.  I can now confirm the time of this message to the user.",
            success_conditions=[
                {
                    "input_text": "1. Time of last message received from Akira Muramoto which said 'Thanks! It definitely will. Take care, John.' is confirmed as 19:24 on July 23, 2024.",
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
                # Milestone 0 – Agent invokes a message-retrieval tool to look for Akira’s last text
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
                # Milestone 1 – Confirm the expected message from Akira was returned by the tool in Milestone 0
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
                                                "value": "Thanks! It definitely will. Take care, John.",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-23T19:24:00-07:00",
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
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – Agent tells the user the correct time of Akira’s last text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("19:24", "7:24")],
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
            name="JOHN_QUINN_12_20ba6332-6627-474e-bf9a-16b3564bcaf4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_12",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T19:30:00-07:00",
            is_read_time="2024-07-23T19:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "Akira is coming to pick up the tent tonight. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Mark the calendar that Akira is visiting at 8 tonight. ",
                },
            ],
            reasoning='Ok so the user is looking to mark the calendar that Akira is visiting at 8 tonight. First I will create a name for the event which I will keep clear and to the point. "Akira Visit" seems suitable. Next is the time which is mostly given by the user. I will set it to the default duration of half an hour. I will now create the event "Akira Visit" is created at 20:00-20:30 on 23 July 2024. ',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The event "Akira Visit" is created at 20:00-20:30 on 23 July 2024. ',
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
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
                                    "calendar_event_name": "Akira",  # verify the event name references Akira
                                    "start_datetime_iso": "2024-07-23T20:00:00-07:00",
                                    "end_datetime_iso": "2024-07-23T20:30:00-07:00",
                                    "creation_datetime_iso": "2024-07-23T19:30:00-07:00",
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
                            reference_milestone_node_index=-1,
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_12_cab8f57e-a12e-4a21-b9ad-7b361c0f0677_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_12",
                "contact",
                "email",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T19:30:00-07:00",
            is_read_time="2024-07-23T19:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You need to send an email to school friend Akira Muramoto because you forgot you had a previous engagement. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send my Soylent Green friend the following email: \nHey, I know you said to come on over to pick up the tent and give me the supplement and all, but i remembered I have to go out now, so I won't be here. I'll leave the tent with my next door neighbor Deborah. Her place is the one with the ugly autumnal wreath on the door. You can leave the Soylent Green with her too. -John",
                },
            ],
            reasoning="User John Quinn has provided the contents of an email to be sent to someone referred to only as their 'Soylent Green friend'. To find who that is, I search the messages for 'Soylent' and find a recent chat with Akira Muramoto about Green by Soylent, so the 'Soylent Green friend' is Akira Muramoto. I shall draft and address the email to akira.muramoto@sportsfan.com and show it to the user for approval. ",
            success_conditions=[
                {
                    "input_text": "An email is sent to Akira Muramoto at akira.muramoto@sportsfan.com.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The email is to state: Hey, I know you said to come on over to pick up the tent and give me the supplement and all, but i remembered I have to go out now, so I won't be here. I'll leave the tent with my next door neighbor Deborah. Her place is the one with the ugly autumnal wreath on the door. You can leave the Soylent Green with her too. -John",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_email",
            ],
            milestones=[
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["akira.muramoto@sportsfan.com"]
                                    ],
                                    "status": "sent",
                                    # Only a key fragment of the body is required.
                                    "body": "pick up the tent",
                                    "creation_datetime_iso": "2024-07-23T19:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "body": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_12_5c8beb79-8df8-476b-b256-d447a0aabb27_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_12",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T19:15:00-07:00",
            is_read_time="2024-07-23T19:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to add an event to calendar for tonight to remind you that Akira is calling over. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Can you create an event between 8 and 11 called "Akira coming over" tonight? ',
                },
            ],
            reasoning="The user wants to create a new event and has provided all the details I need to do so. I will check the user's calendar for availability. The user's calendar is free for the time range they provided. I will add the event. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A new event is created for July 23, 2024 called "Akira coming over" between 20:00 - 23:00.',
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "get_all_contacts",
                "search_contacts",
                "create_calendar_event",
            ],
            milestones=[
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Akira coming over",
                                    "start_datetime_iso": "2024-07-23T20:00:00",
                                    "end_datetime_iso": "2024-07-23T23:00:00",
                                    "creation_datetime_iso": "2024-07-23T19:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_exact_match_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="JOHN_QUINN_12_b1828c69-7cae-473d-9c16-69826b453410_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_12",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T15:00:00-07:00",
            is_read_time="2024-07-24T15:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want a reminder of the name of the supplement Akira mentioned to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What supplement did my friend message me about yesterday?",
                },
            ],
            reasoning="The user wants to know what supplement their friend messaged them about yesterday. Looking through the user's contacts they have multiple people notes as their friends. I'll see if I can find any mention of a supplement in the user's messages. I found a message from Akira Muramoto about a supplement. I can assume this is the friend the user was referring to. I'll inform the user the name of the supplement is 'Green' by Soylent ",
            success_conditions=[
                {
                    "input_text": "1. Akira Muramoto's message containing the name of a supplement is summarised ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 — The agent looked through messages (information-retrieval tool call)
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
                # Milestone 1 — Confirm that the message mentioning the supplement “Green” was returned
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
                                            # We only need to know that some returned message contains “Green”
                                            "content": {
                                                "value": "Green",
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
                # Milestone 2 — The agent tells the user the supplement name (“Green” by Soylent)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("Green", "Green by Soylent")],
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
            name="JOHN_QUINN_12_a64042fa-3287-4f6f-a563-0baf0f1b97fb_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_12",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T19:00:00-07:00",
            is_read_time="2024-07-23T19:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know what Akira's message says but you cannot look at your phone right now. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What did my school friend say?",
                },
            ],
            reasoning='The user wants to know what their "school bro" said. I wonder who that is. I should check their contacts to find out. I see the user has one male contact, listed as a school friend, called Akira Muramoto. I assume the user means him. I will now check for messages from Akira Muramoto. Okay, the user received a message from Akira Muramoto just now at 19:00, July 23rd 2024. I\'ll tell them the content of the message now. ',
            success_conditions=[
                {
                    "input_text": "1. The message received from Akira Muramato on July 23rd, 2024, at 19:00 is read to the user. ",
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
                # Milestone 0 – Agent tries to locate "school friend" messages
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
                # Milestone 1 – Confirm that Akira’s 19:00 message was among the retrieved results
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
                                                "value": "akira.muramoto@sportsfan.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Green",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-23T19:00:00-07:00",
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
                # Milestone 2 – Agent relays Akira’s message content to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "supplement called 'Green'",
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
                (0, 1),  # Message search → verify Akira’s message found
                (1, 2),  # After confirming the message, relay it to the user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_12_a64042fa-3287-4f6f-a563-0baf0f1b97fb_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_12",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T19:00:00-07:00",
            is_read_time="2024-07-23T19:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know what Akira's message says but you cannot look at your phone right now. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What did Akira say?",
                },
            ],
            reasoning="The user wants to know what Akira said. I wonder who Akira is. I should check their contacts to find out. I see the user has one contact called Akira, Akira Muramoto. It must be him. I will now check for messages from Akira Muramoto. Okay, the user received a message from Akira Muramoto just now at 19:00, July 23rd 2024. I'll tell them the content of the message now. ",
            success_conditions=[
                {
                    "input_text": "1. The message received from Akira Muramato on July 23rd, 2024, at 19:00 is read to the user. ",
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
                # Milestone 0 – Agent tries to retrieve the user’s recent messages
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
                # Milestone 1 – The retrieved result includes Akira’s 19:00 message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            # parse the tool outcome captured in Milestone 0
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "sender_address": {
                                                "value": "akira.muramoto@sportsfan.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-23T19:00:00-07:00",
                                                "partial": False,
                                            },
                                            # confirm we found the actual message text
                                            "content": {
                                                "value": "Green",
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
                        ),
                    ],
                ),
                # Milestone 2 – Agent tells the user what Akira said (mentions the supplement “Green” / Soylent)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("Green", "Soylent")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_12_9019e655-4bce-4f22-8b66-3de97c009504_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_12",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T18:35:00-07:00",
            is_read_time="2024-07-26T18:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "The supplement Akira gave you to try has not agreed with you and you want to let him know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a message saying  "Hey just letting you know that supplement has really messed with my gut so be careful." to the sports nutritionist. ',
                },
            ],
            reasoning="The user wants to send a message to the sports nutritionist. First I need to figure out who the sports nutritionist is. I should check the user's Contacts. \n\nHmm, I don't see a contact with that name but Akira Muramoto has his job as sports nutritionist so this must be who the user means. \n\nI will draft a message to Akira, using the content the user has already provided. Lastly I will present the draft to the user for their approval before I send it. ",
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Akira Muramoto reading "Hey just letting you know that supplement has really messed with my gut so be careful."',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 ― the agent looks up the sports-nutritionist contact
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
                # Milestone 1 ― Akira Muramoto is returned from the contact search in Milestone 0
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
                                                "value": "Akira Muramoto",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "408-555-0135",
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
                                    "content": "{matched}",  # will be replaced by extractor
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                        )
                    ],
                ),
                # Milestone 2 ― a message is sent to Akira warning about the supplement
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
                                                "408-555-0135",
                                                "akira.muramoto@sportsfan.com",
                                            )
                                        ]
                                    ],
                                    "content": "gut",  # we will match substring below,
                                    "creation_datetime_iso": "2024-07-26T18:35:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,  # ensure the body references gut issues,
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
            name="JOHN_QUINN_12_0da92c79-bbe9-4fdf-a86a-751ffc44b9c8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_12",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T19:35:00-07:00",
            is_read_time="2024-07-23T19:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to ask if Akira needs to borrow any other equipment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a message reply to Akira Muramoto saying "Hey do you want a sleeping bag to go along with the tent?"',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Akira Muramoto.\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": "1. A reply message is sent to Akira Muramoto asking if he wants to borrow a sleeping bag too.",
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
                # Milestone 0 – Agent looks up Akira’s contact information
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
                # Milestone 1 – The returned contact list includes Akira Muramoto
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
                                                "value": "Akira Muramoto",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "408-555-0135",
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
                # Milestone 2 – A new outgoing message is sent to Akira asking about a sleeping bag
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require that Akira is one of the participants (match by phone or email)
                                    "participants_addresses": [
                                        [
                                            (
                                                "408-555-0135",
                                                "akira.muramoto@sportsfan.com",
                                            )
                                        ]
                                    ],
                                    # Ensure the content mentions “sleeping bag”
                                    "content": "sleeping bag",
                                    "creation_datetime_iso": "2024-07-23T19:35:00-07:00",
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
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact search ➜ verify Akira found
                (1, 2),  # Akira found ➜ message sent
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_12_9019e655-4bce-4f22-8b66-3de97c009504_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_12",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T18:35:00-07:00",
            is_read_time="2024-07-26T18:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "The supplement Akira gave you to try has not agreed with you and you want to let him know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Text Akira to say "Hey just letting you know that supplement has really messed with my gut so be careful."',
                },
            ],
            reasoning="The user wants to text Akira. First I need to figure out who Akira is. I should check the user's Contacts. \n\nHmm, looks like there is only one Akira in the user's Contacts, Akira Muramoto, so this must be who the user means. \n\nNext I will draft a message to Akira, using the content the user has provided. \n\nFinally I will present the draft to the user for approval before sending it. ",
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Akira Muramoto reading "Hey just letting you know that supplement has really messed with my gut so be careful."',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up Akira in contacts
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
                # Milestone 1 – Akira Muramoto is found in the tool result from Milestone 0
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
                                                "value": "Akira Muramoto",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "408-555-0135",
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
                # Milestone 2 – Message is sent to Akira with the correct warning text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # One participant: Akira – match by phone or email, no extras allowed
                                    "participants_addresses": [
                                        [
                                            (
                                                "408-555-0135",
                                                "akira.muramoto@sportsfan.com",
                                            )
                                        ]
                                    ],
                                    "content": "Hey just letting you know that supplement has really messed with my gut so be careful",
                                    "creation_datetime_iso": "2024-07-26T18:35:00-07:00",
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
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox chatter
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → confirm Akira found
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_12_06637516-443d-4ce0-87cc-427581867aca_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_12",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T21:40:00-07:00",
            is_read_time="2024-07-23T21:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to see the last message you sent to Akira. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the last message I sent to my friend who is a sports nutritionist.",
                },
            ],
            reasoning="The user wants to see the last message they sent to their friend who is a sports nutritionist. Let me look in Contacts to see who this is. It is Akira Muramoto.  Let me look for their messages. Okay I have found the conversation. I will show the user the last message they sent.",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last message they sent to Akira Muramoto on July 23rd at 19:26 with the text 'See you soon, Akira!'",
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
                # Milestone 0 – The agent tries to identify the “sports nutritionist” contact
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
                # Milestone 1 – Akira Muramoto (Sports Nutritionist) is found in the previous contact-search result
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
                                                "value": "Akira Muramoto",
                                                "partial": False,
                                            },
                                            "job_title": {
                                                "value": "Sports Nutritionist",
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
                # Milestone 2 – The agent searches the message database
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
                # Milestone 3 – The expected last-sent message to Akira is present in the previous search result
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
                                                "value": "See you soon, Akira!",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "john.quinn@palantir.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-23T19:26:00-07:00",
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
                # Milestone 4 – The agent shows the user the correct last message text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "See you soon, Akira!",
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
                (0, 1),  # contact search → confirm Akira
                (2, 3),  # message search → confirm correct message
                (3, 4),  # once message is confirmed, it should be shown to the user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_12_06637516-443d-4ce0-87cc-427581867aca_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_12",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T21:40:00-07:00",
            is_read_time="2024-07-23T21:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to see the last message you sent to Akira. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the last message I sent to Akira Muramoto.",
                },
            ],
            reasoning="The user wants to see the last message they sent to Akira Muramoto. Let me look for their messages. Okay I have found the conversation. I will show the user the last message they sent.",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last message they sent to Akira Muramoto on July 23rd at 19:26 with the text 'See you soon, Akira!'",
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
                # Milestone 0 – Agent uses a message-retrieval tool
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
                # Milestone 1 – Returned tool output includes the expected last message
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
                                                "value": "See you soon, Akira!",
                                                "partial": False,
                                            },
                                            "participants_addresses": {
                                                "value": "akira.muramoto@sportsfan.com",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-23T19:26:00-07:00",
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
                # Milestone 2 – Agent shows the user the correct last message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "See you soon, Akira!",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
    ]
