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
    column_list_tuple_contains_similarity,
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_any_similarity,
    column_word_contains_similarity,
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


def get_TAG_LUCAS_GARCIA_pilot_plot_19(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="LUCAS_GARCIA_19_d55c3609-d652-41e3-bbea-6c7c391e6270_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "whatsapp_messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T16:35:00-08:00",
            is_read_time="2024-12-06T16:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to make sure you and David Turner are still on for surfing today at the beach as planned.  You want go know if he responded to your text asking him. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did the surfing bro text?",
                },
            ],
            reasoning="The user wants to know if the surfing bro texted. I wonder who they mean. I can check the user's contacts to figure it out. I see one contact, David Turner, listed similarly as Surfing Buddy. I know bro can be used as slang for a friend or buddy. This must be who he means. I'll search for the latest message from David now. I see one new WhatsApp message from David Turner, received on December 6th, 2024, at 16:35. I'll show the user that message now. ",
            success_conditions=[
                {
                    "input_text": "1. The WhatsApp message from David Turner, received on December 6th, 2024, at 16:35, is shown to the user. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks for WhatsApp messages to determine if “the surfing bro” (David Turner) texted
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
                # Milestone 1 – Verify the expected WhatsApp message from David Turner is present in the results of Milestone 0
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
                                                "value": "David Turner",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "can't wait to catch some waves",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-06T16:35:00-08:00",
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
                # Milestone 2 – The agent informs the user and includes (at least part of) David’s message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "can't wait to catch some waves",
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
            name="LUCAS_GARCIA_19_d55c3609-d652-41e3-bbea-6c7c391e6270_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "whatsapp_messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T16:35:00-08:00",
            is_read_time="2024-12-06T16:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to make sure you and David Turner are still on for surfing today at the beach as planned.  You want go know if he responded to your text asking him. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did David text?",
                },
            ],
            reasoning="The user wants to know if David texted. I wonder who they mean. I can check the user's contacts to figure it out. I see one contact with that name; David Turner. This must be who he means. I'll search for the latest message from David now. I see one new WhatsApp message from David Turner, received on December 6th, 2024, at 16:35. I'll show the user that message now. ",
            success_conditions=[
                {
                    "input_text": "1. The WhatsApp message from David Turner, received on December 6th, 2024, at 16:35, is shown to the user. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent retrieves WhatsApp messages
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
                # Milestone 1 – Retrieved WhatsApp output contains the expected message from David Turner
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
                                                "value": "David Turner",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-06T16:35:00-08:00",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "can't wait to catch some waves",
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
                # Milestone 2 – Agent informs the user and shows the message content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "can't wait to catch some waves",
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
                (0, 1),  # Retrieval → confirmation of correct message
                (1, 2),  # Confirmation → informing the user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_a50e5f4b-b271-4c24-883d-6b793d910b25_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T07:55:00-08:00",
            is_read_time="2024-12-11T07:55:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to dictate a reply to David Turner asking him to confirm when he wants to go surfing. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a reply message to Surfing Buddy saying "Hey just checking in, when did you want to go surfing again?"',
                },
            ],
            reasoning="The user wants to dictate a reply to Surfing Buddy. I need to figure out who that is. Looking through the user's contacts I can see David Turner has an alias of 'Surfing Buddy' so I can assume he is the intended recipient.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": "1. A reply message via whatsapp is sent to David Turner asking him to confirm when he wants to go surfing.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the surfing buddy contact (David Turner)
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
                # Milestone 1 – Verify that David Turner was one of the contacts returned from Milestone 0
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
                                        "full_name": {
                                            "value": "David Turner",
                                            "partial": False,
                                        },
                                        "phone_number": {
                                            "value": "+1 12345-6789-1000-9876",
                                            "partial": False,
                                        },
                                    },
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
                # Milestone 2 – Agent looks up the David Turner conversations
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
                    ]
                ),
                # Milestone 3 – Verify that David Turner conversations in whatsapp
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
                                        "conversation_name": {
                                            "value": "David Turner",
                                            "partial": False,
                                        },
                                    },
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
                    ]
                ),
                # Milestone 4 – A WhatsApp reply message is added asking when to surf again
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
                                                "+1 12345-6789-1000-1234",
                                                "lucas.garcia@example.com",
                                            ),  # Lucas’s number
                                            (
                                                "+1 12345-6789-1000-9876",
                                                "david.turner@example.com",
                                            ),  # David’s number
                                        ]
                                    ],
                                    "content": "when did you want to go surfing",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-11T07:55:00-08:00",
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
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # contact search -> confirm David Turner
                (2, 3),  # confirmed WhatsApp message conversation
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_b910eec1-cd27-4e14-b4e7-c926075d25d4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T14:25:00-08:00",
            is_read_time="2024-12-11T14:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to schedule another surf session with David for the same time for Saturday next week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Copy today's event from earlier to the 21st and let him know via email.",
                },
            ],
            reasoning="Right so, the user is looking to copy an event from earlier to 21 December 2024. Looking at the user's calendar, I can see one event which took place earlier the 11 December 2024 from 07:00 to 08:30 titled 'Early Morning Surfing Session with David' with David Turner. This is the event the user is talking about copying and then I can copy it to 21 December 2024 for the same time. A calendar invite will be sent to David Turner notifying him of the event.",
            success_conditions=[
                {
                    "input_text": "1. 'Early Morning Surfing Session with David' scheduled on 11 December 2024 from 07:00 to 08:30 with David Turner is copied to 21 December 2024 and David Turner is notified via email as an invitee.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. David Turner is notified via email.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
                "get_all_contacts",
                "search_contacts",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Agent looks up existing surf event
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
                # Milestone 1 – Confirms the 11-Dec-2024 surf event was found
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
                                                "value": "Early Morning Surfing Session with David",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-11T07:00:00-08:00",
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
                # Milestone 2 – The agent searches contacts (or lists all) to find David Turner
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
                # Milestone 3 – Confirm David Turner’s contact info was returned
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
                                                "value": "David Turner",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "david.turner@example.com",
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
                # Milestone 4 – New calendar event created on 21-Dec-2024 07:00-08:30 with David Turner
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Early Morning Surfing Session with David",
                                    "start_datetime_iso": "2024-12-21T07:00:00-08:00",
                                    "end_datetime_iso": "2024-12-21T08:30:00-08:00",
                                    "attendees_names": [["David Turner"]],
                                    "creation_datetime_iso": "2024-12-11T14:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial calendar state
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
                # Milestone 5 – Email/Invite sent to David Turner
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["david.turner@example.com"]
                                    ],
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-11T14:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_subset_match_similarity,
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
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (2, 3),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_5d285aac-7fa2-4232-86b7-7396bd99494f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "whatsapp_messaging",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T07:33:00-08:00",
            is_read_time="2024-12-11T07:33:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are waiting for a reply from David after your amazing surfing session. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has David Turner replied to me on WhatsApp yet?",
                },
            ],
            reasoning="The user is asking about a reply to their message.\nThe user has indicated that they are seeking a reply on WhatsApp, I should find their conversation with the named contact there. \nI see the user's conversation with David Tuner. I cannot see any new messages from David Turner. I should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Messages are checked for new reply from David Turner to message sent by user on December 11 2024 at 07:30.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_whatsapp_messages", "search_whatsapp_messages"],
            milestones=[
                # Milestone 0 – The agent looks up WhatsApp messages
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
                # Milestone 1 – The retrieved WhatsApp thread with David Turner is present in the tool output
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
                                            # Ensure the conversation with David Turner is found
                                            "participants_names": {
                                                "value": "David Turner",
                                                "partial": True,
                                            },
                                            # Ensure the outbound surfing-session message is present
                                            "content": {
                                                "value": "incredible this morning",
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
                # Milestone 2 – The agent tells the user that David has not replied yet
                Milestone(
                    snapshot_constraints=[
                        # Check for negative confirmation about reply
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
                                            "not yet",
                                            "hasn't",
                                            "has not",
                                            "haven't",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        # Ensure the word "reply" (or derivative) is referenced
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "repl",
                                            "response",
                                            "respond",
                                            "heard back",
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_5d285aac-7fa2-4232-86b7-7396bd99494f_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "whatsapp_messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T07:33:00-08:00",
            is_read_time="2024-12-11T07:33:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are waiting for a reply from your surf instructor after your amazing surfing session. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has the surf instructor replied to me on WhatsApp yet?",
                },
            ],
            reasoning="The user is asking about a reply to their message.\nFirst, I should determine which contact they are referring to. The user has indicated that they are a surf instructor, I will use this to focus my search. I see that David Turner is tagged as a surf instructor in the user's contacts. This must be who the user is referring to.\nThe user has indicated that they are seeking a reply on WhatsApp, I should find their conversation with the named contact there. \nI see the user's conversation with David Tuner. I cannot see any new messages from David Turner. I should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Messages are checked for new reply from David Turner to message sent by user on December 11 2024 at 07:30.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_whatsapp_messages", "search_whatsapp_messages"],
            milestones=[
                # Milestone 0 – The agent consults WhatsApp history
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
                # Milestone 1 – The retrieved WhatsApp result set contains (at least) the outgoing message sent by Lucas
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
                                                "value": "Coach Lucas",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Hey David, those waves were incredible",
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
                # Milestone 2 – The agent tells the user that David has not replied yet
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
                                            "no reply",
                                            "not yet",
                                            "hasn't responded",
                                            "has not responded",
                                            "haven't heard",
                                            "no response",
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
                (0, 1),  # WhatsApp search → confirm retrieved message
                (1, 2),  # confirmation of retrieval → user-facing answer
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_b910eec1-cd27-4e14-b4e7-c926075d25d4_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T14:25:00-08:00",
            is_read_time="2024-12-11T14:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to schedule another surf session with David for the same time for Saturday next week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Copy the morning surf session to Saturday 21st December and let my buddy know via email.",
                },
            ],
            reasoning="Okay so, the user is looking to copy an event named 'morning surf session' to 21 December. Checking the user's calendar, I can see one event matching titled 'Early Morning Surfing Session with David' which was scheduled from 07:00 to 08:30 on 11 December 2024 with David Turner. This is the event the user is wanting to copy to 21 December so I can do so. A calendar invite will be sent to David Turner notifying him of the event.",
            success_conditions=[
                {
                    "input_text": "1. 'Early Morning Surfing Session with David' scheduled on 11 December 2024 from 07:00 to 08:30 with David Turner is copied to 21 December 2024 and David Turner is notified via email as an invitee.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. David Turner is notified via email.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
                "get_all_contacts",
                "search_contacts",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the original surfing event in the calendar
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
                        ),
                    ],
                ),
                # Milestone 1 – Confirm the correct surfing event (Dec 11) was found
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
                                                "value": "Early Morning Surfing Session with David",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-11T07:00:00-08:00",
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
                # Milestone 2 – The agent searches contacts (or lists all) to find David Turner
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
                # Milestone 3 – Confirm David Turner’s contact info was returned
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
                                                "value": "David Turner",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "david.turner@example.com",
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
                # Milestone 4 – A new calendar event is created for Sat Dec 21 at 07:00–08:30 that includes David
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Early Morning Surfing Session with David",
                                    "start_datetime_iso": "2024-12-21T07:00:00-08:00",
                                    "end_datetime_iso": "2024-12-21T08:30:00-08:00",
                                    "attendees_names": [["David Turner"]],
                                    "creation_datetime_iso": "2024-12-11T14:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        ),
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
                # Milestone 5 – An email (invite) is sent to David Turner notifying him
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["david.turner@example.com"]
                                    ],
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-11T14:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_subset_match_similarity,
                                "status": column_exact_match_similarity,
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
            ],
            milestone_edge_list=[
                (0, 1),  # calendar search → confirm event
                (2, 3),  # contact search → confirm David
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_a50e5f4b-b271-4c24-883d-6b793d910b25_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_19",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T07:55:00-08:00",
            is_read_time="2024-12-11T07:55:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to dictate a reply to David Turner asking him to confirm when he wants to go surfing. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a reply message to David Turner saying "Hey just checking in, when did you want to go surfing again?"',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called David Turner.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": "1. A reply message via whatsapp is sent to David Turner asking him to confirm when he wants to go surfing.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the David Turner conversations
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
                    ]
                ),
                # Milestone 1 – Verify that David Turner conversations in whatsapp
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
                                        "conversation_name": {
                                            "value": "David Turner",
                                            "partial": False,
                                        },
                                    },
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
                # Milestone 2 – A new WhatsApp message is sent to David Turner asking about surfing
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
                                                "david.turner@example.com",
                                                "+1 12345-6789-1000-9876",
                                            )
                                        ]
                                    ],
                                    "content": "surfing",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-11T07:55:00-08:00",
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
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # tool usage → confirmation of correct thread
                (1, 2),  # confirmation → new outgoing message
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_60eb9b6c-f0b7-4a6b-8a53-7e0c47cc976e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "messaging",
                "whatsapp_messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T15:25:00-08:00",
            is_read_time="2024-12-12T15:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know if David has gotten back to you so you can block off time for the surf over the weekend. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has David replied to me?",
                },
            ],
            reasoning="The user wants to know if David has replied to them. I should first figure out who David is. I will check the user's Contacts. \nHmm, looks like the user only has one David in their Contacts, David Turner, so this must be who the user means. Next I will check Messages for a message from David. I do not see one. I should check WhatsApp next. \nLooks like the user sent the last message to David at 07:50 on 2024-12-11 with content \"Looking forward to it! Just let me know when it's confirmed.\" so I will tell the user there has been no reply.",
            success_conditions=[
                {
                    "input_text": '1. User is informed that David Turner has not yet replied to their last WhatsApp message "Looking forward to it! Just let me know when it\'s confirmed." sent at 07:50 on 2024-12-11.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent consults WhatsApp history
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
                # Milestone 1 – Agent tells the user that David hasn’t replied yet
                Milestone(
                    snapshot_constraints=[
                        # Check that the response mentions David by name
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "David",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        ),
                        # Check that the response clearly states that no reply has been received
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "hasn't replied",
                                            "has not replied",
                                            "no reply",
                                            "no response",
                                            "hasn't gotten back",
                                            "not responded",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                            },
                        ),
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.PHONE,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_1b4eab37-cbc5-48c4-af28-6fb7a888573d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T08:45:00-08:00",
            is_read_time="2024-12-11T08:45:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to message Dave letting him know he was electric on the waters this morning. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Message Dave on the usual channel; "Killed it today Dave!"',
                },
            ],
            reasoning="Ok so the user wants to message Dave on the usual channel a given message. First I'll establish who Dave is. There is only one Dave in the user's contacts so I assume it is David turner they're looking to message. Next is what the usual channels are which when looking at the user's contact with Dave seems to be whatsapp so thats what I'll use. I will now message David Turner the user's given message at 08:45 on 11 December 2024. ",
            success_conditions=[
                {
                    "input_text": '1. The message "Killed it today Dave!" is sent to David Turner via whatsapp. ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_message",
                "get_all_messages",
                "search_messages",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
            ],
            milestones=[
                # Milestone 0 – The agent tries to identify “Dave” in the channel
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
                                        "get_all_messages",
                                        "search_messages",
                                        "get_all_whatsapp_messages",
                                        "search_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – Confirms that David Turner’s contact information was obtained
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
                                            "participants_names": {
                                                "value": "David Turner",
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
                # Milestone 2 – The text message to David Turner was actually sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least David’s phone (or any of his identifiers) must be present as a participant.
                                    "participants_addresses": [
                                        [
                                            (
                                                "+1 12345-6789-1000-9876",
                                                "david.turner@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "Killed it today Dave!",
                                    "creation_datetime_iso": "2024-12-11T08:45:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Require David’s identifier, allow no extras beyond the union of the tuples
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                # Exact content match is fine – it’s short and precise
                                "content": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_d1f167c8-9d11-4de9-8df2-af1e743ebf82_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "whatsapp_messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T15:00:00-08:00",
            is_read_time="2024-12-11T15:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to see the last message you sent to David. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the last message I sent to David Turner.",
                },
            ],
            reasoning="The user wants to see the last message they sent to David Turner. Let me look for their messages and whatsapp messages. Okay I have found the conversation. I will show the user the last message they sent.",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last message they sent to David Turner on WhatsApp on December 11th at 07:50 that says 'Looking forward to it! Just let me know when it's confirmed.'",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent queries WhatsApp messages
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
                # Milestone 1 – Verify the expected WhatsApp message is returned
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
                                                "value": "Looking forward to it! Just let me know when it's confirmed.",
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
                # Milestone 2 – Agent’s reply to the user includes the correct message text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Looking forward to it! Just let me know when it's confirmed.",
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
                (0, 1),  # WhatsApp search → verify result
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_92812baf-5c4c-4d84-b064-5dad6c224d72_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "whatsapp_messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T08:15:00-08:00",
            is_read_time="2024-12-11T08:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to send another text in your WhatsApp chat with David Turner as you're still awaiting his confirmation. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "WhatsApp David again and tell him 'Hey David, I'm still waiting on the confirmation from you about the surfing next weekend.'.",
                },
            ],
            reasoning="The user wants to WhatsApp someone named David. Firstly I will check the user's contacts and can see only one contact matching named 'David Turner'. Next I will check their WhatsApp chat and can see that today, 11 December 2024 the user was messaging David Turner. This must be the one user intends to send the message to.\n\nNext I shall draft up the message as instructed which says 'Hey David, I'm still waiting on the confirmation from you about the surfing next weekend.' and show it to user for approval. Once they have confirmed no further changes are needed I can send on the text. ",
            success_conditions=[
                {
                    "input_text": "1. A reply text is sent to David Turner's WhatsApp text received on 11 December 2024 at 07:45 saying 'Hey David, I'm still waiting on the confirmation from you about the surfing next weekend.'.",
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
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
            ],
            milestones=[
                # Milestone 0 – Agent uses a tool to look up either the contact entry for David Turner
                #                or the existing WhatsApp conversation where David Turner appears.
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – A new WhatsApp message has been sent to David Turner that
                #               contains the requested text.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At minimum David’s phone number must appear in the conversation
                                    "participants_addresses": [
                                        [
                                            (
                                                "david.turner@example.com",
                                                "+1 12345-6789-1000-9876",
                                            )
                                        ]
                                    ],
                                    "content": "waiting on the confirmation",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-11T08:15:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_31f133d1-0c4d-41f9-b6e1-ad166e910faa_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "whatsapp_messaging",
                "calendar",
                "contact",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T11:00:00-08:00",
            is_read_time="2024-12-12T11:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to set up another surf session with David Turner for on Saturday morning 7am via WhatsApp. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to set up another surf session with David on Saturday at 7 am, can you send him a message ask about wave conditions as usual? ",
                },
            ],
            reasoning="User would like to set up an early morning surf session with David for the upcoming Saturday at 07:00. \n\n The user communicates with David via Whatsapp. I will send David Turner a whatsapp message with potential surfing session on December 14 7 am and ask about wave conditions. ",
            success_conditions=[
                {
                    "input_text": "1. Whatsapp Message is sent to David Turner requesting a surf session on Saturday at 7 am and asking about wave conditions. ",
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
                "create_calendar_event",
                "send_whatsapp_message",
                "send_message",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 — the agent tries to retrieve David Turner’s contact information
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
                # Milestone 1 — confirm that David Turner’s contact was actually returned
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
                                                "value": "David Turner",
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
                # Milestone 2 — a new outgoing message via whatsapp is sent to David Turner confirming the 18 th at 7 am session
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Both Lucas (self) and David must be in the thread
                                    "participants_addresses": [
                                        [
                                            (
                                                "david.turner@example.com",
                                                "+1 12345-6789-1000-9876",
                                            )
                                        ]
                                    ],
                                    # Body should mention wave condition
                                    "content": "wave",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-12T11:00:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_92812baf-5c4c-4d84-b064-5dad6c224d72_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "whatsapp_messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T08:15:00-08:00",
            is_read_time="2024-12-11T08:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to send another text in your WhatsApp chat with David Turner as you're still awaiting his confirmation. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply my surfing buddy saying 'Hey David, I'm still waiting on the confirmation from you about the surfing next weekend. While we're young, David....'.",
                },
            ],
            reasoning="The user wants to reply someone named 'surfing buddy'. Firstly I will check the user's contacts and can see not one contact matching this. Although I can see a contact named 'David Turner' whose alias is 'surfing buddy'. This must be the one user intends to send the message to.\n\nNext I will check their WhatsApp chat and can see that today, 11 December 2024 the user was messaging David Turner. \n\nNext I shall draft up the message as instructed which says 'Hey David, I'm still waiting on the confirmation from you about the surfing next weekend. While we're young, David....' and show it to user for approval. Once they have confirmed no further changes are needed I can send on the text. ",
            success_conditions=[
                {
                    "input_text": "1. A reply text is sent to David Turner's WhatsApp text received on 11 December 2024 at 07:45 saying 'Hey David, I'm still waiting on the confirmation from you about the surfing next weekend. While we're young, David....'.",
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
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the surfing buddy contact (David Turner)
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
                # Milestone 1 – Verify that David Turner was one of the contacts returned from Milestone 0
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
                                        "full_name": {
                                            "value": "David Turner",
                                            "partial": False,
                                        },
                                        "phone_number": {
                                            "value": "+1 12345-6789-1000-9876",
                                            "partial": False,
                                        },
                                    },
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
                # Milestone 2 – Agent looks up the David Turner conversations
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
                    ]
                ),
                # Milestone 3 – Verify that David Turner conversations in whatsapp
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
                                        "conversation_name": {
                                            "value": "David Turner",
                                            "partial": False,
                                        },
                                    },
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
                    ]
                ),
                # Milestone 4 – A new WhatsApp message is sent to David Turner with the expected content
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
                                                "david.turner@example.com",
                                                "+1 12345-6789-1000-9876",
                                            )
                                        ]
                                    ],
                                    "content": "I'm still waiting on the confirmation",
                                    "creation_datetime_iso": "2024-12-11T08:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact search → verify David retrieved
                (2, 3),  # David retrieved → WhatsApp message sent
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_d1f167c8-9d11-4de9-8df2-af1e743ebf82_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "whatsapp_messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T15:00:00-08:00",
            is_read_time="2024-12-11T15:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to see the last message you sent to David. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the last message I sent to my surfing buddy on WhatsApp.",
                },
            ],
            reasoning="The user wants to see the last message they sent to their surfing buddy on WhatsApp. Let me look in Contacts to see who that is. It is David Turner. Let me look for their messages. Okay I have found the conversation. I will show the user the last message they sent.",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last message they sent to David Turner on WhatsApp on December 11th at 07:50 that says 'Looking forward to it! Just let me know when it's confirmed.'",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent queries WhatsApp history
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
                # Milestone 1 – The expected WhatsApp message is found in the tool output
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
                                                "value": "Looking forward to it! Just let me know when it's confirmed.",
                                                "partial": False,
                                            },
                                            "sender_name": {
                                                "value": "Coach Lucas",
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
                # Milestone 2 – Agent replies to the user with the correct message content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Looking forward to it! Just let me know when it's confirmed.",
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
                (0, 1),  # Tool called → validate tool output
                (1, 2),  # Tool output validated → user response
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_1b4eab37-cbc5-48c4-af28-6fb7a888573d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "calendar",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T07:29:00-08:00",
            is_read_time="2024-12-11T07:29:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to message Dave letting him know he was electric on the waters this morning. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Text my surfing mate this morning in our usual way; "You\'ve killed it today!"',
                },
            ],
            reasoning="Ok so the user wants to text his surfing mate a given message. First is the recipient which is David Turner based on the calendar. Next is the method, he only communicates with David via Whatsapp. I will now message David turner via whatsapp the user's given message. ",
            success_conditions=[
                {
                    "input_text": '1. The message "You\'ve Killed it today!" is sent to David Turner via whatsapp message. ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_message",
                "send_whatsapp_message",
                "search_calendar_events",
                "get_all_calendars",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – The agent tries to find David Turner in the Contacts database
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
                # Milestone 1 – Verify that David Turner (and his phone number) appeared in the
                #               results returned by the contact-lookup carried out in Milestone 0
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
                                                "value": "Early Morning Surfing Session with David",
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
                # Milestone 2 – The agent tries to find David Turner in message histories
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
                    ]
                ),
                # Milestone 3 – Verify that David Turner conversations
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
                                            "participants_names": {
                                                "value": "David Turner",
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
                                "content": column_one_similarity,
                            },
                        )
                    ]
                ),
                # Milestone 4 – Confirm that a new outgoing text message was created to David Turner
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require that BOTH Lucas and David participate in the convo
                                    "participants_addresses": [
                                        [
                                            (
                                                "+1 12345-6789-1000-9876",
                                                "david.turner@example.com",
                                            ),  # David Turner
                                        ]
                                    ],
                                    "content": "killed it today",
                                    "creation_datetime_iso": "2024-12-11T07:29:00-08:00",
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
                        DatabaseNamespace.SANDBOX
                    ],  # ignore any sandbox tool-trace rows
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (2, 3),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_60eb9b6c-f0b7-4a6b-8a53-7e0c47cc976e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "messaging",
                "whatsapp_messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T15:25:00-08:00",
            is_read_time="2024-12-12T15:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want a yes or no answer to whether your friend has replied back about your plan for next weekend, so you can block off time for it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has my friend replied back about our plan for next weekend? Yes or No.",
                },
            ],
            reasoning="The user wants a yes or no answer about whether their friend has replied about the plan for next weekend. First I need to work out which plan and which friend. \nSearching the user's messages for the weekend plan, the only thread about it is on WhatsApp with David Turner, where at 07:40 on 2024-12-11 the user wrote about planning their next session for next weekend. \nDavid answered at 07:45 saying early morning should be perfect and that he would confirm back soon, and the user then asked at 07:50 to be told once it was confirmed. \nThere is nothing from David after that, so he has not replied back and the answer is no.",
            success_conditions=[
                {
                    "input_text": "1. User is told no - David Turner has not replied since the user asked him at 07:50 on 2024-12-11 to confirm a time for next weekend. His last message, at 07:45, said he would confirm back soon and nothing has arrived since.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – agent looks up the WhatsApp thread about the weekend plan
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
                    ]
                ),
                # Milestone 1 – retrieved WhatsApp thread shows the last message from Coach Lucas
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
                                                "value": "Coach Lucas",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Looking forward to it! Just let me know when it's confirmed.",
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
                # Milestone 2 – agent tells the user that David has not replied yet
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
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # WhatsApp lookup -> the unanswered message in the result
                (1, 2),  # -> the yes or no answer
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_0f1ae8c2-fd28-4b88-bdd1-7b94984ce4a8_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "whatsapp_messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T15:00:00-08:00",
            is_read_time="2024-12-11T15:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to check if David got back to you about the next surfing session. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has David confirmed the next session yet? Yes or no.",
                },
            ],
            reasoning="I need to check WhatsApp to see whether David has confirmed the next session. I see there's a chat on WhatsApp with someone called David Turner. I'll assume this is the correct person. David's last message only said he would confirm back soon, and he has not sent a confirmation since, so he has not confirmed yet. I let the user know by responding 'No'.",
            success_conditions=[
                {
                    "input_text": "1. User has been informed with 'no', as David Turner has not yet confirmed the next surf session in the WhatsApp chat.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks at WhatsApp messages
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
                    ]
                ),
                # Milestone 1 – Verify that the WhatsApp search returned a message involving David Turner
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
                                                "value": "David Turner",
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
                # Milestone 2 – Agent informs the user whether David has replied (should convey no reply)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("hasn't", "has not", "no", "not")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
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
            name="LUCAS_GARCIA_19_5fab516a-faa9-4608-8e23-7c0014513869_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_19",
                "whatsapp_messaging",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T08:30:00-08:00",
            is_read_time="2024-12-11T08:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are wondering what time you sent in your last WhatsApp message to David Turner "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I send that last WhatsApp message to David Turner",
                },
            ],
            reasoning="The user wants to know when they sent their last WhatsApp message to David Turner. First thing I need to do is search the user's WhatsApp messages to find a contact with a name that matches. Ok I found a conversation with a David Turner. Now that I have found that I just need to take a look at the last message sent by the user. Ok now that I have that I will retrieve the time of the message and inform the user",
            success_conditions=[
                {
                    "input_text": "1. The time of the WhatsApp message sent by the user on December 11, 2024 at 07:50 to David Turner is presented to the user",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_whatsapp_messages", "search_whatsapp_messages"],
            milestones=[
                # Milestone 0 – Agent queries WhatsApp messages
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
                # Milestone 1 – Confirm the specific WhatsApp message (Dec-11-2024 07:50) was returned
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
                                                "value": "Coach Lucas",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-11T07:50:00-08:00",
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
                # Milestone 2 – Agent informs the user of the correct time
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
                                            "07:50",
                                            "7:50",
                                            "07:50 am",
                                            "7:50 am",
                                            "07:50 AM",
                                            "7:50 AM",
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
                (0, 1),  # Retrieval → verification of message existence
                (1, 2),  # Verification → user-facing answer
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_bdbb9a70-44cc-448f-bce2-5b9a740c9b38_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "contact",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T10:00:00-08:00",
            is_read_time="2024-12-13T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You forgot which beach you surfed at last Wednesday "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where did the coolest surf instructor and I go last Wednesday?",
                },
            ],
            reasoning="The user wants to know where they went with 'the coolest surf instructor' last Wednesday. \n\nFirst, I will need to figure out who the user is referring to. I will go through the user contacts. There I see that one contact, David Turner, is reported to work as a surf instructor. It is likely the user is referring to this person. \n\nAlso, the user is referring to an event taking place 'last Wednesday'. The request is being made on Friday December 13, 2024 at 10:00. Looking at the calendar, I see there is an event titled \"Early Morning Surfing Session with David\" from 07:00-08:30 on Wednesday December 11 2024 with David Turner mentioned as an invitee. This must be what the user is asking about. I explore the event details, and I see the location is listed there. I'll inform the user the event took place at Local Beach, Orchard County, CA",
            success_conditions=[
                {
                    "input_text": '1. The location details of the event "Early Morning Surfing Session with David" from 07:00-08:30 on the 11 December 2024 are given',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – the agent queries the calendar to locate last Wednesday’s surf event
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
                # Milestone 1 – confirm the correct calendar event (with location) was returned
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
                                                "value": "Early Morning Surfing Session with David",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Local Beach",
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
                # Milestone 2 – the agent informs the user of the correct location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Local Beach",
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
                (0, 1),  # Calendar query → verify event retrieved
                (1, 2),  # Event verified → respond to user with location
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_64298015-5217-4ac2-bdc6-a5f146a8efa0_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T14:20:00-08:00",
            is_read_time="2024-12-11T14:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are feeling unwell and you need to cancel your next upcoming event. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Cancel the upcoming event.",
                },
            ],
            reasoning="The user wants to cancel an event. They have stated that it is the upcoming event that they want to cancel. The only event scheduled for today is Pre-Holiday Fitness Celebration scheduled from 17:00 to 19:00. I'll delete this event.",
            success_conditions=[
                {
                    "input_text": "1. Cancel the upcoming event Pre-Holiday Fitness Celebration scheduled December 11 from 17:00 to 19:00.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events to locate the one that must be cancelled
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
                # Milestone 1 – Confirm the intended event appeared in the tool output from Milestone 0
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
                                                "value": "Pre-Holiday Fitness Celebration",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-11T17:00:00-08:00",
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
                # Milestone 2 – Event has been cancelled (removed from the calendar database)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Pre-Holiday Fitness Celebration",
                                    "start_datetime_iso": "2024-12-11T17:00:00-08:00",
                                    "end_datetime_iso": "2024-12-11T19:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial snapshot
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
            name="LUCAS_GARCIA_19_8f64f230-6c7f-46c6-85a5-e507a83ccc9a_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "calendar",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T17:00:00-08:00",
            is_read_time="2024-12-13T17:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "Your surfing session went really well this morning! You want to schedule another one in the late afternoon at 4 pm next Friday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Create calendar event called "Evening Surf Session" next Friday at 4 with my surfing buddy as an invitee.',
                },
            ],
            reasoning='The user wants me to create a new event. They gave me the name of the event, "Evening Surf Session", but I have some things to figure out. For one, I need to figure out when "next Friday" is. If today is Friday December 13th 2024, then next Friday must be the 20th December 2024. I\'ll check the user\'s calendar to see if he has any events for that day, but it looks all clear. \nFinally, the user has asked that the surfing buddy be added as an invitee to this event. I see David Turner in the user\'s contacts as a surfing buddy. With the user\'s confirmation, I will create the event "Evening Surf Session" on December 20th 2024 at 16:00',
            success_conditions=[
                {
                    "input_text": '1. A calendar event is created called "Evening Surf Session" for 20th December 2024 at 16:00 with David Turner as an Invitee.',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 — The agent looks up the “surfing buddy” contact
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
                # Milestone 1 — Confirm the contact retrieved is David Turner
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
                                                "value": "David Turner",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "david.turner@example.com",
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
                # Milestone 2 — Calendar event “Evening Surf Session” has been created for 4 pm on 20-Dec-2024 with David Turner invited
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Evening Surf Session",
                                    "start_datetime_iso": "2024-12-20T16:00",
                                    "attendees_names": [["David Turner"]],
                                    "creation_datetime_iso": "2024-12-13T17:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,  # ensure correct date & time substring
                                "attendees_names": column_list_subset_match_similarity,  # must include David, allow extras (e.g., Lucas),
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
                (0, 1),  # Contact lookup → confirm contact
                (1, 2),  # Contact confirmed → event created
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_8f64f230-6c7f-46c6-85a5-e507a83ccc9a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "calendar",
                "contact",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T17:00:00-08:00",
            is_read_time="2024-12-13T17:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "Your surfing session went really well this morning! You want to schedule another one with your surfing buddy David in the late afternoon at 4 pm next Friday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Create calendar event called "Evening Surf Session" on December 20th 2024 at 16:00 with David as an invitee, make sure I don\'t have conflicts.',
                },
            ],
            reasoning="The user wants me to create a new event. They gave me the name of the event, \"Evening Surf Session\" and it will take place on December 20th 2024 at 16:00.  I'll check the user's calendar to see if he has any events for that day, but it looks all clear. Finally, the user has asked that David be added as an invitee to this event. I see David Turner in the user's contacts as a surfing buddy. With the user's confirmation, I will create the event \"Evening Surf Session\" on December 20th 2024 at 16:00",
            success_conditions=[
                {
                    "input_text": '1. A calendar event is created called "Evening Surf Session" for 20th December 2024 at 16:00 with David Turner as an Invitee and no conflict found.',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent tries to locate David Turner in the contacts/calendars
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
                # Milestone 1 — Confirm the contact retrieved is David Turner
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
                                                "value": "David Turner",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "david.turner@example.com",
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
                # Milestone 2 – A calendar event was created on 2024-12-20 at 16:00 named "Evening Surf Session" with David Turner invited
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Evening Surf Session",
                                    "start_datetime_iso": "2024-12-20T16:00",  # substring match below lets the timezone vary
                                    "attendees_names": [["David Turner"]],
                                    "creation_datetime_iso": "2024-12-13T17:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_19_64298015-5217-4ac2-bdc6-a5f146a8efa0_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T14:20:00-08:00",
            is_read_time="2024-12-11T14:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are feeling unwell and you need to cancel your next upcoming event. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Cancel the upcoming event Pre-Holiday Fitness Celebration scheduled from 17:00 to 19:00.",
                },
            ],
            reasoning="The user wants to delete the event Pre-Holiday Fitness Celebration scheduled from 17:00 to 19:00. I'll delete that now.",
            success_conditions=[
                {
                    "input_text": "1. Cancel the upcoming event Pre-Holiday Fitness Celebration scheduled December 11 from 17:00 to 19:00.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
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
                    ]
                ),
                # Milestone 1 – Confirm the desired event appears in the calendar tool output
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
                                                "value": "Pre-Holiday Fitness Celebration",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-11T17:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-11T19:00:00-08:00",
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
                # Milestone 2 – Verify the event has been removed (canceled) from the calendar database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Pre-Holiday Fitness Celebration",
                                    "start_datetime_iso": "2024-12-11T17:00:00-08:00",
                                    "end_datetime_iso": "2024-12-11T19:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
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
            name="LUCAS_GARCIA_19_bdbb9a70-44cc-448f-bce2-5b9a740c9b38_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "contact",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T10:00:00-08:00",
            is_read_time="2024-12-13T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You forgot which beach you surfed at last Wednesday "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where did my surfing buddy and I go last Wednesday?",
                },
            ],
            reasoning="The user wants to know where they went with their surfing buddy  last Wednesday. \n\nFirst, I will need to figure out who the user is referring to. I will go through the user contacts. There I see that one contact, David Turner, is tagged there as a 'Surfing buddy'. It is likely the user is referring to this person. \n\nNow, the user is referring to an event taking place 'last Wednesday'. The request is being made on Friday December 13, 2024 at 10:00. If I look at the calendar, I see there is an event titled \"Early Morning Surfing Session with David\"  on Wednesday December 11 2024 from 07:00 to 08:30 with David Turner mentioned as an invitee. This must be what the user is asking about. I go through the event details, and I see the location is listed there. I'll inform the user the event took place at Local Beach, Orchard County, CA",
            success_conditions=[
                {
                    "input_text": '1. The location details of the event "Early Morning Surfing Session with David" from 07:00-08:30 on the 11 December 2024 are given',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar information (tool invocation)
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
                # Milestone 1 – The expected surfing event is returned with correct location
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
                                                "value": "Early Morning Surfing Session with David",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Local Beach",
                                                "partial": True,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-11T07:00:00-08:00",
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
                            reference_milestone_node_index=0,  # Use output from Milestone 0
                        )
                    ]
                ),
                # Milestone 2 – Agent informs the user of the correct surfing location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("Local Beach", "Orchard County")],
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
            name="LUCAS_GARCIA_19_5fab516a-faa9-4608-8e23-7c0014513869_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "whatsapp_messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T08:30:00-08:00",
            is_read_time="2024-12-11T08:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are wondering what time you sent in your last WhatsApp message to David Turner "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I send my most recent WhatsApp message",
                },
            ],
            reasoning="The user wants to know when they sent their most recent WhatsApp message. First thing I need to do is search the user's WhatsApp messages to try and find the one that was sent most recently by the user. Ok I found it in a conversation with David Turner.  Ok now that I have that I will retrieve the time of the message and inform the user",
            success_conditions=[
                {
                    "input_text": "1. The time of the WhatsApp message sent by the user on December 11, 2024 at 07:50 to David Turner is presented to the user",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_whatsapp_messages", "search_whatsapp_messages"],
            milestones=[
                # Milestone 0 – the agent queries WhatsApp messages
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
                    ]
                ),
                # Milestone 1 – confirms that the WhatsApp message from 2024-12-11 07:50 was returned
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
                                                "value": "2024-12-11T07:50:00-08:00",
                                                "partial": False,
                                            },
                                            "sender_name": {
                                                "value": "Coach Lucas",
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
                # Milestone 2 – the agent tells the user the correct time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("07:50", "7:50")],
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
            name="LUCAS_GARCIA_19_0f1ae8c2-fd28-4b88-bdd1-7b94984ce4a8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_19",
                "whatsapp_messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T15:00:00-08:00",
            is_read_time="2024-12-11T15:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to check if David got back to you about the next surfing session. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has my surfing buddy confirmed the next session yet? yes or no.",
                },
            ],
            reasoning="I need to see whether the user's surfing buddy has confirmed the next session, so I'll find their contact. I found one contact with the alias of surfing buddy, David Turner. I'll check their WhatsApp chat. David's last message only said he would confirm back soon and he has not sent a confirmation yet, so he has not confirmed. I let the user know there is no confirmation yet by replying 'No'.",
            success_conditions=[
                {
                    "input_text": "1. The user has been replied with 'No', as David Turner has not yet confirmed the next surf session in the WhatsApp chat.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks up WhatsApp messages with David Turner
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
                # Milestone 1 – The retrieved WhatsApp result set includes the last message sent by Lucas (no new David message)
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
                                                "value": "Coach Lucas",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-11T07:50:00-08:00",
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
                # Milestone 2 – The agent informs the user that David has not replied yet
                Milestone(
                    snapshot_constraints=[
                        # Contains a negative/reply-not-yet phrase
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "hasn't",
                                            "not",
                                            "no",
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
    ]
