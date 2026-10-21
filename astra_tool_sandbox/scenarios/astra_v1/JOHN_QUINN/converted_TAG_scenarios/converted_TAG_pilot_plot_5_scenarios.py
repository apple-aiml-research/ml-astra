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
    column_list_tuple_subset_contains_similarity,
    column_one_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_matches_tool_names,
    column_word_contains_any_similarity,
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


def get_TAG_JOHN_QUINN_pilot_plot_5(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="JOHN_QUINN_5_b6611385-ca5b-493c-a579-3a0ca0ebcff0_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:00:00-07:00",
            is_read_time="2024-07-29T10:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You recently started seeing a counsellor and wanted to thank the person who suggested you do that. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a text to whoever suggested counselling to me saying "I took your advice on the counselling. Thank you." ',
                },
            ],
            reasoning="The user wants to send a text to whoever suggested counselling to them saying \"I took your advice on the counselling. Thank you.\" I wonder who that person was. I should check the user's messages for mention of counselling and similar phrases. Okay, I see one message from Ursula Quinn received on July 22nd at 18:36, which mentions a family counsellor. Okay, it's Ursula I need to draft the message to then. I draft the message as requested by the user and ask for confirmation befor sending. ",
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Ursula Quinn which says "I took your advice on the counselling. Thank you." ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "send_message",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – Agent looks through messages to figure out who suggested counselling
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
                # Milestone 1 – Verify the retrieved message is from Ursula and mentions counselling
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
                                                "value": "ursula.quinn@modernart.org",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "counsellor",
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
                # Milestone 2 – A new text message is sent to Ursula saying thanks for the counselling advice
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [("408-555-0124", "ursula.quinn@modernart.org")]
                                    ],
                                    "content": "I took your advice on the counselling. Thank you.",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-29T10:00:00-07:00",
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
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # messages lookup → confirm Ursula message retrieved
                (1, 2),  # confirmed source → text message sent
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_b6611385-ca5b-493c-a579-3a0ca0ebcff0_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-29T10:00:00-07:00",
            is_read_time="2024-07-29T10:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You recently started seeing a counsellor and wanted to thank the person who suggested you do that. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Send a text to Ursula saying "I took your advice on the counselling. Thank you." ',
                },
            ],
            reasoning="The user wants to send a text to Ursuls saying \"I took your advice on the counselling. Thank you.\" I wonder who Ursula is. I should check the user's contacts to find that person. I see one person called Ursula, Ursula Quinn in the user's contacts. That must be her. Okay, it's Ursula I need to draft the message to then. I draft the message as requested by the user and ask for confirmation before sending. ",
            success_conditions=[
                {
                    "input_text": '1. A message is sent to Ursula Quinn which says "I took your advice on the counselling. Thank you." ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_messages",
                "search_messages",
                "send_message",
                "get_all_contacts",
                "search_contacts",
            ],
            milestones=[
                # Milestone 0 – The agent looks up Ursula’s contact
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
                # Milestone 1 – The contact search result includes Ursula Quinn
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
                                                "value": "Ursula Quinn",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "ursula.quinn@modernart.org",
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
                # Milestone 2 – A new message to Ursula with the correct text was sent
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
                                                "ursula.quinn@modernart.org",
                                                "408-555-0124",
                                            )
                                        ]
                                    ],
                                    "content": "I took your advice on the counselling. Thank you.",
                                    "creation_datetime_iso": "2024-07-29T10:00:00-07:00",
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
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_53b405ff-c4e3-4beb-a124-6a41b495ff51_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "calendar",
                "email",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T18:45:00-07:00",
            is_read_time="2024-07-22T18:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to set aside time to look at the family counselling newsletter your mom passed on to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set aside half an hour around 6 tomorrow to review what mom just sent me. ",
                },
            ],
            reasoning="Ok so the user wants to set aside half an hour around 6 tomorrow to review what mom just sent them. First let's establish what the user's mother sent them. In text, they refer to a family counsellor and the user asks for details. I can also see an email just received by the user with a link attached. This must be what they are referring to. Next, is the name of the event which I will keep simple to make the intent of the event clear and to the point. I will call it something like Review Newsletter. Next, is the time which was given by the user which is about half an hour around 6 tomorrow. There seems to be no conflicts tomorrow for 6 so I will set the event to 18:00-18:30 on 23 July 2024. I will now create an event Review Newsletter at 18:00-18:30 on 23 July 2024. ",
            success_conditions=[
                {
                    "input_text": "1. The event about Review Newsletter is created at 18:00-18:30 on 23 July 2024. ",
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
                "search_emails",
                "get_all_emails",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                # Milestone 0 – the agent uses an email-retrieval tool to locate what Mom sent
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
                # Milestone 1 – confirm that the email “Family Counsellor Newsletter” from Mom
                # was actually returned by the tool call in Milestone 0
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
                                                "value": "Family Counsellor Newsletter",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "ursula.quinn@modernart.org",
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
                # Milestone 2 – the calendar event “Review Newsletter” is created for
                # 23 July 2024 18:00–18:30
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "review",
                                    "start_datetime_iso": "2024-07-23T18:00:00-07:00",
                                    "end_datetime_iso": "2024-07-23T18:30:00-07:00",
                                    "creation_datetime_iso": "2024-07-22T18:45:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
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
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_5cfbde33-d024-436c-8638-7227105926eb_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T18:45:00-07:00",
            is_read_time="2024-07-22T18:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to write to your mom to thank her for forwarding the email from the family counsellor. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Get back to mom about the family counsellor saying got it thanks",
                },
            ],
            reasoning='The user wants to reply to their mom with the text "got it thanks". First I can find the users mom by looking in contacts, then found an existing email regarding family consellor, and with this I can compose the email and see if the user wants to send it.',
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. An email is replied to to Ursula Quinn saying "got it, thanks"',
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "search_emails",
                "get_all_emails",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – The agent looks up mom’s contact information
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
                # Milestone 1 – Confirm Ursula Quinn's email was returned from the search
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
                                                "value": "Family Counsellor Newsletter",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "ursula.quinn@modernart.org",
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
                # Milestone 2 – An email was sent to Ursula containing “got it” and “thanks”
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["ursula.quinn@modernart.org"]
                                    ],
                                    "status": "sent",
                                    "body": [("got it",)],
                                    "creation_datetime_iso": "2024-07-22T18:45:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_subset_match_similarity,
                                "status": column_exact_match_similarity,
                                "body": column_str_contains_any_similarity,
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
                (0, 1),  # Contact search → verify Ursula found
                (1, 2),  # Ursula found → email sent
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_45892b99-9bd5-4ac9-b5a1-ae992ada7d7f_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T21:00:00-07:00",
            is_read_time="2024-07-22T21:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You know that your mother has sent you an email but you are not really sure what it is.  You want to check the subject, but are too busy to read the full thing. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell me the subject of the email sent to me by my mother today.",
                },
            ],
            reasoning="The user is asking about an email.\nFirst, I should confirm the identity of the person being referred to by looking at the user's contacts. I can see that Ursula Quinn is tagged as mother in the user's contacts.\nNext, I will find the email being referred to in the user's inbox. I see one email received from Ursula Quinn on July 22, 2024 at 18:40. The subject line of this email is Family Counsellor Newsletter.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Subject of email 'Family Counsellor Newsletter' received from 'ursula.quinn@modernart.org' on July 22, 2024 at 18:40 is presented to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent queries the mailbox
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
                # Milestone 1 – The queried email set contains mom’s email with the correct subject
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
                                                "value": "ursula.quinn@modernart.org",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Family Counsellor Newsletter",
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
                # Milestone 2 – Agent replies to the user with the correct subject
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Family Counsellor Newsletter",
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
            name="JOHN_QUINN_5_b894a78e-ff28-4ef2-9940-9fe8cf61d04c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "email",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T13:20:00-07:00",
            is_read_time="2024-07-23T13:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You've had enough of trying to speak sense into your father, because he isn't listening! You want to open the Family Counselling newsletter that your mother sent you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you show me the email from my mom that has the attachment",
                },
            ],
            reasoning="The user is looking for me to show them the email \"from their mom\" that has an attachment. I'm not entirely sure what this means, so I'm going to have to try and figure this out. Checking the user's contacts, I found that Ursula Quinn is the user's mom - I'm going to search his emails and look for emails from Ursula Quinn that might feature an attachment. I found this email, \"Family Counsellor Newsletter\", received on July 22nd 2024 at 18:40. I'll ask the user if this is the correct email.",
            success_conditions=[
                {
                    "input_text": "1. The user is show the email with the subject line Family Counsellor Newsletter which was received from ursula.quinn@modernart.org ay 18:40 on the 22 July 2024. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – an email-retrieval tool is invoked
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
                # Milestone 1 – the expected email (from mom with attachment) is present in the tool result
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
                                                "value": "Family Counsellor Newsletter",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "ursula.quinn@modernart.org",
                                                "partial": False,
                                            },
                                            # We don’t strictly require attachment verification here;
                                            # presence of the exact email is sufficient.
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
                # Milestone 2 – agent shows the email to the user (mentions the subject at minimum)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Family Counsellor Newsletter",
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
                (0, 1),  # retrieval → confirmation of correct email
                (1, 2),  # confirmation → user-facing output
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_a31c1ab3-701b-448e-96b2-1370163821f0_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "email",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T12:10:00-07:00",
            is_read_time="2024-07-23T12:10:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "Your dad won't stop sending you spam emails and it's annoying.  You want to know how many emails he has sent you this week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "How many emails did alfred.quinn@svmetal.com send me so far this week?",
                },
            ],
            reasoning="The user wants to know how many emails 'alfred.quinn@svmetal.com' sent them this week. I should check their Mail to find out. From checking their Mail, I can see that five emails have been received from 'alfred.quinn@svmetal.com' on 22 July 2024 between 14:00 and 14:08. I can present these to the user.\n",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that they have received five emails from 'alfred.quinn@svmetal.com' on 22 July 2024 from 14:00 to 14:08. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – The agent looks through the user’s email
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
                # Milestone 1 – Confirm that at least one email returned by the tool call in Milestone 0
                # is from Alfred Quinn (alfred.quinn@svmetal.com)
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
                                                "value": "alfred.quinn@svmetal.com",
                                                "partial": False,
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
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,  # use the tool output from Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – The agent tells the user the correct count (five emails) and
                # references the sender address
                Milestone(
                    snapshot_constraints=[
                        # Check that the agent mentions the number 5 / five
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("5", "five")],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        # Check that the agent mentions Alfred’s email address in the reply
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "alfred.quinn@svmetal.com",
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
                (0, 1),  # tool search → verify Alfred’s emails present
                (1, 2),  # verified retrieval → user informed
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_a31c1ab3-701b-448e-96b2-1370163821f0_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T12:10:00-07:00",
            is_read_time="2024-07-23T12:10:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "Your dad won't stop sending you spam emails and it's annoying.  You want to know how many emails he has sent you this week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell me how many emails my dad has sent me this week.",
                },
            ],
            reasoning="The user wants to know how many emails their dad has sent them. I should first figure out who their dad is.\n\nFirst I will check the user's Contacts for a contact named Dad. Hmm, there is no Contact named Dad but Alfred Quinn has his Alias as Dad so this must be who the user means.\n\nNext I will check Alfred's contact card for his email address. Looks like it's alfred.quinn@svmetal.com.\n\nLastly, I should now check for any emails from this address in Mail. I see five emails received on 22 July 2024 between 14:00 and 14:08 from 'alfred.quinn@svmetal.com'. I have found the requested information and can tell the user this.",
            success_conditions=[
                {
                    "input_text": "1. The user is informed that they have received five emails from 'alfred.quinn@svmetal.com' on 22 July 2024 from 14:00 to 14:08. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent looks through the user’s email
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
                # Milestone 1 – The email search result includes at least one message from dad
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
                                                "value": "alfred.quinn@svmetal.com",
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
                # Milestone 2 – The agent tells the user the correct count and identifies dad’s email address
                Milestone(
                    snapshot_constraints=[
                        # Contains the phrase “5 emails” or “five emails”
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("5", "five")],
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
                (0, 1),  # Email search → confirm dad’s messages found
                (1, 2),  # Info retrieved → inform the user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_b894a78e-ff28-4ef2-9940-9fe8cf61d04c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_high",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T13:20:00-07:00",
            is_read_time="2024-07-23T13:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You've had enough of trying to speak sense into your father, because he isn't listening! You want to find out the name of the Family Counselling newsletter that your mother sent you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you get me the attachment name in the email about Family Counsellor from my mom",
                },
            ],
            reasoning='The user is looking for me to show them the email about Family Counsellor from their mom that has an attachment. Checking the user\'s contacts, I found that Ursula Quinn is the user\'s mom - I\'m going to search his emails and look for an email titled "Family Counsellor" from Ursula Quinn with an attachment. I found it - the email is called "Family Counsellor Newsletter", received on July 22nd 2024 at 18:40. The attachment is Family_Counselling_Newsletter_July_2024.',
            success_conditions=[
                {
                    "input_text": '1. The user is show the name of the attachment is "Family_Counselling_Newsletter_July_2024"',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent attempts to retrieve the email
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
                # Milestone 1 – Confirm the correct email appears in the tool output
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
                                                "value": "Family Counsellor Newsletter",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "ursula.quinn@modernart.org",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-22T18:40:00-07:00",
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
                # Milestone 2 – Agent shows the email (or indicates opening it) to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Family_Counselling_Newsletter_July_2024",
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
                (0, 1),  # Retrieval → confirm correct email found
                (1, 2),  # Email confirmed → shown to user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_45892b99-9bd5-4ac9-b5a1-ae992ada7d7f_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "email",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T21:00:00-07:00",
            is_read_time="2024-07-22T21:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You know that your mother has sent you an email but you are not really sure what it is.  You want to check the subject, but are too busy to read the full thing. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Tell me the subject of the email sent to me by Ursula Quinn today.",
                },
            ],
            reasoning="The user is asking about an email.\nFirst, I should confirm the named person is present in the user's contacts list. I can see that Ursula Quinn is indeed in the user's contacts.\nNext, I will find the email being referred to in the user's inbox. I see one email received from Ursula Quinn on July 22, 2024 at 18:40. The subject line of this email is Family Counsellor Newsletter.\nI should inform the user.",
            success_conditions=[
                {
                    "input_text": "1. Subject of email 'Family Counsellor Newsletter' received from 'ursula.quinn@modernart.org' on July 22, 2024 at 18:40 is presented to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – The agent looks through the user’s e-mail to locate the relevant message
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
                # Milestone 1 – The agent tells the user the subject “Family Counsellor Newsletter”
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Family Counsellor Newsletter",
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
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_5cfbde33-d024-436c-8638-7227105926eb_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "messaging",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T18:45:00-07:00",
            is_read_time="2024-07-22T18:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to write to your mom to thank her for forwarding the email from the family counsellor. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Reply to mom's email saying got it thanks",
                },
            ],
            reasoning="The user would like to reply to their mom, using the text \"got it thanks\". I'll need to find the users mom via their contacts, and once I've located the contact in question I can compose the message and seek confirmation to send it.",
            success_conditions=[
                {
                    "statefullness": "Stateful",
                    "input_text": '1. An email is sent to Ursula Quinn saying "got it, thanks"',
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "search_emails",
                "get_all_emails",
                "send_email",
            ],
            milestones=[
                # Milestone 0 – The agent looks up mom’s contact information
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
                # Milestone 1 – Confirm Ursula Quinn's email was returned from the search
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
                                                "value": "Family Counsellor Newsletter",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "ursula.quinn@modernart.org",
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
                # Milestone 2 – An email was sent to Ursula containing “got it” and “thanks”
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.EMAIL,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "recipients_addresses": [
                                        ["ursula.quinn@modernart.org"]
                                    ],
                                    "status": "sent",
                                    "body": [("got it",)],
                                    "creation_datetime_iso": "2024-07-22T18:45:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "recipients_addresses": column_list_subset_match_similarity,
                                "status": column_exact_match_similarity,
                                "body": column_str_contains_any_similarity,
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
                (0, 1),  # Contact search → verify Ursula found
                (1, 2),  # Ursula found → email sent
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_53b405ff-c4e3-4beb-a124-6a41b495ff51_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "calendar",
                "email",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T18:45:00-07:00",
            is_read_time="2024-07-22T18:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to set aside time to look at the family counselling newsletter your mom passed on to you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'Create an event "Review Newsletter" tomorrow at 18:00-18:30.',
                },
            ],
            reasoning='Ok so the user wants to create an event "Review Newsletter" tomorrow at 18:00-18:30. I should check the user\'s calendar for any possible conflicts before creating the event. I see no other events happening at that time soI can create the event "Review Newsletter" at 18:00-18:30 on 23 July 2024. ',
            success_conditions=[
                {
                    "input_text": '1. The event "Review Newsletter" is created at 18:00-18:30 on 23 July 2024. ',
                    "statefullness": "Stateful",
                },
                {
                    "input_text": "2. The creation time recorded on the new entry is at or after the reference time, i.e. it is not backdated.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
                "search_emails",
                "get_all_emails",
            ],
            milestones=[
                # Milestone 0 – A new calendar event “Review Newsletter” on 23 Jul 2024 18:00-18:30 is created
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Review Newsletter",
                                    "start_datetime_iso": "2024-07-23T18:00:00-07:00",
                                    "end_datetime_iso": "2024-07-23T18:30:00-07:00",
                                    "creation_datetime_iso": "2024-07-22T18:45:00-07:00",
                                }
                            ),
                            column_similarity_measure={
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=None,
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_afc20d43-aa26-4c4a-b60f-b401f7e3de60_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T19:00:00-07:00",
            is_read_time="2024-07-22T19:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You've tried bringing up your criticisms of your dad's political leanings and his attempt to coerce you into it to your mom, but you feel like she is being very dismissive.  You want to dictate a reply to her messages after some time and thought. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want to dictate a message reply to Ursula Quinn saying \"Hey Mom, I really hear that you are trying to help me in the only way I know you can, but you can't keep excusing Dad's behaviour like this. His involvement with the Pirate Party is unacceptable.\"",
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Ursula Quinn.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply - \"Hey Mom, I really hear that you are trying to help me in the only way I know you can, but you can't keep excusing Dad's behaviour like this. His involvement with the Pirate Party is unacceptable.\". I'll make sure to confirm this with the user in case any changes are needed. I will then send the message if the user confirms that the message was transcribed correctly.\n",
            success_conditions=[
                {
                    "input_text": "1. A reply message is sent to Ursula Quinn saying \"Hey Mom, I really hear that you are trying to help me in the only way I know you can, but you can't keep excusing Dad's behaviour like this. His involvement with the Pirate Party is unacceptable.\"",
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
                # Milestone 0 – Agent retrieves the contact or conversation information first
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
                # Milestone 1
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
                                                "value": "Ursula Quinn",
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
                # Milestone 2 – Verify a new outgoing message to Ursula with the required content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [("408-555-0124", "ursula.quinn@modernart.org")]
                                    ],
                                    "content": "Hey Mom, I really hear that you are trying to help me",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-22T19:00:00-07:00",
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
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (
                    0,
                    1,
                ),  # Information retrieval precedes the actual sending of the message
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_00f9de45-210d-4df9-ad13-5b9e82c68c0d_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T18:45:00-07:00",
            is_read_time="2024-07-22T18:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "Your mother has emailed you about a family counseling newsletter and you want the assistant to read it out to you "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read the email from my mom about the family counsellor newsletter ",
                },
            ],
            reasoning="The user wants me to read them their email from their Mom about family counsellor newsletter. Firstly I'll look through the user's contacts to figure out who Mom is. Okay, I see one contact, Ursula Quinn, listed as the user's Mother so it must be here. Now I need to look through the user's emails for emails from Ursula ab0out family counselling. I have found one email from Ursula Quinn with the subject Family Counsellor Newsletter. That must be what the user wants to hear. I will now read that email to the user",
            success_conditions=[
                {
                    "input_text": "1. The email from ursula.quinn@modernart.org with the subject Family Counsellor Newsletter received on 22/07/2024 at 18:40 is read to the user",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent invokes an email-retrieval tool
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
                # Milestone 1 – Verify the expected email (from Mom, correct subject) was present
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
                                                "value": "Family Counsellor Newsletter",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "ursula.quinn@modernart.org",
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
                # Milestone 2 – Agent reads the email content to the user
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
                                            "Family Counsellor Newsletter",
                                            "family counsellor",
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
            name="JOHN_QUINN_5_aa8249a7-3ebf-47ce-b5a9-5849fa522b13_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-26T08:45:00-07:00",
            is_read_time="2024-07-26T08:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to dictate a reply to Robin Selmoure "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": 'I want to dictate a message reply to Robin Selmoure saying "Hi Robin I will be 5 minutes late to the stand up event sorry about that".',
                },
            ],
            reasoning="The user wants to dictate a reply to the contact called Robin Selmoure.\n\nI should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply and confirm with the user in case any changes are needed.\n\nI will then send the message if the user confirms that the message was transcribed correctly",
            success_conditions=[
                {
                    "input_text": '1. A reply message is sent to Robin Selmoure that says " Hi Robin I will be 5 minutes late to the stand up event sorry about that"',
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
                # Milestone 0 – Agent looks up Robin’s contact details
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
                # Milestone 1 – The returned contact data includes Robin Selmoure
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
                                                "value": "Robin Selmoure",
                                                "partial": False,
                                            },
                                            # Either phone or email must appear in the tool output
                                            "phone_number": {
                                                "value": "408-555-0132",
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
                # Milestone 2 – A new outgoing message to Robin is sent with the dictated text
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
                                                "robin.selmoure@palantir.com",
                                                "408-555-0132",
                                            )
                                        ]
                                    ],
                                    "content": "5 minutes late",
                                    "creation_datetime_iso": "2024-07-26T08:45:00-07:00",
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
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_8282de59-24ce-427d-98c4-1a1e1506cf08_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T19:00:00-07:00",
            is_read_time="2024-07-22T19:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to message your sister saying \"Grace, Mom has started believing dad's crazy Pirate Party crap, I can't deal! Then she sent me a family counselling news letter!\" "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Message my sister saying \"Grace, Mom has started believing dad's crazy Pirate Party crap, I can't deal! Then she sent me a family counselling news letter!\"",
                },
            ],
            reasoning="The user wants to message his sister. I will look in contacts. Grace Quinn is listed as his sister. He wants the message to say \"Grace, Mom has started believing dad's crazy Pirate Party crap, I can't deal! Then she sent me a family counselling news letter!\". I will draft the message and confirm it before sending it.",
            success_conditions=[
                {
                    "input_text": "A message is sent to Grace Quinn",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=["get_all_contacts", "search_contacts", "send_message"],
            milestones=[
                # Milestone 0 – Agent looks up the sister’s contact
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
                # Milestone 1 – Tool output contained Grace Quinn’s contact info
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
                                                "value": "Grace Quinn",
                                                "partial": False,
                                            },
                                            "email": {
                                                "value": "grace.quinn@example.com",
                                                "partial": False,
                                            },
                                            "phone_number": {
                                                "value": "408-555-0126",
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
                # Milestone 2 – A new message to Grace was created/sent
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    # Require that Grace is one of the participants (by phone or email)
                                    "participants_addresses": [
                                        [
                                            (
                                                "408-555-0126",
                                                "grace.quinn@example.com",
                                            )
                                        ]
                                    ],
                                    # Ensure the complaint text is present in the message body
                                    "content": "Mom has started believing dad's crazy Pirate Party",
                                    "creation_datetime_iso": "2024-07-22T19:00:00-07:00",
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_0803f1f8-83f7-4ac0-bb7c-265c8f399e6b_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T14:20:00-07:00",
            is_read_time="2024-07-23T14:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to see the email your mother sent you regarding a family counsellor and take their contact details from the newsletter she attached.  You ask the assistant to bring it up for you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to see the email mom sent me yesterday called Family Counsellor Newsletter",
                },
            ],
            reasoning='The user wants me to display and email they received from their mother yesterday called "Family Counsellor Newsletter", so first I must figure out which contact they are referring to. I have checked the user\'s contacts and have found an "Ursula Quinn" under the "mother" relationship. I will now search the user\'s emails for an email titled "Family Counsellor Newsletter" from Ursula Quinn. I will only search for emails from yesterday, as that is the time range I was given by the user. And I found it - I will display the email "Family Counsellor Newsletter" from Ursula Quinn received on 22 July at 18:40 to the user. ',
            success_conditions=[
                {
                    "input_text": '1. The email with the subject line "Family Counsellor Newsletter" from Ursula Quinn received on July 22nd 2024 at 18:40 is displayed on the screen for the user. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent queries the email database
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
                # Milestone 1 – Confirm the queried result contained the correct email
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
                                                "value": "Family Counsellor Newsletter",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "ursula.quinn@modernart.org",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-22T18:40:00-07:00",
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
                            reference_milestone_node_index=0,  # depends on tool output in milestone 0
                        ),
                    ],
                ),
                # Milestone 2 – Agent displays the email to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Family Counsellor Newsletter",
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
            name="JOHN_QUINN_5_0803f1f8-83f7-4ac0-bb7c-265c8f399e6b_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-23T14:20:00-07:00",
            is_read_time="2024-07-23T14:20:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to see the email your mother sent you regarding a family counsellor and take their contact details from the newsletter she attached.  You ask the assistant to bring it up for you. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you pull up that email Mom sent yesterday",
                },
            ],
            reasoning='The user wants me to display and email they received from their mother yesterday, so first I must figure out which contact they are referring to. I have checked the user\'s contacts and have found an "Ursula Quinn" under the "mother" relationship. I will now search the user\'s emails for correspondence with this contact. I will only search for emails from yesterday, as that is the time range I was given by the user. I have found one email from yesterday from Ursula Quinn - I will display this email Family Counsellor Newsletter" received on 22 July at 18:40.',
            success_conditions=[
                {
                    "input_text": '1. The email with the subject line "Family Counsellor Newsletter" from Ursula Quinn received on July 22nd 2024 at 18:40 is displayed on the screen for the user. ',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent invokes an email-retrieval tool
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
                # Milestone 1 – The returned tool output contains the correct email
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
                                                "value": "Family Counsellor Newsletter",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "ursula.quinn@modernart.org",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-22T18:40:00-07:00",
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
                # Milestone 2 – The agent shows the email to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Family Counsellor Newsletter",
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
                (0, 1),  # tool call ➜ email verified
                (1, 2),  # email verified ➜ displayed to user
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_00f9de45-210d-4df9-ad13-5b9e82c68c0d_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "email",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T18:45:00-07:00",
            is_read_time="2024-07-22T18:45:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "Your mother has emailed you about a family counseling newsletter and you want the assistant to read it out to you "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Read the email from Ursula Quinn about the family counsellor newsletter ",
                },
            ],
            reasoning="The user wants me to read them their email from Ursula Quinn about family counsellor newsletter. I wonder I need to first look through the user's emails and see if any email match that description. I have found one email from Ursula Quinn with the subject Family Counsellor Newsletter. So I will now read that email to the user",
            success_conditions=[
                {
                    "input_text": "1. The email from ursula.quinn@modernart.org with the subject Family Counsellor Newsletter received on 22/07/2024 at 18:40 is read to the user",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent uses an e-mail-retrieval tool (search_emails or get_all_emails)
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
                # Milestone 1 – Confirm the e-mail from Ursula Quinn with the correct subject was returned
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
                                                "value": "Family Counsellor Newsletter",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "ursula.quinn@modernart.org",
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
                            reference_milestone_node_index=0,  # depend on retrieval in Milestone 0
                        )
                    ],
                ),
                # Milestone 2 – Agent reads the e-mail content back to the user
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Here's the newsletter",
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
            name="JOHN_QUINN_5_afc20d43-aa26-4c4a-b60f-b401f7e3de60_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T19:00:00-07:00",
            is_read_time="2024-07-22T19:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You've tried bringing up your criticisms of your dad's political leanings and his attempt to coerce you into it to your mom, but you feel like she is being very dismissive.  You want to dictate a reply to her messages after some time and thought. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to send this to Mom: \"Hey Mom, I really hear that you are trying to help me in the only way I know you can, but you can't keep excusing Dad's behaviour like this. His involvement with the Pirate Party is unacceptable.\"",
                },
            ],
            reasoning="The user wants to dictate a reply to their mom. I'll need to check the user's contact for \"Mom\".... I found Ursula Quinn listed as such in the user's contacts, so this is probably who they want to message. I should locate the message history with this contact by searching their name in the user's Messages and then start a draft reply.\n\nAs the user has dictated exactly what they want to say, I will transcribe the text to the draft reply - \"Hey Mom, I really hear that you are trying to help me in the only way I know you can, but you can't keep excusing Dad's behaviour like this. His involvement with the Pirate Party is unacceptable.\". I'll make sure to confirm this with the user in case any changes are needed. I will then send the message if the user confirms that the message was transcribed correctly.",
            success_conditions=[
                {
                    "input_text": "1. A reply message is sent to Ursula Quinn saying \"Hey Mom, I really hear that you are trying to help me in the only way I know you can, but you can't keep excusing Dad's behaviour like this. His involvement with the Pirate Party is unacceptable.\"",
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
                # Milestone 0 – Agent retrieves the contact or conversation information first
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
                                        "get_all_contacts",
                                        "search_contacts",
                                    ],
                                )
                            },
                        )
                    ]
                ),
                # Milestone 1 – Verify a new outgoing message to Ursula with the required content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.MESSAGING,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "participants_addresses": [
                                        [("408-555-0124", "ursula.quinn@modernart.org")]
                                    ],
                                    "content": "Hey Mom, I really hear that you are trying to help me",
                                    "status": "sent",
                                    "creation_datetime_iso": "2024-07-22T19:00:00-07:00",
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
                            reference_milestone_node_index=-1,
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (
                    0,
                    1,
                ),  # Information retrieval precedes the actual sending of the message
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_345d7a67-a108-49e0-98ef-8aea640ea5bc_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T21:50:00-07:00",
            is_read_time="2024-07-22T21:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know what time your mom sent you the family counselling newsletter. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "When did Mom send me the newsletter for family counselling?",
                },
            ],
            reasoning="The user wants to know when Mom sent them the newsletter for family counselling. First I'll need to figure out who Mom is.\n\nChecking the user's contacts, I can see that Ursula Quinn has the alias Mom. Great, now I'll check the user's messages and emails with Ursula Quinn.\n\nI found an email from Ursula Quinn with subject line Family Counsellor Newsletter and an attachment named Family_Counselling_Newsletter_July_2024.pdf. This must be the newsletter the user is interested in.\n\nGreat, I'll go ahead and inform the user that Ursula Quinn sent them the Family Counselling Newsletter at 18:40 today (2024-07-22).",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. User is informed that Ursula Quinn emailed them the Family Counselling Newsletter at 18:40 on 2024-07-22.",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent searches or lists emails to locate the newsletter
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
                # Milestone 1 – Confirm the expected email from Mom was returned in the result of Milestone 0
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
                                                "value": "Family Counsellor Newsletter",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "ursula.quinn@modernart.org",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-22T18:40:00-07:00",
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
                # Milestone 2 – Agent’s reply to the user contains the correct date and time information
                Milestone(
                    snapshot_constraints=[
                        # Time mention check
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "18:40",
                                            "6:40",
                                            "6:40 pm",
                                            "6:40pm",
                                            "6:40 p.m.",
                                        )
                                    ],
                                }
                            ),
                            column_similarity_measure={
                                "content": column_str_contains_any_similarity
                            },
                        ),
                        # Date mention check
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [
                                        (
                                            "July 22",
                                            "Jul 22",
                                            "22 July",
                                            "7-22",
                                            "07-22",
                                            "7/22",
                                            "07/22",
                                            "the 22nd",
                                            "today",
                                            "2024-07-22T18:40",
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
            milestone_edge_list=[(0, 1), (1, 2)],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_b07243b9-9dc1-4ac2-a654-4873c1cb7cd9_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "messaging",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T19:00:00-07:00",
            is_read_time="2024-07-22T19:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to see the last message you sent to your mom. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the last message I sent to my mom.",
                },
            ],
            reasoning="The user wants to see the last message they sent to their mom. Let me look in Contacts to see who their mom is. It is Ursula Quinn. Let me look for their messages. Okay I have found the conversation. I will show the user the last message they sent, which was sent on July 22nd 2024 at 18:38 and says 'That might be a good idea. Can you send me the details?'.",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last message they sent to Ursula Quinn on July 22nd 2024 at 18:38 that says 'That might be a good idea. Can you send me the details?'",
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
                # Milestone 1 – Verify that the expected message appears in the tool output from Milestone 0
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
                                                "value": "That might be a good idea. Can you send me the details?",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "john.quinn@palantir.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-22T18:38:00-07:00",
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
                # Milestone 2 – Agent shows the user the correct last message
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "That might be a good idea. Can you send me the details?",
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
                (0, 1),  # Message retrieval → verify message found
                (1, 2),  # Message verified → user is shown the message
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_b07243b9-9dc1-4ac2-a654-4873c1cb7cd9_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "messaging",
                "referential_complexity_low",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T19:00:00-07:00",
            is_read_time="2024-07-22T19:00:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to see the last message you sent to your mom. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Show me the last message I sent to Ursula Quinn.",
                },
            ],
            reasoning="The user wants to see the last message they sent to Ursula Quinn. Let me look for their messages. Okay I have found the conversation. I will show the user the last message they sent, which was sent on July 22nd 2024 at 18:38 and says 'That might be a good idea. Can you send me the details?'.",
            success_conditions=[
                {
                    "input_text": "1. The user is shown the last message they sent to Ursula Quinn on July 22nd 2024 at 18:38 that says 'That might be a good idea. Can you send me the details?'",
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
                # Milestone 0 – The agent looks for messages (must call a message-searching tool)
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
                # Milestone 1 – The tool output includes the correct last message sent to Ursula Quinn
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
                                                "value": "Ursula Quinn",
                                                "partial": False,
                                            },
                                            "content": {
                                                "value": "That might be a good idea. Can you send me the details?",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-22T18:38:00-07:00",
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
                # Milestone 2 – The agent tells the user the correct last message content
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "That might be a good idea. Can you send me the details?",
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
                (0, 1),  # tool call → verify correct message present
                (1, 2),  # correct message found → user informed
            ],
        ),
        ScenarioExtension(
            name="JOHN_QUINN_5_345d7a67-a108-49e0-98ef-8aea640ea5bc_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "JOHN_QUINN",
                "plot_5",
                "contact",
                "email",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-22T21:50:00-07:00",
            is_read_time="2024-07-22T21:50:00-07:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, John Quinn. "
                        "You want to know what time your mom sent you the family counselling newsletter. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What time did she send me the newsletter?",
                },
            ],
            reasoning="The user wants to know what time she sent them the newsletter. I'm not sure who \"she\" is, but since they mentioned sending, I will check the user's communications for any mention of a newsletter.\n\nI found an email from Ursula Quinn with subject line Family Counsellor Newsletter and an attachment Family_Counselling_Newsletter_July_2024.pdf. This must be the information the user is looking for.\n\nNow I can let the user know that Ursula Quinn sent them the Family Counselling Newsletter at 18:40 today (2024-07-22).",
            success_conditions=[
                {
                    "statefullness": "Stateless",
                    "input_text": "1. User is informed that Ursula Quinn emailed them the Family Counselling Newsletter at 18:40 on 2024-07-22.",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – Agent queries emails to locate the newsletter
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
                # Milestone 1 – The email from Ursula with the newsletter is present in the previous tool output
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
                                                "value": "Family Counsellor Newsletter",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "ursula.quinn@modernart.org",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-07-22T18:40:00-07:00",
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
                # Milestone 2 – Agent informs the user of the correct send time
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
                                        ("18:40", "6:40 pm", "6:40pm", "6:40 p.m")
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
                (0, 1),  # Email search → email verified
                (1, 2),  # Email verified → user informed
            ],
        ),
    ]
