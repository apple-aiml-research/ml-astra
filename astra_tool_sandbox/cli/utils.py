# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
import argparse
import logging
import traceback
from collections import Counter, defaultdict
from enum import auto
from importlib import import_module
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Type, Union, cast

from strenum import StrEnum

from astra_tool_sandbox.common.evaluation import compute_milestone_completion_score
from astra_tool_sandbox.common.execution_context import (
    RoleType,
    ScenarioCategories,
    get_current_context,
)
from astra_tool_sandbox.common.scenario import Scenario
from astra_tool_sandbox.common.tool_discovery import ToolBackend
from astra_tool_sandbox.roles.base_role import BaseRole
from astra_tool_sandbox.roles.execution_environment import ExecutionEnvironment
from astra_tool_sandbox.scenarios.astra_v1 import named_scenarios

logger = logging.getLogger(__name__)

#: Per-scenario key carrying the judge input from a pool worker back to the parent.
#: Private to the run: `score_llm_evaluations` removes it before anything is written,
#: so it never reaches result_summary.json or any downstream consumer.
LLM_EVAL_TASK_KEY = "_llm_eval_task"

#: Wall-clock budget for scenario *playback*. Grading and the LLM judge both run
#: outside it — grading because it is deterministic CPU work, the judge because it is
#: a network call that could otherwise exhaust the budget it is being timed against.
PLAY_TIMEOUT_SECONDS = 180

#: Separate backstop for rule-based grading. Deliberately far above what the heaviest
#: multi-milestone scenarios need: it exists only so a pathological milestone DFS
#: cannot hang a worker, not to ration normal grading. If this starts firing, the
#: matcher is the thing to look at, not this number.
GRADE_TIMEOUT_SECONDS = 600


def _lazy_factory(
    module: str,
    klass: str,
    *,
    extra: Optional[str] = None,
    kwargs: Optional[Dict[str, Any]] = None,
) -> Callable[..., BaseRole]:
    """
    Returns a callable that imports (module, klass) only when invoked,
    then instantiates it with kwargs (if provided).
    """

    def _ctor(*args: Any, **user_kwargs: Any) -> BaseRole:
        try:
            mod = import_module(module)
        except ModuleNotFoundError as e:
            if extra:
                raise RuntimeError(
                    f"Missing optional dependency for {klass}. "
                    f"Install extras from the repository root: pip install '.[{extra}]'"
                ) from e
            raise
        try:
            cls = cast(Type[BaseRole], getattr(mod, klass))
        except AttributeError as e:
            raise ImportError(f"Class {klass} not found in module {module}") from e
        init_kwargs = {**(kwargs or {}), **user_kwargs}
        return cls(*args, **init_kwargs)

    return _ctor


class RoleImplType(StrEnum):
    Hermes = auto()
    Gorilla = auto()
    GPT_4_o_2024_05_13 = auto()
    GPT_4_o_2024_11_20 = auto()
    GPT_4_o_mini_2024_07_18 = auto()
    GPT_4_1_2025_04_14 = auto()
    GPT_o_3_2025_04_16 = auto()
    GPT_5_2025_08_07 = auto()
    GPT_5_1_2025_11_13 = auto()
    # GPT_5_minimal_2025_08_07 = auto()
    # GPT_5_low_2025_08_07 = auto()
    # GPT_5_high_2025_08_07 = auto()
    DeepSeek_v3 = auto()
    Claude_3_Opus = auto()
    Claude_3_Sonnet = auto()
    Claude_3_Haiku = auto()
    Claude_3_5_Sonnet = auto()
    Claude_4_5_Opus = auto()
    Claude_4_5_Haiku = auto()
    Claude_4_5_Opus_Thinking = auto()
    Claude_4_5_Haiku_Thinking = auto()
    Claude_4_6_V1_Opus = auto()
    Claude_4_6_Sonnet = auto()
    Claude_4_7_Opus = auto()
    Claude_4_8_Opus = auto()
    Claude_Sonnet_5 = auto()
    Claude_4_6_V1_Opus_Thinking = auto()
    Claude_4_6_Sonnet_Thinking = auto()
    Claude_4_7_Opus_Thinking = auto()
    Claude_4_8_Opus_Thinking = auto()
    Claude_Sonnet_5_Thinking = auto()
    Gemini_1_0 = auto()
    Gemini_1_5 = auto()
    Gemini_1_5_Flash = auto()
    Gemini_2_5 = auto()
    Gemini_2_5_Flash = auto()
    Cli = auto()
    Deterministic = auto()
    Unhelpful = auto()
    Qwen_8B = auto()
    Qwen_32B = auto()


