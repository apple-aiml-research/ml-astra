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
    column_list_tuple_contains_similarity,
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
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


def get_TAG_THEO_APPLESEED_pilot_plot_18(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="THEO_APPLESEED_18_7080d3e7-8bee-419c-9d81-09d8a3db92e6_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T11:35:00-07:00",
            is_read_time="2024-07-24T11:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to reply to Emily's last message and tell her that John cooks the best brownies and can bring some to share. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to the last message I received saying "John cooks the best brownies and can bring some to share."',
                },
            ],
            reasoning='The user wants me to send a reply to the last message they received. I will check their messages and set their most recent message as the recipient of the reply. The message is from Emily Rose. \nI draft the reply as the user requested. The message says "John cooks the best brownies and can bring some to share." I wait for confirmation that the message is correct from the user. After receiving confirmation from the user I send the reply to Emily Rose.',
            success_conditions=[
                {
                    "input_text": '1. A reply is sent to Emily Rose saying "John cooks the best brownies and can bring some to share."',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up the most recent message (from Emily) so it can send a reply
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
                # Milestone 1: find Emily's messages
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
                                                "value": "Emily Rose",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "That sounds wonderful. The more, the merrier!",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-24T11:30:00-07:00",
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
                    ]
                ),
                # Milestone 2 – A new outgoing message is created in the Emily conversation
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Conversation should include both Emily and Theo
                                    "participants_addresses": [
                                        [("emily.rose@example.com", "1234-5678-9109")]
                                    ],
                                    "content": "brownies",  # key phrase to verify
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-24T11:35:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,  # must at least include Emily & Theo
                                "content": column_contains_similarity,  # phrase can appear anywhere / with extra text
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against the initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieval precedes sending the reply
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_a1ba471d-3159-4e5b-9baf-87a3611008ce_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
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
            reference_time="2024-07-27T22:00:00-07:00",
            is_read_time="2024-07-27T22:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send the organizer a message thanking her for organising such a great event for the neighbourhood. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send the coordinator a message saying thank her for organising such a great event for the neighbourhood, and mention the event name directly in the message.",
                },
            ],
            reasoning='The user wants me to send tht coordinator a message saying thank her for organising such a great event for the neighbourhood. I first search for user\'s calendar, and found that an event called "Neighborhood Gathering" happend earlier today and the organizer is "Emily Rose". Looking through their contacts, Emily Rose is noted as the user\'s neighbour so I can assume she is the intended recipient. I\'ll write the intended message saying Hey, thank you for organising such a great event for the neighbourhood gathering, and present it to the user. With their approval I will send it.',
            success_conditions=[
                {
                    "input_text": "1. A message is sent to Emily Rose on the 27th July 2024 at 22:00 saying thank her for organising such a great event and mention 'neighborhood gathering' directly in the message. ",
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
                "send_message",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – Agent attempts to look up calendar information
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
                # Milestone 1 – Returned calendar data contains the “Neighborhood Gathering” event with the correct start time
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
                                                "value": "Neighborhood Gathering",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-27T18:00:00-07:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-07-27T21:00:00-07:00",
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
                # Milestone 2 – The agent looks up the neighbour (Emily) in the contacts list
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
                # Milestone 3 – Ensure Emily Rose was actually found in the contact-search results
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
                                                "value": "Emily Rose",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9109",
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
                            reference_milestone_node_index=2,  # depend on Milestone-2 tool output
                        )
                    ]
                ),
                # Milestone 4 – A new message has been sent to Emily containing the user’s thanks
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
                                                "1234-5678-9101",
                                                "theo.appleseed@example.com",
                                            ),  # self (Theo) – any of these must appear
                                            (
                                                "1234-5678-9109",
                                                "emily.rose@example.com",
                                            ),  # Emily
                                        ]
                                    ],
                                    "content": "gathering",
                                    "creation_datetime_iso": "2024-07-27T22:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # Both Theo and Emily must be among the participants, with no extras
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                # Make sure the body broadly contains the gratitude phrase
                                "content": column_contains_similarity,
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
                (0, 1),  # Calendar search
                (2, 3),  # Contact search → confirmation Emily was retrieved
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_b37c1e55-0019-4ab0-b0c1-3f981353f760_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T08:00:00-07:00",
            is_read_time="2024-07-24T08:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to change the name of your event from Neighborhood gathering to Orchard County Community Mingle "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Rename the thing called Neighborhood gathering to Orchard County Community Mingle",
                },
            ],
            reasoning='The user wants to change the name of an event called Neighborhood gathering and change it to Orchard County Community Mingle. I go through the user\'s listed events and I see one event listed on July 27 2024 at 18:00 titled "Neighborhood gathering". This must be the event the user is referring to. I will change the name of this event to "Orchard County Community Mingle", and I will inform the user of this change.',
            success_conditions=[
                {
                    "input_text": '1. The event "Neighborhood Gathering" at 18:00 on July 27, 2024 is renamed to "Orchard County Community Mingle"\n',
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
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events to locate the one that must be renamed
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
                # Milestone 1 – Verify that the correct event (“Neighborhood Gathering” on July 27 @ 18:00) was indeed retrieved
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
                                                "value": "Neighborhood Gathering",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-27T18:00:00-07:00",
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
                # Milestone 2 – Calendar event has been updated with the new name
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Orchard County Community Mingle",
                                    "start_datetime_iso": "2024-07-27T18:00:00-07:00",
                                    "creation_datetime_iso": "2024-07-24T08:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
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
                (0, 1),  # Event search → confirm correct event found
                (1, 2),  # Event confirmed → event renamed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_937760a7-de87-405d-950d-9bf3558bbed6_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T21:15:00-07:00",
            is_read_time="2024-07-27T21:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to let Emily know you had fun at the neighbourhood gathering. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send this to Emily; "Hey Emily, had great fun at the gathering today!"',
                },
            ],
            reasoning="Ok so the user wants to send a given message to Emily. First, I'll establish who Emily is. There is only one Emily in the user's contacts so I'm assuming they're referring to Emily Rose. Next is the method of contact. They most recently contacted Emily through text so it would make most sense to continue this. I will now send the user's given message to Emily Rose at 21:15 on 27 July 2024. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message "Hey Emily, had great fun at the gathering today!" is sent to Emily Rose at 21:15 on 27 July 2024. ',
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent tries to identify Emily in contacts
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
                # Milestone 1 – Verify Emily Rose was returned from the contact search
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
                                                "value": "Emily Rose",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "emily.rose@example.com",
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
                    ]
                ),
                # Milestone 2 – Message sent to Emily at conclusion of gathering
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
                                                "emily.rose@example.com",
                                                "1234-5678-9109",
                                            ),  # Emily Rose
                                            (
                                                "theo.appleseed@example.com",
                                                "1234-5678-9101",
                                            ),  # Theo
                                        ]
                                    ],
                                    "content": "had great fun",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-27T21:15:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare to initial DB state
                        ),
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.CONTACT,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_c3c38c0d-b967-4148-8ced-c6781eff3cde_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T17:35:00-07:00",
            is_read_time="2024-07-27T17:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You are feeling sick and won't be able to attend the Neighborhood Gathering this evening. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I'm too sick to go to the event tonight so please delete it.",
                },
            ],
            reasoning="The user says they're too sick to go to the event tonight. I'll check their calendar for this evening to see what's on their schedule.\n\nI found one event tonight (2024-07-27): Neighborhood Gathering from 18:00 to 21:00. Since the user is too sick to attend this event, I'll delete it from their schedule and inform them that I've done so.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. Event named 'Neighborhood Gathering' from 18:00 to 21:00 on 2024-07-27 is deleted.",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – The agent tries to look up today’s calendar events
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
                # Milestone 1 – Confirm the “Neighborhood Gathering” event for 2024-07-27 18:00 was returned
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
                                                "value": "Neighborhood Gathering",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-27T18:00:00-07:00",
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
                # Milestone 2 – The calendar event has been removed from the CALENDAR database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Neighborhood Gathering",
                                    "start_datetime_iso": "2024-07-27T18:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                ),
                # Milestone 3 – The user receives a confirmation that the event was deleted
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
                                            "deleted",
                                            "removed",
                                            "cancelled",
                                            "canceled",
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
                (0, 1),  # Lookup → confirm event found
                (1, 2),  # Confirm event → event removed
                (2, 3),  # Removal → confirmation to user
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_ed3a2e1e-d3d8-4d37-8501-9248e51cb73d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T12:00:00-07:00",
            is_read_time="2024-07-24T12:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send John Quinn an email letting him know that he's going with you to a neighborhood gathering. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send my Quinn friend an email saying "Hey John Boy, my neighbor Emily Rose invited me to some neighborhood gathering going on on the 27th and I told her you would be there. Can\'t wait to catch up then. It starts at 6PM."',
                },
            ],
            reasoning="User has provided the text of what they want to send by email to a recipient. The recipient is referred to as their  Quinn friend. I wonder who that is. I should check their contacts. I see the user has one contact listed as a college friend with the surname John Quinn. This must be who they want to email. I'll draft the email and seek user's approval before sending. ",
            success_conditions=[
                {
                    "input_text": "An email is sent to John Quinn with the text \"Hey John Boy, my neighbor Emily Rose invited me to some neighborhood gathering going on on the 27th and I told her you would be there. Can't wait to catch up then. It's starts at 6PM.\"",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_email"],
            milestones=[
                # Milestone 0 – Agent looks up the Quinn contact
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
                # Milestone 1 – Verify John Quinn’s contact information was retrieved
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
                # Milestone 2 – Email sent to John Quinn with correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["john.quinn@palantir.com"]
                                    ],
                                    "status": "sent",
                                    "body": "neighbor Emily Rose",
                                    "creation_datetime_iso": "2024-07-24T12:00:00-07:00",
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_b82ae911-dc4d-46b7-9852-70d3dc8c76a5_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-28T13:00:00-07:00",
            is_read_time="2024-07-28T13:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what time your Neighborhood gathering was yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time was my event 'Neighborhood gathering' at yesterday?",
                },
            ],
            reasoning="The user wants to know what time their event 'Neighborhood gathering' was on yesterday (that is, July 27). I will look for the event titled 'Neighborhood gathering' in user's calendar. I will inform the user that their event ran from 18:00 to 21:00.",
            success_conditions=[
                {
                    "input_text": "1.The user is informed that their event 'Neighborhood gathering' on July 27th 2024 ran from 18:00 to 21:00.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent attempts to look up calendar information
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
                # Milestone 1 – Returned calendar data contains the “Neighborhood Gathering” event with the correct start time
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
                                                "value": "Neighborhood Gathering",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-27T18:00:00-07:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-07-27T21:00:00-07:00",
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
                # Milestone 2 – Agent informs the user of the event time window 6 pm–9 pm / 18:00–21:00
                Milestone(
                    snapshot_constraints=[
                        # Check the start time mention
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "18:00",
                                            "6:00",
                                            "6 pm",
                                            "6pm",
                                            "6 p.m.",
                                            "6 o'clock",
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
                (0, 1),  # calendar lookup -> confirmation of event retrieved
                (1, 2),  # event retrieved -> user informed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_b82ae911-dc4d-46b7-9852-70d3dc8c76a5_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-28T13:00:00-07:00",
            is_read_time="2024-07-28T13:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what time your Neighborhood gathering was yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time was the Orchard mingle thing yesterday?",
                },
            ],
            reasoning="The user is asking about the time of an event, which they are referring to as \"Orchard mingle thing\". \nI should consult their calendar and attempt to determine which event they mean. The user wants to find information about an event the day before the reference time, that is, July 27 2024, this will narrow my search.\nI see only one potential match scheduled for yesterday, that is, 'Neighborhood gathering', because the user is using the words 'Orchard' (which surely refers to Orchard County) and 'mingling', which is another way of referring to a gathering. Also, this event took place on July 27th 2024 and ran from 18:00 -21:00.\nTherefore, I will inform the user of these times.",
            success_conditions=[
                {
                    "input_text": "1.The user is informed that their event 'Neighborhood gathering' on July 27th 2024 ran from 18:00 to 21:00.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – A calendar-related tool is invoked
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
                # Milestone 1 – The expected event is present in the tool output from Milestone 0
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
                                                "value": "Neighborhood Gathering",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-27T18:00:00-07:00",
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
                # Milestone 2 – The agent tells the user the event time window
                Milestone(
                    snapshot_constraints=[
                        # Presence of the start time (6 pm / 18:00)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        ("18:00", "6 pm", "6pm", "6 p.m.", "6:00")
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
                (0, 1),  # Tool call → verify event found
                (1, 2),  # Event found → user informed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_ed3a2e1e-d3d8-4d37-8501-9248e51cb73d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T12:00:00-07:00",
            is_read_time="2024-07-24T12:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send your old friend John an email letting him know that he's going with you to a neighborhood gathering. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send my old college friend John the following via email: \"Hey John Boy, my neighbor Emily Rose invited me to some neighborhood gathering going on on the 27th and I told her you would be there. Can't wait to catch up then. It's starts at 6PM.\"",
                },
            ],
            reasoning='The user wants to send an email to their old friend John with the text "Hey John Boy, my neighbor Emily Rose invited me to some neighborhood gathering going on on the 27th and I told her you would be there. Can\'t wait to catch up then. It\'s starts at 6PM." The user has two contacts called John, with John Appleseed as father and John Quinn as College Friend. So I presume I should draft an email to John Quinn as the user mentioned "old friend". I shall show the draft of the email to the user first for approval before sending. ',
            success_conditions=[
                {
                    "input_text": "An email is sent to John Quinn with the text \"Hey John Boy, my neighbor Emily Rose invited me to some neighborhood gathering going on on the 27th and I told her you would be there. Can't wait to catch up then. It's starts at 6PM.\"",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_email"],
            milestones=[
                # Milestone 0 – Agent looks up contacts (either searches or lists all)
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
                # Milestone 1 – The returned contact list includes John Quinn with the correct phone number
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
                                "content": column_one_similarity,
                            },
                            reference_milestone_node_index=0,  # depends on tool output from milestone 0
                        )
                    ]
                ),
                # Milestone 2 – Verify that an email was sent to John Quinn with the correct text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["john.quinn@palantir.com"]
                                    ],
                                    "status": "sent",
                                    "body": "Hey John Boy",
                                    "creation_datetime_iso": "2024-07-24T12:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                # Only require the opening phrase; the full body can vary in punctuation or minor wording
                                "body": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_c1221c0f-9674-4b18-97ff-d882fb820aa9_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T10:00:00-07:00",
            is_read_time="2024-07-27T10:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to move the time of your neighbourhood gathering event to half an hour later. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Change the time of the neighbourhood gathering event to a half hour later",
                },
            ],
            reasoning='It looks like the user wants to change the time of an event. I go through the user\'s events for the day and I see one event named "Neighbourhood Gathering" happening on July 27, 2024, at 18:00. This must be the event the user is referring to, so I will adjust the time so that it now starts at 18:30',
            success_conditions=[
                {
                    "input_text": '1. The event "Neighborhood Gathering" on July 27, 2024 at 18:00 at 128 Neighborly St, Orchard County, CA time is changed to 18:30.',
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
            ],
            milestones=[
                # Milestone 0 – Agent queries calendar to locate the event that needs changing
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
                # Milestone 1 – Confirm that the correct calendar event was returned in Milestone 0
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
                                                "value": "Neighborhood Gathering",
                                                "partial": False,
                                            },
                                            # original start time (optional but strengthens check)
                                            "start_datetime_iso": {
                                                "value": "2024-07-27T18:00:00-07:00",
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
                        ),
                    ],
                ),
                # Milestone 2 – Event time has been successfully updated to 18:30
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Neighborhood Gathering",
                                    "start_datetime_iso": "2024-07-27T18:30:00-07:00",
                                    "creation_datetime_iso": "2024-07-27T10:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_exact_match_similarity,
                                "start_datetime_iso": column_contains_similarity,
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
            name="THEO_APPLESEED_18_c3c38c0d-b967-4148-8ced-c6781eff3cde_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T17:35:00-07:00",
            is_read_time="2024-07-27T17:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You are feeling sick and won't be able to attend the Neighborhood Gathering this evening. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my Neighborhood Gathering.",
                },
            ],
            reasoning="The user wants to delete their Neighborhood Gathering. Let's check to see if they have an event with this title.\n\nI found the relevant event today (2024-07-27) from 18:00 to 21:00. I'll delete it and let the user know.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The event "Neighborhood Gathering" on July 27, 2024, from 18:00 to 21:00 is deleted.',
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events to locate the Neighborhood Gathering
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
                # Milestone 1 – Verify that the Neighborhood Gathering event details were actually retrieved
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
                                                "value": "Neighborhood Gathering",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-27T18:00:00-07:00",
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
                            reference_milestone_node_index=0,  # depends on the search in Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – Confirm the calendar event has been removed
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Neighborhood Gathering",
                                    "start_datetime_iso": "2024-07-27T18:00:00-07:00",
                                    "end_datetime_iso": "2024-07-27T21:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # search → confirm retrieval
                (1, 2),  # retrieval → deletion
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_937760a7-de87-405d-950d-9bf3558bbed6_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T21:15:00-07:00",
            is_read_time="2024-07-27T21:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to let Emily know you had fun at the neighbourhood gathering. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Text Emily this; "Hey Emily, had great fun at the gathering today!"',
                },
            ],
            reasoning="Ok so the user wants to text Emily a given message. First, I'll establish who Emily is. There is only one Emily in the user's contacts so I'm assuming they're referring to Emily Rose. Next is the method of contact. The user states to use text so I will use text messaging. I will now send the user's given message to Emily Rose at 21:15 on 27 July 2024. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message "Hey Emily, had great fun at the gathering today!" is sent to Emily Rose at 21:15 on 27 July 2024. ',
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up Emily’s contact information
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
                # Milestone 1 – The returned contact list includes Emily Rose
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
                                                "value": "Emily Rose",
                                                "partial": False,
                                            },
                                            # Either phone or email confirms identity (partial False = exact)
                                            "phone_number": {
                                                "value": "1234-5678-9109",
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
                # Milestone 2 – The message to Emily is sent (new row in MESSAGING)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Both Emily and Theo must participate, represented by at least one
                                    # identifier for each (email or phone).  No extras allowed.
                                    "participants_addresses": [
                                        [
                                            (
                                                "emily.rose@example.com",
                                                "1234-5678-9109",
                                            ),
                                            (
                                                "theo.appleseed@example.com",
                                                "1234-5678-9101",
                                            ),
                                        ]
                                    ],
                                    "content": "great fun",
                                    "creation_datetime_iso": "2024-07-27T21:15:00-07:00",
                                    "status": "sent",
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
                            reference_milestone_node_index=-1,  # compare to initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_b37c1e55-0019-4ab0-b0c1-3f981353f760_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T08:00:00-07:00",
            is_read_time="2024-07-24T08:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to change the name of your event from Neighborhood gathering to Orchard County community assembly. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Change the name of my event on this Saturday evening to Orchard County community assembly",
                },
            ],
            reasoning='The user wants to change the name of an event. The user is specifically mentioning the event that they want to change is on this Saturday evening. After searching for user\'s calendar, it should be "Neighborhood gathering" which takes place on July 27, 2024, from 18:00. Based on this information, this is the event the user will want to rename. According to their query, I will rename this event to Orchard County community assembly, and I will inform the user of this',
            success_conditions=[
                {
                    "input_text": '1. The event "Neighborhood Gathering" at 18:00 on July 27, 2024 is renamed to Orchard County community assembly\n',
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
            ],
            milestones=[
                # Milestone 0 – Agent tries to locate the calendar event
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
                # Milestone 1 – Confirm the specific event (Neighborhood Gathering) was returned
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
                                                "value": "Neighborhood Gathering",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-27T18:00:00-07:00",
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
                # Milestone 2 – Event has been renamed (calendar row updated)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Orchard County community assembly",
                                    "start_datetime_iso": "2024-07-27T18:00:00-07:00",
                                    "creation_datetime_iso": "2024-07-24T08:00:00-07:00",
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
            name="THEO_APPLESEED_18_a1ba471d-3159-4e5b-9baf-87a3611008ce_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T22:00:00-07:00",
            is_read_time="2024-07-27T22:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send Emily a message thanking her for organising such a great event. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send Emily a message saying 'Hey Emily, thank you for organising such a great event'.",
                },
            ],
            reasoning="The user wants me to send Emily a message saying 'Hey Emily, thank you for organising such a great event'. Looking through the user's contacts I can see they have one contact corresponding to 'Emily' as 'Emily Rose'. I can assume she is the intended recipient. I'll present the message to the user and with their approval I will send it.",
            success_conditions=[
                {
                    "input_text": "1. A message is sent to Emily Rose on the 27th July 2024 at 22:00 saying 'Hey Emily, thank you for organising such a great event'. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up Emily’s contact information
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
                # Milestone 1 – Verify that Emily Rose was returned from the contact search
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
                                                "value": "Emily Rose",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "emily.rose@example.com",
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
                # Milestone 2 – A new message has been sent to Emily with the correct content
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
                                                "1234-5678-9109",
                                                "emily.rose@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "Hey Emily, thank you for organising such a great event",
                                    "creation_datetime_iso": "2024-07-27T22:00:00-07:00",
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
                (0, 1),  # Contact search → confirm Emily retrieved
                (1, 2),  # Emily retrieved → message sent
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_7080d3e7-8bee-419c-9d81-09d8a3db92e6_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T11:35:00-07:00",
            is_read_time="2024-07-24T11:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to reply to a last message and thank her for being so nice about bringing John to the neighborhood gathering. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to the last message I received from my neighbor saying "Thanks so much for being so nice and welcoming my friend John to the neighborhood gathering!"',
                },
            ],
            reasoning='The user wants me to send a reply to the last message they received from their neighbor. I will go through the user\'s contacts to understand who they might be referring to. In the contacts, I see "Emily Rose" listed as the user neighbor. Therefore, I will check the user messages and set their most recent message from Emily Rose as the recipient of the reply. \nI draft the reply as the user requested. The message says "Thanks so much for being so nice and welcoming my friend John to the neighborhood gathering!" I wait for confirmation that the message is correct from the user. After receiving confirmation from the user I send the reply to Emily Rose.',
            success_conditions=[
                {
                    "input_text": '1. A reply is sent to Emily Rose saying "Thanks so much for being so nice and welcoming my friend John to the neighborhood gathering!"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages", "send_message"],
            milestones=[
                # Milestone 0 — the agent looks up the latest conversation/message with Emily
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
                # M1: Emily's messages found
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
                                                "value": "Emily Rose",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "That sounds wonderful. The more, the merrier!",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-24T11:30:00-07:00",
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
                    ]
                ),
                # Milestone 1 — a reply message to Emily was actually sent that includes the requested wording
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Ensure Emily is in the conversation participants
                                    "participants_addresses": [
                                        [("emily.rose@example.com", "1234-5678-9109")]
                                    ],
                                    # Message body must mention John looking strong / feeling insecure
                                    "content": "Thanks so much for being so nice",
                                    "creation_datetime_iso": "2024-07-24T11:35:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # Emily must appear in the participants list (extras allowed)
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                # Relaxed check that the new message contains key phrase(s)
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial DB state
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_b31fc9e1-040f-4c26-8ea5-c08ef2997292_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-28T06:00:00-07:00",
            is_read_time="2024-07-28T06:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You stayed till late at the neighborhood gathering and are now very tired.  You decide not to leave the house today. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want you to cancel the Cooking Class on today.",
                },
            ],
            reasoning="The user is asking me to cancel an event.\nI should find this in the user's calendar.\nI have found the queried event, Cooking Class on July 28, 2024 at 13:00-16:00, I will go ahead and cancel the event as requested.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1) Cooking Class event on July 28, 2024 at 13:00-16:00 is deleted.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 –  Agent looks up the calendar to locate the event that needs cancellation
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
                # Milestone 1 –  Confirm the Cooking Class event appears in the tool output from Milestone 0
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
                                                "value": "Cooking Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-28T13:00:00-07:00",
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
                        ),
                    ],
                ),
                # Milestone 2 –  Verify the Cooking Class event has been removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Cooking Class",
                                    "start_datetime_iso": "2024-07-28T13:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_exact_match_similarity,
                                "start_datetime_iso": column_contains_similarity,
                            },
                            reference_milestone_node_index=-1,  # compare against initial state
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
            name="THEO_APPLESEED_18_42933700-54be-4f03-8d66-e84bec7baa33_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T11:40:00-07:00",
            is_read_time="2024-07-24T11:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to check if Emily has responded yet as you're hoping to bring your friend John to the gathering and need to let him know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you check if the last person I was messaging has responded? If she's happy for more people to come, let my friend John know he can join the neighborhood gathering on Saturday.",
                },
            ],
            reasoning="Right so, the user wants to first check if the last person they were texting with has replied. I can see that the most recent message is received from Emily Rose on 24th July at 11:30 saying 'That sounds wonderful. The more, the merrier!'. I can then read this out to the user to inform them, and it confirms she is happy for more people to come.\n\nNext, they want to message 'my friend John' that he can join the neighborhood gathering on Saturday. The user has two contacts named 'John': 'John Quinn' and 'John Appleseed'. Looking at the two contacts, I can see 'John Quinn' has a 'College Friend' relationship type listed, while 'John Appleseed' is entered as 'Father'. So the user means 'John Quinn', and I send him a message letting him know he can join the neighborhood gathering on Saturday.",
            success_conditions=[
                {
                    "input_text": "1. The latest message from Emily Rose received on the 24th July 2024 at 11:30 saying 'That sounds wonderful. The more, the merrier!' is read out to the user.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. A message is sent to John Quinn saying 'Hey man, you can join the neighborhood gathering on Saturday, what do you think?'. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "send_message",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent tries to look up the latest messages
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
                # Milestone 1 – Verify that the Emily Rose message was actually retrieved
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
                                                "value": "emily.rose@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "That sounds wonderful. The more, the merrier!",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-24T11:30:00-07:00",
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
                # Milestone 2 – Agent reports the content back to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "That sounds wonderful",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        )
                    ],
                    # The agent sends the message to John (milestone 3) BEFORE it replies to
                    # the user, which is the only order the harness allows: the reply is the
                    # final turn. The default guardrail would forbid the MESSAGING write that
                    # milestone 3 requires, making this milestone unreachable. Milestone 3
                    # still grades that write, so excluding it here opens no hole.
                    guardrail_database_exclusion_list=[DatabaseNamespace.MESSAGING],
                ),
                # Milestone 3 – A new outgoing message to John Quinn is created
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
                                                "theo.appleseed@example.com",
                                                "1234-5678-9101",
                                            ),
                                        ]
                                    ],
                                    "content": "neighborhood gathering",
                                    "creation_datetime_iso": "2024-07-24T11:40:00-07:00",
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
                (0, 1),  # Retrieved messages → verified Emily’s message present
                (1, 2),  # Verified retrieval → responded to user
                (2, 3),  # After informing user → sent message to John
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_36ebbf0f-843f-4b05-b997-8b8b984bc806_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T18:10:00-07:00",
            is_read_time="2024-07-27T18:10:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to dictate a reply to Emily apologising for being late to the neighborhood gathering event. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a message reply to Emily Rose saying "Apologies for being late to the party."',
                },
            ],
            reasoning='The user wants to dictate a reply to the contact called Emily Rose.\n\nI should locate the message history with this contact by searching their name in the user\'s Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say: "Apologies for being late to the party.". I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A reply message is sent to Emily Rose with the text "Apologies for being late to the party."',
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "send_message",
                "search_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent tries to locate Emily (either through the contact list or existing messages)
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
                # Milestone 1 – A new message is sent that apologises for being late
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [("emily.rose@example.com", "1234-5678-9109")]
                                    ],
                                    "content": "Apologies for being late to the party.",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-27T18:10:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,  # must include Emily
                                "content": column_contains_similarity,  # must contain apology text
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with pre-task state
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox traces when checking DB change
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_73897293-4cb9-4dfb-97b4-786d4efc25d4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T21:00:00-07:00",
            is_read_time="2024-07-27T21:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        'You want to send a message to Emily Rose saying "Thanks for tonight Emily! looking forward to the next one!" '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a message saying, "Thanks for tonight Emily! looking forward to the next one!"',
                },
            ],
            reasoning='The user wants to send a message saying, "Thanks for tonight Emily! looking forward to the next one!". The user states Emily so I will search for the contact card (Emily Rose) and add and send the message.',
            success_conditions=[
                {
                    "input_text": '1. A text message is sent to Emily Rose via "1234-5678-9109" saying "Thanks for tonight Emily! looking forward to the next one!"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up Emily Rose in contacts
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
                # Milestone 1 – Verify Emily Rose was returned from the contact-search in Milestone 0
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
                                                "value": "Emily Rose",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "emily.rose@example.com",
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
                    ]
                ),
                # Milestone 2 – Confirm a new message was sent to Emily with the correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [("emily.rose@example.com", "1234-5678-9109")]
                                    ],
                                    "content": "Thanks for tonight",
                                    "creation_datetime_iso": "2024-07-27T21:00:00-07:00",
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
                (0, 1),  # Contact lookup → verify Emily
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_0bb0fa14-e086-4e32-acd3-843a413d87cc_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T17:35:00-07:00",
            is_read_time="2024-07-27T17:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send a message to Emily Rose saying 'Hey Emily, my friend John won't make it after all.  ' "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to Emily Rose saying 'Hey Emily, my friend John won't make it after all.'",
                },
            ],
            reasoning="The user wants to send a message to Emily Rose. I'll check the user's contacts for a contact under this name. There is a contact under that name so I'll pull up that number. Next I'll ask the user what they'd like to say. Okay, now that I have the content of the message I can send it and notify the user.",
            success_conditions=[
                {
                    "input_text": "1. A message to Emily Rose saying 'Hey Emily, my friend John won't make it after all.'",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up Emily Rose in contacts
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
                # Milestone 1 – Returned contact information contains Emily Rose
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
                                                "value": "Emily Rose",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9109",
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
                # Milestone 2 – A new message was sent to Emily with the correct content
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
                                                "1234-5678-9109",
                                                "emily.rose@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "Hey Emily, my friend John won't make it after all.",
                                    "creation_datetime_iso": "2024-07-27T17:35:00-07:00",
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
                (0, 1),  # Contact lookup → confirm Emily found
                (1, 2),  # Emily found → message sent
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_42933700-54be-4f03-8d66-e84bec7baa33_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T11:40:00-07:00",
            is_read_time="2024-07-24T11:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to check if Emily has responded yet as you're hoping to bring your friend John to the gathering and need to send a message and let him know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to send John a message inviting him to the neighbourhood gathering but first need to know has Emily responded then send it if so?",
                },
            ],
            reasoning="Okay so the user wants to send a message to John, but they need to first know if Emily has responded. I can see from the message thread that Emily Rose has responded on 24th July at 11:30 saying 'That sounds wonderful. The more, the merrier!', which suggests Emily is OK with my friend John coming to the gathering. I can read that out to the user.\n\nSecondly, they want to send a message to John. The user has two contacts named 'John'. 'John Quinn' and 'John Appleseed'. I can ask them to clarify which contact they wish to send to and the contents of the message.",
            success_conditions=[
                {
                    "input_text": "1. The latest message from Emily Rose received on the 24th July 2024 at 11:30 saying 'That sounds wonderful. The more, the merrier!' is read out to the user.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. A message is sent to John Quinn with invitation to the neighbourhood gathering this Saturday. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "send_message",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent tries to look up Emily’s latest reply in the messages database
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
                # Milestone 1 – Confirm the search outcome actually contained Emily’s 24-Jul-2024 message
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
                                                "value": "emily.rose@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "That sounds wonderful. The more, the merrier!",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-24T11:30:00-07:00",
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
                # Milestone 2 – A new outgoing message to John Quinn was sent
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
                                                "theo.appleseed@example.com",
                                                "1234-5678-9101",
                                            ),
                                        ]
                                    ],
                                    "content": "gathering",
                                    "creation_datetime_iso": "2024-07-24T11:40:00-07:00",
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
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # message search → validation of Emily’s reply
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_b31fc9e1-040f-4c26-8ea5-c08ef2997292_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-28T06:00:00-07:00",
            is_read_time="2024-07-28T06:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You enjoyed yourself a bit too much at the neighborhood gathering and are now hungover.   You decide not to leave the house today. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Cancel whatever event I have today.",
                },
            ],
            reasoning="The user is asking me to cancel events.\nI should find them in the user's calendar.\nI see only one event scheduled for today, Cooking Class on July 28, 2024 at 13:00-16:00, I will go ahead and cancel the event as requested.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1) Cooking Class event on July 28, 2024 at 13:00-16:00 is deleted..",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent queries today’s calendar events
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
                # Milestone 1 – The “Cooking Class” event for July 28 2024 is found in the tool output
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
                                                "value": "Cooking Class",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-28T13:00:00-07:00",
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
                # Milestone 2 – The “Cooking Class” event is removed (cancelled)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Cooking Class",
                                    "start_datetime_iso": "2024-07-28T13:00:00-07:00",
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
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_25b25bc6-9820-4b75-850e-9c6356c3bb21_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T12:00:00-07:00",
            is_read_time="2024-07-24T12:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "Your friend John is coming to the Neighborhood gathering and wants to know what to bring as far as food and drink.   You send a message asking Emily Rose. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Attending a neighborhood gathering on Saturday the 27th at 08:00 and bringing my friend John Quinn. John wants to know what he should bring with him in regards to food or drink. Must message Emily Rose. ",
                },
            ],
            reasoning="The user is bringing his friend John Quinn to the Neighbourhood Gathering and all though she said it was okay to bring someone he wants to confirm with the host Emily Rose. User also wants to know if John can bring any specific food or drink to the gathering. \n\nWill send Emily Rose a message confirming that the users friend John Quinn will be attending. Will inquire what food or beverage John can bring to the gathering on Saturday the 27th. ",
            success_conditions=[
                {
                    "input_text": "1. You message Emily rose to confirm that your friend John Quinn is coming and can he bring any food or drink. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up Emily Rose's contact information
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
                # Milestone 1 – The contact lookup result includes Emily Rose
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
                                                "value": "Emily Rose",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "emily.rose@example.com",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,  # use output from Milestone 0
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
                # Milestone 2 – A new message is sent to Emily Rose mentioning John and asking about food/drink
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
                                                "1234-5678-9109",
                                                "emily.rose@example.com",
                                            ),
                                            (
                                                "1234-5678-9101",
                                                "theo.appleseed@example.com",
                                            ),
                                        ]
                                    ],
                                    "content": "John",  # will verify substring,
                                    "creation_datetime_iso": "2024-07-24T12:00:00-07:00",
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
            name="THEO_APPLESEED_18_a48a5462-3da6-4a6a-8694-d3259f328651_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_18",
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
            reference_time="2024-07-27T17:35:00-07:00",
            is_read_time="2024-07-27T17:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "Your friend John was considering joining the neighborhood gathering, but he decided not to, so you have to let your friend organizing it know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to Emily Rose saying 'my friend John won't make it after all.'",
                },
            ],
            reasoning="The user wants to send a message to Emily Rose. I'll check the user's contacts for a contact under this name. There is a contact under that name so I'll pull up that number. The user gave me the content of the message, which will say: 'my friend John won't make it after all. I will send this message and notify the user.",
            success_conditions=[
                {
                    "input_text": "1. A text message is sent to Emily Rose saying 'my friend John won't make it after all.'",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – the agent looks up Emily Rose in contacts
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
                # Milestone 1 – confirms Emily Rose was returned from the contact lookup in Milestone 0
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
                                                "value": "Emily Rose",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9109",
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
                # Milestone 2 – a text message was sent to Emily containing the correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require that Emily is a participant (allowing extra participants such as self)
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9109",
                                                "emily.rose@example.com",
                                            )
                                        ]
                                    ],
                                    "content": [
                                        ("John won't make it", "won't make it")
                                    ],
                                    "creation_datetime_iso": "2024-07-27T17:35:00-07:00",
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
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → confirm correct contact found
                (1, 2),  # Contact confirmed → message sent
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_78acf828-9cb8-4f3b-b47f-1df0e0769a15_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "calendar",
                "messaging",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T18:15:00-07:00",
            is_read_time="2024-07-27T18:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You are on your way to the neighbourhood gathering but you got stuck in traffic, so you want to send a text to Emily to tell her that you are on the way, "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Can you let the organizer know "I\'m on the way but caught in traffic, see you soon!"',
                },
            ],
            reasoning="The user wants me to send a text message. I need to find out who the organizer of the event is. I searched user's calendar, and the event \"Neighbourhood Gathering\", which is running from 18:00 to 21:00. The attendees contain Emily Rose, who is also the organizer. Next I need to check the user data, and I found messages between Emily Rose and Theo mentioning the neighbourhood gathering and Emily reminding Theo to come. It's likely that Emily Rose is the person that Theo wants to message.\n\nWith the user's confirmation, I will send the message \"Hey I'm on the way but caught in traffic, see you soon!\" to Emily Rose. ",
            success_conditions=[
                {
                    "input_text": '1. The message "Hey I\'m on the way but caught in traffic, see you soon!" is sent to Emily Rose. ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "get_all_messages",
                "send_message",
                "search_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent uses a read-only lookup tool (contacts or calendar) to figure out who to text
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
                # Milestone 1 – Confirm that the correct calendar event was returned in Milestone 0
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
                                                "value": "Neighborhood Gathering",
                                                "partial": False,
                                            },
                                            # original start time (optional but strengthens check)
                                            "start_datetime_iso": {
                                                "value": "2024-07-27T18:00:00-07:00",
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
                        ),
                    ],
                ),
                # Milestone 2 – A new text message is sent to Emily that contains the traffic/“on the way” note
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least Emily’s address (email or phone) must be among the participants.
                                    "participants_addresses": [
                                        [("emily.rose@example.com", "1234-5678-9109")]
                                    ],
                                    "content": "on the way",  # key phrase
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-27T18:15:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare to initial state
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
            name="THEO_APPLESEED_18_668e2282-db2d-4486-a4ba-117d9fc32c1e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T14:20:00-07:00",
            is_read_time="2024-07-27T14:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You have gotten delayed with household chores and want to let Emily Rose know that you will be an hour late this evening to the neighborhood gathering. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell Emily hi and I will be around an hour late this evening ",
                },
            ],
            reasoning="The user wants to inform an 'Emily' that they will be late this evening. To gather context, I will look through the user's calendar to see if there is an event logged for this evening. I have found an event called 'Neighborhood Gathering\" and there appears to be an 'Emily Rose' listed on the event. After searching the user's messages, I can see correspondence with Emily Rose regarding this event. Therefore, I can assume this is the intended contact. ",
            success_conditions=[
                {
                    "input_text": 'A message is sent to Emily Rose that says "Hi Emily. I will be around an hour late this evening" ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent tries to locate Emily Rose in the contacts database
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
                # Milestone 1 – Verify Emily Rose’s contact details were indeed returned from Milestone 0’s search
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
                                                "value": "Emily Rose",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "emily.rose@example.com",
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
                # Milestone 2 – A new message is sent to Emily informing her the user will be an hour late
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Only need to prove Emily’s address is among the participants
                                    "participants_addresses": [
                                        [("emily.rose@example.com", "1234-5678-9109")]
                                    ],
                                    "content": "hour late",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-27T14:20:00-07:00",
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_18_a48a5462-3da6-4a6a-8694-d3259f328651_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_18",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "contact",
                "calendar",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T17:35:00-07:00",
            is_read_time="2024-07-27T17:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "Your friend John was considering joining the neighborhood gathering, but he decided not to, so you have to let your friend organizing it know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text the host of the Neighborhood Gathering and say \"my friend John won't make it after all.'\"",
                },
            ],
            reasoning='The user wants to send a message to the host of an event called Neighborhood Gathering. I see that event is scheduled for 27 July at 18:00-21:00, but I only see Theo on the invitee list. However, the description of the event says "A friendly neighborhood gathering hosted by Emily Rose to engage with neighbors and participate in community activities." Based on this description of the event, the host is Emily Rose, so I will text her "my friend John won\'t make it after all" like the user wants.',
            success_conditions=[
                {
                    "input_text": "1. A text message is sent to Emily Rose saying 'my friend John won't make it after all.'",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the host (Emily Rose) in contacts
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
                # Milestone 1 – Confirm that the retrieved contact is Emily Rose (the gathering host)
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
                                                "value": "Emily Rose",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9109",
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
                # Milestone 2 – A text message is sent to Emily Rose with the specified content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Must include Emily’s phone; agent (Theo) may also appear, so subset match
                                    "participants_addresses": [
                                        [("emily.rose@example.com", "1234-5678-9109")]
                                    ],
                                    "content": "my friend John won't make it after all",
                                    "creation_datetime_iso": "2024-07-27T17:35:00-07:00",
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
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
    ]
