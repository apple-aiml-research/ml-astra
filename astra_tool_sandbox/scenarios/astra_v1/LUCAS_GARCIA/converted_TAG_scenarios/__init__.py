# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
import copy
import random
from pathlib import Path
from typing import Dict, List, Optional, Set, cast

import astra_tool_sandbox.tools
from astra_tool_sandbox.common.evaluation import milestone_tagger
from astra_tool_sandbox.common.execution_context import ScenarioCategories
from astra_tool_sandbox.common.scenario import Scenario, ScenarioExtension
from astra_tool_sandbox.common.tool_discovery import (
    ToolBackend,
    rank_tools_by_similarity,
)
from astra_tool_sandbox.scenarios.astra_v1.base_scenarios import named_base_scenarios
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_challenging_scenarios import (
    get_TAG_LUCAS_GARCIA_challenging_scenarios,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_1_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_1,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_2_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_2,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_3_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_3,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_4_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_4,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_5_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_5,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_6_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_6,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_7_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_7,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_8_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_8,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_9_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_9,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_10_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_10,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_11_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_11,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_12_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_12,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_13_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_13,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_14_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_14,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_15_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_15,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_16_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_16,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_17_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_17,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_18_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_18,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_19_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_19,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_20_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_20,
)
from astra_tool_sandbox.scenarios.astra_v1.LUCAS_GARCIA.converted_TAG_scenarios.converted_TAG_pilot_plot_21_scenarios import (
    get_TAG_LUCAS_GARCIA_pilot_plot_21,
)


def annotated_base_scenarios(
    base_scenarios: dict[str, Scenario],
    protagonist_name: str = "LUCAS_GARCIA",
    output_dir: Path = Path(__file__).parent,
    llm_evaluation: Optional[bool] = False,
) -> List[ScenarioExtension]:
    """Scenarios where more than 1 tool call to be issued to complete the task

    Note that this differs from the simple / multi definition of Gorilla. All scenarios below have only the necessary
    tools provided to the model. Additional scenarios will be created to introduce distractions as well.

    Args:
        preferred_tool_backend: Which backend should be chosen in face of conflicting tool names.

    Returns:
        A dict containing scenario name and scenario
    """
    # preferred_tool_backend = ToolBackend.DEFAULT
    extensions = get_TAG_LUCAS_GARCIA_pilot_plot_1(
        base_scenarios, llm_evaluation=llm_evaluation
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_2(base_scenarios, llm_evaluation=llm_evaluation)
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_3(base_scenarios, llm_evaluation=llm_evaluation)
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_4(base_scenarios, llm_evaluation=llm_evaluation)
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_5(base_scenarios, llm_evaluation=llm_evaluation)
    )

    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_6(base_scenarios, llm_evaluation=llm_evaluation)
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_7(base_scenarios, llm_evaluation=llm_evaluation)
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_8(base_scenarios, llm_evaluation=llm_evaluation)
    )

    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_9(base_scenarios, llm_evaluation=llm_evaluation)
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_10(
            base_scenarios, llm_evaluation=llm_evaluation
        )
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_11(
            base_scenarios, llm_evaluation=llm_evaluation
        )
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_12(
            base_scenarios, llm_evaluation=llm_evaluation
        )
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_13(
            base_scenarios, llm_evaluation=llm_evaluation
        )
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_14(
            base_scenarios, llm_evaluation=llm_evaluation
        )
    )

    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_15(
            base_scenarios, llm_evaluation=llm_evaluation
        )
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_16(
            base_scenarios, llm_evaluation=llm_evaluation
        )
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_17(
            base_scenarios, llm_evaluation=llm_evaluation
        )
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_18(
            base_scenarios, llm_evaluation=llm_evaluation
        )
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_19(
            base_scenarios, llm_evaluation=llm_evaluation
        )
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_20(
            base_scenarios, llm_evaluation=llm_evaluation
        )
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_pilot_plot_21(
            base_scenarios, llm_evaluation=llm_evaluation
        )
    )
    extensions.extend(
        get_TAG_LUCAS_GARCIA_challenging_scenarios(
            base_scenarios, llm_evaluation=llm_evaluation
        )
    )
    milestone_tagger(extensions, output_dir)

    return extensions
