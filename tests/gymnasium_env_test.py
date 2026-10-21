# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Tests for the `gymnasium.Env` adapter.

Skipped entirely without the `gymnasium` extra. All offline, no network and no
model: everything here drives ASTRA with hard-coded actions against a narrow,
by-name scenario resolution (a few seconds), never the full catalog.
"""

from __future__ import annotations

import copy
from typing import Any

import polars as pl
import pytest

pytest.importorskip("gymnasium", reason="requires the gymnasium extra")

# Deliberately below the importorskip: importing the adapter pulls in `gymnasium`,
# so it must not run when the extra is absent.
from astra_tool_sandbox.cli.utils import resolve_scenarios  # noqa: E402
from astra_tool_sandbox.common.evaluation import (  # noqa: E402
    Evaluation,
    Milestone,
    MilestoneMatcher,
    SnapshotConstraint,
    snapshot_similarity,
)
from astra_tool_sandbox.common.execution_context import (  # noqa: E402
    DatabaseNamespace,
    ExecutionContext,
    RoleType,
    get_current_context,
)
from astra_tool_sandbox.common.scenario import Scenario  # noqa: E402
from astra_tool_sandbox.common.tool_discovery import ToolBackend  # noqa: E402
from astra_tool_sandbox.gymnasium_env import (  # noqa: E402
    AstraGymnasiumEnv,
    _is_nl_reply_constraint,
    drop_nl_reply_milestones,
)

SCENARIO_NAME = "get_contact_count_DAWEI_SHEN"
SECOND_SCENARIO_NAME = "get_add_calendar_DAWEI_SHEN"
CODE_ACTION = "```python\nresult = get_all_contacts()\nprint(len(result))\n```"
END_ACTION = "You have 17 contacts in total. end_conversation"


@pytest.fixture(scope="module")
def dawei_shen_scenario() -> Scenario:
    # Narrow resolution by name -- resolving the full 2,428-scenario catalog takes
    # ~91.6s, versus a few seconds for one named scenario.
    scenarios = resolve_scenarios(
        desired_scenario_names=[SCENARIO_NAME],
        scenario_tags=None,
        preferred_tool_backend=ToolBackend.DEFAULT,
    )
    return scenarios[SCENARIO_NAME]


def _play_scripted_episode(
    env: AstraGymnasiumEnv,
) -> tuple[str, float, bool, bool, dict[str, Any]]:
    """Play the deterministic, hard-coded-correct action sequence for
    `get_contact_count_DAWEI_SHEN`: one tool call, then a natural-language reply
    that ends the conversation."""
    env.reset()
    _, _, terminated, truncated, _ = env.step(CODE_ACTION)
    assert not terminated and not truncated
    result = env.step(END_ACTION)
    assert result[2] or result[3]
    return result


# --- 1. reset() / observations --------------------------------------------------


def test_reset_returns_an_observation() -> None:
    env = AstraGymnasiumEnv(desired_scenario_names=[SCENARIO_NAME])
    observation, _info = env.reset()
    assert isinstance(observation, str)
    assert observation


def test_reset_info_carries_the_scenario_system_messages() -> None:
    """A harness cannot solve time-sensitive scenarios without these.

    ASTRA's sandbox clock is the real clock (`tools/utilities.py` returns
    `datetime.datetime.now()`) while scenarios are set in the past, so the
    scenario's date exists only in its SYSTEM -> AGENT messages. ASTRA's own
    agent role reads them from the execution context; a harness has to be handed
    them explicitly.
    """
    env = AstraGymnasiumEnv(desired_scenario_names=[SCENARIO_NAME])
    _, info = env.reset()
    messages = info["system_messages"]
    assert messages, "expected the scenario's SYSTEM -> AGENT messages"
    assert messages == env.system_messages
    # One of them states the scenario's clock, which is what makes "today" mean
    # the scenario's date rather than the real one.
    assert any("Today is" in m for m in messages)


def test_step_before_reset_raises() -> None:
    env = AstraGymnasiumEnv(desired_scenario_names=[SCENARIO_NAME])
    with pytest.raises(RuntimeError, match="reset"):
        env.step(CODE_ACTION)


def test_mutually_exclusive_scenario_filters_raise() -> None:
    with pytest.raises(ValueError, match="scenario_tags"):
        AstraGymnasiumEnv(
            scenario_tags=["test"], desired_scenario_names=[SCENARIO_NAME]
        )


# --- 2. Scenario selection ------------------------------------------------------


def test_scenario_rotation_advances_across_episodes() -> None:
    env = AstraGymnasiumEnv(
        desired_scenario_names=[SCENARIO_NAME, SECOND_SCENARIO_NAME]
    )

    env.reset()
    first_name = env.current_scenario_name
    env.reset()
    second_name = env.current_scenario_name
    env.reset()
    third_name = env.current_scenario_name

    assert first_name != second_name
    assert first_name == third_name  # wraps back around after two scenarios
    assert {first_name, second_name} == {SCENARIO_NAME, SECOND_SCENARIO_NAME}


def test_reset_options_can_name_the_scenario_to_play() -> None:
    """A harness often wants a specific scenario without building a new env."""
    env = AstraGymnasiumEnv(
        desired_scenario_names=[SCENARIO_NAME, SECOND_SCENARIO_NAME]
    )
    env.reset(options={"scenario_name": SECOND_SCENARIO_NAME})
    assert env.current_scenario_name == SECOND_SCENARIO_NAME

    env.reset(options={"scenario_name": SCENARIO_NAME})
    assert env.current_scenario_name == SCENARIO_NAME


def test_named_reset_does_not_disturb_the_rotation_cursor() -> None:
    """Interleaving a targeted episode must not change the order the rotation
    resumes in, or a training loop's scenario coverage silently shifts."""
    env = AstraGymnasiumEnv(
        desired_scenario_names=[SCENARIO_NAME, SECOND_SCENARIO_NAME]
    )
    env.reset()
    first = env.current_scenario_name

    # A named reset in between.
    env.reset(options={"scenario_name": first})
    assert env.current_scenario_name == first

    env.reset()
    assert (
        env.current_scenario_name != first
    ), "rotation should have advanced past the first scenario, not restarted"


