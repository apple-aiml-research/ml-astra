# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Test case scenarios"""

import copy
import json
import logging
import os
import signal
import traceback
import warnings
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union, cast

import polars as pl
from attrs import Factory, define
from tqdm import tqdm

from astra_tool_sandbox.common.constants import (
    GLOBAL_TIME,
    PACKAGE_DIR,
)
from astra_tool_sandbox.common.evaluation import (
    Evaluation,
    EvaluationLLM,
    EvaluationLLMResult,
    EvaluationResult,
    Milestone,
    MilestoneMatcher,
    Minefield,
)
from astra_tool_sandbox.common.execution_context import (
    DatabaseNamespace,
    ExecutionContext,
    RoleType,
    ScenarioCategories,
    get_current_context,
    set_current_context,
)
from astra_tool_sandbox.common.message_conversion import (
    serialize_to_conversation,
)
from astra_tool_sandbox.common.tool_conversion import convert_to_openai_tools
from astra_tool_sandbox.common.utils import (
    format_date_string,
    load_str_time_to_datetime_iso_8601,
)
from astra_tool_sandbox.roles.base_role import BaseRole

logger = logging.getLogger(__name__)


#: Playback timeout while the agent under test was mid-turn. Attributable to the
#: model: it did not converge inside its own budget.
AGENT_TIMEOUT_EXCEPTION = "TimeoutError"

#: Playback timeout while the *user simulator* was mid-turn. `play()` drives both
#: roles, and the simulator makes its own LLM calls, so the budget can expire on its
#: latency rather than the agent's. Kept distinct so it is not scored against the
#: model under test.
USER_SIMULATOR_TIMEOUT_EXCEPTION = "UserSimulatorTimeoutError"

#: Grading exceeded its own budget. A harness resource limit, never the model's fault.
GRADING_TIMEOUT_EXCEPTION = "GradingTimeoutError"


def _attribute_playback_timeout() -> str:
    """Name a playback timeout after whichever role was mid-turn when it fired.

    `play()` dispatches to `roles[last_message.recipient]`, and the in-flight role has
    not committed its reply yet — so the last committed message's recipient is the
    role that was executing. Without this split, a slow user simulator would be
    scored as an agent failure.
    """
    try:
        sandbox = get_current_context().get_database(DatabaseNamespace.SANDBOX)
        mid_turn_role = sandbox["recipient"][-1]
    except Exception:  # noqa: BLE001 - attribution must never mask the timeout
        return AGENT_TIMEOUT_EXCEPTION
    if mid_turn_role == RoleType.USER:
        return USER_SIMULATOR_TIMEOUT_EXCEPTION
    return AGENT_TIMEOUT_EXCEPTION


@contextmanager
def _time_budget(
    seconds: Optional[int], scenario_name: str, phase: str
) -> Iterator[None]:
    """Bound one phase with SIGALRM, guaranteeing the alarm is cancelled on exit.

    Playback and grading get separate budgets. Grading used to share playback's,
    which cost it time on multi-milestone scenarios even though it is CPU-bound work
    on a trajectory already paid for in full. It still gets a generous cap of its
    own: the milestone matcher is a DFS over milestone x snapshot mappings, so while
    it is deterministic it is not provably bounded, and a pathological trajectory
    should not be able to hang a worker.

    No-op when `seconds` is None, or off the main thread where signal handlers
    cannot be installed. Scenario workers are `multiprocessing` processes running on
    their main thread, so the budgets do apply in a normal run.
    """
    if not seconds:
        yield
        return

    def _on_timeout(signum: int, frame: Any) -> None:
        raise TimeoutError(
            f"Scenario {scenario_name!r} exceeded its {seconds} second {phase} budget"
        )

    try:
        previous = signal.signal(signal.SIGALRM, _on_timeout)
    except ValueError:
        # Not the main thread — cannot install a handler.
        yield
        return
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


