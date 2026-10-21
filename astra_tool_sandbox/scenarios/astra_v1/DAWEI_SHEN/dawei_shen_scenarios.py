# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Scenarios where more than 1 tool call to be issued to complete the task"""

import json
from functools import partial
from typing import Any, Dict, List, Optional, Union, cast

import polars as pl
import yaml

from astra_tool_sandbox.common.constants import PACKAGE_DIR
from astra_tool_sandbox.common.evaluation import (
    Milestone,
    SnapshotConstraint,
    addition_similarity,
    column_contains_similarity,
    column_exact_match_similarity,
    column_list_exact_match_similarity,
    column_list_subset_match_similarity,
    column_list_tuple_contains_similarity,
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_tool_trace_partial_arguments_similarity,
    column_word_contains_any_similarity,
    snapshot_similarity,
    tool_trace_dependant_similarity,
)
from astra_tool_sandbox.common.execution_context import (
    DatabaseNamespace,
    RoleType,
    ScenarioCategories,
)
from astra_tool_sandbox.common.scenario import Scenario, ScenarioExtension
from astra_tool_sandbox.common.tool_discovery import ToolBackend
from astra_tool_sandbox.common.tool_trace_extractors import (
    ToolTraceExtractorType,
    result_list_match_count_extractor,
    result_list_match_existence_extractor,
    result_to_birthday_text_extractor,
)
from astra_tool_sandbox.scenarios.astra_v1.base_scenarios import named_base_scenarios
from astra_tool_sandbox.scenarios.astra_v1.DAWEI_SHEN.converted_TAG_scenarios import (
    annotated_base_scenarios,
)
from astra_tool_sandbox.scenarios.astra_v1.protagonist_simulator_few_shot_examples import (
    USER_INSTRUCTION_SINGLE_TURN,
)
from astra_tool_sandbox.scenarios.astra_v1.protagonists import ProtagonistName


def load_bio() -> Dict[str, Any]:
    bio_path = PACKAGE_DIR / "scenarios" / "astra_v1" / "DAWEI_SHEN" / "bio.yaml"
    with open(bio_path) as f:
        return cast(Dict[str, Any], yaml.safe_load(f))


protagonist_bio = load_bio()


