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
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
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


def get_TAG_THEO_APPLESEED_pilot_plot_15(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="THEO_APPLESEED_15_c4169d08-53ec-48b8-85b6-cb89abba4ac0_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_15",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T19:15:00-07:00",
            is_read_time="2024-07-26T19:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to update tomorrow's hiking trip event to add Cookie and Lucas as invitees. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Add Lucas and Cookie as invitees to my hiking trip",
                },
            ],
            reasoning="The user wants to update an event called 'Hiking Trip'. I will check the calendar for the event. I found the event taking place on 27th July 2024 at 06:00. I will update this event.\nThe user wants two people added as invitees. Lucas and Cookie. I will try and find the m in the users contacts. I found them. Lucas Garcia and Cookie Watson. I add them to the event and inform the user that the event has been updated.",
            success_conditions=[
                {
                    "input_text": "1. The calendar event 'Hiking Trip'that occurs on July 27th 2024 at 06:00 is updated to include Lucas Garcia and Cookie Watson as invitees.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "modify_calendar_event",
                "search_calendar_events",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the existing “Hiking Trip” event
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
                # Milestone 1 – The “Hiking Trip” event now contains Cookie Watson and Lucas Garcia
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Hiking Trip",
                                    "start_datetime_iso": "2024-07-27T06:00:00-07:00",
                                    # Check that both new invitees were added (others may remain)
                                    "attendees_names": [
                                        ["Cookie Watson", "Lucas Garcia"]
                                    ],
                                    "creation_datetime_iso": "2024-07-26T19:15:00-07:00",
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
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_15_4661088f-d6c0-4151-a81e-418b4bbbabd6_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_15",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T21:30:00-07:00",
            is_read_time="2024-07-26T21:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to remind yourself did Cookie say everyone's going to the hike tomorrow? "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did Cookie say everybody's going hiking tomorrow?",
                },
            ],
            reasoning='The user wants to know "did Cookie say everybody\'s going hiking tomorrow?".\n\nOkay, firstly, I\'ll check the user\'s Messages to see if they\'ve received any from "Cookie" about "hiking".\n\nGreat, they have. Now I need to see if there any messages that match the above description.\n\nGreat, they received a message from Cookie at 19:10:00 on July 26th, 2024 with the content "Theo, everyone\'s confirmed. What\'s the meeting time?".  This has to be what the user is referring to in their request.\n\nI will now present this message to them. ',
            success_conditions=[
                {
                    "input_text": "1. The user is presented with the message received from Cookie Watson at 19:10:00 on July 26th, 2024 with the content \"Theo's everyone's confirmed. What's the meeting time?\".",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
            milestones=[
                # Milestone 0 — The agent invokes a message-retrieval tool to look for Cookie’s message
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
                # Milestone 1 — The agent answers the user, quoting or paraphrasing Cookie’s line that “everyone’s confirmed”
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
                                            "everyone's confirmed",
                                            "everyone confirmed",
                                            "everybody's confirmed",
                                            "everybody confirmed",
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
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_15_9d15a0f3-bbe6-4c6f-9bdf-a0beabe064de_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_15",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T20:10:00-07:00",
            is_read_time="2024-07-26T20:10:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to text Lucas and ask if he can give you a lift to the hike tomorrow, since you are bringing a lot of equipment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Do you think you could message Lucas for tomorrow and ask "Any chance of getting a lift to the hike tomorrow? I have a lot of our supplies"',
                },
            ],
            reasoning='The user asked me to message a Lucas. I\'m going to check for Lucas in the user\'s contacts, and I found "Lucas Garcia", who is the only Lucas I can find.\n\nWith the user\'s confirmation, I will send Lucas Garcia the message "Any chance of getting a lift to the hike tomorrow? I have a lot of our supplies".',
            success_conditions=[
                {
                    "input_text": '2. The system will send the message "Any chance of getting a lift to the hike tomorrow? I have a lot of our supplies" to Lucas Garcia. ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent uses a contact-lookup tool to find Lucas
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
                # Milestone 1 – Result from Milestone 0 includes Lucas Garcia
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
                                                "value": "Lucas Garcia",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "lucas.garcia@example.com",
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
                # Milestone 2 – A new message is sent to Lucas with the requested content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At minimum Lucas must be a participant
                                    "participants_addresses": [
                                        [("1234-5678-9110", "lucas.garcia@example.com")]
                                    ],
                                    "content": "Any chance of getting a lift to the hike tomorrow?",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-26T20:10:00-07:00",
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
            name="THEO_APPLESEED_15_ff7ecdf3-7e80-4b53-88f9-9cbe2cabedd9_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_15",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T20:20:00-07:00",
            is_read_time="2024-07-26T20:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        'You want to message John Quinn saying "Sorry if Cookie is being a lot right now, sometimes she can be like this when she is stressed out!". '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Can you send a message to John saying "Sorry if Cookie is being a lot right now, sometimes she can be like this when she is stressed out!"',
                },
            ],
            reasoning="The user wants to send a message to John, saying \"Sorry if Cookie is being a lot right now, sometimes she can be like this when she is stressed out!\". I need to check the user's personal context to find out who John is. I found the message thread from Cookie Waston mentioning a hiking trip including John. I further checked the user's calendar and found a hiking trip with John Quinn on the next day. I found it is the contact for John Quinn, so with the user's confirmation I can send this text as requested.",
            success_conditions=[
                {
                    "input_text": "1. The system will check the user's contacts for a John Quinn.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. A message is sent to John Quinn saying "Sorry if Cookie is being a lot right now, sometimes she can be like this when she is stressed out!"',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_message",
                "search_messages",
                "get_all_messages",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – Agent looks up John Quinn in contacts
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
                # Milestone 1 – Verify that the contact for John Quinn was returned from the previous tool call
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
                                                "value": "John Quinn",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "john.quinn@palantir.com",
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
                # Milestone 2 – A new message has been sent to John Quinn with the correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [("1234-5678-9108", "john.quinn@palantir.com")]
                                    ],
                                    "content": "Sorry if Cookie is being a lot right now, sometimes she can be like this when she is stressed out!",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-26T20:20:00-07:00",
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
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_15_1e8155fd-4a6a-4aad-a0e9-fa6dd8ee443c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_15",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T19:20:00-07:00",
            is_read_time="2024-07-26T19:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send a message to Cookie Watson to confirm the meeting time for the hike. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to Cookie Watson to confirm the meeting time for the hike saying, Hey just checking that meeting time is cool with you?",
                },
            ],
            reasoning="The user wants to send a message to Cookie. I'll have a look in contacts for the name Cookie. I can see the only contact containing that name is Cookie Watson so I'll pull up that number. I shall use the text provided by user and show the draft to user before sending. ",
            success_conditions=[
                {
                    "input_text": "1. Retrieve contact information for Cookie Watson.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. Send a message to Cookie Watson saying 'Hey just checking that meeting time is cool with you?'",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up Cookie Watson in the contacts database
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
                # Milestone 1 – Cookie Watson’s contact information is returned from the lookup in Milestone 0
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
                # Milestone 2 – A new outgoing message to Cookie Watson is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At minimum Cookie's phone must appear among the participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9107",
                                                "cookie.watson@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "Hey just checking that meeting time is cool with you?",
                                    "creation_datetime_iso": "2024-07-26T19:20:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
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
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_15_4661088f-d6c0-4151-a81e-418b4bbbabd6_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_15",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T21:30:00-07:00",
            is_read_time="2024-07-26T21:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to remind yourself what the last person you messaged said about everyone going hiking tomorrow. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What did the last person I messaged say about everyone going hiking tomorrow?",
                },
            ],
            reasoning="The user wants to know what the last person they messaged said about everyone going hiking tomorrow.\n\nOkay, firstly, I'll check the user's messages to see if I can find this content. \n\nGreat, I can see the last person they messaged was Cookie Watson. The last message from Cookie at 19:10:00 on July 26th, 2024 says \"Theo, everyone's confirmed. What's the meeting time?\".\nI surmise that this has to be what the user is referring to, given that it talks about \"everyone\" and is a confirmation message.\nI will now present this message to the user.",
            success_conditions=[
                {
                    "input_text": "1. The user is presented with the message received from Cookie Watson at 19:10:00 on July 26th, 2024 with the content \"Theo's everyone's confirmed. What's the meeting time?\".",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
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
                # Milestone 1 – Returned tool output includes Cookie’s confirmation message
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
                                                "value": "cookie.watson@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "everyone's confirmed",
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
                # Milestone 2 – Agent tells the user what Cookie said (must reference the key phrase)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "everyone's confirmed",
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
            name="THEO_APPLESEED_15_c4169d08-53ec-48b8-85b6-cb89abba4ac0_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_15",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_high",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T19:15:00-07:00",
            is_read_time="2024-07-26T19:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to update tomorrow's hiking trip event to add Cookie and Lucas as invitees. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Update the calendar event ' Hiking Trip' to add Lucas and Cookie as invitees.",
                },
            ],
            reasoning="The user wants to update an event called 'Hiking Trip'. I will check the calendar for the event. I found the event taking place on 27th July 2024 at 06:00. I will update this event.\nThe user wants two people added as invitees. Lucas and Cookie. I will try and find the m in the users contacts. I found them. Lucas Garcia and Cookie Watson. I add them to the event and inform the user that the event has been updated.",
            success_conditions=[
                {
                    "input_text": "1. The calendar event 'Hiking Trip'that occurs on July 27th 2024 at 06:00 is updated to include Lucas Garcia and Cookie Watson as invitees.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_calendars",
                "modify_calendar_event",
                "search_calendar_events",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent searches or lists calendar events to locate the “Hiking Trip”
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
                # Milestone 1 – The “Hiking Trip” calendar event is updated to include Cookie and Lucas
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Hiking Trip",
                                    "start_datetime_iso": "2024-07-27T06:00:00-07:00",
                                    # Verify both new invitees are present (allowing existing attendees to remain)
                                    "attendees_names": [
                                        ["Cookie Watson", "Lucas Garcia"]
                                    ],
                                    "creation_datetime_iso": "2024-07-26T19:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
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
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_15_3da3275e-681b-4ceb-aa91-aab5ebc682db_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_15",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T19:15:00-07:00",
            is_read_time="2024-07-26T19:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what time Cookie last messaged you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I get my last message from my college friend today?",
                },
            ],
            reasoning="The user is asking about the time of a message.\nI should first determine who they are referring to by checking their contact list. \nI can see two contacts tagged as college friend: John Quinn and Cookie Watson.\nThe user is asking about a message received today, I should their conversations with John Quinn and Cookie Watson to determine the exact message being queried.\nI can see no messages from John Quinn received today.\nI can see multiple messages from Cookie Watson received today.\nI can see that the most recent message from Cookie Watson was received July 26, 2024 at 19:10.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1) Time most recent message was received from Cookie Watson confirmed as 19:10 on July 26, 2024.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent retrieves messages (should involve either search_messages or get_all_messages)
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
                # Milestone 1 – Confirm the most recent message from Cookie (19:10 on 2024-07-26) was present in the tool output
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
                                                "value": "cookie.watson@example.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-26T19:10:00-07:00",
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
                # Milestone 2 – Agent tells the user the correct time of the last message
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
                                            "19:10",
                                            "7:10 pm",
                                            "7:10pm",
                                            "7:10 p.m.",
                                        )
                                    ],
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
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_15_e03fb54b-fabc-443a-aec0-5d2e252a0dbc_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_15",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T19:15:00-07:00",
            is_read_time="2024-07-26T19:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know if you replied to Cookie yet. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I reply to Cookie yet?",
                },
            ],
            reasoning="The user wants to know if they replied to Cookie yet. I know that they have one contact by that name called Cookie Watson so they must mean them. Now I'll check messages with Cookie Watson to see if the user sent her a text response. I see that the user sent Cookie a text today, July 26th at 19:12",
            success_conditions=[
                {
                    "input_text": "1. Messages are checked for a message   response sent from the user to Cookie Watson and returns the message sent from the user to Cookie Watson on July 26th at 19:12.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The message is shown to the user. ",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks through messages (must call a message-retrieval tool)
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
                # Milestone 1 – Confirm the retrieved thread contains the specific reply sent to Cookie
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
                                                "value": "Great! Let's meet at 6 AM at the trailhead.",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-26T19:12:00-07:00",
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
                # Milestone 2 – The agent tells the user they already replied and shows (part of) that message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("6 am", "6am", "6:00 am", "06:00")],
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
            name="THEO_APPLESEED_15_6d3aa8da-7afc-4385-8c69-dbb31e1f8098_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_15",
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
            reference_time="2024-07-26T19:20:00-07:00",
            is_read_time="2024-07-26T19:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to move the hike on the 27th up one hour to 07:00. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I think 6 am is too early this Saturday to hike I want to change the time to 7 am and get Cookie Watson to tell everybody else that is going on the hike. ",
                },
            ],
            reasoning="The user wants to change the hike time on Saturday the 27th to 07:00 from 06:00. The user would like to send that message to cookie Watson and then have her notify the others in the group. \n\nI will change the Hiking trip start time in the Calendar to 07:00 from 06:00 and first notify Cookie Watson. I will ask Cookie Watson to pass the time change on to John Quinn and Lucas Garcia. ",
            success_conditions=[
                {
                    "input_text": "1. Text Cookie Watson that you want to move the hike on Saturday to 07:00 and she should tell the others involved. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. The calendar event  "Hiking Trip" moved to "2024-07-27T07:00:00"',
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
                "get_all_contacts",
                "search_contacts",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the existing “Hiking Trip” event
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
                # Milestone 1 – Confirm the hike event was actually retrieved
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
                                                "value": "Hiking Trip",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-27T06:00:00-07:00",
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
                # Milestone 2 – Calendar event start time moved to 07:00
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Hiking Trip",
                                    "start_datetime_iso": "2024-07-27T07:00:00-07:00",
                                    "creation_datetime_iso": "2024-07-26T19:20:00-07:00",
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
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
                # Milestone 3 – Agent searches contacts (or lists) to locate Cookie Watson
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
                # Milestone 4 – A new message was sent to Cookie conveying the new 07:00 time
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
                                                "cookie.watson@example.com",
                                                "1234-5678-9107",
                                            ),
                                            (
                                                "theo.appleseed@example.com",
                                                "1234-5678-9101",
                                            ),
                                        ]
                                    ],
                                    "content": [("7 am", "7am", "07:00", "7:00 am")],
                                    "creation_datetime_iso": "2024-07-26T19:20:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_str_contains_any_similarity,
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
                (0, 1),  # calendar search -> confirm retrieval
                (1, 2),  # retrieval -> calendar update
                (3, 4),  # contact lookup -> send message
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_15_f5ce6100-eb5b-4e48-88a4-8e71a4dc1e00_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_15",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T19:20:00-07:00",
            is_read_time="2024-07-26T19:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to dictate a reply to Cookie saying that you might be a little late to the weekend outing because you need to drop your dog off. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to dictate a message reply to Cookie Watson saying \"Hi Cookie I might be a tad late to the weekend outing because I have to drop the dog at my mum's, I'll let you know on the day.\"",
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Cookie Watson.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A reply message is sent to Cookie Watson saying that you might be a little late to the weekend outing because you need to drop your dog off.",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up contact information (Cookie Watson)
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
                # Milestone 1 – Confirm Cookie Watson’s contact was returned by the tool call in Milestone 0
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
                # Milestone 2 – A new message is sent to Cookie containing the user-dictated content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Ensure Cookie is one of the participants (self can be present as well)
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9107",
                                                "cookie.watson@example.com",
                                            )
                                        ]
                                    ],
                                    # Check key phrase from the dictated reply
                                    "content": "drop the dog",
                                    "creation_datetime_iso": "2024-07-26T19:20:00-07:00",
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
                (0, 1),  # Contact lookup → confirm Cookie found
                (1, 2),  # Contact confirmed → message sent
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_15_db1bc101-9b5c-45f8-92c4-b4d5eb5e32ce_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_15",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-30T13:15:00-07:00",
            is_read_time="2024-07-30T13:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to notify the hiking group that you won't be able to make it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to the hiking group saying sorry guys I wont be able to make it",
                },
            ],
            reasoning='The user wants to send a message to a group with reference to "hiking" in its name. There is only one group in messages which matches. The user has provided the message text, so I\'ll add that as a draft before seeking confirmation to send.',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message "sorry guys I wont be able to make it" is sent to the Carpathians Hiking Group Chat at 13:15 on 30 July 2024.',
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_messages", "send_message", "search_messages"],
            milestones=[
                # Milestone 0 – Agent looks up the hiking group conversation
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
                # Milestone 1 – Message with apology is added to the Carpathians Hiking group chat
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
                                                "1234-5678-9107",
                                                "cookie.watson@example.com",
                                            ),
                                            (
                                                "1234-5678-9108",
                                                "john.quinn@palantir.com",
                                            ),
                                            (
                                                "1234-5678-9110",
                                                "lucas.garcia@example.com",
                                            ),
                                            (
                                                "1234-5678-9101",
                                                "theo.appleseed@example.com",
                                            ),
                                        ]
                                    ],
                                    "content": "sorry guys",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-30T13:15:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare with initial DB state
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieval of conversation precedes sending the message
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_15_db1bc101-9b5c-45f8-92c4-b4d5eb5e32ce_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_15",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-30T13:15:00-07:00",
            is_read_time="2024-07-30T13:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to notify the hiking group that you won't be able to make it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Message the hiking group to say 'sorry guys I wont be able to make it'",
                },
            ],
            reasoning='The user wants to send a message to a group. With the reference "hiking", I can locate one group in messages. The user has provided the message text, so I\'ll add that as a draft before seeking confirmation to send.',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message "sorry guys I wont be able to make it" is sent to the Carpathians Hiking Group Chat at 13:15 on 30 July 2024.',
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_messages", "send_message", "search_messages"],
            milestones=[
                # Milestone 0 – Agent tries to locate the hiking group conversation
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
                # Milestone 1 – New “sorry” message is sent to the Carpathians Hiking group chat
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Carpathians Hiking",
                                    "content": "sorry guys",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-30T13:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_15_3515a47b-a6cf-40a5-ab93-1499d29eab5a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_15",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T19:15:00-07:00",
            is_read_time="2024-07-26T19:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to see the last message Cookie Watson sent you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me Cookie's last message.",
                },
            ],
            reasoning="The user wants to see Cookie's last message. Let me look for Cookie in contacts. It must be Cookie Watson. I will look for the last message she sent. I will show it to the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The user is shown the last text message ,'Theo, everyone's confirmed. What's the meeting time?', sent by 1234-5678-9107 sent on July 26th at 19:10.",
                }
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
            milestones=[
                # Milestone 0 – Agent invokes a message-retrieval tool (search_messages / get_all_messages)
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
                # Milestone 1 – The retrieved tool output includes Cookie’s latest message
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
                                                "value": "cookie.watson@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Theo, everyone's confirmed. What's the meeting time?",
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
                # Milestone 2 – Agent responds to the user with Cookie’s last message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Theo, everyone's confirmed",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_15_3da3275e-681b-4ceb-aa91-aab5ebc682db_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_15",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T19:15:00-07:00",
            is_read_time="2024-07-26T19:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what time Cookie last messaged you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I get my last message from Cookie Watson?",
                },
            ],
            reasoning="The user is asking about the time of a message.\nI should check their conversation with the named contact, Cookie Watson.\nI can see that the most recent message from Cookie Watson was received July 26, 2024 at 19:10.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1) Time most recent message was received from Cookie Watson confirmed as 19:10 on July 26, 2024.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent queries the message store (must use a message-retrieval tool)
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
                # Milestone 1 – The returned messages include the most recent one from Cookie
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
                                                "value": "Cookie Watson",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-26T19:10:00-07:00",
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
                                            "19:10",  # 24-hour format
                                            "7:10",  # hour:minute
                                            "7:10 pm",
                                            "7:10 p.m.",
                                            "7 : 10 pm",  # potential unicode colon
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
            name="THEO_APPLESEED_15_cfcbce81-3101-4cce-b756-ef3a20d4d14c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_15",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T18:40:00-07:00",
            is_read_time="2024-07-27T18:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        'You send a message to your hiking folks after the trip to Big Rock Mountain today saying "Well done today guys! excellent hike, one to remember! Looking forward to the next one". '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a message to my hiking folks today saying "Well done today guys! excellent hike, one to remember! Looking forward to the next one"',
                },
            ],
            reasoning='The user wants to send a message to the hiking folks today. I need to look for who has attended the hiking. First I checked the calendar, there\'s a hiking event scheduled earlier today with invitation from John Quinn from 6 am to 10 am to Big Rock Mountain Trail. But the user mentioned "folks" so I need to look for others who have attended. I search the message history, and from Cookie Watson, on 7/26 19:02 she mentioned John and Lucas. Then I checked the user\'s contact card confirmed that it\'s John Quinn (from the calendar event) and Lucas Garcia. Then I will set up a message with them as participants for this in a group. After this I will ask for the body of the message. which is supplied at "Well done today guys! excellent hike, one to remember! Looking forward to the next one". After this, I will send the message>',
            success_conditions=[
                {
                    "input_text": '1. A message is sent to a group chat including John Quinn, Cookie Watson and Lucas Garcia stating "Well done today guys! excellent hike, one to remember! Looking forward to the next one". at 18:40pm.',
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
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – The agent queries the contacts database to locate hiking friends
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
                # Milestone 1 – Confirm that at least John Quinn was returned from the contact lookup
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
                                                "value": "John Quinn",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "john.quinn@palantir.com",
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
                            reference_milestone_node_index=0,  # depends on contact search in milestone 0
                        )
                    ]
                ),
                # Milestone 2 – A new group message to the hiking folks is sent
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
                                                "john.quinn@palantir.com",
                                                "1234-5678-9108",
                                            ),
                                            (
                                                "cookie.watson@example.com",
                                                "1234-5678-9107",
                                            ),
                                            (
                                                "lucas.garcia@example.com",
                                                "1234-5678-9110",
                                            ),
                                        ]
                                    ],
                                    "content": "Well done today guys!",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-27T18:40:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # Require that each hiking friend is present (email or phone allowed), extra addresses (e.g., Theo) are OK
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
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
            name="THEO_APPLESEED_15_ef7a5563-0418-4eb9-8016-0e7050e8144c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_15",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T19:10:00-07:00",
            is_read_time="2024-07-26T19:10:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to reply to Cookie. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message replying top Cookie that says 6PM. ",
                },
            ],
            reasoning="The user wants to reply to a contact called 'Cookie', so first I need to find this intended contact. From the user's request, I can tell they already have correspondence with this contact, so I will start in the user's messages. I found a \"Cookie Watson\" in the users chat history and I can see a message they just received from this contact that refers to a meeting time. With all of this in context, I can assume this is the intended contact. ",
            success_conditions=[
                {
                    "input_text": 'A message is sent to Cookie Watson that says "6PM". ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_messages", "send_message", "search_messages"],
            milestones=[
                # Milestone 0 – Agent tries to locate the existing conversation / message with Cookie
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
                # Milestone 1 – Confirm that the tool call in Milestone 0 returned the thread with Cookie Watson
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
                                                "value": "Cookie Watson",
                                                "partial": False,
                                            },
                                            # Either the conversation name or participant list must match;
                                            # conversation_name is sufficient for positive identification.
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
                # Milestone 2 – A new outgoing message saying “6PM” was sent to Cookie
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At minimum Cookie must be in the participants list.
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9107",
                                                "cookie.watson@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "6PM",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-26T19:10:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,  # allows “6PM”, “6 pm”, etc.
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        )
                    ],
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
    ]
