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
    column_list_tuple_contains_similarity,
    column_list_tuple_subset_contains_similarity,
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


def get_TAG_EMILY_ROSE_pilot_plot_7(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="EMILY_ROSE_7_9071e97b-f7b9-4a80-ab01-01b66f827a1b_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T16:40:00-08:00",
            is_read_time="2024-12-05T16:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to reply to Oliver's message to tell him that it was a pleasure "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to my last message with the text "It was a pleasure"',
                },
            ],
            reasoning='The user wants me to reply to their last message with the text  "It was a pleasure".  First I need to find the most recent message received by the user. Now that I have found that I can draft a reply to the most recent message and ask the user if it is ready to be sent',
            success_conditions=[
                {
                    "input_text": '1. A new text message is sent to Oliver Green saying "It was a pleasure"',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages", "send_message"],
            milestones=[
                # Milestone 0 – The agent tries to locate the relevant conversation or message.
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
                # Milestone 1 – A new outgoing message to Oliver Green with the correct text was sent.
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
                                                "+1 530-555-0123",
                                                "emily.rose@orchardcommunity.org",
                                            ),  # Emily Rose
                                            (
                                                "+1 530-555-0128",
                                                "oliver.green@dailybrewcafe.com",
                                            ),  # Oliver Green
                                        ]
                                    ],
                                    "content": "It was a pleasure",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-05T16:40:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
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
                (0, 1),  # Retrieve messages → send reply
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_38002164-eb8a-46ed-b041-279874a429cb_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T15:03:00-08:00",
            is_read_time="2024-12-05T15:03:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know if Oliver has replied to your message yet. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has my last message been replied? Yes or No.",
                },
            ],
            reasoning="Okay so, the user wants to know has their last message they sent been replied to yet. I will now look into their message threads and can see that Oliver Green was the last person that they messaged on 5 December 2024 at 15:00, saying 'Hi Oliver, just following up about the refreshments for the upcoming community gathering. Are we still on for 4 PM at your cafe today?'. Oliver Green has not replied to the user so I can relay this information to the user.",
            success_conditions=[
                {
                    "input_text": "1. No message reply has been received from Oliver Green on 5 December 2024 and this is displayed to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – Agent uses a messages-retrieval tool
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
                        ),
                    ],
                ),
                # Milestone 1 – Returned data include the user's last (unanswered) message to Oliver
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
                                            "content": {
                                                "value": "Hi Oliver",
                                                "partial": True,
                                            },
                                            "status": {
                                                "value": "sent",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "+1 530-555-0123",
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
                # Milestone 2 – Agent tells the user that no reply has been received
                Milestone(
                    snapshot_constraints=[
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
                                "content": column_word_contains_similarity
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_38002164-eb8a-46ed-b041-279874a429cb_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T15:03:00-08:00",
            is_read_time="2024-12-05T15:03:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know if Oliver has replied to your message yet. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Has Oliver replied yet? Yes or No.",
                },
            ],
            reasoning="Right so the user wants to know if Oliver has replied yet. From their contacts I can only see one match, 'Oliver Green'. Now I can look into their message thread with him and I can see no reply has been given to the user's message sent on 5 December 2024 at 15:00, saying 'Hi Oliver, just following up about the refreshments for the upcoming community gathering. Are we still on for 4 PM at your cafe today?'. I can then relay this information to the user that no new messages have been received.",
            success_conditions=[
                {
                    "input_text": "1. No message reply has been received from Oliver Green on 5 December 2024 and this is displayed to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks for Oliver’s messages
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
                # Milestone 1 – The retrieved messages include the user’s last (unanswered) message to Oliver
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
                                            "content": {
                                                "value": "Hi Oliver, just following up",
                                                "partial": True,
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
                # Milestone 2 – The agent tells the user that Oliver has not replied yet
                Milestone(
                    snapshot_constraints=[
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
                                "content": column_word_contains_similarity
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieved messages → confirm message exists
                (1, 2),  # Confirmation of data → inform user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_9071e97b-f7b9-4a80-ab01-01b66f827a1b_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T16:40:00-08:00",
            is_read_time="2024-12-05T16:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to reply to Oliver's message to tell him that it was a pleasure "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to Oliver\'s message with the text  "It was a pleasure"',
                },
            ],
            reasoning='The user wants me to reply to Oliver\'s message with the text  "It was a pleasure".  First I need to find the conversation with Oliver. Now that I have found that I can draft a reply to the most recent message and ask the user if it is ready to be sent',
            success_conditions=[
                {
                    "input_text": '1. A new text message is sent to Oliver Green saying "It was a pleasure"',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages", "send_message"],
            milestones=[
                # Milestone 0 – the agent looks up the relevant conversation or messages
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
                # Milestone 1 – a new outgoing message to Oliver containing “It was a pleasure” is recorded
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Oliver Green",
                                    "content": "It was a pleasure",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-05T16:40:00-08:00",
                                }
                            ),
                            column_similarity_measure={
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
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_c67d2720-2968-4165-b8a0-04f8302beec0_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T16:05:00-08:00",
            is_read_time="2024-12-05T16:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You're running late to your meeting with Oliver and you don't even really know where the cafe is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where am I meeting my friend today?",
                },
            ],
            reasoning="The user is asking about the location of an event.\nFirst, I should determine who they mean by friend.\nI can see a number of people tagged as friend in the user's contacts, Nathan Blake, Oliver Green, and Jessica Lane.\nNext, I should go to the user's calendar and search for events involving these people.\nI can see only one potential match, Meeting with Oliver Green for Community Gathering Refreshments scheduled for December 05, 2024, 16:00-17:00.\nThe location for this event is currently set as Daily Brew Cafe, Orchard County.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Location of Meeting with Oliver Green for Community Gathering Refreshments scheduled for December 05, 2024, 16:00-17:00 is confirmed as Daily Brew Cafe, Orchard County",
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
                # Milestone 0 – The agent queries the calendar to locate today’s meeting
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
                # Milestone 1 – Verify the meeting with Oliver and its location were found in the tool’s output
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
                                                "value": "Meeting with Oliver Green for Community Gathering Refreshments",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Daily Brew Cafe",
                                                "partial": True,  # allow the full string "Daily Brew Cafe, Orchard County"
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
                # Milestone 2 – The agent tells the user the correct meeting location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Daily Brew Cafe",
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
            name="EMILY_ROSE_7_468e9e06-cb23-432e-87a6-947cc801c349_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "contact",
                "calendar",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T10:00:00-08:00",
            is_read_time="2024-12-16T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You met with your caterer a while ago about the community gathering event.   You want to send a text to him asking if everything still okay for the gathering event. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send our caterer a text checking in if everything is still okay for the gathering",
                },
            ],
            reasoning="The user wants to send 'their caterer' a text checking in if everything is still okay for the gathering. Which gathering are they referring to? I can see if there is anything in their calendar. I can see an event titled \"Community Gathering Event\" scheduled for December 20 at 2:00 pm. I can assume this the gathering they referred to. I'll check the message history with Oliver Green and I found discussion about providing refreshments for the community event. I'll send Oliver Green a text saying \"Hi Oliver, just checking in to see if everything is still okay for the gathering?\" with the user's confirmation.",
            success_conditions=[
                {
                    "input_text": '1. A text is sent to Oliver Green saying something like "Hi Oliver, just checking in to see if everything is still okay for the gathering?"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 –  Agent looks up the caterer (Oliver) in contacts
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
                # Milestone 1 –  Verify that Oliver Green was returned from contact search
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
                                                "value": "Oliver Green",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 530-555-0128",
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
                # Milestone 2 –  A new text message to Oliver was sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Ensure Oliver’s phone is included among the participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "oliver.green@dailybrewcafe.com",
                                                "+1 530-555-0128",
                                            )
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-16T10:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to state before the task
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact search → confirm Oliver
                (1, 2),  # Confirm Oliver → send the text message
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_6475b9d5-8f0d-43b1-bbc1-1a32f8491f3d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T15:05:00-08:00",
            is_read_time="2024-12-05T15:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know if Oliver responded to your latest message as you're anxious to know if he confirmed the meeting with you to discuss the community gathering at the cafe today. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I get a response from the Cafe King to my message?",
                },
            ],
            reasoning="The user wants to know if they got a response from the Cafe King to their message. I wonder who that is. I should check their contacts to figure it out. I can't see a contact with that name but I see one contact, Oliver Green listed with the alias, Cafe King. It must be him. I'll check to see for a message from Oliver. I see the user received one new message from Oliver Green, received on December 5th at 15:05. I'll show the message to the user. ",
            success_conditions=[
                {
                    "input_text": "1. The message from Oliver Green, received on December 5th at 15:05 is shared with the user. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks for the latest reply in messages
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
                # Milestone 1 – Confirms that the expected message from Oliver Green was found
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
                                            # Sender phone number for Oliver Green
                                            "sender_address": {
                                                "value": "+1 530-555-0128",
                                                "partial": False,
                                            },
                                            # Key phrase from the message
                                            "content": {
                                                "value": "everything is set",
                                                "partial": True,
                                            },
                                            # Timestamp (exact match)
                                            "creation_datetime_iso": {
                                                "value": "2024-12-05T15:05:00-08:00",
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
                # Milestone 2 – The agent informs the user about Oliver’s response
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Ensure the key confirmation phrase is relayed
                                    "content": "everything is set",
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
                (0, 1),  # Must find the message before verifying its contents
                (1, 2),  # Must verify the contents before telling the user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_5f18e8a3-c539-44b6-a54c-4bc16dc18536_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "messaging",
                "contact",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T16:05:00-08:00",
            is_read_time="2024-12-05T16:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You're running late to your meeting and you don't even really know where the cafe is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where am I meeting my friend today?",
                },
            ],
            reasoning="The user is asking about the location of an event.\nFirst, I should determine who they mean by friend.\nI can see a number of people tagged as friend in the user's contacts, Nathan Blake, Oliver Green, and Jessica Lane.\nNext, I should go to the user's calendar and search for events involving these people.\nI can see only one potential match, Meeting with Oliver Green for Community Gathering Refreshments scheduled for December 05, 2024, 16:00-17:00. I assume this is the meeting the user is talking about because it's the only event on their calendar today. And the invitee is Oliver Green.\nThe location for this event is currently set as Daily Brew Cafe, Orchard County.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. The location of the event named Meeting with Oliver Green for Community Gathering Refreshments on 5 December 2024 from 16:00-17:00, is presented to the user as Daily Brew Cafe, Orchard County",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "search_messages",
                "get_all_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar to find today's meeting with the friend
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
                # Milestone 1 – Confirm the correct event on Dec 5, 2024 16:00–17:00 with Oliver Green was retrieved
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
                                                "value": "Meeting with Oliver Green for Community Gathering Refreshments",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-05T16:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-05T17:00:00-08:00",
                                                "partial": False,
                                            },
                                            "attendees_names": {
                                                "value": ["Emily Rose", "Oliver Green"],
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
                # Milestone 2 – Agent tells user the correct location: Daily Brew Cafe, Orchard County
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Daily Brew Cafe, Orchard County",
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
                (0, 1),  # Calendar lookup → confirm correct event
                (1, 2),  # Confirmed event → respond to user with location
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_5f18e8a3-c539-44b6-a54c-4bc16dc18536_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "messaging",
                "contact",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T16:05:00-08:00",
            is_read_time="2024-12-05T16:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You're running late to your meeting and you don't even really know where the cafe is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where am I meeting Oliver Green for Community Gathering Refreshments",
                },
            ],
            reasoning="The user is asking about the location of an event.\nI should search their calendar.\nI can see one event which matches the user's query,  Meeting with Oliver Green for Community Gathering Refreshments scheduled for December 05, 2024, 16:00-17:00.\nThe location for this event is currently set as Daily Brew Cafe, Orchard County.\nI should inform the user.\n",
            success_conditions=[
                {
                    "input_text": "1. The location of the event named Meeting with Oliver Green for Community Gathering Refreshments on 5 December 2024 from 16:00-17:00, is presented to the user as Daily Brew Cafe, Orchard County",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "search_messages",
                "get_all_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar to find the meeting with Oliver
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
                # Milestone 1 – Confirm the correct event (Meeting with Oliver Green for Community Gathering Refreshments) was retrieved
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
                                                "value": "Meeting with Oliver Green for Community Gathering Refreshments",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-05T16:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-05T17:00:00-08:00",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Daily Brew Cafe, Orchard County",
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
                # Milestone 2 – User-facing answer includes the correct location "Daily Brew Cafe, Orchard County"
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Daily Brew Cafe",
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
                (0, 1),  # calendar lookup → confirm event details including location
                (1, 2),  # confirmed event → respond to user with the correct location
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_6475b9d5-8f0d-43b1-bbc1-1a32f8491f3d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T15:05:00-08:00",
            is_read_time="2024-12-05T15:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know if Oliver responded to your latest message as you're anxious to know if he confirmed the meeting with you to discuss the community gathering at the cafe today. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I get a response from Oliver to my message?",
                },
            ],
            reasoning="The user wants to know if they got a response from Oliver to their message. I wonder who that is. I should check their contacts to figure it out. I see one contact with the name Oliver, Oliver Green. It must be him. I'll check to see for a message from Oliver. I see the user received one new message from Oliver Green, received on December 5th at 15:05. I'll show the message to the user. ",
            success_conditions=[
                {
                    "input_text": "1. The message from Oliver Green, received on December 5th at 15:05 is shared with the user. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – The agent tries to locate any message from Oliver
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
                # Milestone 1 – Confirm that the retrieved messages include Oliver Green's 15:05 reply
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
                                                "value": "+1 530-555-0128",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-05T15:05:00-08:00",
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
                # Milestone 2 – The agent tells the user that Oliver responded (includes key info)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Oliver",
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
                (0, 1),  # Need to retrieve messages before we can confirm content
                (1, 2),  # After confirming the message, agent informs the user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_468e9e06-cb23-432e-87a6-947cc801c349_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "calendar",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-16T10:00:00-08:00",
            is_read_time="2024-12-16T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You met with Oliver a while ago about the community gathering event.   You want to send a text to him asking if everything still okay for the gathering event. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send Oliver Green a text saying "Hi Oliver, just checking in to see if everything is still okay for the gathering?',
                },
            ],
            reasoning="The user wants to send Oliver Green a text saying \"Hi Oliver, just checking in to see if everything is still okay for the gathering?. I'll check the message history with Oliver Green and I found discussion about providing refreshments for the community event. I'll send Oliver Green a text saying \"Hi Oliver, just checking in to see if everything is still okay for the gathering?\" with the user's confirmation.",
            success_conditions=[
                {
                    "input_text": '1. A text is sent to Oliver Green saying "Hi Oliver, just checking in to see if everything is still okay for the gathering?"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent looks up Oliver’s contact information
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
                # Milestone 1 – Verify that the contact search (from Milestone 0) returned Oliver Green
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
                                                "value": "Oliver Green",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 530-555-0128",
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
                # Milestone 2 – A new text message has been sent to Oliver with the correct content
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
                                                "oliver.green@dailybrewcafe.com",
                                                "+1 530-555-0128",
                                            )
                                        ]
                                    ],
                                    "content": "Hi Oliver, just checking in to see if everything is still okay for the gathering?",
                                    "creation_datetime_iso": "2024-12-16T10:00:00-08:00",
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
                (0, 1),  # Contact lookup → confirm Oliver found
                (1, 2),  # Oliver confirmed → message sent
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_c67d2720-2968-4165-b8a0-04f8302beec0_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T16:05:00-08:00",
            is_read_time="2024-12-05T16:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You're running late to your meeting with Oliver and you don't even really know where the cafe is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where am I meeting Oliver Green for Community Gathering Refreshments",
                },
            ],
            reasoning="The user is asking about the location of an event.\nI should search their calendar.\nI can see one event which matches the user's query,  Meeting with Oliver Green for Community Gathering Refreshments scheduled for December 05, 2024, 16:00-17:00.\nThe location for this event is currently set as Daily Brew Cafe, Orchard County.\nI should inform the user.\n",
            success_conditions=[
                {
                    "input_text": "1. Location of Meeting with Oliver Green for Community Gathering Refreshments scheduled for December 05, 2024, 16:00-17:00 is confirmed as Daily Brew Cafe, Orchard County",
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
                # Milestone 0 – Agent queries the calendar for the meeting
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
                # Milestone 1 – Calendar search returns the correct event with the correct location
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
                                                "value": "Meeting with Oliver Green for Community Gathering Refreshments",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Daily Brew Cafe",
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
                # Milestone 2 – Agent informs the user of the correct meeting location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Daily Brew Cafe",
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
                (0, 1),  # Calendar query → confirm event details
                (1, 2),  # Event confirmed → relay information to user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_97513d69-3165-421d-ba12-9c2ecc717863_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T16:40:00-08:00",
            is_read_time="2024-12-05T16:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You just finished up your meeting with Oliver at his cafe discussing catering for the upcoming community gathering.   You want to reply to Oliver's message saying 'not as excited as me! Don't gate keep excitement.  ' "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text Oliver back saying 'not as excited as me! Don't gate keep excitement.'",
                },
            ],
            reasoning="The user wants to send a message reply to Oliver. The user has been most recently engaged in a text conversation with Oliver Green, so I'll take it that this is the person they wish to reply to. I'll send the message 'Not as excited as me! Don't gate keep excitement.' with the user's confirmation.",
            success_conditions=[
                {
                    "input_text": "1. The message 'Not as excited as me! Don't gate keep excitement.' is sent to Oliver Green.",
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
                # Milestone 0 – Agent consults existing data (contacts or messages) to locate Oliver or the right thread
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
                        ),
                    ],
                ),
                # Milestone 1 – A new outgoing message containing the required text is sent in the Oliver conversation
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Both Emily’s and Oliver’s numbers must be in the conversation
                                    "participants_addresses": [
                                        [
                                            (
                                                "oliver.green@dailybrewcafe.com",
                                                "+1 530-555-0128",
                                            )
                                        ]
                                    ],
                                    # Key phrase from the required reply
                                    "content": "Don't gate keep excitement",
                                    "creation_datetime_iso": "2024-12-05T16:40:00-08:00",
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
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieval → message sent
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_65fd856a-1473-40a3-856c-036abd5959fc_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T16:40:00-08:00",
            is_read_time="2024-12-05T16:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to reply to Oliver to express enthusiasm for the upcoming event. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to Oliver Green and say no problem, see you soon!",
                },
            ],
            reasoning="The user wants to send a message response and has provided the exact name of the contact and the exact message they would like to send. I will start by searching for the contact. I have found a contact who matched the name provided by the user, so I will now search the user's conversations with them. I have found an active conversation. I will send the user's message. ",
            success_conditions=[
                {
                    "input_text": "1. A reply is sent to Oliver Green's latest message saying \"no problem, see you soon!”",
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
                # Milestone 0 – The agent looks up the relevant contact or conversation
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
                    ]
                ),
                # Milestone 1 – A reply message is added to the Oliver Green thread
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
                                                "oliver.green@dailybrewcafe.com",
                                                "+1 530-555-0128",
                                            )
                                        ]
                                    ],
                                    "content": "no problem, see you soon",
                                    "creation_datetime_iso": "2024-12-05T16:40:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
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
                (0, 1),  # Information retrieval → sending the reply
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_65fd856a-1473-40a3-856c-036abd5959fc_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T16:40:00-08:00",
            is_read_time="2024-12-05T16:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to reply to Oliver to express enthusiasm for the upcoming event. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to Oliver to say no problem, see you soon!",
                },
            ],
            reasoning="The user wants to reply to Oliver's latest message with the text \"no problem, see you soon!\". First I'll find the specific message by looking through recently received messages, and with this I can compose the reply and see if the user is happy to send it.",
            success_conditions=[
                {
                    "input_text": "1. A reply is sent to Oliver Green's latest message saying \"no problem, see you soon!”",
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
                # Milestone 0 – The agent looks up recent messages to locate Oliver’s latest text
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
                # Milestone 1 – Verify the tool output from Milestone 0 contained Oliver’s latest message
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
                                                "value": "Oliver Green",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Perfect! Thanks again, Emily. Excited for the gathering!",
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
                # Milestone 2 – A reply has been created in the Messages database
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
                                                "oliver.green@dailybrewcafe.com",
                                                "+1 530-555-0128",
                                            )
                                        ]
                                    ],
                                    "content": "no problem",
                                    "creation_datetime_iso": "2024-12-05T16:40:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with pre-task state
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieved messages → verified correct message
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_97513d69-3165-421d-ba12-9c2ecc717863_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T16:40:00-08:00",
            is_read_time="2024-12-05T16:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You just finished up your meeting with Oliver at his cafe discussing catering for the upcoming community gathering.   You want to reply to Oliver's message saying 'not as excited as me! Don't gate keep excitement.  ' "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text him back saying 'not as excited as me! Don't gate keep excitement.'",
                },
            ],
            reasoning="The user wants to send a message. They have not specified a precise contact but they say it is a reply. The user has been most recently engaged in a text conversation with Oliver Green, so I'll take it that this is the person they wish to reply to. I'll send the message 'Not as excited as me! Don't gate keep excitement.' with the user's confirmation.",
            success_conditions=[
                {
                    "input_text": "1. The message 'Not as excited as me! Don't gate keep excitement.' is sent to Oliver Green.",
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
                # Milestone 0 – Verify that a new text message was sent to Oliver with the requested content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Both Emily (self) and Oliver must be in the conversation
                                    "participants_addresses": [
                                        [
                                            (
                                                "oliver.green@dailybrewcafe.com",
                                                "+1 530-555-0128",
                                            )
                                        ]
                                    ],
                                    # Core content the user asked to send
                                    "content": "Not as excited as me! Don't gate keep excitement.",
                                    # Outgoing message should be marked as sent
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-05T16:40:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare against the initial snapshot
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_9d60066f-564a-4d62-81b7-2f1c64865da1_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T15:30:00-08:00",
            is_read_time="2024-12-05T15:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You're going to be late to your meet-up with Oliver, so you want to check if you have his number you can call and let him know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the person I'm meeting with soon's number",
                },
            ],
            reasoning="User is looking for a person's details in their device, \"the person I'm meeting with soon's number\", so I first need to figure out who it is they're trying to look for. I'll check for the user's upcoming events in their calendar.... the soonest upcoming event is \"Meeting with Oliver Green for Community Gathering Refreshments\" today in 30 minutes. The event has Oliver Green as an attendee, so it seems like this must be the person they want to contact. I'll check the contacts for this person and find their information - I offer this contact card to user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The contact card for Oliver Green is pulled up for User.",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent tries to locate the contact information
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
                # Milestone 1 – Verify that Oliver Green’s contact details were returned by the lookup in Milestone 0
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
                                                "value": "Oliver Green",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 530-555-0128",
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
                # Milestone 2 – Agent presents Oliver’s number to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Oliver Green",
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
                (0, 1),  # Contact lookup → confirm Oliver returned
                (1, 2),  # Oliver confirmed → number shown to user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_3a64eab5-ead2-49cf-8193-6eadcd4883c8_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T15:30:00-08:00",
            is_read_time="2024-12-05T15:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You can't remember what time you agreed to meet Oliver and need to be reminded. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": " When is my catering meeting?",
                },
            ],
            reasoning="The user wants to know when their catering meeting is. I should check their Calendar for such an event. \n\nHmm, I don't see an event with this name. I should look for events about food.  Looks like there is one event about food, the Meeting with Oliver Green for Community Gathering Refreshments, from 16:00-17:99 on the 5 December 2024, so this must be what the user means. \n\nI will tell the user the start time for this event is 16:00.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed the user is meeting Oliver Green at 16:00.",
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
                # Milestone 0 – Agent looks up calendar to find the meeting
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
                # Milestone 1 – Confirm the meeting with Oliver Green at 16:00 was returned
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
                                                "value": "Meeting with Oliver Green for Community Gathering Refreshments",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-05T16:00:00-08:00",
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
                # Milestone 2 – Agent tells the user the correct meeting time
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
                                        ("16:00", "4:00", "4 pm", "4 p.m.", "4pm")
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
                (0, 1),  # Calendar lookup → verify meeting retrieved
                (1, 2),  # Meeting retrieved → user informed
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_3a64eab5-ead2-49cf-8193-6eadcd4883c8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T15:30:00-08:00",
            is_read_time="2024-12-05T15:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You can't remember what time you agreed to meet Oliver and need to be reminded. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When am I meeting Oliver?",
                },
            ],
            reasoning="The user wants to know when they are meeting Oliver. I should first figure out who Oliver is. I should check the user's Contacts for one named Oliver. \n\nI can only see one contact named Oliver, Oliver Green, so this must be who the user meant. Next I should go to Calendar and see if I can find a meeting with Oliver in the user's Calendar. \n\nLooks like there is an event called Meeting with Oliver Green for Community Gathering Refreshments from 16:00 to 17:00 on the 5 December 2024. This must be what the user meant.\n\nI will tell the user they are meeting Oliver at 16:00.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed the user is meeting Oliver Green at 16:00.",
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
                # Milestone 0 – The agent looks through calendar events
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
                # Milestone 1 – Confirm that the calendar event with Oliver at 16:00 was found
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
                                                "value": "Oliver Green",
                                                "partial": True,  # allow substring match
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-05T16:00:00-08:00",
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
                # Milestone 2 – The agent tells the user the correct meeting time
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
                                            "16:00",
                                            "4:00",
                                            "4 pm",
                                            "4pm",
                                            "4 p.m.",
                                            "4PM",
                                            "4 P.M.",
                                            "4 o'clock",
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
                (0, 1),  # Calendar search → confirm event with Oliver
                (1, 2),  # Confirmed event → inform the user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_9d60066f-564a-4d62-81b7-2f1c64865da1_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T15:30:00-08:00",
            is_read_time="2024-12-05T15:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You're going to be late to your meet-up with Oliver, so you want to check if you have his number you can call and let him know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Have I got Oliver Green's details?",
                },
            ],
            reasoning="User is looking for a persons details in their device so I first need to ask who it is they're trying to look for. They tell me Oliver so I check the contacts for this person and find one, Oliver Green. I offer this contact card to user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The contact card for Oliver Green is pulled up for User.",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent attempts to look up Oliver’s contact information
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
                # Milestone 1 – The returned contact list includes Oliver Green with the correct phone number
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
                                                "value": "Oliver Green",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 530-555-0128",
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
                # Milestone 2 – Agent informs the user and shows the phone number (or otherwise confirms details)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Oliver Green",
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_5f18e8a3-c539-44b6-a54c-4bc16dc18536_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "messaging",
                "contact",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T16:05:00-08:00",
            is_read_time="2024-12-05T16:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You're running late to your meeting and you don't even really know where the cafe is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What's the address of my meeting that started five minutes ago? I'm running late.",
                },
            ],
            reasoning='The user is asking for location details about a meeting for which they said they are running late. Let me look at their calendar instead. The only meeting on their calendar today is "Meeting with Oliver Green for Community Gathering Refreshments" and it was scheduled to start five minutes ago at 16:00. This must be the meeting the user is asking about. Now, the user wants to know where this meeting is taking place. I\'ll tell them the location listed on the event, Daily Brew Cafe in Orchard County.',
            success_conditions=[
                {
                    "input_text": "1. The location of the event named Meeting with Oliver Green for Community Gathering Refreshments on 5 December 2024 from 16:00-17:00, is presented to the user as Daily Brew Cafe, Orchard County",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "search_messages",
                "get_all_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent uses a calendar tool to look up the meeting info
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
                # Milestone 1 – Confirm the correct meeting event was retrieved from the calendar
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
                                                "value": "Meeting with Oliver Green for Community Gathering Refreshments",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-05T16:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-05T17:00:00-08:00",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Daily Brew Cafe, Orchard County",
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
                # Milestone 2 – Agent tells the user the meeting location (address/venue)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Ensure the response mentions the correct location text
                                    "content": "Daily Brew Cafe",
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
                (0, 1),  # Calendar lookup → confirm correct meeting and its location
                (1, 2),  # Meeting identified → inform user of location
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_7_5f18e8a3-c539-44b6-a54c-4bc16dc18536_single_turn_3",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_7",
                "messaging",
                "contact",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T16:05:00-08:00",
            is_read_time="2024-12-05T16:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You're running late to your meeting and you don't even really know where the cafe is. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where did Oliver say we were going to meet? I'm late and need to know ASAP.",
                },
            ],
            reasoning="The user seems to be asking for location details about an event for which they said they are running late, but they asked where Oliver said they were going to meet. Their only saved contact named Oliver is Oliver Green, so I'll check the user's text messages with him first to see if Oliver mentioned anything about meeting anywhere. There are two texts I see from Oliver. One from 15:05 says \"Hi Emily, yes, everything is set for our meeting. Looking forward to finalizing the details with you!\" and one from 15:10 says \"Sounds good, see you soon!\". Neither of these mention the location of the meeting. Maybe the user misremembered where this information was stored. Let me look at the user's calendar instead. The only meeting on their calendar for today is \"Meeting with Oliver Green for Community Gathering Refreshments\" and it was scheduled to start five minutes ago at 16:00. Even though its start time is in the past, I'll assume this is the meeting the user is asking about since they're running late. Now, the user wants to know where this meeting is taking place. I'll tell them the location listed on the event, Daily Brew Cafe in Orchard County.",
            success_conditions=[
                {
                    "input_text": "1. The location of the event named Meeting with Oliver Green for Community Gathering Refreshments on 5 December 2024 from 16:00-17:00, is presented to the user as Daily Brew Cafe, Orchard County",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "search_messages",
                "get_all_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looks up where the meeting with Oliver is (calendar retrieval)
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
                # Milestone 1 – Confirm the specific event with Oliver on Dec 5, 2024 16:00–17:00 was retrieved, including its location
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
                                                "value": "Meeting with Oliver Green for Community Gathering Refreshments",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-05T16:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-05T17:00:00-08:00",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Daily Brew Cafe, Orchard County",
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
                # Milestone 2 – User is told the correct meeting location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Focus on key phrase: the cafe name
                                    "content": "Daily Brew Cafe",
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
                (0, 1),  # Calendar lookup -> confirm correct event & location
                (1, 2),  # Confirmed event info -> respond to user with location
            ],
        ),
    ]
