# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
# Auto-generated scenario extensions
from functools import partial
from typing import Optional, cast

import polars as pl

from astra_tool_sandbox.common.evaluation import (
    Milestone,
    SnapshotConstraint,
    column_contains_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_any_similarity,
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


def get_TAG_LUCAS_GARCIA_challenging_scenarios(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="LUCAS_GARCIA_5_9aabdcbd-4798-42d8-9dca-51e93da93df5_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_5",
                "phone_call",
                "contact",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T13:05:00-08:00",
            is_read_time="2024-12-03T13:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are wondering what time you called your high school friend Emmanuel "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I call Emmanuel Gonzales ",
                },
            ],
            reasoning="The user wants to know when they sent their last call to Emmanuel Gonzales took place. First thing I need to do is search the user's call logs. Ok I found a call to Emmanuel Gonzales at 11:45 on December 03, 2024. But it was the incoming instead of outgoing. Ok now that I have that I will retrieve the time of the call and inform the user that the last call was from Emmanuel instead of outgoing, asn was on 11:45.",
            success_conditions=[
                {
                    "input_text": "1. The time of the incoming call from Emmanuel Gonzales on December 03, 2024 at 11:45 is presented to the user",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_phonecall_logs",
                "get_all_phone_calls",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looks up phone-call history
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
                                        "search_phonecall_logs",
                                        "get_all_phone_calls",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – The retrieved phone-call list contains the call with Emmanuel on 2024-12-03 11:45
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
                                            "caller_address": {
                                                "value": "+1 12345-6789-1000-1357",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-03T11:45:00-08:00",
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
                # Milestone 2 – Agent tells the user the correct call time
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
                                            "11:45",
                                            "11:45 am",
                                            "11:45am",
                                            "11:45 a.m.",
                                            "11:45 AM",
                                        )
                                    ],
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
                                            "incoming",
                                            "from",
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
            name="LUCAS_GARCIA_5_c408e47c-5b55-4320-9126-9b52561702c1_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_5",
                "calendar",
                "phone_call",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T11:05:00-08:00",
            is_read_time="2024-12-03T11:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You've forgotten where your lunch with Emmanuel is taking place this afternoon.\n "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where am I getting dinner with Emmanuel?",
                },
            ],
            reasoning="The user wants to know the location of a meal they're sharing with Emmanuel. They said it was dinner, but looking at their calendar the only upcoming event today is named \"Lunch with Emmanuel\" with Emmanuel Gonzales listed as an attendee scheduled for today, 3 December 2024 at 12:00-13:30. The user must have misremembered which meal they're going to get with Emmanuel. I'll tell them the location of the event, Orchard County Cafe.",
            success_conditions=[
                {
                    "input_text": "1. The location of 'Lunch with Emmanuel' event on December 3rd, 2024, at 12:00-13:30, is read out to the user as Orchard County Cafe",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – The agent uses calendar tools to look up the lunch/dinner with Emmanuel
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
                # Milestone 1 – Confirm the "Lunch with Emmanuel" event on 2024-12-03 12:00 exists and has the correct location
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
                                                "value": "Lunch with Emmanuel",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-03T12:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-03T13:30:00-08:00",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Orchard County Cafe",
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
                # Milestone 2 – The agent tells the user the correct location (Orchard County Cafe)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Only check that the response mentions the correct place
                                    "content": "Orchard County Cafe",
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
                (0, 1),  # Calendar lookup → confirm correct event and location
                (1, 2),  # Confirmed event/location → inform user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_5_c408e47c-5b55-4320-9126-9b52561702c1_single_turn_3",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_5",
                "calendar",
                "phone_call",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_yes",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T12:00:00-08:00",
            is_read_time="2024-12-03T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You had a phone call with Emmanuel earlier today where he picked a new place for your lunch this afternoon (he changed his mind about the cuisine), but you've forgotten where it is and want to be reminded.\n "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I had a call with Emmanuel earlier and he picked a new spot for our lunch since he changed his mind about the cuisine, but I've totally forgotten where. Can you remind me where we're meeting?",
                },
            ],
            reasoning="The user wants the new lunch spot Emmanuel proposed on their phone call. I check the phone-call logs: there is an incoming call from Emmanuel today at 11:45, but the log has no transcript of what was said, so it doesn't tell me the location. Their calendar still shows 'Lunch with Emmanuel' at Orchard County Cafe, but the user said Emmanuel changed his mind, so that location is out of date and not what they're asking for. I have no way to recover what was discussed on the call, so I'll tell the user that key information is missing to complete this task.",
            success_conditions=[
                {
                    "input_text": "1. The user is told that key information is missing to complete this task — the new lunch location Emmanuel proposed on the call cannot be determined (the call log has no transcript, and the calendar's Orchard County Cafe is the outdated plan).",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "search_phonecall_logs",
                "get_all_phone_calls",
            ],
            milestones=[
                # Milestone 0 – Agent uses phone call tools to look up the lunch event/location
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
                                        "search_phonecall_logs",
                                        "get_all_phone_calls",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – Insufficient info: the phone-call log has no lunch location, so the agent replies "No"
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
                                            "key information is missing",
                                            "not enough information",
                                            "don't have enough",
                                            "can't determine",
                                            "cannot determine",
                                            "unable to determine",
                                            "no record",
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
                (0, 1),  # phone log lookup → confirm correct event & location
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_6_d53b0e2c-858d-439d-8492-f4c45d7cb16e_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_6",
                "contact",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:40:00-08:00",
            is_read_time="2024-12-05T17:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know what time your lunch with your high school buddy was at yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When was my lunch with my high school buddy yesterday",
                },
            ],
            reasoning="The user asks when their lunch with their high-school buddy was 'yesterday' (Dec 4). The high-school buddy is Emmanuel Gonzales. Checking the calendar, there was no lunch yesterday — Dec 4's only event was the 'Beer Tasting Event with Carol' (17:00-19:00). The lunch with Emmanuel was actually the day before yesterday, on December 3 at 12:00. So the user's 'yesterday' premise is mistaken; I inform them there was no lunch yesterday and that their lunch with Emmanuel was on December 3 at 12:00.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that they did not have a lunch with a high school buddy yesterday; their event yesterday was the 'Beer Tasting Event with Carol' on December 4th 2024, which ran from 17:00 to 19:00.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The user is informed that their lunch with Emmanuel (their high school buddy) was actually on December 3rd 2024 at 12:00 PM.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent uses calendar tools to look up relevant events
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
                                # Allow either direct search or full listing of calendars
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
                # Milestone 1 – Confirm the actual 'Lunch with Emmanuel' event (Dec 3, 2024 at 12:00) was retrieved
                # This grounds that the agent found the real lunch date (the day before yesterday), not "yesterday".
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
                                                "value": "Lunch with Emmanuel",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-03T12:00:00-08:00",
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
                            reference_milestone_node_index=0,  # depends on the calendar lookup in Milestone 0
                        )
                    ]
                ),
                # Milestone 2 – User-facing response gives the corrected date of the lunch (Dec 3 / day before yesterday)
                # This is the misinformation signal: the agent must convey the lunch was NOT yesterday but on the 3rd.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Check the response gives the corrected date (the 3rd / day before
                                    # yesterday) — the misinformation signal that it was NOT yesterday.
                                    "content": [
                                        (
                                            "december 3",
                                            "dec 3",
                                            "12/3",
                                            "2024-12-03",
                                            "the 3rd",
                                            "3rd of December",
                                            "day before yesterday",
                                            "2024-12-03T12:00",
                                            "3 December",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity,
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar lookup → confirm correct event retrieved
                (1, 2),  # Correct event retrieved → respond to user with its time
            ],
        ),
    ]
