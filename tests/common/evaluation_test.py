# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
import json
import logging
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict

import polars as pl
import pytest

from astra_tool_sandbox.common.evaluation import (
    ColumnSimilarityMeasureType,
    Milestone,
    SnapshotConstraint,
    addition_similarity,
    column_contains_similarity,
    column_exact_match_similarity,
    column_rouge_l_similarity,
    column_str_contains_all_similarity,
    column_str_contains_any_similarity,
    column_tool_trace_exact_match_similarity,
    column_word_contains_any_similarity,
    column_word_contains_similarity,
    compute_milestone_completion_score,
    compute_retrieval_efficiency,
    milestone_tagger,
    snapshot_similarity,
    tool_trace_dependant_similarity,
)
from astra_tool_sandbox.common.execution_context import (
    DatabaseNamespace,
    ExecutionContext,
    RoleType,
)


@pytest.fixture
def reference_snapshot() -> pl.DataFrame:
    """Testing snapshot

    Returns:
        A Dataframe object representing a snapshot
    """
    return pl.DataFrame(
        [
            {"sandbox_message_index": 0, "content": "Hello there", "num": 0},
        ]
    )


@pytest.fixture
def snapshot() -> pl.DataFrame:
    """Testing snapshot

    Returns:
        A Dataframe object representing a snapshot
    """
    return pl.DataFrame(
        [
            {"sandbox_message_index": 1, "content": "Hello there", "num": 0},
            {"sandbox_message_index": 1, "content": "Hey there", "num": 1},
        ]
    )


@pytest.fixture
def column_similarities() -> Dict[str, ColumnSimilarityMeasureType]:
    """Testing column similarities

    Returns:

    """
    return {
        "content": column_rouge_l_similarity,
        "num": column_exact_match_similarity,
    }


def test_snapshot_similarity(
    reference_snapshot: pl.DataFrame,
    snapshot: pl.DataFrame,
    column_similarities: Dict[str, ColumnSimilarityMeasureType],
) -> None:
    # Different row count
    assert (
        snapshot_similarity(
            snapshot=snapshot,
            target_dataframe=pl.DataFrame(
                [
                    {"content": "Hello there", "num": 0},
                ]
            ),
            column_similarities=column_similarities,
            reference_snapshot=reference_snapshot,
        )
        == 0
    )
    # Different columns
    assert (
        snapshot_similarity(
            snapshot=snapshot,
            target_dataframe=pl.DataFrame(
                [
                    {
                        "sandbox_message_index": 0,
                        "content": "Hello there",
                        "wrong_column": "?",
                    },
                ]
            ),
            column_similarities=column_similarities,
            reference_snapshot=reference_snapshot,
        )
        == 0
    )
    # Subset columns
    assert (
        snapshot_similarity(
            snapshot=snapshot,
            target_dataframe=pl.DataFrame(
                [
                    {"num": 0},
                    {"num": 1},
                ]
            ),
            column_similarities=column_similarities,
            reference_snapshot=reference_snapshot,
        )
        == 1
    )
    # Similarity shouldn't be affected by row orders
    assert (
        0
        < snapshot_similarity(
            snapshot=snapshot,
            target_dataframe=pl.DataFrame(
                [
                    {"content": "Hi there", "num": 0},
                    {"content": "Hi there", "num": 1},
                ]
            ),
            column_similarities=column_similarities,
            reference_snapshot=reference_snapshot,
        )
        == snapshot_similarity(
            snapshot=snapshot,
            target_dataframe=pl.DataFrame(
                [
                    {"content": "Hi there", "num": 1},
                    {"content": "Hi there", "num": 0},
                ]
            ),
            column_similarities=column_similarities,
            reference_snapshot=reference_snapshot,
        )
        < 1
    )


