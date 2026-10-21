# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Run all scenarios in the tool sandbox."""

from __future__ import annotations

import argparse
import datetime
import json
import logging
import multiprocessing
import os
import random
import subprocess
import sys
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from typing import Any, Optional, Union

import polars as pl
from dotenv import load_dotenv
from tqdm import tqdm

from astra_tool_sandbox.cli.utils import (
    AGENT_TYPE_TO_FACTORY,
    LLM_EVAL_TASK_KEY,
    TEST_SCENARIO_NAMES,
    USER_TYPE_TO_FACTORY,
    RoleImplType,
    get_category_summary,
    get_category_to_scenario_count,
    get_necessary_tool_name_to_scenario_count,
    resolve_scenarios,
    run_scenario,
)
from astra_tool_sandbox.common.evaluation import (
    EvaluationLLM,
    compute_milestone_completion_score,
)
from astra_tool_sandbox.common.execution_context import ScenarioCategories
from astra_tool_sandbox.common.scenario import Scenario
from astra_tool_sandbox.common.tool_discovery import ToolBackend

logger = logging.getLogger(__name__)

#: Default pacing for the LLM judge. Public model APIs enforce per-key request-rate
#: limits, and exceeding one does not fail the run — the scenario is simply left
#: unjudged — so the burst has to be prevented rather than detected.
JUDGE_MAX_REQUESTS_PER_MINUTE = 60


class _RequestPacer:
    """Thread-safe minimum-interval gate on outbound requests.

    A minimum interval rather than a token bucket on purpose: a bucket permits an
    initial burst equal to its capacity, which is precisely the shape that trips a
    sliding-window rate limit. Spacing every request evenly cannot.
    """

    def __init__(self, requests_per_minute: int) -> None:
        self._min_interval = (
            60.0 / requests_per_minute if requests_per_minute > 0 else 0.0
        )
        self._lock = threading.Lock()
        self._next_allowed = 0.0

    def wait(self) -> None:
        if self._min_interval <= 0:
            return
        with self._lock:
            now = time.monotonic()
            sleep_for = self._next_allowed - now
            # Schedule from the later of "now" and the previous slot, so an idle gap
            # does not bank credit for a burst.
            self._next_allowed = max(now, self._next_allowed) + self._min_interval
        if sleep_for > 0:
            time.sleep(sleep_for)


def score_llm_evaluations(
    result_summary: list[dict[str, Any]],
    processes: int,
    requests_per_minute: int = JUDGE_MAX_REQUESTS_PER_MINUTE,
) -> None:
    """Run the LLM judge over every prepared eval task, in place.

    Called once after the scenario pool drains. Each worker built its scenario's judge
    input (which needs the live ExecutionContext) and passed it back as plain data, so
    all that is left here is the network-bound half — which parallelises with threads
    and, crucially, runs with no per-scenario alarm armed.

    A judge failure never fails the run: that scenario keeps None judge scores and is
    counted in the warning below, so it shows up as unjudged rather than as a zero.
    """
    pending = [row for row in result_summary if row.get(LLM_EVAL_TASK_KEY)]
    if not pending:
        # llm_evaluation off, or resumed rows only — strip the key and move on.
        for row in result_summary:
            row.pop(LLM_EVAL_TASK_KEY, None)
        return

    failures = 0
    pacer = _RequestPacer(requests_per_minute)

    def _score(row: dict[str, Any]) -> None:
        nonlocal failures
        pacer.wait()
        try:
            judged = EvaluationLLM.score_eval_task(row[LLM_EVAL_TASK_KEY])
        except Exception:
            failures += 1
            logger.warning(
                "LLM judge failed for scenario %r; leaving it unjudged",
                row.get("name"),
                exc_info=True,
            )
            return
        row["llm_evaluation_review"] = judged.review_reason or ""
        row["llm_evaluation_tool_call_capability"] = judged.tool_call_capability
        row["llm_evaluation_information_retrieval_capability"] = (
            judged.information_retrieval_capability
        )
        row["llm_evaluation_task_completion"] = judged.task_completion
        row["llm_evaluation_conversation_efficiency"] = judged.conversation_efficiency
        row["llm_evaluation_no_hallucination_score"] = judged.no_hallucination_score

    if requests_per_minute > 0:
        logger.info(
            "Judging %d scenarios at <=%d req/min (>=%.1f min).",
            len(pending),
            requests_per_minute,
            len(pending) / requests_per_minute,
        )

    # Threads, not processes: this is pure I/O against the judge endpoint, and the
    # eval tasks are already in this process.
    with ThreadPoolExecutor(max_workers=max(1, processes)) as executor:
        list(
            tqdm(
                executor.map(_score, pending),
                total=len(pending),
                desc="LLM judge",
            )
        )

    # Never leak the judge input into result_summary.json.
    for row in result_summary:
        row.pop(LLM_EVAL_TASK_KEY, None)

    if failures:
        logger.warning(
            "%d/%d scenarios could not be judged; their llm_evaluation_* stay null",
            failures,
            len(pending),
        )