AGENT_TYPE_TO_FACTORY: dict[RoleImplType, Callable[..., BaseRole]] = {
    # GPT family
    RoleImplType.GPT_4_o_2024_05_13: _lazy_factory(
        "astra_tool_sandbox.roles.openai_api_agent", "GPT_4_o_2024_05_13_Agent"
    ),
    RoleImplType.GPT_4_o_2024_11_20: _lazy_factory(
        "astra_tool_sandbox.roles.openai_api_agent", "GPT_4_o_2024_11_20_Agent"
    ),
    RoleImplType.GPT_4_o_mini_2024_07_18: _lazy_factory(
        "astra_tool_sandbox.roles.openai_api_agent", "GPT_4_o_mini_2024_07_18_Agent"
    ),
    RoleImplType.GPT_o_3_2025_04_16: _lazy_factory(
        "astra_tool_sandbox.roles.openai_api_agent", "GPT_o_3_2025_04_16_Agent"
    ),
    RoleImplType.GPT_4_1_2025_04_14: _lazy_factory(
        "astra_tool_sandbox.roles.openai_api_agent", "GPT_4_1_2025_04_14_Agent"
    ),
    RoleImplType.GPT_5_2025_08_07: _lazy_factory(
        "astra_tool_sandbox.roles.openai_api_agent", "GPT_5_2025_08_07_Agent"
    ),
    RoleImplType.GPT_5_1_2025_11_13: _lazy_factory(
        "astra_tool_sandbox.roles.openai_api_agent", "GPT_5_1_2025_11_13_Agent"
    ),
    # RoleImplType.GPT_5_minimal_2025_08_07: _lazy_factory(
    #     "astra_tool_sandbox.roles.openai_api_agent", "GPT_5_minimal_2025_08_07_Agent"
    # ),
    # RoleImplType.GPT_5_low_2025_08_07: _lazy_factory(
    #     "astra_tool_sandbox.roles.openai_api_agent", "GPT_5_low_2025_08_07_Agent"
    # ),
    # RoleImplType.GPT_5_high_2025_08_07: _lazy_factory(
    #     "astra_tool_sandbox.roles.openai_api_agent", "GPT_5_high_2025_08_07_Agent"
    # ),
    RoleImplType.Hermes: _lazy_factory(
        "astra_tool_sandbox.roles.hermes_api_agent",
        "HermesAPIAgent",
        extra="agent-all",
        kwargs={"model_name": "NousResearch/Hermes-2-Pro-Mistral-7B"},
    ),
    RoleImplType.Gorilla: _lazy_factory(
        "astra_tool_sandbox.roles.gorilla_api_agent",
        "GorillaAPIAgent",
        extra="agent-all",
        kwargs={"model_name": "gorilla-llm/gorilla-openfunctions-v2"},
    ),
    RoleImplType.DeepSeek_v3: _lazy_factory(
        "astra_tool_sandbox.roles.deepseek_api_agent",
        "DeepSeekChatAgent",
        extra="agent-all",
    ),
    RoleImplType.Claude_3_Opus: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "ClaudeOpusAgent",
        extra="agent-all",
    ),
    RoleImplType.Claude_3_Sonnet: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "ClaudeSonnetAgent",
        extra="agent-all",
    ),
    RoleImplType.Claude_3_Haiku: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "ClaudeHaikuAgent",
        extra="agent-all",
    ),
    RoleImplType.Claude_3_5_Sonnet: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "Claude_3_5_Sonnet_Agent",
        extra="agent-all",
    ),
    RoleImplType.Claude_4_5_Opus: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "Claude_4_5_Opus_Agent",
        extra="agent-all",
    ),
    RoleImplType.Claude_4_5_Haiku: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "Claude_4_5_Haiku_Agent",
        extra="agent-all",
    ),
    RoleImplType.Claude_4_5_Opus_Thinking: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "Claude_4_5_Opus_Thinking_Agent",
        extra="agent-all",
    ),
    RoleImplType.Claude_4_5_Haiku_Thinking: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "Claude_4_5_Haiku_Thinking_Agent",
        extra="agent-all",
    ),
    RoleImplType.Claude_4_6_V1_Opus: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "Claude_4_6_V1_Opus_Agent",
        extra="agent-all",
    ),
    RoleImplType.Claude_4_6_Sonnet: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "Claude_4_6_Sonnet_Agent",
        extra="agent-all",
    ),
    RoleImplType.Claude_4_7_Opus: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "Claude_4_7_Opus_Agent",
        extra="agent-all",
    ),
    RoleImplType.Claude_4_8_Opus: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "Claude_4_8_Opus_Agent",
        extra="agent-all",
    ),
    RoleImplType.Claude_Sonnet_5: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "Claude_Sonnet_5_Agent",
        extra="agent-all",
    ),
    RoleImplType.Claude_4_6_V1_Opus_Thinking: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "Claude_4_6_V1_Opus_Thinking_Agent",
        extra="agent-all",
    ),
    RoleImplType.Claude_4_6_Sonnet_Thinking: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "Claude_4_6_Sonnet_Thinking_Agent",
        extra="agent-all",
    ),
    RoleImplType.Claude_4_7_Opus_Thinking: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "Claude_4_7_Opus_Thinking_Agent",
        extra="agent-all",
    ),
    RoleImplType.Claude_4_8_Opus_Thinking: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "Claude_4_8_Opus_Thinking_Agent",
        extra="agent-all",
    ),
    RoleImplType.Claude_Sonnet_5_Thinking: _lazy_factory(
        "astra_tool_sandbox.roles.anthropic_api_agent",
        "Claude_Sonnet_5_Thinking_Agent",
        extra="agent-all",
    ),
    RoleImplType.Gemini_1_0: _lazy_factory(
        "astra_tool_sandbox.roles.gemini_agent",
        "GeminiAgent",
        extra="agent-all",
        kwargs={"model_name": "gemini-1.0-pro"},
    ),
    RoleImplType.Gemini_1_5: _lazy_factory(
        "astra_tool_sandbox.roles.gemini_agent",
        "GeminiAgent",
        extra="agent-all",
        kwargs={"model_name": "gemini-1.5-pro-001"},
    ),
    RoleImplType.Gemini_1_5_Flash: _lazy_factory(
        "astra_tool_sandbox.roles.gemini_agent",
        "GeminiAgent",
        extra="agent-all",
        kwargs={"model_name": "gemini-1.5-flash-001"},
    ),
    # --- Utility roles (no extra) ---
    RoleImplType.Cli: _lazy_factory("astra_tool_sandbox.roles.cli_role", "CliAgent"),
    RoleImplType.Unhelpful: _lazy_factory(
        "astra_tool_sandbox.roles.unhelpful_agent", "UnhelpfulAgent"
    ),
    RoleImplType.Qwen_8B: _lazy_factory(
        "astra_tool_sandbox.roles.qwen_api_agent", "Qwen8BChatAgent"
    ),
    RoleImplType.Qwen_32B: _lazy_factory(
        "astra_tool_sandbox.roles.qwen_api_agent", "Qwen32BChatAgent"
    ),
}


