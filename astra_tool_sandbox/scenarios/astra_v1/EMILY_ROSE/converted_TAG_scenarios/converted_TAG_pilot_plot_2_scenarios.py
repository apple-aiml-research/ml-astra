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
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_rouge_l_similarity,
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


def get_TAG_EMILY_ROSE_pilot_plot_2(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="EMILY_ROSE_2_2d3a91be-b115-4e19-b576-fdbc7ae22bf8_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T16:20:00-08:00",
            is_read_time="2024-12-11T16:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Jenna has been so helpful you want to go all out for her birthday but need to be reminded when that is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is the event planner's birthday?",
                },
            ],
            reasoning="The user wants to know when is the event planner's birthday. I should first figure out who the event planner is. I should check the user's Contacts for one with that name. \n\nHmm, seems like there is no contact with that name. Event planner sounds like a job title so I should check the jobs of the Contacts to see if that is it. Looks like Jenna Miles has a job of event planner so this must be who the user means. \n\nNext I will check Jenna's contact card for her birthday. Jenna's birthday is the 14 February 1991. I will tell the user this. \n",
            success_conditions=[
                {
                    "input_text": "1. User is informed Jenna Miles' birthday is the 14 February 1991.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_contacts", "get_all_contacts"],
            milestones=[
                # Milestone 0 – The agent looks up contacts (either via search_contacts or get_all_contacts)
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
                # Milestone 1 – Confirm that Jenna Miles (Event Planner) with her birthday was returned
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
                                                "value": "Jenna Miles",
                                                "partial": False,
                                            },
                                            "job_title": {
                                                "value": "Event Planner",
                                                "partial": False,
                                            },
                                            "birthday": {
                                                "value": "1991-02-14T00:00:00-08:00",
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
                # Milestone 2 – The agent tells the user Jenna’s birthday (must mention February 14, 1991)
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
                                            "February 14",
                                            "14 February",
                                            "Feb 14",
                                            "14 Feb",
                                            "14th of February",
                                            "2/14",
                                            "02/14",
                                            "1991-02-14",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
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
            name="EMILY_ROSE_2_3eafcb54-d4eb-4e02-bd90-e5d58c1d0429_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T10:00:00-08:00",
            is_read_time="2024-12-03T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know who you sent your email to about the Christmas charity event. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who did I send that Christmas charity event email to?",
                },
            ],
            reasoning="Right so, the user wants to know who were the recipients of the 'Christmas charity event email'. Firstly I will check their Mail. I can see one email matching their request, with the subject 'Summary of Today's Meeting on Christmas Charity Event'. The email was sent on 2 December 2024 at 11:45 to Michael Thompson and Jenna Miles. This is the information the user is looking for and then I can then display this to the user.",
            success_conditions=[
                {
                    "input_text": "1. The email sent to Michael Thompson and Jenna Miles on 2 December 2024 at 11:45 with the subject 'Summary of Today's Meeting on Christmas Charity Event' is found.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. User has been told Michael Thompson and Jenna Miles are the recipients."
                },
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – Agent uses an email-retrieval tool
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
                        ),
                    ],
                ),
                # Milestone 1 – Returned email thread contains the expected Christmas charity email
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
                                                "value": "Summary of Today's Meeting on Christmas Charity Event",
                                                "partial": False,
                                            },
                                            "recipients_addresses": {
                                                "value": [
                                                    "michael.thompson@orchardcommunity.org",
                                                    "jenna.miles@orchardcommunity.org",
                                                ],
                                                "partial": True,  # allow list order flexibility
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
                # Milestone 2 – Agent’s reply to the user includes both recipient names
                Milestone(
                    snapshot_constraints=[
                        # Must mention Michael Thompson
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Michael Thompson",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Must mention Jenna Miles
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Jenna Miles",
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
                (0, 1),  # Tool call → verify retrieved email
                (1, 2),  # Retrieved email → verify user-facing response
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_e6ea54c5-90fd-4b79-a579-c9ca07c46443_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T12:00:00-08:00",
            is_read_time="2024-12-02T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to have the last email you sent read aloud. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read the last email I sent out loud.",
                },
            ],
            reasoning="The user wants the last email they sent read aloud. Let me look for it. Found it. I will read it out for them.",
            success_conditions=[
                {
                    "input_text": "1. The email sent from emily.rose@orchardcommunity.org at 11:45 on December 2nd including the text 'Hello Michael and Jenna' is read aloud.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – The agent looks up emails to identify the last one they sent
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
                # Milestone 1 – Confirm that the email returned from the previous tool call
                # is the one sent by Emily Rose on Dec-02-2024 11:45 containing the greeting
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
                                                "value": "emily.rose@orchardcommunity.org",
                                                "partial": False,
                                            },
                                            "body": {
                                                "value": "Hello Michael and Jenna",
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
                # Milestone 2 – The agent reads the email aloud to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Hello Michael and Jenna",
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
                (0, 1),  # Email lookup → verify correct email retrieved
                (1, 2),  # Verified email → user-facing reading
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_9d0f3a82-fdf4-41c1-b1a4-04c138ba9d24_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_2",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T12:30:00-08:00",
            is_read_time="2024-12-02T12:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You are free for the rest of your day and want to see if a friend is free to hang out. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Message Nathan saying hey, any plans for the rest of the day",
                },
            ],
            reasoning="The user wants to message a contact named Nathan Blake. First I'll locate this contact and find any existing message threads with them, and then I'll add the text provided by the user as a draft before seeking confirmation to send.",
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Nathan Blake saying "hey, any plans for the rest of the day”',
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
                # Milestone 0 – A contact lookup is made (either direct list or search)
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
                # Milestone 1 – The lookup result actually included Nathan Blake
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
                                                "value": "Nathan Blake",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 530-555-0129",
                                                "partial": False,
                                            },
                                            # email match is optional – phone is enough
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
                # Milestone 2 – A new outgoing message to Nathan with the intended text exists
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least one of Nathan's identifiers must be present, and no unrelated participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "nathan.blake@eventpros.com",
                                                "+1 530-555-0129",
                                            )
                                        ]
                                    ],
                                    "content": "any plans for the rest of the day",
                                    "creation_datetime_iso": "2024-12-02T12:30:00-08:00",
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
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → verify Nathan found
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_dbfd76ed-8bfe-4293-92ba-891227c7060c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "email",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T16:00:00-08:00",
            is_read_time="2024-12-02T16:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Jenna told you she never got the email, you want to check what time you sent it at so you can confront her. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I email the manager and event planner?",
                },
            ],
            reasoning="The user is asking me about an email.\nI should check their inbox and find the email being referred to.\nThe user has referred to a manager and event planner, I should check their contacts to find matching people. \nI can see that Michael Thompson works as a manager, while Jenna Miles works as an event planner. I am confident these are the correct recipients.\nI can see only one email sent to Michael Thompson and Jenna Miles, sent at 11:45 on December 02, 2024. \nI should inform the user.",
            success_conditions=[
                {
                    "input_text": '1. Time email with subject line "Summary of Today\'s Meeting on Christmas Charity Event" was sent is confirmed as 11:45 on December 02, 2024',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – the agent looks through the email store
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
                # Milestone 1 – the retrieved email matches the expected subject and timestamp
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
                                                "value": "Summary of Today's Meeting on Christmas Charity Event",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-02T11:45:00-08:00",
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
                # Milestone 2 – the agent tells the user the correct send time
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
                                            "11:45",
                                            "11:45 am",
                                            "11:45am",
                                            "11:45 a.m.",
                                            "11:45 AM",
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
                (0, 1),  # email search → verify correct email retrieved
                (1, 2),  # verified retrieval → user informed
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_d94dda1a-477c-4e98-bb6c-a8c04b516f9b_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T12:00:00-08:00",
            is_read_time="2024-12-02T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to set aside some time to make sure you've reviewed the notes you made on the meeting to make sure everything is covered. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set aside some time around 2 so I can be sure I've covered everything in the meeting notes. ",
                },
            ],
            reasoning='Ok so the user wants to set aside some time around 2 to make sure they\'ve covered everything in the meeting notes. First I\'ll name the event something that means the events intent is clear. As the intent is to review the meeting notes I will name the event "Review Meeting Notes." Next is the time in which the event will take place. The user has given most of the details but has not specified a run time. I will set it to the default runtime of half an hour which the user may change if they need more time. I will now create the event "Review Meeting Notes" for 14:00-14:30 on 2 December 2024 at 12:00 on 2 December 2024. ',
            success_conditions=[
                {
                    "input_text": '1. The event "Review Meeting Notes" is created for 14:00-14:30 on 2 December 2024 at 12:00 on 2 December 2024. ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "create_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – verify that the calendar entry was created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Review Meeting Notes",
                                    "start_datetime_iso": "2024-12-02T14:00:00-08:00",
                                    "end_datetime_iso": "2024-12-02T14:30:00-08:00",
                                    "creation_datetime_iso": "2024-12-02T12:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            # Only match the critical fields; defaults are fine for others
                            reference_milestone_node_index=-1,  # compare with the pre-task snapshot
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_1e2bc562-b54b-4979-addc-c5d4a33ec6f2_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "contact",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T16:20:00-08:00",
            is_read_time="2024-12-11T16:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Jenna has been so helpful you want to go all out for her birthday but need to be reminded when that is.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is the event planner's birthday?",
                },
            ],
            reasoning="The user wants to know when is the event planner's birthday. I should first figure out who the event planner is. I should check the user's Contacts for one with that name. \n\nHmm, seems like there is no contact with that name. Event planner sounds like a job title so I should check the jobs of the Contacts to see if that is it. Looks like Jenna Miles has a job of event planner so this must be who the user means. \n\nNext I will check Jenna's contact card for her birthday. Jenna's birthday is the 14 February 1991. I will tell the user this. \n",
            success_conditions=[
                {
                    "input_text": "1. User is informed Jenna Miles' birthday is the 14 February 1991.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – The agent uses contacts tool(s) to look up the event planner
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
                # Milestone 1 – Confirms Jenna Miles (Event Planner) was found in contacts in Milestone 0
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
                                                "value": "Jenna Miles",
                                                "partial": False,
                                            },
                                            "job_title": {
                                                "value": "Event Planner",
                                                "partial": False,
                                            },
                                            "birthday": {
                                                "value": "1991-02-14",
                                                "partial": True,  # allow timezone suffix or full ISO
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
                # Milestone 2 – The agent tells the user Jenna's birthday correctly (14 February 1991)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We only require mention of date and year; phrasing can vary.
                                    "content": [
                                        (
                                            "February 14, 1991",
                                            "14 February 1991",
                                            "1991-02-14",
                                            "February 14",
                                            "Feb 14",
                                            "14 February",
                                            "14 Feb",
                                            "14th of February",
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
                (0, 1),  # Contact lookup → confirm Jenna and her birthday
                (1, 2),  # Correct birthday retrieved → inform user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_d94dda1a-477c-4e98-bb6c-a8c04b516f9b_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T12:00:00-08:00",
            is_read_time="2024-12-02T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to set aside some time to make sure you've reviewed the notes you made on the meeting to make sure everything is covered. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Create an event "Review Meeting Notes" for 14:00-14:30 today. ',
                },
            ],
            reasoning='Ok so the user wants to create an event "Review Meeting Notes" for 14:00-14:30 today. First is the name which is given by the user. Next is the timeframe which is given by the user. I will now create the event "Review Meeting Notes" for 14:00-14:30 on 2 December 2024 at 12:00 on 2 December 2024. ',
            success_conditions=[
                {
                    "input_text": '1. The event "Review Meeting Notes" is created for 14:00-14:30 on 2 December 2024 at 12:00 on 2 December 2024. ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "create_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Verify that a new calendar entry called
                # “Review Meeting Notes” has been added for 14:00-14:30 on
                # 2024-12-02.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Review Meeting Notes",
                                    "start_datetime_iso": "2024-12-02T14:00:00",
                                    "end_datetime_iso": "2024-12-02T14:30:00",
                                    "creation_datetime_iso": "2024-12-02T12:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Event name must match exactly
                                "calendar_event_name": column_exact_match_similarity,
                                # Datetimes: allow timezone or seconds differences by
                                # only requiring the key portion to appear.
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial state
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_1e2bc562-b54b-4979-addc-c5d4a33ec6f2_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "contact",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T16:20:00-08:00",
            is_read_time="2024-12-11T16:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Jenna has been so helpful you want to go all out for her birthday but need to be reminded when that is.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is Jenna's birthday?",
                },
            ],
            reasoning="The user wants to know when Jenna's birthday is. I should first figure out who Jenna is. I will check the user's Contacts for a Jenna. \n\nLooks like there is only one Jenna, Jenna Miles, so this must be who the user means. Next I will check Jenna's contact card for her birthday. It's 14 February 1991 so I'll tell the user.\n\nJenna's birthday is the 14 February 1991. I will tell the user this. ",
            success_conditions=[
                {
                    "input_text": "1. User is informed Jenna Miles' birthday is the 14 February 1991.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – The agent looks up contacts to find Jenna
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
                # Milestone 1 – Confirms Jenna Miles was retrieved with her birthday field
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
                                                "value": "Jenna Miles",
                                                "partial": False,
                                            },
                                            "birthday": {
                                                "value": "1991-02-14",
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
                # Milestone 2 – The agent tells the user Jenna's correct birthday (14 February 1991)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We just need to see that the response mentions Feb 14, 1991 in some form
                                    "content": [
                                        (
                                            "February 14, 1991",
                                            "14 February 1991",
                                            "1991-02-14",
                                            "February 14",
                                            "Feb 14",
                                            "14 February",
                                            "14 Feb",
                                            "14th of February",
                                        )
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
                (0, 1),  # Contact lookup → confirm Jenna and her birthday
                (1, 2),  # Having retrieved Jenna's birthday → informing the user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_3f095950-133f-40fa-8b1f-35a8345adad0_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T12:30:00-08:00",
            is_read_time="2024-12-02T12:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You are free for the rest of your day and want to see if your event helper is free to hang out. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Message the Event Helper saying hey, any plans for the rest of the day",
                },
            ],
            reasoning="The user wants to message a contact referring to them as Event Helper. First I'll locate this contact, it appears to be Nathan Blake as his alias is Event Helper, and find any existing message threads with them, and then I'll add the text provided by the user as a draft before seeking confirmation to send.",
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Nathan Blake saying "hey, any plans for the rest of the day”',
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
                # Milestone 0 – The agent looks up the contact information
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
                # Milestone 1 – Confirm that the returned contact is Nathan Blake (alias Event Helper)
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
                                                "value": "Nathan Blake",
                                                "partial": False,
                                            },
                                            "alias": {
                                                "value": "Event Helper",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 530-555-0129",
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
                # Milestone 2 – A new outgoing message was sent to Nathan with the requested content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require that at least one identifier for Nathan appears among the participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "+1 530-555-0129",
                                                "nathan.blake@eventpros.com",
                                            )
                                        ]
                                    ],
                                    "content": "hey, any plans for the rest of the day",
                                    "creation_datetime_iso": "2024-12-02T12:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to pre-task snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # contact lookup → confirm correct contact
                (1, 2),  # contact confirmed → message sent
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_dbfd76ed-8bfe-4293-92ba-891227c7060c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T16:00:00-08:00",
            is_read_time="2024-12-02T16:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Jenna told you she never got the email, you want to check what time you sent it at so you can confront her. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I email Michael Thompson and Jenna Miles.",
                },
            ],
            reasoning="The user is asking me about an email.\nI should check their inbox and find the email being referred to.\nI can see only one email sent to Michael Thompson and Jenna Miles, sent at 11:45 on December 02, 2024. \nI should inform the user.",
            success_conditions=[
                {
                    "input_text": '1. Time email with subject line "Summary of Today\'s Meeting on Christmas Charity Event" was sent is confirmed as 11:45 on December 02, 2024',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looks through email records
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
                # Milestone 1 – Correct email (subject, timestamp, recipients) was present in the tool output
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
                                                "value": "Summary of Today's Meeting on Christmas Charity Event",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-02T11:45:00-08:00",
                                                "partial": False,
                                            },
                                            "recipients_addresses": {
                                                "value": [
                                                    "michael.thompson@orchardcommunity.org",
                                                    "jenna.miles@orchardcommunity.org",
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
                                        (
                                            "11:45",
                                            "11:45 AM",
                                            "11:45am",
                                            "11:45 a.m.",
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
            name="EMILY_ROSE_2_9d0f3a82-fdf4-41c1-b1a4-04c138ba9d24_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T12:30:00-08:00",
            is_read_time="2024-12-02T12:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You are free for the rest of your day and want to see if a friend is free to hang out. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Message the Event Helper hey, any plans for the rest of the day",
                },
            ],
            reasoning="The user wants to message a contact named Event Helper. First I'll locate this contact, it appears to be Nathan Blake as his alias is Event Helper, and find any existing message threads with them, and then I'll add the text provided by the user as a draft before seeking confirmation to send.",
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Nathan Blake saying something like "hey, any plans for the rest of the day”',
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
                # Milestone 0 – The agent looks up the “Event Helper” contact
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
                # Milestone 1 – The tool output actually contains Nathan Blake (alias “Event Helper”)
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
                                                "value": "Nathan Blake",
                                                "partial": False,
                                            },
                                            "alias": {
                                                "value": "Event Helper",
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
                # Milestone 2 – A new message is created and sent to Nathan asking about plans
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least one of Nathan’s identifiers must appear;
                                    # no extra unknown participants allowed
                                    "participants_addresses": [
                                        [
                                            (
                                                "+1 530-555-0129",
                                                "nathan.blake@eventpros.com",
                                            )
                                        ]
                                    ],
                                    "content": "any plans",
                                    "creation_datetime_iso": "2024-12-02T12:30:00-08:00",
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
                (0, 1),  # contact lookup → confirm correct contact found
                (1, 2),  # contact confirmed → message sent
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_3eafcb54-d4eb-4e02-bd90-e5d58c1d0429_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T10:00:00-08:00",
            is_read_time="2024-12-03T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know who you sent your email to about the Christmas charity event. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who did I send my email yesterday to?",
                },
            ],
            reasoning="Okay so the user is looking for an email they sent yesterday and the recipients of it. From checking their Mail app, I can see one email sent yesterday, 2 December 2024 at 11:45 with the subject 'Summary of Today's Meeting on Christmas Charity Event'. It was sent to Michael Thompson and Jenna Miles and I can display this information to the user.",
            success_conditions=[
                {
                    "input_text": "1. The email sent to Michael Thompson and Jenna Miles on 2 December 2024 at 11:45 with the subject 'Summary of Today's Meeting on Christmas Charity Event' is displayed to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – The agent queries the email database to look for yesterday’s sent email
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
                # Milestone 1 – Confirm that the tool call returned the expected email that was sent
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
                                                "value": "Summary of Today's Meeting on Christmas Charity Event",
                                                "partial": False,
                                            },
                                            # Make sure at least Michael’s address appears in the recipients list
                                            "recipients_addresses": {
                                                "value": "michael.thompson@orchardcommunity.org",
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
                # Milestone 2 – The agent tells the user the email was sent to BOTH Michael Thompson and Jenna Miles
                Milestone(
                    snapshot_constraints=[
                        # Check for Michael Thompson
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Michael Thompson",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        ),
                        # Check for Jenna Miles
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Jenna Miles",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Email search → verify returned email
                (1, 2),  # Verified email → inform user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_2d3a91be-b115-4e19-b576-fdbc7ae22bf8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_2",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T16:20:00-08:00",
            is_read_time="2024-12-11T16:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Jenna has been so helpful you want to go all out for her birthday but need to be reminded when that is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is Jenna's birthday?",
                },
            ],
            reasoning="The user wants to know when Jenna's birthday is. I should first figure out who Jenna is. I will check the user's Contacts for a Jenna. \n\nLooks like there is one Jenna, Jenna Miles, so this must be who the user means. Next I will check Jenna's contact card for her birthday. \n\nJenna's birthday is the 14 February 1991. I will tell the user this. ",
            success_conditions=[
                {
                    "input_text": "1. User is informed Jenna Miles' birthday is the 14 February 1991.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_contacts", "get_all_contacts"],
            milestones=[
                # Milestone 0 – Agent queries the contacts database (either searching or listing all).
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
                # Milestone 1 – The tool call returned a contact whose full_name is “Jenna Miles”.
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
                                                "value": "Jenna Miles",
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
                # Milestone 2 – The agent tells the user Jenna’s birthday (Feb 14 1991).
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
                                            "February 14",
                                            "Feb 14",
                                            "14 February",
                                            "14 Feb",
                                            "14th of February",
                                            "2/14",
                                            "02/14",
                                            "1991-02-14",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity,
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
            name="EMILY_ROSE_2_c3cd714d-5b50-4883-b092-f5100510d247_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T13:20:00-08:00",
            is_read_time="2024-12-03T13:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You're excited with getting the planning ready for the community centre Christmas Charity event - the preparations have been going very well.   You will need to add the event to your calendar and invite your colleagues at the community centre to it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Can you make the event "Christmas Charity event" for the Friday in two weeks\' time at 4pm and invite all my colleagues, ah for 3 hours please?',
                },
            ],
            reasoning='The user wants me to create a new event. They gave me the name of the event, "Christmas Charity event", but I need to figure out when "Friday in two weeks\' time" is. If today is 3rd December 2024, then Friday in two weeks\' time must be the 20th December 2024. I\'ll check the user\'s calendar to see if he has any events for that day, but it looks all clear. Also I need to check user\'s contacts to find out who are the collegues. I found "Michael Thompson" and "Jenna Miles". With the user\'s permission, I will add the event to the calendar as requested.',
            success_conditions=[
                {
                    "input_text": '1. The event "Christmas Charity event" is added to the user\'s calendar for Friday 20th December 2024 at 16:00-19:00, with Michael Thompson and Jenna Miles invited.',
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
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent looks up colleagues in the contacts database
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
                # Milestone 1 – Michael Thompson’s contact information was returned in the previous tool call
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
                                                "value": "Michael Thompson",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "michael.thompson@orchardcommunity.org",
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
                # Milestone 2 – The agent looks up colleagues in the contacts database
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
                # Milestone 3 – Jenna Miles’ contact information was returned in the previous tool call
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
                                                "value": "Jenna Miles",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "jenna.miles@orchardcommunity.org",
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
                # Milestone 4 – A new calendar event has been created for the correct date, time, and attendees
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Christmas Charity event",
                                    "start_datetime_iso": "2024-12-20T16:00:00",
                                    "end_datetime_iso": "2024-12-20T19:00:00",
                                    "attendees_names": [
                                        ["Michael Thompson", "Jenna Miles"]
                                    ],
                                    "creation_datetime_iso": "2024-12-03T13:20:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_rouge_l_similarity,
                                "attendees_names": column_list_subset_match_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox chatter when looking at calendar diff
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # contact search → verify Michael
                (2, 3),  # contact search → verify Jenna
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_c3cd714d-5b50-4883-b092-f5100510d247_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T13:20:00-08:00",
            is_read_time="2024-12-03T13:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You're excited with getting the planning ready for the community centre Christmas Charity event - the preparations have been going very well.   You will need to add the event to your calendar and invite your colleagues at the community centre to it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Can you make the event "Christmas Charity event" for Friday 20th December 2024 for 16:00 and invite all my colleagues?',
                },
            ],
            reasoning='The user wants me to create a new event. They gave me the name of the event, "Christmas Charity event", as well as the date and time - Friday 20th December 2024 for 16:00.  I\'ll check the user\'s calendar to see if they have any events for that day, but it looks all clear. I also found "Michael Thompson" and "Jenna Miles" as the collegues from user\'s contacts. With the user\'s permission, I will add the event to the calendar as requested.',
            success_conditions=[
                {
                    "input_text": '1. The event "Christmas Charity event" is added to the user\'s calendar for Friday 20th December 2024 at 16:00, with Michael Thompson and Jenna Miles invited.',
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
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent looks up colleagues in the contacts database
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
                # Milestone 1 – Michael Thompson is returned from the contact search in Milestone 0
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
                                                "value": "Michael Thompson",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "michael.thompson@orchardcommunity.org",
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
                # Milestone 2 – The agent looks up colleagues in the contacts database
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
                # Milestone 3 – Jenna Miles is also returned from the contact search in Milestone 0
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
                                                "value": "Jenna Miles",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "jenna.miles@orchardcommunity.org",
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
                # Milestone 4 – A new calendar event has been created with both colleagues invited
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Christmas Charity event",
                                    "start_datetime_iso": "2024-12-20T16:00:00",
                                    "attendees_names": [
                                        ["Michael Thompson", "Jenna Miles"]
                                    ],
                                    "creation_datetime_iso": "2024-12-03T13:20:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,  # allow timezone suffix
                                "attendees_names": column_list_subset_match_similarity,
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
                (0, 1),  # Contact search → confirm Michael
                (2, 3),  # Contact search → confirm Jenna
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_1e2bc562-b54b-4979-addc-c5d4a33ec6f2_single_turn_5",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "contact",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T16:20:00-08:00",
            is_read_time="2024-12-11T16:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to look up the birthday of the colleague you met with during your first meeting on the first Monday of this month so you can plan something special.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is the birthday of the person that I met with during my first of my two meetings on the first Monday of this month?",
                },
            ],
            reasoning="I need to retrieve some information for the user. They want to know when someone's birthday is. To figure out who they're talking about, I need to work my way through the user's description. They said they met with this person, so I need to look at invitees on calendar events. To narrow down the events I need to look at, I need to figure out which events the user means when they say \"my two meetings on the first Monday of this month.\" This month is December, and the first Monday of the month was Monday 2 December. There were indeed two meetings on the user's calendar that day: one called \"Event Planning Meeting with Jenna\" from 9:00-10:00 and one called \"Event Coordination Meeting with Michael\" from 10:30-11:30. The user said they want to know the birthday of the person they met with during the first of those two meetings. The first one that occurred that day, December 2nd, was the one named \"Event Planning Meeting with Jenna\" from 9:00-10:00. Jenna Miles was the invitee on that event, so this must be who the user is talking about. I'll look at the user's contacts to see if Jenna is stored in there. Sure enough, she's listed as a contact. This says her birthday is 14 February 1991, so I'll tell this to the user.",
            success_conditions=[
                {
                    "input_text": "1. User is informed Jenna Miles' birthday is the 14 February 1991.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – Agent inspects calendar to figure out "first Monday of this month" and the two meetings
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
                # Milestone 1 – Confirm that the first Monday's two meetings (with Jenna and Michael) were retrieved
                # We only need to confirm the earlier Jenna meeting exists, since that's key to resolving the reference.
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
                                                "value": "Event Planning Meeting with Jenna",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-02T09:00:00-08:00",
                                                "partial": False,
                                            },
                                            "attendees_names": {
                                                "value": ["Emily Rose", "Jenna Miles"],
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
                # Milestone 2 – Agent looks up contacts to resolve the person (Jenna) and retrieve birthday
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
                # Milestone 3 – Confirm Jenna Miles contact with correct birthday was retrieved from contacts in Milestone 2
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
                                                "value": "Jenna Miles",
                                                "partial": False,
                                            },
                                            "birthday": {
                                                "value": "1991-02-14T00:00:00-08:00",
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
                # Milestone 4 – Agent informs user of Jenna's birthday (February 14, 1991)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Allow multiple phrasings for the date;
                                    # must at least mention Feb 14, 1991 in some recognizable format.
                                    "content": [
                                        (
                                            "February 14, 1991",
                                            "Feb 14, 1991",
                                            "14 February 1991",
                                            "1991-02-14",
                                            "February 14",
                                            "Feb 14",
                                            "14 February",
                                            "14 Feb",
                                            "14th of February",
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
                (0, 1),  # calendar lookup → confirm correct first meeting (with Jenna)
                (1, 2),  # identified meeting attendee → lookup contact
                (2, 3),  # contact lookup → confirm Jenna & birthday
                (3, 4),  # having birthday → inform user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_2b7825ee-3f4b-420a-b097-45ffa6de0746_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T06:00:00-08:00",
            is_read_time="2024-12-02T06:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to check what time your first meeting is this morning. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is my first meeting this morning? ",
                },
            ],
            reasoning="The user is looking for the time of an event, so first I must find the event. They mention that this event is a meeting and that it takes place this morning. I can see two meetings today, so I will relay the time for both meetings back to the user. ",
            success_conditions=[
                {
                    "input_text": "1. Calendar is checked for a meeting event in the near future.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The time of the event is relayed back to the user. ",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (information-retrieval step)
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
                # Milestone 1 – Agent tells the user the time of the first meeting (user-facing outcome)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Match any reasonable phrasing that contains 9 AM / 09:00
                                    "content": [
                                        ("9:00", "09:00", "9 am", "9am", "9 a.m.")
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
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_291d6ebe-ec9a-4761-a1c4-54a0fc9c5148_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_2",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T06:00:00-08:00",
            is_read_time="2024-12-02T06:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to check what time your first meeting is this morning.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is my first meeting this morning? ",
                },
            ],
            reasoning="The user is looking for the time of an event, so first I must find the event. They mention that this event is a meeting and that it takes place this morning. I can see two meetings today, so I will relay the time for both meetings back to the user. ",
            success_conditions=[
                {
                    "input_text": "1. Calendar is checked for a meeting event in the near future.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The time of the event is relayed back to the user. ",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Calendar is queried to find upcoming/today's meetings
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
                # Milestone 1 – Confirms the 9:00–10:00 AM event this morning was retrieved
                # "Event Planning Meeting with Jenna" at 2024-12-02T09:00:00-08:00
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
                                                "value": "Event Planning Meeting with Jenna",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-02T09:00:00-08:00",
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
                # Milestone 2 – User-facing reply mentions the correct time of the first meeting (9:00 AM)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Accept common phrasings of 9am
                                    "content": [
                                        ("9:00", "9 am", "9am", "9 a.m.", "9 o'clock")
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
                (0, 1),  # Calendar checked → specific morning meeting identified
                (1, 2),  # Meeting identified → user informed with correct time
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_4d52f764-cb9d-4213-a830-2149fc7e62a8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T11:50:00-08:00",
            is_read_time="2024-12-02T11:50:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to double check the information in the chirstmas event file. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need you to show me the email that contains the file Christmas_Charity_Event_Details.pdf.",
                },
            ],
            reasoning="The user wants to see an email that contains a specific file attachment called 'Christmas_Charity_Event_Details.pdf'. I'll search through their emails to find one with this attachment. I found an email with subject 'Summary of Today's Meeting on Christmas Charity Event' that was sent to Michael Thompson and Jenna Miles, and it has the requested PDF attached. I'll show the user this email.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The email with subject "Summary of Today\'s Meeting on Christmas Charity Event" containing "Christmas_Charity_Event_Details.pdf" is found and shown to the user.',
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – The agent looks through e-mails to locate the one that carries the requested PDF
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
                # Milestone 1 – Confirm the e-mail that contains “Christmas_Charity_Event_Details.pdf”
                #       was indeed returned by the previous tool call
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
                                                "value": "Summary of Today's Meeting on Christmas Charity Event",
                                                "partial": False,
                                            },
                                            "attachments": {
                                                "value": [
                                                    "Christmas_Charity_Event_Details.pdf"
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
                # Milestone 2 – User-facing reply mentions the email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Christmas charity event",
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
            ],
        ),
    ]
