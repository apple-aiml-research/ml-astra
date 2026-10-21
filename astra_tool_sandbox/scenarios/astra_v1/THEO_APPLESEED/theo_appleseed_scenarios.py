# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Scenarios where more than 1 tool call to be issued to complete the task"""

from typing import Any, Dict, List, Optional, Union, cast

import polars as pl
import yaml

from astra_tool_sandbox.common.constants import PACKAGE_DIR
from astra_tool_sandbox.common.evaluation import (
    Milestone,
    SnapshotConstraint,
    addition_similarity,
)
from astra_tool_sandbox.common.execution_context import (
    DatabaseNamespace,
    RoleType,
    ScenarioCategories,
)
from astra_tool_sandbox.common.scenario import Scenario, ScenarioExtension
from astra_tool_sandbox.common.tool_discovery import ToolBackend
from astra_tool_sandbox.scenarios.astra_v1.base_scenarios import named_base_scenarios
from astra_tool_sandbox.scenarios.astra_v1.protagonist_simulator_few_shot_examples import (
    USER_INSTRUCTION_SINGLE_TURN,
)
from astra_tool_sandbox.scenarios.astra_v1.protagonists import ProtagonistName
from astra_tool_sandbox.scenarios.astra_v1.THEO_APPLESEED.converted_TAG_scenarios import (
    annotated_base_scenarios,
)


def load_bio() -> Dict[str, Any]:
    bio_path = PACKAGE_DIR / "scenarios" / "astra_v1" / "THEO_APPLESEED" / "bio.yaml"
    with open(bio_path) as f:
        return cast(Dict[str, Any], yaml.safe_load(f))


protagonist_bio = load_bio()


def get_extensions(
    base_scenarios: dict[str, Scenario],
    llm_evaluation: Optional[bool] = False,
    protagonist_name: str = "THEO_APPLESEED",
) -> list[ScenarioExtension]:
    """Specify test scenario as extensions over a base scenario

    Returns:
        A list of ScenarioExtensions
    """
    # user_simulator_few_shot_examples = named_user_simulator_few_shot_examples()

    return [
        ScenarioExtension(
            name=f"get_make_phonecall_phonenumber_{protagonist_name}",
            base_scenario=base_scenarios["base"],
            tags=[protagonist_name, "phonecall", "test"],
            llm_evaluation=llm_evaluation,
            reference_time="2024-07-27 08:05:00",
            messages=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.USER,
                    "content": USER_INSTRUCTION_SINGLE_TURN
                    + f"Ask User B to call John Appleseed. You are User A, {protagonist_bio['name']}"
                    "You do not have any more information.",
                },
                {
                    "sender": RoleType.USER,
                    "recipient": RoleType.AGENT,
                    "content": "call John Appleseed.",
                },
            ],
            reasoning="The user wants to place a call to John Appleseed. I will look up John Appleseed in the contacts to find their phone number, then call create_outgoing_call with that number.",
            success_conditions=[
                {
                    "input_text": "1. An outgoing call is placed to John Appleseed at 1234-5678-9102.",
                    "statefullness": "Stateful",
                },
            ],
            tool_allow_list=[
                "create_outgoing_call",
                "search_contacts",
                "get_all_contacts",
            ],
            milestones=[
                Milestone(
                    snapshot_constraints=[
                        SnapshotConstraint(
                            database_namespace=DatabaseNamespace.PHONE,
                            snapshot_constraint=addition_similarity,
                            target_dataframe=pl.DataFrame(
                                {
                                    "caller_address": "1234-5678-9101",
                                    "receiver_address": "1234-5678-9102",
                                },
                            ),
                            reference_milestone_node_index=-1,
                        )
                    ],
                ),
            ],
        ),
    ]


def named_theo_appleseed_scenarios(
    preferred_tool_backend: ToolBackend,
    llm_evaluation: Optional[bool] = False,
    desired_scenario_names: Optional[list[str]] = None,
    scenario_tags: Optional[list[str]] = None,
    add_user_simulator_few_shot_examples: bool = False,
    scenario_meta_info_only: bool = False,
) -> Union[Dict[str, Scenario], Dict[str, Dict[str, Union[str, List[str]]]]]:
    """Scenarios where more than 1 tool call to be issued to complete the task

    Note that this differs from the simple / multi definition of Gorilla. All scenarios below have only the necessary
    tools provided to the model. Additional scenarios will be created to introduce distractions as well.

    Args:
        preferred_tool_backend: Which backend should be chosen in face of conflicting tool names.
        llm_evaluation:         Whether to use LLM to judge scenarios
        desired_scenario_names: Name of scenarios to run. If empty all scenarios will be
                                returned.
        scenario_tags:          Scenarios with the given list of tags to run. Need to cover all tags mentioned here.
        add_user_simulator_few_shot_examples: Whether to add user simulator few-shot examples to scenarios.
    Returns:
        A dict containing scenario name and scenario
    """
    # preferred_tool_backend = ToolBackend.DEFAULT
    base_scenarios = named_base_scenarios(
        protagonist_name=cast(ProtagonistName, "THEO_APPLESEED"),
        preferred_tool_backend=preferred_tool_backend,
        single_turn_user_simulator=True,
        add_user_simulator_few_shot_examples=add_user_simulator_few_shot_examples,
    )
    extensions = get_extensions(
        base_scenarios,
        llm_evaluation=llm_evaluation,
    )
    # # extended with TAG scenarios
    extensions.extend(
        annotated_base_scenarios(
            base_scenarios,
            llm_evaluation=llm_evaluation,
        )
    )
    # All scenarios in this module should be single user turn, multiple tool. Add these categories if they aren't there
    for extension in extensions:
        for default_categories in [
            ScenarioCategories.MULTIPLE_TOOL_CALL,
            ScenarioCategories.SINGLE_USER_TURN,
        ]:
            if default_categories not in extension.categories:
                extension.categories.append(default_categories)

    ## NOTE: For debugging purposes
    # loaded_scenarios = {}
    # try:
    #     for extension in extensions:
    #         extension_scenarios = extension.get_extended_scenario()
    #         for key, scenario in extension_scenarios.items():
    #             loaded_scenarios.update({key: scenario})
    # except IndexError as e:
    #     print(f"Error occurred while processing extension: {extension}")
    #     print(f"Last processed key: {key if 'key' in locals() else 'N/A'}")
    #     raise

    # return loaded_scenarios
    """ return scenario extensions with selected ones only and full clipped dataset """
    if desired_scenario_names or scenario_tags:
        # if scenarios selected criteria provided, only load the mentioned ones
        if not scenario_meta_info_only:
            return {
                key: extension.get_extended_scenario()[key]
                for extension in extensions
                for key, scenario in extension.get_extended_scenario_meta().items()
                if (desired_scenario_names and (key in desired_scenario_names))
                or (scenario_tags and (set(scenario["tags"]).issuperset(scenario_tags)))
            }
        else:
            return {
                key: scenario
                for extension in extensions
                for key, scenario in extension.get_extended_scenario_meta().items()
                if (desired_scenario_names and (key in desired_scenario_names))
                or (scenario_tags and (set(scenario["tags"]).issuperset(scenario_tags)))
            }
    else:
        # return all scenarios
        if not scenario_meta_info_only:
            return {
                key: scenario
                for extension in extensions
                for key, scenario in extension.get_extended_scenario().items()
            }
        else:
            return {
                key: scenario
                for extension in extensions
                for key, scenario in extension.get_extended_scenario_meta().items()
            }