USER_TYPE_TO_FACTORY: dict[RoleImplType, Callable[..., BaseRole]] = {
    # OpenAI (default)
    RoleImplType.GPT_4_o_2024_11_20: _lazy_factory(
        "astra_tool_sandbox.roles.openai_api_user", "GPT_4_o_2024_11_20_User"
    ),
    RoleImplType.GPT_4_1_2025_04_14: _lazy_factory(
        "astra_tool_sandbox.roles.openai_api_user", "GPT_4_1_2025_04_14_User"
    ),
    # Utility
    RoleImplType.Cli: _lazy_factory("astra_tool_sandbox.roles.cli_role", "CliUser"),
}
# The scenarios to play back when the `--test_mode` flag is set.
TEST_SCENARIO_NAMES = ["get_contact_count_DAWEI_SHEN"]


def get_available_scenarios_meta(
    scenario_tags: Optional[list[str]] = None,
) -> Dict[str, Dict[str, Union[str, List[str]]]]:
    """Get available scenario metadata without loading full scenario objects.

    This function uses the existing scenario architecture with the new
    scenario_meta_info_only parameter to efficiently retrieve metadata
    without loading complete scenario objects.

    Args:
        scenario_tags: List of tags to filter scenarios by

    Returns:
        Dict mapping scenario names to metadata dict containing 'name' and 'tags'
    """
    result = named_scenarios(
        preferred_tool_backend=ToolBackend.DEFAULT,  # Unused for metadata
        llm_evaluation=False,
        desired_scenario_names=None,
        scenario_tags=scenario_tags,
        add_user_simulator_few_shot_examples=False,
        scenario_meta_info_only=True,
    )
    # Since scenario_meta_info_only=True, this will always be metadata dict
    return cast(Dict[str, Dict[str, Union[str, List[str]]]], result)


