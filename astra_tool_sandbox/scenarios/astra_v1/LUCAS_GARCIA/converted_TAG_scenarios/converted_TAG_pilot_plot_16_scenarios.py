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
    column_list_exact_match_similarity,
    column_list_subset_match_similarity,
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_rouge_l_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_tool_trace_partial_arguments_similarity,
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


def get_TAG_LUCAS_GARCIA_pilot_plot_16(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="LUCAS_GARCIA_16_d34487e9-3b48-41b9-8dbb-e5065cc42b48_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T18:00:00-08:00",
            is_read_time="2024-12-09T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to reply to the message you just received about the coffee shop. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to my beloved coffee shop owner's message saying sounds fantastic. Let me know when it's a good time for the taste test. Speak Soon.",
                },
            ],
            reasoning="User wants to reply to a contact's message. They address the contact as \"beloved coffee shop owner\". By checking user's contacts I see user's father Juan Garcia owns a coffee shop. So I believe user is referring to their father Juan Garcia. I'll check if there's message from Juan. I didn't find any message exchanged between the user and their father. I'll check if there's any email, as email can count as a type of message. Ok, I found emails exchanged just now between user and their father. So I understand user actually wants to reply to Juan Garcia's email saying sounds fantastic. Let me know when it's a good time for the taste test. Speak Soon. I'll draft the email and send the reply. I'll inform user that the email is sent.",
            success_conditions=[
                {
                    "input_text": "1. A reply is sent to Juan Garcia's email saying \"Sounds fantastic. Let me know when it's a good time for the taste test. Speak Soon.\"",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "search_messages",
                "get_all_messages",
                "send_email",
                "send_message",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent retrieves existing emails (to find Dad's email to reply to)
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
                # Milestone 1 – Confirm Juan Garcia's email thread was retrieved from previous email search
                # We just need to know that an email from juan.garcia@example.com exists in the tool result.
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
                                                "value": "juan.garcia@example.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Healthy Snack Options for the Coffee Shop",
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
                # Milestone 2 – A reply email is sent to Juan with the correct body content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # email must be sent to Dad
                                    "recipients_addresses": [
                                        ["juan.garcia@example.com"]
                                    ],
                                    # body should contain the key phrases of the requested reply
                                    "body": "Let me know",
                                    "creation_datetime_iso": "2024-12-09T18:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                # allow minor formatting / spacing variations while requiring same content
                                "body": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Email search → confirm Juan's email is found
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_6af4cf88-a6e5-4bed-81b8-56f3854f5b72_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "email",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T17:15:00-08:00",
            is_read_time="2024-12-09T17:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You just got home after visiting your Dad's coffee shop to discuss expanding healthy snack options.  He said he'd send you an email afterwards about it, so you're wondering if he did that yet.  Once you check, you also want to forward the e-mail to Sarah Lopez to consider these healthy snack options for your clients' dietary plans and recommendations. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you please double check if Dad has already sent an e-mail on healthy snack options? If so, then forward it to my dietary advisor?",
                },
            ],
            reasoning="Okey, first of all the user wants to double check if their Dad has already sent an email. I need to figure out who the user is referring to by 'Dad'. I will scrutinize the user contacts. There, I see there is a contact card for 'Juan Garcia' with alias 'Dad'. The user is referring to this contact. Based on this information, I will now explore the user context communications. The user mentions 'e-mail' on their query, so I will start with this app. There, I see an e-mail sent by Juan Garcia on December 09 2024 at 17:00:00. The user request has been made on December 09 2024 at 17:15:00, so I can now assume that \"the e-mail from Dad\" has been sent. I can notify the user. \n\nAfter this, the user wants to forward this e-mail to his 'dietary advisor'. I will need to figure out how the user is referring to. I will go through the user contacts again. There, I see there is a contact card with the alias and tag 'Dietitian consultant'. The user said 'dietary advisor', which is another way to refer to 'Dietitian consultant'. This contact card is for Sarah Lopez, so I can use the e-mail address stored in their contact card to forward Juan Garcia's email to them. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The email from Juan Garcia, received on December 9th, 2024, at 17:00, is shown to the user. ",
                },
                {
                    "input_text": "2. The email from Juan Garcia on healthy snack options is forwarded to dietitian consultant Sarah Lopez. ",
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
                "get_all_emails",
                "search_emails",
                "send_email",
            ],
            milestones=[
                # Milestone 0 –  Agent looks for the dad’s email in the mailbox
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
                # Milestone 1 –  Verify that the dad’s 17:00 healthy-snack email was in the search results
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
                                                "value": "juan.garcia@example.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Healthy Snack Options",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-09T17:00:00-08:00",
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
                # Milestone 2 – Agent looks up contacts (either search or list all)
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
                # Milestone 3 – The returned contact information contains Sarah Lopez with correct phone number
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
                                                "value": "Sarah Lopez",
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
                # Milestone 4 –  A new forwarded email is sent to Sarah Lopez
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["sarah.lopez@example.com"]
                                    ],
                                    "subject": "Healthy Snack Options",
                                    "creation_datetime_iso": "2024-12-09T17:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "subject": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (2, 3)],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_533b88c8-e016-4c5f-bd79-c54fff30fd14_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "messaging",
                "email",
                "misinformation_no",
                "insufficient_context_no",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T17:15:00-08:00",
            is_read_time="2024-12-09T17:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to thank your dad for the kind words.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to Dad\'s email; "Thanks Dad, Hope they work out! Regards, Lucas."',
                },
            ],
            reasoning="Ok so the user wants to reply to dad's email with a given message. First I will establish who dad is. The contact Juan Garcia is labelled as dad in the user's contacts. Next is the method of communication which is given by the user. I will now message the user's given message to Juan Garcia via email at 17:15 on 9 December 2024. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message "Thanks Dad, Hope they work out! Regards, Lucas" is sent to Juan Garcia via email.',
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_messages",
                "get_all_messages",
                "search_emails",
                "get_all_emails",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Retrieve Dad's email (the one to reply to)
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
                # Milestone 1 – Confirm Juan's email about healthy snack options was retrieved
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
                                                "value": "juan.garcia@example.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Healthy Snack Options for the Coffee Shop",
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
                # Milestone 2 – Email reply sent to Juan with the requested message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["juan.garcia@example.com"]
                                    ],
                                    "status": "sent",
                                    "body": "Thanks Dad, Hope they work out! Regards, Lucas.",
                                    "creation_datetime_iso": "2024-12-09T17:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                # Allow slight variations but ensure key phrases are present
                                "body": column_rouge_l_similarity,
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
                (
                    0,
                    1,
                ),  # Retrieved the relevant email thread → confirmed it's Dad's email
                (1, 2),  # Confirmed correct email → sent reply with correct content
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_e7968af2-cd67-42c4-8908-da1736132769_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T19:00:00-08:00",
            is_read_time="2024-12-09T19:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "Your father is very much interested in expanding the range of snacks in the coffee shop.  He also asked if you knew anyone who was interested in nutrition who could help him out with some leaflets and posters. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Let me see Sarah Lopez's number.",
                },
            ],
            reasoning="The user is asking for a phone number.\nFirst I should find the named contact. \nI have found Sarah Lopez in the user's contacts.\nSarah Lopez's number is saved as +1 12345-6789-1000-9630.\nI should provide this to the user.",
            success_conditions=[
                {
                    "input_text": "1. Sarah Lopez's phone number is provided to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_contacts", "get_all_contacts"],
            milestones=[
                # Milestone 0 – Agent looks up contacts (either search or list all)
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
                # Milestone 1 – The returned contact information contains Sarah Lopez with correct phone number
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
                                                "value": "Sarah Lopez",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 12345-6789-1000-9630",
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
                # Milestone 2 – Agent replies to the user with Sarah Lopez's phone number
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "12345-6789-1000-9630",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity  # ensure number is present somewhere in reply
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # contact lookup -> verify Sarah returned
                (1, 2),  # confirmed contact -> respond to user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_65a3a111-2297-4de5-a827-a821bbd85a07_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T19:00:00-08:00",
            is_read_time="2024-12-09T19:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to see if your dad responded to your email. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did my dad reply to the email I sent him earlier today? Yes or no.",
                },
            ],
            reasoning="The user wants me to check they got a reply from their dad. They specified it would be a reply from an email sent today. \nI check the users emails for emails sent to their dad on 9th December 2024.\nI find one that was sent at 16:00. \nThere is one reply. I pull up the email for the user and reply with Yes.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The users email is checked for a response to their email sent to Juan Garcia at 16:00 on December 9th 2024 and the response Yes is presented to the user",
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent searches / retrieves emails
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
                # Milestone 1 – Confirm dad’s reply email was returned from the email search
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
                                                "value": "juan.garcia@example.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Re: Healthy Snack Options",
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
                # Milestone 2 – Agent informs the user that dad replied and surfaces key content
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
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_f4e6b261-729b-4d71-83fe-cfb188442a91_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T16:15:00-08:00",
            is_read_time="2024-12-09T16:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You've suddenly realised that you may have forgotten to actually attach the PDF document to the email you sent your dad. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Is there an attachment with the email I sent to Dad? Yes or no.",
                },
            ],
            reasoning="The user wants to know if there is an attachment with the email they sent to Dad. First I'll need to figure out who Dad is.\n\nI can see that Juan Garcia is listed as \"Dad\" in the user's contacts, so this must be the contact they mean. I'll now look for an email sent by the user to Juan Garcia.\n\nThe user has sent one email to Juan Garcia: subject line \"Healthy Snack Options for the Coffee Shop\", sent at 16:00 on December 9th, 2024. I'll check for any attachments to this email.\n\nThere is an attachment called Healthy_Snack_Recipes_Dec2024.pdf. I'll go ahead and inform the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. User is informed that the email they sent to juan.garcia@example.com at 16:00 on 2024-12-09 with subject line "Healthy Snack Options for the Coffee Shop" has an attachment called Healthy_Snack_Recipes_Dec2024.pdf.',
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent looks up emails
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
                # Milestone 1 – Email to Dad with the expected attachment is found
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
                                                "value": "Healthy Snack Options for the Coffee Shop",
                                                "partial": False,
                                            },
                                            "attachments": {
                                                "value": "Healthy_Snack_Recipes_Dec2024.pdf",
                                                "partial": True,
                                            },
                                            "recipients_addresses": {
                                                "value": "juan.garcia@example.com",
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
                # Milestone 2 – Agent informs the user that the email has the attachment
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
                (0, 1),  # Email search → confirm correct email located
                (1, 2),  # Confirmation of email info → user-facing response
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_5179074c-e748-4f2b-9fa0-a9c7ad0a3145_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T11:05:00-08:00",
            is_read_time="2024-12-10T11:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to see the last email your dad sent you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show the last email from Juan Garcia.",
                },
            ],
            reasoning="The user wants to see Juan Garcia's last email. I first need to know Juan's email address to check for the email. I will check Contacts for a Juan. \nLooks like there is only one Juan in the user's Contacts, Juan Garcia, so this must be who the user means. Next I will check Juan's contact card for an email address. Looks like it's juan.garcia@example.com. \nNext I will check Mail for the last email from this address. \nSeems like it was received on December 9th at 17:00 with the subject line Re: Healthy Snack Options for the Coffee Shop. I will present this to the user. ",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last email from juan.garcia@example.com sent on December 9th at 17:00 with the subject line Re: Healthy Snack Options for the Coffee Shop. ",
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
                # Milestone 0 – Agent looks for emails (must invoke email-retrieval tool)
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
                # Milestone 1 – Confirm the desired email appears in the tool output from Milestone 0
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
                                                "value": "juan.garcia@example.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Re: Healthy Snack Options for the Coffee Shop",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-09T17:00:00-08:00",
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
                # Milestone 2 – Agent shows the email to the user (must mention the subject at minimum)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Re: Healthy Snack Options for the Coffee Shop",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_5179074c-e748-4f2b-9fa0-a9c7ad0a3145_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T11:05:00-08:00",
            is_read_time="2024-12-10T11:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to see the last email your dad sent you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show the last email from dad.",
                },
            ],
            reasoning="The user wants to see the last email from their dad. Let me look for this person in Contacts. It is Juan Garcia. Next I will check Juan's contact card for an email address. Looks like it's juan.garcia@example.com. \nNext I will check Mail for the last email from this address. \nSeems like it was received on December 9th at 17:00 with the subject line Re: Healthy Snack Options for the Coffee Shop. I will present this to the user. ",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last email from juan.garcia@example.com sent on December 9th at 17:00 with the subject line Re: Healthy Snack Options for the Coffee Shop. ",
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
                # Milestone 0 – Agent looks up emails (dad’s last email should be discoverable)
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
                # Milestone 1 – Tool result included the expected email from Juan Garcia
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
                                                "value": "juan.garcia@example.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Healthy Snack Options",
                                                "partial": True,  # allow any prefix like “Re:”
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-09T17:00:00-08:00",
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
                            reference_milestone_node_index=0,  # depend on Milestone 0 tool call
                        )
                    ],
                ),
                # Milestone 2 – Agent’s response to user contains the key subject (evidence email shown)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Re: Healthy Snack Options for the Coffee Shop",
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
            name="LUCAS_GARCIA_16_f4e6b261-729b-4d71-83fe-cfb188442a91_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T16:15:00-08:00",
            is_read_time="2024-12-09T16:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You've suddenly realised that you may have forgotten to actually attach the PDF document to the email you sent your dad. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I include the Healthy_Snack_Recipes_Dec2024.pdf attachment in the healthy snack options email I sent to my dad? Yes or No.",
                },
            ],
            reasoning="The user wants to know if they included the Healthy_Snack_Recipes_Dec2024.pdf attachment in the healthy snack options email that they sent to their dad. I'll check their contacts to determine who their dad is.\n\nI can see that Juan Garcia is saved as the user's father, so now I'll see if I can find the email they mentioned.\n\nI found the email the user asked about: subject line \"Healthy Snack Options for the Coffee Shop\", sent at 16:00 on December 9th, 2024 to Juan Garcia. I'll check for any attachments to this email.\n\nThere is an attachment called Healthy_Snack_Recipes_Dec2024.pdf. I will let the user know.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. User is informed Yes, that the email they sent to juan.garcia@example.com at 16:00 on 2024-12-09 with subject line "Healthy Snack Options for the Coffee Shop" has an attachment called Healthy_Snack_Recipes_Dec2024.pdf.',
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
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
                # Milestone 1 – Confirm the retrieved email is the correct one and has the PDF attachment
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
                                                "value": "Healthy Snack Options for the Coffee Shop",
                                                "partial": False,
                                            },
                                            "recipients_addresses": {
                                                "value": "juan.garcia@example.com",
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
                # Milestone 2 – The agent tells the user the email indeed contained the attachment
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
                (0, 1),  # Email search → verify correct email data
                (1, 2),  # Verified data → inform the user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_65a3a111-2297-4de5-a827-a821bbd85a07_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T19:00:00-08:00",
            is_read_time="2024-12-09T19:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to see if your dad responded to your email. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you see if I got a reply to the email I sent today at 16:00 with the subject 'Healthy Snack Options for the Coffee Shop'",
                },
            ],
            reasoning="The user wants me to check for a reply to an email sent by them at 16:00 on December 9th 2024. It has the subject 'Healthy Snack Options for the Coffee Shop'. I check the users sent emails. I found the requested email. It has one response. I present it to the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The users email is checked for a response to their email sent to Juan Garcia at 16:00 on December 9th 2024 and the response is presented to the user",
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
                    ],
                ),
                # Milestone 1 – Confirm the reply email from Juan was included in the retrieved results
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
                                                "value": "juan.garcia@example.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Re: Healthy Snack Options for the Coffee Shop",
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
                # Milestone 2 – Agent informs the user that a reply was found and summarizes / presents it
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "recipes look fantastic",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,  # ensure key phrase from Dad's reply is surfaced
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Tool usage → verify retrieved reply
                (1, 2),  # Retrieved reply → agent tells user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_e7968af2-cd67-42c4-8908-da1736132769_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T19:00:00-08:00",
            is_read_time="2024-12-09T19:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "Your father is very much interested in expanding the range of snacks in the coffee shop.  He also asked if you knew anyone who was interested in nutrition who could help him out with some leaflets and posters. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Let me see the dietitian consultant's phone number.",
                },
            ],
            reasoning="The user is asking for a phone number.\nFirst I should find the named contact. The user has referred to them as a dietitian consultant. I should search their contacts with this in mind. I see one potential match, Sarah Lopez, who is tagged as Dietitian consultant. This must be who the user is referring to.\nI have found Sarah Lopez in the user's contacts.\nSarah Lopez's number is saved as +1 12345-6789-1000-9630.\nI should provide this to the user.",
            success_conditions=[
                {
                    "input_text": "1. Sarah Lopez's phone number is provided to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_contacts", "get_all_contacts"],
            milestones=[
                # Milestone 0 – Agent invokes a contact-retrieval tool
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
                # Milestone 1 – Tool output includes the dietitian, Sarah Lopez, with correct phone number
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
                                                "value": "Sarah Lopez",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 12345-6789-1000-9630",
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
                # Milestone 2 – Agent replies to the user with Sarah’s phone number
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "12345-6789-1000-9630",
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
                (0, 1),  # Tool use → verify Sarah Lopez was found
                (1, 2),  # Contact found → respond to user with number
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_533b88c8-e016-4c5f-bd79-c54fff30fd14_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "messaging",
                "email",
                "misinformation_no",
                "insufficient_context_no",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T17:15:00-08:00",
            is_read_time="2024-12-09T17:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to thank your dad for the kind words.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Email Juan Garcia; "Thanks Dad, Hope they work out! Regards, Lucas."',
                },
            ],
            reasoning="Ok so the user wants to email Juan Garcia a given message. First I will establish the recipient which is given by the user. Next is the Method of communication which is given by the user. I will now message the user's given message to Juan Garcia via email at 17:15 on 9 December 2024. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message "Thanks Dad, Hope they work out! Regards, Lucas" is sent to Juan Garcia via email.',
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_messages",
                "get_all_messages",
                "search_emails",
                "get_all_emails",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Retrieve or confirm Juan's email via contacts (search or get_all)
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
                # Milestone 1 – Confirm Juan Garcia contact (with correct email) was available from contact lookup
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
                                                "value": "Juan Garcia",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "juan.garcia@example.com",
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
                # Milestone 2 – Email is sent to Juan Garcia with the intended body
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["juan.garcia@example.com"]
                                    ],
                                    "status": "sent",
                                    "body": "Hope they work out",
                                    "creation_datetime_iso": "2024-12-09T17:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                # Allow minor formatting variations but ensure key phrase is present
                                "body": column_contains_similarity,
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
                (0, 1),  # contact lookup → confirm Juan's contact
                (1, 2),  # confirmed contact → send email
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_6af4cf88-a6e5-4bed-81b8-56f3854f5b72_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "email",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T17:15:00-08:00",
            is_read_time="2024-12-09T17:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You just got home after visiting your Dad's coffee shop to discuss expanding healthy snack options.  He said he'd send you an email afterwards about it, so you're wondering if he did that yet.  Once you check, you also want to forward the e-mail to Sarah Lopez to consider these healthy snack options for your clients' dietary plans and recommendations. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Have I already received an email on healthy snack options today? If so, can you forward it to my nutritionist, please?",
                },
            ],
            reasoning="First of all, the user is interested in knowing if an email on health snack options has been received today. The user request is being made on December 09 2024 at 17:15:00. The user is specifically referring to e-mails, so I will explore the Mail app. There I see an e-mail from Juan Garcia with the following subject line: \"Healthy Snack Options for the Coffee Shop\", received on December 09 2024 at 17:00:00. This must be the e-mail the user is referring to, so I will now show this e-mail to them and confirm. \n\nAfter this, the user wants to forward this e-mail to their 'nutritionist'. I am not sure who the user might be referring to, so I will explore the user contacts. There, I see a contact card for 'Sarah Lopez', who is tagged as 'Dietitian Consultant'. There are no additional contacts with a similar tag or alias, so I can now safely assume this is the contact the user wants to send Juan Garcia's email to. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The email from Juan Garcia, received on December 9th, 2024, at 17:00, is shown to the user. ",
                },
                {
                    "input_text": "2. The email from Juan Garcia on healthy snack options is forwarded to dietitian consultant Sarah Lopez. ",
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
                "get_all_emails",
                "search_emails",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Agent looks for today’s email(s)
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
                # Milestone 1 – Verify the email from Juan Garcia about healthy snacks is among the results
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
                                                "value": "juan.garcia@example.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Healthy Snack Options",
                                                "partial": True,  # allow “Re:” prefix
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-09T17:00:00-08:00",
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
                # Milestone 2 – Agent searches contacts to find the nutritionist
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
                # Milestone 3 – Verify Sarah Lopez (nutritionist) was retrieved
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
                                                "value": "Sarah Lopez",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "sarah.lopez@example.com",
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
                # Milestone 4 – Forward email is actually sent to Sarah Lopez
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["sarah.lopez@example.com"]
                                    ],
                                    "status": "sent",
                                    "subject": "Healthy Snack Options",
                                    "creation_datetime_iso": "2024-12-09T17:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "subject": column_contains_similarity,
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
                (0, 1),  # email search -> confirm correct email
                (2, 3),  # contact search -> confirm Sarah
                (3, 4),  # once Sarah identified, email is forwarded
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_9640e5f1-d7f0-4f20-86da-d02c8cb83d21_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T17:15:00-08:00",
            is_read_time="2024-12-09T17:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You just got home after visiting your Dad's coffee shop to discuss expanding healthy snack options.  He said he'd send you an email afterwards about it, so you're wondering if he did that yet. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did Dad email me back yet about the healthy snack options? Yes or no.",
                },
            ],
            reasoning="The user wants to know if Dad emailed yet. I should check their contacts to figure out who Dad is. I see that Juan Garcia is listed as Dad in the user's contacts. They must mean him. Okay, I'll look for new emails from Juan Garcia. I see one new email from Juan Garcia, received on December 9th, 2024, at 17:00. I'll show that to the user now and reply with 'Yes'.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The user has been infomed with 'Yes', as the email from Juan Garcia, received on December 9th, 2024, at 17:00, is found. ",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – The agent looks through the mailbox to find any email from Dad
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
                # Milestone 1 – Confirm the search result actually included the email from Juan (“Dad”)
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
                                                "value": "juan.garcia@example.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Healthy Snack Options",
                                                "partial": True,  # allow “Re: …”
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-09T17:00:00-08:00",
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
                            reference_milestone_node_index=0,  # inspect the tool output from Milestone 0
                        )
                    ]
                ),
                # Milestone 2 – The agent tells the user and displays / mentions the email
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
                                            "Healthy Snack Options",
                                            "Yes",
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_d34487e9-3b48-41b9-8dbb-e5065cc42b48_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T18:00:00-08:00",
            is_read_time="2024-12-09T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to reply to your father's email "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to my dad's email I received with something like sounds fantastic, let me know what you think, speak soon.",
                },
            ],
            reasoning="The user wants to reply to their dad's email with something like sounds fantastic, let me know what you think, speak soon. The user's father is Lucas Garcia. I'll look at their inbox. The last email they received was from their father Lucas Garcia. I'll write \"Hey Dad, Sounds fantastic. Let me know what you think. Speak Soon. Best, Lucas\" and send the email. I'll inform the suer when this is done.",
            success_conditions=[
                {
                    "input_text": '1. A reply is sent to Juan Garcia\'s email saying "Hey Dad, Sounds fantastic. Let me know what you think. Speak Soon. Best, Lucas"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "send_email",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent retrieves emails (or searches) to find dad's message to reply to
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
                # Milestone 1 – A reply email is sent to Juan with the requested content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["juan.garcia@example.com"]
                                    ],
                                    "status": "sent",
                                    "body": "Sounds fantastic",
                                    "creation_datetime_iso": "2024-12-09T18:00:00-08:00",
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
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # email retrieval precedes sending the reply
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_d34487e9-3b48-41b9-8dbb-e5065cc42b48_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T18:00:00-08:00",
            is_read_time="2024-12-09T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to reply to your father's email "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to the last email I received with something like sounds fantastic, let me know what you think, speak soon.",
                },
            ],
            reasoning="The user wants to reply to the last email they received with something like sounds fantastic, let me know what you think, speak soon. I'll look at their inbox. The last email they received was from their father Lucas Garcia. I'll write \"Hey Dad, Sounds fantastic. Let me know what you think. Speak Soon. Best, Lucas\" and send the email. I'll inform the suer when this is done.",
            success_conditions=[
                {
                    "input_text": '1. A reply is sent to Juan Garcia\'s email saying "Hey Dad, Sounds fantastic. Let me know what you think. Speak Soon. Best, Lucas"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "send_email",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent retrieves/reviews emails to find the latest one from Dad to reply to
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
                # Milestone 1 – A reply email is sent to Juan with the requested content, using reply semantics
                Milestone(
                    snapshot_constraints=[
                        # Optionally verify that the send_email tool was used in reply mode (not mandatory for content, but ensures it's a reply)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "tool_trace": json.dumps(
                                        {
                                            "tool_name": "send_email",
                                            "arguments": {
                                                "recipients_addresses": [
                                                    "juan.garcia@example.com"
                                                ],
                                                "email_action": "send",
                                                "email_id_referred_action": "reply",
                                                "email_id_referred": "place_holder",
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
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
                # Milestone 2 – A reply email is sent to Juan with the requested content, using reply semantics
                Milestone(
                    snapshot_constraints=[
                        # Verify an email was sent with correct recipient and body content
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Must go to Dad (Juan Garcia)
                                    "recipients_addresses": [
                                        ["juan.garcia@example.com"]
                                    ],
                                    "status": "sent",
                                    # Body should contain key phrases requested by user
                                    "body": "Sounds fantastic",
                                    "creation_datetime_iso": "2024-12-09T18:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                # Allow small variations but require presence of critical phrases
                                "body": column_rouge_l_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        ),
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_9640e5f1-d7f0-4f20-86da-d02c8cb83d21_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T17:15:00-08:00",
            is_read_time="2024-12-09T17:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You just got home after visiting your Dad's coffee shop to discuss expanding healthy snack options.  He said he'd send you an email afterwards about it, so you're wondering if he did that yet. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did Juan email yet?",
                },
            ],
            reasoning="The user wants to know if Juan emailed yet. I should check their contacts to figure out who that is. I see one person with that name, Juan Garcia listed in the user's contacts. They must mean him. Okay, I'll look for new emails from Juan Garcia. I see one new email from Juan Garcia, received on December 9th, 2024, at 17:00. I'll show that to the user now.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The email from Juan Garcia, received on December 9th, 2024, at 17:00, is shown to the user. ",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent attempts to locate Juan’s email
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
                # Milestone 1 – Tool output actually contained Juan’s 17:00 email
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
                                                "value": "juan.garcia@example.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-09T17:00:00-08:00",
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
                # Milestone 2 – Agent tells the user that Juan (Dad) did send an email
                Milestone(
                    snapshot_constraints=[
                        # Confirm mention of an email
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "email",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Confirm reference to Juan or Dad
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("Juan", "Dad")],
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
                (0, 1),  # tool invocation → verify correct email in results
                (1, 2),  # verified email → communicate answer to user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_4de180be-befc-4f44-bc12-d2577e194be7_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T18:30:00-08:00",
            is_read_time="2024-12-09T18:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        'You want to dictate a reply email to Juan Garcia saying "Hey I think I have a few new ideas for the healthy eating initiative can I call you?". '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a reply email to Juan Garcia saying "Hey I think I have a few new ideas for the healthy eating initiative can I call you?".',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Juan Garcia.\n\nI should locate the email history with this contact by searching their name in the user's Inbox and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the email if the user confirms that the email was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": '1. A reply email is sent to Juan Garcia saying "Hey I think I have a few new ideas for the healthy eating initiative can I call you?".',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – The agent used at least one information-retrieval email/contact tool
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
                                        "search_emails",
                                        "get_all_emails",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – The reply email to Juan Garcia was sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["juan.garcia@example.com"]
                                    ],
                                    "status": "sent",
                                    "body": "few new ideas for the healthy eating initiative can I call you",
                                    "creation_datetime_iso": "2024-12-09T18:30:00-08:00",
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
                (0, 1),  # information retrieval precedes sending the email
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_9e96002b-d87a-43a3-9a16-d6062f48e481_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T16:55:00-08:00",
            is_read_time="2024-12-09T16:55:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are wondering what time you sent in your last email to Juan Garcia "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I send that last email to my Dad",
                },
            ],
            reasoning="The user wants to know when they sent their last email to my Dad. First thing I need to do is search the user's emails. Ok didn't find any emails to someone with that name. The next thing I should do is search the user's contacts for that name. Ok so I found Juan Garcia whose alias is listed as \"Dad\" so this must be the person the user is referring to. Now I can search through their emails for emails sane to Juan Garcia I found an email sent to juan.garcia@example.com. That must be the email the user is referring to. Ok now that I have that I will retrieve the time of the email and inform the user",
            success_conditions=[
                {
                    "input_text": "1. The time of the email sent by the user on December 09, 2024 at 16:00 to juan.garcia@example.comis presented to the user",
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
                # Milestone 1 – The returned results include the correct email sent to Dad at 16:00
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
                                                "value": ["juan.garcia@example.com"],
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-09T16:00:00-08:00",
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
                # Milestone 2 – Agent tells the user the correct time (4 pm / 16:00)
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
                                            "16:00",
                                            "4:00",
                                            "4 pm",
                                            "4pm",
                                            "4 p.m.",
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
                (0, 1),  # Email search → verify correct email present
                (1, 2),  # Email verified → respond to user with time
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_ca785aa3-2069-44d1-8961-5d6ba3ddbde2_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T22:35:00-08:00",
            is_read_time="2024-12-09T22:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know the name of the document you emailed your dad. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What's the name of the document I emailed to Juan?",
                },
            ],
            reasoning="Right so, the user is looking for the name of a document which they emailed to a contact named 'Juan'. Searching the user's contacts I can see one match for 'Juan', 'Juan Garcia'. \n\nNext, I can check the user's Mail as the name of the document is in an email the user sent to 'Juan'. I can see an email exchange from today, 9 December 2024 between the two of them. There is an email matching with the subject 'Healthy Snack Options for the Coffee Shop' sent at 16:00 to 'Juan Garcia' with the document attached named 'Healthy_Snack_Recipes_Dec2024.pdf'. Now that I have found the requested information, I can read it out to the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The name of the document 'Healthy_Snack_Recipes_Dec2024', sent in the email with the subject 'Healthy Snack Options for the Coffee Shop' on 9 December 2024 at 16:00 to 'Juan Garcia' is read out to the user.",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – The agent looks through email records
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
                # Milestone 1 – Verify the retrieved email includes the expected attachment
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
                                                "value": "Healthy Snack Options for the Coffee Shop",
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
                # Milestone 2 – The agent tells the user the document name
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Healthy_Snack_Recipes_Dec2024",
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
            name="LUCAS_GARCIA_16_699ad6ee-6cbc-46e5-8cc7-2678cdce4a98_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T17:10:00-08:00",
            is_read_time="2024-12-09T17:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to get a second opinion on the snack options your father sent to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you forward the latest email I got from dad to mom",
                },
            ],
            reasoning="The user wants to send the last email they received from their dad to their mom. Once I've located the email by looking through the latest emails to the user, I can locate the recipients who are listed in the users address book as mother and father. Putting these together I can check with the user before forwarding the email.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. The latest email from Juan Garcia should be forwarded to Maria Garcia.",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "send_email",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – the agent looks up the latest email (expects email-retrieval tools)
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
                # Milestone 1 – confirm that an email from Dad (Juan Garcia) was returned by the retrieval in Milestone 0
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
                                                "value": "juan.garcia@example.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Healthy Snack Options",
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
                # Milestone 2 – verify a forwarded email was SENT to Mom (Maria Garcia)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["maria.garcia@example.com"]
                                    ],
                                    "status": "sent",
                                    "subject": "Healthy Snack Options",
                                    "creation_datetime_iso": "2024-12-09T17:10:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "subject": column_contains_similarity,
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
            name="LUCAS_GARCIA_16_699ad6ee-6cbc-46e5-8cc7-2678cdce4a98_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T17:10:00-08:00",
            is_read_time="2024-12-09T17:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to get a second opinion on the snack options your father sent to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Forward that last email from dad to mom",
                },
            ],
            reasoning="The user wants to send an email they received from their dad, or father, to their mom or mother. First I'll need to locate the email, which should be the most recent from the users father, then I'll need to locate the recipients who are in the users address book as mother and father. Putting these together I can forward the email to the recipients, and if the user is happy, send it.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. The latest email from Juan Garcia should be forwarded to Maria Garcia.",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "send_email",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – the agent looks for the most-recent email from Dad
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
                # Milestone 1 – confirm that an email from Dad, about the snacks, was actually found
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
                                                "value": "juan.garcia@example.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Healthy Snack Options",
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
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
                # Milestone 2 – the agent looks up Mom’s contact information
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
                # Milestone 3 – confirm Mom’s contact was found (e-mail address)
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
                                                "value": "Maria Garcia",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "maria.garcia@example.com",
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
                            reference_milestone_node_index=2,
                        )
                    ]
                ),
                # Milestone 4 – a new e-mail is sent/forwarded to Mom
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["maria.garcia@example.com"]
                                    ],
                                    "subject": "Healthy Snack Options",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-09T17:10:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "subject": column_contains_similarity,  # subject should at least carry the original topic
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial DB state
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # email search → confirm email found
                (2, 3),  # contact search → confirm contact found
                (1, 4),  # after finding Dad's email, it can be forwarded
                (3, 4),  # needs Mom's address before forwarding
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_ca785aa3-2069-44d1-8961-5d6ba3ddbde2_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T22:35:00-08:00",
            is_read_time="2024-12-09T22:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know the name of the document you emailed your dad. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell me the name of the document I emailed to my dad.",
                },
            ],
            reasoning="Okay so, the user is requesting the name of a document they emailed to their 'dad'. Searching their contacts I see no contact named 'dad' but I can see a contact with an alias as 'dad', which is 'Juan Garcia'. Now that I have identified the contact that the email was sent to, I can check the user's Mail.\n\nIn the user's Mail, I see an email exchange from today, 9 December 2024 between the two of them. There is an email matching with the subject 'Healthy Snack Options for the Coffee Shop' sent at 16:00 to 'Juan Garcia' with the document attached named 'Healthy_Snack_Recipes_Dec2024.pdf'. Now that I have found the requested information, I can read it out to the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The name of the document 'Healthy_Snack_Recipes_Dec2024.pdf', sent in the email with the subject 'Healthy Snack Options for the Coffee Shop' on 9 December 2024 at 16:00 to 'Juan Garcia' is read out to the user.",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the contact that matches “dad”
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
                # Milestone 1 – Verify Juan Garcia (Dad) was found from the contact search in Milestone 0
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
                                                "value": "Juan Garcia",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "juan.garcia@example.com",
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
                # Milestone 2 – The agent searches emails to locate the one sent to Dad
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
                # Milestone 3 – Confirm the correct outgoing email with the expected attachment was retrieved
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
                                                "value": "Healthy Snack Options for the Coffee Shop",
                                                "partial": False,
                                            },
                                            "attachments": {
                                                "value": "Healthy_Snack_Recipes_Dec2024.pdf",
                                                "partial": True,
                                            },
                                            "recipients_addresses": {
                                                "value": "juan.garcia@example.com",
                                                "partial": True,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=2,
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
                # Milestone 4 – The agent tells the user the document name
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Healthy_Snack_Recipes_Dec2024",
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
                (0, 1),  # Contact search → verify correct contact
                (2, 3),  # Email search → verify correct email
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_9e96002b-d87a-43a3-9a16-d6062f48e481_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T16:55:00-08:00",
            is_read_time="2024-12-09T16:55:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are wondering what time you sent in your last email to Juan Garcia "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I send that last email to Juan Garcia",
                },
            ],
            reasoning="The user wants to know when they sent their last email to Juan Garcia. First thing I need to do is search the user's emails. Ok I found an email sent to juan.garcia@example.com. That must be the email the user is referring to. Ok now that I have that I will retrieve the time of the email and inform the user",
            success_conditions=[
                {
                    "input_text": "1. The time of the email sent by the user on December 09, 2024 at 16:00 to juan.garcia@example.comis presented to the user",
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
                    ]
                ),
                # Milestone 1 – Retrieved results include the expected email to Juan Garcia at the correct time
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
                                                "value": ["juan.garcia@example.com"],
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-09T16:00:00-08:00",
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
                # Milestone 2 – Agent tells the user the send time (any reasonable phrasing)
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
                                        ("4:00", "4 pm", "4pm", "4 p.m.", "16:00")
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
                (0, 1),  # Tool call → verify correct email found
                (1, 2),  # Email found → user informed
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_4de180be-befc-4f44-bc12-d2577e194be7_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T18:30:00-08:00",
            is_read_time="2024-12-09T18:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        'You want to dictate a reply email to Juan Garcia saying "Hey I think I have a few new ideas for the healthy eating initiative can I call you?". '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to reply to the email saying I have a few new ideas for the healthy eating initiative — can I call you?",
                },
            ],
            reasoning="The user wants to reply to 'the email' with a message about new ideas for the healthy eating initiative.\n\nI search the user's Inbox to find the email this refers to. The most recent relevant email is from Juan Garcia, 'Re: Healthy Snack Options for the Coffee Shop', which is about healthy snack/eating options, so this is the email to reply to.\n\nThe user has given what they want to say — that they have a few new ideas for the healthy eating initiative and would like to call — so I transcribe that into a reply to Juan Garcia and send it.",
            success_conditions=[
                {
                    "input_text": '1. A reply email is sent to Juan Garcia saying "Hey I think I have a few new ideas for the healthy eating initiative can I call you?".',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – the agent looks up either the contact or the existing email thread
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
                                        "search_emails",
                                        "get_all_emails",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – a new sent email to Juan Garcia containing the requested text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["juan.garcia@example.com"]
                                    ],
                                    "status": "sent",
                                    "body": "healthy eating initiative",
                                    "creation_datetime_iso": "2024-12-09T18:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_subset_match_similarity,  # ensure Juan is included, allow extras
                                "status": column_exact_match_similarity,
                                "body": column_contains_similarity,  # look for the key phrase fragment,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox chatter when checking EMAIL DB change
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_6f969347-8a86-48d6-8888-399bc8c9265e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T17:15:00-08:00",
            is_read_time="2024-12-09T17:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to thank your dad for the kind words. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to the email about introducing new healthy recipies with "Thanks Dad, Hope they work out! Regards, Lucas."',
                },
            ],
            reasoning="Ok so the user wants to an email with a given message, looks like it's target the user's father. The most recent email is from Juan Garcia, and based on user's contact book it is user's father. I will now reply with the user's given message to Juan Garcia via email at 17:15 on 9 December 2024. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message "Thanks Dad, Hope they work out! Regards, Lucas" is sent to Juan Garcia via email.',
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Agent looks up recent emails (dad’s message)
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
                # Milestone 1 – The retrieved email is the one sent by Juan Garcia
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
                                                "value": "juan.garcia@example.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Healthy Snack Options for the Coffee Shop",
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
                # Milestone 2 – A reply email is sent to Dad with the correct message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["juan.garcia@example.com"]
                                    ],
                                    "body": "Thanks Dad",
                                    "creation_datetime_iso": "2024-12-09T17:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "body": column_contains_similarity,  # body must contain “Thanks Dad …”,
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_5ff86433-3ea5-4ba8-a73e-24cc3e66caa4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "email",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T17:10:00-08:00",
            is_read_time="2024-12-09T17:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to have the email from Juan Garcia read to you "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read dad's email",
                },
            ],
            reasoning="The user wants their email to be read aloud. The email in question is from the user's father, who is listed in the user's contacts as Juan Garcia",
            success_conditions=[
                {
                    "input_text": '1. The email with the subject line "Re: Healthy Snack Options for the Coffee Shop" from Juan Garcia will be read aloud to the user at 17:10 on 9 December 2024. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – the agent looks up emails
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
                # Milestone 1 – the email from Juan Garcia with the correct subject was retrieved
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
                                                "value": "Re: Healthy Snack Options for the Coffee Shop",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "juan.garcia@example.com",
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
                # Milestone 2 – the agent read the email content back to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "The recipes look fantastic",
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
            name="LUCAS_GARCIA_16_533b88c8-e016-4c5f-bd79-c54fff30fd14_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "messaging",
                "email",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T17:15:00-08:00",
            is_read_time="2024-12-09T17:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to thank your dad for the kind words.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply him back and say "Thanks Dad, Hope they work out! Regards, Lucas."',
                },
            ],
            reasoning="User wants to reply to a contact. By the content \"Thanks Dad ... \" I understand user is sending a message to their father. I'll check if there's message thread between user and their father. I didn't find any messages between them. I'll check if there are emails thread, as it's possible that user refers to email as \"message\". Ok, I found very recent emails exchanges between user and their father. I believe user wants to send an email to their father. I'll draft the email as user requested and send it. I'll inform user that the email has been sent.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message "Thanks Dad, Hope they work out! Regards, Lucas" is sent to Juan Garcia via email.',
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_messages",
                "get_all_messages",
                "search_emails",
                "get_all_emails",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Agent looks up relevant email thread (Dad's email) before replying
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
                # Milestone 1 – Confirms Juan/Dad's email to Lucas was actually retrieved from Milestone 0
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
                                                "value": "juan.garcia@example.com",
                                                "partial": False,
                                            },
                                            "recipients_addresses": {
                                                "value": ["lucas.garcia@example.com"],
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Re: Healthy Snack Options for the Coffee Shop",
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
                # Milestone 2 – Email reply sent to Juan Garcia with required body content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Recipients must be exactly Juan
                                    "recipients_addresses": [
                                        ["juan.garcia@example.com"]
                                    ],
                                    "status": "sent",
                                    # Body should contain the requested message (relaxed match)
                                    "body": "Thanks Dad, Hope they work out! Regards, Lucas",
                                    "creation_datetime_iso": "2024-12-09T17:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "body": column_rouge_l_similarity,
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
                (0, 1),  # Email search → confirm correct email from Dad retrieved
                (1, 2),  # Retrieval of Dad's email → send correct reply email
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_349dbf32-dc59-43df-8a84-65a00c98bff1_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_16",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T18:00:00-08:00",
            is_read_time="2024-12-09T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to reply to your father's email "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to the last email I received with something like sounds fantastic, let me know what you think, speak soon.",
                },
            ],
            reasoning="The user wants to reply to the last email they received with something like sounds fantastic, let me know what you think, speak soon. I'll look at their inbox. The last email they received was from their father Lucas Garcia. I'll write \"Hey Dad, Sounds fantastic. Let me know what you think. Speak Soon. Best, Lucas\" and send the email. I'll inform the suer when this is done.",
            success_conditions=[
                {
                    "input_text": '1. A reply is sent to Juan Garcia\'s email saying "Hey Dad, Sounds fantastic. Let me know what you think. Speak Soon. Best, Lucas"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 — Agent looks through emails to locate the most recent message
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
                # Milestone 1 — Verify that the email from Juan Garcia was indeed returned
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
                                                "value": "juan.garcia@example.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Healthy Snack Options",
                                                "partial": True,  # allow the "Re:" prefix
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
                # Milestone 2 — A reply email has been sent to Dad
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["juan.garcia@example.com"]
                                    ],
                                    "status": "sent",
                                    "body": "sounds fantastic",  # minimal key phrase,
                                    "creation_datetime_iso": "2024-12-09T18:00:00-08:00",
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
            name="LUCAS_GARCIA_16_c59bcfa0-20a5-4a89-8b88-b9455e1666ca_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_16",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T11:25:00-08:00",
            is_read_time="2024-12-11T11:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to see if your father has had a chance to look at the recipes yet "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Message Juan and say "Hey just checking have you looked at the recipes yet?".',
                },
            ],
            reasoning='The user wants to message Juan and say "Hey just checking have you looked at the recipes yet?". I should first find out who Juan is. I will check the user\'s Contacts. \nHmm, looks like the user only has 1 Juan in their Contacts, Juan Garcia, so this must be who the user means. \nNext I will draft a message to Juan, using the content the user has already provided. \nLastly, I will present the draft to the user for approval before I send it. ',
            success_conditions=[
                {
                    "input_text": '1. A message saying "Hey just checking have you looked at the recipes yet?" is sent to Juan Garcia. ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up Juan in the contacts list
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
                # Milestone 1 – A new message to Juan Garcia has been sent with the expected content
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
                                                "juan.garcia@example.com",
                                                "+1 12345-6789-1000-4321",
                                            )
                                        ]
                                    ],
                                    "content": "Hey just checking have you looked at the recipes yet?",
                                    "creation_datetime_iso": "2024-12-11T11:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Require that at least one identifier for Juan is present;
                                # allow extra participants such as the user’s own address.
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with pre-task database state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup precedes sending the message
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_becc734d-73c0-4522-afab-ed1d4d48a77a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "email",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T17:05:00-08:00",
            is_read_time="2024-12-09T16:59:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know what Juan said in his last email but you cannot look at your phone right now. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What did Dad's last email say? \n",
                },
            ],
            reasoning='The user wants me to read out the contents of a message. They have provided me with context that the message is an email and it is the last received email from a contact the user refers to as "Dad" This should be enough information to find the email. I have searched the user\'s emails, and I have found an unread email from Juan Garcia, who falls under the "father" relationship in the user\'s contacts. I can assume this is the referenced message, so I will read it out to the user. ',
            success_conditions=[
                {
                    "input_text": "1. The last email received from juan.garcia@example.com is read out loud to the user. \n",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – the agent uses a mail-retrieval tool
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
                # Milestone 1 – verify that the retrieved email is from Dad (Juan Garcia)
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
                                                "value": "juan.garcia@example.com",
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
                # Milestone 2 – the assistant tells the user what the email said (key phrase check)
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
                                            "recipes look fantastic",
                                            "thanks for dropping by",
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
                (0, 1),  # tool call -> verify email retrieved
                (1, 2),  # verified email -> user is told its contents
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_becc734d-73c0-4522-afab-ed1d4d48a77a_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "email",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T17:05:00-08:00",
            is_read_time="2024-12-09T16:59:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know what Juan said in his last email but you cannot look at your phone right now. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read out the email I got from Juan Garcia on December 09 2024 at 17:00.",
                },
            ],
            reasoning="The user is asking me to read out an email.\nFirst, I need to find the email in question in the user's inbox. The user has given me a sender, date, and time. I have found the email in question, received from Juan Garcia on December 09 2024 at 17:00. I will read this out for the user.",
            success_conditions=[
                {
                    "input_text": "1. The last email received from juan.garcia@example.com is read out loud to the user. \n",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
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
                # Milestone 1 – Confirm the retrieved email is the one from Juan on 2024-12-09 17:00
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
                                                "value": "juan.garcia@example.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-09T17:00:00-08:00",
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
                # Milestone 2 – Agent communicates the email body (reads it out loud) to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "The recipes look fantastic",
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
                (0, 1),  # Retrieval tool call → validate correct email found
                (1, 2),  # Correct email found → ensure user is told the contents
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_c59bcfa0-20a5-4a89-8b88-b9455e1666ca_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T11:25:00-08:00",
            is_read_time="2024-12-11T11:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to see if your father has had a chance to look at the recipes yet "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Message Dad and say "Hey just checking have you looked at the recipes yet?".',
                },
            ],
            reasoning="The user wants to message Dad and say \"Hey just checking have you looked at the recipes yet?\" I should first find out who Dad is. I will check the user's Contacts. \nHmm, I don't see a Dad in the user's Contacts, I should check the contact's aliases. Looks like Juan Garcia has the alias Dad so this must be who the user meant. \nNext I will draft a message to Juan, using the content the user has already provided. \nLastly, I will present the draft to the user for approval before I send it. ",
            success_conditions=[
                {
                    "input_text": '1. A message saying "Hey just checking have you looked at the recipes yet?" is sent to Juan Garcia. ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up “Dad” / Juan Garcia in contacts
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
                # Milestone 1 – Confirm the contact record for Juan Garcia / Dad was surfaced
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
                                                "value": "Juan Garcia",
                                                "partial": False,
                                            },
                                            "alias": {"value": "Dad", "partial": False},
                                            "phone_number": {
                                                "value": "+1 12345-6789-1000-4321",
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
                # Milestone 2 – A message with the specified content was sent to Dad (Juan Garcia)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least one of Dad’s identifiers (phone or email) must be in the participant list
                                    "participants_addresses": [
                                        [
                                            (
                                                "+1 12345-6789-1000-4321",
                                                "juan.garcia@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "Hey just checking have you looked at the recipes yet?",
                                    "creation_datetime_iso": "2024-12-11T11:25:00-08:00",
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
                    # We only care about the message addition; ignore changes (if any) to other DBs
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
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_349dbf32-dc59-43df-8a84-65a00c98bff1_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T18:00:00-08:00",
            is_read_time="2024-12-09T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to reply to your father's email "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to my dad's email I received with something like sounds fantastic, let me know what you think, speak soon.",
                },
            ],
            reasoning="The user wants to reply to their dad's email with something like sounds fantastic, let me know what you think, speak soon. The user's father is Lucas Garcia. I'll look at their inbox. The last email they received was from their father Lucas Garcia. I'll write \"Hey Dad, Sounds fantastic. Let me know what you think. Speak Soon. Best, Lucas\" and send the email. I'll inform the suer when this is done.",
            success_conditions=[
                {
                    "input_text": '1. A reply is sent to Juan Garcia\'s email saying something like "Hey Dad, Sounds fantastic. Let me know what you think. Speak Soon. Best, Lucas"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – verify a reply email was sent to Juan Garcia
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,  # a new email should have been created
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["juan.garcia@example.com"]
                                    ],
                                    "status": "sent",
                                    "body": "sounds fantastic",  # will match as substring,
                                    "creation_datetime_iso": "2024-12-09T18:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "body": column_contains_similarity,  # look for the key phrase,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial DB snapshot
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_1cf0bc4a-2c51-4535-8267-33f641c92b7f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T17:35:00-08:00",
            is_read_time="2024-12-09T17:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to send an email to your father saying 'no problem Dad. ' "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Email my Dad back to say 'no problem Dad.'",
                },
            ],
            reasoning="The user wants to email their Dad. Looking in contacts, I can see that Juan Garcia is listed as Dad and his email address Juan.garcia@example.com is there as well. I'll send the message to this email address.",
            success_conditions=[
                {
                    "input_text": "1. Send an email to Juan Garcia saying 'no problem Dad.'",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_email"],
            milestones=[
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["juan.garcia@example.com"]
                                    ],
                                    "status": "sent",
                                    "body": "no problem Dad",
                                    "creation_datetime_iso": "2024-12-09T17:35:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare with the initial state
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_16_5ff86433-3ea5-4ba8-a73e-24cc3e66caa4_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T17:10:00-08:00",
            is_read_time="2024-12-09T17:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to have the email from Juan Garcia read to you "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I wanna hear the last email I got ",
                },
            ],
            reasoning="The user wants their email to be read aloud. The last email received was from Juan Garcia, the user's father",
            success_conditions=[
                {
                    "input_text": '1. The email with the subject line "Re: Healthy Snack Options for the Coffee Shop" from Juan Garcia will be read aloud to the user at 17:10 on 9 December 2024. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – Agent uses an email–retrieval tool to locate the last email
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
                # Milestone 1 – Confirm the correct email (subject + sender) appeared in the retrieved results
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
                                                "value": "Re: Healthy Snack Options for the Coffee Shop",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "juan.garcia@example.com",
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
                # Milestone 2 – Agent relays (reads) that email back to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Healthy Snack Options",
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
            name="LUCAS_GARCIA_16_6f969347-8a86-48d6-8888-399bc8c9265e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T17:15:00-08:00",
            is_read_time="2024-12-09T17:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to thank your dad for the kind words. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to Dad\'s email; "Thanks Dad, Hope they work out! Regards, Lucas."',
                },
            ],
            reasoning="Ok so the user wants to reply to dad's email with a given message. First I will establish who dad is. The contact Juan Garcia is labelled as dad in the user's contacts. Next is the method of communication which is given by the user. I will now message the user's given message to Juan Garcia via email at 17:15 on 9 December 2024. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message "Thanks Dad, Hope they work out! Regards, Lucas" is sent to Juan Garcia via email.',
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – The agent looks up existing emails (e.g., Dad’s original message)
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
                # Milestone 1 – A reply email is sent to Juan (“Dad”) that contains the thank-you message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["juan.garcia@example.com"]
                                    ],
                                    "status": "sent",
                                    "body": "Thanks Dad",
                                    "creation_datetime_iso": "2024-12-09T17:15:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare against initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox traces when checking email DB change
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
    ]
