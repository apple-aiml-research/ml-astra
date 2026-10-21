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
    column_list_subset_match_similarity,
    column_list_tuple_contains_similarity,
    column_one_similarity,
    column_rouge_l_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_any_similarity,
    snapshot_similarity,
    tool_trace_dependant_similarity,
    update_similarity,
)
from astra_tool_sandbox.common.execution_context import DatabaseNamespace, RoleType
from astra_tool_sandbox.common.scenario import Scenario, ScenarioExtension
from astra_tool_sandbox.common.tool_trace_extractors import (
    ToolTraceExtractorType,
    result_list_match_count_extractor,
    result_list_match_existence_extractor,
)
from astra_tool_sandbox.scenarios.astra_v1.protagonist_simulator_few_shot_examples import (
    USER_INSTRUCTION_SINGLE_TURN,
)


def get_TAG_DAWEI_SHEN_pilot_plot_2(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="DAWEI_SHEN_2_921e213e-10fd-4e54-ac83-8363fbd402e9_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T20:00:00-08:00",
            is_read_time="2024-12-01T20:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to let Vickie know that it's ok that she is running late and that you will wait for her arrival to start any group scenes. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to Vickie on WhatsApp saying that's ok and that we will wait for her to start any group scenes. ",
                },
            ],
            reasoning='The user wants to reply to Vickie on WhatsApp. I first look up the contact named Vickie and find one match: Vickie Lee (+1 555-345-6789-0123). I then send her a WhatsApp message that reads, "That\'s ok. We will wait for you to start any group scenes."',
            success_conditions=[
                {
                    "input_text": 'A WhatsApp message is sent to Vickie Lee saying "That\'s ok. We will wait for you to start any group scenes."',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_whatsapp_message",
            ],
            milestones=[
                # Milestone 0: Agent retrieves Vickie's contact
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
                    ]
                ),
                # Milestone 1: Confirm Vickie's contact retrieved
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
                                                "value": "Vickie Lee",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "+1 555-345-6789-0123",
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
                        ),
                    ]
                ),
                # Milestone 2: Send WhatsApp message to Vickie
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Vickie Lee",
                                    "content": "That's ok. We will wait for you to start any group scenes.",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-01T20:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_74968837-b5d4-4c6a-9f53-6ce04a855056_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "email",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T12:40:00-08:00",
            is_read_time="2024-12-02T12:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to view the rehearsal schedule email that Francis sent you last night. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read me the update about practice last night?",
                },
            ],
            reasoning='The user wants to view the "new timetable email".\n\nOkay, first of all I have to go to the user\'s Mail and see if they have any emails that correspond to this description.\n\nRight, so there aren\'t emails that include the term "new timetable", but I have found one email from Francis Wagner about an "Updated Rehearsal Schedule". I surmise that this is the email the user is referring to, given that it refers to a schedule.\n\nI will now open this email for the user to view.\n',
            success_conditions=[
                {
                    "input_text": '1. The user is presented with the email received from Francis Wagner with the subject "Updated Rehearsal Schedule".',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0: Verify that the agent searched or retrieved emails
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
                    ]
                ),
                # Milestone 1: Verify that the correct email with subject "Updated Rehearsal Schedule" from Francis Wagner was found
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
                                                "value": "Updated Rehearsal Schedule",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "francis.wagner@orchardtheater.com",
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
                # Milestone 2: Verify that the agent presented the answer email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "updated schedule",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_834414dc-1782-4cf2-a7ac-67d36993f597_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T20:20:00-08:00",
            is_read_time="2024-12-02T20:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know when your next monthly team meeting is to prepare. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How far away is the next team meeting in days?",
                },
            ],
            reasoning="Okay so, the user wants to check how long until their next team meeting. I can see one event matching that description, the event 'Team Review Meeting' scheduled for 13th December at 10:00. This must be the event that the user is searching for. I will let the user  know it's 11 days away .",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The event 'Team Review Meeting' scheduled for 13th December at 10:00 is found.",
                },
                {
                    "statefullness": "Stateless",
                    "input_text": "2. User has been informed that there's 11 days away.",
                },
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0: Check that agent calls get_all_calendars or search_calendar_events to find the meeting
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
                                        "get_all_calendars",
                                        "search_calendar_events",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1: Check that extracted event includes correct event
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
                                                "value": "Team Review Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-13T10:00:00-08:00",
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
                            reference_milestone_node_index=0,
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                        )
                    ]
                ),
                # Milestone 2: Agent informs user appropriately about date and time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("11", "eleven")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_dd75c71b-90ed-4813-9702-fd4d6608b052_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "contact",
                "email",
                "whatsapp_messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T21:00:00-08:00",
            is_read_time="2024-12-01T21:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to send a follow up email to Charles Wilde, Vickie Lee and Francis Wagner giving feedback on the rehearsal and booking in the next rehearsal date for the same time the following week."
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send an email to Charles, Vickie and Francis about the rehearsal and set up a calendar event for Theatre Rehearsal at 8pm next week and let them know.",
                },
            ],
            reasoning="The user wants to (1) send a follow-up email to Charles Wilde, Vickie Lee and Francis Wagner giving feedback on tonight’s rehearsal and confirming the next rehearsal at the same time next week, and (2) create a calendar event called “Theatre Rehearsal” for 08-December-2024 at 20:00 with all four participants (Dawei, Charles, Vickie, Francis) invited.",
            success_conditions=[
                {
                    "input_text": "An email is sent to Charles Wilde, Vickie Lee and Francis Wagner about tonight’s rehearsal and confirming the next rehearsal at the same time next week.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "A calendar event called 'Theatre Rehearsal' is created for 8-December-2024 at 20:00 inviting Dawei Shen, Charles Wilde, Vickie Lee and Francis Wagner.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_email",
                "create_calendar_event",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0: Check if search contacts initiated (rehearsal was not marked in calendar)
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
                # Milestone 1: Found related person's email
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
                                                "value": "Vickie Lee",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "vickie.lee@orchardtheater.com",
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
                # Milestone 2: Check if search contacts initiated (rehearsal was not marked in calendar)
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
                # Milestone 3: Found related person's email
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
                                                "value": "Charles Wilde",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "charles.wilde@orchardtheater.com",
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
                    ]
                ),
                # Milestone 4: Check if search contacts initiated (rehearsal was not marked in calendar)
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
                # Milestone 5: Found related person's email
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
                                                "value": "Francis Wagner",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "francis.wagner@orchardtheater.com",
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
                        ),
                    ]
                ),
                # Milestone 6: Verify email sent with correct body and recipients
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        [
                                            "charles.wilde@orchardtheater.com",
                                            "vickie.lee@orchardtheater.com",
                                            "francis.wagner@orchardtheater.com",
                                        ]
                                    ],
                                    # "body": "Well done tonight guys, great effort all. We will progress with the next scene next week at the same time?",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-01T21:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                # "body": column_rouge_l_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
                # Milestone 7: Verify calendar event creation
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Theatre Rehearsal",
                                    "start_datetime_iso": "2024-12-08T20:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "Dawei Shen",
                                            "Charles Wilde",
                                            "Vickie Lee",
                                            "Francis Wagner",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-01T21:00:00-08:00",
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
                    guardrail_database_exclusion_list=[DatabaseNamespace.EMAIL],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # find Vickie
                (2, 3),  # find Charles
                (4, 5),  # find Fracis
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_dd75c71b-90ed-4813-9702-fd4d6608b052_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "contact",
                "email",
                "whatsapp_messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T21:00:00-08:00",
            is_read_time="2024-12-01T21:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to send a follow up email to Charles Wilde,  Vickie Lee and Francis Wagner giving feedback on the rehearsal and booking in the next rehearsal date for the same time the following week."
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send an email to the rehearsal participants today and set up a calendar event for Theatre Rehearsal same time next week.",
                },
            ],
            reasoning="The user wants to send a follow-up email to Charles Wilde, Vickie Lee, and Francis Wagner with feedback on tonight’s rehearsal and confirmation of the next rehearsal. After sending that email, I will create a calendar event titled “Theatre Rehearsal” for 8-December-2024 at 20:00, inviting Dawei Shen, Charles Wilde, Vickie Lee, and Francis Wagner.",
            success_conditions=[
                {
                    "input_text": "An email is sent to Charles Wilde, Vickie Lee and Francis Wagner with rehearsal feedback and confirmation of the next session.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "A calendar event called 'Theatre Rehearsal' is created for 8-December-2024 at 20:00 with attendees Dawei Shen, Charles Wilde, Vickie Lee and Francis Wagner.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_email",
                "create_calendar_event",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0: Check if search emails initiated (rehearsal was not marked in calendar)
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
                    ]
                ),
                # Milestone 1: Verify Rehearsal Event Found
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
                                                "value": "Updated Rehearsal Schedule",
                                                "partial": False,
                                            },
                                            "recipients_addresses": {
                                                "value": [
                                                    "dawei.shen@orchardtech.com",
                                                    "charles.wilde@orchardtheater.com",
                                                    "vickie.lee@orchardtheater.com",
                                                ],
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "francis.wagner@orchardtheater.com",
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
                # Milestone 2: Check if search whatsapp initiated (rehearsal time mentioned in whatsapp)
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 3: Verify related messages found
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
                                                "value": "at 8",
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
                            reference_milestone_node_index=2,
                        ),
                    ]
                ),
                # Milestone 4: Verify email sent with correct body and recipients
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        [
                                            "charles.wilde@orchardtheater.com",
                                            "vickie.lee@orchardtheater.com",
                                            "francis.wagner@orchardtheater.com",
                                        ]
                                    ],
                                    # "body": "Well done tonight guys, great effort all. We will progress with the next scene next week at the same time?",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-01T21:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                # "body": column_rouge_l_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.CALENDAR],
                ),
                # Milestone 5: Verify calendar event creation
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Theatre Rehearsal",
                                    "start_datetime_iso": "2024-12-08T20:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "Dawei Shen",
                                            "Charles Wilde",
                                            "Vickie Lee",
                                            "Francis Wagner",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-01T21:00:00-08:00",
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
                    guardrail_database_exclusion_list=[DatabaseNamespace.EMAIL],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Find the email for who has attended tonight's rehearsal
                (2, 3),  # Find whatsapp for the time of rehearsal
                (1, 4),  # send the email  to the group
                (1, 5),  # making sure the right people are invited
                (3, 5),  # create correct calanedar invite
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_74968837-b5d4-4c6a-9f53-6ce04a855056_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T12:40:00-08:00",
            is_read_time="2024-12-02T12:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to view the rehearsal schedule email that Francis sent you last night. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the email related to the play practice.",
                },
            ],
            reasoning="The user wants to view the rehearsal-related email. \n\nFirst, I should search the user’s mailbox (e.g., with get_all_emails or search_emails) to list what is available. \n\nI then locate an email from Francis Wagner with the subject line “Updated Rehearsal Schedule,” which clearly matches the requested rehearsal schedule information. \n\nI will open this email and present it to the user.",
            success_conditions=[
                {
                    "input_text": '1. The user is presented with the email received from Francis Wagner with the subject "Updated Rehearsal Schedule".',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0: Validate that the agent searched for or retrieved all emails
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
                    ]
                ),
                # Milestone 1: Confirm that the email from Francis Wagner about "Updated Rehearsal Schedule" is found
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
                                                "value": "Updated Rehearsal Schedule",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "francis.wagner@orchardtheater.com",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,  # Depend on search_email/get_all_emails result
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
                # Milestone 2: Agent informs user showing the correct email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Updated Rehearsal Schedule",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_834414dc-1782-4cf2-a7ac-67d36993f597_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T20:20:00-08:00",
            is_read_time="2024-12-02T20:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know when your next monthly team meeting is to prepare. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When's my next monthly team meeting?",
                },
            ],
            reasoning="Right so, the user wants to check when is their monthly team meeting. I can see here in their calendar there is one event named 'Team Review Meeting' scheduled for next week, 13th December at 10:00. In the notes of that event, I can see it is a 'monthly team review' so it must be the event the user is requesting. I can display the date and time information for them.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The event 'Team Review Meeting' scheduled for 13th December at 10:00 is displayed to the user.",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0: Verify that the agent searched calendar events
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
                # Milestone 1: Verify that the meeting details for 'Team Review Meeting' were correctly found
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
                                                "value": "Team Review Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-13T10:00:00-08:00",
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
                # Milestone 2: Verify that the user was informed with the correct meeting date & time
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
                                            "December 13",
                                            "Dec 13",
                                            "13 December",
                                            "13th of December",
                                            "12-13",
                                            "12/13",
                                            "the 13th",
                                            "2024-12-13T10:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        ("10 am", "10am", "10 o'clock", "10:00")
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
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_ac08be22-6c0d-4b19-a0ec-f9de37cf80c4_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T14:00:00-08:00",
            is_read_time="2024-12-03T14:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You have just realized that you missed one of your theatre rehearsals.      You know that Francis shared the new schedule recently but you haven't looked at it yet.      You want to know what time this was sent to see if you have a reasonable excuse of being asleep when it arrived. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When did I get those updated practice times?",
                },
            ],
            reasoning="The user is asking what time they received something.\nFirst, I should search their messages for the keywords updated and theatre.\nI could not find any appropriate messages, I should check their email inbox next. \nI have found which may match this query as it contains the keyword updated. The email address, francis.wagner@orchardtheater.com, also contains the other keyword, theatre. I can see that this email contains the attachment Updated Rehearsal Schedule. \nI can assume that this is the email being referred to by the user. \nThis email was received at 19:58, I should report back to the user.",
            success_conditions=[
                {
                    "input_text": "1. Time of arrival for email from francis.wagner@orchardtheater.com received December 1st 2024 at 19:58 is confirmed.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0: Verify the agent used the correct tool(s) to retrieve emails
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
                        ),
                    ]
                ),
                # Milestone 1: Verify that the agent found the correct email from Francis Wagner
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
                                                "value": "francis.wagner@orchardtheater.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Updated Rehearsal Schedule",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-01T19:58:00-08:00",
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
                    ]
                ),
                # Milestone 2: Verify that the agent informs the user properly that the email was received at 19:58
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
                                        ("7:58", "19:58")
                                    ],  # allowing multiple version
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_6ce626e3-768b-4919-9525-d19dc25d32c5_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_moderate",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T20:00:00-08:00",
            is_read_time="2024-12-01T20:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to see the message from Vickie Lee and respond to it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the WhatsApp message from Vickie and respond to it saying That's fine Vickie. Thanks for letting me know.",
                },
            ],
            reasoning='The user wants to see the most recent WhatsApp message from Vickie Lee. I will use the search_whatsapp_messages tool to retrieve the latest message from Vickie (received at 19:55 on December 1 2024) and present it to the user. The user also wants to reply with: "That\'s fine Vickie. Thanks for letting me know." I will draft this reply, confirm with the user if needed, and then send it to Vickie on WhatsApp.',
            success_conditions=[
                {
                    "input_text": "1. The WhatsApp message from Vickie Lee that was received at 19:55 on December 1 2024 is presented to the user.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": '2. A message saying "That\'s fine Vickie. Thanks for letting me know" is drafted and sent to Vickie Lee on WhatsApp.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
            ],
            milestones=[
                # Milestone 0: Verify the agent used WhatsApp search or retrieval tools
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1: Verify that the WhatsApp message from Vickie Lee was retrieved
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
                                                "value": "Vickie Lee",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-01T19:55:00-08:00",
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
                # Milestone 2: Verify that the message sent to Vickie Lee contains the correct text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "Vickie Lee",
                                    "content": "That's fine Vickie. Thanks for letting me know",
                                    "creation_datetime_iso": "2024-12-01T20:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_af354c4c-4f0a-40c6-9145-1dc3b7426572_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "contact",
                "email",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T20:10:00-08:00",
            is_read_time="2024-12-01T20:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You cannot attend the rehearsal tonight due to a medical emergency and have to reschedule for the following day.      You send an email to Charles, Vickie and Francis confirming this and create a new calendar event for the following day 2-December-2024 and invite Charles, Vickie and Francis. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Hey, I need to email Charles, Vickie, and Francis to let them know I can't make tonight's rehearsal because of a medical emergency and that we've moved it to tomorrow at 9 pm. Also, create a new calendar event for tomorrow called 'Rescheduled Theatre Rehearsal' and invite them.",
                },
            ],
            reasoning='The user wants to create a calendar event titled "Rescheduled Theatre Rehearsal". I first ask the user for the correct date and time of this event. The user says tomorrow at 21:00 (9 pm), which is 2-12-2024 at 21:00. I will create an event with this title and correct time. The user states the event will last one hour. This should be added to the event also. The invitees are clearly stated as Charles Wilde, Vickie Lee and Francis Wagner. The event will be sent to their respective calendars.',
            success_conditions=[
                {
                    "input_text": "1. An email message saying \"I apologise for this guys but I wont be able to attend tonight's rehearsal as I'm extremely unwell, I've rescheduled the rehearsal for tomorrow. Calendar event to follow\" is sent.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. A Calendar event is created called "Rescheduled Theatre Rehearsal" for 12-02-2024 at 21:00. Charles Wilde, Vickie Lee, Francis Wagner, and Dawei Shen are the attendees.',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
                "send_email",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0: Verify that the agent searched contacts to find Vick
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
                # Milestone 1: Verify that contact search result includes Vick Li
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
                                                "value": "Vickie Lee",
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
                # Milestone 2-3: Verify that contact search result includes Charles Wilde
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
                # Milestone 3: Verify that contact search result includes Charles Wilde
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
                                                "value": "Charles Wilde",
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
                    ]
                ),
                # Milestone 4-5: Verify that contact search result includes Charles Wilde
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
                # Milestone 5: Verify that contact search result includes Francis Wagner
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
                                                "value": "Francis Wagner",
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
                        ),
                    ]
                ),
                # Milestone 6: Verify agent sent an email informing Charles, Vickie, and Francis about cancellation and reschedule
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        [
                                            "charles.wilde@orchardtheater.com",
                                            "vickie.lee@orchardtheater.com",
                                            "francis.wagner@orchardtheater.com",
                                        ]
                                    ],
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-01T20:10:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR
                    ],  # exclude CALENDAR additions
                ),
                # Milestone 7: Verify agent created a Calendar event "Rescheduled Theatre Rehearsal" on 2-Dec-2024 21:00-22:00 and invited Charles, Vickie, Francis
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Rescheduled Theatre Rehearsal",
                                    "start_datetime_iso": "2024-12-02T21:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "Charles Wilde",
                                            "Dawei Shen",
                                            "Francis Wagner",
                                            "Vickie Lee",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-01T20:10:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL
                    ],  # exclude EMAIL additions
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (2, 3),
                (4, 5),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_af354c4c-4f0a-40c6-9145-1dc3b7426572_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "email",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T20:10:00-08:00",
            is_read_time="2024-12-01T20:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You cannot attend the rehearsal tonight due to a medical emergency and have to reschedule for the following day.      You send an email to everyone in the rehearsal group confirming this and create a new calendar event for the following day 2-December-2024 and invite them. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to email the folks that I can't make it to tonight's rehearsal and we're moving it to tomorrow at 9 o'clock in the evening. Also, create a calendar event for tomorrow called 'Rescheduled Theatre Rehearsal' and invite them. List their names to me as well.",
                },
            ],
            reasoning="The user wants to send an email to Charles, Vickie, and Francis letting them know that, due to a medical emergency, they can’t attend tonight’s rehearsal and have moved it to tomorrow at 9 pm. I will draft and send that email. Then I will immediately create a calendar event titled “Rescheduled Theatre Rehearsal” for 2-Dec-2024 from 21:00–22:00 and invite Charles Wilde, Vickie Lee, Francis Wagner, and myself (Dawei Shen).",
            success_conditions=[
                {
                    "input_text": "1. An email message saying \"I apologise for this guys but I wont be able to attend tonight's rehearsal as I'm extremely unwell, I've rescheduled the rehearsal for tomorrow. Calendar event to follow\" is created at 01-12-2024 at 20:10.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. A Calendar event is created called "Rescheduled Theatre Rehearsal" for 02-12-2024 at 21:00 to 22:00. Charles Wilde, Vickie Lee and Francis Wagner are the invitees.',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "send_email",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0: Verify that the agent uses search tools to figure out who should attend
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
                                        # not including contacts here since the message is about "today"
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1: Verify that the correct email with subject "Updated Rehearsal Schedule" from Francis Wagner was found
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
                                                "value": "Updated Rehearsal Schedule",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "francis.wagner@orchardtheater.com",
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
                # Milestone 2: Verify agent sent an email informing Charles, Vickie, and Francis about cancellation and reschedule
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        [
                                            "charles.wilde@orchardtheater.com",
                                            "vickie.lee@orchardtheater.com",
                                            "francis.wagner@orchardtheater.com",
                                        ]
                                    ],
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-01T20:10:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CALENDAR
                    ],  # exclude CALENDAR additions
                ),
                # Milestone 3: Verify agent created a Calendar event "Rescheduled Theatre Rehearsal" on 2-Dec-2024 21:00-22:00 and invited Charles, Vickie, Francis
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Rescheduled Theatre Rehearsal",
                                    "start_datetime_iso": "2024-12-02T21:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "Charles Wilde",
                                            "Dawei Shen",
                                            "Francis Wagner",
                                            "Vickie Lee",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-01T20:10:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL
                    ],  # exclude EMAIL additions
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # finding who are involved
                (1, 2),  # Send email
                (1, 3),  # create calendar event
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_ac08be22-6c0d-4b19-a0ec-f9de37cf80c4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T14:00:00-08:00",
            is_read_time="2024-12-03T14:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You have just realized that you missed one of your theatre rehearsals.      You know that Francis shared the new schedule recently but you haven't looked at it yet.      You want to know what time this was sent to see if you have a reasonable excuse of being asleep when it arrived. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did Francis email me the Updated Rehearsal Schedule?",
                },
            ],
            reasoning="The user is asking for the time they received a specific email. I should consult their email inbox and find the email they mean. I see one email from Francis. This email contains the attachment Updated Rehearsal Schedule, which was referred to by the user. \n",
            success_conditions=[
                {
                    "input_text": "1. Time of arrival for email from francis.wagner@orchardtheater.com received December 1st 2024 at 19:58 is confirmed.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0: Verify that the agent uses email search tools
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
                    ]
                ),
                # Milestone 1: Validate that the correct email from Francis Wagner with Updated Schedule is found
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
                                                "value": "Updated Rehearsal Schedule",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "francis.wagner@orchardtheater.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-01T19:58:00-08:00",
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
                # Milestone 2: User is informed of the correct email time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("19:58", "7:58")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_7a67084f-0c2d-4ca6-b4d9-b9e808df8d32_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "email",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T20:30:00-08:00",
            is_read_time="2024-12-01T20:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "you want to forward the Rehearsal Schedule to Jess so she knows when you'll be busy in the coming weeks.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Give Jess my Rehearsal Schedule via email.",
                },
            ],
            reasoning="Ok, the user wants me to give jess their rehearsal schedule. The user is referring to Jess Zimmer as they are the only Jess in their contacts. I wonder what they mean by Rehearsal Schedule? I do see a recently received document called 'Updated Rehearsal Schedule'. I think it's safe to say thats what they meant. I will now forward the 'Updated Rehearsal Schedule' document to Jess Zimmer via email. ",
            success_conditions=[
                {
                    "input_text": "1. Document 'Updated Rehearsal Schedule' is forwarded via email to Jess Zimmer jess.zimmer@fintechstartup.com",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "send_email",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent retrieves the relevant rehearsal schedule email (e.g., from Francis)
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
                                # Allow either searching emails or listing all to find the schedule
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=["search_emails", "get_all_emails"],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Confirm that the "Updated Rehearsal Schedule" email was actually found in Milestone 0
                # We check that an email with that subject and attachment exists in the tool output.
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
                                                "value": "Updated Rehearsal Schedule",
                                                "partial": False,
                                            },
                                            # Ensure the attachment containing the schedule is there
                                            "attachments": {
                                                "value": "Rehearsal_Schedule_Updated_2024-12-01.pdf",
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
                            # Use the result from Milestone 0's tool call
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – Email is sent/forwarded to Jess with the rehearsal schedule attached
                # We don't require exact subject/body (could be "Fwd: ..." etc.), just that:
                # - status is "sent"
                # - Jess is the (only) recipient
                # - the schedule attachment is included.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["jess.zimmer@fintechstartup.com"]
                                    ],
                                    "status": "sent",
                                    "attachments": [
                                        ["Rehearsal_Schedule_Updated_2024-12-01.pdf"]
                                    ],
                                    "creation_datetime_iso": "2024-12-01T20:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                # Require that the schedule file is among the attachments; allow extras
                                "attachments": column_list_subset_match_similarity,
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
                (0, 1),  # Email search/listing → confirm rehearsal schedule email found
                (
                    1,
                    2,
                ),  # Rehearsal schedule located → email with that schedule sent to Jess
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_e2bee981-5d66-4d55-847b-188adc232a99_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T21:00:00-08:00",
            is_read_time="2024-12-01T21:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You and Charles are waiting to begin your theatre rehearsal.      You've been waiting since 20:00 for Vickie, she said she'd be only 20 minutes late but she is still not here.      You want to check what time she sent her message. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I get my last message from Vickie Lee?",
                },
            ],
            reasoning="The user is asking what time they received a message.\nI should look through their conversation with Vickie Lee and check the time of the most recent message from her.\nThe most recent message from Vickie Lee was received at 19:55.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Time of arrival for message from Vickie Lee on December 1st 2024, 19:55 is confirmed.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0: Verify that the agent searched WhatsApp or messages appropriately
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1: Verify that Vickie Lee's message timestamp is extracted correctly (19:55)
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
                                            "sender_name": {
                                                "value": "Vickie Lee",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-01T19:55:00",
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
                # Milestone 2: Agent informs the user with appropriate content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("7:55", "19:55")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_38191b65-63de-40b6-8844-e5a960e877d2_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T10:00:00-08:00",
            is_read_time="2024-12-02T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to reschedule your virtual assistant discussion on Wednesday to 1:00 - 2:00 later in the day and send a message to Michelle and Theo telling them the discussion has been moved "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Move Wednesday's discussion to 1 o'clock later in the afternoon and message Michelle and Theo in a group chat about it",
                },
            ],
            reasoning='The user wants me to move Wednesday\'s discussion to 1:00 later in the afternoon and message Michelle and Theo about it, so first I must determine which discussion he is referring to. I will look at the user\'s calendar. There is only one event scheduled for Wednesday prior to 1:00 titled "Discussion on Virtual Assistant Algorithm Updates," so I can assume this is the event the user wishes me to move. I have moved the event to 1:00-2:00 on 4 December.\n\nNow I must message Michelle and Theo about it. I will check the event details to confirm the attendee list. Dawei Shen (the organizer), Michelle Barnes, and Theo Appleseed are listed as attendees. I will draft a group-chat message that includes all three participants saying something like "Just letting you know I had to reschedule the meeting to 1:00 pm on Wednesday." Once the user approves, I will send the message.',
            success_conditions=[
                {
                    "input_text": '1. The event named "Discussion on Virtual Assistant Algorithm Updates" with Michelle Barnes and Theo Appleseed is moved from 10:00-11:00 on 4 December 2024 to 1:00-2:00 on 4 December 2024',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": '2. A message is sent to Michelle Barnes and Theo Appleseed saying "Just letting you know I had to reschedule the meeting to 1:00 pm on Wednesday."',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_message",
                "create_calendar_event",
                "modify_calendar_event",
                "remove_calendar_event",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0: Agent uses get_all_calendars or search_calendar_events to find the existing event
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
                                        "get_all_calendars",
                                        "search_calendar_events",
                                    ],
                                ),
                            },
                        )
                    ]
                ),
                # Milestone 1: Verify that event with correct name and attendees exists
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
                                                "value": "Discussion on Virtual Assistant Algorithm Updates",
                                                "partial": False,
                                            },
                                            "attendees_names": {
                                                "value": [
                                                    "Dawei Shen",
                                                    "Michelle Barnes",
                                                    "Theo Appleseed",
                                                ],
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-04T10:00:00-08:00",
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
                # Milestone 2: Modify the calendar event to be from 1:00pm to 2:00pm
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Discussion on Virtual Assistant Algorithm Updates",
                                    "start_datetime_iso": "2024-12-04T13:00:00-08:00",
                                    "end_datetime_iso": "2024-12-04T14:00:00-08:00",
                                    "creation_datetime_iso": "2024-12-02T10:00:00-08:00",
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
                    guardrail_database_exclusion_list=[DatabaseNamespace.MESSAGING],
                ),
                # Milestone 3: Send a message to Michelle and Theo
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
                                                "michelle.barnes@orchardtech.com",
                                                "+1 555-012-3456-7890",
                                            ),
                                            (
                                                "theo.appleseed@orchardtech.com",
                                                "+1 555-789-0123-4568",
                                            ),
                                            (
                                                "+1 555-123-4567-8901",
                                                "dawei.shen@orchardtech.com",
                                            ),
                                        ]
                                    ],
                                    "content": [("1:00", "13:00", "1 pm", "1pm")],
                                    "creation_datetime_iso": "2024-12-02T10:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
                                "content": column_str_contains_any_similarity,
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
                (0, 1),  # search for calendar
                (1, 2),  # modify the calendar
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_f400c351-5da6-40b5-91b9-f9990b07c175_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T12:30:00-08:00",
            is_read_time="2024-12-02T12:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You get into an argument with Francis and want to check what time the Updated Rehearsal Schedule email was sent to you "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I receive that email from Francis on Sunday",
                },
            ],
            reasoning="The user wants me to check the time of an email from Francis. So I'll look through the user's emails and see if any have been received from Francis. Ok, there is one from Francis Wagner with the subject line \"Updated Rehearsal Schedule\". That must be the email the user is talking about. I see that the email was received at 19:58 (7:58 PM) on Sunday, and I read that time to the user.",
            success_conditions=[
                {
                    "input_text": "1. The received time of the email from francis.wagner@orchardtheater.com about the Updated Rehearsal Schedule is read to the user",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0: Agent uses get_all_emails or search_emails tool
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
                                        "get_all_emails",
                                        "search_emails",
                                    ],
                                )
                            },
                        ),
                    ],
                ),
                # Milestone 1: Verify the email "Updated Rehearsal Schedule" from Francis Wagner is found
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
                                                "value": "Updated Rehearsal Schedule",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "francis.wagner@orchardtheater.com",
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
                # Milestone 2: Agent informs user of the time the email was sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("19:58", "7:58")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_38191b65-63de-40b6-8844-e5a960e877d2_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T10:00:00-08:00",
            is_read_time="2024-12-02T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to reschedule your virtual assistant discussion on Wednesday to 1:00 - 2:00 later in the day and send a message to Michelle and Theo telling them the discussion has been moved "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Move Wednesday's meeting to 1 o'clock later in the afternoon and message the guys together about it",
                },
            ],
            reasoning='The user asked to move Wednesday\'s meeting to one o’clock later in the afternoon and notify the team. I first locate the only Wednesday event titled "Discussion on Virtual Assistant Algorithm Updates," currently set for 10 am – 11 am with attendees Dawei Shen, Michelle Barnes, and Theo Appleseed. I reschedule it to 1 pm – 2 pm on 4 December. Then I draft a notification to "the guys"—Michelle and Theo—letting them know the meeting has been moved to 1 pm. After the user’s approval, I send the message (the conversation thread automatically includes the organizer, Dawei).',
            success_conditions=[
                {
                    "input_text": 'The event named "Discussion on Virtual Assistant Algorithm Updates" with attendees Dawei Shen, Michelle Barnes, and Theo Appleseed is moved from 10:00-11:00 on 4 December 2024 to 13:00-14:00 on 4 December 2024.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "A message is sent to Michelle Barnes and Theo Appleseed informing them that the meeting has been rescheduled to 1 pm-2 pm on Wednesday.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "The creation time recorded on the updated entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_message",
                "create_calendar_event",
                "get_all_calendars",
                "modify_calendar_event",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0: Agent uses get_all_calendars or search_calendar_events to find the existing event
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
                                        "get_all_calendars",
                                        "search_calendar_events",
                                    ],
                                ),
                            },
                        )
                    ]
                ),
                # Milestone 1: Verify that event with correct name and attendees exists
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
                                                "value": "Discussion on Virtual Assistant Algorithm Updates",
                                                "partial": False,
                                            },
                                            "attendees_names": {
                                                "value": [
                                                    "Dawei Shen",
                                                    "Michelle Barnes",
                                                    "Theo Appleseed",
                                                ],
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-04T10:00:00-08:00",
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
                # Milestone 2: Modify the calendar event to be from 1:00pm to 2:00pm
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Discussion on Virtual Assistant Algorithm Updates",
                                    "start_datetime_iso": "2024-12-04T13:00:00-08:00",
                                    "end_datetime_iso": "2024-12-04T14:00:00-08:00",
                                    "creation_datetime_iso": "2024-12-02T10:00:00-08:00",
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
                    guardrail_database_exclusion_list=[DatabaseNamespace.MESSAGING],
                ),
                # Milestone 3: Send a message to Michelle and Theo
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
                                                "michelle.barnes@orchardtech.com",
                                                "+1 555-012-3456-7890",
                                            ),
                                            (
                                                "theo.appleseed@orchardtech.com",
                                                "+1 555-789-0123-4568",
                                            ),
                                            (
                                                "+1 555-123-4567-8901",
                                                "dawei.shen@orchardtech.com",
                                            ),
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-02T10:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_contains_similarity,
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
            milestone_edge_list=[(0, 1), (1, 2), (2, 3)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_e2bee981-5d66-4d55-847b-188adc232a99_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T21:00:00-08:00",
            is_read_time="2024-12-01T21:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You and Charles are waiting to begin your theatre rehearsal.      You've been waiting since 20:00 for Vickie, she said she'd be only 20 minutes late but she is still not here.      You want to check what time she sent her message. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did my theatre friend last text me?",
                },
            ],
            reasoning="The user mentions that Vickie said she would be 20 minutes late, so the “theatre friend” they care about is Vickie Lee. I should look up Vickie Lee’s most recent WhatsApp message and report its timestamp. I find her last message was sent on 1 Dec 2024 at 19:55. I will tell the user that Vickie last texted at 19:55 (7:55 pm).",
            success_conditions=[
                {
                    "input_text": "The assistant tells the user that Vickie Lee’s most recent message was at 19:55 (7:55 pm) on 1 Dec 2024.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0: Verify that the agent searched WhatsApp or messages appropriately
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1: Verify that Vickie Lee's message timestamp is extracted correctly (19:55)
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
                                            "sender_name": {
                                                "value": "Vickie Lee",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-01T19:55:00",
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
                # Milestone 2: Agent informs the user with appropriate content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("7:55", "19:55")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_7a67084f-0c2d-4ca6-b4d9-b9e808df8d32_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "email",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T20:30:00-08:00",
            is_read_time="2024-12-01T20:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "you want to forward the Rehearsal Schedule to Jess so she knows when you'll be busy in the coming weeks.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Pass that document I got to my girlfriend for me via email. ",
                },
            ],
            reasoning="Ok, the user wants me to Pass that document to their girlfriend. What do they mean by 'that document?' The user received a document earlier called 'Updated Rehearsal Schedule', I feel confident this is what they mean. By girlfriend I believe the user means Jess Zimmer. I will now forward the 'Updated Rehearsal Schedule' document to Jess Zimmer via email.",
            success_conditions=[
                {
                    "input_text": "1. Document 'Updated Rehearsal Schedule' is forwarded via email to Jess Zimmer jess.zimmer@fintechstartup.com",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "send_email",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent retrieves the relevant email containing the rehearsal schedule attachment
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
                # Milestone 1 – Confirm the "Updated Rehearsal Schedule" email with the attachment was actually retrieved
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
                                                "value": "Updated Rehearsal Schedule",
                                                "partial": False,
                                            },
                                            "attachments": {
                                                "value": [
                                                    "Rehearsal_Schedule_Updated_2024-12-01.pdf"
                                                ],
                                                "partial": True,  # allow extras if any
                                            },
                                            "sender_address": {
                                                "value": "francis.wagner@orchardtheater.com",
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
                # Milestone 2 – A new email is sent to Jess with the rehearsal schedule attachment
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["jess.zimmer@fintechstartup.com"]
                                    ],
                                    "status": "sent",
                                    "attachments": [
                                        ["Rehearsal_Schedule_Updated_2024-12-01.pdf"]
                                    ],
                                    "creation_datetime_iso": "2024-12-01T20:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                # Require that the specific schedule file is included, but allow additional attachments if present
                                "attachments": column_list_subset_match_similarity,
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
                (0, 1),  # Retrieved the original schedule email → confirmed its content
                (
                    1,
                    2,
                ),  # Confirmed original email → forwarded/sent to Jess with attachment
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_2986e240-6b10-4cdf-bdf5-6881e8b0f034_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T08:25:00-08:00",
            is_read_time="2024-12-02T08:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to find out how many events you have on in the morning next week (starting 12/9 Monday). "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you tell me how many events I have in my calendar for next week that starts in the morning please?",
                },
            ],
            reasoning="The user wants to find out how many events they have beginning early in the morning next week.\n\nFirst, I'll figure out exactly what they mean by the phrase \"in the morning\". I'll surmise that they mean a time between 8:00-11:00.\n\nNow I'll check their Calendar to see if they have any upcoming events next week that fit those parameters.\n\nI've found an event named \"Team Review Meeting\" that begins at 10:00 on Friday, December 13th. I'll inform the user of this information, as it clearly fits within the stated parameters.",
            success_conditions=[
                {
                    "input_text": "The assistant tells the user that they have one calendar event next week that starts in the morning.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "The assistant mentions the event 'Team Review Meeting' occurring at 10:00 AM on Friday, December 13.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0: Verify calendar events are retrieved
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
                                        "get_all_calendars",
                                        "search_calendar_events",
                                    ],
                                )
                            },
                        ),
                    ]
                ),
                # Milestone 1: Verify at least one event is in the morning next week (Dec 9 - Dec 15, morning 8:00-11:00)
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
                                            "calendar_event_name": {
                                                "value": "Team Review Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-13T10:00:00-08:00",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,  # depend on getting calendar events
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
                    ]
                ),
                # Milestone 2: Verify user is informed about the number of morning event
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("one", "1")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "You have one calendar event next week that starts in the morning",
                                }
                            ),
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_1a214b5c-a487-4793-9ea8-434190766b56_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "contact",
                "email",
                "phone_call",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-03T17:00:00-08:00",
            is_read_time="2024-12-03T17:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to see the updated rehearsal schedule to confirm that you are free on Thursday 5th of December for a date with your girlfriend.      You confirm that you are free that evening via phone call. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the email from Francis that I received over the weekend and then give my girlfriend a call.",
                },
            ],
            reasoning="The user wants me to find an email from someone called Francis that was received over the weekend. I found one contact, Francis Wagner, and searched the user’s email for messages from his address. Among those, I located the message with the subject “Updated Rehearsal Schedule,” which was sent over the past weekend. I will display that email to the user.\n\nThe user also asked me to call their girlfriend. I located the contact entry for Jess Zimmer (marked as “girlfriend”) and will place a call to her phone number, +1 555-123-4567-8902.",
            success_conditions=[
                {
                    "input_text": "1. The email from Francis Wagner that was received on Sunday 1st December 2024 at 19:58 is displayed to the user.",
                    "statefullness": "Stateless",
                },
                {
                    "statefullness": "Stateful",
                    "input_text": "2. A phone call is made to Jess Zimmer.",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
                "create_outgoing_call",
            ],
            milestones=[
                # Milestone 0: Agent searches for or retrieves emails
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
                    ]
                ),
                # Milestone 1: Email from Francis Wagner is extracted
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
                                                "value": "Updated Rehearsal Schedule",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "francis.wagner@orchardtheater.com",
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
                            reference_milestone_node_index=0,
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                        )
                    ]
                ),
                # Milestone 2: Email content shown to user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Updated Rehearsal Schedule",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        )
                    ]
                ),
                # Milestone 3: Agent retrieves contacts
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
                # Milestone 4: Jess Zimmer contact found
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
                                            "phone_number": {
                                                "value": "+1 555-123-4567-8902",
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
                            reference_milestone_node_index=3,
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                        )
                    ]
                ),
                # Milestone 5: Verify that a phone call was initiated
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.PHONE,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "receiver_address": "+1 555-123-4567-8902",
                                    "call_type": "outgoing",
                                    "creation_datetime_iso": "2024-12-03T17:00:00-08:00",
                                },
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (3, 4)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_1701d03e-cff4-4059-b0c3-329f280c7d12_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "email",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T20:15:00-08:00",
            is_read_time="2024-12-01T20:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to let your girlfriend Jess know what your theatre schedule is like at the moment.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Pass that doc onto my girlfriend for me. ",
                },
            ],
            reasoning="Ok so the user wants to pass that doc onto their girlfriend. What do they mean by that doc? From recent correspondence I can see the user was sent a document from Francis Wagner. This 'Updated Rehearsal Schedule' must be what they are referring to. Now which contact are they referring to when they say girlfriend? From contact info I believe they are referring to Jess Zimmer. Ok I will now forward 'Updated Rehearsal Schedule' to Jess Zimmer. ",
            success_conditions=[
                {
                    "input_text": '1. The email "Updated Rehearsal Schedule" is forwarded to Jess Zimmer, jess.zimmer@fintechstartup.com.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "send_email",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent uses an email retrieval tool to find the relevant email/doc to forward
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
                    ]
                ),
                # Milestone 1 – Confirm the "Updated Rehearsal Schedule" email was retrieved
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
                                                "value": "Updated Rehearsal Schedule",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "francis.wagner@orchardtheater.com",
                                                "partial": False,
                                            },
                                            "attachments": {
                                                "value": [
                                                    "Rehearsal_Schedule_Updated_2024-12-01.pdf"
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
                        )
                    ]
                ),
                # Milestone 2 – Agent uses contacts tool to resolve "girlfriend" -> Jess Zimmer
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
                # Milestone 3 – Confirm Jess Zimmer contact (girlfriend) was identified
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
                                            "email": {
                                                "value": "jess.zimmer@fintechstartup.com",
                                                "partial": False,
                                            },
                                            "relationship": {
                                                "value": "Girlfriend",
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
                # Milestone 4 – Email is forwarded/sent to Jess with the schedule attached
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # ensure Jess is the sole explicit recipient
                                    "recipients_addresses": [
                                        ["jess.zimmer@fintechstartup.com"]
                                    ],
                                    "status": "sent",
                                    # subject may be auto-prefixed with "Fwd:" or similar, so just check it contains original subject
                                    "subject": "Updated Rehearsal Schedule",
                                    # body should at least reference rehearsal/schedule or be a forward; we keep this loose,
                                    "creation_datetime_iso": "2024-12-01T20:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "subject": column_contains_similarity,
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
                (0, 1),  # Retrieve email → confirm correct email with attachment
                (2, 3),  # Retrieve contacts → confirm Jess as girlfriend
                (1, 4),  # Having the right email → forward/send it
                (3, 4),  # Having Jess's contact → send to her
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_2d338fd9-b548-48ff-87e6-e225a35f642d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T11:00:00-08:00",
            is_read_time="2024-12-02T11:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You are meeting the theater group for coffee and want a reminder of the last email from them. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the most recent email from the theater group .",
                },
            ],
            reasoning="I have to provide the user with the last correspondence from their theater group. I will first search the user’s email for messages from the theater group. After searching, I find the most recent email titled “Updated Rehearsal Schedule,” sent by Francis Wagner to Vickie Lee, Charles Wilde, and the user. I will present this email (including any attachment link) to the user.",
            success_conditions=[
                {
                    "input_text": "1. Updated Rehearsal Schedule email at 20:00 on December 1 2024 is presented to user.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0: Verify agent searches emails (to find the latest theater group email)
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
                        ),
                    ],
                ),
                # Milestone 1: Verify that the "Updated Rehearsal Schedule" email sent by Francis is retrieved
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
                                                "value": "Updated Rehearsal Schedule",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "francis.wagner@orchardtheater.com",
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
                # Milestone 2: Verify that agent informs user about the correct email content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Updated Rehearsal Schedule",
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
                                    "content": "Francis",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_1701d03e-cff4-4059-b0c3-329f280c7d12_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_2",
                "email",
                "contact",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T20:15:00-08:00",
            is_read_time="2024-12-01T20:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to let your girlfriend Jess know what your theatre schedule is like at the moment.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Forward that Google Doc to Jess please. ",
                },
            ],
            reasoning="The user wants to forward that google doc to Jess? what do they mean by that doc attached in an email? From recent correspondence I can see the email 'Updated Rehearsal Schedule' from Francis Wagner mentions an attached updated schedule. This 'Updated Rehearsal Schedule' email must be what they are referring to.  When the user says Jess they must be referring to Jess Zimmer as it is the only Jess in their contacts. Ok I will now forward the email 'Updated Rehearsal Schedule' to Jess Zimmer. ",
            success_conditions=[
                {
                    "input_text": '1. The email "Updated Rehearsal Schedule" is forwarded to Jess Zimmer, jess.zimmer@fintechstartup.com.',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "send_email",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent retrieves the relevant email (the “Google Doc” / schedule email)
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
                # Milestone 1 – Confirm the “Updated Rehearsal Schedule” email was retrieved
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
                                                "value": "Updated Rehearsal Schedule",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "francis.wagner@orchardtheater.com",
                                                "partial": False,
                                            },
                                            # Attachment name helps ensure it's the schedule doc
                                            "attachments": {
                                                "value": [
                                                    "Rehearsal_Schedule_Updated_2024-12-01.pdf"
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
                        )
                    ],
                ),
                # Milestone 2 – Email has been forwarded to Jess (stateful EMAIL change)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Ensure Jess is the sole direct recipient
                                    "recipients_addresses": [
                                        ["jess.zimmer@fintechstartup.com"]
                                    ],
                                    "status": "sent",
                                    # Subject often prefixed with "Fwd:" or "FW:", allow loose match
                                    "subject": "Updated Rehearsal Schedule",
                                    "creation_datetime_iso": "2024-12-01T20:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "subject": column_rouge_l_similarity,
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
                (0, 1),  # Retrieved email → confirmed correct email
                (1, 2),  # Correct email identified → forwarded to Jess
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_2_2986e240-6b10-4cdf-bdf5-6881e8b0f034_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_2",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T08:25:00-08:00",
            is_read_time="2024-12-02T08:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to find out how many events you have on in the morning next week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to know how many events are happening in the morning for me next week.",
                },
            ],
            reasoning="The user wants to know how many events they have that are happening in the morning next week.\n\nFirstly, I need to ascertain what they mean by \"in the morning\". I'll assume they mean sometime between 8:00 and 11:00.\n\nNext, I'll check their calendar to see if they have any upcoming events next week (Monday 2024-12-09 through Sunday 2024-12-15) that fall within that time window.\n\nI've found an event named \"Team Review Meeting\" that's taking place between 10:00 – 11:00 on Friday, 2024-12-13. Since this is the only event matching the criteria, I will inform the user that they have one morning event next week.",
            success_conditions=[
                {
                    "input_text": "The assistant tells the user they have one event happening in the morning next week.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0: Agent uses a calendar retrieval tool to find events
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
                                        "get_all_calendars",
                                        "search_calendar_events",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1: Verify that the event "Team Review Meeting" falls into the correct date and time range
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
                                                "value": "Team Review Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-13T10:00:00-08:00",
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
                # Milestone 2: Agent informs user about the morning event properly
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("one", "1")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
    ]