def test_unknown_scenario_name_in_options_raises() -> None:
    env = AstraGymnasiumEnv(desired_scenario_names=[SCENARIO_NAME])
    with pytest.raises(ValueError, match="not in this env's resolved"):
        env.reset(options={"scenario_name": "no_such_scenario"})


def test_scenario_names_lists_the_resolved_catalog() -> None:
    env = AstraGymnasiumEnv(
        desired_scenario_names=[SCENARIO_NAME, SECOND_SCENARIO_NAME]
    )
    assert env.scenario_names == sorted([SCENARIO_NAME, SECOND_SCENARIO_NAME])


# --- 3. Scripted-episode determinism -------------------------------------------


def test_scripted_action_sequence_produces_a_terminal_reward() -> None:
    env = AstraGymnasiumEnv(desired_scenario_names=[SCENARIO_NAME])
    env.reset()

    _, reward, terminated, truncated, _ = env.step(CODE_ACTION)
    assert not terminated
    assert not truncated
    assert reward == 0.0

    _, reward, terminated, truncated, info = env.step(END_ACTION)
    assert terminated
    assert not truncated
    assert reward == 1.0
    assert info["similarity"] == 1.0


def test_scripted_episode_reward_matches_direct_evaluate(
    dawei_shen_scenario: Scenario,
) -> None:
    env = AstraGymnasiumEnv(desired_scenario_names=[SCENARIO_NAME])
    _, reward, _, _, info = _play_scripted_episode(env)

    # A direct call to `scenario.evaluation.evaluate()` on the resulting context
    # needs no model and is the central correctness check: the env must not
    # compute a different score than ASTRA's own grader would.
    expected = dawei_shen_scenario.evaluation.evaluate(
        execution_context=get_current_context(),
        max_turn_count=dawei_shen_scenario.max_messages,
    )
    assert info["similarity"] == expected.similarity
    assert reward == expected.similarity


