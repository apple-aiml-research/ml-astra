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
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_any_similarity,
    not_contains_presence_similarity,
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


def get_TAG_THEO_APPLESEED_pilot_plot_24(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="THEO_APPLESEED_24_7d1ca737-2a03-4cf2-9a9b-0a893601db5e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T09:00:00-07:00",
            is_read_time="2024-07-29T09:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send a message to Cookie Watson inviting her to your salsa dance classes. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to Cookie Watson saying 'Hey Cookie, I'm starting weekly salsa dance classes, you down to join? Tuesdays at seven thirty.'.",
                },
            ],
            reasoning="The user wants to send a message to Cookie Watson. I'll check the user's contacts for a contact under this name. There is a contact under that name so I'll pull up that number. Next the user has given me what they'd like to say. Now that I have the content of the message I can send 'Hey Cookie, I'm starting weekly salsa dance classes, you down to join? Tuesdays at seven thirty.' to Cookie and notify the user.",
            success_conditions=[
                {
                    "input_text": "1. A message to Cookie Watson is sent saying 'Hey Cookie, I'm starting weekly salsa dance classes, you down to join? Tuesdays at seven thirty.'.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 — The agent looks up Cookie Watson in the contacts
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
                # Milestone 1 — The preceding lookup returned Cookie Watson as a match
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
                                                "value": "Cookie Watson",
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
                            reference_milestone_node_index=0,  # depend on Milestone 0’s tool output
                        )
                    ],
                ),
                # Milestone 2 — A message to Cookie Watson was actually sent with the correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [
                                            # Ensure Cookie is one of the participants.
                                            (
                                                "1234-5678-9107",
                                                "cookie.watson@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "salsa dance classes",
                                    "creation_datetime_iso": "2024-07-29T09:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # Require Cookie to be among the participants; allow other participants such as Theo/self.
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                # Just ensure the main text is included; slight re-phrasing is acceptable
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                    # No guardrail exclusion necessary; only MESSAGING addition is expected
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_077155a2-772e-45dd-8eaa-8852ea0b73ed_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-31T16:30:00-07:00",
            is_read_time="2024-07-31T16:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what time your salsa class starts tonight. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time does dance start tonight?",
                },
            ],
            reasoning='The user wants to know what time "dance" starts tonight. \n\nOkay, firstly, I need to view the user\'s Calendar to see if they have any events that match this description.\n\nGreat, okay, so I see that they have tonight named "Salsa Dance Class", from 19:30 - 20:30. \n\nI will now inform the user of the start time of this event. ',
            success_conditions=[
                {
                    "input_text": '1. The start time of the event named "Salsa Dance Class" is presented to the user: 19:30:00, July 31st, 2024. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent queries the calendar to find tonight's dance event
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
                # Milestone 1 – Verify the returned calendar entry is the Salsa Dance Class at 19:30
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
                                                "value": "Salsa Dance Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-31T19:30:00-07:00",
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
                # Milestone 2 – Agent tells the user the correct start time (7:30 pm / 19:30)
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
                                            "19:30",
                                            "7:30",
                                            "7:30pm",
                                            "7:30 pm",
                                            "19:30 pm",
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
            name="THEO_APPLESEED_24_077155a2-772e-45dd-8eaa-8852ea0b73ed_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-31T16:30:00-07:00",
            is_read_time="2024-07-31T16:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what time your salsa class starts tonight. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time do I get my jig on tonight?",
                },
            ],
            reasoning='The user wants to know what time they get their "jig on" tonight.\n\nOkay, firstly, I need to view the user\'s Calendar to see if they have any events that match this description.\n\nOkay, so there aren\'t any events that exactly match this description. \n\nHowever, they do have one event tonight named "Salsa Dance Class", from 19:30 - 20:30, which I surmise is the event they\'re referring to, given that "jig" is synonymous with dancing.\n\nI will now inform the user of the start time of this event. ',
            success_conditions=[
                {
                    "input_text": '1. The start time of the event named "Salsa Dance Class" is presented to the user: 19:30:00, July 31st, 2024. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
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
                # Milestone 1 – The expected salsa event is found in the tool output
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
                                                "value": "Salsa Dance Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-31T19:30:00-07:00",
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
                # Milestone 2 – User is told the correct start time
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
                                            "19:30",
                                            "7:30",
                                            "7:30 pm",
                                            "7:30pm",
                                            "7:30 p.m.",
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
                (0, 1),  # Calendar lookup → confirm event exists
                (1, 2),  # Event confirmed → respond to user with time
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_d66ab63e-3f35-485c-9611-60c0d64f7386_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-30T21:00:00-07:00",
            is_read_time="2024-07-30T21:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know if you have Salsa tomorrow. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Do I have salsa practice tomorrow?",
                },
            ],
            reasoning="The user wants to know if they have salsa practise tomorrow. I should check their calendar to look for an event matching this description. I can't see an event called salsa practise but I see 'Salsa Dance Class' occurs tomorrow, Tuesday, July 31st from 19:30-20:30. They must mean that event. I'll confirm that the event is tomorrow and give the user the details of the event. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. Calendar is checked for Salsa class and returns the weekly event 'Salsa Dance Class' on Wednesday, July 31st from 19:30 to 20:30. ",
                },
                {
                    "statefullness": "Stateless",
                    "input_text": "2. The event is confirmed to be tomorrow and the details are given to the user. ",
                },
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Calendar lookup happens
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
                # Milestone 1 – The salsa class for tomorrow is returned from the calendar search
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
                                                "value": "Salsa Dance Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-31T19:30:00-07:00",
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
                # Milestone 2 – Agent tells the user they have salsa practice tomorrow with details
                Milestone(
                    snapshot_constraints=[
                        # Must mention Salsa
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("Salsa", "salsa")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        # Must mention the time 19:30 / 7:30 pm
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("19:30", "7:30", "7:30 pm", "7:30pm")],
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
            name="THEO_APPLESEED_24_5096eb84-54d8-41f2-9c5a-af2c378b15d3_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:00:00-07:00",
            is_read_time="2024-07-29T10:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to write a message to Cookie Watson inviting her to attend salsa dance classes with you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a message to Cookie Watson saying "Hi Cookie I\'m going to salsa dance classes on July 31st do you want to come with me? :D"',
                },
            ],
            reasoning="The user wants to dictate a message to the contact called Cookie Watson.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft message with her.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": "1. A message is sent to Cookie Watson inviting her to attend salsa dance classes with you.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up Cookie Watson in the contacts list
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
                # Milestone 1 – Verify that Cookie Watson was returned from the contact lookup
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
                                                "value": "Cookie Watson",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9107",
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
                            reference_milestone_node_index=0,  # depend on Milestone 0 output
                        ),
                    ],
                ),
                # Milestone 2 – A new message inviting Cookie to salsa class was sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Ensure Cookie is one of the participants (either via phone or email)
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9107",
                                                "cookie.watson@example.com",
                                            )
                                        ]
                                    ],
                                    # Check that the body of the message references the salsa class invitation
                                    "content": "salsa",
                                    "creation_datetime_iso": "2024-07-29T10:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial state
                        ),
                    ],
                    # No need to guard-rail other DBs—expected single change
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # contact lookup → confirm Cookie returned
                (1, 2),  # confirm Cookie → message is sent
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_90785582-2dcf-4158-b170-3baa6bacc673_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:45:00-07:00",
            is_read_time="2024-07-29T07:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to delete the upcoming Salsa Dance Class event from your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the upcoming Salsa Dance Class event",
                },
            ],
            reasoning="The user wishes to delete an event named Salsa Dance Class from their calendar. First, I'll locate any events by this name, and then once a list is compiled, I'll delete the upcoming one. ",
            success_conditions=[
                {
                    "input_text": "1. The event Salsa Dance Class on July 31, 2024 - 19:30 is deleted",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. No other calendar event is deleted.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent tries to locate the Salsa class in the calendar
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
                # Milestone 1 – Confirm the Salsa Dance Class event was present in the tool output
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
                                                "value": "Salsa Dance Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-31T19:30:00-07:00",
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
                # Milestone 2 – Salsa Dance Class event has been removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Salsa Dance Class",
                                    "start_datetime_iso": "2024-07-31T19:30:00-07:00",
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
            minefields=[
                # Only the requested class is cancelled; no other lesson shall be removed
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": ["Salsa Dance Class"] * 11
                                    + ["Cooking Class"],
                                    "start_datetime_iso": [
                                        "2024-08-07T19:30:00-07:00",
                                        "2024-08-14T19:30:00-07:00",
                                        "2024-08-21T19:30:00-07:00",
                                        "2024-08-28T19:30:00-07:00",
                                        "2024-09-04T19:30:00-07:00",
                                        "2024-09-11T19:30:00-07:00",
                                        "2024-09-18T19:30:00-07:00",
                                        "2024-09-25T19:30:00-07:00",
                                        "2024-10-02T19:30:00-07:00",
                                        "2024-10-09T19:30:00-07:00",
                                        "2024-10-16T19:30:00-07:00",
                                        "2024-07-28T13:00:00-07:00",
                                    ],
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_dc0c576c-6a3b-4971-b508-5bb347334678_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-30T17:00:00-07:00",
            is_read_time="2024-07-30T17:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to cancel your salsa dance class this week as you will be in Chicago until the end of this week so can't make it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Cancel my salsa class since I will be away in Chicago until the end of this week. ",
                },
            ],
            reasoning="The user mentions their salsa classes, I find such event is an recurring one from 7/31. User further mentioned that they will be in Chicago by the end of this week, I need to check first when he will be away. The user has a train trip to Chicago today, so the user will be out-of-town from 7/30 to 8/4. I assume they want to cancle the 7/31 one as the use is out of town. \n\nThen I will cancel the first salsa class only in users calendar on 07-31-2024 starting at 19:30. ",
            success_conditions=[
                {
                    "input_text": '1. The event "Salsa Dance Class" at 19:30-20:30 on 31 July is deleted.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. No other calendar event is deleted.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent tries to locate the salsa class in the calendar
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
                # Milestone 1 – The salsa class on 31 July 2024 is removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Salsa Dance Class",
                                    "start_datetime_iso": "2024-07-31T19:30:00-07:00",
                                    "end_datetime_iso": "2024-07-31T20:30:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # calendar lookup precedes deletion
            ],
            minefields=[
                # Only the requested class is cancelled; no other lesson shall be removed
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": ["Salsa Dance Class"] * 11
                                    + ["Cooking Class"],
                                    "start_datetime_iso": [
                                        "2024-08-07T19:30:00-07:00",
                                        "2024-08-14T19:30:00-07:00",
                                        "2024-08-21T19:30:00-07:00",
                                        "2024-08-28T19:30:00-07:00",
                                        "2024-09-04T19:30:00-07:00",
                                        "2024-09-11T19:30:00-07:00",
                                        "2024-09-18T19:30:00-07:00",
                                        "2024-09-25T19:30:00-07:00",
                                        "2024-10-02T19:30:00-07:00",
                                        "2024-10-09T19:30:00-07:00",
                                        "2024-10-16T19:30:00-07:00",
                                        "2024-07-28T13:00:00-07:00",
                                    ],
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_c74de520-4bc0-42b7-9351-4e380f14ca4d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-31T17:35:00-07:00",
            is_read_time="2024-07-31T17:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You have caught a stomach bug and are much too sick to attend your salsa class this evening, so you want to delete it from your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete Salsa Dance Class today.",
                },
            ],
            reasoning="The user wants to delete their Salsa Dance Class today. I'll check their calendar.\n\nI found the event the user mentioned: Salsa Dance Class at 19:30-20:30 on 2024-07-31. I will go ahead and delete it, then let the user know.",
            success_conditions=[
                {
                    "input_text": "1. Salsa Dance Class at 19:30-20:30 on 2024-07-31 is deleted.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. No other calendar event is deleted.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the calendar to locate the Salsa Dance Class
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
                # Milestone 1 – The Salsa Dance Class event has been removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Salsa Dance Class",
                                    "start_datetime_iso": "2024-07-31T19:30:00-07:00",
                                    "end_datetime_iso": "2024-07-31T20:30:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to pre-task snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar lookup precedes deletion
            ],
            minefields=[
                # Only the requested class is cancelled; no other lesson shall be removed
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": ["Salsa Dance Class"] * 11
                                    + ["Cooking Class"],
                                    "start_datetime_iso": [
                                        "2024-08-07T19:30:00-07:00",
                                        "2024-08-14T19:30:00-07:00",
                                        "2024-08-21T19:30:00-07:00",
                                        "2024-08-28T19:30:00-07:00",
                                        "2024-09-04T19:30:00-07:00",
                                        "2024-09-11T19:30:00-07:00",
                                        "2024-09-18T19:30:00-07:00",
                                        "2024-09-25T19:30:00-07:00",
                                        "2024-10-02T19:30:00-07:00",
                                        "2024-10-09T19:30:00-07:00",
                                        "2024-10-16T19:30:00-07:00",
                                        "2024-07-28T13:00:00-07:00",
                                    ],
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_c74de520-4bc0-42b7-9351-4e380f14ca4d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-31T17:35:00-07:00",
            is_read_time="2024-07-31T17:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You have caught a stomach bug and are much too sick to attend your salsa class this evening, so you want to delete it from your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I'm really sick, cancel my salsa class.",
                },
            ],
            reasoning="The user is really sick and wants to cancel their salsa class. I'll check their calendar.\n\nI found 12 recurring instances of Salsa Dance Class in the user's schedule, the first of which is at 19:30-20:30 today (2024-07-31). Since the user's reason for cancelling the event is sickness, I can determine that they don't want to cancel all recurring event instances, but rather just today's one.\n\nI will delete the Salsa Dance Class scheduled today and inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Salsa Dance Class at 19:30-20:30 on 2024-07-31 is deleted.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. No other calendar event is deleted.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar to find the salsa class event
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
                # Milestone 1 – Confirm that the salsa class on 2024-07-31 at 19:30 was returned from the calendar search
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
                                                "value": "Salsa Dance Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-31T19:30:00-07:00",
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
                # Milestone 2 – Salsa Dance Class instance is removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Salsa Dance Class",
                                    "start_datetime_iso": "2024-07-31T19:30:00-07:00",
                                    "end_datetime_iso": "2024-07-31T20:30:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare against initial state
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar search → verify correct event found
                (1, 2),  # Event identified → event removed
            ],
            minefields=[
                # Only the requested class is cancelled; no other lesson shall be removed
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": ["Salsa Dance Class"] * 11
                                    + ["Cooking Class"],
                                    "start_datetime_iso": [
                                        "2024-08-07T19:30:00-07:00",
                                        "2024-08-14T19:30:00-07:00",
                                        "2024-08-21T19:30:00-07:00",
                                        "2024-08-28T19:30:00-07:00",
                                        "2024-09-04T19:30:00-07:00",
                                        "2024-09-11T19:30:00-07:00",
                                        "2024-09-18T19:30:00-07:00",
                                        "2024-09-25T19:30:00-07:00",
                                        "2024-10-02T19:30:00-07:00",
                                        "2024-10-09T19:30:00-07:00",
                                        "2024-10-16T19:30:00-07:00",
                                        "2024-07-28T13:00:00-07:00",
                                    ],
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_90785582-2dcf-4158-b170-3baa6bacc673_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:45:00-07:00",
            is_read_time="2024-07-29T07:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to delete the upcoming Salsa Dance Class event from your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Find the next Salsa Dance Class event and delete it form my calendar ",
                },
            ],
            reasoning="The user wants to delete an event from their calendar. First, I'll locate events matching the provided name \"Salsa Dance Class\". Once a list is compiled, I'll rdelete the next one. ",
            success_conditions=[
                {
                    "input_text": "1. The event Salsa Dance Class on July 31, 2024 - 19:30 is deleted",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. No other calendar event is deleted.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – The agent looks up calendar events to locate the upcoming Salsa class
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
                # Milestone 1 – Confirm that the Salsa Dance Class event (July 31, 2024 19:30) appeared in the tool results
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
                                                "value": "Salsa Dance Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-31T19:30:00-07:00",
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
                # Milestone 2 – The Salsa Dance Class event is removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Salsa Dance Class",
                                    "start_datetime_iso": "2024-07-31T19:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_exact_match_similarity,
                                "start_datetime_iso": column_contains_similarity,
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
            minefields=[
                # Only the requested class is cancelled; no other lesson shall be removed
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": ["Salsa Dance Class"] * 11
                                    + ["Cooking Class"],
                                    "start_datetime_iso": [
                                        "2024-08-07T19:30:00-07:00",
                                        "2024-08-14T19:30:00-07:00",
                                        "2024-08-21T19:30:00-07:00",
                                        "2024-08-28T19:30:00-07:00",
                                        "2024-09-04T19:30:00-07:00",
                                        "2024-09-11T19:30:00-07:00",
                                        "2024-09-18T19:30:00-07:00",
                                        "2024-09-25T19:30:00-07:00",
                                        "2024-10-02T19:30:00-07:00",
                                        "2024-10-09T19:30:00-07:00",
                                        "2024-10-16T19:30:00-07:00",
                                        "2024-07-28T13:00:00-07:00",
                                    ],
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_5b765105-55cd-4db6-89d3-944cb4af3fa5_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-30T14:20:00-07:00",
            is_read_time="2024-07-30T14:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know the location of your future Salsa classes. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where will my Salsa Dance classes be on?",
                },
            ],
            reasoning="The user wants to know where their Salsa Dance classes will be on. Let me look for them in Calendar. I can see their event 'Salsa Dance Class' which is scheduled to reoccur weekly on Wednesdays so this must be the event they're talking about. I can see the location which is 'Downtown Dance Studio, Orchard County, CA' and relay this to the user.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their 'Salsa Dance Class' event  scheduled for 31st July 2024 at 19:30 will take place at 'Downtown Dance Studio, Orchard County, CA'.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (read-only)
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
                # Milestone 1 – The expected Salsa class event is present in the retrieved results
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
                                                "value": "Salsa Dance Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-31T19:30:00-07:00",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Downtown Dance Studio",
                                                "partial": True,  # allow full address variations
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
                # Milestone 2 – Agent informs the user of the correct location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Downtown Dance Studio",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,  # only need location mention
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
            name="THEO_APPLESEED_24_115ced33-08ca-467d-92fd-4684e93218e1_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T13:30:00-07:00",
            is_read_time="2024-07-24T13:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to cancel your dinner with Cookie tonight. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my Dinner with Cookie. ",
                },
            ],
            reasoning="The user wants to delete their Dinner with Cookie. Looking at their Calendar, they have a Dinner with Cookie from 19:00-21:00 on 24 July 2024. This must be what the user wants me to delete. I will delete it and let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. Dinner with Cookie from 19:00-21:00 on 24 July 2024 is deleted. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. No other calendar event is deleted.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 — Agent tries to locate the calendar event
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
                # Milestone 1 — Confirm “Dinner with Cookie” was retrieved in milestone 0
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
                                                "value": "Dinner with Cookie",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-24T19:00:00-07:00",
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
                # Milestone 2 — Event is removed from the calendar database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dinner with Cookie",
                                    "start_datetime_iso": "2024-07-24T19:00:00-07:00",
                                    "end_datetime_iso": "2024-07-24T21:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
            minefields=[
                # "Cookie" must not be fuzzy-matched onto the Cooking Class
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Cooking Class",
                                    "start_datetime_iso": "2024-07-28T13:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_1b6749d9-dc54-4de0-8564-02dfbb8d28e3_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:40:00-07:00",
            is_read_time="2024-07-29T07:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to text Cookie asking her if she'd like to join you at the Salsa classes "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text Cookie asking she would like to attend the salsa classes with me",
                },
            ],
            reasoning="The user wants to text Cookie asking if she'd like to attend the salsa classes with them. According to the user's calendar they attend a Salsa class every Wednesday at 7:30pm until October 16th. I'll say something like \" Hey Cookie would you like to come with me to a salsa class I signed up for?\" and present it to the user. With their approval I will send the message to Cookie Watson",
            success_conditions=[
                {
                    "input_text": "1. A text message is sent to Cookie Watson asking if she'd like to come to the Salsa classes",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 — The agent looks up Cookie’s contact information
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
                # Milestone 1 — Confirm Cookie Watson is contained in the contact-search results from Milestone 0
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
                                                "value": "Cookie Watson",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9107",
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
                # Milestone 2 — A new text message to Cookie is sent
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
                                                "1234-5678-9107",  # Cookie's phone
                                                "cookie.watson@example.com",  # Cookie's email
                                            ),
                                            (
                                                "1234-5678-9101",  # Theo (self)
                                                "theo.appleseed@example.com",  # Theo's email
                                            ),
                                        ]
                                    ],
                                    "content": "salsa",
                                    "creation_datetime_iso": "2024-07-29T07:40:00-07:00",
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
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # contact lookup → verify Cookie returned
                (1, 2),  # Cookie verified → message sent
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_9ac0eab7-0359-4d49-9506-a17e581aa2c1_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-04T17:30:00-07:00",
            is_read_time="2024-08-04T17:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to double check the time of your salsa class. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": '"Salsa Dance Class" does take place every Wednesday from 19:30-20:30 right? Until when?',
                },
            ],
            reasoning='Ok so the user wants to know if "Salsa Dance Class" takes place every Wednesday from 19:30-20:30. First I will locate the event "Salsa Dance Class." "Salsa Dance Class" is on the calendar and takes place every Wednesday from 19:30-20:30, starting 7/31 until 10/16.  I will now let the user know that "Salsa Dance Class" takes place every Wednesday from 19:30-20:30 and it ends on 10-16. ',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The user is informed that "Salsa Dance Class" takes place every Wednesday from 19:30-20:30 until October 16. ',
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
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
                    ]
                ),
                # Milestone 1 – The agent tells the user that class is every Wednesday 19:30-20:30
                Milestone(
                    snapshot_constraints=[
                        # Confirms mention of the end date
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "October 16",
                                            "Oct 16",
                                            "16 October",
                                            "10-16",
                                            "10/16",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar lookup precedes user response
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_ea62219d-6d80-4f03-b5cd-ea8922ffc4fa_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-31T19:05:00-07:00",
            is_read_time="2024-07-31T19:05:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You're a tad late leaving the office today and you won't make it on time to your new class.   You want to reschedule the event in your calendar to start half an hour later instead. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Help me change my event time I won't get to my Salsa Dance Class until 20:00 but it'll finish at the same time still",
                },
            ],
            reasoning='The user wants to adjust the time of their event, "Salsa Dance Class", which is occurring today on July 31, 2024 at 19:30. They mentioned that they are running late, so they asked me to adjust the starting time from 19:30 to 20:00. They also said that the event will still end at the same time. Therefore, I will update the time for the "Salsa Dance Class" event to be 20:00 to 20:30.',
            success_conditions=[
                {
                    "input_text": '2. The event "Salsa Dance Class" is rescheduled to July 31, 2024 20:00 - 20:30.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "modify_calendar_event",
                "search_calendar_events",
            ],
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
                # Milestone 1 – Confirm the “Salsa Dance Class” event was found in the previous tool call
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
                                                "value": "Salsa Dance Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-31T19:30:00-07:00",
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
                # Milestone 2 – Event has been rescheduled (updated calendar record)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Salsa Dance Class",
                                    "start_datetime_iso": "2024-07-31T20:00:00-07:00",
                                    "end_datetime_iso": "2024-07-31T20:30:00-07:00",
                                    "creation_datetime_iso": "2024-07-31T19:05:00-07:00",
                                }
                            ),
                            column_similarity_measure={
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
            name="THEO_APPLESEED_24_531176a2-45a1-46f3-8472-95adb30f9090_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T20:00:00-07:00",
            is_read_time="2024-07-29T20:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to text Cookie to ask if she is joining you at salsa class you have booked for Wednesday July 31, 2024.  \n\nYou want to text Cookie to ask if she’s joining you at salsa class tonight. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Message Cookie saying "Do you want to join this salsa dance class I\'m doing every Wednesday? It will be super fun and you never do anything with me!"',
                },
            ],
            reasoning='The user wants to send a message. I will ask first who they want to send the message to. They confirm this as Cookie Watson. After this I will ask what they want to send in the body of the message. They confirm this as "Do you want to join this salsa dance class I\'m doing every Wednesday? It will be super fun and you never do anything with me!". I will then send this message to Cookie Watson.',
            success_conditions=[
                {
                    "input_text": '1. The message "Do you want to join this salsa dance class I\'m doing every Wednesday? It will be super fun and you never do anything with me!" is sent to Cookie Watson at 20:00 on 29th July 2024',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up Cookie in the contacts list
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
                # Milestone 1 – Verify that Cookie Watson was returned by the contact-lookup in Milestone 0
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
                                                "value": "Cookie Watson",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9107",
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
                # Milestone 2 – A new message to Cookie is created that contains the salsa-class invitation
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least one identifier for Cookie must appear in the participants list
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9107",
                                                "cookie.watson@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "join this salsa dance class",
                                    "creation_datetime_iso": "2024-07-29T20:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ],
                    # Ignore unrelated DBs when looking for this new message
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_9ac0eab7-0359-4d49-9506-a17e581aa2c1_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-04T17:30:00-07:00",
            is_read_time="2024-08-04T17:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to double check the time of your salsa class. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "It's at half seven every Wednesday right? until when?",
                },
            ],
            reasoning="Ok so the user wants to know if it's at half seven every Wednesday. First, I'll establish what they mean by it. I will look at what events are around the given timeline to see if there is anything there. There is an event \"Salsa Dance Class\" that takes place every Wednesday from 19:30-20:30 which seems to be the 'it' that the user is referring to. I will now let the user know that \"Salsa Dance Class\" takes place every Wednesday from 19:30-20:30 until 10-16. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The user is informed that "Salsa Dance Class" takes place every Wednesday from 19:30-20:30 and ends on October 16. ',
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent looks up the calendar to confirm the class time
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
                # Milestone 1 – The returned calendar data includes the Salsa Dance Class
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
                                                "value": "Salsa Dance Class",
                                                "partial": False,
                                            },
                                            # Only the name is strictly required; time details are conveyed in Milestone 2
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
                # Milestone 2 – The user is told the class is every Wednesday at 19:30-20:30
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
                                            "October 16",
                                            "Oct 16",
                                            "16 October",
                                            "10-16",
                                            "10/16",
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
            name="THEO_APPLESEED_24_1b6749d9-dc54-4de0-8564-02dfbb8d28e3_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:40:00-07:00",
            is_read_time="2024-07-29T07:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to text Cookie asking her if she'd like to join you at the Salsa classes "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text my friend asking them if they'd like to attend the salsa classes with me",
                },
            ],
            reasoning="The user wants to text their friend if they'd like to attend the salsa classes with them. According to the user's calendar they attend a Salsa class every Wednesday at 7:30pm until October 16th. I must determine who the user is referring to as their friend as the user has multiple contacts notes as friend, I'll ask them to specify. The user wants to text Cookie Watson. I'll say something like \" Hey Cookie would you like to come with me to a salsa class I signed up for?\" and present it to the user. With their approval I will send the message to Cookie Watson",
            success_conditions=[
                {
                    "input_text": "1. A text message is sent to Cookie Watson asking if she'd like to come to the Salsa classes",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up the friend’s contact information
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
                # Milestone 1 – Verify that Cookie Watson was found in the contact-search result
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
                                                "value": "Cookie Watson",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9107",
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
                # Milestone 2 – A new text message is sent to Cookie mentioning the salsa class
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least one identifier for Cookie must be present in the participant list
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9107",
                                                "cookie.watson@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "salsa",
                                    "creation_datetime_iso": "2024-07-29T07:40:00-07:00",
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
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact search → confirm Cookie
                (1, 2),  # Confirm Cookie → message sent
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_115ced33-08ca-467d-92fd-4684e93218e1_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T13:30:00-07:00",
            is_read_time="2024-07-24T13:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to cancel your dinner with Cookie tonight. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my event with Cookie.",
                },
            ],
            reasoning="The user wants to delete their event with Cookie. Looking at their Calendar, they have a Dinner with Cookie from 19:00-21:00 on 24 July 2024. This must be what the user meant. I will delete this and let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. Dinner with Cookie from 19:00-21:00 on 24 July 2024 is deleted. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. No other calendar event is deleted.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – The agent looks up calendar events to locate the dinner with Cookie
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
                # Milestone 1 – Confirm that the “Dinner with Cookie” event was returned from Milestone 0
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
                                                "value": "Dinner with Cookie",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-24T19:00:00-07:00",
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
                # Milestone 2 – The dinner event has been removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dinner with Cookie",
                                    "start_datetime_iso": "2024-07-24T19:00:00-07:00",
                                    "end_datetime_iso": "2024-07-24T21:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # calendar search → confirmation of event retrieval
                (1, 2),  # confirmation of event retrieval → verify deletion
            ],
            minefields=[
                # "Cookie" must not be fuzzy-matched onto the Cooking Class
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Cooking Class",
                                    "start_datetime_iso": "2024-07-28T13:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_5b765105-55cd-4db6-89d3-944cb4af3fa5_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-30T14:20:00-07:00",
            is_read_time="2024-07-30T14:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know the location of your future Salsa classes. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where is my event taking place tomorrow?",
                },
            ],
            reasoning="The user wants to know where their event tomorrow is taking place. I can see from their calendar that they have one event taking place tomorrow, 31st July 2024 at 19:30 titled 'Salsa Dance Class'. This is a reoccurring event that will take place at 'Downtown Dance Studio, Orchard County, CA'. I can then relay this to the user.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their 'Salsa Dance Class' event  scheduled for 31st July 2024 at 19:30 will take place at 'Downtown Dance Studio, Orchard County, CA'.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent queries calendar to find tomorrow's event
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
                # Milestone 1 – Confirm the Salsa class event (with correct location) was returned by the tool call in Milestone 0
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
                                                "value": "Salsa Dance Class",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Downtown Dance Studio",
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
                # Milestone 2 – User-facing reply includes the correct location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Downtown Dance Studio",
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
                (0, 1),  # Tool call → verify returned event
                (1, 2),  # Event verified → user informed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_22127402-d460-4cab-a05c-5c838e866148_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-31T23:00:00-07:00",
            is_read_time="2024-07-31T23:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You had a really good time at your last salsa class, you can't wait for the next one and want to know when it is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell me the date of my next salsa class.",
                },
            ],
            reasoning="The user is asking about the date of an upcoming event.\nI should look into their calendar and confirm.\nI have found the queried event, Salsa Class scheduled for August 7, 2024 19:30-20:30.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1) Date of upcoming salsa class is confirmed as August 7, 2024 19:30-20:30.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent looks in the calendar for upcoming salsa classes
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
                # Milestone 1 – Confirm the retrieved calendar event is the correct salsa class on Aug 7 2024 19:30
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
                                                "value": "Salsa Dance Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-08-07T19:30:00-07:00",
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
                # Milestone 2 – The agent tells the user the correct date and time of the next class
                Milestone(
                    snapshot_constraints=[
                        # Check date mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "August 7",
                                            "Aug 7",
                                            "7 August",
                                            "7 Aug",
                                            "8/7",
                                            "08/07",
                                            "08-07",
                                            "next Wednesday",
                                            "2024-08-07T19:30",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                        # Check time mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "19:30",
                                            "7:30",
                                            "7:30 pm",
                                            "7:30pm",
                                            "19:30-20:30",
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
                (0, 1),  # Calendar search → verify correct event retrieved
                (1, 2),  # Correct event retrieved → user informed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_5eaa4ae3-273f-4a30-9253-6fc4709670c1_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-30T12:20:00-07:00",
            is_read_time="2024-07-30T12:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You told Cookie how excited you are to go ahead with your salsa class tomorrow and she is interested in coming along to try it out with you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you please add Cookie to the event tomorrow and only that one not the rest",
                },
            ],
            reasoning='The user wants me to add someone to their event that they have on tomorrow. The user referred to them as Cookie,  so I\'ll double check the user\'s contacts to see if there is any contact with that name. Looking through the contacts, I found "Cookie Watson". This must be the person the user is referring to.\nNext I need to figure out what exact event the user wants to add Cookie to. Checking the user\'s calendar for tomorrow, July 31st 2024, there is only one event on their calendar, which is the "Salsa Dance Class" event at 19:30-20:30. This is most likely the event the user wants Cookie added to.\nFinally, the user said to only "add them to that one, not the rest". This might refer to the multiple "Salsa Dance Class" entries in the user\'s calendar. The user likely means that they do not want Cookie added as an attendee to every single "Salsa Dance Class" event, just the one for tomorrow. With the user\'s confirmation, I will add Cookie Watson to the event "Salsa Dance Class" on July 31, 2024 at 19:30-20:30.',
            success_conditions=[
                {
                    "input_text": '3. Cookie Watson will be added to the event "Salsa Dance Class" on July 31, 2024 at 19:30-20:30.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "4. The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "modify_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – The agent tries to locate “Cookie” in the contacts
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
                # Milestone 1 – Confirms that Cookie Watson was indeed returned from the contact search
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
                                                "value": "Cookie Watson",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9107",
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
                            reference_milestone_node_index=0,  # depend on contact search
                        ),
                    ],
                ),
                # Milestone 2 – The agent searches calendar to locate tomorrow’s salsa class
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
                # Milestone 3 – Verifies the correct Salsa Dance Class instance (July 31) was found
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
                                                "value": "Salsa Dance Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-31T19:30:00-07:00",
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
                            reference_milestone_node_index=2,  # depend on calendar search
                        ),
                    ],
                ),
                # Milestone 4 – Calendar event is updated so that Cookie Watson is now an attendee
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Salsa Dance Class",
                                    "start_datetime_iso": "2024-07-31T19:30:00-07:00",
                                    "attendees_names": [["Cookie Watson"]],
                                    "creation_datetime_iso": "2024-07-30T12:20:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # Ensure Cookie was added (other names may remain / be reordered)
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # contact search → confirm Cookie
                (2, 3),  # calendar search → confirm event
                (3, 4),  # once event identified → update made
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_3be97209-ac86-4ba4-a9e9-4b2e6d03ec09_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-30T16:00:00-07:00",
            is_read_time="2024-07-30T16:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        'You want to cancel the calendar event called "Salsa Dance Class" on the 31st of July 2024 at 19:30pm because you are away in Chicago this week. '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I will be out of town this week, cancel the lesson",
                },
            ],
            reasoning='The user wants to cancel a lesson because they are away this week. Looking at the calendar for this week, the only lesson-type event is "Salsa Dance Class" on 31 July 2024 at 19:30 — the 7 August recurrence falls in the following week, the Cooking Class on 28 July has already passed, and the gym session is not a lesson. I find that event and cancel it, and leave every other event in place.',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. Calendar event called "Salsa Dance Class" on 31 July 2024 is found and cancelled.',
                },
                {
                    "input_text": "2. No other calendar event is deleted.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events to locate the salsa class
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
                # Milestone 1 – Verify that the salsa class event was indeed returned/found
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
                                                "value": "Salsa Dance Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-31T19:30:00-07:00",
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
                            reference_milestone_node_index=0,  # depend on tool outcome in milestone 0
                        )
                    ],
                ),
                # Milestone 2 – Confirm the event was cancelled (removed from the calendar)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Salsa Dance Class",
                                    "start_datetime_iso": "2024-07-31T19:30:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
            minefields=[
                # Only the requested class is cancelled; no other lesson shall be removed
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": ["Salsa Dance Class"] * 11
                                    + ["Cooking Class"],
                                    "start_datetime_iso": [
                                        "2024-08-07T19:30:00-07:00",
                                        "2024-08-14T19:30:00-07:00",
                                        "2024-08-21T19:30:00-07:00",
                                        "2024-08-28T19:30:00-07:00",
                                        "2024-09-04T19:30:00-07:00",
                                        "2024-09-11T19:30:00-07:00",
                                        "2024-09-18T19:30:00-07:00",
                                        "2024-09-25T19:30:00-07:00",
                                        "2024-10-02T19:30:00-07:00",
                                        "2024-10-09T19:30:00-07:00",
                                        "2024-10-16T19:30:00-07:00",
                                        "2024-07-28T13:00:00-07:00",
                                    ],
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_08502def-b562-4a16-8027-35014bbb32a0_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_24",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:45:00-07:00",
            is_read_time="2024-07-29T07:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to delete the upcoming Salsa Dance Class event from your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Find the next Salsa Dance Class event and delete it form my calendar ",
                },
            ],
            reasoning="The user wants to delete an event from their calendar. First, I'll locate events matching the provided name \"Salsa Dance Class\". Once a list is compiled, I'll delete the next one. ",
            success_conditions=[
                {
                    "input_text": "1. The event Salsa Dance Class on July 31, 2024 - 19:30 is deleted",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. No other calendar event is deleted.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent uses calendar retrieval to find the next Salsa Dance Class
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
                # Milestone 1 – Verify that a Salsa Dance Class event on July 31, 2024 19:30–20:30 was retrieved
                # (i.e., the agent correctly identified the event to delete)
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
                                                "value": "Salsa Dance Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-31T19:30:00-07:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-07-31T20:30:00-07:00",
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
                # Milestone 2 – The Salsa Dance Class event on July 31, 2024 19:30–20:30 is deleted from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Salsa Dance Class",
                                    "start_datetime_iso": "2024-07-31T19:30:00-07:00",
                                    "end_datetime_iso": "2024-07-31T20:30:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
                # Milestone 3 – User is informed that the event was deleted (optional but desirable)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Salsa Dance Class",
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
                (0, 1),  # Calendar lookup → confirm the correct Salsa event
                (1, 2),  # Event identified → event removed
            ],
            minefields=[
                # Only the requested class is cancelled; no other lesson shall be removed
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": ["Salsa Dance Class"] * 11
                                    + ["Cooking Class"],
                                    "start_datetime_iso": [
                                        "2024-08-07T19:30:00-07:00",
                                        "2024-08-14T19:30:00-07:00",
                                        "2024-08-21T19:30:00-07:00",
                                        "2024-08-28T19:30:00-07:00",
                                        "2024-09-04T19:30:00-07:00",
                                        "2024-09-11T19:30:00-07:00",
                                        "2024-09-18T19:30:00-07:00",
                                        "2024-09-25T19:30:00-07:00",
                                        "2024-10-02T19:30:00-07:00",
                                        "2024-10-09T19:30:00-07:00",
                                        "2024-10-16T19:30:00-07:00",
                                        "2024-07-28T13:00:00-07:00",
                                    ],
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_08502def-b562-4a16-8027-35014bbb32a0_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_24",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:45:00-07:00",
            is_read_time="2024-07-29T07:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to delete the upcoming Salsa Dance Class event from your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the upcoming Salsa Dance Class event",
                },
            ],
            reasoning="The user wishes to delete an event named Salsa Dance Class from their calendar. First, I'll locate any events by this name, and then once a list is compiled, I'll delete the upcoming one. ",
            success_conditions=[
                {
                    "input_text": "1. The event Salsa Dance Class on July 31, 2024 - 19:30 is deleted",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. No other calendar event is deleted.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (to find the Salsa Dance Class to delete)
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
                # Milestone 1 – Verify that the Salsa Dance Class event on 2024-07-31T19:30 was among the retrieved events
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
                                                "value": "Salsa Dance Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-31T19:30:00-07:00",
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
                # Milestone 2 – The Salsa Dance Class event on 2024-07-31T19:30 is deleted from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Salsa Dance Class",
                                    "start_datetime_iso": "2024-07-31T19:30:00-07:00",
                                    "end_datetime_iso": "2024-07-31T20:30:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # calendar lookup → confirm correct event identified
                (1, 2),  # correct event identified → event removed
            ],
            minefields=[
                # Only the requested class is cancelled; no other lesson shall be removed
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": ["Salsa Dance Class"] * 11
                                    + ["Cooking Class"],
                                    "start_datetime_iso": [
                                        "2024-08-07T19:30:00-07:00",
                                        "2024-08-14T19:30:00-07:00",
                                        "2024-08-21T19:30:00-07:00",
                                        "2024-08-28T19:30:00-07:00",
                                        "2024-09-04T19:30:00-07:00",
                                        "2024-09-11T19:30:00-07:00",
                                        "2024-09-18T19:30:00-07:00",
                                        "2024-09-25T19:30:00-07:00",
                                        "2024-10-02T19:30:00-07:00",
                                        "2024-10-09T19:30:00-07:00",
                                        "2024-10-16T19:30:00-07:00",
                                        "2024-07-28T13:00:00-07:00",
                                    ],
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_5eaa4ae3-273f-4a30-9253-6fc4709670c1_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-30T12:20:00-07:00",
            is_read_time="2024-07-30T12:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You told Cookie how excited you are to go ahead with your salsa class tomorrow and she is interested in coming along to try it out with you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Add Cookie Watson as a participant to the Salsa Dance Class event on July 31 2024 19:30-20:30.",
                },
            ],
            reasoning="The user is asking me to add a contact as a participant to an event.\nFirst, I will confirm the named contact. I can see Cookie Watson in the user's contacts.\nNext, I will identify the event they are referring to. I can see the event queried by the user,  Salsa Dance Class event on July 31 2024 19:30-20:30.\nI will go ahead and add Cookie Watson as a participant to  Salsa Dance Class event on July 31 2024 19:30-20:30.",
            success_conditions=[
                {
                    "input_text": '3. Cookie Watson will be added to the event "Salsa Dance Class" on July 31, 2024 at 19:30-20:30.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "4. The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "modify_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – the agent looks up Cookie’s contact information
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
                # Milestone 1 – the agent searches for the Salsa Dance Class event
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
                # Milestone 2 – the Salsa Dance Class event is updated to include Cookie Watson
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Salsa Dance Class",
                                    "start_datetime_iso": "2024-07-31T19:30:00-07:00",
                                    "end_datetime_iso": "2024-07-31T20:30:00-07:00",
                                    "attendees_names": [
                                        [
                                            "Cookie Watson",
                                            "Theo Appleseed",
                                            "Downtown Dance Studio",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-07-30T12:20:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 2),  # contact lookup precedes updating the event
                (1, 2),  # event lookup precedes updating the event
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_24_22127402-d460-4cab-a05c-5c838e866148_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_24",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-31T23:00:00-07:00",
            is_read_time="2024-07-31T23:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You had a really good time at your last salsa class, you can't wait for the next one and want to know when it is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When's my next dance opportunity?",
                },
            ],
            reasoning="The user is asking about the date of an upcoming event.\nI should look into their calendar and confirm.\nThe user has specified the event is related to dance, this will narrow my search. \nI have found one potential match coming up within the next week.\nSalsa Class scheduled for August 7, 2024 19:30-20:30.\nI am confident that this is the event being referred to.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1) Date of upcoming salsa class is confirmed as August 7, 2024 19:30-20:30.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent searches the calendar for upcoming dance classes
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
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Calendar search returns the correct upcoming Salsa class
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
                                                "value": "Salsa Dance Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-08-07T19:30:00-07:00",
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
                # Milestone 2 – Agent informs the user of the correct date and time
                Milestone(
                    snapshot_constraints=[
                        # Verify the date is mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": [RoleType.AGENT],
                                    "recipient": [RoleType.USER],
                                    "content": [
                                        (
                                            "August 7",
                                            "Aug 7",
                                            "7 August",
                                            "7 Aug",
                                            "08-07",
                                            "8-07",
                                            "8/7",
                                            "08/07",
                                            "7/08",
                                            "Wednesday the 7th",
                                            "7th of August",
                                            "next Wednesday",
                                            "2024-08-07T19:30",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                        # Verify the time is mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": [RoleType.AGENT],
                                    "recipient": [RoleType.USER],
                                    "content": [
                                        (
                                            "7:30 pm",
                                            "7:30pm",
                                            "19:30",
                                            "7:30 p.m.",
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
    ]
