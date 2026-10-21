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
    column_list_subset_match_similarity,
    column_list_tuple_contains_similarity,
    column_one_similarity,
    column_rouge_l_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
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


def get_TAG_DAWEI_SHEN_pilot_plot_10(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="DAWEI_SHEN_10_bd1daaaf-3666-41b7-9c2c-bcc300ffc520_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_10",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "calendar",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T10:30:00-08:00",
            is_read_time="2024-12-07T10:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You are navigating to the Café to meet Jess for brunch and want to bring up the address attached to the event. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where am I meeting Jess for brunch?",
                },
            ],
            reasoning="Ok, the user wants to know where they're meeting Jess for brunch. First I'll check user's calendar and see if there's any event that matches with this description. OK, I found an event 'Brunch with Jess' on December 07, I understant that's the event user asks about. I'll now check the location of that event. I see it's at Bluebird Café, 202 Main St, Orchard County, CA. I will inform user of the location.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. the user is informed that the location of the event 'Brunch with Jess' is Bluebird Café, 202 Main St, Orchard County, CA. ",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "get_all_messages",
                "search_messages",
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
                # Milestone 1 – find lunch event
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
                                                "value": "Brunch with Jess",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T11:00:00-08:00",
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
                # Milestone 2 – The user is told the brunch address
                Milestone(
                    snapshot_constraints=[
                        # The reply must mention “Bluebird”
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Bluebird",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_10_486a3039-fa30-41a5-84e9-eac28965f523_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_10",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T15:30:00-08:00",
            is_read_time="2024-12-07T15:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "The user wishes to know when the tech panel hosted by Jeff Bing is happening. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I'm attending a panel on Tuesday. What time is it taking place?",
                },
            ],
            reasoning="The user wants to know what time the panel they are attending on Tuesday is taking place. I will look at their calendar for Tuesday 10th December 2024. Ok, I find an event titled “Tech Panel Hosted by Jeff Bing” that starts at 09:00 which matches with user's description. I will tell the user that this panel is scheduled for Tuesday 10th December 2024 at 09:00.",
            success_conditions=[
                {
                    "input_text": "The user is told that the event “Tech Panel Hosted by Jeff Bing” is on Tuesday, 10 December 2024 at 09:00.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent looks up information about the event
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
                # Milestone 1 – The tool output contains the specific Tech Panel event
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
                # Milestone 2 – The user is told the correct date and time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("9", "nine")],
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
                (0, 1),  # Tool use ➜ event identified
                (1, 2),  # Event identified ➜ inform user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_10_961cffa5-a19c-49d5-a7e6-9a4f620a52c9_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_10",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T10:06:00-08:00",
            is_read_time="2024-12-07T10:06:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to add your brunch plans with Jess to your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Add my brunch date with Jess to my calendar. ",
                },
            ],
            reasoning="User wants to add their brunch date with Jess to the calendar. Let me find out when is the brunch. I'll first check messages and see if there's any conversation regarding the brunch. Ok, I found a recent message from Jess on December 07 at 10:05 that says brunch is at 11:00 AM at Bluebird café, 202 Main St, Orchard County. Ok, now I gathered necessary information I'll create the calendar event titled as “Brunch with Jess” and schedule it for 11:00 AM on 2024-12-07 with location set to Bluebird with Jess as invitee. I'll inform user that the event is scheduled.",
            success_conditions=[
                {
                    "input_text": "A calendar event named 'Brunch with Jess' is created for 11:00 AM on 2024-12-07 with location set to Bluebird café and with Jess as invitee.",
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
                "search_messages",
                "get_all_messages",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks through the message history to find brunch details
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
                # Found message from Jess
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
                                                "value": "2024-12-07T10:05:00-08:00",
                                                "partial": False,
                                            },
                                            "status": {
                                                "value": "read",
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
                # Milestone 2 – A new calendar event for brunch at 11 AM is created and contains the café details
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Brunch",  # name mentions brunch
                                    "start_datetime_iso": "2024-12-07T11:00:00",  # starts at 11 AM (any date)
                                    "location": "Bluebird",  # café name / address captured,
                                    "creation_datetime_iso": "2024-12-07T10:06:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "location": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to the initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # After searching messages, the event should be created
                (1, 2),  # After the event is created, the user should be informed
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_10_e52d334f-182f-48d4-9500-bfd874d6f918_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_10",
                "calendar",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T10:05:00-08:00",
            is_read_time="2024-12-07T10:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to add your brunch plans discussed with Jess to your calendar.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Add my brunch date with Jess to my calendar based on our discussion. ",
                },
            ],
            reasoning="The user wants to add Brunch with Jess to calendar. The user mentioned a discussion, so I will first search messages from Jess for brunch details. \n\n"
            "I can see Jess has given the time of 11am for brunch and has also sent the address of the café, Bluebird Café, so I can assume the user wants to add the event for 11am. "
            "I will also save the message to the event containing the address of the café. ",
            success_conditions=[
                {
                    "input_text": "1. Messages from Jess are searched for details regarding brunch.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. New calendar event with title contains 'brunch' and Jess Zimmer as an invitee created, with location Bluebird Café and starts on 2024-12-07T11:00:00. ",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_messages",
                "get_all_messages",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Messages from Jess are searched for brunch details (information retrieval)
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
                # Milestone 1 – Confirm a message thread from Jess with brunch time and address was retrieved
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
                                        # We just need to confirm that the key brunch message from Jess exists
                                        match_conditions={
                                            "participants_addresses": {
                                                "value": [
                                                    "dawei.shen@orchardtech.com",
                                                    "jess.zimmer@fintechstartup.com",
                                                ],
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "jess.zimmer@fintechstartup.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Let's meet at the Bluebird Café",
                                                "partial": True,  # allow full sentence match
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
                # Milestone 2 – Calendar event created for brunch with Jess at 11am on Dec 7, 2024, with address saved
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Brunch with Jess",
                                    "start_datetime_iso": "2024-12-07T11:00:00-08:00",
                                    # We don't strictly require end time; if set, it'll be ignored unless included here
                                    "location": [
                                        ("Bluebird Café", "202 Main St, Orchard County")
                                    ],
                                    # Attendees: at least Dawei and Jess by name, allow extras
                                    "attendees_names": [["Dawei Shen", "Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-07T10:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_rouge_l_similarity,
                                "location": column_str_contains_any_similarity,
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
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Search messages → confirm brunch details from Jess
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_10_41480a14-263b-4c90-a41e-e3f5177364d4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_10",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T08:20:00-08:00",
            is_read_time="2024-12-09T08:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You realized you have scheduled the wrong date and time for 'tech panel' in your calendar.  You need to re-schedule it for the following morning and it is occurring from 10:00 to 12:00. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I got my dates mixed up, the tech panel should be a day later. Could you reschedule that. It starts at 10.",
                },
            ],
            reasoning="Okay, so the user wants to reschedule an event called tech panel and it starts at 10. Firstly, I will look up and find this event in user's calendar. Ok, I see there's an event 'Tech Panel hosted by Jeff Bing' scheduled on December 10 at 9:00 am. I understand this is the event user refers to. User wants to move it to the following day which means the new date shall be December 11 and user indicated that the new start time is at 10:00. Ok, I'll reshedule it to Wednesday December 11 at 10:00 am. I'll retain the original duration and make the new duration 10:00 to 12:00. I'll inform user of this.",
            success_conditions=[
                {
                    "input_text": "Reschedule the event 'Tech Panel Hosted by Jeff Bing' on Tuesday December 10th at 09:00 to Wednesday December 11th from 10:00 to 12:00.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "remove_calendar_event",
                "create_calendar_event",
                "modify_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the existing calendar event
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
                # Milestone 1 – The original “Tech Panel Hosted by Jeff Bing” event is found
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
                        )
                    ]
                ),
                # Milestone 2 - A new event with the correct time is updated for 10:00-12:00 on 2024-12-11
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Tech Panel Hosted by Jeff Bing",
                                    "start_datetime_iso": "2024-12-11T10:00:00-08:00",
                                    "attendees_names": [["Dawei Shen", "Jeff Bing"]],
                                    "creation_datetime_iso": "2024-12-09T08:20:00-08:00",
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
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_10_486a3039-fa30-41a5-84e9-eac28965f523_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_10",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T15:30:00-08:00",
            is_read_time="2024-12-07T15:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "The user wishes to know when the tech panel hosted by Jeff Bing is happening. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is the tech panel hosted by Jeff Bing happening?",
                },
            ],
            reasoning="the user is looking for information about when Tech Panel Hosted by Jeff Bing, is taking place. After looking I have found an event with that name in their calendar. \nThe event takes place on Tuesday 10th December 2024 from 09:00 to 11:00. I relay this information to the user.",
            success_conditions=[
                {
                    "input_text": "1. The date and time for the event 'Tech Panel Hosted by Jeff Bing' , Tuesday 10th December 2024 from 09:00 to 11:00 is given to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the event information via an appropriate retrieval tool
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
                # Milestone 1 – The original “Tech Panel Hosted by Jeff Bing” event is found
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
                        )
                    ]
                ),
                # Milestone 2 – The user is informed of the correct date and time of the tech panel
                Milestone(
                    snapshot_constraints=[
                        # Date mention
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "December 10",
                                            "12-10",
                                            "12/10",
                                            "Tue",
                                            "Dec 10",
                                            "10 December",
                                            "10th of December",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        # Start-time mention (allow common variants)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("9:00", "09:00", "9 am", "9am")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_10_bd1daaaf-3666-41b7-9c2c-bcc300ffc520_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_10",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T10:08:00-08:00",
            is_read_time="2024-12-07T10:08:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You are navigating to the Café to meet Jess for brunch and want to bring up the address attached to the event. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where am I doing brunch today?",
                },
            ],
            reasoning="Ok, so the user wants to know where they are going for brunch today. I first checked their calendar. I don't see any event named 'brunch' in user's calendar. I will search for messages then. Ok, I found the message conversation with Jess on December 07 at 10:00 and 10:05, they talked about having brunch. They mentioned the location is Bluebird Café, 202 Main St, Orchard County. I will let the user know that Brunch with Jess is taking place at Bluebird Café, 202 Main St, Orchard County, CA. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. the user is informed that the address of the brunch is Bluebird Café, 202 Main St, Orchard County, CA. ",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the brunch event (messages or calendar)
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
                                    # The brunch address lives in both the Jess
                                    # messages and the "Brunch with Jess" calendar
                                    # event, so either lookup path is acceptable.
                                    target_tools=[
                                        "search_messages",
                                        "get_all_messages",
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – The user is told the correct café address
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Either the café name or the street address must appear
                                    "content": [("Bluebird", "202 Main St")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_10_bf9db15c-6226-4b0c-a456-57eb5882d509_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_10",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T12:30:00-08:00",
            is_read_time="2024-12-07T12:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to view the email about the revised draft for virtual assistant you received from your co-worker. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Open the virtual assistant email I received a few days ago please, the one with comments ",
                },
            ],
            reasoning='The user wants to view the email about the "virtual assistant" that they received "a few days ago".\n\nFirstly, I\'ll go to their Mail and search for any messages with a subject line that contains "Revised Draft for Virtual Assistant".\n\nI find one matching email from Theo Appleseed, received at 09:15 on Monday, December 2nd 2024. There\'s an attachment called "Revised_Algorithm_Draft_with_Comments". \n\nBecause this matches the user\'s description, I will open it and show its contents to the user.',
            success_conditions=[
                {
                    "input_text": 'The email received from Theo Appleseed with the subject "Revised Draft for Virtual Assistant" is presented to the user.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – An email-retrieval tool is invoked
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
                # Milestone 1 – The search result actually contains Michelle’s email about the revised draft
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
                                                "value": "Revised Draft for Virtual Assistant",
                                                "partial": True,
                                            },
                                            "sender_address": {
                                                "value": "theo.appleseed@orchardtech.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-02T09:15:00-08:00",
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
                # Milestone 2 – The agent shows the user the requested email (any reasonable phrasing)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Theo",  # need to open the one from Theo
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
                (0, 1),  # tool call → verify result contains the email
                (1, 2),  # email located → user is informed
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_10_bf9db15c-6226-4b0c-a456-57eb5882d509_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_10",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T12:30:00-08:00",
            is_read_time="2024-12-07T12:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to view the email about the revised draft for virtual assistant you received from your co-worker. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the revised draft for the virtual assistant email I received from my co-worker a few days ago, the first version",
                },
            ],
            reasoning="The user wants to view the email about the \"revised draft for the virtual assistant\" that they received from a co-worker a few days ago.\n\nFirstly, I'll go to their Mail and see if I can find any emails in their inbox with a subject line that corresponds to the title of the email they mentioned in their request.\n\nI've found two. Both have the subject line \"Revised Draft for Virtual Assistant Algorithm\". One is from Theo Appleseed, received at 09:15 on Monday, December 2nd 2024, and the other is from Michelle Barnes, received at 09:00 on Monday, December 2nd 2024.\n\nNow I have to check the user's Contacts to try and figure out which of these people are the user's co-workers.\n\nOkay, so it turns out that both are the user's co-workers. Since this is the case, I'll explain to the user the situation and ask them to clarify which of the two emails they want to view.\n\nThe user has said they want to view the email received from Michelle Barnes.\n\nI will show them this now.",
            success_conditions=[
                {
                    "input_text": 'The email received from Michelle Barnes with the subject "Revised Draft for Virtual Assistant Algorithm" is presented to the user.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – some email-lookup tool is invoked
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
                # Milestone 1 – the returned email list contains Michelle’s revised-draft email
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
                                                "value": "Revised Draft for Virtual Assistant Algorithm",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "michelle.barnes@orchardtech.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-02T09:00:00-08:00",
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
                # Milestone 2 – the agent shows the user the requested email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Michelle",
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
            name="DAWEI_SHEN_10_e095795c-ac7d-44de-9b75-c93411005dbf_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_10",
                "calendar",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T11:05:00-08:00",
            is_read_time="2024-12-07T11:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "Your sister asked you to help her clean up her flooded basement at the last minute, so you need to cancel brunch with Jess. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Text Jess "So sorry I have to cancel last minute - my sister\'s basement flooded and I need to help her" and get rid of the brunch event going on now. ',
                },
            ],
            reasoning="The user wants to text Jess. There's only one Jess in their contacts, Jess Zimmer, so that's who I'll send the message to. I need to make sure it says \"So sorry I have to cancel last minute - my sister's basement flooded and I need to help her.\"\n\nThe user wants a brunch event happening now cancelled. I see from user's calendar that an event called Brunch with Jess is scheduled for today at 11:00-13:00, and right now it is 11:05, so that must be the event they are talking about. I will remove it from the calendar. ",
            success_conditions=[
                {
                    "input_text": '1. A text message is sent to Jess Zimmer saying "So sorry I have to cancel last minute - my sister\'s basement flooded and I need to help her"',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The event called Brunch with Jess on 7 December 2024 from 11:00-13:00 is removed from calendar. ",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
                "get_all_contacts",
                "search_contacts",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent searches contacts to identify Jess for messaging
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
                # Milestone 1 – Confirms Jess Zimmer was found in contacts (drives correct recipient resolution)
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
                        )
                    ],
                ),
                # Milestone 2 – A message is sent to Jess with the specified cancellation text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Participants must include both Dawei and Jess, via any of their known identifiers
                                    "participants_addresses": [
                                        [
                                            (
                                                "jess.zimmer@fintechstartup.com",
                                                "+1 555-123-4567-8902",
                                            ),
                                            (
                                                "dawei.shen@orchardtech.com",
                                                "+1 555-123-4567-8901",
                                            ),
                                        ]
                                    ],
                                    "content": "So sorry I have to cancel last minute - my sister's basement flooded and I need to help her",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-07T11:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_exact_match_similarity,
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
                # Milestone 3 – The agent searches calendar events (to locate the brunch event to cancel)
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
                # Milestone 4 – Confirms the brunch event on Dec 7, 2024 11:00–13:00 was retrieved
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
                                                "value": "Brunch with Jess",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T11:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-07T13:00:00-08:00",
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
                    ],
                ),
                # Milestone 5 – The brunch event is removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Brunch with Jess",
                                    "start_datetime_iso": "2024-12-07T11:00:00-08:00",
                                    "end_datetime_iso": "2024-12-07T13:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact search → confirm Jess contact
                (1, 2),  # Jess identified → send correct message
                (3, 4),  # Calendar search → confirm brunch event
                (4, 5),  # Event identified → event removed
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_10_5632aa1c-16d7-4e3c-9002-c86a108c37bf_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_10",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T10:10:00-08:00",
            is_read_time="2024-12-09T10:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to be reminded of when the tech panel with Jeff is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "At what time is my event scheduled for tomorrow? the one to talk about consumer electronics?",
                },
            ],
            reasoning="The assistant will look up tomorrow’s calendar events, find the entry titled 'Tech Panel Hosted by Jeff Bing' scheduled for 9:00 AM on 10 Dec 2024 with notes mentioning a panel discussion on upcoming trends in consumer electronics, and tell the user that the it starts at 9:00 AM.",
            success_conditions=[
                {
                    "input_text": "The assistant tells the user that the event 'Tech Panel Hosted by Jeff Bing' is scheduled for tomorrow at 9:00 AM.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The answer does not give 2:00 PM as the time.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – the calendar is queried for the tech panel
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
                # Milestone 1 – the correct event is returned in the tool result
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
                # Milestone 2 – the user is informed of the event time and topic
                Milestone(
                    snapshot_constraints=[
                        # mention of the tech panel
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Tech Panel",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # mention of the start time
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("9:00", "9 am", "9am")],
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
            minefields=[
                # Should not reply with event Dataset Review with Michelle which on 2 pm
                Minefield(
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
                                            "2 pm",
                                            "2 PM",
                                            "14:00",
                                            "2 p.m.",
                                            "2pm",
                                            "2:00",
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
        ),
    ]
