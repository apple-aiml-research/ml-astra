# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""ASTRA scenarios as a `gymnasium.Env`.

The *caller* owns the agent loop. `AstraGymnasiumEnv` gives it `reset()` /
`step()` primitives and does the work of driving one ASTRA scenario turn by
turn, so a harness that already has its own LLM sampling, tool-calling
scaffolding and retries does not have to reach into ASTRA's internals.

`Scenario.play()` (see `common/scenario.py`) is a role-dispatch loop that reads
the last message's recipient and calls `roles[recipient].respond()`. Injecting
the harness's action as an AGENT message -- and never installing an LLM agent
role -- makes ASTRA pluggable at exactly that level, which is what this module
does.

`gymnasium` is imported by this module only, never at `astra_tool_sandbox`
package import time, so a caller that never touches the adapter is not forced to
install the extra:

```
pip install 'astra_tool_sandbox[gymnasium]'
```

Two things a caller must know:

* **`step()` is not bounded by a timeout.** ASTRA executes model-generated
  Python in-process via `code.InteractiveConsole`, so a pathological snippet can
  hang. No bound lives here -- a harness driving untrusted model-generated code
  must supply its own, whether that is `SIGALRM` (main thread only) or running
  the whole trajectory in a subprocess it can `kill()`.
* **ASTRA's execution context is a process-global** (see
  `common/execution_context.py`). `reset()` and `step()` install and mutate it
  via `set_current_context()` / `get_current_context()`, so only one env may be
  stepping per process -- the same constraint the rest of ASTRA already has.
  Vectorise across processes (e.g. `gymnasium.vector.AsyncVectorEnv`), never
  within one.
