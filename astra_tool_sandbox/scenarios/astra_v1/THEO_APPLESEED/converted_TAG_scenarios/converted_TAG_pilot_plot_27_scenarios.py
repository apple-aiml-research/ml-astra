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
    column_one_similarity,
    column_rouge_l_similarity,
    column_str_contains_all_similarity,
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


def get_TAG_THEO_APPLESEED_pilot_plot_27(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="THEO_APPLESEED_27_0f6584cd-6554-4b94-bcb9-af620325e968_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:03:00-07:00",
            is_read_time="2024-07-29T10:03:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You need to reply to the optician confirming your appointment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to the eye doctor telling them 'Thank you for the reminder. I confirm my appointment for August 2nd at 14:30.'.",
                },
            ],
            reasoning='The user wants to "reply to the eye doctor". There is a text from 3 minutes ago from "optician@example.com" which I can deduce is most likely the "eye doctor". I will send the reply of \'Thank you for the reminder. I confirm my appointment for August 2nd at 14:30.\' to that contact address.',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "A text is sent to optician@example.com saying 'Thank you for the reminder. I confirm my appointment for August 2nd at 14:30.'.",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_messages", "send_message", "search_messages"],
            milestones=[
                # Milestone 0 – The agent looks up recent messages to find the optician’s reminder
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
                # Milestone 1 – Confirm that the message retrieved is the reminder from the optician
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
                                            # Conversation must involve the optician
                                            "participants_addresses": {
                                                "value": "optician@example.com",
                                                "partial": True,
                                            },
                                            # Content should mention “reminder”
                                            "content": {
                                                "value": "reminder",
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
                # Milestone 2 – Verify a confirmation message was sent to the optician
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At minimum the optician must be included; allow other participants (e.g., Theo)
                                    "participants_addresses": [
                                        ["optician@example.com"]
                                    ],
                                    "content": "confirm my appointment",  # substring check
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-29T10:03:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_subset_match_similarity,
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
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
            name="THEO_APPLESEED_27_dac6e2f6-d04c-4889-beab-82aa055028a1_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-02T10:05:00-07:00",
            is_read_time="2024-08-02T10:05:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what time your optician appointment was confirmed for. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is my confirmed appointment for today at?",
                },
            ],
            reasoning='The user wants to know what time their "appointment" is at today.\n\nOkay, first of all, I need to go to the user\'s Calendar for today to see if they have any upcoming events that match this description - they don\'t appear to have any events that correspond to this. I will check the user\'s data for any information on this.\n\nGreat, alright, I can see in their messages that they received a text from "optician@example.com" at 10:10:00 on July 29th, 2024 with the content "Thank you, Theo. We have confirmed your appointment for August 2nd at 14:30. We look forward to seeing you then." This must be the message the user is referring to, given that it\'s about an upcoming appointment. I will now present this message to the user. ',
            success_conditions=[
                {
                    "input_text": '1. The message received from "optician@example.com" at 10:10:00 on July 29th, 2024 is presented to the user. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent invokes a message-retrieval tool
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
                # Milestone 1 – Returned tool output contains the confirmation message from the optician
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
                                                "value": "optician@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "14:30",
                                                "partial": True,  # accept substring match
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
                            reference_milestone_node_index=0,  # depends on tool call in Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – Agent communicates the appointment time to the user
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
                                            "14:30",
                                            "2:30",
                                            "2:30 pm",
                                            "2:30pm",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,  # ensure “14:30” is in the reply
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Need tool output after tool invocation
                (1, 2),  # User reply should follow successful retrieval
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_dac6e2f6-d04c-4889-beab-82aa055028a1_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-02T10:05:00-07:00",
            is_read_time="2024-08-02T10:05:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what time your optician appointment was confirmed for. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to know what time my optician appointment is confirmed for please ",
                },
            ],
            reasoning='The user wants to know what time their "optician appointment" is confirmed for. First, I need to go to the user\'s Calendar to see if they have any upcoming events that match this description. They don\'t appear to have any events that correspond to the description in their query. I will now go to their Messages to see if they have received any that match the description. Okay, I can see they\'ve received a message from "optician@example.com" at 10:10:00 on July 29th, 2024 with the content "Thank you, Theo. We have confirmed your appointment for August 2nd at 14:30. We look forward to seeing you then."\n\nI will now present this message to the user. ',
            success_conditions=[
                {
                    "input_text": '1. The message received from "optician@example.com" at 10:10:00 on July 29th, 2024 is presented to the user. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – the agent looks through the user’s messages
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
                # Milestone 1 – confirm that the tool output contained the optician confirmation
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
                                                "value": "optician@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "14:30",
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
                # Milestone 2 – the agent informs the user of the confirmed appointment time
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
                                            "14:30",
                                            "2:30",
                                            "2:30 pm",
                                            "2:30pm",
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
                (0, 1),  # message-search → verify correct message found
                (1, 2),  # correct message found → user is informed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_0f6584cd-6554-4b94-bcb9-af620325e968_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:03:00-07:00",
            is_read_time="2024-07-29T10:03:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You need to reply to the optician confirming your appointment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to that last text tell them 'Thank you for the reminder. I confirm my appointment for August 2nd at 14:30.'.",
                },
            ],
            reasoning='The user wants to "reply to that last text". There is a text from 3 minutes ago from "optician@example.com" which is the most recent received message. I will send the reply  saying \'Thank you for the reminder. I confirm my appointment for August 2nd at 14:30.\' to that contact address.',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "A text is sent to optician@example.com saying 'Thank you for the reminder. I confirm my appointment for August 2nd at 14:30.'.",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_messages", "send_message", "search_messages"],
            milestones=[
                # Milestone 0 – The agent looks up the existing conversation / message from the optician
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
                # Milestone 1 – A reply message has been sent to the optician confirming the appointment
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
                                                "optician@example.com",
                                            ),  # optician - external, email only
                                            (
                                                "theo.appleseed@example.com",
                                                "1234-5678-9101",
                                            ),  # Theo - email or phone
                                        ]
                                    ],
                                    "status": "sent",
                                    "content": [
                                        (
                                            "Thank you for the reminder",
                                            "confirm my appointment",
                                        )
                                    ],
                                    "creation_datetime_iso": "2024-07-29T10:03:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "status": column_exact_match_similarity,
                                "content": column_str_contains_any_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against the pre-task snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_3d7b1b15-1a77-4261-b0df-1f5e61d3431a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:15:00-07:00",
            is_read_time="2024-07-29T10:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You completely forgot about the opticians appointment you had coming up.   You need to add that to your calendar before you forget again! You just got a text reminder that it is on Friday August 2nd 2024 at 14:30. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Help me schedule in opticians appointment for this Friday please 14:30",
                },
            ],
            reasoning='The user is asking me to create a new event for them, "Opticians Appointment". They told me all of the information I need to make it, but I need to double-check when exactly "this Friday" is. Today is Monday 29th July 2024, so that would make Friday the 2nd of August. I also found user data that confirms this data and time.\n\nWith the user\'s confirmation, I will create the event "Opticians Appointment" for Friday August 2nd at 14:30.',
            success_conditions=[
                {
                    "input_text": '1. The system will create the event "Opticians Appointment" for Friday August 2nd at 14:30.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["create_calendar_event"],
            milestones=[
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "optician",  # substring match on event title
                                    "start_datetime_iso": "2024-08-02T14:30",  # substring match on start datetime,
                                    "creation_datetime_iso": "2024-07-29T10:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_e753260e-a505-4ae3-aeac-ad4b29bcc19d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-02T14:00:00-07:00",
            is_read_time="2024-08-02T14:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You are running late to your optician appointment and need to let them know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to the eye people and tell them Hi sorry but I'll be 15 minutes or so late to my appointment is that alright?.",
                },
            ],
            reasoning='The user is asking to send a message. \nFirst, I should identify who the intended recipient is. The user has specified "eye people", I cannot see any matches in their saved contacts. I will search their message history. I can see one potential match, a conversation with optician@example.com. This is the only potential match. I will now draft the message as instructed.\nA message stating "Hi sorry but I\'ll be 15 minutes or so late to my appointment is that alright?" will be sent to optician@example.com',
            success_conditions=[
                {
                    "input_text": '1. A message is sent to optician@example.com stating "Hi sorry but I\'ll be 15 minutes or so late to my appointment is that alright?"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_messages", "send_message", "search_messages"],
            milestones=[
                # Milestone 0 – Agent looks through message history to identify the “eye people”
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
                    ]
                ),
                # Milestone 1 – The previous tool call returned a thread that contains the optician address
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
                                            # We only need to confirm that the optician address appears
                                            "participants_addresses": {
                                                "value": "optician@example.com",
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
                    ]
                ),
                # Milestone 2 – A new outgoing message is sent to the optician with the correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        ["optician@example.com"]
                                    ],
                                    "content": "15 minutes",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-08-02T14:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_subset_match_similarity,
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_bb497869-d7e1-4916-972a-e67effb77ca7_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:15:00-07:00",
            is_read_time="2024-07-29T10:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to create an event to signify the optician's appointment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Create an event called "Optician\'s Appointment" at 14:30-15:30 this Friday. ',
                },
            ],
            reasoning='Ok so the user wants to create an event called "Optician\'s Appointment" at 14:30-15:30 this Friday. First is the name which is given to us by the user. Next is the time frame which is also given to us by the user.  I will now create the event "Optician\'s Appointment" at 14:30-15:30 on 2 August. ',
            success_conditions=[
                {
                    "input_text": '1. The event "Optician\'s Appointment" is created at 14:30-15:30 on 2 August. ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Verify that a new calendar entry for the optician’s appointment
                #                on Friday 2 Aug 2024 14:30-15:30 was created.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Optician's Appointment",
                                    "start_datetime_iso": "2024-08-02T14:30",  # substring match, timezone-flexible
                                    "end_datetime_iso": "2024-08-02T15:30",
                                    "creation_datetime_iso": "2024-07-29T10:15:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_38a2d9e2-c767-45f4-8d97-f6b7026bae01_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:30:00-07:00",
            is_read_time="2024-07-29T10:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to create a new calendar event for your upcoming optician appointment which is one hour long. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Create a calendar event based on the medical confirmation text I got this morning.",
                },
            ],
            reasoning="The user is asking me to schedule a new event.\nThey have asked me to base this on a message they received. The user has mentioned a medical confirmation, this can narrow my search of their messages. \nI can see only one potential match, the message received from optician@example.com on July 29, 2024 10:10. This text provides a time and date for the proposed event. I am confident that this is the message being referred to.\nA new calendar event called Optician Appointment is set for August 2nd 2024 at 14:30",
            success_conditions=[
                {
                    "input_text": "1. A new calendar event called optician appointment is set for August 2nd 2024 at 14:30",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – The agent searches the user’s messages to locate the optician confirmation
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
                # Milestone 1 – Confirm the optician message (containing the appointment details) was actually returned
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
                                                "value": "optician@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "August 2nd at 14:30",
                                                "partial": True,  # only need substring match
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
                            reference_milestone_node_index=0,  # depend on the search in milestone 0
                        ),
                    ],
                ),
                # Milestone 2 – Verify a new calendar event for the optician appointment was added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "optician appointment",
                                    "start_datetime_iso": "2024-08-02T14:30",
                                    "creation_datetime_iso": "2024-07-29T10:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # Flexible matching: only require substrings to avoid timezone-offset issues
                                "calendar_event_name": column_rouge_l_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against the initial snapshot
                        ),
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_38a2d9e2-c767-45f4-8d97-f6b7026bae01_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:30:00-07:00",
            is_read_time="2024-07-29T10:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to create a new calendar event for your upcoming optician appointment which is one hour long. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Make a new calendar event called opticians appointment on August 2nd 2024 at 14:30",
                },
            ],
            reasoning="The user is asking me to create a new calendar event. \nFirst, I will look ahead and ensure this will not result in a clash. I can see no potential clashes.\nI will go ahead and schedule the event as requested.\nA new calendar event called Optician Appointment is set for August 2nd 2024 at 14:30.",
            success_conditions=[
                {
                    "input_text": "1. A new calendar event called optician appointment is set for August 2nd 2024 at 14:30",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent checks existing calendar events to avoid conflicts
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
                # Milestone 1 – A new calendar event for the optician appointment is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "optician",
                                    "start_datetime_iso": "2024-08-02T14:30",
                                    "creation_datetime_iso": "2024-07-29T10:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to pre-task state
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_e753260e-a505-4ae3-aeac-ad4b29bcc19d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-08-02T14:00:00-07:00",
            is_read_time="2024-08-02T14:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You are running late to your optician appointment and need to let them know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a message reply to opticians office saying "Hi sorry but I\'ll be 15 minutes or so late to my appointment is that alright?"',
                },
            ],
            reasoning="The user wants to dictate a reply to the user's optician's office.\nI search for the keyword \"optician's\" in the user's message history and find a match for the following email: optician@example.com\nI should locate the message history with this contact by searching the email in the user's Messages and then start a draft reply.\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\nI will then send the message if the user confirms that the message was transcribed correctly.\n",
            success_conditions=[
                {
                    "input_text": '1. A message is sent to optician@example.com stating "Hi sorry but I\'ll be 15 minutes or so late to my appointment is that alright?"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_messages", "send_message", "search_messages"],
            milestones=[
                # Milestone 0 – The agent looks up the existing conversation / messages with the optician
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
                # Milestone 1 – Verify the optician thread was actually found in the previous tool call
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
                                                "value": "optician@example.com",
                                                "partial": False,
                                            },
                                            "participants_addresses": {
                                                "value": "optician@example.com",
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
                # Milestone 2 – A new message is sent to the optician stating the user will be ~15 minutes late
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        ["optician@example.com"]
                                    ],
                                    "content": "15 minutes",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-08-02T14:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_subset_match_similarity,
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_bb497869-d7e1-4916-972a-e67effb77ca7_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:15:00-07:00",
            is_read_time="2024-07-29T10:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to create an event to signify the optician's appointment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set up an appointment for one-hour at the optician's based on the confirmed time in the message.",
                },
            ],
            reasoning="Ok so the user wants to set up an hour at the optician's from the time in the message. Let's first find the messages they are referring to. From recent correspondence, they were most recently in contact with the optician which lines up with what they are requesting. In these messages we get a confirmation message which includes the date. I can now work with this in mind. Next, I will pick a name for the event which I will keep clear and to the point. I will call the event \"Optician's Appointment.\" Next is the timeframe. The messages referenced give a date and time and the user wishes to set aside an hour for it. I will now create the event \"Optician's Appointment\" at 14:30-15:30 on 2 August. ",
            success_conditions=[
                {
                    "input_text": '1. The event "Optician\'s Appointment" is created at 14:30-15:30 on 2 August. ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 — The agent queries the messages to locate the appointment details
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
                # Milestone 1 — Confirm the message from the optician that contains the Aug 2 14:30 appointment was indeed returned
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
                                                "value": "optician@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "August 2nd at 14:30",
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
                # Milestone 2 — A calendar event for the optician appointment has been added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "optician",
                                    "start_datetime_iso": "2024-08-02T14:30:00-07:00",
                                    "end_datetime_iso": "2024-08-02T15:30:00-07:00",
                                    "creation_datetime_iso": "2024-07-29T10:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,  # allow slight wording variation but must include "Optician"
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieved messages → confirmed correct message
                (1, 2),  # Confirmed message → created calendar event
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_6bce2223-3758-4b2c-9325-22bfa6feaaed_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "calendar",
                "messaging",
                "email",
                "whatsapp_messaging",
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
                        "You want got make sure you are available Friday at 14:30 before confirming your appointment with the optician. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Do I have anything happening or confirmed this Friday during my potential appointment? Yes or No.",
                },
            ],
            reasoning='The user wants to know if they have any events scheduled for Friday during their appointment. I need to first confirm when their appointment is. I searched calendar and messages, found a message from "optician@example.com" with content "Hello Theo, this is a reminder that you have an appointment scheduled with us on Friday, August 2nd at 14:30. Please confirm your availability.". So I only need to check for other events around that time. There are no events for Friday. I shall inform user with No. ',
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "User has been informed 'No', since calendar is searched for any events that are or are not taking place on Friday, August 2 at 14:30.",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "search_messages",
                "get_all_messages",
                "search_emails",
                "get_all_emails",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent searches messages for appointment confirmation
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
                # Milestone 1 – Agent finds optician appointment confirmation
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
                                                "value": "optician@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "August 2nd at 14:30",
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
                # Milestone 2 – Agent checks the calendar for events on Friday during the appointment
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
                # Milestone 3 – User is informed they have a confirmed optician appointment / are unavailable
                Milestone(
                    snapshot_constraints=[
                        # Must mention the existing appointment or being unavailable
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
                                "content": column_word_contains_similarity,
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2), (2, 3)],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_4ee48699-11d7-4173-b141-79812b90dbad_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T11:00:00-07:00",
            is_read_time="2024-07-29T11:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to see the last message from optician@example.  com. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show the last message from optician@example.com .",
                },
            ],
            reasoning="The user wants to see optician@example.com's last message. Let me look for them in contacts. I will look for the last message they sent. I will show it to the user.",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last message sent from optician@example.com on July 29th at 10:10 : 'Thank you, Theo. We have confirmed your appointment for August 2nd at 14:30. We look forward to seeing you then.'",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
            milestones=[
                # Milestone 0 – Agent uses a message-retrieval tool to find messages
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
                    ]
                ),
                # Milestone 1 – Tool output includes the expected last message from optician@example.com
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
                                                "value": "optician@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "We have confirmed your appointment for August 2nd at 14:30",
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
                # Milestone 2 – Agent tells the user the correct message content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("confirmed", "August 2")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_all_similarity
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieval tool call → verify correct message found
                (1, 2),  # Correct message found → agent delivers it to user
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_320121ba-9947-44ed-a341-e011419234f6_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T11:00:00-07:00",
            is_read_time="2024-07-29T11:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to create a calendar event for your upcoming optician appointment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Put down that eye thing I was just texted about for Friday, August 2nd, 2024 at 14:30.",
                },
            ],
            reasoning="User wants a date and time for something noted. This indicates calendar to me. I see from texts that user has an Optician Appointment scheduled at the time user indicated. I shall create a calendar event with these details. ",
            success_conditions=[
                {
                    "input_text": "A calendar event is created for optician appointment Friday, August 2nd, 2024 at 14:30.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – the agent looks through the user’s messages to locate the
                # optician text that mentions the appointment time
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
                # Milestone 1 – confirm that the message thread from the optician and the
                # correct appointment details were actually surfaced by the previous tool call
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
                                            # identify the optician conversation
                                            "conversation_name": {
                                                "value": "optician@example.com",
                                                "partial": False,
                                            },
                                            # make sure the content mentions the confirmed
                                            # date and time
                                            "content": {
                                                "value": "appointment for August 2nd at 14:30",
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
                # Milestone 2 – the calendar event for the optician appointment has been created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # title could vary (eye thing / optician / eye exam);
                                    # we only need to know that it's related to the optician
                                    "calendar_event_name": "appointment",
                                    "start_datetime_iso": "2024-08-02T14:30:00",
                                    "creation_datetime_iso": "2024-07-29T11:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                # timezone could be appended (e.g., -07:00); match the
                                # date-time prefix
                                "start_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # messages were searched → confirm correct message found
                (1, 2),  # correct message found → calendar event created
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_320121ba-9947-44ed-a341-e011419234f6_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T11:00:00-07:00",
            is_read_time="2024-07-29T11:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to create a calendar event for your upcoming optician appointment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Create a calendar event with the following details: Optician appointment Friday, August 2nd, 2024 at 14:30.",
                },
            ],
            reasoning="Use has provided me with all details necessary to create a calendar event for optician appointment on Friday Aug. 2nd at 14:30. \n\nI will create the appointment. ",
            success_conditions=[
                {
                    "input_text": "A calendar event is created for optician appointment Friday, August 2nd, 2024 at 14:30.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "create_calendar_event",
            ],
            milestones=[
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # The event name must reference the optician appointment
                                    "calendar_event_name": "Optician",
                                    # Start-time must include 2024-08-02 14:30
                                    "start_datetime_iso": "2024-08-02T14:30",
                                    "creation_datetime_iso": "2024-07-29T11:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial state
                        ),
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_80af89f5-0a7a-4f79-8736-d4434c04ad94_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
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
                        "You want to send a message to your optician to confirm an appointment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to the optician saying 'Thank you for the reminder. I confirm my appointment for August 2nd at 14:30.'",
                },
            ],
            reasoning="The user wants to send a message to their optician. I'll check the user's contacts for a contact under this title. I'm not seeing a contact under this name, so I'll check messages. The user has several messages with a contact under the title 'Optician' sent from the following email address: optician@example.com. I'll use that address, as it is the closer I can see connected to an optician. The user wants to say the following: 'Thank you for the reminder. I confirm my appointment for August 2nd at 14:30.'. Now that I have the content of the message I can send it and notify the user.",
            success_conditions=[
                {
                    "input_text": "1. A message is sent to the optician saying 'Thank you for the reminder. I confirm my appointment for August 2nd at 14:30.'",
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
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent looks for the optician conversation
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
                # Milestone 1 – The previous search returned the reminder message from the optician
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
                                            # Ensure the conversation found involves the optician
                                            "participants_addresses": {
                                                "value": "optician@example.com",
                                                "partial": True,
                                            },
                                            # And that the reminder text about the appointment is present
                                            "content": {
                                                "value": "August 2nd",
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
                # Milestone 2 – A confirmation message was sent to the optician
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
                                                "optician@example.com",
                                            ),  # optician - external, email only
                                            (
                                                "theo.appleseed@example.com",
                                                "1234-5678-9101",
                                            ),  # Theo - email or phone
                                        ]
                                    ],
                                    "content": "Thank you for the reminder. I confirm my appointment for August 2nd at 14:30.",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-29T10:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_contains_similarity,  # key phrasing must appear
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial database state
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # search → verify retrieved reminder
                (1, 2),  # verification → message sent
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_af7916da-656f-46e3-a127-52fb7a2e9633_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:15:00-07:00",
            is_read_time="2024-07-29T10:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to schedule an opticians appointment on Friday August 2nd 2024 at 14:30 in your calendar, since you forgot to add it in already. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "My optician sent me a text with my appointment details can you add that to my calendar",
                },
            ],
            reasoning='The user wants to add the appointment details he received from his optician by text to his calendar. I need to determine who the user is referring to. Looking through their messages I can see that the user received a message from optician@example.com confirming their appointment for Friday August 2nd 2024 at 2:30pm. I will add "Optician Appointment" to the user\'s calendar for this time.',
            success_conditions=[
                {
                    "input_text": '1. "Optician Appointment" is scheduled on Friday August 2nd 2024 at 14:30 in the calendar ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks through messages to find the optician’s appointment details
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
                # Milestone 1 – Confirm that a message containing the August 2 14:30 appointment was indeed returned
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
                                            # Only need to know the message text mentions Aug 2 and 14:30
                                            "content": {
                                                "value": "August 2",
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
                # Milestone 2 – A new calendar event for the optician appointment is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Optician",  # substring check
                                    "start_datetime_iso": "2024-08-02T14:30",  # substring check,
                                    "creation_datetime_iso": "2024-07-29T10:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against the initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_78ae5dca-8738-4e47-942b-dea1cdcccffb_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T12:00:00-07:00",
            is_read_time="2024-07-29T12:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to add the optician appointment to your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Make a new event called optician appointment on the date and time that I got in the text, make it last an hour.",
                },
            ],
            reasoning="The user is asking me to schedule a new event.\nI should look forward and ensure this will not result in a clash before proceeding. \nI can see no potential clashes.\nThe user has indicated that the date and time for this event is in a text they received. The name given for the event can be used to narrow my search.\nI see one potential message match, received from optician@example.com on July 29, 2024 at 10:10. This message indicates a date and time.\nI am confident that this is the correct message.\nI will make a new event called optician appointment for 2 August 2024 from 14:30 to 15:30.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1) New event Optician Appointment is scheduled for August 2, 2024 at 14:30-15:30.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 — The agent looks through messages to find the appointment information
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
                # Milestone 1 — Confirm that the returned message actually contains the optician appointment details
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
                                                "value": "optician@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "August 2",
                                                "partial": True,  # allow any wording that includes the date
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
                # Milestone 2 — A new calendar event for the optician appointment was created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "optician",  # we just need to contain the keyword
                                    "start_datetime_iso": "2024-08-02T14:30",
                                    "end_datetime_iso": "2024-08-02T15:30",
                                    "creation_datetime_iso": "2024-07-29T12:00:00-07:00",
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
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # message search -> confirm correct message
                (1, 2),  # confirmed info -> calendar event creation
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_d77ba7ca-0da1-4445-b0b1-05ff1b1d68ca_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:15:00-07:00",
            is_read_time="2024-07-29T10:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know if you got a text response from your Optician's. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did the eye people text back? ",
                },
            ],
            reasoning="The user wants to know if the \"eye people\" texted back. I should search their messages for a message from this sender. I can't see any sender with that name. I do see a message from optician@example.com received today, July 29th at 10:10. The user is probably referring to this sender. I'll show the user this message. ",
            success_conditions=[
                {
                    "input_text": '1. Messages are checked for a message from the "eye people" and returns the message received from optician@example.com on July 29th at 10:10. ',
                    "statefullness": "Stateless",
                },
                {
                    "statefullness": "Stateless",
                    "input_text": "2. The message is shown to the user. ",
                },
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
            milestones=[
                # Milestone 0 – Agent looks through messages (either search or full retrieval)
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
                # Milestone 1 – The retrieved message includes the one from the optician confirming the appointment
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
                                                "value": "optician@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "confirmed your appointment",
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
                # Milestone 2 – The agent tells the user that the optician replied / shows the message
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
                                            "August 2",
                                            "Aug. 2",
                                            "confirmed your appointment",
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
                (0, 1),  # messages searched → confirmation message found
                (1, 2),  # confirmation message found → user informed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_7122d9dc-5eab-4d3b-95c4-6e7dc77121aa_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T11:45:00-07:00",
            is_read_time="2024-07-29T11:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to add your optician appointment to your calendar "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Put opticians appointment on Friday August 2 at 14:30",
                },
            ],
            reasoning="The user does not explicitly mention that they want a calendar event but saying the date and time makes it clear that is the user's intent",
            success_conditions=[
                {
                    "input_text": "A calendar event is created for appointment with optician On August the 2nd at 14:30. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["create_calendar_event"],
            milestones=[
                # Milestone 0 – Verify that a calendar event representing the optician
                # appointment has been added for August 2 2024 at 14:30
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # We only verify fields we are certain about.
                                    # The event name just needs to contain “optician”.
                                    "calendar_event_name": "optician",
                                    # Verify the start-date string contains the right date & time
                                    "start_datetime_iso": "2024-08-02T14:30",
                                    "creation_datetime_iso": "2024-07-29T11:45:00-07:00",
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
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_4c0e6435-0d06-4353-87a9-e4cbc33a48aa_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:15:00-07:00",
            is_read_time="2024-07-29T10:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to add your optician appointment to your calendar according to the information in the confirmation text you received. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Make an optician appointment at 2:30 PM on the 2nd of August.",
                },
            ],
            reasoning="The user wants to make an event, so I'll go to their calendar.\n\nThe user has provided me with the event name: Optician Appointment; the date: 2024-08-02; and the start time: 14:30. With this information, I can go ahead and create the event.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. An optician appointment is created at 14:30 on 2024-08-02.",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – A new calendar event for the optician appointment has been created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Optician Appointment",
                                    "start_datetime_iso": "2024-08-02T14:30",
                                    "creation_datetime_iso": "2024-07-29T10:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_rouge_l_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_0b3e8760-0a35-4765-93fd-6fd4119a4312_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:04:00-07:00",
            is_read_time="2024-07-29T10:04:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what the opticians said in their recent message to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read out my last received message.",
                },
            ],
            reasoning="Right, so the user wants me to read out their last received message. From their message threads I can see the last one received is from 'optician@example.com' on 29th July at 10:00 saying 'Hello Theo, this is a reminder that you have an appointment scheduled with us on Friday, August 2nd at 14:30. Please confirm your availability.' I can read out this message to the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The message from 'optician@example.com' received on 29th July at 10:00 saying 'Hello Theo, this is a reminder that you have an appointment scheduled with us on Friday, August 2nd at 14:30. Please confirm your availability.' is read out to the user.",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – Agent invokes a message-retrieval tool
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
                # Milestone 1 – The retrieved message set includes the optician reminder
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
                                                "value": "optician@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "appointment",
                                                "partial": True,  # allow any phrasing containing “appointment”
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
                # Milestone 2 – Agent tells the user the essentials of the message (includes the time 14:30)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("14:30", "2:30 pm", "2:30pm")],
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
            name="THEO_APPLESEED_27_0b3e8760-0a35-4765-93fd-6fd4119a4312_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:04:00-07:00",
            is_read_time="2024-07-29T10:04:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what the opticians said in their recent message to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What did the optician say?",
                },
            ],
            reasoning="Okay, so the user wants to know what the 'optician' said. I can see one message matching this, received from 'optician@example.com' on the 29th July at 10:00 saying 'Hello \nTheo, this is a reminder that you have an appointment scheduled with us on Friday, August 2nd at 14:30. Please confirm your availability.'. I can then read this out to the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The message from 'optician@example.com' received on 29th July at 10:00 saying 'Hello Theo, this is a reminder that you have an appointment scheduled with us on Friday, August 2nd at 14:30. Please confirm your availability.' is read out to the user.",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – the agent uses a messaging-retrieval tool
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
                    ]
                ),
                # Milestone 1 – confirm the optician’s message was retrieved in Milestone 0
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
                                                "value": "optician@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "appointment scheduled with us on Friday, August 2nd at 14:30",
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
                # Milestone 2 – the agent tells the user what the optician said
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
                                            "14:30",
                                            "2:30",
                                            "2:30 pm",
                                            "2:30pm",
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
            name="THEO_APPLESEED_27_4c0e6435-0d06-4353-87a9-e4cbc33a48aa_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:15:00-07:00",
            is_read_time="2024-07-29T10:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to add your optician appointment to your calendar according to the information in the confirmation text you received. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Create an event using the details in the texts from the optician.",
                },
            ],
            reasoning="The user wants to create an event using details from the optician's text. I'll need to find that text to get the information.\n\nI can't see any contacts named Optician, so I'll go to Messages.\n\nI found a message thread from Optician (optician@example.com). Great, now I'll check the messages for any event details.\n\nThere is a message that was received at 10:10 on 2024-07-29 that says \"Thank you, Theo. We have confirmed your appointment for August 2nd at 14:30. We look forward to seeing you then.\" From this message, I can create an event called Optician Appointment on 2024-08-02 at 14:30.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. Event titled Optician Appointment is created at 14:30 on 2024-08-02.",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks through the user’s messages to find the
                # confirmation text from the optician.
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
                # Milestone 1 – Confirm that the tool call in Milestone 0 actually returned
                # the optician confirmation from optician@example.com containing the key
                # details "August 2nd at 14:30".
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
                                                "value": "optician@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "August 2nd at 14:30",
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
                # Milestone 2 – Verify that a new calendar event for the optician
                # appointment was created on 2024-08-02 at 14:30.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Optician Appointment",
                                    "start_datetime_iso": "2024-08-02T14:30",
                                    "creation_datetime_iso": "2024-07-29T10:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_rouge_l_similarity,  # accept slight wording variants but must include “Optician”
                                "start_datetime_iso": column_contains_similarity,  # just needs to include the correct date/time substring,
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
            name="THEO_APPLESEED_27_7122d9dc-5eab-4d3b-95c4-6e7dc77121aa_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "calendar",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T11:45:00-07:00",
            is_read_time="2024-07-29T11:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to add your optician appointment to your calendar "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Add an event for Friday August 2 at 14:30 in the confirmation texts from the optical shop.",
                },
            ],
            reasoning='The user wants to make an event for Friday August 2 at 14:30 for "the guys who make glasses" which is the job of an optician',
            success_conditions=[
                {
                    "input_text": "A calendar event is created for appointment with optician On August the 2nd at 14:30. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "create_calendar_event",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks through the user’s messages to find the appointment details
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
                # Milestone 1 – Confirm that a message containing the appointment on August 2 at 14:30 was actually returned
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
                                                "value": "optician@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "August 2nd at 14:30",
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
                # Milestone 2 – A new calendar event for the optician appointment is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "appointment",
                                    "start_datetime_iso": "2024-08-02T14:30",
                                    "creation_datetime_iso": "2024-07-29T11:45:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,  # must reference “optician” (or similar substring)
                                "start_datetime_iso": column_contains_similarity,  # must include the correct date-time substring,
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
                (0, 1),  # First find the relevant message → then confirm content
                (1, 2),  # After confirming, create the calendar event
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_af7916da-656f-46e3-a127-52fb7a2e9633_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:15:00-07:00",
            is_read_time="2024-07-29T10:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You remember you have an opticians appointment on Friday August 2nd 2024, but you forgot exactly when. You want the agent to look it up for you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to add my confirmed eye check for Friday August 2nd 2024 in my calendar, but I forgot when, try to look it up",
                },
            ],
            reasoning='The user wants to add a confirmed eye check for Friday August 2nd in their calendar. The user hasn\'t mentioned what time the appointment begins at. I can see in their messages the user received a message from optician@example.com confirming their appointment for Friday August 2nd 2024 at 2:30pm. I will add an event titled "Optician Appointment" or "eye check" to the user\'s calendar for this time.',
            success_conditions=[
                {
                    "input_text": "1. the event about Optician Appointment is scheduled on Friday August 2nd 2024 at 14:30 in the calendar ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "get_all_emails",
                "search_emails",
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent searches the user’s messages to locate the optician confirmation
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
                # Milestone 1 – Confirm the optician message (containing the appointment details) was actually returned
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
                                                "value": "optician@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "August 2nd at 14:30",
                                                "partial": True,  # only need substring match
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
                            reference_milestone_node_index=0,  # depend on the search in milestone 0
                        ),
                    ],
                ),
                # Milestone 2 – A new calendar event for the optician appointment is added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": [("eye", "optician")],
                                    "start_datetime_iso": "2024-08-02T14:30",
                                    "creation_datetime_iso": "2024-07-29T10:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_str_contains_any_similarity,
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
            milestone_edge_list=[
                (0, 1),  # Agent checks messages
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_27_78ae5dca-8738-4e47-942b-dea1cdcccffb_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_27",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T12:00:00-07:00",
            is_read_time="2024-07-29T12:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to add the optician appointment to your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Make a new event called optician appointment for 2 August 2024 from 14:30 to 15:30.",
                },
            ],
            reasoning="The user is asking me to schedule a new event.\nI should look forward and ensure this will not result in a clash before proceeding. \nI can see no potential clashes.\nI will make a new event called optician appointment for 2 August 2024 from 14:30 to 15:30.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1) New event Optician Appointment is scheduled for August 2, 2024 at 14:30-15:30.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – verify the new calendar event has been created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "optician appointment",
                                    "start_datetime_iso": "2024-08-02T14:30",
                                    "end_datetime_iso": "2024-08-02T15:30",
                                    "creation_datetime_iso": "2024-07-29T12:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # Allow case/substring differences and possible timezone offsets
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against the initial state
                        )
                    ]
                ),
                # Milestone 1 – agent informed the user about scheduling the appointment
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Any reasonable confirmation that mentions the optician appointment
                                    "content": [("optician", "Optician")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
    ]
