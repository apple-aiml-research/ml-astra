# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
import copy
import random
from typing import Dict, List, Optional, Set, Union, cast

import astra_tool_sandbox.tools
from astra_tool_sandbox.common.execution_context import ScenarioCategories
from astra_tool_sandbox.common.scenario import Scenario
from astra_tool_sandbox.common.tool_discovery import (
    ToolBackend,
    rank_tools_by_similarity,
)
from astra_tool_sandbox.scenarios.astra_v1.DAWEI_SHEN.dawei_shen_scenarios import (
    named_dawei_shen_scenarios,
)
from astra_tool_sandbox.scenarios.astra_v1.EMILY_ROSE.emily_rose_scenarios import (
    named_emily_rose_scenarios,
)
from astra_tool_sandbox.scenarios.astra_v1.JOHN_QUINN.john_quinn_scenarios import (
    named_john_quinn_scenarios,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.lucas_garcia_scenarios import (
    named_lucas_garcia_scenarios,
)
from astra_tool_sandbox.scenarios.astra_v1.THEO_APPLESEED.theo_appleseed_scenarios import (
    named_theo_appleseed_scenarios,
)


def named_scenarios(
    preferred_tool_backend: ToolBackend,
    llm_evaluation: Optional[bool] = False,
    desired_scenario_names: Optional[list[str]] = None,
    scenario_tags: Optional[list[str]] = None,
    add_user_simulator_few_shot_examples: bool = False,
    scenario_meta_info_only: bool = False,
) -> Union[Dict[str, Scenario], Dict[str, Dict[str, Union[str, List[str]]]]]:
    """Aggregate named scenarios from submodules

    In addition, adds tool augmentation scenarios for all

    Args:
        preferred_tool_backend: Which backend should be chosen in face of conflicting tool names.
        llm_evaluation:         Whether to use LLM to judge scenarios
        desired_scenario_names: Name of scenarios to run. If empty all scenarios will be
                                returned.
        scenario_tags:          Scenarios with the given list of tags to run. Need to cover all tags mentioned here.
        add_user_simulator_few_shot_examples: Whether to add user simulator few-shot examples to scenarios.
        scenario_meta_info_only: Whether to return only metadata (name and tags) instead of full scenario objects.
    Returns:
        A dictionary of scenarios (if scenario_meta_info_only=False) or scenario metadata (if scenario_meta_info_only=True)
    """
    # Define the protagonist scenario functions
    protagonist_functions = [
        named_dawei_shen_scenarios,
        named_theo_appleseed_scenarios,
        named_john_quinn_scenarios,
        named_emily_rose_scenarios,
        named_lucas_garcia_scenarios,
    ]

    if scenario_meta_info_only:
        # Handle metadata-only case
        scenarios_meta: Dict[str, Dict[str, Union[str, List[str]]]] = dict()
        for protagonist_func in protagonist_functions:
            new_scenarios = protagonist_func(
                preferred_tool_backend=preferred_tool_backend,
                llm_evaluation=llm_evaluation,
                desired_scenario_names=desired_scenario_names,
                scenario_tags=scenario_tags,
                add_user_simulator_few_shot_examples=add_user_simulator_few_shot_examples,
                scenario_meta_info_only=scenario_meta_info_only,
            )
            new_scenarios_meta = cast(
                Dict[str, Dict[str, Union[str, List[str]]]], new_scenarios
            )
            conflicting_names_meta: Set[str] = set(scenarios_meta.keys()) & set(
                new_scenarios_meta.keys()
            )
            if conflicting_names_meta:
                raise ValueError(
                    f"Conflicting names found between scenarios: {conflicting_names_meta}"
                )
            scenarios_meta.update(new_scenarios_meta)
        return scenarios_meta
    else:
        # Handle full scenarios case
        scenarios_full: Dict[str, Scenario] = dict()
        for protagonist_func in protagonist_functions:
            new_scenarios = protagonist_func(
                preferred_tool_backend=preferred_tool_backend,
                llm_evaluation=llm_evaluation,
                desired_scenario_names=desired_scenario_names,
                scenario_tags=scenario_tags,
                add_user_simulator_few_shot_examples=add_user_simulator_few_shot_examples,
                scenario_meta_info_only=scenario_meta_info_only,
            )
            new_scenarios_full = cast(Dict[str, Scenario], new_scenarios)
            conflicting_names_full: Set[str] = set(scenarios_full.keys()) & set(
                new_scenarios_full.keys()
            )
            if conflicting_names_full:
                raise ValueError(
                    f"Conflicting names found between scenarios: {conflicting_names_full}"
                )
            scenarios_full.update(new_scenarios_full)

        # # Add tool augmentations (commented out)
        # names = list(scenarios_full.keys())
        # for name in names:
        #     similar_tools = rank_tools_by_similarity(
        #         scenarios_full[name].starting_context.tool_allow_list,
        #         astra_tool_sandbox.tools,
        #         preferred_tool_backend=preferred_tool_backend,
        #     )
        #     # Shuffle base scenario tools
        #     assert scenarios_full[name].starting_context.tool_allow_list is not None
        #     random.shuffle(
        #         cast(list[str], scenarios_full[name].starting_context.tool_allow_list)
        #     )

        # # 3 distraction
        # scenario = copy.deepcopy(scenarios_full[name])
        # assert scenario.starting_context.tool_allow_list is not None
        # scenario.starting_context.tool_allow_list.extend(similar_tools[:3])
        # random.shuffle(scenario.starting_context.tool_allow_list)
        # scenario.categories.append(ScenarioCategories.THREE_DISTRACTION_TOOLS)
        # scenarios_full[f"{name}_3_distraction_tools"] = scenario

        # # 10 distraction
        # scenario = copy.deepcopy(scenarios_full[name])
        # assert scenario.starting_context.tool_allow_list is not None
        # scenario.starting_context.tool_allow_list.extend(similar_tools[:10])
        # random.shuffle(scenario.starting_context.tool_allow_list)
        # scenario.categories.append(ScenarioCategories.TEN_DISTRACTION_TOOLS)
        # scenarios_full[f"{name}_10_distraction_tools"] = scenario

        # # All tools
        # scenario = copy.deepcopy(scenarios_full[name])
        # assert scenario.starting_context.tool_allow_list is not None
        # scenario.starting_context.tool_allow_list.extend(similar_tools)
        # random.shuffle(scenario.starting_context.tool_allow_list)
        # scenario.categories.append(ScenarioCategories.ALL_TOOLS_AVAILABLE)
        # scenarios_full[f"{name}_all_tools"] = scenario

        # # No distraction. This is already there. Just add the tag
        # scenarios_full[name].categories.append(ScenarioCategories.NO_DISTRACTION_TOOLS)
        return scenarios_full
