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
    column_list_tuple_contains_similarity,
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
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


def get_TAG_LUCAS_GARCIA_pilot_plot_12(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="LUCAS_GARCIA_12_d9cf7f35-a890-46dc-bf09-70cafbbe3300_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_12",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T17:50:00-08:00",
            is_read_time="2024-12-07T17:50:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to text your triathlon coach to show your enthusiasm. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to my Triathlon coach; "I\'m ready to keep up the pace!"',
                },
            ],
            reasoning="Ok so the user wants to reply to their triathlon coach with a given message. First I will establish who they mean by triathlon coach. The contact Brian Carter is labelled in the contacts as triathlon coach so I assume this is who they're referring to. Next is the method of communication which is hinted at by the user in them saying 'reply.' To me this says they were in contact recently so I will look for that now. They were talking via text most recently so this is probably the route the user wants to message them through. I will now send the user's given message to Brian Carter via text at 17:50 on 7 December 2024. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message "I\'m ready to keep up the pace!" is sent to Brian Carter via text at 17:50 on 7 December 2024. ',
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent tries to identify the triathlon coach in contacts
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
                # Milestone 1 – Confirm that Brian Carter (triathlon coach) was found in the previous contact-search result
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
                                                "value": "Brian Carter",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "brian.carter@example.com",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 12345-6789-1000-7410",
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
                # Milestone 2 – A new text message is sent to Brian Carter with the correct content
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
                                                "brian.carter@example.com",
                                                "+1 12345-6789-1000-7410",
                                            ),
                                            (
                                                "lucas.garcia@example.com",
                                                "+1 12345-6789-1000-1234",
                                            ),
                                        ]
                                    ],
                                    "content": "I'm ready to keep up the pace!",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-07T17:50:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
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
                (0, 1),  # Found the correct contact after searching
                (1, 2),  # Sent the message after confirming the contact
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_955b6f9b-6149-4be3-a346-30b1d6aab25d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_12",
                "messaging",
                "contact",
                "email",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:00:00-08:00",
            is_read_time="2024-12-08T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know if your triathlon coach has messaged you any feedback. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has Brian sent me feedback?",
                },
            ],
            reasoning="Okay so, the user is looking for 'feedback' from 'Brian'. Checking the user's contacts, I can see only one 'Brian' matching named 'Brian Carter'. Next, checking their messages I can see Brian and the user were messaging yesterday, 7 December 2024 and Brian replied to the user saying 'Received it, thanks. Everything looks good so far, but I'll go through in detail later tonight. Expect feedback by tomorrow.'. This seems to be about the 'feedback' the user is asking about. \n\nNext, I will check their emails and can see they emailed Brian yesterday, 7 December 2024 at 16:15 with the subject 'Triathlon Strategy Meeting Notes - December 7, 2024'. Brian has not sent any new messages or emails to the user. Therefore I can relay this information to the user.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that no new messages or emails have been received from Brian Carter on 8 December 2024.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 –  Agent looks for messages / emails from Brian
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
                                        "search_emails",
                                        "get_all_emails",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Agent informs the user that no new feedback/messages from Brian were found
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
                                            "no new",
                                            "hasn't sent",
                                            "has not sent",
                                            "no message from Brian",
                                            "no feedback",
                                            "none from Brian",
                                            "didn't send",
                                            "not received",
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
            name="LUCAS_GARCIA_12_e571a4a9-fe48-4302-afcb-0ae1338491b4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_12",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T11:00:00-08:00",
            is_read_time="2024-12-07T11:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know what time your triathlon strategy meeting is occurring today. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When's the triathlon meeting?",
                },
            ],
            reasoning="The user needs information on a meeting. They have said that it concerns a triathlon so I'll start by checking today's event for that term. I've found Triathlon Strategy Meeting with Brian and Team that it taking place today from 15:00 to 16:00. I'll let the user know the time.",
            success_conditions=[
                {
                    "input_text": '1. The start time of the event "Triathlon Strategy Meeting with Brian and Team" is read out to the user.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent queries the calendar for the triathlon meeting
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
                # Milestone 1 – Verify the correct calendar event was returned from the search in Milestone 0
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
                                                "value": "Triathlon Strategy Meeting with Brian and Team",
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
                # Milestone 2 – Agent informs the user of the meeting start time
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
                                            "3 pm",
                                            "3pm",
                                            "3 p.m.",
                                            "15:00",
                                            "15:00 pm",
                                            "3:00",
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
                (0, 1),  # Calendar search → confirm correct event
                (1, 2),  # Confirm event → user informed
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_6c1c4de0-7fdc-44a7-87c9-73213a4549ff_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_12",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T16:39:00-08:00",
            is_read_time="2024-12-07T16:39:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know if your triathlon coach Brian got the training notes you sent him and if you missed anything important in them. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What did my triathlon coach say?",
                },
            ],
            reasoning="The user wants to know what their triathlon coach said. I wonder what who that is. I'll check the user's contacts to figure it out. I see one contact listed as triathlon coach; Brian Carter. I'll search for the latest message from Brian now. I see one new message from Brian Carter, received on December 7th, 2024, at 16:35. I'll show that to the user now. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The message from Brian Carter, received on December 7th, 2024, at 16:35, is shown to the user. ",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent tries to fetch the relevant messages
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
                # Milestone 1 – Verify that the fetched message includes Brian Carter's 16:35 reply
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
                                            "participants_addresses": {
                                                "value": "brian.carter@example.com",
                                                "partial": True,
                                            },
                                            "content": {
                                                "value": "Received it, thanks",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-07T16:35:00-08:00",
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
                                    "content": "{matched}",  # will be replaced with extractor output
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – Ensure the agent tells the user what Brian said
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
                                            "Received it",
                                            "Everything looks good",
                                            "Expect feedback",
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
            name="LUCAS_GARCIA_12_6c1c4de0-7fdc-44a7-87c9-73213a4549ff_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_12",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T16:39:00-08:00",
            is_read_time="2024-12-07T16:39:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know if your triathlon coach Brian got the training notes you sent him and if you missed anything important in them. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What did Brian say?",
                },
            ],
            reasoning="The user wants to know what Brian said. I wonder what who that is. I'll check the user's contacts to figure it out. I see one contact with that name; Brian Carter. I'll search for the latest message from Brian now. I see one new message from Brian Carter, received on December 7th, 2024, at 16:35. I'll show that to the user now. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The message from Brian Carter, received on December 7th, 2024, at 16:35, is shown to the user. ",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – agent tries to retrieve Brian’s message
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
                # Milestone 1 – confirm that Brian’s 16:35 message was returned in the tool output
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
                                            "value": "brian.carter@example.com",
                                            "partial": False,
                                        },
                                        "content": {
                                            "value": "Received it",
                                            "partial": True,
                                        },
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
                                "content": column_one_similarity,
                            },
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – agent conveys Brian’s message content back to the user
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
                                            "Received it",
                                            "Everything looks good",
                                            "Expect feedback",
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
                (
                    0,
                    1,
                ),  # must first call message-retrieval tool, then verify correct message returned
                (1, 2),  # after retrieving the message, agent informs the user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_e571a4a9-fe48-4302-afcb-0ae1338491b4_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_12",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T11:00:00-08:00",
            is_read_time="2024-12-07T11:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know what time your triathlon strategy meeting is occurring today. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Need the start time for the triathlon strategy meeting with Brian.",
                },
            ],
            reasoning="The user wants to know a start time for a meeting. They have named it as the triathlon strategy meeting with Brian. There is an event matching this name occurring today at 15:00. I'll let the user know.",
            success_conditions=[
                {
                    "input_text": '1. The start time of the event "Triathlon Strategy Meeting with Brian and Team" is read out to the user.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent queries the calendar to locate the meeting
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
                # Milestone 1 – The tool call returned the expected meeting with the correct start time
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
                                                "value": "Triathlon Strategy Meeting with Brian and Team",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T15:00:00-08:00",
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
                # Milestone 2 – The agent tells the user the start time of the meeting
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
                                            "3:00",
                                            "3 pm",
                                            "3pm",
                                            "3 p.m.",
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
            name="LUCAS_GARCIA_12_955b6f9b-6149-4be3-a346-30b1d6aab25d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_12",
                "messaging",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:00:00-08:00",
            is_read_time="2024-12-08T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know if your triathlon coach has messaged you any feedback. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did my triathlon coach send me some feedback? Yes or no.",
                },
            ],
            reasoning="Right so, the user is looking for some 'feedback' from his 'triathlon coach'. Firstly checking the user's contacts, I can see one contact matching under 'Triathlon Coach' named 'Brian Carter'. This is who the user is requesting information from. Next I will check their message thread and emails. I can see that Brian and the user were messaging yesterday, 7 December 2024 and Brian replied to the user saying 'Received it, thanks. Everything looks good so far, but I'll go through in detail later tonight. Expect feedback by tomorrow.'. This seems to be about the 'feedback' the user is asking about. Also, the user sent an email to Brian Carter on 7 December 2024 at 16:15 with the subject 'Triathlon Strategy Meeting Notes - December 7, 2024'. Brian has not sent any new messages or emails to the user. Therefore I can relay that no feedback has been received to the user, and reply with 'No'.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed with 'No', as there are no new messages or emails have been received from Brian Carter on 8 December 2024.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – The agent looks through messages (SMS/imessage) for feedback from the coach
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
                        ),
                    ],
                ),
                # Milestone 1 – The agent looks through emails for feedback from the coach
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
                        ),
                    ],
                ),
                # Milestone 2 – The agent informs the user that no new feedback has been received
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Any reasonable negative confirmation phrasing is acceptable
                                    "content": [("no")],
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
                (0, 2),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_d9cf7f35-a890-46dc-bf09-70cafbbe3300_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_12",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T17:50:00-08:00",
            is_read_time="2024-12-07T17:50:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to text your triathlon coach to show your enthusiasm. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Text Brian Carter; "I\'m ready to keep up the pace!"',
                },
            ],
            reasoning="Ok so the user wants to text Brian Carter a given message. First is who the message is to which is given by the user. Next is the method which is also given by the user.  I will now send the user's given message to Brian Carter via text at 17:50 on 7 December 2024. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message "I\'m ready to keep up the pace!" is sent to Brian Carter via text at 17:50 on 7 December 2024. ',
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent looks up Brian Carter’s contact information
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",  # check only the tool name(s)
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
                # Milestone 1 – The returned contact list actually contains Brian Carter
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
                                                "value": "Brian Carter",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "brian.carter@example.com",
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
                            reference_milestone_node_index=0,  # parse the results from the search in Milestone 0
                        )
                    ]
                ),
                # Milestone 2 – A new text message to Brian Carter was sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Must include Brian; other participants (e.g. Lucas/Self) are allowed
                                    "participants_addresses": [
                                        [
                                            (
                                                "+1 12345-6789-1000-7410",
                                                "brian.carter@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "I'm ready to keep up the pace!",
                                    "creation_datetime_iso": "2024-12-07T17:50:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against the initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox chatter when checking MESSAGING addition
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_a1997c05-0f93-46de-b60b-8ee3d0b56ae6_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_12",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
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
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to arrange a coffee meet up with Brian Carter to discuss the Triathlon Notes. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to Brian Carter inviting him to coffee today and go over the feedback for the triathlon strategy meeting",
                },
            ],
            reasoning="The user would like to arrange a coffee date today with team member Brian Carter and go over notes that were created from the Triathlon Strategy on December 7th. \n\nI will follow the email message thread created called Triathlon Strategy Meeting Notes and inquire if it is possible to create a meet up for coffee. When I receive a reply from Brian Carter I will arrange the date and time for coffee not the users calendar. ",
            success_conditions=[
                {
                    "input_text": "1. Message is sent to Brian Carter requesting a coffee meeting to discuss the recent email regarding Triathlon Strategy Notes. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up Brian Carter in contacts
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
                # Milestone 1 – Verify Brian Carter’s contact record was returned in previous tool output
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
                                                "value": "Brian Carter",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "brian.carter@example.com",
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
                # Milestone 2 – A new message is sent to Brian Carter asking for coffee to discuss triathlon notes
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Ensure Brian is included among recipients / participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "+1 12345-6789-1000-7410",
                                                "brian.carter@example.com",
                                            )
                                        ]
                                    ],
                                    # Message should mention coffee or triathlon notes
                                    "content": [
                                        ("coffee", "Coffee", "triathlon", "Triathlon")
                                    ],
                                    "creation_datetime_iso": "2024-12-08T10:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_str_contains_any_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore SANDBOX changes when checking MESSAGING addition
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_0e51ffae-3c77-46ca-b71d-db8520158b60_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_12",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T20:00:00-08:00",
            is_read_time="2024-12-07T20:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to see what the last message in the triathlon strategy meeting session chat was. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What was the most recent message in the strategy chat?",
                },
            ],
            reasoning="I need to search the users messages for a 'strategy chat'. I found one that is similar called ' Triathlon Strategy Session'. I'll assume that this is the correct chat.\nI search for the most recent message in that chat and present it to the user when it's found.",
            success_conditions=[
                {
                    "input_text": "1. The message sent by Brian Carter on December 7th 2024 at 16:45 is presented to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
            milestones=[
                # Milestone 0 – The agent invokes a message-retrieval tool
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
                # Milestone 1 – Confirm the expected message appears in the tool output from Milestone 0
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
                                                "value": "You too, Lucas! Let's keep this momentum going.",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "brian.carter@example.com",
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
                # Milestone 2 – The agent tells the user the content of the most recent message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "You too, Lucas! Let's keep this momentum going.",
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
                (0, 1),  # tool used → verify message in output
                (1, 2),  # message found → user informed
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_9bb04e50-f13d-4148-80c9-d338c672a4ad_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_12",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T17:00:00-08:00",
            is_read_time="2024-12-07T17:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to reply to a recently received message in a thread about triathlon strategy. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to Brian to say Will do!",
                },
            ],
            reasoning="The user would like to send a message to a contact named Brian, containing the text \"Will do!\". I'll need to find the named contact via their contact list and or messages, and once I've located the contact in question I can compose the message and seek confirmation to send it.",
            success_conditions=[
                {
                    "input_text": '1. A reply is sent to Brian Carter with the text "Will do!"',
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
                # Milestone 0 – The agent looks up the existing conversation or messages
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
                # Milestone 1 – A new message sent to Brian with the required content
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
                                                "+1 12345-6789-1000-7410",
                                                "brian.carter@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "Will do!",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-07T17:00:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare with pre-task snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Information retrieval precedes sending the reply
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_1e4a7919-a5a6-4fc3-a25a-338e5088f9a2_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_12",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
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
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know what time your meeting was at yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time was my 'Triathlon Strategy Meeting with Brian and Team' yesterday?",
                },
            ],
            reasoning="The user wants to know what time their event 'Triathlon Strategy Meeting with Brian and Team' was on yesterday. I will look for the event in Calendar. I see one event with that name. I will inform the user that their event 'Triathlon Strategy Meeting with Brian and Team' on Saturday, December 7th, 2024, ran from 15:00- 16:00.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their event 'Triathlon Strategy Meeting with Brian and Team' on December 7th ran from 15:00 -16:00.\n",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent looks up the calendar to find the meeting
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
                # Milestone 1 – Confirm that the retrieved calendar entry is the correct meeting
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
                                                "value": "Triathlon Strategy Meeting with Brian and Team",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T15:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-07T16:00:00-08:00",
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
                            reference_milestone_node_index=0,  # depends on the tool output from Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – The agent informs the user of the meeting time (3 pm – 4 pm / 15:00 – 16:00)
                Milestone(
                    snapshot_constraints=[
                        # Check start time mention
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        ("3 pm", "3 p.m.", "3pm", "15:00", "3:00")
                                    ],
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
                (0, 1),  # Calendar lookup → confirmation of correct meeting
                (1, 2),  # Confirmed meeting → inform the user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_b8767c71-be4a-423f-a498-649690b5fce8_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_12",
                "email",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
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
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to ask your friend if he wants to get coffee to discuss the Triathlon Notes you sent him. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send another email to the friend I emailed about triathlon strategy yesterday. Set the subject as "Notes over Coffee" and have it say "I want to propose a coffee meeting to discuss our Triathlon Strategy Notes. What do you think?".',
                },
            ],
            reasoning='The user would like to send a new email. They said the recipient should be the friend they "emailed about triathlon strategy yesterday." To figure out who they\'re talking about, let me first check the emails the user sent. I see two that mention triathlons in the subject: "Triathlon Training Session Summary - December 3, 2024" from 3 December 2024 at 8:30 from lucas.garcia@example.com to jason.baker@example.com, and "Triathlon Strategy Meeting Notes - December 7, 2024" from 7 December 2024 at 10:00 from lucas.garcia@example.com to brian.carter@example.com. The user referred to the triathlon-related email from yesterday specifically, so that\'s the one I\'ll use to continue my reasoning. Now, the user sent this email to Brian Carter, so that\'s the person they want to send this new email to. They want the subject to be "Notes over Coffee" and for the email to say "I want to propose a coffee meeting to discuss our Triathlon Strategy Notes. What do you think?" so that\'s what I\'ll send.',
            success_conditions=[
                {
                    "input_text": '1. An email with the subject "Notes over Coffee" is sent to Brian Carter saying "I want to propose a coffee meeting to discuss our Triathlon Strategy Notes. What do you think?" is sent to the user.',
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
                # Milestone 0 – agent inspects past email threads to figure out who the “friend” is
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
                # Milestone 1 – verify that the required email was actually sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["brian.carter@example.com"]
                                    ],
                                    "subject": "Notes over Coffee",
                                    "body": "I want to propose a coffee meeting to discuss our Triathlon Strategy Notes. What do you think?",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-08T10:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "subject": column_exact_match_similarity,
                                "body": column_contains_similarity,  # allows minor paraphrasing but must include proposal text
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with pre-task snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_f48441f7-e818-4d90-9ae0-65f0aea7933b_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_12",
                "contact",
                "email",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T12:00:00-08:00",
            is_read_time="2024-12-09T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to see if your trainer responded to your last email as you haven't heard from him and are worried you may have missed a reply. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did my trainer respond to my email from Saturday? Yes or no.",
                },
            ],
            reasoning="The user wants to know if their trainer responded to their email from Saturday. I must determine who the user's trainer is, I'll check their contacts. There is nobody in the user's contacts named Trainer but I can see Brian Carter has an alias of 'Triathlon Coach' which could be substituted for trainer and the user emailed Brian Carter on Saturday. With this information I can assume Brian Carter is the user's trainer. I'll see if Brian responded to the user's email. There have been no replies to the user's email. I'll inform the user.",
            success_conditions=[
                {
                    "input_text": "1. The email sent to brian.carter@example.com is found",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. A reply from brian.carter@example.com is searched for and user is informed 'No' as there's not reply.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent queries the email store to locate the user’s own message to Brian
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
                # Milestone 1 – Confirm that among the results returned in Milestone 0 there is the email Lucas sent to Brian
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
                                            # We only need to confirm that an email addressed to Brian was retrieved
                                            "recipients_addresses": {
                                                "value": "brian.carter@example.com",
                                                "partial": True,
                                            },
                                            "status": {
                                                "value": "sent",
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
                                    "content": "{matched}",  # gets filled with the extractor’s “matched” value
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – Agent informs the user that no reply from Brian was found
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "no",
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
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_f48441f7-e818-4d90-9ae0-65f0aea7933b_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_12",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T12:00:00-08:00",
            is_read_time="2024-12-09T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to see if Brian Carter responded to your last email as you haven't heard from him and are worried you may have missed a reply "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did Brian respond to my email from Saturday? Yes or no.",
                },
            ],
            reasoning="The user wants to know if Brian responded to their email from Saturday. Brian Carter is the only Brian in the user's contacts. I'll find the user's email to Brian. I've found the user's email from December 7th at 4:15 pm to brian.carter@example.com. There have been no replies to this email. I'll inform the user.",
            success_conditions=[
                {
                    "input_text": "1. The email sent to brian.carter@example.com is found",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. A reply from brian.carter@example.com is searched for and user is informed with No.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent looks through the mailbox
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
                # Milestone 1 – The outgoing Saturday email to Brian is surfaced
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
                                            # Lucas sent it …
                                            "sender_address": {
                                                "value": "lucas.garcia@example.com",
                                                "partial": False,
                                            },
                                            # … to Brian
                                            "recipients_addresses": {
                                                "value": "brian.carter@example.com",
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
                # Milestone 2 – User is informed that no reply has been received
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "no",
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
                (0, 1),  # mailbox search → confirms outgoing email
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_b8767c71-be4a-423f-a498-649690b5fce8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_12",
                "email",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
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
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to ask your friend if he wants to get coffee to discuss the Triathlon Notes you sent him. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want send an email to Brian with the subject "Notes over Coffee" saying, "I want to propose a coffee meeting to discuss our Triathlon Strategy Notes. What do you think?"',
                },
            ],
            reasoning="The user would like to send a new email. they listed the recipient as Brian. There's only one Brian in their contacts, Brian Carter, so that's who I'll send it to. They want the subject to be \"Notes over Coffee\" and for the email to say \"I want to propose a coffee meeting to discuss our Triathlon Strategy Notes. What do you think?\" so that's what I'll send.",
            success_conditions=[
                {
                    "input_text": '1. An email with the subject "Notes over Coffee" is sent to Brian Carter saying "I want to propose a coffee meeting to discuss our Triathlon Strategy Notes. What do you think?" is sent to the user.',
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
                # Milestone 0 – The agent looks up Brian Carter’s contact information
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
                # Milestone 1 – Confirms Brian Carter was found in the contact lookup
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
                                                "value": "Brian Carter",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "brian.carter@example.com",
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
                # Milestone 2 – A new email is sent to Brian with correct subject and body
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["brian.carter@example.com"]
                                    ],
                                    "subject": "Notes over Coffee",
                                    "status": "sent",
                                    "body": "coffee meeting",
                                    "creation_datetime_iso": "2024-12-08T10:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "subject": column_exact_match_similarity,
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
                (0, 1),  # Contact lookup leads to confirming Brian’s contact
                (1, 2),  # After contact confirmed, the email is sent
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_1e4a7919-a5a6-4fc3-a25a-338e5088f9a2_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_12",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
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
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know what time your meeting was at yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time was my event with Brian yesterday?",
                },
            ],
            reasoning="The user wants to know what time their event with Brian was on yesterday. Let me look in Calendar. I found similarly named event. It must be 'Triathlon Strategy Meeting with Brian and Team' on Saturday, December 7th, 2024. I will inform the user that their event ran from 15:00- 16:00.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their event 'Triathlon Strategy Meeting with Brian and Team' on December 7th ran from 15:00 -16:00.\n",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent queries the calendar to find yesterday’s event
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
                # Milestone 1 – Calendar search result contains the expected meeting with correct start time
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
                                                "value": "Triathlon Strategy Meeting with Brian and Team",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T15:00:00-08:00",
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
                # Milestone 2 – Agent informs the user of the correct meeting time
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
                                            "3 pm",
                                            "3 p.m.",
                                            "15:00",
                                            "3:00 pm",
                                            "3:00 p.m.",
                                            "3:00",
                                            "3pm",
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_9bb04e50-f13d-4148-80c9-d338c672a4ad_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_12",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T17:00:00-08:00",
            is_read_time="2024-12-07T17:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to reply to a recently received message in a thread about triathlon strategy. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to Brian and say Will do!",
                },
            ],
            reasoning='The user wants to reply to Brian Carter with the text "Will do!". First I\'ll find the contact by looking through messages for a chat with individuals going by this name. With this I can compose the reply and confirm that the user is happy to send it.',
            success_conditions=[
                {
                    "input_text": '1. A reply is sent to Brian Carter with the text "Will do!"',
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
                # Milestone 0 – Agent looks for the thread / messages with Brian
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
                # Milestone 1 – Confirm that the messages retrieval located the conversation with Brian Carter
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
                                            # Ensure Brian’s address is among the participants of at least one returned thread / message
                                            "participants_addresses": {
                                                "value": "brian.carter@example.com",
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
                # Milestone 2 – A new outgoing message “Will do!” is sent to Brian
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
                                                "+1 12345-6789-1000-7410",
                                                "brian.carter@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "Will do!",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-07T17:00:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # found messages → verified Brian’s presence
                (1, 2),  # after confirming, a reply is sent
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_0e51ffae-3c77-46ca-b71d-db8520158b60_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_12",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T20:00:00-08:00",
            is_read_time="2024-12-07T20:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to see what the last message in the triathlon strategy meeting session chat was. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Pull up the last message sent to the 'Triathlon Strategy Session' today.",
                },
            ],
            reasoning="I will check the users messages for the chat called ' Triathlon Strategy Session'. I found it. The last message was sent by Brian Carter at 16:45 on December 7th 2024. I present this message to the user.",
            success_conditions=[
                {
                    "input_text": "1. The message sent by Brian Carter on December 7th 2024 at 16:45 is presented to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
            milestones=[
                # Milestone 0 – Agent invokes a message-retrieval tool
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
                # Milestone 1 – The expected “Triathlon Strategy Session” message is present in the tool output
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
                                                "value": "Triathlon Strategy Session",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Let's keep this momentum going.",
                                                "partial": True,
                                            },
                                            "sender_address": {
                                                "value": "brian.carter@example.com",
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
                # Milestone 2 – Agent tells the user the content of the last message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Let's keep this momentum going.",
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
                (0, 1),  # Tool call → verify retrieved message
                (1, 2),  # Retrieved message → user-facing reply
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_a1997c05-0f93-46de-b60b-8ee3d0b56ae6_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_12",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
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
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to arrange a coffee meet up with Brian Carter to discuss the Triathlon Notes. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to go for coffee today with Brian Carter and go over the feedback for the triathlon strategy meeting. ",
                },
            ],
            reasoning="The user would like to arrange a coffee date today with team member Brian Carter and go over notes that were created from the Triathlon Strategy on December 7th. \n\nI will follow the email message thread created called Triathlon Strategy Meeting Notes and inquire if it is possible to create a meet up for coffee. When I receive a reply from Brian Carter I will arrange the date and time for coffee not the users calendar. ",
            success_conditions=[
                {
                    "input_text": "1. Message is sent to Brian Carter requesting a coffee meeting to discuss the recent email regarding Triathlon Strategy Notes. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up Brian Carter in the contacts database
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
                # Milestone 1 – Confirm the returned contact is Brian Carter
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
                                                "value": "Brian Carter",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "brian.carter@example.com",
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
                # Milestone 2 – A new outgoing message is sent to Brian Carter proposing coffee
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Ensure Brian is an explicit participant (by email or phone) – allow extras like Lucas
                                    "participants_addresses": [
                                        [
                                            (
                                                "brian.carter@example.com",
                                                "+1 12345-6789-1000-7410",
                                            )
                                        ]
                                    ],
                                    "content": "coffee",
                                    "creation_datetime_iso": "2024-12-08T10:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial state
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # contact search → verify Brian retrieved
                (1, 2),  # verified contact → message sent
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_47ece0fd-e25b-4d7e-acc0-ec2e44632d9a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_12",
                "contact",
                "email",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T19:35:00-08:00",
            is_read_time="2024-12-07T19:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are wondering what time you sent in your last email to Brian Carter "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I send that last email to Brian Carter",
                },
            ],
            reasoning="The user wants to know when they sent their last email to Brian Carter. First thing I need to do is search the user's emails. Ok I found an email sent to brian.carter@example.com at 16:15 on December 07, 2024. That must be the email the user is referring to. Ok now that I have that I will retrieve the time of the email and inform the user",
            success_conditions=[
                {
                    "input_text": "1. The time of the email sent by the user on December 07, 2024 at 16:15 to brian.carter@example.comis presented to the user",
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
                # Milestone 0 – Agent queries the email database to locate emails to Brian Carter
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
                # Milestone 1 – Verify the retrieved email is the one sent to Brian Carter at 2024-12-07T16:15:00-08:00
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
                                                "value": "brian.carter@example.com",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-07T16:15:00-08:00",
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
                            reference_milestone_node_index=0,  # depends on email search in Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – Agent tells the user the correct time (4:15 PM / 16:15)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("16:15", "4:15")],
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
            name="LUCAS_GARCIA_12_1d085856-492e-4c93-a960-73125ac6f094_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_12",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T10:10:00-08:00",
            is_read_time="2024-12-06T10:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to visit your parents for dinner but need to know what time you'll finish the meeting first. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is the strategy meeting over?",
                },
            ],
            reasoning="The user wants to know what time the strategy meeting is over. I should check the user's Calendar. \nHmm, looks like the user has only one event with this name, the Triathlon Strategy Meeting with Brian and Team from 15:00-16:00 on the 7 December 2024. The user wants to know the finishing time so I will check the event details. Looks like the event finishes at 16:00. I will let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. User is informed the Triathlon Strategy Meeting with Brian and Team from 15:00-16:00 on the 7 December 2024 finishes at 16:00.  ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 ─ The agent looks up calendar events
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
                # Milestone 1 ─ Confirm the correct meeting (and its end-time) was returned from the tool call in Milestone 0
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
                                                "value": "Triathlon Strategy Meeting with Brian and Team",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-07T16:00:00-08:00",
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
                # Milestone 2 ─ The user is informed that the meeting ends at 4 pm / 16:00
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
                                            "4:00",
                                            "4 pm",
                                            "4pm",
                                            "4 p.m.",
                                            "16:00",
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
            name="LUCAS_GARCIA_12_ca0360fc-1eeb-4a03-8885-4553742233bd_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_12",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T13:00:00-08:00",
            is_read_time="2024-12-08T13:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You're trying to think of what time you had the Triathlon meeting with Brian but it's escaping you.  You want to ask the assistant what time it was at. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Can you please tell me what time I had the "Triathlon Strategy Meeting with Brian and Team" event at?',
                },
            ],
            reasoning="The user is asking me what time their event \"Triathlon Strategy Meeting with Brian and Team\" occurred at. I'll search in their calendar for events with this name.... I only found one event which matches the exact criteria, an event which occurred on Saturday 7th December at 15:00. This has to be the event the user is referring to, so I'll show them the event as requested.",
            success_conditions=[
                {
                    "input_text": '1. The event information of "Triathlon Strategy Meeting with Brian and Team" on Saturday 7th December at 15:00-16:00 is shown to the user.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent queries the calendar database to find the requested event
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
                # Milestone 1 – Confirm the correct event (name and start time) was returned by the calendar query
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
                                                "value": "Triathlon Strategy Meeting with Brian and Team",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T15:00:00-08:00",
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
                # Milestone 2 – The agent tells the user the correct time of the meeting
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
                                            "3 pm",
                                            "3:00 pm",
                                            "3pm",
                                            "3 p.m.",
                                            "15:00",
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_ca0360fc-1eeb-4a03-8885-4553742233bd_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_12",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T13:00:00-08:00",
            is_read_time="2024-12-08T13:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You're trying to think of what time you had the Triathlon meeting with Brian but it's escaping you.  You want to ask the assistant what time it was at. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Will you help me figure out what time I had the triathlon meeting yesterday",
                },
            ],
            reasoning="The user is asking me what time they had the triathlon meeting yesterday. I need to try and figure out what meeting they are taking about. If today is Sunday 8th December 2024, then yesterday must be Saturday 7th December. I'll have a look in the user's calendar for anything that might match a 'triathlon meeting'....\n\nI found the event \"Triathlon Strategy Meeting with Brian and Team\" in the user's calendar for yesterday at 15:00-16:00. This is the only event that looks to match the user's criteria, so I'll show the event information to the user.",
            success_conditions=[
                {
                    "input_text": '1. The event information of "Triathlon Strategy Meeting with Brian and Team" on Saturday 7th December at 15:00-16:00 is shown to the user.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent queries the calendar to find the triathlon meeting
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
                # Milestone 1 – The queried calendar results include the correct triathlon meeting
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
                                                "value": "Triathlon Strategy Meeting with Brian and Team",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T15:00:00-08:00",
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
                # Milestone 2 – Agent tells the user the correct meeting time
                Milestone(
                    snapshot_constraints=[
                        # Must convey the correct time (3 pm / 15:00)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "3 pm",
                                            "3pm",
                                            "3:00 pm",
                                            "15:00",
                                            "3 p.m",
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_1d085856-492e-4c93-a960-73125ac6f094_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_12",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T10:10:00-08:00",
            is_read_time="2024-12-06T10:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to visit your parents for dinner but need to know what time you'll finish the meeting first. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is the event in the Conference Room finished?",
                },
            ],
            reasoning="The user wants to know when the event in the Conference Room is finished. I should check the user's Calendar for an event in the Conference Room. \nHmm, the user has multiple events this week. I need to check the event details of each event to see if any have the location set as Conference Room. \nLooks like only one event has the location set as Conference Room, the Triathlon Strategy Meeting with Brian and Team from 15:00-16:00 on the 7 December 2024. \nNext I will check the event details for the end time of this event. It looks like the event is scheduled to end at 16:00. I will let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. User is informed the Triathlon Strategy Meeting with Brian and Team from 15:00-16:00 on the 7 December 2024 finishes at 16:00.  ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent looks up calendar events (likely filtering by location “Conference Room”)
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
                # Milestone 1 – Confirm the “Triathlon Strategy Meeting …” ending at 16:00 was retrieved
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
                                                "value": "Triathlon Strategy Meeting with Brian and Team",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-07T16:00:00-08:00",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Conference Room",
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
                # Milestone 2 – Agent tells the user the meeting finishes at 16:00 / 4 pm
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
                                        ("16:00", "4 pm", "4:00 pm", "4pm", "4 p.m.")
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
                (0, 1),  # Event search → verify correct event found
                (1, 2),  # Correct event found → inform the user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_47ece0fd-e25b-4d7e-acc0-ec2e44632d9a_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_12",
                "contact",
                "email",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T19:35:00-08:00",
            is_read_time="2024-12-07T19:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are wondering what time you sent in your last email to Brian Carter "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I send that last email to my triathlon coach",
                },
            ],
            reasoning="The user wants to know when they sent their last email to their triathlon coach. First thing I need to do is search the user's contacts for \"triathlon coach\". I didn't find any with that name but I found Brian Carter who's alias is \"Triathlon coach\" so that must be who the user is referring to. I will now search the user's emails for emails to Brian Carter. Ok I found an email sent to brian.carter@example.com at 16:15 on December 07, 2024. That must be the email the user is referring to. Ok now that I have that I will retrieve the time of the email and inform the user",
            success_conditions=[
                {
                    "input_text": "1. The time of the email sent by the user on December 07, 2024 at 16:15 to brian.carter@example.comis presented to the user",
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
                # Milestone 0 – The agent looks through the user’s email to find the relevant message
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
                                    # Any one of the email-retrieval tools is acceptable
                                    target_tools=["search_emails", "get_all_emails"],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Confirm the correct email (to Brian Carter on 2024-12-07 16:15) appeared in the tool result
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
                                            # Must be an email to Brian Carter
                                            "recipients_addresses": {
                                                "value": "brian.carter@example.com",
                                                "partial": True,
                                            },
                                            # Must have the precise timestamp
                                            "creation_datetime_iso": {
                                                "value": "2024-12-07T16:15:00-08:00",
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
                            reference_milestone_node_index=0,  # Parse the output from Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – The agent actually tells the user the correct time
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
                                        ("4:15", "16:15")
                                    ],  # Accept either 4:15 PM or 16:15
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
            name="LUCAS_GARCIA_12_41d95ea9-b8de-427a-99c4-90cbdca4561d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_12",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T16:10:00-08:00",
            is_read_time="2024-12-07T16:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "Brian needs the strategy notes as soon as possible but you can't find his email. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Give me the triathlon coach's email address",
                },
            ],
            reasoning="The user is looking for a contact's email address.\nFirst, I should identify the contact the user is referring to. The user has indicated they are a triathlon coach, I can use this to narrow my search. I can see only one potential match, Brian Carter is tagged as working as a triathlon coach. This must be who the user is referring to.\n Brian Carter's email address is saved as brian.carter@example.com.\nI should provide this to the user.",
            success_conditions=[
                {
                    "input_text": "1. Brian Carter's email address, brian.carter@example.com, is provided to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts"],
            milestones=[
                # Milestone 0 – Agent queries contacts to locate the triathlon coach
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
                # Milestone 1 – Tool response contains Brian Carter with correct email
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
                                                "value": "Brian Carter",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "brian.carter@example.com",
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
                # Milestone 2 – Agent tells the user Brian’s email address
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "brian.carter@example.com",
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
            name="LUCAS_GARCIA_12_763bfa0a-84e1-4c0b-b9bb-c45e234dbb28_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_12",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T16:50:00-08:00",
            is_read_time="2024-12-07T16:50:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to dictate a reply to Triathlon Coach asking for your feedback from the session. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a reply to Brian Carter saying "Hey do you have my feedback from the training session yet"',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Brian Carter.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.\n",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message; "Hey do you have my feedback from the training session yet" is sent to Brian Carter at 16:50 on 7 December 2024. ',
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 –  The agent looks up Brian Carter in the contacts database
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
                # Milestone 1 –  Confirm that Brian Carter was part of the contact-search results
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
                                                "value": "Brian Carter",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "brian.carter@example.com",
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
                # Milestone 2 –  A new outgoing message to Brian Carter is created with the dictated content
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
                                                "lucas.garcia@example.com",
                                                "+1 12345-6789-1000-1234",
                                            ),  # Lucas Garcia
                                            (
                                                "brian.carter@example.com",
                                                "+1 12345-6789-1000-7410",
                                            ),  # Brian Carter
                                        ]
                                    ],
                                    "content": "Hey do you have my feedback from the training session yet",
                                    "creation_datetime_iso": "2024-12-07T16:50:00-08:00",
                                    "status": "sent",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                                "status": column_exact_match_similarity,
                            },
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact search -> verify Brian Carter found
                (1, 2),  # Contact confirmed  -> message sent
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_763bfa0a-84e1-4c0b-b9bb-c45e234dbb28_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_12",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T16:50:00-08:00",
            is_read_time="2024-12-07T16:50:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to dictate a reply to Triathlon Coach asking for your feedback from the session. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a reply message to Triathlon Coach saying "Hey do you have my feedback from the training session yet?"',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Triathlon Coach.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.\n",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message; "Hey do you have my feedback from the training session yet" is sent to Brian Carter at 16:50 on 7 December 2024. ',
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the Triathlon Coach contact information
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
                # Milestone 1 –  Confirm the contact lookup returned Brian Carter (Triathlon Coach)
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
                                                "value": "Brian Carter",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "brian.carter@example.com",
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
                # Milestone 2 – The agent looks up the Triathlon Coach contact information
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
                # Milestone 3 –  Confirm the contact lookup returned Brian Carter (Triathlon Coach)
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
                                                "value": "Triathlon Strategy Session",
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
                # Milestone 4 –  Verify a new message was sent to Brian Carter with the correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require it send to the conversation
                                    "conversation_name": "Triathlon Strategy Session",
                                    "content": "Hey do you have my feedback from the training session yet",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-07T16:50:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox traffic while checking messaging DB change
                ),
            ],
            milestone_edge_list=[(0, 1), (2, 3)],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_12_41d95ea9-b8de-427a-99c4-90cbdca4561d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_12",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T16:10:00-08:00",
            is_read_time="2024-12-07T16:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "Brian needs the strategy notes as soon as possible but you can't find his email. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Give me Brian Carter's email address.",
                },
            ],
            reasoning="The user is asking for a contact's email address.\nFirst, I should find the named person in the user's contacts.\nI have found Brian Carter.  \nBrian Carter's email address is saved as brian.carter@example.com. I should provide this to the user.",
            success_conditions=[
                {
                    "input_text": "1. Brian Carter's email address, brian.carter@example.com, is provided to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts"],
            milestones=[
                # Milestone 0 – The agent tries to look up Brian Carter in contacts
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
                # Milestone 1 – The user receives Brian Carter’s email address
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "brian.carter@example.com",
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
                (0, 1),  # Contact lookup precedes informing the user
            ],
        ),
    ]
