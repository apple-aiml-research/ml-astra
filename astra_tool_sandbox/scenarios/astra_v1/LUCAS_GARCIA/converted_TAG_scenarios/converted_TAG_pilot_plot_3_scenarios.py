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
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_rouge_l_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    contains_presence_similarity,
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


def get_TAG_LUCAS_GARCIA_pilot_plot_3(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="LUCAS_GARCIA_3_3ad31229-72e1-4031-bd65-cbfd11cf0ebc_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T19:30:00-08:00",
            is_read_time="2024-12-02T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You're eager to know if your gym buddy Theo got back to you about your gym session suggestion. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I get a reply from my gym buddy?",
                },
            ],
            reasoning="The user wants to know if they got a reply from my gym buddy. I wonder who they mean. I should check their contacts to try to figure it out. I see that Theo Appleseed is listed as a gym buddy so I think it must be him. Okay, I'll check for a new message from Theo Appleseed. I see one new message from Theo Appleseed, received on December 2nd, 2024, at 19:25. I'll show that message to the user now. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The message from Theo Appleseed, received on December 2nd, 2024, at 19:25, is shown to the user. ",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks through messages to find any reply from the gym buddy
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
                # Milestone 1 – Confirm that the expected message from Theo Appleseed (gym buddy) was
                # returned in the tool output captured in Milestone 0
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
                                                "value": "Theo Appleseed",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Perfect.",
                                                "partial": True,  # allow substring match
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-02T19:25:00-08:00",
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
                # Milestone 2 – The agent’s response to the user shows (quotes or includes) the
                # message from Theo so the user can read it
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Perfect.",
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
                (0, 1),  # message-search → verify Theo’s reply found
                (1, 2),  # verified reply → user is shown the message
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_61c36a19-14d7-4a3a-9a79-ca73fb18393c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "calendar",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T17:45:00-08:00",
            is_read_time="2024-12-02T17:45:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to send a message to Theo saying 'Hey man I'm gonna be 10 minutes late, sorry traffic is terrible!'. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Message who my next event is with saying 'Hey man I'm gonna be 10 minutes late, sorry traffic is terrible!'.",
                },
            ],
            reasoning="Right so, the user is looking to message a contact who will be at their next event. Firstly, checking their calendar, I can see that the next event is 'Evening Workout Session with Theo', which is scheduled for today, 2 December 2024 at 18:00 with 'Theo Appleseed' listed as an attendee. 'Theo' is who the user would like to send the message to. They have given me the message content which reads 'Hey man I'm gonna be 10 minutes late, sorry traffic is terrible!'. Now that I have all the information, I can draft up the message and confirm with the user that no further changes are needed, and then can send the message to 'Theo'.",
            success_conditions=[
                {
                    "input_text": "1. A message is sent to 'Theo Appleseed' on 2 December 2024 at 17:45 saying 'Hey man I'm gonna be 10 minutes late, sorry traffic is terrible!'.",
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
                "get_all_calendars",
                "search_calendar_events",
                "send_message",
            ],
            milestones=[
                # Milestone 0 –  Agent looks up the user’s next calendar event
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
                # Milestone 1 –  Confirm the “Evening Workout Session with Theo” event (18:00) was found
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
                                                "value": "Evening Workout Session with Theo",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-02T18:00:00-08:00",
                                                "partial": False,
                                            },
                                            "attendees_names": {
                                                "value": [
                                                    "Lucas Garcia",
                                                    "Theo Appleseed",
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
                # Milestone 2 –  Agent looks up the contact information for Theo
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
                # Milestone 3 –  Confirm contact result includes “Theo Appleseed”
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
                                                "value": "Theo Appleseed",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 12345-6789-1000-5678",
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
                # Milestone 4 –  Message is sent to Theo with correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At minimum, the message must include Theo’s phone or email
                                    "conversation_name": "Theo Appleseed",
                                    "content": "10 minutes late",
                                    "creation_datetime_iso": "2024-12-02T17:45:00-08:00",
                                }
                            ),
                            column_similarity_measure={
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
                (0, 1),  # Calendar lookup → confirm event
                (2, 3),  # Contact lookup → confirm Theo
                # Message sending (Milestone 4) depends logically on finding Theo but does not need explicit graph edge
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_990bc6ae-43dd-4212-b673-b6e50312d859_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T19:30:00-08:00",
            is_read_time="2024-12-02T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to send a text message in the chat you are having with Theo Appleseed. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a text to Theo Appleseed saying: By the way, Theo, there's something else I want to smash in the new year, and it's prejudice and unfair business practices. Just want you to know that. ",
                },
            ],
            reasoning="User has provided the content for a text and the intended recipient. I shall prepare ans send it as instructed. ",
            success_conditions=[
                {
                    "input_text": "A text message is sent in the chat with Theo Appleseed saying, By the way, Theo, there's something else I want to smash in the new year, and it's prejudice and unfair business practices. Just want you to know that. ",
                    "statefullness": "Stateful",
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
                # Milestone 0 – The agent looks up either the contact or the existing conversation
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
                                        "search_messages",
                                        "get_all_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – A new message is added to the Theo Appleseed conversation
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require both Lucas and Theo to be present, matched by either email or phone,
                                    # and no unexpected extra participants.
                                    "participants_addresses": [
                                        [
                                            (
                                                "lucas.garcia@example.com",
                                                "+1 12345-6789-1000-1234",
                                            ),
                                            (
                                                "theo.appleseed@example.com",
                                                "+1 12345-6789-1000-5678",
                                            ),
                                        ]
                                    ],
                                    "content": "prejudice and unfair business practices",
                                    "creation_datetime_iso": "2024-12-02T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with pre-task state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_fed4d92a-6d4d-49dd-ac6e-20a8d7844195_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T19:30:00-08:00",
            is_read_time="2024-12-03T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to dictate a reply message to Theo Appleseed . "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a reply message to Theo Appleseed saying "Hey did you get a chance to look at those times in your calendar yet?".',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Theo Appleseed.\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": '1. A reply message is sent to Theo Appleseed saying "Hey did you get a chance to look at those times in your calendar yet?".',
                    "statefullness": "Stateful",
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
                # Milestone 0 – Agent tries to locate Theo Appleseed in the contacts list
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
                # Milestone 1 – Verify that Theo Appleseed is indeed returned from the contact-lookup in Milestone 0
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
                                                "value": "Theo Appleseed",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 12345-6789-1000-5678",
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
                # Milestone 2 – A new outgoing message to Theo is created with the dictated text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least one identifier for Theo must appear; extras (e.g. Lucas) are allowed
                                    "participants_addresses": [
                                        [
                                            (
                                                "+1 12345-6789-1000-5678",
                                                "theo.appleseed@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "Hey did you get a chance to look at those times in your calendar yet?",
                                    "creation_datetime_iso": "2024-12-03T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against pre-task snapshot
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
            name="LUCAS_GARCIA_3_fed4d92a-6d4d-49dd-ac6e-20a8d7844195_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T19:30:00-08:00",
            is_read_time="2024-12-03T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to dictate a reply message to Theo Appleseed . "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a reply message to gym buddy saying "Hey did you get a chance to look at those times in your calendar yet?".',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called gym buddy.\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply. I cannot see anyone named Gym Buddy in the user's contacts. I can see, however, that Theo Appleseed is tagged as gym buddy. This must be who the user is referring to.\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": '1. A reply message is sent to Theo Appleseed saying "Hey did you get a chance to look at those times in your calendar yet?".',
                    "statefullness": "Stateful",
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
                # Milestone 0 – Agent tries to locate “Gym Buddy” (Theo) in contacts
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
                # Milestone 1 – The returned contact information contains Theo Appleseed
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
                                                "value": "Theo Appleseed",
                                                "partial": False,
                                            },
                                            "alias": {
                                                "value": "Gym Buddy",
                                                "partial": True,
                                            },
                                            "phone_number": {
                                                "value": "+1 12345-6789-1000-5678",
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
                # Milestone 2 – A new message with the dictated text is sent to Theo
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
                                                "+1 12345-6789-1000-5678",
                                                "theo.appleseed@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "Hey did you get a chance to look at those times in your calendar yet?",
                                    "creation_datetime_iso": "2024-12-03T19:30:00-08:00",
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
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → verify Theo returned
                (1, 2),  # Theo identified → message sent
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_990bc6ae-43dd-4212-b673-b6e50312d859_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T19:30:00-08:00",
            is_read_time="2024-12-02T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to send a text message in the chat you are having with Theo Appleseed. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a text to Gym Buddy saying: By the way, Theo, there's something else I want to smash in the new year, and it's prejudice and unfair business practices. Just want you to know that. ",
                },
            ],
            reasoning="User has provided the content for a text and the intended recipient. I shall prepare ans send it as instructed. ",
            success_conditions=[
                {
                    "input_text": "A text message is sent in the chat with Theo Appleseed saying, By the way, Theo, there's something else I want to smash in the new year, and it's prejudice and unfair business practices. Just want you to know that. ",
                    "statefullness": "Stateful",
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
                # Milestone 0 – Verify a new message was sent to Theo Appleseed that contains the requested text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Both Lucas (the user) and Theo must be in the conversation.
                                    # Either their e-mail or phone identifier is acceptable.
                                    "participants_addresses": [
                                        [
                                            (
                                                "lucas.garcia@example.com",
                                                "+1 12345-6789-1000-1234",
                                            ),
                                            (
                                                "theo.appleseed@example.com",
                                                "+1 12345-6789-1000-5678",
                                            ),
                                        ]
                                    ],
                                    # Check that the message body references the key phrase
                                    "content": "prejudice and unfair business practices",
                                    "creation_datetime_iso": "2024-12-02T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_61c36a19-14d7-4a3a-9a79-ca73fb18393c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "calendar",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T17:45:00-08:00",
            is_read_time="2024-12-02T17:45:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to send a message to Theo saying 'Hey man I'm gonna be 10 minutes late, sorry traffic is terrible!'. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Message Theo saying 'Hey man I'm gonna be 10 minutes late, sorry traffic is terrible!'.",
                },
            ],
            reasoning="Okay so, the user wants to message 'Theo' with the message content 'Hey man I'm gonna be 10 minutes late, sorry traffic is terrible!'. First, from checking the user's contacts, I can see only one 'Theo', 'Theo Appleseed'. This is who the user wants to message. As they have given me the message content, I will draft up the message and confirm with the user that no further changes are required before sending the message off.",
            success_conditions=[
                {
                    "input_text": "1. A message is sent to 'Theo Appleseed' on 2 December 2024 at 17:45 saying 'Hey man I'm gonna be 10 minutes late, sorry traffic is terrible!'.",
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
                "get_all_calendars",
                "search_calendar_events",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent looks up Theo in the contacts list
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
                # Milestone 1 – Confirm the contact lookup returned Theo Appleseed
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
                                                "value": "Theo Appleseed",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 12345-6789-1000-5678",
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
                            reference_milestone_node_index=0,  # Parse result from Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – Message to Theo was sent with the correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Theo Appleseed",
                                    "content": "Hey man I'm gonna be 10 minutes late, sorry traffic is terrible!",
                                    "creation_datetime_iso": "2024-12-02T17:45:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # Compare against initial DB state
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
            name="LUCAS_GARCIA_3_1ea3e5af-9636-45a3-8bc6-be674a3db9e7_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T19:30:00-08:00",
            is_read_time="2024-12-02T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        'You want to message Theo Appleseed saying "Sorry, I meant to say Mondays Wednesdays and Sundays, not Fridays" '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Oops I need to correct the message I\'ve sent earlier, send him the message "Sorry, I meant to say Mondays Wednesdays and Sundays, not Fridays"',
                },
            ],
            reasoning="The user wants to send another message to correct the message they have sent earlier without specifying who is the recipients. From the message history it can be seen that it was Theo Appleseed, since they were discussing a schedule. I will go ahead and send the message based on the user provided content.",
            success_conditions=[
                {
                    "input_text": 'A message is sent to Theo Appleseed saying "Sorry, I meant to say Mondays Wednesdays and Sundays, not Fridays"',
                    "statefullness": "Stateful",
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
                # Milestone 0 – The agent looks up either the contact or the existing conversation
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
                # Milestone 1 – Confirm the contact lookup returned Theo Appleseed
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
                                                "value": "Theo Appleseed",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "How about we aim for evening sessions on Mondays, Wednesdays, and Fridays around 6 pm",
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
                            reference_milestone_node_index=0,  # Parse result from Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – A new message with the correction is sent to Theo Appleseed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require that the conversation includes Lucas and Theo (via any valid identifier for each)
                                    "participants_addresses": [
                                        [
                                            (
                                                "lucas.garcia@example.com",
                                                "+1 12345-6789-1000-1234",
                                            ),
                                            (
                                                "theo.appleseed@example.com",
                                                "+1 12345-6789-1000-5678",
                                            ),
                                        ]
                                    ],
                                    # Key fragment of the corrective message
                                    "content": "Mondays Wednesdays and Sundays",
                                    "creation_datetime_iso": "2024-12-02T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Information retrieval precedes sending the corrective message
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_3ad31229-72e1-4031-bd65-cbfd11cf0ebc_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T19:30:00-08:00",
            is_read_time="2024-12-02T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You're eager to know if your gym buddy Theo got back to you about your gym session suggestion. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I get a reply from the gym bro?",
                },
            ],
            reasoning="The user wants to know if they got a reply from the gym bro. I wonder who they mean. I should check their contacts to try to figure it out. I see that Theo Appleseed is listed as a gym buddy. I know that \"bro\" is slang which sometimes used to describe a male friend or buddy so I think it must be him. Okay, I'll check for a new message from Theo Appleseed. I see one new message from Theo Appleseed, received on December 2nd, 2024, at 19:25. I'll show that message to the user now. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The message from Theo Appleseed, received on December 2nd, 2024, at 19:25, is shown to the user. ",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
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
                # Milestone 1 – Tool output contains Theo’s reply from 2024-12-02 19:25
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
                                                "value": "theo.appleseed@example.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-02T19:25:00-08:00",
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
                # Milestone 2 – Agent tells the user the content of Theo’s reply
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
                                            "Perfect",
                                            "Looking forward",
                                            "smashing those goals",
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
                (0, 1),  # Message retrieval → verify correct message in results
                (1, 2),  # Verified message → agent conveys it to the user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_f4ca239e-89f7-47a3-83ae-ddbf049741f3_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T15:00:00-08:00",
            is_read_time="2024-12-03T15:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to remember when you said you'd work out with Theo Appleseed. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the message I sent to Theo Appleseed with the new workout schedule.",
                },
            ],
            reasoning="The users wants me to find a specific message they sent to Theo Appleseed so I'll open up the chat between Theo and the user. I will narrow my search to only messages sent by the user unless other context clues are needed.\nI will check the contents of the messages for something that appears to be a schedule of some kind. \nI found one that was send on December 2nd 2024 at 19:20. I assume this is the message the user wants. I present this message tot the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The message sent to Theo Appleseed at 19:20 on December 02 2024 with the proposed new workout schedule is presented to the user.",
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
                # Milestone 1 – Tool output contains user sent information
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
                                                "value": "lucas.garcia@example.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-02T19:20:00-08:00",
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
                # Milestone 2 – Agent shows the user the correct workout-schedule message
                Milestone(
                    snapshot_constraints=[
                        # Must mention the schedule days
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Mondays, Wednesdays, and Fridays",
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
                (0, 1),  # Retrieval precedes user-facing response
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_8128e120-2c0e-4557-8edd-330b375d2291_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T19:30:00-08:00",
            is_read_time="2024-12-02T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to reply to Theo's message to tell him that it's great he's being so proactive about his fitness goals. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a reply to my gym buddy's message that says \"Fantastic! It's so great that you're being proactive about your fitness goals\"",
                },
            ],
            reasoning="The user wants me to send a reply to the gym buddy's message that says \"Fantastic! It's so great that you're being proactive about your fitness goals\". First thing I need to do is look at the user's messages and see if there any conversations with a gym buddy. I didn't find any so I will now look through the user's contacts to search for someone by that name. Ok I've found Theo Appleseed whose alias is gym buddy so that must be him. I will now search the user's conversations for Theo Appleseed.... I found it, so now I will find the most recent received message and draft a reply to it with the given text. Now that that's done, I will ask the user if it is ready to be sent.",
            success_conditions=[
                {
                    "input_text": "1. A new text message saying \"Fantastic! It's so great that you're being proactive about your fitness goals\" is sent to Theo Appleseed",
                    "statefullness": "Stateful",
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
                # Milestone 0 — Agent performs any reasonable information-retrieval action
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
                                        "search_messages",
                                        "get_all_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 — A new outgoing message to Theo with the requested content exists
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require at least Theo’s address among participants
                                    "conversation_name": "Theo Appleseed",
                                    # Verify the body contains the user-specified sentence
                                    "content": "Fantastic! It's so great that you're being proactive about your fitness goals",
                                    "creation_datetime_iso": "2024-12-02T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against the initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieval action precedes sending the reply
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_c0c6a6d7-ae16-430d-a06c-0fae43ec0396_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T21:00:00-08:00",
            is_read_time="2024-12-02T21:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to clone to event Evening Workout Session with Theo to also take place on Wednesday and Friday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Copy my event from today called Evening Workout Session with Theo and book it in for Wednesday and Friday as well.",
                },
            ],
            reasoning="The user wants a copy an event from today and they named it as Evening Workout Session with Theo, and looking at the calendar, that took place at 18:00 to 19:00. The user wants to repeat the same event on Wednesday and Friday so I'll book that in for them.",
            success_conditions=[
                {
                    "input_text": "1. Find the event Evening Workout Session with Theo scheduled December 2 from 18:00 to 19:00.",
                    "statefullness": "Stateless",
                },
                {
                    "statefullness": "Stateful",
                    "input_text": "2. Create a new event called Evening Workout Session with Theo scheduled December 4 from 18:00 to 19:00.",
                },
                {
                    "input_text": "3. Create a new event called Evening Workout Session with Theo scheduled December 6 from 18:00 to 19:00.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 — Agent looks up the existing workout session on the calendar
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
                # Milestone 1 — Confirm the correct event was found (Evening Workout Session with Theo on Dec 2, 18:00-19:00)
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
                                                "value": "Evening Workout Session with Theo",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-02T18:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-02T19:00:00-08:00",
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
                # Milestone 2 – A new Wednesday (Dec 4) and Friday workout session has been created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": [
                                        "Evening Workout Session with Theo",
                                        "Evening Workout Session with Theo",
                                    ],
                                    "start_datetime_iso": [
                                        "2024-12-04T18:00:00-08:00",
                                        "2024-12-06T18:00:00-08:00",
                                    ],
                                    "end_datetime_iso": [
                                        "2024-12-04T19:00:00-08:00",
                                        "2024-12-06T19:00:00-08:00",
                                    ],
                                    "attendees_names": [
                                        ["Lucas Garcia", "Theo Appleseed"],
                                        ["Lucas Garcia", "Theo Appleseed"],
                                    ],
                                    "creation_datetime_iso": "2024-12-02T21:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
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
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_c0c6a6d7-ae16-430d-a06c-0fae43ec0396_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T21:00:00-08:00",
            is_read_time="2024-12-02T21:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to clone to event Evening Workout Session with Theo to also take place on Wednesday and Friday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Clone to event from 6pm this evening and copy it in to Wednesday and Friday's schedule.",
                },
            ],
            reasoning="The user wants to clone an event from 18:00. Looking at the calendar, I can see that an event named Evening Workout Session with Theo took place this evening at 18:00. I'll copy that event over to Wednesday and Friday.",
            success_conditions=[
                {
                    "input_text": "1. Find the event Evening Workout Session with Theo scheduled December 2 from 18:00 to 19:00.",
                    "statefullness": "Stateless",
                },
                {
                    "statefullness": "Stateful",
                    "input_text": "2. Create a new event called Evening Workout Session with Theo scheduled December 4 from 18:00 to 19:00.",
                },
                {
                    "input_text": "3. Create a new event called Evening Workout Session with Theo scheduled December 6 from 18:00 to 19:00.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the original workout session on the calendar
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
                # Milestone 1 – Confirms the December 2 18:00 workout session was returned from the search in Milestone 0
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
                                                "value": "Evening Workout Session with Theo",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-02T18:00:00-08:00",
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
                # Milestone 2 – A new Wednesday (Dec 4) and Friday workout session has been created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": [
                                        "Evening Workout Session with Theo",
                                        "Evening Workout Session with Theo",
                                    ],
                                    "start_datetime_iso": [
                                        "2024-12-04T18:00:00-08:00",
                                        "2024-12-06T18:00:00-08:00",
                                    ],
                                    "end_datetime_iso": [
                                        "2024-12-04T19:00:00-08:00",
                                        "2024-12-06T19:00:00-08:00",
                                    ],
                                    "attendees_names": [
                                        ["Lucas Garcia", "Theo Appleseed"],
                                        ["Lucas Garcia", "Theo Appleseed"],
                                    ],
                                    "creation_datetime_iso": "2024-12-02T21:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
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
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_8128e120-2c0e-4557-8edd-330b375d2291_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T19:30:00-08:00",
            is_read_time="2024-12-02T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to reply to Theo's message to tell him that it's great he's being so proactive about his fitness goals. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a reply to Theo's message that says \"Fantastic! It's so great that you're being proactive about your fitness goals\"",
                },
            ],
            reasoning="The user wants me to send a reply to Theo's message that says \"Fantastic! It's so great that you're being proactive about your fitness goals\". First thing I need to do is look at the user's messages and see if there any conversations with a Theo... I found it, so now I will find the most recent received message and draft a reply to it with the given text. Now that that's done, I will ask the user if it is ready to be sent.",
            success_conditions=[
                {
                    "input_text": "1. A new text message saying \"Fantastic! It's so great that you're being proactive about your fitness goals\" is sent to Theo Appleseed",
                    "statefullness": "Stateful",
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
                # Milestone 0 – The agent tries to locate the relevant conversation or contact
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
                # Milestone 1 – A new outgoing message to Theo containing the expected text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Ensure Theo is among the participants
                                    "conversation_name": "Theo Appleseed",
                                    # Verify the required phrase is present
                                    "content": "Fantastic! It's so great that you're being proactive about your fitness goals",
                                    "creation_datetime_iso": "2024-12-02T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (
                    0,
                    1,
                ),  # Information-retrieval action should logically precede sending the message
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_f4ca239e-89f7-47a3-83ae-ddbf049741f3_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T15:00:00-08:00",
            is_read_time="2024-12-03T15:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to remember when you said you'd work out with Theo Appleseed. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me my last message sent to Theo.",
                },
            ],
            reasoning="The users looking for a specific message. I have to find their chat with someone called Theo. I check the users messages. I see one conversation with someone called 'Theo Appleseed'. I assume that this is the correct person.\nI check for the most recent message sent by the user to Theo Appleseed.\nI found it. It was sent on December 02 2024 at 19:20.\nI present the message to the user ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The message sent to Theo Appleseed at 19:20 on December 02 2024 with the proposed new workout schedule is presented to the user.",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – Agent uses a message-retrieval tool
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
                # Milestone 1 – Tool output contains the specific 2024-12-02 19:20 message to Theo
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
                                                "value": "Theo Appleseed",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Sure thing! How about we aim for evening sessions",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-02T19:20:00-08:00",
                                                "partial": False,
                                            },
                                            "status": {
                                                "value": "sent",
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
                # Milestone 2 – Agent tells the user the correct last message
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
                                            "Sure thing!",
                                            "evening sessions on Mondays, Wednesdays, and Fridays",
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
                (0, 1),  # Retrieval tool call → verify correct message in output
                (1, 2),  # Correct retrieval → verify user-facing response
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_734e53db-71cd-479f-a33e-9ce4a9ce2e94_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T20:00:00-08:00",
            is_read_time="2024-12-02T20:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to send Theo a text saying you'll start this schedule from Friday onwards "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a reply to my gym buddy saying lets start from this Friday onwards",
                },
            ],
            reasoning="The user wants to send a reply to their gym buddy saying lets start from this Friday onwards. I found the message thread with Theo Appleseed so I'll send a reply here. I'll Sedna. message saying \"Let's start from this Friday onwards\" and inform the user",
            success_conditions=[
                {
                    "input_text": '1. A text is sent to Theo Appleseed saying "Let\'s start from this Friday onwards"',
                    "statefullness": "Stateful",
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
                # Milestone 0 – Agent looks up Theo’s contact information
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
                # Milestone 1 – Verify that Theo Appleseed was returned in the contact search
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
                                                "value": "Theo Appleseed",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 12345-6789-1000-5678",
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
                # Milestone 2 – Outgoing text message to Theo is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Theo Appleseed",
                                    "content": "Friday onwards",
                                    "creation_datetime_iso": "2024-12-02T20:00:00-08:00",
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
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → verification of Theo
                (1, 2),  # Verification of Theo → message sent
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_58591c5a-12c1-4aa1-9df6-57abf9a5c00d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T18:35:00-08:00",
            is_read_time="2024-12-02T18:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You injured yourself going too hard in the gym so have to cancel any upcoming events. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the fitness planning from my calendar. ",
                },
            ],
            reasoning="The user wants to delete fitness planning from their Calendar. I should check for an event that matches this description. \nHmm, seems like there is only one, the Fitness Planning for Next 3 Months from 19:00-19:30 on the 2 December 2024. This must be the event the user meant. \nI will delete it and let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. Fitness Planning for Next 3 Months from 19:00-19:30 on the 2 December 2024 is deleted from Calendar. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events to locate the fitness planning session
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
                # Milestone 1 – The specific fitness-planning event is removed from the Calendar database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Fitness Planning for Next 3 Months",
                                    "start_datetime_iso": "2024-12-02T19:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
                            },
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
            name="LUCAS_GARCIA_3_fd292047-259d-4bb4-80e2-4feff3c9c301_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "calendar",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T11:30:00-08:00",
            is_read_time="2024-12-03T11:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You and Lucas had a great workout session on Monday and you're not sure if you'll meet tomorrow like you planned, but you're going to schedule in for this Friday at 18:00 like you discussed. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need you to add a workout with Theo for Friday 6th December at 18:00.",
                },
            ],
            reasoning="The user asked me to add a workout with Theo, for Friday 6th December 2024 at 18:00. First I'll just check that the user has this time slot open in their calendar and everything looks clear. I'll go ahead and create the event \"Workout with Theo\" for the date requested. From their contacts I can see only one Theo, Theo Appleseed. I will ask the user if they want to add Theo Appleseed as an attendee and then create the event.",
            success_conditions=[
                {
                    "input_text": '1. The event "Workout with Theo", scheduled for Friday 6th December 2024 at 18:00, is added to the user\'s calendar, with Theo Appleseed as an attendee.',
                    "statefullness": "Stateless",
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
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent looks up Theo in contacts
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
                # Milestone 1 – The contact search result contained “Theo Appleseed”
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
                                                "value": "Theo Appleseed",
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
                                "content": column_one_similarity,
                            },
                        )
                    ]
                ),
                # Milestone 2 – A new calendar event for the workout with Theo on Friday 6 Dec 2024 18:00 was created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Workout with Theo",
                                    "start_datetime_iso": "2024-12-06T18:00:00-08:00",
                                    "attendees_names": [["Theo Appleseed"]],
                                    "creation_datetime_iso": "2024-12-03T11:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Allow additional attendees (e.g., Lucas) but require Theo
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_127b239c-2395-4819-80d5-d28705d7d853_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T18:40:00-08:00",
            is_read_time="2024-12-02T18:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You and Theo are both craving proper coffee so you decide to move your planning session. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need you to change the location of Fitness Planning for Next 3 Months to Blue Heron Cafe.",
                },
            ],
            reasoning="The user is asking to edit an event.\nFirst, I need to find the event in question in the user's calendar. I see an exact match for the user's query, Fitness Planning for Next 3 Months scheduled for December 02, 2024, 19:00-19:30. The current location of this event is Cafe at Orchard County Fitness Center. \nI will alter this as requested. The location of Fitness Planning for Next 3 Months scheduled for December 02, 2024, 19:00-19:30 is now set to Blue Heron Cafe.",
            success_conditions=[
                {
                    "input_text": "1. Location of Fitness Planning for Next 3 Months scheduled for December 02, 2024, 19:00-19:30, is altered to Blue Heron Cafe.",
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
            ],
            milestones=[
                # Milestone 0 – the agent looks up calendar information to locate the event
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
                # Milestone 1 – confirm that the correct calendar event was retrieved
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
                                            "start_datetime_iso": {
                                                "value": "2024-12-02T19:00:00-08:00",
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
                # Milestone 2 – verify that the calendar event’s location was updated
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Fitness Planning for Next 3 Months",
                                    "location": "Blue Heron Cafe",
                                    "creation_datetime_iso": "2024-12-02T18:40:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with original snapshot
                        )
                    ],
                    # ignore potential sandbox traces etc. when validating calendar update
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_127b239c-2395-4819-80d5-d28705d7d853_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T18:40:00-08:00",
            is_read_time="2024-12-02T18:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You and Theo are both craving proper coffee so you decide to move your planning session. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Change the location of the upcoming event to Blue Heron Cafe.",
                },
            ],
            reasoning="The user is asking to edit an event.\nFirst, I need to find the event in question in the user's calendar. The user has indicated this is an upcoming event. I can see only one future event scheduled for today, Fitness Planning for Next 3 Months scheduled for December 02, 2024, 19:00-19:30. The current location of this event is Cafe at Orchard County Fitness Center. \nI will alter this as requested. The location of Fitness Planning for Next 3 Months scheduled for December 02, 2024, 19:00-19:30 is now set to Blue Heron Cafe.",
            success_conditions=[
                {
                    "input_text": "1. Location of Fitness Planning for Next 3 Months scheduled for December 02, 2024, 19:00-19:30, is altered to Blue Heron Cafe.",
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
            ],
            milestones=[
                # Milestone 0 – The agent looks up the existing event in the calendar
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
                # Milestone 1 – Confirm the desired calendar event was returned from the search
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
                                            "start_datetime_iso": {
                                                "value": "2024-12-02T19:00:00-08:00",
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
                # Milestone 2 – The calendar event’s location has been updated to “Blue Heron Cafe”
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Fitness Planning for Next 3 Months",
                                    "location": "Blue Heron Cafe",
                                    "creation_datetime_iso": "2024-12-02T18:40:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_exact_match_similarity,
                                "location": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against the initial snapshot
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
            name="LUCAS_GARCIA_3_fd292047-259d-4bb4-80e2-4feff3c9c301_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "calendar",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T11:30:00-08:00",
            is_read_time="2024-12-03T11:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You and Lucas had a great workout session on Monday and you're not sure if you'll meet tomorrow like you planned, but you're going to schedule in for this Friday at 18:00 like you discussed. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I need you to add the event "workout with Theo" in three days at 18:00 and add my gym buddy.',
                },
            ],
            reasoning="The user asked me to add a workout with Theo, in three days at 18:00. Today is 3 December 2024 so in three days it will be 6 December 2024. I will check the user's calendar to see if the time slot is free and everything looks clear. \n\nNext the user wants to add their 'gym buddy' to the event. I will check the user's contacts and can see no one named that but 'Theo Appleseed' is listed as 'gym buddy and workout partner'. This is the contact the user wants to add as an invitee.\n\n I'll go ahead and create the event \"Workout with Theo\" for the date requested and add Theo Appleseed as an invitee.",
            success_conditions=[
                {
                    "input_text": '1. The event "Workout with Theo", scheduled for Friday 6th December 2024 at 18:00, is added to the user\'s calendar, with Theo Appleseed as an attendee.',
                    "statefullness": "Stateless",
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
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent searches contacts to locate the "gym buddy" (Theo)
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
                # Milestone 1 – Confirm that Theo Appleseed was found in the contact-search results
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
                                                "value": "Theo Appleseed",
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
                # Milestone 2 – A new calendar event for Friday, 6 Dec 2024 18:00 with Theo as attendee is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Workout with Theo",
                                    "start_datetime_iso": "2024-12-06T18:00:00-08:00",
                                    "attendees_names": [["Theo Appleseed"]],
                                    "creation_datetime_iso": "2024-12-03T11:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,  # event name contains the phrase
                                "attendees_names": column_list_subset_match_similarity,  # must include Theo,
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
            milestone_edge_list=[
                (0, 1),  # contact search → confirm Theo found
                (1, 2),  # Theo found → create calendar event
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_734e53db-71cd-479f-a33e-9ce4a9ce2e94_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T20:00:00-08:00",
            is_read_time="2024-12-02T20:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to send Theo a text saying you'll start this schedule from Friday onwards "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a reply to Theo saying lets start from this Friday onwards",
                },
            ],
            reasoning="The user wants to send a reply to Theo saying lets start from this Friday onwards. I found the message thread with Theo Appleseed so I'll send a reply here. I'll Sedna. message saying \"Let's start from this Friday onwards\" and inform the user",
            success_conditions=[
                {
                    "input_text": '1. A text is sent to Theo Appleseed saying "Let\'s start from this Friday onwards"',
                    "statefullness": "Stateful",
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
                # Milestone 0 – The agent looks up Theo’s contact information
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
                # Milestone 1 – Confirm that Theo Appleseed was actually found in the contact-search result
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
                                                "value": "Theo Appleseed",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 12345-6789-1000-5678",
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
                # Milestone 2 – A new text message to Theo containing the key phrase was sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Theo Appleseed",
                                    "content": "start from this Friday",
                                    "creation_datetime_iso": "2024-12-02T20:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
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
                (0, 1),  # contact search → confirm Theo found
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_58591c5a-12c1-4aa1-9df6-57abf9a5c00d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T18:35:00-08:00",
            is_read_time="2024-12-02T18:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You injured yourself going too hard in the gym so have to cancel any upcoming events. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the event in 25 minutes. ",
                },
            ],
            reasoning="The user wants to delete the event in 25 minutes. I need to figure out which event they mean. To do so I need to figure out what time it will be in 25 minutes. \nHmm, it is 18:35 so that means in 25 minutes it will be 19:00. This means I am looking for an event at 19:00. Next I will check the Calendar for an event at that time. \nLooks like there is only one event that starts at 19:00-19:30, the Fitness Planning for Next 3 Months on the 2 December 2024 so this must be what the user meant. \nLastly, I will delete this event and let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. Fitness Planning for Next 3 Months from 19:00-19:30 on the 2 December 2024 is deleted from Calendar. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (evidence that it tried to find the right one)
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
                        ),
                    ],
                ),
                # Milestone 1 – The specific calendar event has been removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Fitness Planning for Next 3 Months",
                                    "start_datetime_iso": "2024-12-02T19:00:00-08:00",
                                    "end_datetime_iso": "2024-12-02T19:30:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Lookup must logically occur before deletion
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_d60f6455-94cb-480d-807b-4e0703b6f5bb_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T19:30:00-08:00",
            is_read_time="2024-12-02T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to follow up on your last message from Theo. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to Theo saying Me too, see you soon!",
                },
            ],
            reasoning="The user would like to reply to a message from Theo, containing the text \"Me too, see you soon!\". I'll need to find the named contact via their contact list and or messages, and once I've located the contact in question I can compose the message and seek confirmation to send it.",
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Theo Appleseed saying "Me too, see you soon!”',
                    "statefullness": "Stateful",
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
                # Milestone 0 – The agent looks up contact information (Theo)
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
                # Milestone 1 – Verify Theo Appleseed was returned by the contact lookup
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
                                        "full_name": {
                                            "value": "Theo Appleseed",
                                            "partial": False,
                                        },
                                        "email": {
                                            "value": "theo.appleseed@example.com",
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
                # Milestone 2 – A new message is sent to Theo saying "Me too, see you soon!"
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
                                                "lucas.garcia@example.com",
                                                "+1 12345-6789-1000-1234",
                                            ),
                                            (
                                                "theo.appleseed@example.com",
                                                "+1 12345-6789-1000-5678",
                                            ),
                                        ]
                                    ],
                                    "content": "Me too, see you soon!",
                                    "creation_datetime_iso": "2024-12-02T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_contains_similarity,
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
                (0, 1),  # Contact lookup → confirm Theo found
                (1, 2),  # Theo confirmed → send reply message
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_b73339f2-a66a-45dd-8292-4b6a2d54b10b_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "calendar",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T19:30:00-08:00",
            is_read_time="2024-12-02T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You and Theo have agreed to the plan proposed in your messages and you want to schedule them in the calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to schedule two events with Theo for our planned evening workout sessions on Wednesday and Friday for an hour at 6. ",
                },
            ],
            reasoning='Ok so the user wants to schedule two events with Theo for their planned evening workout sessions on Wednesday and Friday for an hour at 6. These events seem interconnected so I believe some of the information will overlap. Let\'s start with what does. First is establishing who Theo is. There is only one Theo in the user\'s contacts which is Theo Appleseed. I will add them as an invitee to both events. Next is the name which I will deduce from what the user is looking to do on both days. I Feel "Evening Workout Session with Theo" would make sense. Next is the runtime which is consistent to both events. Both will be scheduled for 18:00-19:00. Now where they split apart is the days they are due to happen on as this is still two different events. The first event is occurring on Wednesday so I will schedule it in on 4 December. The second is happening on Friday so I will schedule it in on 6 of December. I will now schedule the event "Evening Workout Session with Theo" for 18:00-19:00 on 4 December 2024 and the event "Evening Workout Session with Theo" for 18:00-19:00 on 6 December 2024. ',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The event "Evening Workout Session with Theo" with Theo Appleseed as an invitee is scheduled for 18:00-19:00 on 4 December 2024. ',
                },
                {
                    "input_text": '2. The event "Evening Workout Session with Theo" with Theo Appleseed as an invitee is scheduled for 18:00-19:00 on 6 December 2024. ',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up contact information (Theo)
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
                # Milestone 1 – Verify Theo Appleseed is found in the contact-search results
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
                                                "value": "Theo Appleseed",
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
                # Milestone 2 – Calendar event for Wednesday 4-Dec-2024 is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Evening Workout Session with Theo",
                                    "start_datetime_iso": "2024-12-04T18:00:00-08:00",
                                    "end_datetime_iso": "2024-12-04T19:00:00-08:00",
                                    "attendees_names": [["Theo Appleseed"]],
                                    "creation_datetime_iso": "2024-12-02T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_rouge_l_similarity,
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
                # Milestone 3 – Calendar event for Friday 6-Dec-2024 is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Evening Workout Session with Theo",
                                    "start_datetime_iso": "2024-12-06T18:00:00-08:00",
                                    "end_datetime_iso": "2024-12-06T19:00:00-08:00",
                                    "attendees_names": [["Theo Appleseed"]],
                                    "creation_datetime_iso": "2024-12-02T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_rouge_l_similarity,
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
                (0, 1),  # contact search → confirm Theo
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_b73339f2-a66a-45dd-8292-4b6a2d54b10b_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "calendar",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T19:30:00-08:00",
            is_read_time="2024-12-02T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You and Theo have agreed to the plan proposed in your messages and you want to schedule them in the calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Schedule the event "Evening Workout Session with Theo" with Theo Appleseed as an invitee on Wednesday 18:00-19:00 on Wednesday and also schedule the event "Evening Workout Session with Theo" with Theo Appleseed as an invitee on Friday from 18:00-19:00.',
                },
            ],
            reasoning='Ok so the user wants to schedule the event "Evening Workout Session with Theo" with Theo Appleseed as an invitee on Wednesday 18:00-19:00 on Wednesday and also schedule the event "Evening Workout Session with Theo" with Theo Appleseed as an invitee on Friday from 18:00-19:00 too. These events seem interconnected so I believe some of the information will overlap. Let\'s start with what does. First is establishing the name which is given to us by the user. Next is the invitees which is given to us by the user. Next is the runtime which is given to us by the user. The events split at the days they occur so "Evening Workout Session with Theo" no. 1 occurs on Wednesday as given by the user and "Evening Workout Session with Theo" no. 2 occurs on Friday as given by the user. I will now schedule the event "Evening Workout Session with Theo" for 18:00-19:00 on 4 December 2024 and the event "Evening Workout Session with Theo" for 18:00-19:00 on 6 December 2024. ',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The event "Evening Workout Session with Theo" with Theo Appleseed as an invitee is scheduled for 18:00-19:00 on 4 December 2024. ',
                },
                {
                    "input_text": '2. The event "Evening Workout Session with Theo" with Theo Appleseed as an invitee is scheduled for 18:00-19:00 on 6 December 2024. ',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Calendar event created for Wednesday 4 Dec 2024 18:00-19:00
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": [
                                        "Evening Workout Session with Theo",
                                        "Evening Workout Session with Theo",
                                    ],
                                    "start_datetime_iso": [
                                        "2024-12-04T18:00:00-08:00",
                                        "2024-12-06T18:00:00-08:00",
                                    ],
                                    "end_datetime_iso": [
                                        "2024-12-04T19:00:00-08:00",
                                        "2024-12-06T19:00:00-08:00",
                                    ],
                                    "attendees_names": [
                                        ["Theo Appleseed"],
                                        ["Theo Appleseed"],
                                    ],
                                    "creation_datetime_iso": "2024-12-02T19:30:00-08:00",
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
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_378e5664-6d26-4c2a-abdf-462f4ee16131_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T19:30:00-08:00",
            is_read_time="2024-12-02T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You message Theo inquiring if he would like a training session outside such as running or cycling. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to suggest to my client Theo Appleseed that we could mix up the workout session during the week to include some outside activity like cycling or running. ",
                },
            ],
            reasoning="The user wants to suggest to his client Theo Appleseed that their weekly workout sessions should include outside activity such as Cycling or Running. \n\n\nI will message Theo appleseed and inquire if he would like to have a session outdoors and suggest cycling or running. Moving sessions outside can be very refreshing and a healthy option. ",
            success_conditions=[
                {
                    "input_text": "1. You suggest to your client Theo Appleseed that some exercise outside the gym maybe be an enjoyable experience. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up Theo’s contact information
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
                # Milestone 1 – Verify that the contact returned from Milestone 0 is Theo Appleseed
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
                                                "value": "Theo Appleseed",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "theo.appleseed@example.com",
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
                # Milestone 2 – A new message is sent to Theo suggesting an outdoor activity
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Theo Appleseed",
                                    "content": [
                                        ("outdoor", "outside")
                                    ],  # either phrasing is acceptable,
                                    "creation_datetime_iso": "2024-12-02T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # contact lookup → verify Theo found
                (1, 2),  # verified Theo → message sent
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_3_d60f6455-94cb-480d-807b-4e0703b6f5bb_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_3",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T19:30:00-08:00",
            is_read_time="2024-12-02T19:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to follow up on your last message from Theo. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Get back to Theo and say Me too, see you soon!",
                },
            ],
            reasoning='The user wants to reply to Theo with the text "Me too, see you soon!". First, I\'ll need to find the contact by looking through messages for a chat with individuals going by this name. Then I can compose the reply with the provided text and confirm that the user is happy to send it.',
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Theo Appleseed saying "Me too, see you soon!”',
                    "statefullness": "Stateful",
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
                # Milestone 0 – Agent invokes a lookup tool to find Theo / the conversation
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
                                        "search_messages",
                                        "get_all_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Confirm Theo Appleseed was actually returned in the lookup results
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
                                                "value": "Theo Appleseed",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "theo.appleseed@example.com",
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
                # Milestone 2 – A new message is sent to Theo with the required content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Theo Appleseed",
                                    "content": "Me too, see you soon",
                                    "creation_datetime_iso": "2024-12-02T19:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial state
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
            name="LUCAS_GARCIA_3_4aa628f9-1268-45ae-b528-9d946fc5f798_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_3",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T12:15:00-08:00",
            is_read_time="2024-12-01T12:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know when your workout session is taking place tomorrow. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Remind me what time my session is with Theo tomorrow evening. ",
                },
            ],
            reasoning='The user wants to know the start time of an event and has provided key words and a time range. I will start by searching within the provided time range and use the keywords provided. I have found an event tomorrow, that is, Monday December 2 from 06:00 pm to 07:00 pm called "Evening Workout Session with Theo". I can assume this is the referenced event, as it contains the keywords provided by the user. I will call out the start time of this event to the user, as requested. \n',
            success_conditions=[
                {
                    "input_text": "1. The start time of Evening Workout Session with Theo is read out to the user. \n",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – A calendar lookup tool is invoked
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
                # Milestone 1 – The expected workout event is found in the tool result
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
                                                "value": "Evening Workout Session with Theo",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-02T18:00:00-08:00",
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
                                    # any acceptable phrasing that mentions the 6 pm start time
                                    "content": [
                                        (
                                            "6 pm",
                                            "6:00 pm",
                                            "6pm",
                                            "18:00",
                                            "6 p.m.",
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
    ]
