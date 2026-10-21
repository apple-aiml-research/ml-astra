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
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
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


def get_TAG_EMILY_ROSE_pilot_plot_9(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="EMILY_ROSE_9_391405e7-058b-4d58-9875-646867d15e1a_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T08:00:00-08:00",
            is_read_time="2024-12-07T08:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You have fallen ill suddenly and can no longer attend the upcoming holiday party setup.   You wish to remove the event from your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the holiday party preparation event. ",
                },
            ],
            reasoning="The user wants to delete the holiday party preparation event. I should check their calendar for that event. I see no event with that exact event title. However I see one similar event, 'Holiday Party Setup with Nathan Blake', today, Saturday, December 7th at 11:00-14:00. It must be that one. I'll ask the user to confirm before deleting the event. ",
            success_conditions=[
                {
                    "input_text": "1. The event, 'Holiday Party Setup with Nathan Blake' on Saturday, December 7th, at 11:00-14:00, is deleted from the user's calendar. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the calendar to find the event to delete
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
                # Milestone 1 – Confirm the correct holiday-party setup event was returned in the search
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
                                                "value": "Holiday Party Setup with Nathan Blake",
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
                            reference_milestone_node_index=0,  # use the tool results from milestone 0
                        )
                    ],
                ),
                # Milestone 2 – Verify the event has been removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Holiday Party Setup with Nathan Blake",
                                    "start_datetime_iso": "2024-12-07T11:00:00-08:00",
                                    "end_datetime_iso": "2024-12-07T14:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
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
            name="EMILY_ROSE_9_9d3a7d7a-08c3-4394-8cc5-0469896042fd_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T19:40:00-08:00",
            is_read_time="2024-12-07T19:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to send an email to Nathan Blake to apologize for a small mix-up and thank him for his help. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Email Nathan Blake the following message; "My apologies, Nathan, it totally slipped my mind, and I think I entered your birth year wrong when I set up your details. Thank you so much for all your help, and I hope you can make it to the Community Holiday Party in two weeks. -Emily Rose."',
                },
            ],
            reasoning="Ok so the user wants to email a given message to Nathan Blake. First is the recipient which is given by the user. Next is the Mode of communication which is given by the user. Now I will email the Nathan Blake the user's given message. ",
            success_conditions=[
                {
                    "input_text": 'The email; "My apologies, Nathan, it totally slipped my mind, and I think I entered your birth year wrong when I set up your details. Thank you so much for all your help, and I hope you can make it to the Community Holiday Party in two weeks. -Emily Rose" is sent to event helper Nathan Blake. ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_email"],
            milestones=[
                # Milestone 0 – Agent looks up Nathan Blake’s contact information
                Milestone(
                    snapshot_constraints=[
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
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Verify Nathan Blake’s contact was included in the lookup results
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
                                                "value": "Nathan Blake",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "nathan.blake@eventpros.com",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": [RoleType.EXECUTION_ENVIRONMENT],
                                    "recipient": [RoleType.AGENT],
                                    "content": ["{matched}"],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – Email sent to Nathan Blake with appropriate content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["nathan.blake@eventpros.com"]
                                    ],
                                    "status": ["sent"],
                                    "body": ["birth year wrong"],
                                    "creation_datetime_iso": "2024-12-07T19:40:00-08:00",
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
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # contact lookup → confirmation of Nathan’s contact
                (1, 2),  # confirmed contact → email sent
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_9_3f9b88ad-48be-41d3-8c36-42c13613d9a9_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T12:00:00-08:00",
            is_read_time="2024-12-07T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You can't remember if you agreed to meet Nathan at the center or at a cafe, you want to check. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What is the location of my Holiday Party Setup with Nathan Blake?",
                },
            ],
            reasoning="The user is asking about the location of an event.\nI should check their calendar. I can see an exact match for the user's query. \nThe location of Holiday Party Setup with Nathan Blake scheduled for December 07 2024, 11:00-14:00 is currently set as Orchard County Community Center.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Location of Holiday Party Setup with Nathan Blake scheduled for December 07 2024, 11:00-14:00 is confirmed as Orchard County Community Center.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – the agent looks up calendar events
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
                # Milestone 1 – confirm the holiday setup event with correct location is present in the tool output
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
                                                "value": "Holiday Party Setup with Nathan Blake",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Orchard County Community Center",
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
                # Milestone 2 – agent informs the user of the correct location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Orchard County Community Center",
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
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_9_3f9b88ad-48be-41d3-8c36-42c13613d9a9_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T12:00:00-08:00",
            is_read_time="2024-12-07T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You can't remember if you agreed to meet Nathan at the center or at a cafe, you want to check. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where am I meeting the event specialist for the party this Saturday?",
                },
            ],
            reasoning="The user is asking about the location of an event.\nI should check their calendar. I cannot see an exact match for the user's query. \nI should attempt to identify who they are referring to. I can see that one person is tagged as an event specialist in the user's contacts, Nathan Blake.\nReturning to the calendar and searching on the specified day of the week, I can see a potential match, Holiday Party Setup with Nathan Blake.\nThe location of Holiday Party Setup with Nathan Blake scheduled for December 07 2024, 11:00-14:00 is currently set as Orchard County Community Center.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Location of Holiday Party Setup with Nathan Blake scheduled for December 07 2024, 11:00-14:00 is confirmed as Orchard County Community Center.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – Agent uses a calendar-related read tool
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
                # Milestone 1 – Returned calendar data includes the correct event & location
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
                                                "value": "Holiday Party Setup with Nathan Blake",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Orchard County Community Center",
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
                # Milestone 2 – Agent tells the user the meeting location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Orchard County Community Center",
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_9_9d3a7d7a-08c3-4394-8cc5-0469896042fd_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T19:40:00-08:00",
            is_read_time="2024-12-07T19:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to send an email to Nathan Blake to apologize for a small mix-up and thank him for his help. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send my event helper the following by electronic mail: My apologies, Nathan, it totally slipped my mind, and I think I entered your birth year wrong when I set up your details. Thank you so much for all your help, and I hope you can make it to the Community Holiday Party in two weeks. -Emily Rose",
                },
            ],
            reasoning="User Emily Rose wants to send what i'm fairly certain is an email. User has provided the contents for the email, and refers to the intended recipient as user's event helper. I don't see anyone in contacts with that exact title, but i see from the text of the message that the recipient's name is Nathan. I find a Nathan Blake in contacts. Contact Nathan Blake is listed as an event specialist and i see from earlier messages that user Emily Rose and contact Nathan Blake engaged in an email correspondence about event planning. I'm certain this is the recipient user intends and i shall drafft and address the email accordingly and show it to user for approval. ",
            success_conditions=[
                {
                    "input_text": 'The email; "My apologies, Nathan, it totally slipped my mind, and I think I entered your birth year wrong when I set up your details. Thank you so much for all your help, and I hope you can make it to the Community Holiday Party in two weeks. -Emily Rose" is sent to event helper Nathan Blake. ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_email"],
            milestones=[
                # Milestone 0 – Agent attempts to retrieve contact info (Nathan Blake) via a contacts-related tool
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
                # Milestone 1 – Confirm that Nathan Blake appears in the result of Milestone 0
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
                                                "value": "Nathan Blake",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "nathan.blake@eventpros.com",
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
                            reference_milestone_node_index=0,  # use the tool output from Milestone 0
                        )
                    ]
                ),
                # Milestone 2 – Verify that an email was sent to Nathan with the appropriate body content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["nathan.blake@eventpros.com"]
                                    ],
                                    "status": "sent",
                                    "body": "birth year wrong",  # key phrase from the user-provided body,
                                    "creation_datetime_iso": "2024-12-07T19:40:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "body": column_contains_similarity,  # relaxed match on body text,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial state
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
            name="EMILY_ROSE_9_391405e7-058b-4d58-9875-646867d15e1a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T08:00:00-08:00",
            is_read_time="2024-12-07T08:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You have fallen ill suddenly and can no longer attend the upcoming holiday party setup.   You wish to remove the event from your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the event Holiday Party Setup with Nathan Blake.",
                },
            ],
            reasoning="The user wants to delete the event Holiday Party Setup with Nathan Blake. I should check their calendar for that event. I see one event with that exact event title, 'Holiday Party Setup with Nathan Blake', today, Saturday, December 7th at 11:00-14:00. It must be that one. I'll ask the user to confirm before deleting the event. ",
            success_conditions=[
                {
                    "input_text": "1. The event, 'Holiday Party Setup with Nathan Blake' on Saturday, December 7th, at 11:00-14:00, is deleted from the user's calendar. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the calendar event
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
                # Milestone 1 – Confirm that the correct event was returned from the calendar search
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
                                                "value": "Holiday Party Setup with Nathan Blake",
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
                # Milestone 2 – Verify the event was removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Holiday Party Setup with Nathan Blake",
                                    "start_datetime_iso": "2024-12-07T11:00:00-08:00",
                                    "end_datetime_iso": "2024-12-07T14:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to the initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Event search → verification of correct result
                (1, 2),  # Verification → deletion confirmation
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_9_84de11d5-7dae-4d68-9b1d-c93ab2688e4d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T16:00:00-08:00",
            is_read_time="2024-12-16T16:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You feel you have been almost too ahead of planning as you have lost track of when things are happening.   You want to double check when the community holiday party is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is the holiday party on? I'm all in a tangle. ",
                },
            ],
            reasoning='Ok so the user wants to know when the holiday party is on. First I will establish which event the user is referring to. I will look for events that use the keyword \'holiday party\' or similar words. I have found the event "Community Holiday Party," which I assume is what they are referring to. I will now inform the user that the event "Community Holiday Party" takes place at 17:00-20:00 on 20 December 2024. ',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the event "Community Holiday Party" takes place at 17:00-20:00 on 20 December 2024. ',
                    "statefullness": "Stateless",
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
                    ]
                ),
                # Milestone 1 – Confirm the “Community Holiday Party” event was returned from the calendar search
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
                                                "value": "Community Holiday Party",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-20T17:00:00-08:00",
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
                # Milestone 2 – User is told the correct date and time range
                Milestone(
                    snapshot_constraints=[
                        # Date mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "December 20",
                                            "Dec 20",
                                            "20 December",
                                            "12/20",
                                            "12-20",
                                            "2024-12-20",
                                            "this Friday",
                                            "Friday the 20th",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        # Start-time mentioned (5 pm / 17:00)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("5:00", "5 pm", "5pm", "17:00")],
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
                (0, 1),  # Calendar lookup → verify event retrieved
                (1, 2),  # Event retrieved → user informed
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_9_bef5ff94-6e74-4d88-a552-aa615a5b8849_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T14:05:00-08:00",
            is_read_time="2024-12-07T14:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You have already forgotten if you mentioned to Nathan about uploading the photos to cloud, better check the email. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read out the email I sent at 14:00 today.",
                },
            ],
            reasoning="The user is asking me to read an email.\nFirst, I need to find the email they are referring to. The user has provided me with a date and time. I see an exact match for the user's query, received from December 7 2024 at 14:00. This must be what the user is referring to.\nI will read out the contents of this email for the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The most recent email to nathan.blake@eventpros.com is read out.",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – The agent uses an email-retrieval tool
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
                # Milestone 1 – The agent reads the correct email back to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "uploaded the photos",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,  # look for key phrase from email body
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
            name="EMILY_ROSE_9_a2cbc818-16a3-44f6-a3b3-13ad4528ec1a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T12:20:00-08:00",
            is_read_time="2024-12-16T12:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know who else is attending the community holiday party. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who's attending the holiday party on Friday?",
                },
            ],
            reasoning="Right so, the user wants to know who are the attendees to their 'holiday party on Friday'. From checking their calendar, I can see three events scheduled in for Friday, 20 December 2024. The user is specifically looking for a 'holiday party' and there is one event matching for that day named 'Community Holiday Party' which is scheduled from 17:00 to 20:00. This is the event the user is referring to and I can see that the attendees are 'Community Members, Event Volunteers and Nathan Blake'. I can then display this information to the user.",
            success_conditions=[
                {
                    "input_text": "1. The attendees, 'Community Members, Event Volunteers and Nathan Blake' are displayed to the user for the 'Community Holiday Party' scheduled for 20 December 2024 from 17:00 to 20:00. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent looks up the calendar to find the holiday party
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
                # Milestone 1 – Confirm the holiday party event was returned from the previous tool call
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
                                                "value": "Community Holiday Party",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-20T17:00:00-08:00",
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
                # Milestone 2 – Agent’s reply to the user includes the expected attendee names
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Community Members",
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
                                    "content": "Event Volunteers",
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
                                    "content": "Nathan Blake",
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
                (0, 1),  # Calendar lookup -> confirm event retrieved
                (1, 2),  # Event retrieved -> user informed
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_9_d6fa62ff-5189-4623-8f6b-d70ad04f4fa6_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_high",
                "calendar",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
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
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You are not feeling well so you need to cancel the event Holiday Party Setup with Nathan Blake and also you want to send a message to Nathan Blake to apologise. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the event Holiday Party Setup with Nathan Blake and text him saying 'so sorry Nathan, I'm sick today so I can't make it to the party setup.'",
                },
            ],
            reasoning="The user has explicitly stated the event that they would like to delete. They have made no reference to time or date so first of all I'll presume the event takes places today. Looking at the calendar, there is an event with this exact title. I'll delete that. \n\nNext the user wants to send a message. There is no mention of a name, however the message request directly following the request to delete an event that featured Nathan Blake. I think it's highly likely that this is who the user means to message. I'll send the message now.",
            success_conditions=[
                {
                    "input_text": "1. Delete the calendar event Holiday Party Setup with Nathan Blake scheduled for December 7 2024 from 11:00 to 14:00.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. Send a message to Nathan Blake saying 'So sorry Nathan, I'm sick today so I can't make it to the party setup.'",
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
                # Milestone 0 – Agent looks up upcoming calendar events
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
                # Milestone 1 – Confirms the correct holiday-setup event was surfaced
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
                                                "value": "Holiday Party Setup with Nathan Blake",
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
                    ],
                ),
                # Milestone 2 – The calendar event is removed (canceled)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Holiday Party Setup with Nathan Blake",
                                    "start_datetime_iso": "2024-12-07T11:00:00-08:00",
                                }
                            ),
                            # default similarity functions are sufficient here
                            reference_milestone_node_index=-1,  # compare to state before the task
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.MESSAGING,
                    ],
                ),
                # Milestone 3 – A text message is sent to Nathan Blake with an apology
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require Nathan to be one of the participants; allow either phone or email identifier
                                    "participants_addresses": [
                                        [
                                            (
                                                "+1 530-555-0129",
                                                "nathan.blake@eventpros.com",
                                            )
                                        ]
                                    ],
                                    "content": "sorry",  # key phrase that should appear,
                                    "creation_datetime_iso": "2024-12-07T10:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Ensure at least one of Nathan’s identifiers appears; allow extras (e.g., Emily)
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                # Loosely check that apology text is present
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_9_a2cbc818-16a3-44f6-a3b3-13ad4528ec1a_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T12:20:00-08:00",
            is_read_time="2024-12-16T12:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know who else is attending the community holiday party. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who's coming to the party in four days?",
                },
            ],
            reasoning="Okay, the user wants to know who is attending their 'party in four days'. From checking their calendar, I can see that in four days, which would be 20 December 2024, there is a matching event named 'Community Holiday Party' lasting from 17:00 to 20:00. This is the event the user is referring to and I can see that the attendees are 'Community Members, Event Volunteers and Nathan Blake'. I can then display this information to the user.",
            success_conditions=[
                {
                    "input_text": "1. The attendees, 'Community Members, Event Volunteers and Nathan Blake' are displayed to the user for the 'Community Holiday Party' scheduled for 20 December 2024 from 17:00 to 20:00. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent queries the calendar for upcoming events
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
                # Milestone 1 – Calendar query returns the Community Holiday Party with Nathan Blake listed
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
                                                "value": "Community Holiday Party",
                                                "partial": False,
                                            },
                                            # Ensure at least one attendee match (Nathan Blake)
                                            "attendees_names": {
                                                "value": ["Nathan Blake"],
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
                # Milestone 2 – Agent tells the user who is attending
                Milestone(
                    snapshot_constraints=[
                        # Must mention "Community Members"
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Community Members",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Must mention "Event Volunteers"
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Event Volunteers",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Must mention "Nathan Blake"
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Nathan Blake",
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
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_9_bef5ff94-6e74-4d88-a552-aa615a5b8849_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T14:05:00-08:00",
            is_read_time="2024-12-07T14:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You have already forgotten if you mentioned to Nathan about uploading the photos to cloud, better check the email. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to know what I already said just a few minutes ago to nathan.blake@eventpros.com.",
                },
            ],
            reasoning="User mentions an email address, I assume they'd like to send mail to this contact so I ask for the content. They correct em and say they'd actually like the message content to the mail they most recently sent to this contacts a few minutes ago. I find a message to this contact sent 5 minutes previously and so I read this to user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The most recent email to nathan.blake@eventpros.com is presented.",
                }
            ],
            tool_allow_list=["search_emails", "get_all_emails"],
            milestones=[
                # Milestone 0 – The agent queries the email store to locate the latest email to Nathan Blake
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
                # Milestone 1 – Returned email to Nathan
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
                                                "value": "Photos and Calendar Invite for Holiday Party",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-07T14:00:00",
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
                # Milestone 2 – The agent tells the user what was said (content from the located email)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "uploaded",  # key phrase from the email body
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "photos",  # key phrase from the email body
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_9_84de11d5-7dae-4d68-9b1d-c93ab2688e4d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T16:00:00-08:00",
            is_read_time="2024-12-16T16:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You feel you have been almost too ahead of planning as you have lost track of when things are happening.   You want to double check when the community holiday party is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'When is the event "Community Holiday Party?"',
                },
            ],
            reasoning='Ok so the user wants to know when the event "Community Holiday Party" is. First I will find the event in the calendar. I have found the event "Community Holiday Party." I will now inform the user that the event "Community Holiday Party" takes place at 17:00-20:00 on 20 December 2024. ',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the event "Community Holiday Party" takes place at 17:00-20:00 on 20 December 2024. ',
                    "statefullness": "Stateless",
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
                    ],
                ),
                # Milestone 1 – Returned tool output contains the Community Holiday Party event
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
                                                "value": "Community Holiday Party",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-20T17:00:00-08:00",
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
                # Milestone 2 – Agent informs the user with correct date and time
                Milestone(
                    snapshot_constraints=[
                        # Check the date appears
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "December 20",
                                            "20 December",
                                            "Dec 20",
                                            "Dec. 20",
                                            "2024-12-20",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        # Check the start time appears (either 17:00 or 5:00 PM variants)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "17:00",
                                            "5:00",
                                            "5 pm",
                                            "5 p.m.",
                                            "5pm",
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
                (0, 1),  # Need to find the event before verifying its presence
                (1, 2),  # Need the event details before responding to the user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_9_d9af3817-aba6-47c0-b342-e857650863f7_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T12:00:00-08:00",
            is_read_time="2024-12-08T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You realise that you forgot to ask about kosher options for the Community Holiday event.  .  .  .   You need to inform Nathan immediately and send him an urgent email to address this. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I need to email him again about the party planning write "Hey Nathan - I completely blindsided the kosher options for the party. What can we do to fix this?"',
                },
            ],
            reasoning='The user wants me to send a new email to "him" about the party planning and to write "Hey Nathan - I completely blindsided the kosher options for the party. What can we do to fix this?". I\'m not fully sure who I\'m meant to contact - but if I look at the requested user message content, it mentions the name Nathan. Is it possible that the user wants to send this to someone called Nathan? \n\nSearching the user\'s contacts, I found "Nathan Blake", who is listed as "Event Helper". It seems likely that this must be the correct person if the user wants to talk about more details for their party planning. \n\nI\'ll draft the message "Hey Nathan - I completely blindsided the kosher options for the party. What can we do to fix this?" to Nathan Blake and proceed to send with the user\'s confirmation.',
            success_conditions=[
                {
                    "input_text": '1. The email "Hey Nathan - I completely blindsided the kosher options for the party. What can we do to fix this?" is sent to Nathan Blake.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_email"],
            milestones=[
                # Milestone 0 – The agent looks up Nathan’s contact info
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
                # Milestone 1 – Confirm that Nathan Blake was found in the search results
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
                                                "value": "Nathan Blake",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "nathan.blake@eventpros.com",
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
                # Milestone 2 – The email to Nathan has been sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["nathan.blake@eventpros.com"]
                                    ],
                                    "status": "sent",
                                    "body": "kosher",
                                    "creation_datetime_iso": "2024-12-08T12:00:00-08:00",
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
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → confirmation of Nathan
                (1, 2),  # Confirmation of Nathan → email sent
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_9_11b4b967-db37-42e4-abc7-6df0ad54f2f3_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "calendar",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
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
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You are not feeling well so you need to cancel the event Holiday Party Setup with Nathan Blake and also you want to send a message to Nathan Blake to apologise. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the next event in my calendar and text him saying 'so sorry Nathan, I'm sick today so I can't make it to the party setup.'",
                },
            ],
            reasoning="The user wants to delete an event from the calendar. The request is made on December 07, 2024 at 10:05, so the 'next' event the user is referring to must be the \"Holiday Party Setup with Nathan Blake\" from 11:00 to 14:00. I'll delete the event.\n\nNext they would like to send a message to Nathan. There is only one Nathan in the contact list, Nathan Blake, so I'll send the message to him.",
            success_conditions=[
                {
                    "input_text": "1. Delete the calendar event Holiday Party Setup with Nathan Blake scheduled for December 7 2024 from 11:00 to 14:00.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. Send a message to Nathan Blake saying 'So sorry Nathan, I'm sick today so I can't make it to the party setup.'",
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
                # Milestone 0 – Agent looks up upcoming calendar events
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
                # Milestone 1 – Confirms the correct holiday-setup event was surfaced
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
                                                "value": "Holiday Party Setup with Nathan Blake",
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
                                    "calendar_event_name": "Holiday Party Setup with Nathan Blake",
                                    "start_datetime_iso": "2024-12-07T11:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.MESSAGING],
                ),
                # Milestone 3 – Agent looks up contact information (Nathan)
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
                # Milestone 4 – Confirms Nathan Blake contact details were found
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
                                                "value": "Nathan Blake",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 530-555-0129",
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
                # Milestone 5 – Message sent to Nathan with an apology
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
                                                "nathan.blake@eventpros.com",
                                                "+1 530-555-0129",
                                            )
                                        ]
                                    ],
                                    "content": "sorry",
                                    "creation_datetime_iso": "2024-12-07T10:05:00-08:00",
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
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar lookup → event identified
                (3, 4),  # Contact lookup → Nathan confirmed
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_9_11b4b967-db37-42e4-abc7-6df0ad54f2f3_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "calendar",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
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
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You are not feeling well so you need to cancel the event Holiday Party Setup with Nathan Blake and also you want to send a message to Nathan Blake to apologise. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the event coming up next with my event helper and text him saying 'so sorry Nathan, I'm sick today so I can't make it to the party setup.'",
                },
            ],
            reasoning="The user wants to cancel an event coming up next. The request is coming on December 07, 2024 at 10:05, so the next event must be the one named \"Holiday Party Setup with Nathan Blake\". Looking at the calendar, there is an event with this exact title. I'll delete that. \n\nNext the user wants to send a message to the user's 'event helper'. If I go through the contacts, I see the contact card 'Nathan Blake' tagged as Event Helper. I think it's highly likely that this is who the user means to message. I'll send the message now including the text 'so sorry Nathan, I'm sick today so I can't make it to the party setup.'",
            success_conditions=[
                {
                    "input_text": "1. Delete the calendar event Holiday Party Setup with Nathan Blake scheduled for December 7 2024 from 11:00 to 14:00.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. Send a message to Nathan Blake saying 'So sorry Nathan, I'm sick today so I can't make it to the party setup.'",
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
                # Milestone 0 – The agent looks up upcoming calendar events
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
                # Milestone 1 – Confirm the desired event was found in the tool output from Milestone 0
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
                                                "value": "Holiday Party Setup with Nathan Blake",
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
                # Milestone 2 – The agent retrieves Nathan Blake’s contact information
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
                # Milestone 3 – Confirm Nathan Blake was returned from the contact lookup in Milestone 2
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
                                                "value": "Nathan Blake",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 530-555-0129",
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
                    ],
                ),
                # Milestone 4 – Verify the calendar event was removed (canceled)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Holiday Party Setup with Nathan Blake",
                                    "start_datetime_iso": "2024-12-07T11:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
                # Milestone 5 – Verify a message was sent to Nathan with the apology text
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
                                                "nathan.blake@eventpros.com",
                                                "+1 530-555-0129",
                                            )
                                        ]
                                    ],
                                    "content": "sorry",
                                    "creation_datetime_iso": "2024-12-07T10:05:00-08:00",
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
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # calendar lookup → confirm event
                (2, 3),  # contact lookup → confirm contact
                (1, 4),  # after event identified → event removed
                (3, 5),  # after contact identified → message sent
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_9_d9af3817-aba6-47c0-b342-e857650863f7_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T12:00:00-08:00",
            is_read_time="2024-12-08T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You realise that you forgot to ask about kosher options for the Community Holiday event.  .  .  .   You need to inform Nathan immediately and send him an urgent email to address this. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Write an email to the event helper saying "Hey Nathan - I completely blindsided the kosher options for the party. What can we do to fix this?"',
                },
            ],
            reasoning='The user wants me to send a new email to "the event helper" and to write "Hey Nathan - I completely blindsided the kosher options for the party. What can we do to fix this?". I\'m not fully sure who I\'m meant to contact - but if I look at the requested user message content, it mentions the name Nathan. Is it possible that the user wants to send this to someone called Nathan? \n\nSearching the user\'s contacts, I found "Nathan Blake", who is listed as "Event Helper". It seems likely that this must be the correct person if the user wants to talk about more details for their party planning. \n\nI\'ll draft the message "Hey Nathan - I completely blindsided the kosher options for the party. What can we do to fix this?" to Nathan Blake and proceed to send with the user\'s confirmation.',
            success_conditions=[
                {
                    "input_text": '1. The email "Hey Nathan - I completely blindsided the kosher options for the party. What can we do to fix this?" is sent to Nathan Blake.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_email"],
            milestones=[
                # Milestone 0 – Agent searches contacts for Nathan (Event Helper)
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
                # Milestone 1 – Confirm the Nathan Blake contact was found in the previous tool output
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
                                                "value": "Nathan Blake",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "nathan.blake@eventpros.com",
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
                # Milestone 2 – Verify the email was sent to Nathan with the requested message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["nathan.blake@eventpros.com"]
                                    ],
                                    "status": "sent",
                                    "body": "kosher options",
                                    "creation_datetime_iso": "2024-12-08T12:00:00-08:00",
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
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_9_b2a01556-e208-4d13-a7ba-af0a0cbf6240_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T14:40:00-08:00",
            is_read_time="2024-12-07T14:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You cant remember what time you created the Community Holiday Party for  so you decide to ask "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When does the community holiday party start ",
                },
            ],
            reasoning="The user is asking when the community holiday party starts. I need to search through the calendar to see if any events match that name. I found an event named Community Holiday Party on December 20, 2024. That must be it. Now that I have found it I can retrieve the start time and let the user know",
            success_conditions=[
                {
                    "input_text": '1. The start time of the event "Community Holiday Party" on December 20, 2024 at 17:00-20:00 is presented to the user',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – A calendar-lookup tool is invoked
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
                # Milestone 1 – The returned calendar data contains the “Community Holiday Party”
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
                                                "value": "Community Holiday Party",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-20T17:00:00-08:00",
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
                # Milestone 2 – The agent tells the user the correct start time
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
                                            "5:00",
                                            "5pm",
                                            "5 pm",
                                            "5 p.m.",
                                            "17:00",
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
            name="EMILY_ROSE_9_20832c42-b14e-40a4-ab4c-2d7910f58faf_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T14:05:00-08:00",
            is_read_time="2024-12-07T14:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You have already forgotten if you mentioned to Nathan about uploading the photos to cloud, better check the email. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to go through the e-mail I sent to nathan.blake@eventpros.com just a few minutes ago, please read it to me. ",
                },
            ],
            reasoning="The user mentions an email address sent a few minutes ago, and the request from the user is coming on December 07, 2024, at 14:05. To be clear, I double check with the user, and they tell me the address of the email they want to go through. I select the email the user sent to Nathan Blake on December 07, 2024, at 14:05. The user asks me to 'read it' to them, I guess that pronoun is referring to the e-mail. I will read that e-mail to the user. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The most recent email to nathan.blake@eventpros.com is read out.",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – Agent uses an email-retrieval tool
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
                # Milestone 1 – The retrieved tool output contains the correct recent email to Nathan
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
                                                "value": "Photos and Calendar Invite for Holiday Party",
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
                # Milestone 2 – Agent reads the email content back to the user
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
                                            "I've uploaded the photos",
                                            "uploaded the photos",
                                            "photos we took",
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
                (0, 1),  # Tool call -> verify correct email located
                (1, 2),  # Email located -> agent reads content to user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_9_20832c42-b14e-40a4-ab4c-2d7910f58faf_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_9",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T14:05:00-08:00",
            is_read_time="2024-12-07T14:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You have already forgotten if you mentioned to Nathan about uploading the photos to cloud, better check the email. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read out the email I sent at five minutes ago. ",
                },
            ],
            reasoning="The user is asking me to read an email.\nFirst, I need to find the email they are referring to. The user has told me the email was sent five minutes ago. I see an exact match for the user's query, received from December 7 2024 at 14:00. This must be what the user is referring to, so the email the user wants me to read is the one sent to Nathan Blake on December 07, 2024, at 14:05. I will read out the contents of this email for the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The most recent email to nathan.blake@eventpros.com is read out.",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – The agent invokes an email-retrieval tool
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
                # Milestone 1 – The retrieved results include the most-recent email sent to Nathan Blake
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
                                            "recipients_addresses": {
                                                "value": ["nathan.blake@eventpros.com"],
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Photos and Calendar Invite for Holiday Party",
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
                # Milestone 2 – The agent reads the email back to the user (key phrase present)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "uploaded the photos",
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
                (0, 1),  # Email retrieval tool call → confirm correct email in results
                (1, 2),  # Email identified → agent reports contents to user
            ],
        ),
    ]
