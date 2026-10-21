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
    column_list_subset_match_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_similarity,
    contains_presence_similarity,
    not_contains_presence_similarity,
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


def get_TAG_DAWEI_SHEN_pilot_plot_17(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="DAWEI_SHEN_17_9284bf84-4815-46e3-a5af-390377bc938d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-04T17:15:00-08:00",
            is_read_time="2024-12-04T17:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to be reminded of who emailed you today. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who emailed me today?",
                },
            ],
            reasoning="The user wants to know who emailed them today.\n\nFirst I need to figure out today's date. Today is 4 December 2024. Now I will check Mail for the timestamps on the emails there.\n\nLooks like there was only one email with today's date, from kevin.chen@orchardtech.com. Next I should check Contacts to see who that email belongs to.\n\nHmm looks like it belongs to Kevin Chen. I will tell the user this.",
            success_conditions=[
                {
                    "input_text": "The assistant tells the user that Kevin Chen (kevin.chen@orchardtech.com) emailed today.",
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
                # Milestone 0 – The agent looks at today's emails
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
                # Milestone 1 – The returned email list contains Kevin’s message
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
                                                "value": "kevin.chen@orchardtech.com",
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
                # Milestone 2 – The agent tells the user Kevin emailed today
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
                                            "kevin.chen@orchardtech.com",
                                            "Kevin",
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
            name="DAWEI_SHEN_17_01694538-94be-4a27-ba14-88856a15d76b_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "whatsapp_messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T20:15:00-08:00",
            is_read_time="2024-12-11T20:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to reply to Jess to let her know that you booked tickets for the play "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to Jess saying I got tickets for next weekend",
                },
            ],
            reasoning="The user wants to respond to a WhatsApp message from a contact named Jess. I can identify one individual named Jess in my contacts, so I will send the response to her. I will request the content of the user’s message, and present them with a draft of the message for approval before sending after confirmation",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A new WhatsApp message is sent to Jess Zimmer that says "I got tickets for next weekend"',
                }
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "search_contacts",
                "get_all_contacts",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
            ],
            milestones=[
                # M0: search for conversation
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
                                ),
                            },
                        )
                    ]
                ),
                # Milestone 1: Jess's conversation found
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
                                            "creation_datetime_iso": {
                                                "value": "2024-12-11T20:00:00",
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
                # Milestone 2 – a new WhatsApp message to Jess is stored
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Both participants must appear, identifiable by either phone or e-mail
                                    "conversation_name": "Jess Zimmer",
                                    # Message should mention that tickets were booked
                                    "content": "I got tickets for next weekend",
                                    "creation_datetime_iso": "2024-12-11T20:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_c8002e1c-8f22-4387-9ac1-c886b067fd69_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T20:05:00-08:00",
            is_read_time="2024-12-11T20:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to add the play to your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Add an event called 'Play Date with Jess' to my calendar on 21 December 2024 between 8pm and 11pm with Jess as an invitee.",
                },
            ],
            reasoning="The user wants me to add an event to the calendar. The event is to take place on December 21st 2024. It takes place between 8pm and 11pm. I'll change that to the 24-hour time. It will take place between 20:00 and 23:00. I'll add that to the calendar and name the event 'Play Date with Jess' as requested.\nThe user wants someone called Jess to be added to the event. In their contacts there is only one Jess, Jess Zimmer, so I'll add them to the event.\nThe event is added.",
            success_conditions=[
                {
                    "input_text": "The event 'Play Date with Jess' is added to the calendar on December 21st 2024 from 20:00 to 23:00 and Jess Zimmer is included as an attendee.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "create_calendar_event",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – a new calendar event matching the play is added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Play Date with Jess",
                                    "start_datetime_iso": "2024-12-21T20:00:00-08:00",
                                    "end_datetime_iso": "2024-12-21T23:00:00-08:00",
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-11T20:05:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare with initial state
                        ),
                    ]
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_303903d2-51d2-4f95-a37b-4a3404e9024e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "whatsapp_messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T21:00:00-08:00",
            is_read_time="2024-12-11T21:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to text back Jess on WhatsApp since you forgot to reply to her message sooner, and she might not have seen the email with the theatre tickets you bought yet. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I would like you to reply Jess on the app saying "Looks like we have plans for next weekend!"',
                },
            ],
            reasoning="The user wants me to reply a simple text to Jess. There is only one Jess in the contacts, Jess Zimmer. Jess’ last WhatsApp message (2024-12-11 20:00) mentions 'next weekend' so I’ll respond in the same WhatsApp thread. I will send the exact text: “Looks like we have plans for next weekend!”",
            success_conditions=[
                {
                    "input_text": '1. The system will send the text message ""Looks like we have plans for next weekend!" to Jess Zimmer on WhatsApp.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "send_message",
                "search_contacts",
                "get_all_contacts",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # M0: search for conversation
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
                                ),
                            },
                        )
                    ]
                ),
                # Milestone 1: Jess's conversation found
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
                                            "creation_datetime_iso": {
                                                "value": "2024-12-11T20:00:00",
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
                # Milestone 2 – A new WhatsApp message record exists addressed to Jess with the expected content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Jess Zimmer",
                                    "content": "Looks like we have plans",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-11T21:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
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
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_303903d2-51d2-4f95-a37b-4a3404e9024e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "whatsapp_messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T21:00:00-08:00",
            is_read_time="2024-12-11T21:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to text back Jess on WhatsApp since you forgot to reply to her message sooner, and she might not have seen the email with the theatre tickets you bought yet. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I would like you to text Jess on WhatsApp saying "Looks like we have plans for next weekend!"',
                },
            ],
            reasoning="The user wants me to send a simple text to Jess. Let me just double-check who Jess is – there is only one Jess in the user contacts, and it is Jess Zimmer, the user's girlfriend. I'll go ahead and send the message \"Looks like we have plans for next weekend!\" to her on WhatsApp.",
            success_conditions=[
                {
                    "input_text": 'The system sends the text message "Looks like we have plans for next weekend!" to Jess Zimmer on WhatsApp.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "search_contacts",
                "get_all_contacts",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – A new WhatsApp message record exists addressed to Jess with the expected content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Jess Zimmer",
                                    "content": "Looks like we have plans",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-11T21:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_c8002e1c-8f22-4387-9ac1-c886b067fd69_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_high",
                "informational_complexity_low",
                "functional_complexity_moderate",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T20:05:00-08:00",
            is_read_time="2024-12-11T20:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to add the play to your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Create an event called 'Play Date with Jess' on 21st December 2024 at 20:00 to 23:00 and add my girlfriend to the event.",
                },
            ],
            reasoning="The user wants me to add an event to the calendar. The event is to take place on December 21st 2024. It will take place between 20:00 and 23:00. I'll add that to the calendar.\nI'll name the event 'Play Date with Jess' as requested.\nThe user wishes to add their girlfriend to the event. I'll look through their contacts to find someone labeled as their girlfriend. I found one contact that fits the criteria. The contact Jess Zimmer has been added to the calendar event.",
            success_conditions=[
                {
                    "input_text": "The event 'Play Date with Jess' is created on December 21st 2024 from 20:00 to 23:00 with Jess Zimmer added as an attendee.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "create_calendar_event",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – the agent finds girl friend's contact
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
                    ]
                ),
                # Milestone 1: Verify contact search results
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
                # Milestone 2 – a new calendar event matching the play is added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Play Date with Jess",
                                    "start_datetime_iso": "2024-12-21T20:00:00-08:00",
                                    "end_datetime_iso": "2024-12-21T23:00:00-08:00",
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-11T20:05:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare with initial state
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_01694538-94be-4a27-ba14-88856a15d76b_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "whatsapp_messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T20:15:00-08:00",
            is_read_time="2024-12-11T20:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to reply to Jess to let her know that you booked tickets for the play "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to Jess on WhatsApp and say I got tickets for next weekend",
                },
            ],
            reasoning="The user would like to send a reply to a message on WhatsApp from A contact named Jess. I can see only one Jess in contacts, so I'll send the reply to her. I'll ask the user what they want to say, and once they've told me, I'll show them a draft of the message and send upon confirmation.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A new WhatsApp message is sent to Jess Zimmer that says "I got tickets for next weekend"',
                }
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "search_contacts",
                "get_all_contacts",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
            ],
            milestones=[
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Both participants must appear, identifiable by either phone or e-mail
                                    "conversation_name": "Jess Zimmer",
                                    # Message should mention that tickets were booked
                                    "content": "I got tickets for next weekend",
                                    "creation_datetime_iso": "2024-12-11T20:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_9284bf84-4815-46e3-a5af-390377bc938d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-04T17:15:00-08:00",
            is_read_time="2024-12-04T17:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to be reminded of who emailed you today. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What emails did I get today?",
                },
            ],
            reasoning="The user wants to know what emails they achieved today.\n\nFirst I will check the date. Looks like it's 4 December 2024. Next I will check the timestamps of the emails in Mail to see which were received today.\n\nHmm looks like there was only one email received today from kevin.chen@orchardtech.com. I should check who that email belongs to in Contacts.\n\nAfter checking it in Contacts that email belongs to Kevin Chen.\n\nI will tell the user they have only received an email from Kevin Chen today.",
            success_conditions=[
                {
                    "input_text": "The assistant tells the user they received an email from Kevin Chen today.",
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
                # Milestone 0 – The agent inspects today’s email
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
                # Milestone 1 – The returned email list contains Kevin’s message
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
                                                "value": "kevin.chen@orchardtech.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-04T17:00:00",
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
                # Milestone 2 – The user is told that Kevin Chen emailed today
                Milestone(
                    snapshot_constraints=[
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
                                "content": column_contains_similarity,
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Email lookup precedes informing the user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_aef2483e-1ae2-4068-bf1a-c99d9a826e46_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "email",
                "messaging",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T09:35:00-08:00",
            is_read_time="2024-12-12T09:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know where your team meeting about action items location is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What's the location of the project gathering tomorrow? Not the one about recent research updates.",
                },
            ],
            reasoning='The user wants to know the location of the "project gathering".\n\nFirstly, I\'ll go to their Calendar to see if they have any upcoming events that correspond to this description.\n\nOkay, so they have one event named "Team Review Meeting" that\'s scheduled from 10:00 - 11:00 on Friday, December 13th 2024. I surmise that this is what the user is referring to, especially given the event description which mentions "project progress". \n\nI will now inform the user that the location of this event is Conference Room B, Orchard Tech HQ.',
            success_conditions=[
                {
                    "input_text": '1. The location of the event "Team Review Meeting" is presented to the user: Conference Room B, Orchard Tech HQ. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "get_all_emails",
                "search_emails",
                "get_all_messages",
                "search_messages",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks up calendar information (uses an appropriate calendar-query tool)
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
                # Milestone 1 – The returned the calendar event
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
                                                "value": "Team Review Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-13T10:00:00-08:00",
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
                # Milestone 1 – The user is told the meeting location “Conference Room B, Orchard Tech HQ”
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Conference Room B",
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
            name="DAWEI_SHEN_17_b5a797c4-3eda-43ab-924d-af8ea0dd1994_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "whatsapp_messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T22:00:00-08:00",
            is_read_time="2024-12-11T22:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to have another look at the link to the play that Jess Zimmer sent you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you pull up the WhatsApp message with the link to the play that my girlfriend sent to me.",
                },
            ],
            reasoning="To satisfy the user, I will first search the WhatsApp message history for any messages that contain a link to a play. I will look for one sent by “Jess Zimmer.” After locating that message, I will confirm that “Jess Zimmer” is indeed listed in the contacts (tagged as the girlfriend). Finally, I will show the user the original WhatsApp message that contains the text “check out this play I found” along with the link to the play.",
            success_conditions=[
                {
                    "input_text": "1. WhatsApp message from Jess Zimmer containing a link to a play is presented.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent looks for WhatsApp messages
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
                # Milestone 1 – The retrieved result contains Jess Zimmer’s message with the play link
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
                                            "sender_name": {
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
                # Milestone 2 – The agent looks for contacts to make sure who is the girlfried
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
                # Milestone 3 – The retrieved result contains Jess Zimmer
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
                # Milestone 4 – The agent shows the message (or link) to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "check out this play I found",
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
                (0, 1),  # Search WhatsApp → verify Jess’s message found
                (2, 3),  # Verify Jess is his girlfriend
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_99fe346f-247f-4487-9275-a2d2c4eca7a5_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T20:05:00-08:00",
            is_read_time="2024-12-11T20:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to create an event in calendar for your play date with Jess. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Add my play date with jess to my calendar for this Friday at 7. ",
                },
            ],
            reasoning='I\'ll schedule a new calendar event titled "Play Date with Jess" for Friday, December 13 th, 2024 at 19:00 (7 PM) and invite Jess Zimmer.',
            success_conditions=[
                {
                    "input_text": 'A new event is created called "Play Date with Jess" for 13/12/24 at 7pm.  ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "create_calendar_event",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent looks for contacts to
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
                # Milestone 1 – The retrieved result contains Jess Zimmer
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
                # Milestone 2 – A new calendar event for the play date has been added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Play Date with Jess",
                                    "start_datetime_iso": "2024-12-13T19:00:00-08:00",
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-11T20:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,
                                "attendees_names": column_list_subset_match_similarity,
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
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_0a45f5bb-b8fb-4b0d-97f9-47d2ef390d01_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "calendar",
                "contact",
                "whatsapp_messaging",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T20:16:00-08:00",
            is_read_time="2024-12-11T20:16:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You’ve booked play tickets for Jess, and you want to add it to your calendar.       You and Jess agreed in your messages that it’s 'next weekend'.       There’s no confirmed message saying Sunday is unavailable, but past emails and calendar events show that Sunday night is usually reserved for theater rehearsal.       Now ask the assistant to schedule the event without saying which day it is — let it infer Saturday is the only viable option based on prior patterns. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I’ve booked the play tickets she was excited about — it’s this weekend, on the day I don’t have the usual rehearsal. Create an event called 'Play Night', 2 hours starting at 7. Add her to the invite.",
                },
            ],
            reasoning="The user wants to create an event called 'Play Night' for 2 hours starting at 7 PM, and add 'her' to the invite. I need to figure out who 'she' is. The user mentions 'the play tickets she was excited about', so I should check recent messages to find who was discussing play tickets. From WhatsApp messages, I find Jess Zimmer was excited about a play. So 'she' refers to Jess Zimmer, the user's girlfriend. The user says it's 'this weekend, on the day I don't have the usual rehearsal'. I need to check the calendar to find which day has rehearsal. I find Theater Rehearsal is on Sunday evening, so the play must be on Saturday when there's no rehearsal. I will create an event called 'Play Night' with Jess Zimmer as an invitee at 19:00-21:00 on Saturday, 14th of December 2024.",
            success_conditions=[
                {
                    "input_text": "1. an event 'Play Night' is created with Jess Zimmer as an invitee at 19:00-21:00 on 14th of December 2024. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "create_calendar_event",
                "search_contacts",
                "get_all_contacts",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_emails",
                "get_all_emails",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – The agent looks for WhatsApp messages
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
                # Milestone 1 – The retrieved result contains Jess Zimmer’s message with the play link
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
                                            "sender_name": {
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
                # Milestone 2 – The agent looks up calendar information (uses an appropriate calendar-query tool)
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
                # Milestone 3 – The returned the calendar event
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
                                                "value": "2024-12-08T19:00:00",
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
                # Milestone 4 – The play event was added to the calendar with the right core details
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Play Night",
                                    "start_datetime_iso": "2024-12-14T19:00:00-08:00",
                                    "end_datetime_iso": "2024-12-14T21:00:00-08:00",
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-11T20:16:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
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
                (0, 1),
                (2, 3),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_a4de5c01-2073-49e0-b528-088fe978bfef_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "whatsapp_messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T20:10:00-08:00",
            is_read_time="2024-12-11T20:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to let Jess Zimmer know that you will book the tickets so you ask the assistant to send a message "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a WhatsApp message to Jess Zimmer that says "I\'ll book them"',
                },
            ],
            reasoning="The user asked me to send a WhatsApp message to Jess Zimmer saying “I'll book them”. I locate the chat with Jess Zimmer and send the message right away; the outgoing message now appears in the conversation with status “sent.”",
            success_conditions=[
                {
                    "input_text": '1. A message with the text "I\'ll book them" is sent to Jess Zimmer on WhatsApp ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – a new WhatsApp message saying “I'll book them now” is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Jess Zimmer",
                                    "content": "book them",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-11T20:10:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial DB state
                        )
                    ],
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_85134dc4-a0be-4eea-aca3-506de56b275a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T20:05:00-08:00",
            is_read_time="2024-12-11T20:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to create an event in calendar for your play date with Jess.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Add my play date with jess to my calendar for this Sunday at 7 and invite her. ",
                },
            ],
            reasoning='I\'m going to schedule a new event called "Play date with Jess" on Sunday at 7. I need to figure out who Jess is, so I need to search for messages and whatsapp messages first. I found one whatsapp message from Jess Zimmer mentioned "Hey Dawei, check out this play I found! Looks fascinating and right up our alley. How about we plan to see it next weekend?", so Jess Zimmer should be the invitee. \n\nOkay, I\'ll schedule "Play Date with Jess" with Jess for 19:00 on December 15th.',
            success_conditions=[
                {
                    "input_text": 'A new event is created called "Play Date with Jess" for 12/15/24 at 7pm.  ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "create_calendar_event",
                "search_contacts",
                "get_all_contacts",
                "get_all_messages",
                "search_messages",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – (Optional) Agent may look up contacts or calendars, but not strictly needed.
                # Agent need to find the full name of Jess to complete this task
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
                                # Allow any of these lookups if the agent chooses to use them;
                                # this milestone is not depended on by others.
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "search_contacts",
                                        "get_all_contacts",
                                        "get_all_messages",
                                        "search_messages",
                                        "get_all_whatsapp_messages",
                                        "search_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – calendar event has been created for the play date with Jess
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Play Date",
                                    # 15 December 2024 is the Sunday implied by the context
                                    "start_datetime_iso": "2024-12-15T19:00:00-08:00",
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-11T20:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                # Use close similarity for time to allow small differences (e.g., timezone offsets or seconds)
                                "start_datetime_iso": column_contains_similarity,
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
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_b5a797c4-3eda-43ab-924d-af8ea0dd1994_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "whatsapp_messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T22:00:00-08:00",
            is_read_time="2024-12-11T22:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to have another look at the link to the play that Jess Zimmer sent you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you pull up the WhatsApp message with the link to the play that Jess sent to me.",
                },
            ],
            reasoning="The user wants to see the WhatsApp message from Jess Zimmer that contains a link to a play. I will search Jess Zimmer’s chat, locate the specific message which includes the text “check out this play I found” along with the link, and then present that exact message (or the link itself) back to the user.",
            success_conditions=[
                {
                    "input_text": "1. WhatsApp message from Jess Zimmer containing a link to a play is presented.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent looks for WhatsApp messages
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
                # Milestone 1 – The retrieved result contains Jess Zimmer’s message with the play link
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
                                            "sender_name": {
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
                # Milestone 2 – The agent shows the message (or link) to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "check out this play I found",
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
                (0, 1),  # Search WhatsApp → verify Jess’s message found
                (1, 2),  # Message found → shown to user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_aef2483e-1ae2-4068-bf1a-c99d9a826e46_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T09:55:00-08:00",
            is_read_time="2024-12-12T09:55:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know where your team meeting location is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where's tomorrow's monthly team meeting being held",
                },
            ],
            reasoning="The user wants to know the location of their only event tomorrow, “Team Review Meeting,” scheduled for Friday, December 13 2024 from 10:00 – 11:00. I check their calendar, find that event, confirm its location is “Conference Room B,” and relay that location to the user.",
            success_conditions=[
                {
                    "input_text": 'The location of the event "Team Review Meeting" is presented to the user: Conference Room B.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent looked up calendar information
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
                # Milestone 1 – The returned the calendar event
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
                                                "value": "Team Review Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-13T10:00:00-08:00",
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
                # Milestone 2 – The user was told the meeting location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Conference Room B",
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
            name="DAWEI_SHEN_17_2c53a8a5-1182-4b43-8e7b-78503dfecb45_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "calendar",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T14:35:00-08:00",
            is_read_time="2024-12-12T14:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You need to update the time with your dinner with Lukas and Vick to start half an hour later as you want to schedule in an 1-hour-long meditative walk in beforehand after the long week, starting 18:00.       You also need to text into the group to let them know of the change.       If there's a duplication event, ask the agent to only keep one. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to push the dinner with Vick and Lukas back by half an hour, and then add an event for a 1-hour meditative walk at 6 PM. Also send them: 'Hi guys, sorry I've had to update our start time as I have some things I need to get done beforehand'",
                },
            ],
            reasoning="First, locate the existing event ‘Dinner with Lukas and Vick’ on 14 Dec 2024 at 19:00 and shift its start time to 19:30 (keeping only one instance if duplicates exist). Next, create a new calendar event titled ‘Meditative Walk’ on 14 Dec 2024 that runs from 18:00 to 19:00. Finally, send a group message in the ‘Dinner at a local restaurant’ conversation to Lukas Hürholz and Vick Li saying: “Hi guys, sorry I've had to update our start time as I have some things I need to get done beforehand.”",
            success_conditions=[
                {
                    "input_text": "One of the duplicated event 'Dinner with Lukas and Vick' scheduled for 14th December at 19:00 is removed.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The event 'Dinner with Lukas and Vick' scheduled for 14th December at 19:00 is updated to begin at 19:30. Lukas Hürholz and Vick Li are notified as invitees of the event.",
                    "statefullness": "Stateful",
                },
                {
                    "statefullness": "Stateful",
                    "input_text": "An event named 'Meditative Walk' is added to the calendar for the 14th December at 18:00-19:00.",
                },
                {
                    "statefullness": "Stateful",
                    "input_text": "A text message is composed and sent to 'Dinner at a local restaurant' saying 'Hi guys, sorry I've had to update our start time as I have some things I need to get done beforehand'.",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "modify_calendar_event",
                "remove_calendar_event",
                "create_calendar_event",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Calendar lookup tool used
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
                # Milestone 1 – The specific dinner event was surfaced
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
                # Milestone 2 – Calendar removal tool used
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
                                        "remove_calendar_event",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 3 – Duplicated event removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dinner with Lukas and Vick",
                                    "start_datetime_iso": "2024-12-14T19:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.MESSAGING],
                ),
                # Milestone 4 – Dinner event time was updated to 19:30
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dinner with Lukas and Vick",
                                    "start_datetime_iso": "2024-12-14T19:30:00-08:00",
                                    # allow any end time – only start must change
                                    "attendees_names": [
                                        ["Dawei Shen", "Lukas Hürholz", "Vick Li"]
                                    ],
                                    "creation_datetime_iso": "2024-12-12T14:35:00-08:00",
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
                            require_added=True,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.MESSAGING],
                ),
                # Milestone 5 – An event created at 18:00
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Meditative Walk",
                                    "start_datetime_iso": "2024-12-14T18:00:00-08:00",
                                    "end_datetime_iso": "2024-12-14T19:00:00-08:00",
                                    "creation_datetime_iso": "2024-12-12T14:35:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                            require_added=True,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.MESSAGING],
                ),
                # Milestone 6 – Group message sent announcing the change
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Dinner at a local restaurant",
                                    "content": "Hi guys, sorry I've had to update our start time as I have some things I need to get done beforehand",
                                    "creation_datetime_iso": "2024-12-12T14:35:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # tool usage → dinner event find
                (2, 3),  # Need a remove calendar call
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_2c53a8a5-1182-4b43-8e7b-78503dfecb45_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "calendar",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T14:35:00-08:00",
            is_read_time="2024-12-12T14:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You need to update the time with your dinner with Lukas and Vick to start half an hour later as you want to schedule in a meditative walk in beforehand after the long week.       You also need to text into the group to let them know of the change.     If there's a duplication in the calendar, remove one. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Change the dinner time this weekend to start at 19:30 and then put an 1 hour long meditative walk in beforehand at 18:00. I also need to text into the local restaurant chat, 'Hi guys, sorry I've had to update our start time as I have some things I need to get done beforehand'.",
                },
            ],
            reasoning="Right, the user firstly wants to update their event, 'Dinner with Lukas and Vick', scheduled for 14th December at 19:00, to begin at 19:30. But I found duplicated calendar event, I shall let the user know and delete one of them and update the remaining one.\n\nNext, they want to add a new event named 'Meditative Walk' before their dinner event at 18:00, lasting one hour (ending at 19:00).\n\nLastly, the user needs to send a message into the 'Dinner at a local restaurant' group chat saying: \"Hi guys, sorry I've had to update our start time as I have some things I need to get done beforehand.\"",
            success_conditions=[
                {
                    "input_text": "The event 'Dinner with Lukas and Vick' scheduled for 14th December at 19:00 is updated to begin at 19:30. Lukas Hürholz and Vick Li are notified as invitees of the event.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The duplicated event 'Dinner with Lukas and Vick' scheduled for 14th December at 19:00 is deleted.",
                    "statefullness": "Stateful",
                },
                {
                    "statefullness": "Stateful",
                    "input_text": "An event named 'Meditative Walk' is added to the calendar for the 14th December at 18:00.",
                },
                {
                    "statefullness": "Stateful",
                    "input_text": "A text message is composed and sent to 'Dinner at a local restaurant' saying 'Hi guys, sorry I've had to update our start time as I have some things I need to get done beforehand'.",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "modify_calendar_event",
                "remove_calendar_event",
                "create_calendar_event",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Calendar lookup tool used
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
                # Milestone 1 – The specific dinner event was surfaced
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
                # Milestone 2 – Calendar removal tool used
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
                                        "remove_calendar_event",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 3 – Duplicated event removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dinner with Lukas and Vick",
                                    "start_datetime_iso": "2024-12-14T19:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.MESSAGING],
                ),
                # Milestone 4 – Dinner event time was updated to 19:30
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dinner with Lukas and Vick",
                                    "start_datetime_iso": "2024-12-14T19:30:00-08:00",
                                    # allow any end time – only start must change
                                    "attendees_names": [
                                        ["Dawei Shen", "Lukas Hürholz", "Vick Li"]
                                    ],
                                    "creation_datetime_iso": "2024-12-12T14:35:00-08:00",
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
                            require_added=True,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.MESSAGING],
                ),
                # Milestone 5 – An event created at 18:00
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Meditative Walk",
                                    "start_datetime_iso": "2024-12-14T18:00:00-08:00",
                                    "end_datetime_iso": "2024-12-14T19:00:00-08:00",
                                    "creation_datetime_iso": "2024-12-12T14:35:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                            require_added=True,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.MESSAGING],
                ),
                # Milestone 6 – Group message sent announcing the change
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Dinner at a local restaurant",
                                    "content": "Hi guys, sorry I've had to update our start time as I have some things I need to get done beforehand",
                                    "creation_datetime_iso": "2024-12-12T14:35:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # tool usage → dinner event find
                (2, 3),  # Need a remove calendar call
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_728f435c-00c4-4186-84a7-0dc153e3b0b2_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T20:17:00-08:00",
            is_read_time="2024-12-11T20:17:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You bought the tickets for the show Jess was talking about and want to make sure you've sent Jess the ticket confirmations. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I send an email to Jess with the ticket confirmation yet? Yes or No.",
                },
            ],
            reasoning='The assistant should search the user\'s sent mail for an email to Jess with subject "Ticket Confirmation for Our Play Date" that was sent on 2024-12-11T20:15:00-08:00. If that email exists, respond to the user with "Yes"; otherwise respond with "No."',
            success_conditions=[
                {
                    "input_text": "A ticket confirmation email to Jess with subject 'Ticket Confirmation for Our Play Date' was sent at 2024-12-11T20:15:00-08:00.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The assistant replies to the user with 'Yes'.",
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
                # Milestone 0 – send email
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
                # Milestone 1 – A confirmation email to Jess was actually sent
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
                                                "value": "Ticket Confirmation for Our Play Date",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-11T20:15:00-08:00",
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
                # Milestone 2 – The user is told the email has been sent
                Milestone(
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
                                "content": column_word_contains_similarity,
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_b5a797c4-3eda-43ab-924d-af8ea0dd1994_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "whatsapp_messaging",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T22:00:00-08:00",
            is_read_time="2024-12-11T22:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to have another look at the link to the play that Jess Zimmer sent you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you pull up the text with the link to the play that my girlfriend sent to me.",
                },
            ],
            reasoning="The user wants to see a text from their girlfriend containing a link to a play, first I will determine which contact the user is talking about. \n\nLooking through the user’s contacts I can see that Jess Zimmer is tagged as girlfriend, I can assume that this is the person in question and look through their text messages to find the one containing the link.\n\nI can’t see any link shared in the text message chain, I will consider that the user could be referring to a message in another app when they say text, I will now look through the user’s WhatsApp message to see if there is the link in question.\n\nI will now present the WhatsApp message with the link to the play to the user.",
            success_conditions=[
                {
                    "input_text": "1. WhatsApp message from Jess Zimmer containing a link to a play is presented.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_messages",
                "get_all_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent looks for WhatsApp messages
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
                # Milestone 1 – The retrieved result contains Jess Zimmer’s message with the play link
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
                                            "sender_name": {
                                                "value": "Jess Zimmer",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-11T20:00:00",
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
                # Milestone 2 – The agent shows the message (or link) to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Play Link",
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
                (0, 1),  # Search WhatsApp → verify Jess’s message found
                (1, 2),  # Message found → shown to user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_c3c51b11-3a19-4983-ac75-172d4c7de762_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_moderate",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T20:15:00-08:00",
            is_read_time="2024-12-11T20:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to pull up your most recent message from Jess on WhatsApp and respond to it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the most recent message from Jess on WhatsApp and reply to it saying Hey Jess, just bought us tickets for the play. I emailed the confirmation to you.",
                },
            ],
            reasoning="The user wants me to show them the most recent message from Jess on WhatsApp. I look up WhatsApp messages for the contact Jess Zimmer by calling the appropriate WhatsApp-read tool. The most recent message was received at 20:00 on 11 December 2024 and says something like, “Hey Dawei, here’s the play I found …”. I present that message to the user. Next, the user wants to reply, “Hey Jess, just bought us tickets for the play. I emailed the confirmation to you.” I draft that exact reply, confirm, and then send it to Jess Zimmer on WhatsApp.",
            success_conditions=[
                {
                    "input_text": "1. The most recent message from Jess Zimmer on WhatsApp, which was received on December 11 2024 at 20:00 is presented to the user. ",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": '2. A message is drafted saying " Hey Jess, just bought us tickets for the play. I emailed the confirmation to you." And sent to Jess Zimmer on WhatsApp.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
            ],
            milestones=[
                # Milestone 0 – The agent looks up WhatsApp messages (must call a WhatsApp-read tool)
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
                                        "get_all_whatsapp_messages",
                                        "search_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – The retrieved result contains Jess Zimmer’s message with the play link
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
                                            "sender_name": {
                                                "value": "Jess Zimmer",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-11T20:00:00",
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
                # Milestone 2 – A WhatsApp reply is actually sent out
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Jess Zimmer",
                                    "content": "just bought us tickets",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-11T20:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
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
                (0, 1),  # retrieved the message
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_17_c3c51b11-3a19-4983-ac75-172d4c7de762_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "whatsapp_messaging",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T20:15:00-08:00",
            is_read_time="2024-12-11T20:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to pull up your most recent message from Jess on WhatsApp and respond to it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you reply to my girlfriend’s last message with: 'Hey Jess, just bought us tickets for the play. I emailed the confirmation to you.' Also show me what she said earlier.",
                },
            ],
            reasoning='The user wants me to show them the most recent message from their girlfriend on WhatsApp. I will check their contacts for someone labelled as their girlfriend. I have found only one contact with that label, Jess Zimmer.\nI will look at WhatsApp messages from this contact. The most recent message appears to have been received at 20:00 on 11 December 2024 and contains her note about the play ("…play I found…"). I present this message to the user.\nThe user also wants me to reply to this message saying Hey Jess, just bought us tickets for the play. I emailed the confirmation to you. I will draft that message and await confirmation from the user.\nThe user is happy with the message so I send it to the desired contact, Jess Zimmer, on WhatsApp.',
            success_conditions=[
                {
                    "input_text": "1. The most recent message from Jess Zimmer on WhatsApp, which was received on December 11 2024 at 20:00 is presented to the user. ",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": '2. A message is drafted saying " Hey Jess, just bought us tickets for the play. I emailed the confirmation to you." And sent to Jess Zimmer on WhatsApp.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "send_whatsapp_message",
                "search_contacts",
                "get_all_contacts",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # milestone 0: search for contacts
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",  # Value not used in similarity calculation
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
                # milestone 1: confirm Jess is his girlfriend
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
                # Milestone 2 – The agent looks up WhatsApp messages (must call a WhatsApp-read tool)
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
                                        "get_all_whatsapp_messages",
                                        "search_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 3 – The retrieved result contains Jess Zimmer’s message with the play link
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
                                            "sender_name": {
                                                "value": "Jess Zimmer",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-11T20:00:00",
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
                        ),
                    ],
                ),
                # Milestone 4 – A WhatsApp reply is actually sent out
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Jess Zimmer",
                                    "content": "just bought us tickets",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-11T20:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
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
                (0, 1),  # retrieved the Jess is his girlfriend
                (2, 3),  # retrieved the message
            ],
        ),
    ]
