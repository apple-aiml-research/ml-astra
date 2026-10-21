# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
# Auto-generated scenario extensions
from functools import partial
from typing import Optional, cast

import polars as pl

from astra_tool_sandbox.common.evaluation import (
    Milestone,
    Minefield,
    SnapshotConstraint,
    addition_similarity,
    column_contains_similarity,
    column_datetime_window_similarity,
    column_exact_match_similarity,
    column_list_exact_match_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_similarity,
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


def get_TAG_THEO_APPLESEED_pilot_plot_26(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="THEO_APPLESEED_26_aa8816c4-5cb3-4c98-a8ae-04019fbf8d32_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T11:00:00-07:00",
            is_read_time="2024-07-29T11:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to get rid of and block all the recent annoying spams from your message inbox. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want you to delete those annoying messages and can you block the senders? Yes or No.",
                },
            ],
            reasoning="The user wants me to delete those annoying messages and ask if I can block the senders. I first need to understand what are the annoying messages. I will search the user's messages and emails for these. User has received a large amount of spam messages in regards to cryptocurrency and would like to set up blocking and filters. \n\nI will ask the user permission and then delete these messages. Also the user want to block the senders, but after searching the available tools, there're no related tools. I will reply \"No\" to them as I cannot perform the ask due to lack of tools ",
            success_conditions=[
                {
                    "input_text": "1. Crypto spam has been deleted from incoming messages. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. User has been informed with 'No' as there's no related blocking tools for senders. ",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "remove_message_or_conversation",
                "search_messages",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – The agent tries to discover the spam messages
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
                # Milestone 1 – All eight crypto-spam conversations have been removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": [
                                        "unknown1@crypto-invest.com",
                                        "offers@blockchainbuzz.net",
                                        "info@cryptogains.io",
                                        "promo@digitalcoins.com",
                                        "contact@futurecrypto.net",
                                        "deals@coinrealm.org",
                                        "hello@investcrypto.today",
                                        "team@cryptonow.com",
                                    ]
                                }
                            ),
                            # default exact-match on conversation_name is sufficient
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        ),
                    ],
                ),
                # Milestone 2: Check that the user is informed with No
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
                                "content": column_word_contains_similarity,
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Must first inspect messages, then delete them
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_869b440e-6c90-483d-93b2-3b290eaff753_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:25:00-07:00",
            is_read_time="2024-07-22T14:25:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to delete the spam message from Blockchain Buzz "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Get rid of the spam from Blockchain.",
                },
            ],
            reasoning="The user wants to get rid of the spam from Blockchain. I'm not sure if they mean spam email, spam message, or some other type of spam, so I'll take a look through their info.\n\nI didn't find a contact named Blockchain, but I did find a message from Blockchain Buzz received at 10:20 on 2024-07-22 that reads \"Theo, don't miss out on the next big wave in blockchain technology. Invest today at www.blockchainbuzz.net/offer\". I conclude that this is the entity in question.\n\nSince the user wants to get rid of the spam, I will delete this message and let the user know.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. Message received at 10:20 on 2024-07-22 from Blockchain Buzz that reads "Theo, don\'t miss out on the next big wave in blockchain technology. Invest today at www.blockchainbuzz.net/offer" is deleted.',
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "remove_message_or_conversation",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks up messages to locate the spam
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": [RoleType.EXECUTION_ENVIRONMENT],
                                    "recipient": [RoleType.AGENT],
                                    "tool_trace": [""],
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
                # Milestone 1 – Verify the spam message from Blockchain Buzz was actually retrieved
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
                                                "value": "offers@blockchainbuzz.net",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-22T10:20:00-07:00",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Theo, don't miss out on the next big wave in blockchain technology. Invest today at www.blockchainbuzz.net/offer",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": [RoleType.EXECUTION_ENVIRONMENT],
                                    "recipient": [RoleType.AGENT],
                                    "content": ["{matched}"],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
                # Milestone 2 – Confirm the spam message has been removed from the MESSAGING database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender_address": ["offers@blockchainbuzz.net"],
                                    "creation_datetime_iso": [
                                        "2024-07-22T10:20:00-07:00"
                                    ],
                                    "content": [
                                        "Theo, don't miss out on the next big wave in blockchain technology. Invest today at www.blockchainbuzz.net/offer"
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieved message after searching
                (1, 2),  # Deleted the located spam message
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_d8890c0b-93e5-4f7f-a827-211967cadeb5_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:45:00-07:00",
            is_read_time="2024-07-29T10:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to view the crypto message you received yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you show me that crypto message I got yesterday please?",
                },
            ],
            reasoning='The user wants to view "that crypto message i got yesterday". I will explore the messages the user received and I see there are 8 different messages related to cryptocurrencies from three different senders. However, I see the dates the messages were received are different, ranging from the dates July 21, 2024 to July 28, 2024. The user wants to see the messages received yesterday. As the user is requesting this on July 29, 2024 - 10:45, I will only take into account messages sent the day before, that is, July 28, 2024. Out of the different messages, there is only one sent on July 28. The sender of this message is Crypto Now. The user must be referring to this message, so I will show it to them. \n',
            success_conditions=[
                {
                    "input_text": '1. The message received from "team@cryptonow.com" at 13:25:00 on July 28th, 2024, is presented to the user.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – Agent looks through the messages database
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
                # Milestone 1 – Confirm the July 28 2024 crypto-now message was returned
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
                                                "value": "team@cryptonow.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-28T13:25:00-07:00",
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
                                    "content": [
                                        (
                                            "Don't miss your chance",
                                            "www.cryptonow.com",
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
            name="THEO_APPLESEED_26_147dfe59-d3c8-43af-bcfa-b466602e0c11_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T16:50:00-07:00",
            is_read_time="2024-07-23T16:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to delete all the spam crypto messages   that you received. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Remove my spam messages.",
                },
            ],
            reasoning="Okay so, the user wants to remove their spam messages. I can see in their messages that they have three messages from unknown senders. These messages contain content about crypto. I can confirm with the user that they wish to delete the messages from 'unknown1@crypto-invest.com', 'offers@blockchainbuzz.net' and 'info@cryptogains.io' and then delete them.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. The message received from 'unknown1@crypto-invest.com' on the 21st July 2024 at 14:35 saying 'Unlock the potential of your future with our exclusive cryptocurrency investment opportunities! Visit now: www.crypto-invest.com/start' is deleted.",
                },
                {
                    "input_text": "2. The message received from 'offers@blockchainbuzz.net' on the 22nd July 2024 at 10:20 saying 'Theo, don't miss out on the next big wave in blockchain technology. Invest today at www.blockchainbuzz.net/offer' is deleted.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The message received from 'info@cryptogains.io' on the 23rd July 2024 at 16:45 saying 'See how you can multiply your investment in just a few months! Visit www.cryptogains.io for more information.' is deleted.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "remove_message_or_conversation",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent consults message list (information-retrieval prerequisite)
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
                # Milestone 1 – Spam message from unknown1@crypto-invest.com removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender_address": "unknown1@crypto-invest.com",
                                    "content": "Unlock the potential",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                            reference_milestone_node_index=-1,  # compare with original snapshot
                        )
                    ]
                ),
                # Milestone 2 – Spam message from offers@blockchainbuzz.net removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender_address": "offers@blockchainbuzz.net",
                                    "content": "don't miss out",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
                # Milestone 3 – Spam message from info@cryptogains.io removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender_address": "info@cryptogains.io",
                                    "content": "multiply your investment",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_fa291a37-fbc0-433b-a496-d70fd7f9fad2_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:05:00-07:00",
            is_read_time="2024-07-29T10:05:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to delete the crypto message you received yesterday "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the message I received from team@cryptonow.com",
                },
            ],
            reasoning="The user wants to delete the message they received from team@cryptonow.com. Looking through the user's messages I can see they received a message from team@cryptonow.com yesterday. I will delete this message fro the user now.",
            success_conditions=[
                {
                    "input_text": "1. The message from team@cryptonow.com is deleted",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "remove_message_or_conversation",
            ],
            milestones=[
                # Milestone 0 – Agent looks for the spam message
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
                # Milestone 1 – The specific message from team@cryptonow.com is found
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
                                                "value": "team@cryptonow.com",
                                                "partial": False,
                                            },
                                            # Only require that crypto‐related text is present in the body
                                            "content": {
                                                "value": "crypto",
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
                            reference_milestone_node_index=0,  # depend on the tool output in Milestone 0
                        ),
                    ],
                ),
                # Milestone 2 – Message is removed from the database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender_address": "team@cryptonow.com",
                                    "content": "Don't miss your chance",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Search → verify retrieval
                (1, 2),  # Retrieval → verify deletion
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_fa291a37-fbc0-433b-a496-d70fd7f9fad2_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:05:00-07:00",
            is_read_time="2024-07-29T10:05:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to delete the crypto message you received yesterday "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the message I received from the crypto website",
                },
            ],
            reasoning="The user wants to delete the message they received from the crypto website. Looking through the user's messages I can see they received messages from multiple crypto websites so I will ask the user to clarify which message they are referring to. The user wants to deleted the message from team@cryptonow.com so I will do this now",
            success_conditions=[
                {
                    "input_text": "1. The message from team@cryptonow.com is deleted",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "remove_message_or_conversation",
            ],
            milestones=[
                # Milestone 0 – Agent looks up messages to locate the crypto spam
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
                # Milestone 1 – The specific message from team@cryptonow.com has been removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "team@cryptonow.com",
                                    "sender_address": "team@cryptonow.com",
                                    "creation_datetime_iso": "2024-07-28T13:25:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieval precedes deletion
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_147dfe59-d3c8-43af-bcfa-b466602e0c11_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T16:50:00-07:00",
            is_read_time="2024-07-23T16:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to delete all the spam crypto messages   that you received. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete all the messages I've received about crypto.",
                },
            ],
            reasoning="Right, the user wants me to delete messages about 'crypto'. I can see that there are three messages received from 'unknown1@crypto-invest.com', 'offers@blockchainbuzz.net' and 'info@cryptogains.io' all containing content about crypto. I can confirm with the user that these are the messages they would like to delete and then delete them.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. The message received from 'unknown1@crypto-invest.com' on the 21st July 2024 at 14:35 saying 'Unlock the potential of your future with our exclusive cryptocurrency investment opportunities! Visit now: www.crypto-invest.com/start' is deleted.",
                },
                {
                    "input_text": "2. The message received from 'offers@blockchainbuzz.net' on the 22nd July 2024 at 10:20 saying 'Theo, don't miss out on the next big wave in blockchain technology. Invest today at www.blockchainbuzz.net/offer' is deleted.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The message received from 'info@cryptogains.io' on the 23rd July 2024 at 16:45 saying 'See how you can multiply your investment in just a few months! Visit www.cryptogains.io for more information.' is deleted.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "remove_message_or_conversation",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent retrieves messages (either via search_messages or get_all_messages)
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
                # Milestone 1 – Message from unknown1@crypto-invest.com on 2024-07-21 removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "unknown1@crypto-invest.com",
                                    "creation_datetime_iso": "2024-07-21T14:35:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
                # Milestone 2 – Message from offers@blockchainbuzz.net on 2024-07-22 removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "offers@blockchainbuzz.net",
                                    "creation_datetime_iso": "2024-07-22T10:20:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
                # Milestone 3 – Message from info@cryptogains.io on 2024-07-23 removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "info@cryptogains.io",
                                    "creation_datetime_iso": "2024-07-23T16:45:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_7f70cab7-c917-468c-99cd-9e171fc6721b_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-28T13:25:00-07:00",
            is_read_time="2024-07-28T13:25:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know who the sender of the first crypto text you got was. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who was the sender of the first crypto text I got? ",
                },
            ],
            reasoning='The user wants to know who was the sender of the first crypto text they got was. Okay, I start off by searching messages for messages mentioning "crypto" and I find multiple matches. I see that the earliest message was received on July 21st at 14:35 from Cypto Invest. I\'ll show the user the message with its sender. ',
            success_conditions=[
                {
                    "input_text": "1. The sender of that message received on July 21st at 14:35 is checked and given to the user as Crypto Invest (unknown1@crypto-invest.com).",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – The agent queries the message store for crypto-related messages
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
                # Milestone 1 – Confirm the July 21 2024 14:35 message from unknown1@crypto-invest.com was returned
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
                                                "value": "unknown1@crypto-invest.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-21T14:35:00-07:00",
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
                            reference_milestone_node_index=0,  # validate result of Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – The agent tells the user the sender was “Crypto Invest” (or gives the exact address)
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
                                            "Crypto Invest",
                                            "unknown1@crypto-invest.com",
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
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_d8890c0b-93e5-4f7f-a827-211967cadeb5_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:45:00-07:00",
            is_read_time="2024-07-29T10:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to view the crypto message you received yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me crypto message i got yesterday. ",
                },
            ],
            reasoning="The user wants me to show them the crypto message they got yesterday. I will explore the messages the user received and I see there are 8 different messages related to cryptocurrencies from three different senders. However, I see the dates the messages were received are different, ranging from the dates July 21, 2024 to July 28, 2024. The user wants to see the messages received yesterday. As the user is requesting this on July 29, 2024 - 10:45, I will only take into account messages sent the day before, that is, July 28, 2024. Out of the different messages, there is only one sent on July 28. The sender of this message is Crypto Now. The user must be referring to this message, so I will show it to them. \n",
            success_conditions=[
                {
                    "input_text": '1. The message received from "team@cryptonow.com" at 13:25:00 on July 28th, 2024, is presented to the user.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
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
                # Milestone 1 – The returned tool output contains the 28-Jul-2024 message from team@cryptonow.com
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
                                                "value": "team@cryptonow.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-28T13:25:00-07:00",
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
                # Milestone 2 – Agent’s reply to the user includes the key content of that message
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
                                            "Don't miss your chance",
                                            "www.cryptonow.com",
                                            "team@cryptonow.com",
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
                (0, 1),  # Retrieval → confirm correct message in results
                (1, 2),  # Confirmation → user-facing presentation
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_869b440e-6c90-483d-93b2-3b290eaff753_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:25:00-07:00",
            is_read_time="2024-07-22T14:25:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to delete the spam message from Blockchain Buzz "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Blockchain Buzz message delete.",
                },
            ],
            reasoning="The user wants to delete Blockchain Buzz message. I can't find any contact called Blockchain Buzz, so I'll check the user's messages.\n\nI found a message from offers@blockchainbuzz.net at 10:20 on 2024-07-22 that reads \"Theo, don't miss out on the next big wave in blockchain technology. Invest today at www.blockchainbuzz.net/offer\". This must be the message the user mentioned, so I'll delete it and inform the user.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. Message received at 10:20 on 2024-07-22 from Blockchain Buzz that reads "Theo, don\'t miss out on the next big wave in blockchain technology. Invest today at www.blockchainbuzz.net/offer" is deleted.',
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "remove_message_or_conversation",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks up messages to locate the spam from Blockchain Buzz
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
                # Milestone 1 – Confirms the Blockchain Buzz spam message appeared in the tool output
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
                                                "value": "offers@blockchainbuzz.net",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "next big wave in blockchain technology",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-22T10:20:00-07:00",
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
                # Milestone 2 – The spam message has been deleted from the messaging database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "offers@blockchainbuzz.net",
                                    "sender_address": "offers@blockchainbuzz.net",
                                    "content": "Theo, don't miss out on the next big wave in blockchain technology. Invest today at www.blockchainbuzz.net/offer",
                                    "creation_datetime_iso": "2024-07-22T10:20:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "conversation_name": column_exact_match_similarity,
                                "sender_address": column_exact_match_similarity,
                                # Allow flexible matching on body text
                                "content": column_contains_similarity,
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (
                    0,
                    1,
                ),  # Message lookup → verification the correct spam message was found
                (1, 2),  # Verification → deletion confirmed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_aa8816c4-5cb3-4c98-a8ae-04019fbf8d32_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T11:00:00-07:00",
            is_read_time="2024-07-29T11:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to get rid of all the recent crypto spam from your message inbox. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Clear all email and messages in regards to cryptocurrency. ",
                },
            ],
            reasoning="User has received a large amount of spam in regards to cryptocurrency and would like to remove those. \n\n I will search the messages and emails. The cryptocurrency spam is all in the messages; the mailbox holds only ordinary work email, so there is nothing to remove there. I will delete the incoming cryptocurrency messages completely and leave the email untouched. ",
            success_conditions=[
                {
                    "input_text": "1. Crypto spam has been deleted from incoming messages. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. No email is deleted; the mailbox contains no cryptocurrency spam, only ordinary work email.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "remove_message_or_conversation",
                "search_messages",
                "get_all_emails",
                "search_emails",
                "remove_email_or_thread",
            ],
            milestones=[
                # Milestone 0 – Agent investigates the inbox for potential crypto spam
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
                                        "search_emails",
                                        "get_all_emails",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – All identified crypto-related message threads have been removed / cleared
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": [
                                        "unknown1@crypto-invest.com",
                                        "offers@blockchainbuzz.net",
                                        "info@cryptogains.io",
                                        "promo@digitalcoins.com",
                                        "contact@futurecrypto.net",
                                        "deals@coinrealm.org",
                                        "hello@investcrypto.today",
                                        "team@cryptonow.com",
                                    ]
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Information retrieval → deletion of spam threads
            ],
            minefields=[
                # There is no crypto spam in the mailbox, so the agent must not delete any email
                Minefield(
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
                                    target_tools=["remove_email_or_thread"],
                                )
                            },
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_536e5e0f-6da3-4984-b25c-23fc97fbc6f0_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:05:00-07:00",
            is_read_time="2024-07-29T10:05:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to delete all of the spam you've received lately "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me all the messages about crypto or blockchain and delete them",
                },
            ],
            reasoning="The user is asking me to delete messages.\nFirst, I will perform a search with the key terms prompted. \nI have found eight messages matching this search. I can see no other potential messages. \nMessages from unknown1@crypto-invest.com, offers@blockchainbuzz.net, info@cryptogains.io, promo@digitalcoins.com, promo@digitalcoins.com, contact@futurecrypto.net, deals@coinrealm.org, hello@investcrypto.today, team@crypto.now will be deleted.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. All recent messages referring to "crypto" or "blockchain" are deleted',
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "remove_message_or_conversation",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks up messages (either via search or full listing)
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
                # Milestone 1 – All crypto / blockchain spam messages have been removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": [
                                        "unknown1@crypto-invest.com",
                                        "offers@blockchainbuzz.net",
                                        "info@cryptogains.io",
                                        "promo@digitalcoins.com",
                                        "contact@futurecrypto.net",
                                        "deals@coinrealm.org",
                                        "hello@investcrypto.today",
                                        "team@cryptonow.com",
                                    ]
                                }
                            ),
                            column_similarity_measure={
                                "conversation_name": column_exact_match_similarity,
                            },
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieval precedes deletion verification
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_536e5e0f-6da3-4984-b25c-23fc97fbc6f0_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:05:00-07:00",
            is_read_time="2024-07-29T10:05:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to delete all of the spam you've received lately "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete all the spam messages.",
                },
            ],
            reasoning="The user is asking me to delete messages.\nFirst, I will perform a search of the user's message conversations. I can identify spam messages by looking for shared key terms, and identifying whether or not the user has interacted with the conversation through replies or reactions.\nI have found eight messages matching this search. I can see no other potential matches. \nMessages from unknown1@crypto-invest.com, offers@blockchainbuzz.net, info@cryptogains.io, promo@digitalcoins.com, promo@digitalcoins.com, contact@futurecrypto.net, deals@coinrealm.org, hello@investcrypto.today, team@crypto.now will be deleted.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. All recent messages referring to "crypto" or "blockchain" are deleted',
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "remove_message_or_conversation",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks for spam messages first
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
                # Milestone 1 – All crypto / blockchain spam messages have been removed
                Milestone(
                    snapshot_constraints=[
                        # Single SnapshotConstraint with all spam conversations to be removed
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": [
                                        "unknown1@crypto-invest.com",
                                        "offers@blockchainbuzz.net",
                                        "info@cryptogains.io",
                                        "promo@digitalcoins.com",
                                        "contact@futurecrypto.net",
                                        "deals@coinrealm.org",
                                        "hello@investcrypto.today",
                                        "team@cryptonow.com",
                                    ]
                                }
                            ),
                            column_similarity_measure={
                                "conversation_name": column_exact_match_similarity
                            },
                            reference_milestone_node_index=-1,
                        ),
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox traces while checking removals
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_68edf8cf-c0f5-4404-a839-c26e8f84f7f1_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:20:00-07:00",
            is_read_time="2024-07-29T10:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You are very frustrated at seeing the amount of spam emails you've received.   You send an email to your manager about it asking if he is having a similar issue. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Will you please email my manager with the message 'Are you also getting a ridiculous amount of emails about crypto scams?'.",
                },
            ],
            reasoning='The user wants me to send an email to his manager. He told me the message content: "Are you also getting a ridiculous amount of emails about crypto scams?", but I need to figure out is who exactly the user\'s "manager" is. I can do this by checking the user\'s contacts and seeing if there is any contact that is listed as "manager". Looking through the contacts, I found "Kevin Chen" who is listed as the user\'s manager.\n\nWith the user\'s confirmation, I will send the email "Are you also getting a ridiculous amount of emails about crypto scams?" to Kevin Chen.',
            success_conditions=[
                {
                    "input_text": "1. An email will be sent saying, 'Are you also getting a ridiculous amount of emails about crypto scams?' to Kevin Chen at 10:20 on July 29th 2024.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_email"],
            milestones=[
                # Milestone 0 – Agent looks up the manager’s (Kevin Chen’s) contact information
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
                # Milestone 1 – Verify Kevin Chen’s contact record was returned from the contact-lookup step
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
                                                "value": "Kevin Chen",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "kevin.chen@example.com",
                                                "partial": False,
                                            },
                                            # Any one of the following proves he is the manager
                                            "relationship": {
                                                "value": "Manager",
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
                # Milestone 2 – An email is actually sent to Kevin Chen containing the requested text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["kevin.chen@example.com"]
                                    ],
                                    "body": "Are you also getting a ridiculous amount of emails about crypto scams?",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-29T10:20:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "body": column_contains_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        ),
                    ],
                    # No need to guard-rail other DBs; only EMAIL change matters here
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → confirm Kevin
                (1, 2),  # Kevin confirmed → email sent
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_1b3d624d-8296-446d-879c-56000f8dc21d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:25:00-07:00",
            is_read_time="2024-07-29T10:25:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to delete all the messages from unknown and suspected spam numbers. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to delete all messages I've received that look like spam or junk or are from suspicious numbers.",
                },
            ],
            reasoning='The user wants to delete all messages that look like spam or junk or are from suspicious numbers.\n\nI search in the user\'s messages and find several from unknown numbers and email addresses which include keywords such as "crypto", "blockchain", "offers" and similar. I can infer that these are the message which the user would like to delete as the keywords are associated with common scams and junk mail.\n\nI will then delete the specified messages.\n',
            success_conditions=[
                {
                    "input_text": "1. All messages from suspected spam numbers are deleted. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "remove_message_or_conversation",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – The agent inspects existing messages (spam detection step)
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
                # Milestone 1 – All spam / unknown-sender message threads have been deleted
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": [
                                        "unknown1@crypto-invest.com",
                                        "offers@blockchainbuzz.net",
                                        "info@cryptogains.io",
                                        "promo@digitalcoins.com",
                                        "contact@futurecrypto.net",
                                        "deals@coinrealm.org",
                                        "hello@investcrypto.today",
                                        "team@cryptonow.com",
                                    ]
                                }
                            ),
                            column_similarity_measure={
                                "conversation_name": column_exact_match_similarity
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox chatter when checking DB state change
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_db2ec738-91b6-4799-a845-90cb6e2bcbe3_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T17:40:00-07:00",
            is_read_time="2024-07-23T17:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to ring Lucas Garcia to arrange a gym session.    So you ask what his phone number is "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What is Lucas Garcia's number?",
                },
            ],
            reasoning="The user is looking for Lucas Garcia's number. I should check the user's contacts. Lucas's number is 1234-5678-9110 so I will tell the user this.",
            success_conditions=[
                {
                    "input_text": "1. Contacts is checked for the phone number of Lucas Garcia. ",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. 1234-5678-9110 returned to the user",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=["get_all_contacts", "search_contacts"],
            milestones=[
                # Milestone 0 – Agent queries the contacts database
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
                # Milestone 1 – Tool output contains Lucas Garcia with the correct number
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
                                                "value": "Lucas Garcia",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9110",
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
                # Milestone 2 – Agent tells the user Lucas Garcia's phone number
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "1234-5678-9110",
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
                (0, 1),  # Must first query contacts then confirm Lucas info
                (1, 2),  # After confirming, agent replies to user
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_db2ec738-91b6-4799-a845-90cb6e2bcbe3_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T17:40:00-07:00",
            is_read_time="2024-07-23T17:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to ring Lucas Garcia to arrange a gym session.    So you ask what his phone number is "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What is my gym buddy's number?",
                },
            ],
            reasoning="The user is looking for their gym buddy's number. Looking in their Contacts I can't see one named gym buddy but from the user's relationships I see Lucas Garcia has gym buddy as his relationship iso this must be who the user means. I will tell the user Lucas' number is 1234-5678-9110.",
            success_conditions=[
                {
                    "input_text": "1. Contacts is checked for the phone number of Lucas Garcia. ",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. 1234-5678-9110 returned to the user",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=["get_all_contacts", "search_contacts"],
            milestones=[
                # Milestone 0 – Verify the agent invoked a contact-retrieval tool
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
                # Milestone 1 – Confirm Lucas Garcia (with correct phone number) was included in the tool’s results
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
                                                "value": "Lucas Garcia",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9110",
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
                # Milestone 2 – Verify the agent provided the phone number to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "1234-5678-9110",
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
                (0, 1),  # Tool call → verify Lucas retrieved
                (1, 2),  # Lucas retrieved → user informed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_7bbb2f73-939d-4ca8-8be2-2ce635d3929a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:05:00-07:00",
            is_read_time="2024-07-29T10:05:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        'You want to delete messages that related to the words "crypto" and "blockchain" '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Remove all spam messages that related to crypto or blockchain.",
                },
            ],
            reasoning="Looks like the user wants to remove all messages related to crypto or blockchain. There looks to be eight messages that fit the description. I shall remove them per the users wishes.",
            success_conditions=[
                {
                    "input_text": 'A message from "Crypto Invest" is deleted',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": 'A message from "Blockchain Buzz" is deleted',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": 'A message from "Crypto Gains" is deleted',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": 'A message from "Digital Coins" is deleted',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": 'A message from "Future Crypto" is deleted',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": 'A message from "Coin Realm" is deleted',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": 'A message from "Invest Crypto" is deleted',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": 'A message from "Crypto Now" is deleted',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "remove_message_or_conversation",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks up messages (either via search or full listing)
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
                # Milestone 1 – All eight crypto / blockchain spam messages have been removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender_address": [
                                        "unknown1@crypto-invest.com",
                                        "offers@blockchainbuzz.net",
                                        "info@cryptogains.io",
                                        "promo@digitalcoins.com",
                                        "contact@futurecrypto.net",
                                        "deals@coinrealm.org",
                                        "hello@investcrypto.today",
                                        "team@cryptonow.com",
                                    ],
                                    "conversation_name": [
                                        "unknown1@crypto-invest.com",
                                        "offers@blockchainbuzz.net",
                                        "info@cryptogains.io",
                                        "promo@digitalcoins.com",
                                        "contact@futurecrypto.net",
                                        "deals@coinrealm.org",
                                        "hello@investcrypto.today",
                                        "team@cryptonow.com",
                                    ],
                                }
                            ),
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
            name="THEO_APPLESEED_26_98c2aca4-5478-4f88-a8e7-b441a7039ce4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:20:00-07:00",
            is_read_time="2024-07-29T10:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You are very frustrated at seeing the amount of spam emails you've received.   You send an email to your manager about it asking if he is having a similar issue. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Will you please email my manager with the message 'Are you also getting a ridiculous amount of messages about crypto scams?'.",
                },
            ],
            reasoning='The user wants me to send an email to his manager. He told me the message content: "Are you also getting a ridiculous amount of emails about crypto scams?", but I need to figure out is who exactly the user\'s "manager" is. I can do this by checking the user\'s contacts and seeing if there is any contact that is listed as "manager". Looking through the contacts, I found "Kevin Chen" listed as the user\'s manager.\n\nWith the user\'s confirmation, I will send the email "Are you also getting a ridiculous amount of messages about crypto scams?" to Kevin Chen.',
            success_conditions=[
                {
                    "input_text": "1. An email will be sent saying, 'Are you also getting a ridiculous amount of messages about crypto scams?' to Kevin Chen at 10:20 on July 29th 2024.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_email"],
            milestones=[
                # Milestone 0 – Agent looks up the manager’s contact information
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
                # Milestone 1 – Kevin Chen (manager) was returned from the contact search in Milestone 0
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
                                                "value": "Kevin Chen",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "kevin.chen@example.com",
                                                "partial": False,
                                            },
                                            "relationship": {
                                                "value": "Manager",
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
                # Milestone 2 – Email is sent to Kevin Chen containing the spam-complaint text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["kevin.chen@example.com"]
                                    ],
                                    "status": "sent",
                                    "body": "crypto scams",
                                    "creation_datetime_iso": "2024-07-29T10:20:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                # Body must contain the key phrase, phrasing can vary
                                "body": column_contains_similarity,
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
            name="THEO_APPLESEED_26_dec3bed8-d5c0-47ec-bff7-fa669567f928_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T17:40:00-07:00",
            is_read_time="2024-07-29T17:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to delete all messages about cryptocurrencies. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete all cryptocurrency messages.",
                },
            ],
            reasoning="The user wants to delete all cryptocurrency messages. I will search for these in messages. I will delete all messages that mention cryptocurrency.",
            success_conditions=[
                {
                    "input_text": "1. All messages from unknown1@crypto-invest.com, offers@blockchainbuzz.net, info@cryptogains.io, promo@digitalcoins.com,contact@futurecrypto.net, deals@coinrealm.org,\nhello@investcrypto.today and team@cryptonow.com are deleted.\n",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "remove_message_or_conversation",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – The agent attempts to locate the cryptocurrency-related messages
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
                # Milestone 1 – All messages from the listed cryptocurrency senders have been removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender_address": [
                                        "unknown1@crypto-invest.com",
                                        "offers@blockchainbuzz.net",
                                        "info@cryptogains.io",
                                        "promo@digitalcoins.com",
                                        "contact@futurecrypto.net",
                                        "deals@coinrealm.org",
                                        "hello@investcrypto.today",
                                        "team@cryptonow.com",
                                    ],
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Agent searched for messages -> those messages are removed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_26_fd33640b-88c4-4cdb-993f-b78d95fe8125_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-28T13:30:00-07:00",
            is_read_time="2024-07-28T13:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You've been getting a lot of crypto texts, and you want to know who the very first one was from. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who was the sender of the first crypto text I got? ",
                },
            ],
            reasoning='The user wants to know who was the sender of the first crypto text they got. Okay, I start off by searching texts mentioning crypto. I\'ll look for "crypto" "digital coin" or "blockchain" in the name of the sender or the content of the message. There are eight matches. Now I need to find the first one with the earliest date and time among all of them. I see that the earliest message was received on July 21st at 14:35 from Cypto Invest. I\'ll show the user the message with its sender. ',
            success_conditions=[
                {
                    "input_text": "1. The user is informed that Crypto Invest was the sender of the first crypto text they received at 14:35 on 21 July 2024.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – Agent looks through the user’s messages to find crypto texts
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
                # Milestone 1 – The earliest crypto-related text (21 Jul 2024 14:35 from unknown1@crypto-invest.com)
                # is included in the result returned by the tool call in Milestone 0
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
                                                "value": "unknown1@crypto-invest.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-21T14:35:00-07:00",
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
                    ]
                ),
                # Milestone 2 – Agent tells the user that Crypto Invest / unknown1@crypto-invest.com
                # was the sender of the first crypto text
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
                                        ("Crypto Invest", "unknown1@crypto-invest.com")
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
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
            name="THEO_APPLESEED_26_2da39964-0dda-4e81-83a9-e3529491634f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_26",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-28T14:00:00-07:00",
            is_read_time="2024-07-28T14:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You've been getting a lot of spam text messages with links in them lately and you're tired of it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete all my texts that contain links",
                },
            ],
            reasoning='The user asked me to delete all of their texts that contain links. I\'ll look at all their text message threads to see which messages contain a "www." or "https" or a ".com" or ".io" or ".net" or ".org". I\'ve found eight text messages. With the user\'s confirmation, I will delete all these spam texts that contain links.',
            success_conditions=[
                {
                    "input_text": "1. The text from unknown1@crypto-invest.com is deleted",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The text from offers@blockchainbuzz.net is deleted",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The text from info@cryptogains.io is deleted",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "4. The text from promo@digitalcoins.com is deleted",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "5. The text from contact@futurecrypto.net is deleted",
                    "statefullness": "Stateful",
                },
                {
                    "statefullness": "Stateful",
                    "input_text": "6. The text from deals@coinrealm.org is deleted",
                },
                {
                    "statefullness": "Stateful",
                    "input_text": "7. The text from hello@investcrypto.today is deleted",
                },
                {
                    "statefullness": "Stateful",
                    "input_text": "8. The text from team@cryptonow.com is deleted",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "remove_message_or_conversation",
            ],
            milestones=[
                # Milestone 0 – Agent inspects messages to determine which contain links
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
                # Milestone 1 – All spam/link messages are removed from the MESSAGING store
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": [
                                        "unknown1@crypto-invest.com",
                                        "offers@blockchainbuzz.net",
                                        "info@cryptogains.io",
                                        "promo@digitalcoins.com",
                                        "contact@futurecrypto.net",
                                        "deals@coinrealm.org",
                                        "hello@investcrypto.today",
                                        "team@cryptonow.com",
                                    ],
                                    "sender_address": [
                                        "unknown1@crypto-invest.com",
                                        "offers@blockchainbuzz.net",
                                        "info@cryptogains.io",
                                        "promo@digitalcoins.com",
                                        "contact@futurecrypto.net",
                                        "deals@coinrealm.org",
                                        "hello@investcrypto.today",
                                        "team@cryptonow.com",
                                    ],
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # First inspect messages, then delete them
            ],
        ),
    ]