def test_addition_similarity(
    reference_snapshot: pl.DataFrame,
    snapshot: pl.DataFrame,
    column_similarities: Dict[str, ColumnSimilarityMeasureType],
) -> None:
    assert (
        addition_similarity(
            snapshot=snapshot,
            target_dataframe=pl.DataFrame(
                [
                    {"content": "Hi there", "num": 1},
                    {"content": "Hi there", "num": 0},
                ]
            ),
            column_similarities=column_similarities,
            reference_snapshot=pl.DataFrame(
                [
                    {"sandbox_message_index": 0, "content": "Hello there", "num": 2},
                ]
            ),
        )
        == 0
    )
    assert (
        addition_similarity(
            snapshot=snapshot,
            target_dataframe=pl.DataFrame(
                [
                    {"content": "Hi there", "num": 1},
                    {"content": "Hi there", "num": 0},
                ]
            ),
            column_similarities=column_similarities,
            reference_snapshot=reference_snapshot,
        )
        == 0
    )
    assert (
        addition_similarity(
            snapshot=snapshot,
            target_dataframe=pl.DataFrame(
                [
                    {"content": "Hi there", "num": 0},
                ]
            ),
            column_similarities=column_similarities,
            reference_snapshot=reference_snapshot,
        )
        == 0
    )
    assert (
        0
        < addition_similarity(
            snapshot=snapshot,
            target_dataframe=pl.DataFrame(
                [
                    {"content": "Hi there", "num": 1},
                ]
            ),
            column_similarities=column_similarities,
            reference_snapshot=reference_snapshot,
        )
        < 1
    )


@pytest.fixture
def tool_trace_snapshot() -> pl.DataFrame:
    """Testing snapshot containing a tool_trace.

    Returns:
        Testing snapshot containing a tool_trace.
    """
    return pl.DataFrame(
        [
            {
                "tool_trace": [
                    json.dumps(
                        {
                            "tool_name": "search_holiday",
                            "arguments": {
                                "holiday_name": "Christmas Day",
                                "year": 2024,
                            },
                        },
                        ensure_ascii=False,
                    ),
                    json.dumps(
                        {
                            "tool_name": "search_lat_lon",
                            "arguments": {
                                "latitude": 37.334606,
                                "longitude": -122.009102,
                            },
                        },
                        ensure_ascii=False,
                    ),
                ]
            }
        ],
        schema={
            "tool_trace": pl.List(pl.String),
        },
    )


def test_column_tool_trace_exact_match_similarity(
    tool_trace_snapshot: pl.DataFrame,
) -> None:
    # Matching against 1 golden trace. Only present arguments are checked
    assert (
        column_tool_trace_exact_match_similarity(
            dataframe=tool_trace_snapshot,
            column_name="tool_trace",
            value=json.dumps(
                {
                    "tool_name": "search_stock",
                    "arguments": {
                        "query": "Apple",
                    },
                }
            ),
        )["similarity"][0]
        == 0
    )
    assert (
        column_tool_trace_exact_match_similarity(
            dataframe=tool_trace_snapshot,
            column_name="tool_trace",
            value=json.dumps(
                {
                    "tool_name": "search_holiday",
                    "arguments": {
                        "holiday_name": "Christmas Day",
                        "year": None,
                    },
                }
            ),
        )["similarity"][0]
        == 0
    )
    assert (
        column_tool_trace_exact_match_similarity(
            dataframe=tool_trace_snapshot,
            column_name="tool_trace",
            value=json.dumps(
                {
                    "tool_name": "search_holiday",
                    "arguments": {
                        "holiday_name": "Christmas Day",
                        "year": 2024,
                    },
                }
            ),
        )["similarity"][0]
        == 1
    )
    assert (
        column_tool_trace_exact_match_similarity(
            dataframe=tool_trace_snapshot,
            column_name="tool_trace",
            value=json.dumps(
                {
                    "tool_name": "search_holiday",
                    "arguments": {
                        "year": 2024,
                    },
                }
            ),
        )["similarity"][0]
        == 1
    )
    # Test multiple golden traces. Should match if one of them matches
    assert (
        column_tool_trace_exact_match_similarity(
            dataframe=tool_trace_snapshot,
            column_name="tool_trace",
            value=json.dumps(
                [
                    {
                        "tool_name": "search_holiday",
                        "arguments": {
                            "holiday_name": "Christmas Day",
                            "year": None,
                        },
                    },
                    {
                        "tool_name": "search_holiday",
                        "arguments": {
                            "holiday_name": "Christmas Day",
                            "year": 2024,
                        },
                    },
                ]
            ),
        )["similarity"][0]
        == 1
    )
    # Exact match float
    assert (
        column_tool_trace_exact_match_similarity(
            dataframe=tool_trace_snapshot,
            column_name="tool_trace",
            value=json.dumps(
                {
                    "tool_name": "search_lat_lon",
                    "arguments": {
                        "latitude": 37.34,
                        "longitude": -122.01,
                    },
                },
            ),
        )["similarity"][0]
        == 0
    )
    # atol in range
    assert (
        column_tool_trace_exact_match_similarity(
            dataframe=tool_trace_snapshot,
            column_name="tool_trace",
            value=json.dumps(
                {
                    "tool_name": "search_lat_lon",
                    "arguments": {
                        "latitude": 37.34,
                        "longitude": -122.01,
                    },
                },
            ),
            atol_dict={"latitude": 0.2, "longitude": 0.2},
        )["similarity"][0]
        == 1
    )
    # atol out of range
    assert (
        column_tool_trace_exact_match_similarity(
            dataframe=tool_trace_snapshot,
            column_name="tool_trace",
            value=json.dumps(
                {
                    "tool_name": "search_lat_lon",
                    "arguments": {
                        "latitude": 37.34,
                        "longitude": -122.01,
                    },
                },
            ),
            atol_dict={"latitude": 0.002, "longitude": 0.002},
        )["similarity"][0]
        == 0
    )


