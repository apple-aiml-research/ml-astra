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
    column_one_similarity,
    column_rouge_l_similarity,
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


def get_TAG_EMILY_ROSE_pilot_plot_18(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="EMILY_ROSE_18_4ed82f54-614d-47d9-88e0-eeb5dc93ea5d_single_turn_4",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_18",
                "messaging",
                "contact",
                "email",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T11:20:00-08:00",
            is_read_time="2024-12-14T11:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know the location of where you're meeting Daniel in order to get a good parking space. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What's the address of my event that starts in an hour?",
                },
            ],
            reasoning="Okay so, the user wants to know where their event that starts in an hour is taking place. From checking their calendar, I can see they have one event today, 14 December 2024 at 12:00 titled 'Meeting with Daniel Kim at Local Cafe' with Daniel Kim as an attendee. However, it's 11:20 right now and the user said the event starts in an hour, but this event at 12:00 starts in 40 minutes. I'll have to assume the user is talking about this event anyway because it's the only event on the calendar, and I can't expect them to keep track of the exact times of all their events! This 'Meeting with Daniel Kim at Local Cafe' must be the event the user is requesting the address for. I only see the location listed as \"Local Cafe, Orchard County,\" without a specific address. I don't see any email exchanges or text messages with Daniel Kim that mention the address of the cafe, either. I'll inform the user that the only information about the location for this event is that it's at a venue named Local Cafe, located in Orchard County.",
            success_conditions=[
                {
                    "input_text": "1. The location of 'Meeting with Daniel Kim at Local Cafe', 'Local Cafe, Orchard County', which is scheduled for 14 December 2024 from 12:00 to 13:00 is presented to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "search_contacts",
                "get_all_contacts",
                "search_emails",
                "get_all_emails",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks up calendar events to find the meeting that starts around now
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
                # Milestone 1 – Confirms that the correct calendar event was retrieved
                # "Meeting with Daniel Kim at Local Cafe" on 2024-12-14T12:00:00-08:00 with location "Local Cafe, Orchard County"
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
                                                "value": "Meeting with Daniel Kim at Local Cafe",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-14T12:00:00-08:00",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Local Cafe, Orchard County",
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
                # Milestone 2 – The agent tells the user the event location ("Local Cafe, Orchard County")
                # and clarifies that this is all the location detail available (no full street address).
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We only require that the response mention the location string.
                                    "content": "Local Cafe",
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
                (0, 1),  # calendar lookup → confirm correct event and location
                (1, 2),  # confirmed event → inform user of location
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_18_4ed82f54-614d-47d9-88e0-eeb5dc93ea5d_single_turn_3",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "messaging",
                "contact",
                "email",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T11:20:00-08:00",
            is_read_time="2024-12-14T11:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know the location of where you're meeting Daniel in order to get a good parking space. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What's the location of my event that starts in an hour?",
                },
            ],
            reasoning="Okay so, the user wants to know where their event that starts in an hour is taking place. From checking their calendar, I can see they have one event today, 14 December 2024 at 12:00 titled 'Meeting with Daniel Kim at Local Cafe' with Daniel Kim as an attendee. However, it's 11:20 right now and the user said the event starts in an hour, but this event at 12:00 starts in 40 minutes. I'll have to assume the user is talking about this event anyway because it's the only event on the calendar, and I can't expect them to keep track of the exact times of all their events! This 'Meeting with Daniel Kim at Local Cafe' must be the event the user is requesting the location information about. The location on the event is 'Local Cafe, Orchard County'. I can present this to the user.",
            success_conditions=[
                {
                    "input_text": "1. The location of 'Meeting with Daniel Kim at Local Cafe', 'Local Cafe, Orchard County', which is scheduled for 14 December 2024 from 12:00 to 13:00 is presented to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "search_contacts",
                "get_all_contacts",
                "search_emails",
                "get_all_emails",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – The agent uses calendar tools to look up upcoming events (to find the one starting in ~1 hour)
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
                # Milestone 1 – Confirms that the correct event with Daniel was retrieved from the calendar tools
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
                                            # Verify this exact meeting was found
                                            "calendar_event_name": {
                                                "value": "Meeting with Daniel Kim at Local Cafe",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-14T12:00:00-08:00",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Local Cafe, Orchard County",
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
                            # Use the result of the calendar search in Milestone 0
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
                # Milestone 2 – The agent tells the user the correct location of that event
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Only check for essential pieces: cafe and Orchard County
                                    "content": [("Local Cafe",)],
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
                (0, 1),  # Calendar lookup → confirm correct event found
                # Milestone 2 (user response) does not have to depend strictly on Milestone 1 for validation,
                # but logically follows it; we don't enforce with an edge to keep evaluation simple.
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_18_f18771d8-831c-4ed0-8ac0-7014bfc952c5_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T20:00:00-08:00",
            is_read_time="2024-12-13T20:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to be reminded of the time you're meeting Daniel Kim at the Cafe tomorrow, as you're wondering how much time you have tomorrow morning to brainstorm ideas beforehand, to bring up when you meet. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is my coffee thing at? ",
                },
            ],
            reasoning="The user wants to know what time their coffee thing is at. I wonder what they're referring to. I should check their calendar to figure it out. I see an event called 'Meeting with Daniel Kim at Local Cafe' happening tomorrow, Saturday, December 14th 2024, at 12:00-13:00. Meeting at a cafe is associated with having coffee so I think this is the event they're referring to. I'll tell them the details, including the time of this event now.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The time of the event 'Meeting with Daniel Kim at Local Cafe', on Saturday, December 14th 2024, at 12:00-13:00 is shown to the user.",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent looks up calendar events (information-retrieval step)
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
                # Milestone 1 – Confirms the café meeting with Daniel Kim is returned from the tool call in Milestone 0
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
                                                "value": "Meeting with Daniel Kim at Local Cafe",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-14T12:00:00-08:00",
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
                # Milestone 2 – Agent tells the user the correct meeting time (user-facing response)
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
                                            "12:00",
                                            "12 pm",
                                            "12 p.m.",
                                            "noon",
                                            "12-1",
                                            "12-1",
                                            "12–1",
                                            "12pm",
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
                (0, 1),  # Calendar lookup → verify event found
                (1, 2),  # Event found → user informed of time
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_18_2dd944fe-d374-4bac-8614-87f9a2eaea48_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T13:10:00-08:00",
            is_read_time="2024-12-14T13:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to dictate a reply email to Daniel saying that you need to speak with him as you're unhappy with the vegan options. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a reply email saying "Hi Daniel can we meet later to discuss the menu again? I\'m really not happy with the vegan options available at the moment."',
                },
            ],
            reasoning="The user wants to dictate a reply email. Accordign to the content, it should be a contact named 'Daniel'. \n\nI should locate the email history with this contact by searching their name in the user's Inbox and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the email if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": '1. A reply email is sent in response to the email from Daniel Kim  on December 14th at 13:00, with the text "Hi Daniel can we meet later to discuss the menu again? I\'m really not happy with the vegan options available at the moment."',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "modify_draft_email",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Agent looks up email thread(s) to find Daniel’s message
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
                # Milestone 1 – Confirm Daniel Kim’s 14-Dec-2024 email was actually found
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
                                                "value": "daniel.kim@localcafe.com",
                                                "partial": False,
                                            },
                                            # Subject match is partial to avoid strictness on “Re:” prefixes, etc.
                                            "subject": {
                                                "value": "Confirmation of Menu and Resources",
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
                # Milestone 2 – A reply email has been SENT to Daniel with the user-dictated text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["daniel.kim@localcafe.com"]
                                    ],
                                    "body": ("can we meet later"),
                                    "creation_datetime_iso": "2024-12-14T13:10:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_subset_match_similarity,
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
            name="EMILY_ROSE_18_b72a84fb-f13c-4df6-9dc3-c3a154db65bc_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T10:00:00-08:00",
            is_read_time="2024-12-14T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know what time you're meeting Daniel later "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is the meeting later?",
                },
            ],
            reasoning="The user wants to know what time the meeting is later. Which meeting are they referring to? I'll check their calendar to see if they have anything scheduled. I can see they have an event titled \"Meeting with Daniel Kim at Local Cafe\" scheduled for 12:00 pm later today. I an assume this is the meeting they were referring to. I'll give this information to the user.",
            success_conditions=[
                {
                    "input_text": '1. The time of the event "Meeting with Daniel Kim at Local Cafe" scheduled for December 14 2024 12:00-13:00 is given to the user.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent looks at the calendar to figure out today's meeting time
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
                # Milestone 1 – Verify that the returned calendar data contains the meeting with Daniel Kim at 12:00 PM
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
                                                "value": "Meeting with Daniel Kim at Local Cafe",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-14T12:00:00-08:00",
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
                # Milestone 2 – The agent tells the user the meeting is at 12 PM (noon)
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
                                            "12:00 PM",
                                            "12:00 PM",
                                            "12 pm",
                                            "12 p.m.",
                                            "noon",
                                            "12pm",
                                            "12:00",
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
            name="EMILY_ROSE_18_4ed82f54-614d-47d9-88e0-eeb5dc93ea5d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "messaging",
                "contact",
                "email",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T11:20:00-08:00",
            is_read_time="2024-12-14T11:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know the location of where you're meeting Daniel in order to get a good parking space. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where am I meeting Daniel Kim?",
                },
            ],
            reasoning="Right so, the user is looking for the location of where they're meeting 'Daniel Kim'. From checking the user's contacts I see no one under that name. Next, I will check the user's calendar and can see an event matching, scheduled for today, 14 December 2024 at 12:00 titled 'Meeting with Daniel Kim at Local Cafe' with Daniel Kim' with Daniel Kim as an attendee. This is the event the user is requesting the location information. The location has been added as 'Local Cafe, Orchard County'. I can display this to the user.",
            success_conditions=[
                {
                    "input_text": "1. The location of 'Meeting with Daniel Kim at Local Cafe', 'Local Cafe, Orchard County', which is scheduled for 14 December 2024 from 12:00 to 13:00 is presented to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "search_contacts",
                "get_all_contacts",
                "search_emails",
                "get_all_emails",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – Agent uses calendar tools to look up the meeting with Daniel Kim
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
                # Milestone 1 – Confirm the specific event with Daniel Kim on Dec 14, 2024, 12:00–13:00 and its location was retrieved
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
                                                "value": "Meeting with Daniel Kim at Local Cafe",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-14T12:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-14T13:00:00-08:00",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Local Cafe, Orchard County",
                                                "partial": False,
                                            },
                                            "attendees_names": {
                                                "value": ["Daniel Kim", "Emily Rose"],
                                                "partial": True,  # allow list-order/format flexibility
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
                # Milestone 2 – User-facing answer includes the correct meeting location text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Just ensure the location phrase appears somewhere in the response
                                    "content": "Local Cafe, Orchard County",
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
                (0, 1),  # calendar lookup → confirm correct event & location
                (1, 2),  # confirmed event → respond to user with location
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_18_4ed82f54-614d-47d9-88e0-eeb5dc93ea5d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "messaging",
                "contact",
                "email",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T11:20:00-08:00",
            is_read_time="2024-12-14T11:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know the location of where you're meeting Daniel in order to get a good parking space. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where is my event at 12:00 taking place?",
                },
            ],
            reasoning="Okay so, the user wants to know where their event at 12:00 is. From checking their calendar, I can see they have one event today, 14 December 2024 at 12:00 titled 'Meeting with Daniel Kim at Local Cafe' with Daniel Kim as an attendee. This is the event the user is requesting the location information about. The location has been added as 'Local Cafe, Orchard County'. I can display this to the user.",
            success_conditions=[
                {
                    "input_text": "1. The location of 'Meeting with Daniel Kim at Local Cafe', 'Local Cafe, Orchard County', which is scheduled for 14 December 2024 from 12:00 to 13:00 is presented to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "search_contacts",
                "get_all_contacts",
                "search_emails",
                "get_all_emails",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – The agent uses calendar tools to look up the 12:00 event (or all calendar events)
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
                # Milestone 1 – Confirms the correct 12:00 event with Daniel Kim at Local Cafe was retrieved
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
                                                "value": "Meeting with Daniel Kim at Local Cafe",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-14T12:00:00-08:00",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Local Cafe, Orchard County",
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
                # Milestone 2 – User is informed of the correct location of the 12:00 event
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Only check that the response mentions the key location phrase
                                    "content": "Local Cafe, Orchard County",
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
                (0, 1),  # Calendar lookup → confirm correct event and location
                (1, 2),  # Confirmed event/location → answer user with that location
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_18_b72a84fb-f13c-4df6-9dc3-c3a154db65bc_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T10:00:00-08:00",
            is_read_time="2024-12-14T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know what time you're meeting Daniel later "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is my meeting with Daniel Kim today?",
                },
            ],
            reasoning="The user is asking about the time of an event.\nFirst I should find the event in the user's calendar. I can see an exact match for the user's query, Meeting with Daniel Kim at Local Cafe scheduled for December 14 2024 12:00-13:00.\nI should inform the user that this event begins today at 12:00.",
            success_conditions=[
                {
                    "input_text": '1. The time of the event "Meeting with Daniel Kim at Local Cafe" scheduled for December 14 2024 12:00-13:00 is given to the user.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
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
                    ]
                ),
                # Milestone 1 – Confirm the Daniel Kim meeting was returned
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
                                                "value": "Daniel Kim",
                                                "partial": True,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-14T12:00:00-08:00",
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
                # Milestone 2 – Agent tells the user the meeting time
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
                                            "12:00",
                                            "12 pm",
                                            "12pm",
                                            "12 p.m.",
                                            "12:00 PM",
                                            "noon",
                                            "midday",
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
                (0, 1),  # calendar lookup → confirm meeting retrieved
                (1, 2),  # meeting retrieved → user informed
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_18_2dd944fe-d374-4bac-8614-87f9a2eaea48_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T13:10:00-08:00",
            is_read_time="2024-12-14T13:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to dictate a reply email to Daniel saying that you need to speak with him as you're unhappy with the vegan options. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a reply email to Danny saying "Hi Daniel can we meet later to discuss the menu again? I\'m really not happy with the vegan options available at the moment."',
                },
            ],
            reasoning="The user wants to dictate a reply email to someone called Danny. I don't see any email coming from someone with that name. However, I know that Danny could be used to refer to someone called Daniel. I should check to see if the user has any emails from someone called Daniel. I see the user has one email from a Daniel Kim received on December 14th, 2024, at 13:00. \nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the email if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": '1. A reply email is sent in response to the email from Daniel Kim  on December 14th at 13:00, with the text "Hi Daniel can we meet later to discuss the menu again? I\'m really not happy with the vegan options available at the moment."',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "modify_draft_email",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – Agent searches or lists emails to locate Daniel’s message
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
                # Milestone 1 – Validate that the retrieved email is the one from Daniel Kim
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
                                                "value": "daniel.kim@localcafe.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Confirmation of Menu and Resources",
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
                # Milestone 2 – A reply email has been sent to Daniel with the requested text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["daniel.kim@localcafe.com"]
                                    ],
                                    "status": "sent",
                                    "body": "not happy with the vegan options",
                                    "creation_datetime_iso": "2024-12-14T13:10:00-08:00",
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
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Email search → confirm correct email located
                (1, 2),  # Confirmed email → reply sent
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_18_f18771d8-831c-4ed0-8ac0-7014bfc952c5_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T20:00:00-08:00",
            is_read_time="2024-12-13T20:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to be reminded of the time you're meeting Daniel Kim at the Cafe tomorrow, as you're wondering how much time you have tomorrow morning to brainstorm ideas beforehand, to bring up when you meet. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time is meeting Daniel at?",
                },
            ],
            reasoning="The user wants to know what time meeting Daniel is at. I wonder what they're referring to. I should check their calendar to figure it out. I see an event with a similar name, 'Meeting with Daniel Kim at Local Cafe' happening tomorrow, Saturday, December 14th 2024, at 12:00-13:00. I assume this is the event they mean. I'll tell them the details, including the time of this event now.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The time of the event 'Meeting with Daniel Kim at Local Cafe', on Saturday, December 14th 2024, at 12:00-13:00 is shown to the user.",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – A calendar-lookup tool is invoked so the agent can find the meeting time
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
                # Milestone 1 – The tool output included the correct event with the correct start time
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
                                                "value": "Meeting with Daniel Kim at Local Cafe",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-14T12:00:00-08:00",
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
                # Milestone 2 – The agent tells the user the meeting time (must mention the time and Daniel)
                Milestone(
                    snapshot_constraints=[
                        # Must contain a reference to the meeting time (any reasonable phrasing)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "12:00",
                                            "12 pm",
                                            "12 p.m.",
                                            "12:00 pm",
                                            "noon",
                                            "12pm",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
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
            name="EMILY_ROSE_18_0487ba0c-aba4-4eae-a58c-7937bab6be30_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T13:05:00-08:00",
            is_read_time="2024-12-14T13:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to send a reply email to Daniel Kim about the menu and resources. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Email back the local cafe and say "Hey Daniel, Yeah, it was swell seeing you too. So I just want to make absolutely sure that everything you agreed to provide is being provided gratis, right? Thanks, Emily Rose, Event Guru"',
                },
            ],
            reasoning='The user is asking to send an email.\nFirst, I should find the intended recipient. The user has provided me with local cafe, I can see they have recently received an email from this address daniel.kim@localcafe.com. \nNext, I will draft the message as instructed.\nAn email with the text "Hey Daniel, Yeah, it was swell seeing you too. So I just want to make absolutely sure that everything you agreed to provide is being provided gratis, right? Thanks, Emily Rose, Event Guru" will be send to daniel.kim@localcafe.com',
            success_conditions=[
                {
                    "input_text": '1. An email is sent in reply to the email from Daniel Kim called Re: Confirmation of Menu and Resources for Upcoming Events to say  "Hey Daniel, Yeah, it was swell seeing you too. So I just want to make absolutely sure that everything you agreed to provide is being provided gratis, right? Thanks, Emily Rose, Event Guru"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – The agent looks up Daniel’s previous email (information-retrieval)
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
                # Milestone 1 – Confirm the retrieved email is Daniel Kim’s
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
                                                "value": "daniel.kim@localcafe.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Re: Confirmation of Menu and Resources for Upcoming Events",
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
                # Milestone 2 – A reply email is sent to Daniel Kim
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["daniel.kim@localcafe.com"]
                                    ],
                                    "status": "sent",
                                    "body": "gratis",
                                    "creation_datetime_iso": "2024-12-14T13:05:00-08:00",
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
            name="EMILY_ROSE_18_9d548f04-3071-4bce-a567-3dc12b9d4dc1_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T13:45:00-08:00",
            is_read_time="2024-12-14T13:45:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to follow up with Daniel Kim after your meeting at his cafe. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to Daniel saying thank you for confirming, it was great talking to you today\n",
                },
            ],
            reasoning="The user wants to reply to Daniel Kim's latest email with the text \"thank you for confirming, it was great talking to you today\". First I'll find the specific email by looking through recently received emails, and with this I can compose the reply and see if the user is happy to send it.",
            success_conditions=[
                {
                    "input_text": "1. A reply is sent to Daniel Kim's latest email saying \"thank you for confirming, it was great talking to you today”",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – Agent searches / retrieves emails to locate Daniel Kim's latest message
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
                # Milestone 1 – Confirm the email from Daniel Kim was found in the tool result of Milestone 0
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
                                                "value": "daniel.kim@localcafe.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Confirmation of Menu and Resources",
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
                # Milestone 2 – A reply email has been sent to Daniel Kim containing the thank-you message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["daniel.kim@localcafe.com"]
                                    ],
                                    "status": "sent",
                                    "body": "thank you",  # we will match with contains-similarity below,
                                    "creation_datetime_iso": "2024-12-14T13:45:00-08:00",
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
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_18_9d548f04-3071-4bce-a567-3dc12b9d4dc1_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T13:45:00-08:00",
            is_read_time="2024-12-14T13:45:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to follow up with Daniel Kim after your meeting at his cafe. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to Daniel Kim with this; "thank you for confirming, it was great talking to you today."',
                },
            ],
            reasoning="Ok so the user wants to reply to Daniel Kim with a given message. First is the recipients which is given by the user. Next is the mode of communication which is hinted at by the user but not said outright. They want to reply to something so that suggests that there is already a conversation in progress. I will now look for recent conversations Daniel Kim. I have found an email thread with Daniel Kim this must be what the user wants to reply to. I will now send the user's given message to Daniel Kim via email at 13:45 on 14 December 2024. ",
            success_conditions=[
                {
                    "input_text": "1. A reply is sent to Daniel Kim's latest email saying \"thank you for confirming, it was great talking to you today”",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – Agent looks up email threads (information-retrieval step)
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
                # Milestone 1 – Confirm Daniel Kim’s latest email was among the results
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
                                                "value": "daniel.kim@localcafe.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Confirmation of Menu and Resources for Upcoming Events",
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
                # Milestone 2 – A reply email has been sent to Daniel Kim
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["daniel.kim@localcafe.com"]
                                    ],
                                    "status": "sent",
                                    "body": "thank you for confirming, it was great talking to you today.",
                                    "creation_datetime_iso": "2024-12-14T13:45:00-08:00",
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
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Email search → verify correct email found
                (1, 2),  # After verifying, send the reply
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_18_0487ba0c-aba4-4eae-a58c-7937bab6be30_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T13:05:00-08:00",
            is_read_time="2024-12-14T13:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to send a reply email to Daniel Kim about the menu and resources. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to Danny, saying: Hey Daniel, Yeah, it was swell seeing you too. So I just want to make absolutely sure that everything you agreed to provide is being provided gratis, right? Thanks, Emily Rose, Event Guru",
                },
            ],
            reasoning="User Emily Rose wants to reply to someone referred to as Danny. I don't see anyone with that name in contacts, but i do see a recent email from a Daniel Kim. I see the message is about providing resources and this fits with the content of the message user wants to send. I shall draft the email reply to Daniel Kim and show it to user for approval. ",
            success_conditions=[
                {
                    "input_text": '1. An email is sent in reply to the email from Daniel Kim called Re: Confirmation of Menu and Resources for Upcoming Events to say  "Hey Daniel, Yeah, it was swell seeing you too. So I just want to make absolutely sure that everything you agreed to provide is being provided gratis, right? Thanks, Emily Rose, Event Guru"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – Agent looks up existing email thread(s)
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
                # Milestone 1 – The email from Daniel Kim is included in the tool result
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
                                                "value": "daniel.kim@localcafe.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Re: Confirmation of Menu and Resources for Upcoming Events",
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
                # Milestone 2 – A reply email is sent to Daniel Kim with the requested content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["daniel.kim@localcafe.com"]
                                    ],
                                    "subject": "Re: Confirmation of Menu and Resources for Upcoming Events",
                                    "status": "sent",
                                    "body": "gratis",
                                    "creation_datetime_iso": "2024-12-14T13:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "subject": column_rouge_l_similarity,
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
            name="EMILY_ROSE_18_d3989954-0538-4464-a410-6dc71ada1518_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-15T16:00:00-08:00",
            is_read_time="2024-12-15T16:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know who you have met at Local Cafe yesterday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Who did I meet at the Local Cafe yesterday?",
                },
            ],
            reasoning="The user wants to know who they meet yesterday. Let me look in Calendar to find out which event they are on about. It must be 'Meeting with Daniel Kim at Local Cafe'. I will inform them on who attended.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that Daniel Kim is the person they have met at Local Cafe' on December 14th from 12:00-13:00.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent queries the calendar to figure out yesterday’s meeting
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
                # Milestone 1 – The returned calendar entry is the meeting with Daniel Kim at Local Cafe
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
                                                "value": "Meeting with Daniel Kim at Local Cafe",
                                                "partial": False,
                                            },
                                            # It’s enough to confirm the correct event name
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
                # Milestone 2 – The user is informed that Daniel Kim was the person they met
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Daniel Kim",
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
            name="EMILY_ROSE_18_51ed2454-e466-43f1-8eef-1c9d5711778d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T13:30:00-08:00",
            is_read_time="2024-12-14T13:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "After going over the menu you realise that there will be an additional 12 guests that will be attending the event.   You want to inform Daniel Kim of this. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send an email to Chef Daniel Kim saying 'Hi Daniel, I just realised that we actually have 12 extra guests attending the event. Best, Emily.'",
                },
            ],
            reasoning="The user wants to send Chef Daniel Kim an email. Let me look in Mail to see who this is. It must be daniel.kim@localcafe.com as they are the only chef the user has emailed and they have the same name.\n\nI will draft up the message with the requested text which is 'Hi Daniel, I just realised that we actually have 12 extra guests attending the event. Best, Emily.'\n\nI will confirm it with the user and then send it.",
            success_conditions=[
                {
                    "input_text": "1. An email is sent to Chef Daniel Kim with the text ' Hi Daniel, I just realised that we actually have 12 extra guests attending the event. Best, Emily.'",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – Verify that a new email was sent to Daniel Kim with the correct message text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["daniel.kim@localcafe.com"]
                                    ],
                                    "body": "12 extra guests",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-14T13:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "body": column_contains_similarity,  # message must mention “12 extra guests”
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against the initial state
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_18_8586c1f8-3096-46dc-9a92-e372d7ec836e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T14:30:00-08:00",
            is_read_time="2024-12-10T14:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You are worried that you have scheduled the meeting with Daniel Kim for the wrong time so you decide to check the time. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you tell me what time I scheduled the meeting on the 14th?",
                },
            ],
            reasoning="The user wants to know what time they scheduled their meeting on the 14th. Checking their calendar, I can see one event I scheduled for 14th December 2024 from 12:00 to 13:00 titled 'Meeting with Daniel Kim at Local Cafe' with Daniel Kim listed as an attendee. This is the event that the user has requested so I can tell them the time of this event.",
            success_conditions=[
                {
                    "input_text": "1. The time of the event \"Meeting with Daniel Kim at Local Cafe\" on December 14, 2024 from 12:00 to 13:00 with 'Daniel Kim' as an attendee is informed to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent uses a calendar-retrieval tool
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
                # Milestone 1 – The expected event (Daniel Kim meeting) is present in the tool output
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
                                                "value": "Meeting with Daniel Kim at Local Cafe",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-14T12:00:00-08:00",
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
                # Milestone 2 – Agent informs the user of the scheduled time (12 PM)
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
                                            "12:00",
                                            "12 pm",
                                            "12pm",
                                            "12 p.m.",
                                            "noon",
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
            name="EMILY_ROSE_18_98b5787f-d318-4983-95bf-f58d5db4cecf_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T18:30:00-08:00",
            is_read_time="2024-12-12T18:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Daniel has broken his arm and is unable to attend the meeting on Saturday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the meeting with Daniel. ",
                },
            ],
            reasoning="The user wants to delete the meeting with Daniel. I should check the user's Calendar for an event by that name. \n\nHmm, looks like there is one event with a similar name, the Meeting with Daniel Kim at Local Cafe from 12:00-13:00 on the 14 December 2024. This must be the event the user means. \n\nI will now delete the event and let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. Meeting with Daniel Kim at Local Cafe from 12:00-13:00 on the 14 December 2024 is deleted from Calendar.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 –  Agent looks through the calendar for Daniel’s meeting
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
                # Milestone 1 –  The tool output from Milestone 0 actually contained the meeting with Daniel Kim
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
                                                "value": "Meeting with Daniel Kim at Local Cafe",
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
                            reference_milestone_node_index=0,  # depend on the search in Milestone 0
                        )
                    ],
                ),
                # Milestone 2 –  The meeting has been removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Meeting with Daniel Kim at Local Cafe",
                                    "start_datetime_iso": "2024-12-14T12:00:00-08:00",
                                }
                            ),
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
            name="EMILY_ROSE_18_98b5787f-d318-4983-95bf-f58d5db4cecf_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T18:30:00-08:00",
            is_read_time="2024-12-12T18:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Daniel has broken his arm and is unable to attend the meeting on Saturday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the event in two days. ",
                },
            ],
            reasoning="The user wants to delete the event in two days. I need to figure out which event they mean. \n\nI know today is the 12 December 2024, so in two days time it will be the 14 December 2024. This means the user wants to delete an event on this date. \n\nNext I will check the user's Calendar for any events on the 14 December 2024. Looks like there is only one event on the 14 December 2024, the Meeting with Daniel Kim at Local Cafe from 12:00-13:00 so this must be what the user meant. \n\nI will delete the event and let the user know. ",
            success_conditions=[
                {
                    "input_text": "1. Meeting with Daniel Kim at Local Cafe from 12:00-13:00 on the 14 December 2024 is deleted from Calendar.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent investigates upcoming calendar events (optional information-retrieval check)
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
                # Milestone 1 – The meeting with Daniel Kim on 14 Dec 2024 has been removed from the Calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Meeting with Daniel Kim at Local Cafe",
                                    "start_datetime_iso": "2024-12-14T12:00:00-08:00",
                                    "end_datetime_iso": "2024-12-14T13:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar lookup precedes deletion verification
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_18_8586c1f8-3096-46dc-9a92-e372d7ec836e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T14:30:00-08:00",
            is_read_time="2024-12-10T14:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You are worried that you have scheduled the meeting with Daniel Kim for the wrong time so you decide to check the time. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you tell me what time I scheduled the meeting with Daniel Kim?",
                },
            ],
            reasoning="The user wants to know what time they scheduled the meeting with Daniel Kim. First thing I need to do is look at the user's calendar and see if there are any events that match that name. Ok I found one named 'Meeting with Daniel Kim at Local Cafe' on December 14, 2024 from 12:00 to 13:00 with Daniel Kim listed as an attendee. This must be the event the user is referring to. Now that I have found it I can retrieve the time it is scheduled for and inform the user.",
            success_conditions=[
                {
                    "input_text": "1. The time of the event \"Meeting with Daniel Kim at Local Cafe\" on December 14, 2024 from 12:00 to 13:00 with 'Daniel Kim' as an attendee is informed to the user.",
                    "statefullness": "Stateless",
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
                # Milestone 1 – Confirm the desired event is present in the tool output
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
                                                "value": "Meeting with Daniel Kim at Local Cafe",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-14T12:00:00-08:00",
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
                # Milestone 2 – The agent tells the user the scheduled time
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
                                            "12:00",
                                            "12 pm",
                                            "12 p.m.",
                                            "12:00 PM",
                                            "12 PM",
                                            "noon",
                                            "12pm",
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
            name="EMILY_ROSE_18_51ed2454-e466-43f1-8eef-1c9d5711778d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T13:30:00-08:00",
            is_read_time="2024-12-14T13:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "After going over the menu you realise that there will be an additional 12 guests that will be attending the event.   You want to inform Daniel Kim of this. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send an email to the Chef saying 'Hi Daniel, I just realised that we actually have 12 extra guests attending the event. Best, Emily.'",
                },
            ],
            reasoning="The user wants to send the Chef an email. Let me look in Mail to see who this is. It must be daniel.kim@localcafe.com as they are the only chef the user has emailed.\n\nI will draft up the message with the requested text which is 'Hi Daniel, I just realised that we actually have 12 extra guests attending the event. Best, Emily.'\n\nI will confirm it with the user and then send it.",
            success_conditions=[
                {
                    "input_text": "1. An email is sent to Chef Daniel Kim with the text ' Hi Daniel, I just realised that we actually have 12 extra guests attending the event. Best, Emily.'",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – Verify that an email was sent to Daniel Kim containing the correct message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # The email must only go to Daniel Kim
                                    "recipients_addresses": [
                                        ["daniel.kim@localcafe.com"]
                                    ],
                                    # Email must be actually sent, not just drafted
                                    "status": "sent",
                                    # Body should mention the “12 extra guests” note
                                    "body": "12 extra guests",
                                    "creation_datetime_iso": "2024-12-14T13:30:00-08:00",
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
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ]
                )
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_18_6a8ee231-b6db-4829-9652-32508218adfe_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T14:00:00-08:00",
            is_read_time="2024-12-14T14:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to reply to the last email from Daniel Kim. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to the email with "Thanks for all the help Daniel".',
                },
            ],
            reasoning="The user wants to reply to an email from Daniel. I'll have to search through the user's inbox to see if there is any mail from Daniel ... I found a recent email from Daniel Kim, \"Confirmation of Menu and Resources for Upcoming Events\", received at 13:00 today, which matches the name of the person mentioned by the user. I'll take it that this is the person the user wants to reply to.",
            success_conditions=[
                {
                    "input_text": '1. A message saying "Thanks for all the help Daniel" is sent to Daniel Kim via email at 14:00 on 14 December 2024. ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – the agent looks for Daniel’s most recent email
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
                # Milestone 1 – confirm the email found in Milestone 0 is Daniel Kim’s latest message
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
                                                "value": "daniel.kim@localcafe.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Re: Confirmation of Menu and Resources for Upcoming Events",
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
                # Milestone 2 – a reply email has been sent to Daniel with the required content and timing
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["daniel.kim@localcafe.com"]
                                    ],
                                    "status": "sent",
                                    "body": "Thanks for all the help Daniel",
                                    "creation_datetime_iso": "2024-12-14T14:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
                                "status": column_exact_match_similarity,
                                "body": column_contains_similarity,  # allow additional text around the phrase
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
            name="EMILY_ROSE_18_365a76f7-7260-41fe-8cf6-6bc8b76b8620_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T11:20:00-08:00",
            is_read_time="2024-12-14T11:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know the location of where you're meeting Daniel in order to get a good parking space. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where is my event at 12:00 taking place?",
                },
            ],
            reasoning="Okay so, the user wants to know where their event at 12:00 is. From checking their calendar, I can see they have one event today, 14 December 2024 at 12:00 titled 'Meeting with Daniel Kim at Local Cafe' with Daniel Kim as an attendee. This is the event the user is requesting the location information about. The location has been added as 'Local Cafe, Orchard County'. I can display this to the user.",
            success_conditions=[
                {
                    "input_text": "1. The location of 'Meeting with Daniel Kim at Local Cafe', 'Local Cafe, Orchard County', which is scheduled for 14 December 2024 from 12:00 to 13:00 is displayed to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent invokes a calendar-retrieval tool to look up the event
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
                # Milestone 1 – Verify the returned tool output contained the noon meeting with Daniel Kim
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
                                                "value": "Meeting with Daniel Kim at Local Cafe",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-14T12:00:00-08:00",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Local Cafe, Orchard County",
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
                # Milestone 2 – Agent tells the user the correct location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Local Cafe, Orchard County",
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
            name="EMILY_ROSE_18_b6d27fbd-3ee4-4a9f-a4cd-5a0bf0ff0f78_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T11:25:00-08:00",
            is_read_time="2024-12-14T11:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You are about to leave for your meeting with Daniel Kim and want to know the location before you start driving. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Which café are we meeting at?",
                },
            ],
            reasoning='The user wants to know the location of an event, but has not provided much information besides the fact the event takes place at a cafe. I will start by searching the keyword cafe and focus on events taking place in the near future. I have found an event at 1PM called "Meeting with Daniel Kim at Local Cafe". I can assume this is the referenced event, as it contains the keyword provided by the user. I will call out the location of this event to the user, as requested. \n',
            success_conditions=[
                {
                    "input_text": '1. The location of calendar event "Meeting with Daniel Kim at Local Cafe" is displayed and read out to the user. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent tries to look up the meeting information in the calendar
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
                # Milestone 1 – The retrieved calendar event includes the correct name and location
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
                                                "value": "Meeting with Daniel Kim at Local Cafe",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Local Cafe, Orchard County",
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
                # Milestone 2 – Agent tells the user the location of the café
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
                                        ("Local Cafe", "Local Cafe, Orchard County")
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
            name="EMILY_ROSE_18_365a76f7-7260-41fe-8cf6-6bc8b76b8620_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T11:20:00-08:00",
            is_read_time="2024-12-14T11:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know the location of where you're meeting Daniel in order to get a good parking space. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where am I meeting Daniel Kim?",
                },
            ],
            reasoning="Right so, the user is looking for the location of where they're meeting 'Daniel Kim'. From checking the user's contacts I see no one under that name. Next, I will check the user's calendar and can see an event matching, scheduled for today, 14 December 2024 at 12:00 titled 'Meeting with Daniel Kim at Local Cafe' with Daniel Kim' with Daniel Kim as an attendee. This is the event the user is requesting the location information. The location has been added as 'Local Cafe, Orchard County'. I can display this to the user.",
            success_conditions=[
                {
                    "input_text": "1. The location of 'Meeting with Daniel Kim at Local Cafe', 'Local Cafe, Orchard County', which is scheduled for 14 December 2024 from 12:00 to 13:00 is displayed to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent queries the calendar to locate the meeting
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
                # Milestone 1 – Confirm that the desired meeting with Daniel Kim was found
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
                                                "value": "Meeting with Daniel Kim at Local Cafe",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Local Cafe",
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
                # Milestone 2 – Agent tells the user the correct meeting location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Local Cafe",  # key phrase that must appear
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
                (0, 1),  # calendar query → verify meeting found
                (1, 2),  # meeting found → agent informs user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_18_6a8ee231-b6db-4829-9652-32508218adfe_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-14T14:00:00-08:00",
            is_read_time="2024-12-14T14:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to reply to the last email from Daniel Kim. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to my most recently received email with "Thanks for all the help Daniel".',
                },
            ],
            reasoning="The user wants to reply to their most recently received email. I'll have to search through the user's inbox to find what that could be ... The most recent email was received at 13:00 today from Daniel Kim, called \"Confirmation of Menu and Resources for Upcoming Events\", which matches the name mentioned by the user. I'll take it that this is the person the user wants to reply to.",
            success_conditions=[
                {
                    "input_text": '1. A message saying "Thanks for all the help Daniel" is sent to Daniel Kim via email at 14:00 on 14 December 2024. ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=["get_all_emails", "search_emails", "send_email"],
            milestones=[
                # Milestone 0 – Agent looks through the inbox to find the most recent email
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
                # Milestone 1 – Confirm that an email from Daniel Kim was indeed surfaced
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
                                                "value": "daniel.kim@localcafe.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Confirmation of Menu and Resources for Upcoming Events",
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
                # Milestone 2 – A reply email was sent to Daniel Kim containing the required phrase at ~14:00
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["daniel.kim@localcafe.com"]
                                    ],
                                    "body": "Thanks for all the help Daniel",
                                    "creation_datetime_iso": "2024-12-14T14:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_exact_match_similarity,
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
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
    ]
