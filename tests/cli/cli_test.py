# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
import sys
from pathlib import Path
from typing import Any, Optional, cast

import pytest

import astra_tool_sandbox.cli as cli
from astra_tool_sandbox.cli.utils import get_category_summary, resolve_scenarios
from astra_tool_sandbox.common.tool_discovery import ToolBackend
from astra_tool_sandbox.scenarios.astra_v1 import named_scenarios


def test_getting_all_scenarios() -> None:
    name_to_scenario = resolve_scenarios(
        desired_scenario_names=None,
        scenario_tags=None,
        preferred_tool_backend=ToolBackend.DEFAULT,
    )
    assert set(
        named_scenarios(preferred_tool_backend=ToolBackend.DEFAULT).keys()
    ) == set(name_to_scenario.keys())


def test_getting_scenarios_with_empty_filters() -> None:
    # Per the documented contract, empty filter lists behave like ``None``: all
    # scenarios are returned. This mirrors the CLI, which treats ``--scenarios`` /
    # ``--tags`` supplied with no values as "no filter".
    name_to_scenario = resolve_scenarios(
        desired_scenario_names=[],
        scenario_tags=[],
        preferred_tool_backend=ToolBackend.DEFAULT,
    )
    assert set(
        named_scenarios(preferred_tool_backend=ToolBackend.DEFAULT).keys()
    ) == set(name_to_scenario.keys())


def test_getting_desired_scenarios() -> None:
    # Pick the first N names from all available scenarios to ensure that this test is
    # using existing scenario names.
    desired_scenario_names = list(
        named_scenarios(preferred_tool_backend=ToolBackend.DEFAULT).keys()
    )[:5]
    name_to_scenario = resolve_scenarios(
        desired_scenario_names=desired_scenario_names,
        scenario_tags=None,
        preferred_tool_backend=ToolBackend.DEFAULT,
    )
    assert set(desired_scenario_names) == set(name_to_scenario.keys())


def test_getting_non_existent_scenarios() -> None:
    all_scenario_names = set(
        named_scenarios(preferred_tool_backend=ToolBackend.DEFAULT).keys()
    )
    non_existent_scenario = "this scenario does not exist"
    assert non_existent_scenario not in all_scenario_names

    with pytest.raises(KeyError, match="desired scenarios do not exist"):
        resolve_scenarios(
            desired_scenario_names=[non_existent_scenario],
            scenario_tags=None,
            preferred_tool_backend=ToolBackend.DEFAULT,
        )


def test_get_category_summary_excludes_none_retrieval_efficiency() -> None:
    def _r(eff: Optional[float], get_all: int) -> dict[str, Any]:
        return {
            "categories": ["catA"],
            "similarity": 1.0,
            "turn_count": 3,
            "retrieval_get_all_count": get_all,
            "retrieval_failed_search_count": 0,
            "retrieval_efficiency": eff,
        }

    summ = get_category_summary([_r(1.0, 0), _r(0.0, 1), _r(None, 0)])
    # The None (no-retrieval, N/A) scenario is excluded from the efficiency list...
    assert summ["catA"]["retrieval_efficiency"] == [1.0, 0.0]
    assert summ["ALL_CATEGORIES"]["retrieval_efficiency"] == [1.0, 0.0]
    # ...but counts still include every scenario.
    assert summ["catA"]["retrieval_get_all_count"] == [0, 1, 0]


def test_get_category_summary_excludes_none_similarity() -> None:
    """A scenario that stopped early records similarity=None and must be excluded.

    Appending the None instead would survive get_category_summary and then blow up
    the `sum(v) / len(v)` in write_result_summary at the very end of the run,
    destroying the summary for every scenario.
    """

    def _r(similarity: Optional[float]) -> dict[str, Any]:
        return {
            "categories": ["catA"],
            "similarity": similarity,
            "turn_count": 3,
            "retrieval_get_all_count": 0,
            "retrieval_failed_search_count": 0,
            "retrieval_efficiency": 1.0,
        }

    summ = get_category_summary([_r(1.0), _r(None), _r(0.5)])

    assert summ["catA"]["similarity"] == [1.0, 0.5]
    assert summ["ALL_CATEGORIES"]["similarity"] == [1.0, 0.5]
    # turn_count is never None (the crash path falls back to max_messages).
    assert summ["catA"]["turn_count"] == [3, 3, 3]
    # The reduction write_result_summary performs must not raise.
    for values in summ["ALL_CATEGORIES"].values():
        assert sum(values) / len(values) is not None


# --- Judge-pass request pacing ------------------------------------------------------
#
# Model APIs enforce a per-key request-rate quota. Exceeding it does NOT fail the run:
# the scenario is left unjudged and only `coverage_llm_evaluation_*` drops, so the burst
# has to be prevented rather than detected. The judge pass is the concentrated burst --
# one call per scenario, spread over `--parallel` threads with no other work between
# them -- which is why it is paced and the scenario pass is not.


