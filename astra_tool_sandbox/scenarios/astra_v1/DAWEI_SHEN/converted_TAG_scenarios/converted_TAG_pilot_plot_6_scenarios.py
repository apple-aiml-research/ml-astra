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


def get_TAG_DAWEI_SHEN_pilot_plot_6(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="DAWEI_SHEN_6_69971ad6-cf4a-4bb3-b2ff-eaec5ff58f0f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_6",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T21:30:00-08:00",
            is_read_time="2024-12-03T21:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to schedule an event to chat with your parents tomorrow. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Add an event to Wednesday 2024-12-04 at 18:00 - 19:00 pm named "Chat to Mom and Dad" with Yuting Tao and Hua Shen as attendees.',
                },
            ],
            reasoning="The user wants to add an event for tomorrow, 2024-12-04. I'll ask them for the event name, and then the event time. They asked for Mom and Dad to be added as attendees, I see Yuting Tao is user's mom and Hua Shen is user's dad. I have the event \"Chat to Mom and Dad\" with Yuting Tao and Hua Shen as attendees added for 2024-12-04 at 18:00 - 19:00 pm to the calendar.",
            success_conditions=[
                {
                    "input_text": 'An event is added to Wednesday 2024-12-04 at 18:00 - 19:00 pm named "Chat to Mom and Dad" with Yuting Tao and Hua Shen as attendees.',
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
                # Milestone 0 – A new calendar event with the correct details has been added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Chat to Mom and Dad",
                                    "start_datetime_iso": "2024-12-04T18:00",
                                    "end_datetime_iso": "2024-12-04T19:00",
                                    "attendees_names": [["Hua Shen", "Yuting Tao"]],
                                    "creation_datetime_iso": "2024-12-03T21:30:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_6_5b9d20fa-8a73-4084-8cce-4bc75667c3d8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_6",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_high",
                "calendar",
                "email",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T13:15:00-08:00",
            is_read_time="2024-12-05T13:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to block off the trip to Shanghai for the holidays in your calendar and also email this to your team lead in work, Kevin Chen. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you please mark the 20th December to the 5th January in my calendar as Christmas Holidays and email it to Kevin Chen",
                },
            ],
            reasoning="The user wants me to put 20th December 2024 to the 5th January 2025 in their calendar as Christmas Holidays. There are no conflicts in the calendar so I am able to add this without difficulty.\n\nThe user also asks me to email it to Kevin Chen. By it, I'm guessing that they must be referring to their newly scheduled event. This would make sense, because Kevin Chen is a coworker and is Dawei's team lead, so would benefit from knowing the user's holiday schedule. I will email this information, including a mention of \"Christmas Holidays\", to kevin.chen@orchardtech.com.",
            success_conditions=[
                {
                    "input_text": '1. The system will list December 20th 2024 to January 5th 2025 in the user\'s calendar as "Christmas Holidays".',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. Kevin Chen will be emailed Dawei\'s calendar schedule of  December 20th 2024 to January 5th 2025 being "Christmas Holidays".',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "create_calendar_event",
                "send_email",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – The holiday trip is entered into the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Christmas Holidays",
                                    "start_datetime_iso": "2024-12-20",  # only check the date portion
                                    "end_datetime_iso": "2025-01-05",
                                    "creation_datetime_iso": "2024-12-05T13:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.EMAIL],
                ),
                # Milestone 1 – The agent looks at the user’s contact
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
                # Milestone 2 – Kevin’s contact information was actually returned
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
                                                "value": "Kevin Chen",
                                                "partial": False,
                                            },
                                            "email": {
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
                            reference_milestone_node_index=1,  # parse the results of the search done in milestone 0
                        )
                    ],
                ),
                # Milestone 3 – An email is sent to Kevin Chen with the holiday schedule
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["kevin.chen@orchardtech.com"]
                                    ],
                                    "status": "sent",
                                    "body": "Christmas",  # ensure the holiday mention is present somewhere,
                                    "creation_datetime_iso": "2024-12-05T13:15:00-08:00",
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
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
            ],
            milestone_edge_list=[(0, 3), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_6_451ef2ce-21e2-4d60-816c-ef89e1c826bf_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_6",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "phone_call",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T20:40:00-08:00",
            is_read_time="2024-12-03T20:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know how long your video call with your parents was. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How long was my call with my father?",
                },
            ],
            reasoning="The user wants to know how long their call was with their father. I see in their contacts that Hua Shen is listed as father so I need to look for phone calls with him. I find one phone call with Hua Shen on the 3rd at 20:00. I tell the user the duration of the call. ",
            success_conditions=[
                {
                    "input_text": "1. A call with Hua Shen is searched for and returns the call on December 3rd at 20:00 with a duration of 30 minutes. ",
                    "statefullness": "Stateless",
                },
                {
                    "statefullness": "Stateless",
                    "input_text": "2. The duration of the call is given to the user. ",
                },
            ],
            tool_allow_list=[
                "search_phonecall_logs",
                "get_all_phone_calls",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent looks at the user’s contact
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
                # Milestone 1 – Hua Shen's contact information was actually returned
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
                                                "value": "Hua Shen",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "hua.shen@shenelectronics.cn",
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
                            reference_milestone_node_index=0,  # parse the results of the search done in milestone 0
                        )
                    ],
                ),
                # Milestone 2 – Agent inspects phone-call history (or all calls)
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
                        ),
                    ],
                ),
                # Milestone 3 – Returned result contains the 3-Dec-2024 20:00 call with Hua Shen
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
                                            # look for correct participant
                                            "caller_address": {
                                                "value": "+86 123-456-7890-1234",
                                                "partial": False,
                                            },
                                            # correct date & time
                                            "creation_datetime_iso": {
                                                "value": "2024-12-03T20:00",
                                                "partial": True,
                                            },
                                            "duration_in_hms": {
                                                "value": "00:30:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=2,  # parse tool outcome from milestone 2
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
                # Milestone 4 – User is told the call lasted 30 minutes
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
                                            "30 minutes",
                                            "30 min",
                                            "half an hour",
                                            "thirty minutes",
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
                (0, 1),  # Found HuaShen
                (2, 3),  # Phone-call search → verify call found
                (3, 4),  # Call found → inform user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_6_451ef2ce-21e2-4d60-816c-ef89e1c826bf_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_6",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "phone_call",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T20:40:00-08:00",
            is_read_time="2024-12-03T20:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know how long your video call with your parents was. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How long was my call with Hua Shen?",
                },
            ],
            reasoning="The user wants to know how long their phone call with Hua Shen was. The user only has one contact called Hua Shen so I search for a call with them. I find one phone call with Hua Shen on the 3rd at 20:00. I tell the user the duration of the call. ",
            success_conditions=[
                {
                    "input_text": "1. A call with Hua Shen is searched for and returns the call on December 3rd at 20:00 with a duration of 30 minutes. ",
                    "statefullness": "Stateless",
                },
                {
                    "statefullness": "Stateless",
                    "input_text": "2. The duration of the call is given to the user. ",
                },
            ],
            tool_allow_list=[
                "search_phonecall_logs",
                "get_all_phone_calls",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent looks at the user’s contact
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
                # Milestone 1 – Hua Shen's contact information was actually returned
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
                                                "value": "Hua Shen",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "hua.shen@shenelectronics.cn",
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
                            reference_milestone_node_index=0,  # parse the results of the search done in milestone 0
                        )
                    ],
                ),
                # Milestone 2 – Phone-call log is queried
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
                # Milestone 3 – Returned result contains the 3-Dec-2024 20:00 call with Hua Shen
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
                                            # look for correct participant
                                            "caller_address": {
                                                "value": "+86 123-456-7890-1234",
                                                "partial": False,
                                            },
                                            # correct date & time
                                            "creation_datetime_iso": {
                                                "value": "2024-12-03T20:00",
                                                "partial": True,
                                            },
                                            "duration_in_hms": {
                                                "value": "00:30:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=2,  # parse tool outcome from milestone 2
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
                # Milestone 4 – User is told the call lasted 30 minutes (or equivalent phrasing)
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
                                            "30 minutes",
                                            "30 mins",
                                            "half an hour",
                                            "thirty minutes",
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
                (0, 1),  # Found HuaShen
                (2, 3),  # Phone-call search → verify call found
                (3, 4),  # Call found → inform user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_6_5b9d20fa-8a73-4084-8cce-4bc75667c3d8_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_6",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "calendar",
                "email",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T13:15:00-08:00",
            is_read_time="2024-12-05T13:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to block off the trip to Shanghai for the holidays in your calendar and also email this to your team lead in work. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Put the dates I'm going to Shanghai as Christmas Holidays and email it to my team lead",
                },
            ],
            reasoning="The user asked me to add the dates that they are visiting Shanghai down in their calendar as Christmas Holidays. They didn't specify when exactly their Christmas Holidays are. I'm going to need to check if the user mentions anything about Shanghai or Christmas Holidays in their messages or emails. \n\nAfter checking, I found an email talking about a trip to Shanghai sent on December 3rd 2024 at 21:00 addressed to the user's Mom and Dad. It mentions spending the holidays with them and says that Dawei will be arriving on December 20th 2024 and staying until January 5th 2025. These dates occur during the general Christmas celebratory period, so it is safe to assume that these are when the user will be celebrating as Christmas Holidays with their family. I am going to add 20th December 2024 to the 5th January to the calendar as \"Christmas Holidays\".\n\nThe user also asks me to email it to their team lead. By it, I'm guessing that they must be referring to their newly scheduled event. I am not fully sure who \"team lead\" would refer to. I'm going to check the user's personal information and I found that Kevin Chen is a team lead in the applied research department that Dawei works at. This must be the team lead that the user is hoping to inform of their holiday schedule. I will email this information to kevin.chen@orchardtech.com.",
            success_conditions=[
                {
                    "input_text": '1. The system will list December 20th 2024 to January 5th 2025 in the user\'s calendar as "Christmas Holidays".',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. Kevin Chen will be emailed Dawei\'s calendar schedule of  December 20th 2024 to January 5th 2025 being "Christmas Holidays".',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "create_calendar_event",
                "send_email",
                "search_contacts",
                "get_all_contacts",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – The agent looks at the user’s contact
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
                # Milestone 1 – Kevin’s contact information was actually returned
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
                                                "value": "Kevin Chen",
                                                "partial": False,
                                            },
                                            "email": {
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
                            reference_milestone_node_index=0,  # parse the results of the search done in milestone 0
                        )
                    ],
                ),
                # MISSING MILESTONE - Need a step to determine what dates the user means when they say "the trip to Shanghai"
                # Milestone 2 – The agent looks at the user’s email
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
                # Milestone 3 – Email with travel date found
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
                                                "value": "Visit Details for Shanghai Trip",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-03T21:00:00-08:00",
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
                            reference_milestone_node_index=2,  # parse the results of the search done in milestone 2
                        )
                    ],
                ),
                # Milestone 4 – A calendar event covering the holiday trip is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Christmas Holidays",
                                    "start_datetime_iso": "2024-12-20",
                                    "end_datetime_iso": "2025-01-05",
                                    "creation_datetime_iso": "2024-12-05T13:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial state
                        ),
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.EMAIL],
                ),
                # Milestone 5 – Kevin Chen is emailed the holiday schedule
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["kevin.chen@orchardtech.com"]
                                    ],
                                    "status": "sent",
                                    "body": "holiday",
                                    "creation_datetime_iso": "2024-12-05T13:15:00-08:00",
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
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # find kevin
                (2, 3),  # find exact date of travel
                (3, 4),  # add calendar details
                (1, 5),  # send message to Kevin with correct address
                (3, 5),  # send message to Kevin with correct dates
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_6_2df07031-0c7f-4362-bc9d-b6dad851dfe1_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_6",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T13:00:00-08:00",
            is_read_time="2024-12-07T13:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "you have promised your parents thats you will send them on your flight details for your trip to Shanghai later in the month and want to set a reminder to do so. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set up an event with my parents called Flight Details for Shanghai next Saturday, the whole day I mean. ",
                },
            ],
            reasoning="The user wants to set up an event with their family called Flight Details for Shanghai next Saturday for the whole day. As I was given the name that is already decided. From conversations on the device I can see that the mentioned flight details were talked about with the users parents Yuting Tao and Hua Shen. As they want the event to involve their family I assume that having their parents as invitees would work. As they want this to serve as a reminder and forwarding the details should be a quick job I will make the event all day so it is clearly visible and permeates the users schedule that day. and the day selected is next Saturday being the 14th of December. I will now create An event called 'flight details for Shanghai' with Yuting Tao and Hua Shen as invitees all day on 14th of December 2024",
            success_conditions=[
                {
                    "input_text": "1. An event is created called 'flight details for Shanghai' with Yuting Tao and Hua Shen as invitees all day on 14th of December 2024",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – the agent looks up parents in contacts
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
                # M1: find Hua Shen
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
                                                "value": "Hua Shen",
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
                            reference_milestone_node_index=0,  # parse the results of the search done in milestone 0
                        )
                    ],
                ),
                # Milestone 2 – the agent looks up parents in contacts
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
                # M3: find Yuting Tao
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
                                                "value": "Yuting Tao",
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
                            reference_milestone_node_index=2,  # parse the results of the search done in milestone 0
                        )
                    ],
                ),
                # Milestone 4 – calendar event “flight details for Shanghai” is created for 14 Dec 2024 with both parents invited
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "flight details",
                                    "start_datetime_iso": "2024-12-14T00:",  # substring match is fine
                                    "end_datetime_iso": "2024-12-14T23:",  # substring match is fine
                                    "attendees_names": [["Hua Shen", "Yuting Tao"]],
                                    "creation_datetime_iso": "2024-12-07T13:00:00-08:00",
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
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.MESSAGING,
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (2, 3)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_6_2df07031-0c7f-4362-bc9d-b6dad851dfe1_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_6",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T13:00:00-08:00",
            is_read_time="2024-12-07T13:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "you have promised your parents thats you will send them on your flight details for your trip to Shanghai two days before the flight and want to set a reminder to do so. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Create an event with mom and dad to share flight details two days before my arrival around 9pm. ",
                },
            ],
            reasoning="The user wants to create an event to remind them to send their mom and dad their flight details two days before his arrival around 9pm. The user has mentioned flight details. From info on their device it seems they are talking about their itinerary for their flight to Shanghai at the end of the month from December 20th. This leads me to the name of the event as I can call it Flight Details for Shanghai so the user knows exactly what the event is for. Two days before the flight which should be on December 18th at 9pm. I believe mom and dad refers to Yuting Tao and Hua Shen respectively from the users contacts. I can list them as invitees to help remember who the details are for. I will now create An event called 'flight details for Shanghai' with Yuting Tao and Hua Shen as invitees on 18th of December 2024 at 9pm",
            success_conditions=[
                {
                    "input_text": "1. A Calendar event is created called 'flight details for Shanghai' or similar with Yuting Tao and Hua Shen as invitees at 9:00 pm on 18th of December 2024",
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
                "search_emails",
                "get_all_emails",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – the agent looks up parents in contacts
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
                # M1: find Hua Shen
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
                                                "value": "Hua Shen",
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
                            reference_milestone_node_index=0,  # parse the results of the search done in milestone 0
                        )
                    ],
                ),
                # Milestone 2 – the agent looks up parents in contacts
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
                # M3: find Yuting Tao
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
                                                "value": "Yuting Tao",
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
                            reference_milestone_node_index=2,  # parse the results of the search done in milestone 0
                        )
                    ],
                ),
                # milesone 4: search for trip details
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
                                        "search_emails",
                                        "get_all_emails",
                                    ],
                                )
                            },
                        )
                    ]
                ),
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
                                                "value": "Visit Details for Shanghai Trip",
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
                            reference_milestone_node_index=4,  # or wherever the tool call happens
                        )
                    ]
                ),
                # Milestone 6 – calendar event “flight details for Shanghai” is created for 18 Dec 2024 with both parents invited
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "flight details",
                                    "start_datetime_iso": "2024-12-18",  # substring match is fine
                                    "attendees_names": [["Hua Shen", "Yuting Tao"]],
                                    "creation_datetime_iso": "2024-12-07T13:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
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
                        DatabaseNamespace.MESSAGING,
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (2, 3), (4, 5)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_6_fa4e55ee-2230-403f-8ade-d57572b3414d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_6",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T16:25:00-08:00",
            is_read_time="2024-12-10T16:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know if either of your parents have emailed you a response about anything special they'd like to do during your upcoming trip to Shanghai. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "My email last week about my Shanghai trip, any reply from them? Yes or No.",
                },
            ],
            reasoning="The user has inquired as to whether there is any reply \"from them\" to their email last week about their Shanghai trip. First I'll need to find the email they're referring to.\n\nI found one email the user sent last week on December 3rd 2024 at 21:00 with the subject line Visit Details for Shanghai Trip, to recipients Hua Shen and Yuting Tao. In the body of the email, the user mentions \"my upcoming trip to Shanghai,\" so I will assume this is the email to which they are referring.\n\nNext, I'll need to determine who the user meant by \"them.\" The recipients of the email the user sent are Hua Shen and Yuting Tao. It makes sense that these are the people from whom the user would be expecting a reply.\n\nFinally, I'll check the user's Mail inbox to see if there are any emails from Hua Shen or Yuting Tao since December 3rd 2024 at 21:00. I didn't find any emails from either contact within this time frame.\n\nGreat, now I can go ahead and let the user know that they have not yet received an email reply from Hua Shen or Yuting Tao to the email they sent regarding their upcoming trip to Shanghai.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The user is informed that they have not received an email response from Hua Shen or Yuting Tao.",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – The agent looks through the mailbox to determine if any replies exist
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
                # Milestone 1 – Email with travel date found
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
                                                "value": "Visit Details for Shanghai Trip",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-03T21:00:00-08:00",
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
                            reference_milestone_node_index=0,  # parse the results of the search done in milestone 0
                        )
                    ],
                ),
                # Milestone 2 – The user is informed that no reply from parents was found
                Milestone(
                    snapshot_constraints=[
                        # Check that the agent's final response mentions there is no reply
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
                                "content": column_word_contains_similarity,
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # searching the emails,
                (1, 2),  # the agent informs the user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_6_462715c0-1412-46cb-b069-140df3ae9b2b_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_6",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "email",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-04T18:00:00-08:00",
            is_read_time="2024-12-04T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to check if your parents have replied to your email you sent to them yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did Mom or Dad reply to my email since last night? Yes or No.",
                },
            ],
            reasoning="The user wants to know if either parent has replied to the email they sent last night (2024-12-03 21:00). I look up the parents’ contact entries (Hua Shen and Yuting Tao) to get their email addresses, then search the mailbox for any messages FROM either address with a received-time later than 2024-12-03T21:00:00-08:00. No such emails appear—only the user’s own original message (“Visit Details for Shanghai Trip”, sent at 21:00) is found—so I tell the user that neither parent has replied yet (answer: “No”).",
            success_conditions=[
                {
                    "input_text": 'The assistant replies that neither parent has replied (answering "No" or similar).',
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
                # Milestone 0 – the agent looks up parents in contacts
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
                # M1: find Hua Shen
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
                                                "value": "Hua Shen",
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
                            reference_milestone_node_index=0,  # parse the results of the search done in milestone 0
                        )
                    ],
                ),
                # Milestone 2 – the agent looks up parents in contacts
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
                # M3: find Yuting Tao
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
                                                "value": "Yuting Tao",
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
                            reference_milestone_node_index=2,  # parse the results of the search done in milestone 0
                        )
                    ],
                ),
                # Milestone 4 – The agent looks through the mailbox to determine if any replies exist
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
                # Milestone 5 – Email with travel date found
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
                                                "value": "Visit Details for Shanghai Trip",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-03T21:00:00-08:00",
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
                            reference_milestone_node_index=4,  # parse the results of the search done in milestone 3
                        )
                    ],
                ),
                # Milestone 6 – The user is informed that no reply from parents was found
                Milestone(
                    snapshot_constraints=[
                        # Check that the agent's final response mentions there is no reply
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
                                "content": column_word_contains_similarity,
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Search contact dad
                (2, 3),  # search contact Mom
                (4, 5),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_6_8de16c53-dc65-45b7-86cb-b5ac971a336d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_6",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T21:35:00-08:00",
            is_read_time="2024-12-03T21:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know the strategy meeting time so you can schedule in an 1-hour long dentist appointment for that day. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "At what time does my strategy meeting preparation begin, as I need to add a dentist appointment on the same day at 13:30.",
                },
            ],
            reasoning="Okay so, the user would like to know when 'Strategy Meeting Preparation' is scheduled for. I inform the user that it is scheduled for the 4th December at 15:00. Then I will add 'Dentist Appointment' for the 4th December at 13:30 to their calendar.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that the 'Strategy Meeting Preparation' is scheduled for the 4th December at 15:00.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. A dentist appointment is added for the 4th December at the time the user requests.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the meeting in the calendar
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
                # Milestone 1 – Returned result contains meeting
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
                                            # look for correct participant
                                            "calendar_event_name": {
                                                "value": "Strategy Meeting Preparation",
                                                "partial": False,
                                            },
                                            # correct date & time
                                            "start_datetime_iso": {
                                                "value": "2024-12-04T15:00:00-08:00",
                                                "partial": True,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,  # parse tool outcome from milestone 0
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
                # Milestone 2 – User is told when the meeting is
                Milestone(
                    snapshot_constraints=[
                        # time/date mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("15:00", "3:00", "3 pm", "3pm")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                    ],
                ),
                # Milestone 3 – Dentist appointment added to the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dentist",
                                    "start_datetime_iso": "2024-12-04T13:30:00",
                                    "creation_datetime_iso": "2024-12-03T21:35:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
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
            name="DAWEI_SHEN_6_462715c0-1412-46cb-b069-140df3ae9b2b_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_6",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-04T18:00:00-08:00",
            is_read_time="2024-12-04T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to check if your parents have replied to your email you sent to them yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I get a reply to the email I sent last night at 21:00? Yes or no.",
                },
            ],
            reasoning="The user is asking if they got a reply to an email they sent last night at 21:00. Yesterday was December 3rd 2024. I will check the emails sent at that time, find the single message, look for any replies from the user’s parents, and since there are none, tell the user there has been no reply.",
            success_conditions=[
                {
                    "input_text": 'The assistant answers that no reply has been received to the email sent at 21:00 on December 3 2024 (e.g., responds "No" or "Not yet").',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – The agent looks through the mailbox to determine if any replies exist
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
                # Milestone 1 – Email with travel date found
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
                                                "value": "Visit Details for Shanghai Trip",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-03T21:00:00-08:00",
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
                            reference_milestone_node_index=0,  # parse the results of the search done in milestone 3
                        )
                    ],
                ),
                # Milestone 2 – The user is informed that no reply from parents was found
                Milestone(
                    snapshot_constraints=[
                        # Check that the agent's final response mentions there is no reply
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
                                "content": column_word_contains_similarity,
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
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
                                "content": column_contains_similarity
                            },
                        ),
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_6_8de16c53-dc65-45b7-86cb-b5ac971a336d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_6",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T21:35:00-08:00",
            is_read_time="2024-12-03T21:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know the strategy meeting time so you can schedule in a dentist appointment for that day. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell me when tomorrow's strategy prep begins as I need to add a dentist appointment in for 13:30 for that day.",
                },
            ],
            reasoning="Right so, the user is looking for when tomorrow's strategy prep is and, after checking, I can see that there's an event named 'Strategy Meeting Preparation' scheduled for the 4th December at 15:00. This should be the event the user wishes to know about. I will announce the time of that event and then add an event named 'Dentist' for the 4th December at 13:30 in their calendar.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that the 'Strategy Meeting Preparation' is scheduled for the 4th December at 15:00.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. A 'Dentist' appointment is added for the 4th December at 13:30, as requested.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the meeting in the calendar
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
                # Milestone 1 – Returned result contains meeting
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
                                            # look for correct participant
                                            "calendar_event_name": {
                                                "value": "Strategy Meeting Preparation",
                                                "partial": False,
                                            },
                                            # correct date & time
                                            "start_datetime_iso": {
                                                "value": "2024-12-04T15:00:00-08:00",
                                                "partial": True,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,  # parse tool outcome from milestone 0
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
                # Milestone 2 – User is told when the meeting is
                Milestone(
                    snapshot_constraints=[
                        # meeting name mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Strategy Meeting Preparation",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # time/date mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("15:00", "3:00", "3 pm", "3pm")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
                # Milestone 3 – Dentist appointment added to the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dentist",
                                    "start_datetime_iso": "2024-12-04T13:30:00",
                                    "creation_datetime_iso": "2024-12-03T21:35:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
    ]