@pytest.fixture
def tool_trace_dependant_similarity_kwargs() -> dict[str, Any]:
    """Testing kwargs for tool_trace_dependant_similarity.

    Returns:
        Testing kwargs for tool_trace_dependant_similarity.
    """
    return {
        "snapshot": pl.DataFrame(
            [
                {
                    "tool_trace": [
                        json.dumps(
                            {
                                "tool_name": "search_holiday",
                                "arguments": {
                                    "holiday_name": "Christmas Day",
                                    "year": 2024,
                                },
                            },
                            ensure_ascii=False,
                        ),
                    ]
                }
            ],
            schema=ExecutionContext.dbs_schemas[DatabaseNamespace.SANDBOX],
        ),
        "reference_snapshot": pl.DataFrame(
            [
                {
                    "tool_trace": [
                        json.dumps(
                            {"results": 2024},
                            ensure_ascii=False,
                        ),
                    ]
                }
            ],
            schema=ExecutionContext.dbs_schemas[DatabaseNamespace.SANDBOX],
        ),
        "column_similarities": {"tool_trace": column_tool_trace_exact_match_similarity},
        "fill_to": "tool_trace",
    }


def test_tool_trace_dependant_similarity(
    tool_trace_dependant_similarity_kwargs: dict[str, Any],
) -> None:
    # Test extracting 1 argument
    assert (
        tool_trace_dependant_similarity(
            **tool_trace_dependant_similarity_kwargs,
            target_dataframe=pl.DataFrame(
                {
                    "tool_trace": json.dumps(
                        {
                            "tool_name": "search_holiday",
                            "arguments": {
                                "holiday_name": "Christmas Day",
                            },
                        },
                        ensure_ascii=False,
                    ),
                }
            ),
            extractor=lambda x: [{"year": x["results"]}],
        )
        == 1
    )
    # Test extraction error
    assert (
        tool_trace_dependant_similarity(
            **tool_trace_dependant_similarity_kwargs,
            target_dataframe=pl.DataFrame(
                {
                    "tool_trace": json.dumps(
                        {
                            "tool_name": "search_holiday",
                            "arguments": {
                                "holiday_name": "Christmas Day",
                            },
                        },
                        ensure_ascii=False,
                    ),
                }
            ),
            extractor=lambda x: [{"day": x["results"]}],
        )
        == 0
    )
    # Test incorrect extracted argument
    assert (
        tool_trace_dependant_similarity(
            **tool_trace_dependant_similarity_kwargs,
            target_dataframe=pl.DataFrame(
                {
                    "tool_trace": json.dumps(
                        {
                            "tool_name": "search_holiday",
                            "arguments": {
                                "holiday_name": "Christmas Day",
                            },
                        },
                        ensure_ascii=False,
                    ),
                }
            ),
            extractor=lambda x: [{"year": x["results"] + 1}],
        )
        == 0
    )
    # Test prefers provided argument 1 argument
    assert (
        tool_trace_dependant_similarity(
            **tool_trace_dependant_similarity_kwargs,
            target_dataframe=pl.DataFrame(
                {
                    "tool_trace": json.dumps(
                        {
                            "tool_name": "search_holiday",
                            "arguments": {
                                "holiday_name": "Christmas Day",
                                "year": 2024,
                            },
                        },
                        ensure_ascii=False,
                    ),
                }
            ),
            extractor=lambda x: [{"year": x["results"] + 1}],
        )
        == 1
    )
    # Test multiple traces
    assert (
        tool_trace_dependant_similarity(
            **tool_trace_dependant_similarity_kwargs,
            target_dataframe=pl.DataFrame(
                {
                    "tool_trace": json.dumps(
                        [
                            {
                                "tool_name": "search_holiday",
                                "arguments": {
                                    "holiday_name": "Christmas Day",
                                    "year": None,
                                },
                            },
                            {
                                "tool_name": "search_holiday",
                                "arguments": {
                                    "holiday_name": "Christmas Day",
                                },
                            },
                        ],
                        ensure_ascii=False,
                    ),
                }
            ),
            extractor=lambda x: [{"year": x["results"]}],
        )
        == 1
    )
    # Test multiple traces, preferring provided value
    assert (
        tool_trace_dependant_similarity(
            **tool_trace_dependant_similarity_kwargs,
            target_dataframe=pl.DataFrame(
                {
                    "tool_trace": json.dumps(
                        [
                            {
                                "tool_name": "search_holiday",
                                "arguments": {
                                    "holiday_name": "Christmas Day",
                                    "year": 2024,
                                },
                            },
                            {
                                "tool_name": "search_holiday",
                                "arguments": {
                                    "holiday_name": "Christmas Day",
                                },
                            },
                        ],
                        ensure_ascii=False,
                    ),
                }
            ),
            extractor=lambda x: [{"year": x["results"] + 1}],
        )
        == 1
    )