def test_pacer_spaces_requests_and_never_bursts() -> None:
    """A token bucket would allow an opening burst equal to its capacity, which is exactly
    what trips a sliding-window quota. A minimum interval cannot."""
    import time
    from concurrent.futures import ThreadPoolExecutor

    from astra_tool_sandbox.cli import _RequestPacer

    pacer = _RequestPacer(1200)  # 20/s -> 50ms apart
    stamps: list[float] = []

    def call(_: int) -> None:
        pacer.wait()
        stamps.append(time.monotonic())

    with ThreadPoolExecutor(max_workers=16) as executor:
        list(executor.map(call, range(20)))

    stamps.sort()
    gaps = [b - a for a, b in zip(stamps, stamps[1:])]
    # Allow generous slack for timer resolution; the point is that gaps EXIST.
    assert min(gaps) > 0.02
    # 16 threads must not all fire at once.
    assert stamps[-1] - stamps[0] > 0.5


def test_pacer_disabled_is_free() -> None:
    """A pacing rate of 0 must be a true no-op, not a tiny sleep."""
    import time

    from astra_tool_sandbox.cli import _RequestPacer

    pacer = _RequestPacer(0)
    started = time.monotonic()
    for _ in range(500):
        pacer.wait()
    assert time.monotonic() - started < 0.1


def test_pacer_does_not_bank_credit_while_idle() -> None:
    """After a quiet period the next call may go immediately, but the one after it must
    still be spaced — otherwise an idle gap funds a burst."""
    import time

    from astra_tool_sandbox.cli import _RequestPacer

    pacer = _RequestPacer(600)  # 100ms apart
    pacer.wait()
    time.sleep(0.3)  # idle far longer than one interval
    started = time.monotonic()
    pacer.wait()  # allowed immediately
    pacer.wait()  # must be spaced
    assert time.monotonic() - started > 0.05


def test_judge_pass_is_paced_by_default() -> None:
    """The default must stay below the rate limits public model APIs hand out, with
    headroom: the quota is per-key, so a same-key user simulator shares the bucket."""
    from astra_tool_sandbox.cli import JUDGE_MAX_REQUESTS_PER_MINUTE

    assert 0 < JUDGE_MAX_REQUESTS_PER_MINUTE < 80


def test_resumed_result_nullifies_completion_score_on_a_minefield(
    tmp_path: Path,
) -> None:
    """The resume path reads minefield_similarity off the artifact, so it must veto too.

    Otherwise a resumed run and a fresh run of the same trajectory would disagree
    about the same scenario.
    """
    import json
    from types import SimpleNamespace

    import polars as pl

    from astra_tool_sandbox.cli import load_results_from_trajectories
    from astra_tool_sandbox.common.evaluation import (
        Milestone,
        SnapshotConstraint,
        snapshot_similarity,
    )
    from astra_tool_sandbox.common.execution_context import DatabaseNamespace, RoleType
    from astra_tool_sandbox.common.scenario import Scenario

    answer_milestone = Milestone(
        snapshot_constraints=[
            SnapshotConstraint(
                database_namespace=DatabaseNamespace.SANDBOX,
                snapshot_constraint=snapshot_similarity,
                target_dataframe=pl.DataFrame(
                    {
                        "sender": RoleType.AGENT,
                        "recipient": RoleType.USER,
                        "content": "done",
                    }
                ),
            )
        ]
    )
    scenario = SimpleNamespace(
        evaluation=SimpleNamespace(
            milestone_matcher=SimpleNamespace(milestones=[answer_milestone])
        )
    )

    def _load(minefield_similarity: float) -> Optional[float]:
        scenario_dir = tmp_path / str(minefield_similarity) / "trajectories" / "s"
        scenario_dir.mkdir(parents=True)
        (scenario_dir / "execution_context.json").write_text(
            json.dumps(
                {
                    "evaluation_result": {
                        "milestone_mapping": {"0": [4, 1.0]},
                        "milestone_similarity": 1.0,
                        "minefield_similarity": minefield_similarity,
                        "similarity": 0.0 if minefield_similarity else 1.0,
                        "turn_count": 4,
                    }
                }
            )
        )
        results = load_results_from_trajectories(
            tmp_path / str(minefield_similarity),
            cast("dict[str, Scenario]", {"s": scenario}),
        )
        assert len(results) == 1
        score: Optional[float] = results[0]["milestone_completion_score"]
        return score

    assert _load(0) == 1.0
    assert _load(1.0) == 0.0


@pytest.mark.parametrize("num_failed, expected_exit", [(0, None), (2, 1)])
def test_main_exit_code_reflects_failed_scenarios(
    monkeypatch: pytest.MonkeyPatch, num_failed: int, expected_exit: Optional[int]
) -> None:
    monkeypatch.setattr(sys, "argv", ["astra_tool_sandbox", "--user", "Cli"])
    monkeypatch.setattr(cli, "resolve_scenarios", lambda **_: {})
    monkeypatch.setattr(cli, "run_sandbox", lambda **_: num_failed)
    if expected_exit is None:
        cli.main()
    else:
        with pytest.raises(SystemExit) as exc_info:
            cli.main()
        assert exc_info.value.code == expected_exit