def resolve_scenarios(
    desired_scenario_names: Optional[list[str]],
    scenario_tags: Optional[list[str]],
    preferred_tool_backend: ToolBackend,
    llm_evaluation: Optional[bool] = False,
    add_user_simulator_few_shot_examples: bool = False,
) -> dict[str, Scenario]:
    """Resolve the scenarios to run.

    Args:
        desired_scenario_names: Name of scenarios to run. If empty all scenarios will be
                                returned.
        scenario_tags:          Scenarios with the given list of tags to run. Need to cover all tags mentioned here.
        preferred_tool_backend: Which backend should be chosen in face of conflicting tool names.
        llm_evaluation:         Whether to use LLM judge for evaluation. By default is False.
        add_user_simulator_few_shot_examples: Whether to add user simulator few-shot examples to scenarios.

    Returns:
        Dictionary from scenario name to definition.
    """
    scenario_tags = [tag.lower() for tag in scenario_tags] if scenario_tags else None

    all_name_to_scenario = named_scenarios(
        preferred_tool_backend=preferred_tool_backend,
        llm_evaluation=llm_evaluation,
        desired_scenario_names=desired_scenario_names,
        scenario_tags=scenario_tags,
        add_user_simulator_few_shot_examples=add_user_simulator_few_shot_examples,
        scenario_meta_info_only=False,  # We want full scenarios, not just metadata
    )
    # Since scenario_meta_info_only=False, this will always be Dict[str, Scenario]
    all_name_to_scenario = cast(Dict[str, Scenario], all_name_to_scenario)

    if desired_scenario_names is None and scenario_tags is None:
        # No filtering needed. Return all scenarios.
        return all_name_to_scenario

    if scenario_tags and not all_name_to_scenario:
        raise KeyError(f"No scenarios found with tags {scenario_tags}")

    if desired_scenario_names and (
        len(desired_scenario_names) != len(all_name_to_scenario)
    ):
        missing_scenarios = set(desired_scenario_names) - set(
            all_name_to_scenario.keys()
        )
        raise KeyError(
            "The following desired scenarios do not exist: "
            f"{sorted(list(missing_scenarios))}"
        )

    return all_name_to_scenario


