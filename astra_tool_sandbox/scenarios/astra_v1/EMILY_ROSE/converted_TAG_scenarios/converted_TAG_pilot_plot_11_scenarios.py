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


def get_TAG_EMILY_ROSE_pilot_plot_11(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="EMILY_ROSE_11_6d391d52-b15c-4381-b0aa-336f62cd8847_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_11",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T10:00:00-08:00",
            is_read_time="2024-12-09T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know the gardening tips attachment's name you sent to Henry yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the name of the attachment I sent to Henry yesterday.",
                },
            ],
            reasoning="Okay so, the user wants to be shown an attachment that was sent by the user in an email to Henry yesterday. From their Mail, I can see they were email corresponding with Henry, 'henry.chester@gardensupplies.com'. I can see an email the user sent to Henry at 09:30 on 8 December 2024 with the subject 'Gardening Tips from Today's Walk' and there is an attachment in it, 'Gardening_Tips_Dec2024.pdf'. Now that I have found the requested information, I can now show this attachment name to the user.",
            success_conditions=[
                {
                    "input_text": "The attachment 'Gardening_Tips_Dec2024.pdf' attached to the email delivered to 'henry.chester@gardensupplies.com' with the subject 'Gardening Tips from Today's Walk' on 8 December 2024 at 09:30 is displayed to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – The agent looks through emails to find the one sent to Henry
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
                # Milestone 1 – Verify the retrieved email contains the correct attachment
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
                                                "value": "Gardening Tips from Today's Walk",
                                                "partial": False,
                                            },
                                            "attachments": {
                                                "value": "Gardening_Tips_Dec2024.pdf",
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
                                "content": column_one_similarity,
                            },
                        )
                    ],
                ),
                # Milestone 2 – The agent shows the attachment to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Gardening_Tips_Dec2024",
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
                (0, 1),  # Email search → confirm correct email found
                (1, 2),  # Confirmed email → show attachment to user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_11_7b269c26-f854-4079-af82-3a56c218cdcd_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_11",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T10:05:00-08:00",
            is_read_time="2024-12-08T09:59:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know what Henry said in his last email but you cannot look at your phone right now. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read me the reply to my horticulture email.",
                },
            ],
            reasoning='The user wants me to read out the contents of a message. They have provided me with context that the message is an email, it is a reply to an email they have sent, and it is about horticulture. I\'ll look for emails whose subject lines start with "Re:". I found the subjects "Re: Thank You for Your Feedback!" and "Re: Gardening Tips from Today\'s Walk." Horticulture is the art and science of growing fruits, vegetables, flowers, trees, shrubs and ornamental plants. That means it\'s a synonym for "gardening," so the email whose subject line contains the word "gardening" must be the one they\'re talking about. I\'ll read out the contents of the email with the subject line "Re: Gardening Tips from Today\'s Walk" from henry.chester@gardensupplies.com received at 10:00 on 8 December 2024.  ',
            success_conditions=[
                {
                    "input_text": '1. The email received from henry.chester@gardensupplies.com, with the subject "Re: Gardening Tips from Today\'s Walk" from 10:00 on 8 December 2024, is read out loud to the user. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – agent looks through emails
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
                # Milestone 1 – the expected email from Henry is among the results of Milestone 0
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
                                                "value": "henry.chester@gardensupplies.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Re: Gardening Tips from Today's Walk",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-08T10:00:00-08:00",
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
                # Milestone 2 – agent tells the user the content of Henry's email
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
                                            "Thank you for the wonderful morning",
                                            "Looking forward to our next walk",
                                            "pass this along to our customers",
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
                (0, 1),  # email search → confirm correct email found
                (1, 2),  # correct email found → read email to user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_11_89c46017-96f1-47a2-ba84-068c21876ee9_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_11",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T18:00:00-08:00",
            is_read_time="2024-12-05T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Your gardening project coordination meeting has been rescheduled for 1 hour later due to a scheduling conflict for 2 of the members.   You want to update the change in your Calendar accordingly. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reschedule the gardening project discussion event to start an hour later.",
                },
            ],
            reasoning="The user wants to reschedule the gardening project discussion. I wonder what they're referring to. I should check their calendar for related events. I can't see an event with that exact name in the user's calendar. However, I do see an event with a similar title, 'Gardening Project Coordination Meeting' on Friday, December 6th 2024 at 15:00-16:00. It must be that one. Before I reschedule the event I need to check for any events occurring at the request time, 16:00-17:00. Okay, I see no possible conflict with the requested rescheduling. I'll reschedule the event now for December 6th at 16:00-17:00 and tell the user the event time was successfully updated.",
            success_conditions=[
                {
                    "input_text": "1. The 'Gardening Project Coordination Meeting' event on Friday, December 6th 2024 at 15:00 - 16:00 is rescheduled for the same day, at 16:00-17:00. ",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "modify_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent inspects the calendar to locate the gardening meeting
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
                # Milestone 1 – Confirm the correct event (December 6, 15:00–16:00) was found in Milestone 0’s tool output
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
                                                "value": "Gardening Project Coordination Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
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
                # Milestone 2 – Calendar event has been updated to start one hour later (16:00–17:00)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Gardening Project Coordination Meeting",
                                    "start_datetime_iso": "2024-12-06T16:00:00-08:00",
                                    "end_datetime_iso": "2024-12-06T17:00:00-08:00",
                                    "creation_datetime_iso": "2024-12-05T18:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial calendar state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # calendar lookup → confirm event
                (1, 2),  # event identified → event updated
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_11_89c46017-96f1-47a2-ba84-068c21876ee9_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_11",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T18:00:00-08:00",
            is_read_time="2024-12-05T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Your gardening project coordination meeting has been rescheduled for 1 hour later due to a scheduling conflict for 2 of the members.   You want to update the change in your Calendar accordingly. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reschedule the Gardening Project Coordination Meeting to start an hour later. ",
                },
            ],
            reasoning="The user wants to reschedule the the Gardening Project Coordination Meeting. I wonder what they're referring to. I should check their calendar for related events. I see an event with the same title, 'Gardening Project Coordination Meeting' on Friday, December 6th at 15:00-16:00. It must be that one. Before I reschedule the event I need to check for any events occurring at the request time, 16:00-17:00. Okay, I see no possible conflict with the requested rescheduling. I'll reschedule the event now for December 6th 2024 at 16:00-17:00 and tell the user the event time was successfully updated.",
            success_conditions=[
                {
                    "input_text": "1. The 'Gardening Project Coordination Meeting' event on Friday, December 6th 2024 at 15:00 - 16:00 is rescheduled for the same day, at 16:00-17:00. ",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "modify_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up calendar events to find the meeting
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
                # Milestone 1 – The meeting has been moved from 15:00–16:00 to 16:00–17:00 on the same date
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Gardening Project Coordination Meeting",
                                    "start_datetime_iso": "2024-12-06T16:00:00-08:00",
                                    "end_datetime_iso": "2024-12-06T17:00:00-08:00",
                                    "creation_datetime_iso": "2024-12-05T18:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
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
            name="EMILY_ROSE_11_6d391d52-b15c-4381-b0aa-336f62cd8847_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_11",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T10:00:00-08:00",
            is_read_time="2024-12-09T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know the gardening tips attachment's name you sent to Henry yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to know the attachment name I sent to the person I was emailing yesterday. ",
                },
            ],
            reasoning="Right so, the user is looking to check an attachment name that they sent to a person they were emailing yesterday. Yesterday was 8 December 2024, so I will check their emails and I can see there was a correspondence with Henry, 'henry.chester@gardensupplies.com'. In the email that the user sent to Henry at 09:30 with the subject 'Gardening Tips from Today's Walk', there is an attachment in it, 'Gardening_Tips_Dec2024.pdf'. Now that I have found the requested information, I can now show this attachment to the user.",
            success_conditions=[
                {
                    "input_text": "The attachment name 'Gardening_Tips_Dec2024' is displayed to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – Agent looks through emails (search_emails / get_all_emails)
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
                # Milestone 1 – Confirm the correct email (with attachment) was returned from the tool call in Milestone 0
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
                                                "value": "Gardening Tips from Today's Walk",
                                                "partial": False,
                                            },
                                            "attachments": {
                                                "value": ["Gardening_Tips_Dec2024.pdf"],
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,  # look at result of Milestone 0
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
                # Milestone 2 – Agent shows the attachment name to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Gardening_Tips_Dec2024",
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
                (0, 1),  # Email search → verify correct email found
                (1, 2),  # Correct email found → attachment shown to user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_11_99bd9304-0adf-418e-aa38-c0d1119f2b51_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_11",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T10:15:00-08:00",
            is_read_time="2024-12-08T10:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to email your friend to finish the conversation with them. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to the email "Gardening Tips from Today\'s Walk" saying "you\'re welcome, let me know if you need anything else"',
                },
            ],
            reasoning='The user wants to reply to an email with the subject "Gardening Tips from Today\'s Walk" but I see two emails with a subject containing that string, so I need to disambiguate between the two to figure out which one the user means. I see one email FROM the user sent TO henry.chester@gardensupplies.com with that subject, and one email FROM henry.chester@gardensupplies.com TO the user with the subject "Re: Gardening Tips from Today\'s Walk" where the sender is thanking the user. That\'s probably what the user meant when they said they want to reply to the email because even though it has "Re" at the beginning, they wouldn\'t want to reply to the email without the "Re" because that would be the user replying to themself. So I\'ll reply to the one with the subject "Re: Gardening Tips from Today\'s Walk". The user wants to say “you\'re welcome, let me know if you need anything else” so I\'ll write that and reply to henry.chester@gardensupplies.com',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. An email is sent to henry.chester@gardensupplies.com saying "you\'re welcome, let me know if you need anything else"',
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – The agent looks up existing emails to find the one to reply to
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
                # Milestone 1 – Confirm that the email from Henry about gardening tips was returned
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
                                                "value": "Gardening Tips from Today's Walk",
                                                "partial": True,
                                            },
                                            "sender_address": {
                                                "value": "henry.chester@gardensupplies.com",
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
                # Milestone 2 – Verify a reply email was sent to Henry with the expected message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["henry.chester@gardensupplies.com"]
                                    ],
                                    "status": "sent",
                                    "body": "let me know if you need anything else",
                                    "creation_datetime_iso": "2024-12-08T10:15:00-08:00",
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
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_11_de48f250-6d0b-4c91-aa45-8c573a7d7b83_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_11",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T10:05:00-08:00",
            is_read_time="2024-12-08T10:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to reply to Henry Chester's email to let him know it was a pleasure and you don't mind helping out "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a reply to Henry Chester's email about the gardening tips and say \"Hi Henry,\nIt was a pleasure! I don't mind helping out.\nBest regards, Emily Rose\"",
                },
            ],
            reasoning='The user wants me to reply to an email from Henry Chester with the text "Hi Henry,\nIt was a pleasure! I don\'t mind helping out.\nBest regards, Emily Rose". First thing I need to do is find this email they are referencing. I will look in their inbox and see if I can find any from a Henry Chester. Ok I have found one email from someone listed as Henry Chester with the subject line "Gardening Tips from Today\'s Walk". This must be the email. I will draft an email reply with the text the user has given me and then I will ask the user if it is ready to be sent. ',
            success_conditions=[
                {
                    "input_text": '1. An email reply to the email with subject "Gardening Tips from Today\'s Walk" is sent to henry.chester@gardensupplies.com with the body "Hi Henry,\nIt was a pleasure! I don\'t mind helping out.\nBest regards, Emily Rose"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
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
                    ]
                ),
                # Milestone 1 – A reply email is sent to Henry Chester with the expected content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["henry.chester@gardensupplies.com"]
                                    ],
                                    "status": "sent",
                                    "body": "It was a pleasure",
                                    "creation_datetime_iso": "2024-12-08T10:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "body": column_contains_similarity,  # checks presence of the key phrase,
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
            name="EMILY_ROSE_11_5fa4bf53-b775-43ba-a684-77b9ac609099_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_11",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T10:00:00-08:00",
            is_read_time="2024-12-08T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You spent your walk thinking about the meetings you have coming up.   You realize you are not sure if you have added the right people to tomorrow's activity planning. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who are the invitees for tomorrow's Student Engagement Activity Planning?",
                },
            ],
            reasoning="The user is asking about the invitees of an event.\nFirst, I should try and find the event in the user's calendar.\nI can see an exact match for the user's query,\nStudent Engagement Activity Planning scheduled for December 09 2024, 16:00-17:30.\nThe invitees for this event are currently Jenna Miles and Matt Duncan.\nI should inform the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. Invitees of Student Engagement Activity Planning scheduled for December 09 2024, 16:00-17:30 are confirmed as Jenna Miles and Matt Duncan.",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (either by searching or listing all)
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
                # Milestone 1 – The expected event is present in the tool’s returned results
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
                                                "value": "Student Engagement Activity Planning",
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
                # Milestone 2 – Agent tells the user the invitees include “Jenna Miles”
                Milestone(
                    snapshot_constraints=[
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
                        # Also confirm the second invitee “Matt Duncan” appears in the same or subsequent reply
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Matt Duncan",
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
                (0, 1),  # Calendar lookup → event confirmation
                (1, 2),  # Event confirmation → user-facing answer
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_11_7b269c26-f854-4079-af82-3a56c218cdcd_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_11",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T10:05:00-08:00",
            is_read_time="2024-12-08T09:59:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know what Henry said in his last email but you cannot look at your phone right now. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What did henry's last email say? Be literal, verbatim.",
                },
            ],
            reasoning='The user wants me to read out the contents of a message. They have provided me with context that the message is an email and it is the last received email from a contact named "Henry". This should be enough information to find the email. I have searched the user\'s emails, and I have found an email from Henry Chester. I can assume this is the referenced message, so I will read it out to the user. ',
            success_conditions=[
                {
                    "input_text": '1. The email received from henry.chester@gardensupplies.com, with the subject "Re: Gardening Tips from Today\'s Walk" from 10:00 on 8 December 2024, is read out loud to the user. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – Agent tries to locate Henry’s most recent email
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
                # Milestone 1 – Confirm the retrieved email matches Henry’s last message
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
                                                "value": "henry.chester@gardensupplies.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Re: Gardening Tips from Today's Walk",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-08T10:00:00-08:00",
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
                # Milestone 2 – Agent relays the email content back to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Thank you for the wonderful morning",
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
                (0, 1),  # Email search → confirm correct email
                (1, 2),  # Correct email found → user informed
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_11_7b269c26-f854-4079-af82-3a56c218cdcd_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_11",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T10:05:00-08:00",
            is_read_time="2024-12-08T09:59:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know what Henry said in his last email but you cannot look at your phone right now. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'What did the unread email I received from "henry.chester@gardensupplies.com" say? Be literal, verbatim. ',
                },
            ],
            reasoning="The user wants me to read out the contents of a message. They have provided me with context that the message is from \"henry.chester@gardensupplies.com\" and it's unread. This should be enough information to find the email. I have searched the user's emails, and I have found an unread email from Henry Chester, from henry.chester@gardensupplies.com on December 08, 2024  at 10:00 . I can assume this is the referenced message, so I will read it out to the user. ",
            success_conditions=[
                {
                    "input_text": '1. The email received from henry.chester@gardensupplies.com, with the subject "Re: Gardening Tips from Today\'s Walk" from 10:00 on 8 December 2024, is read out loud to the user. ',
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
                # Milestone 1 – The retrieved email is the one from Henry on 2024-12-08 10:00
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
                                                "value": "henry.chester@gardensupplies.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-08T10:00:00-08:00",
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
                # Milestone 2 – Agent tells the user the content of Henry’s email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Thank you for the wonderful morning",
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
            name="EMILY_ROSE_11_5fa4bf53-b775-43ba-a684-77b9ac609099_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_11",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T10:00:00-08:00",
            is_read_time="2024-12-08T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You spent your walk thinking about the meetings you have coming up.   You realize you are not sure if you have added the right people to tomorrow's activity planning. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who is coming to the school meeting tomorrow?",
                },
            ],
            reasoning="The user is asking about the invitees of an event.\nFirst, I should try and find the event in the user's calendar.\nI cannot see an exact match for the user's query,\nThe user has mentioned that the event is scheduled for tomorrow, December 09 2024.\nI can see only one event for this date. \nStudent Engagement Activity Planning scheduled for December 09 2024, 16:00-17:30.\nThe invitees for this event are currently Jenna Miles and Matt Duncan.\nI should inform the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. Invitees of Student Engagement Activity Planning scheduled for December 09 2024, 16:00-17:30 are confirmed as Jenna Miles and Matt Duncan.",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent examines the calendar to find tomorrow’s meeting
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
                # Milestone 1 – Verify the “Student Engagement Activity Planning” event was found
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
                                                "value": "Student Engagement Activity Planning",
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
                # Milestone 2 – Agent tells user Jenna Miles is attending
                Milestone(
                    snapshot_constraints=[
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
                        )
                    ],
                ),
                # Milestone 3 – Agent tells user Matt Duncan is attending
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Matt Duncan",
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
                (1, 3),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_11_de48f250-6d0b-4c91-aa45-8c573a7d7b83_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_11",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T10:05:00-08:00",
            is_read_time="2024-12-08T10:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to reply to Henry Chester's email to let him know it was a pleasure and you don't mind helping out "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to the email from henry.chester@gardensupplies.com I received at 10am today and say "Hi Henry,\nIt was a pleasure! I don\'t mind helping out.\nBest regards, Emily Rose"',
                },
            ],
            reasoning='The user wants me to reply to an email they received at 10am from henry.chester@gardensupplies.com with the text "Hi Henry,\nIt was a pleasure! I don\'t mind helping out.\nBest regards, Emily Rose". First thing I need to do is find this email they are referencing. I will look in their inbox and see if I can find any from this email address. Ok I have found one email from that address with the subject line "Gardening Tips from Today\'s Walk" received at 10am. This must be the email. I will draft an email reply with the text the user has given me and then I will ask the user if it is ready to be sent. ',
            success_conditions=[
                {
                    "input_text": '1. An email reply to the email with subject "Gardening Tips from Today\'s Walk" is sent to henry.chester@gardensupplies.com with the body "Hi Henry,\nIt was a pleasure! I don\'t mind helping out.\nBest regards, Emily Rose"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
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
                                    target_tools=[
                                        "search_emails",
                                        "get_all_emails",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Confirms the correct email (from Henry, right subject) was found
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
                                                "value": "henry.chester@gardensupplies.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Gardening Tips",
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
                # Milestone 2 – A reply email is sent to Henry with the required body text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["henry.chester@gardensupplies.com"]
                                    ],
                                    "status": "sent",
                                    "body": "It was a pleasure! I don't mind helping out.",
                                    "creation_datetime_iso": "2024-12-08T10:05:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare with initial state
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Must find email before confirming content
                (1, 2),  # After confirming, send reply
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_11_99bd9304-0adf-418e-aa38-c0d1119f2b51_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_11",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T10:15:00-08:00",
            is_read_time="2024-12-08T10:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to email your friend to finish the conversation with them. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to the email from 10am and say “you're welcome, let me know if you need anything else”",
                },
            ],
            reasoning='I need to write a reply to an email for the user. They want me to reply to the email from 10:00. I see one email received at 10:00 today 8 December 2024, from henry.chester@gardensupplies.com, with the subject "Re: Gardening Tips from Today\'s Walk". I\'ll reply to this with the content the user dictated, "you\'re welcome, let me know if you need anything else".',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. An email is sent to henry.chester@gardensupplies.com saying "you\'re welcome, let me know if you need anything else"',
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – The agent looks up the 10 a.m. email (information-retrieval step)
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
                # Milestone 1 – Confirm that the email from Henry at 10:00 a.m. was found
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
                                                "value": "Re: Gardening Tips from Today's Walk",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "henry.chester@gardensupplies.com",
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
                # Milestone 2 – A reply email has been sent to Henry with the required wording
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["henry.chester@gardensupplies.com"]
                                    ],
                                    "status": "sent",
                                    "body": "you're welcome",
                                    "creation_datetime_iso": "2024-12-08T10:15:00-08:00",
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
                (0, 1),  # must find the email before confirming contents
                (1, 2),  # retrieval precedes sending the reply
            ],
        ),
    ]