DEFAULT_USER_TYPE = RoleImplType.GPT_4_o_2024_11_20


def get_git_sha() -> Optional[str]:
    """Get the git SHA of the `HEAD` branch."""
    # From https://stackoverflow.com/a/21901260
    # Note that there are some 3rd party Python modules for interacting with git. I have
    # tried `pygit2` and `GitPython`, but both failed to get the commit associated with
    # `HEAD` for me.
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "HEAD"])
            .decode("ascii")
            .strip()
        )
    except subprocess.CalledProcessError:
        # The tool sandbox script was not executed from within the git repository so we
        # cannot figure out the git SHA.
        return None


def has_local_changes() -> bool:
    # From https://stackoverflow.com/a/3878934 . `git diff --exit-code` will return 0 if
    # there are no local changes. The `--quiet` suppresses printing to stdout. Note that
    # this approach does not detect untracked files, but this should be fine for our
    # purposes.
    completed_proc = subprocess.run(["git", "diff", "--exit-code", "--quiet"])
    return completed_proc.returncode == 1


def write_result_summary(
    result_summary: list[dict[str, Any]],
    category_summary: dict[str, dict[str, list[float]]],
    output_directory: Path,
) -> None:
    # Try to get the current git SHA so that there is some provenance on with which
    # version of the code results have been generated with.
    git_sha = get_git_sha()
    if git_sha is not None and has_local_changes():
        git_sha += " + local changes"

    with open(output_directory / "result_summary.json", "w") as f:
        json.dump(
            {
                "per_scenario_results": result_summary,
                "category_aggregated_results": {
                    category: {
                        k: (sum(v) / len(v) if v else None)
                        for k, v in aggregation.items()
                    }
                    for category, aggregation in category_summary.items()
                },
                "git_sha": git_sha,
            },
            f,
            indent=4,
            ensure_ascii=False,
        )


def load_results_from_trajectories(
    output_directory: Path,
    name_to_scenario: dict[str, Scenario] | None = None,
) -> list[dict[str, Any]]:
    """Load evaluation results from existing trajectory files.

    This enables resuming incomplete runs by reading results from previously
    executed scenarios and including them in the final result_summary.json.

    Args:
        output_directory: Directory containing trajectories/ subdirectory
        name_to_scenario: Optional mapping used to recompute
            ``milestone_completion_score`` for resumed scenarios (needs the
            scenario's milestone definitions, which aren't persisted in
            ``execution_context.json``). When absent, the score is left ``None``.

    Returns:
        List of result dictionaries in the same format as run_scenario() returns
    """
    results: list[dict[str, Any]] = []
    trajectories_dir = output_directory / "trajectories"

    if not trajectories_dir.exists():
        return results

    for scenario_dir in trajectories_dir.iterdir():
        if not scenario_dir.is_dir():
            continue

        exec_context_file = scenario_dir / "execution_context.json"
        if exec_context_file.exists():
            try:
                with open(exec_context_file, "r") as f:
                    data = json.load(f)
                    if "evaluation_result" in data:
                        milestone_mapping = data["evaluation_result"].get(
                            "milestone_mapping", {}
                        )
                        completion_score: float | None = None
                        if name_to_scenario is not None:
                            scenario = name_to_scenario.get(scenario_dir.name)
                            if scenario is not None:
                                completion_score = compute_milestone_completion_score(
                                    scenario.evaluation.milestone_matcher.milestones,
                                    milestone_mapping,
                                    data["evaluation_result"].get(
                                        "minefield_similarity", 0
                                    ),
                                )
                        results.append(
                            {
                                "name": scenario_dir.name,
                                "categories": data.get("categories", []),
                                "tags": data.get("tags", []),
                                "traceback": data.get("traceback"),
                                "exception_type": data.get("exception_type"),
                                "milestone_similarity": data["evaluation_result"].get(
                                    "milestone_similarity", 0
                                ),
                                "minefield_similarity": data["evaluation_result"].get(
                                    "minefield_similarity", 0
                                ),
                                "similarity": data["evaluation_result"].get(
                                    "similarity", 0
                                ),
                                "turn_count": data["evaluation_result"].get(
                                    "turn_count", 0
                                ),
                                "retrieval_get_all_count": data[
                                    "evaluation_result"
                                ].get("retrieval_get_all_count", 0),
                                "retrieval_failed_search_count": data[
                                    "evaluation_result"
                                ].get("retrieval_failed_search_count", 0),
                                "retrieval_efficiency": data["evaluation_result"].get(
                                    "retrieval_efficiency", None
                                ),
                                "milestone_mapping": milestone_mapping,
                                "minefield_mapping": data["evaluation_result"].get(
                                    "minefield_mapping", {}
                                ),
                                "milestone_completion_score": completion_score,
                                "llm_evaluation_review": data.get(
                                    "evaluation_LLM_result", {}
                                ).get("review_reason", ""),
                                "llm_evaluation_tool_call_capability": data.get(
                                    "evaluation_LLM_result", {}
                                ).get("tool_call_capability", 0),
                                "llm_evaluation_information_retrieval_capability": data.get(
                                    "evaluation_LLM_result", {}
                                ).get("information_retrieval_capability", 0),
                                "llm_evaluation_task_completion": data.get(
                                    "evaluation_LLM_result", {}
                                ).get("task_completion", 0),
                            }
                        )
            except Exception as e:
                print(f"Warning: Could not load trajectory {scenario_dir.name}: {e}")

    return results


