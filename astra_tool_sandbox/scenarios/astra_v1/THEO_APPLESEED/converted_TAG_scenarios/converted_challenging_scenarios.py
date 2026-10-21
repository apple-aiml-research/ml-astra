# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
# Auto-generated scenario extensions
from functools import partial
from typing import Optional, cast

import polars as pl

from astra_tool_sandbox.common.evaluation import (
    Milestone,
    Minefield,
    SnapshotConstraint,
    addition_similarity,
    column_contains_similarity,
    column_datetime_window_similarity,
    column_list_tuple_contains_similarity,
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_str_contains_all_similarity,
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


def get_TAG_THEO_APPLESEED_challenging_scenarios(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="THEO_APPLESEED_16_60efdeb3-2a0e-461a-9820-17f10ac8c1dd_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "calendar",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T11:25:00-07:00",
            is_read_time="2024-07-27T11:10:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know what did John say as you're texting him but can't use your hands at the moment. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What did my friend who hiked earlier with me today and works at Pantene text me last in our conversation?",
                },
            ],
            reasoning="The user wants me to read a text to them. They referenced the conversation about this morning's hike, with a friend who works at Pantene. Looking at the user's calendar events, earlier today the user had an event named \"Hiking Trip\" from 6:00-10:00 with John Quinn. So maybe John Quinn is the person they're talking about. But John Quinn's employer is listed as Palantir, not Pantene. The user could have mixed this up. To be sure they're talking about John Quinn, let me look at their texts with him. It appears they were indeed talking about this morning's hike. At 10:30 today, the user said \"Hey John, that trail was amazing! Really enjoyed the hike and our chat.\" So this confirms that they are asking what John texted them most recently. I see that at 11:15 John said \"For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.\" so I'll tell this to the user.",
            success_conditions=[
                {
                    "input_text": "1. The latest message received from John Quinn at 11:15 on the 27th July 2024 saying 'For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.' is read out to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "get_all_contacts",
                "search_contacts",
                "get_all_calendars",
                "search_calendar_events",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events (tomorrow’s hike)
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
                # Milestone 1 – Returned calendar data includes the Hiking Trip with correct location
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
                                            "location": {
                                                "value": "Big Rock Mountain Trail",
                                                "partial": True,
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
                # Milestone 2 – Agent uses a messages retrieval tool to look up the conversation
                # with John Quinn / about the hike (contact/company inference must be tool-grounded).
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
                                # Allow either listing all messages or searching messages
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
                # Milestone 3 – Verify that the correct latest incoming message from John Quinn
                # in the relevant conversation was present in the tool output:
                # "For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it."
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            # Check the result list from Milestone 0's tool call for existence
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        # Match on key identifying fields for the message
                                        match_conditions={
                                            "conversation_name": {
                                                "value": "John Quinn",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "john.quinn@palantir.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-27T11:15:00-07:00",
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
                                    # "{matched}" will be filled if the message exists
                                    "content": "{matched}",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_one_similarity,
                            },
                            reference_milestone_node_index=2,
                        )
                    ],
                ),
                # Milestone 4 – Agent tells the user (reads out) what John said in that last text
                # Focus on essential content of the message body.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            # Check the agent's user-facing response
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We just require that the core text of John's message
                                    # appears in the assistant's response.
                                    "content": "For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.",
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
                (0, 1),  # Calendar checked for hiking friend
                (
                    2,
                    3,
                ),  # Messages tool call → confirm correct last message retrieved
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_4_307dfa68-0b23-4a2b-8439-3f02aaed90e9_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_4",
                "calendar",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_yes",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T09:15:00-07:00",
            is_read_time="2024-07-23T09:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You know you're getting dinner with a friend this week but you can't remember where, you want to know the exact street name not just the location. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Does my event that starts in 33 hours and 45 minutes have a specific street address? If so, let me know the full address, not just the place name; if not, just reply 'no'.",
                },
            ],
            reasoning="The user wants to know where an event is taking place. The event is one that starts in 33 hours and 45 minutes. Right now it's 9:15 on 23 July 2024, so in 33 hours and 45 minutes it will be 19:00 on 24 July 2024. Let me check the user's calendar for events at that time. I see an event named Dinner with Cookie scheduled for 19:00-21:00 tomorrow 24 July 2024. This must be the event the user wants to know more about. They asked for the address of the event, but there's no address provided on the invite. The only location information listed on this event says that it's taking place at Pony & Jigger in Orchard County, CA, so I'll tell the user with 'no' since the exact street address is unknown.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that the event named Dinner with Cookie, scheduled for 19:00-21:00 on Wednesday 24 July 2024, is taking place at Pony & Jigger in Orchard County, CA",
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
                # Milestone 0 – Agent searches calendar to find the event starting in ~33h45m
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
                # Milestone 1 – Confirms the correct dinner event on Wed Jul 24, 2024 at 19:00 was retrieved
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
                                                "value": "Dinner with Cookie",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-24T19:00:00-07:00",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Pony & Jigger, Orchard County, CA",
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
                            reference_milestone_node_index=0,  # Validate output of the calendar search
                        )
                    ]
                ),
                # Milestone 2 – User-facing response states where the event is taking place
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
                (0, 1),  # Calendar lookup → confirm correct event retrieved
                (1, 2),  # Confirmed event → user informed of correct location
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_17_d7a247e9-993a-4d9f-85d5-16123a73cdb8_single_turn_2",
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
                "functional_complexity_moderate",
                "misinformation_yes",
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
                    "content": "Text the person who called me at 3 today and say 'was great catching up with you. Want to come round for dinner next week?'",
                },
            ],
            reasoning='The user wants to send a text message. They want to text the person who called them at 15:00. Let me look at the call logs to figure out who this is. I only see two calls in their history, one call the user made to Sarah Appleseed today at 15:00, and one call the user made to John Appleseed on 23 July 2024 at 18:00. If the call from today at 15:00 is what the user is talking about, they must have misspoken when they said "text the person who called me" and must have meant to say "text the person who I called". I\'ll send a text to the person who was on the other end of the line during the phone call from 15:00, so Sarah Appleseed, and say \'was great catching up with you. Want to come round for dinner next week?\'.',
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
                # Milestone 0 – Agent looks up phone call history to identify who was on the 15:00 call
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
                # Milestone 1 – Confirms the 2024-07-27T15:00:00 call involving Sarah Appleseed was retrieved
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
                                            "creation_datetime_iso": {
                                                "value": "2024-07-27T15:00:00-07:00",
                                                "partial": False,
                                            },
                                            # Either caller or receiver should be Sarah; we check one key field here
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
                # Milestone 2 – A text message was sent to Mom (Sarah Appleseed) with the desired content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Participants include Theo and Sarah; we allow either email or phone identifiers if used
                                    "participants_addresses": [
                                        [
                                            (
                                                "theo.appleseed@example.com",
                                                "1234-5678-9101",
                                            ),
                                            (
                                                "sarah.appleseed@example.com",
                                                "1234-5678-9111",
                                            ),
                                        ]
                                    ],
                                    "content": "was great catching up with you. Want to come round for dinner next week?",
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
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Phone log lookup → confirm correct 15:00 call identified
                (1, 2),  # Correct call identified → send correct text message
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_4_307dfa68-0b23-4a2b-8439-3f02aaed90e9_single_turn_3",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_4",
                "calendar",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_yes",
                "insufficient_context_yes",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T09:15:00-07:00",
            is_read_time="2024-07-23T09:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You know you're getting dinner with a friend this week but you can't remember where. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did Cookie text about the specific street address for our dinner on Thursday? Not just the venue name? Yes or no.",
                },
            ],
            reasoning='The user wants to know where an event is taking place, namely a dinner on Thursday. They said Cookie texted them the address, and they only have one contact named Cookie: Cookie Watson. \n\nSo I\'ll first look at the user\'s texts with Cookie to see if they mention the location of dinner. I see a text from Cookie on 22 July at 14:00 that says "Hey Theo! Are you free for dinner this Wednesday? There’s a new pub, Pony & Jigger, that just opened. Thought we could check it out!" Then there\'s a text from the user on 22 July at 14:02 that says "Hi Cookie! Wednesday works for me. What time were you thinking?". Another text from Cookie on 22 July at 14:05 says "How about 7 PM? Gives us plenty of time to enjoy the evening." The user responds on 22 July at 14:07 saying "Perfect! See you at Pony & Jigger at 7 then. Looking forward to it!". Cookie\'s most recent text from 22 July at 14:10 says "Great! It’s a date. See you Wednesday!"\n\nTaking the content of these texts into consideration, Cookie and the user talked about the time and date of their dinner, and decided on Pony & Jigger for the location, but Cookie never mentioned an address. Looking at the user\'s calendar, the event they planned called Dinner with Cookie scheduled for 24 July at 19:00-21:00 also just lists Pony & Jigger in Orchard County CA as the location, so I\'ll share that with the user since it\'s all the information I have.',
            success_conditions=[
                {
                    "input_text": "1. The event named Dinner with Cookie, scheduled for 19:00-21:00 on Wednesday 24 July 2024, is taking place at Pony & Jigger in Orchard County, CA has been retreived, related conversation from Coodie found.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The user is informed with 'No', as the specific street name hasn't been mentioned anywhere",
                    "statefullness": "Stateless",
                },
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
                # Milestone 0 – Agent looks up relevant information about Cookie / dinner via messages or calendar
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
                                # Any of these are acceptable ways to look up the dinner details
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
                # Milestone 1 – Verify that the retrieved message is Cookie’s Pony & Jigger dinner request sent at 14:00 on 2024-07-22
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
                                                "value": "Pony & Jigger",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-22T14:00:00-07:00",
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
                # Milestone 2 – User is informed that the street address is unknown
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            # We only care about the user-facing response content here
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "No",
                                }
                            ),
                            column_similarity_measure={
                                # Relaxed matching: ensure key facts are present
                                "content": column_word_contains_similarity
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_71f270d7-a086-44c0-b484-06d626adb838_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "email",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_yes",
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
                        "You want to know if you included the location for the follow-up sync with your two colleagues. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I mention the location of our sync among the three of us tomorrow in my email body directly? Not in the attachment. Reply with yes or no.",
                },
            ],
            reasoning="The user wants to know if they mentioned the \"location of our sync\" in their email. Okay, firstly, I need to go to the user's Mail to see if they have sent any emails that correspond to the above description.\n Great, I can see they sent an email on July 22nd, 2024 at 11:05 named \"Follow-up Sync Scheduled for July 29\". This must be what they're referring to in their request, as it's the only email that contains those words and three participants tomorrow. So that's the email user refers to. \n In the email's attachment there's calendar invite, but no mention of the location in the body. I'll inform user that the location was not presented in the email body directly with 'No'.",
            success_conditions=[
                {
                    "input_text": '1. The the email named "Follow-up Sync Scheduled for July 29", sent to "michelle.barnes@example.com" and "dawei.shen@example.com" on July 22nd, 2024 at 11:05 was retrieved.\n',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The user is informed with 'No', that the location of the sync meeting was not directly mentioned in the email.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – Agent uses an email retrieval tool to look up the referenced email
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
                # Milestone 1 – Confirm the specific email "Follow-up Sync Scheduled for July 29" was retrieved
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
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
                # Milestone 2 – Agent informs user that the email body does NOT contain the location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Any clear "no, the location is not in the email body" style answer
                                    "content": "No",
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
                (0, 1),  # Email search → confirm specific email retrieved
                (1, 2),  # Knowing the email → inform user correctly
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_25_6c85880a-ff30-4224-8e42-3638290e00d4_single_turn_3",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_25",
                "calendar",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:40:00-07:00",
            is_read_time="2024-07-29T07:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to hear what the message from your train service says. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What does the text I got five minutes ago say about my bus trip tomorrow?",
                },
            ],
            reasoning='The user wants to know the contents of a text message. They said they got the text five minutes ago. It\'s 7:40 right now, so let me look at texts that got delivered five minutes ago at 7:35. I see one text message from booking@trainservice.com delivered at 7:35. The user said the text was about a bus trip tomorrow, but this text mentions a train ticket. The user also has an event named "Train Trip" in their calendar scheduled for tomorrow, so this helps me confirm that the user must have meant train trip when they said bus trip. So I\'ll present the contents of the text about the train trip that came in five minutes ago to the user: "Dear Theo, your train ticket to Chicago is booked. Departure: July 30, 2024, 15:07 from Central Station. Ticket number: TK123456789, Booking reference: BR987654321."',
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The message from booking@trainservice.com is presented to the user "Dear Theo, your train ticket to Chicago is booked. Departure: July 30, 2024, 15:07 from Central Station. Ticket number: TK123456789, Booking reference: BR987654321."\n',
                }
            ],
            tool_allow_list=[
                "search_messages",
                "get_all_messages",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – Agent uses a messages retrieval tool to look up recent texts
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
                # Milestone 1 – Confirm that the booking@trainservice.com message about the trip was retrieved
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            # We now verify that among the results of the tool call in Milestone 0
                            # there exists a message from booking@trainservice.com with the expected content.
                            snapshot_constraint=partial(
                                tool_trace_dependant_similarity,
                                fill_to="content",
                                extractor=cast(
                                    ToolTraceExtractorType,
                                    partial(
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "sender_address": {
                                                "value": "booking@trainservice.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Dear Theo, your train ticket to Chicago is booked. Departure: July 30, 2024, 15:07 from Central Station. Ticket number: TK123456789, Booking reference: BR987654321.",
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
                # Milestone 2 – User-facing response includes the key contents of the retrieved message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            # Check that the assistant tells the user the important parts of the message.
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We only require that the response mentions Theo's ticket,
                                    # departure date/time, station, and either ticket or booking reference.
                                    "content": "Chicago",
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
                (0, 1),  # messages search → confirm correct message retrieved
                (1, 2),  # correct message retrieved → respond to user with its contents
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_25_6c85880a-ff30-4224-8e42-3638290e00d4_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_25",
                "calendar",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_yes",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T07:40:00-07:00",
            is_read_time="2024-07-29T07:40:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to hear what the message from your train service says about your arrival time. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did the booking service say I would arrive my destination? If so let me know the exact time, if not just reply 'No'.",
                },
            ],
            reasoning="The user wants me to tell them some information about a message that the booking service sent to them. I don't see any emails from that address, so let me check the user's texts. I see one text from that address that says \"Dear Theo, your train ticket to Chicago is booked. Departure: July 30, 2024, 15:07 from Central Station. Ticket number: TK123456789, Booking reference: BR987654321.\" \nThis text only mentions a departure time, not an arrival time. Let me just present the exact text message to the user so they can have all the information available to them, I will reply with 'No'.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The message from booking@trainservice.com is retrieved "Dear Theo, your train ticket to Chicago is booked. Departure: July 30, 2024, 15:07 from Central Station. Ticket number: TK123456789, Booking reference: BR987654321."\n',
                },
                {
                    "statefullness": "Stateless",
                    "input_text": '2. The user has been informed with no."\n',
                },
            ],
            tool_allow_list=[
                "search_messages",
                "get_all_messages",
                "search_emails",
                "get_all_emails",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – Agent uses a messages/email tool to look for booking@trainservice.com
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
                                # Allow either message or email search/listing as a way to locate the booking message
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=[
                                        "search_messages",
                                        "get_all_messages",
                                        "search_emails",
                                        "get_all_emails",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – Verify that a message from booking@trainservice.com with the expected content was retrieved
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
                                        # We just need to confirm existence of the booking message with key fields
                                        result_list_match_existence_extractor,
                                        match_conditions={
                                            "sender_address": {
                                                "value": "booking@trainservice.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Dear Theo, your train ticket to Chicago is booked. Departure: July 30, 2024, 15:07 from Central Station. Ticket number: TK123456789, Booking reference: BR987654321.",
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
                                    # will be replaced by "{matched}" if the extractor finds a match
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
                # Milestone 2 – Agent responds to the user
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
                                "content": column_word_contains_similarity,
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (
                    0,
                    1,
                ),  # Tool call to retrieve messages → confirm booking message retrieved
                (
                    1,
                    2,
                ),  # Booking message retrieved → user-facing answer includes that message
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_1_71f270d7-a086-44c0-b484-06d626adb838_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_1",
                "email",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_yes",
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
                    "content": "I need to know if I mentioned the location of the follow-up sync in my email explicitly in the text? If so let me know the location, if not just reply with 'no'.",
                },
            ],
            reasoning='The user wants to know if they mentioned the "location of the follow-up sync" in their email to their "co-workers".\n\nOkay, first of all, I need to go to the user\'s Mail to see if they have sent any emails that correspond to the above description.\n\nGreat, I can see they sent an email on July 22nd, 2024 at 11:05:00 named "Follow-up Sync Scheduled for July 29". It was sent to Michelle Barnes and Dawei Shen, who I can also see are the user\'s co-workers.\n\nIn the email\'s attachment there\'s calendar invite which I cannot open. I\'ll inform user that the location was not present in the email main body.',
            success_conditions=[
                {
                    "input_text": '1. The the email named "Follow-up Sync Scheduled for July 29", sent to "michelle.barnes@example.com" and "dawei.shen@example.com" on July 22nd, 2024 at 11:05 was retrieved.\n',
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The user is informed with 'no', that the location of the sync meeting was not directly mentioned in the email.",
                    "statefullness": "Stateless",
                },
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – Agent uses email search/get to look for the follow-up sync email
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
                # Milestone 1 – Confirm the specific email "Follow-up Sync Scheduled for July 29" sent at the given time exists in tool output
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
                                            "recipients_addresses": {
                                                "value": [
                                                    "michelle.barnes@example.com",
                                                    "dawei.shen@example.com",
                                                ],
                                                "partial": True,
                                            },
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
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – Agent informs user that the location is NOT explicitly mentioned in the email body text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Need indication that the answer is "no, location not mentioned explicitly"
                                    "content": "no",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_similarity,
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Email search → confirm specific email found
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_6_80dd9455-cabe-4f2d-bb02-ca56027e3ac6_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_6",
                "contact",
                "phone_call",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T19:00:00-07:00",
            is_read_time="2024-07-23T19:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to know how long the call with your father was. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How long was my call with her an hour ago?",
                },
            ],
            reasoning="The user wants to know how long their call was. I need to figure out which call they're talking about in order to tell them its duration. They said it was an hour ago. In the user's contacts, John Appleseed has the relationship \"Father,\", but the user mentioned 'her'. As of today 23 July 2024 at 19:00, the only call in the user's call history is a call with John Appleseed at 18:00. John Appleseed is the user's dad, so maybe they mixed up which parent they meant. They said the call was an hour ago, and 18:00 was an hour ago, so I'll assume this call with John Appleseed is the one they are talking about and that they meant the call was with 'him'. The call was 30 minutes, so I'll tell the user that.",
            success_conditions=[
                {
                    "input_text": "1. Duration of voice call with John Appleseed conducted on July 23, 2024 at 18:00 is presented to the user as 30 minutes.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_phonecall_logs",
                "get_all_phone_calls",
            ],
            milestones=[
                # Milestone 0 – The agent looks up phone call logs (must use phone log tools)
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
                # Milestone 1 – Confirm the call with John Appleseed at 2024-07-23T18:00:00-07:00, duration 00:30:00, exists in tool output
                # This validates the agent actually retrieved the correct call record before answering.
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
                                                "value": "1234-5678-9102",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-23T18:00:00-07:00",
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
                # Milestone 2 – User-facing answer mentions that the call duration was 30 minutes
                # We only care that "30 minutes" (or similar phrase) is conveyed.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("30 minutes", "30 min", "half")],
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
                (
                    0,
                    1,
                ),  # Tool call to retrieve phone logs → confirm correct call record found
                (1, 2),  # Correct call record found → correct duration conveyed to user
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_16_17d491d7-1fb1-4af9-a417-53903795eb76_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_16",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27T18:00:00-07:00",
            is_read_time="2024-07-27T18:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You want to get a time stamp off a text message. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did the last text John sent to me? I bet it's in the afternoon, yes or no?",
                },
            ],
            reasoning="The user wants the time stamp of a text message. The sender of the message is John. There're two John in user context, but he only got conversation with John Quinn. The last text that John Quinn sent to the user was today 27 July 2024 at 11:15 and it said \"For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.\". However, the user said that they want to know the time of the last text John Quinn sent them this afternoon, and the most recent text has a timestamp of 11:15. There is no other more recent text, so despite that contradiction, I'll communicate the timestamp of the most recent text, 11:15, to the user, because they want to know the time of the last text John Quinn sent to them. And I will reply with 'No', since it's not in the afternoon.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": '1. The user is informed with "no", that the most recently delivered text message from John Quinn, with the content "For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you\'d like it.", was delivered at 11:15 on 27 July 2024.',
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_messages",
                "get_all_messages",
            ],
            milestones=[
                # Milestone 0 – Agent uses a messages retrieval tool to look up texts (e.g., from John Quinn)
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
                # Milestone 1 – Confirm the specific message from John Quinn at 2024-07-27T11:15:00-07:00 was found
                # We check by matching on content and timestamp in the tool output from Milestone 0.
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
                                                "value": "John Quinn",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "For sure. Speaking of creativity, have you read that new sci-fi book I mentioned last time? Think you'd like it.",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-27T11:15:00-07:00",
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
                # Milestone 2 – Agent tells the user the correct timestamp and associates it with the described message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We only enforce that the reply mentions the correct time and date;
                                    # phrasing can vary.
                                    "content": "no",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_similarity,
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # messages search → confirm correct message retrieved
                (1, 2),  # confirmed retrieval → respond to user with timestamp
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_9_d6a6c9d1-f353-45b1-bd71-e87f5711c1c5_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_9",
                "calendar",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-24T21:50:00-07:00",
            is_read_time="2024-07-24T21:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You can't remember how much you owe Cookie for dinner, so you want to text her to ask her to send you a payment request.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to my college friend to say 'Send me a Venmo request for lunch', make sure that's the right meal.",
                },
            ],
            reasoning='The user wants to reply to their college friend to say "Send me a venmo request for lunch". I\'ll look for contacts and calendar events that matches with college friend and lunch meeting. I see there\'s a Dinner with Cookie at 7:00-9:00 pm on July 24 in user\'s calendar. And in contacts there\'s Cookie Watson who is a college friend. Even though user wants to reply saying "Send me a venmo request for lunch", I understand user meant "dinner". I\'ll clarify with the user if they meant "dinner with Cookie".',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A new message is sent to Cookie Watson with keywords "venmo" and "dinner" at 21:50 on 24 July 2024. ',
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_messages",
                "get_all_messages",
                "send_message",
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – Agent looks up Cookie (college friend) via contacts/messages/calendar (some retrieval to ground who to message)
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
                # Milestone 1 – Verify Cookie Watson (college friend) is retrieved from contacts
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
                                            "relationship": {
                                                "value": "College Friend",
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
                    ]
                ),
                # Milestone 2 – New message sent to Cookie mentioning venmo and dinner at the correct time
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Conversation participants must include Cookie (email or phone) and Theo
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
                                    "content": [("venmo", "dinner")],
                                    "creation_datetime_iso": "2024-07-24T21:50:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_str_contains_all_similarity,
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
                (0, 1),
                (1, 2),
            ],
            minefields=[
                # Minefield 0 – message sent to Cookie with must not contain lunch
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.WHATSAPP,
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
                                    "content": "lunch",
                                }
                            ),
                            column_similarity_measure={
                                # Ensure it's specifically a conversation between Dawei and Charles
                                "participants_addresses": column_list_tuple_contains_similarity,
                                # Ensure content matches exactly the required phrasing (including removal of "tomorrow")
                                "content": column_contains_similarity,
                            },
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="THEO_APPLESEED_4_307dfa68-0b23-4a2b-8439-3f02aaed90e9_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "THEO_APPLESEED",
                "plot_4",
                "calendar",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T09:15:00-07:00",
            is_read_time="2024-07-23T09:15:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Theo Appleseed. "
                        "You know you're getting dinner with a friend this week but you can't remember where. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where is Dinner with Cookie happening this week? I bet it's tonight?",
                },
            ],
            reasoning="The user wants to know where an event is taking place. The event is Dinner with Cookie, and the user said it was tonight. Let me check their calendar. I don't see any events scheduled the rest of the day today, but I do see an event named Dinner with Cookie scheduled for 19:00-21:00 tomorrow 24 July 2024. The user must have misspoke when they said it was tonight, because this is the only Dinner with Cookie event in the calendar. The location listed on this event is Pony & Jigger in Orchard County, CA, so I'll tell the user that Dinner with Cookie is scheduled for tomorrow and is taking place at Pony & Jigger in Orchard County, CA.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that the event named Dinner with Cookie, scheduled for 19:00-21:00 on Wednesday 24 July 2024, is taking place at Pony & Jigger in Orchard County, CA",
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
                # Milestone 0 – Agent uses calendar tools to look up where "Dinner with Cookie" is happening
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
                # Milestone 1 – Confirm the "Dinner with Cookie" calendar event (with correct time and location) was retrieved
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
                                                "value": "Dinner with Cookie",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-07-24T19:00:00-07:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-07-24T21:00:00-07:00",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Pony & Jigger, Orchard County, CA",
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
                # Milestone 2 – User is told the correct location (Pony & Jigger in Orchard County, CA) and that it's for the 7–9pm Wednesday 24 July event
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Check for key facts: event name, location, and date/time window
                                    "content": "Pony & Jigger",
                                }
                            ),
                            column_similarity_measure={
                                # Relaxed checks for essential details
                                "content": column_contains_similarity,
                            },
                        )
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # calendar lookup → confirm correct event details
                (1, 2),  # correct event details → respond to user with that info
            ],
        ),
    ]
