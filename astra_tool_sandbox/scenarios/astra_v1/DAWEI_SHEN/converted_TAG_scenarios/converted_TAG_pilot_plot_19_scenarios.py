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
    column_list_subset_match_similarity,
    column_list_tuple_contains_similarity,
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_rouge_l_similarity,
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


def get_TAG_DAWEI_SHEN_pilot_plot_19(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="DAWEI_SHEN_19_bd422699-7479-45a5-aad8-c65435ecdb2c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "messaging",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T10:20:00-08:00",
            is_read_time="2024-12-13T10:14:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You are currently out driving and notice you have a new email notification.       As you are currently on the clock for work, you want to know who the email is from and if it's important. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Do I have any unread messages or emails?",
                },
            ],
            reasoning="Right so, the user wants to know if they have any new messages or emails notifications. From searching I can see that there is one new email received from Michelle Barnes today at 10:15.\n\nI can relay this information to the user and ask if they would like me to read or summarise the email, and then in turn reply to it.",
            success_conditions=[
                {
                    "input_text": "The assistant informs the user that there is one new (unread) email from Michelle Barnes received today at 10:15.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "get_all_messages",
                "search_messages",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent fetches the new email(s)
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
                # Milestone 1 – The returned email list contains Michelle Barnes' 10:15 email
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
                                                "value": "michelle.barnes@orchardtech.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-13T10:15:00-08:00",
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
                # Milestone 2 – Agent informs the user about the email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Michelle Barnes",
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
            name="DAWEI_SHEN_19_e841fbc6-a038-4336-9b99-d408674f64bf_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "messaging",
                "email",
                "contact",
                "whatsapp_messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T21:15:00-08:00",
            is_read_time="2024-12-12T21:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You ran into Charles at a bar and he wanted you to text him in your usual way the name of the person you sent the receipt for the stage props order to, but you can't remember. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text Francis Wagner's email address to Charles in our usual way.",
                },
            ],
            reasoning="The user wants to text Charles in their usual way. They only have one Charles in their contact list, Charles Wilde, so that's who I'll compose a message for. The user also mentioned 'the usual way', based on the past message history, I assume it should be whatsapp message. They want to send him Francis Wagner's email address, probably because Francis is who they sent the stage props order receipt to. I'll send Charles a text saying \"I sent the receipt for the stage props order to Francis Wagner. His email address is francis.wagner@orchardtheater.com\"",
            success_conditions=[
                {
                    "input_text": "1. The contact for Francis Wagner (francis.wagner@orchardtheater.com) is found",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": '2. A Whatsapp message is sent to Charles Wilde contains "francis.wagner@orchardtheater.com"',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "search_contacts",
                "get_all_contacts",
                "send_whatsapp_message",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_message",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent searches contacts to find Francis Wagner's email address
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
                # Milestone 1 – Confirm Francis Wagner's contact (with email) was found in the contact search
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
                                                "value": "Francis Wagner",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "francis.wagner@orchardtheater.com",
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
                # Milestone 2 – A WhatsApp message is sent to Charles containing Francis's email address
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [
                                            (
                                                "+1 555-234-5678-9012",
                                                "charles.wilde@orchardtheater.com",
                                            ),
                                            (
                                                "+1 555-123-4567-8901",
                                                "dawei.shen@orchardtech.com",
                                            ),
                                        ]
                                    ],
                                    "content": "francis.wagner@orchardtheater.com",
                                    "sender_address": "PLACEHOLDER",  # we don't strictly check this,
                                    "creation_datetime_iso": "2024-12-12T21:15:00-08:00",
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
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Email search → confirm correct email thread
                (
                    1,
                    2,
                ),  # Having found Francis's email → send WhatsApp to Charles with that email
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_ac04e2a6-7c80-4071-8ba6-f40b49e01f9f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "email",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T20:00:00-08:00",
            is_read_time="2024-12-12T20:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You have sent the receipt to Francis.       You want to know when you sent it for your own records. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I send email to Francis?",
                },
            ],
            reasoning="The user wants to know what time they sent the email.\nI should first clarify who they mean by Francis. I can see one Francis in their inbox, Francis Wagner.\nThe user sent an email with the subject “Receipt for Stage Props Order” on December 12 2024 at 19:30 (7:30 pm). I can assume this is the email the user is referring to.\nI should inform them of the exact send time.",
            success_conditions=[
                {
                    "input_text": "The assistant tells the user the email to francis.wagner@orchardtheater.com was sent at 7:30 pm on December 12, 2024 or today.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent queries the email database
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
                # Milestone 1 – The queried result includes the receipt email sent to Francis
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
                                                "value": "Receipt for Stage Props Order",
                                                "partial": True,
                                            },
                                            "recipients_addresses": {
                                                "value": [
                                                    "francis.wagner@orchardtheater.com"
                                                ],
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-12T19:30:00-08:00",
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
                # Milestone 2 – Agent tells the user the correct send time
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
                                        ("7:30pm", "7:30 pm", "7:30 p.m.", "19:30")
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
            name="DAWEI_SHEN_19_7547607e-4f6e-4232-bb34-5acc17362244_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "whatsapp_messaging",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:00:00-08:00",
            is_read_time="2024-12-12T19:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to send a message to your theatre friend, Charles, to tell him you've run into a small problem and to ask him to call you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to send Charles Wilde a message in our usual way that says "We\'ve run into a small problem. Can you call?". ',
                },
            ],
            reasoning="The user wants to send Charles Wilde a message 'in our usual way', so first I need to work out which channel that is. Checking our recent conversations, a search of WhatsApp shows Charles and I regularly message there, so WhatsApp is our usual way. The message content is given: \"We've run into a small problem. Can you call?\". I'll confirm and send that message to Charles Wilde over WhatsApp.",
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Charles Wilde with the text "We\'ve run into a small problem. Can you call?"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "send_message",
                "search_contacts",
                "get_all_contacts",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0: Check if search whatsapp initiated (rehearsal time mentioned in whatsapp)
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1: Verify related messages found
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
                                                "value": "Charles Wilde",
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
                # Milestone 2 – A new WhatsApp (or message) entry to Charles is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [
                                            (
                                                "charles.wilde@orchardtheater.com",
                                                "+1 555-234-5678-9012",
                                            )
                                        ]
                                    ],
                                    "content": "can you call",
                                    "creation_datetime_iso": "2024-12-12T19:00:00-08:00",
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
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_bf6be7a0-c2dc-45c1-aeec-54ef9da6f9f7_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "email",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:30:00-08:00",
            is_read_time="2024-12-12T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to let your friend know you placed the order for theatre props already so that she doesn't need to do it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you forward the stage props order email to Vickie?",
                },
            ],
            reasoning='Alright, the user asked me to forward an email to Vickie. I need to find out who Vickie is, is there a Vickie in their contacts? I found a "Vick Li" and a "Vickie Lee", I need to be careful not to get confused here. Let\'s try to do some more reasoning first before I decide. The user wants me to forward an email about stage props, and if I check their contacts, "Vick Li" is a college friend and "Vickie Lee" is a theatre friend, so I think that the user must be wanting to email Vickie Lee since they both do theatre together.\n\nNow I need to figure out which email the user wants me to forward. Looking at their past emails, I see they sent something with the subject "Receipt for Stage Props Order" to Francis. It has an attached order receipt, so I\'ll assume that\'s what they want me to forward. ',
            success_conditions=[
                {
                    "input_text": '1. The email "Receipt for Stage Props Order" along with its Order_Receipt_12122024.pdf attachment is forwarded to Vickie Lee vickie.lee@orchardtheater.com',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_emails",
                "get_all_emails",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – The agent uses an email retrieval tool to locate the stage props order email
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
                # Milestone 1 – Confirm the "Receipt for Stage Props Order" email was retrieved (with correct recipient)
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
                                                "value": "Receipt for Stage Props Order",
                                                "partial": False,
                                            },
                                            "recipients_addresses": {
                                                "value": [
                                                    "francis.wagner@orchardtheater.com"
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
                # Milestone 2 – Optional: The agent uses contacts retrieval to distinguish Vickie Lee vs Vick Li (supports correct recipient choice)
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
                # Milestone 3 – The email is forwarded to the correct recipient (Vickie Lee) and sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Forwarded email should go to Vickie Lee at the theater email
                                    "recipients_addresses": [
                                        ["vickie.lee@orchardtheater.com"]
                                    ],
                                    # Subject likely starts with "Fwd:" or similar but must contain original subject phrase
                                    "subject": "Receipt for Stage Props Order",
                                    "status": "sent",
                                    # Body should include some indication it's about the stage props order / forwarding
                                    "body": "stage props",
                                    # Attachment should include the original receipt file
                                    "attachments": [["Order_Receipt_12122024.pdf"]],
                                    "creation_datetime_iso": "2024-12-12T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "subject": column_contains_similarity,
                                "status": column_exact_match_similarity,
                                "body": column_contains_similarity,
                                "attachments": column_list_subset_match_similarity,
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
                (0, 1),  # email search → confirm correct props receipt email retrieved
                (1, 3),  # retrieved correct email → forward it to Vickie
                (
                    2,
                    3,
                ),  # (optional) contacts lookup supports choosing the correct Vickie → forward email
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_bf6be7a0-c2dc-45c1-aeec-54ef9da6f9f7_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "email",
                "contact",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:30:00-08:00",
            is_read_time="2024-12-12T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to let your friend know you placed the order for theatre props already so that she doesn't need to do it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you forward my Receipt for Stage Props Order email to the other theatre friend in my contacts?",
                },
            ],
            reasoning='Alright, the user asked me to forward an email to their "other theatre friend." To determine who they mean, I\'ll start by deciding who their theatre friends are. I see Charles Wilde, Francis Wagner, and Vickie Lee all have email addresses through orchardtheater.com, so now I need to figure out which of these three contacts the user wants to forward an email to. They corresponded with both Francis and Charles in the last half hour about the order, so when they say "other" theatre friend they must mean Vickie, so I\'ll forward the email with the subject "Receipt for Stage Props Order" to vickie.lee@orchardtheater.com. ',
            success_conditions=[
                {
                    "input_text": '1. The email "Receipt for Stage Props Order" along with its Order_Receipt_12122024.pdf attachment is forwarded to Vickie Lee vickie.lee@orchardtheater.com',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_emails",
                "get_all_emails",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Agent uses an email retrieval tool to find the "Receipt for Stage Props Order" email
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
                # Milestone 1 – Confirm that the correct "Receipt for Stage Props Order" email was retrieved
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
                                                "value": "Receipt for Stage Props Order",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "dawei.shen@orchardtech.com",
                                                "partial": False,
                                            },
                                            "attachments": {
                                                "value": ["Order_Receipt_12122024.pdf"],
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
                            reference_milestone_node_index=0,  # Validate based on retrieval in Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – A new sent email exists to Vickie Lee containing the forwarded receipt (stateful change)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["vickie.lee@orchardtheater.com"]
                                    ],
                                    "status": "sent",
                                    # Subject/body need not be exact, but should reference stage props/order/receipt
                                    "subject": "Receipt for Stage Props Order",
                                    "attachments": [["Order_Receipt_12122024.pdf"]],
                                    "creation_datetime_iso": "2024-12-12T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "subject": column_rouge_l_similarity,
                                "attachments": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against pre-task state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Email retrieval → confirm correct email
                (1, 2),  # Correct email identified → forwarded email exists
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_ac04e2a6-7c80-4071-8ba6-f40b49e01f9f_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "messaging",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T20:00:00-08:00",
            is_read_time="2024-12-12T20:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You have sent the receipt to Francis.       You want to know when you sent it for your own records. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When did I send out that receipt for the theatre?",
                },
            ],
            reasoning="The user wants to know what time they sent out a bill.\nI can assume that this is referring to an email. I should check their inbox for anything that matches their query.\nI see one email sent to Francis Wagner on December 12th 2024 at 19:30 with the subject line Receipt for Stage Props Order.\nI can assume that this is the email the user is referring to, as a bill is similar to a receipt, and props are used in theater.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "The assistant tells the user that the receipt was sent on December 12, 2024 at 7:30 pm.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "get_all_messages",
                "search_messages",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent queries the email database
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
                # Milestone 1 – The queried result includes the receipt email sent to Francis
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
                                            "recipients_addresses": {
                                                "value": [
                                                    "francis.wagner@orchardtheater.com"
                                                ],
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-12T19:30:00-08:00",
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
                # Milestone 2 – Agent tells the user the correct send time
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
                                        ("7:30pm", "7:30 pm", "7:30 p.m.", "19:30")
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
            name="DAWEI_SHEN_19_7547607e-4f6e-4232-bb34-5acc17362244_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "whatsapp_messaging",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:01:00-08:00",
            is_read_time="2024-12-12T19:01:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to send a message to your theatre friend, Charles, to tell him you've run into a small problem and to ask him to call you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send my theatre friend a message who just texted me that says "We\'ve run into a small problem. Can you call?". ',
                },
            ],
            reasoning='The user wants to message the theatre friend who just texted them. Checking contacts, two people are listed as "Theater Friend": Vickie Lee and Charles Wilde. To find which one just texted, I look at recent messages and see that Charles Wilde recently sent a text, so the user means Charles Wilde. I\'ll send him the message the user dictated, "We\'ve run into a small problem. Can you call?".',
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Charles Wilde with the text "We\'ve run into a small problem. Can you call?"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_messages",
                "get_all_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0: agent search contacts
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
                                        "get_all_contacts",
                                        "search_contacts",
                                    ],
                                ),
                            },
                        )
                    ]
                ),
                # Milestone 1: Charles contact found
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
                                                "value": "Charles Wilde",
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
                # Milestone 2: agent search contacts
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
                                        "get_all_whatsapp_messages",
                                        "search_whatsapp_messages",
                                    ],
                                ),
                            },
                        )
                    ]
                ),
                # Milestone 3: Charles text found
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
                                                "value": "Charles Wilde",
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
                        ),
                    ]
                ),
                # Milestone 4 – A new WhatsApp entry to Charles is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [
                                            (
                                                "charles.wilde@orchardtheater.com",
                                                "+1 555-234-5678-9012",
                                            )
                                        ]
                                    ],
                                    "content": "can you call",
                                    "creation_datetime_iso": "2024-12-12T19:01:00-08:00",
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
            milestone_edge_list=[
                (0, 1),
                (2, 3),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_811187da-f773-4308-9272-f78ac8e04e73_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T09:00:00-08:00",
            is_read_time="2024-12-12T09:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to schedule a team review meeting to consolidate all comments regarding research progress. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Add an event to my calendar called "Team Review Meeting" for tomorrow at 9am to 10:30am and add my colleagues Kevin Chen and Stefan Mustermann. The location is Conference Room C, Orchard Tech, Orchard County, CA. Please add a note that says "Review meeting to consolidate comments on the recent research updates" and set it as a busy work event',
                },
            ],
            reasoning='Ok what I\'m thinking is that I need to add an event to the calendar called "Team Review Meeting" for 2024.12.13 09:00 am - 10:30 \nInvite contacts "Kevin Chen" and "Stefan Mustermann", the location is Conference Room C, Orchard Tech, Orchard County, CA.\nTag the event as "Busy" and "work".\nFinally add a note that says:\n"Review meeting to consolidate comments on the recent research updates"\nSo the plan is to schedule the event immediately as there is no other Calendar conflicts.',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A meeting called "Team Review Meeting" is scheduled for  2024.12.13 09:00 am - 10:30 am at Conference Room C, Orchard Tech, Orchard County, CA',
                },
                {
                    "input_text": '2. Kevin Chen, Stefan Mustermann are added to the "Team Review Meeting" event',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '3. The following note is added to the "Team Review Meeting" event: Review meeting to consolidate comments on the recent research updates.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "4. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "create_calendar_event",
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 –  A “Team Review Meeting” entry created with the requested details
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Team Review Meeting",
                                    "start_datetime_iso": "2024-12-13T09:00:00-08:00",
                                    "end_datetime_iso": "2024-12-13T10:30:00-08:00",
                                    "location": "Conference Room C",
                                    "attendees_names": [
                                        [
                                            "Kevin Chen",
                                            "Stefan Mustermann",
                                            "Dawei Shen",
                                        ]
                                    ],
                                    "notes": "Review meeting to consolidate comments on the recent research updates",
                                    "creation_datetime_iso": "2024-12-12T09:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
                                "location": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_e0548498-6054-4309-a878-76fd404d039b_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T22:35:00-08:00",
            is_read_time="2024-12-12T22:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to send Francis another email with a new receipt as you sent the wrong receipt earlier. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a follow-up email to Francis Wagner about the Stage Props Order — I accidentally sent the wrong one earlier, will send it to him later.",
                },
            ],
            reasoning="First, I will search the mailbox to locate the previously-sent email to Francis Wagner with the subject “Receipt for Stage Props Order,” confirming the mistaken receipt. Next, I will compose a follow-up message to Francis that explains the mix-up receipt for the Stage Props Order. After confirming, I will send the new email with the attachment.",
            success_conditions=[
                {
                    "input_text": "1. A message is sent to francis.wagner@orchardtheater.com via e-mail about the wrong receipt sent and will send him the correct one later.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["send_email", "search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0: agent search emails
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
                                        "get_all_emails",
                                        "search_emails",
                                    ],
                                ),
                            },
                        )
                    ]
                ),
                # Milestone 1: Previous email to Francis found
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
                                                "value": "Receipt for Stage Props Order",
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
                # Milestone 2 – a new email to Francis is actually sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["francis.wagner@orchardtheater.com"]
                                    ],
                                    "body": "wrong",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-12T22:35:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_e841fbc6-a038-4336-9b99-d408674f64bf_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "messaging",
                "email",
                "contact",
                "whatsapp_messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T21:15:00-08:00",
            is_read_time="2024-12-12T21:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You ran into Charles at a bar and he wanted you to text him in your usual way the name of the person you sent the receipt for the stage props order to, but you can't remember. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text Charles the name and email of the person I sent the stage props order receipt to, in our usual way.",
                },
            ],
            reasoning="The user wants to text Charles in their usual way. They only have one Charles in their contact list, Charles Wilde, so that's who I'll compose a message for. The user also mentioned 'the usual way', based on the past message history, I assume it should be whatsapp message. They want to send him the name and email of the person they sent the stage props order receipt to. Looking at the user's emails, I see an email with the subject line \"Receipt for Stage Props Order.\" That's probably what they're referring to. The person they sent that email to is Francis Wagner. I'll send Charles a text saying \"I sent the receipt for the stage props order to Francis Wagner. His email address is francis.wagner@orchardtheater.com\"",
            success_conditions=[
                {
                    "input_text": '1. The email "Receipt for Stage Props Order" to Francis Wagner francis.wagner@orchartheater.com is found',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": '2. A Whatsapp message is sent to Charles Wilde contains "francis.wagner@orchardtheater.com"',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "search_contacts",
                "get_all_contacts",
                "send_whatsapp_message",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_message",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent uses an email retrieval tool to find the stage props receipt email
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
                                    # Either direct search or listing then filtering is acceptable
                                    target_tools=["search_emails", "get_all_emails"],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Confirm the "Receipt for Stage Props Order" email to Francis Wagner was actually retrieved
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
                                                "value": "Receipt for Stage Props Order",
                                                "partial": False,
                                            },
                                            "recipients_addresses": {
                                                "value": [
                                                    "francis.wagner@orchardtheater.com"
                                                ],
                                                "partial": True,  # allow list matching inside tool result
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
                # Milestone 2 – Agent sends a WhatsApp message to Charles that includes Francis's email address
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Participants must include both Dawei and Charles (by any valid identifier)
                                    "participants_addresses": [
                                        [
                                            (
                                                "charles.wilde@orchardtheater.com",
                                                "+1 555-234-5678-9012",
                                            ),
                                            (
                                                "dawei.shen@orchardtech.com",
                                                "+1 555-123-4567-8901",
                                            ),
                                        ]
                                    ],
                                    "content": "francis.wagner@orchardtheater.com",
                                    "creation_datetime_iso": "2024-12-12T21:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Ensure it's exactly that pair of participants, no extras
                                "participants_addresses": column_list_tuple_contains_similarity,
                                # Message body must contain the key email address
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
                (0, 1),  # Email tool usage → confirm correct email retrieved
                (
                    1,
                    2,
                ),  # Correct recipient info retrieved → WhatsApp message sent with that info
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_bd422699-7479-45a5-aad8-c65435ecdb2c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T10:20:00-08:00",
            is_read_time="2024-12-13T10:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You are currently out driving and notice you have a new email notification.       As you are currently on the clock for work, you want to know who the email is from and if it's important. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who's my latest email from?",
                },
            ],
            reasoning="To answer the user, I will look up their most recent email. The newest one in the inbox is from Michelle Barnes, received today (Dec 13) at 10:15. I will then inform the user that their latest email is from Michelle Barnes and read the message aloud so they can determine its importance while driving.",
            success_conditions=[
                {
                    "input_text": "The assistant reads aloud the email from Michelle Barnes received on December 13 at 10:15 to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – The agent looks up recent email(s)
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
                # Milestone 1 – The returned result contains the email from Michelle Barnes sent on Dec 13 at 10:15
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
                                                "value": "michelle.barnes@orchardtech.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-13T10:15:00-08:00",
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
                            reference_milestone_node_index=0,  # depend on the search in Milestone 0
                        ),
                    ],
                ),
                # Milestone 2 – The agent informs the user about the email (reads it aloud / summarizes)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Michelle",
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
            name="DAWEI_SHEN_19_2980c6ab-0a80-4913-acbe-65e50a9cf894_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:25:00-08:00",
            is_read_time="2024-12-12T19:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "After sending the prop receipts to Francis you want to meet with him to discuss further prop acquisition in the future. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Could you make an event on Sunday to discuss props with Francis around lunch time at 1?",
                },
            ],
            reasoning="ok so the user wants to create an event on Sunday to discuss props with Francis around lunch time at 1. I believe Francis refers to Francis Wagner as there is no other Francis in their contacts. I will add them as an invitee. So the events meaning is clear I will call it 'Prop Discussion.' The user wants to schedule it for Sunday around lunch time, which when looking at the calendar seems free so I will pencil this event in for 13:00.  I will now create an event called 'Prop Discussion' for 13:00 on Sunday 15th of December 2024",
            success_conditions=[
                {
                    "input_text": "1. an event called 'Prop Discussion' or similar with Francis Wagner as an invitee is created for 13:00 on 15th of December 2024",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "create_calendar_event",
                "search_contacts",
                "get_all_contacts",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 — The agent looks up Francis’ contact information
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
                # Milestone 1: Francis contact found
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
                                                "value": "Francis Wagner",
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
                # Milestone 2 — A calendar event has been created for the correct time, date, and attendee
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Prop",
                                    "start_datetime_iso": "2024-12-15T13:00",
                                    "attendees_names": [["Francis Wagner"]],
                                    "creation_datetime_iso": "2024-12-12T19:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_816a296f-fc54-44ab-912d-dfbdc7b0cdb2_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "email",
                "messaging",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T13:25:00-08:00",
            is_read_time="2024-12-13T13:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to find out what time dinner is tomorrow so you can book a massage to relax after your work week. "
                        "You have no other information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is dinner tomorrow? Also, add a half-hour massage appointment one hour before dinner.",
                },
            ],
            reasoning="The user wants to know when their dinner is tomorrow. Looking at their calendar, there is one event on 14 December at 19:00 named 'Dinner with Lukas and Vick'. I'm confident this is the event they mean, so I'll let them know.\n\nThey also asked me to add a half-hour massage appointment one hour before dinner, so I'll schedule it from 17:30 to 18:00 on 14 December.",
            success_conditions=[
                {
                    "input_text": "The user is told that 'Dinner with Lukas and Vick' is at 7:00 pm on 14 December.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "A calendar event named 'Massage appointment' is created for 14 December 2024 from 5:30 pm to 6:00 pm.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
                "get_all_emails",
                "search_emails",
                "get_all_messages",
                "search_messages",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the dinner event in the calendar
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
                # Milestone 1: Dinner event found
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
                                                "value": "Dinner with Lukas and Vick",
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
                # Milestone 2 – User is informed about the dinner time
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
                                            "7:00pm",  # 7:00 pm
                                            "7:00 pm",
                                            "7:00 p.m.",
                                            "19:00",  # 24-hour format
                                            "7 pm",
                                            "7pm",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR,
                    ],
                ),
                # Milestone 3 – A massage appointment is added to the calendar for 14 Dec 2024 17:30
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Massage appointment",
                                    "start_datetime_iso": "2024-12-14T17:30",
                                    "end_datetime_iso": "2024-12-14T18:00",
                                    "creation_datetime_iso": "2024-12-13T13:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
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
            name="DAWEI_SHEN_19_29615c2b-6ab8-4f3e-91ad-da6b087f27c5_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "contact",
                "email",
                "whatsapp_messaging",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:30:00-08:00",
            is_read_time="2024-12-12T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to send your other theatre friend a message saying that you placed an order for theatre props already so that they don't need to do it. You are going to forward the picture of the receipt you sent to francis.wagner@orchardtheater.com to them as well. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Can you send a text message to my theatre friend other than Charles in my contacts and write "I placed an order for the theatre props already so you don\'t need to do it." Then forward them the picture of the receipt I sent to francis.wagner@orchardtheater.com as well.',
                },
            ],
            reasoning='Alright, the user asked me to send the text message "I placed an order for the theatre props already so you don\'t need to do it" to their "other theatre friend". I really don\'t know what they mean by this. I\'m going to have to check their contacts - they have two names listed under "theatre friend", which are Charles Wilde and Vickie Lee. I already know that Dawei and Charles were exchanging WhatsApp messages about stage props for the theatre show, so they have already been in contact. It makes sense that Dawei wants to reach out to Vickie Lee. I\'m going to draft the message to her.\n\nAdditionally, the user wants me to forward the picture of the receipt they sent to Francis. First, I\'m going to look for any emails sent to francis.wagner@orchardtheater.com. I found one email titled "Receipt for Stage Props Order" on December 12th 2024 at 19:30, which contains the receipt attachment.\n\nWith the correct recipient identified and the receipt located, I send the text message to Vickie Lee, and forward the receipt to her by email, attaching the Order_Receipt_12122024.pdf file from the Francis email.',
            success_conditions=[
                {
                    "input_text": '1. The message "I placed an order for the theatre props already so you don\'t need to do it" will be sent to Vickie Lee.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The picture of the receipt from the email sent on December 12th 2024 at 19:30 to francis.wagner@orchardtheater.com is forwarded to Vickie Lee.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_emails",
                "get_all_emails",
                "send_whatsapp_message",
                "send_message",
                "send_email",
            ],
            milestones=[
                # Milestone 0
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
                                    # Either of these tools would plausibly be used to fetch the email / attachment
                                    target_tools=[
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1: Vick contact found
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
                                                "value": "Vickie Lee",
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
                # Milestone 2 – The agent looked up the email that has the props receipt
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
                                    # Either of these tools would plausibly be used to fetch the email / attachment
                                    target_tools=["search_emails", "get_all_emails"],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 3 – The returned result contains the email
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
                                            "recipients_addresses": {
                                                "value": [
                                                    "francis.wagner@orchardtheater.com"
                                                ],
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Receipt for Stage Props Order",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-12T19:30:00-08:00",
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
                            reference_milestone_node_index=2,  # depend on the search in Milestone 0
                        ),
                    ],
                ),
                # Milestone 4 – A new outgoing text / chat message was created to Vickie
                Milestone(
                    snapshot_constraints=[
                        # Verify the actual stateful change – new message in either MESSAGING or WHATSAPP DB.
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Vickie Lee",
                                    "content": "I placed an order for the theatre props already so you don't need to do it",
                                    "creation_datetime_iso": "2024-12-12T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "conversation_name": column_exact_match_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        ),
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.WHATSAPP,
                    ],
                ),
                # Milestone 5 – The receipt is forwarded to Vickie Lee by email with the attachment
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["vickie.lee@orchardtheater.com"]
                                    ],
                                    "attachments": [["Order_Receipt_12122024.pdf"]],
                                    "creation_datetime_iso": "2024-12-12T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "attachments": column_list_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.WHATSAPP,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (2, 3),
                (
                    3,
                    5,
                ),  # receipt email located → forwarded to Vickie with the attachment
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_58efccf5-5cbc-4b61-9f68-408b4b4545e4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "email",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:35:00-08:00",
            is_read_time="2024-12-12T19:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You have just sent the receipts for the props to Francis and want to let him know.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Text Fran saying; "Hey man, I just passed on the receipts for the props."',
                },
            ],
            reasoning="The user wants to Text Fran saying; \"Hey man, I just passed on the receipts for the props.\"\nwho do they mean by Fran? From recent correspondence email, I found the email titled 'Receipt for Stage Props Order' sent to Francis Wagner at 19:30:00, and the users contacts I can assume Fran refers to Francis Wagner in their contacts. I will now send their given statement to Francis Wagner via messages. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A message is sent to Francis Wagner saying; "Hey man, I just passed on the receipts for the props" at 19:35 12th of December 2024. ',
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "send_message",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – Agent looks up Francis / Fran in contacts (to resolve who "Fran" is)
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
                # Milestone 1 – Confirms that Francis Wagner was retrieved from the contact lookup
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
                                                "value": "Francis Wagner",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 555-456-7890-1234",
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
                # Milestone 2 – A text message to Francis is created with the right content and approximate time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Participants: Dawei (self) and Francis; allow either email or phone identifiers
                                    "participants_addresses": [
                                        [
                                            (
                                                "dawei.shen@orchardtech.com",
                                                "+1 555-123-4567-8901",
                                            ),
                                            (
                                                "francis.wagner@orchardtheater.com",
                                                "+1 555-456-7890-1234",
                                            ),
                                        ]
                                    ],
                                    "content": "I just passed on the receipts for the props.",
                                    "status": "sent",
                                    # Target time 2024-12-12T19:35:00; allow close match
                                    "creation_datetime_iso": "2024-12-12T19:35:00-08:00",
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
                (0, 1),  # Contacts lookup → confirm Francis
                (1, 2),  # Confirm Francis → send correct text message
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_da1a40a4-f2f9-4e01-87e1-e6ea506e8a99_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_low",
                "contact",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T12:00:00-08:00",
            is_read_time="2024-12-14T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You forgot to order a certain prop and want to see the link to the online supplier that Charles Wilde sent to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you pull up the WhatsApp message from Charles with the link to the theater item seller.",
                },
            ],
            reasoning="The user wants to see a WhatsApp message from Charles containing a link to a theater item seller. First, I will use the WhatsApp search tool to look through their messages.\n\nLooking through the user’s contacts I can see that Charles Wilde is the only contact with this first name, so I will focus on that conversation and search the WhatsApp messages to find the one containing the link.\n\nI can’t see any link to a theater item seller, however there is a link to a prop supplier: PropsSupplier.com. Due to the similarity of these phrases I will assume that this is what the user is referring to.\n\nI will now present the WhatsApp message with the link to the prop supplier to the user.",
            success_conditions=[
                {
                    "input_text": "1. WhatsApp message from Charles Wilde containing the link to PropsSupplier.com is presented.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent uses a WhatsApp retrieval tool
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Returned WhatsApp message contains link from Charles Wilde
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
                                            "sender_name": {
                                                "value": "Charles Wilde",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "PropsSupplier.com",
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
                # Milestone 2 – Agent informs user and shows the link
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "PropsSupplier.com",
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
            name="DAWEI_SHEN_19_d227c4cc-13bb-4292-b4e3-86dba6dbc617_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "whatsapp_messaging",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T20:00:00-08:00",
            is_read_time="2024-12-12T20:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know if Charles Wilde has responded to your last message. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has my last message regarding placing the props order gotten a response. Yes or No.",
                },
            ],
            reasoning="The user is asking wether their message has received a reply.\nFirst, i should confirm which messages they mean.\nI cannot see any recent conversations in their messages, I should check WhatsApp.\nI can see one conversation that may match the query, with Charles Wilde. The last message in this conversation was sent by the user on December 12th 2024 at 19:05, there are no recent messages from Charles Wilde.\nI should inform the user that Charles has not responded to their last message.",
            success_conditions=[
                {
                    "input_text": 'The assistant replies with "No", indicating that Charles Wilde has not responded to the user\'s last message.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – The agent checks WhatsApp messages (uses either search or get-all)
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Returned last WhatsApp message
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
                                                "value": "Charles Wilde",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Looks good, I'll place the order.",
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
                # Milestone 2 – The agent informs the user that Charles hasn’t replied
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
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # After checking WhatsApp, find the last sent message
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_ffd504fe-b4ca-44b5-ae3d-4e26a0c6466e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:25:00-08:00",
            is_read_time="2024-12-12T19:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You have just sent the receipts for the props to Francis and want to let him know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Text the theatre manager "Hey Fran, I have sent the receipts for the props to your email."',
                },
            ],
            reasoning='The user wants to message the theatre manager saying "Hey Fran, I have sent the receipts for the props to your email." Who do they mean when they say theatre manager? From recent correspondence and the users contacts I can assume that the theatre manager they speak of refers to Francis Wagner in their contacts. I will now send their given statement to Francis Wagner.',
            success_conditions=[
                {
                    "input_text": 'A message is sent to Francis Wagner saying "Hey Fran, I have sent the receipts for the props to your email." at 19:25 12th of December 2024.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["search_contacts", "get_all_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent tries to find Francis in the contacts
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
                # Milestone 1 – Returned Francis
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
                                                "value": "Francis Wagner",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 555-456-7890-1234",
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
                # Milestone 2 – A new message to Francis is created in the messaging database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Make sure Francis is one of the participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "francis.wagner@orchardtheater.com",
                                                "+1 555-456-7890-1234",
                                            )
                                        ]
                                    ],
                                    # Make sure the content references the receipts
                                    "content": "Hey Fran, I have sent the receipts for the props to your email.",
                                    "creation_datetime_iso": "2024-12-12T19:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against the initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_d227c4cc-13bb-4292-b4e3-86dba6dbc617_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T20:00:00-08:00",
            is_read_time="2024-12-12T20:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know if Charles Wilde has responded to your last message. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has Charles responded to my last message on WhatsApp? Yes or No.",
                },
            ],
            reasoning="The user is asking whether their last message to Charles Wilde on WhatsApp has received a reply. I check the WhatsApp conversation with Charles Wilde using the appropriate tools. The most recent message in that thread is the user’s own message—“Looks good, I'll place the order.” There are no newer messages from Charles. Therefore, Charles has not responded. I should tell the user: “No.”",
            success_conditions=[
                {
                    "input_text": 'The assistant replies with "No."',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_whatsapp_messages", "get_all_whatsapp_messages"],
            milestones=[
                # Milestone 0 – The agent inspects WhatsApp messages
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – Returned last WhatsApp message
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
                                                "value": "Charles Wilde",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Looks good, I'll place the order.",
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
                # Milestone 2 – The user receives confirmation that Charles has not responded
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
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Check last whatsapp message
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_ffd504fe-b4ca-44b5-ae3d-4e26a0c6466e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:25:00-08:00",
            is_read_time="2024-12-12T19:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You have just sent the receipts for the props to Francis and want to let him know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Text Fran saying; "Hey Fran, I have sent the receipts for the props to your email."',
                },
            ],
            reasoning='The user wants to Text Fran saying; "Hey Fran, I have sent the receipts for the props to your email." Who do they mean by Fran? From recent correspondence and the user\'s contacts I can assume Fran refers to Francis Wagner in their contacts. I will now send their given statement to Francis Wagner.',
            success_conditions=[
                {
                    "input_text": 'A message is sent to Francis Wagner saying; "Hey Fran, I have sent the receipts for the props to your email."',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["search_contacts", "get_all_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent tries to locate Francis in the contacts
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
                # Milestone 1: Find Francis
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
                                                "value": "Francis Wagner",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 555-456-7890-1234",
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
                # Milestone 2 – A new outgoing message to Francis exists in the MESSAGING DB
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
                                                "francis.wagner@orchardtheater.com",
                                                "+1 555-456-7890-1234",
                                            )
                                        ]
                                    ],
                                    "content": "Hey Fran, I have sent the receipts for the props to your email.",
                                    "creation_datetime_iso": "2024-12-12T19:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # found contact
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_da1a40a4-f2f9-4e01-87e1-e6ea506e8a99_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T12:00:00-08:00",
            is_read_time="2024-12-14T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You forgot to order a certain prop and want to see the link to the online supplier that Charles Wilde sent to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you pull up the WhatsApp message from Charles with the link to the prop supplier.",
                },
            ],
            reasoning="The user wants to see a WhatsApp message from Charles containing a link to a prop supplier, first I will determine which contact the user is talking about. \n\nLooking through the user’s contacts I can see that Charles Wilde is the only contact with this first name, I can assume that this is the person in question and look through their WhatsApp messages to find the one containing the link.\n\nI will now present the WhatsApp message with the link to the prop supplier to the user.",
            success_conditions=[
                {
                    "input_text": "1. WhatsApp message from Charles Wilde containing the link to PropsSupplier.com is presented.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks through WhatsApp messages (search or full list)
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – The tool output contains Charles’s message with the supplier link
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
                                            "sender_name": {
                                                "value": "Charles Wilde",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "PropsSupplier.com",
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
                            reference_milestone_node_index=0,  # tie to tool call in Milestone 0
                        ),
                    ],
                ),
                # Milestone 2 – The agent shows the link/message to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "PropsSupplier.com",
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
                (0, 1),  # Tool used → correct WhatsApp message identified
                (1, 2),  # Message identified → user informed
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_58efccf5-5cbc-4b61-9f68-408b4b4545e4_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "email",
                "messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:35:00-08:00",
            is_read_time="2024-12-12T19:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You have just sent the receipts for the props to Francis and want to let him know.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Message the one I just sent an email to saying "Hey man, I just passed on the receipts for the props."',
                },
            ],
            reasoning="The user wants to message the one he just sent an email to saying \"Hey man, I just passed on the receipts for the props.\" From recent correspondence email, I found the email titled 'Receipt for Stage Props Order' sent to Francis Wagner at 19:30:00. I will now send their given statement to Francis Wagner via messages. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A message is sent to Francis Wagner saying; "Hey man, I just passed on the receipts for the props" at 19:35 12th of December 2024. ',
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "send_message",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – Agent locates the recent email / recipient (Francis) via email tools
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
                # Milestone 1 – Confirm that the email to Francis about the props receipt was actually retrieved
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
                                                "value": "Receipt for Stage Props Order",
                                                "partial": False,
                                            },
                                            "recipients_addresses": {
                                                "value": "francis.wagner@orchardtheater.com",
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
                # Milestone 2 – A message is sent to Francis with the specified content at the specified time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Participants: Dawei (self) and Francis; we allow matching by email or phone for each
                                    "participants_addresses": [
                                        [
                                            (
                                                "dawei.shen@orchardtech.com",
                                                "+1 555-123-4567-8901",
                                            ),
                                            (
                                                "francis.wagner@orchardtheater.com",
                                                "+1 555-456-7890-1234",
                                            ),
                                        ]
                                    ],
                                    "content": "I just passed on the receipts for the props",
                                    "creation_datetime_iso": "2024-12-12T19:35:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
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
            milestone_edge_list=[
                (
                    0,
                    1,
                ),  # Email tools used → confirm props email to Francis was retrieved
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_29615c2b-6ab8-4f3e-91ad-da6b087f27c5_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "email",
                "messaging",
                "whatsapp_messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:30:00-08:00",
            is_read_time="2024-12-12T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to send Vickie Lee a message saying that you placed an order for theatre props already so that she doesn't need to do it.    Also mention that the other theatre friend's full name who already knew it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Can you message Vickie in our usual way and write "I placed an order for the theatre props already so you don\'t need to do it" and mention the theatre friend full name who already knew it via email in the message.',
                },
            ],
            reasoning='The user wants to notify Vickie Lee that the theatre-props order has already been placed and include the full name of the theatre friend who already knew it. I first locate the contact “Vickie Lee”, open our existing WhatsApp conversation, fetch the email with subject “Receipt for Stage Props Order” sent on 2024-12-12 19:30 to francis.wagner@orchardtheater.com, and send the message: "I placed an order for the theatre props already so you don’t need to do it." also mention Francis Wagner directly',
            success_conditions=[
                {
                    "input_text": 'The message "I placed an order for the theatre props already so you don\'t need to do it" and "Francis Wagner" was mentioned directly in that message is sent to Vickie Lee.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "send_message",
                "send_whatsapp_message",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0
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
                                    # Either of these tools would plausibly be used to fetch the email / attachment
                                    target_tools=[
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1: Vick contact found
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
                                                "value": "Vickie Lee",
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
                # Milestone 2: search for whatsapp messages
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
                                    # Either of these tools would plausibly be used to fetch the email / attachment
                                    target_tools=[
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 3: Conversation with Vickie Found
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
                                                "value": "Vickie Lee",
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
                        ),
                    ]
                ),
                # Milestone 4 – The agent looked up the email that has the props receipt
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
                                    # Either of these tools would plausibly be used to fetch the email / attachment
                                    target_tools=["search_emails", "get_all_emails"],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 5 – The returned result contains the email
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
                                            "recipients_addresses": {
                                                "value": [
                                                    "francis.wagner@orchardtheater.com"
                                                ],
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Receipt for Stage Props Order",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-12T19:30:00-08:00",
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
                            reference_milestone_node_index=4,  # depend on the search in Milestone 0
                        ),
                    ],
                ),
                # Milestone 6 – A new outgoing text / chat message was created to Vickie
                Milestone(
                    snapshot_constraints=[
                        # Verify the actual stateful change – new message in WHATSAPP DB.
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Vickie Lee",
                                    "content": "I placed an order for the theatre props",
                                    "creation_datetime_iso": "2024-12-12T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "conversation_name": column_exact_match_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Vickie Lee",
                                    "content": "francis",
                                    "creation_datetime_iso": "2024-12-12T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "conversation_name": column_exact_match_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
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
            name="DAWEI_SHEN_19_816a296f-fc54-44ab-912d-dfbdc7b0cdb2_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T13:25:00-08:00",
            is_read_time="2024-12-13T13:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know what time is dinner tomorrow as you want to schedule in a massage after your work week to relax. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is my event with Lukas and Vick as I need to add in an appointment.",
                },
            ],
            reasoning="Right, so the user wants to know the start time of their event, 'Dinner with Lukas and Vick'. I can see it is scheduled in their calendar for the 14th December at 19:00. I will relay this to the user.",
            success_conditions=[
                {
                    "input_text": "The event, 'Dinner with Lukas and Vick' scheduled for 14th December at 19:00 is announced to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the dinner event in the calendar
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
                # Milestone 1: Dinner Found
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
                                                "value": "Dinner with Lukas and Vick",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-14T19:00:00-08:00",
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
                # Milestone 2 – User is informed about the dinner time
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
                                            "7:00",  # 7:00 pm
                                            "19:00",  # 24-hour format
                                            "7 pm",
                                            "7pm",
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
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_2980c6ab-0a80-4913-acbe-65e50a9cf894_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:25:00-08:00",
            is_read_time="2024-12-12T19:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "After sending the prop receipts to Francis you want to meet with him to discuss further prop acquisition in the future. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Make an event called 'Prop Discussion' on Sunday at one and add Francis to it while you're at it. ",
                },
            ],
            reasoning="The user wants to make an event called 'Prop Discussion' on Sunday at one and add Francis to it. Francis refers to Francis Wagner, as he is the only Francis in contacts. The user themself, Dawei Shen, will also be an attendee by default. Because no duration was specified, I will schedule it for the default 30 minutes, 13:00 – 13:30, on Sunday, 15 December 2024. I will create the event titled 'Prop Discussion' for 13:00-13:30 on 15 December 2024 with attendees Dawei Shen and Francis Wagner.",
            success_conditions=[
                {
                    "input_text": "1. an event called 'Prop Discussion' with Francis Wagner as an invitee is created for 13:00-13:30 on 15th of December 2024",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up Francis in the contacts list
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
                # Milestone 1: Francis contact found
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
                                                "value": "Francis Wagner",
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
                # Milestone 2 – The “Prop Discussion” event is actually added to the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Prop Discussion",
                                    "start_datetime_iso": "2024-12-15T13:00:00-08:00",
                                    "attendees_names": [
                                        ["Dawei Shen", "Francis Wagner"]
                                    ],
                                    "creation_datetime_iso": "2024-12-12T19:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
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
                (0, 1),  # looked up contact → initiate calendar creation
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_8bbc3ee4-0ec2-4338-be8a-1e75b97adb60_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "email",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T10:20:00-08:00",
            is_read_time="2024-12-13T10:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You are currently out driving and notice you have a new email notification. As you are currently on the clock for work, you want to know who the most recent email is from. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who's my latest email from?",
                },
            ],
            reasoning='Okay so, the user wants to know who their latest email is from. I just need to search their recent emails and can see that the newest one is from Stefan Mustermann on the 12th December at 9:15, with the subject line "Re: Research Progress Update"',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that their most recent email, received on the 12th December at 9:15, is from Stefan Mustermann, with the subject line "Re: Research Progress Update"',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – The agent uses an email-retrieval tool to look for the latest email
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
                # Milestone 1 – Confirms that an email from Stefan Mustermann with the correct subject and time was retrieved as (one of) the results
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            # Validate the output of the email search in Milestone 0
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "sender_address": {
                                                "value": "stefan.mustermann@orchardtech.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Re: Research Progress Update",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-12T09:15:00-08:00",
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
                # Milestone 2 – The agent informs the user who the latest email is from, with subject and time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            # Check the user-facing response mentions sender name, subject, and approximate time
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We only require the critical details to appear in some form
                                    "content": [
                                        (
                                            "Stefan",  # sender first name
                                            "Mustermann",  # last name
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            # Separate constraint for subject phrase
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("Research Progress Update",)],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            # Separate constraint for mention of the time (9:15 or similar)
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("9:15", "9.15", "09:15")],
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
                (0, 1),  # Email search → confirm correct latest email retrieved
                (1, 2),  # Retrieved email → user informed with correct details
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_581d637d-ed7b-42af-b66d-8ce984c3b3fb_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "whatsapp_messaging",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:25:00-08:00",
            is_read_time="2024-12-12T19:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You checked out the link that Charles sent you about the props website, you want to send him a message thanking him and telling him you ordered a couple pieces. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a reply to Charles saying "Thanks for that Charles! Ordered us a couple bits.".',
                },
            ],
            reasoning='The user wants me to send a reply to a message that Charles sent saying "Thanks for that Charles! Ordered us a couple bits.". I\'m just going to check who Charles refers to - I found Charles Wilde in the user\'s contacts. I see recent WhatsApp messages from Charles Wilde, including the link to PropsSupplier.com. Since the user said "send a reply", it makes sense to answer on WhatsApp where the conversation is. I\'ll go ahead and send the requested reply to Charles Wilde on WhatsApp.',
            success_conditions=[
                {
                    "input_text": 'The system sends the message "Thanks for that Charles! Ordered us a couple bits." to Charles Wilde on WhatsApp.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_messages",
                "get_all_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – Returned WhatsApp message contains link from Charles Wilde
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
                                            "sender_name": {
                                                "value": "Charles Wilde",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "PropsSupplier.com",
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
                # Milestone 2 – a new WhatsApp message to Charles is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least Charles’ number must be among the participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "charles.wilde@orchardtheater.com",
                                                "+1 555-234-5678-9012",
                                            )
                                        ]
                                    ],
                                    # Body should clearly thank Charles / mention ordering
                                    "content": "Thanks for that Charles! Ordered us a couple bits.",
                                    "creation_datetime_iso": "2024-12-12T19:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial state
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_9e65db4f-668a-40ae-93bb-0b8413fa71a6_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "whatsapp_messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:40:00-08:00",
            is_read_time="2024-12-12T19:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to send a message to Charles letting him know you emailed the receipt to Francis "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell Charles via WhatsApp that I emailed the receipt to Francis.",
                },
            ],
            reasoning="The user would like me to tell Charles via WhatsApp that he emailed the receipt to Francis. Looking through the user's contacts there is only one contact named Charles. The user also has an existing WhatsApp chat with Charles so I will assume Charles Wilde is the intended recipient. I'll write \"I emailed receipt to Francis.\" and present it to the user. With their approval I will send the message.",
            success_conditions=[
                {
                    "input_text": 'A WhatsApp message is sent to Charles Wilde saying "I emailed receipt to Francis."',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "search_contacts",
                "get_all_contacts",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0: Check if search contacts initiated (rehearsal was not marked in calendar)
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
                # Milestone 1: Found related person's email
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
                                                "value": "Charles Wilde",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "charles.wilde@orchardtheater.com",
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
                # Milestone 2 – new WhatsApp message to Charles confirming the receipt was emailed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require Charles to be one of the participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "charles.wilde@orchardtheater.com",
                                                "+1 555-234-5678-9012",
                                            )
                                        ]
                                    ],
                                    "content": "I emailed receipt to Francis.",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-12T19:40:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
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
            name="DAWEI_SHEN_19_da1a40a4-f2f9-4e01-87e1-e6ea506e8a99_single_turn_3",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "whatsapp_messaging",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T12:00:00-08:00",
            is_read_time="2024-12-14T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You forgot to order a certain prop and want to see the link to the online supplier that Charles Wilde sent to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you pull up the message from my theater buddy with the link to the theater item seller.",
                },
            ],
            reasoning="The user wants to see a WhatsApp message from their theater buddy containing a link to a theater item seller, first I will determine which contact the user is talking about. \n\nLooking through the user’s contacts I can see that Charles Wilde and Vickie Lee are both tagged as Theater Friends. I will now search through the user’s WhatsApp messages with each contact to find the corresponding link.\n\nI can’t see any link to a theater item seller, however I can see in the WhatsApp thread with Charles Wilde that the user has been sent a link to a prop supplier.Due to the similarity of these phrases I will assume that this is what the user is referring to.\n\n I will now present the WhatsApp message with the link to the prop supplier to the user.",
            success_conditions=[
                {
                    "input_text": "1. WhatsApp message from Charles Wilde containing the link to PropsSupplier.com is presented.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_messages",
                "get_all_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent looks up Francis in the contacts list
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
                # Milestone 1: Charles contact found
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
                                                "value": "Charles Wilde",
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
                # Milestone 2 – The agent looks up WhatsApp messages
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 3 – The returned WhatsApp message is the one from Charles with the prop-supplier link
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
                                            "sender_name": {
                                                "value": "Charles Wilde",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "PropsSupplier.com",
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
                                "content": column_one_similarity,
                            },
                            reference_milestone_node_index=2,
                        )
                    ],
                ),
                # Milestone 4 – The user is shown the supplier link
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "PropsSupplier.com",
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
                (2, 3),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_da1a40a4-f2f9-4e01-87e1-e6ea506e8a99_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "whatsapp_messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T12:00:00-08:00",
            is_read_time="2024-12-14T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You forgot to order a certain prop and want to see the link to the online supplier that Charles Wilde sent to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you pull up the WhatsApp message from my theater buddy with the link to the prop supplier.",
                },
            ],
            reasoning="The user wants to see a WhatsApp message from their theater buddy containing a link to a prop supplier, first I will determine which contact the user is talking about. \n\nLooking through the user’s contacts I can see that Charles Wilde and Vickie Lee are both tagged as Theater Friends. I will now search through the user’s WhatsApp messages with each contact to find the corresponding link.\n\nI can see in the WhatsApp thread with Charles Wilde that the user has been sent a link to a prop supplier. I will now present the WhatsApp message with the link to the prop supplier to the user.",
            success_conditions=[
                {
                    "input_text": "1. WhatsApp message from Charles Wilde containing the link to PropsSupplier.com is presented.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent looks up Francis in the contacts list
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
                # Milestone 1: Charles contact found
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
                                                "value": "Charles Wilde",
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
                # Milestone 2 – The agent looks up WhatsApp messages
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 3 – The returned WhatsApp message is the one from Charles with the prop-supplier link
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
                                            "sender_name": {
                                                "value": "Charles Wilde",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "PropsSupplier.com",
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
                                "content": column_one_similarity,
                            },
                            reference_milestone_node_index=2,
                        )
                    ],
                ),
                # Milestone 4 – The user is shown the supplier link
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "PropsSupplier.com",
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
                (2, 3),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_9e65db4f-668a-40ae-93bb-0b8413fa71a6_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "whatsapp_messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:40:00-08:00",
            is_read_time="2024-12-12T19:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to send a message to Charles letting him know you emailed the receipt to Francis "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell my theater friend, not Vickie, via WhatsApp that I emailed the receipt to Francis.",
                },
            ],
            reasoning="The user would like me to tell his theater friend via WhatsApp that he emailed the receipt to Francis. Looking through the user's contacts there are two different people described as theater friend so I will ask the user to specify who they wish to message. Charles Wilde is the intended recipient. I'll write \"I emailed the receipt to Francis\" and present it to the user. With their approval I will send the message.",
            success_conditions=[
                {
                    "input_text": '1. A WhatsApp message is sent to Charles Wilde saying "I just emailed the receipt to Francis."',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "search_contacts",
                "get_all_contacts",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – a WhatsApp send action was invoked
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
                # Milestone 1: Charles contact found
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
                                                "value": "Charles Wilde",
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
                # Milestone 2 – new WhatsApp message to Charles confirming the receipt was emailed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require Charles to be one of the participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "charles.wilde@orchardtheater.com",
                                                "+1 555-234-5678-9012",
                                            )
                                        ]
                                    ],
                                    "content": "receipt to Francis",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-12T19:40:00-08:00",
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
            name="DAWEI_SHEN_19_581d637d-ed7b-42af-b66d-8ce984c3b3fb_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "whatsapp_messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:25:00-08:00",
            is_read_time="2024-12-12T19:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You checked out the link that Charles sent you about the props website, you want to send him a message thanking him and telling him you ordered a couple pieces. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a reply to Charles on WhatsApp saying "Thanks for that Charles! Ordered us a couple bits.".',
                },
            ],
            reasoning='The user wants to send a WhatsApp reply to Charles (contact: +1 555-234-5678-9012 / charles.wilde@orchardtheater.com) saying "Thanks for that Charles! Ordered us a couple bits.". I will locate that chat and send the message.',
            success_conditions=[
                {
                    "input_text": 'The message "Thanks for that Charles! Ordered us a couple bits." is sent to Charles Wilde on WhatsApp.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – a new WhatsApp message to Charles is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least Charles’ number must be among the participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "charles.wilde@orchardtheater.com",
                                                "+1 555-234-5678-9012",
                                            )
                                        ]
                                    ],
                                    # Body should clearly thank Charles / mention ordering
                                    "content": "Thanks for that Charles! Ordered us a couple bits.",
                                    "creation_datetime_iso": "2024-12-12T19:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial state
                        )
                    ]
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_cbf4696d-abfe-46e3-9682-97c372db12a1_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "messaging",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T14:55:00-08:00",
            is_read_time="2024-12-14T14:55:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You're not sure if you remembered to send the stage props order receipt to Francis, so you ask your assistant to check. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I send Francis the stage props receipt? Yes or No.",
                },
            ],
            reasoning="The user wants to know whether they sent Francis the stage props receipt. I'll check their communication channels.\n\nI didn't find any text messages with any contact named Francis. I did find an email that the user sent to Francis Wagner on December 12th 2024 at 19:30. I'll have a look at the email content now.\n\nThe subject line of this email is Receipt for Stage Props Order, and the body of the email states that the receipt for the order for stage props is attached. Great, this must be what the user was looking for. I'll go ahead and let them know that they did send the stage props order receipt to Francis via email on December 12th 2024.",
            success_conditions=[
                {
                    "input_text": "1. User is informed with Yes, that they emailed Francis Wagner with the receipt for stage props order on December 12th 2024.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "search_messages",
                "get_all_messages",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks through emails
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
                # Milestone 1 – The searched emails contain (at least) the receipt sent to Francis
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
                                            "recipients_addresses": {
                                                "value": [
                                                    "francis.wagner@orchardtheater.com",
                                                ],
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Receipt",
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
                                    "content": "{matched}",  # will be replaced by extractor output
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                        )
                    ],
                ),
                # Milestone 2 – User is informed that the email/receipt was already sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "yes",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_similarity,
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Search emails ➜ confirm receipt email exists
                (1, 2),  # Confirmation ➜ inform the user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_89674089-f422-4b83-86dc-8aa0c5d179a8_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T13:00:00-08:00",
            is_read_time="2024-12-13T13:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to ask Francis Wagner where the props for the theater show should be delivered to. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text Francis asking where the props should be delivered to. ",
                },
            ],
            reasoning="The user wants to send a text to Francis asking where the props should be delivered to, first I need to find out which contact they are referring to.\nThe user has a contact named Francis Wagner, I will assume that this contact in question.\nI will draft a message to him containing the user's query.\nWith the user's confirmation I will send the text.",
            success_conditions=[
                {
                    "input_text": '1. Text message sent to Francis Wagner containing the phrase "where should the props be delivered to".',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["send_message", "search_contacts", "get_all_contacts"],
            milestones=[
                # Milestone 0 – the agent looked up Francis Wagner’s contact information
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
                # Milestone 1: Francis contact found
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
                                                "value": "Francis Wagner",
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
                # Milestone 2 – a text message to Francis Wagner was sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Confirm Francis’ phone appears among the participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "francis.wagner@orchardtheater.com",
                                                "+1 555-456-7890-1234",
                                            )
                                        ]
                                    ],
                                    # Confirm the core question about delivery location is in the body
                                    "content": "where should the props be delivered to",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-13T13:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_9fa879eb-8355-4622-bc61-cdcdc5102a2f_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "calendar",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:35:00-08:00",
            is_read_time="2024-12-12T19:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "After sending the prop receipt to Francis, you want to meet with them to discuss further prop acquisition in the future.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Make an event called 'Prop Discussion' on Sunday at one pm and add Francis to it. ",
                },
            ],
            reasoning="The user wants to make an event called 'Prop Discussion' on Sunday at one and add Francis to it. I believe Francis refers to Francis Wagner as there is no other Francis in their contacts. I will add them as an invitee. They have given me the event title so I will call the event 'Prop Discussion.' The user wants to schedule it for Sunday at one so but didn't specify a duration so I will set the event to run from 13:00-13:30; the default duration. I will now create an event called 'Prop Discussion' for 13:00-13:30 on Sunday 15th of December 2024. ",
            success_conditions=[
                {
                    "input_text": "1. An event called 'Prop Discussion' with Francis Wagner as an invitee is created for 13:00-13:30 on 15th of December 2024",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up contacts to resolve "Francis"
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
                # Milestone 1 – Confirm that Francis Wagner is retrieved from contact search in Milestone 0
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
                                                "value": "Francis Wagner",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "francis.wagner@orchardtheater.com",
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
                # Milestone 2 – Calendar event "Prop Discussion" created on Sunday 2024-12-15, 13:00–13:30 with Francis as attendee
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Prop Discussion",
                                    "start_datetime_iso": "2024-12-15T13:00:00-08:00",
                                    "end_datetime_iso": "2024-12-15T13:30:00-08:00",
                                    "attendees_names": [["Francis Wagner"]],
                                    "creation_datetime_iso": "2024-12-12T19:35:00-08:00",
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
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # contact lookup → confirm Francis
                (1, 2),  # Francis resolved → event created with Francis as attendee
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_3e210596-0a3c-4865-b58c-d1afffecb2ae_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "whatsapp_messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:20:00-08:00",
            is_read_time="2024-12-12T19:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know let Charles know you've ordered the props through the supplier he sent to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a new Whatsapp Message to Charles Wilde, tell him Hey Charlie, I've got everything ordered for Cambodian Rock Band.",
                },
            ],
            reasoning="The user wants to send a message. I'll first have to find out to whom. I see only one Charles in their contacts so I know they mean to message Charles Wilde. Next I need to know what they'd like to say to Charles Wilde. Then I'm ready to send the message.",
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Charles Wilde to say "Hey Charlie, I\'ve got everything ordered for Cambodian Rock Band.".',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – a WhatsApp send action was invoked
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
                # Milestone 1: Charles contact found
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
                                                "value": "Charles Wilde",
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
                # Milestone 2 – a new outgoing message to Charles is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [
                                            (
                                                "charles.wilde@orchardtheater.com",
                                                "+1 555-234-5678-9012",
                                            )
                                        ]
                                    ],
                                    "content": "Cambodian Rock Band",
                                    "creation_datetime_iso": "2024-12-12T19:20:00-08:00",
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
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_cb83121e-5f5a-4b15-910a-594efddb501b_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T21:00:00-08:00",
            is_read_time="2024-12-12T21:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to be told when you're having Dinner with Lukas and Vick. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When am I having dinner with Lukas and Vick?",
                },
            ],
            reasoning="The user wants to know when their calendar event dinner with Lukas and Vick is happening. I will check the calendar for this event. I found the event. It takes place on Saturday 14th December 2024 from 19:00 to 21:00. As the user uses the 12 hour clock on their phone I will present the time to them in the same format. I tell the user that the event will take place on Saturday 14 December from 7pm to 9pm.",
            success_conditions=[
                {
                    "input_text": "The time and date of the event Dinner with Lukas and Vick, Saturday 14 December 2024 from 19:00 to 21:00, is present to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent looks up calendar information
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
                # Milestone 1 – The correct dinner event is present in the calendar results
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
                                                "value": "Dinner with Lukas and Vick",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-14T19:00:00-08:00",
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
                # Milestone 2 – The user is informed of the correct date and time
                Milestone(
                    snapshot_constraints=[
                        # Date mentioned (allowing either ordering)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "December 14",
                                            "12-14",
                                            "12/14",
                                            "Dec 14",
                                            "14 December",
                                            "14th of December",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                            },
                        ),
                        # Time mentioned (allowing 12- or 24-hour format)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("7 pm", "7pm", "19:00", "7:00")],
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
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_9fa879eb-8355-4622-bc61-cdcdc5102a2f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "calendar",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:35:00-08:00",
            is_read_time="2024-12-12T19:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "After sending the prop receipt to Francis, you want to meet with them to discuss further prop acquisition in the future.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Could you make an event on Sunday to discuss props with Francis around lunch time at 1?",
                },
            ],
            reasoning="Ok, so the user wants to create an event on Sunday to discuss props with Francis around lunch time. I believe Francis refers to Francis Wagner, as there is no other Francis in their contacts. I will add them as an invitee. The purpose of the event is clear based on the user query, so I will name the event 'Prop Discussion.' The user wants to schedule it for Sunday around lunch time. The user query is on December 12, Thursday, so the user is likely to be referring to Sunday, December 15. The user wants the event to happen around lunch time, so 13:00 PM can be an option. When looking at the calendar, the user seems free on this day at this time, so I will pencil this event in for 13:00. The user didn't specify a duration so I will set it for the default length of time, that is, 30 minutes. I will now create an event called 'Prop Discussion' on Sunday 15th of December 2024 between 13:00-13:30. ",
            success_conditions=[
                {
                    "input_text": "1. An event called 'Prop Discussion' with Francis Wagner as an invitee is created for 13:00-13:30 on 15th of December 2024",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up Francis in contacts (by name / email / role)
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
                # Milestone 1 – Confirms Francis Wagner (Theater Manager) was retrieved from contact search
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
                                                "value": "Francis Wagner",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "francis.wagner@orchardtheater.com",
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
                # Milestone 2 – Calendar event "Prop Discussion" created for Sunday Dec 15, 2024 13:00–13:30 with Francis as attendee
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Prop",
                                    "start_datetime_iso": "2024-12-15T13:00:00-08:00",
                                    "end_datetime_iso": "2024-12-15T13:30:00-08:00",
                                    "attendees_names": [["Francis Wagner"]],
                                    "creation_datetime_iso": "2024-12-12T19:35:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "attendees_names": column_list_subset_match_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → confirm Francis found
                (
                    1,
                    2,
                ),  # Francis identified → create calendar event with Francis invited
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_c42ea828-ca42-4a35-8913-ef29b790d1f4_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "whatsapp_messaging",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:15:00-08:00",
            is_read_time="2024-12-12T19:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to browse the theatre prop suppliers website. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read Charles message and show the messages with any links",
                },
            ],
            reasoning="The user would like the content of their recent WhatsApp message from their contact, Charles Wilde, to be read to them. I will search for Charles’s latest WhatsApp message, read it to the user, and if the message contains a link (e.g., “PropsSupplier.com”), I will show the message to them.",
            success_conditions=[
                {
                    "input_text": "The assistant reads the most recent message from Charles Wilde to the user.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "The assistant presents the message with link “PropsSupplier.com” to the user.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_messages",
                "get_all_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent inspects WhatsApp messages
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – The returned WhatsApp result contains Charles’s latest message with the supplier link
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
                                            "sender_name": {
                                                "value": "Charles Wilde",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "PropsSupplier.com",
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
                            reference_milestone_node_index=0,  # use output of milestone 0
                        ),
                    ],
                ),
                # Milestone 2 – The agent informs the user and references or opens the link
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "PropsSupplier.com",
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
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_89674089-f422-4b83-86dc-8aa0c5d179a8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T13:00:00-08:00",
            is_read_time="2024-12-13T13:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to ask Francis Wagner where the props for the theater show should be delivered to. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text my theater manager asking where the props should be delivered to. ",
                },
            ],
            reasoning="The user wants to send a text to their theater manager asking where the props should be delivered to, first I need to find out which contact they are referring to as theatre manager.\nI will search through the user's calendar events, messages, and emails to look for a contact matching this query. The user received an email from a Francis Wagner, regarding a rehearsal schedule, I will assume that this schedule is for theater, and that this contact is the manager in question.\nI will find Francis Wagner's corresponding phone number and draft a message to him containing the user's query.\nWith the user's confirmation I will send the text.",
            success_conditions=[
                {
                    "input_text": '1. Text message sent to Francis Wagner containing the phrase "where should the props be delivered to".',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – the agent looked up Francis Wagner’s contact information
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
                # Milestone 1: Francis contact found
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
                                                "value": "Francis Wagner",
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
                # Milestone 2 – a text message to Francis Wagner was sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Confirm Francis’ phone appears among the participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "francis.wagner@orchardtheater.com",
                                                "+1 555-456-7890-1234",
                                            )
                                        ]
                                    ],
                                    # Confirm the core question about delivery location is in the body
                                    "content": "where should the props be delivered to",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-13T13:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_cbf4696d-abfe-46e3-9682-97c372db12a1_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "email",
                "messaging",
                "whatsapp_messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T14:55:00-08:00",
            is_read_time="2024-12-14T14:55:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You're not sure if you remembered to send the stage props order receipt to Francis, so you ask your assistant to check. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I remember to send the receipt to the theatre manager? Yes or No.",
                },
            ],
            reasoning="The user wants to know if they sent a receipt to the theatre manager. First I'll need to figure out who the theatre manager is.\n\nBy checking the user's contacts I can see that Francis Wagner is listed as Theatre Manager. Now I'll see if I can find any communications with Francis Wagner mentioning a receipt.\n\nI didn't find any text messages with Francis Wagner. I did find an email that the user sent to Francis Wagner on December 12th 2024 at 19:30. I'll have a look at the email content now.\n\nThe email's subject line is Receipt for Stage Props Order, and the body of the email states that the receipt for the order for stage props is attached. I can't find any other emails to Francis Wagner that mention a receipt, so I will assume that this is the receipt the user wanted to send.\n\nNow I can inform the user that they emailed Francis Wagner the receipt for an order for stage props on December 12th 2024.",
            success_conditions=[
                {
                    "input_text": "1. User is informed that they emailed Francis Wagner with the receipt for stage props order on December 12th 2024.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "search_messages",
                "get_all_messages",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0: agent search contacts
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
                                        "get_all_contacts",
                                        "search_contacts",
                                    ],
                                ),
                            },
                        )
                    ]
                ),
                # Milestone 1: Francis contact found
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
                                                "value": "Francis Wagner",
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
                # Milestone 2 – the agent looks through the mailbox
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
                # Milestone 3 – the queried email to Francis is indeed found
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
                                                "value": "Receipt",
                                                "partial": True,
                                            },
                                            "recipients_addresses": {
                                                "value": [
                                                    "francis.wagner@orchardtheater.com"
                                                ],
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
                            reference_milestone_node_index=2,
                        )
                    ],
                ),
                # Milestone 4 – the user is informed of the result
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "yes",
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
                (0, 1),
                (2, 3),
            ],
        ),
    ]