def run_sandbox(
    *,
    args: argparse.Namespace,
    agent_type: RoleImplType,
    user_type: RoleImplType,
    name_to_scenario: dict[str, Scenario],
    processes: int,
    output_base_dir: Path,
) -> int:
    """Entry point for Tool Sandbox

    Args:
        agent_type:       The agent type to use.
        user_type:        The user type to use.
        name_to_scenario: Dictionary from scenario name to scenario definition.
        processes:        Number of processes to run in parallel.
        output_base_dir:  Base directory for model outputs.

    Returns:
        The number of scenarios that failed to run.
    """
    # Show all rows and all columns when converting polars dataframes to strings.
    # Sadly, there is no way to specify an unlimited format length for strings. Note
    # that for tracebacks or long explanations from Claude 3 Opus a value of `1000` was
    # insufficient.
    pl.Config.set_tbl_rows(-1).set_tbl_cols(-1).set_fmt_str_lengths(10000)
    pl.Config.set_tbl_formatting("ASCII_FULL")

    agent = AGENT_TYPE_TO_FACTORY[agent_type]()

    user = USER_TYPE_TO_FACTORY[user_type]()
    output_directory = (
        Path(output_base_dir) / f"agent_{getattr(agent, 'model_name', agent_type)}_"
        f"user_{getattr(user, 'model_name', user_type)}_"
        f"{datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}"
    )
    print(f"Storing outputs to '{output_directory}'.")

    # Print a category-wise count before playing scenarios
    category_counter: Counter[Union[ScenarioCategories, str]] = (
        get_category_to_scenario_count(name_to_scenario)
    )
    print(
        "Number of test cases per category:",
        json.dumps(
            {str(k): v for k, v in category_counter.most_common(len(category_counter))},
            indent=4,
            ensure_ascii=False,
        ),
    )
    # Print a necessary tool-wise count before playing scenarios
    necessary_tool_counter: Counter[str] = get_necessary_tool_name_to_scenario_count(
        name_to_scenario
    )
    print(
        "Number of test cases per necessary tool name:",
        json.dumps(
            {
                str(k): v
                for k, v in necessary_tool_counter.most_common(
                    len(necessary_tool_counter)
                )
            },
            indent=4,
            ensure_ascii=False,
        ),
    )
    # Shuffle scenarios for load balancing
    name_and_scenario_list = list(name_to_scenario.items())
    random.shuffle(name_and_scenario_list)
    num_scenarios = len(name_and_scenario_list)
    if processes > 1 and num_scenarios > 1:
        # As described in e.g. https://stackoverflow.com/a/66113051 the default option
        # for starting a process is to fork the parent process, which by design can
        # cause dead locks. We have seen such dead locks when running the tool sandbox
        # on Linux, but not on MacOS. Switching to the `spawn` instead of `fork` method
        # for starting a new process eliminated the deadlock.
        mpctx = multiprocessing.get_context("spawn")
        with mpctx.Pool(min(processes, num_scenarios)) as pool:
            result_summary = pool.map(
                partial(
                    run_scenario,
                    agent_type=agent_type,
                    user_type=user_type,
                    args=args,
                    output_directory=output_directory,
                ),
                name_and_scenario_list,
            )
    else:
        result_summary = []
        tqdm_iterator = tqdm(name_and_scenario_list, desc="Scenarios")
        for name_and_scenario in tqdm_iterator:
            result_summary.append(
                run_scenario(
                    name_and_scenario,
                    agent_type=agent_type,
                    user_type=user_type,
                    args=args,
                    output_directory=output_directory,
                )
            )

    # Score the LLM judge now that every worker has finished. Each scenario passed
    # back a prepared eval task instead of calling the judge inline, so the network
    # work happens here with no per-scenario alarm armed.
    score_llm_evaluations(result_summary, processes=processes)

    # Load existing results from trajectories (for resume scenarios)
    existing_results = load_results_from_trajectories(
        output_directory, name_to_scenario=name_to_scenario
    )

    # Filter out duplicates - prefer newly run results over existing
    newly_run_names = {res["name"] for res in result_summary}
    filtered_existing = [
        r for r in existing_results if r["name"] not in newly_run_names
    ]

    # Merge: existing + new results for complete summary
    complete_result_summary = filtered_existing + result_summary

    # Run-end infra-failure summary: scenarios that failed to play out are recorded
    # with exception_type set (API error / empty completion / 180s timeout). Surface
    # the rate + a breakdown by exception type so the operator isn't blind to silent drops.
    failed = [r for r in result_summary if r.get("exception_type")]
    if failed:
        by_type = Counter(r["exception_type"] for r in failed)
        breakdown = ", ".join(f"{t}: {c}" for t, c in by_type.most_common())
        logger.warning(
            "%d/%d scenarios failed to run (infra/API errors) — {%s}",
            len(failed),
            len(result_summary),
            breakdown,
        )
        for r in failed[:20]:
            logger.warning("  failed scenario: %s (%s)", r["name"], r["exception_type"])
        if len(failed) > 20:
            logger.warning(
                "  … and %d more (see per-scenario error logs above)", len(failed) - 20
            )
    else:
        logger.info(
            "All %d scenarios ran without infra/API errors.", len(result_summary)
        )

    # Log resume info if applicable
    if filtered_existing:
        print(f"\n✓ Loaded {len(filtered_existing)} existing trajectory results")
        print(f"✓ Ran {len(result_summary)} new scenarios")
        print(
            f"✓ Total scenarios in result_summary.json: {len(complete_result_summary)}\n"
        )

    # Aggregate results by category using complete summary
    category_summary = get_category_summary(complete_result_summary)
    write_result_summary(
        result_summary=complete_result_summary,
        category_summary=category_summary,
        output_directory=output_directory,
    )
    return len(failed)


