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


def get_TAG_EMILY_ROSE_pilot_plot_8(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="EMILY_ROSE_8_f3e1fe2d-d813-4e32-9715-78fe18b69852_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T16:15:00-08:00",
            is_read_time="2024-12-06T16:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You had a really productive community meeting with some really invaluable feedback.   You're going to compile all of the discussion and call a meeting with the rest of the team at the community centre - you want to send a message to Jenna, Michael and Jessica to ask them when they are next free. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Hit up Community Leader, Decor Diva and Bestie saying "Hey Team! The community meeting was a huge success and I think we should try to review all of the feedback together. When do you think we can schedule a group huddle?"',
                },
            ],
            reasoning="The user wants to send a message to Community Leader, Decor Diva and Bestie. I don't have any idea who these people are meant to be. I'll check and see if there's anything in user's contacts for these people.... And I was able to find a match for every person, because I figured out these are aliases pertaining to certain people. I found they match Jessica Lane, Jenna Miles and Michael Thompson - these must be the people they want to contact. With the user's confirmation, I'll send the message \"Hey Team! The community meeting was a huge success and I think we should try to review all of the feedback together. When do you think we can schedule a group huddle?\"",
            success_conditions=[
                {
                    "input_text": '1. The message "Hey Team! The community meeting was a huge success and I think we should try to review all of the feedback together. When do you think we can schedule a group huddle?" to Jessica Lane, Jenna Miles and Michael Thompson.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up contacts (either search or list-all)
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
                                            "full_name": {
                                                "value": "Michael Thompson",
                                                "partial": False,
                                            },
                                            "alias": {
                                                "value": "Community Leader",
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
                            reference_milestone_node_index=0,  # Based on tool call results in Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – Agent looks up contacts (either search or list-all)
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
                # Milestone 3
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
                                                "value": "Jessica Lane",
                                                "partial": False,
                                            },
                                            "alias": {
                                                "value": "Bestie",
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
                            reference_milestone_node_index=2,  # Based on tool call results in Milestone 0
                        )
                    ],
                ),
                # Milestone 4 – Agent looks up contacts (either search or list-all)
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
                # Milestone 5 – Tool output contains Jenna Miles (alias Decor Diva) with correct birthday
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
                                            "alias": {
                                                "value": "Decor Diva",
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
                            reference_milestone_node_index=4,  # Based on tool call results in Milestone 4
                        )
                    ],
                ),
                # Milestone 6 – Verify a new message was created that includes Jenna, Michael, and Jessica
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
                                                "+1 530-555-0131",
                                                "jenna.miles@orchardcommunity.org",
                                            ),
                                            (
                                                "+1 530-555-0130",
                                                "michael.thompson@orchardcommunity.org",
                                            ),
                                            (
                                                "+1 530-555-0127",
                                                "jessica.lane@orchardmail.com",
                                            ),
                                        ]
                                    ],
                                    "content": "community meeting was a huge success",
                                    "creation_datetime_iso": "2024-12-06T16:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Each tuple represents acceptable identifiers for one participant.
                                # At least one identifier per tuple must be present. Extras (like sender) allowed.
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                # Message body should reference the meeting’s success (exact phrasing can vary)
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
            milestone_edge_list=[(0, 1), (2, 3), (4, 5)],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_8_8cd507aa-e544-4910-b880-a7e584dc8c87_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T15:25:00-08:00",
            is_read_time="2024-12-06T15:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You are wondering what time you sent in your last email to Chloe Waters "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I send that last email to Chloe Waters",
                },
            ],
            reasoning="The user wants to know when they sent their last email to Chloe Waters. First thing I need to do is search the user's emails. Ok I found an email sent to chloe.waters@orchardmail.com. That must be the email the user is referring to. Ok now that I have that I will retrieve the time of the email and inform the user",
            success_conditions=[
                {
                    "input_text": "1. The time of the email sent by the user on December 06, 2024 at 15:00 to chloe.waters@orchardmail.com is presented to the user",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – The agent consults the email store (search or list) to locate emails
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
                # Milestone 1 – Confirm that an email to Chloe Waters with the correct timestamp was returned
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
                                            # make sure the email involves Chloe Waters
                                            "recipients_addresses": {
                                                "value": "chloe.waters@orchardmail.com",
                                                "partial": True,
                                            },
                                            # and has the expected creation timestamp
                                            "creation_datetime_iso": {
                                                "value": "2024-12-06T15:00:00-08:00",
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
                # Milestone 2 – The agent tells the user the time (3 PM / 15:00)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Accept common ways of expressing 3 PM
                                    "content": [
                                        (
                                            "3:00 PM",
                                            "3 PM",
                                            "3pm",
                                            "3:00 pm",
                                            "15:00",
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
            name="EMILY_ROSE_8_8cd507aa-e544-4910-b880-a7e584dc8c87_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T15:25:00-08:00",
            is_read_time="2024-12-06T15:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You are wondering what time you sent in your last email to Chloe Waters "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I send that last email to chloe.waters@orchardmail.com",
                },
            ],
            reasoning="The user wants to know when they sent their last email to chloe.waters@orchardmail.com. First thing I need to do is search the user's emails. Ok I found an email sent to chloe.waters@orchardmail.com. That must be the email the user is referring to. Ok now that I have that I will retrieve the time of the email and inform the user",
            success_conditions=[
                {
                    "input_text": "1. The time of the email sent by the user on December 06, 2024 at 15:00 to chloe.waters@orchardmail.com is presented to the user",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – The agent looks through the email database
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
                # Milestone 1 – The returned email includes one sent to Chloe on 2024-12-06 at 15:00-08:00
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
                                                "value": "chloe.waters@orchardmail.com",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-06T15:00:00-08:00",
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
                # Milestone 2 – The agent tells the user the correct send time
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
                                        ("3:00", "3 pm", "3pm", "3 p.m.", "15:00")
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
            name="EMILY_ROSE_8_f3e1fe2d-d813-4e32-9715-78fe18b69852_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_high",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T16:15:00-08:00",
            is_read_time="2024-12-06T16:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You had a really productive community meeting with some really invaluable feedback.   You're going to compile all of the discussion and call a meeting with the rest of the team at the community centre - you want to send a message to Jenna, Michael and Jessica to ask them when they are next free. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I\'m going to need you to message Jessica, Jenna and Michael and say "Hey Team! The community meeting was a huge success and I think we should try to review all of the feedback together. When do you think we can schedule a group huddle?"',
                },
            ],
            reasoning="The user wants to send a message to Jessica, Jenna and Michael. I'll check the user's contacts for these people.... And I was able to successfully locate them all, so I think these must be the people they want to contact. With the user's confirmation, I'll send the message \"Hey Team! The community meeting was a huge success and I think we should try to review all of the feedback together. When do you think we can schedule a group huddle?\"",
            success_conditions=[
                {
                    "input_text": '1. The message "Hey Team! The community meeting was a huge success and I think we should try to review all of the feedback together. When do you think we can schedule a group huddle?" to Jessica Lane, Jenna Miles and Michael Thompson.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up the contacts it needs to message
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
                # Milestone 1 – The contact list returned in Milestone 0 contains Jessica Lane
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
                                                "value": "Jessica Lane",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "jessica.lane@orchardmail.com",
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
                # Milestone 2 – The agent looks up the contacts it needs to message
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
                # Milestone 3 – The contact list returned in Milestone 0 contains Jenna Miles
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
                # Milestone 4 – The agent looks up the contacts it needs to message
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
                # Milestone 5 – The contact list returned in Milestone 0 contains Michael Thompson
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
                            reference_milestone_node_index=4,
                        )
                    ]
                ),
                # Milestone 6 – A new message has been sent to all three participants with the requested text
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
                                                "jessica.lane@orchardmail.com",
                                                "+1 530-555-0127",
                                            ),
                                            (
                                                "jenna.miles@orchardcommunity.org",
                                                "+1 530-555-0131",
                                            ),
                                            (
                                                "michael.thompson@orchardcommunity.org",
                                                "+1 530-555-0130",
                                            ),
                                        ]
                                    ],
                                    "content": (
                                        "Hey Team! The community meeting was a huge success and I think we should try to review "
                                        "all of the feedback together. When do you think we can schedule a group huddle?"
                                    ),
                                    "creation_datetime_iso": "2024-12-06T16:15:00-08:00",
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
            milestone_edge_list=[(0, 1), (2, 3), (4, 5)],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_8_5fadf20b-32ab-4889-9658-00bd249de35e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T16:15:00-08:00",
            is_read_time="2024-12-06T16:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You need to schedule time to compile the feedback from the community meeting. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set aside time today to compile feedback for an hour at 5",
                },
            ],
            reasoning='Ok so the user wants to set aside time to compile feedback for an hour at 5. First I\'ll establish the name of the event which I will keep simple and the intention of the event clear. I will title the event Compile Feedback. Next is the time which the user gives. I will now create the event "Compile Feedback" at 17:00-18:00 on 6 December 2024. ',
            success_conditions=[
                {
                    "input_text": "1. An event called Compile feedback from 17:00-18:00 on 6 December 2024 is created. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "create_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – verify that the new calendar event was added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Compile feedback",
                                    "start_datetime_iso": "2024-12-06T17:00:00-08:00",
                                    "end_datetime_iso": "2024-12-06T18:00:00-08:00",
                                    "creation_datetime_iso": "2024-12-06T16:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Allow flexible capitalization / phrasing for the title, but require the key phrase “compile feedback”
                                "calendar_event_name": column_contains_similarity,
                                # Times must match exactly
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to the initial snapshot
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_8_cd883b67-a730-4948-bf93-5a68320b65e0_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T15:15:00-08:00",
            is_read_time="2024-12-06T15:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You meant to express your gratitude by email to two attendees, Chloe, and Sophia, for giving feedback during today's community meeting.   You want to make sure you sent them the email. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I send an email to Chloe and Sophia? Yes or No",
                },
            ],
            reasoning="The user wants to know if they sent an email to Chloe and Sophia. I wonder who they are. I don't see anyone with those names in the user's contacts. I'll check their emails to see if they sent any emails that could be sent to those recipients. I see the user sent an email addressed to \"Chloe and Sophia\" and sent to email addresses containing those names, on December 6th, 2024, at 15:00. This must be the email the user wants to know if they sent. I'll tell the user the details of this email now and reply with Yes. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. Email messages are checked for an email sent from the user to Chloe and Sophia and the email sent on December 6th at 15:00 is found. ",
                },
                {
                    "statefullness": "Stateless",
                    "input_text": "2. The user is informed with 'Yes'.",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent looks through e-mails
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
                # Milestone 1 – The searched/returned e-mail is the one sent to Chloe and Sophia
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
                                                "value": "Thank You for Your Feedback!",
                                                "partial": False,
                                            },
                                            "recipients_addresses": {
                                                "value": [
                                                    "chloe.waters@orchardmail.com",
                                                    "sophia.taylor@orchardbusiness.org",
                                                ],
                                                "partial": True,  # allow list order formatting differences
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
                # Milestone 2 – Agent informs the user that the e-mail was indeed sent
                Milestone(
                    snapshot_constraints=[
                        # Must indicate that the e-mail was sent (confirmation)
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
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_8_a07ddb29-435b-4112-b937-1b57ed9f6537_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T16:05:00-08:00",
            is_read_time="2024-12-06T15:44:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to read the email you just received from Sophia Taylor, but you are driving so you want the email to be read out to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you read out the last email I received from Sophia. ",
                },
            ],
            reasoning="The user wants me to read out the last email received from Sophia, so I must first search the user's emails for an email from a contact under that name. I have searched the users inbox, and I found an unread email from sophia.taylor@orchardbusiness.org that was sent 20 minutes ago. I can safely assume this is the email the user referenced, so I will read out the contents of the message to the user. ",
            success_conditions=[
                {
                    "input_text": "1. The email received on December 6, 2024 at 15:45 from Sophia.taylor@orchardbusiness.org is read out to the user. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – The agent invokes an email-retrieval tool
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
                # Milestone 1 – The tool output includes the expected email from Sophia Taylor
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
                                                "value": "sophia.taylor@orchardbusiness.org",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Thank You for Your Feedback",
                                                "partial": True,  # allow "Re:" prefix
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-06T15:45:00-08:00",
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
                # Milestone 2 – The agent reads the email content back to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "It was indeed a great meeting",
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
                (0, 1),  # Tool invocation → confirm correct email found
                (1, 2),  # Email found → read it to the user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_8_ebbda065-f84c-4d18-bb06-4772828452b3_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T15:50:00-08:00",
            is_read_time="2024-12-06T15:50:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        'You want to set up a calendar event called "Next events discussion" on 17th December 2024 at 10:00 am. '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Create a calendar event called "Next events discussion" on 17th December 2024 at 10:00 am please',
                },
            ],
            reasoning='The user wants to create an event called "Next events discussion". I will ask the user for the date and time of the event. This is given as 17th December 2024 at 10:00 am. After this I will set up the event.',
            success_conditions=[
                {
                    "input_text": '1. A calendar event called "Next events discussion" on 17th December 2024 at 10:00 am is created.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["create_calendar_event"],
            milestones=[
                # Milestone 0 – Agent invokes the calendar-creation tool
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
                                    target_tools=["create_calendar_event"],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – A new calendar event matching the requested title and start-time exists
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Next events discussion",
                                    "start_datetime_iso": "2024-12-17T10:00",  # partial string; timezone/seconds may vary,
                                    "creation_datetime_iso": "2024-12-06T15:50:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
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
                (0, 1),  # Tool call should precede the actual creation in the database
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_8_9a8e3598-d28f-48b5-ab56-f9004cf59d5c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T15:45:00-08:00",
            is_read_time="2024-12-06T15:45:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to dictate a reply to Sophia asking her if she's free to meet up for a coffee to discuss her contributions during the community meeting. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a reply email to sophia.taylor@orchardbusiness.org saying "Hi Sophia I was just wondering if you were free to meet for a coffee to discuss your ideas during the community meeting."',
                },
            ],
            reasoning='The user wants to dictate a reply email to sophia.taylor@orchardbusiness.org. The last email from this address has the subject line "Re: Thank You for Your Feedback" and was received on 6 December 2024 at 15:45, so that\'s the one I\'ll reply to. I\'ll say what the user wants: "Hi Sophia I was just wondering if you were free to meet for a coffee to discuss your ideas during the community meeting."',
            success_conditions=[
                {
                    "input_text": "1. A reply to the email \"Re: Thank You for your Feedback!\" is sent to sophia.taylor@orchardbusiness.org saying 'Hi Sophia I was just wondering if you were free to meet for a coffee to discuss your ideas during the community meeting'",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – the agent looks up existing emails to find the thread to reply to
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
                # Milestone 1 – confirm that the email from Sophia with the proper subject was retrieved
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
                                                "value": "sophia.taylor@orchardbusiness.org",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Re: Thank You for Your Feedback!",
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
                            reference_milestone_node_index=0,  # depend on retrieval in Milestone 0
                        ),
                    ],
                ),
                # Milestone 2 – verify a reply email was sent to Sophia with the correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["sophia.taylor@orchardbusiness.org"]
                                    ],
                                    "status": "sent",
                                    "body": "coffee",
                                    "creation_datetime_iso": "2024-12-06T15:45:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare with initial snapshot
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
            name="EMILY_ROSE_8_cd883b67-a730-4948-bf93-5a68320b65e0_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T15:15:00-08:00",
            is_read_time="2024-12-06T15:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You meant to express your gratitude by email to two attendees, Chloe, and Sophia, for giving feedback during today's community meeting.   You want to make sure you sent them the email. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I send an email to the two ladies who spoke up today? Yes or No.",
                },
            ],
            reasoning='The user wants to know if they sent an email to the two ladies who spoke up today. I wonder who they are. I\'ll check their emails to see if they sent any emails that could be sent to those people. I see the user sent an email addressed to "Chloe and Sophia", on December 6th, 2024, at 15:00. It seems to express gratitude for feedback the two girls gave today. I think this could be what the user is referring to by "the two ladies who spoke up today". I assume then this is the email the user wants to know if they sent. I\'ll tell the user the details of this email now and reply with Yes.',
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. Email messages are checked for an email sent from the user to Chloe and Sophia and the email sent on December 6th at 15:00 is found. ",
                },
                {
                    "statefullness": "Stateless",
                    "input_text": "2. The user is replied with 'Yes'.",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 — Agent invokes an email–retrieval tool
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
                # Milestone 1 — Returned tool output includes the specific “Thank You” email sent to Chloe & Sophia
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
                                                    "chloe.waters@orchardmail.com",
                                                    "sophia.taylor@orchardbusiness.org",
                                                ],
                                                "partial": False,
                                            },
                                            "status": {
                                                "value": "sent",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Thank You for Your Feedback!",
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
                # Milestone 2 — Agent answers the user, confirming the email was sent and showing its details
                Milestone(
                    snapshot_constraints=[
                        # Response contains confirmation
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
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_8_a07ddb29-435b-4112-b937-1b57ed9f6537_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T16:05:00-08:00",
            is_read_time="2024-12-06T16:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to read the email you just received from Sophia Taylor, but you are driving so you want the email to be read out to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read me the email from Sophia",
                },
            ],
            reasoning="The user wants to read the email from Sophia. I first need to know Sophia's email address. I should check the user's Mail. \nThere is only one email address with Sophia in the email address, sophia.taylor@orchardbusiness.org, so this must be who the user meant. \nThe last email from Sophia was received at 15:46 on the 6 December 2024 and has a subject line of Re: Thank You for Your Feedback!. I will read this email to the user. ",
            success_conditions=[
                {
                    "input_text": "1. The email received on December 6, 2024 at 15:45 from Sophia.taylor@orchardbusiness.org is read out to the user. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – Agent looks up emails (should invoke an email-retrieval tool)
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
                # Milestone 1 – Confirm the retrieved email is the one from Sophia Taylor
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
                                                "value": "sophia.taylor@orchardbusiness.org",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Re: Thank You for Your Feedback!",
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
                # Milestone 2 – Agent reads the email content back to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "great meeting today",
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
                (0, 1),  # Tool call → validate correct email found
                (1, 2),  # Correct email found → agent reads it out
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_8_5fadf20b-32ab-4889-9658-00bd249de35e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T16:15:00-08:00",
            is_read_time="2024-12-06T16:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You need to schedule time to compile the feedback from the community meeting. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Make a new event from 17:00-18:00 today called Compile feedback. ",
                },
            ],
            reasoning="The user wants to create an event. I will use the details the user has provided to create this event. \n\nThe user wants to call it Compile feedback so I shall make that the name of the event. The user has specified the duration will be one hour from 17:00-18:00 so I shall set the event for that time.      \n\nI will let the user know the event has been created. ",
            success_conditions=[
                {
                    "input_text": "1. An event called Compile feedback from 17:00-18:00 on 6 December 2024 is created. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "create_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Compile feedback",
                                    "start_datetime_iso": "2024-12-06T17:00:00-08:00",
                                    "end_datetime_iso": "2024-12-06T18:00:00-08:00",
                                    "creation_datetime_iso": "2024-12-06T16:15:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_8_b7686b6c-37ae-401b-93b1-c6f5a6da41ee_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T16:15:00-08:00",
            is_read_time="2024-12-06T16:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You need to schedule time to compile the feedback from the community meeting.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set aside time next Monday to compile feedback from the community meeting with the folks for an hour at 1",
                },
            ],
            reasoning='Ok so the user wants to set aside time to compile feedback for an hour at 1 next Monday with the folks attending the community meeting. First I need to find out who are the folks mentioned in the query. There\'re no such community meeting in the user\'s calendar, however, I found an email thread with "chloe.waters@orchardmail.com" and "sophia.taylor@orchardbusiness.org" were discussing the community meeting. Second I\'ll establish the name of the event which I will keep simple and the intention of the event clear. I will title the event Compile Feedback. Next is the time which the user gives. I will now create the event "Compile Feedback" at 13:00-14:00 on 9 December 2024. ',
            success_conditions=[
                {
                    "input_text": '1. An event called Compile feedback from 13:00-14:00 on 9 December 2024 is created with "Chloe Waters" and "Sophia Taylor" as invitees.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "create_calendar_event",
                "get_all_calendars",
                "search_calendar_events",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – search for community meeting
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
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Confirm the retrieved email is for community meeting
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
                                            "subject": {
                                                "value": "Thank You for Your Feedback!",
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
                # Milestone 2 – Verify a new calendar event for compiling feedback from 17:00–18:00 on Dec 6, 2024 exists
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "feedback",
                                    "start_datetime_iso": "2024-12-09T13:00:00-08:00",
                                    "end_datetime_iso": "2024-12-09T14:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "chloe.waters@orchardmail.com",  # Chloe not in contacts using email
                                            "sophia.taylor@orchardbusiness.org",  # Sophia not in contacts using email
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-06T16:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Allow slight variations like "Compile feedback from community meeting"
                                "calendar_event_name": column_contains_similarity,
                                "attendees_names": column_list_subset_match_similarity,
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
            name="EMILY_ROSE_8_28874f5c-0113-41bd-8d92-d3a235060882_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T16:00:00-08:00",
            is_read_time="2024-12-06T16:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to reply to a recently received email related to feedback received by the user. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to Sophia's email with 'Thank you, I will be in touch once your feedback has been implemented.'.",
                },
            ],
            reasoning="The user wants to reply to Sophia's email. Let me loo for it in Mail. It must be the last email from sophia.taylor@orchardbusiness.org.\n\nI will use the content provided by the user and then send it.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. An email reply is sent to sophia.taylor@orchardbusiness.org with the text "Thank you, I will be in touch once your feedback has been implemented."',
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – the agent looks up recent emails (expects a search/get email tool)
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
                # Milestone 1 – confirm that Sophia’s email was found in the previous tool result
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
                                                "value": "sophia.taylor@orchardbusiness.org",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Re: Thank You for Your Feedback!",
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
                # Milestone 2 – verify a reply email was sent to Sophia with the required message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["sophia.taylor@orchardbusiness.org"]
                                    ],
                                    "body": "I will be in touch",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-06T16:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_subset_match_similarity,
                                "body": column_contains_similarity,
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
            name="EMILY_ROSE_8_acd809e3-74e7-4c5b-adc5-c370d896f1ef_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T17:00:00-08:00",
            is_read_time="2024-12-06T17:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to see the last email Chloe sent you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show the last email from Chloe.",
                },
            ],
            reasoning="The user wants to see the last email from Chloe. Let me find Chloe in Contacts. There is no Chloe in Contacts. I will look in Mail. I can see an account named chloe.waters@orchardmail.com. It must be this one. I will show the user the last email she sent, which was received at 15:45 on the 6 December 2024 with the subject line Re: Thank You for Your Feedback!.",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last email sent by chloe.waters@orchardmail.com at 15:30 on December 6th with the subject line Re: Thank You for Your Feedback!",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – The agent invokes an email-retrieval tool
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
                # Milestone 1 – The retrieved results include Chloe’s latest email
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
                                                "value": "chloe.waters@orchardmail.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Re: Thank You for Your Feedback!",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-06T15:30:00-08:00",
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
                            reference_milestone_node_index=0,  # parse tool output from Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – The agent shows the email (subject) to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Re: Thank You for Your Feedback!",
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
            name="EMILY_ROSE_8_0d5a14b3-470b-4300-ac10-3e2f6029e255_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T08:10:00-08:00",
            is_read_time="2024-12-07T08:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know the subject line of the email you sent out yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell me the subject of the email sent to Sophia and Chloe yesterday.",
                },
            ],
            reasoning="Okay, the user is looking for the subject line of an email sent to 'Sophia and Chloe yesterday'. Checking their contacts, I can see no one under 'Sophia' or 'Chloe'. Next I will check their Mail. I can see an email the user sent yesterday, 6 December 2024 at 15:00 to Chloe Waters and Sophia Taylor, with the subject line 'Thank You for Your Feedback!'. As I know this is the information the user was requesting, I can read out the subject line to them.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The name of the email subject line 'Thank You for Your Feedback!' sent on 6 December 2024 at 15:00 to Chloe Waters and Sophia Taylor is read out to the user.",
                }
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
                        )
                    ]
                ),
                # Milestone 1 – The tool output includes the expected email
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
                                                "value": "Thank You for Your Feedback!",
                                                "partial": False,
                                            },
                                            "recipients_addresses": {
                                                "value": [
                                                    "chloe.waters@orchardmail.com",
                                                    "sophia.taylor@orchardbusiness.org",
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
                    ]
                ),
                # Milestone 2 – Agent tells the user the correct subject line
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Thank You for Your Feedback!",
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
            name="EMILY_ROSE_8_180418c6-0c70-42cd-9102-fcf99f6fff31_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T15:45:00-08:00",
            is_read_time="2024-12-06T15:45:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to dictate a reply to Sophia asking her if she's free to meet up for a coffee to discuss her contributions during the community meeting. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Email Sophia Taylor back this; "Hi Sophia I was just wondering if you were free to meet for a coffee to discuss your ideas during the community meeting."',
                },
            ],
            reasoning="Ok so the user wants to email Sophia Taylor a given message. First is the recipient which is given by the user. Next is the mode of communication which is given by the user also. I will now send the user's given message to Sophia Taylor via email. ",
            success_conditions=[
                {
                    "input_text": "1. The email; 'Hi Sophia I was just wondering if you were free to meet for a coffee to discuss your ideas during the community meeting' is sent to Sophia Taylor at 15:45 on 6 December 2024. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "modify_draft_email",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Agent looks through existing emails to locate Sophia’s address / thread
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
                # Milestone 1 – Confirm the search returned (or included) an email from / to Sophia Taylor
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
                                                "value": "sophia.taylor@orchardbusiness.org",
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
                # Milestone 2 – A new outgoing email to Sophia is sent with the correct content and timestamp
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["sophia.taylor@orchardbusiness.org"]
                                    ],
                                    "status": "sent",
                                    "body": "Hi Sophia I was just wondering if you were free to meet for a coffee to discuss your ideas during the community meeting",
                                    "creation_datetime_iso": "2024-12-06T15:45:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_8_180418c6-0c70-42cd-9102-fcf99f6fff31_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T15:45:00-08:00",
            is_read_time="2024-12-06T15:45:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to dictate a reply to Sophia asking her if she's free to meet up for a coffee to discuss her contributions during the community meeting. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a reply email to Sophia saying "Hi Sophia I was just wondering if you were free to meet for a coffee to discuss your ideas during the community meeting."',
                },
            ],
            reasoning="The user wants to dictate a reply email to the contact called Sophia.\n\nI should locate the email history with this contact by searching their name in the user's Inbox and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the email if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": "1. The email; 'Hi Sophia I was just wondering if you were free to meet for a coffee to discuss your ideas during the community meeting' is sent to Sophia Taylor at 15:45 on 6 December 2024. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "modify_draft_email",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the relevant email thread (or inbox) before replying
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
                # Milestone 1 – A reply (or new) email is actually sent to Sophia with the requested coffee-chat text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["sophia.taylor@orchardbusiness.org"]
                                    ],
                                    "status": "sent",
                                    "body": "meet for a coffee",
                                    "creation_datetime_iso": "2024-12-06T15:45:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Ensure Sophia is in the To/Recipients list (allowing possible extras like CC)
                                "recipients_addresses": column_list_subset_match_similarity,
                                "status": column_exact_match_similarity,
                                # Body must contain the key phrase; we allow for additional text/formatting
                                "body": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial state
                        )
                    ],
                    # Ignore unrelated sandbox traffic when checking EMAIL DB addition
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_8_0d5a14b3-470b-4300-ac10-3e2f6029e255_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T08:10:00-08:00",
            is_read_time="2024-12-07T08:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know the subject line of the email you sent out yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What was the subject line of the email I sent  yesterday? ",
                },
            ],
            reasoning="Right, the user is searching for the subject line of an email they sent yesterday. From checking their Mail, I can see only one email was sent yesterday, 6 December 2024. This was sent to Chloe Waters and Sophia Taylor at 15:00, with the subject line 'Thank You for Your Feedback!'. As I know this is the information the user was requesting, I can read out the subject line to them.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The name of the email subject line 'Thank You for Your Feedback!' sent on 6 December 2024 at 15:00 to Chloe Waters and Sophia Taylor is read out to the user.",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – The agent tries to retrieve emails from yesterday
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
                    ]
                ),
                # Milestone 1 – Confirm the email with the correct subject was present in the tool output from Milestone 0
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
                                                "value": "Thank You for Your Feedback!",
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
                # Milestone 2 – The agent tells the user the subject line
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Thank You for Your Feedback!",
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
                (0, 1),  # Retrieval → confirmation of correct email found
                (1, 2),  # Confirmation → user-facing answer
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_8_acd809e3-74e7-4c5b-adc5-c370d896f1ef_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T17:00:00-08:00",
            is_read_time="2024-12-06T17:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to see the last email Chloe sent you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show the last email from chloe.waters@orchardmail.com.",
                },
            ],
            reasoning="The user wants to see the last email from chloe.waters@orchardmail.com. I will look for this in Mail. \nI can see that the user received a number of messages from this address, the latest of these arrived 15:30 December 6 2024 with the subject line Re: Thank You for Your Feedback!. This must be the message the user is referring to. I will show this to the user.",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last email sent by chloe.waters@orchardmail.com at 15:30 on December 6th with the subject line Re: Thank You for Your Feedback!",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent tries to locate the relevant email
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
                # Milestone 1 – The expected email from Chloe is present in the tool output
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
                                                "value": "chloe.waters@orchardmail.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Re: Thank You for Your Feedback!",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-06T15:30:00-08:00",
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
                # Milestone 2 – Agent shows the email (or its key details) to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Re: Thank You for Your Feedback!",
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
            name="EMILY_ROSE_8_28874f5c-0113-41bd-8d92-d3a235060882_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T16:00:00-08:00",
            is_read_time="2024-12-06T16:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to reply to a recently received email related to feedback received by the user. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to the most recent email and say Thank you, I will be in touch once your feedback has been implemented",
                },
            ],
            reasoning="The user would like to reply to the most recently received email, using the text \"Thank you, I will be in touch once your feedback has been implemented\". I'll need to find the specified email by looking at the most recent item in their inbox, and once I've located the email in question I can compose the reply and seek confirmation to send it.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. An email reply is sent to sophia.taylor@orchardbusiness.org with the text "Thank you, I will be in touch once your feedback has been implemented."',
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – Agent looks up the most recent email
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
                    ]
                ),
                # Milestone 1 – Confirm Sophia’s email was found in the previous tool call
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
                                                "value": "sophia.taylor@orchardbusiness.org",
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
                # Milestone 2 – A reply email was sent to Sophia with the required text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["sophia.taylor@orchardbusiness.org"]
                                    ],
                                    "status": "sent",
                                    "body": "Thank you, I will be in touch once your feedback has been implemented",
                                    "creation_datetime_iso": "2024-12-06T16:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_subset_match_similarity,
                                "status": column_exact_match_similarity,
                                "body": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # Compare to initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Found the email -> confirmed correct email
                (1, 2),  # After confirmation -> sent reply
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_8_b7686b6c-37ae-401b-93b1-c6f5a6da41ee_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_8",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T16:15:00-08:00",
            is_read_time="2024-12-06T16:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You need to schedule time to compile the feedback from the community meeting.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Make a new event from 17:00-18:00 today called Compile feedback. ",
                },
            ],
            reasoning="The user wants to create an event. I will use the details the user has provided to create this event. \n\nThe user wants to call it Compile feedback so I shall make that the name of the event. The user has specified the duration will be one hour from 17:00-18:00 so I shall set the event for that time.      \n\nI will let the user know the event has been created. ",
            success_conditions=[
                {
                    "input_text": "1. An event called Compile feedback from 17:00-18:00 on 6 December 2024 is created. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["create_calendar_event"],
            milestones=[
                # Milestone 0 – A calendar event is created for today (2024-12-06) from 17:00–18:00 named "Compile feedback"
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Compile feedback",
                                    "start_datetime_iso": "2024-12-06T17:00:00-08:00",
                                    "end_datetime_iso": "2024-12-06T18:00:00-08:00",
                                    "creation_datetime_iso": "2024-12-06T16:15:00-08:00",
                                }
                            ),
                            # Time fields may include timezone or slight formatting differences, so allow close match
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_8_8a7a61fb-2004-4092-8a41-21493dcf0d23_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T16:00:00-08:00",
            is_read_time="2024-12-06T16:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You like Chloe and Sophia's ideas so much you wish to meet with them more directly for idea generation. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set up a little community brainstorming session with Sophia and Chloe, their ideas were amazing. Let's say its for an hour at 1 around lunch on Sunday.",
                },
            ],
            reasoning="Ok so the user wants to set up a community brainstorming session with Sophia and Chloe. First I'll establish who Sophia and Chloe are. There is only one Sophia and Chloe in the emails thread user just sent and received which means this is Sophia Taylor and Chloe Waters that user is referring to. I will add their email address as invitees' contact address. Next is the name of the event which I will keep clear and to the point. I will title the event \"Community Brainstorming\" as it fits within the intent of the event. Next is the timeframe which is given by the user, at 1 around noon, I assume it is 1 pm. I will now create the event \"Community brainstorming\" at 13:00-14:00 on 8 December 2024 with Chloe Waters and Sophia Taylor's email address as invitees' contact address.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The event "Community brainstorming" with Chloe Waters and Sophia Taylor as invitees is created for 13:00-14:00 on 8 December 2024. ',
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "create_calendar_event",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – verify that the requested community-brainstorming event was created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Community brainstorming",
                                    "start_datetime_iso": "2024-12-08T13:00:00-08:00",
                                    "end_datetime_iso": "2024-12-08T14:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "chloe.waters@orchardmail.com",  # Chloe not in contacts using email
                                            "sophia.taylor@orchardbusiness.org",  # Sophia not in contacts using email
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-06T16:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_rouge_l_similarity,  # allow minor wording variance
                                "attendees_names": column_list_subset_match_similarity,  # must include both, extras allowed,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_8_8a7a61fb-2004-4092-8a41-21493dcf0d23_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T16:00:00-08:00",
            is_read_time="2024-12-06T16:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You like Chloe and Sophia's ideas so much you wish to meet with them more directly for idea generation. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Create event "Community brainstorming" at 13:00-14:00 on Sunday and add Chloe Waters and Sophia Taylor as invitees.',
                },
            ],
            reasoning='Ok so the user wants to create an event "Community brainstorming" with Chloe Waters and Sophia Taylor as invitees at 13:00-14:00 on Sunday. First I will schedule the event with the name and start date time as given by the user. Next the invitees\' email address are in the recent email thread with the user. I will now create the event "Community brainstorming" at 13:00-14:00 on 8 December 2024 with Chloe Waters and Sophia Taylor\' email address as their contact address. And I\'ll informa user the event is correctly scheduled. ',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The event "Community brainstorming" with Chloe Waters and Sophia Taylor as invitees is created for 13:00-14:00 on 8 December 2024. ',
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "create_calendar_event",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – verify the “Community brainstorming” event was created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Community brainstorming",
                                    "start_datetime_iso": "2024-12-08T13:00:00-08:00",
                                    "end_datetime_iso": "2024-12-08T14:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "chloe.waters@orchardmail.com",  # Chloe not in contacts using email
                                            "sophia.taylor@orchardbusiness.org",  # Sophia not in contacts using email
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-06T16:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_rouge_l_similarity,
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                )
            ],
            milestone_edge_list=[],
        ),
    ]