def run_scenario(
    name_and_scenario: tuple[str, Scenario],
    *,
    agent_type: RoleImplType,
    user_type: RoleImplType,
    args: argparse.Namespace,
    output_directory: Path,
) -> dict[str, Any]:
    """Play and evaluate a scenario.

    This is a necessary utility function to make multiprocessing work.

    Args:
        name_and_scenario:              Scenario name and Scenario object.
        agent_type:                     Agent type.
        user_type:                      User type.
        output_directory:               Directory to write output into.

    Returns:
        Evaluation info
    """
    agent = AGENT_TYPE_TO_FACTORY[agent_type]()

    user = USER_TYPE_TO_FACTORY[user_type]()

    name, scenario = name_and_scenario
    roles: dict[RoleType, BaseRole] = {
        RoleType.USER: user,
        RoleType.EXECUTION_ENVIRONMENT: ExecutionEnvironment(),
        RoleType.AGENT: agent,
    }
    output_directory.mkdir(parents=True, exist_ok=True)

    try:
        result = scenario.play_and_evaluate(
            roles=roles,
            output_directory=output_directory,
            scenario_name=name,
            play_timeout_seconds=PLAY_TIMEOUT_SECONDS,
            grade_timeout_seconds=GRADE_TIMEOUT_SECONDS,
        )

        # `play_and_evaluate` no longer re-raises when playback stops early: it grades
        # whatever trajectory exists and reports what went wrong. So a scenario that
        # failed part-way still contributes its real milestone scores here, and only
        # the metrics that genuinely could not be computed are left as None for the
        # aggregators to exclude.
        rule = result.evaluation_result
        judge = result.evaluation_LLM_result
        return {
            "name": name,
            "categories": scenario.categories,
            "tags": scenario.tags,
            "traceback": result.play_traceback,
            "exception_type": result.play_exception_type,
            "milestone_similarity": rule.milestone_similarity if rule else None,
            "minefield_similarity": rule.minefield_similarity if rule else None,
            "similarity": rule.similarity if rule else None,
            # Never None: the aggregator appends turn_count unconditionally.
            "turn_count": rule.turn_count if rule else scenario.max_messages,
            # Recoverable agent failure modes. Both leave no other trace in the
            # summary: the scenario completes and simply scores low.
            "empty_agent_turn_count": rule.empty_agent_turn_count if rule else 0,
            "hallucinated_tool_call_count": (
                rule.hallucinated_tool_call_count if rule else 0
            ),
            "retrieval_get_all_count": rule.retrieval_get_all_count if rule else 0,
            "retrieval_failed_search_count": (
                rule.retrieval_failed_search_count if rule else 0
            ),
            "retrieval_efficiency": rule.retrieval_efficiency if rule else None,
            "milestone_mapping": rule.milestone_mapping if rule else {},
            "minefield_mapping": rule.minefield_mapping if rule else {},
            "milestone_completion_score": (
                compute_milestone_completion_score(
                    scenario.evaluation.milestone_matcher.milestones,
                    rule.milestone_mapping,
                    rule.minefield_similarity,
                )
                if rule
                else None
            ),
            "llm_evaluation_review": judge.review_reason if judge else "",
            "llm_evaluation_tool_call_capability": (
                judge.tool_call_capability if judge else None
            ),
            "llm_evaluation_information_retrieval_capability": (
                judge.information_retrieval_capability if judge else None
            ),
            "llm_evaluation_task_completion": judge.task_completion if judge else None,
            "llm_evaluation_conversation_efficiency": (
                judge.conversation_efficiency if judge else None
            ),
            "llm_evaluation_no_hallucination_score": (
                judge.no_hallucination_score if judge else None
            ),
            # Scored after the pool drains by cli.score_llm_evaluations, then
            # stripped before the summary is written.
            LLM_EVAL_TASK_KEY: result.llm_eval_task,
        }
    except Exception as e:
        # Reaching here now means the harness itself failed outside playback —
        # scenario construction, role setup, or grading on a *complete* trajectory.
        # Playback that stopped early is handled above and keeps its real scores.
        logger.error(
            "Scenario %r failed (%s): %s\n%s",
            name,
            type(e).__name__,
            e,
            traceback.format_exc(),
        )
        return {
            "name": name,
            "categories": scenario.categories,
            "tags": scenario.tags,
            "traceback": traceback.format_exc(),
            "exception_type": type(e).__name__,
            "milestone_similarity": 0,
            "minefield_similarity": 0,
            "similarity": 0,
            "turn_count": scenario.max_messages,
            "empty_agent_turn_count": 0,
            "hallucinated_tool_call_count": 0,
            "retrieval_get_all_count": 0,
            "retrieval_failed_search_count": 0,
            "retrieval_efficiency": None,
            "milestone_mapping": {},
            "minefield_mapping": {},
            "milestone_completion_score": None,
            "llm_evaluation_review": "",
            "llm_evaluation_tool_call_capability": 0,
            "llm_evaluation_information_retrieval_capability": 0,
            "llm_evaluation_task_completion": 0,
            "llm_evaluation_conversation_efficiency": 0,
            "llm_evaluation_no_hallucination_score": 0,
        }
    finally:
        for role in roles.values():
            role.teardown()


