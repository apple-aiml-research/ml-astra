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
    column_list_tuple_subset_contains_similarity,
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
    result_list_match_existence_extractor,
)
from astra_tool_sandbox.scenarios.astra_v1.protagonist_simulator_few_shot_examples import (
    USER_INSTRUCTION_SINGLE_TURN,
)


def get_TAG_JOHN_QUINN_pilot_plot_19(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="JOHN_QUINN_19_6bf997bf-ec67-4332-b0c0-4502e0ce7de0_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "contact",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-02T18:00:00-07:00",
            is_read_time="2024-08-02T18:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "It has escaped you when you set the hike with apricot to start at as you planned it quite a while ago. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When am I heading out with my girlfriend on Sunday?",
                },
            ],
            reasoning='Ok so the user wants to know when they are heading out with my girlfriend on Sunday. First I will establish who their girlfriend is. In their contacts Apricot Sweeney is labelled as their girlfriend so this must be who they are referring to. Next is where they are heading with Apricot. I will look to future events with Apricot as an invitee. I have found the event "Hiking with Apricot" which I believe is the event they are talking about. I will now inform the user that the event "Hiking with Apricot" takes place at 09:00-12:00 on 4 August 2024. ',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the event "Hiking with Apricot" takes place at 09:00-12:00 on 4 August 2024. ',
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
                # Milestone 0 – The agent consults the calendar to look for the relevant Sunday hike
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
                # Milestone 1 – Confirm that the calendar query returned the correct hike event
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
                                                "value": "Hiking with Apricot",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-08-04T09:00:00-07:00",
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
                # Milestone 2 – The user is informed of the event name, date, and time
                Milestone(
                    snapshot_constraints=[
                        # Time must be mentioned (any common 9 a.m. representation)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        ("09:00", "9:00", "9 am", "9am", "9 a.m.")
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
                (0, 1),  # Calendar lookup → confirm correct event retrieved
                (1, 2),  # Event retrieved → user informed
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_93da9c5a-cc7f-4dc0-a17f-b751537fce11_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-03T20:00:00-07:00",
            is_read_time="2024-08-03T20:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You can't remember what time your hike with Apricot is tomorrow.  You want to know if you'll have time to run to the store tomorrow morning before the hike so you need to know the time. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is the hike?",
                },
            ],
            reasoning="The user wants to know when \"the hike\" is. I wonder what they meant by that. I should check their calendar for a related event. I see one similar event with the name 'Hiking with Apricot', occurring tomorrow, August 4th, at 9:00-12:00. I assume this is what they're referring to. I'll show the user the details of the event including the time now. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The time of the event 'Hiking with Apricot' tomorrow, on Sunday, August 4th at 9:00-12:00 is shown to the user. ",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent looks up calendar events
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
                # Milestone 1 – Returned calendar data contains the hike event with correct start time
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
                                                "value": "Hiking with Apricot",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-08-04T09:00:00-07:00",
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
                            reference_milestone_node_index=0,  # depends on calendar search
                        )
                    ]
                ),
                # Milestone 2 – Agent tells the user the hike time (9 am start)
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
                                            "9:00",
                                            "09:00",
                                            "9 am",
                                            "9am",
                                            "9 a.m.",
                                            "9 am",
                                            "9 a.m.",
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
            name="JOHN_QUINN_19_93da9c5a-cc7f-4dc0-a17f-b751537fce11_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_19",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-03T20:00:00-07:00",
            is_read_time="2024-08-03T20:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You can't remember what time your hike with Apricot is tomorrow.  You want to know if you'll have time to run to the store tomorrow morning before the hike so you need to know the time. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is Hiking with Apricot? ",
                },
            ],
            reasoning="The user wants to know when \"Hiking with Apricot\" is. I should check their calendar for a related event. I see one matching event, 'Hiking with Apricot', occurring tomorrow, August 4th, at 9:00-12:00. I assume this is what they're referring to. I'll show the user the details of the event including the time now. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The time of the event 'Hiking with Apricot' tomorrow, on Sunday, August 4th at 9:00-12:00 is shown to the user. ",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent looks up calendar information
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
                # Milestone 1 – Verify that the event “Hiking with Apricot” on 2024-08-04 09:00 was found
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
                                                "value": "Hiking with Apricot",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-08-04T09:00:00-07:00",
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
                # Milestone 2 – Agent tells the user the correct time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("9:00", "9 am", "9am", "09:00")],
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
                (0, 1),  # Calendar lookup → confirm event found
                (1, 2),  # Event found → inform the user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_eee97407-f6be-4e9b-a244-a7678a37d4bc_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_19",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T17:50:00-07:00",
            is_read_time="2024-07-25T17:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to dictate a reply to Apricot Sweeney saying that you will be 30 minutes late to the Hiking Trip event. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a message reply saying "Hi Apricot babe I will be 30 minutes late to the hiking event sorry about that".',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Apricot Sweeney.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.\n",
            success_conditions=[
                {
                    "input_text": "1. A reply message is sent to Apricot Sweeney saying that you will be 30 minutes late to the Hiking Trip event.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "send_message",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent tries to locate Apricot or the existing conversation
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
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – A new outgoing message to Apricot Sweeney is added stating the 30-minute delay
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Ensure Apricot is one of the participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "415-555-0128",
                                                "apricot.sweeney@sfhealth.com",
                                            )
                                        ]
                                    ],
                                    # Make sure the message conveys being 30 minutes late
                                    "content": [("30 minutes", "thirty minutes")],
                                    "creation_datetime_iso": "2024-07-25T17:50:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_str_contains_any_similarity,
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
                (
                    0,
                    1,
                ),  # Retrieval of contact/conversation precedes sending the message
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_6bf997bf-ec67-4332-b0c0-4502e0ce7de0_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "contact",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-02T18:00:00-07:00",
            is_read_time="2024-08-02T18:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "It has escaped you when you set the hike with apricot to start at as you planned it quite a while ago. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'When is "Hiking with Apricot?"',
                },
            ],
            reasoning='Ok so the user wants to know when "Hiking with Apricot" is. First I will find the event "Hiking with Apricot." Now that I have found it I will inform the user that the event "Hiking with Apricot" takes place at 09:00-12:00 on 4 August 2024. ',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the event "Hiking with Apricot" takes place at 09:00-12:00 on 4 August 2024. ',
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
                # Milestone 0 – Agent looks up calendar to find the event
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
                # Milestone 1 – Verify the returned calendar entry is “Hiking with Apricot”
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
                                                "value": "Hiking with Apricot",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-08-04T09:00:00-07:00",
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
                # Milestone 2 – Agent informs the user with correct date & time
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
                                            "August 4",
                                            "4 August",
                                            "8-04",
                                            "8/04",
                                            "Sunday",
                                            "Aug 4",
                                            "8/4",
                                            "2024-08-04",
                                            "2024-08-04T09:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                        # Check start-time mention (9 AM)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        ("09:00", "9:00", "9 am", "9am", "9 a.m.")
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
            name="JOHN_QUINN_19_6b8bbb6e-fc4a-4ed6-8dc0-921bb456918c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-02T19:45:00-07:00",
            is_read_time="2024-08-02T19:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know to know when is your hike with Apricot as you want to schedule in a spin class for later that day. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is my next hike with Apricot, as I want to schedule in a spin class at 16:00 that day?",
                },
            ],
            reasoning="Okay, the user wants to first know when is they next 'hike with Apricot'. I can see in their contacts they only have one person named 'Aprciot', 'Apricot Sweeney' so I can assume this the contact the user has an event with. Next, I can check the user's calendar and I can see there is one event matching with Apricot Sweeney named 'Hiking with Apricot' scheduled for 4 August 2024 from 09:00 to 12:00. This is the event the user is looking for so I can read out the requested information to them.\n\nSecondly, they want to schedule a new event named 'Spin Class' at 16:00 on that day, 4 August 2024. There are no conflicting events so I can schedule that in for the user.",
            success_conditions=[
                {
                    "input_text": "1. The event 'Hiking with Apricot' scheduled for 4 August 2024 from 09:00 to 12:00 with Apricot Sweeney is read out to the user.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. A new event titled 'Spin Class' is created on 4 August 2024 at 16:00.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar to find next hike with Apricot
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
                # Milestone 1 – User is told the correct hike details (event with Apricot on Aug 4 2024)
                Milestone(
                    snapshot_constraints=[
                        # Must mention the correct date
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Accept a variety of ways the date might be phrased
                                    "content": [
                                        (
                                            "August 4",
                                            "Aug 4",
                                            "4 August",
                                            "8-4",
                                            "08-04",
                                            "8/4",
                                            "08/04",
                                            "the 4th",
                                            "Sunday",
                                            "2024-08-04T09:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                    ],
                    # The write graded by a later milestone necessarily lands BEFORE the agent's final
                    # reply, so the default CALENDAR guardrail here would make this milestone unreachable.
                    # That later milestone still grades the write, so no hole is opened.
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
                # Milestone 2 – New “Spin Class” calendar entry is created for 16:00 on 4 Aug 2024
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Spin Class",
                                    "start_datetime_iso": "2024-08-04T16:00:00-07:00",
                                    "creation_datetime_iso": "2024-08-02T19:45:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar lookup precedes telling the user
                (0, 2),  # Calendar lookup supplies date needed to create spin class
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_76f03c88-4e8b-4bba-9187-d6bccff349c3_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "contact",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T18:15:00-07:00",
            is_read_time="2024-07-25T18:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know where your hike with Apricot is taking place. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where is the hike with my girlfriend taking place?",
                },
            ],
            reasoning="The user wants to know where their hike with their girlfriend is taking place. Let me look for their girlfriend in contacts. It is Apricot Sweeney.  Let me look for their hike in Calendar. I found it. I will inform the user that the event 'Hiking with Apricot' on August 4th from 09:00-12:00 is located at Lake Serenity Trail.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their event 'Hiking with Apricot' on August 4th from 09:00-12:00 is located at Lake Serenity Trail.",
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
                # Milestone 0 – The agent looks through the calendar for the hike event
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
                # Milestone 1 – Confirm the returned calendar search includes the hike at Lake Serenity Trail
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
                                                "value": "Hiking with Apricot",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Lake Serenity Trail",
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
                        ),
                    ],
                ),
                # Milestone 2 – The user receives a message containing the correct location (and event identifier)
                Milestone(
                    snapshot_constraints=[
                        # Must mention the location
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Lake Serenity Trail",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
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
            name="JOHN_QUINN_19_07ab842a-e3d0-4b7b-9eb4-6c384e43d39c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-03T16:00:00-07:00",
            is_read_time="2024-08-03T16:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to cancel your hike with Apricot tomorrow after hurting your foot at today's hike "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to cancel tomorrow with Apricot",
                },
            ],
            reasoning='The user wants to cancel tomorrow with Apricot. I\'ll look at their calendar to see if anything is scheduled. The user has an event titled "Hiking with Apricot" scheduled for tomorrow at 9:00 am. I\'ll remove "Hiking with Apricot" from the calendar and inform the user.',
            success_conditions=[
                {
                    "input_text": '1. "Hiking with Apricot" is removed from the calendar ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (must access calendar DB)
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
                # Milestone 1 – “Hiking with Apricot” event is removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Hiking with Apricot",
                                    "start_datetime_iso": "2024-08-04T09:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_b09f4d47-e5cb-4394-882d-28bac2b5b6d6_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "contact",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T18:00:00-07:00",
            is_read_time="2024-07-25T18:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to make sure you have set the right date for your hike with Apricot. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What date is my hike with Apricot?",
                },
            ],
            reasoning="The user is asking about the date of an event.\nI should consult their calendar. I can see an exact match for the user's query. \nThe event Hiking with Apricot is scheduled for August 04, 2024, 09:00-12:00.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Date of Hiking with Apricot scheduled for August 04, 2024, 09:00-12:00 is confirmed as August 04, 2024.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent consults the calendar to look for the hike event
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
                # Milestone 1 – The agent tells the user the correct hike date
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
                                            "August 4",  # common full-month phrasing
                                            "Aug 4",  # abbreviated month
                                            "August 04",  # zero-padded day
                                            "2024-08-04",  # ISO style
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
            name="JOHN_QUINN_19_b09f4d47-e5cb-4394-882d-28bac2b5b6d6_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
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
            reference_time="2024-07-25T18:00:00-07:00",
            is_read_time="2024-07-25T18:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to make sure you have set the right date for your hike with Apricot. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What date is my trip with my girlfriend?",
                },
            ],
            reasoning="The user is asking about the date of an event.\nFirst, I should determine who they are referring to. I can see that Apricot Sweeney is tagged as girlfriend in the user's contacts.\nNext, I should consult their calendar. I cannot see an exact match for the user's query. Searching for events with Apricot I can see only one potential match. \nThe event Hiking with Apricot is scheduled for August 04, 2024, 09:00-12:00.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Date of Hiking with Apricot scheduled for August 04, 2024, 09:00-12:00 is confirmed as August 04, 2024.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent looks up calendar information
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
                # Milestone 1 – The expected hike event is found in the tool output from Milestone 0
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
                                                "value": "Hiking with Apricot",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-08-04T09:00:00-07:00",
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
                # Milestone 2 – The agent tells the user the correct date
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
                                            "August 4",
                                            "Aug 4",
                                            "2024-08-04",
                                            "04 August",
                                            "August 4th",
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
                (0, 1),  # Calendar lookup -> verify event found
                (1, 2),  # Event confirmed -> user informed
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_07ab842a-e3d0-4b7b-9eb4-6c384e43d39c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-03T16:00:00-07:00",
            is_read_time="2024-08-03T16:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to cancel your hike with Apricot tomorrow after hurting your foot at today's hike "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to cancel tomorrow with her",
                },
            ],
            reasoning='The user wants to cancel tomorrow with someone. I need to determine who the user is referring to. I\'ll look at their calendar to see if anything is scheduled. The user has an event titled "Hiking with Apricot" scheduled for tomorrow at 9:00 am. I can assume Apricot Sweeney is who the user was referring to. I\'ll remove "Hiking with Apricot" from the calendar and inform the user.',
            success_conditions=[
                {
                    "input_text": '1. "Hiking with Apricot" is removed from the calendar ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up upcoming calendar events (tool invocation)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",  # we only care that a calendar-searching tool was invoked
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
                # Milestone 1 – The calendar event “Hiking with Apricot” is removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Hiking with Apricot",
                                    "start_datetime_iso": "2024-08-04T09:00:00-07:00",
                                    "end_datetime_iso": "2024-08-04T12:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to original state
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # First discover the event, then remove it
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_76f03c88-4e8b-4bba-9187-d6bccff349c3_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "contact",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T18:15:00-07:00",
            is_read_time="2024-07-25T18:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know where your hike with Apricot is taking place. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where is the hike with Apricot taking place?",
                },
            ],
            reasoning="The user wants to know where their hike with Apricot is taking place. Let me look for the event in Calendar. I found it. I will inform the user that the event 'Hiking with Apricot' on August 4th from 09:00-12:00 is located at Lake Serenity Trail.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their event 'Hiking with Apricot' on August 4th from 09:00-12:00 is located at Lake Serenity Trail.",
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
                # Milestone 0 – The agent looks up calendar information
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
                # Milestone 1 – Confirm the expected calendar event was found in the tool output
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
                                                "value": "Hiking with Apricot",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Lake Serenity Trail",
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
                            reference_milestone_node_index=0,  # depend on the calendar lookup in Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – The agent informs the user of the location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Lake Serenity Trail",
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
                (0, 1),  # Calendar lookup -> confirm event
                (1, 2),  # Confirm event -> inform user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_6b8bbb6e-fc4a-4ed6-8dc0-921bb456918c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-02T19:45:00-07:00",
            is_read_time="2024-08-02T19:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know to know when is your hike with Apricot as you want to schedule in a spin class for later that day. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is my next hike, not the group one? And I need to put a spin class in for that day starting 4 hours after the hike finishes.",
                },
            ],
            reasoning="Right, the user wants to firstly know when is the next hike but not with a group. I can see one event matching this in their calendar named 'Hiking with Apricot' scheduled for 4 August 2024 from 09:00 to 12:00 with Apricot Sweeney. This must be the event the user wants and I can read out the required information to them.\n\nNext, they want to schedule in a new event called 'Spin Class' with at least 4 hours gap between. I can confirm with the user what time they wish to add the event at 16:00 that day and then can add it in for them.",
            success_conditions=[
                {
                    "input_text": "1. The event 'Hiking with Apricot' scheduled for 4 August 2024 from 09:00 to 12:00 with Apricot Sweeney is read out to the user.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. A new event titled 'Spin Class' is created on 4 August 2024 at 16:00.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the user’s upcoming hike in the calendar
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
                # Milestone 1 – Confirm the hiking event (Aug 4, 09:00–12:00) was included in the tool output
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
                                                "value": "Hiking with Apricot",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-08-04T09:00:00-07:00",
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
                # Milestone 2 – Agent tells the user when the hike is
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
                                            "August 4",
                                            "Aug 4",
                                            "4 August",
                                            "8-4",
                                            "08-04",
                                            "8/4",
                                            "08/04",
                                            "the 4th",
                                            "Sunday",
                                            "2024-08-04T09:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity,
                            },
                        )
                    ],
                    # The write graded by a later milestone necessarily lands BEFORE the agent's final
                    # reply, so the default CALENDAR guardrail here would make this milestone unreachable.
                    # That later milestone still grades the write, so no hole is opened.
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
                # Milestone 3 – A new calendar event “Spin Class” on Aug 4 at 16:00 is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Spin Class",
                                    "start_datetime_iso": "2024-08-04T16:00:00-07:00",
                                    "creation_datetime_iso": "2024-08-02T19:45:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,
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
                (0, 1),  # calendar search → confirm event present
                (1, 2),  # event confirmed → user informed
                (1, 3),  # event confirmed → schedule spin class
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_f4340985-d461-4029-b203-7d08e4abb9c6_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T17:50:00-07:00",
            is_read_time="2024-07-25T17:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        'You want to send a message to Apricot Sweeney saying "Hey Babes! I almost forgot to ask if you could bring the massage oil I left at your house last time, I find after these hikes my calves get very tight and might need your tender touch.  A massage from an Apricot, how unusual!" '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send my belle a textual communiqué that says "Hey Babes! I almost forgot to ask if you could bring the massage oil I left at your house last time, I find after these hikes my calves get very tight and might need your tender touch. A massage from an Apricot, how unusual!"',
                },
            ],
            reasoning='The user refers to his "belle" which refers to a girlfriend or partner, which is evident from the user\'s contacts is Apricot Sweeney. The user wants the message to say "Hey Babes! I almost forgot to ask if you could bring the massage oil I left at your house last time, I find after these hikes my calves get very tight and might need your tender touch. A massage from an Apricot, how unusual!"',
            success_conditions=[
                {
                    "input_text": "A message is sent to Apricot Sweeney",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up Apricot’s contact information
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
                # Milestone 1 – Confirm Apricot Sweeney appeared in the retrieved contact list
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
                                                "value": "Apricot Sweeney",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "415-555-0128",
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
                # Milestone 2 – A new text message to Apricot is sent with the requested content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Each tuple lists alternative identifiers for the same participant
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9108",
                                                "john.quinn@palantir.com",
                                            ),  # John (sender)
                                            (
                                                "415-555-0128",
                                                "apricot.sweeney@sfhealth.com",
                                            ),  # Apricot (receiver)
                                        ]
                                    ],
                                    "content": "massage oil",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-25T17:50:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare with initial state
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
            name="JOHN_QUINN_19_f6d86091-37ce-4412-8492-9cba1841b4d6_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T18:00:00-07:00",
            is_read_time="2024-07-25T18:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to message Apricot to ask about rescheduling your planned hike. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Text my girlfriend to say "actually can we do 11:00 instead"',
                },
            ],
            reasoning='The user is asking me to send a message.\nFirst, I should identify the intended recipient. The user has mentioned their girlfriend. Looking through their contacts I can see one person with a relationship tag of girlfriend, Apricot Sweeney. This must be the intended recipient.\nNext, I will go ahead and draft the message as instructed.\nA message saying "actually can we do 11:00 instead" will be sent to Apricot Sweeney,',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A message is sent to Apricot Sweeney saying "actually can we do 11:00 instead”',
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 ─ Agent uses a contacts-lookup tool to find the girlfriend
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
                # Milestone 1 ─ The returned contact list contains Apricot Sweeney
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
                                                "value": "Apricot Sweeney",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "415-555-0128",
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
                # Milestone 2 ─ A new message is sent to Apricot with the requested text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Ensure Apricot is one of the conversation participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "415-555-0128",
                                                "apricot.sweeney@sfhealth.com",
                                            )
                                        ]
                                    ],
                                    "content": "actually can we do 11:00 instead",
                                    "creation_datetime_iso": "2024-07-25T18:00:00-07:00",
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
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # contact lookup ➜ confirm Apricot contact
                (1, 2),  # confirmed contact ➜ message sent
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_f6d86091-37ce-4412-8492-9cba1841b4d6_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T18:00:00-07:00",
            is_read_time="2024-07-25T18:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to message Apricot to ask about rescheduling your planned hike. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Message Apricot asking actually can we do 11:00 instead",
                },
            ],
            reasoning='The user wants to message a contact named "Apricot" with the text "actually can we do 11:00 instead". First, I should find the named contact. I see Apricot Sweeney in the user\'s contacts.\nNext, I will draft the message as requested. \nA message saying "actually can we do 11:00 instead?" will be sent to Apricot Sweeney.',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A message is sent to Apricot Sweeney saying "actually can we do 11:00 instead”',
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up Apricot in contacts
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
                # Milestone 1 – Verify Apricot Sweeney surfaced from the contact search
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
                                                "value": "Apricot Sweeney",
                                                "partial": False,
                                            },
                                            # Either email or phone number is acceptable for a match
                                            "email": {
                                                "value": "apricot.sweeney@sfhealth.com",
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
                # Milestone 2 – New outgoing message sent to Apricot containing the reschedule text
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
                                                "415-555-0128",
                                                "apricot.sweeney@sfhealth.com",
                                            )
                                        ]
                                    ],
                                    "content": "actually can we do 11:00 instead",
                                    "creation_datetime_iso": "2024-07-25T18:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial baseline
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
            name="JOHN_QUINN_19_77318469-4819-4a0a-8fce-8d768760ed96_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T17:45:00-07:00",
            is_read_time="2024-07-25T17:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "I forgot to mention that it's due to rain so my girlfriend should bring a good coat. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send another message to my girlfriend that says \"It's due to rain so make sure you've got a hood\".",
                },
            ],
            reasoning='User wants to "send another" and I see they just sent a message 3 minutes ago to their girlfriend, Apricot Sweeney. I need the content message and once I have that I\'m ready to send this message.',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A message is sent to Apricot Sweeney to say \"It's due to rain so make sure you've got a hood\".",
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
                # Milestone 0 – Agent looks up contact info before sending the message
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
                # Milestone 1 – Verify that the message was actually sent to Apricot with the key phrasing
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # We only need to make sure Apricot’s address is among the participants;
                                    # extra participants (e.g., John’s own address) are allowed.
                                    "participants_addresses": [
                                        [
                                            (
                                                "415-555-0128",
                                                "apricot.sweeney@sfhealth.com",
                                            )
                                        ]
                                    ],
                                    "content": "hood",  # key phrase
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-25T17:45:00-07:00",
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
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_5397e3ee-00cc-4492-a829-213309801cd1_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_19",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-03T11:10:00-07:00",
            is_read_time="2024-08-03T11:10:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You forget what time your hike is with Apricot so you want to double-check. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is my hike with Apricot tomorrow? ",
                },
            ],
            reasoning='The user wants to know the time of an event tomorrow. First I will search for an event in calendar that includes an "Apricot" as an attendee. I have found "Hiking with Apricot" in the user\'s calendar. I will now check the timeframe of the event. I will now inform the user that the event "Hiking with Apricot" starts 09:00 on 4 August 2024. ',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the event "Hiking with Apricot" starts 09:00 on 4 August 2024. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent looks up calendar information (either lists all or searches)
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
                # Milestone 1 – Returned calendar data includes the “Hiking with Apricot” event
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
                                                "value": "Hiking with Apricot",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-08-04T09:00:00-07:00",
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
                # Milestone 2 – Agent informs the user of the event time (and optionally the date/event name)
                Milestone(
                    snapshot_constraints=[
                        # Ensure time is mentioned
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
                                            "09:00 am",
                                            "9 a.m.",
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
            name="JOHN_QUINN_19_a0fbbb9c-0968-438b-bfae-7dc099cb06a8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T15:25:00-07:00",
            is_read_time="2024-07-26T15:25:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You just can't wait until Sunday 4th August 2024 to see Apricot. . . .  You want to send her a message asking if she'd like to get dinner on Saturday or Sunday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to message my girlfriend please send her the message \"hello my bunny bear cutie pie, I can't stop thinking about how much I miss you. Do you think you have any free time to meet with me for dinner on Saturday or Sunday? Of course I'll treat my princess right... Let me know if you have free time. Lots of Love from your little cottage pie John\"",
                },
            ],
            reasoning="The user would like me to send a message to his girlfriend. I'm going to need to check the user's data to figure out who fits this relationship criteria.... I found Apricot Sweeney listed as the user's girlfriend, so this must be the person that the user wants to contact. With the user's confirmation, I'll send the message \"hello my bunny bear cutie pie, I can't stop thinking about how much I miss you. Do you think you have any free time to meet with me for dinner on Saturday or Sunday? Of course I'll treat my princess right... Let me know if you have free time. Lots of Love from your little cottage pie John\" to Apricot Sweeney.",
            success_conditions=[
                {
                    "input_text": "2. The message \"hello my bunny bear cutie pie, I can't stop thinking about how much I miss you. Do you think you have any free time to meet with me for dinner on Saturday or Sunday? Of course I'll treat my princess right... Let me know if you have free time. Lots of Love from your little cottage pie John\" to Apricot Sweeney.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent invokes a contact-lookup tool
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
                # Milestone 1 – Apricot Sweeney is returned from the contact search
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
                                                "value": "Apricot Sweeney",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "apricot.sweeney@sfhealth.com",
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
                # Milestone 2 – The love message is sent to Apricot
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require that Apricot’s phone number appears among the conversation participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "415-555-0128",
                                                "apricot.sweeney@sfhealth.com",
                                            )
                                        ]
                                    ],
                                    # Check that the affectionate opening is present in the message body
                                    "content": "hello my bunny bear cutie pie",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-26T15:25:00-07:00",
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
                (0, 1),  # contact lookup → confirm Apricot found
                (1, 2),  # Apricot found → message sent
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_ebd52a21-87b7-4123-8c39-27f56b3e23c5_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "email",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T17:50:00-07:00",
            is_read_time="2024-07-25T17:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want desperately to recall your email to Apricot because you mistakenly attached the video of your last hike with Theo Appleseed instead of your last hike with Apricot, and this could be hugely embarassing. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to recall the email with the video i made on the trails now. ",
                },
            ],
            reasoning="User John Quinn wants to recall an email. User isn't specific, but does mention trails. I see that user has just sent an email five minutes ago called Looking forward to our hike. Hiking can involve trails, so this lead looks promising. Digging deeper into this email, I see a video has been sent along with the email and the name of the video is LastHike. I shall confirm with user that this is the rdesired email and recall it if so. ",
            success_conditions=[
                {
                    "input_text": "The email Looking forward to our hike!\n25/07/2024, 17:45:00\nLastHike.mp4\nis recalled. \n",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "remove_email_or_thread",
            ],
            milestones=[
                # Milestone 0 – Agent looks for the email that must be recalled
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
                # Milestone 1 – Verify the targeted email (subject & attachment) appears in the search results
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
                                                "value": "Looking forward to our hike!",
                                                "partial": False,
                                            },
                                            # Only need to know the attachment list contains the filename
                                            "attachments": {
                                                "value": ["LastHike.mp4"],
                                                "partial": True,
                                            },
                                            "recipients_addresses": {
                                                "value": [
                                                    "apricot.sweeney@sfhealth.com"
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
                                "content": column_one_similarity,
                            },
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – The email has been successfully recalled / removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "subject": "Looking forward to our hike!",
                                    "sender_address": "john.quinn@palantir.com",
                                    "recipients_addresses": [
                                        ["apricot.sweeney@sfhealth.com"]
                                    ],
                                    "attachments": [["LastHike.mp4"]],
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "attachments": column_list_subset_match_similarity,
                                "subject": column_exact_match_similarity,
                                "sender_address": column_exact_match_similarity,
                            },
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # searched → verified correct email located
                (1, 2),  # located email → email removed / recalled
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_9f7d860a-08a2-4b41-aab3-1e5b83341f2a_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "contact",
                "calendar",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-03T12:20:00-07:00",
            is_read_time="2024-08-03T12:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to send a message to Apricot Sweeney and you also want to cancel the event Hiking with Apricot scheduled August 4 2024 from 09:00 to 12:00. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the event Hiking with Apricot tomorrow. Also text her saying 'In light of recent events, I think it's best to cancel the hike.'",
                },
            ],
            reasoning="The user wants to delete an event that they have explicitly named as Hiking with Apricot. That's scheduled for tomorrow morning. The user also wants to send a message to an unnamed person. It seems they are carrying on from the named event, which was scheduled to include Apricot Sweeney, so I'll presume this is the desired contact that the user wants to message. I'll send the message to Apricot Sweeney.",
            success_conditions=[
                {
                    "input_text": "1. Send a message to Apricot Sweeney saying 'In light of recent events, I think it's best to cancel the hike.'",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. Delete the calendar event Hiking with Apricot scheduled August 4 2024 from 09:00 to 12:00 is deleted.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_message",
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up calendar information (required to locate the hike event)
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
                # Milestone 1 – Verify that the event “Hiking with Apricot” on 2024-08-04 09:00 was found
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
                                                "value": "Hiking with Apricot",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-08-04T09:00:00-07:00",
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
                # Milestone 2 – The “Hiking with Apricot” event has been removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Hiking with Apricot",
                                    "start_datetime_iso": "2024-08-04T09:00:00-07:00",
                                    "end_datetime_iso": "2024-08-04T12:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare against the initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.MESSAGING],
                ),
                # Milestone 3 – A message was sent to Apricot containing the cancellation text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least one of Apricot’s identifiers (phone or email) must appear among the participants.
                                    "participants_addresses": [
                                        [
                                            (
                                                "415-555-0128",
                                                "apricot.sweeney@sfhealth.com",
                                            )
                                        ]
                                    ],
                                    "content": "In light of recent events, I think it's best to cancel the hike.",
                                    "creation_datetime_iso": "2024-08-03T12:20:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against the initial state
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
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_607a0c2a-f25d-46f5-80cb-c6791130edca_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_19",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-03T21:00:00-07:00",
            is_read_time="2024-08-03T21:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to text Apricot to make sure she is ready for the hike tomorrow "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a message to my girlfriend saying "Hey are you ready for our big hike tomorrow"',
                },
            ],
            reasoning='The user wants me to send a message to their girlfriend saying "Hey are you ready for our big hike tomorrow". I will look through their contacts to try and find someone listed as girlfriend. I did not find anyone with that name however I have found Apricot Sweeney listed as girlfriend in the user\'s contacts. I will draft the message with the given text and ask the user if it is ready to be sent.',
            success_conditions=[
                {
                    "input_text": '1. A new text message that says "Hey are you ready for our big hike tomorrow?" is sent to Apricot Sweeney',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up contacts to find girlfriend
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
                # Milestone 1 – The lookup result includes Apricot Sweeney
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
                                                "value": "Apricot Sweeney",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "415-555-0128",
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
                # Milestone 2 – A new outgoing text message is sent to Apricot with the expected content
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
                                                "415-555-0128",
                                                "apricot.sweeney@sfhealth.com",
                                            )
                                        ]
                                    ],
                                    "content": "Hey are you ready for our big hike tomorrow?",
                                    "creation_datetime_iso": "2024-08-03T21:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
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
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_607a0c2a-f25d-46f5-80cb-c6791130edca_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_19",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-03T21:00:00-07:00",
            is_read_time="2024-08-03T21:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to text Apricot to make sure she is ready for the hike tomorrow "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a message to Apricot saying "Hey are you ready for our big hike tomorrow"',
                },
            ],
            reasoning='The user wants me to send a message to Apricot saying "Hey are you ready for our big hike tomorrow". I will look through their contacts to try and find an Apricot. I have found Apricot Sweeney in the user\'s contacts. I will draft the message with the given text and ask the user if it is ready to be sent.',
            success_conditions=[
                {
                    "input_text": '1. A new text message that says "Hey are you ready for our big hike tomorrow?" is sent to Apricot Sweeney',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up Apricot’s contact info
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
                # Milestone 1 – Confirm Apricot Sweeney is in the retrieved contact results
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
                                                "value": "Apricot Sweeney",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "415-555-0128",
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
                # Milestone 2 – A new text message is sent to Apricot
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
                                                "415-555-0128",
                                                "apricot.sweeney@sfhealth.com",
                                            )
                                        ]
                                    ],
                                    "content": "Hey are you ready for our big hike tomorrow?",
                                    "creation_datetime_iso": "2024-08-03T21:00:00-07:00",
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
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → verify Apricot found
                (1, 2),  # Apricot found → message sent
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_9f7d860a-08a2-4b41-aab3-1e5b83341f2a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "contact",
                "calendar",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-03T12:20:00-07:00",
            is_read_time="2024-08-03T12:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to send a message to Apricot Sweeney and you also want to cancel the event Hiking with Apricot scheduled August 4 2024 from 09:00 to 12:00. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to Apricot saying 'In light of recent events, I think it's best to cancel the hike.' Also delete the hike tomorrow.",
                },
            ],
            reasoning="The user wants to send a message to Apricot. There's only one Apricot in contacts, Apricot Sweeney, so I'll send the message to them. The user now wants delete the hike tomorrow. I'll assume this is referring to a calendar event. Looking at tomorrow's schedule, I can see an event named Hiking with Apricot scheduled for 09:00. I'll delete that event.",
            success_conditions=[
                {
                    "input_text": "1. Send a message to Apricot Sweeney saying 'In light of recent events, I think it's best to cancel the hike.'",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. Delete the calendar event Hiking with Apricot scheduled August 4 2024 from 09:00 to 12:00 is deleted.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_message",
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up Apricot’s contact information
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
                # Milestone 1 – Confirms that Apricot Sweeney was returned from the contact-lookup in Milestone 0
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
                                                "value": "Apricot Sweeney",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "apricot.sweeney@sfhealth.com",
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
                # Milestone 2 – A new message was sent to Apricot containing the cancellation text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Participants must include Apricot (by either phone or email)
                                    "participants_addresses": [
                                        [
                                            (
                                                "apricot.sweeney@sfhealth.com",
                                                "415-555-0128",
                                            )
                                        ]
                                    ],
                                    "content": "cancel the hike",
                                    "creation_datetime_iso": "2024-08-03T12:20:00-07:00",
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
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
                # Milestone 3: search for calendars
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
                # Milestone 4 – Verify that the event “Hiking with Apricot” on 2024-08-04 09:00 was found
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
                                                "value": "Hiking with Apricot",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-08-04T09:00:00-07:00",
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
                        ),
                    ],
                ),
                # Milestone 5 – The “Hiking with Apricot” calendar event on Aug 4 2024 was removed (canceled)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Hiking with Apricot",
                                    "start_datetime_iso": "2024-08-04T09:00:00-07:00",
                                    "end_datetime_iso": "2024-08-04T12:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        ),
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (3, 4)],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_19_a0fbbb9c-0968-438b-bfae-7dc099cb06a8_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_19",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T15:25:00-07:00",
            is_read_time="2024-07-26T15:25:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You just can't wait until Sunday 4th August 2024 to see Apricot. . . .  You want to send her a message asking if she'd like to get dinner on Saturday or Sunday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you message my love Apricot with the message \"hello my bunny bear cutie pie, I can't stop thinking about how much I miss you. Do you think you have any free time to meet with me for dinner on Saturday or Sunday? Of course I'll treat my princess right... Let me know if you have free time. Lots of Love from your little cottage pie John\"",
                },
            ],
            reasoning="The user would like me to send a message to his love Apricot. I'm going to need to check the user's data to figure out who fits this relationship criteria.... I found Apricot Sweeney listed as the user's girlfriend, so this must be the person that the user wants to contact. With the user's confirmation, I'll send the message \"hello my bunny bear cutie pie, I can't stop thinking about how much I miss you. Do you think you have any free time to meet with me for dinner on Saturday or Sunday? Of course I'll treat my princess right... Let me know if you have free time. Lots of Love from your little cottage pie John\" to Apricot Sweeney.",
            success_conditions=[
                {
                    "input_text": "2. The message \"hello my bunny bear cutie pie, I can't stop thinking about how much I miss you. Do you think you have any free time to meet with me for dinner on Saturday or Sunday? Of course I'll treat my princess right... Let me know if you have free time. Lots of Love from your little cottage pie John\" to Apricot Sweeney.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up Apricot’s contact information
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
                # Milestone 1 – The returned contact list includes Apricot Sweeney
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
                                                "value": "Apricot Sweeney",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "415-555-0128",
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
                # Milestone 2 – A new outgoing message to Apricot containing the requested text is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require that both John and Apricot appear in the participant list
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9108",
                                                "john.quinn@palantir.com",
                                            ),
                                            (
                                                "415-555-0128",
                                                "apricot.sweeney@sfhealth.com",
                                            ),
                                        ]
                                    ],
                                    "content": "hello my bunny bear cutie pie",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-26T15:25:00-07:00",
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
    ]