def get_extensions(
    base_scenarios: dict[str, Scenario],
    protagonist_name: str = "DAWEI_SHEN",
    llm_evaluation: Optional[bool] = False,
) -> list[ScenarioExtension]:
    """Specify test scenario as extensions over a base scenario

    Returns:
        A list of ScenarioExtensions
    """
    # user_simulator_few_shot_examples = named_user_simulator_few_shot_examples()

    return [
        ScenarioExtension(
            name=f"get_make_phonecall_phonenumber_{protagonist_name}",
            base_scenario=base_scenarios["base"],
            tags=[protagonist_name, "phonecall", "test"],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07 08:05:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + f"Ask User B to call '+1 555-890-1234-5678'. You are User A, {protagonist_bio['name']}"
                    "You do not have any more information.",
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "call '+1 555-890-1234-5678'.",
                },
            ],
            reasoning=(
                "The user wants me to place an outgoing call to '+1 555-890-1234-5678'. "
                "I will call create_outgoing_call with receiver_address='+1 555-890-1234-5678' "
                "to initiate the call, then confirm to the user that the call has been placed."
            ),
            success_conditions=[
                {
                    "input_text": "1. An outgoing call is placed to '+1 555-890-1234-5678'.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["create_outgoing_call"],
            milestones=[
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.PHONE,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "caller_address": "+1 555-123-4567-8901",
                                    "receiver_address": "+1 555-890-1234-5678",
                                },
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name=f"get_send_message_by_phonenumber_{protagonist_name}",
            base_scenario=base_scenarios["base"],
            tags=[protagonist_name, "message", "test"],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07 08:05:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + f"Ask User B to send a message to '+1 555-890-1234-5678' saying thank you. You are User A, {protagonist_bio['name']}"
                    "You do not have any more information.",
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to '+1555-890-1234-5678', with content: 'Thank you'.",
                },
            ],
            reasoning=(
                "The user wants me to send a text message to '+1555-890-1234-5678' with the content "
                "'Thank you'. I will call send_message with recipient_address='+1555-890-1234-5678' "
                "and content='Thank you', then confirm to the user that the message has been sent."
            ),
            success_conditions=[
                {
                    "input_text": "1. A message with content 'Thank you' is sent to '+1555-890-1234-5678'.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["send_message"],
            milestones=[
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [
                                            "+155589012345678",
                                        ]
                                    ],
                                    "content": "Thank you",
                                    "sender_address": "+155512345678901",
                                },
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_subset_match_similarity
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name=f"get_send_message_by_name_{protagonist_name}",
            base_scenario=base_scenarios["base"],
            tags=[protagonist_name, "message", "test"],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07 08:05:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + f"Ask User B to send a message to Kevin Chen saying thank you. You are User A, {protagonist_bio['name']}"
                    "You do not have any more information.",
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to Kevin Chen, +1 555-890-1234-5678, with content: 'Thank you'.",
                },
            ],
            reasoning=(
                "The user wants me to send a message to Kevin Chen at +1 555-890-1234-5678 with the "
                "content 'Thank you'. The recipient's phone number is provided directly in the request, "
                "so I will call send_message with recipient_address='+1 555-890-1234-5678' and "
                "content='Thank you', then confirm to the user that the message has been sent."
            ),
            success_conditions=[
                {
                    "input_text": "1. A message with content 'Thank you' is sent to Kevin Chen at +1 555-890-1234-5678 (kevin.chen@orchardtech.com).",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["send_message"],
            milestones=[
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
                                                "+1 555-890-1234-5678",
                                                "kevin.chen@orchardtech.com",
                                            ),
                                            (
                                                "+1 555-123-4567-8901",
                                                "dawei.shen@orchardtech.com",
                                            ),
                                        ]
                                    ],
                                    "content": "Thank you",
                                },
                            ),
                            reference_milestone_node_index=-1,
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity
                            },
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name=f"get_send_messages_separately_{protagonist_name}",
            base_scenario=base_scenarios["base"],
            tags=[protagonist_name, "message", "test"],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07 08:05:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + f"Ask User B to send a message to Kevin Chen saying thank you. You are User A, {protagonist_bio['name']}"
                    "You do not have any more information.",
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to +1 555-890-1234-5678 and +1 555-345-6789-0123 separately with content: 'Thank you'.",
                },
            ],
            reasoning=(
                "The user wants me to send the message 'Thank you' separately to two recipients: "
                "+1 555-890-1234-5678 and +1 555-345-6789-0123. I must send two separate messages, "
                "not a group message. I will call send_message twice — once for each number — "
                "then confirm to the user that both messages have been sent."
            ),
            success_conditions=[
                {
                    "input_text": "1. A message with content 'Thank you' is sent separately to +1 555-890-1234-5678 (Kevin Chen / kevin.chen@orchardtech.com).",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. A message with content 'Thank you' is sent separately to +1 555-345-6789-0123 (Vickie Lee / vickie.lee@orchardtheater.com).",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["send_message"],
            milestones=[
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
                                                "+1 555-890-1234-5678",
                                                "kevin.chen@orchardtech.com",
                                            ),
                                        ],
                                        [
                                            (
                                                "+1 555-345-6789-0123",
                                                "vickie.lee@orchardtheater.com",
                                            ),
                                        ],
                                    ],
                                    "content": ["Thank you", "Thank you"],
                                },
                            ),
                            reference_milestone_node_index=-1,
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity
                            },
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name=f"get_send_message_by_name_subset_{protagonist_name}",
            base_scenario=base_scenarios["base"],
            tags=[protagonist_name, "message", "test"],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07 08:05:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + f"Ask User B to send a message to Kevin Chen saying thank you. You are User A, {protagonist_bio['name']}"
                    "You do not have any more information.",
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to Kevin Chen, +1 555-890-1234-5678, with content: 'Thank you'.",
                },
            ],
            reasoning=(
                "The user wants me to send a message to Kevin Chen at +1 555-890-1234-5678 with the "
                "content 'Thank you'. The recipient's phone number is provided directly. I will call "
                "send_message with recipient_address='+1 555-890-1234-5678' and content='Thank you', "
                "then confirm to the user that the message has been sent."
            ),
            success_conditions=[
                {
                    "input_text": "1. A message with content 'Thank you' is sent to Kevin Chen at +1 555-890-1234-5678 (kevin.chen@orchardtech.com).",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["send_message"],
            milestones=[
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
                                                "+1 555-890-1234-5678",
                                                "kevin.chen@orchardtech.com",
                                            ),
                                        ]
                                    ],
                                    "content": "Thank you",
                                },
                            ),
                            reference_milestone_node_index=-1,
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity
                            },
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name=f"get_add_calendar_{protagonist_name}",
            base_scenario=base_scenarios["base"],
            tags=[protagonist_name, "calendar", "test"],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07 08:05:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + f"Ask User B to schedule a coffee chat with Theo. You are User A, {protagonist_bio['name']}"
                    "You do not have any more information.",
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Schedule a coffeechat with Theo Appleseed at 10am today, with title 'Coffeechat with Theo'.",
                },
            ],
            reasoning=(
                "The user wants me to schedule a coffee chat with Theo Appleseed at 10am today "
                "(2024-12-07T10:00:00). I may need to look up Theo Appleseed's contact details via "
                "get_all_contacts or search_contacts, then call create_calendar_event with "
                "calendar_event_name='Coffeechat with Theo', start_datetime_iso='2024-12-07T10:00:00', "
                "and attendees including Theo Appleseed and Dawei Shen."
            ),
            success_conditions=[
                {
                    "input_text": "1. A calendar event titled 'Coffeechat with Theo' is created at 2024-12-07T10:00:00 with attendees Theo Appleseed and Dawei Shen.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "create_calendar_event",
                "search_contacts",
            ],
            milestones=[
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Coffeechat with Theo",
                                    "start_datetime_iso": "2024-12-07T10:00:00",
                                    "attendees_names": [
                                        ["Theo Appleseed", "Dawei Shen"]
                                    ],
                                },
                            ),
                            reference_milestone_node_index=-1,
                            column_similarity_measure={
                                "attendees_names": column_list_exact_match_similarity,
                            },
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name=f"get_contact_count_{protagonist_name}",
            base_scenario=base_scenarios["base"],
            tags=[protagonist_name, "contact", "test"],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07 08:05:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + f"Ask User B to find the total number of contacts of your (User A's). You are User A, {protagonist_bio['name']}"
                    "You do not have any more information.",
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How many contacts do I have in total?",
                },
            ],
            reasoning=(
                "The user wants to know the total number of contacts in their address book. "
                "I will call get_all_contacts to retrieve the full contact list, then count the entries "
                "and report the total back to the user. The address book contains 17 contacts, "
                "so the answer is 17."
            ),
            success_conditions=[
                {
                    "input_text": "1. The assistant retrieves the full contact list and tells the user the total number of contacts is 17.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=["get_all_contacts"],
            milestones=[
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": json.dumps(
                                        {
                                            "tool_name": "get_all_contacts",
                                            "arguments": {},
                                        },
                                        ensure_ascii=False,
                                    ),
                                }
                            ),
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
                                        result_list_match_count_extractor,
                                        count_expected=17,
                                        match_conditions=None,
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
                            reference_milestone_node_index=0,  # or wherever the tool call happens
                        )
                    ]
                ),
                # The agent must report the count to the user (numeral or word).
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("17", "seventeen")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity,
                            },
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
            ],
        ),
        ScenarioExtension(
            name=f"get_contact_birthday_{protagonist_name}",
            base_scenario=base_scenarios["base"],
            llm_evaluation=llm_evaluation,
            tags=[protagonist_name, "contact"],
            reference_time="2024-12-07 23:07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + f"Ask User B to find the names of contacts of your (User A's) who are born this month. You are User A, {protagonist_bio['name']}."
                    "You do not have any more information. Ask the user B to retrieve all contacts and then get birthday information.",
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you find which of my contacts have a birthday this month?",
                    # "content": "Find which of my contacts have a birthday this month.",
                    # "content": "Can you retrieve all of my contacts first with correct tool? Also find which of my contacts have a birthday this month.",
                },
            ],
            reasoning=(
                "The user wants to know which contacts have a birthday in the current month (December). "
                "I will call get_all_contacts or search_contacts to retrieve the contact list, then filter "
                "for contacts whose birthday falls in December. Based on the contact data, Theo and Lukas "
                "both have birthdays this month, so I will report both names to the user."
            ),
            success_conditions=[
                {
                    "input_text": "1. The assistant retrieves contacts and identifies that Theo has a birthday this month (December).",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The assistant also identifies that Lukas has a birthday this month (December).",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=["search_contacts", "get_all_contacts"],
            milestones=[
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
                                        "search_contacts",
                                        "get_all_contacts",
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
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Theo",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                            reference_milestone_node_index=0,
                        ),
                    ],
                ),
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Lukas",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                            reference_milestone_node_index=0,
                        ),
                    ]
                ),
            ],
        ),
        ScenarioExtension(
            name=f"get_calendar_involve_vick_{protagonist_name}",
            base_scenario=base_scenarios["base"],
            tags=[protagonist_name, "calendar"],
            llm_evaluation=llm_evaluation,
            reference_time="2024-11-30 23:59:00",
            is_read_time="2024-11-30 23:59:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + f"Ask User B to find how many scheduled calendar events involving Vick Li of your (User A's) calendar. You are User A, {protagonist_bio['name']}"
                    "You do not have any more information.",
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Get all my scheduled calendar events involve Vick",
                },
            ],
            reasoning=(
                "The user wants to find all scheduled calendar events that involve Vick. "
                "I will call get_all_calendars or search_calendar_events to look up upcoming events, "
                "then filter for events involving Vick. The calendar contains an event called "
                "'Cycling Trip with Vick', so I will report that event to the user."
            ),
            success_conditions=[
                {
                    "input_text": "1. The assistant searches the calendar and reports the event 'Cycling Trip with Vick' as a scheduled event involving Vick.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
            ],
            milestones=[
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
                                        "search_calendar_events",
                                        "get_all_calendars",
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
                                            "calendar_event_name": {
                                                "value": "Cycling Trip with Vick",
                                                "partial": True,
                                            }
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
                            reference_milestone_node_index=0,  # or wherever the tool call happens
                        )
                    ]
                ),
            ],
        ),
        ScenarioExtension(
            name=f"get_unread_emails_michelle_{protagonist_name}",
            base_scenario=base_scenarios["base"],
            tags=[protagonist_name, "email", "test"],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13 23:59:00",
            is_read_time="2024-12-13 10:13:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + f"Ask User B to find latest unread message from Michelle of your (User A's) calendar. You are User A, {protagonist_bio['name']}"
                    "You do not have any more information.",
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Do I have any unread emails from Michelle? How many in total?",
                },
            ],
            reasoning=(
                "The user wants to know if they have any unread emails from Michelle and how many. "
                "I will call search_emails or get_all_emails to look up emails, filtering for unread "
                "messages from michelle.barnes@orchardtech.com. There is one unread email from Michelle, "
                "so I will tell the user they have one unread email from Michelle."
            ),
            success_conditions=[
                {
                    "input_text": "1. The assistant searches the inbox and reports that there is one unread email from Michelle (michelle.barnes@orchardtech.com).",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
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
                                            "status": {
                                                "value": "unread",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "michelle.barnes@orchardtech.com",
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
                            reference_milestone_node_index=0,  # or wherever the tool call happens
                        )
                    ]
                ),
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("1 unread", "one unread")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                    ]
                ),
            ],
        ),
        ScenarioExtension(
            name=f"reply_emails_michelle_{protagonist_name}",
            base_scenario=base_scenarios["base"],
            tags=[protagonist_name, "email", "test"],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T09:20:00-08:00",
            is_read_time="2024-12-02T09:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + f"Ask User B to find latest unread message from Michelle of your (User A's) calendar. You are User A, {protagonist_bio['name']}"
                    "You do not have any more information.",
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply Michelle's email with subject Revised Draft for Virtual Assistant Algorithm, saying thanks for sharing it",
                },
            ],
            reasoning=(
                "The user wants me to reply to an email from Michelle with the subject 'Revised Draft for "
                "Virtual Assistant Algorithm'. I will first search the inbox using search_emails or "
                "get_all_emails to locate the email from michelle.barnes@orchardtech.com with that subject. "
                "Once I find the email, I will call send_email with email_action='send', "
                "email_id_referred set to the found email's ID, email_id_referred_action='reply', "
                "and body content expressing thanks for sharing it."
            ),
            success_conditions=[
                {
                    "input_text": "1. The email from michelle.barnes@orchardtech.com with subject 'Revised Draft for Virtual Assistant Algorithm' is found in the inbox.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. A reply email is sent to michelle.barnes@orchardtech.com with a subject containing 'RE' and status 'sent'.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_emails",
                "get_all_emails",
                "send_email",
            ],
            milestones=[
                # 0: search for the email
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
                        ),
                    ]
                ),
                # 1: found the target email
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
                                                "value": "Revised Draft for Virtual Assistant Algorithm",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "michelle.barnes@orchardtech.com",
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
                            reference_milestone_node_index=0,  # or wherever the tool call happens
                        )
                    ]
                ),
                # 2: reply to the email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "tool_trace": json.dumps(
                                        {
                                            "tool_name": "send_email",
                                            "arguments": {
                                                "email_action": "send",
                                                "email_id_referred": "place_holder",  # must send email with a thread id to reply an email
                                                "email_id_referred_action": "reply",
                                            },
                                        },
                                        ensure_ascii=False,
                                    )
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": column_tool_trace_partial_arguments_similarity
                            },
                        ),
                    ]
                ),
                # 3: reply to the email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        [
                                            "michelle.barnes@orchardtech.com",
                                        ]
                                    ],
                                    "subject": "RE",
                                    "status": "sent",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "subject": column_contains_similarity,
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name=f"forward_emails_michelle_{protagonist_name}",
            base_scenario=base_scenarios["base"],
            tags=[protagonist_name, "email", "test"],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13 23:59:00",
            is_read_time="2024-12-13 23:59:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + f"Ask User B to find latest unread message from Michelle of your (User A's) calendar. You are User A, {protagonist_bio['name']}"
                    "You do not have any more information.",
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Forward the email from Michelle with subject Revised Draft for Virtual Assistant Algorithm to stefan.mustermann@orchardtech.com and kevin.chen@orchardtech.com",
                },
            ],
            reasoning=(
                "The user wants me to forward Michelle's email with subject 'Revised Draft for Virtual "
                "Assistant Algorithm' to stefan.mustermann@orchardtech.com and kevin.chen@orchardtech.com. "
                "I will first search the inbox using search_emails or get_all_emails to find the email from "
                "michelle.barnes@orchardtech.com with that subject. Then I will call send_email with "
                "email_action='send', email_id_referred set to the found email's ID, "
                "email_id_referred_action='forward', and recipients_addresses set to both "
                "stefan.mustermann@orchardtech.com and kevin.chen@orchardtech.com."
            ),
            success_conditions=[
                {
                    "input_text": "1. The email from michelle.barnes@orchardtech.com with subject 'Revised Draft for Virtual Assistant Algorithm' is found in the inbox.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The email is forwarded to both stefan.mustermann@orchardtech.com and kevin.chen@orchardtech.com with a subject containing 'Fwd' and status 'sent'.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_emails",
                "get_all_emails",
                "send_email",
            ],
            milestones=[
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
                                                "value": "Revised Draft for Virtual Assistant Algorithm",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "michelle.barnes@orchardtech.com",
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
                            reference_milestone_node_index=0,  # or wherever the tool call happens
                        )
                    ]
                ),
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "tool_trace": json.dumps(
                                        {
                                            "tool_name": "send_email",
                                            "arguments": {
                                                "email_action": "send",
                                                "email_id_referred": "place_holder",  # must send email with a thread id to reply an email
                                                "email_id_referred_action": "forward",
                                            },
                                        },
                                        ensure_ascii=False,
                                    )
                                }
                            ),
                            column_similarity_measure={
                                "tool_trace": column_tool_trace_partial_arguments_similarity
                            },
                        ),
                    ]
                ),
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        [
                                            "stefan.mustermann@orchardtech.com",
                                            "kevin.chen@orchardtech.com",
                                        ]
                                    ],
                                    "subject": "Fwd",
                                    "status": "sent",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "subject": column_contains_similarity,
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        ),
                    ]
                ),
            ],
            # 2 and 3 are both satisfied by the send_email snapshot. Chaining them after 1
            # would guardrail the EMAIL database that the very same snapshot writes to.
            milestone_edge_list=[(0, 1), (2, 3)],
        ),
        ScenarioExtension(
            name=f"get_girlfried_birthday_{protagonist_name}",
            base_scenario=base_scenarios["base"],
            tags=[protagonist_name, "contact"],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13 23:59:00",
            is_read_time="2024-12-13 10:13:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + f"Ask User B to find girlfriend birthday (User A's). You are User A, {protagonist_bio['name']}"
                    "You do not have any more information.",
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is my girlfriend birthday?",
                },
            ],
            reasoning=(
                "The user wants to know their girlfriend's birthday. I will call search_contacts to look up "
                "contacts and identify who the user's girlfriend is. The girlfriend's name is Jess Zimmer. "
                "I will then retrieve Jess Zimmer's birthday from the contact record. "
                "Jess Zimmer's birthday is February 14, so I will report that date to the user."
            ),
            success_conditions=[
                {
                    "input_text": "1. The assistant identifies Jess Zimmer as the user's girlfriend by searching contacts.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The assistant reports that Jess Zimmer's birthday is February 14.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=["search_contacts"],
            milestones=[
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
                                        "search_contacts",
                                        "get_all_contacts",
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
                                            "full_name": {
                                                "value": "Jess Zimmer",
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
                            # Use column_one_similarity to return a similarity score of 1
                            # if the extractor finds a match and a filled target row is generated.
                            # This makes the SnapshotConstraint act like a logic gate: it passes
                            # if the reference tool_trace contains the expected value (e.g., a contact
                            # with full_name == "Jess Zimmer"). The actual snapshot content is ignored.
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
                Milestone(
                    snapshot_constraints=[
                        # Fuzzy partial match version
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    result_to_birthday_text_extractor,
                                ),
                            ),
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "{birthday}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                            reference_milestone_node_index=1,
                        ),
                    ]
                ),
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
                                            "February 14",
                                            "Feb 14",
                                            "14 February",
                                            "14 Feb",
                                            "14th of February",
                                            "02/14",
                                            "2/14",
                                            "1994-02-14",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        )
                    ]
                ),
            ],
        ),
        ScenarioExtension(
            name=f"get_rehearsal_time_{protagonist_name}",
            base_scenario=base_scenarios["base"],
            tags=[protagonist_name, "contact"],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T19:56:00",
            is_read_time="2024-12-01T19:55:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + f"Ask User B to find when will Vickie arrive for the rehearsal tonight. You are User A, {protagonist_bio['name']}"
                    "You do not have any more information.",
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "It's nearly 8pm, when Vickie will join us at the rehearsal tonight?",
                },
            ],
            reasoning=(
                "The user wants to know when Vickie will arrive at tonight's rehearsal. "
                "I will call search_whatsapp_messages to look for a recent message from Vickie Lee "
                "about the rehearsal. Vickie Lee sent a WhatsApp message saying: "
                "'Hey Dawei, I might be around 20 mins late, sorry! Caught up with something.' "
                "I will relay this to the user: Vickie will be about 20 minutes late to the rehearsal."
            ),
            success_conditions=[
                {
                    "input_text": "1. The assistant searches WhatsApp messages and finds Vickie Lee's message indicating she will be late.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The assistant tells the user that Vickie will be approximately 20 minutes late to the rehearsal.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "search_messages",
                "search_whatsapp_messages",
                "search_calendar_events",
            ],
            milestones=[
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
                                    target_tools=["search_whatsapp_messages"],
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
                                        result_list_match_count_extractor,
                                        count_expected=1,
                                        match_conditions={
                                            "conversation_name": {
                                                "value": "Vickie Lee",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Hey Dawei, I might be around 20 mins late, sorry! Caught up with something.",
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
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "20",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        )
                    ]
                ),
            ],
        ),
    ]