@define
class ScenarioResult:
    """Output of Scenario Play, saving both the execution context after the rollout is collected,
    and evaluation result

    """

    ending_context: ExecutionContext
    evaluation_result: Optional[EvaluationResult]
    evaluation_LLM_result: Optional[EvaluationLLMResult]
    # Set when playback stopped early (agent/user API error, a grading bug, or the
    # caller's per-scenario timeout). The trajectory is still graded up to that
    # point, so the results above are real rather than placeholder zeros; these
    # record what went wrong so callers can still attribute the failure. Either
    # result is None only when grading itself could not run on the partial
    # trajectory — meaning "not scored", not "scored zero".
    play_exception_type: Optional[str] = None
    play_traceback: Optional[str] = None
    # Judge input, built here because it needs the live ExecutionContext, but scored
    # by the caller after the scenario pool drains — see
    # EvaluationLLM.prepare_eval_task. None when llm_evaluation is off.
    llm_eval_task: Optional[Dict[str, Any]] = None


@define
class Scenario:
    """Test case scenarios that defines a test case
    Each scenario contains an execution context defining starting state, and an evaluation object defining
    evaluation criteria
    """

    # Initial context, contains initial world state
    starting_context: ExecutionContext = Factory(ExecutionContext)
    # Evaluation definition
    evaluation: Evaluation = Factory(Evaluation)
    # Evaluation LLM
    evaluation_LLM: EvaluationLLM = Factory(EvaluationLLM)
    # Max number of total messages in roll out
    max_messages: int = 30
    # Category tags
    categories: List[ScenarioCategories] = Factory(list)
    # Scenario context tags
    tags: List[str] = Factory(list)

    def play(
        self, roles: Dict[RoleType, BaseRole], scenario_name: str
    ) -> ExecutionContext:
        """Play out the scenario and return execution context

        Args:
            roles:  A mapping indicating which Role we should use for each role type
            scenario_name: The scenario name.

        Returns:
            Execution context after playing out the scenario

        """
        execution_context = copy.deepcopy(self.starting_context)

        set_current_context(execution_context)
        execution_context = get_current_context()
        # Prepare InteractiveConsole by consuming system message addressed to it
        sandbox_db = execution_context.get_database(
            DatabaseNamespace.SANDBOX,
            drop_sandbox_message_index=False,
            get_all_history_snapshots=True,
        )
        max_sandbox_message_index = execution_context.max_sandbox_message_index
        for message_index in range(max_sandbox_message_index + 1):
            if (
                sandbox_db["recipient"][message_index] == RoleType.EXECUTION_ENVIRONMENT
                and sandbox_db["sender"][message_index] == RoleType.SYSTEM
            ):
                roles[sandbox_db["recipient"][message_index]].respond(
                    ending_index=message_index
                )
        # Since this should only be processing system message, there should be no new messages after this
        assert (
            get_current_context().max_sandbox_message_index == max_sandbox_message_index
        )
        # Start processing non-system messages
        with tqdm(total=self.max_messages, desc=scenario_name) as pbar:
            while (
                sandbox_db["conversation_active"][-1]
                and sandbox_db["sandbox_message_index"][-1]
                < self.max_messages + max_sandbox_message_index
            ):
                roles[sandbox_db["recipient"][-1]].respond()
                sandbox_db = get_current_context().get_database(
                    DatabaseNamespace.SANDBOX, drop_sandbox_message_index=False
                )
                pbar.update(1)
            # Update max turns on successful end.
            pbar.total = pbar.n
            pbar.update(0)

        return get_current_context()

    def play_and_evaluate(
        self,
        roles: Dict[RoleType, BaseRole],
        output_directory: Path,
        scenario_name: str,
        play_timeout_seconds: Optional[int] = None,
        grade_timeout_seconds: Optional[int] = None,
    ) -> ScenarioResult:
        """Play out the scenario and evaluate according to evaluation

        Args:
            roles:                      A mapping indicating which Role we should use for each role type
            output_directory:           Directory to write results to
            scenario_name:              Unique name for scenario. Used to serialize message history

        Returns:
            A ScenarioResult object containing the final execution context and evaluation result
            If play failed due to errors, return None object

        """
        # Prepare directories
        scenario_output_directory: Path = (
            output_directory / "trajectories" / scenario_name
        )
        scenario_output_directory.mkdir(exist_ok=True, parents=True)

        # A scenario that stopped part-way still has the turns it completed, and those
        # are worth grading — an agent that reached three of four milestones before
        # naming a tool it was not offered should keep the three. So record the failure
        # and continue to evaluation instead of re-raising, which used to discard the
        # whole trajectory and force every metric to a placeholder zero.
        play_exception_type: Optional[str] = None
        play_traceback: Optional[str] = None
        try:
            with _time_budget(play_timeout_seconds, scenario_name, "playback"):
                self.play(roles=roles, scenario_name=scenario_name)
        except Exception as play_exception:
            play_exception_type = type(play_exception).__name__
            if isinstance(play_exception, TimeoutError):
                play_exception_type = _attribute_playback_timeout()
            play_traceback = traceback.format_exc()
            logger.warning(
                "Scenario %r stopped early (%s); grading the partial trajectory",
                scenario_name,
                play_exception_type,
            )
        finally:
            execution_context = get_current_context()

            # Write pretty print messages
            # Skip user simulator few shot messages
            pretty_print_str = (
                "Note that User Simulator few shot messages have been omitted\n"
                + str(
                    execution_context.get_database(
                        DatabaseNamespace.SANDBOX,
                        get_all_history_snapshots=True,
                        drop_sandbox_message_index=False,
                    )
                    .filter(
                        (pl.col("visible_to") != [RoleType.USER])
                        | (pl.col("visible_to").is_null())
                    )
                    .drop(
                        [
                            "openai_tool_call_id",
                            "conversation_active",
                        ]
                    )
                )
            )
            with open(
                scenario_output_directory / "pretty_print.txt", "w", encoding="utf-8"
            ) as f:
                f.write(pretty_print_str)
            # Write execution_context
            with open(
                scenario_output_directory / "execution_context.json",
                "w",
                encoding="utf-8",
            ) as f:
                # We'll have to ditch dill InteractiveConsole here because
                # dill creates a bytes instead of raw string
                f.write(
                    json.dumps(
                        execution_context.to_dict(serialize_console=False),
                        ensure_ascii=False,
                        indent=4,
                    )
                )

        # Grading a partial trajectory is best-effort: a matcher can legitimately fail
        # on a truncated conversation. Never let that mask the original playback
        # failure, and never let it be mistaken for a scored zero — an ungradeable
        # partial keeps None so the aggregators exclude it. When playback succeeded a
        # grading failure is a real bug and must still surface.
        evaluation_result: Optional[EvaluationResult]
        try:
            with _time_budget(grade_timeout_seconds, scenario_name, "grading"):
                evaluation_result = self.evaluation.evaluate(
                    execution_context=execution_context,
                    max_turn_count=self.max_messages,
                )
        except TimeoutError:
            # A resource limit, not a defect, so never fatal — unlike the branch
            # below. Recorded as a failure so the scenario is excluded rather than
            # silently scoring None with no stated reason.
            logger.warning(
                "Scenario %r: rule-based grading exceeded its %ss budget",
                scenario_name,
                grade_timeout_seconds,
            )
            evaluation_result = None
            if play_exception_type is None:
                play_exception_type = GRADING_TIMEOUT_EXCEPTION
                play_traceback = traceback.format_exc()
        except Exception:
            if play_exception_type is None:
                raise
            logger.warning(
                "Scenario %r: rule-based grading failed on the partial trajectory",
                scenario_name,
                exc_info=True,
            )
            evaluation_result = None

        # Build the judge input but do NOT call the judge here. This runs inside the
        # caller's per-scenario timeout, and the judge client retries with a long
        # timeout — so an LLM call here can itself exhaust the budget it is being
        # timed against, and once that alarm has fired it cannot fire again. The
        # caller scores these after the pool drains.
        llm_eval_task: Optional[Dict[str, Any]]
        try:
            llm_eval_task = self.evaluation_LLM.prepare_eval_task(
                execution_context=execution_context,
                stopped_early_reason=play_exception_type,
            )
        except Exception:
            if play_exception_type is None:
                raise
            logger.warning(
                "Scenario %r: could not build the judge input from the partial "
                "trajectory",
                scenario_name,
                exc_info=True,
            )
            llm_eval_task = None
        evaluation_LLM_result: Optional[EvaluationLLMResult] = None

        # Write the conversation to a JSON file. The serializer is keyed on the
        # milestone mapping, so there is nothing to write when grading could not run.
        conversation: List[Dict[str, Any]] = []
        if evaluation_result is not None:
            conversation = serialize_to_conversation(
                execution_context=execution_context,
                evaluation_result=evaluation_result,
                milestones=cast(
                    list[Milestone], self.evaluation.milestone_matcher.milestones
                ),
                minefields=cast(
                    list[Minefield], self.evaluation.minefield_matcher.milestones
                ),
            )
        with open(
            scenario_output_directory / "conversation.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(conversation, f, indent=2, ensure_ascii=False)

        # Write OpenAI client format messages and tools for reproducibility/debugging.
        # Extract only the standard OpenAI message fields (drop evaluation extras).
        openai_message_fields = {
            "role",
            "content",
            "tool_calls",
            "tool_call_id",
            "name",
        }
        openai_messages_clean = [
            {k: v for k, v in turn.items() if k in openai_message_fields}
            for turn in conversation
        ]
        available_tools = execution_context.get_available_tools(scrambling_allowed=True)
        openai_tools = convert_to_openai_tools(available_tools)
        with open(
            scenario_output_directory / "openai_request.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                {"messages": openai_messages_clean, "tools": openai_tools},
                f,
                indent=2,
                ensure_ascii=False,
            )

        return ScenarioResult(
            ending_context=execution_context,
            evaluation_result=evaluation_result,
            evaluation_LLM_result=evaluation_LLM_result,
            play_exception_type=play_exception_type,
            play_traceback=play_traceback,
            llm_eval_task=llm_eval_task,
        )


@define
class ScenarioExtension:
    """Extends a few fields over base scenario to form a valid test scenario"""

    # Name for the resulting extended scenario
    name: str
    # Base scenario to extend on
    base_scenario: Scenario
    # Messages to extend to the starting context of base scenario
    messages: list[dict[str, Union[str, list[RoleType]]]] = Factory(list)
    # Tool allow list to extend to starting context of base scenario
    tool_allow_list: Optional[List[str]] = None
    # Tool deny list to extend to starting context of base scenario
    tool_deny_list: Optional[List[str]] = None
    # Evaluation milestones to extend to the evaluation of base scenario
    milestones: List[Milestone] = Factory(list)
    # Optional edge list defining Milestone dependencies. If None, creates a linked list
    milestone_edge_list: Optional[List[Tuple[int, int]]] = None
    # Evaluation minefields to extend to the evaluation of base scenario
    minefields: List[Minefield] = Factory(list)
    # Optional edge list defining Minefield dependencies. If None, creates a linked list
    minefield_edge_list: Optional[List[Tuple[int, int]]] = None
    # Categories to extend to scenario
    categories: List[ScenarioCategories] = Factory(list)
    # Tags associated to extend to scenarios
    tags: List[str] = Factory(list)
    # Reference Time for this scenario
    reference_time: str = GLOBAL_TIME
    # Is Read Time for this scenario
    is_read_time: Optional[str] = None
    # Reasoning Monologue
    reasoning: Optional[str] = None
    # Success Conditions for this scenario extension
    success_conditions: Optional[List[Dict[str, str]]] = None
    # Optional user of LLM evaluation
    llm_evaluation: Optional[bool] = False

    def get_extended_scenario_meta(self) -> Dict[str, Any]:
        """Get an extended scenario with meta data only based on specified extensions without updating personal context relevant to the scenario extensions for faster iteration

        Returns:
            A dictionary containing extended scenario name and meta information
        """

        return {
            self.name: {"name": self.name, "tags": [tag.lower() for tag in self.tags]}
        }

    def get_extended_scenario(self) -> Dict[str, Scenario]:
        """Get an extended scenario based on specified extensions with cutoff of the personal context

        Returns:
            A dictionary containing extended scenario and name
        """
        scenario: Scenario = copy.deepcopy(self.base_scenario)
        scenario.categories.extend(self.categories)
        scenario.tags.extend(self.tags)
        if self.tool_allow_list is not None:
            if scenario.starting_context.tool_allow_list is None:
                scenario.starting_context.tool_allow_list = ["end_conversation"]
            scenario.starting_context.tool_allow_list.extend(self.tool_allow_list)
        if self.tool_deny_list is not None:
            if scenario.starting_context.tool_deny_list is None:
                scenario.starting_context.tool_deny_list = []
            scenario.starting_context.tool_deny_list.extend(self.tool_deny_list)
        # Add reasoning and success_conditions to execution_context
        if self.reasoning is not None:
            if scenario.starting_context.reasoning is None:
                scenario.starting_context.reasoning = self.reasoning

        if self.success_conditions is not None:
            if scenario.starting_context.success_conditions is None:
                scenario.starting_context.success_conditions = self.success_conditions

        def safely_add_to_database(
            db_update: pl.DataFrame, database_namespace: DatabaseNamespace
        ) -> None:
            schema = scenario.starting_context.dbs_schemas[database_namespace]
            persist_cols = [c for c in schema if c != "sandbox_message_index"]

            # Guard: unknown columns (prefer raising over silent drop)
            unknown = set(db_update.columns) - set(persist_cols)
            if unknown:
                raise KeyError(
                    f"Unknown columns for {database_namespace}: {unknown}. Allowed: {set(persist_cols)}"
                )

            # Add missing cols as typed nulls, then order & cast
            if missing := [c for c in persist_cols if c not in db_update.columns]:
                db_update = db_update.with_columns(
                    [pl.lit(None, dtype=schema[c]).alias(c) for c in missing]
                )
            db_update = db_update.select(persist_cols).with_columns(
                [pl.col(c).cast(schema[c]).alias(c) for c in persist_cols]
            )

            if db_update.is_empty():
                headguard = pl.DataFrame(
                    {c: [None] for c in persist_cols}
                ).with_columns(
                    [pl.col(c).cast(schema[c]).alias(c) for c in persist_cols]
                )
                scenario.starting_context.add_to_starting_context_database(
                    namespace=database_namespace, rows_frame=headguard, force=True
                )
            else:
                scenario.starting_context.add_to_starting_context_database(
                    namespace=database_namespace, rows_frame=db_update
                )

        """ Add Reference Time Filter """
        contact_db = scenario.starting_context.get_database(
            namespace=DatabaseNamespace.CONTACT
        )
        self_person_id = contact_db.filter(pl.col("is_self"))[0, "person_id"]
        self_full_name = contact_db.filter(pl.col("is_self"))[0, "full_name"]

        # Update PhoneCall
        phonecall_db = scenario.starting_context.get_database(
            namespace=DatabaseNamespace.PHONE
        )
        if not phonecall_db.is_empty():
            # print(f"PHONE CALL is NOT EMPTY: {phonecall_db}")
            phonecall_db_updated = filter_contexts_by_reference_time(
                dataframe=phonecall_db,
                datetime_col="creation_datetime_iso",
                reference_time=self.reference_time,
            )
            scenario.starting_context._dbs[DatabaseNamespace.PHONE] = pl.DataFrame(
                schema=scenario.starting_context.dbs_schemas[DatabaseNamespace.PHONE]
            )
            safely_add_to_database(
                db_update=phonecall_db_updated,
                database_namespace=DatabaseNamespace.PHONE,
            )

        # Update Messages
        message_db = scenario.starting_context.get_database(
            namespace=DatabaseNamespace.MESSAGING
        )
        if not message_db.is_empty():
            message_db_updated = label_and_filter_messages(
                message_db=message_db,
                self_person_identifier=self_person_id,
                self_person_identifier_colname="sender_person_id",
                reference_time=self.reference_time,
                is_read_time=self.is_read_time,
            )

            scenario.starting_context._dbs[DatabaseNamespace.MESSAGING] = pl.DataFrame(
                schema=scenario.starting_context.dbs_schemas[
                    DatabaseNamespace.MESSAGING
                ]
            )
            safely_add_to_database(
                db_update=message_db_updated,
                database_namespace=DatabaseNamespace.MESSAGING,
            )

        # Update Calendar
        calendar_db = scenario.starting_context.get_database(
            namespace=DatabaseNamespace.CALENDAR
        )
        if not calendar_db.is_empty():
            calendar_db_updated = filter_contexts_by_reference_time(
                dataframe=calendar_db,
                datetime_col="creation_datetime_iso",
                reference_time=self.reference_time,
            )
            scenario.starting_context._dbs[DatabaseNamespace.CALENDAR] = pl.DataFrame(
                schema=scenario.starting_context.dbs_schemas[DatabaseNamespace.CALENDAR]
            )
            safely_add_to_database(
                db_update=calendar_db_updated,
                database_namespace=DatabaseNamespace.CALENDAR,
            )

        # Update Emails
        email_db = scenario.starting_context.get_database(
            namespace=DatabaseNamespace.EMAIL
        )
        if not email_db.is_empty():
            email_db_updated = label_and_filter_emails(
                email_db=email_db,
                self_person_id=self_person_id,
                reference_time=self.reference_time,
                is_read_time=self.is_read_time,
            )

            scenario.starting_context._dbs[DatabaseNamespace.EMAIL] = pl.DataFrame(
                schema=scenario.starting_context.dbs_schemas[DatabaseNamespace.EMAIL]
            )
            safely_add_to_database(
                db_update=email_db_updated, database_namespace=DatabaseNamespace.EMAIL
            )

        # Updata whatsapp
        whatsapp_db = scenario.starting_context.get_database(
            namespace=DatabaseNamespace.WHATSAPP
        )
        if not whatsapp_db.is_empty():
            whatsapp_db_updated = label_and_filter_messages(
                message_db=whatsapp_db,
                self_person_identifier=self_full_name,
                self_person_identifier_colname="sender_name",
                reference_time=self.reference_time,
                is_read_time=self.is_read_time,
            )
            scenario.starting_context._dbs[DatabaseNamespace.WHATSAPP] = pl.DataFrame(
                schema=scenario.starting_context.dbs_schemas[DatabaseNamespace.WHATSAPP]
            )
            safely_add_to_database(
                db_update=whatsapp_db_updated,
                database_namespace=DatabaseNamespace.WHATSAPP,
            )

        scenario.starting_context.add_to_database(
            namespace=DatabaseNamespace.SANDBOX,
            rows=[
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.AGENT,
                    "content": format_date_string(self.reference_time),
                }
            ]
            + self.messages,
        )

        scenario.evaluation = Evaluation(
            milestone_matcher=MilestoneMatcher(
                milestones=self.milestones, edge_list=self.milestone_edge_list
            ),
            minefield_matcher=MilestoneMatcher(
                milestones=self.minefields, edge_list=self.minefield_edge_list
            ),
        )

        # Add annotation_meta information
        annotation_meta = None
        # print(f"Scenario Name {self.name}")

        tags = self.tags

        if self.llm_evaluation:
            if (
                not scenario.starting_context.reasoning
                and not scenario.starting_context.success_conditions
            ):
                warnings.warn(
                    f"{self.name}: Reasoning and success conditions must be provided for LLM Evaluation, Skipped.",
                    UserWarning,
                )
            else:
                scenario.evaluation_LLM = EvaluationLLM(
                    reasoning=None,
                    success_conditions=None,
                    related_entities=None,
                )
            # to avoid circular impot
            from astra_tool_sandbox.scenarios.astra_v1.protagonists import (
                ProtagonistName,
            )

            protagonist_name = [
                tag for tag in tags if tag in [p.value for p in ProtagonistName]
            ]
            if protagonist_name:
                converted_dir = (
                    PACKAGE_DIR
                    / "scenarios"
                    / "astra_v1"
                    / protagonist_name[0]
                    / "converted_TAG_scenarios"
                )
                # Standard scenarios' annotation metadata lives in scenarios_jsons;
                # the misinformation/insufficient (challenging) set lives in
                # challenging_scenarios_jsons. Search both.
                for subdir in ("scenarios_jsons", "challenging_scenarios_jsons"):
                    jsons_path = converted_dir / subdir
                    if not jsons_path.is_dir():
                        continue
                    scenario_json = [
                        path_ for path_ in os.listdir(jsons_path) if self.name in path_
                    ]
                    if scenario_json:
                        try:
                            with open(
                                jsons_path / scenario_json[0],
                                "r",
                                encoding="utf-8",
                            ) as f:
                                annotation_meta = json.load(f)
                            break
                        except (OSError, ValueError):
                            print(f"{self.name} could not be read from {jsons_path}")
            else:
                print(
                    f"{self.name} annotation metafile does not exist, related entities will not be provided in LLM judge"
                )

            scenario.evaluation_LLM = EvaluationLLM(
                reasoning=scenario.starting_context.reasoning,
                success_conditions=scenario.starting_context.success_conditions,
                related_entities={
                    k: annotation_meta[k]
                    for k in (
                        "messages",
                        "whatsapp_messages",
                        "emails",
                        "calendars",
                        "contacts",
                        "phonecalls",
                    )
                    if k in annotation_meta
                }
                if annotation_meta
                else None,
            )
        else:
            # print("LLM evluation skipped")
            scenario.evaluation_LLM = EvaluationLLM(
                reasoning=None,
                success_conditions=None,
                related_entities=None,
            )

        # scenario.categories.extend(self.categories)

        # scenario.tags.extend(self.tags)
        return {self.name: scenario}


