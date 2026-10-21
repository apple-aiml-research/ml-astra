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


def get_TAG_EMILY_ROSE_pilot_plot_14(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="EMILY_ROSE_14_4e32bf80-664c-49cb-b410-9eb7a1be96a8_single_turn_3",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_14",
                "messaging",
                "contact",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T13:15:00-08:00",
            is_read_time="2024-12-10T13:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Your fruitful conversation with Sarah reminds you that you had a fruitful conversation with your friend Oliver last week, and you want to be reminded of the last messages you two exchanged. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you remind me how Oliver Green thought our meeting went last week based on our text messages? What did he say last?",
                },
            ],
            reasoning='I need to retrieve some information for the user. They want to know what Oliver Green had to say over text about how their meeting went last week. Let me figure out which meeting the user is talking about. Since it\'s December 10th, I\'ll look at meetings from the past seven days. I see the user had a meeting, "Meeting with Oliver Green for Community Gathering Refreshments", where Oliver Green was invited on December 5th at 16:00-17:00. This must be the meeting the user is talking about.\n\nNow, they want to know what Oliver Green had to say over text about this meeting. I can only know what Oliver had to say by looking at texts that came in after the start time of the meeting. I see the user sent one text to Oliver at 16:30 on 5 December. Even though the meeting was scheduled 16:00-17:00, it must have ended early because the text says "Just left your cafe. Thanks for confirming everything, Oliver. I’ll send over the calendar invite shortly." So then the next text from Oliver at 16:35 on 5 December says "Perfect! Thanks again, Emily. Excited for the gathering!". Now, Oliver gives no indication in that text of how he thought the meeting went, and even if I tried to summarize his text, it wouldn\'t explain his impression of the meeting. All I can do is tell the user what his text says, because that\'s all the information and context I have, even if that doesn\'t exactly answer their question.',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the last text they received from Oliver Green on 5 December 2024 at 16:35 says "Perfect! Thanks again, Emily. Excited for the gathering!"',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_messages",
                "get_all_messages",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – Agent uses a messages retrieval tool (search or get_all) to look up conversation with Oliver
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – Confirm that the specific last message from Oliver was retrieved from tool output
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
                                            # Must match Oliver as sender
                                            "sender_address": {
                                                "value": "+1 530-555-0128",
                                                "partial": False,
                                            },
                                            # And match the exact last-content text
                                            "content": {
                                                "value": "Perfect! Thanks again, Emily. Excited for the gathering!",
                                                "partial": False,
                                            },
                                            # And the meeting date/time to ensure it's the right message
                                            "creation_datetime_iso": {
                                                "value": "2024-12-05T16:35:00-08:00",
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
                            reference_milestone_node_index=0,  # validate based on messages retrieval in milestone 0
                        )
                    ],
                ),
                # Milestone 2 – User-facing response includes what Oliver said last, with key details
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Ensure the answer mentions Oliver's last message content
                                    "content": "Excited for the gathering",
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
                (0, 1),  # messages retrieval → confirm correct last message from Oliver
                (1, 2),  # correct retrieval → inform user with that content
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_14_146bcdf2-52c9-49a2-953e-eb17c8f1b4ea_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T12:15:00-08:00",
            is_read_time="2024-12-10T12:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to thank Sarah for the work you put in together this morning. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to Sarah with this; "Hey Sarah, thanks for passing this on. great work today!"',
                },
            ],
            reasoning="Ok so the user wants to reply to Sarah with a given message. First we'll establish who Sarah is. There is only one Sarah in the user's contacts which is Sarah Green so this must be who they are referring to. Next is the method which we can get from the way the user phrased their request. They want to reply which means we are looking for a previous message from Sarah. I have found the message from Sarah on email which means we are looking to reply via email. I will now send the user's given message at 12:15 on 10 December 2024. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message "Hey Sarah, thanks for passing this on. great work today!" is sent to Sarah Green via email at 12:15 on 10 December 2024. ',
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – Agent looks up Sarah’s e-mail thread (information-retrieval)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – Confirms the correct e-mail from Sarah Green was found
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
                                                "value": "Great Ideas from Our Coffee Meeting",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "sarah.green@orchardmail.com",
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
                # Milestone 2 – A reply e-mail is sent to Sarah with the correct content and timestamp
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["sarah.green@orchardmail.com"]
                                    ],
                                    "body": "Hey Sarah, thanks for passing this on. great work today!",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-10T12:15:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox chatter
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # email search → verify correct thread
                (1, 2),  # verified thread → send reply
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_14_2ec6915f-d87a-4951-8561-69c1ba354cc5_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T12:15:00-08:00",
            is_read_time="2024-12-10T12:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to thank your friend for sending you their resources. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Get back to Sarah's email and say Hi Sarah, thank you for the links!",
                },
            ],
            reasoning="The user intends to respond to Sarah Green's latest email with the text “Hi Sarah, thank you for the links!\". First, I'll locate the email exchange by searching through recently received emails from Sarah. Once I’ve found it, I’ll compose the reply and check if the user is satisfied with it before sending it.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A reply is sent to Sarah Green's latest email saying \"Hi Sarah, thank you for the links!”",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
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
                                    target_tools=["search_emails", "get_all_emails"],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Email from Sarah Green is found
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
                                                "value": "Great Ideas from Our Coffee Meeting",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "sarah.green@orchardmail.com",
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
                # Milestone 2 – Reply email is sent with the thank-you message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "status": "sent",
                                    "body": "thank you",
                                    "creation_datetime_iso": "2024-12-10T12:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "status": column_exact_match_similarity,
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
            name="EMILY_ROSE_14_85389aa0-4045-4edd-a859-1f114f5cccf7_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T13:00:00-08:00",
            is_read_time="2024-12-10T13:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to see the last email from Sarah Green. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show the last email from Sarah Green.",
                },
            ],
            reasoning="The user wants to see the last email from Sarah Green. Let me look for it in Mail. Found it. I will show it to the user.",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last email from Sarah Green sent on December 10th at 12:00 with the text 'Hi Emily, It was wonderful catching up over coffee this morning! I've attached a few links and resources that could help us with the new environmental outreach programs we discussed. Looking forward to seeing how these ideas take shape and benefit our community. Best regards, Sarah'.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – The agent uses an email-retrieval tool
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – The agent shows the email content to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "It was wonderful catching up over coffee this morning!",
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
            name="EMILY_ROSE_14_04593c2b-f8ca-40f9-b53b-ac44bca8929e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T12:05:00-08:00",
            is_read_time="2024-12-10T12:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to check if you have received the the attachments sent by Sarah Green in her recent email "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Have I received attachments regarding the new environmental program?",
                },
            ],
            reasoning='The user wants to see whether they have received the file that was attached to an email they just received. I can take that to mean their most recent email. So first thing I need to do is search their inbox for their most recent email. Ok I have found an email received 5 minutes ago from Sarah Green so that must be it. I will let the user know the attached document named "Environmental_Resources_Links.pdf" exists',
            success_conditions=[
                {
                    "input_text": '1. The existence of the document "Environmental_Resources_Links.pdf" attached to the email from Sarah Green received at 12:00 on December 10 2024 is informed to the user',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – Agent looks for the recent email (tool invocation)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – Confirm the correct email (with attachment) was found
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
                                                "value": "sarah.green@orchardmail.com",
                                                "partial": False,
                                            },
                                            "attachments": {
                                                "value": [
                                                    "Environmental_Resources_Links.pdf"
                                                ],
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
                        ),
                    ],
                ),
                # Milestone 2 – Agent presents the attachment to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Environmental_Resources_Links",
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
                (0, 1),  # Must find the email before confirming its content
                (1, 2),  # Must confirm the email before presenting attachment
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_14_04593c2b-f8ca-40f9-b53b-ac44bca8929e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T12:05:00-08:00",
            is_read_time="2024-12-10T12:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to view the attachments sent by Sarah Green in her recent email "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the name of the document attached to the email from Sarah Green",
                },
            ],
            reasoning='The user wants to see a document that was attached to an email they received for Sarah Green. First thing I need to do is search their inbox for an email from someone with that name. Ok I have found an email received 5 minutes ago from Sarah Green so that must be it. I will take the attached document named "Environmental_Resources_Links.pdf" and present it to the user',
            success_conditions=[
                {
                    "input_text": '1. The document name "Environmental_Resources_Links.pdf" attached to the email from Sarah Green received at 12:00 on December 10 2024 is presented to the user',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
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
                # Milestone 1 – The retrieved email is the one from Sarah Green
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
                                                "value": "sarah.green@orchardmail.com",
                                                "partial": False,
                                            },
                                            "attachments": {
                                                "value": "Environmental_Resources_Links.pdf",
                                                "partial": True,  # allow the list to include this file (and possibly others)
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
                # Milestone 2 – Agent shows / references the attachment to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Environmental_Resources_Links",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity  # ensure the filename (or link) appears in the reply
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
            name="EMILY_ROSE_14_85389aa0-4045-4edd-a859-1f114f5cccf7_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T13:00:00-08:00",
            is_read_time="2024-12-10T13:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to see the last email from Sarah Green. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show the last email I received.",
                },
            ],
            reasoning="The user wants to see the last meal they received. Let me look for it in Mail. It appears to be from Sarah Green. I will show it to the user.",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last email from Sarah Green sent on December 10th at 12:00 with the text 'Hi Emily, It was wonderful catching up over coffee this morning! I've attached a few links and resources that could help us with the new environmental outreach programs we discussed. Looking forward to seeing how these ideas take shape and benefit our community. Best regards, Sarah'.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – Agent retrieves the inbox to find the last email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – The search result includes the expected email from Sarah Green
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
                                                "value": "sarah.green@orchardmail.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Great Ideas from Our Coffee Meeting",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-10T12:00:00-08:00",
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
                        ),
                    ],
                ),
                # Milestone 2 – Agent shows the email body (or key excerpt) to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "It was wonderful catching up over coffee this morning",
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
            name="EMILY_ROSE_14_2ec6915f-d87a-4951-8561-69c1ba354cc5_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T12:15:00-08:00",
            is_read_time="2024-12-10T12:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to thank your friend for sending you their resources in the coffee chat. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to her email saying Hi, thank you for the links!",
                },
            ],
            reasoning="The user wants to reply to her latest email with the text \"Hi, thank you for the links!\". First I'll find the specific email by looking through recently received emails, there's one from Sarah Green with resources links, and with this I can compose the reply and see if the user is happy to send it.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A reply is sent to Sarah Green's latest email saying \"Hi Sarah, thank you for the links!”",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – Agent looks up Sarah’s email thread
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – confirm last email from sara green found
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
                                                "value": "Great Ideas from Our Coffee Meeting",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-10T12:00:00",
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
                # Milestone 2 – A reply email has been sent that thanks Sarah
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["sarah.green@orchardmail.com"]
                                    ],
                                    "body": "thank you",
                                    "creation_datetime_iso": "2024-12-10T12:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "body": column_contains_similarity,  # ensure the body contains the required phrase,
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
                (0, 1),  # The agent first retrieves the email
                (1, 2),  # After finding the email, reply to it
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_14_146bcdf2-52c9-49a2-953e-eb17c8f1b4ea_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T12:15:00-08:00",
            is_read_time="2024-12-10T12:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to thank Sarah for the work you put in together this morning. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Email Sarah Green this; "Hey Sarah, thanks for passing this on. great work today!"',
                },
            ],
            reasoning="Ok so the user wants to email Sarah Green a given message. First is who the message is to which is given by the user. Next is the method which is also given by the user.  I will now send the user's given message at 12:15 on 10 December 2024. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message "Hey Sarah, thanks for passing this on. great work today!" is sent to Sarah Green via email at 12:15 on 10 December 2024. ',
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – Agent looks through emails to find Sarah / the relevant thread
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – Confirm the email from Sarah Green was actually surfaced
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
                                                "value": "Great Ideas from Our Coffee Meeting",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "sarah.green@orchardmail.com",
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
                # Milestone 2 – A new email is sent that thanks Sarah
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "status": "sent",
                                    "body": "Hey Sarah, thanks for passing this on. great work today!",
                                    "creation_datetime_iso": "2024-12-10T12:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "status": column_exact_match_similarity,
                                "body": column_contains_similarity,
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
                (0, 1)
            ],  # M1 confirms M0's search; the send (M2) stays ungated
        ),
        ScenarioExtension(
            name="EMILY_ROSE_14_93f950ba-1e95-4b97-a037-d0ed7bb4dabd_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T12:10:00-08:00",
            is_read_time="2024-12-11T12:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know what time you received the email from Sarah yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did Sarah email me yesterday?",
                },
            ],
            reasoning="Okay so, the user is looking for an email from Sarah from yesterday. Firstly I shall look into the contacts of the user. There is one contact matching 'Sarah' named 'Sarah Rose'. Next I shall check their Mail with all emails received yesterday, which was 10 December 2024. There is only one email received from 'Sarah Green' with the subject 'Great Ideas from Our Coffee Meeting'. This is different to the 'Sarah Rose' in their contacts but as the user has specified they are looking for an email from Sarah, I can confidently say the email received from 'Sarah Green' at 12:00 is the one the user is requesting. I can then read out this information to them.",
            success_conditions=[
                {
                    "input_text": "1. The time of the email received from Sarah Green on 10 December 2024 at 12:00, with the subject 'Great Ideas from Our Coffee Meeting' is read out to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – The agent looks for the relevant email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – Confirms the email from Sarah Green dated 2024-12-10 12:00 −08:00 was found
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
                                                "value": "sarah.green@orchardmail.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-10T12:00:00-08:00",
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
                # Milestone 2 – The agent tells the user the correct time (any reasonable phrasing)
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
                                        ("12:00", "12 pm", "12 p.m.", "noon", "12pm")
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
                (0, 1),  # Email search → confirm email exists
                (1, 2),  # Confirmed email → inform user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_14_bdc39570-aa3b-44e7-b905-9e38d89f6c5a_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T12:10:00-08:00",
            is_read_time="2024-12-10T12:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to dictate a reply to Sarah saying that the links in the email aren't working. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a reply to the email I got today at 12:00 and say "Hi Sarah would it be possible to resend the file because the links aren\'t working for me."',
                },
            ],
            reasoning='The user is asking to send an email.\nFirst, I need to identify the intended recipient. The user has specified the recipient is the send of an email they received on December 10 2024 at 12:00. I can see only one email matching this: the email received from Sarah Green.\nNext, I will compose the message as instructed. A message saying "Hi Sarah would it be possible to resend the file because the links aren\'t working for me." will be send to Sarah Green.',
            success_conditions=[
                {
                    "input_text": '1. A reply email is sent to Sarah Green saying "Hi Sarah would it be possible to resend the file because the links aren\'t working for me."',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – the agent looks up the relevant email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – confirm the email from Sarah Green (Dec 10, 12:00 PM) was found
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
                                                "value": "sarah.green@orchardmail.com",
                                                "partial": True,
                                            },
                                            "subject": {
                                                "value": "Great Ideas",
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
                # Milestone 2 – a reply email is actually sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "status": "sent",
                                    "body": "links aren't working",
                                    "creation_datetime_iso": "2024-12-10T12:10:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "status": column_exact_match_similarity,
                                "body": column_contains_similarity,
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_14_bdc39570-aa3b-44e7-b905-9e38d89f6c5a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T12:10:00-08:00",
            is_read_time="2024-12-10T12:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to dictate a reply to Sarah saying that the links in the email aren't working. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a reply email to Sarah saying "Hi Sarah would it be possible to resend the file because the links aren\'t working for me."',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Sarah.\nI should locate the email history with this contact by searching their name in the user's Inbox and then start a draft reply.\nI can see two people named Sarah in the user's contacts. The most recently contacted Sarah is Sarah Green. This must be who the user is referring to.\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": '1. A reply email is sent to Sarah Green saying "Hi Sarah would it be possible to resend the file because the links aren\'t working for me."',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – Agent looks up recent email(s) to or from Sarah
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – Confirm at least one email from Sarah Green was returned in the previous tool call
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
                                                "value": "sarah.green@orchardmail.com",
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
                # Milestone 2 – A reply email has been sent to Sarah with the requested wording
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["sarah.green@orchardmail.com"]
                                    ],
                                    "status": "sent",
                                    "body": "links aren't working",
                                    "creation_datetime_iso": "2024-12-10T12:10:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # email search → confirm Sarah’s email found
                (1, 2),  # confirmation → verify reply sent
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_14_93f950ba-1e95-4b97-a037-d0ed7bb4dabd_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T12:10:00-08:00",
            is_read_time="2024-12-11T12:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know what time you received the email from Sarah yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I receive that email yesterday?",
                },
            ],
            reasoning="Right so, the user is requesting the time information about an email received yesterday, which is 10 December 2024. I can check their Mail and can see that only one email was received yesterday at 12:00 from 'Sarah Green' with the subject 'Great Ideas from Our Coffee Meeting'. This is the email that the user is searching for and therefore I can read out the time information to them.",
            success_conditions=[
                {
                    "input_text": "1. The time of the email received from Sarah Green on 10 December 2024 at 12:00, with the subject 'Great Ideas from Our Coffee Meeting' is read out to the user.",
                    "statefullness": "Stateless",
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
                # Milestone 1 – Confirm the expected email from Sarah Green was retrieved
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
                                                "value": "sarah.green@orchardmail.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Great Ideas from Our Coffee Meeting",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-10T12:00:00-08:00",
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
                # Milestone 2 – Agent tells the user the correct time (12:00 PM / noon)
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
                                            "12:00",
                                            "12 pm",
                                            "12 p.m.",
                                            "12pm",
                                            "12 PM",
                                            "noon",
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
            name="EMILY_ROSE_14_eee01cb8-3fa6-45b9-a7d7-239d6888e302_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T12:05:00-08:00",
            is_read_time="2024-12-10T12:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know what Sarah said in her last email but you cannot look at your phone right now. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What did the email I received from Sarah Green at 12:00 on December 10 2024 say.",
                },
            ],
            reasoning="I have every bit of information I need to access the email. I open the email and present it to the user and also read it out loud.",
            success_conditions=[
                {
                    "input_text": "1. The email received from 'Sarah Green' on 10 December 2024 at 12:00 with the subject line 'Great Ideas from Our Coffee Meeting' is read out loud to the user. \n",
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
                    ]
                ),
                # Milestone 1 – The retrieved email matches Sarah Green’s 12 pm Dec 10 2024 message
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
                                                "value": "sarah.green@orchardmail.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-10T12:00:00-08:00",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Great Ideas from Our Coffee Meeting",
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
                # Milestone 2 – Agent conveys the email body (or key excerpts) to the user
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
                                            "It was wonderful catching up",
                                            "wonderful catching up over coffee",
                                            "I've attached a few links",
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
            name="EMILY_ROSE_14_6a0b0342-45e0-4f0a-b9b1-172d3fffdeaa_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T15:30:00-08:00",
            is_read_time="2024-12-10T15:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Sarah's email is superb.   You want to forward this on to your manager Michael Thompson since maybe you could use some of the information for the community centre going forward. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Please forward the great ideas coffee morning email from Sarah on to my community leader with the message "I just received these from Sarah. I think there\'s a lot of beneficial information in here!"',
                },
            ],
            reasoning='The user has requested for me to forward the great ideas coffee morning email from Sarah on to their community leader. I\'ll have to check through the user\'s emails and see if I can find anything that matches this criteria... I did find one matching email called "Great Ideas from Our Coffee Meeting" from Sarah Green received on December 10th 2024 at 12:00. It has an attachment called Environmental_Resources_Links.pdf.\n\nThey asked me to forward it on to their community leader. I\'ll look through the user\'s contacts to find if there is anyone called Community Leader... and I found "Michael Thompson" listed in their contacts, who has the alias Community Leader. This must be who the user is referring to.\n\nWith the user\'s confirmation, I\'ll forward the email "Great Ideas from Our Coffee Meeting" from Sarah Green received on December 10th 2024 at 12:00 to Michael Thompson with the message "I just received these from Sarah. I think there\'s a lot of beneficial information in here!".',
            success_conditions=[
                {
                    "input_text": '1. The email  "Great Ideas from Our Coffee Meeting" from Sarah Green received on December 10th 2024 at 12:00 is forwarded to Michael Thompson with the message "I just received these from Sarah. I think there\'s a lot of beneficial information in here!".',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
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
                # Milestone 0 – Agent tries to locate the referenced email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – Verify the correct email (from Sarah, correct subject) surfaced in the preceding tool output
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
                                                "value": "Great Ideas from Our Coffee Meeting",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "sarah.green@orchardmail.com",
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
                # Milestone 2 – Forwarded email is successfully sent to Michael Thompson
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["michael.thompson@orchardcommunity.org"]
                                    ],
                                    "subject": "Great Ideas",  # forward likely keeps/contains the original subject
                                    "body": "I just received these from Sarah. I think there's a lot of beneficial information in here!",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-10T15:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_subset_match_similarity,  # must at least include Michael
                                "subject": column_contains_similarity,  # ensure original subject carried over
                                "body": column_contains_similarity,  # ensure custom message present
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
            name="EMILY_ROSE_14_6a0b0342-45e0-4f0a-b9b1-172d3fffdeaa_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T15:30:00-08:00",
            is_read_time="2024-12-10T15:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Sarah's email is superb.   You want to forward this on to your manager Michael Thompson since maybe you could use some of the information for the community centre going forward. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Please forward that great email from Sarah on to my manager with the message "I just received these from Sarah. I think there\'s a lot of beneficial information in here!"',
                },
            ],
            reasoning="The user has requested for me to forward an email to their manager. I'm not fully sure what email the user is referring to. They only told me to forward 'the great email from Sarah'. I'll have to check through the user's emails and see if I can find anything from a Sarah... I did find one matching email called \"Great Ideas from Our Coffee Meeting\" from Sarah Green received on December 10th 2024 at 12:00. It has an attachment called Environmental_Resources_Links.pdf.\n\nThey asked me to forward it on to their manager. I'll look through the user's contacts to see who their manager is.... and I found \"Michael Thompson\" listed in their contacts as manager. This must be who the user is referring to.\n\nWith the user's confirmation, I'll forward the email \"Great Ideas from Our Coffee Meeting\" from Sarah Green received on December 10th 2024 at 12:00 to Michael Thompson with the message \"I just received these from Sarah. I think there's a lot of beneficial information in here!\".",
            success_conditions=[
                {
                    "input_text": '1. The email  "Great Ideas from Our Coffee Meeting" from Sarah Green received on December 10th 2024 at 12:00 is forwarded to Michael Thompson with the message "I just received these from Sarah. I think there\'s a lot of beneficial information in here!".',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
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
                # Milestone 0 – email lookup
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – correct email from Sarah Green is present in the tool output from Milestone 0
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
                                                "value": "Great Ideas from Our Coffee Meeting",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "sarah.green@orchardmail.com",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-10T12:00:00-08:00",
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
                # Milestone 2 – forwarded email sent to Michael Thompson
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["michael.thompson@orchardcommunity.org"]
                                    ],
                                    "status": "sent",
                                    "body": "I just received these from Sarah. I think there's a lot of beneficial information in here!",
                                    "creation_datetime_iso": "2024-12-10T15:30:00-08:00",
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
            name="EMILY_ROSE_14_eee01cb8-3fa6-45b9-a7d7-239d6888e302_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T12:05:00-08:00",
            is_read_time="2024-12-10T12:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know what Sarah said in her last email but you cannot look at your phone right now. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What did Sarah's last email say? ",
                },
            ],
            reasoning="The user wants me to read out the contents of an email received from a contact named 'Sarah'. Firstly, going into the user's contacts, I can see one contact matching named 'Sarah Rose'. Next, I check the user's Mail and can see that there are no e-mails received from 'Sarah Rose', but there is an email received from 'Sarah Green'. This contact isn't in the user's contacts but this has to be the email the user is searching for. The email has been received on 10 December 2024 at 12:00, with the subject line 'Great Ideas from Our Coffee Meeting'. Now that I have found the correct email, I can read out the contents of this email to the user which reads as 'Hi Emily, It was wonderful catching up over coffee this morning! I've attached a few links and resources that could help us with the new environmental outreach programs we discussed. Looking forward to seeing how these ideas take shape and benefit our community. Best regards, Sarah'.",
            success_conditions=[
                {
                    "input_text": "1. The email received from 'Sarah Green' on 10 December 2024 at 12:00 with the subject line 'Great Ideas from Our Coffee Meeting' is read out loud to the user. \n",
                    "statefullness": "Stateless",
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
                # Milestone 1 – Confirm the returned email is Sarah Green’s message with the correct subject
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
                                                "value": "Great Ideas from Our Coffee Meeting",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "sarah.green@orchardmail.com",
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
                # Milestone 2 – Agent tells the user the contents of Sarah’s email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "wonderful catching up over coffee",
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
            name="EMILY_ROSE_14_956a9749-25cc-4986-bf15-a5afae975df5_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T12:05:00-08:00",
            is_read_time="2024-12-10T12:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know if Sarah Green has sent an email. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did Sarah email yet?",
                },
            ],
            reasoning="The user wants to know if Sarah emailed yet. I wonder who that is. I should check their contacts to figure it out. Okay, the user only has one contact called Sarah, Sarah Rose. I don't see any emails received from that user. However the user received an email from a sender called Sarah Green, today, December 10th at 12:00. This must be what they want to see. I'll show them this email. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The email from Sarah Green, received on December 10th 2024, at 12:00 with the subject 'Great Ideas from Our Coffee Meeting' is shown to the user. ",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
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
                # Milestone 1 – Sarah Green’s email is present in the retrieved results
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
                                                "value": "Great Ideas from Our Coffee Meeting",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "sarah.green@orchardmail.com",
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
                # Milestone 2 – Agent answers the user mentioning the email / subject
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("Great Ideas",)],
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
                (0, 1),  # Email lookup → confirm Sarah’s email found
                (1, 2),  # Confirmation of email → user-facing response
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_14_10866eee-d9d1-4e69-a838-4260a7d1c490_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "email",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T15:30:00-08:00",
            is_read_time="2024-12-10T15:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Sarah's email is superb.   You want to forward this on to your manager Michael Thompson since maybe you could use some of the information for the community centre going forward. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Please forward that email from Sarah on to my manager with the message "I just received these from Sarah. I think there\'s a lot of beneficial information in here!"',
                },
            ],
            reasoning="The user has requested for me to forward an email to their manager. I'm not fully sure what email the user is referring to. They only told me to forward 'that email from Sarah'. I'll have to check through the user's emails and see if I can find anything from a Sarah... I did find one matching email called \"Great Ideas from Our Coffee Meeting\" from Sarah Green received on December 10th 2024 at 12:00. It has an attachment called Environmental_Resources_Links.pdf.\n\nThey asked me to forward it on to their manager. I'll look through the user's contacts to see who their manager is.... and I found \"Michael Thompson\" listed in their contacts as manager. This must be who the user is referring to.\n\nWith the user's confirmation, I'll forward the email \"Great Ideas from Our Coffee Meeting\" from Sarah Green received on December 10th 2024 at 12:00 to Michael Thompson with the message \"I just received these from Sarah. I think there's a lot of beneficial information in here!\".",
            success_conditions=[
                {
                    "input_text": '1. The email  "Great Ideas from Our Coffee Meeting" from Sarah Green received on December 10th 2024 at 12:00 is forwarded to Michael Thompson with the message "I just received these from Sarah. I think there\'s a lot of beneficial information in here!".',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "send_email",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looks through email to locate Sarah’s message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – Confirm that the email from Sarah with correct subject was actually surfaced
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
                                                "value": "Great Ideas from Our Coffee Meeting",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "sarah.green@orchardmail.com",
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
                # Milestone 2 – A new outgoing email (forward) was created and sent to Michael Thompson
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["michael.thompson@orchardcommunity.org"]
                                    ],
                                    "status": "sent",
                                    "body": "I just received these from Sarah. I think there's a lot of beneficial information in here!",
                                    "creation_datetime_iso": "2024-12-10T15:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Require Michael is among the recipients; allow extras if any
                                "recipients_addresses": column_list_subset_match_similarity,
                                "status": column_exact_match_similarity,
                                "body": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # Ignore sandbox chatter when comparing EMAIL additions
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_14_897df834-ba92-429b-8cb3-b634717d61cc_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T13:30:00-08:00",
            is_read_time="2024-12-10T13:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You can't remember what the name of the document in your most recently received email is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell me the file name of the attachment on the newest email in my inbox.",
                },
            ],
            reasoning='I need to figure out the name of an attachment in an email. The user said the attachment they\'re asking about is in the newest email in their inbox. The most recent email is from 12:00 today, an email with the subject "Great Ideas from Our Coffee Meeting." I\'ll read the name of the file attached to that email, "Environmental_Resources_Links.pdf", to the user.',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the email with the subject "Great Ideas from Our Coffee Meeting," received at 12;00 on 10 December 2024, has an attached file named "Environmental_Resources_Links.pdf"',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – the agent uses an email-reading tool (search_emails or get_all_emails)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – confirm that the retrieved email is the expected newest email and that it
                # contains the correct attachment filename
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
                                                "value": "Great Ideas from Our Coffee Meeting",
                                                "partial": False,
                                            },
                                            "attachments": {
                                                "value": [
                                                    "Environmental_Resources_Links.pdf"
                                                ],
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,  # depend on Milestone 0 tool output
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
                # Milestone 2 – the agent informs the user of the attachment filename
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Environmental_Resources_Links.pdf",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,  # check filename mentioned
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
            name="EMILY_ROSE_14_4e32bf80-664c-49cb-b410-9eb7a1be96a8_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "messaging",
                "contact",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T13:15:00-08:00",
            is_read_time="2024-12-10T13:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Your fruitful conversation with Sarah reminds you that you had a fruitful conversation with your friend Oliver last week, and you want to be reminded of the last messages you two exchanged. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What does the last text from the guy I met with on Thursday December 5th say?",
                },
            ],
            reasoning="I need to retrieve some information for the user. They want to know what the last text message was from one of their contacts. I need to first figure out which contact's messages they want to know about. They said the contact is the guy they met with on Thursday December 5th. Let me look at the user's calendar events from that day. The only meeting they had on that day was one from 16:00-17:00 called \"Meeting with Oliver Green for Community Gathering Refreshments\" where Oliver Green was the only other attendee. So that means Oliver Green is the person whose texts the user is asking about. They want to know what he last texted to them. Looking at the messages between the user and Oliver, I see Oliver's last message says \"Perfect! Thanks again, Emily. Excited for the gathering!\" so I'll present this to the user.",
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the last text they received from Oliver Green on 5 December 2024 at 16:35 says "Perfect! Thanks again, Emily. Excited for the gathering!"',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_messages",
                "get_all_messages",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – Agent looks up who the user met on Thursday Dec 5 (via calendar)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – Confirm the Dec 5 meeting with Oliver Green was retrieved
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
                                                "value": "Meeting with Oliver Green for Community Gathering Refreshments",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-05T16:00:00-08:00",
                                                "partial": False,
                                            },
                                            "attendees_names": {
                                                "value": ["Emily Rose", "Oliver Green"],
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
                # Milestone 2 – Agent uses messaging tools to look up texts with Oliver around that time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 3 – Confirm the last message from Oliver in that thread is correctly identified
                # (content "Perfect! Thanks again, Emily. Excited for the gathering!")
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
                                                "value": "Oliver Green",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "+1 530-555-0128",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Perfect! Thanks again, Emily. Excited for the gathering!",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-05T16:35:00-08:00",
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
                # Milestone 4 – User-facing answer includes the key content of Oliver's last text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Perfect! Thanks again, Emily. Excited for the gathering!",
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
                (
                    0,
                    1,
                ),  # Found Dec 5 calendar event → confirmed it's the meeting with Oliver
                (1, 2),  # Identified Oliver as the person → searched messages
                (
                    2,
                    3,
                ),  # Searched messages → confirmed correct last message from Oliver
                (
                    3,
                    4,
                ),  # Correct last message identified → informed user with that content
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_14_10866eee-d9d1-4e69-a838-4260a7d1c490_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "email",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T15:30:00-08:00",
            is_read_time="2024-12-10T15:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Sarah's email is superb.   You want to forward this on to your manager Michael Thompson since maybe you could use some of the information for the community centre going forward. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Please forward the email with the environmental brainstorming on to my community leader with the message "I just received these from Sarah. I think there\'s a lot of beneficial information in here!"',
                },
            ],
            reasoning="The user has requested for me to forward he email with the environmental brainstorming on to their community leader. I'll have to check through the user's emails and see if I can find anything that matches this criteria... I did find one matching email called \"Great Ideas from Our Coffee Meeting\" from Sarah Green received on December 10th 2024 at 12:00. It has an attachment called Environmental_Resources_Links.pdf. If I think of 'environmental brainstorming' and this e-mail that talks about ideas and includes an attachment with environmental resources... It must be this e-mail the user is referring to. \n\nThey asked me to forward it on to their community leader. I'll look through the user's contacts to find if there is anyone called Community Leader... and I found \"Michael Thompson\" listed in their contacts, who has the alias Community Leader. This must be who the user is referring to.\n\nWith the user's confirmation, I'll forward the email \"Great Ideas from Our Coffee Meeting\" from Sarah Green received on December 10th 2024 at 12:00 to Michael Thompson with the message \"I just received these from Sarah. I think there's a lot of beneficial information in here!\".",
            success_conditions=[
                {
                    "input_text": '1. The email  "Great Ideas from Our Coffee Meeting" from Sarah Green received on December 10th 2024 at 12:00 is forwarded to Michael Thompson with the message "I just received these from Sarah. I think there\'s a lot of beneficial information in here!".',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "send_email",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 — the agent looks through the mailbox
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 — the searched/returned email is the one from Sarah with the expected subject
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
                                                "value": "Great Ideas from Our Coffee Meeting",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "sarah.green@orchardmail.com",
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
                # Milestone 2 — a new email was sent/forwarded to Michael Thompson with the requested message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["michael.thompson@orchardcommunity.org"]
                                    ],
                                    "status": "sent",
                                    "body": "I just received these from Sarah. I think there's a lot of beneficial information in here!",
                                    "creation_datetime_iso": "2024-12-10T15:30:00-08:00",
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
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # email lookup → confirm correct email found
                (1, 2),  # correct email found → new email forwarded
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_14_c7cb12db-7bc9-4441-ae5a-9f993ae400ad_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T18:40:00-08:00",
            is_read_time="2024-12-09T18:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to create an event tomorrow called Coffee Meet with Sarah Green. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Make a new calendar event called Coffee Meet with Sarah Green. Schedule it for tomorrow morning 10:00 till 10:30.",
                },
            ],
            reasoning="The user wants to create a new calendar event. The new event will be called Coffee Meet with Sarah Green. The user has clearly stated the date and time. They have requested that it takes place tomorrow morning, which is December 10, and the time will be from 10:00 till 10:30. ",
            success_conditions=[
                {
                    "input_text": "1. Create a new calendar event called Coffee Meet with Sarah Green on December 10 2024 from 10:00 to 10:30.",
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
                                    "calendar_event_name": "Coffee Meet with Sarah Green",
                                    "start_datetime_iso": "2024-12-10T10:00",  # allow any timezone suffix
                                    "end_datetime_iso": "2024-12-10T10:30",
                                    "creation_datetime_iso": "2024-12-09T18:40:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against the pre-task snapshot
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_14_956a9749-25cc-4986-bf15-a5afae975df5_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_14",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T12:05:00-08:00",
            is_read_time="2024-12-10T12:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know if Sarah Green has sent an email. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did Sarah Green email yet?",
                },
            ],
            reasoning="The user wants to know if Sarah Green emailed yet. I wonder who that is. I should check their contacts to figure it out. Okay, the user doesn't have any contacts with that name. However the user received an email from a sender called Sarah Green, today, December 10th at 12:00. This must be what they want to see. I'll show them this email. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The email from Sarah Green, received on December 10th 2024, at 12:00 with the subject 'Great Ideas from Our Coffee Meeting' is shown to the user. ",
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
                # Milestone 1 – The tool output contains the specific email from Sarah Green
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
                                                "value": "sarah.green@orchardmail.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Great Ideas from Our Coffee Meeting",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-10T12:00:00-08:00",
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
                # Milestone 2 – Agent communicates the email (or its key details) to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Great Ideas from Our Coffee Meeting",
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
                (0, 1),  # Tool call → verify email present in results
                (1, 2),  # Email found → agent responds to user
            ],
        ),
    ]
