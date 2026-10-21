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
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_similarity,
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


def get_TAG_THEO_APPLESEED_pilot_plot_1(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="THEO_APPLESEED_1_bce9caf8-f434-45f2-8e01-9006e31c66bc_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
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
                        "You want to delete your follow-up sync meeting at 11:00 as you have a family emergency and can no longer make it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you delete the event titled Follow-up Sync with Michelle and Dawei at 11:00 from my calendar",
                },
            ],
            reasoning='The user wants me to delete their event named "Follow-up Sync with Michelle and Dawei" at 11:00. First I need to find it in the user\'s calendar. Ok I found one matching that event name taking place on July 29th at 11:00-12:00.  Now that I have found it I can delete it and inform the user.',
            success_conditions=[
                {
                    "input_text": '1. The event named "Follow-up Sync with Michelle and Dawei" on July 29th  at 11:00-12:00 is deleted. ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (information-retrieval step)
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
                # Milestone 1 – Confirm the correct follow-up sync event was returned from the search
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
                                                "value": "Follow-up Sync with Michelle and Dawei",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T11:00:00-07:00",
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
                # Milestone 2 – Verify the event has been removed from the calendar database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Follow-up Sync with Michelle and Dawei",
                                    "start_datetime_iso": "2024-07-29T11:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar search → verify correct event found
                (1, 2),  # Event identified → verify deletion
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_0ae9c071-a14d-4b7c-9452-0c9f4c274226_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-28T21:45:00-07:00",
            is_read_time="2024-07-28T21:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know if you have specifically mentioned the location for the follow-up meeting directly in the email with Michelle and Dawei. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I mention the location of our sync in my email? Yes or No.",
                },
            ],
            reasoning='The user wants to know if they mentioned the "location of our sync" in their email.\n\nOkay, firstly, I need to go to the user\'s Mail to see if they have sent any emails that contain "sync" in the subject.\n\nGreat, I can see they sent an email on July 22nd, 2024 at 11:05 named "Follow-up Sync Scheduled for July 29" to "michelle.barnes@example.com" and "dawei.shen@example.com". This must be what they\'re referring to in their request, as it\'s the only email that contains the word "sync".\n\nThe email says "Hello Michelle and Dawei, Following our stand-up meeting today, I\'ve scheduled a follow-up sync for us on July 29 at 11 am to discuss our project in more detail. Please find the calendar invite attached. Best, Theo". Even though there\'s a calendar invite .ics file attached, there\'s no direct mention of the event location in the body of the email. That means the user did not mention the location. I will reply "No" to the user.',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that they did not mention the location of the event named "Follow-up Sync with Michelle and Dawei" scheduled for 29 July 2024 at 11:00-12:00 in the text of the email that they sent to "michelle.barnes@example.com" and "dawei.shen@example.com" with the subject "Follow-up Sync Scheduled for July 29" on 22 July 2024 at 11:05.',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. There're no direct mention of the location in the email, so assistant will reply 'No' to the user.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – Agent used an email-retrieval tool
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
                # Milestone 1 – The retrieved email is the correct follow-up sync message
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
                                                "value": "Follow-up Sync Scheduled for July 29",
                                                "partial": False,
                                            },
                                            "sender_address": {
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
                # Milestone 2 – Agent answers the user with “No”
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
                (0, 1),  # Retrieval tool call → confirm correct email found
                (1, 2),  # Email confirmed → respond to user
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_a16b0e19-6f9e-4826-8343-89fabb590fc6_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-19T17:30:00-07:00",
            is_read_time="2024-07-19T17:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to check you have entered the right details into your Calendar for your meeting on Monday so will ask for the location. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where is my Monday Stand-up Meeting taking place?",
                },
            ],
            reasoning="The user is asking for the location of their Monday Stand-up Meeting. First I will check their Calendar. Looks like they have an event called Monday Stand-up Meeting at 10:00-10:30 on 22 July 2024 so now I will look at the location. Looks like it is set for Conference Room A, Innovative Tech Solutions so I will tell the user this. ",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that the event named 'Monday Stand-up Meeting' at 10:00-10:30 on 22 July 2024 is taking place at the location 'Conference Room A, Innovative Tech Solutions'.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent looks in the calendar for the Monday Stand-up Meeting
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
                # Milestone 1 – Verify the correct calendar event (Monday Stand-up) was returned in the tool output
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
                                                "value": "Monday Stand-up Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-22T10:00:00-07:00",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Conference Room A",
                                                "partial": True,  # allow the full string with company name
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
                            reference_milestone_node_index=0,  # depend on tool output checked in milestone 0
                        )
                    ],
                ),
                # Milestone 2 – The agent tells the user where the meeting is
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Conference Room A",
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
                (0, 1),  # Tool call → verify correct event returned
                (1, 2),  # Correct event info → user informed
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_ed61ed52-3949-4965-b278-7dea2061e045_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T09:45:00-07:00",
            is_read_time="2024-07-22T09:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You are on your way in to work for your Monday stand-up meeting, but something has come up that is going to delay your arrival, so you need to send a message to your boss. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text the one in charge of the Monday Stand-up Meeting that I'll be late to the meeting",
                },
            ],
            reasoning='The user wants to send a text, but I need to figure out who the recipient will be because they just referred to them as "the one in charge of the Monday Stand-up Meeting." I\'ll start by looking at the calendar for the details of the meeting they\'re talking about. I see an event named "Monday Stand-up Meeting" today 22 July 2024 from 10:00-10:30. I see Kevin Chen, Michelle Barnes, and Dawei Shen listed as invitees. Now I need to determine who among these people the user would consider "in charge" of the meeting. I see Dawei and Michelle listed as the user\'s coworkers in their contacts, and Kevin is listed as the user\'s manager. The event notes describe it as a "Regular weekly stand-up meeting to discuss ongoing projects and tasks for the week." I assume the manager would be the one most interested in staying up-to-date on everyone\'s projects and therefore would be the one the user considers "in charge" of the meeting. That means the user wants to text Kevin Chen. So I\'ll craft the text message "I\'ll be late to the meeting" to send to the user\'s manager, Kevin Chen.',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The text message "I\'ll be late to the meeting" is sent to Kevin Chen.',
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_message",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up a contact (Kevin) in the contacts database
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
                # Milestone 1 – Confirm that Kevin Chen’s contact entry was returned from the previous tool call
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
                                                "value": "Kevin Chen",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9103",
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
                # Milestone 2 – A new outgoing message is created that tells Kevin the user will be late
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Kevin’s phone number must be among the participants
                                    "participants_addresses": [
                                        [("kevin.chen@example.com", "1234-5678-9103")]
                                    ],
                                    # Message body must indicate lateness
                                    "content": [("late", "I'll be late", "delay")],
                                    "creation_datetime_iso": "2024-07-22T09:45:00-07:00",
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
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.EMAIL,
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
            name="THEO_APPLESEED_1_a16b0e19-6f9e-4826-8343-89fabb590fc6_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-19T17:30:00-07:00",
            is_read_time="2024-07-19T17:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to check you have entered the right details into your Calendar for your meeting on Monday so will ask for the location. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where is my meeting on Monday morning?",
                },
            ],
            reasoning='The user wants to know the location of their meeting on Monday morning. The closest Monday to today, 19 July 2024, is Monday 22 July 2024 so first I should check the user\'s Calendar to see how many meetings they have on that Monday morning. Looks like they only have the one, the "Monday Stand-up Meeting" at 10:00-10:30 on 22 July 2024, so this must be the one the user meant. Looking at the details for it, the location is set for Conference Room A, Innovative Tech Solutions so I will tell the user this. ',
            success_conditions=[
                {
                    "input_text": "1. The user is informed that the event named 'Monday Stand-up Meeting' at 10:00-10:30 on 22 July 2024 is taking place at the location 'Conference Room A, Innovative Tech Solutions'.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent looks up Monday’s meeting in the calendar
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
                # Milestone 1 – Confirm the correct Monday Stand-up event was returned
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
                                                "value": "Monday Stand-up Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-22T10:00:00-07:00",
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
                # Milestone 2 – The user is told the correct location (“Conference Room A”)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Conference Room A",
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
                (0, 1),  # calendar lookup → confirm correct event found
                (1, 2),  # confirmed event → reply to user with location
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_ed61ed52-3949-4965-b278-7dea2061e045_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T09:45:00-07:00",
            is_read_time="2024-07-22T09:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You are on your way in to work for your Monday stand-up meeting, but something has come up that is going to delay your arrival, so you need to send a message to your boss. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text Kevin I'll be late to the meeting",
                },
            ],
            reasoning='The user wants to text Kevin "I\'ll be late to the meeting". I need to check the user\'s contacts for someone named "Kevin" - I found only one contact called Kevin Chen. Therefore, this must be the correct person. With the user\'s confirmation, I will send the message as requested.',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message "I\'ll be late to the meeting" is sent to Kevin Chen.',
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_message",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up Kevin in the contacts
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
                # Milestone 1 – The returned contact list includes Kevin Chen
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
                                                "value": "Kevin Chen",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9103",
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
                # Milestone 2 – A text message is sent to Kevin saying the user will be late
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
                                                "1234-5678-9103",
                                                "kevin.chen@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "be late",
                                    "creation_datetime_iso": "2024-07-22T09:45:00-07:00",
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
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.EMAIL,
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
            name="THEO_APPLESEED_1_0ae9c071-a14d-4b7c-9452-0c9f4c274226_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-28T21:45:00-07:00",
            is_read_time="2024-07-28T21:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know if you have specifically mentioned the location for the follow-up meeting directly in the email with Michelle and Dawei. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to know if I mentioned the location of the follow-up sync in my email to my co-workers? Yes or No.",
                },
            ],
            reasoning='The user wants to know if they mentioned the "location of the follow-up sync" in their email to their "co-workers".\n\nOkay, first of all, I need to go to the user\'s Mail to see if they have sent any emails that correspond to the above description.\n\nGreat, I can see they sent an email on July 22nd, 2024 at 11:05:00 named "Follow-up Sync Scheduled for July 29". It was sent to Michelle Barnes and Dawei Shen, who I can also see are the user\'s co-workers.\n\nIn the content, there\'s no direct mention of the location, only a .ics file of the calendar invite which I cannot read. The text says "Hello Michelle and Dawei, Following our stand-up meeting today, I\'ve scheduled a follow-up sync for us on July 29 at 11 am to discuss our project in more detail. Please find the calendar invite attached. Best, Theo". None of the text mentions the location of the meeting. I will reply \'No\' to the user. \n\n',
            success_conditions=[
                {
                    "input_text": "1. The user is informed that they did not mention the location of the event named 'Follow-up Sync with Michelle and Dawei' scheduled for 29 July 2024 at 11:00-12:00 in the text of the email that they sent to michelle.barnes@example.com and dawei.shen@example.com with the subject 'Follow-up Sync Scheduled for July 29' on 22 July 2024 at 11:05.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. There're no direct mention of the location in the email, so assistant will reply 'No' to the user.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – The agent looks through the email database
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
                # Milestone 1 – The expected follow-up email is present in the tool’s result
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
                                                "value": "Follow-up Sync Scheduled for July 29",
                                                "partial": False,
                                            },
                                            # Subject match is enough to prove the correct email was surfaced
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
                # Milestone 2 – The assistant answers the user with “No”
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
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_bce9caf8-f434-45f2-8e01-9006e31c66bc_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
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
                        "You want to delete your follow-up sync meeting at 11:00 as you have a family emergency and can no longer make it. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete the follow-up sync meeting later",
                },
            ],
            reasoning='The user wants me to delete their follow-up sync meeting later. First I need to find it in the user\'s calendar. Ok I found an event titled "Follow-up Sync with Michelle and Dawei" on July 29th at 11:00-12:00. That must be the event they are referring to.  Now that I have found it I can delete it and inform the user.',
            success_conditions=[
                {
                    "input_text": '1. The event named "Follow-up Sync with Michelle and Dawei" on July 29th  at 11:00-12:00 is deleted. ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – The agent queries the calendar to locate the follow-up sync
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
                # Milestone 1 – The expected event is returned from the search in Milestone 0
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
                                                "value": "Follow-up Sync with Michelle and Dawei",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T11:00:00-07:00",
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
                # Milestone 2 – The event has been removed from the calendar database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Follow-up Sync with Michelle and Dawei",
                                    "start_datetime_iso": "2024-07-29T11:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.MESSAGING,
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
            name="THEO_APPLESEED_1_cdd9bb4e-709b-410b-9af4-45253c32359a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T09:50:00-07:00",
            is_read_time="2024-07-22T09:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to see what your schedule is like next Monday before you send out an invite for a follow-up sync with Michelle and Dawei "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What do I have going on next Monday? ",
                },
            ],
            reasoning="The user wants to know what they have scheduled for next Monday, so I will search calendar for events taking place on Monday 29th of July 2024. As of right now, 9:50 on 22 July, the user has no events scheduled for 29 July. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The user is informed that there are no events scheduled on their calendar on Monday 29 July 2024.",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent queries the calendar to find events for next Monday
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
                # Milestone 1 – The agent tells the user they have nothing scheduled that day
                Milestone(
                    snapshot_constraints=[
                        # Confirms the reply states the schedule is clear
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "nothing",
                                            "no events",
                                            "free",
                                            "open",
                                            "clear",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                            },
                        ),
                        # Confirms the reply references the correct day/date
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "Monday",
                                            "July 29",
                                            "29 July",
                                            "29th",
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
                (0, 1),  # Calendar search precedes the user-facing answer
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_0a22abe3-916a-4fde-8b4c-54fe9975cd40_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T10:00:00-07:00",
            is_read_time="2024-07-26T10:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send an email to Dawei and Michelle letting them know you won't be able to make it to the follow-up sync you scheduled for the 29th of July. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send Michelle Barnes and Dawei Shen the following message by email: Hey guys, my aunt Cassie's birthday party is on the 29th so I won't be able to make it to that meeting I scheduled for us then. Let me know how it goes though. -Theo. Set the subject as 'Reschedule.' ",
                },
            ],
            reasoning='The user wants to send an email to Michelle Barnes and Dawei Shen with the subject "Reschedule" saying "Hey guys, my aunt Cassie\'s birthday party is on the 29th so I won\'t be able to make it to that meeting I scheduled for us then. Let me know how it goes though. -Theo". I shall do so and present it to user for user\'s approbation. ',
            success_conditions=[
                {
                    "input_text": "1. An email is sent to both Dawei Shen and Michelle Barnes with the subject 'Reschedule', saying 'Hey guys, my aunt Cassie's birthday party is on the 29th so I won't be able to make it to that meeting I scheduled for us then. Let me know how it goes though. -Theo.' ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_email"],
            milestones=[
                # Milestone 0 – the agent looks up contact information
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
                # Milestone 1 – a single email is sent to both Michelle Barnes and Dawei Shen with the correct message body
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        [
                                            "michelle.barnes@example.com",
                                            "dawei.shen@example.com",
                                        ]
                                    ],
                                    "status": "sent",
                                    "body": "my aunt Cassie",  # key phrase expected in body,
                                    "creation_datetime_iso": "2024-07-26T10:00:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_0a22abe3-916a-4fde-8b4c-54fe9975cd40_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "email",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T10:00:00-07:00",
            is_read_time="2024-07-26T10:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send an email to Dawei and Michelle letting them know you won't be able to make it to the follow-up sync you scheduled for the 29th of July. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell the attendees of the 29 July follow-up sync the following by electronic post, with the subject 'Reschedule': Hey guys, my aunt Cassie's birthday is on the 29th so I won't be able to make it to that meeting I scheduled for us then. Let me know how it goes though. -Theo. ",
                },
            ],
            reasoning='The user wants to send an email to the attendees of an event on 29 July. I\'ll check the calendar for events on that date with "follow-up sync" in the name. I see one event, "Follow-up Sync with Michelle and Dawei," scheduled for 29 July from 11:00-12:00 with the attendees Dawei Shen and Michelle Barnes. I shall compose an email to them with the subject "Reschedule" for the user\'s approval. The user wants it to say "Hey guys, my aunt Cassie\'s birthday party is on the 29th so I won\'t be able to make it to that meeting I scheduled for us then. Let me know how it goes though. -Theo". I shall wrire that and present it to user for user\'s approbation. ',
            success_conditions=[
                {
                    "input_text": "1. An email is sent to both Dawei Shen and Michelle Barnes with the subject 'Reschedule', saying 'Hey guys, my aunt Cassie's birthday is on the 29th so I won't be able to make it to that meeting I scheduled for us then. Let me know how it goes though. -Theo.' ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_email",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – agent looks up people to email (contacts or calendar)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    "tool_trace": "",  # verify one of the allowed lookup tools was invoked
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
                # Milestone 1 – calendar attendees was retrieved
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
                                                "value": "Follow-up Sync with Michelle and Dawei",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T11:00:00",
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
                # Milestone 2 – email was sent to both recipients with correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        [
                                            "dawei.shen@example.com",
                                            "michelle.barnes@example.com",
                                        ]
                                    ],
                                    "status": "sent",
                                    "body": "aunt Cassie",  # substring to confirm correct message,
                                    "creation_datetime_iso": "2024-07-26T10:00:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare to initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox chatter
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_873a34c3-ac43-4793-9b39-092db147157f_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-28T21:45:00-07:00",
            is_read_time="2024-07-28T21:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know if you included the location for the follow-up sync with Michelle and Dawei event. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I mention the location of our sync in my email?",
                },
            ],
            reasoning='The user wants to know if they mentioned the "location of our sync" in their email.\n\nOkay, firstly, I need to go to the user\'s Mail to see if they have sent any emails that correspond to the above description.\n\nGreat, I can see they sent an email on July 22nd, 2024 at 11:05 named "Follow-up Sync Scheduled for July 29". This must be what they\'re referring to in their request, as it\'s the only email that contains those words.\n\nI will present this email to the user now.',
            success_conditions=[
                {
                    "input_text": '1. The user is presented with the email named "Follow-up Sync Scheduled for July 29", sent to "michelle.barnes@example.com" and "dawei.shen@example.com" on July 22nd, 2024 at 11:05.',
                    "statefullness": "Stateless",
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
                    ]
                ),
                # Milestone 1 – The retrieved result list contains the expected follow-up email
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
                                                "value": "Follow-up Sync Scheduled for July 29",
                                                "partial": False,
                                            },
                                            "sender_address": {
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
                    ]
                ),
                # Milestone 2 – Agent presents the email (or its key details) back to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Follow-up Sync Scheduled for July 29",
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
                (0, 1),  # tool invocation → verify email retrieved
                (1, 2),  # email retrieved → user is shown the email
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_0f843e38-240f-4a37-ab98-d402d3da94cc_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T14:00:00-07:00",
            is_read_time="2024-07-25T14:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to cancel next Monday's morning meetings because you will be in the hospital visiting your friend who just had a baby. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I can't make any meetings Monday at 11am. Can you remove anything scheduled for that time from my calendar.",
                },
            ],
            reasoning='The user wants to delete any calendar events that occur next Monday at 11 am. The next Monday in the calendar is July 29th 2024. I can see an event named "Follow-up Sync with Michelle and Dawei" scheduled for that date from 11:00-12:00.  The user said they can\'t make any meetings at 11:00 so I will delete it from the calendar.',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. The event 'Follow-up Sync with Michelle and Dawei' that is set to take place July 29th 2024 at 11:00-12:00 is deleted from the calendar.",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – The agent inspects the calendar to locate the event
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
                # Milestone 1 – The follow-up sync on July 29 11:00 is removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Follow-up Sync with Michelle and Dawei",
                                    "start_datetime_iso": "2024-07-29T11:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # calendar inspection precedes deletion
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_b2df2f5c-29e2-420c-afd7-4d3a089c5f4b_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "email",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T11:55:00-07:00",
            is_read_time="2024-07-24T11:55:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You're not sure whether you remembered to send a follow-up sync email to Michelle and Dawei after your stand-up meeting on Monday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Have I sent an email about the meeting I had on Monday to my coworkers who attended?",
                },
            ],
            reasoning="The user wants to know whether they emailed their coworkers who attended a meeting they had on Monday. First I'll need to figure out which meeting they're referring to.\n\nI found one event on the most recent Monday before today: 22 July 2024. The meeting is \"Monday Stand-up Meeting\" from 10:00-10:30. Kevin Chen, Michelle Barnes, and Dawei Shen are listed as participants. Now I'll check the user's contacts to figure out which of these are coworkers.\n\nIt seems that Michelle Barnes and Dawei Shen are the user's coworkers and Kevin Chen is the user's manager. The user wants to know if they emailed their coworkers, so I'll now check whether the user emailed Dawei and Michelle about the meeting by looking at their sent emails.\n\nI found an email with subject line \"Follow-up Sync Scheduled for July 29\" that was sent to Michelle Barnes and Dawei Shen at 11:05 on 22 July 2024. Checking the contents of this email, I can see that it references \"our stand-up meeting today\". Therefore, 'today' must be referring to 2024-07-22. The email even has an attached file named \"Follow-up Sync Calendar Invite.ics\" that seems to be a calendar invite. This must be the email the user is looking for.\n\nGreat, now I can go ahead and inform the user that they sent the referenced email.",
            success_conditions=[
                {
                    "input_text": '1. User is informed that they sent an email with the subject "Follow-up Sync Scheduled for July 29" to Michelle Barnes and Dawei Shen on 2024-07-22 at 11:05.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "get_all_calendars",
                "search_calendar_events",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent looks through the email database
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
                # Milestone 1 – The retrieved email is the follow-up sync sent to Michelle and Dawei
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
                                                "value": "Follow-up Sync Scheduled for July 29",
                                                "partial": False,
                                            },
                                            "recipients_addresses": {
                                                "value": "michelle.barnes@example.com",
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
                # Milestone 2 – The agent tells the user they already sent the email
                Milestone(
                    snapshot_constraints=[
                        # Subject mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Follow-up Sync",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Michelle mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Michelle",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Dawei mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Dawei",
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
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_67c70715-2405-4a8b-a9bc-41a506048251_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T09:55:00-07:00",
            is_read_time="2024-07-22T09:55:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to message all attendees of the meeting Monday Stand-up Meeting together to ask them if they'd like a sit-down meeting instead. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to all attendees of the Monday Stand-up Meeting to ask them if they'd like a sit-down meeting instead: 'Hey how about we make this meeting a sit-down meeting instead?'",
                },
            ],
            reasoning="The user wants to message all the attendees of the meeting Monday Stand-up Meeting. \nLooking at the calendar, I can see there is an event named Monday Stand-up Meeting scheduled for this morning 22 July 2024 at 10:00-10:30. First I'll check all the attendees of the meeting. The attendees are Michelle Barnes, Kevin Chen and Dawei Shen. They are all featured in the user's contacts so I'll send a message to them that says what the user wanted 'Hey how about we make this meeting a sit-down meeting instead?'.",
            success_conditions=[
                {
                    "input_text": '1. A group message is sent to Kevin Chen, Michelle Barnes, and Dawei Shen all in one thread saying "Hey how about we make this meeting a sit-down meeting instead?"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "get_all_contacts",
                "search_contacts",
                "send_message",
            ],
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
                # Milestone 1 – Monday Stand-up Meeting Found
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
                                                "value": "Monday Stand-up Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-22T10:00:00-07:00",
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
                # Milestone 2 – A group message has been sent to all the attendees
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
                                                "michelle.barnes@example.com",
                                                "1234-5678-9105",
                                            ),
                                            (
                                                "dawei.shen@example.com",
                                                "1234-5678-9106",
                                            ),
                                            (
                                                "kevin.chen@example.com",
                                                "1234-5678-9103",
                                            ),
                                        ]
                                    ],
                                    "content": "sit-down meeting",
                                    "creation_datetime_iso": "2024-07-22T09:55:00-07:00",
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
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_aaa0878a-2a69-4f92-8b90-55c3734c682f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T11:10:00-07:00",
            is_read_time="2024-07-22T11:10:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You're planning a one-on-one meeting with Stefan after the stand-up meeting this morning, and you want to book it in your calendar for this Wednesday afternoon. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Help me to make an event called "One-on-one with Stefan" for Wednesday 24th July 2024 at 14:00 and add him as an attendee',
                },
            ],
            reasoning='The user wants me to make an event called "One-on-one with Stefan" for Wednesday 24th July 2024 at 14:00. Checking the user\'s calendar, it doesn\'t look like there are any scheduling conflicts. The user also asked me to add "him" as an attendee, so I need to figure out who that refers to. The event title has the name "Stefan" in it, and if I check the user\'s contacts, I found one Stefan Mustermann who is the user\'s coworker. Since this is the only Stefan I can find, and since the event is about a work meeting, this seems like it is the correct Stefan. With the user\'s confirmation, I can create the event "One-on-one with Stefan" on Wednesday 24th July 2024 at 14:00 with Stefan Mustermann as an attendee\n',
            success_conditions=[
                {
                    "input_text": '1. A new event named "One-on-one with Stefan" is scheduled for Wednesday 24th July 2024 at 14:00 with Stefan Mustermann as an attendee.',
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
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent tries to find Stefan in the Contacts database
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
                # Milestone 1 – Confirm the tool call in Milestone 0 actually returned Stefan Mustermann
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
                                                "value": "Stefan Mustermann",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "stefan.mustermann@example.com",
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
                # Milestone 2 – The new one-on-one event with Stefan has been added to the Calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "One-on-one with Stefan",
                                    "start_datetime_iso": "2024-07-24T14:00:00",
                                    "attendees_names": [["Stefan Mustermann"]],
                                    "creation_datetime_iso": "2024-07-22T11:10:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against the initial calendar snapshot
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact search → confirm Stefan retrieved
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_ed61ed52-3949-4965-b278-7dea2061e045_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T09:45:00-07:00",
            is_read_time="2024-07-22T09:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You are on your way in to work for your Monday stand-up meeting, but something has come up that is going to delay your arrival, so you need to send a message to your boss. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text the one in charge of the meeting that starts in 15 minutes that I'll be late to the meeting",
                },
            ],
            reasoning='The user wants to send a text, but I need to figure out who the recipient will be because they just referred to them as "the one in charge of the meeting that starts in 15 minutes". I\'ll start by trying to find the event the user is talking about. 15 minutes from now, 9:45, is 10:00. I see an event named "Monday Stand-up Meeting" today that starts at that time. Now I\'ll look at the details of that event to learn more. I see Kevin Chen, Michelle Barnes, and Dawei Shen listed as invitees. Now I need to determine who among these people the user would consider "in charge" of the meeting. I see Dawei and Michelle listed as the user\'s coworkers in their contacts, and Kevin is listed as the user\'s manager. The event notes describe it as a "Regular weekly stand-up meeting to discuss ongoing projects and tasks for the week." I assume the manager would be the one most interested in staying up-to-date on everyone\'s projects and therefore would be the one the user considers "in charge" of the meeting. So I\'ll craft the text message "I\'ll be late to the meeting" to the user\'s manager, Kevin Chen.',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The message with content like "I\'ll be late to the meeting" is sent to Kevin Chen.',
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_message",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the imminent meeting
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
                # Milestone 1 – The expected stand-up meeting is found from the tool call in Milestone 0
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
                                                "value": "Monday Stand-up Meeting",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-22T10:00:00-07:00",
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
                # Milestone 2 – A text message to Kevin Chen indicating lateness has been sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least Kevin’s address must be in the conversation participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9103",  # Kevin’s phone
                                                "kevin.chen@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "be late to",
                                    "creation_datetime_iso": "2024-07-22T09:45:00-07:00",
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
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # meeting lookup → confirm meeting details
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_2ef5ed5e-eeee-4376-8820-b62861bf0a72_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T11:05:00-07:00",
            is_read_time="2024-07-22T11:05:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know if you sent the follow-up email after your stand-up meeting to Dawei. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I send Dawei the follow-up email? Yes or no.",
                },
            ],
            reasoning="The user wants to know if they sent the follow-up email after their stand-up meeting to Dawei. I wonder what email they're referring to. I'll check their emails for something mentioning a follow-up. I see one email sent on July 22nd at 11:05 with the subject 'Follow-up Sync Scheduled for July 29' so I assume it is that one. Okay,  I check the recipients and see that Dawei Shen is listed so I'll tell the user yes, he was sent the message. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The user is informed with yes, that Dawei Shen was a recipient of the email with the subject 'Follow-up Sync Scheduled for July 29' sent at 11:05 on 22 July 2024. ",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – The agent looks through the mailbox for the follow-up email
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
                # Milestone 1 – The email that went to Dawei on 22-Jul-2024 11:05 is found in the result list
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
                                            # Subject substring is enough, do not require exact match
                                            "subject": {
                                                "value": "Follow-up Sync Scheduled",
                                                "partial": True,
                                            },
                                            # Ensure Dawei is one of the recipients
                                            "recipients_addresses": {
                                                "value": ["dawei.shen@example.com"],
                                                "partial": True,
                                            },
                                            # Confirm the timestamp to avoid matching unrelated email
                                            "creation_datetime_iso": {
                                                "value": "2024-07-22T11:05:00-07:00",
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
                            reference_milestone_node_index=0,  # parse the result of Milestone-0
                        ),
                    ],
                ),
                # Milestone 2 – The agent tells the user that Dawei received the follow-up email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "yes",  # key phrase to be found
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_similarity,  # just make sure the answer mentions Dawei / confirmation
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
            name="THEO_APPLESEED_1_b2df2f5c-29e2-420c-afd7-4d3a089c5f4b_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_low",
                "email",
                "calendar",
                "contact",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T11:55:00-07:00",
            is_read_time="2024-07-24T11:55:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You're not sure whether you remembered to send a follow-up sync email to Michelle and Dawei after your stand-up meeting on Monday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Check my sent emails for one to Michelle and Dawei about our Monday stand-up meeting.",
                },
            ],
            reasoning="The user wants to check their sent emails to see if there is one about their Monday stand-up meeting sent to Michelle and Dawei.\n\nI found one email sent to Michelle Barnes and Dawei Shen at 11:05 on 2024-07-22 with subject line Follow-up Sync Scheduled for July 29. Checking the contents of this email, I can see that it references \"our stand-up meeting today\". There is an event on the user's calendar on the same day named \"Monday Stand-up Meeting\" happening on 2024-07-22 at 10:00. Therefore, 'today' must be referring to 2024-07-22. Hence, I can determine that this email is the one the user was looking for.\n\nI'm going to let them know that they did send the email.",
            success_conditions=[
                {
                    "input_text": '1. User is informed that they sent a "Follow-up Sync Scheduled for July 29" email to Michelle Barnes and Dawei Shen on 2024-07-22 at 11:05.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_emails",
                "search_emails",
                "get_all_calendars",
                "search_calendar_events",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looks through sent emails
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
                # Milestone 1 – The desired email is returned in the tool output from Milestone 0
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
                                                "value": "Follow-up Sync Scheduled for July 29",
                                                "partial": False,
                                            },
                                            "recipients_addresses": {
                                                "value": [
                                                    "michelle.barnes@example.com",
                                                    "dawei.shen@example.com",
                                                ],
                                                "partial": True,  # list containment
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-22T11:05:00-07:00",
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
                # Milestone 2 – Agent informs the user about having sent that email
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Follow-up Sync",
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
                (0, 1),  # tool invocation → confirm email found
                (1, 2),  # email confirmed → inform user
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_75cd4244-7ca7-4378-b403-43c85981b900_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-15T09:45:00-07:00",
            is_read_time="2024-07-15T09:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You are on your way in to work for your Monday stand-up meeting, but something has come up that is going to delay your arrival, so you need to send a message to Kevin Chen. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell Kevin I'll be late to the meeting",
                },
            ],
            reasoning="The user wants to message Kevin saying \"I'll be late to the meeting\". I need to check the user's contacts for someone named \"Kevin\" - I found one contact called Kevin Chen. Additionally, there is a meeting in 15 minutes in the user's calendar data for today, and one of the participants is Kevin Chen. Therefore, this must be the correct person. With the user's confirmation, I will send the message as requested.",
            success_conditions=[
                {
                    "input_text": '1. The user\'s contacts are checked for "Kevin Chen".',
                    "statefullness": "Stateless",
                },
                {
                    "statefullness": "Stateful",
                    "input_text": '2. The message "I\'ll be late to the meeting" is sent to Kevin Chen.',
                },
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up Kevin in the contacts
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
                # Milestone 1 – Verify Kevin Chen appears in the result from Milestone 0
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
                                                "value": "Kevin Chen",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "kevin.chen@example.com",
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
                # Milestone 2 – A new message is sent to Kevin indicating the user will be late
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
                                                "kevin.chen@example.com",
                                                "1234-5678-9103",
                                            )
                                        ]
                                    ],
                                    "content": "be late to the meeting",
                                    "creation_datetime_iso": "2024-07-15T09:45:00-07:00",
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
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.EMAIL,
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
            name="THEO_APPLESEED_1_0f843e38-240f-4a37-ab98-d402d3da94cc_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-25T14:00:00-07:00",
            is_read_time="2024-07-25T14:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to cancel next Monday's stand up meeting because you will be in the hospital visiting a friend's baby. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you delete my event \"Follow-up Sync with Michelle and Dawei\". I can't go cause I'll be visiting my friend's new baby.",
                },
            ],
            reasoning='The user wishes to remove an event from the calendar. The event is called "Follow-up Sync with Michelle and Dawei". I must check their calendar for an event with this name. I found an event with this name on July 29th 2024 at 11:00. I\'ll delete this event. ',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The event "Follow-up Sync with Michelle and Dawei" that is set to take place July 29th 2024 at 11:00 is deleted from the calendar.',
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "remove_calendar_event",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – The agent tries to fetch calendar data (search or list)
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
                # Milestone 1 – Confirm that the correct event was returned by the previous tool call
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
                                                "value": "Follow-up Sync with Michelle and Dawei",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-29T11:00:00-07:00",
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
                # Milestone 2 – Verify the event is removed from the CALENDAR database
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Follow-up Sync with Michelle and Dawei",
                                    "start_datetime_iso": "2024-07-29T11:00:00-07:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare to initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.MESSAGING,
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
    ]
