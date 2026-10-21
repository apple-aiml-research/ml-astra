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
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_tool_trace_partial_arguments_similarity,
    contains_presence_similarity,
    not_contains_presence_similarity,
    snapshot_similarity,
    tool_trace_dependant_similarity,
    update_similarity,
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


def get_TAG_THEO_APPLESEED_pilot_plot_23(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="THEO_APPLESEED_23_8ff38971-b901-4e65-b9b7-e279dbcb2f4f_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:00:00-07:00",
            is_read_time="2024-07-29T10:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to add your 1:1 with Kevin to your calendar today and set a reminder 10 minutes before it starts. "
                        "You're not sure of the exact time off the top of your head — the assistant will need to find it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you add my 1:1 with Kevin to my calendar today and remind me 10 minutes before?",
                },
            ],
            reasoning="The user wants their 1:1 with Kevin on the calendar today with a reminder 10 minutes ahead, but hasn't stated the time. I'll search the user's emails for the meeting details. I find Kevin Chen's email offering 1:00 PM to 2:00 PM, which Theo confirmed, so the 1:1 runs 1:00-2:00 PM. I'll create a calendar event ' 1:1 with Kevin' from 1:00 PM to 2:00 PM today and set the reminder to 10 minutes before.",
            success_conditions=[
                {
                    "input_text": '1. A calendar event "1:1 with Kevin" is created for July 29, 2024 from 1:00 PM to 2:00 PM with a 10-minute reminder.',
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
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent invokes an email-retrieval tool to find the meeting time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – The retrieved emails contain Kevin's 1:00-2:00 PM availability email
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
                                                "value": "kevin.chen@example.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-29T08:05:00-07:00",
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
                # Milestone 2 – The 1:1 with Kevin (1:00-2:00 PM) is created with a 10-minute reminder
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "1:1 with Kevin",
                                    "start_datetime_iso": "2024-07-29T13:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T14:00:00-07:00",
                                    "reminder_time_ahead": "10 minute",
                                    "creation_datetime_iso": "2024-07-29T10:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # Title need only reference Kevin; reminder value is a substring
                                # ("10 minute") so both "10 minutes"/"10 minute" satisfy the non-default offset.
                                "calendar_event_name": column_contains_similarity,
                                "reminder_time_ahead": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_23_9114225e-122b-4bb3-82d4-b5e7905a031d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T08:05:00-07:00",
            is_read_time="2024-07-29T08:05:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to view Kevin's email. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me Kevin's email please",
                },
            ],
            reasoning="The user wants to view \"Kevin's email\".\n\nAlright, firstly, I need to check the user's Mail to see if they've received any emails from Kevin.\n\nGreat, I can see that they've just received an email from \"kevin.chen@example.com\". I will now present this to the user. ",
            success_conditions=[
                {
                    "input_text": "1. The email received from Kevin Chen at 08:05:00 on July 29th, 2024 is presented to the user. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – Agent invokes an email–retrieval tool
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – The retrieved result set contains Kevin’s email from 2024-07-29 08:05
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
                                                "value": "kevin.chen@example.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-29T08:05:00-07:00",
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
                # Milestone 2 – Agent shows the user Kevin’s email content (must mention Kevin and the 1-2 pm availability)
                Milestone(
                    snapshot_constraints=[
                        # Check Kevin is referenced
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Kevin",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Check the time window is referenced (any reasonable phrasing)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "1:00 PM",
                                            "1:00pm",
                                            "1 pm",
                                            "1-2",
                                            "1:00",
                                            "13:00",
                                            "1pm",
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
                (0, 1),  # Email retrieval → confirm Kevin’s email exists
                (1, 2),  # Confirmed email → presented to user
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_23_9114225e-122b-4bb3-82d4-b5e7905a031d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T08:05:00-07:00",
            is_read_time="2024-07-29T08:05:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to view the email you were just sent. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show email ",
                },
            ],
            reasoning='The user wants to "show email".\n\nOkay, so I surmise from this that user would like to view their most recent email. I will therefore need to go to their Mail to check to see if they\'ve received any.\n\nGreat, I see that they\'ve just received an email from "kevin.chen@example.com". This must be what they\'re referring to.\n\nI will now present this email to the user.\n',
            success_conditions=[
                {
                    "input_text": "1. The email received from Kevin Chen at 08:05:00 on July 29th, 2024 is presented to the user. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – The agent calls an email-retrieval tool
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – The returned email list contains Kevin Chen’s email from 08:05 AM
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
                                                "value": "kevin.chen@example.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-29T08:05:00-07:00",
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
                # Milestone 2 – The agent presents the email content to the user
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
                                            "Thank you for reaching out",
                                            "1:00 PM",
                                            "1 to 2",
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
            name="THEO_APPLESEED_23_b8e927fb-d612-4ae5-b481-4cf5e4e12240_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T08:07:00-07:00",
            is_read_time="2024-07-29T08:07:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to schedule an urgent 1:1 with Kevin today, however, his proposed a time which contradicts with your existing dental appointment. You want to message Kevin back saying \"That doesn't work for me as I have a dentist appointment at 1pm, let's find another slot later this week maybe?.  \" "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to reply to Kevin: \"That doesn't work for me as I have a dentist appointment at 1pm, let's find another slot later this week maybe?\"",
                },
            ],
            reasoning="The user wants to reply Kevin saying \"That doesn't work for me as I have a dentist appointment at 1pm, let's find another slot later this week maybe?\". I need to find the messages from Kevin first. After checking user's messages and emails, I found Kevin Chen's email received on '2024-07-29T08:05:00', proposing meeting time 1:00-2:00 today. I will reply this email with the content provided by the user.",
            success_conditions=[
                {
                    "input_text": "An email reply is sent to Kevin Chen with content  \"That doesn't work for me as I have a dentist appointment at 1pm, let's find another slot later this week maybe?\"",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "send_email",
                "search_emails",
                "get_all_emails",
                "search_messages",
                "get_all_messages",
                "send_message",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looks up Kevin’s contact information
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – Verify Kevin Chen’s email thread found
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
                                                "value": "Urgent: Request for 1:1 Meeting Today",
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
                # Milestone 2 – used corret tools
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
                                                "email_id_referred": "place_holder",  # must send email with a thread id to reply an email
                                                "email_id_referred_action": "reply",
                                                "recipients_addresses": [
                                                    "kevin.chen@example.com"
                                                ],
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
                # Milestone 3 – A new message to Kevin has been created and sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        [
                                            "kevin.chen@example.com",
                                        ]
                                    ],
                                    "body": "dentist",
                                    "creation_datetime_iso": "2024-07-29T08:07:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # Require Kevin to be among the participants
                                "recipients_addresses": column_list_exact_match_similarity,
                                # Content must mention “dentist” (captures core of the user’s message)
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
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_23_371a3c62-c450-4ba6-b60c-82f0ce5e800d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T12:00:00-07:00",
            is_read_time="2024-07-29T12:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You got through to Kevin and managed to schedule a quick meeting! But you you want to remind yourself what time your 1:1 with Kevin is today according to your emails with him. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is my 1:1 meeting with Kevin Chen today according to our email conversation?",
                },
            ],
            reasoning="The user wants to know what time their meeting is at today according to an email. Checking the user's calendar, I can't see any events with Kevin Chen in the user's calendar. Checking the user data, I did find an email thread titled \"Urgent: Request for 1:1 Meeting Today\" sent by the user today at 07:50. - it seems likely that this is the email the user is referring toI will go ahead and search through the user's email thread with Kevin Chen. I can see that the two have agreed to a meeting time of 13:00-14:00 on July 29, 2024. I will inform the user of this.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their 1:1 with Kevin Chen is set for 13:00-14:00 on July 29th according to their email.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – Agent looks through email to find the meeting time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                                                "value": "Urgent: Request for 1:1 Meeting Today",
                                                "partial": True,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,  # Depend on search_email/get_all_emails result
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
                # Milestone 2 – Agent tells the user that the meeting is at 1 PM–2 PM
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
                                        ("1:00", "1 pm", "1 pm", "13:00", "1pm")
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
                (0, 1),  # Email search precedes informing the user
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_23_5dc34568-ee16-47b9-b907-51af35a2437c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_high",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T08:15:00-07:00",
            is_read_time="2024-07-29T08:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You need to remove your dentist appointment from your calendar and schedule an urgent meeting with Kevin Chen at the same time "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my dentist appointment from the calendar and replace it with a 1:1 with Kevin Chen",
                },
            ],
            reasoning='The user wants to delete their dentist appointment from the calendar and replace it with a 1:1 with Kevin. Kevin Chen is the only Kevin in their contacts and looking through the user\'s emails I can see they arranged to meet each other at 1pm later today. I will delete the event titled "Dentist Appointment\' as it takes place at the same time as the user wishes to meet Kevin and I will schedule an event titled "1:1 with Kevin" for July 24 at 1pm',
            success_conditions=[
                {
                    "input_text": '1. The calendar event "Dentist Appointment" is deleted from the user\'s calendar ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. A calendar event "1:1 with Kevin" is scheduled for 1pm on July 29',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
                "create_calendar_event",
                "search_contacts",
                "get_all_contacts",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – the agent looks at the calendar to figure out what is on the user’s schedule
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – confirms that the dentist appointment (the event to be removed) was actually retrieved
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
                                                "value": "Dentist Appointment",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T13:00:00-07:00",
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
                # Milestone 2 – the “Dentist Appointment” event is gone
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dentist Appointment",
                                    "start_datetime_iso": "2024-07-29T13:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T14:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ],
                ),
                # Milestone 3 – a new 1:1 meeting with Kevin has been scheduled in its place
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "1:1 with Kevin",
                                    "start_datetime_iso": "2024-07-29T13:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T14:00:00-07:00",
                                    "attendees_names": [["Kevin Chen"]],
                                    "creation_datetime_iso": "2024-07-29T08:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
                                "calendar_event_name": column_contains_similarity,
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
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_23_171bb259-79d8-47a5-afd0-d94cae00f78c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T13:06:00-07:00",
            is_read_time="2024-07-23T13:06:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You are busy at the moment but want to know what the most recent message from Stefan Mustermann said. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What does my most recent message from Stefan Mustermann say?",
                },
            ],
            reasoning="The user wants to know the content of their most recent message from Stefan. First I should figure out who Stefan is. Looking at the user's Contacts there is only one Stefan, Stefan Mustermann, so this must be who they mean. I should check Messages now for a text from Stefan. Looking at the user's Messages, the most recent text from Stefan Mustermann was received at 13:05 on 23 July 2024. I will tell the user the message says \"Got it. I'm already here, saved us a spot.\".",
            success_conditions=[
                {
                    "input_text": "1. The most recent message from Stefan Mustermann is read aloud. ",
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
                # Milestone 0 – Some message-retrieval tool is invoked
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – The retrieved tool result contains the latest message from Stefan
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
                                                "value": "Got it. I'm already here, saved us a spot.",
                                                "partial": True,  # allow minor punctuation / whitespace variation
                                            },
                                            # At least one indication that Stefan is a participant
                                            "participants_addresses": {
                                                "value": "stefan.mustermann@example.com",
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
                # Milestone 2 – Agent tells the user what Stefan’s most recent message says
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Got it. I'm already here, saved us a spot.",
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
            name="THEO_APPLESEED_23_834b6ec9-d10e-4981-bfa1-f92c033ee527_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T08:30:00-07:00",
            is_read_time="2024-07-29T08:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You need to cancel your dentist appointment and schedule a meeting with Kevin Chen at 13:00 on July 29th. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my medical event today, schedule a 1:1 meeting with Kevin Chen in its place.",
                },
            ],
            reasoning="The user is asking me to perform a number of tasks.\nFirst, they want me to delete an event. I should search their calendar for this event.\nThe user has mentioned a medical event, this will narrow my search.\nI have found the relevant event, Dentist Appointment at 13:00-14:00 on July 29th 2024. I will go ahead and delete this event.\nNext, they have asked me to schedule a new event at the same times as the previous. \nNew event 1:1 meeting with Kevin Chen will be scheduled for 13:00-14:00 on July 29, 2024.\n",
            success_conditions=[
                {
                    "input_text": "1. Dentist appointment at 13:00-14:00 on July 29th 2024 has been cancelled. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. 1:1 meeting with Kevin Chen has been scheduled for 13:00-14:00 on July 29th 2024.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
                "create_calendar_event",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looked up calendar events to locate the medical appointment
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – Confirm the Dentist Appointment surfaced in the tool output from Milestone 0
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
                                                "value": "Dentist Appointment",
                                                "partial": False,
                                            },
                                            # Start time check is optional but adds confidence
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T13:00:00-07:00",
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
                # Milestone 2 – The original dentist appointment has been removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dentist Appointment",
                                    "start_datetime_iso": "2024-07-29T13:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T14:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ]
                ),
                # Milestone 3 – A new 1:1 meeting with Kevin Chen has been created for the same slot
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "1:1 meeting with Kevin Chen",
                                    "start_datetime_iso": "2024-07-29T13:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T14:00:00-07:00",
                                    "attendees_names": [
                                        ["Kevin Chen", "Theo Appleseed"]
                                    ],
                                    "creation_datetime_iso": "2024-07-29T08:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,  # just needs to mention "1:1" or Kevin Chen
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox noise when checking calendar addition
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_23_834b6ec9-d10e-4981-bfa1-f92c033ee527_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T08:30:00-07:00",
            is_read_time="2024-07-29T08:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You need to cancel your dentist appointment and schedule a meeting with Kevin Chen at 13:00 on July 29th. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to have a 1:1 meeting with Kevin Chen at 13:00 but I have a dentist appointment at the same time. Cancel the dentist appointment and book the meeting with Kevin. ",
                },
            ],
            reasoning="The user is asking me to perform a number of tasks.\nFirst, they want me to delete an event. I should search their calendar for this event.\nI have found the relevant event, Dentist Appointment at 13:00-14:00 on July 29th 2024. I will go ahead and delete this event.\nNext, they have asked me to schedule a new event at the same times as the previous. \nNew event 1:1 meeting with Kevin Chen will be scheduled for 13:00-14:00 on July 29, 2024.\n",
            success_conditions=[
                {
                    "input_text": "1. Dentist appointment at 13:00-14:00 on July 29th 2024 has been cancelled. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. 1:1 meeting with Kevin Chen has been scheduled for 13:00-14:00 on July 29th 2024.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
                "create_calendar_event",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looks up existing calendar events (to find the dentist appointment)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – The dentist appointment was indeed returned in the previous tool call
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
                                                "value": "Dentist Appointment",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T13:00:00-07:00",
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
                # Milestone 2 – The dentist appointment has been removed / cancelled
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dentist Appointment",
                                    "start_datetime_iso": "2024-07-29T13:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        ),
                    ],
                ),
                # Milestone 3 – New 1:1 meeting with Kevin is on the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Kevin",  # we will match substrings
                                    "start_datetime_iso": "2024-07-29T13:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T14:00:00-07:00",
                                    "attendees_names": [
                                        ["Kevin Chen", "Theo Appleseed"]
                                    ],
                                    "creation_datetime_iso": "2024-07-29T08:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "attendees_names": column_list_subset_match_similarity,
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
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_23_171bb259-79d8-47a5-afd0-d94cae00f78c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T13:06:00-07:00",
            is_read_time="2024-07-23T13:06:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You are busy at the moment but want to know what the most recent message from Stefan Mustermann said. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read me Stefan's last message. ",
                },
            ],
            reasoning="The user wants the last message from Stefan read to them. The first thing I should do is figure out who Stefan is. Hmmm, looking at the user's Contacts they only have one Stefan, Stefan Mustermann, so this must be who they mean. Next I will check Messages for the most recent message from him. From this I can see the most recent message from Stefan Mustermann was received at 13:05 on 23 July 2024. It reads \"Got it. I'm already here, saved us a spot.\". I will tell the user this. ",
            success_conditions=[
                {
                    "input_text": "1. The most recent message from Stefan Mustermann is read aloud. ",
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
                # Milestone 0 – The agent queries the message store to find Stefan’s messages
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – Confirm the tool output included the most recent message from Stefan
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
                                                "value": "stefan.mustermann@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Got it. I'm already here, saved us a spot.",
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
                # Milestone 2 – The agent tells the user the content of Stefan’s last message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "saved us a spot",
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
            name="THEO_APPLESEED_23_5dc34568-ee16-47b9-b907-51af35a2437c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T08:15:00-07:00",
            is_read_time="2024-07-29T08:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You need to remove your dentist appointment from your calendar and schedule an urgent meeting with Kevin Chen at the same time as discussed in the email thread "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my appointment today from the calendar and replace it with the urgent 1:1 meeting with information in the thread",
                },
            ],
            reasoning="The user wants to delete their appointment today from the calendar and replace it with an urgent 1:1 meeting. Looking through the user's emails I can see Kevin Chen and the user arranged to meet each other at 1pm later today.  Looking at the user's calendar I can see they already have a dentist appointment scheduled for this time so I can assume this is the appointment the user wishes to delete. I will delete the event titled \"Dentist Appointment' and I will schedule an event titled something like \"1:1 with Kevin\" for July 24 at 1pm.",
            success_conditions=[
                {
                    "input_text": '1. The calendar event "Dentist Appointment" is deleted from the user\'s calendar ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. A calendar event with keyword "1:1" is scheduled for 1pm on July 29 with Kevin Chen as an invitee',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
                "create_calendar_event",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – Agent looks up today’s calendar events
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 - Dentist appointment found
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
                                                "value": "Dentist Appointment",
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
                # Milestone 2 – The “Dentist Appointment” event has been removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dentist Appointment",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial state
                        )
                    ],
                ),
                # Milestone 3 – Agent searches emails for anything with urgent meeting
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 4 – Confirm that the relevant email from Kevin retrieved
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
                                        # We only require that this email exists in the search results.
                                        match_conditions={
                                            "subject": {
                                                "value": "Urgent: Request for 1:1 Meeting Today",
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
                            reference_milestone_node_index=3,
                        )
                    ]
                ),
                # Milestone 5 – A new 1:1 with Kevin is scheduled for 1-2 pm on 29 Jul 2024
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "1:1",
                                    "start_datetime_iso": "2024-07-29T13:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T14:00:00-07:00",
                                    "attendees_names": [
                                        ["Kevin Chen", "Theo Appleseed"]
                                    ],
                                    "creation_datetime_iso": "2024-07-29T08:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
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
                (3, 4),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_23_371a3c62-c450-4ba6-b60c-82f0ce5e800d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T12:00:00-07:00",
            is_read_time="2024-07-29T12:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You got through to Kevin and managed to schedule a quick meeting! But you you want to remind yourself what time your 1:1 with Kevin is today according to your emails with him. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is my meeting today according to my manager?",
                },
            ],
            reasoning="The user wants to know what time their meeting is at today according to his manager. First, I should determine if they are referring to a specific contact. I can see that Kevin Chen is tagged as manager in the user's contacts, but I don't see any events with Kevin Chen in the user's calendar scheduled for today. Checking the user data, I did find an email thread titled \"Urgent: Request for 1:1 Meeting Today\" sent by the user today at 07:50. - it seems likely that this is the email the user is referring toI will go ahead and search through the user's email thread with Kevin Chen. I can see that the two have agreed to a meeting time of 13:00-14:00 on July 29, 2024. I will inform the user of this.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their 1:1 with Kevin Chen is set for 13:00-14:00 on July 29th according to their email.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "get_all_contacts",
                "search_contacts",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – The agent looks through the user’s emails to find the meeting details
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                                                "value": "Urgent: Request for 1:1 Meeting Today",
                                                "partial": True,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,  # Depend on search_email/get_all_emails result
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
                # Milestone 2 – The agent’s reply to the user mentions the meeting start time (1 PM / 13:00)
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
                                            "1:00",
                                            "1 pm",
                                            "1pm",
                                            "13:00",
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
                # Milestone 3 – The agent’s reply also mentions the meeting end time (2 PM / 14:00)
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
                                            "2:00",
                                            "2 pm",
                                            "2pm",
                                            "14:00",
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
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_23_f5d136b7-5b4e-4336-8622-608b75feeb11_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T08:00:00-07:00",
            is_read_time="2024-07-29T08:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You need to meet Kevin but he is only available during your already scheduled dentist appointment.   You decide to reschedule your dentist. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Move my dentist appointment to tomorrow, keep the times the same.",
                },
            ],
            reasoning="The user is asking to reschedule an event.\nI should find the event in their calendar.\nI have found the event, Dentist Appointment scheduled for July 29, 2024 13:00-14:00.\nBefore rescheduling I should look ahead and ensure there are not possible clashes. I can see no potential clashes.\nDentist Appointment event scheduled for July 29, 2024 13:00-14:00 is now scheduled for July 30, 2024, 13:00-14:00.",
            success_conditions=[
                {
                    "input_text": "1) Dentist Appointment event scheduled for July 29, 2024 13:00-14:00 is rescheduled to July 30, 2024, 13:00-14:00.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "modify_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – The agent looks up existing calendar events
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – Confirm that the dentist appointment on July 29 was located
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
                                                "value": "Dentist Appointment",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T13:00:00-07:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-07-29T14:00:00-07:00",
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
                # Milestone 2 – Dentist appointment is rescheduled to July 30 at the same time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dentist Appointment",
                                    "start_datetime_iso": "2024-07-30T13:00:00-07:00",
                                    "end_datetime_iso": "2024-07-30T14:00:00-07:00",
                                    "creation_datetime_iso": "2024-07-29T08:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
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
                (0, 1),  # event search → confirmation
                (1, 2),  # confirmation → event update
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_23_83a7927d-7ed1-4944-8816-ca4bf22df160_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T08:20:00-07:00",
            is_read_time="2024-07-29T08:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to dictate a reply email to Kevin saying that his availability won't work today, and that the user will speak to him tomorrow about it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to dictate an email reply to Kevin Chen saying \"Hi Kevin I don't think your availability for the 1:1 meeting works for me today, I'll check my calendar and speak to you tomorrow about it to reschedule.\"",
                },
            ],
            reasoning="The user wants to dictate a reply email to the contact called Kevin Chen.\n\nI should locate the email history with this contact by searching their name in the user's inbox and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will add the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the email was transcribed correctly.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A reply email is sent to Kevin Chen saying that his availability for the 1:1 meeting won't work today, and that the user will speak to him tomorrow about it.",
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "send_email",
                "modify_draft_email",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the existing thread with Kevin (email search)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – A reply email is sent to Kevin stating that today's availability won't work
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
                                    "body": "availability",  # will be matched with contains-similarity,
                                    "creation_datetime_iso": "2024-07-29T08:20:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "body": column_contains_similarity,  # checks the phrase “availability” is present,
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
                (0, 1),  # Agent searches emails → sends the reply
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_23_f94a529b-70a3-4214-8f22-6d8e7918fa9f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T08:05:00-07:00",
            is_read_time="2024-07-29T08:05:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know if your manager responded to your email yet. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did my manager respond to my email?",
                },
            ],
            reasoning="The user wants to know if their manager has responded to their email yet. I better check who their manager is by searching through their contacts. I see that Kevin Chen is listed as Manager. Okay, now I need look for a recent email message from Kevin Chen. I see one message received just now on July 27th at 08:05. This must be the reply the user was expecting. I'll show the message to the user. ",
            success_conditions=[
                {
                    "input_text": "1. Mail is checked for new messages from Kevin Chen. ",
                    "statefullness": "Stateless",
                },
                {
                    "statefullness": "Stateless",
                    "input_text": "2. The message from Kevin Chen received on July 29th at 08:05 is shown to the user. ",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – The agent looks for emails (should invoke an email-retrieval tool)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – Confirm the expected reply email from Kevin Chen is present in the tool output of Milestone 0
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
                                                "value": "kevin.chen@example.com",
                                                "partial": False,
                                            },
                                            "body": {
                                                "value": "1:00 PM",
                                                "partial": True,  # allow substring match within body
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
                # Milestone 2 – The agent shows the user Kevin’s response (key info must appear)
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
                                            "Kevin",
                                            "1:00 PM",
                                            "1-2",
                                            "available",
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
                (0, 1),  # Email search → verify correct email found
                (1, 2),  # Email verified → user is shown the response
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_23_f5d136b7-5b4e-4336-8622-608b75feeb11_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T08:00:00-07:00",
            is_read_time="2024-07-29T08:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You need to meet Kevin but he is only available during your already scheduled dentist appointment.   You decide to reschedule your dentist. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reschedule my medical thing to tomorrow, keep the times as they are.",
                },
            ],
            reasoning="The user is asking to reschedule an event.\nI should find the event in their calendar.\nThe user has specified it is a medical event, I can see only one potential match scheduled for today: the event Dentist Appointment scheduled for July 29, 2024 13:00-14:00.\nBefore rescheduling I should look ahead and ensure there are not possible clashes. I can see no potential clashes.\nDentist Appointment event scheduled for July 29, 2024 13:00-14:00 is now scheduled for July 30, 2024, 13:00-14:00.",
            success_conditions=[
                {
                    "input_text": "1) Dentist Appointment event scheduled for July 29, 2024 13:00-14:00 is rescheduled to July 30, 2024, 13:00-14:00.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "modify_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (information-retrieval)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – The dentist appointment on July 29 was actually found
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
                                                "value": "Dentist Appointment",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T13:00:00-07:00",
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
                # Milestone 2 – The calendar event has been rescheduled (stateful change)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dentist Appointment",
                                    "start_datetime_iso": "2024-07-30T13:00:00-07:00",
                                    "end_datetime_iso": "2024-07-30T14:00:00-07:00",
                                    "attendees_names": [["Theo Appleseed"]],
                                    "creation_datetime_iso": "2024-07-29T08:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
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
            milestone_edge_list=[
                (0, 1),  # Found the event after searching
                (1, 2),  # Rescheduled after confirming the correct event
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_23_0ab0b2a3-ed88-4a3e-99ea-38bb00941a27_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_23",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T08:20:00-07:00",
            is_read_time="2024-07-29T08:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to cancel your dentist appointment event and schedule a 1:1 with Kevin there instead from 1:00 pm - 2:00 pm with him as an invitee. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my Dentist Appointment event and replace it with a new event called 1:1 with Kevin.",
                },
            ],
            reasoning="The user wants to delete Dentist Appointment. I'll first find it in their calendar. Ok, I found the Dentist Appointment today scheduled at 1:00-2:00pm. I will delete it. And next, user wants to schedule a 1:1 with Kevin from 1:00pm - 2:00pm. I need to figure out which Kevin, so I searched the contact and find Kevin Chen as the mananger. I've created it with Kevin Chen as an attendee. I'll inform user that I've deleted the event and replaced it with 1:1 with Kevin as user has instructed. ",
            success_conditions=[
                {
                    "input_text": "1. The Dentist appointment calendar event Is deleted.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. A new calendar event titled "1:1 with Kevin" is created for 1:00pm - 2:00 pm with Kevin Chen as an invitee.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
                "create_calendar_event",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looks through the calendar to locate the Dentist appointment
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
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
                # Milestone 1 – Confirm the Dentist Appointment surfaced in the tool output from Milestone 0
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
                                                "value": "Dentist Appointment",
                                                "partial": False,
                                            },
                                            # Start time check is optional but adds confidence
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T13:00:00-07:00",
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
                # Milestone 2 – Dentist Appointment is removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dentist Appointment",
                                    "start_datetime_iso": "2024-07-29T13:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T14:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ]
                ),
                # Milestone 3 – New 1:1 with Kevin Chen is created for the same time slot
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "1:1 with Kevin",
                                    "start_datetime_iso": "2024-07-29T13:00:00-07:00",
                                    "end_datetime_iso": "2024-07-29T14:00:00-07:00",
                                    "attendees_names": [["Kevin Chen"]],
                                    "creation_datetime_iso": "2024-07-29T08:20:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # Require at least Kevin in attendees; allow extras (e.g., Theo)
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox chatter when checking calendar diff
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # calendar search → confirmation of Dentist appointment found
            ],
        ),
    ]
