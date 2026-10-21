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
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_rouge_l_similarity,
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


def get_TAG_LUCAS_GARCIA_pilot_plot_14(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="LUCAS_GARCIA_14_a7e87b81-719f-4b4a-977b-b431ba71997c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T17:00:00-08:00",
            is_read_time="2024-12-08T17:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to post another text in the group chat called YouTube Channel Engagement. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Put this in my YouTube chat: Hey guys, this channel has been so popular that i want to ask what you think if i started an OnlyFans. Any interest here? ",
                },
            ],
            reasoning="User Lucas Garcia want to post a message in a chat related to YouTube. I see from user's chat history that user has been engaed in a chat called YouTube Channel Engagement. That and user's mention of channel in the desired post make me certain this is where user wants to post the message. I shall prepare the message and present my handiwork to user for approval. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A text is posted in the group chat YouTube Channel Engagement which says: Hey guys, this channel has been so popular that i want to ask what you think if i started an OnlyFans. Any interest here? ",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up the existing group chat
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
                # Milestone 1 – The conversation “YouTube Channel Engagement” is found in the tool output above
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
                                                "value": "YouTube Channel Engagement",
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
                # Milestone 2 – The new message containing the OnlyFans question has been posted to the group chat
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "YouTube Channel Engagement",
                                    "content": "Hey guys, this channel has been so popular that i want to ask what you think if i started an OnlyFans. Any interest here?",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-08T17:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "conversation_name": column_exact_match_similarity,
                                "content": column_contains_similarity,
                                "status": column_exact_match_similarity,
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
                (0, 1),  # search → confirmation
                (1, 2),  # confirmation → message sent
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_14_616c079c-5c77-436f-b69a-1396d39e382e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T16:30:00-08:00",
            is_read_time="2024-12-08T16:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        'You want to dictate a reply message to Theo Appleseed saying "I can give you a quick call if you want to go over anything else from the session lmk". '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Write a message saying "I can give you a quick call if you want to go over anything else from the session lmk" to my gym buddy on my group thread for audience response and then send it',
                },
            ],
            reasoning="The user wants to write a message saying \"I can give you a quick call if you want to go over anything else from the session lmk\" to his gym buddy. I don't know who this might refer to, so I will go through the user contacts and try to find out. I see a lot of buddies listed there, but the only reference to 'gym buddy' in the aliases is made for 'Theo Appleseed'. I know now this is the contact the user is referring to. \n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply. I see that there are two possibilities. There is a message thread with Theo directly and there is another message thread for the YouTube Channel Engagement. The user says he wants to send this message to his 'thread for audience response', which must be a different way to refer to the group thread named  'YouTube Channel Engagement' (audience response and channel engagement are similar possibilities). I will use this thread to send this message, as the contact Theo Appleseed is part of that message group as well.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": '1. A reply message is sent to Theo Appleseed saying "I can give you a quick call if you want to go over anything else from the session lmk".',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent looks up who the “gym buddy” is
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
                # Milestone 1 – The contact returned from the search includes Theo Appleseed
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
                                                "value": "Theo Appleseed",
                                                "partial": False,
                                            },
                                            "email": {
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
                # Milestone 2 – A new group message containing the dictated text is sent and includes Theo
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "content": "I can give you a quick call if you want to go over anything else from the session lmk",
                                    "participants_addresses": [
                                        [
                                            (
                                                "+1 12345-6789-1000-5678",
                                                "theo.appleseed@example.com",
                                            )
                                        ]
                                    ],
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-08T16:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "status": column_exact_match_similarity,
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
                (0, 1),  # found contact → verified Theo present
                (1, 2),  # after confirming Theo, message is sent
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_14_8f15cc31-ef3b-4b81-ba99-e85e7720218c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:00:00-08:00",
            is_read_time="2024-12-08T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You really appreciate Alex engaging with your youtube channel, you want to email him and see if he'd be interested in a collaboration. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Give me Alex Martin's email address",
                },
            ],
            reasoning="The user is asking about a contacts email address.\nFirst, I should find the named person in the user's contacts.\nI have found Alex Martin. Alex Martin's email address is saved as alex.martin@example.com. I should provide this to the user.",
            success_conditions=[
                {
                    "input_text": "1. Email address of Alex Martin, alex.martin@example.com, is provided to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts"],
            milestones=[
                # Milestone 0 – Agent looks up contact information
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
                # Milestone 1 – Verify Alex Martin with correct email appears in previous tool output
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
                                                "value": "Alex Martin",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "alex.martin@example.com",
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
                # Milestone 2 – Agent informs the user with Alex's email address
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "alex.martin@example.com",
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
            name="LUCAS_GARCIA_14_d68fd249-6549-4797-b0be-0d7bddf6879c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T16:20:00-08:00",
            is_read_time="2024-12-08T16:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know who messaged you and what they said. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What’s that last message?\n",
                },
            ],
            reasoning='The user wants to know what the last message they received was. This means I need to look at all of the text messages the user has received and find the one that was sent to the user most recently, with a time stamp closest to the current time of 16:20 on 8 December 2024. I see a message from Theo Appleseed, in the group chat named YouTube Channel Engagement, that just came in now at 16:20. This is the most recent message, so I\'ll tell the user that the last message is from Theo Appleseed saying "Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?"\n',
            success_conditions=[
                {
                    "input_text": "1. The last message received from Theo Appleseed in Youtube Channel Engagement is read out loud to the user. \n",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent retrieves messages to figure out the last one
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
                # Milestone 1 – The agent tells the user who sent the last message and what was said
                Milestone(
                    snapshot_constraints=[
                        # Confirm the agent mentions the sender (Theo Appleseed)
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
                        ),
                        # Confirm the agent includes the key part of the message content (tracking progress)
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "tracking progress",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # Retrieval precedes informing the user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_14_d68fd249-6549-4797-b0be-0d7bddf6879c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T16:20:00-08:00",
            is_read_time="2024-12-08T16:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know who messaged you and what they said. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read out the last message received in the Youtube Channel Engagement group chat. ",
                },
            ],
            reasoning='Ok so the user wants to read out the last message in the Youtube Channel Engagement group chat. First I will go to that group chat and look for the last message received. I have found the group chat and the message; it was from Theo Appleseed received at 16:20 on December 8 2024. It says "Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?" so I\'ll read this to the user.',
            success_conditions=[
                {
                    "input_text": "1. The last message received from Theo Appleseed in Youtube Channel Engagement is read out loud to the user. \n",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent uses a message-retrieval tool
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
                # Milestone 1 – Returned result set contains Theo’s last message in the
                # “YouTube Channel Engagement” conversation
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
                                                "value": "YouTube Channel Engagement",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "theo.appleseed@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": (
                                                    "Thanks, Lucas, for the awesome session! "
                                                    "How do you recommend tracking progress"
                                                ),
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
                            reference_milestone_node_index=0,  # depend on retrieval in Milestone 0
                        )
                    ]
                ),
                # Milestone 2 – Agent tells the user what Theo said
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "How do you recommend tracking progress",
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_14_8f15cc31-ef3b-4b81-ba99-e85e7720218c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:00:00-08:00",
            is_read_time="2024-12-08T18:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You really appreciate Alex engaging with your youtube channel, you want to email him and see if he'd be interested in a collaboration. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Give me my youtube follower's email.",
                },
            ],
            reasoning="The user is asking about a contacts email address.\nFirst, I should find the named person in the user's contacts.\nI can see that only one person is tagged Youtube follower in the user's contacts, this must be the person being referred to.\nI have found Alex Martin. Alex Martin's email address is saved as alex.martin@example.com. I should provide this to the user.",
            success_conditions=[
                {
                    "input_text": "1. Email address of Alex Martin, alex.martin@example.com, is provided to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts"],
            milestones=[
                # Milestone 0 – The agent uses a contact-retrieval tool
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
                # Milestone 1 – The tool output includes Alex Martin with the correct email
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
                                                "value": "Alex Martin",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "alex.martin@example.com",
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
                # Milestone 2 – The agent tells the user Alex's email address
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "alex.martin@example.com",
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
                (0, 1),  # tool call -> verify output
                (1, 2),  # verified output -> user informed
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_14_616c079c-5c77-436f-b69a-1396d39e382e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_14",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T16:30:00-08:00",
            is_read_time="2024-12-08T16:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        'You want to dictate a reply message to Theo Appleseed saying "I can give you a quick call if you want to go over anything else from the session lmk". '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a reply message to Theo saying "I can give you a quick call if you want to go over anything else from the session lmk".',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Theo Appleseed.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply. I see that there are two possibilities. There is a message thread with Theo directly and there is another message thread for the YouTube Channel Engagement. Based on the context (the user is reviewing comments on his YouTube channel), I will use the group thread named 'YouTube Channel Engagement' to send this message, as the contact Theo Appleseed is part of that message group as well. \n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": '1. A reply message is sent to Theo Appleseed saying "I can give you a quick call if you want to go over anything else from the session lmk".',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – New reply message sent to Theo with the dictated text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # At least one Theo identifier must be included, extras allowed
                                    "participants_addresses": [
                                        [
                                            (
                                                "theo.appleseed@example.com",
                                                "+1 12345-6789-1000-5678",
                                            )
                                        ]
                                    ],
                                    "content": "I can give you a quick call if you want to go over anything else from the session lmk",
                                    "creation_datetime_iso": "2024-12-08T16:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with pre-task snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_14_a7e87b81-719f-4b4a-977b-b431ba71997c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T17:00:00-08:00",
            is_read_time="2024-12-08T17:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to post another text in the group chat called YouTube Channel Engagement. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send the following message to YouTube Channel Engagement: Hey guys, this channel has been so popular that i want to ask what you think if i started an OnlyFans. Any interest here? ",
                },
            ],
            reasoning="User Lucas Garcia want to post a message in a conversation thread and has provided the full name of the chat. I see from user's chat history that user has been engaged in a chat called YouTube Channel Engagement. That and user's mention of channel in the desired post make me certain this is where user wants to post the message. I shall prepare the message and present my handiwork to user for approval. ",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": "1. A text is posted in the group chat YouTube Channel Engagement which says: Hey guys, this channel has been so popular that i want to ask what you think if i started an OnlyFans. Any interest here? ",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up the conversation before sending
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
                # Milestone 1 – A new message is posted to the “YouTube Channel Engagement” group chat
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "conversation_name": "YouTube Channel Engagement",
                                    "content": "Hey guys, this channel has been so popular that i want to ask what you think if i started an OnlyFans. Any interest here?",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-12-08T17:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "conversation_name": column_exact_match_similarity,
                                "content": column_rouge_l_similarity,
                                "status": column_exact_match_similarity,
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
                (0, 1),  # message lookup precedes sending the message
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_14_bf967511-fb49-49e8-a3e2-8136d815ab83_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T16:30:00-08:00",
            is_read_time="2024-12-08T16:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        'You want to dictate a reply message to Theo Appleseed saying "I can give you a quick call if you want to go over anything else from the session lmk". '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a reply message to Theo Appleseed saying "I can give you a quick call if you want to go over anything else from the session lmk".',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Theo Appleseed.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": '1. A reply message is sent to Theo Appleseed saying "I can give you a quick call if you want to go over anything else from the session lmk".',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages", "send_message"],
            milestones=[
                # Milestone 0 – The agent looks up the relevant conversation or messages
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
                # Milestone 1 – A new reply message to Theo Appleseed was actually sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Must include Theo’s address among the participants
                                    "participants_addresses": [
                                        [
                                            (
                                                "+1 12345-6789-1000-5678",
                                                "theo.appleseed@example.com",
                                            )
                                        ]
                                    ],
                                    # Core dictated text must appear in the sent content
                                    "content": "quick call",
                                    "creation_datetime_iso": "2024-12-08T16:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with the initial DB snapshot
                        )
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_14_bbac8535-fb14-4574-8512-6b99a8922d70_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T17:45:00-08:00",
            is_read_time="2024-12-08T17:45:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are wondering what time you sent in your last message to the Youtube Channel Engagement group "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I send that last message into the group with Alex and Megan and Theo",
                },
            ],
            reasoning='The user wants to know when they sent their last message into the group with Alex and Megan and Theo. First thing I need to do is search the user\'s messages to find a group with names that match those participants . Ok I found the group named "YouTube Channel Engagement" with Alex, Megan, Theo and the user. Now that I have found that I just need to take a look at the last message sent by the user. Ok now that I have that I will retrieve the time of the message and inform the user',
            success_conditions=[
                {
                    "input_text": '1. The time of the message sent by the user December 08, 2024 at 16:25 to the "YouTube Channel Engagement" group is presented to the user',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_messages", "get_all_messages"],
            milestones=[
                # Milestone 0 – Agent retrieves messages (needs to look up the group conversation)
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
                # Milestone 1 – Confirm the correct message (Dec-08-2024 16:25) was returned in the tool output
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
                                                "value": "YouTube Channel Engagement",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "lucas.garcia@example.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-08T16:25:00-08:00",
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
                # Milestone 2 – Agent tells the user the correct send time
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
                                        ("16:25", "4:25")
                                    ],  # allow 24-h or 12-h phrasing
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
                (0, 1),  # message search → verify correct message found
                (1, 2),  # after finding message → inform user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_14_aec44c78-0628-46b1-bdac-a0b7cda4a772_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "contact",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T10:00:00-08:00",
            is_read_time="2024-12-09T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You're thinking of making an entire YouTube video based on Theo's question but have forgotten the question "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Remind me of the question my gym buddy asked yesterday",
                },
            ],
            reasoning="The user wants a reminder of the question his gym buddy asked yesterday. I must figure out who the user's gym buddy is. In the user's contacts Theo Appleseed has been given an alias of 'Gym Buddy' so I can assume the user is referring to Theo. \n\nI'll search for any emails or messages from Theo Appleseed that were received yesterday. I have spotted a message from Theo Appleseed received yesterday in the YouTube Channel Engagement Chat. This must be the question the user was referring to. It reads \"Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?\" I'll present this message to the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The message from Theo Appleseed in YouTube Channel Engagement is presented to the user.",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – The agent uses a message-retrieval tool to look for yesterday’s question
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
                # Milestone 1 – Confirm the retrieved message is Theo’s question about tracking progress
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
                                                "value": "theo.appleseed@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "How do you recommend tracking progress",
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
                # Milestone 2 – The agent tells the user the exact question
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "How do you recommend tracking progress",
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
                (0, 1),  # Retrieval tool call → match correct message
                (1, 2),  # Having found the message → relay it to the user
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_14_7ebb89e0-70b2-4fa5-9882-2a0026fb8533_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T16:35:00-08:00",
            is_read_time="2024-12-08T16:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to send another message to Theo Appleseed. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a message to the person I texted on December 02 2024 at 19:25 today and say "by the way, any tips on my presenting style?"',
                },
            ],
            reasoning='The user is asking to send a message.\nFirst, I need to identify the intended recipient. The user has indicated that this is a contact messaged at a specified time. Looking through the user\'s conversations I can see only one person was messaged on December 02 2024 at 19:25, Theo Appleseed. This must be who the user is referring to.\nNext, I will compose the message as requested.\nA message saying "by the way, any tips on my presenting style?" will be sent to Theo Appleseed.',
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Theo Appleseed saying "\'by the way, any tips on my presenting style?"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – The agent looks up past messages to figure out whom to text
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
                # Milestone 1 – A new outgoing message to Theo Appleseed was created with the correct content
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
                                                "+1 12345-6789-1000-5678",
                                                "theo.appleseed@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "by the way, any tips on my presenting style?",
                                    "creation_datetime_iso": "2024-12-08T16:35:00-08:00",
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
                    ],
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_14_7ebb89e0-70b2-4fa5-9882-2a0026fb8533_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T16:35:00-08:00",
            is_read_time="2024-12-08T16:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to send another message to Theo Appleseed. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Send a message to Theo saying 'by the way, any tips on my presenting style?\"",
                },
            ],
            reasoning="The user wants to send a message. Theo is the intended recipient, and I can see in contacts that Theo Appleseed is the only person with that first name. I'll send the message now.",
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Theo Appleseed saying "\'by the way, any tips on my presenting style?"',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
                "send_message",
            ],
            milestones=[
                # Milestone 0 – Agent queries contacts (or lists all contacts) to locate Theo
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
                # Milestone 1 – Confirm Theo Appleseed appears in the result of the contact-lookup step
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
                                                "value": "Theo Appleseed",
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
                # Milestone 2 – A new message is sent to Theo containing the requested text
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
                                                "+1 12345-6789-1000-5678",
                                                "theo.appleseed@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "tips on my presenting style",
                                    "creation_datetime_iso": "2024-12-08T16:35:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "participants_addresses": column_list_tuple_subset_contains_similarity,
                                "content": column_contains_similarity,
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
            name="LUCAS_GARCIA_14_aec44c78-0628-46b1-bdac-a0b7cda4a772_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-09T10:00:00-08:00",
            is_read_time="2024-12-09T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You're thinking of making an entire YouTube video based on Theo's question but have forgotten the question "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Remind me of the question Theo asked yesterday",
                },
            ],
            reasoning="The user wants a reminder of the question Theo asked yesterday. Theo Appleseed is the only Theo in the user's contacts. I'll check for messages from Theo received yesterday. There are no messages from Theo received yesterday in the user's private chat but I have found a message from Theo Appleseed received yesterday in the YouTube Channel Engagement Chat. This must be the question the user was referring to. It reads \"Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?\" I'll present this message to the user.",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The message from Theo Appleseed in YouTube Channel Engagement is presented to the user.",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – The agent looks up recent messages (should invoke a message-retrieval tool)
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
                # Milestone 1 – Confirm the retrieved result includes Theo’s question
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
                                                "value": "theo.appleseed@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?",
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
                # Milestone 2 – Verify the agent tells the user what Theo asked
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "How do you recommend tracking progress",
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
            name="LUCAS_GARCIA_14_bbac8535-fb14-4574-8512-6b99a8922d70_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T17:45:00-08:00",
            is_read_time="2024-12-08T17:45:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are wondering what time you sent in your last message to the Youtube Channel Engagement group "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did I send that last message into the YouTube channel engagement group",
                },
            ],
            reasoning='The user wants to know when they sent their last message into the YouTube Channel Engagement group. First thing I need to do is search the user\'s messages to find a group with a name that matches. Ok I found the group "YouTube Channel Engagement". Now that I have found that I just need to take a look at the last message sent by the user. Ok now that I have that I will retrieve the time of the message and inform the user',
            success_conditions=[
                {
                    "input_text": '1. The time of the message sent by the user December 08, 2024 at 16:25 to the "YouTube Channel Engagement" group is presented to the user',
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
                # Milestone 1 – The sought message (Dec-08-2024 16:25, YouTube Channel Engagement) is present
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
                                                "value": "YouTube Channel Engagement",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-08T16:25:00-08:00",
                                                "partial": False,
                                            },
                                            "sender_address": {
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
                            reference_milestone_node_index=0,  # depends on Milestone 0 tool output
                        )
                    ],
                ),
                # Milestone 2 – Agent’s reply to the user includes the correct time
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
                                            "16:25",
                                            "4:25",
                                            "4:25 pm",
                                            "4:25 p.m.",
                                            "16:25 pm",
                                            "4:25PM",
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
                (0, 1),  # Retrieval tool call → confirm message found
                (1, 2),  # Message found → user informed
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_14_bf967511-fb49-49e8-a3e2-8136d815ab83_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T16:30:00-08:00",
            is_read_time="2024-12-08T16:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        'You want to dictate a reply message to Theo Appleseed saying "I can give you a quick call if you want to go over anything else from the session lmk". '
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send Theo a message saying "I can give you a quick call if you want to go over anything else from the session lmk"',
                },
            ],
            reasoning="The user wants to send a message to the contact called Theo .\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": '1. A reply message is sent to Theo Appleseed saying "I can give you a quick call if you want to go over anything else from the session lmk".',
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages", "send_message"],
            milestones=[
                # Milestone 0 – The agent queries existing message threads to locate Theo Appleseed’s conversation
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
                # Milestone 1 – Confirm that the tool output from Milestone 0 contained a conversation
                # involving Theo Appleseed (by email address)
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
                                                "value": "theo.appleseed@example.com",
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
                    ]
                ),
                # Milestone 2 – A new outgoing message is sent that includes Theo and the correct body text
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require at least Theo’s address; allow additional participants (e.g., Lucas, others)
                                    "participants_addresses": [
                                        [
                                            (
                                                "+1 12345-6789-1000-5678",
                                                "theo.appleseed@example.com",
                                            )
                                        ]
                                    ],
                                    "content": "I can give you a quick call",
                                    "creation_datetime_iso": "2024-12-08T16:30:00-08:00",
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
            name="LUCAS_GARCIA_14_4f856b58-7e16-46b8-b8ea-2beb8e3a231d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T16:23:00-08:00",
            is_read_time="2024-12-08T16:23:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know what Theo replied with in the YouTube message thread. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What was the latest response on the YouTube engagement group?",
                },
            ],
            reasoning="Okay so, the user is looking for the response message from the last person they messaged. From checking their message thread, I can see their last conversation took place in the thread 'YouTube Channel Engagement' with 'Megan Johnson', 'Theo Appleseed' and 'Alex Martin' included in it. The last message received was from 'Theo Appleseed' on 8 December 2024 at 16:20 saying 'Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?'. Now that I have found the requested information, I can read this out to the user.",
            success_conditions=[
                {
                    "input_text": "1. The message received from 'Theo Appleseed' in the 'YouTube Channel Engagement' on 8 December 2024 at 16:20 saying 'Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?' is read out to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – The agent consults the messaging database to locate the relevant thread/message
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
                # Milestone 1 – Verify that the tool’s result set actually contains Theo’s 8-Dec-2024 message
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
                                                "value": "theo.appleseed@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-08T16:20:00-08:00",
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
                # Milestone 2 – The agent tells the user what Theo said
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "tracking progress throughout",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity  # key phrase must appear
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
            name="LUCAS_GARCIA_14_b8f7d384-c515-44e9-afc9-b9871bd9ede2_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:40:00-08:00",
            is_read_time="2024-12-08T18:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to see the last message you sent to the Youtube Channel Engagement group. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the last response I sent to the group chat to my followers.",
                },
            ],
            reasoning="The user wants to see the last response they sent to the group chat to their followers. Let me look in messages to find this group. It must be YouTube Channel Engagement, as the participants Alex Martin and others mentioned watched the newest videos and have comments. I will show the user the last message they sent at 16:25.",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last message they sent to YouTube Channel Engagement on December 8th 2024 at 16:25.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – Agent uses a message-retrieval tool to look up the group chat
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
                # Milestone 1 – The queried result contains latest message at 16:25
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
                                                "value": "lucas.garcia@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Happy to help",
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
                # Milestone 2 – Agent replies to the user, showing the content of the last message sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Happy to help",  # key phrase from the last message
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity,
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1)],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_14_37f6f3e1-c162-4e43-892e-1f9c1b7da822_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T16:22:00-08:00",
            is_read_time="2024-12-08T16:22:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are driving but would like to know what your most recent message reads. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What does my most recent text message say?",
                },
            ],
            reasoning='The user wants to know what their most recent text message says. I should check their Messages to find the most recent. \nLooks like the last message the user has received was from Theo Appleseed at 16:20 on the 8 December 2024 which reads "Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?". I will let the user know. ',
            success_conditions=[
                {
                    "input_text": '1. User is informed the message received from Theo Appleseed at 16:20 on the 8 December 2024 reads "Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?".',
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
                # Milestone 0 – The agent queries the message database for the latest message
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
                # Milestone 1 – The queried result contains Theo’s 16:20 message
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
                                                "value": "theo.appleseed@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Thanks, Lucas, for the awesome session!",
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
                # Milestone 2 – The agent tells the user what the message says
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Thanks, Lucas, for the awesome session!",
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
            name="LUCAS_GARCIA_14_e1804ed0-5548-414e-a373-0d7e568cc98e_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "calendar",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T17:00:00-08:00",
            is_read_time="2024-12-08T17:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to review you YouTube engagement in a weeks time to see how it develops. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Create an event "Review Youtube Engagement" for 16:00-16:30 next Sunday. ',
                },
            ],
            reasoning='Ok so the user wants to create an event "Review Youtube Engagement" for 16:00-16:30 next Sunday. First is the name of the event which is given by the user. Next is the timeframe of the event which is given by the user. I will now create the event "Review Youtube Engagement" for 16:00-16:30 on 15 December 2024. ',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The event "Review Youtube Engagement" is created for 16:00-16:30 on 15 December 2024. ',
                }
            ],
            tool_allow_list=["create_calendar_event"],
            milestones=[
                # Milestone 0 – Verify the calendar event was created with the correct
                # name and a start/end time on Sunday 15 Dec 2024 from 16:00–16:30.
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Review Youtube Engagement",
                                    "start_datetime_iso": "2024-12-15T16:00",
                                    "end_datetime_iso": "2024-12-15T16:30",
                                    "creation_datetime_iso": "2024-12-08T17:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Require the event name to match exactly
                                "calendar_event_name": column_exact_match_similarity,
                                # Allow any valid timezone offset by checking the substring
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare against initial snapshot
                        ),
                    ],
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_14_e1804ed0-5548-414e-a373-0d7e568cc98e_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "calendar",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T17:00:00-08:00",
            is_read_time="2024-12-08T17:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to review you YouTube engagement in a weeks time to see how it develops. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set something up to remind me to view my YouTube engagement next Sunday around 4.",
                },
            ],
            reasoning='Ok so the user wants to set something up to remind me to view my YouTube engagement next Sunday around 4. First we\'ll get a name for this event; something that sets out the intent clearly. I will call it "Review Youtube Engagement." Next is the timeframe mostly given by the user. I will set the duration to the default time of half an hour and the user may change this later if necessary. I will now create the event "Review Youtube Engagement" for 16:00-16:30 on 15 December 2024. ',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. The event "Review Youtube Engagement" is created for 16:00-16:30 on 15 December 2024. ',
                }
            ],
            tool_allow_list=["create_calendar_event"],
            milestones=[
                # Milestone 0 – Verify the calendar event “Review Youtube Engagement” is added
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Review Youtube Engagement",
                                    "start_datetime_iso": "2024-12-15T16:00:00-08:00",
                                    "end_datetime_iso": "2024-12-15T16:30:00-08:00",
                                    "creation_datetime_iso": "2024-12-08T17:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "start_datetime_iso": column_contains_similarity,
                                "end_datetime_iso": column_contains_similarity,
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
            name="LUCAS_GARCIA_14_37f6f3e1-c162-4e43-892e-1f9c1b7da822_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T16:22:00-08:00",
            is_read_time="2024-12-08T16:22:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You are driving but would like to know what your most recent message reads. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What does the last message from Theo say?",
                },
            ],
            reasoning="The user wants to know what the last message from Theo says. I first need to figure out who Theo is. I will check the user's Contacts. \nHmm, seems like there is only one Theo in the user's Contacts, Theo Appleseed so this must be who the user means. I will next check for Theo's most recent message in Messages. \nLooks like the most recent message from Theo was received 6 days ago. This seems too long ago to be the one the user means. I should check group chats. I found a message in the Youtube Channel Engagement from Theo which was received at 16:20 on the 8 December 2024 so this must be the message the user means. \nI will let the user know the message reads \"Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?\".",
            success_conditions=[
                {
                    "input_text": '1. User is informed the message received from Theo Appleseed at 16:20 on the 8 December 2024 reads "Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?".',
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
                # Milestone 0 – Agent invokes a message-retrieval tool to look for Theo’s latest message
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
                # Milestone 1 – Confirm the retrieved result actually contains Theo’s message
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
                                                "value": "theo.appleseed@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?",
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
                # Milestone 2 – Agent tells the user what Theo’s last message says
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?",
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
            name="LUCAS_GARCIA_14_b8f7d384-c515-44e9-afc9-b9871bd9ede2_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T18:40:00-08:00",
            is_read_time="2024-12-08T18:40:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to see the last message you sent to the Youtube Channel Engagement group. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the last message I sent to YouTube Channel Engagement.",
                },
            ],
            reasoning="The user wants to see the last message they sent to YouTube Channel Engagement . Let me look for their messages. Okay I have found the conversation. I will show the user the last message they sent.",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last message they sent to YouTube Channel Engagement on December 8th 2024 at 16:25.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
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
                # Milestone 1 – The returned tool output contains the correct last message in the
                # “YouTube Channel Engagement” conversation
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
                                                "value": "YouTube Channel Engagement",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Happy to help, Theo!",
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
                # Milestone 2 – Agent shows the user the correct last message content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("Happy to help", "workout journal")],
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
            name="LUCAS_GARCIA_14_4f856b58-7e16-46b8-b8ea-2beb8e3a231d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T16:23:00-08:00",
            is_read_time="2024-12-08T16:23:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know what Theo replied with in the YouTube message thread. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What was the last response in the YouTube message thread?",
                },
            ],
            reasoning="Right so, the user is looking for the last response in their ' YouTube message thread' to be read out to them. Firstly, searching their message threads, I can see one matching named 'YouTube Channel Engagement' with 'Megan Johnson', 'Theo Appleseed' and 'Alex Martin' included in this thread. The last message received was from 'Theo Appleseed' on 8 December 2024 at 16:20 saying 'Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?'. Now that I have found the requested information, I can read this out to the user.",
            success_conditions=[
                {
                    "input_text": "1. The message received from 'Theo Appleseed' in the 'YouTube Channel Engagement' on 8 December 2024 at 16:20 saying 'Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?' is read out to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_messages", "search_messages"],
            milestones=[
                # Milestone 0 – Agent queries the message store (search_messages / get_all_messages)
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
                # Milestone 1 – The retrieved tool result contains Theo’s latest message
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
                                                "value": "theo.appleseed@example.com",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-08T16:20:00-08:00",
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
                # Milestone 2 – Agent relays Theo’s message content back to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "How do you recommend tracking progress",
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
            name="LUCAS_GARCIA_14_d68fd249-6549-4797-b0be-0d7bddf6879c_single_turn_2",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T16:20:00-08:00",
            is_read_time="2024-12-08T16:20:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to know who messaged you and what they said. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What's the most recent message sent to me in my group chat where Megan and friends were asking about exercises in my fitness video?",
                },
            ],
            reasoning='The user wants to know what the last message they received was in one of their group chats. I need to figure out which group chat they are talking about. They said it\'s the group chat with "Megan and friends." The user only has one contact named Megan: Megan Johnson. I\'ll look for text message threads with three or more participants (group chats) where Megan Johnson is included. I see the group chat "Online Fitness Class Feedback" with a couple of messages from Megan Johnson. I also see the group chat "YouTube Channel Engagement" with a message from Megan Johnson. \n\nNow I need to determine which of these two group chats, "Online Fitness Class Feedback" or "YouTube Channel Engagement", the user is asking about. Let\'s see, the user mentioned that their friends\' texts were asking about exercises in their fitness video. I need to see which thread contains questions about exercises in a fitness video. Both threads have names that suggest the conversation might involve questions about fitness videos, so let me look at the messages themselves to see if they\'re asking about exercises in a fitness video. One message from Megan at 12:00 in the chat "Online Fitness Class Feedback" has a question "Can you share the link?". That\'s not exactly a question about exercises. Let me check "YouTube Channel Engagement." I see questions from everyone. Part of one message from Megan at 16:10 asks "What do you suggest for adding more intensity to the cooldown stretches?". Part of another message says "Any tips for improving my form on those lunges?" And another asks "How do you recommend tracking progress throughout the program?". These messages are all asking about exercises. That means this thread, "YouTube Channel Engagement" is the thread the user is asking about. Now, back to the user\'s original query, they asked what the most recent message sent to them in this group chat was. I\'ll look for the message in this chat that\'s closest to the current time of 16:20. The message from Theo Appleseed that just came in at 16:20 is the most recent. It says "Thanks, Lucas, for the awesome session! How do you recommend tracking progress throughout the program?" so I\'ll share this with the user.',
            success_conditions=[
                {
                    "input_text": "1. The last message received from Theo Appleseed in Youtube Channel Engagement is read out loud to the user. \n",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent uses a messaging-related retrieval tool
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
                # Milestone 1 – Agent tells the user the content of Theo’s latest message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "How do you recommend tracking progress",
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
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_14_4cc14312-6f72-4cba-a4c3-558b0d7ec867_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "contact",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T16:18:00-08:00",
            is_read_time="2024-12-08T16:18:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to make sure you remembered to respond to Megan, a follower of your youtube exercise videos, as you don't like to let your fans down. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I send a message in YouTube Channel Engagement?",
                },
            ],
            reasoning="The user wants to know if they sent a message in YouTube Channel Engagement. I wonder what they mean. I'll search their messages to find out. I see one message thread called YouTube Channel Engagement with several participants. I see one message sent from the user a few minutes ago today, December 8th, at 16:15. I assume this is what they are looking for. I'll show that message to them now. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The message sent by the user on December 8th, 2024, at 16:15, in Youtube Channel Engagement, is shown to the user. ",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – agent retrieves messages (either by listing all or searching)
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
                # Milestone 1 – confirm that the expected YouTube message is present in the tool output
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
                                                "value": "YouTube Channel Engagement",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "Great question, Megan!",
                                                "partial": True,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-08T16:15:00-08:00",
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
                # Milestone 2 – agent shows the retrieved message to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Great question, Megan!",
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
                (0, 1),  # message retrieval → validate retrieved content
                (1, 2),  # validated content → user-facing response
            ],
        ),
        ScenarioExtension(
            name="LUCAS_GARCIA_14_4cc14312-6f72-4cba-a4c3-558b0d7ec867_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "LUCAS_GARCIA",
                "plot_14",
                "messaging",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-08T16:18:00-08:00",
            is_read_time="2024-12-08T16:18:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Lucas Garcia. "
                        "You want to make sure you remembered to respond to Megan, a follower of your youtube exercise videos, as you don't like to let your fans down. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Did I send a message in the group with Megan? Yes or no.",
                },
            ],
            reasoning="The user wants to know if they sent a message in the group with Megan. I wonder what they mean. First I'll figure out who Megan is. Okay, I found a Megan Johnson in the user's contacts. I'll search for a message thread with her in it so. I see one message thread called YouTube Channel Engagement with several participants including Megan. I see one message sent from the user a few minutes ago today, December 8th, at 16:15. I assume this is what they are looking for. I'll show that message to them now and reply with Yes. ",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. The message sent by the user on December 8th, 2024, at 16:15, in Youtube Channel Engagement, is found. ",
                },
                {
                    "statefullness": "Stateless",
                    "input_text": "2. The user is informed with Yes.",
                },
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_messages",
                "search_messages",
            ],
            milestones=[
                # Milestone 0 – the agent tries to retrieve messages (search or list)
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
                # Milestone 1 – confirm the tool output includes the expected message to Megan
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
                                                "value": "YouTube Channel Engagement",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-08T16:15:00-08:00",
                                                "partial": False,
                                            },
                                            "status": {
                                                "value": "sent",
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
                # Milestone 2 – the agent shows the user the message (or clearly confirms it)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Yes",
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
                (0, 1),
                (1, 2),
            ],
        ),
    ]
