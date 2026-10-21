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
    column_word_contains_any_similarity,
    contains_presence_similarity,
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


def get_TAG_DAWEI_SHEN_pilot_plot_8(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="DAWEI_SHEN_8_53df768b-3924-4ca4-9a98-631282d87e9c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "calendar",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:05:00-08:00",
            is_read_time="2024-12-05T17:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to add your upcoming theatre night to your calendar, making sure the friend you're going with is listed as an attendee.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Create a new Calendar event called Theater Night with the friend I'm supposed to be going with on Monday at 19:00-22:00. ",
                },
            ],
            reasoning="The user wants to create a new calendar event called theatre Night with the friend they're supposed to be going with, on Monday the 9th from 19:00 to 22:00. I wonder who the friend they're supposed to be going with is. I should search messages for a message thread mentioning a theater night. I see the user has a recent message thread with Jess Zimmer that talks about  plans for theater night. This must be the friend the user means. \nI should check to see if the user has any other events happening at the same time that could be conflicting. Okay, I don't see any other events happening at that time. I'll create the calendar event at that time. I can tell the user that I scheduled the \"Theater Night\" event with Jess Zimmer on Monday the 9th at 19:00-22:00.",
            success_conditions=[
                {
                    "input_text": '1. A new calendar event is created called "Theatre Night with Jess" on Monday the 9th of December 2024 from 19:00-22:00. ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_messages",
                "get_all_messages",
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent looks up who the friend / theater companion is via messages or WhatsApp
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Confirms that Jess / theater night conversation was found (i.e., identifies the friend)
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
                                        # We just need to see that a thread mentioning theater night with Jess exists
                                        match_conditions={
                                            "conversation_name": {
                                                "value": "Jess Zimmer",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "theater night",
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
                # Milestone 2 – Calendar event created for Theater Night with Jess on Monday Dec 9, 2024, 19:00–22:00
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Theater Night",
                                    "start_datetime_iso": "2024-12-09T19:00:00-08:00",
                                    "end_datetime_iso": "2024-12-09T22:00:00-08:00",
                                    # Attendees_names is optional in many schemas; if present we want Jess included
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-05T17:05:00-08:00",
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
            milestone_edge_list=[
                (0, 1),  # Find theater night conversation → confirm Jess as the friend
                (1, 2),  # After identifying Jess, create the calendar event
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_63e4c469-4545-46de-9f1c-a8cc9e139315_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "messaging",
                "whatsapp_messaging",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T20:14:00-08:00",
            is_read_time="2024-12-11T20:14:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You and your girlfriend hung out last week and got in a bit of a disagreement. You're thinking of texting her because you haven't spoken since then, but you first need to see how many days it's been since you last messaged each other about your upcoming plans. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How many days ago were Jess and I talking about theater night?",
                },
            ],
            reasoning="The user is asking about communications with Jess. I presume the user means thier contact Jess Zimmer, so I'll look at their last messages to and from Jess Zimmer. In the Messages app, they last texted Jess on 5 December. In WhatsApp, Jess last messaged them on 5 December. Either way, their last communication was 5 December. Today is 11 December, so let me subtract 5 from 11, which is 6. It has been 6 days since the user last communicated with Jess.",
            success_conditions=[
                {
                    "input_text": "1. The user is told that their conversation with Jess about theater night was six days ago.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent searches/retrieves messages or WhatsApp messages to find theater night conversation
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Agent correctly identifies the Dec 5, 2024 conversation about theater night
                # from the tools used in Milestone 0 (either email-style messages or WhatsApp)
                Milestone(
                    snapshot_constraints=[
                        # Confirm an email-style message on Dec 5 about theater night was seen
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
                                            # match that there is a message involving theater night on Dec 5
                                            "creation_datetime_iso": {
                                                "value": "2024-12-05T17:02:00-08:00",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "theater night",
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
                # Milestone 2 – User is told the correct number of days since that conversation (six days)
                # We assume reference_time = 2024-12-11T??:??-08:00 based on success conditions.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Any reasonable phrasing that clearly communicates "6 days"
                                    "content": [("6 days", "six days")],
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
                (
                    0,
                    1,
                ),  # retrieval of conversations → confirm correct theater-night message found
                (
                    1,
                    2,
                ),  # correctly identified date → correctly computed days and told user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_433c27b2-37ee-440d-af09-8b68301bf168_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T18:30:00-08:00",
            is_read_time="2024-12-05T18:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You have received confirmation on the purchase of tickets from Jess for your theatre night with her.     You now want to put the event in you calendar officially "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Could you create an event with Jess called 'Theatre with Jess?' its on the 7th, is 2 hours long and starts at 19:00. ",
                },
            ],
            reasoning="The user wants to create an event called 'Theatre with Jess' with Jess. They have given me the relevant info when it comes to the name and where it falls on the calendar. The Jess they're referring to seems to be Jess Zimmer as they are the only Jess in their contacts. I will now create an event called 'Theatre with Jess' with Jess Zimmer as an invitee for 19:00-21:00 on 7th of December 2024. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. An event called 'Theatre with Jess' with Jess Zimmer as an invitee is created for 19:00-21:00 on 7th of December 2024. ",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent tries to look up “Jess” in contacts
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
                # Milestone 1 – Confirm that the contact returned includes Jess Zimmer
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
                # Milestone 2 – Calendar event “Theatre with Jess” has been created for 7 Dec 2024 19:00-21:00 with Jess as attendee
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Theatre with Jess",
                                    "start_datetime_iso": "2024-12-07T19:00",
                                    "end_datetime_iso": "2024-12-07T21:00",
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-05T18:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_rouge_l_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
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
                (0, 1),  # Contact lookup → confirmation of Jess
                (1, 2),  # Contact confirmed → calendar event created
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_433c27b2-37ee-440d-af09-8b68301bf168_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T18:30:00-08:00",
            is_read_time="2024-12-05T18:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You have received confirmation on the purchase of tickets from Jess for your theatre night with her.     You now want to put the event in you calendar officially "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I have a theatre night with my girlfriend on Saturday from 19:00 to 21:00 can you make an event for it?",
                },
            ],
            reasoning="ok so the user wants to make an event for their theatre night with their girlfriend. It's on Saturday and runs from 19:00-21:00 thats some factual information provided by the user. From their contacts info I know their girlfriend refers to Jess Zimmer. I can add Jess as an invitee to this event. Now to get to that theatre night; if it's with Jess I can look at their correspondence to see if they talked about anything similar. It seems they did, Jess has just recently set over a photo of tickets on WhatsApp and they were also discussing the itinerary of the night. From this I will name the event 'Theatre with Jess' so there is no confusion on. the users end. I will now create an event called 'Theatre with Jess' with Jess Zimmer as an invitee for 19:00-21:00 on 7th of December 2024. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. An event called 'Theatre with Jess' with Jess Zimmer as an invitee is created for 19:00-21:00 on 7th of December 2024. ",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 — Agent looks up girlfriend contact information
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
                # Milestone 1 — Jess Zimmer contact appears in the tool output from Milestone 0
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
                # Milestone 2 — Calendar event for the theatre night is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "theatre",
                                    "start_datetime_iso": "2024-12-07T19:00",
                                    "end_datetime_iso": "2024-12-07T21:00",
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-05T18:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,  # allow Theatre/Theater etc.
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
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
            milestone_edge_list=[
                (0, 1),  # contact search → confirm Jess
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_7cc0bef3-446d-4f7d-a3fb-f7904c15522c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:10:00-08:00",
            is_read_time="2024-12-05T17:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to acknowledge receipt of Jess's text by sending a thumbs-up emoji via WhatsApp. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply with a thumbs-up emoji to Jess Zimmer\'s latest WhatsApp message that says "Here are the tickets for our theater night! 🎭."',
                },
            ],
            reasoning="The user wants me to reply with a thumbs-up emoji to Jess Zimmer's latest WhatsApp message. I have found the message and will send the reaction. ",
            success_conditions=[
                {
                    "input_text": '1. A thumbs-up emoji is sent as a message to Jess\'s WhatsApp message that says "Here are the tickets for our theater night! 🎭"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
            ],
            milestones=[
                # Milestone 0 – Agent looks up WhatsApp messages to locate Jess’s latest ticket photo
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
                    ],
                ),
                # Milestone 1 – Verify the message whose content starts with “Here are the tickets” from Jess is returned
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
                                                "value": "Here are the tickets",
                                                "partial": True,
                                            },
                                            "sender_name": {
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
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – A thumbs-up reaction (WhatsApp message containing 👍) is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [
                                            (
                                                "dawei.shen@orchardtech.com",
                                                "+1 555-123-4567-8901",
                                            ),
                                            (
                                                "jess.zimmer@fintechstartup.com",
                                                "+1 555-123-4567-8902",
                                            ),
                                        ]
                                    ],
                                    "sender_name": "Dawei Shen",
                                    "content": "👍",
                                    "creation_datetime_iso": "2024-12-05T17:10:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "sender_name": column_exact_match_similarity,
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
            name="DAWEI_SHEN_8_63e4c469-4545-46de-9f1c-a8cc9e139315_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "messaging",
                "whatsapp_messaging",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T19:00:00-08:00",
            is_read_time="2024-12-11T19:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You and your girlfriend hung out last week and got in a bit of a disagreement. You're thinking of texting her because you haven't spoken since then, but you first need to see how many days it's been since you last messaged each other about your upcoming plans. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How long since my girlfriend and I texted about the play?",
                },
            ],
            reasoning="The user is asking about communications with their girlfriend. Jess Zimmer is listed as their girlfriend in their contacts, so I'll look at their last messages to and from Jess Zimmer. In the Messages app, they last texted Jess on 5 December. In WhatsApp, Jess last messaged them on 5 December. In both cases, they were messaging about theater night, which sounds related to the \"play\" they're asking about in their query. So their last communication about this was 5 December. Today is 11 December, so let me subtract 5 from 11, which is 6. It has been 6 days since the user last communicated with Jess.",
            success_conditions=[
                {
                    "input_text": "1. The user is told that their conversation with Jess about theater night was six days ago.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent uses tools to look up past communications (messages/WhatsApp)
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Confirm that a message thread about the theater/play with Jess was retrieved
                # (email message confirming theater night or WhatsApp with tickets)
                Milestone(
                    snapshot_constraints=[
                        # Check email/message app conversation about theater night (the play)
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
                                            # The exact content from the Messages thread
                                            "content": {
                                                "value": "theater night",
                                                "partial": True,
                                            },
                                            "participants_addresses": {
                                                "value": [
                                                    "jess.zimmer@fintechstartup.com"
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
                # Milestone 2 – User is informed correctly that it has been six days
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Accept any phrasing that clearly states "6 days" or "six days"
                                    "content": [("6 days", "six days")],
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
                (
                    0,
                    1,
                ),  # Tool use to search communications → confirm the relevant theater/play conversation
                (
                    1,
                    2,
                ),  # After identifying the conversation, inform the user of elapsed time
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_53df768b-3924-4ca4-9a98-631282d87e9c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "calendar",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:05:00-08:00",
            is_read_time="2024-12-05T17:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to add your upcoming theatre night with Jess to your calendar.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Create a new Calendar event called Theatre Night, with Jess Zimmer on Monday the 9th from 7 to 10. ",
                },
            ],
            reasoning="The user wants to create a new calendar event called Theater Night, with Jess on Monday the 9th from 19:00 to 22:00. I should first check to see if the user has any other events happening at the same time that could be conflicting. Okay, I don't see any other events happening at that time. I'll create the calendar event at that time. I can tell the user that I scheduled the event. ",
            success_conditions=[
                {
                    "input_text": '1. A new calendar event is created called "Theatre Night with Jess" on Monday the 9th of December 2024 from 19:00-22:00. ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_messages",
                "get_all_messages",
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Calendar event created for Theatre Night with Jess on Monday Dec 9, 2024 19:00–22:00
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Theatre Night",
                                    "start_datetime_iso": "2024-12-09T19:00:00-08:00",
                                    "end_datetime_iso": "2024-12-09T22:00:00-08:00",
                                    "creation_datetime_iso": "2024-12-05T17:05:00-08:00",
                                }
                            ),
                            # Allow slight flexibility on timestamps if needed, but here we expect exact
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
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
            name="DAWEI_SHEN_8_190ee9dc-7983-4f76-9be5-2bba2958347f_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "messaging",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:05:00-08:00",
            is_read_time="2024-12-05T17:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to add your upcoming theatre night with Jess to your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Create a new Calendar event called Theater Night with the friend I'm supposed to be going with on Monday at 7 to 10. ",
                },
            ],
            reasoning="The user wants to create a new calendar event called theatre Night with the friend they're supposed to be going with, on Monday the 9th from 7 to 10, since the keyword is night, I assume it should be 19:00 to 22:00. I wonder who the friend they're supposed to be going with is. I should search messages (messages/whatsapp/emails) for a message thread mentioning a theater night. I see the user has a recent message thread with Jess Zimmer that talks about  plans for theater night. This must be the friend the user means. \nI should check to see if the user has any other events happening at the same time that could be conflicting. Okay, I don't see any other events happening at that time. I'll create the calendar event at that time. I can tell the user that I scheduled the \"Theater Night\" event with Jess Zimmer on Monday the 9th at 19:00-22:00.",
            success_conditions=[
                {
                    "input_text": '1. A new calendar event is created called "Theatre Night with Jess" on Monday the 9th of December 2024 from 19:00-22:00. ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "create_calendar_event",
                "get_all_calendars",
                "search_messages",
                "get_all_messages",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks up the friend in Contacts
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 — Theatre night key word found
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
                                                "value": "theater night",
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
                # Milestone 2 – Verify that the new calendar event was created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "theater night",
                                    "start_datetime_iso": "2024-12-09T19:00",
                                    "end_datetime_iso": "2024-12-09T22:00",
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-05T17:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
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
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_174642c9-27d2-4eec-8585-f2786c05c492_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:15:00-08:00",
            is_read_time="2024-12-05T17:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        'You want to indicate your excitement for the evening to Jess by replying "Can\'t wait!" to their last WhatsApp message. '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Please reply "Can\'t wait!" to the last WhatsApp message from Jess Zimmer ',
                },
            ],
            reasoning="The user wants to reply \"Can't wait!\" to the most recently received WhatsApp message from their contact Jess Zimmer. Only one individual named Jess Zimmer exists in the users contacts, however they have sent messages both on iMessage and WhatsApp. I will ask the user which of these platforms they'd like to react on, before sending the response. Based on the user's input, it seems they want to respond to Jess Zimmer's last WhatsApp message. I will send \"Can't wait!\" in that WhatsApp conversation. ",
            success_conditions=[
                {
                    "input_text": '1. "Can\'t wait!" is sent in reply to the most recently received WhatsApp message from Jess Zimmer',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
            ],
            milestones=[
                # Milestone 0 – A new WhatsApp message ("Can't wait!") has been sent to Jess (the only graded requirement)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender_name": "Dawei Shen",
                                    "participants_names": [
                                        ["Dawei Shen", "Jess Zimmer"]
                                    ],
                                    "content": [("can't wait", "cannot wait")],
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-05T17:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_names": column_list_subset_match_similarity,
                                "content": column_str_contains_any_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial state
                        )
                    ]
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_74451c4c-7944-4e4e-bd45-8fd601b51bff_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:20:00-08:00",
            is_read_time="2024-12-05T17:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "Jess is asking about your itinerary for the theatre night.  You've told her you're all set but you haven't actually checked.  You should probably check now and make sure. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Check if I have any events on this Friday.",
                },
            ],
            reasoning="The user is asking me to check events scheduled for a specific day. The request is being made on December 05, 2024 at 17:20, Thursday, so I guess the user is referring to December 05, 2024, Friday, the following day.\nI will consult the user's calendar and check. \nI can see two events scheduled for December 6th 2024, Pay Property Tax scheduled for 08:00-08:30, and Cat Sitting for Paul scheduled for all day.\nI will inform the user of these two events.",
            success_conditions=[
                {
                    "input_text": '1. Schedule for Friday December 6th is presented to the user with "Pay Property Tax" and "Cat Sitting for Paul".',
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
                # Milestone 0 – agent looks up Friday’s schedule (calendar read)
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
                # Milestone 1 – verify the two expected Friday events were surfaced from the tool call in Milestone 0
                Milestone(
                    snapshot_constraints=[
                        # a) Pay Property Tax
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
                                                "value": "Pay Property Tax",
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
                # Milestone 2 – agent looks up Friday’s schedule (calendar read)
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
                # Milestone 3 – verify the two expected Friday events were surfaced from the tool call in Milestone 0
                Milestone(
                    snapshot_constraints=[
                        # b) Cat Sitting for Paul
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
                                                "value": "Cat Sitting for Paul",
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
                # Milestone 4 – agent’s reply to user includes both event names (summary delivered)
                Milestone(
                    snapshot_constraints=[
                        # mention of Pay Property Tax
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Pay Property Tax",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # mention of Cat Sitting for Paul
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "Cat Sitting for Paul",
                                            "cat sitting",
                                            "cat-sitting",
                                            "cat sit",
                                            "Paul's cat",
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
                (2, 3),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_110fa8f0-5363-4c4f-9520-284bdcc308bd_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:25:00-08:00",
            is_read_time="2024-12-05T17:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to put the holiday plans with Jess into Calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Make an event for December 25 2024, starting at 12:00 with Jess Zimmer as an attendee called Christmas with the folks.",
                },
            ],
            reasoning="The user wants to add an event to their calendar. \nThey have provided me with the name of the event, as well as the start time and date so I will fill those details in. \nThey also want to add Jess as an attendee. I should figure out who Jess is. Looking at the user's Contacts, there is only one Jess, Jess Zimmer, so this must be who the user meant. I will add Jess as an attendee. ",
            success_conditions=[
                {
                    "input_text": '1. The event "Christmas with the folks" with attendee Jess Zimmer is added to the calendar December 25, 2024 - at 12:00.',
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
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Verify calendar event “Christmas with the folks” was added on Dec 25, 2024 12:00 with Jess as an attendee
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Christmas with the folks",
                                    "start_datetime_iso": "2024-12-25T12:00:00",
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-05T17:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_rouge_l_similarity,
                                "start_datetime_iso": column_contains_similarity,  # ensure date & time substring present
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        ),
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_a40a72d2-918d-427b-bc1d-7c23f92c9ba4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "calendar",
                "email",
                "contact",
                "whatsapp_messaging",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:05:00-08:00",
            is_read_time="2024-12-05T17:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to create a new event for the theater night you were talking about with Jess on the 19th December. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you create the event Theater Night with Jess for me on Thursday 19th December 2024 at 19:00 and invite her",
                },
            ],
            reasoning='The user wants me to create an event in their calendar called "Theater Night with Jess". It will take place on Thursday 19th December 2024 at 19:00. They mentioned Jess in their request to me, and it must be the same Jess that I just sent a message to, so I will add Jess Zimmer as an attendee for this event.',
            success_conditions=[
                {
                    "input_text": '1. A new calendar event called "Theater Night with Jess" will be created for Thursday 19th December 2024 at 19:00 with Jess Zimmer as an invitee.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – Look up Jess in contacts (information retrieval)
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
                # Milestone 1 – Confirm that contact for Jess Zimmer was retrieved (correct entity)
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
                # Milestone 2 – New calendar event created for Theater Night with Jess on Dec 19, 2024 at 19:00 including Jess
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Theater Night",
                                    "start_datetime_iso": "2024-12-19T19:00:00-08:00",
                                    # We do not strictly enforce end time; only that event exists at the requested start.
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-05T17:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "start_datetime_iso": column_contains_similarity,
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
            milestone_edge_list=[
                (0, 1),  # Contact tool use → confirm Jess contact retrieved
                (1, 2),  # Correct Jess identified → event created with Jess as attendee
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_a40a72d2-918d-427b-bc1d-7c23f92c9ba4_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "calendar",
                "email",
                "contact",
                "whatsapp_messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:05:00-08:00",
            is_read_time="2024-12-05T17:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to create a new event for the theater night you were talking about with Jess on the 19th December. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Create the event with Jess named Theater Night for me for the Thursday after next at 19:00.",
                },
            ],
            reasoning='The user wants me to create an event in their calendar called "Theater Night with Jess". They told me that it will take place the Thursday after next - I need to find out exactly when that is. I already know that today is Thursday 5th December 2024. So next Thursday is December 12th, and the Thursday after that is December 19th. That means that this event will take place on Thursday 19th December 2024. I\'ll schedule it for 19:00 like the user asked. They mentioned Jess in their request to me, and it must be the same Jess that they just sent a text message to, so I will add Jess Zimmer as an attendee for this event.',
            success_conditions=[
                {
                    "input_text": '1. A new calendar event called "Theater Night with Jess" will be created for Thursday 19th December 2024 at 19:00 with Jess Zimmer as an invitee.',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – Retrieve contact info to resolve "Jess"
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
                # Milestone 1 – Confirm that Jess Zimmer was retrieved from contacts
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
                # Milestone 2 – Calendar event created for Theater Night with Jess on 2024-12-19 at 19:00, with Jess as attendee
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Theater Night",
                                    "start_datetime_iso": "2024-12-19T19:00:00-08:00",
                                    # End time is not specified by user, so we don't constrain it.
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-05T17:05:00-08:00",
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
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → confirm Jess
                (1, 2),  # Jess resolved → create calendar event with Jess as attendee
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_110fa8f0-5363-4c4f-9520-284bdcc308bd_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:25:00-08:00",
            is_read_time="2024-12-05T17:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to put the holiday plans with Jess into Calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Add Christmas with the folks as an event on December 25, 2024 - at 12:00 with Jess as an attendee.",
                },
            ],
            reasoning="The user wants to add an event to their calendar. \nThey have provided me with the name of the event, as well as the start time and date so I will fill those details in. \nThey also want to add Jess as an attendee. I should figure out who Jess is. Looking at the user's Contacts, there is only one Jess, Jess Zimmer, so this must be who the user meant. I will add Jess as an attendee. ",
            success_conditions=[
                {
                    "input_text": '1. The event "Christmas with the folks" with attendee Jess Zimmer is added to the calendar December 25, 2024 - at 12:00.',
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
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up Jess in the contacts database
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
                # Milestone 1 – Verify the contact result contains Jess Zimmer
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
                # Milestone 2 – Calendar event “Christmas with the folks” is created on Dec 25 2024 at 12:00 with Jess as attendee
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Christmas with the folks",
                                    "start_datetime_iso": "2024-12-25T12:00",
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-05T17:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,  # allow timezone suffix
                                "attendees_names": column_list_subset_match_similarity,
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
            name="DAWEI_SHEN_8_74451c4c-7944-4e4e-bd45-8fd601b51bff_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:20:00-08:00",
            is_read_time="2024-12-05T17:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "Jess is asking about your itinerary for the theatre night.   You've told her you're all set but you haven't actually checked.   You should probably check now and make sure. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "My girlfriend wants to go the theatre on Friday, am I free that day?",
                },
            ],
            reasoning="The user is asking if they are free on a specific date because their girlfriend wants to go to the theatre. I will go through the user's contacts. I see there a contact card for Jessie Zimmerman, who is listed as 'girlfriend'. \n\nI can assume that this is a request for me to summarize the events of that date. I should consult their calendar and check. The user is making the request on Thursday, December 5th 20204. This Friday must be referring to December 6th 2024, then. \nI can see two events scheduled for this date, Pay Property Tax scheduled for 08:00-08:30, and Cat Sitting for Paul scheduled for the whole day.\n\nI should inform the user of these two events.",
            success_conditions=[
                {
                    "input_text": "1. Schedule for Friday December 6th is summarized.",
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
                # Milestone 0 – The agent looks up Friday’s schedule in the calendar
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
                # Milestone 1 – The agent tells the user about BOTH events on Friday
                Milestone(
                    snapshot_constraints=[
                        # Must mention cat-sitting
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "Cat Sitting",
                                            "cat sitting",
                                            "cat-sitting",
                                            "cat-sitting for Paul",
                                            "cat-sitting for paul",
                                            "cat sitting for Paul",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        # Must mention property-tax payment
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "Property Tax",
                                            "property tax",
                                            "pay property tax",
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
                (0, 1),  # calendar lookup precedes informing the user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_d1400b1a-9942-42f6-8adc-9071621a39ea_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T21:10:00-08:00",
            is_read_time="2024-12-05T21:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You need to remind yourself of when your property tax is due to avoid late fees. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time do I have to pay my property tax?",
                },
            ],
            reasoning="Okay so, the user is looking for the time they have to pay their property tax.\n\nI can see that there is an event corresponding to the user's query named 'Pay Property Tax'. This should be the event that the user means and I can relay to the user that 'Pay Property Tax' is scheduled for the 6th December at 8:00.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that the event named 'Pay Property Tax' is scheduled for 6th December at 8:00.",
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
                    ],
                ),
                # Milestone 1 – Confirm the “Pay Property Tax” event with the correct start time was returned
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
                                                "value": "Pay Property Tax",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-06T08:00:00-08:00",
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
                # Milestone 2 – The user is informed of the correct date and time
                Milestone(
                    snapshot_constraints=[
                        # Check for the time mention (8 am variants)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "8:00",
                                            "8 am",
                                            "8am",
                                            "8 a.m.",
                                            "8 o'clock",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        # Check for the date mention (December 6 variants)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "December 6",
                                            "6 December",
                                            "6th December",
                                            "Dec 6",
                                            "Dec. 6",
                                            "tomorrow",
                                            "Friday",
                                            "Fri",
                                            "12-06",
                                            "12/06",
                                            "12/6",
                                            "6th of December",
                                            "2024-12-06T08:00",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar lookup → confirmation of correct event
                (1, 2),  # Confirmation → informing the user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_174642c9-27d2-4eec-8585-f2786c05c492_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:15:00-08:00",
            is_read_time="2024-12-05T17:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        'You want to indicate your excitement for the evening to Jess by replying "Can\'t wait!" to their last WhatsApp message. '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Can you reply "Can\'t wait!" to the last WhatsApp message my girlfriend sent me? ',
                },
            ],
            reasoning="The user wants to reply \"Can't wait!\" to the last WhatsApp message sent by their girlfriend. First off, I will have to figure out who the user girlfriend is. I go through the user contacts, and I see Jess Zimmer is listed as 'Girlfriend'. I see the user and Jess Zimmer have exchanged messages on both iMessage and WhatsApp. Before sending the response, I will ask the user which messaging tool they are referring to. Based on their input, it seems the user wants this response to be sent to WhatsApp. I will go through the last WhatsApp messages sent from Jess Zimmer, and I will reply \"Can't wait!\" in that conversation. ",
            success_conditions=[
                {
                    "input_text": '1. "Can\'t wait!" is sent in reply to the most recently received WhatsApp message from Jess Zimmer',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_whatsapp_messages",
                "search_whatsapp_messages",
                "send_whatsapp_message",
            ],
            milestones=[
                # Milestone 0 – The agent looks up contacts to identify the user's girlfriend (Jess Zimmer)
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
                # Milestone 1 – A "Can't wait!" reply is sent in WhatsApp
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender_name": "Dawei Shen",
                                    "participants_names": [
                                        ["Dawei Shen", "Jess Zimmer"]
                                    ],
                                    "content": [("can't wait", "cannot wait")],
                                    "creation_datetime_iso": "2024-12-05T17:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_names": column_list_subset_match_similarity,
                                "content": column_str_contains_any_similarity,
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
                (0, 1),  # Contacts lookup precedes sending the reply
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_190ee9dc-7983-4f76-9be5-2bba2958347f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:05:00-08:00",
            is_read_time="2024-12-05T17:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to add your upcoming theatre night with Jess to your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Create a new Calendar event called Theatre Night, with Jess on Monday the 9th from 7 to 10, and don't forget to invite her. ",
                },
            ],
            reasoning="The user wants to create a new calendar event called Theater Night, with Jess on Monday the 9th from 7 to 10. First I need to check who 'Jess' is, I found Jess Zimmer in user's contact and recent messages regarding theatre night. Since it has keyword 'Night', I assume it should be 19:00 to 22:00. I should first check to see if the user has any other events happening at the same time that could be conflicting. Okay, I don't see any other events happening at that time. I'll create the calendar event at that time. I can tell the user that I scheduled the event with correct attendees. ",
            success_conditions=[
                {
                    "input_text": '1. A new calendar event is created with key word "Theatre Night" on Monday the 9th of December 2024 from 19:00-22:00 and Jess Zimmer is invited ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_calendar_events",
                "create_calendar_event",
                "get_all_calendars",
                "search_messages",
                "get_all_messages",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent tries to look up Jess in the contacts list
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
                # Milestone 1 – Confirm that the contact lookup returned Jess Zimmer
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
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – Verify the new calendar event was created correctly
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Theatre Night",
                                    "start_datetime_iso": "2024-12-09T19:00:00-08:00",
                                    "end_datetime_iso": "2024-12-09T22:00:00-08:00",
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-05T17:05:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,  # allow “Theatre Night with Jess”, etc.
                                "attendees_names": column_list_subset_match_similarity,  # at least Jess must be present, Dawei may also appear,
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
                (0, 1),  # Contact lookup → confirm Jess found
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_9cee730e-a1ee-42c4-87a0-51e000199dbf_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "contact",
                "calendar",
                "messaging",
                "whatsapp_messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T18:00:00-08:00",
            is_read_time="2024-12-05T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You have confirmed the itinerary for your theatre night with Jess and want to create an event to mark it in your calendar tonight, last about 3 hours. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Schedule my night out with Jess tonight — roughly two hours from when she sent the ticket and last for three hours.",
                },
            ],
            reasoning="The user wants to set up their night out with Jess for tonight, roughly two hours from when she sent the ticket. Jess seems to refer to Jess Zimmer as it is the only Jess in their contacts. The only information I have about a theatre night is through different messages on Messages and WhatsApp. These conversations take place on December 5 between 17:00 and 17:05. I will now create an event 'Theatre Night' with Jess Zimmer as an invitee around 19:00 on 5th of December 2024 and end around 22:00. ",
            success_conditions=[
                {
                    "input_text": "1. An event with Jess Zimmer as an invitee is set up around 19:00 to 22:00 on 5th of December 2024",
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
                "create_calendar_event",
                "search_messages",
                "get_all_messages",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
            ],
            milestones=[
                # Milestone 0 – Agent tries to locate the message
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
                                        "search_whatsapp_messages",
                                        "get_all_whatsapp_messages",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Confirm messages with key word theater night is found
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
                                                "value": "theater night",
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
                # Milestone 2 – Verify the calendar event was created as requested
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "start_datetime_iso": "2024-12-05T19:",
                                    "end_datetime_iso": "2024-12-05T22:",
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-05T18:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,  # allow slight variations in time
                                "end_datetime_iso": column_contains_similarity,  # allow slight variations in time
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with pre-task snapshot
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact search ➜ confirmation of correct contact
                (1, 2),  # Contact confirmed ➜ event creation
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_a22c0433-20e3-485a-9a70-117ae3b71ad0_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T12:00:00-08:00",
            is_read_time="2024-12-01T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to check what events you have scheduled at 13:00 this week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Please inform me which calendar events I have this week at 13:00.",
                },
            ],
            reasoning="The user wants to look at calendar events in the current week at 13:00 between  2024.12.01 00:00 and 2024.12.08 23:59.\n\nI need to look at the user calendar for any events scheduled at 13:00 between these dates.\n\nI don't see any events scheduled this week at the time which the user specified, I will relay this information to the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. User calendar is checked for events scheduled at 13:00 hours from 2024.12.01 00:00 - 2024.12.08 23:59 and no events found is relayed to the user.",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent checks the calendar (information-retrieval)
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
                # Milestone 1 – Agent tells the user there are no events at 13:00 this week
                Milestone(
                    snapshot_constraints=[
                        # Response conveys that there are no events
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "no",
                                            "not",
                                            "none",
                                            "nothing",
                                            "don't have any",
                                            "nothing scheduled",
                                            "clear",
                                            "free",
                                            "empty",
                                            "no meetings",
                                            "no appointments",
                                            "aren't any",
                                            "no events",
                                            "zero",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_35872f2d-0b62-4af4-bcc5-e8dfc846cd47_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:15:00-08:00",
            is_read_time="2024-12-08T18:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You feel sick and need to cancel your theater rehearsal and let Jess know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Let my girlfriend know that I am not feeling well so I am not going.",
                },
            ],
            reasoning='The user is asking me to send a message.\nFirst, I need to identify the intended recipient.\nThe user has referred to their girlfriend, I can see one person tagged as this in the user\'s contacts, Jess Zimmer.\nI will now compose the message as requested. \nA message with the content like "I am not feeling well so I am going to give rehearsal a skip" will be sent to Jess Zimmer',
            success_conditions=[
                {
                    "input_text": '1. A text message is sent to Jess Zimmer that like "I am not feeling well so I am going to give rehearsal a skip". ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up girlfriend contact information
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
                # Milestone 1 – Contact lookup returns Jess Zimmer
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
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        ),
                    ],
                ),
                # Milestone 2 – Message sent to Jess stating sickness / missing rehearsal
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
                                                "+1 555-123-4567-8902",
                                                "jess.zimmer@fintechstartup.com",
                                            ),
                                            (
                                                "+1 555-123-4567-8901",
                                                "dawei.shen@orchardtech.com",
                                            ),
                                        ]
                                    ],
                                    "content": "not feeling well",
                                    "creation_datetime_iso": "2024-12-08T18:15:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Require both Jess and Dawei (self) to be in the conversation
                                "participants_addresses": column_list_tuple_contains_similarity,
                                # Message body must mention being unwell
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
                (0, 1),  # Contact search → confirmation of Jess found
                (1, 2),  # Jess found → message sent
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_c97b290c-5dd6-4107-ab13-cb2d11f7052a_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T10:30:00-08:00",
            is_read_time="2024-12-07T10:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You need to cancel your brunch and want to reschedule so you can still meet Jess. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Cancel the meal with my girlfriend and schedule in a two hour dinner with her starting at 19:00 instead.",
                },
            ],
            reasoning="The user is asking me to perform multiple tasks.\nFirst, they have asked me to delete a scheduled event. I should search the calendar for meal events. While I cannot find an exact match, I see one potential match, Brunch with Jess scheduled for December 7 2024 11:00-13:00. I should check the user's contacts and confirm identity of the girlfriend. I can see that Jess Zimmer has the girlfriend tag. I am confident that this is the right event to cancel.\nNext, the user has asked me to schedule a new event. \nI will schedule a new event as instructed.\nDinner with Jess is scheduled for December 7 2024, 19:00-21:00.",
            success_conditions=[
                {
                    "input_text": "1. The event Brunch with Jess at 11:00-13:00 on 07 December 2024 is cancelled",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. A new calendar event is created called like Dinner with Jess at 19:00 on the 07 December 2024.",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "3. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "search_calendar_events",
                "create_calendar_event",
                "get_all_calendars",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up calendar events to locate the brunch
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
                # Milestone 1 – The brunch event (11:00-13:00 on 7 Dec 2024) was actually returned by the search in Milestone 0
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
                                        "calendar_event_name": {
                                            "value": "Brunch with Jess",
                                            "partial": False,
                                        },
                                        "start_datetime_iso": {
                                            "value": "2024-12-07T11:00:00-08:00",
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
                            reference_milestone_node_index=0,  # depend on search outcome
                        )
                    ],
                ),
                # Milestone 2 – The brunch event has been removed / cancelled
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=not_contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Brunch with Jess",
                                    "start_datetime_iso": "2024-12-07T11:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ]
                ),
                # Milestone 3 – A new dinner event has been created for 19:00-21:00 on 7 Dec 2024
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=contains_presence_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dinner",
                                    "start_datetime_iso": "2024-12-07T19:00:00-08:00",
                                    "end_datetime_iso": "2024-12-07T21:00:00-08:00",
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-07T10:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
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
                (0, 1),  # search → confirm event found
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_16bbdd91-caa2-441e-acd9-1dec29b22265_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T18:00:00-08:00",
            is_read_time="2024-12-06T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "Jess is asking you about your availability.    You are unsure and need to check. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Do I have any events set Saturday or Sunday?",
                },
            ],
            reasoning="The user is asking about events this Saturday and Sunday.\nLooking at the calendar I can see one event, Cat Sitting for Paul, this event begins at 00:00 December 6th 2024 and ends at 23:59 December 8th 2024. I should notify the user.",
            success_conditions=[
                {
                    "input_text": "1. December 7th and 8th are checked for events.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent looks up weekend events (Saturday/Sunday)
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
                # Milestone 1 – Verify the weekend “Cat Sitting for Paul” event is found
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
                                                "value": "Cat Sitting for Paul",
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
                # Milestone 2 – Agent informs the user about the weekend cat-sitting event
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("Cat Sitting", "cat sitting")],
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
                (0, 1),  # Calendar lookup → confirm event found
                (1, 2),  # Event found → user informed
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_9a2049e8-daf3-4ae6-a47a-3aca02c947e2_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_8",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T18:00:00-08:00",
            is_read_time="2024-12-05T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "Jess is asking you about your availability for theater night. You admittedly told her you were all set for theater night, but you're not sure if you're available this weekend anymore and need to double check. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Do I have any events set Saturday or Sunday?",
                },
            ],
            reasoning="The user is asking about events this Saturday and Sunday.\nLooking at the calendar I can see one event, Cat Sitting for Paul, this event begins at 00:00 December 6th 2024 and ends at 23:59 December 8th 2024. I should notify the user.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their only event between 7 December and 8 December 2024 is all-day Cat-Sitting for Paul.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent checks calendar (search or list) for events on the weekend
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
                # Milestone 1 – Confirms the "Cat Sitting for Paul" weekend event (Dec 6–8, 2024) is present in retrieved results
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
                                                "value": "Cat Sitting for Paul",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-06T00:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-08T23:59:59-08:00",
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
                # Milestone 2 – User is informed that the only event on Saturday and Sunday is cat sitting for Paul
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Ensure the response mentions cat sitting for Paul and that it's the only event that weekend
                                    "content": [
                                        (
                                            "Cat Sitting for Paul",
                                            "cat sitting for Paul",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                            },
                        ),
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            # A second loose check that they convey it's the only / just / one event that weekend
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "only event",
                                            "just that",
                                            "nothing else",
                                            "no other events",
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
                (0, 1),  # Calendar lookup → confirm weekend event exists
                (1, 2),  # Confirm event → inform user correctly
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_9a2049e8-daf3-4ae6-a47a-3aca02c947e2_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_8",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T18:00:00-08:00",
            is_read_time="2024-12-05T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "Jess is asking you about your availability for theater night. You admittedly told her you were all set for theater night, but you're not sure if you're available this weekend anymore and need to double check. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Am I free this weekend?",
                },
            ],
            reasoning="The user is asking if they are free for the coming weekend.\nI can assume this is referring to their schedule.\nLooking at the calendar I can see one event, Cat Sitting for Paul, this event begins at 00:00 December 6th 2024 and ends at 23:59 December 8th 2024. I should notify the user.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their only event between 7 December and 8 December 2024 is all-day Cat-Sitting for Paul.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent checks calendar for the upcoming weekend (Dec 7–8, 2024)
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
                # Milestone 1 – Confirms that the "Cat Sitting for Paul" all-weekend event is present (Dec 6–8)
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
                                                "value": "Cat Sitting for Paul",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-06T00:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-08T23:59:59-08:00",
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
                # Milestone 2 – User is informed that the only event that weekend is Cat Sitting for Paul
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Key information: only event is cat sitting that spans the weekend
                                    "content": [
                                        (
                                            "Cat Sitting for Paul",
                                            "cat sitting",
                                            "cat-sitting",
                                            "cat sit",
                                            "Paul's cat",
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
                (0, 1),  # Calendar checked → specific weekend event confirmed
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_16bbdd91-caa2-441e-acd9-1dec29b22265_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T18:00:00-08:00",
            is_read_time="2024-12-06T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "Jess is asking you about your availability.    You are unsure and need to check. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Am I free this weekend?",
                },
            ],
            reasoning="The user is asking if they are free for the coming weekend.\nI can assume this is referring to their schedule.\nLooking at the calendar I can see one event, Cat Sitting for Paul, this event begins at 00:00 December 6th 2024 and ends at 23:59 December 8th 2024. I should notify the user.",
            success_conditions=[
                {
                    "input_text": "1. December 7th and 8th are checked for events.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – the agent inspects the calendar for the coming weekend
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
                # Milestone 1 – confirm that the weekend event “Cat Sitting for Paul” is present in the tool output from milestone 0
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
                                                "value": "Cat Sitting for Paul",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-06T00:00:00-08:00",
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
                # Milestone 2 – the agent’s reply to the user indicates they are not free / have cat-sitting duties
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
                                            "cat sitting",
                                            "Cat Sitting",
                                            "watch Paul",
                                            "busy",
                                            "not free",
                                            "occupied",
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
                (0, 1),  # calendar checked → event confirmed
                (1, 2),  # event confirmed → user informed
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_c97b290c-5dd6-4107-ab13-cb2d11f7052a_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T20:10:00-08:00",
            is_read_time="2024-12-07T20:10:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You need to cancel your brunch and want to reschedule so you can still meet Jess. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Cancel the brunch with Jess today and create a 'Dinner with Jess' event instead, 7 hours after the brunch ends.",
                },
            ],
            reasoning="The user wants to cancel the existing brunch with Jess today and create a dinner with her instead, timed 7 hours after the brunch ends.\n\nI look up today's calendar and find the Brunch with Jess at 11:00-13:00. I cancel it, then create a new 'Dinner with Jess' event 7 hours after it ends: 13:00 + 7 hours = 20:00.",
            success_conditions=[
                {
                    "input_text": "1. The event Brunch with Jess at 11:00-13:00 on 07 December 2024 is cancelled",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. A new calendar event is created called Dinner with Jess at 20:00 on the 07 December 2024.",
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
                "search_calendar_events",
                "create_calendar_event",
                "get_all_calendars",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – The agent looks up existing calendar events (information-retrieval)
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
                # Milestone 1 – Confirms the Brunch with Jess event was returned in the tool output
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
                                                "value": "Brunch with Jess",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-07T11:00:00-08:00",
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
                            reference_milestone_node_index=0,  # depends on retrieval in milestone 0
                        ),
                    ],
                ),
                # Milestone 2 – A new dinner event is created/updated for 19:00-21:00 the same day
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=update_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Dinner with Jess",
                                    "start_datetime_iso": "2024-12-07T20:00:00-08:00",
                                    "attendees_names": [["Dawei Shen", "Jess Zimmer"]],
                                    # "attendees_names": [["Dawei Shen"]],
                                    "creation_datetime_iso": "2024-12-07T20:10:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against the removal
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # retrieval → confirmation of brunch event exists
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_35872f2d-0b62-4af4-bcc5-e8dfc846cd47_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:15:00-08:00",
            is_read_time="2024-12-08T18:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You feel sick and need to cancel your theater rehearsal and let Jess know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Text Jess to say "I am not feeling well so I am going to give rehearsal a skip".',
                },
            ],
            reasoning='The user is asking me to send a message.\nFirst, I will find Jess in the user\'s contacts. I can see only one Jess, Jess Zimmer.\nI will now compose the message as requested. \nA message with the content "I am not feeling well so I am going to give rehearsal a skip" will be sent to Jess Zimmer',
            success_conditions=[
                {
                    "input_text": '1. A text message is sent to Jess Zimmer that says "I am not feeling well so I am going to give rehearsal a skip". ',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up Jess in contacts
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
                # Milestone 1 – Confirm that Jess Zimmer was returned from contact search in Milestone 0
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
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,  # use results from milestone 0
                        ),
                    ],
                ),
                # Milestone 2 – A new text message to Jess with correct content is created
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
                                                "+1 555-123-4567-8902",
                                                "jess.zimmer@fintechstartup.com",
                                            ),
                                            (
                                                "+1 555-123-4567-8901",
                                                "dawei.shen@orchardtech.com",
                                            ),
                                        ]
                                    ],
                                    "content": "not feeling well",
                                    "creation_datetime_iso": "2024-12-08T18:15:00-08:00",
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
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → confirm Jess found
                (1, 2),  # Jess confirmed → message sent
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_a22c0433-20e3-485a-9a70-117ae3b71ad0_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-01T12:00:00-08:00",
            is_read_time="2024-12-01T12:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to check what events you have scheduled at 13:00 this week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Do I have any stuff on this week which is scheduled at the same time as 3 hours after my Cycling Trip with Vick ends?",
                },
            ],
            reasoning='I infer that "Do I have stuff on this week" means that user wants to look at calendar events in the current week. The request is being made on December 01, 2024 at 12:00, so I will check between 2024.12.01 at 12:00 and 2024.12.07 23:59, the time frame corresponding to \'this week\' taking into account the user\'s request.\n\nThe time frame they want to look at is stated as "the same time as 3 hours after my Cycling Trip with Vick ends". \n\nI should search for cycling trip in the user calendar and confirm the time at which this event ends. To calculate the time frame the user wants to look at I should add 3 hours to this time (10:00 + 03:00 = 13:00). \n\nI should then search the user calendar for the current week with the time frame 13:00. To do this, I will need to take into account all the events the user has scheduled for the current week. \n\nI see no events scheduled in the user calendar at 13:00 in the current week, so I will share this information with the user.',
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. User calendar is checked for events scheduled at 13:00 hours from 2024.12.01 00:00 - 2024.12.07 23:59 and the information is relayed to the user.",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent queries the calendar for this week
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
                # Milestone 1 – Agent tells the user there are no events at 13:00 this week
                Milestone(
                    snapshot_constraints=[
                        # Response conveys that there are no events
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "no",
                                            "not",
                                            "none",
                                            "don't have any",
                                            "nothing scheduled",
                                            "clear",
                                            "no meetings",
                                            "no appointments",
                                            "aren't any",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar search precedes the user-facing response
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_8afd9149-9db7-4a89-be08-8b6cc0ec8db4_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "contact",
                "whatsapp_messaging",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T17:20:00-08:00",
            is_read_time="2024-12-05T17:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to check the tickets Jess sent you for theatre night so that you can make a note of the date and time on them. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you show me the message which contains our theatre night tickets my girlfriend sent me? ",
                },
            ],
            reasoning='The user wants me to retrieve a message containing our theatre night tickets that their girlfriend sent, so first I must figure out which contact that is. I have managed to find Jess Zimmer saved in the user contacts listed as "girlfriend", so I can assume the user wants me to find an attachment that Jess Zimmer sent. Next I need to figure out through which tool this attachment was sent. I have checked messages, mail and WhatsApp and I have found a message regarding theatre night tickets that has contains an attachment. This a WhatsApp message sent on 05 December 2024 at 17:05:00.\n\nI can assume this is the message with the attachment the user wants to see, so I will open it up on the user\'s screen. ',
            success_conditions=[
                {
                    "input_text": "The last WhatsApp message sent by Jess, which includes the tickets for the theater night, is retrieved for the user to read. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_whatsapp_messages",
                "get_all_whatsapp_messages",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – Agent tries to locate the relevant WhatsApp message
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
                    ],
                ),
                # Milestone 1 – Confirm the returned WhatsApp message is the one from Jess with the tickets
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
                                                "value": "Jess Zimmer",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "tickets",
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
                # Milestone 2 – Agent shows the user (in its reply) the message containing the tickets
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
                                            "Here are the tickets",
                                            "tickets for our theater night",
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
                (0, 1),  # Tool invocation → verify correct message retrieved
                (1, 2),  # Retrieval confirmed → verify user-facing reply
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_8_9cee730e-a1ee-42c4-87a0-51e000199dbf_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T18:00:00-08:00",
            is_read_time="2024-12-05T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You have confirmed the itinerary for your theatre night with Jess and want to create an event to mark it in your calendar at 7pm tonight, last about 2 hours. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set up my theatre night with my girlfriend tonight, one hour from now and last 2 hours. ",
                },
            ],
            reasoning="The user wants to set up their theatre night with their girlfriend for tonight one hour from now. I assume their girlfriend refers to Jess Zimmer by the information provided on the contact card for Jess Zimmer. They have also spoken about a theatre night recently over Messages and WhatsApp, and have shared itinerary of it on December 5 at 17:00.  I will now create an event 'Theatre Night' with Jess Zimmer as an invitee at 19:00 and end at 21:00 on 5th of December 2024. ",
            success_conditions=[
                {
                    "input_text": "1. An event called 'Theatre Night' with Jess Zimmer as an invitee is set up at 19:00 to 21:00 on 5th of December 2024",
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
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up girlfriend / Jess in contacts
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
                # Milestone 1 – Verify that the contact data for Jess Zimmer was actually returned
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
                # Milestone 2 – A new calendar event has been created for the theatre night
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Theatre Night",
                                    "start_datetime_iso": "2024-12-05T19:00:00-08:00",
                                    "end_datetime_iso": "2024-12-05T21:00:00-08:00",
                                    "attendees_names": [["Jess Zimmer"]],
                                    "creation_datetime_iso": "2024-12-05T18:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                # Require Jess to be on the invite list, allow extra attendees such as self
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
            name="DAWEI_SHEN_8_bc3ae404-0e7d-4dc9-b9fa-757cdec13c8f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_8",
                "calendar",
                "messaging",
                "contact",
                "misinformation_no",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_high",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:15:00-08:00",
            is_read_time="2024-12-08T18:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You feel sick and need to cancel your theater rehearsal and let Jess know. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Clear the rehearsal from my calendar and let my girlfriend know that I am not feeling well so I am not going.",
                },
            ],
            reasoning='I need to find an event on the calendar today named "Rehearsal" I found one containing that name at 19:00 with title "Theater Rehearsal". Now I\'ll delete it from the calendar.\n\nI need to figure out who "my girlfriend" is. I\'ll look in the user\'s contacts. I found Jess Zimmer in the \'girlfriend\' relationship.\n\nI will ask the user what they want me to text to Jess. ',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "'Theater Rehearsal' scheduled at \"2024-12-08T19:00:00-08:00\" is deleted from calendar. ",
                },
                {
                    "input_text": 'A text message is sent to Jess Zimmer that says something like "I am not feeling well. I am going to give rehearsal a skip". ',
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "remove_calendar_event",
                "search_contacts",
                "get_all_contacts",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Retrieve contacts to identify "my girlfriend" as Jess Zimmer
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
                # Milestone 1 – Confirm Jess (girlfriend) was found in contacts
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
                                            "relationship": {
                                                "value": "Girlfriend",
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
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
                # Milestone 2 – Calendar search to find the "Theater Rehearsal" event
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
                # Milestone 3 – Confirm the correct Theater Rehearsal event was retrieved
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
                                                "value": "Theater Rehearsal",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-08T19:00:00-08:00",
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
                # Milestone 4 – Theater Rehearsal event is removed from the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Theater Rehearsal",
                                    "start_datetime_iso": "2024-12-08T19:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
                # Milestone 5 – A message is sent to Jess explaining sickness and skipping rehearsal
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
                                                "jess.zimmer@fintechstartup.com",
                                                "+1 555-123-4567-8902",
                                            ),
                                            (
                                                "dawei.shen@orchardtech.com",
                                                "+1 555-123-4567-8901",
                                            ),
                                        ]
                                    ],
                                    "content": [
                                        (
                                            "not feeling well",
                                            "unwell",
                                            "sick",
                                            "under the weather",
                                        )
                                    ],
                                    "creation_datetime_iso": "2024-12-08T18:15:00-08:00",
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
                (0, 1),  # Contact lookup → confirm Jess as girlfriend
                (2, 3),  # Calendar lookup → confirm specific Theater Rehearsal event
                (3, 4),  # Once event identified → event removed
                (1, 5),  # Once Jess identified → send message to her
            ],
        ),
    ]