def named_dawei_shen_scenarios(
    preferred_tool_backend: ToolBackend,
    llm_evaluation: Optional[bool] = False,
    desired_scenario_names: Optional[list[str]] = None,
    scenario_tags: Optional[list[str]] = None,
    add_user_simulator_few_shot_examples: bool = False,
    scenario_meta_info_only: bool = False,
) -> Union[Dict[str, Scenario], Dict[str, Dict[str, Union[str, List[str]]]]]:
    """Scenarios where more than 1 tool call to be issued to complete the task

    Note that this differs from the simple / multi definition of Gorilla. All scenarios below have only the necessary
    tools provided to the model. Additional scenarios will be created to introduce distractions as well.

    Args:
        preferred_tool_backend: Which backend should be chosen in face of conflicting tool names.
        llm_evaluation:         Whether to use LLM to judge scenarios
        desired_scenario_names: Name of scenarios to run. If empty all scenarios will be
                                returned.
        scenario_tags:          Scenarios with the given list of tags to run. Need to cover all tags mentioned here.
        add_user_simulator_few_shot_examples: Whether to add user simulator few-shot examples to scenarios.
    Returns:
        A dict containing scenario name and scenario
    """
    # preferred_tool_backend = ToolBackend.DEFAULT
    base_scenarios = named_base_scenarios(
        protagonist_name=cast(ProtagonistName, "DAWEI_SHEN"),
        preferred_tool_backend=preferred_tool_backend,
        single_turn_user_simulator=True,
        add_user_simulator_few_shot_examples=add_user_simulator_few_shot_examples,
    )
    extensions = get_extensions(
        base_scenarios=base_scenarios,
        llm_evaluation=llm_evaluation,
    )
    # extended with TAG scenarios
    extensions.extend(
        annotated_base_scenarios(
            base_scenarios,
            llm_evaluation=llm_evaluation,
        )
    )
    # All scenarios in this module should be single user turn, multiple tool. Add these categories if they aren't there
    for extension in extensions:
        for default_categories in [
            ScenarioCategories.MULTIPLE_TOOL_CALL,
            ScenarioCategories.SINGLE_USER_TURN,
        ]:
            if default_categories not in extension.categories:
                extension.categories.append(default_categories)

    ## NOTE: For debugging purposes
    # loaded_scenarios = {}
    # try:
    #     for extension in extensions:
    #         extension_scenarios = extension.get_extended_scenario()
    #         for key, scenario in extension_scenarios.items():
    #             loaded_scenarios.update({key: scenario})
    # except IndexError as e:
    #     print(f"Error occurred while processing extension: {extension}")
    #     print(f"Last processed key: {key if 'key' in locals() else 'N/A'}")
    #     raise

    """ return loaded_scenarios with selected ones only and full clipped dataset """
    if desired_scenario_names or scenario_tags:
        # if scenarios selected criteria provided, only load the mentioned ones
        if not scenario_meta_info_only:
            return {
                key: extension.get_extended_scenario()[key]
                for extension in extensions
                for key, scenario in extension.get_extended_scenario_meta().items()
                if (desired_scenario_names and (key in desired_scenario_names))
                or (scenario_tags and (set(scenario["tags"]).issuperset(scenario_tags)))
            }
        else:
            return {
                key: scenario
                for extension in extensions
                for key, scenario in extension.get_extended_scenario_meta().items()
                if (desired_scenario_names and (key in desired_scenario_names))
                or (scenario_tags and (set(scenario["tags"]).issuperset(scenario_tags)))
            }
    else:
        # return all scenarios
        if not scenario_meta_info_only:
            return {
                key: scenario
                for extension in extensions
                for key, scenario in extension.get_extended_scenario().items()
            }
        else:
            return {
                key: scenario
                for extension in extensions
                for key, scenario in extension.get_extended_scenario_meta().items()
            }