def label_and_filter_messages(
    message_db: pl.DataFrame,
    self_person_identifier: str,
    self_person_identifier_colname: str,
    reference_time: str,
    is_read_time: Union[str, None],
) -> pl.DataFrame:
    """
    Labels and filters a message DataFrame based on sender identity and message timestamps.

    Parameters:
    ----------
    message_db : pl.DataFrame
        The DataFrame containing message data. Must include:
        - 'sender_person_id' (str or int)
        - 'creation_datetime_iso' (datetime)
    self_person_identifier : str
        The protagonist contact person id or full name
    self_person_identifier_colname : str
        The protagonist contact person id or full name column name in the schema
    reference_time : str
        The current reference time to compare message timestamps.
    is_read_time : str
        The timestamp until which messages are considered read.

    Returns:
    -------
    pl.DataFrame
        The updated message DataFrame with a new `status` column and filtered to exclude null-status rows.
        Status values: 'sent', 'received', 'unread'.
    """
    if isinstance(reference_time, str):
        reference_time = cast(str, load_str_time_to_datetime_iso_8601(reference_time))
    if isinstance(is_read_time, str):
        is_read_time = load_str_time_to_datetime_iso_8601(is_read_time)
    elif is_read_time is None:
        # If is_read_time is None, fall back to reference_time
        is_read_time = reference_time

    message_db = message_db.with_row_index(name="row_index")

    message_db = (
        message_db.lazy()
        .with_columns(
            [
                pl.when(
                    (pl.col(self_person_identifier_colname) == self_person_identifier)
                    & (pl.col("creation_datetime_iso") <= is_read_time)
                )
                .then(pl.lit("sent"))
                # .when(
                #     (pl.col(self_person_identifier_colname) == self_person_identifier)
                #     & (pl.col("creation_datetime_iso") > is_read_time)
                # )
                # .then(pl.lit(f"future-sent at {is_read_time}"))
                .when(
                    (pl.col(self_person_identifier_colname) != self_person_identifier)
                    & (pl.col("creation_datetime_iso") <= is_read_time)
                )
                .then(pl.lit("read"))
                .when(
                    (pl.col(self_person_identifier_colname) != self_person_identifier)
                    & (pl.col("creation_datetime_iso") > is_read_time)
                    & (pl.col("creation_datetime_iso") <= reference_time)
                )
                .then(pl.lit("unread"))
                .otherwise(None)
                .alias("status")
            ]
        )
        .collect()
    )
    # Find cutoff index for pruning: first None-status row per (conversation_id, sender_person_id)
    cutoff_df = (
        message_db.filter(
            (
                pl.col("status").is_null()
                & (pl.col(self_person_identifier_colname) == self_person_identifier)
            )
        )
        .group_by(["conversation_id"])
        .agg(pl.col("row_index").min().alias("cutoff_index"))
    )

    # Join and prune rows after the first None-status per group
    message_db = (
        message_db.join(cutoff_df, on=["conversation_id"], how="left")
        .filter(
            (pl.col("cutoff_index").is_null())
            | (pl.col("row_index") < pl.col("cutoff_index"))
        )
        .drop("cutoff_index", "row_index")
    )

    return message_db.filter(pl.col("status").is_not_null())
    # return message_db.drop("row_index")


