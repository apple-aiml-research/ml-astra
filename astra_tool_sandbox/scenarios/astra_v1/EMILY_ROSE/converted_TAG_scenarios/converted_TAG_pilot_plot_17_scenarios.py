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
    column_list_tuple_contains_similarity,
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_similarity,
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


def get_TAG_EMILY_ROSE_pilot_plot_17(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="EMILY_ROSE_17_87c83005-0e63-417f-a5d1-62fa6a0c2c94_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_17",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T18:40:00-08:00",
            is_read_time="2024-12-13T18:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to see the last message you sent to Oscar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the last message I sent to +1 530-555-0140.",
                },
            ],
            reasoning="The user wants to see the last message they sent to +1 530-555-0140. . Let me look for their messages. Okay I have found the conversation. I will show the user the last message they sent.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1.The user is shown the last message they sent to Oscar Martinez on December 13th at 15:40 that says 'Awesome! Thanks for your enthusiasm, Oscar. Looking forward to it!'.",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – Agent tries to locate messages (must call a message-retrieval tool)
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
                # Milestone 1 – Confirm that the expected message to Oscar exists in the tool output
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
                                                "value": "Awesome! Thanks for your enthusiasm, Oscar. Looking forward to it!",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "+1 530-555-0123",
                                                "partial": False,
                                            },
                                            "status": {
                                                "value": "sent",
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
                # Milestone 2 – Agent’s reply to the user contains the message content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Awesome! Thanks for your enthusiasm, Oscar. Looking forward to it!",
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
            name="EMILY_ROSE_17_d66a4657-338a-4120-be2f-4fb006947889_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T16:15:00-08:00",
            is_read_time="2024-12-13T16:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You are wondering what time you sent in your last message to Oscar Martinez "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I send that last message to Oscar ",
                },
            ],
            reasoning="The user wants to know when they sent their last message to Oscar. First thing I need to do is search the user's messages to find a conversation with a name that matches. Ok I found a conversation with Oscar Martinez, this must be what the user is referring to. Now that I have found that I just need to take a look at the last message sent by the user. Ok now that I have that I will retrieve the time of the message and inform the user",
            success_conditions=[
                {
                    "input_text": "1. The time of the message sent by the user on December 13, 2024 at 15:40 to Oscar Martinez is presented to the user",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_messages",
                "get_all_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looks through messages to find the relevant conversation
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
                # Milestone 1 – Confirm the expected message (to Oscar, sent 2024-12-13 15:40) appeared in the tool output
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
                                                "value": "Oscar Martinez",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-13T15:40:00-08:00",
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
                                    "content": [("3:40", "15:40")],
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
                (0, 1),  # tool call → verify message found
                (1, 2),  # message found → inform user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_17_d66a4657-338a-4120-be2f-4fb006947889_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T16:15:00-08:00",
            is_read_time="2024-12-13T16:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You are wondering what time you sent in your last message to Oscar Martinez "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I send that last message to the person who wants to organise 'Paws at the Park'.",
                },
            ],
            reasoning="The user wants to know what time they last messaged the person who wants to organise 'Paws at the Park'. I will first look for this person in messages. I have found Oscar Martinez who has sent a message about organising 'Paws at the Park'.\n\nI will inform the user that the last message they sent to Oscar was at 15:40 on December 13th.",
            success_conditions=[
                {
                    "input_text": "1. The time of the message sent by the user on December 13, 2024 at 15:40 to Oscar Martinez is presented to the user",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
            milestones=[
                # Milestone 0 – The agent consults the messages database (search or list)
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
                # Milestone 1 – The returned result set contains the expected message to Oscar at 2024-12-13 15:40
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
                                                "value": "Oscar Martinez",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-13T15:40:00-08:00",
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
                # Milestone 2 – The agent informs the user of the correct time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("3:40", "15:40")],
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
                (0, 1),  # Message lookup → verify correct message exists
                (1, 2),  # Verified message → respond to user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_17_87c83005-0e63-417f-a5d1-62fa6a0c2c94_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_17",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T18:40:00-08:00",
            is_read_time="2024-12-13T18:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to see the last message you sent to Oscar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the last message I sent to the guy I just messaged",
                },
            ],
            reasoning="The user wants to see the last message they sent to Oscar Martinez. Let me look for their messages. Okay I have found the conversation. I will show the user the last message they sent.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1.The user is shown the last message they sent to Oscar Martinez on December 13th at 15:40 that says 'Awesome! Thanks for your enthusiasm, Oscar. Looking forward to it!'.",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
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
                # Milestone 1 – The retrieved tool output contains the expected last-sent message
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
                                                "value": "Oscar Martinez",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Awesome! Thanks for your enthusiasm, Oscar. Looking forward to it!",
                                                "partial": False,
                                            },
                                            "status": {
                                                "value": "sent",
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
                            reference_milestone_node_index=0,  # depends on tool call in Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – The agent tells the user the content of that last message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Awesome! Thanks for your enthusiasm",
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
                (0, 1),  # Tool call → verify correct message in tool output
                (1, 2),  # Verified data → confirm it was communicated to the user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_17_daae2723-2f91-48dd-9d4f-75f26171edf8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T15:33:00-08:00",
            is_read_time="2024-12-13T15:33:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know if Oscar has replied to your message. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has the last person I messaged replied? Yes or No.",
                },
            ],
            reasoning="Okay so the user wants to know if the last person they messaged has replied. Looking into their message thread, I can see the last person they messaged was 'Oscar Martinez' at 15:30 saying 'Great plan! Let me know how you go with that. Once we have a draft plan, we could run it by the community board for approval.'. There has been no reply from Oscar so I can inform the user of this.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The user is informed that no new messages have been received from Oscar Martinez on 13 December 2024.",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – The agent looks up messages to check for Oscar’s reply
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
                # Milestone 1 – Return the existing conversation with Oscar
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
                                            # Either direction is acceptable; one side must match the sister’s number
                                            "conversation_name": {
                                                "value": "Oscar Martinez",
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
                # Milestone 2 – The agent tells the user Oscar has not replied
                Milestone(
                    snapshot_constraints=[
                        # 1b ‑ States no reply / response
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "no",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_similarity,
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
            name="EMILY_ROSE_17_58764f45-bd19-4e15-b833-3861e178226c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T16:45:00-08:00",
            is_read_time="2024-12-13T16:45:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        'You want to dictate a reply to Oscar Martinez saying "Hey was just wondering how your noters are coming along so far and if you need any help.  " '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to the message I just received and ask how the noters are coming along so far and if I can offer any help",
                },
            ],
            reasoning="User wants to reply to the message they just received. I'll check their message first. Ok, I found the message received at 15:35 on December 13, and the sender of the message is Oscar Martinez with the phone number +1 530-555-0140. I'll draft the message saying \"How are the noters coming along so far. Let me know if you need any help.\" and send it to Oscar Martinez to their number +1 530-555-0140. ",
            success_conditions=[
                {
                    "input_text": "1. A reply message is sent to Oscar Martinez asking how their notes are coming along.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["search_messages", "get_all_messages", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up recently received messages
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
                # Milestone 1 – Confirm the message from Oscar Martinez was retrieved
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
                                                "value": "+1 530-555-0140",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Sounds good",
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
                # Milestone 2 – A reply message was sent to Oscar asking about notes and offering help
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [["+1 530-555-0140"]],
                                    "content": "help",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-13T16:45:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Ensure Oscar’s number is included among all participants
                                "participants_addresses": column_list_subset_match_similarity,
                                # Make sure the message text includes the word "help"
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
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
                (0, 1),  # Message search → confirmation of retrieved message
                (1, 2),  # Retrieved message → sending reply
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_17_58764f45-bd19-4e15-b833-3861e178226c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_17",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T16:45:00-08:00",
            is_read_time="2024-12-13T16:45:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        'You want to dictate a reply to Oscar Martinez saying "Hey was just wondering how your noters are coming along so far and if you need any help.  " '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a reply message to Oscar Martinez saying "Hey was just wondering how your noters are coming along so far and if you need any help."',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Oscar Martinez.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": "1. A reply message is sent to Oscar Martinez asking how their notes are coming along.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["search_messages", "get_all_messages", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up the existing conversation / contact information
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
                # Milestone 1 – Return the existing conversation with Oscar
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
                                            # Either direction is acceptable; one side must match the sister’s number
                                            "conversation_name": {
                                                "value": "Oscar Martinez",
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
                # Milestone 2 – A new outgoing message is added to the Oscar Martinez thread
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require that the user’s and Oscar’s numbers are present in participants
                                    "participants_addresses": [
                                        [
                                            ("+1 530-555-0140",),  # Oscar
                                            (
                                                "+1 530-555-0123",
                                                "emily.rose@orchardcommunity.org",
                                            ),  # Emily (self)
                                        ]
                                    ],
                                    # Core content of the dictated reply
                                    "content": "wondering",
                                    "creation_datetime_iso": "2024-12-13T16:45:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                # Message body just needs to contain the main phrase
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox chatter
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_17_daae2723-2f91-48dd-9d4f-75f26171edf8_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T15:33:00-08:00",
            is_read_time="2024-12-13T15:33:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know if Oscar has replied to your message. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has Oscar replied? Yes or No.",
                },
            ],
            reasoning="Right so, the user is wanting to know if 'Oscar' has replied. Checking their contacts, I can only see no one under 'Oscar'. Next, I will check the user's message threads and I can see there is an exchange with an 'Oscar Martinez'. The user sent a message to him at 15:30 saying 'Great plan! Let me know how you go with that. Once we have a draft plan, we could run it by the community board for approval.'. There has been no reply from Oscar so I can inform the user of this.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The user is informed that no new messages have been received from Oscar Martinez on 13 December 2024.",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – the agent looks through the message database
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
                # Milestone 1 – Return the existing conversation with Oscar
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
                                            # Either direction is acceptable; one side must match the sister’s number
                                            "conversation_name": {
                                                "value": "Oscar Martinez",
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
                # Milestone 2 – the agent tells the user that Oscar has not replied
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
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Agent searched messages before informing the user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_17_004992d0-fdf7-4539-9a01-bd9623c58090_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T15:50:00-08:00",
            is_read_time="2024-12-13T15:50:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You had a really good brainstorming session with Oscar.   You want to send him a message requesting that the notes be submitted by email. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a message to Oscar Martinez saying "Can you submit your notes via email?". ',
                },
            ],
            reasoning='The user wants to send a message to Oscar to say "Can you submit your notes via email?". But Oscar does not in the contacts, so I need to search messages conversations. I\'ll ask if the user is ready to send, and send as requested.',
            success_conditions=[
                {
                    "input_text": '1. A message saying "Can you submit your notes via email?" is sent to Oscar Martinez.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up the existing conversation with Oscar
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
                # Milestone 1 – Return the existing conversation with Oscar
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
                                            # Either direction is acceptable; one side must match the sister’s number
                                            "conversation_name": {
                                                "value": "Oscar Martinez",
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
                # Milestone 2 – A new outgoing message asking for notes via email is sent to Oscar
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
                                                "+1 530-555-0123",
                                                "emily.rose@orchardcommunity.org",
                                            ),  # Emily (self)
                                            ("+1 530-555-0140",),  # Oscar
                                        ]
                                    ],
                                    "content": "Can you submit your notes via email?",
                                    "creation_datetime_iso": "2024-12-13T15:50:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_17_b6399746-e549-4c13-afcc-08bb9b6b3f06_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_17",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T17:25:00-08:00",
            is_read_time="2024-12-13T17:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You need to schedule time to compile the ideas from the brainstorming. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Make a new event from 08:00-09:00 on Saturday called Compile Ideas. ",
                },
            ],
            reasoning="The user wants to create an event. I will use the details the user has provided to create this event. \nThe user wants to call it Compile Ideas so I shall make that the name of the event. The user has specified the duration will be one hour from 08:00-09:00 so I shall set the event for that time. The user said they wanted the event on Saturday, which is the 14 December 2024, so I will schedule the event for that day. \nI will let the user know the event has been created. ",
            success_conditions=[
                {
                    "input_text": "1. An event called Compile Ideas from 08:00-09:00 on 14 December 2024 is created. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["create_calendar_event"],
            milestones=[
                # Milestone 0 – verify that the “Compile Ideas” event was added for the correct
                # date and time (08:00-09:00 on 14 Dec 2024).
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Compile Ideas",
                                    "start_datetime_iso": "2024-12-14T08:00",
                                    "end_datetime_iso": "2024-12-14T09:00",
                                    "creation_datetime_iso": "2024-12-13T17:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Allow any timezone offset so only check that the expected
                                # date-time substring is present.
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_17_004992d0-fdf7-4539-9a01-bd9623c58090_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_17",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T15:50:00-08:00",
            is_read_time="2024-12-13T15:50:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You had a really good brainstorming session with Oscar.   You want to send him a message requesting that the notes be submitted by email. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Message him again and say "Can you submit your notes via email?". ',
                },
            ],
            reasoning="The user wants to send a message \"Can you submit your notes via email?\". They are requesting to message someone again, so I'll check who they were recently in conversation with... I can see that they were talking Oscar Martinez discussing notes, so it seems likely that this is who the user wants to message. With the user's confirmation, I will send the message as requested.",
            success_conditions=[
                {
                    "input_text": '1. A message saying "Can you submit your notes via email?" is sent to Oscar Martinez.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up the existing conversation or contact info
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
                # Milestone 1 – Return the existing conversation with Oscar
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
                                            # Either direction is acceptable; one side must match the sister’s number
                                            "conversation_name": {
                                                "value": "Oscar Martinez",
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
                # Milestone 2 – New message to Oscar asking for notes via email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require both Emily and Oscar to appear, no extras
                                    "participants_addresses": [
                                        [
                                            (
                                                "+1 530-555-0123",
                                                "emily.rose@orchardcommunity.org",
                                            ),  # Emily (self)
                                            ("+1 530-555-0140",),  # Oscar
                                        ]
                                    ],
                                    "content": "Can you submit your notes via email?",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-13T15:50:00-08:00",
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
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox traces when checking DB change
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Lookup precedes sending the message
            ],
        ),
    ]