def test_tool_specs_and_openai_tools_available_after_reset() -> None:
    env = AstraGymnasiumEnv(desired_scenario_names=[SCENARIO_NAME])
    env.reset()

    specs = env.tool_specs()
    assert "get_all_contacts" in specs
    assert specs["get_all_contacts"].name == "get_all_contacts"

    openai_tools = env.openai_tools()
    assert any(tool["function"]["name"] == "get_all_contacts" for tool in openai_tools)


# --- 4. Guardrail ---------------------------------------------------------------


def test_guardrail_ends_episode_after_three_nl_replies() -> None:
    env = AstraGymnasiumEnv(desired_scenario_names=[SCENARIO_NAME])
    env.reset()

    _, _, terminated, truncated, _ = env.step("I'm not sure what you mean.")
    assert not (terminated or truncated)
    _, _, terminated, truncated, _ = env.step("Could you clarify your request?")
    assert not (terminated or truncated)
    _, _, terminated, truncated, _ = env.step("I still don't understand.")
    assert terminated or truncated


# --- 5. Milestone dropping ------------------------------------------------------


def _milestone(nl_reply: bool, reference_milestone_node_index: int | None) -> Milestone:
    if nl_reply:
        target_dataframe = pl.DataFrame(
            {"recipient": [RoleType.USER.value], "content": ["hello"]}
        )
        namespace = DatabaseNamespace.SANDBOX
    else:
        target_dataframe = pl.DataFrame({"person_id": ["p1"]})
        namespace = DatabaseNamespace.CONTACT
    constraint = SnapshotConstraint(
        database_namespace=namespace,
        snapshot_constraint=snapshot_similarity,
        target_dataframe=target_dataframe,
        reference_milestone_node_index=reference_milestone_node_index,
    )
    return Milestone(snapshot_constraints=[constraint])


def test_drop_nl_reply_milestones_reindexes_references_and_dag() -> None:
    # 0: unrelated tool milestone (no reference).
    # 1: AGENT -> USER nl-reply milestone -- gets dropped. References 0.
    # 2: tool milestone referencing the initial snapshot (-1), independent of 1.
    # 3: tool milestone referencing 2, which shifts to index 1 after the drop.
    milestones = [
        _milestone(False, None),
        _milestone(True, 0),
        _milestone(False, -1),
        _milestone(False, 2),
    ]
    matcher = MilestoneMatcher(milestones=milestones)
    evaluation = Evaluation(milestone_matcher=matcher)

    drop_nl_reply_milestones(evaluation)

    assert len(matcher.milestones) == 3
    assert sorted(matcher.milestone_dag.nodes()) == [0, 1, 2]
    # Edge (0, 1) -> (1, 2) in the old numbering was bridged across the removed
    # node 1 into (0, 1) -> (1, 2) in the new numbering.
    assert sorted(matcher.milestone_dag.edges()) == [(0, 1), (1, 2)]

    # The milestone that referenced the initial snapshot (-1) is untouched: -1 is
    # not a milestone index, so it must not be reindexed.
    unreindexed_ref = matcher.milestones[1].snapshot_constraints[0]
    assert unreindexed_ref.reference_milestone_node_index == -1

    # The milestone that referenced the (kept, renumbered) old milestone 2 now
    # points at its new index, 1.
    reindexed_ref = matcher.milestones[2].snapshot_constraints[0]
    assert reindexed_ref.reference_milestone_node_index == 1

    # No surviving constraint should reference a milestone index that no longer
    # exists (the removed nl-reply milestone's old index, 1).
    for milestone in matcher.milestones:
        for constraint in milestone.snapshot_constraints:
            ref = constraint.reference_milestone_node_index
            if ref is not None and ref >= 0:
                assert ref < len(matcher.milestones)

    # Grading still runs (does not raise) on the mutated matcher.
    result = evaluation.evaluate(
        execution_context=ExecutionContext(), max_turn_count=30
    )
    assert result.milestone_similarity is not None


