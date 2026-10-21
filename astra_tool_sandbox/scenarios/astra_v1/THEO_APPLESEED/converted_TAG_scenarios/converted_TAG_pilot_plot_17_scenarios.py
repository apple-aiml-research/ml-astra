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


def get_TAG_THEO_APPLESEED_pilot_plot_17(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="THEO_APPLESEED_17_d7a247e9-993a-4d9f-85d5-16123a73cdb8_single_turn_3",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "contact",
                "messaging",
                "phone_call",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T15:35:00-07:00",
            is_read_time="2024-07-27T15:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send your mom a message after your lovely chat with her. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text the person I called half an hour ago and say 'It was great catching up with you. Want to come round for dinner next week?'",
                },
            ],
            reasoning="The user wants to send a text message. They want the recipient to be the person they called half an hour ago. Let me look at their call logs. The only call from today, 27 July 2024, was at 15:00. Right now it's 15:35, so 15:00 was 35 minutes ago, not 30 minutes ago. However, 5 minutes seems like a reasonable margin of error for the user to make; 35 minutes is close enough to half an hour for me to assume that this is the call the user was talking about, primarily because it's the only call in their call history today. This call was to Sarah Appleseed, so that's who I'll send the text to. I'll send the text that says 'It was great catching up with you. Want to come round for dinner next week?'.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A text message is sent to Sarah Appleseed saying, 'was great catching up with you. Want to come round for dinner next week?'",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_phone_calls",
                "search_phonecall_logs",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent checks phone call logs to identify "the person I called half an hour ago"
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
                                        "search_phonecall_logs",
                                        "get_all_phone_calls",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – Confirms that Sarah Appleseed was identified from phone logs in Milestone 0
                # (called party of the recent call)
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
                                            # We just need to see that a log entry exists where Sarah is the other party
                                            "receiver_address": {
                                                "value": "1234-5678-9111",
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
                # Milestone 2 – A text message was sent to Sarah with the requested content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Participants must include Sarah's phone number; Theo/self may also appear
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9111",  # Sarah's phone
                                                "sarah.appleseed@example.com",
                                            ),
                                            (
                                                "1234-5678-9101",  # Theo/self
                                                "theo.appleseed@example.com",
                                            ),
                                        ]
                                    ],
                                    "content": "was great catching up with you. Want to come round for dinner next week?",
                                    "creation_datetime_iso": "2024-07-27T15:35:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # Ensure at least one identifier for Sarah and Theo appears; allow no extras beyond these two logical participants
                                "participants_addresses": column_list_tuple_contains_similarity,
                                # Content should contain the user-specified message (case-insensitive, substring ok)
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # phone log lookup → confirm Sarah identified
                (1, 2),  # Sarah identified as callee → message sent to her
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_17_cf096ca9-9b71-485e-8628-a4db64d5fe77_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "phone_call",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T19:00:00-07:00",
            is_read_time="2024-07-27T19:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send a message to your mother saying that you enjoyed your call earlier today and that you love her "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send my mom a text saying I enjoyed our call today and I love her.",
                },
            ],
            reasoning="The user wants me to send their mom a text saying they enjoyed their call today and they love her. Sarah Appleseed is noted as the user's mother in their contacts. I'll write something like \"Hi Mom I really enjoyed our call earlier today. I love you.\" and present it to the user. With their approval I will send the message to Sarah Appleseed.",
            success_conditions=[
                {
                    "input_text": '1. A text message is sent to Sarah Appleseed saying "I really enjoyed our call earlier today Mom. I love you."',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_phone_calls",
                "search_phonecall_logs",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent looks up Mom’s contact information
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
                # Milestone 1 – The previous contact-lookup returned Sarah Appleseed (Mom)
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
                                                "value": "Sarah Appleseed",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9111",
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
                    ],
                ),
                # Milestone 2 – A new text message was sent to Mom containing the required sentiment
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
                                                "1234-5678-9111",
                                                "sarah.appleseed@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "enjoyed our call",
                                    "creation_datetime_iso": "2024-07-27T19:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,  # allow agent’s own number to also appear
                                "content": column_contains_similarity,  # must contain the phrase fragment,
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
            name="THEO_APPLESEED_17_cf096ca9-9b71-485e-8628-a4db64d5fe77_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "contact",
                "phone_call",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T19:00:00-07:00",
            is_read_time="2024-07-27T19:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send a message to your mother saying that you enjoyed your call earlier today and that you love her "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a text saying I enjoyed our call today and I love her.",
                },
            ],
            reasoning="The user wants me to send someone a text saying they enjoyed their call today and they love her. I must first determine who they wish to send the message too. The user mentioned they enjoyed their call today, looking at the user's call log they only had one call today with Sarah Appleseed who is noted as the user's mother in their contacts. I can assume Sarah is the intended recipient but I will ask for confirmation. the user has confirmed Sarah Appleseed is the intended recipient.  I'll write something like \"Hi Mom I really enjoyed our call earlier today. I love you.\" and present it to the user. With their approval I will send the message to Sarah Appleseed.",
            success_conditions=[
                {
                    "input_text": '1. A text message is sent to Sarah Appleseed saying something like "I really enjoyed our call earlier today Mom. I love you."',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_phone_calls",
                "search_phonecall_logs",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent uses a contact-retrieval tool to locate Mom’s info
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
                # Milestone 1 – Confirm the tool output contained Sarah Appleseed (Mom)
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
                                                "value": "Sarah Appleseed",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9111",
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
                # Milestone 2 – A new outgoing text message was created & sent to Mom
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Must include Mom as a participant (self may also appear)
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9111",  # Sarah's phone
                                                "sarah.appleseed@example.com",  # Sarah's email
                                            )
                                        ]
                                    ],
                                    # Message body must convey affection / call enjoyment
                                    "content": "love",
                                    "creation_datetime_iso": "2024-07-27T19:00:00-07:00",
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
                (0, 1),  # Tool call ➜ verify Mom’s contact retrieved
                (1, 2),  # Contact retrieved ➜ message successfully sent
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_17_42d5626e-4166-4fb9-9492-8acea0a73a93_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T16:15:00-07:00",
            is_read_time="2024-07-27T16:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You had a great call with your mother and you want to schedule in another call for Monday 29th July 2024 at around 17:00. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you schedule in a call with mom for Monday at 17:00",
                },
            ],
            reasoning='The user wants me to schedule in an event in their calendar. Based on their query, they want to schedule a call with their mom. I need to check if they have their mom listed as a contact so I can find out easily who to add to the event. I found "Sarah Appleseed" who is listed as "Mother" in the user\'s contacts.\nNext, they asked me to schedule it on Monday at 17:00. If today is Saturday 27th July 2024, then Monday is the 29th July 2024. Therefore, I should schedule the event for Monday 29th July 2024 at 17:00. There don\'t appear to be any scheduling conflicts in the calendar for this time. With the user\'s confirmation, I will create the event "Call with Mom" with Sarah Appleseed as an invitee for Monday 29th July 2024 at 17:00. ',
            success_conditions=[
                {
                    "input_text": '1. The event "Call with Mom" is created with Sarah Appleseed as an invitee at 17:00 on 29 July 2024. ',
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
                # Milestone 0 – Agent looks up Mom’s contact information
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
                # Milestone 1 – Verify that Sarah Appleseed (“Mom”) was retrieved from the contact search
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
                                                "value": "Sarah Appleseed",
                                                "partial": False,
                                            },
                                            "relationship": {
                                                "value": "Mother",
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
                # Milestone 2 – Calendar event “Call with Mom” on 29 Jul 2024 17:00 with Sarah Appleseed added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Mom",  # will be matched loosely
                                    "start_datetime_iso": "2024-07-29T17:00:00",
                                    "attendees_names": [["Sarah Appleseed"]],
                                    "creation_datetime_iso": "2024-07-27T16:15:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,  # event title contains “Mom”
                                "start_datetime_iso": column_contains_similarity,  # contains correct date-time string
                                "attendees_names": column_list_subset_match_similarity,  # must include Sarah, allow extras (e.g., Theo),
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
                (0, 1),  # contact search → confirm mom retrieved
                (1, 2),  # mom confirmed → new calendar event created
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_17_90d93890-fc2b-4cce-ae78-88b0e32f8ba7_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T15:35:00-07:00",
            is_read_time="2024-07-27T15:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "Talking with your mother, you decide to set up a lunch with her.   You want to make sure that you have no plans that Saturday and to add the lunch to the calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Check if there are any plans in my calendar for August 3rd and if not add "Lunch with Mom" at 1pm that day.',
                },
            ],
            reasoning='The user wants to know if they have any plans in their calendar for 3rd August 2024. I will check. There are no events currently scheduled for that day. I inform the user of that fact. I then create an event for 3rd August 2024 at 13:00 as per requested by the user . The event is called "Lunch with Mom" .',
            success_conditions=[
                {
                    "input_text": "1. An event called 'Lunch with Mom' is created at 13:00 on August 3rd 2024.",
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
                # Milestone 0 – The agent looks at the calendar to see if anything is scheduled
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
                # Milestone 1 – A new calendar event called “Lunch with Mom” at 1 pm on 3 Aug 2024 is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Lunch with Mom",
                                    "start_datetime_iso": "2024-08-03T13:00:00",
                                    "creation_datetime_iso": "2024-07-27T15:35:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # Allow timezone info or seconds differences by only requiring the base timestamp substring
                                "start_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare to initial state
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_17_f0f98438-152b-4b08-9dc8-d854dfa5ef2e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T18:20:00-07:00",
            is_read_time="2024-07-29T18:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You haven't heard from Cookie in a while and want to know when she last contacted you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When did Cookie last text me?",
                },
            ],
            reasoning="The user wants to know when Cookie last texted them. First I should figure out who Cookie is by checking the user's Contacts. Looks like the user only has one Cookie, Cookie Watson, in their Contacts. Now I will check Messages for the last text from Cookie. Looks like the last text from Cookie was received at 19:10 on 26 July 2024 and said 'Theo, everyone's confirmed. What's the meeting time?'. I can then announce this to the user as this is what they're looking for.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that last message received from Cookie Watson on 26th July 2024 at 19:10, saying 'Theo, everyone's confirmed. What's the meeting time?'.",
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
                # Milestone 1 – The returned tool result contains the correct last message from Cookie
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
                                            "creation_datetime_iso": {
                                                "value": "2024-07-26T19:10:00-07:00",
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
                # Milestone 2 – Agent informs the user with the key information
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("19:10", "7:10")],
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
            name="THEO_APPLESEED_17_18e3fb17-a227-4830-9598-f26bdd249ef7_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "messaging",
                "phone_call",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T19:00:00-07:00",
            is_read_time="2024-07-27T19:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send a message to your mother saying that you enjoyed your call earlier today and that you love her "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send her a text saying I enjoyed our call today and I love her.",
                },
            ],
            reasoning="The user wants me to send someone a text saying they enjoyed their call today and they love her. I must first determine who they wish to send the message too. The user mentioned they enjoyed their call today, looking at the user's call log they only had one call today with Sarah Appleseed who is noted as the user's mother in their contacts. I can assume Sarah is the intended recipient but I will ask for confirmation. the user has confirmed Sarah Appleseed is the intended recipient.  I'll write something like \"Hi Mom I really enjoyed our call earlier today. I love you.\" and present it to the user. With their approval I will send the message to Sarah Appleseed.",
            success_conditions=[
                {
                    "input_text": '1. A text message is sent to Sarah Appleseed saying content like "I really enjoyed our call earlier today Mom. I love you."',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "send_message",
                "search_phonecall_logs",
                "get_all_phone_calls",
            ],
            milestones=[
                # Milestone 0 – Agent invokes a phone call logs search
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
                                        "search_phonecall_logs",
                                        "get_all_phone_calls",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – The returned tool result contains the phone call to mon
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
                                            "receiver_address": {
                                                "value": "1234-5678-9111",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-27T15:00:00-07:00",
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
                # Milestone 2 – A new text message is sent to Mom (Sarah Appleseed)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require that Mom's phone number appears among the participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9111",  # Sarah's phone
                                                "sarah.appleseed@example.com",  # Sarah's email
                                            )
                                        ]
                                    ],
                                    # Require the content to mention both that the call was enjoyed and that she is loved
                                    "content": [("enjoy", "love")],
                                    "creation_datetime_iso": "2024-07-27T19:00:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_str_contains_any_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial state
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_17_f0f98438-152b-4b08-9dc8-d854dfa5ef2e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_17",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T18:20:00-07:00",
            is_read_time="2024-07-29T18:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You haven't heard from Cookie in a while and want to know when she last contacted you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When did Cookie Watson last text?",
                },
            ],
            reasoning="The user wants to know when Cookie Watson last text them. I should check Messages. Seems like Cookie last text at 19:10 on 26 July 2024 and said 'Theo, everyone's confirmed. What's the meeting time?'. Now that I have found the correct message, I can announce this to the user.",
            success_conditions=[
                {
                    "input_text": "1. The user has been informed that the last message received from Cookie Watson on 26th July 2024 at 19:10, saying 'Theo, everyone's confirmed. What's the meeting time?' is announced to the user.",
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
                # Milestone 0 – Agent uses a messaging lookup tool to find Cookie’s latest text
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
                # Milestone 1 – Confirm that the tool output actually contained Cookie Watson’s
                # 2024-07-26 19:10 message
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
                                            # Either the conversation name or sender address must match
                                            "conversation_name": {
                                                "value": "Cookie Watson",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "cookie.watson@example.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-26T19:10:00-07:00",
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
                    ]
                ),
                # Milestone 2 – Agent answers the user with the correct date (July 26 2024) and
                # time (19:10 / 7:10 pm) or close paraphrase
                Milestone(
                    snapshot_constraints=[
                        # Must mention the correct time (any reasonable 19:10 / 7:10 pm variant)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("19:10", "7:10 pm", "7:10 pm")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity,
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Tool call → verify message present
                (1, 2),  # Verified retrieval → user-facing answer
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_17_d7a247e9-993a-4d9f-85d5-16123a73cdb8_single_turn_4",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "contact",
                "messaging",
                "phone_call",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T15:35:00-07:00",
            is_read_time="2024-07-27T15:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send your mom a message after your lovely chat with her. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Text the person I talked to more recently among the two people in my call history who were born in the 1960s and say 'was great catching up with you. Want to come round for dinner next week?'",
                },
            ],
            reasoning="The user wants to send a text message. They want to text the person who they \"talked to\" most recently. That could mean text, call, email, or something else. I'll try to figure out who exactly the user wants to contact, and that should help me determine how exactly they want to contact them. To start narrowing down the list of people the user might potentially be talking about, I'll use the fact that they said it would be among the two people in the user's call history who were born in the 1960s. I only see two calls in the user's call history, one call the user made to Sarah Appleseed today at 15:00, and one call the user made to John Appleseed on 23 July 2024 at 18:00. Looking at the user's contacts, Sarah Appleseed was born in 1967, and John Appleseed was born in 1965. So I need to figure out which of these two people the user wants to contact by determining who they talked to more recently. I don't see any emails or text messages from or to Sarah Appleseed or John Appleseed, so I'll assume that the user means phone calls when they say \"talked to.\" So I need to figure out which of these two people the user was on the phone with more recently. Their call to Sarah Appleseed was today at 15:00, and their call to John Appleseed was on 23 July 2024 at 18:00. Their call to Sarah Appleseed is the more recent one, just 35 minutes ago. So the user wants me to text Sarah Appleseed. I'll text her and say 'was great catching up with you. Want to come round for dinner next week?'.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A text message is sent to Sarah Appleseed saying, 'was great catching up with you. Want to come round for dinner next week?'",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_phone_calls",
                "search_phonecall_logs",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Retrieve phone call history to identify recent calls, including mom and dad
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
                                        "get_all_phone_calls",
                                        "search_phonecall_logs",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – Confirm both John and Sarah (parents, born in 1960s) appear in phone call logs, and Sarah is the more recent call
                # We don't check timestamps explicitly here, but we ensure both entities are retrieved from the previous tool call.
                Milestone(
                    snapshot_constraints=[
                        # Check John exists in phone logs result
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
                                            "receiver_address": {
                                                "value": "1234-5678-9102",
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
                # Milestone 2 – Retrieve phone call history to identify recent calls, including mom and dad
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
                                        "get_all_phone_calls",
                                        "search_phonecall_logs",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 3 – Confirm both John and Sarah (parents, born in 1960s) appear in phone call logs, and Sarah is the more recent call
                # We don't check timestamps explicitly here, but we ensure both entities are retrieved from the previous tool call.
                Milestone(
                    snapshot_constraints=[
                        # Check Sarah exists in phone logs result
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
                                            "receiver_address": {
                                                "value": "1234-5678-9111",
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
                # Milestone 4 – Optionally retrieve contacts to resolve messaging identifier for Sarah (e.g., phone or other handle)
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
                # Milestone 5 – The correct contact (Sarah Appleseed, Mom) is retrieved from contacts
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
                                                "value": "Sarah Appleseed",
                                                "partial": False,
                                            },
                                            "relationship": {
                                                "value": "Mother",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9111",
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
                        )
                    ]
                ),
                # Milestone 6 – A text message is sent to Sarah with the requested content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least Sarah must be a participant; allow extras (e.g., group messaging) if any
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9111",
                                                "sarah.appleseed@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "was great catching up with you. Want to come round for dinner next week?",
                                    "creation_datetime_iso": "2024-07-27T15:35:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_exact_match_similarity,
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
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.CALENDAR,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # phone logs retrieved → confirm John & Sarah are present
                (2, 3),  # phone logs retrieved → confirm John & Sarah are present
                (4, 5),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_17_b47b3a35-233d-401d-b539-6618bd9f8d5e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-28T15:30:00-07:00",
            is_read_time="2024-07-28T15:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send an event invitation to your mother. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Invite mom to dinner in my house tomorrow 7pm",
                },
            ],
            reasoning="The user wants to invite their mother to dinner at their house tomorrow at 7pm. First, I will need to figure out who the user is referring to by 'mother'. I go through the user's contacts and I see Sarah Appleseed listed as the user's mother there. The user is making this request on July 28th at 15:30. Therefore, I will create the event for Monday, July 29th, at 19:00 as requested by the user. There is no matching event at that specific time, so I will create a new one and invite Sarah Appleseed to participate.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. An event "Dinner with Mom" is created for Monday, July 29th, at 19:00. ',
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
                # Milestone 0 – Agent looks up the mother’s contact information
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
                # Milestone 1 – Verify that Sarah Appleseed (Mom) was actually returned
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
                                                "value": "Sarah Appleseed",
                                                "partial": False,
                                            },
                                            # Email or phone are optional here – full_name is sufficient to confirm the match
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
                # Milestone 2 – A new calendar event for dinner is created and Sarah is an attendee
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "dinner",  # will match substrings like "Family Dinner"
                                    "start_datetime_iso": "2024-07-29T19:00",  # ensure the time is 7 PM
                                    "attendees_names": [["Sarah Appleseed"]],
                                    "creation_datetime_iso": "2024-07-28T15:30:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare with the initial snapshot
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
            name="THEO_APPLESEED_17_20c936c4-75e7-4bfe-ba6d-bbc06c902797_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "phone_call",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T15:35:00-07:00",
            is_read_time="2024-07-27T15:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send your mom a message after your lovely chat with her. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send this message saying 'Hey mom, was great catching up with you. Want to come round for dinner next week?' to the person I was just on the phone with.",
                },
            ],
            reasoning="Right, the user wants to send 'Hey mom, was great catching up with you. Want to come round for dinner next week?' to the last person they were calling with. From their call log I can see the person they were just on the phone with is Sarah Appleseed. I can then send the user's message to Sarah Appleseed.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A message is sent to Sarah Appleseed on the 27th July at 15:35 saying, 'Hey mom, was great catching up with you. Want to come round for dinner next week?'",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "search_phonecall_logs",
                "get_all_phone_calls",
                "send_message",
            ],
            milestones=[
                # Milestone 0 –  The agent looks up recent phone calls to identify who was “just on the phone”
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
                                        "search_phonecall_logs",
                                        "get_all_phone_calls",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 –  Confirm that the phone-log result the agent relied on actually contains the
                #               most recent call with Sarah Appleseed
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
                                            "caller_address": {
                                                "value": "1234-5678-9101",
                                                "partial": False,
                                            },
                                            "receiver_address": {
                                                "value": "1234-5678-9111",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-27T15:00:00-07:00",
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
                            reference_milestone_node_index=0,  # parse the tool output from Milestone-0
                        )
                    ],
                ),
                # Milestone 2 –  A new message has been created / sent to Sarah that contains the requested text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require that Sarah is included among the conversation participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9111",  # Sarah's phone
                                                "sarah.appleseed@example.com",  # Sarah's email
                                            )
                                        ]
                                    ],
                                    "content": "Hey mom, was great catching up with you. Want to come round for dinner next week?",
                                    "creation_datetime_iso": "2024-07-27T15:35:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial DB state
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
                (0, 1),  # first retrieve phone logs → then confirm Sarah found
                (1, 2),  # after confirming, send the message
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_17_20c936c4-75e7-4bfe-ba6d-bbc06c902797_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "phone_call",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T15:35:00-07:00",
            is_read_time="2024-07-27T15:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send your mom a message after your lovely chat with her. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell my mom 'hey mom, was great catching up with you. Want to come round for dinner next week?'.",
                },
            ],
            reasoning="Okay so, the user wants to send a message with the content 'Hey mom, was great catching up with you. Want to come round for dinner next week?' to their mom. They have no explicit contact named 'mom' but I can see that Sarah Appleseed is put down as 'mother' in their contacts. I can deduce that this is whom the user is speaking about. I can then send this message to Sarah Appleseed.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A message is sent to Sarah Appleseed on the 27th July at 15:35 saying, 'Hey mom, was great catching up with you. Want to come round for dinner next week?'",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "search_phonecall_logs",
                "get_all_phone_calls",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent tries to identify “mom” in contacts
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
                # Milestone 1 – The returned contact list contains Sarah Appleseed (mom)
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
                                                "value": "Sarah Appleseed",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9111",
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
                # Milestone 2 – Message is created/sent to Mom with correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # One–on–one conversation containing mom’s address
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9111",
                                                "sarah.appleseed@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "Hey mom, was great catching up with you. Want to come round for dinner next week?",
                                    "creation_datetime_iso": "2024-07-27T15:35:00-07:00",
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
                    ],
                    guardrail_database_exclusion_list=[DatabaseNamespace.SANDBOX],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup ➜ verify mom found
                (1, 2),  # Mom found ➜ message sent
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_17_8050cf37-71ae-48f3-8d2c-253a5a802c11_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "phone_call",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T15:35:00-07:00",
            is_read_time="2024-07-27T15:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You had a good call with your mother.   You want to know how long the phone call was. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How long was the call with my mother?",
                },
            ],
            reasoning="The user is asking about the length of a voice call.\nI should find the specified contact and determine the length of the call through the call log.\nThe user has referred to their mother, I can see that Sarah Appleseed is tagged as mother in the user's contact list.\nI have found the call with Sarah Appleseed, started at 15:00.\nThe call lasted for 30 minutes.\nI can now inform the user that the call lasted for 30 minutes.",
            success_conditions=[
                {
                    "input_text": "1. The user is told that the length of their phone call with their mother, Sarah Appleseed, on July 27, 2024 at 15:00, was 30 minutes.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_phone_calls",
                "search_phonecall_logs",
            ],
            milestones=[
                # Milestone 0 – Agent consults phone-call history
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
                                        "search_phonecall_logs",
                                        "get_all_phone_calls",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – Returned phone-call entry matches mother (Sarah Appleseed) with 30-minute duration
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
                                            "receiver_address": {
                                                "value": "1234-5678-9111",
                                                "partial": False,
                                            },
                                            "duration_in_hms": {
                                                "value": "00:30:00",
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
                # Milestone 2 – Agent tells user the call was 30 minutes (or equivalent phrasing)
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
                                            "30 minutes",
                                            "half an hour",
                                            "00:30",
                                            "0:30",
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
            name="THEO_APPLESEED_17_5e603949-f195-4974-9b0d-8aa1b7aa619e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "contact",
                "phone_call",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T15:30:00-07:00",
            is_read_time="2024-07-27T15:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You just wrapped up a great catch-up call with your mother.   You want to send a message to her to schedule a future call. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a new message to whom I just had a call with saying when would you be free for another call",
                },
            ],
            reasoning='The user wants to send the text "when would you be free for another call?" to "the person they just had a call with". First, I\'ll look through the user\'s call history information to see any calls they made today (July 27th). I found one call on that day between the user and Sarah Appleseed, so she must be the person that the user wants to text. I\'ll add the user provided text as requested and check for confirmation before sending.',
            success_conditions=[
                {
                    "input_text": '1. A new message is sent to Sarah Appleseed ("1234-5678-9111") with the text "when would you be free for another call?"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_phone_calls",
                "search_phonecall_logs",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent looks up who the last call was with (or otherwise identifies the mother)
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
                                        "search_phonecall_logs",
                                        "get_all_phone_calls",
                                        "search_contacts",
                                        "get_all_contacts",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – The tool output includes the recent call with Sarah Appleseed
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
                                            "receiver_address": {
                                                "value": "1234-5678-9111",
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
                # Milestone 2 – A new message is created and sent to Sarah Appleseed with the requested text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require that Sarah is one of the participants; self contact may also appear
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9111",
                                                "sarah.appleseed@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "when would you be free for another call",
                                    "creation_datetime_iso": "2024-07-27T15:30:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
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
                (0, 1),  # Tool use → verify Sarah found
                (1, 2),  # Sarah identified → message sent
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_17_d7a247e9-993a-4d9f-85d5-16123a73cdb8_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "contact",
                "messaging",
                "phone_call",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T15:35:00-07:00",
            is_read_time="2024-07-27T15:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send your mom a message after your lovely chat with her. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send this message saying 'It was great catching up with you. Want to come round for dinner next week?' to her, the one I was just on the phone with.",
                },
            ],
            reasoning="Right, the user wants to send 'It was great catching up with you. Want to come round for dinner next week?' to the last person they were calling with with female pronoun 'her'. From their call log I can see the person they were just on the phone with is Sarah Appleseed. I can then send the user's message to Sarah Appleseed.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A text message is sent to Sarah Appleseed saying, 'It was great catching up with you. Want to come round for dinner next week?'",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_phone_calls",
                "search_phonecall_logs",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent looks up recent phone calls to identify "the person I was just on the phone with"
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
                                        "get_all_phone_calls",
                                        "search_phonecall_logs",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Confirms that the recent call with Sarah Appleseed (mom) was retrieved from phone logs
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
                                            # We only need to know that a call with Sarah exists
                                            "receiver_address": {
                                                "value": "1234-5678-9111",
                                                "partial": False,
                                            },
                                            "call_type": {
                                                "value": "outgoing",
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
                # Milestone 2 – A text message is sent to Sarah with the requested content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Participants must include Sarah's phone number; Theo (self) may also be present.
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9111",
                                                "sarah.appleseed@example.com",
                                            ),
                                            (
                                                "1234-5678-9101",
                                                "theo.appleseed@example.com",
                                            ),
                                        ]
                                    ],
                                    "content": "was great catching up with you. Want to come round for dinner next week",
                                    "creation_datetime_iso": "2024-07-27T15:35:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # At least one identifier for Sarah and Theo must be present; no unrelated participants
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.CONTACT,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Phone log lookup → confirm Sarah call
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_17_20caff90-3427-4c7c-b3cc-17a6edd1a217_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "THEO_APPLESEED",
                "plot_17",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T16:00:00-07:00",
            is_read_time="2024-07-27T16:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You and your mother had a disagreement during your call and you want to apologize to her via texting. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell Sarah Appleseed this: \"Mom, I'm so sorry! I shouldn't have gotten so angry.",
                },
            ],
            reasoning="The user wants to send a message.\nFirst, I should find the named contact, I can see only one Sarah Appleseed in the user's contacts. \nI will go ahead and compose the message as requested. A message will be sent to Sarah Appleseed stating \"Mom, I'm so sorry! I shouldn't have gotten so angry.\"\nI should inform the user.\n",
            success_conditions=[
                {
                    "input_text": "1. A message is sent to Sarah Appleseed stating \"Mom, I'm so sorry! I shouldn't have gotten so angry\"",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["search_contacts", "get_all_contacts", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up the mother’s contact information
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
                # Milestone 1 – Verify Sarah Appleseed (Mom) was returned by the previous contact search
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
                                                "value": "Sarah Appleseed",
                                                "partial": False,
                                            },
                                            # We only need to confirm the correct person—not every field
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
                # Milestone 2 – A new outgoing message to Mom containing an apology is added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require Mom to be included among the participants; allow extras like the user’s own address
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9111",
                                                "sarah.appleseed@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "sorry",
                                    "creation_datetime_iso": "2024-07-27T16:00:00-07:00",
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_17_20caff90-3427-4c7c-b3cc-17a6edd1a217_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T16:00:00-07:00",
            is_read_time="2024-07-27T16:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You and your mother had a disagreement during your call and you want to apologize to her via texting. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send an apology to my mom: \"Mom, I'm so sorry. I shouldn't have gotten so angry.\"",
                },
            ],
            reasoning="The user wants to send a message.\nFirst, I should find the named contact, the user has referred to as their mom.\nI can see that Sarah Appleseed is tagged as mother in the user's contacts.\nI will go ahead and compose the message as requested. A message will be sent to Sarah Appleseed stating \"Mom, I'm so sorry! I shouldn't have gotten so angry.\"\nI should inform the user.\n",
            success_conditions=[
                {
                    "input_text": "1. A message is sent to Sarah Appleseed stating \"Mom, I'm so sorry! I shouldn't have gotten so angry\"",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["search_contacts", "get_all_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up mom’s contact information
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
                # Milestone 1 – Lookup result includes Sarah Appleseed (Mom)
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
                                                "value": "Sarah Appleseed",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9111",
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
                # Milestone 2 – New outgoing message with apology is created and addressed to Mom
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least one identifier for Mom must appear in the participants list
                                    "participants_addresses": [
                                        [
                                            (
                                                "1234-5678-9111",
                                                "sarah.appleseed@example.com",
                                                "Sarah Appleseed",
                                            )
                                        ]
                                    ],
                                    "content": "sorry",
                                    "creation_datetime_iso": "2024-07-27T16:00:00-07:00",
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_17_d7a247e9-993a-4d9f-85d5-16123a73cdb8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "contact",
                "messaging",
                "phone_call",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T15:35:00-07:00",
            is_read_time="2024-07-27T15:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to send your mom a message after your lovely chat with her. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell my mom 'was great catching up with you. Want to come round for dinner next week?'.",
                },
            ],
            reasoning="Okay so, the user wants to send a message with the content 'was great catching up with you. Want to come round for dinner next week?' to their mom. They have no explicit contact named 'mom' but I can see that Sarah Appleseed is put down as 'mother' in their contacts. I can deduce that this is whom the user is speaking about. I can then send this message to Sarah Appleseed.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A text message is sent to Sarah Appleseed saying, 'was great catching up with you. Want to come round for dinner next week?'",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_phone_calls",
                "search_phonecall_logs",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent looks up mom's contact information (needs to resolve "my mom" → Sarah Appleseed)
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
                # Milestone 1 – Confirms that Sarah Appleseed (Mom) was retrieved from contacts in Milestone 0
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
                                                "value": "Sarah Appleseed",
                                                "partial": False,
                                            },
                                            "relationship": {
                                                "value": "Mother",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "1234-5678-9111",
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
                # Milestone 2 – A text message is sent to Sarah with the requested content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Sarah's address should appear in the participants of the conversation
                                    "participants_addresses": [
                                        [
                                            (
                                                "sarah.appleseed@example.com",
                                                "1234-5678-9111",
                                            )
                                        ]
                                    ],
                                    "content": "was great catching up with you. Want to come round for dinner next week?",
                                    "creation_datetime_iso": "2024-07-27T15:35:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                # Require that Sarah is included; allow extras like the user's own number if present
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                # Content should match the user's requested message text (allow slight variations but prefer exact)
                                "content": column_rouge_l_similarity,
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
                (0, 1),  # Contact lookup → confirm Sarah (Mom)
                (1, 2),  # Confirmed mom contact → send message to her
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_17_8050cf37-71ae-48f3-8d2c-253a5a802c11_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "contact",
                "phone_call",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T15:35:00-07:00",
            is_read_time="2024-07-27T15:35:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You had a good call with your mother.   You want to know how long the phone call was. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How long was my voice call with Sarah Appleseed?",
                },
            ],
            reasoning="The user is asking about the length of a voice call with Sarah Appleseed.\nI should find the specified contact and determine the length of the call through the call log.\nI have found the call with Sarah Appleseed, which started at 15:00 and ended at 15:30.\nTherefore, the call lasted for 30 minutes.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that the length of the phone call with their mother, Sarah Appleseed, on July 27, 2024 at 15:00 was 30 minutes.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_phone_calls",
                "search_phonecall_logs",
            ],
            milestones=[
                # Milestone 0 – The agent consults the phone-log database
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
                                        "search_phonecall_logs",
                                        "get_all_phone_calls",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – The returned tool output contains the correct call entry
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
                                            "receiver_address": {
                                                "value": "1234-5678-9111",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-27T15:00:00-07:00",
                                                "partial": False,
                                            },
                                            "duration_in_hms": {
                                                "value": "00:30:00",
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
                            reference_milestone_node_index=0,  # depends on Milestone 0’s tool call
                        )
                    ]
                ),
                # Milestone 2 – The agent tells the user the call lasted 30 minutes
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
                                            "30 minutes",
                                            "30 min",
                                            "00:30:00",
                                            "half an hour",
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
            name="THEO_APPLESEED_17_5e603949-f195-4974-9b0d-8aa1b7aa619e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_17",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "contact",
                "phone_call",
                "messaging",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T15:30:00-07:00",
            is_read_time="2024-07-27T15:30:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You just wrapped up a great catch-up call with your mother.   You want to send a message to her to schedule a future call. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Message mom asking when would you be free for another call?",
                },
            ],
            reasoning="The user wants to send a message to their mom. First I'll find the contact noted as mom in contacts. Going through the user's contact, I find Sarah Appleseed listed as the user's mother. I'll start a new message to her and add the text \"when would you be free for another call?\" as requested, before checking for confirmation from the user.",
            success_conditions=[
                {
                    "input_text": '1. A new message is sent to Sarah Appleseed with the text "when would you be free for another call?"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_phone_calls",
                "search_phonecall_logs",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent queries contacts (either by search or listing all)
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
                # Milestone 1 – Confirm Sarah Appleseed is present in the returned contact results
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
                                                "value": "Sarah Appleseed",
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
                # Milestone 2 – A new message is sent to Mom with the requested text
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
                                                "1234-5678-9111",
                                                "sarah.appleseed@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "when would you be free for another call?",
                                    "creation_datetime_iso": "2024-07-27T15:30:00-07:00",
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
                (0, 1),
                (1, 2),
            ],
        ),
    ]
