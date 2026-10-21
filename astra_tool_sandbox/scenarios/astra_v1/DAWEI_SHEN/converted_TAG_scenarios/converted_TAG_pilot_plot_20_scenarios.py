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
    column_list_tuple_contains_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_tool_trace_partial_arguments_similarity,
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


def get_TAG_DAWEI_SHEN_pilot_plot_20(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="DAWEI_SHEN_20_23ea1efb-1405-4387-853a-a8bee00192be_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_20",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "contact",
                "calendar",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-15T10:00:00-08:00",
            is_read_time="2024-12-15T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to set up a meeting on Monday at 9:00 to see how the folks are getting on with their action items from the review meeting, you have sent emails about action items last Friday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set up a meeting to see how the guys are getting on with their action items from the team review meeting tomorrow at 9.",
                },
            ],
            reasoning='The user wants to set up a meeting with the guys to check how they are getting on with their action items, first I will find out when the user wants this meeting to be held.\nThe user has confirmed a date and time for the meeting, now I need to find out who he is referring to as the guys. I have found emails from the user addressed to Michelle Barnes and Kevin Chen with the title "Action Items", I will assume these are the people the user is referencing in his query.\nI will now create a calendar event titled Team Meeting at 9:00 on Monday December 16 2024 with Dawei Shen, Michelle Barnes and Kevin Chen.',
            success_conditions=[
                {
                    "input_text": "A calendar event is created for 9:00 AM on Monday, December 16, 2024 with attendees Dawei Shen, Michelle Barnes, and Kevin Chen.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "create_calendar_event",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0: search for emails
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
                # M1: Action items found from email
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
                                                "value": "2024-12-13",
                                                "partial": True,
                                            },
                                            "subject": {
                                                "value": "Action Items from Team Review",
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
                # Milestone 2 – A calendar event reflecting the user’s request is added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "start_datetime_iso": "2024-12-16T09:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "Dawei Shen",
                                            "Michelle Barnes",
                                            "Kevin Chen",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-15T10:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,
                                "attendees_names": column_list_exact_match_similarity,
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
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_20_3c62508a-42c3-466d-b3b2-a57011a1f738_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_20",
                "email",
                "contact",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T18:00:00-08:00",
            is_read_time="2024-12-13T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "After your meeting you sent out assignments to your coworkers. You want to know if either of them has replied to your email yet. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Have my coworkers replied to the action items I sent?\n",
                },
            ],
            reasoning="The user wants to know if they have gotten replies from their coworkers.\nFirst I should determine who they mean by coworkers. By checking user's contacts I see Dawei has 4 coworkers. \nThe user has specified that they are looking for replies to action items, I should determine what this means.\nIn the user's inbox I can see two email threads with the subject line Action Items from Team Review, I can assume that this is what the user is referring to.\nThese thread were sent out to Kevin Chen and Michelle Barnes, who are user's coworkers.\nNow that I know specifically which emails they are looking at, I can go ahead and check if the user has received a reply from them.\nI see one reply from Michelle Barnes received today at 10:15. I do not see any replies from Kevin Chen. I will inform user about this.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Inbox is checked for replies from Michelle Barnes.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. Inbox is checked for replies from Kevin Chen.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent checks emails for replies (via search or list)
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
                # Milestone 1 – Confirms that the reply from Michelle exists in email data
                # (Re: Action Items from Team Review from michelle.barnes@orchardtech.com)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            # Validate that the previous email retrieval actually surfaced Michelle's reply
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "subject": {
                                                "value": "Re: Action Items from Team Review",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "michelle.barnes@orchardtech.com",
                                                "partial": False,
                                            },
                                            "recipients_addresses": {
                                                "value": ["dawei.shen@orchardtech.com"],
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
                # Milestone 2 – Agent informs user correctly about replies status:
                # Michelle replied, Kevin has not replied yet.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Content must mention that Michelle has replied AND Kevin has not (or similar).
                                    "content": [
                                        (
                                            "Michelle",
                                            "repl",
                                            "Kevin",
                                            "not",
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
                (0, 1),  # email search/list → confirming Michelle's reply exists
                (0, 2),  # email search/list → user-facing summary
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_20_3c62508a-42c3-466d-b3b2-a57011a1f738_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_20",
                "email",
                "contact",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T18:00:00-08:00",
            is_read_time="2024-12-13T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "After your meeting you sent out assignments to your coworkers. You want to know if either of them has replied to your email yet. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Have Michelle and Kevin replied to the action items I sent them?",
                },
            ],
            reasoning="The user is asking if they have received replies to an email they sent.\nFirstly I should check their inbox for the names Michelle and Kevin. I see only one person with each name in the user's inbox, I can safely assume that these are the people the user is referring to.\nThe user wants to know if these people have replied to action items that the user sent. I see one email from the user with the subject line Action Items from Team Review sent to Michelle Barnes and Kevin Chen at 10:05 and 10:10 respectively.\nI can now see if either of them has replied to this thread.\nI see one reply from Michelle Barnes at 10:15. I do not see any replies from Kevin Chen.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Inbox is checked for replies from Michelle Barnes, and user is told Michelle replied.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. Inbox is checked for replies from Kevin Chen, and user is told Kevin hasn't replied yet.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent uses an email retrieval tool (search or list) to look for replies
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
                # Milestone 1 – Confirm that a reply email from Michelle was retrieved
                # (She has replied to the action items email thread.)
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
                                            "subject": {
                                                "value": "Re: Action Items from Team Review",
                                                "partial": False,
                                            },
                                            # body check is optional, but we assert it's an acknowledgment of the action items
                                            "body": {
                                                "value": "received the action items",
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
                            reference_milestone_node_index=0,  # based on email retrieval in milestone 0
                        ),
                    ],
                ),
                # Milestone 2 – User is informed correctly about who has replied
                # We only check that the answer reflects:
                # - Michelle HAS replied
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We allow multiple phrasings but require these key facts:
                                    "content": [
                                        ("Michelle", "replied", "reply", "respond")
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                    ],
                ),
                # Milestone 3 – User is informed correctly about who has replied
                # - Kevin has NOT replied yet (at least no reply is reported)
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
                                            "not replied",
                                            "hasn't replied",
                                            "no reply",
                                            "not yet",
                                            "not respond",
                                            "hasn't responded",
                                            "yet to",
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
                (0, 1),  # Email search/list → confirm Michelle's reply exists
                (1, 2),  # Knowing reply status → inform user accurately
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_20_23ea1efb-1405-4387-853a-a8bee00192be_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_20",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "contact",
                "calendar",
                "messaging",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-15T10:00:00-08:00",
            is_read_time="2024-12-15T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to set up a meeting on Monday at 9:00 to see how the folks are getting on with their action items from the review meeting, you have sent them emails regarding this on last Friday.    And send a group message to both of them. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set up a meeting tomorrow at 9 to see how the guys are getting on with their action items and drop them a text together.",
                },
            ],
            reasoning="The user needs a meeting scheduled to review action-item progress. I’ll first search recent emails; the thread titled “Action Items from Team Review” shows the people involved are Michelle Barnes and Kevin Chen. I’ll schedule a calendar event called “Team Meeting” for Monday, 16 Dec 2024 at 9 am and list all three of us—Dawei Shen (the user), Michelle Barnes, and Kevin Chen—as attendees. Then I’ll send a single group text that includes Michelle and Kevin (and the user for reference) letting them know about the 9 am meeting.",
            success_conditions=[
                {
                    "input_text": "A calendar event is created for 9:00 AM on Monday December 16 2024 with attendees Dawei Shen, Michelle Barnes, and Kevin Chen.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "A group message is sent to Michelle Barnes and Kevin Chen (with the user included) that mentions the 9 am meeting.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "create_calendar_event",
                "send_message",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0: search for emails
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
                # M1: Action items found from email
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
                                                "value": "2024-12-13",
                                                "partial": True,
                                            },
                                            "subject": {
                                                "value": "Action Items from Team Review",
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
                # Milestone 2 – A calendar event reflecting the user’s request is added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "start_datetime_iso": "2024-12-16T09:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "Dawei Shen",
                                            "Michelle Barnes",
                                            "Kevin Chen",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-15T10:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,
                                "attendees_names": column_list_exact_match_similarity,
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
                    ],
                ),
                # Milestone 3: Ensure a message is sent to Kevin and Michelle
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
                                                "kevin.chen@orchardtech.com",
                                                "+1 555-890-1234-5679",
                                            ),
                                            (
                                                "michelle.barnes@orchardtech.com",
                                                "+1 555-012-3456-7890",
                                            ),
                                            (
                                                "dawei.shen@orchardtech.com",
                                                "+1 555-123-4567-8901",
                                            ),
                                        ]
                                    ],
                                    "content": [("9:00", "9 am", "9am", "nine")],
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-15T10:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_str_contains_any_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CALENDAR,
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_20_c384dc55-857f-4ca5-9c97-4371baa8590d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_20",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "contact",
                "calendar",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T14:30:00-08:00",
            is_read_time="2024-12-13T14:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to schedule a quick check-in with both Michelle and Kevin after the team review for next week.       You also are going to reply them an email to inform them "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set up a quick follow-up with Michelle for Monday at 10 and Kevin for Tuesday at noon to go over what came out of Friday’s meeting. Please also shoot them each a quick note about the upcoming meetings.",
                },
            ],
            reasoning='The user is asking me to create two separate events. The first event is a check-in with Michelle on Monday 16th December 2024 at 10:00. Since there are no scheduling conflicts, I can add this event to the calendar.\n\nThe second event is a check-in with Kevin on Tuesday 17th December 2024 at 12:00. Since there are no scheduling conflicts, I can add this event to the calendar.\n\nThe user requested me to email Michelle "about hers". Judging from the new event I just created, the user must want me to email Michelle at michelle.barnes@orchardtech.com about the "Check-in with Michelle" on Monday 16th December 2024 at 10:00. I will send this in an email. I can assume the same thing for emailing Kevin "about his". I will email Kevin Chen at kevin.chen@orchardtech.com about "Check-in with Kevin" on Tuesday 17th December 2024 at 12:00.',
            success_conditions=[
                {
                    "input_text": '1. A new event "Check-in with Michelle" is created for Monday 16th December 2024 at 10:00.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. A new event "Check-in with Kevin" is created for Tuesday 17th December 2024 at 12:00.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '3. An email will be sent to Michelle Barnes about the "Check-in with Michelle" event.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '3. An email will be sent to Kevin Chen about the "Check-in with Kevin" event.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "4. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "create_calendar_event",
                "send_email",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0: search for calendars to see what is last Friday's meeting
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
                # M1: Friday's meeting recalled
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
                                            "start_datetime_iso": {
                                                "value": "2024-12-13T10:00:00",
                                                "partial": True,
                                            },
                                            "calendar_event_name": {
                                                "value": "Team Review Meeting",
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
                # Milestone 2 – Calendar events added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "start_datetime_iso": [
                                        "2024-12-16T10:00:00-08:00",
                                        "2024-12-17T12:00:00-08:00",
                                    ],
                                    "attendees_names": [
                                        [
                                            "Dawei Shen",
                                            "Michelle Barnes",
                                        ],
                                        [
                                            "Dawei Shen",
                                            "Kevin Chen",
                                        ],
                                    ],
                                    "creation_datetime_iso": "2024-12-13T14:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,
                                "attendees_names": column_list_exact_match_similarity,
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
                    ],
                ),
                # Milestone 3 – Emails sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["michelle.barnes@orchardtech.com"],
                                        ["kevin.chen@orchardtech.com"],
                                    ],
                                    "status": ["sent", "sent"],
                                    "creation_datetime_iso": "2024-12-13T14:30:00-08:00",
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
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.MESSAGING,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_20_9bbf6166-662c-4ace-83f7-b4b11fa52218_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_20",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T10:30:00-08:00",
            is_read_time="2024-12-13T10:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to reply to the email from Michelle to thank her "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to Michelle\'s email with the text "Thanks Michelle"',
                },
            ],
            reasoning="The user wants me to reply to Michelle's email. I will search for the most recent email from michelle.barnes@orchardtech.com (received at 2024-12-13 10:15). Once found, I will send a reply in that thread with the body “Thanks Michelle”.",
            success_conditions=[
                {
                    "input_text": 'An email reply with the body "Thanks Michelle" is sent to michelle.barnes@orchardtech.com.',
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
                # Milestone 0: Agent uses a tool to find recent emails from Michelle
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
                # Milestone 1: Verify emails from michelle.barnes@orchardtech.com were returned
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
                                            "subject": {
                                                "value": "Action Items from Team Review",
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
                        )
                    ],
                ),
                # Milestone 2: Confirm a new sent email to Michelle with the phrase “Thanks Michelle”
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
                    ]
                ),
                # Milestone 3: Confirm a new sent email to Michelle with the phrase “Thanks Michelle”
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["michelle.barnes@orchardtech.com"]
                                    ],
                                    "body": "Thanks Michelle",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-13T10:30:00-08:00",
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
                            reference_milestone_node_index=-1,
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_20_c384dc55-857f-4ca5-9c97-4371baa8590d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_20",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "contact",
                "calendar",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T14:30:00-08:00",
            is_read_time="2024-12-13T14:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to schedule a quick check-in with each of your two coworkers the week after the team review, and email each of them about it. The one who replied to the action items should be booked for that Monday at the same time the review was held, and the other for that Tuesday two hours later. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you schedule a check-in with each of my coworkers the week after our Team Review Meeting? Book the one who replied to the action items for that Monday at the same time the review was held, and the other for that Tuesday two hours later. Then email each of them about it.",
                },
            ],
            reasoning='First, I will search recent emails to see which coworker replied to the action items — I expect a reply from michelle.barnes@orchardtech.com sent on 2024-12-13 at 10:15, so Michelle replied and Kevin did not. Next, I will search the calendar to recall last Friday’s "Team Review Meeting", which took place on 2024-12-13 at 10:00. The check-ins fall the week after: Michelle (who replied) on Monday 2024-12-16 at 10:00 — the same time as the review — and Kevin on Tuesday 2024-12-17 at 12:00 — two hours later. \n\nI will add two new calendar events: \n• "Check-in with Michelle" on Monday, 2024-12-16, at 10:00 (Pacific) with attendees Dawei Shen and Michelle Barnes.\n• "Check-in with Kevin" on Tuesday, 2024-12-17, at 12:00 (Pacific) with attendees Dawei Shen and Kevin Chen.\n\nFinally, I will send an email to each coworker confirming their respective check-in time: one to michelle.barnes@orchardtech.com for the 16-Dec-2024 10:00 meeting and one to kevin.chen@orchardtech.com for the 17-Dec-2024 12:00 meeting.',
            success_conditions=[
                {
                    "input_text": '1. A new event "Check-in with Michelle" is created for Monday 16th December 2024 at 10:00.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. A new event "Check-in with Kevin" is created for Tuesday 17th December 2024 at 12:00.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '3. An email will be sent to Michelle Barnes about the "Check-in with Michelle" event.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '4. An email will be sent to Kevin Chen about the "Check-in with Kevin" event.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "5. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "create_calendar_event",
                "search_calendar_events",
                "get_all_calendars",
                "search_emails",
                "get_all_emails",
                "send_email",
            ],
            milestones=[
                # Milestone 0: Agent uses a tool to find recent emails from Michelle
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
                # Milestone 1: Verify emails from michelle.barnes@orchardtech.com were returned
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
                                            "subject": {
                                                "value": "Action Items from Team Review",
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
                        )
                    ],
                ),
                # Milestone 2: search for calendars to see what is last Friday's meeting
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
                # M3: Friday's meeting recalled
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
                                            "start_datetime_iso": {
                                                "value": "2024-12-13T10:00:00",
                                                "partial": True,
                                            },
                                            "calendar_event_name": {
                                                "value": "Team Review Meeting",
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
                # Milestone 4 – Calendar events added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "start_datetime_iso": [
                                        "2024-12-16T10:00:00-08:00",
                                        "2024-12-17T12:00:00-08:00",
                                    ],
                                    "attendees_names": [
                                        [
                                            "Dawei Shen",
                                            "Michelle Barnes",
                                        ],
                                        [
                                            "Dawei Shen",
                                            "Kevin Chen",
                                        ],
                                    ],
                                    "creation_datetime_iso": "2024-12-13T14:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,
                                "attendees_names": column_list_exact_match_similarity,
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
                    ],
                ),
                # Milestone 5 – Emails sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["michelle.barnes@orchardtech.com"],
                                        ["kevin.chen@orchardtech.com"],
                                    ],
                                    "status": ["sent", "sent"],
                                    "creation_datetime_iso": "2024-12-13T14:30:00-08:00",
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
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.MESSAGING,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Search for Michelle's email
                (2, 3),  # Figure out Kevin is the other participant
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_20_2751c46c-b3a2-4692-83d2-b8e97286612e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_20",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T17:40:00-08:00",
            is_read_time="2024-12-13T17:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You forgot when your dinner with Lukas and Vick is taking place, so you'd like your assistant to help you remember. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When am I hanging out with my friends this week?",
                },
            ],
            reasoning='The user wants to know when their "social event" is happening this week.\n\nOkay, firstly I\'ll check their calendar to see if they have any events that correspond to their description.\n\nSo they don\'t have any events that directly match their description, but they do have one event named "Dinner with Lukas and Vick" that\'s happening on Saturday, December 14th 2024 from 19:00 - 21:00 which I surmise is the "social event" they\'re referring to, given it\'s inherent nature.\n\nI will inform them of the time and date now.',
            success_conditions=[
                {
                    "input_text": '1. User is informed that the event named "Dinner with Lukas and Vick" is scheduled from 19:00 - 21:00 on Saturday, December 14th 2024.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0:  The assistant looks up calendar information (either by searching events
                #               or fetching calendars that contain the events).
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
                # Milestone 1:  The returned tool result contains the event
                #               “Dinner with Lukas and Vick”.
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
                        )
                    ]
                ),
                # Milestone 2:  The assistant’s reply to the user clearly states the
                #               event name and the correct date / time.
                Milestone(
                    snapshot_constraints=[
                        # Check the date is mentioned (December 14th)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "14",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Check the time-range is mentioned (either 19:00 or 7 pm)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "19:00",
                                            "7:00 PM",
                                            "7:00PM",
                                            "7 PM",
                                            "7PM",
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
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_20_2751c46c-b3a2-4692-83d2-b8e97286612f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_20",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T17:40:00-08:00",
            is_read_time="2024-12-14T17:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You are running late for your dinner with Lukas and Vick, so you'd like your assistant to help you calculate how much time left. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How much time do I have left until my outing with Lukas and Vick? Reply in X hour and XX minutes format.",
                },
            ],
            reasoning="1. Look up the user’s calendar using search_calendar_events / get_all_calendars.\n2. Find the event named “Dinner with Lukas and Vick,” which starts at 7:00 PM today.\n3. Compare the current time (5:40 PM) with the event start time (7:00 PM) to get the remaining duration.\n4. Reply to the user in the requested “X hour and XX minutes” format: “1 hour and 20 minutes.”",
            success_conditions=[
                {
                    "input_text": "The assistant tells the user there are 1 hour and 20 minutes left until the outing.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent looks up calendar information with the proper tool
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
                # Milestone 1 – The returned calendar data contains the correct event
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
                # Milestone 2 – The user is informed of the correct date and time
                Milestone(
                    snapshot_constraints=[
                        # Check the time-of-day is mentioned (allow several possible phrasings)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "1 hour and 20 minutes",
                                            "1 hr and 20 min",
                                            "1 hour 20 minutes",
                                            "1 hr 20 min",
                                            "an hour and 20 minutes",
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
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_20_88c2ce99-dfb5-4492-80f6-c4af61458b84_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_20",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "contact",
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
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to reconfirm the start time of dinner with your friends Lukas and Vick tonight. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is my dinner tomorrow? ",
                },
            ],
            reasoning="Right so, the user wants to know the start time for their dinner for tomorrow. I can see that there is one event named 'Dinner with Lukas and Vick' scheduled for 14th December at 19:00. This should be the event the user is looking for. I relay this information to them.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed of the start time for 'Dinner with Lukas and Vick' which is scheduled for 14th December at 19:00.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "search_contacts",
                "get_all_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – A calendar-searching tool is used to look up dinner details
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
                # Milestone 1 – The returned calendar event includes “Dinner with Lukas and Vick”
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
                                "content": column_one_similarity
                            },
                        )
                    ]
                ),
                # Milestone 2 – User is informed of the 7 pm / 19:00 start time
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
                                            "19:00",
                                            "7:00 PM",
                                            "7:00PM",
                                            "7 PM",
                                            "7PM",
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
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_20_f66c6afc-3341-45bb-a9ec-97aae066015f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_20",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T10:05:00-08:00",
            is_read_time="2024-12-13T10:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You have had a busy week at work and haven't had much down-time.       You want to schedule an hour to chill today in your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Add an event called 'Chill' for today at 16:00 - 17:00.",
                },
            ],
            reasoning='The user wants to add an event called "Chill" to their calendar, I\'ll have to find out when. Now I have the time information I can add the Chill event to the calendar on 2024-12-13 at 16:00 - 17:00.',
            success_conditions=[
                {
                    "input_text": 'A new event is added on 2024-12-13 from 16:00 to 17:00 called "Chill".',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["create_calendar_event"],
            milestones=[
                # Milestone 0:  A new calendar event called “chill” on 2024-12-13 from 16:00-17:00 must be added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Chill",
                                    "start_datetime_iso": "2024-12-13T16:00:00",
                                    "end_datetime_iso": "2024-12-13T17:00:00",
                                    "creation_datetime_iso": "2024-12-13T10:05:00-08:00",
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
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_20_88c2ce99-dfb5-4492-80f6-c4af61458b84_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_20",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
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
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to reconfirm the start time of dinner with your friends Lukas and Vick tonight. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is my dinner with Lukas and Vick?",
                },
            ],
            reasoning="Okay so, the user wants to know when is 'Dinner with Lukas and Vick'. One event with a complete match is 'Dinner with Lukas and Vick', and I can let the user know that it is scheduled to start at 19:00 (7 PM).",
            success_conditions=[
                {
                    "input_text": "The user is informed that 'Dinner with Lukas and Vick' starts at 19:00 (7 PM).",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent consults the calendar database to look up the dinner event
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
                # Milestone 1 – The retrieved results include the specific dinner event
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
                # Milestone 2 – The user is informed of the correct start time
                Milestone(
                    snapshot_constraints=[
                        # Ensure the reply contains the correct start time (accept 24-h or 12-h representation)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "19:00",
                                            "7:00 PM",
                                            "7:00PM",
                                            "7 PM",
                                            "7PM",
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
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
    ]