# ---------- Unicode-punctuation normalization ----------


def _score(df: pl.DataFrame) -> float:
    """Extract the single similarity score from a similarity-result frame."""
    return float(df["similarity"][0])


CURLY = "’"  # right single quotation mark (typographic apostrophe)


def test_normalize_text_for_matching_helper() -> None:
    from astra_tool_sandbox.common.utils import normalize_text_for_matching

    # Curly apostrophe -> ASCII
    assert normalize_text_for_matching("don’t") == "don't"
    # Curly double quotes
    assert normalize_text_for_matching("“hi”") == '"hi"'
    # En / em dash -> hyphen
    assert normalize_text_for_matching("a–b—c") == "a-b-c"
    # Ellipsis
    assert normalize_text_for_matching("wait…") == "wait..."
    # NBSP -> regular space
    assert normalize_text_for_matching("a b") == "a b"
    # NFKC fullwidth letter compatibility form
    assert normalize_text_for_matching("Ａ") == "A"
    # Non-string passes through
    assert normalize_text_for_matching(None) is None
    assert normalize_text_for_matching(42) == 42


@pytest.mark.parametrize(
    "column_value,expected_score",
    [
        (f"I don{CURLY}t have anything", 1.0),  # curly in agent output
        ("I don't have anything", 1.0),  # ASCII in agent output
        ("I dont have anything", 0.0),  # apostrophe removed — must NOT match
    ],
)
def test_column_str_contains_any_similarity_folds_curly_apostrophe(
    column_value: str, expected_score: float
) -> None:
    df = pl.DataFrame({"content": [column_value]})
    result = column_str_contains_any_similarity(
        dataframe=df, column_name="content", value=("don't have",)
    )
    assert _score(result) == expected_score


def test_column_str_contains_any_similarity_curly_expected_matches_ascii_column() -> (
    None
):
    df = pl.DataFrame({"content": ["I haven't seen it"]})
    # Expected value written with curly apostrophe should still match ASCII column
    result = column_str_contains_any_similarity(
        dataframe=df, column_name="content", value=(f"haven{CURLY}t",)
    )
    assert _score(result) == 1.0


def test_column_str_contains_all_similarity_folds_curly_apostrophe() -> None:
    df = pl.DataFrame({"content": [f"I don{CURLY}t have it and I won{CURLY}t"]})
    result = column_str_contains_all_similarity(
        dataframe=df,
        column_name="content",
        value=("don't", "won't"),
    )
    assert _score(result) == 1.0


def test_column_contains_similarity_folds_curly_apostrophe() -> None:
    df = pl.DataFrame({"content": [f"I don{CURLY}t have it"]})
    result = column_contains_similarity(
        dataframe=df, column_name="content", value="don't have"
    )
    assert _score(result) == 1.0


