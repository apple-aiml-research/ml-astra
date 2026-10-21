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
    column_list_subset_match_similarity,
    column_list_tuple_contains_similarity,
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_any_similarity,
    removal_similarity,
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


def get_TAG_LUCAS_GARCIA_pilot_plot_10(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="LUCAS_GARCIA_10_9a0a1e3f-57ab-4af5-8046-68b4f2c07c47_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_10",
                "contact",
                "messaging",
                "whatsapp_messaging",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T16:38:00-08:00",
            is_read_time="2024-12-06T16:34:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know what your last WhatsApp message from David Turner says.\n "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What did my instructor's text message say?",
                },
            ],
            reasoning="User wants to know what their instructor's text message said. I'll check their contacts and see if there's any contact that shows as user's instructor. Ok, I see there are fitness instructor whose name is  Jessica Lin and surf instructor whose name is David Turner. I'll check user's messages and see if either of these two contacts exchanged texts with the user. Ok, I didn't find any text message threads with these two contacts. I'll keep looking at other message apps, such as whatsApp. Ok, I found a whatsApp message from David Turner that literally just came in. I believe that's the message user refers to even though user mistakenly said \"text message\". I'll read David Turner's whatsApp message received on December 6 at 16:35 to user. ",
            success_conditions=[
                {
                    "input_text": "1. The last WhatsApp message received from David Turner is read out loud to the user. \n",
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
                # Milestone 0 – Agent uses WhatsApp retrieval tool(s) to look for the instructor's message
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
                                # Allow either a direct search or a full fetch of WhatsApp messages
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
                # Milestone 1 – Confirm that the WhatsApp message from David Turner was retrieved
                # and matches key identifying fields (sender and content snippet)
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
                                            # Verify we found the WhatsApp message from David Turner
                                            "sender_name": {
                                                "value": "David Turner",
                                                "partial": False,
                                            },
                                            "participants_names": {
                                                # Conversation participants include Lucas and David
                                                "value": [
                                                    "Coach Lucas",
                                                    "David Turner",
                                                ],
                                                "partial": True,
                                            },
                                            # Check a distinctive phrase from the message body
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
                                "content": column_one_similarity,
                            },
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – Agent tells the user what the last message from David said
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            # We only care that the agent's reply paraphrases or quotes
                            # the actual WhatsApp message content from David Turner.
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Require that the response includes the core idea / phrase
                                    "content": "can't wait to catch some waves. What time are you thinking?",
                                }
                            ),
                            column_similarity_measure={
                                # Use substring / fuzzy match so paraphrasing is allowed,
                                # but the key content of David's message must be present.
                                "content": column_contains_similarity,
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (
                    0,
                    1,
                ),  # WhatsApp search/fetch → confirm correct David Turner message found
                (1, 2),  # Correct message identified → user is told what it says
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_81295fbe-d03d-4dbc-89ab-779cab47839c_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_10",
                "whatsapp_messaging",
                "contact",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T17:05:00-08:00",
            is_read_time="2024-12-06T17:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to send another WhatsApp message to David Turner saying \"surf's up brah, let's curl the biggest wave and rip the fattest cloud and ride the last gnar. \" "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Message the person again who I'm riding waves with later and say \"surf's up brah, let's curl the biggest wave and rip the fattest cloud and ride the last gnar\"",
                },
            ],
            reasoning="The user wants to send a message again to a person. I need to figure out who the recipient will be. They said to message the person they're riding waves with later. Let me look at their calendar events for later today. I don't see anything with \"riding waves\" in the event name, but I do see an event named \"Surfing Session with David\" at 18:00 today. \"riding waves\" is a reasonable way to describe a surfing session, so I'll assume this is the event the user is talking about. So now I need to see who is invited to this event; that is the person the user wants to text. I see David Turner is listed as an invitee, so that's who I'll send the message to. The user only has exchanged whatsapp messages with David, so I'll send the message on whatsapp: \"surf's up brah, let's curl the biggest wave and rip the fattest cloud and ride the last gnar\"",
            success_conditions=[
                {
                    "input_text": "1. A whatsapp message is sent to David Turner saying \"surf's up brah, let's curl the biggest wave and rip the fattest cloud and ride the last gnar.\"",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
                "send_message",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks up who the user is “riding waves with later”.
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
                                        "get_all_calendars",
                                        "search_calendar_events",
                                        "get_all_contacts",
                                        "search_contacts",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – A WhatsApp message is sent to David Turner with the requested content.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At minimum, David’s phone number must be among the participants.
                                    "participants_addresses": [
                                        [
                                            (
                                                "david.turner@example.com",
                                                "+1 12345-6789-1000-9876",
                                            )
                                        ]
                                    ],
                                    "content": "surf's up brah",
                                    "creation_datetime_iso": "2024-12-06T17:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_86688dc6-5f9f-49ee-976b-bdfa590cb2bf_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_10",
                "calendar",
                "contact",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T21:00:00-08:00",
            is_read_time="2024-12-06T21:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "David needs some motivation so you invited him to tomorrow's talk. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Add David to the motivational talk at local gym tomorrow.",
                },
            ],
            reasoning="The user is asking to edit invitees of an event.\nFirst, I should find the queried event in the user's calendar. I see an exact match for the user's query, Motivational Talk at Local Gym scheduled for December 07, 2024, 09:00-10:00.\nNext, I will locate the named person in the user's contacts. I have found David Turner in the user's contacts.\nFinally I will add David as an invitee to the named event. David Turner is now an invitee of Motivational Talk at Local Gym scheduled for December 07, 2024, 09:00-10:00. I should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. David Turner is added as an invitee to Motivational Talk at Local Gym scheduled for December 07, 2024, 09:00-10:00.",
                    "statefullness": "Stateful",
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
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the calendar to locate the “Motivational Talk” event
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
                # Milestone 1 – Confirm the desired calendar event was actually returned in Milestone 0
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
                                                "value": "Motivational Talk at Local Gym",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T09:00:00-08:00",
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
                # Milestone 2 – Agent searches contacts to resolve “David Turner”
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
                # Milestone 3 – Confirm that the contact search actually contained David Turner
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
                # Milestone 4 – Calendar event updated so that David Turner is now an attendee
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Motivational Talk at Local Gym",
                                    "start_datetime_iso": "2024-12-07T09:00:00-08:00",
                                    "end_datetime_iso": "2024-12-07T10:00:00-08:00",
                                    "attendees_names": [["David Turner"]],
                                    "creation_datetime_iso": "2024-12-06T21:00:00-08:00",
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
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # found event
                (2, 3),  # found contact
                (1, 4),  # after locating event, it gets modified
                (3, 4),  # after confirming contact, event is modified
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_f8240144-b866-48f1-b20f-ce5275a88cac_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_10",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T09:35:00-08:00",
            is_read_time="2024-12-06T09:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are worried that you have scheduled the Surfing Session with David for the wrong time so you decide to check the time "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you tell me what time I scheduled the Surfing Session with David for",
                },
            ],
            reasoning='The user wants to know what time they scheduled their Surfing Session with David for. First thing I need to do is look at the user\'s calendar and see if there are any events that match that name. Ok I found one named "Surfing Session with David" on December 06, 2024 at 18:00-19:30. This must be the event the user is referring to. Now that I have found it I can retrieve the time it is scheduled for and inform the user\n',
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The time of the event "Surfing Session with David" on December 06, 2024 at 18:00-19:30 is presented to the user',
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent uses a calendar-lookup tool to find the event
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
                # Milestone 1 – The returned calendar result contains the correct event with the expected start time
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
                                                "value": "Surfing Session with David",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-06T18:00:00-08:00",
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
                            reference_milestone_node_index=0,  # depend on tool call in Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – Agent tells the user the scheduled time
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
                                            "6 pm",
                                            "6 p.m.",
                                            "6pm",
                                            "6:00 pm",
                                            "6:00pm",
                                            "6:00 p.m.",
                                            "18:00",
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
                (0, 1),  # calendar lookup → verify correct event
                (1, 2),  # event verified → user informed
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_e6efac77-448d-41a9-a569-4ac2613ecd06_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_10",
                "messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T20:55:00-08:00",
            is_read_time="2024-12-06T20:55:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        'Another text is sent to David Turner saying, Hey David, funny story – I said we should make the most of the day, but then i fell asleep on the couch and woke up in the plate of baked beans I was eating.  Totally gnarly.  Let\'s try to meet up at 6pm tomorrow instead.  Cowabunga, Lucas "The Kookus" Garcia. '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send my surfing buddy this text via Whatsapp: Hey David, funny story – I said we should make the most of the day, but then i fell asleep on the couch and woke up in the plate of baked beans I was eating. Totally gnarly. Let\'s try to meet up at 6pm tomorrow instead. Cowabunga, Lucas "The Kookus" Garcia. ',
                },
            ],
            reasoning="User Lucas Garcia wants to send a surfing buddy of his named David a text message. I see from contacts and the content of the desired message that this must be David Turner, who goes by the alias Surfing Buddy. I shall prepare the text for user and present it for approval before sending. ",
            success_conditions=[
                {
                    "input_text": 'A text message is sent to David Turner saying, Hey David, funny story – I said we should make the most of the day, but then i fell asleep on the couch and woke up in the plate of baked beans I was eating. Totally gnarly. Let\'s try to meet up at 6pm tomorrow instead. Cowabunga, Lucas "The Kookus" Garcia. ',
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
                "send_message",
                "send_whatsapp_message",
            ],
            milestones=[
                # Milestone 0 – Verify that a new whatsapp message was sent to David Turner with the correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require both Lucas’s and David’s phone numbers to be present (order-insensitive, no extras)
                                    "participants_addresses": [
                                        [
                                            (
                                                "+1 12345-6789-1000-1234",
                                                "lucas.garcia@example.com",
                                            ),
                                            (
                                                "+1 12345-6789-1000-9876",
                                                "david.turner@example.com",
                                            ),
                                        ]
                                    ],
                                    # Key phrase from the requested text to ensure it is the right message
                                    "content": "baked beans",
                                    "creation_datetime_iso": "2024-12-06T20:55:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial state
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_f8240144-b866-48f1-b20f-ce5275a88cac_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_10",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T09:35:00-08:00",
            is_read_time="2024-12-06T09:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are worried that you have scheduled the Surfing Session with David for the wrong time so you decide to check the time "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When's the Surfing session?",
                },
            ],
            reasoning='The user wants to know what time they scheduled their Surfing Session. First thing I need to do is look at the user\'s calendar and see if there are any events that match that name. Ok I found one named "Surfing Session with David" on December 06, 2024 at 18:00-19:30. This must be the event the user is referring to. Now that I have found it I can retrieve the time it is scheduled for and inform the user\n',
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The time of the event "Surfing Session with David" on December 06, 2024 at 18:00-19:30 is presented to the user',
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent looks up the calendar to find the surfing event
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
                # Milestone 1 – Confirm the surfing event with correct time is present in the tool output from Milestone 0
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
                                                "value": "Surfing Session with David",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-06T18:00:00-08:00",
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
                # Milestone 2 – The agent tells the user the correct time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("6 pm", "6:00 pm", "18:00", "6pm")],
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
                (0, 1),  # calendar lookup → verify correct event in output
                (1, 2),  # verified event → inform user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_86688dc6-5f9f-49ee-976b-bdfa590cb2bf_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_10",
                "calendar",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T21:00:00-08:00",
            is_read_time="2024-12-06T21:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "David needs some motivation so you invited him to tomorrow's talk. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Add my surfing buddy to the motivational talk at local gym tomorrow.",
                },
            ],
            reasoning="The user is asking to edit invitees of an event.\nFirst, I should find the queried event in the user's calendar. I see an exact match for the user's query, Motivational Talk at Local Gym scheduled for December 07, 2024, 09:00-10:00.\nNext, I will locate the named person in the user's contacts. The user has referred to a surfing buddy, I can see only one potential match, David Turner, who is tagged Surfing buddy in the user's contacts. I have found David Turner in the user's contacts.Finally I will add David as an invitee to the named event.\nDavid Turner is now an invitee of Motivational Talk at Local Gym scheduled for December 07, 2024, 09:00-10:00. I should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. David Turner is added as an invitee to Motivational Talk at Local Gym scheduled for December 07, 2024, 09:00-10:00.",
                    "statefullness": "Stateful",
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
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – agent looks up the calendar to locate the motivational talk
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
                # Milestone 1 – verifies the correct event was returned from the calendar lookup
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
                                                "value": "Motivational Talk at Local Gym",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T09:00:00-08:00",
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
                # Milestone 2 – the calendar event is updated so that David Turner is now an attendee
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Motivational Talk at Local Gym",
                                    "start_datetime_iso": "2024-12-07T09:00:00-08:00",
                                    "end_datetime_iso": "2024-12-07T10:00:00-08:00",
                                    "attendees_names": [["David Turner"]],
                                    "creation_datetime_iso": "2024-12-06T21:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Require that David Turner is now included; allow existing attendees
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # calendar search → confirm correct event
                (1, 2),  # event identified → event updated with David Turner
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_ff4e872f-a4dd-4292-b464-63e518298553_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_10",
                "calendar",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T17:30:00-08:00",
            is_read_time="2024-12-06T17:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to double check the time you're due to surf with Dave. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When am I surfing with Dave again?",
                },
            ],
            reasoning='Ok so the user wants to know when they are surfing with Dave. First I\'ll establish who Dave is. Dave is a shortening of David and there is only one in the user\'s contacts which is David Turner. Next I will look for events with David that have the key word surfing or similar terms. I have found the event "Surfing Session with David" which must be what they are referring to. Next I will look at the start time of this event. I will now inform the user that the event "Surfing Session with David" is due to start at 18:00 on 6 December 2024. ',
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The user is informed that the event "Surfing Session with David" is due to start at 18:00 on 6 December 2024. ',
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent consults the calendar
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
                # Milestone 1 – The expected surfing event is returned from the calendar query
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
                                                "value": "Surfing Session with David",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-06T18:00:00-08:00",
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
                # Milestone 2 – The agent informs the user of the correct date and time
                Milestone(
                    snapshot_constraints=[
                        # Check date mention
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "December 6",
                                            "6 December",
                                            "Dec 6",
                                            "2024-12-06",
                                            "today",
                                            "tonight",
                                            "this evening",
                                            "2024-12-06T18:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                        # Check time mention
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "18:00",
                                            "6 pm",
                                            "6pm",
                                            "6 p.m",
                                            "6:00 pm",
                                            "6:00 p.m",
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
                (0, 1),  # Calendar query → confirm event presence
                (1, 2),  # Event found → inform user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_ff4e872f-a4dd-4292-b464-63e518298553_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_10",
                "calendar",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T17:30:00-08:00",
            is_read_time="2024-12-06T17:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to double check the time you're due to surf with Dave. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'When does the event "Surfing Session with David" start?',
                },
            ],
            reasoning='Ok so the user wants to know when does the event "Surfing Session with David" start. First I will find the event as given by the user. Now that I have found the event I will check the start time. I will now inform the user that the event "Surfing Session with David" is due to start at 18:00 on 6 December 2024. ',
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The user is informed that the event "Surfing Session with David" is due to start at 18:00 on 6 December 2024. ',
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (either specific search or full list)
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
                # Milestone 1 – The returned calendar data includes the “Surfing Session with David” event
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
                                                "value": "Surfing Session with David",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-06T18:00:00-08:00",
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
                # Milestone 2 – The user is informed with the correct start time & date
                Milestone(
                    snapshot_constraints=[
                        # Check time mention
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "18:00",
                                            "6 pm",
                                            "6pm",
                                            "6 p.m",
                                            "6:00 pm",
                                            "6:00 p.m",
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
            name="LUCAS_GARCIA_10_9a0a1e3f-57ab-4af5-8046-68b4f2c07c47_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_10",
                "contact",
                "messaging",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
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
                        "You want to know what your last WhatsApp message from David Turner says.\n "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What’s that last WhatsApp message?\n",
                },
            ],
            reasoning="The user wants to know what their last message was, so I will find the message, tell the user who it is from and then read it out. I can see the user just received a message from David Turner on WhatsApp and because this is the most recent message received, I can assume this is the message the user referred to. \n",
            success_conditions=[
                {
                    "input_text": "1. The last WhatsApp message received from David Turner is read out loud to the user. \n",
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
                # Milestone 0 – Agent uses a WhatsApp retrieval tool to look for recent messages
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
                # Milestone 1 – Confirms that a WhatsApp message from David Turner was retrieved
                # (verifies the tool output includes David Turner as sender and the expected content)
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
                                                "value": "Hey Lucas! Definitely, can't wait to catch some waves. What time are you thinking?",
                                                "partial": False,
                                            },
                                            "participants_names": {
                                                "value": [
                                                    "Coach Lucas",
                                                    "David Turner",
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
                            reference_milestone_node_index=0,
                        ),
                    ],
                ),
                # Milestone 2 – Agent tells the user what David's last WhatsApp message says
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Only need to ensure the core message text is relayed to the user
                                    "content": "Hey Lucas! Definitely, can't wait to catch some waves. What time are you thinking?",
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
                (0, 1),  # WhatsApp retrieval → confirm David's message was found
                (
                    1,
                    2,
                ),  # Confirmed retrieval → agent reports the correct message to the user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_302c4be7-5d88-4112-a1e7-fa4f501e9781_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_10",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T10:00:00-08:00",
            is_read_time="2024-12-07T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know where your Surfing Session with David was on yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where was my 'Surfing Session with David' on yesterday?",
                },
            ],
            reasoning="The user wants to know where their 'Surfing Session with David' was on yesterday. This sounds like an event is I will look in Calendar. Hmmm, ah I see an event called surfing. I will open it. I see its full name is indeed Surfing Lesson with David. I see it took place on the 6th of December 2024 from 18:00 to 19:30, at the Local Beach in Orchard County, California. I will inform there user of this.",
            success_conditions=[
                {
                    "input_text": "1.The user is informed that their event 'Surfing Session with David' on December 6th 2024 from 18:00-19:30 occurred at Local Beach, Orchard County, CA.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – the agent looks up calendar information
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
                # Milestone 1 – confirm the correct calendar event was found in the tool result
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
                                                "value": "Surfing Session with David",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Local Beach, Orchard County, CA",
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
                # Milestone 2 – the agent informs the user of the location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Local Beach, Orchard County, CA",
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
                (0, 1),  # tool call → confirm correct event retrieved
                (1, 2),  # event retrieved → agent responds to user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_751fa32e-3564-4b1b-9e93-082194109bdf_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_10",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T14:00:00-08:00",
            is_read_time="2024-12-06T14:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "The weather is terrible so you won't be able to go surfing. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my event in 4 hours. ",
                },
            ],
            reasoning="The user wants to delete the event in 4 hours. I should first figure out what time that will be. It is currently 14:00 so in 4 hours it will be 18:00. I will look for an event at this time. \nLooks like there is one, the Surfing Session with David from 18:00-19:30 on the 6 December 2024, so this must be the event the user meant. \nI will delete the event and let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. Surfing Session with David from 18:00-19:30 on the 6 December 2024 is deleted from Calendar. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up events around the referenced time
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
                # Milestone 1 – Confirm the “Surfing Session with David” event was found
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
                                                "value": "Surfing Session with David",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-06T18:00:00-08:00",
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
                # Milestone 2 – Event is removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Surfing Session with David",
                                    "start_datetime_iso": "2024-12-06T18:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare against initial state
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
            name="LUCAS_GARCIA_10_751fa32e-3564-4b1b-9e93-082194109bdf_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_10",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T14:00:00-08:00",
            is_read_time="2024-12-06T14:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "The weather is terrible so you won't be able to go surfing. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the surf session with David. ",
                },
            ],
            reasoning="The user wants to delete the surf session with David. I should check their Calendar for an event with this name. \nLooks like there is one, the Surfing Session with David from 18:00-19:30 on the 6 December 2024, so this must be the event the user meant. \nI will delete the event and let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. Surfing Session with David from 18:00-19:30 on the 6 December 2024 is deleted from Calendar. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events to find the surf session
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
                # Milestone 1 – Confirm the correct surf session was found in the tool output from Milestone 0
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
                                                "value": "Surfing Session with David",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-06T18:00:00-08:00",
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
                # Milestone 2 – Verify the surf session event has been removed from the Calendar database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Surfing Session with David",
                                    "start_datetime_iso": "2024-12-06T18:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare against initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Found calendar event → confirmed correct match
                (1, 2),  # Confirmed match → event removed
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_302c4be7-5d88-4112-a1e7-fa4f501e9781_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_10",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T10:00:00-08:00",
            is_read_time="2024-12-07T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know where your Surfing Session with David was on yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where was my evening event on yesterday?",
                },
            ],
            reasoning="The user wants to know where their evening event was on yesterday. I will look in Calendar. So yesterday was the 6th of December 2024. The only event they had on in the evening was 'Surfing Session with David'. I will confirm with the user if this is the correct event. I will inform them that it took place at the Local Beach in Orchard County, California and lasted from 18:00 to 19:30.",
            success_conditions=[
                {
                    "input_text": "1.The user is informed that their event 'Surfing Session with David' on December 6th 2024 from 18:00-19:30 occurred at Local Beach, Orchard County, CA.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Calendar lookup initiated
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
                                ),
                            },
                        )
                    ]
                ),
                # Milestone 1 – The correct event with its location is present in the tool output
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
                                                "value": "Surfing Session with David",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Local Beach",
                                                "partial": True,  # allow full address or short form
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
                # Milestone 2 – User receives a message that contains the location
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
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar lookup → verify event & location
                (1, 2),  # Event verified → inform user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_75d3b4a7-4e24-44e5-a0c2-7a9e436a684a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_10",
                "whatsapp_messaging",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
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
                        "You want to know what your last WhatsApp message from David Turner says. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What’s that last WhatsApp message?\n",
                },
            ],
            reasoning="The user wants to know what their last message was, so I will find the message, tell the user who it is from and then read it out. I can see the user just received a message from David Turner on WhatsApp and because this is the most recent message received, I can assume this is the message the user referred to. \n",
            success_conditions=[
                {
                    "input_text": "1. The last WhatsApp message received from David Turner is read out loud to the user. \n",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_whatsapp_messages", "search_whatsapp_messages"],
            milestones=[
                # Milestone 0 – Agent queries WhatsApp messages to locate the most recent one
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
                # Milestone 1 – Agent relays the content of the last message to the user
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
                                            "can't wait to catch some waves",
                                            "can’t wait to catch some waves",
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
                (0, 1),  # Retrieval of WhatsApp message precedes informing the user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_077f4562-27d6-414d-9d13-6fea94bafcfc_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_10",
                "whatsapp_messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T17:05:00-08:00",
            is_read_time="2024-12-06T17:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to send another WhatsApp message to David Turner saying 'surf's up brah, let's curl the biggest wave and rip the fattest cloud and ride the last gnar. ' "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Message my surfing buddy saying 'surf's up brah, let's curl the biggest wave and rip the fattest cloud and ride the last gnar'",
                },
            ],
            reasoning="The user wants to send a message their surfing buddy. Looking in the users contacts I see their name is David Turner.I can see they have been using WhatsApp to message.I'll send the message to him.",
            success_conditions=[
                {
                    "input_text": "1. Send a message to David Turner.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
            ],
            milestones=[
                # Milestone 0 – A new WhatsApp message was sent to David Turner with the requested surfing text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Both Lucas (self) and David must be in the chat
                                    "participants_addresses": [
                                        [
                                            (
                                                "david.turner@example.com",
                                                "+1 12345-6789-1000-9876",
                                            ),
                                        ]
                                    ],
                                    # Key phrase from the requested message
                                    "content": "surf's up brah",
                                    "creation_datetime_iso": "2024-12-06T17:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial DB state
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_4d5e2cb3-3ff8-4251-a132-5f8d85f30423_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_10",
                "calendar",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T21:00:00-08:00",
            is_read_time="2024-12-06T21:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "The surf session was amazing today so you want to schedule another one "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Copy the thing with David to the same time next week",
                },
            ],
            reasoning='The user wants to copy the thing with David to the same time next week. David Turner is the only David in the user\'s contacts. I must determine what thing they are referring to. I\'ll try and find an event in the user\'s calendar including David.\n\nI found an event from earlier today titled "Surfing Session with David" including David Turner. This must be the thing the user wants to copy. I will schedule another "Surfing Session with David" for 6:00 pm on December 13th and inform the user.\n',
            success_conditions=[
                {
                    "input_text": '1. The calendar event "Surfing Session with David" is found',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": '2. The calendar event "Surfing Session with David" is copied to December 13th at 6:00 pm',
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
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up existing calendar event with David
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
                # Milestone 1 – Confirm the “Surfing Session with David” event (Dec 6 @ 6 pm) was actually returned
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
                                                "value": "Surfing Session with David",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-06T18:00:00-08:00",
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
                # Milestone 2 – New calendar event one week later at the same time has been created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Surfing Session with David",
                                    "start_datetime_iso": "2024-12-13T18:00:00-08:00",
                                    "attendees_names": [
                                        ["David Turner", "Lucas Garcia"]
                                    ],
                                    "creation_datetime_iso": "2024-12-06T21:00:00-08:00",
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
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # First look up → then confirm retrieved event
                (1, 2),  # After confirming event, new event should be created
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_81295fbe-d03d-4dbc-89ab-779cab47839c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_10",
                "whatsapp_messaging",
                "contact",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T17:05:00-08:00",
            is_read_time="2024-12-06T17:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to send another WhatsApp message to David Turner saying \"surf's up brah, let's curl the biggest wave and rip the fattest cloud and ride the last gnar. \" "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "WhatsApp David again and say 'surf's up brah, let's curl the biggest wave and rip the fattest cloud and ride the last gnar.'",
                },
            ],
            reasoning="The user wants to send a message via WhatsApp to David. Looking in WhatsApp, I can see that the user has been messaging David Turner so I'll send the message to him.",
            success_conditions=[
                {
                    "input_text": "1. A whatsapp message is sent to David Turner saying \"surf's up brah, let's curl the biggest wave and rip the fattest cloud and ride the last gnar.\"",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
            ],
            milestones=[
                # Milestone 0 – a new WhatsApp message was sent to David Turner with the requested text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Ensure David’s address is among the participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "david.turner@example.com",
                                                "+1 12345-6789-1000-9876",
                                            )
                                        ]
                                    ],
                                    # Check that the required phrase appears in the content
                                    "content": "surf's up brah",
                                    "creation_datetime_iso": "2024-12-06T17:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial state
                        )
                    ]
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_4d5e2cb3-3ff8-4251-a132-5f8d85f30423_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_10",
                "calendar",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T21:00:00-08:00",
            is_read_time="2024-12-06T21:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "The surf session was amazing today so you want to schedule another one "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Copy the thing with my surfing buddy to the same time next week",
                },
            ],
            reasoning="The user wants to copy the thing with their surfing buddy to the same time next week. I must determine what thing they are referring to and who their surf buddy is. In the user's contacts David Turner has an alias of 'Surfing Buddy' so he must be who the user was talking about. I'll try and find an event in the user's calendar including David.\n\nI found an event from earlier today titled \"Surfing Session with David\" including David Turner. This must be the thing the user wants to copy. I will schedule another \"Surfing Session with David\" for 6:00 pm on December 13th and inform the user.",
            success_conditions=[
                {
                    "input_text": '1. The calendar event "Surfing Session with David" is found',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": '2. The calendar event "Surfing Session with David" is copied to December 13th at 6:00 pm',
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
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 –  The agent looks up the existing surfing event in the calendar
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
                # Milestone 1 –  Verify that the event “Surfing Session with David” scheduled for
                # 2024-12-06 18:00 was returned from the calendar search in Milestone 0
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
                                                "value": "Surfing Session with David",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-06T18:00:00-08:00",
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
                            reference_milestone_node_index=0,  # depends on the search in Milestone 0
                        )
                    ]
                ),
                # Milestone 2 –  A new calendar event one week later at the same time is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Surfing Session with David",
                                    "start_datetime_iso": "2024-12-13T18:00:00-08:00",
                                    "attendees_names": [
                                        ["David Turner", "Lucas Garcia"]
                                    ],
                                    "creation_datetime_iso": "2024-12-06T21:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
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
                (0, 1),  # The search precedes confirming the correct event
                (1, 2),  # Confirmation precedes creating the new event
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_10_81295fbe-d03d-4dbc-89ab-779cab47839c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_10",
                "whatsapp_messaging",
                "contact",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T17:05:00-08:00",
            is_read_time="2024-12-06T17:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to send another WhatsApp message to David Turner saying \"surf's up brah, let's curl the biggest wave and rip the fattest cloud and ride the last gnar. \" "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Message my surfing buddy again saying 'surf's up brah, let's curl the biggest wave and rip the fattest cloud and ride the last gnar'",
                },
            ],
            reasoning="The user wants to send a message their surfing buddy in their usual way. Looking in the users contacts I see their name is David Turner. I can see they have been using WhatsApp to message. I'll send the message via whatsapp to him.",
            success_conditions=[
                {
                    "input_text": "1. A whatsapp message is sent to David Turner saying \"surf's up brah, let's curl the biggest wave and rip the fattest cloud and ride the last gnar.\"",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
                "send_message",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – the agent looks up either the contact or the existing WhatsApp thread
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
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require both Lucas and David to be in the WhatsApp thread
                                    "participants_addresses": [
                                        [
                                            (
                                                "+1 12345-6789-1000-9876",  # David Turner
                                                "david.turner@example.com",
                                            ),
                                            (
                                                "+1 12345-6789-1000-1234",  # Lucas (self)
                                                "lucas.garcia@example.com",
                                            ),
                                        ]
                                    ],
                                    # Key phrase from the requested message
                                    "content": "surf's up brah",
                                    "creation_datetime_iso": "2024-12-06T17:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Each tuple represents one required participant; no extras allowed
                                "participants_addresses": column_list_tuple_contains_similarity,
                                # Only need to confirm the distinctive phrase is present
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against pre-task snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=None,
        ),
    ]
