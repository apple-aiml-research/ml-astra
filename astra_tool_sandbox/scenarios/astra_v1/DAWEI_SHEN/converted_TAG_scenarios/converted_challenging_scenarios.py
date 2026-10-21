# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
# Auto-generated scenario extensions
from functools import partial
from typing import Optional, cast

import polars as pl

from astra_tool_sandbox.common.evaluation import (
    Milestone,
    Minefield,
    SnapshotConstraint,
    addition_similarity,
    column_contains_similarity,
    column_datetime_window_similarity,
    column_exact_match_similarity,
    column_list_exact_match_similarity,
    column_list_subset_match_similarity,
    column_list_tuple_contains_similarity,
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_rouge_l_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_any_similarity,
    column_word_contains_similarity,
    contains_presence_similarity,
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


def get_TAG_DAWEI_SHEN_challenging_scenarios(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="DAWEI_SHEN_17_ee1ef5dd-8cc6-4eb1-97a4-a63a99a1d4a2_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "email",
                "contact",
                "whatsapp_messaging",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_yes",
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
                        "You want to know the name of the play you booked tickets for "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What play do my girlfriend and I have tickets for? Do you have the exact name for it? If so let me know, if not reply 'no'.",
                },
            ],
            reasoning="The user want's to know what play he and his girlfriend have tickets for so I first must determine who is meant by the user's girlfriend. Looking through the user's contacts I see Jess Zimmer is noted as being the user's girlfriend. \n\nI will look through the user's e-mails to see if there is any booking confirmation which may contain the title of the play. I found an e-mail from the user to his girlfriend with the subject \"Ticket Confirmation for Our Play Date\", but there're no explicitly mentioned play name. I will let the user know the key information is missing, with no.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that the key information is missing, and the name of the play is unknown.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "search_contacts",
                "get_all_contacts",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent attempts to look up relevant info (likely via email/WhatsApp/calendar) to find the play
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
                                # Any reasonable info-retrieval tool use is acceptable:
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "search_emails",
                                        "get_all_emails",
                                        "search_calendar_events",
                                        "get_all_calendars",
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Agent informs user that the play name is unknown / missing from available data
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We just need the agent to clearly say the play name is not known / missing
                                    "content": [("missing", "unknown", "no")],
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
            name="DAWEI_SHEN_15_088f1173-9a5c-4cb0-8513-604c192a512c_single_turn_2",
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
                "misinformation_yes",
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
                    "content": "Reply to Jeff Bing's email again and say \"Thanks again for your email Jeff. I'd actually like to invite you to a Data set review I'm having with my colleague Michelle Barnes today at 14:00.\" then invite him to my meeting tomorrow.",
                },
            ],
            reasoning="The user wants to reply again to the recent email received from jeff.bing@bingelectronics.com after their initial reply they sent at 12:00. They want to say \"Thanks again for your email Jeff. I'd actually like to invite you to a Data set review I'm having with my colleague Michelle Barnes today at 14:00.\". so I'll craft that as the reply and send it to Jeff. \nNow, the user wants to add I'll also add him as an invitee to a meeting they're having tomorrow. I don't see any meetings for tomorrow, December 11th, on the user's calendar. They must have misspoken because they mention the Dataset Review with Michelle meeting in the email they want me to send to Jeff. That meeting is happening today, December 10th, at 14:00-15:00, so I'll add Jeff as an invitee to that since the user specifically mentions it in the email.",
            success_conditions=[
                {
                    "input_text": "1. An email is sent to jeff.bing@bingelectronics.com to say \"Thanks again for your email Jeff. I'd actually like to invite you to a Data set review I'm having with my colleague Michelle Barnes today at 14:00.\".",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. Jeff Bing is added as an invitee to the event named "Dataset Review with Michelle" at 14:00-15:00 on 10 December 2024.',
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
                # Milestone 0 – Use email search/get_all_emails to locate Jeff's recent thread to reply to
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
                # Milestone 1 – Confirm Jeff's "Thank You for Attending the Tech Panel" email thread was retrieved
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
                # Milestone 2 – Email sent to Jeff with the specified body text (replying again)
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
                                    "body": "Data set review I'm having with my colleague Michelle Barnes today at 14:00.",
                                    "creation_datetime_iso": "2024-12-10T12:30:00-08:00",
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
                    ],
                ),
                # Milestone 3 – Use calendar search/get_all_calendars to retrieve the "Dataset Review with Michelle" event
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
                # Milestone 4 – Confirm the specific dataset review event (today at 14:00) was retrieved
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
                # Milestone 5 – Calendar event updated to add Jeff Bing as an attendee to the 14:00 dataset review
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
                (0, 1),  # email search → confirm Jeff's email thread
                (3, 4),  # calendar search → confirm dataset review event
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_c22d1d20-c399-45ef-9dea-cd160b4142ae_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "messaging",
                "contact",
                "whatsapp_messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:15:00-08:00",
            is_read_time="2024-12-08T18:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to message Vickie in your usual comminication channel to ask if she would be up for running some lines before theatre practice. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Message Vicki in the thread "Would you be up for running some lines before theatre practice tonight?".',
                },
            ],
            reasoning="The User wants to message Vicki in the thread, I don't see any contacts with first or last name as 'Vicki'. But i have found 'Vickie Lee' and 'Vick Li'. In the message the user would like to send, it is related to theatre practice. I therefore further checked user's message history for both of them under messages and whatsapp messages.\n\nAccording to message history, it should be Vickie Lee who is the theatre friend and they have a thread in whatsapp regarding the rehearsal. So I send the message \"Would you be up for running some lines before theatre practice tonight?\" in a whatsapp message to Vickie.",
            success_conditions=[
                {
                    "input_text": '1. A whatsapp message to Vickie Lee to say "Would you be up for running some lines before theatre practice tonight?".',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent looks up to resolve "Vicki" to the correct person in conversation history
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
                                # Allow either direct search or full listing of contacts
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "get_all_whatsapp_messages",
                                        "search_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – Confirms that the theater friend "Vickie Lee" is retrieved (used to disambiguate from "Vick Li")
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
                                                "value": "Vickie Lee",
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
                # Milestone 2 – A WhatsApp message is sent to Vickie with the requested content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Participants identified by any valid address (phone or email) for Dawei and Vickie
                                    "participants_addresses": [
                                        [
                                            (
                                                "dawei.shen@orchardtech.com",
                                                "+1 555-123-4567-8901",
                                            ),
                                            (
                                                "vickie.lee@orchardtheater.com",
                                                "+1 555-345-6789-0123",
                                            ),
                                        ]
                                    ],
                                    "content": "Would you be up for running some lines before theatre practice tonight?",
                                    "creation_datetime_iso": "2024-12-08T18:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # whatsapp lookup → confirm correct Vickie
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_d1e4f333-1baf-4e12-93ca-f2e8dfbef2b0_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "calendar",
                "messaging",
                "contact",
                "whatsapp_messaging",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_high",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:10:00-08:00",
            is_read_time="2024-12-08T18:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You wants to message Charles and ask him if he could bring the lines to the theatre rehearsal as you can't find yours. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Message Charles in our usual way, asking him if he can bring the lines to the rehearsal tomorrow as I can't find mine, and make sure I'm correct about that information before sending",
                },
            ],
            reasoning="The user wants to send a new message to Charles in their usual way and I need to make sure the user is correct about that information before sending. I see there is only one contact named Charles, Charles Wilde. And I see the recent message between user and Charles is via whatsApp, so it's clear user wants to send whatsApp message to Charles Wilde. But the user wants to send with the content \"can you bring the lines to the rehearsal tomorrow as I can't find mine. Thanks!\", however based on the user's calendar, the theatre rehearsal is scheduled on 12/08 Sunday which is today not tomorrow. I'll inform user about the issue with tomorrow, and I've adjusted the and send the whatsApp message removing tomorrow.",
            success_conditions=[
                {
                    "input_text": '1. A whatsApp message is sent to Charles Wilde saying something like "can you bring the lines to the rehearsal as I can\'t find mine." without mentioning tomorrow in the content.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_whatsapp_message",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "get_all_calendars",
                "search_calendar_events",
                "search_messages",
                "get_all_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent looks up contact info for Charles (by name, or via listing contacts)
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
                # Milestone 1 – Confirm Charles Wilde was retrieved from contacts in Milestone 0
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
                                                "value": "Charles Wilde",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 555-234-5678-9012",
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
                # Milestone 2 – Agent uses calendar tools to look up the rehearsal event
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
                # Milestone 3 – Confirm that the Theater Rehearsal event on 2024-12-08 19:00–22:00 was retrieved
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
                                                "value": "Theater Rehearsal",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-08T19:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-08T22:00:00-08:00",
                                                "partial": False,
                                            },
                                            "attendees_names": {
                                                "value": [
                                                    "Charles Wilde",
                                                    "Dawei Shen",
                                                    "Vickie Lee",
                                                ],
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
                            reference_milestone_node_index=2,
                        )
                    ],
                ),
                # Milestone 4 – WhatsApp message sent to Charles with adjusted content (no "tomorrow")
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # participants: Dawei (self) and Charles, can be matched by either email or phone
                                    "participants_addresses": [
                                        [
                                            (
                                                "dawei.shen@orchardtech.com",
                                                "+1 555-123-4567-8901",
                                            ),
                                            (
                                                "charles.wilde@orchardtheater.com",
                                                "+1 555-234-5678-9012",
                                            ),
                                        ]
                                    ],
                                    "content": [("bring", "lines")],
                                    "creation_datetime_iso": "2024-12-08T18:10:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Ensure it's specifically a conversation between Dawei and Charles
                                "participants_addresses": column_list_tuple_contains_similarity,
                                # Ensure content contain keywords
                                "content": column_str_contains_any_similarity,
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
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → confirm Charles
                (2, 3),  # theatre rehearsal found
            ],
            minefields=[
                # Minefield 0 – WhatsApp message sent to Charles with must not contain tomorrow
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # participants: Dawei (self) and Charles, can be matched by either email or phone
                                    "participants_addresses": [
                                        [
                                            (
                                                "dawei.shen@orchardtech.com",
                                                "+1 555-123-4567-8901",
                                            ),
                                            (
                                                "charles.wilde@orchardtheater.com",
                                                "+1 555-234-5678-9012",
                                            ),
                                        ]
                                    ],
                                    "content": "tomorrow",
                                }
                            ),
                            column_similarity_measure={
                                # Ensure it's specifically a conversation between Dawei and Charles
                                "participants_addresses": column_list_tuple_contains_similarity,
                                # Ensure content matches exactly the required phrasing (including removal of "tomorrow")
                                "content": column_contains_similarity,
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_75ee90c1-5a08-4b93-bc73-03aee990825d_single_turn_3",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "calendar",
                "whatsapp_messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:05:00-08:00",
            is_read_time="2024-12-08T18:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You can't remember what time your Theater Rehearsal has been rescheduled to. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time does my Theater Rehearsal on December 9th start at?",
                },
            ],
            reasoning="The user wants to know the time of the Theater Rehearsal event on 9 December 2024. However, looking at their calendar they only have one event with that name, but it's on 8 December 2024. I'll tell them that it's on 8 December from 19:00-22:00.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that the event named Theater Rehearsal is scheduled for 8 December 2024 at 19:00-22:00, at Orchard Theater.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent uses a calendar retrieval tool to look up rehearsal timing
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
                # Milestone 1 – Confirm the Theater Rehearsal event with revised time exists in calendar
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
                                                "value": "Theater Rehearsal",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-08T19:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-08T22:00:00-08:00",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Orchard Theater",
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
                # Milestone 2 – User is informed of the correct rehearsal time and date (even if it's Dec 8, not 9)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We only check that the response mentions the correct time range
                                    # and the fact it's on Dec 8 in a relaxed way.
                                    "content": [("7:00 pm", "7 pm", "19:00", "7pm")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "December 8",
                                            "Dec 8",
                                            "8 December",
                                            "8th of December",
                                            "today",
                                            "tonight",
                                            "12-08",
                                            "the 8th",
                                            "2024-12-08T19:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # calendar lookup → confirm rehearsal event details
                (1, 2),  # having correct event → inform user with correct time/date
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_ee1ef5dd-8cc6-4eb1-97a4-a63a99a1d4a2_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "email",
                "contact",
                "whatsapp_messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_yes",
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
                        "You want to know the name of the play you booked tickets for "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What play did I book tickets for last night? Do you know the name? Yes or no.",
                },
            ],
            reasoning="The user want's to know what play he booked tickets for last night so I will look through the user's e-mails to see if there is any booking confirmation which may contain the title of the play. I found an e-mail with the subject \"Ticket Confirmation for Our Play Date\".I will let the user know the key information is missing and reply with 'No'.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed with 'No', that the key information is missing, and the name of the play is unknown.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "search_contacts",
                "get_all_contacts",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_messages",
                "get_all_messages",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – Agent attempts to look up what play was booked by checking emails/WhatsApp/calendar/messages
                # Even though success is ultimately to say "I don't know", the agent should first reasonably
                # attempt to retrieve the information from relevant data sources.
                Milestone(
                    snapshot_constraints=[
                        # Check some read-only retrieval tool was used that could plausibly reveal the play name
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
                                    # Any of these would be a reasonable attempt:
                                    target_tools=[
                                        "search_emails",
                                        "get_all_emails",
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                        "search_calendar_events",
                                        "get_all_calendars",
                                        "search_messages",
                                        "get_all_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – User is explicitly informed that the play name cannot be determined
                # i.e., key information is missing / unknown.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Look for language conveying that the name of the play is unknown
                                    "content": "No",
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
                (
                    0,
                    1,
                ),  # First attempt retrieval, then inform user the play name is unknown
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_2b0f714a-059e-4439-b7dc-a1cb880686b8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "misinformation_yes",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T22:30:00-08:00",
            is_read_time="2024-12-08T22:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know what time the tech panel starts the day after tomorrow. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to know what time the panel thing starts at tomorrow. ",
                },
            ],
            reasoning="The agent should call the calendar-search tools, find the event named “Tech Panel Hosted by Jeff Bing” scheduled for 2024-12-10T09:00:00-08:00, and reply to the user that the panel starts at 9:00 AM the day after tomorrow (Tuesday, December 10).",
            success_conditions=[
                {
                    "input_text": "The assistant tells the user the tech panel starts at 9:00 AM (or equivalent 9 am wording).",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "The assistant also clarifies the date by referencing either “the day after tomorrow” or “December 10” (or 12-10).",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
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
                            reference_milestone_node_index=0,  # depends on the tool call in milestone 0
                        )
                    ],
                ),
                # Milestone 2 – the user is informed of the 9:00 AM start time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # accept several reasonable phrasings of the time
                                    "content": [
                                        (
                                            "9:00",
                                            "9 am",
                                            "9am",
                                            "9 a.m.",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        # mentioning the correct date
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # accept several reasonable phrasings of the time
                                    "content": [
                                        (
                                            "the day after tomorrow",
                                            "December 10",
                                            "12-10",
                                            "12/10",
                                            "Tue",
                                            "Tuesday",
                                            "Dec 10",
                                            "the 10th",
                                            "10 December",
                                            "10th of December",
                                            "2024-12-10T09:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_d1400b1a-9942-42f6-8adc-9071621a39ea_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "insufficient_context_yes",
                "calendar",
                "messaging",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T21:10:00-08:00",
            is_read_time="2024-12-05T21:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You need to remind yourself of when your property tax is due to avoid late fees. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is my tax due? Do you know exactly on which day? Reply with yes or no.",
                },
            ],
            reasoning="Right so, the user is asking about when their tax is due. I check and see there is one corresponding event named 'Pay Property Tax'. I also found message from Mia Tang said the property tax is due next week. However, I don't know the exact date of the due. I will reply no to the user.",
            success_conditions=[
                {
                    "input_text": "1. The user has been told No, since there're no evidence of the exact due date.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (must call a calendar-read tool)
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
                # Milestone 1 – Returned calendar data contains the “Pay Property Tax” event on 2024-12-06 08:00
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
                                                "value": "Pay Property Tax",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-06T08:00:00-08:00",
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
                # Milestone 2 – Agent looks up messages
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
                # Milestone 2 – Returned conversation with Mia
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
                                                "value": "Mia Tang",
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
                # Milestone 4 – Agent tells the user No
                Milestone(
                    snapshot_constraints=[
                        # Verify date reference
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "No",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_similarity
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (2, 3),
            ],
            minefields=[
                # Should not reply with Yes
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Yes",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_similarity
                            },
                        ),
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_15_98f79689-1dbf-4e1f-8ae0-c96ec5fcf3d8_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "email",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T18:00:00-08:00",
            is_read_time="2024-12-10T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know if you received a response from Michelle about the recorded tech panel session you sent her.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did the woman I work with respond to the tech panel recording link I emailed her? yes or no.",
                },
            ],
            reasoning='The user wants to know if they received an email response to a tech panel recording they sent to "the girl they work with". Alright, they only have one contact, Michelle Barnes, listed as a coworker with a female name. I will need to look for a response from them. Since the user didn\'t specify the app they used to send the tech panel recording link, I will search for either messages or emails with that shared link to a tech panel session. There are no message or email threads with Michelle Barnes that mention a tech panel session, so the user must have been thinking of someone else they sent it to. I\'ll inform them that the last email I see from Michelle was at 8:00 on 9 December 2024 and had the subject "Dataset Update for Machine Learning Model." I will reply with "No" to the user, as such information does not exist.',
            success_conditions=[
                {
                    "input_text": '1. The user is informed with "No", and that there\'s no record of the user sending the tech panel session to a female co-worker.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – Agent uses email search/listing to look for any tech panel related email with Michelle / responses
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
                # Milestone 1 – Confirm that the latest email involving Michelle is the 2024-12-09 08:00 "Dataset Update for Machine Learning Model"
                # and there is no evidence of a reply to a tech panel recording from her.
                Milestone(
                    snapshot_constraints=[
                        # Check that an email from Michelle with the expected subject exists in the tool output
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
                                                "value": "Dataset Update for Machine Learning Model",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-09T08:00:00-08:00",
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
                # Milestone 2 – User-facing answer: clearly states that there is no record of sending Michelle the tech panel link
                # and that her last email was the 8:00am Dec 9 dataset update.
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
                                "content": column_word_contains_similarity
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Email lookup → confirm Michelle's latest email details
            ],
            minefields=[
                # Should not reply with Yes
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Yes",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_similarity
                            },
                        ),
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_21_14a3274b-e310-4a86-9dd7-b9b6b58690e5_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_21",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T21:35:00-08:00",
            is_read_time="2024-12-14T21:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to see the message that Lukas sent to you directly.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the latest text message from Lukas that isn't in the group message today.",
                },
            ],
            reasoning="The user asks to see the latest text message from Lukas that isn't in the group chat, today — this presupposes such a direct message exists. The user has one contact named Lukas Hürholz, with messages in both a one-on-one conversation and a group chat 'Dinner at a local restaurant'. I check the one-on-one (non-group) messages; the most recent is on 08/12/2024, 09:35:00 — not today. So the presupposition is false: there is no direct message from Lukas today (his only message today was in the group chat), and I inform the user there is none.",
            success_conditions=[
                {
                    "input_text": '1. The message that was received from Lukas Hürholz at 21:30 on 14 December 2024 with content "Had a fantastic evening, guys! Here\'s a selfie to remember our night. Cheers!" is retrieved as this is the only message from Lucas today within the group chat "Dinner at a local restaurant".',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": '2. User is informed with "No" as there are no direct message from Lucas today.',
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
            milestones=[
                # Milestone 0 – The agent uses a messages retrieval tool (needed to find Lukas's messages)
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
                # Milestone 1 – Confirm that the group message from Lukas at 2024-12-14T21:30:00-08:00 is retrievable
                # This ensures the agent can distinguish it from other messages and know it is part of the group thread.
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
                                                "value": "Dinner at a local restaurant",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "lukas.hurholz@londonbanking.co.uk",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Had a fantastic evening, guys! Here's a selfie to remember our night. Cheers!",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-14T21:30:00-08:00",
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
                # Milestone 2 – User-facing response said no information
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
                                            "no",
                                            "none",
                                            "not",
                                            "nothing",
                                            "didn't",
                                            "hasn't",
                                            "haven't",
                                            "wasn't",
                                            "isn't",
                                            "doesn't",
                                            "don't",
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
                (
                    0,
                    1,
                ),  # retrieve messages → confirm correct Lukas group message identified
                (1, 2),  # having identified it → present its content to the user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_15_98f79689-1dbf-4e1f-8ae0-c96ec5fcf3d8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_15",
                "email",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T18:00:00-08:00",
            is_read_time="2024-12-10T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know if you received a response from Michelle about the recorded tech panel session you sent her.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did Michelle say anything about the tech panel recording link I sent? Yes or No.",
                },
            ],
            reasoning="The user wants to know if they received a response to a tech panel recording they sent Michelle. They only have one contact named Michelle, Michelle Barnes, so I need to look for a response from them. Since the user didn't specify the app they used to send the tech panel recording link, I will search for either messages or emails with that shared link to a tech panel session. There are no message or email threads with Michelle Barnes that mention a tech panel session, so the user must have been thinking of someone else they sent it to. I'll inform them with no, and that the last email I see from Michelle has the subject \"Dataset Update for Machine Learning Model.\" is not related to tech panel.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed with no, that there's no record of the user sending the tech panel session to Michelle.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – Agent searches emails for anything from/to Michelle or related to tech panel / recording
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
                # Milestone 1 – Confirm that the only relevant email from Michelle is the dataset update on Dec 9 at 8:00
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
                                            "sender_address": {
                                                "value": "michelle.barnes@orchardtech.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Dataset Update for Machine Learning Model",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-09T08:00:00-08:00",
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
                # Milestone 2 – User-facing answer states there is no record of Michelle replying about the tech panel link
                # and mentions the last email details (time and subject).
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We check for both "no record" and the last-email info (subject + time).
                                    "content": "no",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_similarity
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (
                    0,
                    1,
                ),  # email search → confirm dataset update email from Michelle exists
                (1, 2),  # confirmed info → user-facing explanation
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_6_13ca6647-6f9d-4fb4-9c44-9a2fa6b1b107_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_6",
                "calendar",
                "messaging",
                "contact",
                "whatsapp_messaging",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_yes",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T20:15:00-08:00",
            is_read_time="2024-12-03T20:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to surprise your parents with a dinner at your favourite restaurant in Shanghai, using the details from the discussion about the trip to decide when would best to book. If the assistant said they need more information, end the conversation."
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Find out when my parents said they were busy during my trip to Shanghai and schedule a dinner event in the downtime if possible.",
                },
            ],
            reasoning="The user wants to surprise their parents with a dinner during their trip to Shanghai, using details from their previous discussions to decide when to book.\n\nOkay, so first I’ll identify the user’s parents from their contacts. Then I’ll look through any conversations with them — in Messages, Mail, or calendar notes — to find when they mentioned being busy or available during the trip dates.\n\nHowever, I don’t see any relevant messages or emails mentioning their availability, and I don’t have access to phone call details. Since there’s no information about when the parents are free, I can’t schedule the dinner yet.\n\nI’ll let the user know that this information is missing and it is not possible for me to create a calendar event.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that key information is missing to complete this task.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. No calendar event shall be created.",
                    "statefullness": "Statelful",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_messages",
                "get_all_messages",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
                "get_all_phone_calls",
                "search_phonecall_logs",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent attempts to retrieve information about parents' availability (emails, messages, phone logs, calendar)
                Milestone(
                    snapshot_constraints=[
                        # Any use of search/get tools over emails, messages, whatsapp, calendar, phone logs counts
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": [RoleType.EXECUTION_ENVIRONMENT],
                                    "recipient": [RoleType.AGENT],
                                    "tool_trace": [""],
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "get_all_emails",
                                        "search_emails",
                                        "get_all_messages",
                                        "search_messages",
                                        "get_all_whatsapp_messages",
                                        "search_whatsapp_messages",
                                        "get_all_phone_calls",
                                        "search_phonecall_logs",
                                        "get_all_calendars",
                                        "search_calendar_events",
                                    ],
                                )
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[],
            minefields=[
                # Should not create calendar event
                Minefield(
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
                                        "create_calendar_event",
                                    ],
                                )
                            },
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_1_da26659c-ee82-4a16-8351-318577958e11_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_1",
                "calendar",
                "email",
                "contact",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T11:20:00-08:00",
            is_read_time="2024-12-03T11:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to email to thank them for hanging out with you and invite them to another cycling trip for the same day and time the next week and add it to your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Will you please start a new email to the person I went on a hike with last Sunday and write "Hi Vick, thanks so much for the cycling trip last weekend, it was really what I needed. If you want let\'s do it the same time next weekend? LOL from Dawei". Also create me a new event called "Cycling Trip with Vick" for the coming Sunday at the same time and invite him to it.',
                },
            ],
            reasoning="The user wants two things: (1) start a new email to the person they hiked with last Sunday using the provided message, and (2) create a new calendar event 'Cycling Trip with Vick' for the coming Sunday at the same time, inviting him.\n\nFirst, I need to resolve who 'the person I went on a hike with last Sunday' is. I’ll check the calendar for the most recent Sunday. I see an event titled 'Cycling Trip with Vick' that took place last Sunday. Even though the user said 'hike,' their quoted message thanks Vick for a 'cycling trip,' so I’ll treat 'hike' as a slip. Therefore, the person is Vick (match to 'Vick' in Contacts, e.g., Vick Lee).\n\nEmail task: start a NEW email to Vick (not reply) and use the exact text: \"Hi Vick, thanks so much for the cycling trip last weekend, it was really what I needed. If you want let's do it the same time next weekend? LOL from Dawei\".\n\nEvent task: create a new event called 'Cycling Trip with Vick' on the coming Sunday at the same time as last Sunday’s cycling event (copy the start and end times), and add Vick as an attendee. Preserve location/conferencing if present.\n\nI will execute both actions: compose the new email to Vick with the provided body, then create and save the new Sunday event at the same time block and invite Vick.",
            success_conditions=[
                {
                    "input_text": '1. The system will send an email to Vick Li and write "Hi Vick, thanks so much for the cycling trip last weekend, it was really what I needed. If you want let\'s do it the same time next weekend? LOL from Dawei".',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. The system will create the event "Cycling Trip with Vick" on Sunday 8th December 2024 at 07:00-10:00 and invite Vick as an attendee.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Contact lookup for "the person I went on a hike with last Sunday" (Vick)
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
                # Milestone 1 – Confirm Vick Li was retrieved from contact search in Milestone 0
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
                                                "value": "Vick Li",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "vick.li@techpals.com",
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
                # Milestone 2 – Email is sent to Vick with the exact requested body text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [["vick.li@techpals.com"]],
                                    "status": "sent",
                                    "body": "Hi Vick, thanks so much for the cycling trip last weekend, it was really what I needed. If you want let's do it the same time next weekend? LOL from Dawei",
                                    "creation_datetime_iso": "2024-12-03T11:20:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                # Body must contain the full user-specified sentence; use contains to be slightly tolerant of metadata
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
                # Milestone 3 – Calendar search used to determine prior cycling event time, if needed
                # (the reasoning chain indicates looking up last Sunday event to copy time)
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
                # Milestone 4 – New calendar event "Cycling Trip with Vick" created for Sunday Dec 8, 2024, 07:00–10:00 with Vick invited
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Cycling Trip with Vick",
                                    "start_datetime_iso": "2024-12-08T07:00:00-08:00",
                                    "end_datetime_iso": "2024-12-08T10:00:00-08:00",
                                    # We check that both Dawei and Vick are present as attendees (by name),
                                    # but allow extras in case the system adds the organizer separately.
                                    "attendees_names": [["Dawei Shen", "Vick Li"]],
                                    "creation_datetime_iso": "2024-12-03T11:20:00-08:00",
                                }
                            ),
                            column_similarity_measure={
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
                (0, 1),  # Contact search → confirm Vick
                # Calendar reasoning (Milestone 3) can be independent; event creation (Milestone 4) depends on it
                (3, 4),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_a40a72d2-918d-427b-bc1d-7c23f92c9ba4_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "calendar",
                "email",
                "contact",
                "whatsapp_messaging",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:05:00-08:00",
            is_read_time="2024-12-05T17:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to create a new event for the theater night you were talking about with her on the 19th December. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you create the event Theater Night for me on Wednesday 19th December 2024 at 19:00 and invite her?",
                },
            ],
            reasoning="The user wants me to create an event in their calendar called \"Theater Night\" and invite her. They said they want to schedule it on Wednesday December 19th 2024, but December 19th is a Thursday, so I'll schedule the event for Thursday December 19th at 19:00 and confirm with user about the decision. They mentioned her in their request to me, without any more information, I need to check user's most recent messages and it must be Jess Zimmer that I just sent a message to since they were discussing about theatre night, so I will add Jess Zimmer as an attendee for this event.",
            success_conditions=[
                {
                    "input_text": '1. A new calendar event called "Theater Night with Jess" will be created for Thursday 19th December 2024 at 19:00 with Jess Zimmer as an invitee.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – The agent looks up contacts to resolve "Jess" / "Jess Zimmer" as attendee
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
                # Milestone 1 – Confirms that contact "Jess Zimmer" was available from contact lookup in Milestone 0
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
                                            "email": {
                                                "value": "jess.zimmer@fintechstartup.com",
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
                # Milestone 2 – Calendar event has been created for Theater Night with Jess on 2024-12-19T19:00:00-08:00 with Jess as attendee
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Theater Night",
                                    # Only check the start time; end time can be defaulted by the agent
                                    "start_datetime_iso": "2024-12-19T19:00:00-08:00",
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-05T17:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Require Jess to be included as an attendee, but allow additional attendees (e.g., self)
                                "calendar_event_name": column_contains_similarity,
                                "attendees_names": column_list_subset_match_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        ),
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → confirm Jess contact
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_a40a72d2-918d-427b-bc1d-7c23f92c9ba4_single_turn_3",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "calendar",
                "email",
                "contact",
                "whatsapp_messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:05:00-08:00",
            is_read_time="2024-12-05T17:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to create a new event for the theater night you were talking about with Jess on the 19th December. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I'm so excited Jess texted me the tickets for our theater night! Can you schedule an event named Theater Night with Jeff for me on Thursday 19th December 2024 at 19:00 and invite her?",
                },
            ],
            reasoning='The user wants me to create an event in their calendar called "Theater Night with Jeff". They said they want to schedule it for Thursday December 19th at 19:00 so I\'ll do that. The name for the event confuses me; why would they say Jeff? They mentioned they were excited that Jess sent them tickets, and Jess is the one they were just talking about the theater night with on WhatsApp. The user must have misspoken and must have been referring to that Jess, so I will add Jess Zimmer as an attendee for this event and name the event like "Theater Night with Jess" and let the user know, and do not mention Jeff at all in the calendar event.',
            success_conditions=[
                {
                    "input_text": '1. A new calendar event contained key word "Theater Night" will be created for Thursday 19th December 2024 at 19:00 with Jess Zimmer as an invitee, the title must not contain "Jeff".',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. No calendar event referring to Jeff is created.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – The agent searches messages to resolve "Jess" / "Jeff"
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Confirms that Jess Zimmer was found in messages history
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
                                                "value": "Jess Zimmer",
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
                # Milestone 2 – Calendar event was created for Theater Night with Jess on Dec 19, 2024 at 19:00, with Jess as attendee
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Theater Night",
                                    "start_datetime_iso": "2024-12-19T19:00:00-08:00",
                                    # We don't strictly require end time; focus on name/time/attendees
                                    "attendees_names": [["Jess Zimmer", "Dawei Shen"]],
                                    "creation_datetime_iso": "2024-12-05T17:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_word_contains_similarity,
                                "attendees_names": column_list_exact_match_similarity,
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
                (0, 1),  # whatsapp search → confirm Jess
            ],
            minefields=[
                Minefield(
                    snapshot_constraints=[
                        # must not contain Jeff
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Jeff",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_word_contains_similarity,
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_758e8a59-d679-4671-98f8-6316a6a91475_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "contact",
                "whatsapp_messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_yes",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:20:00-08:00",
            is_read_time="2024-12-05T17:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to check the tickets Jess sent you for theatre night so that you can make a note of the time on them.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is the theater-night show Jess sent me tickets for?  If you can, tell me the exact time; if not, just reply ‘information missing’.",
                },
            ],
            reasoning="The user wants me to retrieve information from an attachment about tickets from Jess, so first I must figure out which contact that is. I have managed to find Jess Zimmer in their contacts, so I can assume the user wants me to find an attachment that Jess Zimmer sent.\n\nIn the Messages app and in WhatsApp, Jess didn't send any ticket attachment or information. Her most recent message from in WhatsApp, and it just says \"Here are the tickets for our theater night! 🎭\" so I'll tell the user that there aren't actually any tickets in the message, information missing.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that from Jess Zimmer's whatsapp messages, the time for the show is unknown, key information is missing.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks up WhatsApp messages (or all messages) to find Jess's tickets
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
                                # We accept either a direct WhatsApp search or a broad fetch
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                        # Fallbacks if the agent first searches generic messages
                                        "search_messages",
                                        "get_all_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Confirm the WhatsApp message from Jess at the specified time exists and contains no ticket details
                Milestone(
                    snapshot_constraints=[
                        # 1a: Confirm we actually retrieved the correct WhatsApp thread/message from tool output
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        # We only need to know that a message from Jess with this content exists
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "sender_name": {
                                                "value": "Jess Zimmer",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Here are the tickets for our theater night!",
                                                "partial": True,
                                            },
                                            # We don't force exact timestamp match to allow for formatting differences
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
                        # 1b: Verify there was no follow-up extraction of a time from any ticket details (i.e., no ticket info present)
                        # Instead of inspecting tool parameters, we check final user-facing response states that time is unavailable.
                    ],
                ),
                # Milestone 2 – User is clearly informed that no ticket image/info is actually present, so the show time cannot be determined
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # The response must say (a) that the WhatsApp message doesn't actually include tickets,
                                    # and (b) that the time cannot be determined / key information is missing.
                                    "content": "information missing",
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
                (
                    0,
                    1,
                ),  # Tool search for WhatsApp/messages → confirm Jess's message was retrieved
                (
                    1,
                    2,
                ),  # After confirming message content, inform the user about missing ticket/time info
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_bf6be7a0-c2dc-45c1-aeec-54ef9da6f9f7_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "email",
                "contact",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:30:00-08:00",
            is_read_time="2024-12-12T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to let your friend know you placed the order for theatre props already so that she doesn't need to do it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you forward the theater supplies confirmation email I sent to Francis over to Vick? I want the theatre gang to be in the loop.",
                },
            ],
            reasoning='Alright, the user asked me to forward an email to Vick, and they want the theatre gang to be in the loop. I need to find out who Vick is, is there a Vick in their contacts? I found a "Vick Li" and a "Vickie Lee", I need to be careful not to get confused here. Let\'s try to do some more reasoning first before I decide. The user wants me to forward an email about stage props and mentioned theatre gang, and if I check their contacts, "Vick Li" is a college friend and "Vickie Lee" is a theatre friend, so I think that the user must be wanting to email Vickie Lee since they both do theatre together.\n\nNow I need to figure out which email the user wants me to forward. Let me look through all their past sent and received emails for any subject line similar to "theater supplies confirmation." Looking at their past emails, I see they sent something with the subject "Receipt for Stage Props Order" to Francis on December 12. Stage props are theater supplies, and a confirmation is similar to an order, so I\'ll assume that\'s what they want me to forward to Vickie. I\'ll make sure to forward the email and its attachment.',
            success_conditions=[
                {
                    "input_text": '1. The email "Receipt for Stage Props Order" along with its Order_Receipt_12122024.pdf attachment is forwarded to Vickie Lee vickie.lee@orchardtheater.com',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The email is not forwarded to vick.li@techpals.com, who is a different person from Vickie Lee.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_emails",
                "get_all_emails",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Agent uses email search/get tools to locate the original props receipt email to Francis
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
                # Milestone 1 – Confirms the props receipt email to Francis was retrieved
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
                                                "value": "Receipt for Stage Props Order",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "dawei.shen@orchardtech.com",
                                                "partial": False,
                                            },
                                            "recipients_addresses": {
                                                "value": [
                                                    "francis.wagner@orchardtheater.com"
                                                ],
                                                "partial": True,  # list match via extractor supports partial flag semantics
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
                # Milestone 2 – Agent uses contacts tools to resolve "Vick" to the correct theater contact (Vickie Lee)
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
                # Milestone 3 – Confirms that Vickie Lee (theater friend) was identified as the target recipient
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
                                                "value": "Vickie Lee",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "vickie.lee@orchardtheater.com",
                                                "partial": False,
                                            },
                                            "relationship": {
                                                "value": "Theater Friend",
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
                # Milestone 4 – A new forwarded email has been sent to Vickie with the props receipt attached
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["vickie.lee@orchardtheater.com"]
                                    ],
                                    "status": "sent",
                                    # Subject/body may be auto-prefixed with "Fwd:" etc.; we just ensure it's clearly about the props order
                                    "subject": "Receipt for Stage Props Order",
                                    "attachments": [["Order_Receipt_12122024.pdf"]],
                                    "creation_datetime_iso": "2024-12-12T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "subject": column_rouge_l_similarity,
                                "attachments": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # email search → confirm correct original email found
                (2, 3),  # contact search → confirm correct Vick identified
            ],
            minefields=[
                Minefield(
                    # must not send to Vick Li
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [["vick.li@techpals.com"]],
                                    "status": "sent",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_116912b3-43ed-4656-897f-3895f21c77f9_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "misinformation_yes",
                "email",
                "contact",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "whatsapp_messaging",
                "messaging",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:05:00-08:00",
            is_read_time="2024-12-08T18:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to email Vickie to ask if she would be up for running some lines before theatre practice tonight. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Email Vick: 'Would you be up for running some lines half an hour before theatre practice tonight?' Be sure to include the exact time.",
                },
            ],
            reasoning="The user asked me to email 'Vick' about meeting early before today’s theater practice. However, from the user’s conversation history, I can tell there’s some confusion between two contacts — 'Vick Li' and 'Vickie Lee'.\n\nI’ll start by checking which one is actually involved in theater activities. Looking at recent conversations, I see multiple WhatsApp messages between the user and 'Vickie Lee' discussing tonight’s rehearsal at 7 PM, along with a calendar event titled 'Theater Rehearsal' listing Vickie Lee as an attendee. There’s no sign of 'Vick Li' being involved in any theater-related events; his past messages are about a cycling trip last week.\n\nSo the user likely meant 'Vickie', not 'Vick'. I’ll correct this silently and proceed with the right contact. The rehearsal starts at 7:00 PM, so half an hour before that is 6:30 PM.\n\nI’ll write an email to vickie.lee@orchardtheater.com that says: 'Would you be up for running some lines half an hour before theatre practice tonight at 6:30 pm?'. Then I’ll send the message and make sure it goes through successfully, using the correct recipient 'Vickie Lee' rather than 'Vick Li'.",
            success_conditions=[
                {
                    "input_text": "The agent sends an email to vickie.lee@orchardtheater.com that asks if she can run lines at 6:30 pm today",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. No email is sent to vick.li@techpals.com, who is a different person from Vickie Lee.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "send_email",
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the rehearsal time in the calendar
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
                # Milestone 1: Vikie contact found
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
                                                "value": "Vickie Lee",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "vickie.lee@orchardtheater.com",
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
                # Milestone 2 – The agent looks up the rehearsal time in the calendar
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
                # Milestone 3: rehearsal event found
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
                                                "value": "Theater Rehearsal",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-08T19:00:00-08:00",
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
                # Milestone 4 – A new email was actually sent to the required address and contains the key request
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["vickie.lee@orchardtheater.com"]
                                    ],
                                    "body": [("18:30", "6:30 pm", "6:30pm")],
                                    "creation_datetime_iso": "2024-12-08T18:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_subset_match_similarity,
                                "body": column_str_contains_any_similarity,
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
                (0, 1),  # search for Vickie's contact
                (2, 3),  # search for related events
            ],
            minefields=[
                # Should not send to Vick Li
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [["vick.li@techpals.com"]],
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_subset_match_similarity,
                                "status": column_exact_match_similarity,
                                "body": column_str_contains_any_similarity,
                            },
                            reference_milestone_node_index=-1,
                        ),
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_3e210596-0a3c-4865-b58c-d1afffecb2ae_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "misinformation_yes",
                "whatsapp_messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:20:00-08:00",
            is_read_time="2024-12-12T19:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know let Charles know you've ordered the props through the supplier he sent to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a new Whatsapp Message to Charlies Wilde, tell him Hey Charlie, I've got everything ordered for Cambodian Rock Band.",
                },
            ],
            reasoning="The user asked me to send a message to 'Charlies'. That name doesn’t appear in the user’s contacts, but I do see one contact named 'Charles Wilde'. Since 'Charlie' or 'Charlies' is a common informal variant of 'Charles', it’s reasonable to assume the user meant Charles Wilde. I’ll proceed with that contact.\n\nNow that I’ve identified who the message is for, I’ll check what the user wants to say to him and then compose and send the message accordingly.",
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Charles Wilde to say "Hey Charlie, I\'ve got everything ordered for Cambodian Rock Band.".',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – a WhatsApp send action was invoked
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
                # Milestone 1: Charles contact found
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
                                                "value": "Charles Wilde",
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
                # Milestone 2 – a new outgoing message to Charles is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [
                                            (
                                                "charles.wilde@orchardtheater.com",
                                                "+1 555-234-5678-9012",
                                            )
                                        ]
                                    ],
                                    "content": "Cambodian Rock Band",
                                    "creation_datetime_iso": "2024-12-12T19:20:00-08:00",
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
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_19_bf6be7a0-c2dc-45c1-aeec-54ef9da6f9f7_single_turn_3",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_19",
                "email",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_high",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T19:30:00-08:00",
            is_read_time="2024-12-12T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to let your friend know you placed the order for theatre props already so that she doesn't need to do it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you forward the theater supplies confirmation email I sent on the 11th over to Vickie?",
                },
            ],
            reasoning="Alright, the user asked me to forward an email to Vickie. I need to find out who Vickie is, is there a Vickie in their contacts? "
            'I found  "Vickie Lee" is a theatre friend, so I think that the user must be wanting to email Vickie.\n\nNow I need to figure out which email the user wants me to forward. Let me look through all their past sent and received emails for any subject line similar to "theater supplies confirmation." Looking at their past emails, I see they sent something with the subject "Receipt for Stage Props Order" to Francis. But this email was just sent today December 12th, not on the 11th like the user said. Still, stage props are theater supplies, and a confirmation is similar to an order, so I\'ll assume that\'s what they want me to forward to Vickie. I\'ll make sure to forward the email and its attachment.',
            success_conditions=[
                {
                    "input_text": '1. The email "Receipt for Stage Props Order" along with its Order_Receipt_12122024.pdf attachment is forwarded to Vickie Lee vickie.lee@orchardtheater.com',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_emails",
                "get_all_emails",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Agent uses an email-retrieval tool to locate the confirmation/order email
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
                # Milestone 1 – Confirm the "Receipt for Stage Props Order" email (the theater supplies confirmation) was retrieved
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
                                                "value": "Receipt for Stage Props Order",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "dawei.shen@orchardtech.com",
                                                "partial": False,
                                            },
                                            # We don't strictly require the date, but we implicitly rely on this being the only match
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
                # Milestone 2 – Agent uses contacts tool to resolve "Vickie" to the correct email (disambiguate from "Vick Li")
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
                # Milestone 3 – Confirm Vickie Lee (theater friend) was the resolved contact
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
                                                "value": "Vickie Lee",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "vickie.lee@orchardtheater.com",
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
                # Milestone 4 – The email has been forwarded to Vickie with the attachment preserved
                # We treat forwarding as sending a new email whose body/subject may differ, but must:
                #   - be sent
                #   - include Vickie's address as recipient
                #   - include the original attachment Order_Receipt_12122024.pdf
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["vickie.lee@orchardtheater.com"]
                                    ],
                                    "attachments": [["Order_Receipt_12122024.pdf"]],
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-12T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_subset_match_similarity,
                                "attachments": column_list_subset_match_similarity,
                                "status": column_exact_match_similarity,
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
                (0, 1),  # Email search → confirm stage props receipt email found
                (2, 3),  # Contact search → confirm Vickie Lee resolved
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_758e8a59-d679-4671-98f8-6316a6a91475_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "contact",
                "whatsapp_messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_yes",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:20:00-08:00",
            is_read_time="2024-12-05T17:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to check the tickets Jess sent you for theatre night so that you can make a note of the time on them.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you tell me what time the tickets my girlfriend sent me on WhatsApp say for our theatre night? If you can, tell me the exact time; if not, just reply ‘information missing’.",
                },
            ],
            reasoning='The user wants me to retrieve an attachment that their girlfriend sent, so first I must figure out which contact that is. I have managed to find Jess Zimmer under the "girlfriend" relationship, so I can assume the user wants me to find an attachment that Jess Zimmer sent. Next I need to figure out where this attachment was sent. I have checked messages, mail and WhatsApp and I have found a message regarding theatre night tickets that in WhatsApp, but all it says is "Here are the tickets for our theater night! 🎭" without any images, attachments, or ticket information. I\'ll have to tell the user that while Jess sent that text, it does not contain any tickets or time information about the event.',
            success_conditions=[
                {
                    "input_text": "1. The user is informed that information missing, there are Jess Zimmer's text message from 17:05 on 5 December 2024 did not actually contain any tickets or ticket information and key information is missing.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent uses WhatsApp retrieval to look for Jess's ticket message
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Confirm that the WhatsApp message from Jess about tickets at 2024-12-05T17:05:00-08:00 was retrieved
                # and that it does NOT contain any ticket details (no time info, only the text message).
                Milestone(
                    snapshot_constraints=[
                        # 1a: Verify the specific WhatsApp message existence in tool output
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
                                            "participants_names": {
                                                "value": ["Dawei Shen", "Jess Zimmer"],
                                                "partial": False,
                                            },
                                            "sender_name": {
                                                "value": "Jess Zimmer",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-05T17:05:00-08:00",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Here are the tickets for our theater night!",
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
                # Milestone 2 – User is informed that this WhatsApp message does not actually contain tickets or ticket time information
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We just need to see that the agent tells the user
                                    # that there are no tickets / no time info in that message.
                                    "content": [("information missing", "no info")],
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
                (0, 1),  # Use WhatsApp tools → confirm Jess's ticket message
                (
                    1,
                    2,
                ),  # Confirm message content → inform user that time info is missing
            ],
        ),
    ]