def test_column_contains_similarity_null_still_zero() -> None:
    df = pl.DataFrame({"content": [None]}, schema={"content": pl.Utf8})
    result = column_contains_similarity(
        dataframe=df, column_name="content", value="don't have"
    )
    assert _score(result) == 0.0


def test_column_contains_similarity_literal_dot_is_not_wildcard() -> None:
    """Value 'foo.bar' must match literally, not treat '.' as regex wildcard."""
    df = pl.DataFrame({"content": ["fooxbar"]})
    result = column_contains_similarity(
        dataframe=df, column_name="content", value="foo.bar"
    )
    assert _score(result) == 0.0


def test_column_contains_similarity_regex_metachars_do_not_crash() -> None:
    """Value with unbalanced regex metachars must not crash during compile."""
    df = pl.DataFrame({"content": ["some (hint) text"]})
    result = column_contains_similarity(
        dataframe=df, column_name="content", value="(hint)"
    )
    assert _score(result) == 1.0


def test_column_str_contains_any_similarity_null_cell_is_zero() -> None:
    df = pl.DataFrame({"content": [None]}, schema={"content": pl.Utf8})
    result = column_str_contains_any_similarity(
        dataframe=df, column_name="content", value=("anything",)
    )
    assert _score(result) == 0.0


def test_column_word_contains_any_similarity_null_cell_is_zero() -> None:
    df = pl.DataFrame({"content": [None]}, schema={"content": pl.Utf8})
    result = column_word_contains_any_similarity(
        dataframe=df, column_name="content", value=("anything",)
    )
    assert _score(result) == 0.0


def test_column_word_contains_any_similarity_folds_curly_apostrophe() -> None:
    df = pl.DataFrame({"content": [f"Sorry, I don{CURLY}t know"]})
    result = column_word_contains_any_similarity(
        dataframe=df, column_name="content", value=("don't",)
    )
    assert _score(result) == 1.0


def test_column_word_contains_similarity_folds_curly_apostrophe() -> None:
    df = pl.DataFrame({"content": [f"I haven{CURLY}t seen it"]})
    result = column_word_contains_similarity(
        dataframe=df, column_name="content", value="haven't"
    )
    assert _score(result) == 1.0


def test_column_exact_match_similarity_folds_curly_apostrophe() -> None:
    df = pl.DataFrame({"content": [f"don{CURLY}t"]})
    result = column_exact_match_similarity(
        dataframe=df, column_name="content", value="don't"
    )
    assert _score(result) == 1.0


def test_column_exact_match_similarity_still_distinguishes_missing_apostrophe() -> None:
    # Negative control: exact-match must not fold *away* the apostrophe.
    df = pl.DataFrame({"content": ["dont"]})
    result = column_exact_match_similarity(
        dataframe=df, column_name="content", value="don't"
    )
    assert _score(result) == 0.0


def test_column_rouge_l_similarity_folds_curly_apostrophe() -> None:
    df_curly = pl.DataFrame({"content": [f"I don{CURLY}t have it"]})
    df_ascii = pl.DataFrame({"content": ["I don't have it"]})
    result_curly = column_rouge_l_similarity(
        dataframe=df_curly, column_name="content", value="I don't have it"
    )
    result_ascii = column_rouge_l_similarity(
        dataframe=df_ascii, column_name="content", value="I don't have it"
    )
    # After folding, both should score identically (and be full match).
    assert _score(result_curly) == pytest.approx(_score(result_ascii))
    assert _score(result_curly) == pytest.approx(1.0)


def _trace(tool_name: str, result: Any) -> str:
    return json.dumps({"tool_name": tool_name, "arguments": {}, "result": result})


def test_retrieval_efficiency_single_search_hit() -> None:
    df = pl.DataFrame({"tool_trace": [[_trace("search_contacts", [{"id": 1}])]]})
    assert compute_retrieval_efficiency(df) == {
        "retrieval_get_all_count": 0,
        "retrieval_failed_search_count": 0,
        "retrieval_efficiency": 1.0,
    }


def test_retrieval_efficiency_failed_then_hit() -> None:
    df = pl.DataFrame(
        {
            "tool_trace": [
                [_trace("search_calendar_events", [])],  # empty result = failed query
                [_trace("search_calendar_events", [{"id": 1}])],
            ]
        }
    )
    r = compute_retrieval_efficiency(df)
    assert r["retrieval_get_all_count"] == 0
    assert r["retrieval_failed_search_count"] == 1
    assert r["retrieval_efficiency"] == pytest.approx(0.5)  # 1 - 1/2