def get_category_summary(
    result_summary: list[dict[str, Any]],
) -> dict[str, dict[str, list[float]]]:
    """Aggregate per test case result summary into category wise summary.

    Args:
        result_summary:     A list of results for each test case.

    Returns:
        Category wise summary.
    """
    # Aggregate results by category
    category_summary: dict[str, dict[str, list[float]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for current_summary in result_summary:
        for category in current_summary["categories"]:
            # The augmented scenarios are based on top of the `THREE_DISTRACTION_TOOLS`,
            # but we do not want to double count the stats for `THREE_DISTRACTION_TOOLS`.
            # Otherwise it would not be comparable to e.g. `TEN_DISTRACTION_TOOLS`.
            if category == ScenarioCategories.THREE_DISTRACTION_TOOLS and set(
                current_summary["categories"]
            ) & {
                ScenarioCategories.TOOL_NAME_SCRAMBLED,
                ScenarioCategories.TOOL_DESCRIPTION_SCRAMBLED,
                ScenarioCategories.ARG_DESCRIPTION_SCRAMBLED,
                ScenarioCategories.ARG_TYPE_SCRAMBLED,
                ScenarioCategories.ARG_NAME_SCRAMBLED,
            }:
                continue
            # similarity is None when the scenario stopped early and could not be
            # graded at all. Exclude it rather than appending None, which would blow
            # up the `sum(v) / len(v)` in cli.write_result_summary at the very end of
            # a run and take the whole summary with it. Same treatment as
            # retrieval_efficiency below.
            if current_summary.get("similarity") is not None:
                category_summary[category]["similarity"].append(
                    current_summary["similarity"]
                )
            category_summary[category]["turn_count"].append(
                current_summary["turn_count"]
            )
            category_summary[category]["retrieval_get_all_count"].append(
                current_summary.get("retrieval_get_all_count", 0)
            )
            category_summary[category]["retrieval_failed_search_count"].append(
                current_summary.get("retrieval_failed_search_count", 0)
            )
            # retrieval_efficiency is None (N/A) when no retrieval calls -> exclude from mean
            if current_summary.get("retrieval_efficiency") is not None:
                category_summary[category]["retrieval_efficiency"].append(
                    current_summary["retrieval_efficiency"]
                )
        if current_summary.get("similarity") is not None:
            category_summary["ALL_CATEGORIES"]["similarity"].append(
                current_summary["similarity"]
            )
        category_summary["ALL_CATEGORIES"]["turn_count"].append(
            current_summary["turn_count"]
        )
        category_summary["ALL_CATEGORIES"]["retrieval_get_all_count"].append(
            current_summary.get("retrieval_get_all_count", 0)
        )
        category_summary["ALL_CATEGORIES"]["retrieval_failed_search_count"].append(
            current_summary.get("retrieval_failed_search_count", 0)
        )
        if current_summary.get("retrieval_efficiency") is not None:
            category_summary["ALL_CATEGORIES"]["retrieval_efficiency"].append(
                current_summary["retrieval_efficiency"]
            )
    return category_summary


def get_category_to_scenario_count(
    name_to_scenario: dict[str, Scenario],
) -> Counter[Union[ScenarioCategories, str]]:
    """Count number of scenarios based on ScenarioCategories.

    Args:
        name_to_scenario:   A dict with scenario name as keys, scenario objects as values.

    Returns:
        A counter object containing counts for each category.
    """
    category_counter: Counter[Union[ScenarioCategories, str]] = Counter()
    for scenario in name_to_scenario.values():
        for category in scenario.categories:
            # The augmented scenarios are based on top of the `THREE_DISTRACTION_TOOLS`,
            # but we do not want to double count the stats for `THREE_DISTRACTION_TOOLS`.
            # Otherwise it would not be comparable to e.g. `TEN_DISTRACTION_TOOLS`.
            if category == ScenarioCategories.THREE_DISTRACTION_TOOLS and set(
                scenario.categories
            ) & {
                ScenarioCategories.TOOL_NAME_SCRAMBLED,
                ScenarioCategories.TOOL_DESCRIPTION_SCRAMBLED,
                ScenarioCategories.ARG_DESCRIPTION_SCRAMBLED,
                ScenarioCategories.ARG_TYPE_SCRAMBLED,
                ScenarioCategories.ARG_NAME_SCRAMBLED,
            }:
                continue
            category_counter[category] += 1
        category_counter["ALL_CATEGORIES"] += 1
    return category_counter


def get_necessary_tool_name_to_scenario_count(
    name_to_scenario: dict[str, Scenario],
) -> Counter[Union[ScenarioCategories, str]]:
    """Count number of scenarios based on necessary tool names.

    Args:
        name_to_scenario:   A dict with scenario name as keys, scenario objects as values.

    Returns:
        A counter object containing counts for each necessary tool names.
    """
    tool_name_counter: Counter[Union[ScenarioCategories, str]] = Counter(
        {
            tool_name: 0
            for tool_name in get_current_context().get_available_tools(
                scrambling_allowed=False
            )
        }
    )
    # # Necessary tool names can be deducted from allowed tools in NO_DISTRACTION_TOOLS category
    # # Then the total count equals the count from this category * number of augmentations.
    # augmentation_categories: set[Union[ScenarioCategories, str]] = set()
    for scenario in name_to_scenario.values():
        # if ScenarioCategories.NO_DISTRACTION_TOOLS in scenario.categories:
        #         assert scenario.starting_context.tool_allow_list is not None
        #         for necessary_tool in scenario.starting_context.tool_allow_list:
        #             tool_name_counter[necessary_tool] += 1
        #     augmentation_categories |= {
        #         ScenarioCategories.NO_DISTRACTION_TOOLS,
        #         ScenarioCategories.THREE_DISTRACTION_TOOLS,
        #         ScenarioCategories.TEN_DISTRACTION_TOOLS,
        #         ScenarioCategories.ALL_TOOLS_AVAILABLE,
        #         ScenarioCategories.TOOL_NAME_SCRAMBLED,
        #         ScenarioCategories.TOOL_DESCRIPTION_SCRAMBLED,
        #         ScenarioCategories.ARG_DESCRIPTION_SCRAMBLED,
        #         ScenarioCategories.ARG_TYPE_SCRAMBLED,
        #         ScenarioCategories.ARG_NAME_SCRAMBLED,
        #     } & set(scenario.categories)
        # for necessary_tool in tool_name_counter:
        #     tool_name_counter[necessary_tool] *= len(augmentation_categories)
        if scenario.starting_context.tool_allow_list is not None:
            for tool in scenario.starting_context.tool_allow_list:
                if tool in tool_name_counter:
                    tool_name_counter[tool] += 1
    return tool_name_counter
