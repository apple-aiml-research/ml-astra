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
    column_rouge_l_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_any_similarity,
    not_contains_presence_similarity,
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


def get_TAG_LUCAS_GARCIA_pilot_plot_1(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="LUCAS_GARCIA_1_eda1201c-1b0f-4ac5-9e27-7a72d6c099fc_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_1",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T15:15:00-08:00",
            is_read_time="2024-12-03T15:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know who attended the Afternoon Group Fitness Class yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who attended the 'Afternoon Group Fitness Class' yesterday apart from me?",
                },
            ],
            reasoning="The user wants to know who attended their event 'Afternoon Group Fitness Class' yesterday. I should check their Calendar for this event. \nLooks like there user means the Afternoon Group Fitness Class from 15:00-16:00 on the 3 December 2024. Next I will check the event details for the attendees. \nLooks like Jessica Lin, Olivia Clark, Alex Martin and Theo Appleseed attended. I will let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their event 'Afternoon Group Fitness Class' at Orchard County Fitness Center from 15:00- 16:00 on December 2nd was attended by Jessica Lin, Olivia Clark, Alex Martin and Theo Appleseed.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Calendar information retrieval
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
                # Milestone 1 – Verify the correct calendar event was returned
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
                                                "value": "Afternoon Group Fitness Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-02T15:00:00-08:00",
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
                # Milestone 2 – User is informed with the correct attendee names
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Jessica Lin",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Olivia Clark",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Alex Martin",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Theo Appleseed",
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
                (0, 1),  # Calendar search → confirm event
                (1, 2),  # Event confirmed → inform user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_1_c905864c-adfa-426c-bfcf-e913b5eb0a14_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_1",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T08:05:00-08:00",
            is_read_time="2024-12-02T08:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to clear your calendar for the day because you are not feeling well. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete all my events from today.",
                },
            ],
            reasoning='The user wants to clear events from their schedule. They have specified today, and I can see that they have a lot of events scheduled: "Morning Personal Training Session with Nathan" from 9:00-10:00, "Meeting with Jessica: Joint Fitness Workshop Planning" from 10:00-11:00, "Online Fitness Class with Megan" from 11:00-12:00, "Lunch Meeting with Dietitian Sarah" from 13:00-14:00, "Afternoon Group Fitness Class" from 15:00-16:00, "Evening Workout Session with Theo" from 18:00-19:00, and "Fitness Planning for Next 3 Months" from 19:00-19:30. I\'l delete them all now.',
            success_conditions=[
                {
                    "input_text": '1. The event "Morning Personal Training Session with Nathan" from 9:00-10:00 on 2 December 2024 is deleted.',
                    "statefullness": "Stateful",
                },
                {
                    "statefullness": "Stateful",
                    "input_text": '2. The event "Meeting with Jessica: Joint Fitness Workshop Planning" from 10:00-11:00 on 2 December 2024 is deleted.',
                },
                {
                    "statefullness": "Stateful",
                    "input_text": '3. The event "Online Fitness Class with Megan" from 11:00-12:00 on 2 December 2024 is deleted.',
                },
                {
                    "statefullness": "Stateful",
                    "input_text": '4. The event "Lunch Meeting with Dietitian Sarah" from 13:00-14:00 on 2 December 2024 is deleted.',
                },
                {
                    "statefullness": "Stateful",
                    "input_text": '5. The event "Afternoon Group Fitness Class" from 15:00-16:00 on 2 December 2024 is deleted.',
                },
                {
                    "statefullness": "Stateful",
                    "input_text": '6. The event "Evening Workout Session with Theo" from 18:00-19:00 on 2 December 2024 is deleted.',
                },
                {
                    "input_text": '7. The event "Fitness Planning for Next 3 Months" from 19:00-19:30 on 2 December 2024 is deleted.',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up today’s calendar events
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
                # Milestone 1 – All of the user’s events for 2024-12-02 are removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Morning Personal Training Session with Nathan",
                                    "start_datetime_iso": "2024-12-02T09:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        ),
                    ],
                ),
                # Milestone 2 – All of the user’s events for 2024-12-02 are removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Meeting with Jessica: Joint Fitness Workshop Planning",
                                    "start_datetime_iso": "2024-12-02T10:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        ),
                    ],
                ),
                # Milestone 3 – All of the user’s events for 2024-12-02 are removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Online Fitness Class with Megan",
                                    "start_datetime_iso": "2024-12-02T11:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        ),
                    ],
                ),
                # Milestone 4 – All of the user’s events for 2024-12-02 are removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Lunch Meeting with Dietitian Sarah",
                                    "start_datetime_iso": "2024-12-02T13:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        ),
                    ],
                ),
                # Milestone 5 – All of the user’s events for 2024-12-02 are removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Afternoon Group Fitness Class",
                                    "start_datetime_iso": "2024-12-02T15:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        ),
                    ],
                ),
                # Milestone 6 – All of the user’s events for 2024-12-02 are removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Evening Workout Session with Theo",
                                    "start_datetime_iso": "2024-12-02T18:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        ),
                    ],
                ),
                # Milestone 7 – All of the user’s events for 2024-12-02 are removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Fitness Planning for Next 3 Months",
                                    "start_datetime_iso": "2024-12-02T19:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        ),
                    ],
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_1_eda1201c-1b0f-4ac5-9e27-7a72d6c099fc_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_1",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T15:15:00-08:00",
            is_read_time="2024-12-03T15:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know who attended the Afternoon Group Fitness Class yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who else attended the event at 15:00 yesterday?",
                },
            ],
            reasoning="The user wants to know who attended the event at 15:00 yesterday. Let me look in Calendar for any events at that time. Today is the 3 December 2024 so yesterday was the 2 December 2024. \nThere is only one vent scheduled for 15:00 on this date, the Afternoon Group Fitness Class from 15:00-16:00 on the 3 December 2024. Next I will check the event details for the attendees. \nLooks like Jessica Lin, Olivia Clark, Alex Martin and Theo Appleseed attended. I will let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their event 'Afternoon Group Fitness Class' at Orchard County Fitness Center from 15:00- 16:00 on December 2nd was attended by Jessica Lin, Olivia Clark, Alex Martin and Theo Appleseed.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent queries the calendar to find yesterday’s 15:00 event
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
                # Milestone 1 – Confirm the correct event (Afternoon Group Fitness Class at 15:00) was found
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
                                                "value": "Afternoon Group Fitness Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-02T15:00:00-08:00",
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
                # Milestone 2 – User is informed with the correct attendee list
                Milestone(
                    snapshot_constraints=[
                        # Check each required attendee is mentioned in the agent's response
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Jessica Lin",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Olivia Clark",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Alex Martin",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Theo Appleseed",
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
            name="LUCAS_GARCIA_1_9d8ebc84-cf63-4179-8220-c4fbf225d5c4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_1",
                "contact",
                "email",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T07:15:00-08:00",
            is_read_time="2024-12-02T07:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to make sure Jessica Lin is still okay to attend the meeting scheduled for 10AM. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need help sending Jessica Lin an email that says Hi Jessica. Are you still okay for our meeting this morning?",
                },
            ],
            reasoning='The user wants to send an email and has provided me with all the necessary details. I will start by searching for the intended contact. The user has provided me with a full name, so this requires little work on my part. I have found a contact called "Jessica Lin". The user also provided me with the exact contents they want written in the email, so I will copy what they said and send it in an email to this contact. ',
            success_conditions=[
                {
                    "input_text": '1. An email is sent to Jessica Lin that says "Hi Jessica. Are you still okay for our meeting this morning?"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_email"],
            milestones=[
                # Milestone 0 – Agent looks up contact information (either by searching or listing all)
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
                # Milestone 1 – Confirm that Jessica Lin was returned from the contact-lookup tool
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
                                                "value": "Jessica Lin",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "jessica.lin@example.com",
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
                # Milestone 2 – A new email was sent to Jessica with the requested body content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["jessica.lin@example.com"]
                                    ],
                                    "status": "sent",
                                    "body": "Hi Jessica. Are you still okay for our meeting this morning?",
                                    "creation_datetime_iso": "2024-12-02T07:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                # Body just needs to contain the key sentence; allow for any additional text
                                "body": column_contains_similarity,
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
            name="LUCAS_GARCIA_1_9d8ebc84-cf63-4179-8220-c4fbf225d5c4_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_1",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T07:15:00-08:00",
            is_read_time="2024-12-02T07:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to make sure Jessica Lin is still okay to attend the meeting scheduled for 10AM. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need help sending my coworker an email that says Hi Jessica. Are you still okay for our meeting this morning?",
                },
            ],
            reasoning='The user wants to send an email and has provided me with all the necessary details. I will start by searching for the intended contact. The user has provided me with an alias, so this requires little work on my part. I have found a contact called "Jessica Lin" with this alias. The user also provided me with the exact contents they want written in the email, so I will copy what they said and send it in an email to this contact. ',
            success_conditions=[
                {
                    "input_text": '1. An email is sent to Jessica Lin that says "Hi Jessica. Are you still okay for our meeting this morning?"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_email"],
            milestones=[
                # Milestone 0 – Agent invokes a contact-lookup tool
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
                # Milestone 1 – The correct coworker (Jessica Lin) is returned from the contact search
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
                                                "value": "Jessica Lin",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "jessica.lin@example.com",
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
                # Milestone 2 – A new email is sent to Jessica with the requested body text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["jessica.lin@example.com"]
                                    ],
                                    "status": "sent",
                                    "body": "Hi Jessica. Are you still okay for our meeting this morning?",
                                    "creation_datetime_iso": "2024-12-02T07:15:00-08:00",
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
            name="LUCAS_GARCIA_1_4aad046d-5d87-4121-a63b-8acd135bd655_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_1",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T12:00:00-08:00",
            is_read_time="2024-12-02T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are worried that you have scheduled the Afternoon Group Fitness Class for the wrong time so you decide to check the time "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you tell me what time I scheduled the Group Fitness thing later",
                },
            ],
            reasoning='The user wants to know what time they scheduled their Group Fitness thing later for. First thing I need to do is look at the user\'s calendar and see if there are any events that match that name. Ok there were no exact matches but I did find one named "Afternoon Group Fitness Class" on December 02, 2024 at 15:00-16:00. This must be the event the user is referring to. Now that I have found it I can retrieve the time it is scheduled for and inform the user',
            success_conditions=[
                {
                    "input_text": '1. The time of the event "Afternoon Group Fitness Class" on December 02, 2024 at 15:00-16:00 is read to the user',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent looks up the calendar to find the event
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
                # Milestone 1 – Confirm the correct calendar event was returned by the search
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
                                        "calendar_event_name": {
                                            "value": "Afternoon Group Fitness Class",
                                            "partial": False,
                                        },
                                        "start_datetime_iso": {
                                            "value": "2024-12-02T15:00:00-08:00",
                                            "partial": False,
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
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
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
                                            "3:00",  # 3:00 format
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
            name="LUCAS_GARCIA_1_73c3f7c3-8d79-4887-99b7-51c2f2de7b1a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_1",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T08:05:00-08:00",
            is_read_time="2024-12-02T08:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You're not sure how long your first gym session today is, so you want to ask the assistant to check. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'How long is my event "morning personal training session with Nathan" today?',
                },
            ],
            reasoning="The user is asking about the duration of an event.\nFirst, I should find the event in the user's calendar. I see an exact match for the user's query, \"Morning Personal Training Session with Nathan\" scheduled for today at 09:00-10:00. The duration of this event is 1 hour. I should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Duration of Morning Personal Training Session with Nathan scheduled for 09:00-10:00 is confirmed as 1 hour.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Verify the agent looked up the calendar for the event
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
                # Milestone 1 – Verify the user was told the event lasts 1 hour (or equivalent wording)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("1 hour", "one hour", "60 minutes")],
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
                ),  # Calendar lookup precedes the final answer delivered to the user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_1_73c3f7c3-8d79-4887-99b7-51c2f2de7b1a_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_1",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T08:05:00-08:00",
            is_read_time="2024-12-02T08:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You're not sure how long your first gym session today is, so you want to ask the assistant to check. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How long is my first event today?",
                },
            ],
            reasoning="The user is asking about the duration of an event.\nFirst, I should find the event in the user's calendar. The user has indicated this is their first event scheduled today December 02, 2024. The first event today is Morning Personal Training Session with Nathan scheduled for today at 09:00-10:00. The duration of this event is 1 hour. I should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Duration of Morning Personal Training Session with Nathan scheduled for 09:00-10:00 is confirmed as 1 hour.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent looks up today’s calendar events
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
                # Milestone 1 – Confirm the correct first-event record was returned
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
                                                "value": "Morning Personal Training Session with Nathan",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-02T09:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-02T10:00:00-08:00",
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
                # Milestone 2 – Assistant tells the user the duration is 1 hour
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("1 hour", "one hour", "60 minutes")],
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
                (0, 1),  # Calendar lookup → verify correct event
                (1, 2),  # Event verified → respond to user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_1_4aad046d-5d87-4121-a63b-8acd135bd655_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_1",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T12:00:00-08:00",
            is_read_time="2024-12-02T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are worried that you have scheduled the Afternoon Group Fitness Class for the wrong time so you decide to check the time "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you tell me what time I scheduled the Afternoon Group Fitness Class for",
                },
            ],
            reasoning='The user wants to know what time they scheduled their Afternoon Group Fitness Class for. First thing I need to do is look at the user\'s calendar and see if there are any events that match that name. Ok I found one named "Afternoon Group Fitness Class" on December 02, 2024 at 15:00-16:00. This must be the event the user is referring to. Now that I have found it I can retrieve the time it is scheduled for and inform the user',
            success_conditions=[
                {
                    "input_text": '1. The time of the event "Afternoon Group Fitness Class" on December 02, 2024 at 15:00-16:00 is read to the user',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
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
                # Milestone 1 – Confirm the correct calendar event was found in Milestone 0
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
                                                "value": "Afternoon Group Fitness Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-02T15:00:00-08:00",
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
                                    "content": [
                                        (
                                            "3:00 pm",
                                            "3 pm",
                                            "3pm",
                                            "15:00",
                                            "3 p.m.",
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
                (0, 1),  # Calendar lookup → event confirmation
                (1, 2),  # Event confirmed → user informed
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_1_92dd306c-0b9d-423d-9283-0a410a93905a_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_1",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T13:30:00-08:00",
            is_read_time="2024-12-02T13:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want a quick reminder when the afternoon class is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'When does "Afternoon Group Fitness Class" start today?',
                },
            ],
            reasoning='Ok so the user wants to know when "Afternoon Group Fitness Class" starts today. First I will find the given event in the calendar. Now that I have found it I will check the start time.  I will now inform the user that the event "Afternoon Group Fitness Class" is scheduled to start at 15:00 on 2 December 2024. ',
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The user is informed that the event "Afternoon Group Fitness Class" is scheduled to start at 15:00 on 2 December 2024. ',
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent uses a calendar-related read tool to find the event
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
                # Milestone 1 – Confirm that the correct event was returned by the calendar search
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
                                                "value": "Afternoon Group Fitness Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-02T15:00:00-08:00",
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
                # Milestone 2 – Agent informs the user of the correct start time and date
                Milestone(
                    snapshot_constraints=[
                        # Check that the reply contains the correct time
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "15:00",
                                            "3:00 pm",
                                            "3 pm",
                                            "3 p.m.",
                                            "3pm",
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
                (0, 1),  # Calendar search → verify event
                (1, 2),  # Event found → reply to user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_1_50703c11-37d4-4901-ab80-dd86ed294a66_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_1",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T07:15:00-08:00",
            is_read_time="2024-12-02T07:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You need to mentally prepare for the day so  want to know how many meetings you have. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How many meetings today that are not workouts or fitness classes? Return the number only.",
                },
            ],
            reasoning="The user wants to know how many meeting they have today. I should check their Calendar for any meetings today. \nHmm, looks like there is only 3 meetings today, the Meeting with Jessica: Joint Fitness Workshop Planning from 10:00-11:00 on the 2 December 2024 and Lunch Meeting with Dietitian Sarah from 13:00-14:00 on 2 December 2024, and Fitness Planning for Next 3 Months with Theo at 7pm. All other events like 'Evening Workout Session with Theo', 'Afternoon Group Fitness Class' and 'Online Fitness Class with Megan' are not meeting related \nI will let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. The user is informed they have 3 meetings today: Meeting with Jessica: Joint Fitness Workshop Planning from 10:00-11:00, Lunch Meeting with Dietitian Sarah from 13:00-14:00, and Fitness Planning for Next 3 Months from 19:00-19:30 on 2 December 2024. ",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The workout and fitness class events are not listed or counted among the meetings.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent looks up today’s calendar events
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
                # Milestone 1 – Calendar output includes the Jessica planning meeting
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
                                                "value": "Meeting with Jessica: Joint Fitness Workshop Planning",
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
                # Milestone 2 – Agent looks up today’s calendar events
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
                # Milestone 3 – Calendar output includes the lunch meeting with Sarah
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
                                                "value": "Lunch Meeting with Dietitian Sarah",
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
                # Milestone 4 – Agent looks up today’s calendar events
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
                # Milestone 5 – Calendar output includes the  planning session with Theo
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
                                                "value": "Fitness Planning for Next 3 Months",
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
                            reference_milestone_node_index=4,
                        )
                    ]
                ),
                # Milestone 6 – Agent tells the user they have two meetings and names them
                Milestone(
                    snapshot_constraints=[
                        # States there are 2 meetings (numeric or word)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("3", "three")],
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
                (0, 1),  # calendar search -> confirm Jessica event returned
                (2, 3),  # calendar search -> confirm Sarah event returned
                (4, 5),  # Fitness Planning for Next 3 Months returned
            ],
            minefields=[
                # Should not return the other meetings
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
                                            "Evening Workout Session with Theo",
                                            "Afternoon Group Fitness Class",
                                            "Online Fitness Class with Megan",
                                            "Morning Personal Training Session with Nathan",
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
        ScenarioExtension(
            name="LUCAS_GARCIA_1_da3c51e1-0d26-4034-b8bb-cc0135b29a64_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_1",
                "calendar",
                "contact",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T08:20:00-08:00",
            is_read_time="2024-12-02T08:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know when is your lunch with Sarah. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is my lunch with Sarah later?",
                },
            ],
            reasoning="Right so, the user is looking for when their lunch with a contact named 'Sarah' is. Firstly, looking at their contacts I see only one match, 'Sarah Lopez'. \n\nNext, checking their calendar, I can see one matching event with 'Sarah Lopez' for today, 2 December 2024, taking place from 13:00 to 14:00 titled 'Lunch Meeting with Dietitian Sarah'. 'Sarah Lopez' is listed as an attendee. This is the event the user is requesting so I can read out the timing details to them.",
            success_conditions=[
                {
                    "input_text": "1. The date and time details of 'Lunch Meeting with Dietitian Sarah' scheduled from 13:00 to 14:00 on 2 December 2024 with 'Sarah Lopez' listed as an attendee, is read out to the user.",
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
                # Milestone 0 – The agent looks through the calendar to locate the lunch with Sarah
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
                # Milestone 1 – Verify that the calendar tool output contained the expected lunch event
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
                                                "value": "Lunch Meeting with Dietitian Sarah",
                                                "partial": False,
                                            },
                                            "attendees_names": {
                                                "value": ["Sarah Lopez"],
                                                "partial": True,  # only need to see Sarah in the list
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
                # Milestone 2 – The agent tells the user the correct time of the lunch
                Milestone(
                    snapshot_constraints=[
                        # Check the reply contains the time (any reasonable phrasing) …
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "1:00 pm",
                                            "1 pm",
                                            "1pm",
                                            "13:00",
                                            "1:00 pm",  # non-breaking space variant
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
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_1_0c2b75f0-fa18-4c48-a64c-1030d1ebe537_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_1",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T08:05:00-08:00",
            is_read_time="2024-12-02T08:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to schedule a short reflection session at the end of a busy day."
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Schedule time for reflection later at 6 pm for half an hour for me",
                },
            ],
            reasoning="The user wants to block 30 minutes at 6 p.m. today for reflection. Since they said 'for me,' the event should include only the user. I'll create an event which title contains keyword 'Reflection' from 6:00 p.m. to 6:30 p.m.",
            success_conditions=[
                {
                    "input_text": '1. A new event with title contains "Reflection" is scheduled for 2024-12-02T18:00:00 - 2024-12-02T18:30:00 in the user\'s calendar ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["create_calendar_event"],
            milestones=[
                # Milestone 0 – A new calendar event is added for 6:00 pm–6:30 pm and includes Lucas
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Reflection",
                                    "start_datetime_iso": "2024-12-02T18:00",  # substring match → 6:00 pm
                                    "end_datetime_iso": "2024-12-02T18:30",  # substring match → 6:30 pm
                                    "attendees_names": [["Lucas Garcia"]],
                                    "creation_datetime_iso": "2024-12-02T08:05:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_1_eccd80da-9e2f-4006-b4b8-3029f207ae6a_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_1",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T08:15:00-08:00",
            is_read_time="2024-12-02T08:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to remove the training session with Nathan from your calendar because you need more sleep. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the training with Nathan. ",
                },
            ],
            reasoning="The user wants to delete the training with Nathan. I need to figure out which event the user means. I should check the user's Calendar. \nHmm, looks like only one event that matches this description, the Morning Personal Training Session with Nathan from 09:00-10:00 on the 2 December 2024.\nI will delete this event and let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. Morning Personal Training Session with Nathan from 09:00-10:00 on the 2 December 2024 is deleted. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the calendar to locate the event
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
                # Milestone 1 – The training session with Nathan has been removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Morning Personal Training Session with Nathan",
                                    "start_datetime_iso": "2024-12-02T09:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_rouge_l_similarity,
                                "start_datetime_iso": column_contains_similarity,
                            },
                            reference_milestone_node_index=-1,  # compare to initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar lookup precedes deletion verification
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_1_eccd80da-9e2f-4006-b4b8-3029f207ae6a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_1",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T08:15:00-08:00",
            is_read_time="2024-12-02T08:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to remove the training session with Nathan from your calendar because you need more sleep. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Get rid of the first event today; I'm just too tired. ",
                },
            ],
            reasoning="The user wants to get rid of their first event today. I need to figure out which event they mean. \nI know today is the 2 December 2024 so I should check Calendar for any events on that day. Hmm, looks like the user has multiple events today, I need to figure out which event they want. \nThey specified they want the first event today and looking at their Calendar that is the Morning Personal Training Session with Nathan from 09:00-10:00.\nI will delete this event and let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. Morning Personal Training Session with Nathan from 09:00-10:00 on the 2 December 2024 is deleted. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent tries to look up today’s calendar events
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
                # Milestone 1 – The retrieved event is the training session with Nathan at 09:00
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
                                                "value": "Morning Personal Training Session with Nathan",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
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
                                "content": column_one_similarity,
                            },
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
                # Milestone 2 – The event is removed from the calendar database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Morning Personal Training Session with Nathan",
                                    "start_datetime_iso": "2024-12-02T09:00:00-08:00",
                                    "end_datetime_iso": "2024-12-02T10:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # event retrieval → confirmation of correct event
                (1, 2),  # confirmation → removal of the event
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_1_da3c51e1-0d26-4034-b8bb-cc0135b29a64_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_1",
                "calendar",
                "contact",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T08:20:00-08:00",
            is_read_time="2024-12-02T08:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know when is your lunch with Sarah. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is my lunch with my dietician taking place?",
                },
            ],
            reasoning="Okay so, the user is looking for the date and time for when their event 'lunch with my dietician' is taking place. Firstly, looking at the user's contacts, I cannot see any matches for 'dietician', but there is a match under the alias of 'Sarah Lopez' for 'Dietitian Consultant'. \n\nNow that I have found the desired contact, I can now check the user's calendar and see if there are any corresponding events. I can see one matching that is taking place today, 2 December 2024 from 13:00 to 14:00, titled 'Lunch Meeting with Dietitian Sarah'. 'Sarah Lopez' is listed as an attendee. Now that I have found the requested information, I can read out the timing details to the user.",
            success_conditions=[
                {
                    "input_text": "1. The date and time details of 'Lunch Meeting with Dietitian Sarah' scheduled from 13:00 to 14:00 on 2 December 2024 with 'Sarah Lopez' listed as an attendee, is read out to the user.",
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
                # Milestone 0 – Agent tries to locate the lunch meeting in the calendar
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
                # Milestone 1 – Verify the expected lunch meeting was returned from the calendar lookup
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
                                                "value": "Lunch Meeting with Dietitian Sarah",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-02T13:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-02T14:00:00-08:00",
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
                # Milestone 2 – Agent tells the user the correct date & time
                Milestone(
                    snapshot_constraints=[
                        # Check the date reference
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "December 2",
                                            "Dec 2",
                                            "2 December",
                                            "2024-12-02",
                                            "today",
                                            "this afternoon",
                                            "2024-12-02T13:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                        # Check the time reference
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("1:00", "1 pm", "1pm", "13:00")],
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
                (0, 1),  # Calendar lookup → confirmation of correct event data
                (1, 2),  # Event data found → user informed
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_1_50703c11-37d4-4901-ab80-dd86ed294a66_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_1",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T07:15:00-08:00",
            is_read_time="2024-12-02T07:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You need to mentally prepare for the day so  want to know how many meetings you have, not workout sessions. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What do I have scheduled for today, meeting-wise, not fitness classes? How many in total?",
                },
            ],
            reasoning="The user wants to know how many meeting they have today. I should check their Calendar for any meetings today. \nHmm, looks like there is only 3 meetings today, the Meeting with Jessica: Joint Fitness Workshop Planning from 10:00-11:00 on the 2 December 2024 and Lunch Meeting with Dietitian Sarah from 13:00-14:00 on 2 December 2024, and Fitness Planning for Next 3 Months with Theo at 7pm. All other events like 'Evening Workout Session with Theo', 'Afternoon Group Fitness Class' and 'Online Fitness Class with Megan' are not meeting related \nI will let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. The user is informed they have 3 meetings today: Meeting with Jessica: Joint Fitness Workshop Planning from 10:00-11:00, Lunch Meeting with Dietitian Sarah from 13:00-14:00, and Fitness Planning for Next 3 Months from 19:00-19:30 on 2 December 2024. ",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The workout and fitness class events are not listed or counted among the meetings.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent looks up today’s calendar events
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
                # Milestone 1 – Calendar output includes the Jessica planning meeting
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
                                                "value": "Meeting with Jessica: Joint Fitness Workshop Planning",
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
                # Milestone 2 – Agent looks up today’s calendar events
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
                # Milestone 3 – Calendar output includes the lunch meeting with Sarah
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
                                                "value": "Lunch Meeting with Dietitian Sarah",
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
                # Milestone 4 – Agent looks up today’s calendar events
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
                # Milestone 5 – Calendar output includes the  planning session with Theo
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
                                                "value": "Fitness Planning for Next 3 Months",
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
                            reference_milestone_node_index=4,
                        )
                    ]
                ),
                # Milestone 6 – Agent tells the user they have three meetings
                Milestone(
                    snapshot_constraints=[
                        # States there are 3 meetings (numeric or word)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("3", "three")],
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
                (0, 1),  # calendar search -> confirm Jessica event returned
                (2, 3),  # calendar search -> confirm Sarah event returned
                (4, 5),  # Fitness Planning for Next 3 Months returned
            ],
            minefields=[
                # Should not return the other meetings
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
                                            "Evening Workout Session with Theo",
                                            "Afternoon Group Fitness Class",
                                            "Online Fitness Class with Megan",
                                            "Morning Personal Training Session with Nathan",
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
        ScenarioExtension(
            name="LUCAS_GARCIA_1_92dd306c-0b9d-423d-9283-0a410a93905a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_1",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T13:30:00-08:00",
            is_read_time="2024-12-02T13:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want a quick reminder when the afternoon class is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When's my afternoon class start again?",
                },
            ],
            reasoning='Ok so the user wants to know when their afternoon class starts. First I will establish which event they are referring to. I will search for upcoming events with the key words Afternoon class or similar terms. I have found the event "Afternoon Group Fitness Class" which I believe is the event in question. Next I will look for the start time of this event. I will now inform the user that the event "Afternoon Group Fitness Class" is scheduled to start at 15:00 on 2 December 2024. ',
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The user is informed that the event "Afternoon Group Fitness Class" is scheduled to start at 15:00 on 2 December 2024. ',
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent queries the calendar to find the afternoon class
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
                # Milestone 1 – The retrieved calendar data contains the expected afternoon class event
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
                                                "value": "Afternoon Group Fitness Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-02T15:00:00-08:00",
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
                # Milestone 2 – The user is informed of the correct start time and date
                Milestone(
                    snapshot_constraints=[
                        # Contains the correct start time (allowing multiple common phrasings)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "15:00",
                                            "3:00",
                                            "3 pm",
                                            "3pm",
                                            "3 p.m.",
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
                (0, 1),  # Calendar queried ➜ event confirmed
                (1, 2),  # Event confirmed ➜ user informed
            ],
        ),
    ]