def test_retrieval_efficiency_get_all_dumps() -> None:
    df = pl.DataFrame(
        {"tool_trace": [[_trace("get_all_contacts", [{"id": 1}, {"id": 2}])]]}
    )
    r = compute_retrieval_efficiency(df)
    assert r["retrieval_get_all_count"] == 1
    assert r["retrieval_efficiency"] == pytest.approx(0.0)  # 1 - 1/1


def test_retrieval_efficiency_no_retrieval_is_none() -> None:
    df = pl.DataFrame({"tool_trace": [[_trace("send_email", "ok")], None]})
    r = compute_retrieval_efficiency(df)
    assert r["retrieval_efficiency"] is None  # N/A — no retrieval calls
    assert r["retrieval_get_all_count"] == 0
    assert r["retrieval_failed_search_count"] == 0


def _answer_milestone() -> Milestone:
    """A milestone tagged ``response_generation``: its constraint targets the user."""
    return Milestone(
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


def test_completion_score_is_the_mean_when_no_minefield_fires() -> None:
    score = compute_milestone_completion_score(
        [_answer_milestone(), _answer_milestone()],
        OrderedDict({0: (5, 1.0), 1: (6, 0.0)}),
        minefield_similarity=0,
    )
    assert score == 0.5


def test_completion_score_is_nullified_by_a_triggered_minefield() -> None:
    """The veto EvaluationResult.similarity applies: forbidden action, no credit."""
    score = compute_milestone_completion_score(
        [_answer_milestone(), _answer_milestone()],
        OrderedDict({0: (5, 1.0), 1: (6, 1.0)}),
        minefield_similarity=1.0,
    )
    assert score == 0.0


def test_completion_score_stays_none_when_nothing_is_tagged() -> None:
    """None is N/A and stays out of the aggregates; a minefield must not make it a 0."""
    retrieval_only = Milestone(
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
            )
        ]
    )
    assert (
        compute_milestone_completion_score(
            [retrieval_only], OrderedDict({0: (5, 1.0)}), minefield_similarity=1.0
        )
        is None
    )


def test_completion_score_reads_json_string_milestone_indices() -> None:
    """Resumed runs hand back a mapping whose keys went through JSON as strings."""
    assert (
        compute_milestone_completion_score(
            [_answer_milestone()], OrderedDict({"0": (5, 1.0)})
        )
        == 1.0
    )


def test_user_simulator_calls_are_not_charged_to_the_agent() -> None:
    """The allow list is shared between roles — the simulator calls from it too. Only
    the agent's own requests may count."""
    from astra_tool_sandbox.common.evaluation import compute_failure_mode_counts
    from astra_tool_sandbox.common.execution_context import RoleType

    df = pl.DataFrame(
        [
            {
                "sender": RoleType.USER,
                "recipient": RoleType.EXECUTION_ENVIRONMENT,
                "content": "end_conversation()",
                "openai_function_name": "something_odd",
                "tool_call_exception": None,
            }
        ]
    )
    counts = compute_failure_mode_counts(df, tool_allow_list=["end_conversation"])
    assert counts["hallucinated_tool_call_count"] == 0


def test_milestone_tagger_writes_missing_file(tmp_path: Path) -> None:
    milestone_tagger([], tmp_path)
    assert (tmp_path / "milestone_tags.json").read_text() == "{}\n"


def test_milestone_tagger_leaves_up_to_date_file_untouched(tmp_path: Path) -> None:
    # Scenario loading calls this on every run, including from a read-only install.
    output_path = tmp_path / "milestone_tags.json"
    output_path.write_text("{}\n")
    output_path.chmod(0o444)
    tmp_path.chmod(0o555)
    try:
        milestone_tagger([], tmp_path)
    finally:
        tmp_path.chmod(0o755)
        output_path.chmod(0o644)
    assert output_path.read_text() == "{}\n"


def test_milestone_tagger_warns_instead_of_raising_when_unwritable(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    tmp_path.chmod(0o555)
    try:
        with caplog.at_level(logging.WARNING):
            milestone_tagger([], tmp_path)
    finally:
        tmp_path.chmod(0o755)
    assert not (tmp_path / "milestone_tags.json").exists()
    assert "Could not write" in caplog.text
