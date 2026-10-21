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
    column_list_exact_match_similarity,
    column_list_subset_match_similarity,
    column_one_similarity,
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


def get_TAG_DAWEI_SHEN_pilot_plot_7(
    base_scenarios: dict[str, Scenario], llm_evaluation: Optional[bool] = False
) -> list[ScenarioExtension]:
    return [
        ScenarioExtension(
            name="DAWEI_SHEN_7_36ffb147-bd91-4ad2-bfdf-02c226f424c3_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_7",
                "referential_complexity_high",
                "informational_complexity_high",
                "contact",
                "calendar",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-04T17:30:00-08:00",
            is_read_time="2024-12-04T17:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You now, after correspondence with your team want to set up a discussion about Strategy meeting two days later "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set up an hour long meeting with my colleagues for Friday at noon, oh, to discuss the upcoming strategy meeting again. ",
                },
            ],
            reasoning="the user wants an hour long meeting with their colleagues on Friday at noon about strategy meeting. who do they mean by their colleagues? Today with Kevin Chen and Stefan Mustermann there's a strategy meeting preparation agenda. I understand these are the colleagues user wants to add to the meeting. I will add both of them as invitees to the event. In that conversation they also speak of a Strategy Meeting. this isn't on the calendar already so this must be the event the user is trying to create. I will name the event Strategy meeting to coincide with this. they have also stated they want the meeting to be an hour long on Friday at noon. I will set the event to run from 12:00-13:00. I will now create the event 'Strategy Meeting' at 12:00-13:00 on Friday 6th of December 2024 with Kevin and Stefan as invitees and inform user of it.",
            success_conditions=[
                {
                    "input_text": "1. An event with name contains 'Strategy Meeting' is created for 12:00-13:00 6th December 2024 with Kevin Chen and Stefan Mustermann as invitees. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – agent looks up strategy meeting
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
                # Milestone 1 – Strategy meeting found
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
                                                "value": "Strategy Meeting Preparation",
                                                "partial": False,
                                            },
                                            "stastart_datetime_iso": {
                                                "value": "2024-12-04T15:00:00",
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
                # Milestone 2 – Strategy meeting is created on Friday at noon for one hour with colleagues
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Strategy Meeting",
                                    "start_datetime_iso": "2024-12-06T12:00",
                                    "end_datetime_iso": "2024-12-06T13:00",
                                    "attendees_names": [
                                        ["Kevin Chen", "Stefan Mustermann"]
                                    ],
                                    "creation_datetime_iso": "2024-12-04T17:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
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
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_7_36ffb147-bd91-4ad2-bfdf-02c226f424c3_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_7",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "contact",
                "calendar",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-04T15:30:00-08:00",
            is_read_time="2024-12-04T15:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You now, after correspondence with your team want to set up the Strategy meeting you have discussed with them again on Friday noon "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set an hour long strategy meeting with Kevin and Stefan at 12:00 on Friday. ",
                },
            ],
            reasoning="the user wants an hour long meeting with Kevin and Stefan at 12:00 on Friday.  Kevin and Stefan must be Kevin Chen and Stefan Mustermann as they are the only people with their respective first names in the users contacts. I will make them both invitees. The user said it was a strategy meeting so I will name the event 'Strategy Meeting.' they want it to be an hour long and start at 12:00 so I will set the run time to be 12:00-13:00. they also want it to be on Friday 6th of December. I will create the event 'Strategy Meeting' at 12:00-13:00 on Friday 6th of December 2024 with Kevin and Stefan as invitees and inform user of it.",
            success_conditions=[
                {
                    "input_text": "1. An event named 'Strategy Meeting' is created for 12:00-13:00 6th December 2024 with Kevin Chen and Stefan Mustermann as invitees. ",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "get_all_contacts",
                "search_contacts",
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – the agent looks up contacts or calendars to find out participants
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
                                        "search_calendar_events",
                                        "get_all_calendars",
                                    ],
                                )
                            },
                        )
                    ],
                ),
                # Milestone 1 – A new calendar event has been created for Friday, 6 Dec 2024, 12:00-13:00 with Kevin and Stefan as invitees
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Strategy Meeting",
                                    "start_datetime_iso": "2024-12-06T12:00:00-08:00",
                                    "end_datetime_iso": "2024-12-06T13:00:00-08:00",
                                    "attendees_names": [
                                        ["Kevin Chen", "Stefan Mustermann"]
                                    ],
                                    "creation_datetime_iso": "2024-12-04T15:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Require Kevin and Stefan; allow additional attendees such as the user
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
                (0, 1),  # search → event created
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_7_6e0d77b3-28f2-4825-b542-90be79cf286c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_7",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T09:00:00-08:00",
            is_read_time="2024-12-06T09:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know if you have any review meetings planned for next week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Do I have any review meetings between now and Friday 13th December 2024?",
                },
            ],
            reasoning="The user has requested me to check if there's any review meetings they have between today, December 6th 2024, and December 13th 2024. Over the next 7 days I have found one event that meets the criteria. It is a meeting on Friday December 13th 2024  called ' Team Review Meeting'. \nI tell the user this information.",
            success_conditions=[
                {
                    "input_text": "1. The 'Team Review Meeting' scheduled on 13th December 2024 between 10:00 and 11:00 is announced to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – The agent queries the calendar
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
                # Milestone 1 – Confirm the expected event appears in the tool’s result
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
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – The agent informs the user about the meeting
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
                                            "Team Review Meeting",
                                            "team review meeting",
                                            "December 13",
                                            "13th December",
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
                (0, 1),  # Calendar queried → verify event found
                (1, 2),  # Event found → user is informed
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_7_9601cad0-63df-4ec0-8402-6e48969e6559_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_7",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T16:55:00-08:00",
            is_read_time="2024-12-05T16:55:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to summarise Kevin's email to better prepare for the next meeting together. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I want a summary of the email I got yesterday.",
                },
            ],
            reasoning="Okay so, the user wants a summary of the email they received yesterday.\n\nThe request is being made on Thursday, December 5, so I need to check on emails received the day before, that is, Wednesday December 4. I can see that only one email was received from Kevin Chen on the 4th December at 17:00. This must be the email the user is referring to so I can confidently summarise this message to them. I'll provide the summary to the user.",
            success_conditions=[
                {
                    "input_text": "1. The email received from Kevin Chen on 4th December at 17:00 is summarised for the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 – The agent looks up the email(s) in the mailbox
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
                # Milestone 1 – Confirm the email from Kevin Chen dated 2024-12-04 17:00 was returned
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
                                                "value": "kevin.chen@orchardtech.com",
                                                "partial": False,
                                            },
                                            "subject": {
                                                "value": "Follow-up: Strategy Meeting Preparation",
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
                # Milestone 2 – The agent provides a summary to the user that contains the key points
                Milestone(
                    snapshot_constraints=[
                        # Must mention that Kevin will take the lead on data integration
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "data integration",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                        # Must mention the attached / listed action items
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("action item", "action items")],
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
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_7_9601cad0-63df-4ec0-8402-6e48969e6559_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_7",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_moderate",
                "email",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T16:55:00-08:00",
            is_read_time="2024-12-05T16:55:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to summarise Kevin's email to better prepare for the next meeting together. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Summarise the email I got from Kevin.",
                },
            ],
            reasoning="Right so, the user wants a summary of an email from Kevin. \n\nBased on the user's contacts, it can only be Kevin Chen (listed as a coworker) so I check and can see that there is one email from Kevin Chen from yesterday Wednesday, 4th December at 17:00. This must be the email the user is referring to so I will summarise it and read the summary to the user.",
            success_conditions=[
                {
                    "input_text": "1. The email received from Kevin Chen on 4th December at 17:00 is summarised for the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_emails", "search_emails"],
            milestones=[
                # Milestone 0 –  agent looks up emails to find Kevin's message
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
                # Milestone 1 –  correct email from Kevin Chen was surfaced in the tool result
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
                                                "value": "Follow-up: Strategy Meeting Preparation",
                                                "partial": False,
                                            },
                                            "sender_address": {
                                                "value": "kevin.chen@orchardtech.com",
                                                "partial": False,
                                            },
                                            "creation_datetime_iso": {
                                                "value": "2024-12-04T17:00:00-08:00",
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
                # Milestone 2 –  user receives a summary that contains the key points of Kevin's email
                Milestone(
                    snapshot_constraints=[
                        # Mention of Kevin leading data integration
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "data integration",
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_7_6e0d77b3-28f2-4825-b542-90be79cf286c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_7",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T09:00:00-08:00",
            is_read_time="2024-12-06T09:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know if you have any review meetings planned for next week. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What review meetings do I have next week?",
                },
            ],
            reasoning="The user has requested me to check what review meetings they have next week. As today is December 6th 2024 I will check dates from December 7th to December 13th 2024. I have found one event that meets the criteria. It is on Friday December 13th 2024  called ' Team Review Meeting'. \nI tell the user this information.",
            success_conditions=[
                {
                    "input_text": "1. The 'Team Review Meeting' that takes place next week on 13th December 2024 between 10:00 and 11:00 gets presented to the user.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["search_calendar_events", "get_all_calendars"],
            milestones=[
                # Milestone 0 – the agent looks up calendar events (next-week range filter is handled internally by the agent)
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
                # Milestone 1 – the tool call returned the “Team Review Meeting” on 2024-12-13 10:00–11:00
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
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,  # parse output of Milestone 0
                        )
                    ]
                ),
                # Milestone 2 – the user-facing reply mentions the found meeting
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Team Review Meeting",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity  # ensure meeting name is conveyed
                            },
                        )
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),  # calendar search → verify correct event retrieved
                (1, 2),  # event retrieved → reply to user
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_7_ed4e6a37-a482-4bce-a329-aaf0b8b5fbeb_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_7",
                "referential_complexity_low",
                "informational_complexity_low",
                "functional_complexity_high",
                "contact",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T10:00:00-08:00",
            is_read_time="2024-12-05T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You realized that after everything you discussed yesterday with Kevin and Stefan about Friday's strategy session, that none of you bothered to schedule it on Friday.  You shall schedule the strategy meeting on Friday. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Add Strategy meeting to my calendar from 10 to 11 tomorrow, Friday the 6th of December and list Kevin Chen and Stefan Mustermann as invitees. ",
                },
            ],
            reasoning="The user wants to add a new event to the calendar. User has provided all the necessary details, I will create this event named 'Strategy meeting' with Kevin Chen and Stefan Mustermann as invitees on Friday December 6th at 10am to 11am. I'll inform user that the event is scheduled.",
            success_conditions=[
                {
                    "input_text": "1. The event 'Strategy Meeting' is added to the calendar at 10 - 11 am, on Friday 06 December 2024 with the invitees Kevin Chen and Stefan Mustermann. ",
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
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – A new Strategy meeting is added on Friday 6 Dec 2024, 09:00-11:00,
                #               and includes Kevin Chen and Stefan Mustermann as invitees
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Strategy",  # partial match allowed
                                    "start_datetime_iso": "2024-12-06T10:00:00-08:00",
                                    "end_datetime_iso": "2024-12-06T11:00:00-08:00",
                                    "attendees_names": [
                                        ["Kevin Chen", "Stefan Mustermann"]
                                    ],
                                    "creation_datetime_iso": "2024-12-05T10:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with initial state
                        )
                    ],
                    guardrail_database_exclusion_list=[
                        DatabaseNamespace.SANDBOX
                    ],  # ignore sandbox noise
                ),
            ],
            milestone_edge_list=[],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_7_5dc59fe2-083c-45b0-9339-3bb102398648_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_7",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-04T17:35:00-08:00",
            is_read_time="2024-12-04T17:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to find out whether or not you've created a reminder in Calendar to pay your property tax. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need to know if I have a financial reminder in my calendar coming up ",
                },
            ],
            reasoning="The user wants to know if they have a \"financial reminder\" in their Calendar. \n\nFirstly, I'll check the user's Calendar to see if they have any events that correspond to the above term.\n\nI see one event named \"Pay Property Tax\", scheduled for 08:00 - 08:30 on Friday, December 6th 2024, that I surmise is the even the user is referring to, given that it's about taxation which I think is inextricably linked to finance. \n\nI'll present this reminder to the user now and inform user that they have an event 'Pay Property Tax' scheduled on Friday. ",
            success_conditions=[
                {
                    "input_text": '1. The event "Pay Property Tax" scheduled for 08:00 - 08:30 on Friday, December 6th 2024, is presented to the user.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent uses a calendar-reading tool
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
                # Milestone 1 – Tool output contains the “Pay Property Tax” event
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
                # Milestone 2 – Agent tells the user that they do have a scheduled event 'pay property tax'
                Milestone(
                    snapshot_constraints=[
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
            name="DAWEI_SHEN_7_ea0942df-bfd7-4213-8f32-4ff4afeea246_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_7",
                "calendar",
                "contact",
                "referential_complexity_moderate",
                "informational_complexity_low",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-04T15:30:00-08:00",
            is_read_time="2024-12-04T15:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You now, after correspondence with your team, want to set up the Strategy meeting you have discussed with them "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set an hour long strategy meeting with Kevin and Stefan at 12:00 on Friday. ",
                },
            ],
            reasoning="the user wants an hour long meeting with Kevin and Stefan at 12:00 on Friday.  Kevin and Stefan must be Kevin Chen and Stefan Mustermann as they are the only people with their respective first names in the users contacts. I will make them both invitees. The user said it was a strategy meeting so I will name the event 'Strategy Meeting.' they want it to be an hour long and start at 12:00 so I will set the run time to be 12:00-13:00. they also want it to be on Friday 6th of December. The user has an all-day event called \"Cat-Sitting for Paul\" that day, but they can attend a virtual meeting while cat-sitting, so that's not an issue. I will now finalise and create the event 'Strategy Meeting' at 12:00-13:00 on Friday 6th of December 2024 with Kevin and Stefan as invitees.",
            success_conditions=[
                {
                    "input_text": "1. An event named 'Strategy Meeting' is created for 12:00-13:00 6th December 2024 with Kevin Chen and Stefan Mustermann added as invitees.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – (Optional but recommended) Agent looks up contacts to resolve Kevin and Stefan
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
                # Milestone 1 – Strategy meeting calendar event created correctly
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Strategy Meeting",
                                    "start_datetime_iso": "2024-12-06T12:00:00-08:00",
                                    "end_datetime_iso": "2024-12-06T13:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "Dawei Shen",
                                            "Kevin Chen",
                                            "Stefan Mustermann",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-04T15:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                # Allow extra attendees (e.g., a room resource) but require these three
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
                        DatabaseNamespace.CONTACT,
                        DatabaseNamespace.MESSAGING,
                        DatabaseNamespace.WHATSAPP,
                        DatabaseNamespace.PHONE,
                        DatabaseNamespace.SANDBOX,
                    ],
                ),
            ],
            milestone_edge_list=[
                (0, 1),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_7_ea0942df-bfd7-4213-8f32-4ff4afeea246_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_7",
                "calendar",
                "contact",
                "referential_complexity_high",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-04T15:30:00-08:00",
            is_read_time="2024-12-04T15:30:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You now, after correspondence with your team, want to set up the meeting you have just discussed with them and prepared for"
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Set up an hour long meeting with my colleagues for Friday at noon about the meeting we are preparing for",
                },
            ],
            reasoning="The user wants an hour long meeting with their colleagues on Friday at noon about 'the meeting we are preparing for'. I need to check the calendar to find what meeting they are preparing for. I find a calendar event called 'Strategy Meeting Preparation' scheduled for today with Kevin Chen and Stefan Mustermann as attendees. This indicates the meeting they want to set up is the 'Strategy Meeting' itself, with Kevin and Stefan as the colleagues to invite. The user wants it on Friday at noon for one hour, so I will set it from 12:00-13:00 on Friday, December 6th, 2024. The user has an all-day event called 'Cat-Sitting for Paul' that day, but they can attend a meeting while cat-sitting, so that's not an issue. I will create the event 'Strategy Meeting' at 12:00-13:00 on Friday 6th of December 2024 with Kevin Chen and Stefan Mustermann as invitees.",
            success_conditions=[
                {
                    "input_text": "1. An event with name containing 'Strategy Meeting' is created for 12:00-13:00 6th December 2024 with Kevin Chen and Stefan Mustermann added as invitees.",
                    "statefullness": "Stateful",
                }
            ],
            tool_allow_list=[
                "search_contacts",
                "get_all_contacts",
                "search_calendar_events",
                "get_all_calendars",
                "create_calendar_event",
            ],
            milestones=[
                # Milestone 0 – Agent looks up the meeting in the calendar
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
                # Milestone 1 – Returned result contains meeting
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
                                            # look for correct participant
                                            "calendar_event_name": {
                                                "value": "Strategy Meeting Preparation",
                                                "partial": False,
                                            },
                                            # correct date & time
                                            "start_datetime_iso": {
                                                "value": "2024-12-04T15:00:00-08:00",
                                                "partial": True,
                                            },
                                        },
                                    ),
                                ),
                            ),
                            reference_milestone_node_index=0,  # parse tool outcome from milestone 0
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
                # Milestone 2 – A new calendar event "Strategy Meeting" is created for Friday Dec 6, 2024 12:00–13:00 with Kevin & Stefan as attendees
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Strategy",
                                    "start_datetime_iso": "2024-12-06T12:00:00-08:00",
                                    "end_datetime_iso": "2024-12-06T13:00:00-08:00",
                                    "attendees_names": [
                                        [
                                            "Dawei Shen",
                                            "Kevin Chen",
                                            "Stefan Mustermann",
                                        ]
                                    ],
                                    "creation_datetime_iso": "2024-12-04T15:30:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                # All three required attendees must be present; allow extras if system adds, e.g., resource rooms
                                "attendees_names": column_list_exact_match_similarity,
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
                (0, 1),  # Calendar lookup → confirm Kevin & Stefan
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_7_5dc59fe2-083c-45b0-9339-3bb102398648_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_7",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-04T17:35:00-08:00",
            is_read_time="2024-12-04T17:35:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to find out whether or not you've created a reminder in Calendar to pay your property tax. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Can you tell me if I have a property fee reminder in my calendar",
                },
            ],
            reasoning="The user wants to know if they have a \"property fee reminder\" in their Calendar. \n\nFirstly, I'll check the user's Calendar to see if they have any events that correspond to the above term. \n\nI see one event named \"Pay Property Tax\", scheduled for 08:00 - 08:30 on Friday, December 6th 2024, that I surmise is the event the user is referring to, given that it's about property.\n\nI'll present this reminder to the user and inform them they do have 'Pay Property Tax' scheduled. ",
            success_conditions=[
                {
                    "input_text": '1. The event "Pay Property Tax" scheduled for 08:00 - 08:30 on Friday, December 6th 2024, is presented to the user.',
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – Agent queries the calendar to look for the reminder
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
                # Milestone 1 – Verify the returned calendar payload contains the specific reminder
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
                # Milestone 2 – Agent informs the user that the reminder exists (user-facing response)
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": [("property tax", "property fee")],
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
                (0, 1),
                (1, 2),
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_7_ed4e6a37-a482-4bce-a329-aaf0b8b5fbeb_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_7",
                "contact",
                "email",
                "calendar",
                "referential_complexity_high",
                "informational_complexity_high",
                "functional_complexity_high",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-05T10:00:00-08:00",
            is_read_time="2024-12-05T10:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You realize that after everything you discussed yesterday with Kevin and Stefan about Friday's strategy session, that none of you bothered to schedule the Friday strategy session at 10 am and last for 1 hour.  You shall add this to the calendar. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "I need the Strategy Meeting we have been prepared added to my calendar tomorrow, at 10 and last one hour. Invite the related folks too. ",
                },
            ],
            reasoning="The user wants a Strategy Meeting added to calendar. Checking at Wednesday December 4 event 'Strategy Meeting Preparation' it contains notes say 'Virtual meeting to discuss updates and prepare for Friday's strategy meeting'. I understand user, Kevin and Stefan are going to have a strategy meeting on Friday, also information can be found with email titled 'Follow-up: Strategy Meeting Preparation' among the user, Kevin and Stefan. I will go ahead and schedule the Strategy meeting on this Friday 12/6 at 10-11 am, and add Kevin and Stefan as invitees.",
            success_conditions=[
                {
                    "input_text": "1. Add an event 'Strategy Meeting' to calendar on Friday,  06 December 2024 from 10-11 am with Kevin Chen and Stefan Mustermann as invitees.",
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
                "get_all_calendars",
                "search_calendar_events",
                "create_calendar_event",
                "get_all_emails",
                "search_emails",
            ],
            milestones=[
                # Milestone 0 – agent looks up strategy meeting
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
                # Milestone 1 – Strategy meeting found
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
                                                "value": "Strategy Meeting Preparation",
                                                "partial": False,
                                            },
                                            "stastart_datetime_iso": {
                                                "value": "2024-12-04T15:00:00",
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
                # Milestone 2 – agent looks up strategy meeting emails
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
                # Milestone 3 – Strategy meeting found
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
                                                "value": "Follow-up: Strategy Meeting Preparation",
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
                # Milestone 4 – Verify the new Friday Strategy Meeting was added to the calendar
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.CALENDAR,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "calendar_event_name": "Strategy",  # We’ll match by substring
                                    "start_datetime_iso": "2024-12-06T10:00:00-08:00",
                                    "end_datetime_iso": "2024-12-06T11:00:00-08:00",
                                    "attendees_names": [
                                        ["Kevin Chen", "Stefan Mustermann"]
                                    ],
                                    "creation_datetime_iso": "2024-12-05T10:00:00-08:00",
                                }
                            ),
                            column_similarity_measure={
                                "calendar_event_name": column_contains_similarity,
                                "attendees_names": column_list_subset_match_similarity,
                                "creation_datetime_iso": partial(
                                    column_datetime_window_similarity, max_minutes=30
                                ),
                            },
                            reference_milestone_node_index=-1,  # compare with pre-task snapshot
                        )
                    ]
                ),
            ],
            milestone_edge_list=[(0, 1), (2, 3)],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_7_2cbd6d27-4722-4c2c-90ab-5e7d6ac7806c_single_turn_0",
            base_scenario=base_scenarios["base"],
            tags=[
                "DAWEI_SHEN",
                "plot_7",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_low",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T09:00:00-08:00",
            is_read_time="2024-12-06T09:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know if you have any work meetings planned for next working week, starting Monday December 9 till Friday December 13. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "What work meetings do I have next week?",
                },
            ],
            reasoning="The user has requested me to check what work meetings they have next week.  As the request is being made on December 6th 2024, I will check dates from Monday December 9th to Friday December 13th 2024, as these are usually the working days in a week. Over the next 7 days I have found one event that meets the criteria. There is a meeting on Friday December 13th 2024  called 'Team Review Meeting'.  I will retrieve this information and share it with the user. ",
            success_conditions=[
                {
                    "input_text": "1. The meetings scheduled for the working week (from Monday December 9 till Friday December 13) are presented to the user. 'Team Review Meeting' is the only one scheduled at this moment.",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – A calendar-lookup tool is invoked
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
                # Milestone 1 – The returned calendar data contains the expected meeting
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
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ],
                ),
                # Milestone 2 – The agent informs the user about the meeting
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Team Review Meeting",
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
                (0, 1),  # Tool call → verify output
                (1, 2),  # Output verified → user informed
            ],
        ),
        ScenarioExtension(
            name="DAWEI_SHEN_7_2cbd6d27-4722-4c2c-90ab-5e7d6ac7806c_single_turn_1",
            base_scenario=base_scenarios["base"],
            tags=[
                "astra_core",
                "DAWEI_SHEN",
                "plot_7",
                "referential_complexity_moderate",
                "informational_complexity_moderate",
                "functional_complexity_moderate",
                "calendar",
                "misinformation_no",
                "insufficient_context_no",
            ],
            llm_evaluation=llm_evaluation,
            reference_time="2024-12-06T09:00:00-08:00",
            is_read_time="2024-12-06T09:00:00-08:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + (
                        "Ask User B to complete the following task. You are User A, Dawei Shen. "
                        "You want to know if you have any work meetings planned for next working week, starting Monday December 9 till Friday December 13. "
                        "You do not have any more information."
                    ),
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "Do I have any work meetings between now and Friday 13th December 2024?",
                },
            ],
            reasoning="The user has requested me to check what meetings they have from today, December 6th 2024 till and December 13th 2024. I will only tell the user events that are tagged as work based on their request. Over the next 7 days I have found one event that meets the criteria. It is a meeting on Friday December 13th 2024  called 'Team Review Meeting'. \nI tell the user this information.",
            success_conditions=[
                {
                    "input_text": "1. The meetings scheduled for the working week (from Monday December 9 till Friday December 13) are presented to the user, 'Team Review meeting' is the only one. ",
                    "statefullness": "Stateless",
                }
            ],
            tool_allow_list=["get_all_calendars", "search_calendar_events"],
            milestones=[
                # Milestone 0 – The agent looks up the calendar for the requested period
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
                # Milestone 1 – Verify that the Dec-13 Team Review Meeting was returned from the calendar lookup
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
                            column_similarity_measure={
                                "content": column_one_similarity
                            },
                            reference_milestone_node_index=0,
                        )
                    ]
                ),
                # Milestone 2 – The agent tells the user about the meeting
                Milestone(
                    snapshot_constraints=[
                        # Check the meeting name is mentioned
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.SANDBOX,
                            snapshot_constraint=snapshot_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "sender": RoleType.AGENT,
                                    "recipient": RoleType.USER,
                                    "content": "Team Review Meeting",
                                }
                            ),
                            column_similarity_measure={
                                "content": column_contains_similarity
                            },
                        ),
                    ]
                ),
            ],
            milestone_edge_list=[
                (0, 1),
                (1, 2),
            ],
        ),
    ]