def filter_contexts_by_reference_time(
    dataframe: pl.DataFrame,
    reference_time: str,
    datetime_col: Optional[str] = "creation_datetime_iso",
) -> pl.DataFrame:
    if isinstance(reference_time, str):
        reference_time = cast(str, load_str_time_to_datetime_iso_8601(reference_time))
    return dataframe.filter(pl.col(cast(str, datetime_col)) <= reference_time)


def label_and_filter_emails(
    email_db: pl.DataFrame,
    self_person_id: str,
    reference_time: str,
    is_read_time: Union[str, None],
) -> pl.DataFrame:
    """
    Labels and filters an email DataFrame based on sender identity and email timestamps.

    Parameters:
    ----------
    email_db : pl.DataFrame
        The DataFrame containing email data. Must include:
        - 'sender_person_id' (str or int)
        - 'creation_datetime_iso' (datetime)
    self_person_id : str
        The protagonist contact person id
    reference_time : str
        The current reference time to compare email timestamps.
    is_read_time : str
        The timestamp until which emails are considered read.

    Returns:
    -------
    pl.DataFrame
        The updated email DataFrame with a new `status` column and filtered to exclude null-status rows.
        Status values: 'sent', 'received', 'unread', 'draft'.
    """
    if isinstance(reference_time, str):
        reference_time = cast(str, load_str_time_to_datetime_iso_8601(reference_time))
    if isinstance(is_read_time, str):
        is_read_time = load_str_time_to_datetime_iso_8601(is_read_time)
    elif is_read_time is None:
        # If is_read_time is None, fall back to reference_time
        is_read_time = reference_time

    email_db = email_db.with_row_index(name="row_index")

    email_db = (
        email_db.lazy()
        .with_columns(
            [
                pl.when(
                    (pl.col("sender_id") == self_person_id)
                    & (pl.col("creation_datetime_iso") <= is_read_time)
                    & (pl.col("recipients_ids").is_null())
                )
                .then(pl.lit("draft"))
                .when(
                    (pl.col("sender_id") == self_person_id)
                    & (pl.col("creation_datetime_iso") <= is_read_time)
                    & (~pl.col("recipients_ids").is_null())
                )
                .then(pl.lit("sent"))
                # .when(
                #     (pl.col("sender_person_id") == self_person_id)
                #     & (pl.col("creation_datetime_iso") > is_read_time)
                # )
                # .then(pl.lit(f"future-sent at {is_read_time}"))
                .when(
                    (pl.col("sender_id") != self_person_id)
                    & (pl.col("creation_datetime_iso") <= is_read_time)
                )
                .then(pl.lit("read"))
                .when(
                    (pl.col("sender_id") != self_person_id)
                    & (pl.col("creation_datetime_iso") > is_read_time)
                    & (pl.col("creation_datetime_iso") <= reference_time)
                )
                .then(pl.lit("unread"))
                .otherwise(None)
                .alias("status")
            ]
        )
        .collect()
    )
    # Find cutoff index for pruning: first None-status row per (conversation_id, sender_person_id)
    cutoff_df = (
        email_db.filter(
            (pl.col("status").is_null() & (pl.col("sender_id") == self_person_id))
        )
        .group_by(["thread_id"])
        .agg(pl.col("row_index").min().alias("cutoff_index"))
    )
    # Join and prune rows after the first None-status per group
    email_db = (
        email_db.join(cutoff_df, on=["thread_id"], how="left")
        .filter(
            (pl.col("cutoff_index").is_null())
            | (pl.col("row_index") < pl.col("cutoff_index"))
        )
        .drop("cutoff_index", "row_index")
    )
    return email_db.filter(pl.col("status").is_not_null())
