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
    column_exact_match_similarity,
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_rouge_l_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_any_similarity,
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


def get_TAG_EMILY_ROSE_challenging_scenarios(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="EMILY_ROSE_10_ba4d2d19-9463-421f-a14f-daf2c4f6ac2c_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_10",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T16:25:00-08:00",
            is_read_time="2024-12-07T16:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to dictate a reply to Linda saying that you will be a little late to the holiday party because you have to feed your goldfish. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to Linda's text from 16:15 where she told me what time she'd be coming to the party and say \"I will be a little late to the holiday party because I have to feed my goldfish.\"",
                },
            ],
            reasoning="The user wants to reply to a text from Linda. They must mean Linda Rose, because that's the only Linda in their contacts. They said that Linda texted them at 16:15 telling them what time she'd be coming to the party, but I only see a text from Linda from 16:15 that says \"That should be all. See you soon at the party!\". The user must have misremembered the content of this text. Regardless, they want to reply to the message from 16:15, so I'll reply to the one that says \"That should be all. See you soon at the party!\" because that's the time it came in and there's no text that mentions what time Linda will be at the party. I'll write the reply to Linda that they asked me to: \"I will be a little late to the holiday party because I have to feed my goldfish.\"",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A reply message is sent to Linda saying"I will be a little late to the holiday party because I have to feed my goldfish.',
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_messages",
                "get_all_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent locates the relevant message from Linda around 16:15
                Milestone(
                    snapshot_constraints=[
                        # Verify a message search/list tool was used
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
                    ]
                ),
                # Milestone 1 – Verify that the retrieved messages include Linda's 16:15 party message
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
                                            # We match on sender and a key phrase in the content
                                            "sender_address": {
                                                "value": "linda.rose@homemadetreats.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "See you soon at the party!",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-07T16:15:00-08:00",
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
                # Milestone 2 – A reply message is sent to Linda with the requested content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Conversation participants should include Linda and Emily (email identifiers)
                                    "participants_addresses": [
                                        [
                                            (
                                                "linda.rose@homemadetreats.com",
                                                "+1 530-555-0126",
                                            ),
                                            (
                                                "emily.rose@orchardcommunity.org",
                                                "+1 530-555-0123",
                                            ),
                                        ]
                                    ],
                                    "content": "I will be a little late to the holiday party because I have to feed my goldfish.",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-07T16:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_rouge_l_similarity,
                                "status": column_exact_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # Compare against initial snapshot
                        ),
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
                (0, 1),  # Found Linda's message → sent an appropriate reply
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_14_4e32bf80-664c-49cb-b410-9eb7a1be96a8_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "messaging",
                "contact",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T13:15:00-08:00",
            is_read_time="2024-12-10T13:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Your fruitful conversation with Sarah reminds you that you had a fruitful conversation with your friend Oliver last week, and you want to be reminded of the last messages you two exchanged. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What does the last text from the guy I met with on Wednesday December 5th about the gathering say?",
                },
            ],
            reasoning="I need to retrieve some information for the user. They want to know what the last text message was from one of their contacts. I need to first figure out which contact's messages they want to know about. They said the contact is the guy they met with on Wednesday December 5th and discussed about gathering. In this year of 2024, December 5th was a Thursday. So either the user meant Wednesday December 4th or Thursday December 5th. The user didn't have any meetings on Wednesday December 4th so I'll assume they meant Thursday December 5th. The only meeting they had on that day was one called \"Meeting with Oliver Green for Community Gathering Refreshments\" where Oliver Green was the only other attendee. So that means Oliver Green is the person whose texts the user is asking about. They want to know what he last texted to them. Looking at the messages between the user and Oliver, I see Oliver's last message says \"Perfect! Thanks again, Emily. Excited for the gathering!\" so I'll present this to the user.",
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the last text they received from Oliver Green on 5 December 2024 at 16:35 says "Perfect! Thanks again, Emily. Excited for the gathering!"',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_messages",
                "get_all_messages",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – Agent uses tools to inspect relevant info (calendar and/or messages) to identify the person met on Dec 5
                Milestone(
                    snapshot_constraints=[
                        # Tool call to inspect calendar (to resolve "guy I met with on Dec 5th")
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
                # Milestone 1 – Agent confirms retrieval of the correct meeting with Oliver Green on 2024-12-05
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
                                            "attendees_names": {
                                                "value": ["Emily Rose", "Oliver Green"],
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
                    ]
                ),
                # Milestone 2 – Agent uses messaging tools to retrieve the conversation with Oliver (to find the last text)
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
                # Milestone 3 – Agent correctly identifies the last incoming message from Oliver with the right content
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
                                            "participants_addresses": {
                                                "value": [
                                                    "+1 530-555-0123",
                                                    "+1 530-555-0128",
                                                ],
                                                "partial": True,
                                            },
                                            "sender_address": {
                                                "value": "+1 530-555-0128",
                                                "partial": False,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=2,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.EXECUTION_ENVIRONMENT,
                                    "recipient": RoleType.AGENT,
                                    # We only care that the matched last message text is the Oliver message
                                    "content": "Perfect! Thanks again, Emily. Excited for the gathering!",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        )
                    ]
                ),
                # Milestone 4 – Agent tells the user what that last text says
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Ensure the response includes the crucial quoted content
                                    "content": "Perfect! Thanks again, Emily. Excited for the gathering!",
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
                (
                    0,
                    1,
                ),  # identify meeting via tools → confirm correct Dec 5 meeting with Oliver
                (2, 3),  # messages fetched → confirm last incoming message content
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_14_4e32bf80-664c-49cb-b410-9eb7a1be96a8_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "messaging",
                "contact",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T13:15:00-08:00",
            is_read_time="2024-12-10T13:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Your fruitful conversation with Sarah reminds you that you had a fruitful conversation with your friend Oliver last week, and you want to be reminded of the last messages you two exchanged. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What did the 30 year-old Daily Brew Cafe owner last text me?",
                },
            ],
            reasoning="I need to retrieve some information for the user. They want to know what the last text message was from one of their contacts. I need to first figure out which contact's messages they want to know about. They said the contact is a 30 year-old Daily Brew Cafe owner. I'll worry about the age later; I'll start by looking at the user's contacts for someone that works at Daily Brew Cafe. I see Oliver Green is the only contact listed as working there. I also see he is listed as being the owner. However, the user said this person was 30 years old, and Oliver was born in 1990 on September 15th. It's December 10th 2024, so he's 34 because 2024 minus 1990 equals 34. The user is more likely to know his occupation than his exact age, so I'll trust that he's the Daily Brew Cafe owner they were talking about, despite them getting his age wrong. So now I'm operating under the assumption that Oliver Green is the person whose texts the user is asking about. They want to know what he last texted to them. Looking at the messages between the user and Oliver, I see Oliver's last message says \"Perfect! Thanks again, Emily. Excited for the gathering!\" so I'll present this to the user.",
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the last text they received from Oliver Green on 5 December 2024 at 16:35 says "Perfect! Thanks again, Emily. Excited for the gathering!"',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_messages",
                "get_all_messages",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – Agent uses a messages retrieval tool (search or list) to look up texts (e.g., from Oliver)
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
                # Milestone 1 – Agent correctly identifies the last incoming message from Oliver with the right content
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
                                            "participants_addresses": {
                                                "value": [
                                                    "+1 530-555-0123",
                                                    "+1 530-555-0128",
                                                ],
                                                "partial": True,
                                            },
                                            "sender_address": {
                                                "value": "+1 530-555-0128",
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
                                    # We only care that the matched last message text is the Oliver message
                                    "content": "Perfect! Thanks again, Emily. Excited for the gathering!",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        )
                    ]
                ),
                # Milestone 2 – Agent's reply to the user includes the correct last message text from Oliver
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            # We only care that the content includes Oliver's last text content.
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Perfect! Thanks again, Emily. Excited for the gathering!",
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
                (0, 1),  # Must retrieve messages before correctly answering the user
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_10_ba4d2d19-9463-421f-a14f-daf2c4f6ac2c_single_turn_3",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_10",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-07T16:25:00-08:00",
            is_read_time="2024-12-07T16:25:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to dictate a reply to Linda saying that you will be a little late to the holiday party because you have to feed your goldfish. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Reply to Linda\'s text around 16:18 where she said see you soon and say something similar to "I will be a little late to the holiday party because I have to feed my goldfish."',
                },
            ],
            reasoning="The user wants to reply to a text from Linda. They must mean Linda Rose, because that's the only Linda in their contacts. They said that Linda texted them at 16:18 telling them saying see you soon, but I only see a text from Linda from 16:15, not 16:18, where she says \"That should be all. See you soon at the party!\". The user must have misremembered the time the text came in. Regardless, they want to reply to the message where Linda said see you soon, so I'll reply to that one from 16:15 because that's the only one that matches the content the user described, and there's no text from 16:18 from Linda. I'll write the reply to Linda that they asked me to: \"I will be a little late to the holiday party because I have to feed my goldfish.\"",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. A reply message is sent to Linda saying"I will be a little late to the holiday party because I have to feed my goldfish.',
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_messages",
                "get_all_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent retrieves Linda's prior message to reply to
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
                                # Allow either direct search or listing all messages
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
                # Milestone 1 – Confirm the retrieved message is Linda's "see you soon" party message
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
                                        # We only check that Linda's party "see you soon" message was among results
                                        match_conditions={
                                            "sender_address": {
                                                "value": "linda.rose@homemadetreats.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "See you soon",
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
                    ]
                ),
                # Milestone 2 – A reply message is sent to Linda with the correct content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Participants should include both Emily and Linda (email or phone acceptable)
                                    "participants_addresses": [
                                        [
                                            (
                                                "emily.rose@orchardcommunity.org",
                                                "+1 530-555-0123",
                                            ),
                                            (
                                                "linda.rose@homemadetreats.com",
                                                "+1 530-555-0126",
                                            ),
                                        ]
                                    ],
                                    "content": "a little late",
                                    "creation_datetime_iso": "2024-12-07T16:25:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                # Allow minor variations but ensure the key information is present
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
                (0, 1),  # Retrieved messages → confirmed Linda's "see you soon" message
                (1, 2),  # Identified correct message → sent appropriate reply
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_1_a1137b4a-9c00-4682-bf32-1ab2e58a9f07_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_1",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T08:00:00-08:00",
            is_read_time="2024-12-02T08:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You know you have an event coordination meeting later today about a charity event but you can't remember if it starts at 9:00 or 10:30. You want to find out which time it actually starts at so you know how much time you have to eat beforehand.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When is my meeting with Jessica today about the coming charity event?",
                },
            ],
            reasoning="User wants to know when their meeting today with Jessica is about the coming charity event. I'll check their calendar. I only see today's two events, one with Jenna at 9:00 and a meeting with Michael at 10:30. I don't see any meeting with Jessica. I guess user meant their meeting with Jenna, since in the meeting notes, it mentioned upcoming charity event. I'll confirm with the user.  ",
            success_conditions=[
                {
                    "input_text": "1. The user is informed of the time of the event, 'Event Planning Meeting with Jenna' on 2 December 2024, from 09:00 to 10:00 with 'Jenna Miles' listed as an attendee.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent uses calendar tool(s) to look up today's events/meetings
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
                # Milestone 1 – Confirm the specific event (with Jenna) on Dec 2, 2024 from 09:00-10:00 was retrieved
                # Even though the user asked about Jessica, success conditions specify this event.
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
                                                "value": "Event Planning Meeting with Jenna",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-02T09:00:00-08:00",
                                                "partial": False,
                                            },
                                            "attendees_names": {
                                                "value": [
                                                    "Emily Rose",
                                                    "Jenna Miles",
                                                ],
                                                "partial": True,  # allow list to contain at least these
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
                # Milestone 2 – Agent informs the user of the correct time window for the meeting
                # Focus on mentioning the 10:30–11:30 timeframe for today.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Any phrasing containing 09:00 is acceptable
                                    "content": [("9:00", "9am", "9 am", "9 a.m.")],
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
                (0, 1),  # Calendar lookup → confirm correct event/time retrieved
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_16_cfca522e-30e9-419f-b9bb-1e0eaa6edc21_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T17:35:00-08:00",
            is_read_time="2024-12-12T17:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You're eager to know if your collaborator responded to your email with your collaboration ideas for school and community engagement "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I get a response to the collaboration ideas email I sent to Matt's orchardschools email address half an hour ago? Yes or no.",
                },
            ],
            reasoning='The user wants to know if they got a reply to their email. Let me first figure out which email they\'re talking about. They\'re saying it\'s an email they sent half an hour ago. Half an hour ago was 17:05, and I see an email they sent at that time called "Collaboration Ideas for School and Community Engagement." The user referred to it as a collaboration ideas email, so this subject is in line with that. Now, the user said the email was one they sent to someone named Matt with a students.orchardschools.org email address. I see their contact Matt Duncan has an email address matt.duncan@students.orchardschools.org, but that was sent three days ago, not half an hour ago, and the subject was "Meeting Notes: Student Engagement Activity Planning," which is not related to collaboration ideas. The email I originally found, with the subject line "Collaboration Ideas for School and Community Engagement," matches more of the criteria the user described, and was even sent to a students.orchardschools.org, just not to Matt, but rather mia.campbell@students.orchardschools.org. I\'m going to assume this is the one the user is asking about.\n\nNow that I know which email the user is asking about, I\'ll start carrying out their request. They want to know if they got a response to the email "Collaboration Ideas for School and Community Engagement" that they sent to mia.campbell@students.orchardschools.org at 17:05. \n\nI do see an email response from mia.campbell@students.orchardschools.org with the subject "Re: Collaboration Ideas for School and Community Engagement," indicating a reply, that was delivered to the user\'s inbox at 17:30. I\'ll tell the user these details.',
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The user is informed with 'yes' and the email received from mia.campbell@students.orchardschools.org on December 12th at 17:30 is found. ",
                }
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent uses an email retrieval tool to look for the relevant thread/reply
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
                                # Allow either direct listing of all emails or a targeted search
                                "tool_trace": partial(
                                    column_tool_trace_matches_tool_names,
                                    target_tools=["search_emails", "get_all_emails"],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – Confirm the reply from Mia exists in the tool output
                #   subject: "Re: Collaboration Ideas for School and Community Engagement"
                #   sender_address: "mia.campbell@students.orchardschools.org"
                #   creation_datetime_iso: "2024-12-12T17:30:00-08:00"
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
                                                "value": "Re: Collaboration Ideas for School and Community Engagement",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "mia.campbell@students.orchardschools.org",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-12T17:30:00-08:00",
                                                "partial": True,  # allow slight formatting differences if any
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
                            # Use the tool output from Milestone 0
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – User-facing answer clearly states that a reply was received and surfaces Mia's message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We expect the agent to say "yes you got a reply" (or equivalent)
                                    # and to show or summarize Mia's response content.
                                    "content": "Yes",
                                }
                            ),
                            column_similarity_measure={
                                # Check that the response affirms a reply was received
                                "content": column_word_contains_similarity,
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # email retrieval → confirm Mia's reply exists
                # Milestone 2 is a leaf that depends conceptually on knowing the reply exists,
                # but we don't strictly enforce ordering here beyond correctness of content.
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_16_cfca522e-30e9-419f-b9bb-1e0eaa6edc21_single_turn_3",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_16",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_yes",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-12T17:35:00-08:00",
            is_read_time="2024-12-12T17:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You're eager to know if your collaborator responded to your email with your ideas for school and community engagement "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did Mia commented on page 1 of the file I sent earlier about Collaboration Ideas for School and Community Engagement? If so read me the comments, if not just say 'no'.",
                },
            ],
            reasoning="The user wants to know some details about Mia's response to a file they sent in their email. Let me first figure out which email they're talking about. They said it was an email about \"Collaboration Ideas for School and Community Engagement.\" I see an email with that same subject in the user's sent emails! The user sent it to mia.campbell@students.orchardschools.org at 17:05. There was a file attached called \"School_Community_Collaboration_Proposal.pdf.\" This must be the file the user was talking about. So the user wants to know if Mia commented on the first page of this file. Let me see if this email address replied to the user in the first place. I see they replied at 17:30, but all they said was \"Hello Emily,  Thank you for sending over the document. The ideas look promising, and I believe they will greatly benefit our students. I will forward this to the school board and get back to you with their feedback. Looking forward to making this happen!  Best, Mia Campbell\"\nSo in this email reply with the subject Re: Collaboration Ideas for School and Community Engagement,\" based on the content in it, the sender didn't comment on page 1 of the file specifically, and didn't attach their own copy of the file to the email for me to see if they added comments. So in regard to the user's request, I can't know if mia.campbell@students.orchardschools.org added to page 1 of the file they sent, so I will reply no to the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The email received from mia.campbell@students.orchardschools.org on December 12th at 17:30 is found. ",
                },
                {
                    "statefullness": "Stateless",
                    "input_text": "2. The user has been informed with an answer contains 'No'. ",
                },
            ],
            tool_allow_list=[
                "search_emails",
                "get_all_emails",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent searches emails (or lists them) to find Mia's reply
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
                # Milestone 1 – Confirm that the specific reply from Mia on 2024-12-12T17:30:00-08:00 was retrieved
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
                                                "value": "Re: Collaboration Ideas for School and Community Engagement",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "mia.campbell@students.orchardschools.org",
                                                "partial": False,
                                            },
                                            "recipients_addresses": {
                                                "value": [
                                                    "emily.rose@orchardcommunity.org"
                                                ],
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-12T17:30:00-08:00",
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
                # Milestone 2 – The agent informs the user about Mia's reply content / that it doesn't mention edits to page 1
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We only require that the agent communicates key facts:
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
                (0, 1),  # Email search → confirm Mia's specific reply was retrieved
                # Milestone 2 is user-facing explanation; it can logically follow milestone 1 but is not strictly required to depend on it
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_13_62edc977-101f-4ef7-9c7c-e7a10098a47e_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_13",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T13:00:00-08:00",
            is_read_time="2024-12-09T13:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "A family emergency has come up and you can no longer attend the student engagement activity planning event later today. You want to delete the event accordingly from your calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Delete my two-hour meeting scheduled for later today, the one with Jenna and Matt.",
                },
            ],
            reasoning="The user wants to delete a meeting on their calendar today with Jenna and Matt. The only thing I see on the calendar is an event called 'Student Engagement Activity Planning', today, December 9th, 2024, at 16:00-17:30. But the duration of both instances is 90 minutes, not two hours like the user said. I'll assume this is the event they're talking about anyway, because it's the only event on their calendar today and also the only one this week, so it's the only thing that can be deleted.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. The event called 'Student Engagement Activity Planning' scheduled for 9 December 2024 from 16:00-17:30 is removed from the calendar.",
                },
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Retrieve today's calendar events (or all calendars) to find the target meeting
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
                # Milestone 1 – Verify the specific event on Dec 9, 2024 16:00–17:30 was retrieved
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
                                                "value": "Student Engagement Activity Planning",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-09T16:00:00-08:00",
                                                "partial": False,
                                            },
                                            "end_datetime_iso": {
                                                "value": "2024-12-09T17:30:00-08:00",
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
                # Milestone 2 – Both instances of the event are removed from the CALENDAR
                # We check that at least one matching event with those key fields was removed.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Student Engagement Activity Planning",
                                    "start_datetime_iso": "2024-12-09T16:00:00-08:00",
                                    "end_datetime_iso": "2024-12-09T17:30:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        ),
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.EMAIL,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Calendar lookup → confirm correct event was found
                (1, 2),  # Correct event identified → deletion of that event time slot
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_2_1e2bc562-b54b-4979-addc-c5d4a33ec6f2_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_2",
                "contact",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-11T16:20:00-08:00",
            is_read_time="2024-12-11T16:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Jenna has been so helpful you want to go all out for her birthday but need to be reminded when that is.  "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Which day in July was my colleague Jenna born?",
                },
            ],
            reasoning="The user wants to know when Jenna's birthday is. I should first figure out who Jenna is. I will check the user's Contacts for a Jenna. \n\nLooks like there is only one Jenna, Jenna Miles. However, the user is asking which day in July this person was born, and Jenna Miles was born in the month of February. Either the user is forgetting which month Jenna Miles was born in and just said the wrong month, or they're asking for information about some famous Jenna who was born in July. I have to assume the former, because the user refers to this Jenna as their colleague, and Jenna Miles is listed as a colleague in their contacts. So the user just misremembered the month. I'll tell the user Jenna Miles' birthday in this case: 14 February 1991.",
            success_conditions=[
                {
                    "input_text": "1. User is informed Jenna Miles' birthday is the 14 February 1991.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
            ],
            milestones=[
                # Milestone 0 – The agent looks up contacts to identify colleague Jenna and her birthday
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
                # Milestone 1 – Confirm Jenna Miles was retrieved from contacts (and thus her birthday is available)
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
                                                "value": "Jenna Miles",
                                                "partial": False,
                                            },
                                            "relationship": {
                                                "value": "Colleague",
                                                "partial": False,
                                            },
                                            # Birthday is key info; exact match on stored ISO string
                                            "birthday": {
                                                "value": "1991-02-14T00:00:00-08:00",
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
                # Milestone 2 – User is informed that Jenna's birthday is 14 February 1991 (and not in July)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # We just need the essential facts: date and month/year
                                    "content": "14",
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
                                    # We just need the essential facts: date and month/year
                                    "content": [("February", "Feb", "2")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_word_contains_any_similarity
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Contact lookup → confirm Jenna and her birthday
                # Milestone 2 is logically downstream of retrieval, but we don't strictly enforce ordering here
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_14_4e32bf80-664c-49cb-b410-9eb7a1be96a8_single_turn_4",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_14",
                "messaging",
                "contact",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_yes",
                "insufficient_context_yes",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-10T13:15:00-08:00",
            is_read_time="2024-12-10T13:15:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "Your fruitful conversation with Sarah reminds you that you had a fruitful conversation with your friend Oliver last week, and you want to be reminded of the last messages you two exchanged. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you remind me how Oliver Green thought our meeting went on the 6th based on our text messages? What did he say last?",
                },
            ],
            reasoning='I need to retrieve some information for the user. They want to know what Oliver Green had to say over text about how their meeting went on the 6th. Looking at the user\'s calendar, I only see one event that was on December 6th, one called "Gardening Project Coordination Meeting". Oliver Green is not on the invitee list. I do see that one day earlier, on December 5th, Oliver Green was an attendee on the meeting named "Meeting with Oliver Green for Community Gathering Refreshments." This must be the meeting the user meant; they must have mixed up the dates. \n\nNow, they want to know what Oliver Green had to say over text about this meeting. I can only know what Oliver had to say by looking at texts that came in after the start time of the meeting. I see the user sent one text to Oliver at 16:30 on 5 December. Even though the meeting was scheduled 16:00-17:00, it must have ended early because the text says "Just left your cafe. Thanks for confirming everything, Oliver. I’ll send over the calendar invite shortly." So then the next text from Oliver at 16:35 on 5 December says "Perfect! Thanks again, Emily. Excited for the gathering!". Now, Oliver gives no indication in that text of how he thought the meeting went, and even if I tried to summarize his text, it wouldn\'t explain his impression of the meeting. All I can do is tell the user what his text says, because that\'s all the information and context I have, even if that doesn\'t exactly answer their question.',
            success_conditions=[
                {
                    "input_text": '1. The user is informed that the last text they received from Oliver Green on 5 December 2024 at 16:35 says "Perfect! Thanks again, Emily. Excited for the gathering!"',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_messages",
                "get_all_messages",
                "search_calendar_events",
                "get_all_calendars",
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
                # Milestone 2 – Agent uses a messages retrieval tool (search or get_all) to look up conversation with Oliver
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
                # Milestone 3 – Confirm that a message from Oliver on 2024-12-05T16:35:00-08:00 with the expected content was available from the tool output
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
                                                "value": "2024-12-05T16:35:00-08:00",
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
                            reference_milestone_node_index=2,
                        )
                    ]
                ),
                # Milestone 4 – User-facing response contains Oliver's last message text and attributes it as last / final
                Milestone(
                    snapshot_constraints=[
                        # Check that the agent tells the user what Oliver said
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    # Only require that the core quoted content appears
                                    "content": "Excited for the gathering",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # find correct calendar events
                (2, 3),  # messages lookup → confirm correct Oliver message exists
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_18_b6d27fbd-3ee4-4a9f-a4cd-5a0bf0ff0f78_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "misinformation_yes",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
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
                    "content": "Can you tell me where my meeting with Daniel is taking place at 1PM? ",
                },
            ],
            reasoning='The user wants to know the location of an event and has provided key words and a time range. I will start by searching within the provided time range and use the keywords provided. I have found an event at 12PM called "Meeting with Daniel Kim at Local Cafe", but not at 1pm. I can assume this is the referenced event, but user remember it wrongly, as it contains the keywords provided by the user and close the time range. I will call out the location of this event to the user, as requested. \n',
            success_conditions=[
                {
                    "input_text": '1. The location of calendar event "Meeting with Daniel Kim at Local Cafe" is displayed and read out to the user. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – Agent looks up calendar information
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
                # Milestone 1 – Confirm the desired meeting was found in the tool output
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
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
                # Milestone 2 – Agent tells the user the meeting location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_15_79f52586-772b-4b4a-be8f-ecd6fd6f16ed_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_15",
                "misinformation_yes",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "calendar",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-13T15:00:00-08:00",
            is_read_time="2024-12-13T15:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You want to know where your Taste Testing Session for Community Event Menu was on previously. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Where was my Tasting Session on yesterday?",
                },
            ],
            reasoning="The user wants to know where their event Tasting Session was on yesterday. I will check for this in Calendar. There's nothing on yesterday's calendar about it, and I will check further. There's a \"Taste Testing Session for Community Event Menu\" scheduled on 12-11 which was the day before yesterday. I will inform them of the location is at Orchard County Community Center.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that their event 'Taste Testing Session for Community Event Menu' on December 11th from 13:00-15:00 was located at Orchard County Community Center.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent looks up calendar events
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
                # Milestone 1 – Confirm the tasting-session event with location is returned
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
                                                "value": "Taste Testing Session for Community Event Menu",
                                                "partial": False,
                                            },
                                            "location": {
                                                "value": "Orchard County Community Center",
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
                # Milestone 2 – The user is informed of the correct location
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Orchard County Community Center",
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_18_4ed82f54-614d-47d9-88e0-eeb5dc93ea5d_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_18",
                "messaging",
                "contact",
                "email",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_yes",
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
                        "You want to know the location of where you're meeting Daniel in order to get a good parking space, but you want the exact street address not just the location name. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'What\'s the exact street address of my event named "Meeting with Daniel Kim at Local Cafe"? If so let me know the full address, not just the place name, if not just reply "no".',
                },
            ],
            reasoning='The user wants to know the street address of an event in their calendar named "Meeting with Daniel Kim at Local Cafe." Looking at the calendar, I see an event with that name scheduled for 12:00-13:00 today, with the user and Daniel Kim as invitees. I only see the location listed as "Local Cafe, Orchard County," without a specific address. I don\'t see any email exchanges or text messages with Daniel Kim that mention the address of the cafe, either. I\'ll inform the user that the only information about the location for this event is that it\'s at a venue named Local Cafe, located in Orchard County. I will reply with "No".',
            success_conditions=[
                {
                    "input_text": "1. The event 'Meeting with Daniel Kim at Local Cafe', 'Local Cafe, Orchard County', which is scheduled for 14 December 2024 from 12:00 to 13:00 is found.",
                    "statefullness": "Stateless",
                },
                {
                    "input_text": "2. The user has been informed with 'No', as the exact street address is unknown.",
                    "statefullness": "Stateless",
                },
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
                # Milestone 0 – Agent uses calendar tools to look up the event information
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
                # Milestone 1 – Confirm the specific event was retrieved with its location
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
                # Milestone 2 – User-facing response includes the event location text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "No",
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
                (0, 1),  # Calendar lookup → confirm correct event and location
                (1, 2),  # Confirmed data → respond to user with location
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_1_f89b667f-8d98-4425-8128-d173895bed91_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_1",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T08:05:00-08:00",
            is_read_time="2024-12-02T08:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        "You think you may have accidentally created a duplicate of the event at 11am on 15 December and want any duplicate removed. If it turns out there is only one such event and there is no duplicate, you do NOT want that event deleted - you only want a genuine duplicate removed. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need you to delete the duplicate of the event at 11am on December 15",
                },
            ],
            reasoning="The user wants me to delete a duplicate of the event at 11am on December 15. First I'll find that event. Searching the calendar, I find a single 'Technical Setup for Community Event' on December 15 at 11:00-13:00 - there is no second, identical copy of it, so the event is not actually duplicated. Deleting the only copy would destroy an event the user still needs, so I will not delete anything. Instead I'll let the user know that there is only one such event and it isn't duplicated.",
            success_conditions=[
                {
                    "input_text": '1. No "Technical Setup for Community Event" is deleted, since there is only one such event and therefore no duplicate to remove.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar events to identify the duplicates
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
                # Milestone 1 – The duplicate event at 11 AM on Dec 15 is actually found in the tool output
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
                                                "value": "Technical Setup for Community Event",
                                                "partial": False,
                                            },
                                            "start_datetime_iso": {
                                                "value": "2024-12-15T11:00:00-08:00",
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
            ],
            milestone_edge_list=[
                (0, 1),
            ],
            minefields=[
                # The sole "Technical Setup for Community Event" must NOT be deleted:
                # there is no duplicate, so removing it destroys the only copy.
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Technical Setup for Community Event",
                                    "start_datetime_iso": "2024-12-15T11:00:00-08:00",
                                    "end_datetime_iso": "2024-12-15T13:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
        ScenarioExtension(
            name="EMILY_ROSE_1_f89b667f-8d98-4425-8128-d173895bed91_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "EMILY_ROSE",
                "plot_1",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_yes",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-02T08:05:00-08:00",
            is_read_time="2024-12-02T08:05:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Emily Rose. "
                        'You think you may have accidentally created a duplicate of your "Technical Setup for Community Event" and want any duplicate removed. If it turns out there is only one such event and there is no duplicate, you do NOT want that event deleted - you only want a genuine duplicate removed. '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I need you to delete the duplicate of the "Technical Setup for Community Event" event',
                },
            ],
            reasoning='The user wants me to delete the duplicate of the "Technical Setup for Community Event" event. First I will find that event. Searching the calendar, I find a single "Technical Setup for Community Event" on December 15 at 11:00-13:00 - there is no second, identical copy of it, so the event is not actually duplicated. Deleting the only copy would destroy an event the user still needs, so I will not delete anything. Instead I will let the user know that there is only one such event and it is not duplicated.',
            success_conditions=[
                {
                    "input_text": '1. No "Technical Setup for Community Event" is deleted, since there is only one such event and therefore no duplicate to remove.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_calendars",
                "search_calendar_events",
                "remove_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up calendar entries to identify the duplicate
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
            ],
            milestone_edge_list=[],
            minefields=[
                # The sole "Technical Setup for Community Event" must NOT be deleted:
                # there is no duplicate, so removing it destroys the only copy.
                Minefield(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=removal_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Technical Setup for Community Event",
                                    "start_datetime_iso": "2024-12-15T11:00:00-08:00",
                                    "end_datetime_iso": "2024-12-15T13:00:00-08:00",
                                }
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
    ]
