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
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_any_similarity,
    removal_similarity,
    snapshot_similarity,
    tool_trace_dependant_similarity,
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


def get_TAG_DAWEI_SHEN_pilot_plot_12(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="DAWEI_SHEN_12_9c3dc8ec-a404-4f63-aa16-f5316a962cbd_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T11:40:00-08:00",
            is_read_time="2024-12-09T11:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You are a bit tired from last night's late theatre rehearsals so you schedule a self reflection walk to decompress from work. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Add a self reflection walk for today at a quarter past 6.",
                },
            ],
            reasoning="The user has asked to add a new calendar event titled “Self Reflection Walk” for today (Monday, 9 Dec 2024) at a quarter past six in the evening (18:15). I already have the title, date, and time, so I can go ahead and create the event in their calendar. I might optionally ask if they want to specify a location or invitees, but the core information needed to add the event is complete.",
            success_conditions=[
                {
                    "input_text": "1. The event titled 'Self Reflection Walk' scheduled for 9th December at 18:15 is added to the calendar.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["create_calendar_event"],
            milestones=[
                # Milestone 0 – A new calendar event “Self Reflection Walk” on 9 Dec 2024 18:15 was created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Self Reflection Walk",
                                    "start_datetime_iso": "2024-12-09T18:15",
                                    "creation_datetime_iso": "2024-12-09T11:40:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_exact_match_similarity,
                                "start_datetime_iso": column_contains_similarity,  # allow any valid timezone suffix,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_8c94825f-765a-4866-b025-8f169af97404_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "whatsapp_messaging",
                "messaging",
                "contact",
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
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to ask Vickie and Charles if they want you to bring anything to the rehearsal. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you message Vickie and Charles separately, like we usually do, and ask if they need me to bring anything to the rehearsal?",
                },
            ],
            reasoning="The user wants to send two separate messages: one to Vickie and another to Charles. I'll first find out the exact contacts that user wants to send message to, then find their contact cards. OK, I see that there's an immediate event that matches with 'rehearsal' - \"Theater Rehearsal\" on December 08 at 19:00 with Vickie Lee and Charles Wilde as invitees. So user wants to message Vickie Lee and Charles Wilde. Now I shall locate Vickie and Charles' contact cards. I got them. Now I need to find out what messaging app they usually use. Ok, I see they messaged each other via whatsApp. I'll now send a whatsApp message to Vickie Lee and another to Charles Wilde saying \"Do you want me to bring anything to the rehearsal?\". Ok, I'll inform user that both messages are sent.",
            success_conditions=[
                {
                    "input_text": '1. A whatsApp message is sent to Vickie Lee that says "Do you need me to bring anything to the rehearsal?" ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. A WhatsApp message is sent to Charles Wilde that says something like "Do you need me to bring anything to the rehearsal?" ',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "send_message",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_messages",
                "get_all_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0: the agent should have tried to search whatsapp for past conversations
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
                # Milestone 1: Vickie Lee's conversation found
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
                        ),
                    ]
                ),
                # Milestone 2: the agent should have tried to search whatsapp for past conversations
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
                # Milestone 3: Charles's conversation found
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
                            reference_milestone_node_index=2,
                        ),
                    ]
                ),
                # Milestone 4 – new WhatsApp message to Vickie Lee and Charles Wilde
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": [
                                        "Vickie Lee",
                                        "Charles Wilde",
                                    ],
                                    "content": [
                                        "rehearsal",
                                        "rehearsal",
                                    ],
                                    "creation_datetime_iso": "2024-12-08T18:00:00-08:00",
                                }
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
            milestone_edge_list=[
                (0, 1),  # found Vickie' past messages
                (2, 3),  # found Charles messages
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_38db6d63-46da-49c4-8b5b-dbf77dfb157e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:25:00-08:00",
            is_read_time="2024-12-08T18:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You can't remember when Theater Rehearsal starts. You need to ask your assistant when is it scheduled for  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time does my rehearsal start tonight again?",
                },
            ],
            reasoning='The user wants to know when his Theater Rehearsal event is. I need to look at the calendar and find this event. I find an event titled "Theater Rehearsal" at 19:00 on 08/Dec/2024. I present this information to the user ',
            success_conditions=[
                {
                    "input_text": '1. The start time of the "Theater Rehearsal" event is presented to the user',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent uses calendar tools to look up rehearsal time
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
                # Milestone 1 – Confirms the "Theater Rehearsal" event with correct start time was retrieved
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
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
                # Milestone 2 – The assistant tells the user the correct start time for tonight's rehearsal
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We accept multiple phrasings but must mention 7:00 pm / 7 pm / 19:00
                                    "content": [
                                        ("7pm", "7 pm", "7 p.m.", "19:00", "7:00")
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
                (0, 1),  # calendar lookup → confirm correct event and time
                (1, 2),  # having correct time → respond to user with that time
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_75ee90c1-5a08-4b93-bc73-03aee990825d_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "calendar",
                "whatsapp_messaging",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T17:52:00-08:00",
            is_read_time="2024-12-08T17:52:00-08:00",
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
                    "content": "What time does the event Charles needed to reschedule start at?",
                },
            ],
            reasoning="The user wants to know information about an event they were discussing with Charles. They only have one contact named Charles: Charles Wilde. I don't see any normal texts with Charles Wilde, but I see a whatsapp thread with him, so I'll look there to see what event the user could be asking about. Charles most recently mentioned that the rehearsal schedule needed to be adjusted to 19:00. I'll look for something in the user's calendar with the word 'event' in the title to double-check the start time. The event Theater Rehearsal does indeed start at 19:00, so I'll inform the user.",
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
                # Milestone 0 – Agent uses calendar tools to look up the rehearsal event
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
                # Milestone 1 – Confirms that Charles was found in messages history
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
                    ],
                ),
                # Milestone 2 – User-facing answer mentions the correct start time and date
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
                                            "7 pm",
                                            "7 p.m.",
                                            "7pm",
                                            "19:00",
                                            "7:00",
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
                (0, 1),  # information lookup → confirm correct event details
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_bdb92f49-c2cd-4b9d-ab4c-83ade9fd8809_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:30:00-08:00",
            is_read_time="2024-12-08T18:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "As you were informed on late notice you want to double check the new times for theatre rehearsals this evening. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is the Theatre Rehearsal again?",
                },
            ],
            reasoning="The user wants to know when the Theater rehearsal is. The calendar event 'Theater Rehearsal' is today from 19:00 to 22:00. I will inform the user that 'Theater Rehearsal' is today from 19:00 to 22:00.",
            success_conditions=[
                {
                    "input_text": "1. the user is informed the event 'Theater Rehearsal' runs from 19:00-22:00 on 8th of December. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
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
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1: rehearsal event found
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
                            reference_milestone_node_index=0,
                        ),
                    ]
                ),
                # Milestone 2 – The user is informed the rehearsal is 7-10 PM (19:00-22:00) tonight
                Milestone(
                    snapshot_constraints=[
                        # Mentions start time (7 PM / 19:00)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "7 pm",
                                            "7 p.m.",
                                            "7pm",
                                            "19:00",
                                            "7:00",
                                        )
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
                (0, 1),  # Calendar lookup
                (1, 2),  # inform user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_216bfcfd-ea39-4794-a281-bccf8d45deb4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
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
                        "Before you start your journey you want to ask the assistant the location to the Theater Rehearsal event in you calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'What is the location of the "Theater Rehearsal" event at 19:00 in my calendar',
                },
            ],
            reasoning='So the user wants me to tell them the location of the Theater Rehearsal event at 19:00. First I will look at the user\'s calendar and find an event by that description. I have found an event titled "Theater Rehearsal" at 19:00 today, so that must be what the user is referring to. I will present the user with the address attached to this event, which is "Orchard Theater, 789 Culture St."',
            success_conditions=[
                {
                    "input_text": '1. The location of the "Theater Rehearsal" event, "Orchard Theater, 789 Culture St.", is presented to the user',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent queries the calendar for the event
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
                # Milestone 1: rehearsal event found
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
                            reference_milestone_node_index=0,
                        ),
                    ]
                ),
                # Milestone 2 – The user is told the correct location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("Orchard Theater", "789 Culture St")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_3f439e66-782f-42fd-b33d-e38da723b6e8_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T22:05:00-08:00",
            is_read_time="2024-12-08T22:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "Your practice group has decided to meet at the same time next week and you want your assistant to create this event in your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Practice is going to be at the same time next week, can you pop it in my calendar",
                },
            ],
            reasoning="The user wants to add 'practice' in their calendar for next week at the same.\n\nI'll first find out what user refers to by 'practice'. I see user has just finished their theatre rehearsal, I understand that's what they refer to by 'practice'. By checking the existing event “Theater Rehearsal” which was 19:00–22:00 on Sunday, 8 Dec 2024. I'll create a new event with the same title “Theater Rehearsal” for next week which will be Sunday, 15 Dec 2024, and at the same time 19:00–22:00. Ok, I'll copy the exact details as current theatre rehearsal event's, I'll add Charles Wilde and Vickie Lee as invitees. I'll inform user that new event is scheduled.",
            success_conditions=[
                {
                    "input_text": "A new event titled Theater Rehearsal is created from 19:00 to 22:00 on 15 December 2024 with Charles Wilde and Vickie Lee.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "create_calendar_event",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – The agent queries the calendar for the event
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
                # Milestone 1: rehearsal event found
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
                            reference_milestone_node_index=0,
                        ),
                    ]
                ),
                # Milestone 2 – A new rehearsal event for next Sunday was added to the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Theater Rehearsal",
                                    "start_datetime_iso": "2024-12-15T19:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "Charles Wilde",
                                            "Vickie Lee",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-08T22:05:00-08:00",
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
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_72ab6a56-9006-4f5e-b148-c0d2bb0fd751_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "phone_call",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T19:00:00-08:00",
            is_read_time="2024-12-08T19:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You don't see Vickie at the Orchard theater.  You want to give Vickie a call and make sure that she is definitely on her way to your new rehearsal schedule. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you please give Vickie a call for me",
                },
            ],
            reasoning="The user asked me to call Vickie. I found two people in Dawei's contacts, one is Vickie Lee and the other is Vick Li. These sound pretty similar, so I need to figure out which one the user actually wants to contact. I can check what's in user's calendar- it is currently 19:00 on December 8th 2024 and they have a calendar event called \"Theater Rehearsal\" that is on-going right now. Checking the attendees, it is Charles Wilde and Vickie Lee. This must be the Vickie he wants to contact, because maybe this person is not here yet for the rehearsal. I will find Vickie Lee's contact card. Ok, I located her contact and I'm calling her. I'll let user know, calling Vickie Lee.",
            success_conditions=[
                {
                    "input_text": "1. An outgoing call to Vickie Lee is made.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "create_outgoing_call",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent search for contacts
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
                # Milestone 1 – correct number returned
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
                                            "phone_number": {
                                                "value": "+1 555-345-6789-0123",
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
                            reference_milestone_node_index=0,  # based on the function results in milestone 0
                        ),
                    ],
                ),
                # Milestone 2 – A new outgoing phone-call record to Vickie Lee exists
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.PHONE,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "receiver_address": [
                                        (
                                            "+1 555-345-6789-0123",
                                            "vickie.lee@orchardtheater.com",
                                        )
                                    ],
                                    "call_type": "outgoing",
                                    "creation_datetime_iso": "2024-12-08T19:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "receiver_address": column_str_contains_any_similarity,
                                "call_type": column_exact_match_similarity,
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
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_c727a5d9-b482-4b30-9ba9-38641659af4a_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "whatsapp_messaging",
                "contact",
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
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to send a message to Charles asking how he thought last night's rehearsals went "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a WhatsApp text to Charles asking what he thought of last night's rehearsal",
                },
            ],
            reasoning="The user wants me to send a WhatsApp text to Charles asking what they thought of last night's rehearsal.\n\nI'll find out which contact user wants to message with. Ok, I see there's only one Charles Wilde in user's contacts. I located his contact card. User wants to send him a whatsApp message. Ok, I'll send Charles a whatsApp message saying \"How do you think last night's rehearsal went?\" and I'll inform the user that the message is sent.",
            success_conditions=[
                {
                    "input_text": 'A WhatsApp message is sent to Charles Wilde asking "How do you think last night\'s rehearsal went?"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0: agent search contacts
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
                                        "get_all_contacts",
                                        "search_contacts",
                                    ],
                                ),
                            },
                        )
                    ]
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
                                            "email": {
                                                "value": "charles.wilde@orchardtheater.com",
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
                # Milestone 2 – a new WhatsApp message to Charles containing the rehearsal question was created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Charles Wilde",
                                    # agent-composed message (query only says "ask what he thought
                                    # of last night's rehearsal") — grade the topic, not exact wording
                                    "content": "rehearsal",
                                    "creation_datetime_iso": "2024-12-09T10:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
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
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_e48966ce-7f9a-4ea2-bef8-a8a9199eabdb_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:40:00-08:00",
            is_read_time="2024-12-08T18:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to message your friend about grabbing a celebratory dinner the evening of the upcoming tech panel you're both attending. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text my friend saying 'Hey there, looking forward to the tech panel! Are you free for dinner on Tuesday at 18:30?'.",
                },
            ],
            reasoning="The user wants to send the message: 'Hey there, looking forward to the tech panel! Are you free for dinner on Tuesday at 18:30?' to their friend. From the message content I understand the user wants to message someone and it's related to 'tech panel'. I see there's an upcoming event \"Tech Panel Hosted by Jeff Bing\" scheduled on December 10 at 09:00. I understand the contact user refers to is Jeff Bing. I’ll locate Jeff Bing's contact card. Ok, I found his contact. I'll sent him a message saying \"Hey Jeff, looking forward to the tech panel! Are you free for dinner on Tuesday at 18:30?\" Now I'll inform user that the message is sent.",
            success_conditions=[
                {
                    "input_text": "1. A message is composed and sent to Jeff Bing saying 'Hey Jeff, looking forward to the tech panel! Are you free for dinner on Tuesday at 18:30?'.",
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
                "send_message",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – The agent queries calendars to locate tech panel
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
                # Milestone 1 – Tech Panel returned from the contact lookup
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
                # Milestone 2 – The agent queries contacts to locate Jeff Bing
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
                # Milestone 3 – Jeff Bing is returned from the contact lookup
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
                                                "value": "Jeff Bing",
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
                # Milestone 4 – Message is sent to Jeff and recorded in the messaging log
                Milestone(
                    snapshot_constraints=[
                        # A new outbound message appears with the correct content
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Jeff Bing",
                                    "content": "Are you free for dinner",
                                    "creation_datetime_iso": "2024-12-08T18:40:00-08:00",
                                }
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
            milestone_edge_list=[
                (0, 1),  # Tech Panel Found
                (2, 3),  # Contact search → confirmation Jeff found
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_794925b3-4bdd-4f79-bbca-cf2340692843_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:25:00-08:00",
            is_read_time="2024-12-08T18:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to see the location of the theatre rehearsal for tonight. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where is the rehearsal on later? ",
                },
            ],
            reasoning='The user wants to know the location of the rehearsal later, so I must search tonight\'s calendar for the keyword "rehearsal".\n\nI have found the event titled "Theater Rehearsal" that\'s tonight at 19:00, so now I\'ll check the event\'s location. I found out the location is "Orchard Theater, 789 Culture St, Orchard County". I\'ll inform user of it.',
            success_conditions=[
                {
                    "input_text": 'The assistant tells the user the rehearsal location is "Orchard Theater".',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent looks up tonight's rehearsal in the calendar
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
                # Milestone 1: rehearsal event found
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
                            reference_milestone_node_index=0,
                        ),
                    ]
                ),
                # Milestone 2 – The user is told the rehearsal location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Orchard Theater",
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
            name="DAWEI_SHEN_12_2b0f714a-059e-4439-b7dc-a1cb880686b8_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
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
                    "content": "Tell me what time the discussion on trends in consumer electronics is starting",
                },
            ],
            reasoning='The user wants to know what time the "discussion on trends in consumer electronics" is starting. \n\nOkay, firstly I need to go to the user\'s Calendar to see if they have any upcoming events that correspond to this description.\n\nOkay, so the description matches with an event on Tuesday, December 10th at 09:00 named "Tech Panel Hosted by Jeff Bing". I surmise that this is the event that the user is referring to.\n\nI\'ll now inform the user that the event "Tech Panel Hosted by Jeff Bing" on December 10th starts at 09:00.',
            success_conditions=[
                {
                    "input_text": '1. The user is presented with the event "Tech Panel Hosted by Jeff Bing", starting at 09:00 on Tuesday, December 10th 2024.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent searches calendar to locate the event that matches "trends in consumer electronics" and find that the event is 'tech panel'
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
                # Milestone 1: tech panel event found
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
                            reference_milestone_node_index=0,
                        ),
                    ]
                ),
                # Milestone 2 – Agent tells the user the tech-panel start time
                Milestone(
                    snapshot_constraints=[
                        # Ensure the 9 AM start time (various formats) is mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "9:00",
                                            "09:00",
                                            "9 am",
                                            "9am",
                                            "9 AM",
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
                (1, 2),  # After searching the calendar, the agent informs the user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_e48966ce-7f9a-4ea2-bef8-a8a9199eabdb_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:40:00-08:00",
            is_read_time="2024-12-08T18:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You're looking forward to Jeff's tech panel during the week but want to ask him to see if he's free to get a celebratory dinner that evening in the thread. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send the following to Jeff back 'Hey Jeff, looking forward to the tech panel! Are you free for dinner on Tuesday at 18:30?'.",
                },
            ],
            reasoning="First, I look up \"Jeff\" in the user's contacts and find only one matching entry, \"Jeff Bing\". I don't see any text message or whatsApp message threads between the user and Jeff Bing. I see they talked via email. So I'll send this message back to Jeff Bing via email. I'll go ahead and compose the exact content the user dictated: “Hey Jeff, looking forward to the tech panel! Are you free for dinner on Tuesday at 18:30?”  I'll inform user that email has been successfully sent to Jeff.",
            success_conditions=[
                {
                    "input_text": "An email is composed and sent to Jeff Bing saying 'Hey Jeff, looking forward to the tech panel! Are you free for dinner on Tuesday at 18:30?'.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "send_email",
                "send_message",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – the agent looks up Jeff in the email thread
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
                # Milestone 1 – Jeff Bing’s  prior email was actually returned
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
                # Milestone 2 – the new email actually exists in the datastore
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
                                    "body": "are you free for dinner",
                                    "creation_datetime_iso": "2024-12-08T18:40:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "body": column_contains_similarity,
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
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_c727a5d9-b482-4b30-9ba9-38641659af4a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "whatsapp_messaging",
                "messaging",
                "contact",
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
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to send a message to Charles asking how he thought last night's rehearsals went with WhatsApp "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a follow up message to my theatre friend asking what he thought of last night’s rehearsal",
                },
            ],
            reasoning="The user wants me to send a message to their theatre friend asking what they thought of last night's rehearsal so first I must determine who is meant by theatre friend. Looking through the user's contacts there are two people listed as theatre friends, Vickie Lee and Charles Wilde. And as user says they want to \"ask what he thought of last night’s rehearsal\", I understand by 'he' they refer to Charles. So I will locate Charles contact card. I see that the user and Charles only communicated via WhatsApp. I assume the user will prefer to use WhatsApp. I will send a whatsApp message to Charles Wilde saying \"what do you think of last night’s rehearsal\". \n\nOk I'll inform user that the message was sent.",
            success_conditions=[
                {
                    "input_text": 'A WhatsApp message is sent to Charles Wilde asking "What do you think of last night\'s rehearsal?"',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The message is not sent with the text-message tool; WhatsApp is the usual channel with Charles Wilde.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "send_message",
                "search_contacts",
                "get_all_contacts",
                "search_whatsapp_messages",
                "search_messages",
                "get_all_whatsapp_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – the agent looks up Jeff in the contacts list
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
                # Milestone 1 – Charles Wilde’s contact information was actually returned
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
                        )
                    ]
                ),
                # Milestone 2: the agent should have tried to search messages or whatsapp for past conversations
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
                # Milestone 3: conversation with Charles found
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
                            reference_milestone_node_index=2,
                        ),
                    ]
                ),
                # Milestone 4 – A new outgoing WhatsApp message to Charles is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Charles Wilde",
                                    # Make sure the text references last night’s rehearsal
                                    "content": "rehearsal",
                                    "creation_datetime_iso": "2024-12-09T10:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
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
            milestone_edge_list=[
                (0, 1),
                (2, 3),
            ],
            minefields=[
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
                                        "send_message",
                                    ],
                                )
                            },
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_32411cc5-429a-4f0c-83ce-e66c3a934553_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "whatsapp_messaging",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T01:00:00-08:00",
            is_read_time="2024-12-09T01:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You wake up and want to send Charles a text to thank him for updating you on the rehearsal time earlier.  This is in addition to the earlier text you sent him.  This one is to say Thanks for letting me know about the updated rehearsal time earlier -- what a great night. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a follow up message to my theatre friend saying Thanks for letting me know about the updated rehearsal time earlier -- what a great night. ",
                },
            ],
            reasoning="Looks like the user is trying to reply to a previous message from a theatre friend. I will bring up messages and whatsapp messages earlier, and found Charles Wilde message mentioned about updated rehearsal. Then I will gin up the text with the desired message and show it to user for approval. ",
            success_conditions=[
                {
                    "input_text": "Charles Wilde’s 2024-12-08T17:50:00-08:00 whatsapp message is surfaced.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": 'A WhatsApp text is sent to Charles Wilde saying "Thanks for letting me know about the updated rehearsal time earlier -- what a great night."',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "send_whatsapp_message",
                "send_message",
                "search_contacts",
                "get_all_contacts",
                "search_whatsapp_messages",
                "search_messages",
                "get_all_whatsapp_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – the agent looks up Jeff in the contacts list
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
                # Milestone 1 – Charles's previous message brought up
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
                                                "value": "Charles Wilde",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-08T17:50:00-08:00",
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
                # Milestone 2 – a new outgoing message to Charles is recorded
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Charles Wilde",
                                    "content": "the updated rehearsal time",
                                    "creation_datetime_iso": "2024-12-09T01:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # ensure the gist of the thank-you text is there
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
            name="DAWEI_SHEN_12_dd0abaf8-0405-40e9-b30b-a5ea80641319_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_low",
                "informational_complexity_high",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T22:35:00-08:00",
            is_read_time="2024-12-08T22:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know how many not work related events you have this week that are 2 hours long "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How many events do I have this week that are 2 hours long? not work related",
                },
            ],
            reasoning='The user wants to know how many events they have this week that are "2 hours long". I\'ll check their Calendar to see which events correspond to this stated duration.\n\nI\'ve found two events, one named "Tech Panel Hosted by Jeff Bing", taking place from 09:00 - 11:00 on December 10th 2024, and the other named "Dinner with Lukas and Vick", taking place from 19:00 - 21:00 on December 14th 2024, but there is a duplication. I\'ll inform the user the number of non-work events are one which is the dinner with Lucas and Vick.',
            success_conditions=[
                {
                    "input_text": "1. The number of non-work related events in the user's calendar with a duration of two hours taking place over the next seven days is presented to the user: one.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent looks at the calendar
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
                # Milestone 1 – Tech Panel found
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
                        ),
                    ]
                ),
                # Milestone 2 – User is informed about the number (2) of 2-hour events
                Milestone(
                    snapshot_constraints=[
                        # Must mention the number 2 (either numeral or word)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("1", "one")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_2a340b6a-f93a-42c5-9673-7908f6c68340_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
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
                        "You want to know the location of your Theater Rehearsal. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where is my event later today?",
                },
            ],
            reasoning="The user wants to know where there event is on later today. I do not know what event they are referring to. Let me check what events are on today in their calendar. They must be referring to 'Theater Rehearsal'.The location for the event 'Theater Rehearsal' on December 8th from 19:00 until 22:00 is Orchard Theater, 789 Culture St, Orchard County, CA 94022, USA. I will inform them of this.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their event 'Theater Rehearsal' is located at Orchard Theater, 789 Culture St, Orchard County, CA 94022, USA.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent consults the calendar to find the rehearsal event
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
                # Milestone 1: rehearsal event found
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
                            reference_milestone_node_index=0,
                        ),
                    ]
                ),
                # Milestone 2 – The user is told where the rehearsal is
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Orchard Theater",  # key phrase to confirm
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_a634ebea-6e98-4a75-85ba-be6fec5047c8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T17:51:00-08:00",
            is_read_time="2024-12-08T17:51:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to read the message sent by Charles and respond to it saying Got it.  Updating our calendar now.      . "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Display the new message on WhatsApp to me and reply to it saying Got it. Updating our calendar now.",
                },
            ],
            reasoning="User wants to see the new message on WhatsApp and send back a reply. Ok, firstly I need to check their WhatsApp messages and find the most recent one. The message is from Charles Wilde, received at 17:50 on December 8, 2024. I present that message to the user.\nThe user wants me to send a response to that message saying \"Got it. Updating our calendar now.\". I'll send the whatsApp message to Charles Wilde on WhatsApp. I'll inform user that the message has been sent.",
            success_conditions=[
                {
                    "input_text": "The message from Charles Wilde received on WhatsApp at 17:50 on December 8 2024 is presented to the user.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": 'A message is sent to Charles Wilde on WhatsApp saying "Got it. Updating our calendar now."',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
            ],
            milestones=[
                # Milestone 0 – the agent looks up WhatsApp messages (either by searching or listing all)
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
                # Milestone 1: Latest whatsapp message from Charles found
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
                                                "value": "Charles Wilde",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-08T17:50:00-08:00",
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
                # Milestone 2 – the agent surfaces Charles’s rehearsal-change message to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Charles Wilde",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.WHATSAPP
                    ],  # exclude WHATSAPP additions
                ),
                # Milestone 3 – a new outgoing WhatsApp message is recorded in the WHATSAPP DB
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_names": [
                                        ["Charles Wilde", "Dawei Shen"]
                                    ],
                                    "content": "Got it. Updating our calendar now.",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-08T17:51:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with original DB state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # after fetching messages, the agent shows it to the user
                (0, 2),  # after fetching messages, the agent can compose the reply
                (1, 3),  # sending tool call should result in DB addition
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_0dc7d9b2-8ca5-4b1c-b980-b137331c0ac3_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T18:20:00-08:00",
            is_read_time="2024-12-13T18:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You were looking at your Calendar to see what events you have coming up this week when you noticed that you have a duplicate event.  You want to delete one. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete one of the events with Vick and Lukas.",
                },
            ],
            reasoning="Ok, the user wants to delete one of the events with Vick and Lukas. I'll check up the calendar and find out which event with Vick and Lukas they want to delete. I see in the calendar there are two identical events titled “Dinner with Lukas and Vick” scheduled for 14 Dec 2024 from 19:00–21:00. I will remove one of them and then notify the user that the duplicated event has been deleted.",
            success_conditions=[
                {
                    "input_text": "One instance of the event 'Dinner with Lukas and Vick' on 14 December 2024 from 19:00 to 21:00 is deleted.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "remove_calendar_event",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Fix - milestone 0 should be search the calendar event.
                # Milestone 0 – The agent looks up tonight's rehearsal in the calendar
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
                # Milestone 1: Dinner with Lukas and Vick event found
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
                        ),
                    ]
                ),
                # Milestone 2 – One duplicate “Dinner with Lukas and Vick” event is removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dinner with Lukas and Vick",
                                    "start_datetime_iso": "2024-12-14T19:00:00-08:00",
                                    "end_datetime_iso": "2024-12-14T21:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_0dc7d9b2-8ca5-4b1c-b980-b137331c0ac3_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T18:20:00-08:00",
            is_read_time="2024-12-13T18:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You were looking at your Calendar to see what events you have coming up this week when you noticed that you have a duplicate event.  You want to delete one. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the duplicate event.",
                },
            ],
            reasoning="Looks like there is a duplicate event the user wants me to delete.\n\nFirst, I will search the user’s calendar and see that events they refer to. I found two identical “Dinner with Lukas and Vick” entries scheduled for 14 December 2024 from 19:00–21:00. Since they are duplicates, I will delete one of them.\n\nAfter removing one copy of the event, I will inform the user that the duplicate “Dinner with Lukas and Vick” event on 14 December 2024 at 19:00 has been deleted.",
            success_conditions=[
                {
                    "input_text": 'One instance of "Dinner with Lukas and Vick" on 14 December 2024 from 19:00 to 21:00 is deleted.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": 'The assistant tells the user that the duplicate "Dinner with Lukas and Vick" event has been deleted.',
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the calendar to identify the duplicate
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
                # Milestone 1: Dinner with Lukas and Vick event found
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
                        ),
                    ]
                ),
                # Milestone 2 – One of the duplicate dinner events is removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dinner with Lukas and Vick",
                                    "start_datetime_iso": "2024-12-14T19:00:00-08:00",
                                    "end_datetime_iso": "2024-12-14T21:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                ),
                # Milestone 3 – The user is informed that the duplicate was deleted
                Milestone(
                    snapshot_constraints=[
                        # Event name mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Dinner with Lukas and Vick",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_a634ebea-6e98-4a75-85ba-be6fec5047c8_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T17:50:00-08:00",
            is_read_time="2024-12-08T17:50:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to read the message sent by Charles and respond to it saying Got it, Charles.  Updating our calendar now. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Open Charles Wilde's conversation on WhatsApp and reply to it saying Got it, Charles. Updating our calendar now.",
                },
            ],
            reasoning="The user wants me to open the conversation with Charles Wilde on WhatsApp. I will search WhatsApp for the contact Charles Wilde. I found it. I'll open the chat with Charles Wilde and present it to the user. The user wants me to also send a response to that message. The user wants the message to say Got it, Charles. Updating our calendar now. I draft up the message and ask the user for confirmation that the message is correct. I receive the confirmation and send the message to Charles Wilde on WhatsApp.",
            success_conditions=[
                {
                    "input_text": "Charles Wilde’s most recent WhatsApp message is displayed to the user.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": 'A WhatsApp message saying "Got it, Charles. Updating our calendar now." is sent to Charles Wilde.',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
            ],
            milestones=[
                # Milestone 0 – Agent queries WhatsApp messages (so it can surface Charles’s note)
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
                # Milestone 1: conversation with Charles found
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
                # Milestone 2 – A new outgoing WhatsApp message exists in the DB
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Charles Wilde",
                                    "content": "Got it, Charles. Updating our calendar now.",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-08T17:50:00-08:00",
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
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Fetched messages
                (1, 2),  # send the message
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_2a340b6a-f93a-42c5-9673-7908f6c68340_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
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
                        "You want to know the location of your Theater Rehearsal. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where is my event 'Theater Rehearsal' on?",
                },
            ],
            reasoning="The user wants to know where their event 'Theater Rehearsal' is on. Let me look for this event in their calendar. Ok, I found the event 'Theatre Rehearsal' user looks for. The location for the event 'Theater Rehearsal' on December 8th from 19:00 until 22:00 is Orchard Theater, 789 Culture St, Orchard County, CA 94022, USA. I will inform them of this.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their event 'Theater Rehearsal' is located at Orchard Theater, 789 Culture St, Orchard County, CA 94022, USA.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent looks up the calendar to find the rehearsal details
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
                # Milestone 1: rehearsal event found
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
                            reference_milestone_node_index=0,
                        ),
                    ]
                ),
                # Milestone 2 – The user is told where the rehearsal is taking place
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Orchard Theater",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_dd0abaf8-0405-40e9-b30b-a5ea80641319_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_low",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T22:35:00-08:00",
            is_read_time="2024-12-08T22:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know how many events you have in the coming week that are more than 1 hour long for work "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Do I have any work related events in the coming week that will last longer at least an hour? How many in total?",
                },
            ],
            reasoning='The user wants to know how many calendar events they have in the coming week (the next seven days) that are longer or equal than one hour. I will look at the events that fall between 2024-12-09 and 2024-12-15 (inclusive) and have a duration at least 60 minutes.\n\nFrom the calendar I find two such work-related events:\n1. "Tech Panel Hosted by Jeff Bing" on 2024-12-10 from 09:00–11:00 (2 h)\n2. "Team Review Meeting" on 2024-12-13 from 10:00–11:00 (1 h)\n\nThere are no other work events within that window that equal or exceed one hour. I will tell the user that they have 2 events in total.',
            success_conditions=[
                {
                    "input_text": "1. The number of work-related events in the user's calendar with a duration of at least an hour taking place over the next seven days is presented to the user: two.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 — The agent queries the calendar to figure out the answer
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
                # Milestone 1: events with longer than one hour retrieved
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
                                                "value": "2024-12-13T10:00:00",
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
                # Milestone 2 — The agent queries the calendar to figure out the answer
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
                # Milestone 3: events with longer than one hour retrieved
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
                                                "value": "2024-12-10T09:00:00",
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
                    ]
                ),
                # Milestone 4 — The agent tells the user there are two events this week that are equal or longer than an hour
                Milestone(
                    snapshot_constraints=[
                        # Must mention the count
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("two", "2")],  # either wording is fine
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity,
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (2, 3), (1, 4), (3, 4)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_32411cc5-429a-4f0c-83ce-e66c3a934553_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "whatsapp_messaging",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T01:00:00-08:00",
            is_read_time="2024-12-09T01:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You wake up and want to send Charles a text to thank him for updating you on the rehearsal time earlier.  This is in addition to the earlier text you sent him.  This one is to say Thanks for letting me know about the updated rehearsal time earlier -- what a great night. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to Charles in our conversation saying Thanks for letting me know about the updated rehearsal time earlier -- what a great night. ",
                },
            ],
            reasoning="I will first look up Charles Wilde in the contacts list to confirm his details, then search our WhatsApp threads to bring up the prior conversation about the rehearsal time. Once I have that chat open, I will draft a WhatsApp message that says, “Thanks for letting me know about the updated rehearsal time earlier -- what a great night,” and show it to the user for approval before sending.",
            success_conditions=[
                {
                    "input_text": "1. A WhatsApp message is sent to Charles Wilde saying Thanks for letting me know about the updated rehearsal time earlier -- what a great night. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The reply is sent on WhatsApp only; the text-message tool is not used, since the conversation with Charles Wilde is on WhatsApp.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_messages",
                "get_all_messages",
                "send_whatsapp_message",
                "send_message",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0: the agent should have tried to search messages or whatsapp for past conversations
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
                # M1: Charles conversation Found
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
                # Milestone 2 – A new WhatsApp message to Charles Wilde was actually created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Only need to make sure Charles is included among the participants
                                    "conversation_name": "Charles Wilde",
                                    "content": "Thanks for letting me know about the updated rehearsal time earlier",
                                    "creation_datetime_iso": "2024-12-09T01:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
            minefields=[
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
                                        "send_message",
                                    ],
                                )
                            },
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_3f439e66-782f-42fd-b33d-e38da723b6e8_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T22:05:00-08:00",
            is_read_time="2024-12-08T22:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "Your theater rehearsal group has decided to meet at the same time next week and you want your assistant to create this event in your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Our play practice is going to be at the same time next week, can you pop it in my calendar.",
                },
            ],
            reasoning="The user wants to create a calendar event for their practise next week, at the same time. \n\nFirst I will need to figure out which event the user is referring to as “practise”, I can’t find an exact match for the user’s query but they did have a recent event titled Theater Rehearsal. As practise and rehearsal are synonyms, I will assume that this is what the user is talking about.\n\nNow I will need to find out with time the theater rehearsal was at this week, looking through the user's calendar events, I can see Theater Rehearsal was from 19:00 to 22:00 on Sunday. With this information I can create an event for next Sunday, December 15 from 19:00 to 22:00 again. \n\nI can also see that Charles Wilde and Vickie Lee were attendees of this event and will add them to next weeks version.\n\nSo finally, a new event titled Theater Rehearsal is created from 19:00 to 22:00 on 15 December 2024, with Charles Wilde and Vickie Lee.",
            success_conditions=[
                {
                    "input_text": "1. New event titled Theater Rehearsal is created from 19:00 to 22:00 on 15 December 2024, with  Charles Wilde and Vickie Lee.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "create_calendar_event",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – The agent looks up existing calendar information and finds out that by "practice" user refers to "rehearsal".
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
                        ),
                    ],
                ),
                # Milestone 1: rehearsal event found
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
                            reference_milestone_node_index=0,
                        ),
                    ]
                ),
                # Milestone 2 – A new calendar event for next week’s rehearsal has been created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Theater Rehearsal",
                                    "start_datetime_iso": "2024-12-15T19:00:00-08:00",
                                    "end_datetime_iso": "2024-12-15T22:00:00-08:00",
                                    "attendees_names": [
                                        ["Charles Wilde", "Vickie Lee"]
                                    ],
                                    "creation_datetime_iso": "2024-12-08T22:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "attendees_names": column_list_subset_match_similarity,
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
                (0, 1),  # looked up calendar → created new event
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_182de13e-854e-4796-b8eb-5700c91d4d39_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:25:00-08:00",
            is_read_time="2024-12-08T18:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to see the location of the theatre rehearsal for tonight.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where is the rehearsal on later? ",
                },
            ],
            reasoning='The user wants to know the location of tonight\'s rehearsal, so I must search tonight\'s calendar for the keyword "rehearsal". \n\nI have found the event titled "Theatre Rehearsal", so now I must search the event for a location and read it out to the user. \n\nI will inform user that the location of the rehearsal is "Orchard Theater, 789 Culture St, Orchard County". ',
            success_conditions=[
                {
                    "input_text": 'Calendar is checked for the location of "Theatre Rehearsal". ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent uses calendar tools to look up rehearsal information
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
                # Milestone 1 – Confirms the "Theater Rehearsal" event with correct location was retrieved
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
                                            "location": {
                                                "value": "Orchard Theater, 789 Culture St, Orchard County, CA 94022, USA",
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
                            reference_milestone_node_index=0,
                        ),
                    ],
                ),
                # Milestone 2 – User is informed of the rehearsal location in the assistant's reply
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Orchard Theater",
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
                ),  # Calendar lookup → confirm correct rehearsal event and location
                (1, 2),  # Retrieved location → communicated to user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_e0e7def9-ff00-407b-9f6c-b8399b959bc0_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:25:00-08:00",
            is_read_time="2024-12-08T18:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You can't remember when Theater Rehearsal starts.  You need to ask your assistant when is it scheduled for "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time does my rehearsal start tonight again?",
                },
            ],
            reasoning='The user wants to know when his Theater Rehearsal event is. I need to look at the calendar and find this event. I find an event titled "Theater Rehearsal" at 19:00 (7 pm) on 08/Dec/2024. I present this information to the user.',
            success_conditions=[
                {
                    "input_text": '1. The start time of the "Theater Rehearsal" event is presented to the user',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The assistant looks up calendar information
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
                # Milestone 1 – The "Theater Rehearsal" event is found
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
                            reference_milestone_node_index=0,
                        ),
                    ],
                ),
                # Milestone 2 – The assistant informs the user of the rehearsal start time
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
                                            "7 pm",
                                            "7 p.m.",
                                            "7pm",
                                            "19:00",
                                            "7:00",
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
                (0, 1),  # Calendar lookup → event found
                (1, 2),  # Event found → user informed
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_f0b73bd3-732d-4a5a-97ef-9c143e4e4a1f_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T17:54:00-08:00",
            is_read_time="2024-12-08T17:51:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You have responded to Charles message about the new time, but you'd like to know how others respond to it, since you are driving you cannot check your phone. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has anyone else agreed on the proposed new time tonight? Only give me the names.",
                },
            ],
            reasoning="The user wants to know who ELSE has agreed to the new rehearsal time proposed in the group chat tonight. This is about the messages, not the calendar, so I check the WhatsApp 'Theater Group' conversation. Charles proposed moving tonight's rehearsal to 7 PM. Scanning the replies, Vickie Lee responded 'I'm in for 7 PM', so she has agreed. Charles is the proposer and Dawei is the user, so neither counts as 'anyone else'. I will tell the user that Vickie is the only other person who has agreed so far.",
            success_conditions=[
                {
                    "input_text": "The user is told that Vickie Lee is the only other person (besides the proposer, Charles) who has agreed to the proposed new 7 PM rehearsal time.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – The agent searches WhatsApp for the group conversation
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
                # Milestone 1 – Vickie Lee's agreement to the 7 PM time is found in the thread
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
                                                "value": "Vickie Lee",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "7 PM",
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
                # Milestone 2 – The user is told Vickie is the one who agreed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("Vickie", "Vickie Lee")],
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
            minefields=[
                # The response must not present Charles (the proposer) or Dawei (the
                # user) as "someone else who agreed" — only Vickie qualifies.
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("Charles", "Dawei")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_75ee90c1-5a08-4b93-bc73-03aee990825d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "calendar",
                "whatsapp_messaging",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T17:54:00-08:00",
            is_read_time="2024-12-08T17:54:00-08:00",
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
                    "content": "Remind me of the new time for tonight practice again.",
                },
            ],
            reasoning="The user wants to be reminded the new time of tonight practice. This implies that one of their events has changed times.\n\nFrom their recent messages in the last half hour I can see that Charles sent a message about changing their rehearsal time so that must be what the user is looking for.\n\nThe user's Theater Rehearsal event on 8 December 2024 is scheduled from 19:00-22:00 so I will tell the user that.",
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
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – Agent uses calendar tools to look up rehearsal timing
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
                # Milestone 1 – Confirms that related conversation was found in messages history
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
                    ],
                ),
                # Milestone 2 – User-facing response mentions the correct date, time window, and location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We just need key facts; phrasing can vary
                                    "content": [
                                        (
                                            "7 pm",
                                            "7 p.m.",
                                            "7pm",
                                            "19:00",
                                            "7:00",
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
                (0, 1),  # Whatsapp lookup → confirm correct event details
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_75ee90c1-5a08-4b93-bc73-03aee990825d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "calendar",
                "whatsapp_messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
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
                    "content": "What time is the Theater Rehearsal?",
                },
            ],
            reasoning="The user wants to know the time of the Theater Rehearsal event on 8 December 2024 from 19:00-22:00. Looking at their calendar they only have one event with that name so I will tell them the start time for that.",
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
                # Milestone 0 – Agent uses calendar tools to look up the rehearsal
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
                # Milestone 1 – Confirm Theater Rehearsal event (with correct date and time) was retrieved
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
                # Milestone 2 – User is told the correct rehearsal time window (focus on time/date in response)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We only check that the content mentions the correct date and time window.
                                    "content": [
                                        (
                                            "December 8",
                                            "Dec 8",
                                            "8 December",
                                            "8th of December",
                                            "12-08",
                                            "today",
                                            "tonight",
                                            "2024-12-08T19:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Separate check to ensure the 7–10 pm (19:00–22:00) window is conveyed
                                    "content": [("7:00 pm", "7 pm", "19:00", "7pm")],
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
                (0, 1),  # Calendar lookup → confirm correct rehearsal event
                (
                    1,
                    2,
                ),  # Correct event retrieved → user informed with correct time/date
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_116912b3-43ed-4656-897f-3895f21c77f9_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "email",
                "contact",
                "calendar",
                "misinformation_no",
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
                        "You want to email Vickie to ask if she would be up for running some lines before theatre practice tonight. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Email Vickie: 'Would you be up for running some lines half an hour before theatre practice tonight?' Be sure to include the exact time.",
                },
            ],
            reasoning="The user wants to email Vickie. I look up contacts and find Vickie Lee (vickie.lee@orchardtheater.com). Next, I check the calendar and see that “Theater Rehearsal” starts tonight at 7:00 pm, so half an hour before is 6:30 pm. I send an email to vickie.lee@orchardtheater.com: “Would you be up for running some lines at 6:30 pm, half an hour before theatre practice tonight?”",
            success_conditions=[
                {
                    "input_text": 'An email is sent to vickie.lee@orchardtheater.com asking: "Would you be up for running some lines at 6:30 pm, half an hour before theatre practice tonight?"',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "send_email",
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Fix - milestone 0 sould first find Vickie's contact in this case their email address
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
                                    "status": "sent",
                                    "body": [("18:30", "6:30 pm", "6:30pm")],
                                    "creation_datetime_iso": "2024-12-08T18:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_subset_match_similarity,
                                "status": column_exact_match_similarity,
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
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_f0b73bd3-732d-4a5a-97ef-9c143e4e4a1f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "calendar",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T17:51:00-08:00",
            is_read_time="2024-12-08T17:51:00-08:00",
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
                    "content": "Remind me of the new time for tonight's practice again.",
                },
            ],
            reasoning="The user wants to be reminded of the new time for tonight’s rehearsal. From their WhatsApp messages I can see that Charles sent a note rescheduling the rehearsal to 7 PM (19:00). I will surface that information to the user.",
            success_conditions=[
                {
                    "input_text": "The assistant tells the user that tonight's Theater Rehearsal has been rescheduled to 7 PM (19:00).",
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
                # Milestone 0 – Agent queries WhatsApp messages (so it can surface Charles’s note)
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
                # Milestone 1: conversation with Charles found
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
                                                "value": "Charles Wilde",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-08T17:50:00-08:00",
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
                # Milestone 2 – The user is informed of the 7 PM (19:00) rehearsal time
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
                                            "7 PM",
                                            "7pm",
                                            "7 p.m.",
                                            "19:00",
                                            "7:00",
                                            "7 pm",
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
                (0, 1),  # Calendar lookup precedes informing the user
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_12_3f439e66-782f-42fd-b33d-e38da723b6e8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_12",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T22:05:00-08:00",
            is_read_time="2024-12-08T22:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "Your theater rehearsal group has decided to meet at the same time next week and you want your assistant to create this event in your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Theater rehearsal is going to be at the same time next week, can you pop it in my calendar.",
                },
            ],
            reasoning="The user wants to create a calendar event for their theater rehearsal next week, at the same time.\n\nFirst I will need to find out with time the theater rehearsal was at this week, looking through the user's calendar events, I can see Theater Rehearsal was from 19:00 to 22:00 on Sunday. With this information I can create an event for next Sunday, December 15 from 19:00 to 22:00 again.\n\nI can also see that Charles Wilde and Vickie Lee were attendees of this event and will add them to next week’s version.\n\nSo finally, a new event titled Theater Rehearsal is created from 19:00 to 22:00 on 15 December 2024, with Charles Wilde and Vickie Lee, and the user is informed that the event has been scheduled.",
            success_conditions=[
                {
                    "input_text": "New event titled Theater Rehearsal is created from 19:00 to 22:00 on 15 December 2024, with Charles Wilde and Vickie Lee.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The assistant informs the user that the Theater Rehearsal has been scheduled for December 15.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=[
                "create_calendar_event",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – The agent looks up existing calendar information and finds out that by "practice" user refers to "rehearsal".
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
                        ),
                    ],
                ),
                # Milestone 1: rehearsal event found
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
                            reference_milestone_node_index=0,
                        ),
                    ]
                ),
                # Milestone 2 – A new calendar event for next week’s rehearsal has been created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Theater Rehearsal",
                                    "start_datetime_iso": "2024-12-15T19:00:00-08:00",
                                    "end_datetime_iso": "2024-12-15T22:00:00-08:00",
                                    "attendees_names": [
                                        ["Charles Wilde", "Vickie Lee"]
                                    ],
                                    "creation_datetime_iso": "2024-12-08T22:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial state
                        ),
                    ],
                ),
                # Milestone 3 – The user is informed that the event has been scheduled
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
                                            "December 15",
                                            "12-15",
                                            "Dec 15",
                                            "15 December",
                                            "15th of December",
                                            "12/15",
                                        )
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
                (0, 1),  # looked up calendar → created new event
                (1, 2),  # event created
                (2, 3),  # informed the user
            ],
        ),
    ]
