# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
# Auto-generated scenario extensions
import json
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
    column_rouge_l_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_tool_trace_partial_arguments_similarity,
    column_word_contains_any_similarity,
    contains_presence_similarity,
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


def get_TAG_JOHN_QUINN_pilot_plot_3(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="JOHN_QUINN_3_8e44d699-603f-405b-8a65-4eacf2e3b5f2_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "email",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
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
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to count the emails received from your father related 'Pirate Party'. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Count all of Dad's emails about the pirate party.",
                },
            ],
            reasoning="The user wants me to count emails sent by their Dad related to pirate party. I will first check for their father's contact details. I found Alfred Quinn's contact details. I will use this as the senders email address. The user wants to specifically target emails with 'pirate party'. \nI found 5 emails containing those words in the subject.",
            success_conditions=[
                {
                    "input_text": "1. The emails from alfred.quinn@svmetal.com with 'Pirate Party' in the subject found",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. User has been told there're 5 emails related with Pirate Party from Alfred Quinn has been found.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
                "remove_email_or_thread",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent tries to retrieve dad’s Pirate Party emails
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
                # Milestone 1 – Returned email list contains at least one Pirate Party email from Alfred Quinn
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
                                                "value": "alfred.quinn@svmetal.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Pirate Party",
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
                # Milestone 2 – User is informed there are exactly five Pirate Party emails
                Milestone(
                    snapshot_constraints=[
                        # Check mention of Pirate Party
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Pirate Party",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Check mention of the count “5” (numeral or word)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("5", "five")],
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
                (0, 1),  # Retrieval → validate email match
                (0, 2),  # Retrieval → final user-facing answer
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_185b864d-f194-48c6-b629-ae54e5207f04_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:30:00-07:00",
            is_read_time="2024-07-22T14:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to dictate a message to your sister saying that you will be unavailable for the next 2 hours. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a message reply to my little sis saying "Hi sis, I will be unavailable for the next 2 hours sorry about that".',
                },
            ],
            reasoning="The user wants to dictate a reply to the their \"little sis\". I am not sure who the user might be referring to. I go through the user contacts and I see there is a contact card with the alias 'Sis' attached to Grace Quinn. I can assume that's the contact the user wants to send the message to. \n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": "1. A message is sent to Grace Quinn saying that you will be unavailable for the next 2 hours.",
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
                # Milestone 0 ─ The agent tries to find the sister’s contact
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
                # Milestone 1 ─ Verify the contact result includes Grace Quinn (the sister)
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
                                                "value": "Grace Quinn",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "408-555-0126",
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
                # Milestone 2 ─ A new message to the sister is sent
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
                                            ),  # self
                                            (
                                                "408-555-0126",
                                                "grace.quinn@example.com",
                                            ),  # sister
                                        ]
                                    ],
                                    "content": [("unavailable for the next 2 hours",)],
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-22T14:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_str_contains_any_similarity,
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
                (0, 1),  # Must find contact before confirming it
                (1, 2),  # Must confirm contact before sending the message
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_18faaf47-e89b-4400-ac95-12dc0f237d31_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:30:00-07:00",
            is_read_time="2024-07-22T14:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "Your dad has been really annoying sending emails about pirate parties.  It feels like it's been a lot of emails, but you just want to see how many it has actually been in a short amount of time. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What is the number of emails my dad has sent me in the last thirty minutes?",
                },
            ],
            reasoning="The user wants to know how many emails their dad has sent them in the last thirty minutes. It's 14:30 right now, so I'll check all the emails the user has received since 14:00 because that was thirty minutes ago. The user only wants to know about emails from their dad. I see in their contacts the person with the relationship \"Father\" is Alfred Quinn, so I'll look for emails he sent the user between 14:00 and 14:30. There is Upcoming Pirate Party Events from 14:00, Join Us at the Pirate Party Rally from 14:02, Pirate Party Volunteer Opportunities from 14:04, Pirate Party Fundraiser Event from 14:06, and Pirate Party Discussion Forum Invitation from 14:08. That's five emails, so I'll tell that to the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The user is informed that Alfred Quinn has sent them five emails about pirates in the last thirty minutes.",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent uses an email-searching tool to look for dad’s messages
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
                # Milestone 1 – Agent tells the user the correct count (five/5 emails)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("five", "5")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_f8c151d1-801a-4f6c-b2d8-a85cac5d192c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:20:00-07:00",
            is_read_time="2024-07-22T14:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to delete the all the emails from your dad about the Pirate Party. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Please delete all the 'Pirate Party' emails I have received today.",
                },
            ],
            reasoning="Right so, the user wants to delete the 'Pirate Party' emails received today, 22 July 2024. Inside their Mail app, I can see five corresponding emails received between 14:00 and 14:08 from Alfred Quinn on 22 July 2024. Their subject lines are 'Upcoming Pirate Party Events',  'Join Us at the Pirate Party Rally', 'Pirate Party Volunteer', 'Pirate Party Fundraiser Event' and 'Pirate Party Discussion Forum Invitation'. Now that I have identified which emails the user would like to delete, I can confirm with the user that these are the correct ones and then delete them.",
            success_conditions=[
                {
                    "input_text": "1. The email received from Alfred Quinn on 22 July 2024 at 14:00 with the subject 'Upcoming Pirate Party Events' is deleted.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The email received from Alfred Quinn on 22 July 2024 at 14:02 with the subject 'Join Us at the Pirate Party Rally' is deleted.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The email received from Alfred Quinn on 22 July 2024 at 14:04 with the subject 'Pirate Party Volunteer Opportunities' is deleted.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "4. The email received from Alfred Quinn on 22 July 2024 at 14:06 with the subject 'Pirate Party Fundraiser Event' is deleted.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "5. The email received from Alfred Quinn on 22 July 2024 at 14:08 with the subject 'Pirate Party Discussion Forum Invitation' is deleted.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "remove_email_or_thread",
            ],
            milestones=[
                # Milestone 0 – Agent looks up today’s Pirate-Party emails
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
                # Milestone 1 – Confirm at least one Pirate-Party email was returned by the search
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
                                            # Any subject that contains “Pirate Party”
                                            "subject": {
                                                "value": "Pirate Party",
                                                "partial": True,
                                            },
                                            "sender_address": {
                                                "value": "alfred.quinn@svmetal.com",
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
                # Milestone 2 – "Pirate Party" related emails deleted
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "subject": "Upcoming Pirate Party Events",
                                }
                            ),
                            column_similarity_measure={
                                "subject": column_exact_match_similarity,
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
                # Milestone 3 – “Join Us at the Pirate Party Rally” deleted
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "subject": "Join Us at the Pirate Party Rally",
                                    "sender_address": "alfred.quinn@svmetal.com",
                                }
                            ),
                            column_similarity_measure={
                                "subject": column_exact_match_similarity,
                                "sender_address": column_exact_match_similarity,
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
                # Milestone 4 – "Pirate Party Volunteer Opportunities" deleted
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "subject": "Pirate Party Volunteer Opportunities",
                                    "sender_address": "alfred.quinn@svmetal.com",
                                }
                            ),
                            column_similarity_measure={
                                "subject": column_exact_match_similarity,
                                "sender_address": column_exact_match_similarity,
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
                # Milestone 5 – “Pirate Party Fundraiser Event” deleted
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "subject": "Pirate Party Fundraiser Event",
                                    "sender_address": "alfred.quinn@svmetal.com",
                                }
                            ),
                            column_similarity_measure={
                                "subject": column_exact_match_similarity,
                                "sender_address": column_exact_match_similarity,
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
                # Milestone 6 – “Pirate Party Discussion Forum Invitation” deleted
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "subject": "Pirate Party Discussion Forum Invitation",
                                    "sender_address": "alfred.quinn@svmetal.com",
                                }
                            ),
                            column_similarity_measure={
                                "subject": column_exact_match_similarity,
                                "sender_address": column_exact_match_similarity,
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_3edb58a8-0e06-4f0f-9395-91fb21cb07b3_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:01:00-07:00",
            is_read_time="2024-07-22T14:01:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know who just emailed you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell me the name of the sender of that communication just now.",
                },
            ],
            reasoning="The user wants to know the name of the sender of that communication just now. First I'll need to identify which communication they're talking about. I'll check their messages and emails to find any recent communications.\n\nI found an email with the subject line Upcoming Pirate Party Events received just one minute ago at 14:00 on 2024-07-22. Since this is the most recent communication the user has received, it must be the one that the user wants to know about. I can see that the sender of this email is Alfred Quinn.\n\nGreat, I'll go ahead and let the user know that Alfred Quinn emailed them just now.",
            success_conditions=[
                {
                    "input_text": "1. User is informed that the sender of their most recently received email (subject line Upcoming Pirate Party Events, received at 14:00 on 2024-07-22) is Alfred Quinn.",
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
                # Milestone 0 – Agent looks up recent emails
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
                # Milestone 1 – Confirm the expected email was found in Milestone 0’s output
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
                                                "value": "Upcoming Pirate Party Events",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "alfred.quinn@svmetal.com",
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
                # Milestone 2 – Agent tells the user the sender is Alfred Quinn
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Alfred Quinn",
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
            name="JOHN_QUINN_3_3edb58a8-0e06-4f0f-9395-91fb21cb07b3_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:01:00-07:00",
            is_read_time="2024-07-22T14:01:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know who just emailed you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who just emailed me?",
                },
            ],
            reasoning="The user wants to know who just emailed them. I'll check their email inbox to find the email they're referring to.\n\nI can see an email received just one minute ago at 14:00 on 2024-07-22, with subject line Upcoming Pirate Party Events. This must be the email the user wants to know about. Checking the sender, I can see that it was sent by Alfred Quinn.\n\nNow I can go ahead and inform the user that Alfred Quinn just emailed them.",
            success_conditions=[
                {
                    "input_text": "1. User is informed that the sender of their most recently received email (subject line Upcoming Pirate Party Events, received at 14:00 on 2024-07-22) is Alfred Quinn.",
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
                # Milestone 0 — The agent looks at the inbox
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
                # Milestone 1 — The email with the correct subject and sender is present in the
                # tool’s returned data from Milestone 0
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
                                                "value": "Upcoming Pirate Party Events",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "alfred.quinn@svmetal.com",
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
                # Milestone 2 — The agent tells the user that Alfred Quinn sent the email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Alfred Quinn",
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
            name="JOHN_QUINN_3_f8c151d1-801a-4f6c-b2d8-a85cac5d192c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:20:00-07:00",
            is_read_time="2024-07-22T14:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to delete the all the emails from your dad about the Pirate Party. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete all the emails I got from my dad today.",
                },
            ],
            reasoning="Okay so, the user wants all the emails received today from their father deleted. From their contacts, I can see Alfred Quinn is listed as their father. I am looking for any emails from Alfred received today, 22 July 2024 and I can see 5 emails corresponding. \nNow that I know that these are the emails that the user is referring to, I can then delete them. I will then inform the user that the following emails received from Alfred Quinn on 22 July 2024 between 14:00 and 14:08, with the subject lines 'Upcoming Pirate Party Events',  'Join Us at the Pirate Party Rally', 'Pirate Party Volunteer', 'Pirate Party Fundraiser Event' and 'Pirate Party Discussion Forum Invitation' have been deleted.",
            success_conditions=[
                {
                    "input_text": "1. The email received from Alfred Quinn on 22 July 2024 at 14:00 with the subject 'Upcoming Pirate Party Events' is deleted.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The email received from Alfred Quinn on 22 July 2024 at 14:02 with the subject 'Join Us at the Pirate Party Rally' is deleted.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The email received from Alfred Quinn on 22 July 2024 at 14:04 with the subject 'Pirate Party Volunteer' is deleted.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "4. The email received from Alfred Quinn on 22 July 2024 at 14:06 with the subject 'Pirate Party Fundraiser Event' is deleted.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "5. The email received from Alfred Quinn on 22 July 2024 at 14:08 with the subject 'Pirate Party Discussion Forum Invitation' is deleted.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "remove_email_or_thread",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looked up the relevant emails (optional info-retrieval check)
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
                # Milestone 1 – All five Pirate Party emails from Alfred Quinn were removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender_address": [
                                        "alfred.quinn@svmetal.com",
                                        "alfred.quinn@svmetal.com",
                                        "alfred.quinn@svmetal.com",
                                        "alfred.quinn@svmetal.com",
                                        "alfred.quinn@svmetal.com",
                                    ],
                                    "subject": [
                                        "Upcoming Pirate Party Events",
                                        "Join Us at the Pirate Party Rally",
                                        "Pirate Party Volunteer Opportunities",
                                        "Pirate Party Fundraiser Event",
                                        "Pirate Party Discussion Forum Invitation",
                                    ],
                                    "status": [
                                        "read",
                                        "read",
                                        "read",
                                        "read",
                                        "read",
                                    ],
                                }
                            ),
                            # default similarity is fine for these exact-match fields
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_8fea7dd0-8fc7-40fb-b4cd-739be715cc8c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:30:00-07:00",
            is_read_time="2024-07-22T14:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to dictate a reply to Grace Quinn saying that you will be unavailable for the next 2 days. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a message reply to Grace Quinn saying "Hi Grace I will be unavailable for the next 2 days sorry about that".',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Cookie Watson.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": "1. A reply message is sent to Grace Quinn saying that you will be unavailable for the next 2 days.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_messages",
                "get_all_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent searches or lists messages to locate the conversation with Grace
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
                    ]
                ),
                # Milestone 1 – A new outgoing message to Grace Quinn is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Both John's and Grace's contact info must appear in the conversation
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9108",
                                                "john.quinn@palantir.com",
                                            ),
                                            ("408-555-0126", "grace.quinn@example.com"),
                                        ]
                                    ],
                                    "content": "Hi Grace I will be unavailable for the next 2 days sorry about that",  # Check key phrase,
                                    "creation_datetime_iso": "2024-07-22T14:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_rouge_l_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieval of conversation precedes sending the message
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_75855665-5cc2-4902-b581-1b57e887bf45_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "email",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
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
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to tell Grace how many emails your Dad has sent you about the Pirate Party events "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How many emails have I got from Alfred Quinn about pirate party events",
                },
            ],
            reasoning='The user wants to know how many emails about pirate party events they have got from Alfred Quinn. Let me check their emails for anything mentioning "pirate party". I have found 5 emails with "Pirate party" in the subject line and they are all from Alfred Quinn. I will inform the user now.',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that there are 5 emails in their inbox from alfred.quinn@svmetal.com that mention "Pirate Party"',
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
                # Milestone 0 – Agent invokes an email-retrieval tool
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
                # Milestone 1 – The retrieved results include at least one Pirate Party email from Alfred Quinn
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
                                                "value": "alfred.quinn@svmetal.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Pirate Party",
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
                    ]
                ),
                # Milestone 2 – User-facing answer states that there are 5 Pirate Party emails
                Milestone(
                    snapshot_constraints=[
                        # Numerical mention (5 / five)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("5", "five")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        # Mention of Pirate Party context
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Pirate Party",
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
                (0, 1),  # Retrieval tool call → verify output
                (1, 2),  # Verified output → check final user response
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_782596af-1284-495e-8e60-6dea19bd665e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:20:00-07:00",
            is_read_time="2024-07-22T14:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You decide to message your Dad after all he sent you all those emails. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell Alfred Quinn \"I can't believe you're forwarding me a few emails, please respect my boundaries.\"",
                },
            ],
            reasoning="The user wants to send a message. \nFirst I should find the named person in the user's contacts. I see Alfred Quinn is saved in the user's contacts.\nNext, I will draft the message as instructed.\nA message will be sent to Alfred Quinn saying \"I can't believe you're forwarding me a few emails, please respect my boundaries.\"",
            success_conditions=[
                {
                    "input_text": "1. A message is sent to Alfred Quinn saying \"I can't believe you're forwarding me a few emails, please respect my boundaries.\"",
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
                # Milestone 0 – The agent tries to locate Alfred in the contacts list
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
                # Milestone 1 – Confirm Alfred Quinn was included in the contact-search results
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
                                                "value": "Alfred Quinn",
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
                # Milestone 2 – A new outgoing message to Alfred with the requested content exists
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require Alfred to be one of the participants (allowing either phone or email)
                                    "participants_addresses": [
                                        [
                                            (
                                                "408-555-0125",
                                                "alfred.quinn@svmetal.com",
                                            )
                                        ]
                                    ],
                                    "content": "please respect my boundaries",
                                    "creation_datetime_iso": "2024-07-22T14:20:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial DB snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.CONTACT,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact search → confirm Alfred found
                (1, 2),  # Alfred found → message sent
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_782596af-1284-495e-8e60-6dea19bd665e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:20:00-07:00",
            is_read_time="2024-07-22T14:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You decide to message your Dad after all he sent you all those emails. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell Dad \"I can't believe you're forwarding me a few emails, please respect my boundaries.\"",
                },
            ],
            reasoning="The user wishes to message their Dad. A quick glance at contacts tells me that there are no contacts listed under 'Dad'. However, if I look in messages, I can see that Alfred Quinn is tagged as father, this must be who the user is referring to.\nNext, I will compose the message as instructed.\nA message will be sent to Alfred Quinn saying \"I can't believe you're forwarding me a few emails, please respect my boundaries.\"",
            success_conditions=[
                {
                    "input_text": "1. A message is sent to Alfred Quinn saying \"I can't believe you're forwarding me a few emails, please respect my boundaries.\"",
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
                # Milestone 0 – Agent looks up Dad’s contact information
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
                # Milestone 1 – Verify Alfred Quinn was returned from the contact search
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
                                                "value": "Alfred Quinn",
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
                # Milestone 2 – Message to Dad is actually sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [("408-555-0125", "alfred.quinn@svmetal.com")]
                                    ],
                                    "content": "respect my boundaries",
                                    "creation_datetime_iso": "2024-07-22T14:20:00-07:00",
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
                (0, 1),  # contact search → verify Alfred Quinn present
                (1, 2),  # verified contact → message sent
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_75855665-5cc2-4902-b581-1b57e887bf45_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_moderate",
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
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to tell Grace how many emails your Dad has sent you about the Pirate Party events "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How many emails have I got from my dad about pirate party events",
                },
            ],
            reasoning='The user wants to know how many emails about pirate party events they have got from their dad. First I need to check their contacts and see if I can find their dad. I have found Alfred Quinn who is listed as the user\'s father. Let me check their emails for anything mentioning "pirate party". I have found 5 emails with "Pirate party" in the subject line and they are all from Alfred Quinn. I will inform the user now.',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that there are 5 emails in their inbox from alfred.quinn@svmetal.com that mention "Pirate Party"',
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
                # Milestone 0 – The agent looks through the mailbox
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
                # Milestone 1 – At least one email from dad that mentions Pirate Party is returned
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
                                                "value": "alfred.quinn@svmetal.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Pirate Party",
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
                # Milestone 2 – The agent tells the user there are 5 Pirate Party emails from dad
                Milestone(
                    snapshot_constraints=[
                        # Check that the count “5 / five” and the word “email” appear
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "5 email",
                                            "5 emails",
                                            "five email",
                                            "five emails",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        # Check the phrase “Pirate Party” is mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Pirate Party",
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
                (0, 1),  # Email search → verify correct results
                (1, 2),  # After verifying results → inform user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_4ccd82c9-13ae-4606-b179-08cbb9ce3708_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T15:00:00-07:00",
            is_read_time="2024-07-22T15:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to see the last message your sister sent you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to see the last message from Garce Quinn.",
                },
            ],
            reasoning="The user wants to see the last message from Grace Quinn.I will find the last message sent by Grace Quinn. I will show it to the user.",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last message sent from Grace Quinn at 14:17 on July 22nd that says 'Probably a good call. Just ignore it, maybe he'll stop if he doesn't get a reaction.'",
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
                # Milestone 0 – Agent attempts to retrieve messages (either by searching or listing all)
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
                # Milestone 1 – Confirm the retrieved results include Grace’s last message
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
                                                "value": "Grace Quinn",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Probably a good call.",
                                                "partial": True,  # allow substring match
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-22T14:17:00-07:00",
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
                                    "content": "Probably a good call.",
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
                (0, 1),  # Retrieval action → verify correct message in tool output
                (1, 2),  # Verified data → ensure user-facing reply contains it
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_1511cfda-f749-4466-9588-4fc8c98affe0_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "calendar",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:30:00-07:00",
            is_read_time="2024-07-22T14:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "Dad's emails being so annoying. You want to text your sister that you'll call her later and schedule the call in your calendar "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Dad’s email spam is driving me crazy. Text my sister saying I'll call her later and then schedule the call in my calendar for 6:00 pm",
                },
            ],
            reasoning="The user wants to text their sis saying they'll call them later and then schedule the call for 6:00 pm in their calendar. I must first figure out who the user wishes to send the message to. I found a contact in his contact book that his sister is Grace Quinn so I will send her a message saying \"I'll call you later\" and inform the user. \n\nI must now schedule the call in the calendar. I'll title the event \"Call Grace\" and schedule it for 6:00 pm in the user's calendar.",
            success_conditions=[
                {
                    "input_text": '1. A text is sent to Grace Quinn saying "I\'ll call you later".',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. An event "Call Grace" is scheduled in the calendar for 6:00 pm on July 22nd.',
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
                "send_message",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up (or lists) contacts to find the sister
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
                # Milestone 1 – The contact returned from the tool call in Milestone 0 includes Grace Quinn
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
                                                "value": "Grace Quinn",
                                                "partial": False,
                                            },
                                            "relationship": {
                                                "value": "Sister",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "408-555-0126",
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
                # Milestone 2 – A text message is sent to Grace saying the call will be later
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
                                            ),  # self
                                            (
                                                "408-555-0126",
                                                "grace.quinn@example.com",
                                            ),  # sister
                                        ]
                                    ],
                                    "content": [("call", "later")],
                                    "creation_datetime_iso": "2024-07-22T14:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_str_contains_any_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        ),
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
                # Milestone 3 – A calendar event “Call Grace” is created for 6 pm on 22 July 2024
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Call",
                                    "start_datetime_iso": "2024-07-22T18:00",
                                    "creation_datetime_iso": "2024-07-22T14:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.MESSAGING],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 3),  # need to figure out who Grace is first
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_bf8799dd-0c7d-4766-a5a9-0393bd39c232_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T15:00:00-07:00",
            is_read_time="2024-07-22T15:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know how many emails you have gotten from your father about the pirate party. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How many emails about the pirate party have I gotten from my father?",
                },
            ],
            reasoning="The user is asking about emails.\nFirst, I should confirm that the named person is in the user's contacts. I see Alfred Quinn is tagged as father in the user's contacts.\nNext, I will look in the user's email inbox and determine the number of emails received from this contact.\nI see a total of five emails, all of which contain the keywords pirate party, as mentioned by the user.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Number of emails received from Alfred Quinn is confirmed as 5.",
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
                # Milestone 0 – Agent looks through the email inbox
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
                # Milestone 1 – At least one Pirate-Party email from Alfred Quinn is returned
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
                                                "value": "alfred.quinn@svmetal.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Pirate",
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
                # Milestone 2 – Agent tells the user there are 5 Pirate-Party emails
                Milestone(
                    snapshot_constraints=[
                        # Check the agent mentions the correct count (5 / five)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("5", "five")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        # And explicitly references the Pirate Party topic
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Pirate Party",
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
                (0, 1),  # Email search → validate returned emails
                (1, 2),  # Confirm results → inform user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_225d7ccf-cab2-45ed-9337-167a6574b73c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "email",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:09:00-07:00",
            is_read_time="2024-07-22T14:09:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You are talking to your sister about the Pirate Party emails you've been getting from Dad and you want to have your facts straight.  You want to know when you received the first Pirate Party email from him so you can tell your sister. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When did I get the first pirate party email? ",
                },
            ],
            reasoning='The user wants to know when they received the first pirate party email. I should search their email messages for party party and see what comes up. I see the earliest message concerning a pirate party was received on July 22nd at 14:00 from Alfred Quinn and has the subject "Upcoming Pirate Party Events". I can assume that this is what the user is looking for. I\'ll share the time and date of that email with the user. ',
            success_conditions=[
                {
                    "input_text": "1. The date and time of the email received from Alfred Quinn on July 22nd at 14:00 is shown. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – The agent looks through emails
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
                # Milestone 1 – The earliest Pirate Party email (July 22 2024 14:00) is returned from that search
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
                                                "value": "Upcoming Pirate Party Events",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-22T14:00:00-07:00",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "alfred.quinn@svmetal.com",
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
                # Milestone 2 – The agent tells the user the correct date and time
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
                                            "July 22",
                                            "Jul 22",
                                            "22 July",
                                            "7-22",
                                            "07-22",
                                            "7/22",
                                            "07/22",
                                            "the 22nd",
                                            "today",
                                            "2024-07-22T14:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                        # Check time mention (any reasonable phrasing)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        ("2:00", "2 pm", "2 pm", "14:00", "2pm")
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
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
            name="JOHN_QUINN_3_d063dac2-694d-455d-9f30-b6204522a419_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:20:00-07:00",
            is_read_time="2024-07-22T14:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You decide to email back your Dad after all he sent you all those emails and then you forward that message to your sister. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell Dad \"I can't believe you're forwarding me these many emails, please respect my boundaries. Pirate parties are lame and we both know that\" and then forward that to my sister. ",
                },
            ],
            reasoning="The user wishes to email their Dad. A quick glance at contacts tells me that there are no contacts listed under 'Dad'. However, if I look in messages, I can see that Alfred Quinn is tagged as father, this must be who the user is referring to.\nNext, I need to figure out which channel of communication does the the user want. There're no message history between them, but there're a bunch of emails from Alfred, I will compose the email as instructed.\nAn email will be sent to Alfred Quinn saying \"I can't believe you're forwarding me these many emails, please respect my boundaries. Pirate parties are lame and we both know that\". \nThe user then wants me to forward this message to their sister. I will go through the user's contacts to understand who this might be referring to. I see there is a contact with alias 'Sis' under the user's contacts, and this is 'Grace Quinn'. This seems the person to forward the message to. ",
            success_conditions=[
                {
                    "input_text": "1. An email is sent to Alfred Quinn saying \"I can't believe you're forwarding me these many emails, please respect my boundaries. Pirate parties are lame and we both know that.\"",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The same email sent to Alfred Quinn is then forwarded to Grace Quinn.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_email",
                "send_message",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks up contacts to figure out who “Dad” is
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
                # Milestone 1 – Alfred Quinn (Dad) appears in the most-recent contact-search result
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
                                                "value": "Alfred Quinn",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "408-555-0125",
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
                # Milestone 2 – The agent looks up contacts to figure out who “sister” is
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
                # Milestone 3 – Grace Quinn (sister) appears in the same / next contact-search result
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
                                                "value": "Grace Quinn",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "408-555-0126",
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
                # Milestone 4 – A new outgoing message to Alfred Quinn was created with the requested text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["alfred.quinn@svmetal.com"]
                                    ],
                                    "body": "respect my boundaries",
                                    "creation_datetime_iso": "2024-07-22T14:20:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "body": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
                # Milestone 5 – The same text is forwarded / sent to Grace Quinn via correct tools
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "tool_trace": json.dumps(
                                        {
                                            "tool_name": "send_email",
                                            "arguments": {
                                                "email_action": "send",
                                                "email_id_referred": "place_holder",  # must send email with an email id to forward an email
                                                "email_id_referred_action": "forward",
                                            },
                                        },
                                        ensure_ascii=False,
                                    )
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": column_tool_trace_partial_arguments_similarity
                            },
                        ),
                    ],
                ),
                # Milestone 6 – The same text is forwarded / sent to Grace Quinn
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["grace.quinn@example.com"]
                                    ],
                                    "body": "respect my boundaries",
                                    "subject": "Fwd",
                                    "creation_datetime_iso": "2024-07-22T14:20:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "body": column_contains_similarity,
                                "subject": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup for Dad → verify Alfred found
                (2, 3),  # Contact lookup for sister → verify Grace found
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_beae55c3-5548-434a-ad63-98f933877e94_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T17:40:00-07:00",
            is_read_time="2024-07-22T17:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You are sick of the spam emails coming from Alfred Quinn and want to block his email address.  You need to find his email address first. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What is my Dad's email address?",
                },
            ],
            reasoning="The user wants to know their Dad's email address. I first need to figure out who they mean. I should check their Contacts for one named Dad.\n\nHmm, I can't see a Contact named Dad, but there is one with Father in their Contact Card, Alfred Quinn, and I know Father is a synonym for Dad so this must be who the user means. \n\nNext I will check Alfred's contact card for their email address. Looks like it's alfred.quinn@svmetal.com. \n\nI will now pass this information on to the user. ",
            success_conditions=[
                {
                    "input_text": "1. Contacts is searched for the email address of Alfred Quinn and given to the user as alfred.quinn@svmetal.com.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts"],
            milestones=[
                # Milestone 0 – Agent queries Contacts to locate “Dad / Alfred Quinn”
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
                # Milestone 1 – Tool result includes Alfred Quinn with his email address
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
                                                "value": "Alfred Quinn",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "alfred.quinn@svmetal.com",
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
                # Milestone 2 – Agent tells the user the correct email address
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "alfred.quinn@svmetal.com",
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
                (0, 1),  # Contact search → verify result contains Alfred’s info
                (1, 2),  # Retrieved info → agent answers user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_18faaf47-e89b-4400-ac95-12dc0f237d31_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "email",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:30:00-07:00",
            is_read_time="2024-07-22T14:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "Your dad has been really annoying sending emails about pirate parties.  It feels like it's been a lot of emails, but you just want to see how many it has actually been in a short amount of time. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How many pirate emails have I gotten in the past 30 minutes?",
                },
            ],
            reasoning='The user wants to know how many emails about pirates they have received since 14:00 today July 22nd. It is 14:30 right now so I\'ll see how many emails have come in since 14:00 with the word "pirate" in the subject line. I see five emails with a time stamp between 14:00 and 14:30 the word "pirate" in the subject line, all from Alfred Quinn, so I\'ll tell the user 5.',
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The user is informed that Alfred Quinn has sent them five emails about pirates in the last thirty minutes.",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – the agent tries to inspect the mailbox
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
                # Milestone 1 – from the previous email-search, at least one pirate-related email
                # from Alfred Quinn is returned (confirms correct filtering logic)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=partial(
                                    result_list_match_existence_extractor,
                                    match_conditions={
                                        "sender_address": {
                                            "value": "alfred.quinn@svmetal.com",
                                            "partial": False,
                                        },
                                        "subject": {"value": "Pirate", "partial": True},
                                    },
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
                # Milestone 2 – the user is informed they received five pirate emails
                Milestone(
                    snapshot_constraints=[
                        # Must mention the number 5 / five
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("five", "5")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        # Must mention that they are pirate emails (context confirmation)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "pirate",
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
            name="JOHN_QUINN_3_beae55c3-5548-434a-ad63-98f933877e94_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T17:40:00-07:00",
            is_read_time="2024-07-22T17:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You are sick of the spam emails coming from Alfred Quinn and want to block his email address.  You need to find his email address first. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you tell me Alfred's email address?",
                },
            ],
            reasoning="The user wants to know Alfred's email address. I should first check their Contacts for a contact with that name. \n\nI only see one contact with the name Alfred, Alfred Quinn, so this must be who the user means. Next I'll check Alfred's contact card to see if it contains their email address. \n\nTurns out Alfred's email address is alfred.quinn@svmetal.com. I will tell the user this. ",
            success_conditions=[
                {
                    "input_text": "1. Contacts is searched for the email address of Alfred Quinn and given to the user as alfred.quinn@svmetal.com.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts"],
            milestones=[
                # Milestone 0 – A contact-lookup tool is invoked (either a direct search or full listing)
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
                # Milestone 1 – The returned contact data from Milestone 0 includes Alfred Quinn with the correct e-mail
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
                                                "value": "Alfred Quinn",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "alfred.quinn@svmetal.com",
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
                # Milestone 2 – The agent tells the user Alfred’s e-mail address
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "alfred.quinn@svmetal.com",
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
            name="JOHN_QUINN_3_18faaf47-e89b-4400-ac95-12dc0f237d31_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "email",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:30:00-07:00",
            is_read_time="2024-07-22T14:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "Your dad has been really annoying sending emails about pirate parties.  It feels like it's been a lot of emails, but you just want to see how many it has actually been in a short amount of time. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How many emails has Alfred Quinn sent since 14:00?",
                },
            ],
            reasoning="The user wants to know how many emails Alfred Quinn has sent them since 14:00 today July 22nd. It is 14:30 right now so I'll see how many emails have come in since 14:00. I see five emails with a time stamp between 14:00 and 14:30, so I'll tell the user 5.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The user is informed that Alfred Quinn has sent them five emails about pirates in the last thirty minutes.",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent invokes a tool to retrieve emails
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
                # Milestone 1 – Agent tells the user that Alfred sent 5 emails
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Accept any phrasing that clearly states the count “5 emails”
                                    "content": [("5 email", "five email")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_d063dac2-694d-455d-9f30-b6204522a419_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:20:00-07:00",
            is_read_time="2024-07-22T14:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You decide to message your Dad via email after all he sent you all those emails and then you forward that message to your sister. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Compose a reply for my stupid dad saying \"I can't believe you're forwarding me these many emails, please respect my boundaries. Pirate parties are lame and we both know that\" and send it to him. Then forward the message to my sister.",
                },
            ],
            reasoning="The user first tells me that they want to compose a reply for their stupid dad.\nFirst I should understand who 'stupid dad' might be referring to. I see Alfred Quinn is saved in the user's contacts as 'Dad', and based on the context I believe the user is upset, hence the 'stupid dad'. \nNext, I need to figure out which channel of communication does the the user want. There're no message history between them, but there're a bunch of emails from Alfred, I will draft the email as instructed. The user says that I should send the message to 'him', which is the pronoun likely referring to Alfred Quinn.\nA message will be sent to Alfred Quinn saying \"I can't believe you're forwarding me these many emails, please respect my boundaries. Pirate parties are lame and we both know that\". \nAfter this, the user wants to forward the same message to his 'sister'. I will have to go through the user's contact to find out who they might be referring to. It is now when I figure out the user is referring to 'Grace Quinn', who is listed as 'sis' in the user's contacts. I will forward the same email via forwarding action I sent to the user's father to her. ",
            success_conditions=[
                {
                    "input_text": "1. An email is sent to Alfred Quinn saying \"I can't believe you're forwarding me these many emails, please respect my boundaries. Pirate parties are lame and we both know that.\"",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The same email sent to Alfred Quinn is then forwarded to Grace Quinn.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_email",
                "get_all_emails",
                "search_emails",
                "send_message",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks up emails to find email from dad
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
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – A message is sent to Alfred Quinn with the requested text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["alfred.quinn@svmetal.com"]
                                    ],
                                    "body": "please respect my boundaries",
                                    "creation_datetime_iso": "2024-07-22T14:20:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "body": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ],
                ),
                # Milestone 2 – The agent tries to find the sister in contacts
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
                # Milestone 3 – Confirm that Grace Quinn (the sister) appeared in the contact search result
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
                                                "value": "Grace Quinn",
                                                "partial": False,
                                            },
                                            "relationship": {
                                                "value": "Sister",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "408-555-0126",
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
                    ],
                ),
                # Milestone 4 – The same email (forward) is sent to Grace Quinn via proper tool action
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "tool_trace": json.dumps(
                                        {
                                            "tool_name": "send_email",
                                            "arguments": {
                                                "email_action": "send",
                                                "email_id_referred": "place_holder",  # must send email with an email id to forward an email
                                                "email_id_referred_action": "forward",
                                            },
                                        },
                                        ensure_ascii=False,
                                    )
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": column_tool_trace_partial_arguments_similarity
                            },
                        ),
                    ],
                ),
                # Milestone 5 – The same email (forward) is sent to Grace Quinn
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        [
                                            "grace.quinn@example.com",
                                        ]
                                    ],
                                    "subject": "Fwd",
                                    "body": "please respect my boundaries",
                                    "creation_datetime_iso": "2024-07-22T14:20:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "subject": column_contains_similarity,
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
                (2, 3),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_fc752c4f-4946-4412-8f85-0c43f36d422f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
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
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to delete all of your father's emails because they are annoying you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Please delete all the emails Dad has sent me today.",
                },
            ],
            reasoning='The user wants me to delete all the emails they received from their Dad today. First, I will figure out which contact this is. I can see in the user\'s contacts, there is an "Alfred Quinn" under the "father" relationship. Now, I will check the emails to figure out how many I must delete. I can see 5 emails received from this contact today.  ',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The email with the subject line "Upcoming Pirate Party Events" from Alfred Quinn is deleted.',
                },
                {
                    "input_text": '2. The email with the subject line "Join Us at the Pirate Party Rally" from Alfred Quinn is deleted.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '3. The email with the subject line "Pirate Party Volunteer Opportunities" from Alfred Quinn is deleted.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '4. The email with the subject line "Pirate Party Fundraiser Event" from Alfred Quinn is deleted.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '5. The email with the subject line "Pirate Party Discussion Forum Invitation" from Alfred Quinn is deleted. ',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
                "remove_email_or_thread",
            ],
            milestones=[
                # Milestone 0 – The agent looks up today’s emails (dad’s messages) via an email-retrieval tool
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
                # Milestone 1 – The five unwanted emails from Alfred Quinn are gone
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "subject": [
                                        "Upcoming Pirate Party Events",
                                        "Join Us at the Pirate Party Rally",
                                        "Pirate Party Volunteer Opportunities",
                                        "Pirate Party Fundraiser Event",
                                        "Pirate Party Discussion Forum Invitation",
                                    ],
                                    "sender_address": [
                                        "alfred.quinn@svmetal.com",
                                        "alfred.quinn@svmetal.com",
                                        "alfred.quinn@svmetal.com",
                                        "alfred.quinn@svmetal.com",
                                        "alfred.quinn@svmetal.com",
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "subject": column_rouge_l_similarity,
                                "sender_address": column_exact_match_similarity,
                            },
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Agent retrieves emails → emails are deleted
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_225d7ccf-cab2-45ed-9337-167a6574b73c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:09:00-07:00",
            is_read_time="2024-07-22T14:09:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You are talking to your sister about the Pirate Party emails you've been getting from Dad and you want to have your facts straight.  You want to know when you received the first Pirate Party email from him so you can tell your sister. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When did I get the first email from Dad since this week? ",
                },
            ],
            reasoning="The user wants to know when they received the first email from Dad. I wonder who Dad is. I see from their contacts that Alfred Quinn is listed as Father so this must be who they mean. I'll search for the earliest email the user received from them and tell them when exactly it was received. I see that the earliest email received from Alfred Quinn was received on July 22nd at 14:00 so I'll share that date and time with the user. ",
            success_conditions=[
                {
                    "input_text": "1. The date and time of the email received from Alfred Quinn on July 22nd at 14:00 is shown. ",
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
                # Milestone 1 – Tool output contained the first Pirate Party email from Dad (Alfred Quinn at 2024-07-22 14:00)
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
                                                "value": "alfred.quinn@svmetal.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-22T14:00:00-07:00",
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
                # Milestone 2 – Agent’s reply to the user includes the correct date and time
                Milestone(
                    snapshot_constraints=[
                        # Date mention
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "July 22",
                                            "Jul 22",
                                            "22 July",
                                            "7-22",
                                            "07-22",
                                            "7/22",
                                            "07/22",
                                            "the 22nd",
                                            "today",
                                            "2024-07-22T14:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                        # Time mention
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "14:00",
                                            "2:00 pm",
                                            "2 pm",
                                            "2pm",
                                            "2 p.m.",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Email retrieval → verify correct email found
                (1, 2),  # Correct email found → user response contains the info
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_1511cfda-f749-4466-9588-4fc8c98affe0_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "calendar",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T14:30:00-07:00",
            is_read_time="2024-07-22T14:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "Your dad sent a bunch of emails that are quite annoying. You want to text your sister that you'll call her later and schedule the call in your calendar "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Dad’s email spam is driving me crazy. Text my sis saying I'll call her later and then schedule the call in my calendar for 6:00 pm",
                },
            ],
            reasoning="The user wants to text their sister saying they'll call her later and then schedule the call for 6:00 pm in their calendar. The user only has one sister listed in their contacts named Grace Quinn so I will text Grace \"I'll call you later\" and inform the user. \n\nI must now schedule the call in the calendar. I'll title the event \"Call Grace\" and schedule it for 6:00 pm in the user's calendar.",
            success_conditions=[
                {
                    "input_text": '1. A text is sent to Grace Quinn saying "I\'ll call you later".',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. An event "Call Grace" is scheduled in the calendar for 6:00 pm on July 22nd.',
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
                "send_message",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent tries to find the sister in contacts
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
                # Milestone 1 – Confirm that Grace Quinn (the sister) appeared in the contact search result
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
                                                "value": "Grace Quinn",
                                                "partial": False,
                                            },
                                            "relationship": {
                                                "value": "Sister",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "408-555-0126",
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
                # Milestone 2 – A text message was sent to Grace saying "I'll call you later"
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
                                            ),  # self
                                            (
                                                "408-555-0126",
                                                "grace.quinn@example.com",
                                            ),  # sister
                                        ]
                                    ],
                                    "content": [("call", "later")],
                                    "creation_datetime_iso": "2024-07-22T14:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_str_contains_any_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        ),
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
                # Milestone 3 – A calendar event for the call at 6:00 pm on July 22 2024 is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Call Grace",
                                    "start_datetime_iso": "2024-07-22T18:00:00",
                                    "creation_datetime_iso": "2024-07-22T14:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        ),
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
                (1, 3),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_bf8799dd-0c7d-4766-a5a9-0393bd39c232_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "email",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T15:00:00-07:00",
            is_read_time="2024-07-22T15:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know how many emails you have gotten from your father about the pirate party. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How many emails about the Pirate Party have I gotten from Alfred Quinn?",
                },
            ],
            reasoning="The user is asking about emails.\nFirst, I should confirm that the named person is in the user's contacts. I see Alfred Quinn in the user's contacts.\nNext, I will look in the user's email inbox and determine the number of emails received from this contact.\nI see a total of five emails, all of which contain the keywords pirate party, as mentioned by the user.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Number of emails received from Alfred Quinn is confirmed as 5.",
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
                # Milestone 0 – Agent retrieves or searches the mailbox
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
                # Milestone 1 – Agent tells the user the correct count (5 emails about Pirate Party)
                Milestone(
                    snapshot_constraints=[
                        # Must mention the Pirate Party topic
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Pirate Party",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Must state the quantity (5 / five)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("5", "five")],
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
                (0, 1),  # Retrieval of emails → user-facing answer
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_3_4ccd82c9-13ae-4606-b179-08cbb9ce3708_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_3",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T15:00:00-07:00",
            is_read_time="2024-07-22T15:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to see the last message your sister sent you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to see the last message from my sister.",
                },
            ],
            reasoning="The user wants to see the last message from their sister. Okay let me look for their sister in contacts. it appears to be Grace Quinn. I will find the last message sent by Grace Quinn. I will show it to the user.",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last message sent from Grace Quinn at 14:17 on July 22nd that says 'Probably a good call. Just ignore it, maybe he'll stop if he doesn't get a reaction.'",
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
                # Milestone 0 – Agent retrieves messages (satisfies information-retrieval requirement)
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
                # Milestone 1 – Agent shows the user the correct last message from Grace Quinn
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Probably a good call.",  # key phrase from the sister’s last message
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,  # just needs to include the phrase
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (
                    0,
                    1,
                ),  # The user-facing response should logically follow the retrieval step
            ],
        ),
    ]