def main() -> None:
    random.seed(42)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--agent",
        help="Agent type.",
        default="GPT_4_o_2024_11_20",
        choices=[str(t) for t in AGENT_TYPE_TO_FACTORY.keys()],
    )
    parser.add_argument(
        "--user",
        help="User type.",
        default=str(DEFAULT_USER_TYPE),
        choices=[str(t) for t in USER_TYPE_TO_FACTORY.keys()],
    )
    parser.add_argument(
        "--preferred_tool_backend",
        help="Preferred tool backend to use.",
        default="DEFAULT",
        choices=[str(t) for t in ToolBackend],
    )
    scenario_selection_group = parser.add_mutually_exclusive_group()
    scenario_selection_group.add_argument(
        "-t",
        "--test_mode",
        action="store_true",
        help="Only run a few scenarios rather than the full suite.",
    )
    scenario_selection_group.add_argument(
        "-s",
        "--scenarios",
        nargs="*",
        help="Name of scenarios to run.",
        required=False,
    )
    scenario_selection_group.add_argument(
        "--tags",
        nargs="*",
        help="scenarios with certain tags to run.",
        required=False,
    )
    parser.add_argument(
        "-llm_eval",
        "--llm_evaluation",
        action="store_true",
        help="Whether to use LLM evaluation for scenarios.",
    )
    parser.add_argument(
        "-p",
        "--parallel",
        type=int,
        default=16,
        help="Max number of processes for running scenarios in parallel.",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=Path,
        default=Path("data"),
        help="Output base directory.",
    )
    args = parser.parse_args()
    # The parser for `--test_mode` and `--scenarios` are in a mutually exclusive group
    # so we can safely ignore the value of `args.scenarios` when `args.test_mode` is
    # true.
    scenario_names = TEST_SCENARIO_NAMES if args.test_mode else args.scenarios
    scenario_tags = args.tags if args.tags else None

    # Technically, strings can automatically be converted to the `RoleImplType` since it
    # is a `StrEnum`, but we are being explicit here.
    agent_type = RoleImplType(args.agent)
    user_type = RoleImplType(args.user)

    # Automatically determine whether to add user simulator few-shot examples
    # Only add them when the user type is an LLM (not CLI)
    add_user_simulator_few_shot_examples = user_type != RoleImplType.Cli

    name_to_scenario = resolve_scenarios(
        desired_scenario_names=scenario_names,
        scenario_tags=scenario_tags,
        preferred_tool_backend=args.preferred_tool_backend,
        llm_evaluation=args.llm_evaluation,
        add_user_simulator_few_shot_examples=add_user_simulator_few_shot_examples,
    )
    num_failed = run_sandbox(
        args=args,
        agent_type=agent_type,
        user_type=user_type,
        name_to_scenario=name_to_scenario,
        processes=args.parallel,
        output_base_dir=args.output_dir,
    )
    # Non-zero exit so scripts and CI notice a run where scenarios failed to play out.
    if num_failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
