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
    snapshot_similarity,
    tool_trace_dependant_similarity,
    update_similarity,
)
from astra_tool_sandbox.common.execution_context import DatabaseNamespace, RoleType
from astra_tool_sandbox.common.scenario import Scenario, ScenarioExtension
from astra_tool_sandbox.common.tool_trace_extractors import (
    ToolTraceExtractorType,
    result_list_match_count_extractor,
    result_list_match_existence_extractor,
)
from astra_tool_sandbox.scenarios.astra_v1.protagonist_simulator_few_shot_examples import (
    USER_INSTRUCTION_SINGLE_TURN,
)


def get_TAG_DAWEI_SHEN_pilot_plot_15(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="DAWEI_SHEN_15_8c8cf0eb-7645-43d5-87d8-c547104740ec_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T10:00:00-08:00",
            is_read_time="2024-12-12T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to ask Theo if he has any feedback on the recorded Tech Panel session. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send an e-mail to Theo Appleseed asking if he has any feedback on the recorded Tech Panel session",
                },
            ],
            reasoning='The user wants me to send an email to Theo Appleseed asking if he has any feedback on the recorded Tech Panel session, so I will look through the user\'s contacts to find Theo Appleseed. After retrieving his address, I will compose and send the message with the subject like "Feedback on the Recorded Tech Panel Session", asking for any feedback on the recorded Tech Panel session.',
            success_conditions=[
                {
                    "input_text": 'An e-mail is sent to theo.appleseed@orchardtech.com with the subject like "Feedback on the Recorded Tech Panel Session", asking if he has any feedback on the recorded Tech Panel session.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "add_contact",
                "get_all_contacts",
                "search_contacts",
                "send_email",
            ],
            milestones=[
                Milestone(
                    snapshot_constraints=[
                        # Agent uses a contact search tool to retrieve Theo's contact
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
                Milestone(
                    snapshot_constraints=[
                        # Verify that Theo Appleseed's contact is among the results
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
                                                "value": "Theo Appleseed",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "theo.appleseed@orchardtech.com",
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
                # Agent send email to Theo - only with structured critical fields
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
                                                "recipients_addresses": [
                                                    "theo.appleseed@orchardtech.com"
                                                ],
                                                "email_action": "send",
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
                # Agent send email to Theo - only with structured critical fields
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["theo.appleseed@orchardtech.com"]
                                    ],  # List of recipients_addresses
                                    "subject": "Feedback on the Recorded Tech Panel Session",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-12T10:00:00-08:00",
                                },
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_15_18b5db6d-5444-4d93-925a-628189096205_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T11:10:00-08:00",
            is_read_time="2024-12-10T11:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to check how long until your next meeting as you want to bring Jeff out to lunch to celebrate his achievement of hosting a tech panel. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How long until my next meeting today with Michelle? Replies in 'X hours and XX minutes' format.",
                },
            ],
            reasoning="The user wants to know how long until their next meeting today with Michelle. I'll check their calendar and find out when's their next meeting with Michelle. Ok, I find the meeint user refers to 'Dataset Review with Michelle' starting at 14:00. From the current time of 11:10, the difference is 2 hours and 50 minutes, so I'll inform user the gap in their requested format: “2 hours and 50 minutes.”",
            success_conditions=[
                {
                    "input_text": "The assistant replies with \"2 hours and 50 minutes\" to indicate the time remaining until the 'Dataset Review with Michelle' meeting at 14:00 today.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "create_calendar_event",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                Milestone(
                    snapshot_constraints=[
                        # 1. Tool usage to search calendar events
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
                Milestone(
                    snapshot_constraints=[
                        # 2. Ensure calendar event with 'Dataset Review with Michelle' at 14:00 on Dec 10 is retrieved
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
                                                "value": "Dataset Review with Michelle",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-10T14:00:00-08:00",
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
                Milestone(
                    snapshot_constraints=[
                        # 3. User-facing response includes reference to time until 2pm event with Michelle
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "2 hours and 50 minutes",
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
            name="DAWEI_SHEN_15_18b5db6d-5444-4d93-925a-628189096205_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "email",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T11:10:00-08:00",
            is_read_time="2024-12-10T11:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to check how long until your next meeting as you want to bring Jeff out to lunch to celebrate his achievement of hosting a tech panel. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How much time do I have until my next event with the person who emailed me yesterday? Replies in 'X hours and XX minutes' format.",
                },
            ],
            reasoning="Right so the user wants to know how much time is left until the next event today with the person who emailed them yesterday.\n\nI need to find out who emailed them yesterday so I check their emails and see the latest is from Michelle Barnes received on the 9th December at 8:00, subject Dataset Update for Machine Learning Model.\n\nNow that I know who is the person for the event they have with, I will check their calendar and find the event scheduled with Michelle. I can see the next event is named 'Dataset Review with Michelle'. It is scheduled for 10th December at 14:00 with Michelle Barnes as an invitee. \n\nThe current time is 10th December 11:10. Therefore the time remaining until 14:00 is 2 hours and 50 minutes. I will respond user with exactly \"2 hours and 50 minutes\" in the requested format.",
            success_conditions=[
                {
                    "input_text": "The assistant replies with '2 hours and 50 minutes'.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                Milestone(
                    snapshot_constraints=[
                        # 0. Tool usage to search emails
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
                                    target_tools=["get_all_emails", "search_emails"],
                                )
                            },
                        )
                    ]
                ),
                Milestone(
                    snapshot_constraints=[
                        # 1. Ensure email from Michelle Found
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
                                                "value": "Dataset Update for Machine Learning Model",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "michelle.barnes@orchardtech.com",
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
                Milestone(
                    snapshot_constraints=[
                        # 2. Tool usage to search calendar events
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
                Milestone(
                    snapshot_constraints=[
                        # 3. Ensure calendar event with 'Dataset Review with Michelle' at 14:00 on Dec 10 is retrieved
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
                                                "value": "Dataset Review with Michelle",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-10T14:00:00-08:00",
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
                Milestone(
                    snapshot_constraints=[
                        # 4. User-facing response includes reference to time until 2pm event with Michelle
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "2 hours and 50 minutes",
                                            "two hours and fifty minutes",
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
                (0, 1),  # find the emails
                (2, 3),  # find the calendar evnets
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_15_8c8cf0eb-7645-43d5-87d8-c547104740ec_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T10:00:00-08:00",
            is_read_time="2024-12-12T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to ask your coworker who suggested the extra improvement to the user-interaction section in the email threads earlier, if he has any feedback on the recording you sent him. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Email my coworker—the one who suggested the extra improvement to the user interaction section—and ask if he’s had a chance to look at the link I sent.",
                },
            ],
            reasoning="The user wants me to email the co-worker who suggested the extra improvement to the user-interaction section. I’ll search email and find out email thread that matches with this description. Ok, I found the email titled Re: Revised Draft for Virtual Assistant Algorithm recieved on 02/12/2024, 09:15:00 that matches with the content user mentioned. The email was from Theo Appleseed. I understand user wants to email Theo. I'll look up Theo's contact card and find his email address. Now I'll send him the email saying something like \"Have you had a chance to look at the recording I sent. Any feedback on the Recorded Tech Panel Session?\" Finally, I’ll inform user that the email has been sent to Theo.",
            success_conditions=[
                {
                    "input_text": 'An e-mail is sent to theo.appleseed@orchardtech.com asking if he has any feedback on the recorded Tech Panel session saying something like "Have you had a chance to look at the recording I sent. Any feedback on the Recorded Tech Panel Session?".',
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
                # 0. Agent search emails trying to find who the co-worker is
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
                # 1. found the email sent by theo
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
                                                "value": "theo.appleseed@orchardtech.com",
                                                "partial": False,
                                            },
                                            "body": {
                                                "value": "adding an additional improvement to the section on user interaction",
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
                # 2. Agent send email to Theo - only with structured critical fields
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
                                                "recipients_addresses": [
                                                    "theo.appleseed@orchardtech.com"
                                                ],
                                                "email_action": "send",
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
                # 3. Agent send email to Theo - only with structured critical fields
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["theo.appleseed@orchardtech.com"]
                                    ],  # List of recipients_addresses
                                    # "subject": "Feedback on the Recorded Tech Panel Session",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-12T10:00:00-08:00",
                                },
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # find the emails to figure out who the co-worker is
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_15_10e8bd71-55aa-4d17-93d9-e4f1b8d51b47_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "calendar",
                "email",
                "contact",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
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
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to schedule a time on Saturday half an hour later after dinner to re-watch the full length of the Tech Panel you attended this week. Thankfully Jeff emailed a link of the recording to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Block off time to watch that link with full length on Saturday night, oh I need half an hour to get home. ",
                },
            ],
            reasoning="The user wants to block off time to watch a link on Saturday night, and they mentioned needing half an hour to get home first.\n\nOkay, so first I need to figure out which link the user is referring to. I’ll check both Messages and Mail for any recently received links. There are no links in Messages, but I do see several in Mail. Only one of them is a recording, so that must be the link the user means.\n\nNext, I’ll check the user’s calendar for Saturday to find when they’re free. I see a dinner event scheduled from 19:00 to 21:00. Since the user said they need half an hour to get home, I’ll plan the new event to start at 21:30 so they have travel time.\n\nThe user said they want to watch the link 'with full length,' which means I should schedule enough time to cover the entire recording. The recording is of the 'Tech Panel Hosted by Jeff Bing' event, which lasted around two hours, so I’ll set the duration to match that.\n\nI’ll now create the calendar event 'Watch the Recording' for Saturday, 14 December 2024, from 21:30 to 23:30.",
            success_conditions=[
                {
                    "input_text": '1. An event with name including keywords "recording" is created on 14 December 2024 from 21:30-23:30.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up emails to find the recording link from Jeff (or the recording email)
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
                # Milestone 1 – Confirm the Tech Panel recording email from Jeff was retrieved
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
                                                "value": "Thank You for Attending the Tech Panel",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "jeff.bing@bingelectronics.com",
                                                "partial": False,
                                            },
                                            # Just confirming attachment presence in general via partial match on name
                                            "attachments": {
                                                "value": "Tech_Panel_Recording_2024-12-10.mp4",
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
                # Milestone 2 – Agent inspects calendar to align with Saturday dinner and free time
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
                                    # Can either list all or search specifically;
                                    # both are acceptable paths to check Saturday schedule
                                    target_tools=[
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 3 – Verify the Saturday dinner event is known (to infer post-dinner time)
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
                                            "end_datetime_iso": {
                                                "value": "2024-12-14T21:00:00-08:00",
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
                # Milestone 4 – A new calendar event is created on Saturday night for watching the recording
                # from 21:30 to 23:30, with "recording" in the event name.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Only check the critical fields tied to success conditions
                                    "calendar_event_name": "recording",
                                    "start_datetime_iso": "2024-12-14T21:30:00-08:00",
                                    "end_datetime_iso": "2024-12-14T23:30:00-08:00",
                                    "creation_datetime_iso": "2024-12-10T12:10:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Name must contain "recording" (case-insensitive)
                                "calendar_event_name": column_contains_similarity,
                                # Start and end must match the expected time;
                                # use close similarity to allow minor formatting differences if any
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
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Email lookup → confirm recording email
                (2, 3),  # Calendar lookup → confirm dinner timing
                # Event creation (Milestone 4) is a leaf that logically depends on both
                (1, 4),
                (3, 4),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_15_ea914e78-1d97-4066-a7e4-03c575056d01_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "contact",
                "messaging",
                "calendar",
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
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to send your girlfriend a text message as you're finished at the Tech Panel event and then you want to call her. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text Jess that I just finished the event, and letting her know what that event is, and see if she's available to chat.",
                },
            ],
            reasoning='First, identify the correct Jess contact (Jess Zimmer, the girlfriend). Next, look up the calendar to confirm the event that has just ended: "Tech Panel Hosted by Jeff Bing". Compose a text to Jess that says you’ve just finished the Tech Panel and asks if she’s available to chat, then send it.',
            success_conditions=[
                {
                    "input_text": "A text message is sent to Jess Zimmer saying the user just finished the Tech Panel and asking if she's available to chat.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_message",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0: Search contacts or retrieve all to identify Jess
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
                # Milestone 1: Contact result includes Jess Zimmer
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
                                                "value": "Jess Zimmer",
                                                "partial": False,
                                            },
                                            "relationship": {
                                                "value": "Girlfriend",
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
                # 2. Search for the events that just finished
                Milestone(
                    snapshot_constraints=[
                        # 1. Tool usage to search calendar events
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
                # 3. Ensure calendar event with 'Dataset Review with Michelle' at 14:00 on Dec 10 is retrieved
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
                                                "value": "Tech Panel Hosted by Jeff Bing",
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
                # Milestone 4: Agent sends message to Jess including Tech Panel
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Jess Zimmer",
                                    "content": "tech panel",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-10T12:05:00-08:00",
                                },
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (2, 3)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_15_24bc17b1-020a-4a66-be88-d4041dbc6187_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
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
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to remember when you sent the picture of Paul's cat to him when you are eating lunch with colleagues to show them the picture. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When did I send Paul Harper a text message with the picture of his cat napping by the window?",
                },
            ],
            reasoning="Okay so the user wants me to find out when they sent a message to Paul Harper. The message is about Paul's cat napping by the window so I'll look for mentions of that in the messages. The message I'm looking for has an image attached of the cat napping by the window. I found one message mentioning this. It was sent at 19:02 on December 9th 2024. I'll relay that information to the user.",
            success_conditions=[
                {
                    "input_text": "1. The date and time that the image of Paul's cat napping is given to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # 0. Search for messages
                Milestone(
                    snapshot_constraints=[
                        # 0. Tool usage to access messages
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
                                        "get_all_messages",
                                        "search_messages",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # 1. Message data extracted correctly (about Paul's cat photo on Dec 9, 2024, 19:02 PST)
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
                                            "creation_datetime_iso": {
                                                "value": "2024-12-09T19:02:00-08:00",
                                                "partial": False,
                                            },
                                            "conversation_name": {
                                                "value": "Paul Harper",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "No worries, Paul! It was my pleasure. Check out this funny photo of your cat napping by the window.",
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
                # 2. User Facing response
                Milestone(
                    snapshot_constraints=[
                        # Agent response to user with time that photo was sent, using time here for more loose match
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("7:02", "19:02")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_15_24bc17b1-020a-4a66-be88-d4041dbc6187_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "contact",
                "messaging",
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
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to remember when you sent the picture of Paul's cat to him when you are eating lunch with colleagues to show them the picture. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When did I send the picture of my neighbor's pet sleeping by the window to him? Pull that message up.",
                },
            ],
            reasoning="Okay so the user wants me to find out when they sent a message to their neighbor. So firstly I'll try to figure out who the users neighbor is. Looking through their contacts I only found one person,  Paul Harper, with the label of neighbor.\nI'll continue under the assumption that the users is talking about Paul Harper.\nThe message is about Paul's pet so I'll look for mentions of that in the messages. I see messages mentioning a cat so I think that this is Paul's pet. The message I'm looking for has an image attached of the cat sleeping by the window. I found one message mentioning this. It was sent at 19:02 on December 9th 2024. I'll relay that information to the user.",
            success_conditions=[
                {
                    "input_text": "1. The date and time that the image of Paul's cat napping is given to the user.",
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
                # 0. Search Contact to find Paul Harper is the neighbour
                Milestone(
                    snapshot_constraints=[
                        # Verify that who is my neighbour
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
                # 1. search results contain Harper
                Milestone(
                    snapshot_constraints=[
                        # Verify Paul's contact has been found
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
                                                "value": "Paul Harper",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 555-678-9012-3456",
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
                # 2. search messages
                Milestone(
                    snapshot_constraints=[
                        # Tool usage to access messages
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
                                        "get_all_messages",
                                        "search_messages",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # 3. correct message included in the searching function
                Milestone(
                    snapshot_constraints=[
                        # Message data extracted correctly (about Paul's cat photo on Dec 9, 2024, 19:02 PST)
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
                                            "creation_datetime_iso": {
                                                "value": "2024-12-09T19:02:00-08:00",
                                                "partial": False,
                                            },
                                            "conversation_name": {
                                                "value": "Paul Harper",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "No worries, Paul! It was my pleasure. Check out this funny photo of your cat napping by the window.",
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
                # 4. User facing responses contains the message with time
                Milestone(
                    snapshot_constraints=[
                        # Agent response to user with date/time that photo was sent
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("7:02", "19:02")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (2, 3)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_15_ea914e78-1d97-4066-a7e4-03c575056d01_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "calendar",
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
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to send your girlfriend a text message as you're finished at the Tech Panel event and then you want ask her if she is available for a call. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send my girlfriend a text that I am done at the event, mentioning the event directly, and check if she is available for a call.",
                },
            ],
            reasoning="First, search the user’s contacts to confirm that the girlfriend is Jess Zimmer. Then draft a text to Jess that says the user is done at the Tech Panel event and asks if she is available for a call. Once the user approves, send the text to Jess.",
            success_conditions=[
                {
                    "input_text": "A text message is sent to Jess Zimmer saying the user is done at the Tech Panel event and asking if she is available for a call.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_message",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0: Search contacts or retrieve all to identify Jess
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
                # Milestone 1: Contact result includes Jess Zimmer
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
                                                "value": "Jess Zimmer",
                                                "partial": False,
                                            },
                                            "relationship": {
                                                "value": "Girlfriend",
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
                # Milestone 2: Agent sends message to Jess including Tech Panel
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Jess Zimmer",
                                    "content": "tech panel",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-10T12:05:00-08:00",
                                },
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Jess Zimmer",
                                    "content": [("call", "chat")],
                                    "creation_datetime_iso": "2024-12-10T12:05:00-08:00",
                                },
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_15_10e8bd71-55aa-4d17-93d9-e4f1b8d51b47_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "calendar",
                "email",
                "contact",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
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
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to schedule a time on Saturday half an hour later after dinner to re-watch the full length of the Tech Panel you attended this week. Thankfully Jeff emailed a link of the recording to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Make time to re-watch Jeff's recording from beginning to end on Saturday, starting once I'm home from dinner — it takes me about 30 minutes to get home.",
                },
            ],
            reasoning="The user wants to re-watch Jeff’s recording on Saturday night, starting right after they get home from dinner. They also said 'from beginning to end' and that it takes them about 30 minutes to get home.\n\nFirst, I’ll find the relevant dinner on Saturday. I see 'Dinner with Lukas and Vick' ending at 21:00. Since the user said they need time to get home, I’ll add a 30-minute buffer and plan the new event to start at 21:30.\n\nNext, I’ll identify the recording. There’s one Jeff in contacts (Jeff Bing). In email, I see a link from jeff.bing@bingelectronics.com to a 'Tech Panel' recording. That’s the likely target.\n\nDuration logic: because the user said 'from the beginning to the end,' I should schedule the full runtime if known. The source event 'Tech Panel Hosted by Jeff Bing' lasted ~2 hours, so I’ll set the event length to 2 hours. \n\nI’ll create a calendar event titled 'Re-watch Jeff’s recording' on Saturday from 21:30–23:30 and present it for confirmation.",
            success_conditions=[
                {
                    "input_text": '1. An event with name including keywords "recording" is created on 14 December 2024 from 21:30-23:30.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – (Optional but likely) calendar search used to understand Saturday dinner timing
                # The agent may look up existing calendar events to know when dinner ends on Saturday.
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
                                    # Either search a specific day/event or just list calendars
                                    target_tools=[
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – The specific event was surfaced
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
                                        result_list_match_count_extractor,
                                        count_expected=2,
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
                        )
                    ]
                ),
                # Milestone 0 – the agent looks up the calendar to find the event
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
                # Milestone 1 – the calendar lookup returns the correct Tech Panel event
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
                                                "value": "Tech Panel Hosted by Jeff Bing",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-10T09:00:00-08:00",
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
                            reference_milestone_node_index=2,  # depends on the tool call in milestone 0
                        )
                    ],
                ),
                # Milestone 1 – New calendar event created for re-watching the recording on 2024-12-14 from 21:30–23:30
                # This is the main success condition.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Event name must reference "recording" somewhere
                                    "calendar_event_name": "recording",
                                    "start_datetime_iso": "2024-12-14T21:30:00-08:00",
                                    "end_datetime_iso": "2024-12-14T23:30:00-08:00",
                                    "creation_datetime_iso": "2024-12-10T12:10:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Only require that "recording" appears as a substring in the title
                                "calendar_event_name": column_contains_similarity,
                                # Times should match exactly for this task
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                # Calendar lookup (0) may inform the scheduling (1), but creation can be validated independently.
                (0, 1),
                (2, 3),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_15_7fea2d6e-9fd3-4b1c-88f6-7b9cb416cf22_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "calendar",
                "email",
                "contact",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
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
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to send the link of the recorded session you received from Jeff to all your team members before the review meeting. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to send out that link I got earlier for a recording to my team before the review meeting. ",
                },
            ],
            reasoning='User wants a link from earlier about a recording. Checking messages, I see user received email from Jeff Bing earlier containing a link to a recorded meeting session, email titled "Thank You for Attending the Tech Panel" with link in the attachments "Tech_Panel_Recording_2024-12-10.mp4". User wants to send link to his team.  I see a calendar event called "Team Review Meeting": its invitees are the user, a Michelle Barnes, and one Kevin Chen. I will then look for their contacts for the emails. I will show user link ready to be sent via email and ask if user wants to send. ',
            success_conditions=[
                {
                    "input_text": "1. The email with link to the recorded session from Jeff is found.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": '2. The email with the recording link is attached is sent to the team members "michelle.barnes@orchardtech.com" and "kevin.chen@orchardtech.com" sent. ',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "send_email",
                "search_calendar_events",
                "get_all_calendars",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looks up previous email(s) to find the recording/link from Jeff
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
                # Milestone 1 – Confirms that the email from Jeff with the recording was found
                # (subject & sender identify it; this validates retrieval of the recording source)
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
                                                "value": "Thank You for Attending the Tech Panel",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "jeff.bing@bingelectronics.com",
                                                "partial": False,
                                            },
                                            # We don't know the exact link, but verifying attachment existence shows it's the recording email
                                            "attachments": {
                                                "value": "Tech_Panel_Recording_2024-12-10.mp4",
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
                # Milestone 2 – Email with the recording (or its link/attachment) is sent to team members Kevin & Michelle
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Must be sent to exactly Kevin and Michelle
                                    "recipients_addresses": [
                                        [
                                            "michelle.barnes@orchardtech.com",
                                            "kevin.chen@orchardtech.com",
                                        ]
                                    ],
                                    "status": "sent",
                                    # Body should mention recording or link; we don't enforce exact phrasing
                                    "body": "record",
                                    "creation_datetime_iso": "2024-12-10T12:15:00-08:00",
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
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                    ],
                ),
            ],
            milestone_edge_list=[
                (
                    0,
                    1,
                ),  # find Jeff's recording email → confirm it was correctly identified
                (1, 2),  # after finding the correct email, send recording to team
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_15_1268ef52-c6f7-4f36-a105-619608214ff1_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_moderate",
                "contact",
                "email",
                "calendar",
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
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You will need to message Jeff inviting him and create a new event in your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Email Jeff Bing saying "And another thing, how would you like to go for lunch tomorrow at 13:00?" and create a lunch event.',
                },
            ],
            reasoning="First, I need to email Jeff Bing. The user wants to say \"And another thing, how would you like to go for lunch tomorrow at 13:00?\". There's only one Jeff Bing in the contacts so there's no issue there.\n\nNow the user wants to create a lunch event. They haven't explicitly said but I presume they are referring to the lunch mentioned in the email to Jeff Bing. I'll go ahead and create an event at the time specified and call it 'Lunch with Jeff Bing'.",
            success_conditions=[
                {
                    "input_text": '1. Send an email to jeff.bing@bingelectronics.com saying "And another thing, how would you like to go for lunch tomorrow at 13:00?".',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. Create a calendar event called 'Lunch with Jeff Bing' for 13:00 December 11th 2024.",
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
                "send_email",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 & 1: Verify that Jeff Bing's email is found
                Milestone(
                    snapshot_constraints=[
                        # Agent uses a contact search tool to retrieve Theo's contact
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
                Milestone(
                    snapshot_constraints=[
                        # Verify that Jeff Bing's contact is among the results
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
                                            "email": {
                                                "value": "jeff.bing@bingelectronics.com",
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
                # Milestone 2: Verify that email sent includes correct content and recipient
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["jeff.bing@bingelectronics.com"]
                                    ],
                                    "body": "And another thing, how would you like to go for lunch tomorrow at 13:00?",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-10T11:05:00-08:00",
                                },
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR
                    ],  # exclude CALENDAR additions
                ),
                # Milestone 3: Verify calendar event details
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Lunch with Jeff Bing",
                                    "start_datetime_iso": "2024-12-11T13:00:00-08:00",
                                    "creation_datetime_iso": "2024-12-10T11:05:00-08:00",
                                },
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL
                    ],  # exclude EMAIL additions
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_15_088f1173-9a5c-4cb0-8513-604c192a512c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "calendar",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T12:30:00-08:00",
            is_read_time="2024-12-10T12:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "Now that you have read the email from Jeff and replied, you want to reach out again to invite him to the Dataset Review with Michelle today. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Email him again \"Thanks again for your email Jeff. I'd actually like to invite you to a Data set review I'm having with my colleague Michelle Barnes today at 14:00.\" and add him to the Dataset Review with Michelle later.",
                },
            ],
            reasoning="So the user wants to reply to someone they emailed before. Based on the content they want to include in the email mentioning Jeff, I'll assume they want to reply again to the recent email received from jeff.bing@bingelectronics.com after their initial reply they sent at 12:00. They want to say \"Thanks again for your email Jeff. I'd actually like to invite you to a Data set review I'm having with my colleague Michelle Barnes today at 14:00.\". so I'll craft that as the reply and send it to Jeff. I'll also add him as an invitee to the Dataset Review with Michelle at 14:00-15:00 today.",
            success_conditions=[
                {
                    "input_text": "1. An email is sent to jeff.bing@bingelectronics.com to say \"Thanks again for your email Jeff. I'd actually like to invite you to a Data set review I'm having with my colleague Michelle Barnes today at 14:00.\".",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. Jeff Bing is added as an invitee to the event named "Dataset Review with Michelle" at 14:00-15:30 on 10 December 2024.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "send_email",
                "get_all_calendars",
                "search_calendar_events",
                "modify_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Ensure the agent used an email-related retrieval tool (optional but plausible to reference prior thread)
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
                # Milestone 1 – Verify an email to Jeff was sent with the specified body text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["jeff.bing@bingelectronics.com"]
                                    ],
                                    "status": "sent",
                                    "body": "Thanks again for your email Jeff. I'd actually like to invite you to a Data set review I'm having with my colleague Michelle Barnes today at 14:00.",
                                    "creation_datetime_iso": "2024-12-10T12:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                # Require that the exact requested sentence appears in the body
                                "body": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
                # Milestone 2 – Ensure the agent looked up calendar information (to find/confirm the Dataset Review with Michelle event)
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
                # Milestone 3 – Verify that the existing "Dataset Review with Michelle" event was updated to include Jeff as an attendee
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dataset Review with Michelle",
                                    "start_datetime_iso": "2024-12-10T14:00:00-08:00",
                                    "end_datetime_iso": "2024-12-10T15:30:00-08:00",
                                    # Attendees must at least include Dawei, Michelle, and Jeff; extras allowed
                                    "attendees_names": [
                                        [
                                            "Dawei Shen",
                                            "Michelle Barnes",
                                            "Jeff Bing",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-10T12:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
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
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Email retrieval → sending the new email to Jeff
                (2, 3),  # Calendar lookup → updating the event to add Jeff
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_15_088f1173-9a5c-4cb0-8513-604c192a512c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "calendar",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T12:30:00-08:00",
            is_read_time="2024-12-10T12:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "Now that you have read the email from Jeff and replied, you want to reach out again to invite him to the Dataset Review with Michelle today. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to Jeff Bing's email again and say \"Thanks again for your email Jeff. I'd actually like to invite you to a Data set review I'm having with my colleague Michelle Barnes today at 14:00.\" then invite him to my meeting later today.",
                },
            ],
            reasoning="The user wants to reply again to the recent email received from jeff.bing@bingelectronics.com after their initial reply they sent at 12:00. They want to say \"Thanks again for your email Jeff. I'd actually like to invite you to a Data set review I'm having with my colleague Michelle Barnes today at 14:00.\". so I'll craft that as the reply and send it to Jeff. \nNow, the user wants to add him as an invitee to a meeting they're having later today. Today is December 10th, and it's already 12:30, so I'll see what other meetings are happening today after this point. I see Dataset Review with Michelle at 14:00-15:00, so I'll add Jeff as an invitee to that.",
            success_conditions=[
                {
                    "input_text": "1. An email is sent to jeff.bing@bingelectronics.com to say \"Thanks again for your email Jeff. I'd actually like to invite you to a Data set review I'm having with my colleague Michelle Barnes today at 14:00.\".",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. Jeff Bing is added as an invitee to the event named "Dataset Review with Michelle" at 14:00-15:30 on 10 December 2024.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "send_email",
                "get_all_calendars",
                "search_calendar_events",
                "modify_calendar_event",
                "create_calendar_event",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent reads/searches the relevant email thread with Jeff
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
                # Milestone 1 – Confirm Jeff's "Thank You for Attending the Tech Panel" email was retrieved
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
                                                "value": "Thank You for Attending the Tech Panel",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "jeff.bing@bingelectronics.com",
                                                "partial": False,
                                            },
                                            "recipients_addresses": {
                                                "value": ["dawei.shen@orchardtech.com"],
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
                # Milestone 2 – Email is sent to Jeff with the specified body (replying again)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["jeff.bing@bingelectronics.com"]
                                    ],
                                    "status": "sent",
                                    "body": "Thanks again for your email Jeff. I'd actually like to invite you to a Data set review I'm having with my colleague Michelle Barnes today at 14:00.",
                                    "creation_datetime_iso": "2024-12-10T12:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                # Require the key phrase to appear; allow extra polite text if the agent adds any
                                "body": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
                # Milestone 3 – The agent looks up today's calendar events (to find "Dataset Review with Michelle")
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
                # Milestone 4 – Confirm the "Dataset Review with Michelle" event at 14:00 was retrieved
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
                                                "value": "Dataset Review with Michelle",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-10T14:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-10T15:30:00-08:00",
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
                            reference_milestone_node_index=3,
                        )
                    ]
                ),
                # Milestone 5 – Jeff is added as an attendee to the "Dataset Review with Michelle" event via update_similarity
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dataset Review with Michelle",
                                    "start_datetime_iso": "2024-12-10T14:00:00-08:00",
                                    "end_datetime_iso": "2024-12-10T15:30:00-08:00",
                                    "attendees_names": [
                                        ["Dawei Shen", "Michelle Barnes", "Jeff Bing"]
                                    ],
                                    "creation_datetime_iso": "2024-12-10T12:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Ensure at least these attendees are included; allow extras if the agent invites others
                                "attendees_names": column_list_subset_match_similarity,
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
                (0, 1),  # Email search → confirm Jeff's email
                (1, 2),  # Having found Jeff's email, send reply/invitation email
                (3, 4),  # Calendar search → confirm target event
                (4, 5),  # After confirming event, update attendees to include Jeff
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_15_1268ef52-c6f7-4f36-a105-619608214ff1_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_high",
                "contact",
                "email",
                "calendar",
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
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You will need to email Jeff inviting him and create a new event in your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Also another thing for Jeff, say "And another thing, how would you like to go for lunch tomorrow at 13:00?" by email. And calendar that.',
                },
            ],
            reasoning="Firstly, the user seems to want to message someone called Jeff. The user has recently emailed Jeff Bing and by the way they say 'and another thing for Jeff', I think I can safely assume that they are emailing him again. A scan of the user's contacts confirms that there is only one Jeff in their contacts so it must be Jeff Bing.\n\nWhen the user say 'calendar that', they must mean the aforementioned lunch plan with Jeff Bing. I'll create an event for 13:00 December 11th 2024 called 'Lunch with Jeff Bing'.",
            success_conditions=[
                {
                    "input_text": '1. Send an email to jeff.bing@bingelectronics.com saying "And another thing, how would you like to go for lunch tomorrow at 13:00?".',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. Create a calendar event called 'Lunch with Jeff Bing' for 13:00 December 11th 2024.",
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
                "send_email",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 & 1: Verify that Jeff Bing's email is found
                Milestone(
                    snapshot_constraints=[
                        # Agent uses a contact search tool to retrieve Theo's contact
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
                Milestone(
                    snapshot_constraints=[
                        # Verify that Jeff Bing's contact is among the results
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
                                            "email": {
                                                "value": "jeff.bing@bingelectronics.com",
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
                # Milestone 2: Verify that email sent includes correct content and recipient
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["jeff.bing@bingelectronics.com"]
                                    ],
                                    "body": "And another thing, how would you like to go for lunch tomorrow at 13:00?",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-10T11:05:00-08:00",
                                },
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR
                    ],  # exclude CALENDAR additions
                ),
                # Milestone 3: Verify calendar event details
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Lunch with Jeff Bing",
                                    "start_datetime_iso": "2024-12-11T13:00:00-08:00",
                                    "creation_datetime_iso": "2024-12-10T11:05:00-08:00",
                                },
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL
                    ],  # exclude EMAIL additions
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
    ]