def test_exclude_nl_reply_milestones_option_still_grades() -> None:
    # Dropping the AGENT -> USER milestone of `get_contact_count_DAWEI_SHEN`
    # leaves its two tool milestones, which the scripted episode satisfies; what
    # matters here is that opting in does not break stepping or grading end to end.
    env = AstraGymnasiumEnv(
        desired_scenario_names=[SCENARIO_NAME], exclude_nl_reply_milestones=True
    )
    _, _, _, _, info = _play_scripted_episode(env)
    assert info["similarity"] == 1.0


def test_drop_nl_reply_milestones_on_real_scenarios() -> None:
    """Exercise milestone dropping against the real catalog, not a synthetic stub.

    Just over half the catalog (1,224 of 2,428 scenarios) carries an AGENT->USER
    milestone, so the reindexing path this covers is well travelled -- including
    one scenario inside the cheap `test` tag. Each surviving
    `reference_milestone_node_index` must still point at a live milestone, or
    grading reads the wrong node.
    """
    name = "get_unread_emails_michelle_DAWEI_SHEN"
    catalog = resolve_scenarios(
        desired_scenario_names=[name],
        scenario_tags=None,
        preferred_tool_backend=ToolBackend.DEFAULT,
    )
    scenario = copy.deepcopy(catalog[name])
    matcher = scenario.evaluation.milestone_matcher

    before = len(matcher.milestones)
    assert any(
        any(_is_nl_reply_constraint(c) for c in m.snapshot_constraints)
        for m in matcher.milestones
    ), "fixture scenario no longer has an AGENT->USER milestone"

    drop_nl_reply_milestones(scenario.evaluation)

    after = len(matcher.milestones)
    assert after < before, "expected at least one milestone to be dropped"

    for milestone in matcher.milestones:
        for constraint in milestone.snapshot_constraints:
            ref = constraint.reference_milestone_node_index
            if ref is not None and ref >= 0:
                assert ref < after


# --- 6. Reward modes ------------------------------------------------------------


def test_reward_mode_none_returns_raw_similarity() -> None:
    env = AstraGymnasiumEnv(
        desired_scenario_names=[SCENARIO_NAME], similarity_threshold=None
    )
    _, reward, _, _, info = _play_scripted_episode(env)
    assert info["similarity"] == 1.0
    assert reward == 1.0


def test_reward_mode_threshold_below_similarity_gives_success_reward() -> None:
    env = AstraGymnasiumEnv(
        desired_scenario_names=[SCENARIO_NAME],
        similarity_threshold=0.99,
        success_reward=2.5,
    )
    _, reward, _, _, info = _play_scripted_episode(env)
    assert info["similarity"] == 1.0
    assert reward == 2.5


def test_reward_mode_threshold_above_similarity_gives_zero() -> None:
    # Nothing can be >= 1.01, so this is proof the option reached the grading
    # path rather than being silently dropped.
    env = AstraGymnasiumEnv(
        desired_scenario_names=[SCENARIO_NAME], similarity_threshold=1.01
    )
    _, reward, _, _, info = _play_scripted_episode(env)
    assert info["similarity"] == 1.0
    assert reward == 0.0


# --- 7. Grader robustness -------------------------------------------------------


class _SimulatedRustPanic(BaseException):
    """Stand-in for polars' `pyo3_runtime.PanicException`: a Rust panic surfaced
    at the FFI boundary, which is not an `Exception`."""


def test_grader_basexception_is_caught_not_propagated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _raise(self: Evaluation, **kwargs: Any) -> None:
        raise _SimulatedRustPanic("simulated FFI panic")

    monkeypatch.setattr(Evaluation, "evaluate", _raise)

    env = AstraGymnasiumEnv(desired_scenario_names=[SCENARIO_NAME])
    _, reward, terminated, truncated, info = _play_scripted_episode(env)

    assert terminated or truncated
    assert reward == 0.0
    assert info["eval_error"] is True
    assert info["similarity"] is None