"""

from __future__ import annotations

import copy
import re
import string
from dataclasses import dataclass
from typing import Any

import gymnasium as gym
import networkx
from gymnasium import spaces
from openai.types.chat import ChatCompletionToolParam

from astra_tool_sandbox.cli.utils import resolve_scenarios
from astra_tool_sandbox.common.evaluation import Evaluation, SnapshotConstraint
from astra_tool_sandbox.common.execution_context import (
    DatabaseNamespace,
    RoleType,
    get_current_context,
    set_current_context,
)
from astra_tool_sandbox.common.message_conversion import Message
from astra_tool_sandbox.common.scenario import Scenario
from astra_tool_sandbox.common.tool_conversion import (
    convert_python_function_to_openai_function,
    convert_to_openai_tools,
)
from astra_tool_sandbox.common.tool_discovery import ToolBackend
from astra_tool_sandbox.roles.base_role import BaseRole
from astra_tool_sandbox.roles.execution_environment import ExecutionEnvironment

_CODE_BLOCK_RE = re.compile(r"```python\n(.*?)(?:```|$)", re.DOTALL)

# gymnasium's `spaces.Text` default charset is alphanumeric-only and its
# default `min_length` is 1 (no empty strings) -- neither holds for ASTRA text,
# which includes code blocks, punctuation, whitespace, and the empty
# observation `_get_observation` returns after a non-terminal natural-language
# step.
#
# `string.printable` is still NARROWER than real ASTRA content: scenario data
# contains accented Latin, em-dashes, curly quotes and emoji (verified in saved
# trajectories -- e.g. e-acute, u-umlaut, "—", "’" and three emoji appear in
# DAWEI_SHEN contexts). `observation_space.contains(obs)` will therefore return
# False for legitimate observations, and `gymnasium.utils.env_checker` will
# complain.
#
# Treat the spaces as advisory shape declarations, not validators, and do not
# gate rollouts on `contains()`. Enumerating a Unicode-wide charset would mean a
# frozenset of tens of thousands of entries for no practical gain, and the
# alternative -- silently truncating or replacing characters to fit -- would
# corrupt the observations the agent is graded on.
_TEXT_CHARSET = frozenset(string.printable)
_DEFAULT_MAX_TEXT_LENGTH = 50_000


def extract_code(text: str) -> tuple[str, str]:
    """Extract the first ```python code block from agent text.

    ASTRA has no code-block-extraction utility of its own, and a fenced `python`
    block is exactly the action convention `AstraGymnasiumEnv.step()` expects.

    Args:
        text: The agent's raw action text.

    Returns:
        A `(code, prefix)` tuple. `code` is the contents of the first ```python
        block with comment-only lines stripped, or `""` if no block is found.
        `prefix` is `text` up to and including the end of that block (or all of
        `text`, when `code` is empty) -- callers that want to render what the
        agent "said" alongside the code use this.
    """
    match = _CODE_BLOCK_RE.search(text)
    if not match:
        return "", text

    code = match.group(1)
    code = "\n".join(
        line for line in code.splitlines() if not line.lstrip().startswith("#")
    )
    prefix = text[: match.end()]  # content up to and including the first match
    return code, prefix


def _is_nl_reply_constraint(constraint: SnapshotConstraint) -> bool:
    """True if `constraint` grades an AGENT -> USER natural-language reply."""
    df = constraint.target_dataframe
    if df is None or "recipient" not in df.columns:
        return False
    return set(df["recipient"].to_list()) == {RoleType.USER.value}


def drop_nl_reply_milestones(evaluation: Evaluation) -> None:
    """Remove milestones that grade the agent's natural-language replies to the
    user, so the episode is scored purely on tool-call / database effects.

    Intended for harnesses that install no LLM user simulator: with nothing to
    receive the agent's reply, grading it is not meaningful. Exposed as
    `AstraGymnasiumEnv`'s `exclude_nl_reply_milestones` option.

    A milestone is dropped when any of its snapshot constraints checks an
    AGENT -> USER message. Edges are bridged across the removed nodes so the
    ordering of the remaining milestones is preserved, and constraint
    `reference_milestone_node_index` values are reindexed to match.

    Mutates `evaluation.milestone_matcher` in place.
    """
    mm = evaluation.milestone_matcher
    milestones = mm.milestones
    removed = {
        i
        for i, m in enumerate(milestones)
        if any(_is_nl_reply_constraint(c) for c in m.snapshot_constraints)
    }
    if not removed:
        return

    kept = [i for i in range(len(milestones)) if i not in removed]
    old_to_new = {old: new for new, old in enumerate(kept)}

    # Bridge each kept node to the nearest kept descendants reachable through the
    # removed nodes, so ordering constraints survive removal.
    dag = mm.milestone_dag
    new_edges: set[tuple[int, int]] = set()
    for u in kept:
        stack = list(dag.successors(u))
        seen: set[int] = set()
        while stack:
            v = stack.pop()
            if v in seen:
                continue
            seen.add(v)
            if v in old_to_new:
                new_edges.add((old_to_new[u], old_to_new[v]))
            else:
                stack.extend(dag.successors(v))

    new_milestones = []
    for old in kept:
        m = milestones[old]
        constraints = []
        for c in m.snapshot_constraints:
            ref = c.reference_milestone_node_index
            if ref is not None and ref >= 0:
                if ref not in old_to_new:
                    # References a removed milestone; drop the constraint.
                    continue
                c.reference_milestone_node_index = old_to_new[ref]
            constraints.append(c)
        m.snapshot_constraints = constraints
        new_milestones.append(m)

    # Mutate the matcher in place to avoid re-running its post-init (which would
    # re-add guardrail constraints already present on the milestones).
    mm.milestones = new_milestones
    mm.edge_list = sorted(new_edges)
    mm.milestone_dag = networkx.DiGraph(mm.edge_list)
    mm.milestone_dag.add_nodes_from(range(len(new_milestones)))
    # Rebuild the dependents map, which is keyed by milestone index and is now
    # stale. It is not merely a pruning table: `_dfs` reads it to compute a
    # `lookahead_bonus` (common/evaluation.py:2473) that steers which
    # milestone-to-snapshot mapping the search settles on, so a map keyed by
    # pre-drop indices could change the resulting similarity rather than just
    # the time taken to find it. We could not demonstrate a score difference, but
    # the call is free and removes the question. Just over half the catalog
    # (1,224 of 2,428 scenarios) has an AGENT->USER milestone, so this path is
    # well travelled.
    mm._build_dependents_map()


@dataclass(frozen=True)
class ToolSpec:
    """A tool's OpenAI function-calling signature, name/description/parameters
    only -- enough for a harness to build its own tool-calling scaffolding
    without importing ASTRA internals.
    """

    name: str
    description: str
    parameters: dict[str, Any]


def _build_diagnostics_info() -> dict[str, Any]:
    """The diagnostics `info` carries: `None` until the episode ends and grading
    actually runs, since these are properties of the full trajectory, not of a
    single step.
    """
    return {
        "similarity": None,
        "milestone_similarity": None,
        "minefield_similarity": None,
        "turn_count": None,
        "empty_agent_turn_count": None,
        "hallucinated_tool_call_count": None,
        "retrieval_get_all_count": None,
        "retrieval_failed_search_count": None,
        "retrieval_efficiency": None,
        # True when grading itself failed (see `_calculate_reward`), so a caller
        # can tell a genuine 0.0 apart from an episode that could not be scored.
        "eval_error": False,
    }


class AstraGymnasiumEnv(gym.Env[str, str]):
    """A `gymnasium.Env` over one or more ASTRA scenarios.

    Resolves its scenario catalog once, at construction (via
    `astra_tool_sandbox.cli.utils.resolve_scenarios`), because resolving it per
    episode would cost 91.6s / ~950MB unfiltered versus 2.4s for
    `scenario_tags=["test"]` (measured 2026-09-10) -- always pass a filter. Each
    `reset()` deep-copies the scenario it is about to play, so per-episode state
    never leaks across episodes.

    `reset()` rotates through the resolved scenarios in a fixed round-robin
    order, or plays a named one when given `options={"scenario_name": ...}`.

    Only one env may be stepping per process: ASTRA's execution context is a
    process-global, so two concurrent episodes in one process would corrupt each
    other's databases. Vectorise across processes.
    """

    def __init__(
        self,
        *,
        scenario_tags: list[str] | None = None,
        desired_scenario_names: list[str] | None = None,
        preferred_tool_backend: ToolBackend = ToolBackend.DEFAULT,
        max_text_length: int = _DEFAULT_MAX_TEXT_LENGTH,
        exclude_nl_reply_milestones: bool = False,
        max_messages: int | None = None,
        max_unsuccessful_user_responses: int = 3,
        similarity_threshold: float | None = None,
        success_reward: float = 1.0,
    ) -> None:
        """Args:
        scenario_tags: Only resolve scenarios carrying all of these tags.
            Mutually exclusive with `desired_scenario_names`: ASTRA's
            underlying filter unions the two rather than intersecting them,
            which surfaces as a confusing empty-catalog error when both are
            set (see `resolve_scenarios`).
        desired_scenario_names: Only resolve these scenario names.
        preferred_tool_backend: Which backend to prefer for conflicting tool
            names (passed straight through to `resolve_scenarios`).
        max_text_length: `max_length` for both `action_space` and
            `observation_space`.
        exclude_nl_reply_milestones: When set, drop milestones that grade the
            agent's natural-language reply to the user (see
            `drop_nl_reply_milestones`). For harnesses with no LLM user
            simulator installed to receive that reply. Not a no-op: 1,224 of
            2,428 scenarios carry an AGENT->USER milestone.
        max_messages: Episode step budget. `None` (the default) falls back to
            each scenario's own `max_messages`.
        max_unsuccessful_user_responses: Number of consecutive natural-language
            actions (i.e. steps without a ```python code block) before the
            3-strike guardrail ends the episode.
        similarity_threshold: `None` (the default, and ASTRA's own convention)
            makes the terminal reward the raw `similarity` score. Otherwise the
            terminal reward is binary: `success_reward` when
            `similarity >= similarity_threshold`, else `0.0`.
        success_reward: The terminal reward on success when
            `similarity_threshold` is set. Unused otherwise.

        Raises:
            ValueError: if both `scenario_tags` and `desired_scenario_names`
                are given, or if the resolved catalog is empty.
        """
        if scenario_tags and desired_scenario_names:
            raise ValueError(
                "AstraGymnasiumEnv does not support combining scenario_tags "
                "and desired_scenario_names: ASTRA's resolve_scenarios() "
                "unions the two filters rather than intersecting them, and "
                "its arity check then raises a misleading empty-list "
                "KeyError. Pass one or the other."
            )
        super().__init__()

        resolved = resolve_scenarios(
            desired_scenario_names=desired_scenario_names,
            scenario_tags=scenario_tags,
            preferred_tool_backend=preferred_tool_backend,
        )
        if not resolved:
            raise ValueError(
                f"No scenarios resolved for scenario_tags={scenario_tags!r}, "
                f"desired_scenario_names={desired_scenario_names!r}"
            )

        self._scenarios = resolved
        self._scenario_names = sorted(resolved)
        self._task_idx = -1

        self._exclude_nl_reply_milestones = exclude_nl_reply_milestones
        self._max_messages = max_messages
        self._max_unsuccessful_user_responses = max_unsuccessful_user_responses
        self._similarity_threshold = similarity_threshold
        self._success_reward = success_reward

        # Set by reset(); None beforehand so tool_specs()/openai_tools()/step()
        # fail loudly rather than silently operating on ASTRA's default global
        # context if called first.
        self._scenario: Scenario | None = None
        self._current_scenario_name: str | None = None
        self._roles: dict[RoleType, BaseRole] = {}
        self._step_count = 0
        self._unsuccessful_response_count = 0
        self._episode_done = False
        self._truncated = False
        self._system_messages: list[str] = []

        self.action_space = spaces.Text(
            max_length=max_text_length, min_length=0, charset=_TEXT_CHARSET
        )
        self.observation_space = spaces.Text(
            max_length=max_text_length, min_length=0, charset=_TEXT_CHARSET
        )

    @property
    def scenario_names(self) -> list[str]:
        """The resolved catalog, in the order `reset()` rotates through it. These
        are the names accepted by `reset(options={"scenario_name": ...})`.
        """
        return list(self._scenario_names)

    @property
    def current_scenario_name(self) -> str:
        """The scenario the current (or most recently started) episode is
        playing. Raises `RuntimeError` before the first `reset()`.
        """
        if self._current_scenario_name is None:
            raise RuntimeError("Call reset() before current_scenario_name.")
        return self._current_scenario_name

    def _effective_max_messages(self) -> int:
        assert self._scenario is not None
        return (
            self._max_messages
            if self._max_messages is not None
            else self._scenario.max_messages
        )

    def _select_scenario_name(self, options: dict[str, Any] | None) -> str:
        """Pick the scenario for the episode `reset()` is about to start.

        `options={"scenario_name": ...}` plays that scenario without disturbing
        the round-robin cursor, so interleaving a targeted episode does not
        change the order the rotation resumes in. Anything else advances the
        rotation.
        """
        if options is not None and "scenario_name" in options:
            name = options["scenario_name"]
            if name not in self._scenarios:
                raise ValueError(
                    f"scenario_name={name!r} is not in this env's resolved "
                    f"catalog of {len(self._scenario_names)} scenario(s). The "
                    "catalog is fixed at construction because resolving it is "
                    "expensive; widen `scenario_tags` / "
                    "`desired_scenario_names` to include it."
                )
            return str(name)

        self._task_idx = (self._task_idx + 1) % len(self._scenario_names)
        return self._scenario_names[self._task_idx]

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[str, dict[str, Any]]:
        """Start a fresh episode and return `(observation, info)`.

        `observation` is the scenario's initial user query. `info` carries
        `system_messages`, which a harness MUST forward to its model -- see the
        `system_messages` property for why.

        Deep-copies the scenario and its starting context, installs the context
        as ASTRA's current one, and replays the
        SYSTEM -> EXECUTION_ENVIRONMENT messages (tool imports) so the
        interactive console has every tool bound by name before the first step.

        Args:
            seed: Forwarded to `gymnasium.Env.reset`. ASTRA scenarios are
                deterministic given an action sequence, so this seeds nothing
                of ASTRA's own.
            options: `{"scenario_name": <name>}` plays that scenario instead of
                advancing the round-robin rotation. The name must be in the
                catalog resolved at construction; see `scenario_names`.

        Raises:
            ValueError: if `options["scenario_name"]` is not in the catalog.
        """
        super().reset(seed=seed)

        name = self._select_scenario_name(options)
        self._current_scenario_name = name
        self._scenario = copy.deepcopy(self._scenarios[name])
        if self._exclude_nl_reply_milestones:
            drop_nl_reply_milestones(self._scenario.evaluation)

        self._step_count = 0
        self._unsuccessful_response_count = 0
        self._episode_done = False
        self._truncated = False

        execution_context = copy.deepcopy(self._scenario.starting_context)
        set_current_context(execution_context)
        execution_context = get_current_context()

        sandbox_db = execution_context.get_database(
            DatabaseNamespace.SANDBOX,
            drop_sandbox_message_index=False,
            get_all_history_snapshots=True,
        )
        max_sandbox_message_index = execution_context.max_sandbox_message_index

        self._roles = {
            RoleType.EXECUTION_ENVIRONMENT: ExecutionEnvironment(),
            RoleType.USER: BaseRole(),
        }

        for message_index in range(max_sandbox_message_index + 1):
            if (
                sandbox_db["recipient"][message_index] == RoleType.EXECUTION_ENVIRONMENT
                and sandbox_db["sender"][message_index] == RoleType.SYSTEM
            ):
                self._roles[RoleType.EXECUTION_ENVIRONMENT].respond(
                    ending_index=message_index
                )

        # Capture the SYSTEM -> AGENT messages. ASTRA's own agent role reads these
        # out of the execution context during `play()`'s dispatch, so a harness
        # that does not forward them under-informs the model relative to a normal
        # ASTRA run. They carry the assistant instructions AND the scenario's
        # clock, e.g. "Today is Saturday, December 7, 2024. Current time (ISO
        # format): 2024-12-07T08:05:00."
        #
        # These messages are the ONLY source of that date. Scenarios are set in
        # the past; `starting_context.reference_time` is None for them; and they
        # do not expose a time tool (none of the 14 `test`-tag scenarios lists one
        # in `tool_allow_list`). There is no time mocking anywhere in ASTRA, so a
        # model that writes its own `datetime.now()` -- which the interpreter will
        # happily run -- reads the real clock and gets the wrong day.
        #
        # Consequence: without these messages a task phrased "at 10am today" is
        # unsatisfiable. `get_add_calendar_DAWEI_SHEN` requires
        # `start_datetime_iso=2024-12-07T10:00:00`, verified by driving it with a
        # real model.
        self._system_messages = [
            str(sandbox_db["content"][i])
            for i in range(max_sandbox_message_index + 1)
            if sandbox_db["sender"][i] == RoleType.SYSTEM
            and sandbox_db["recipient"][i] == RoleType.AGENT
        ]

        # Only system messages should have been processed above.
        assert (
            get_current_context().max_sandbox_message_index == max_sandbox_message_index
        )

        scenario_user_messages = [
            sandbox_db["content"][i]
            for i in range(len(sandbox_db))
            if sandbox_db["sender"][i] == RoleType.USER
            and sandbox_db["recipient"][i] == RoleType.AGENT
        ]
        initial_query = scenario_user_messages[-1] if scenario_user_messages else ""
        return str(initial_query), {"system_messages": list(self._system_messages)}

    def step(self, action: str) -> tuple[str, float, bool, bool, dict[str, Any]]:
        """Play one step and return `(observation, reward, terminated, truncated, info)`.

        `action` is either a ```python code block (executed against the
        EXECUTION_ENVIRONMENT) or natural-language text (sent to the USER role,
        subject to the 3-strike guardrail). Calling `end_conversation()` from a
        code block, or mentioning `end_conversation` in text, finishes the
        episode.

        `terminated` and `truncated` are kept apart deliberately: `truncated` is
        True when the step budget ran out while the conversation was still
        active. RL value learning bootstraps from the final state of a truncated
        episode but not a terminated one, so collapsing the two biases the
        learned value function. An episode that both exhausts the budget and
        ends the conversation counts as terminated -- it did finish.

        Not bounded by a timeout -- see the module docstring.
        """
        if self._episode_done:
            raise RuntimeError("Episode is done. Call reset() to start a new episode.")
        if self._scenario is None:
            raise RuntimeError("Call reset() before step().")

        code, _ = extract_code(action)
        if code:
            # Issuing a tool call counts as progress, so reset the
            # natural-language guardrail counter.
            self._unsuccessful_response_count = 0
            self._execute_python_code(code)
        else:
            self._handle_natural_language(action)

        self._step_count += 1
        self._check_episode_completion()

        observation = self._get_observation()
        info = _build_diagnostics_info()
        info["truncated"] = self._truncated

        reward = 0.0
        if self._episode_done:
            reward = self._calculate_reward(info)

        terminated = self._episode_done and not self._truncated
        return observation, reward, terminated, self._truncated, info

    def _execute_python_code(self, python_code: str) -> None:
        """Send the agent's code to the execution environment and run it.

        Tool execution happens inside ASTRA's `code.InteractiveConsole`, so
        ordinary tool errors (e.g. a bad argument) already come back as the
        printed-traceback content of the environment's reply message. This
        guards only the surrounding role-dispatch machinery from aborting the
        whole step.
        """
        agent_to_env_message = Message(
            sender=RoleType.AGENT,
            recipient=RoleType.EXECUTION_ENVIRONMENT,
            content=python_code,
        )
        self._roles[RoleType.EXECUTION_ENVIRONMENT].add_messages([agent_to_env_message])
        try:
            self._roles[RoleType.EXECUTION_ENVIRONMENT].respond()
        except Exception as exc:  # noqa: BLE001
            self._send_error_message(f"ERROR: Python code execution failed: {exc}")

    def _send_error_message(self, content: str) -> None:
        error_message = Message(
            sender=RoleType.EXECUTION_ENVIRONMENT,
            recipient=RoleType.AGENT,
            content=content,
        )
        self._roles[RoleType.EXECUTION_ENVIRONMENT].add_messages([error_message])

    def _handle_natural_language(self, action: str) -> None:
        """A natural-language action is sent to the USER role.

        Either an explicit "end_conversation" mention or the 3-strike guardrail
        triggers conversation end.
        """
        agent_to_user_message = Message(
            sender=RoleType.AGENT,
            recipient=RoleType.USER,
            content=action,
        )
        self._roles[RoleType.USER].add_messages([agent_to_user_message])

        is_completion_signal = "end_conversation" in action.lower()

        is_failed_signal = False
        if not is_completion_signal:
            self._unsuccessful_response_count += 1
            if (
                self._unsuccessful_response_count
                >= self._max_unsuccessful_user_responses
            ):
                is_failed_signal = True

        if is_completion_signal or is_failed_signal:
            self._trigger_conversation_end()

    def _trigger_conversation_end(self) -> None:
        """Inject an `end_conversation()` tool call as if the USER role had
        issued it, since there is no LLM user simulator installed to do so
        itself.
        """
        self._unsuccessful_response_count = 0

        self._roles[RoleType.USER].add_messages(
            [
                Message(
                    sender=RoleType.USER,
                    recipient=RoleType.EXECUTION_ENVIRONMENT,
                    content=(
                        "parameters_end = {}\n"
                        "result_end = end_conversation(**parameters_end)\n"
                        "print(result_end)"
                    ),
                )
            ]
        )

        user_messages = self._roles[RoleType.USER].get_messages()
        if (
            user_messages
            and user_messages[-1].recipient == RoleType.EXECUTION_ENVIRONMENT
        ):
            self._roles[RoleType.EXECUTION_ENVIRONMENT].respond()

    def _check_episode_completion(self) -> None:
        """The episode ends when `end_conversation()` flipped
        `conversation_active` to `False` in the SANDBOX database, or the step
        budget is exhausted.
        """
        if self._episode_done:
            return

        current_context = get_current_context()
        sandbox_db = current_context.get_database(
            DatabaseNamespace.SANDBOX,
            drop_sandbox_message_index=False,
        )

        conversation_active = True
        if len(sandbox_db) > 0:
            conversation_active = sandbox_db["conversation_active"][-1]

        budget_exhausted = self._step_count >= self._effective_max_messages()
        self._episode_done = not conversation_active or budget_exhausted
        self._truncated = budget_exhausted and conversation_active

    def _get_observation(self) -> str:
        """The observation is the most recent EXECUTION_ENVIRONMENT -> AGENT
        message, or `""` when the last message was not addressed to the agent
        (e.g. after a natural-language action that did not end the
        conversation).
        """
        current_context = get_current_context()
        sandbox_db = current_context.get_database(
            DatabaseNamespace.SANDBOX,
            drop_sandbox_message_index=False,
        )

        if len(sandbox_db) == 0:
            return ""

        is_env_to_agent = (
            sandbox_db["recipient"][-1] == RoleType.AGENT.value
            and sandbox_db["sender"][-1] == RoleType.EXECUTION_ENVIRONMENT.value
        )
        if is_env_to_agent:
            content = sandbox_db["content"][-1] or ""
            return str(content) if content else "Tool execution completed."

        return ""

    def _calculate_reward(self, info: dict[str, Any]) -> float:
        """Grade the finished episode and fill `info`'s diagnostics in place.

        Deliberately catches `BaseException`, not `Exception`: ASTRA's
        brute-force evaluator can raise arbitrary errors on some trajectories --
        including a polars `pyo3_runtime.PanicException` (a Rust panic surfaced
        at the FFI boundary, e.g. calling `.lower()` on a `None` value in
        rouge-l similarity). These are not ordinary `Exception`s, so the episode
        is scored 0 here rather than letting the error propagate and abort a
        whole rollout.
        """
        assert self._scenario is not None
        try:
            current_context = get_current_context()
            evaluation_result = self._scenario.evaluation.evaluate(
                execution_context=current_context,
                max_turn_count=self._effective_max_messages(),
            )
        except BaseException:  # noqa: BLE001
            info["eval_error"] = True
            return 0.0

        info["similarity"] = evaluation_result.similarity
        info["milestone_similarity"] = evaluation_result.milestone_similarity
        info["minefield_similarity"] = evaluation_result.minefield_similarity
        info["turn_count"] = evaluation_result.turn_count
        info["empty_agent_turn_count"] = evaluation_result.empty_agent_turn_count
        info["hallucinated_tool_call_count"] = (
            evaluation_result.hallucinated_tool_call_count
        )
        info["retrieval_get_all_count"] = evaluation_result.retrieval_get_all_count
        info["retrieval_failed_search_count"] = (
            evaluation_result.retrieval_failed_search_count
        )
        info["retrieval_efficiency"] = evaluation_result.retrieval_efficiency

        if self._similarity_threshold is None:
            return evaluation_result.similarity
        if evaluation_result.similarity >= self._similarity_threshold:
            return self._success_reward
        return 0.0

    @property
    def system_messages(self) -> list[str]:
        """The current episode's SYSTEM -> AGENT messages, in order.

        A harness MUST forward these to its model. ASTRA's own agent role reads
        them from the execution context, so omitting them under-informs the model
        relative to a normal ASTRA run -- they carry both the assistant
        instructions and the scenario's clock ("Today is Saturday, December 7,
        2024...").

        They are the only source of that date: scenarios are set in the past,
        `reference_time` is None, no time tool is exposed, and nothing in ASTRA
        mocks the clock -- so a model left to its own `datetime.now()` reads the
        real one and answers for the wrong day.

        Also returned as `info["system_messages"]` by `reset()`. Empty until
        `reset()` has been called.
        """
        return list(self._system_messages)

    def tool_specs(self) -> dict[str, ToolSpec]:
        """The tools available to the agent right now, keyed by agent-facing
        name, as name/description/parameters only -- enough for a harness to
        build its own tool-calling scaffolding without touching ASTRA
        internals. Must be called after `reset()`.

        Reuses `common/tool_conversion.py::convert_python_function_to_openai_function`
        (which itself uses `augmented_getdoc`/`augmented_parameters` for
        docstring parsing and `NotGiven` handling) rather than a hand-rolled
        `inspect.signature` walk.
        """
        if self._scenario is None:
            raise RuntimeError("Call reset() before tool_specs().")
        tools = get_current_context().get_available_tools(scrambling_allowed=False)
        specs: dict[str, ToolSpec] = {}
        for name, func in tools.items():
            function = convert_python_function_to_openai_function(name, func)
            specs[name] = ToolSpec(
                name=name,
                description=str(function["description"]),
                parameters=dict(function["parameters"]),
            )
        return specs

    def openai_tools(self) -> list[ChatCompletionToolParam]:
        """The tools available to the agent right now, in OpenAI
        `chat.completions` tool-calling format. Must be called after `reset()`.
        """
        if self._scenario is None:
            raise RuntimeError("Call reset() before openai_tools().")
        tools = get_current_context().get_available_tools(scrambling_allowed=False)
        return convert_to_openai_tools(tools)
