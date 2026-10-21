# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
import functools
import heapq
import itertools
import json
import math
import os
import re
import string
import time
from collections import OrderedDict
from copy import deepcopy
from datetime import datetime, timedelta
from logging import getLogger
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

import networkx
import numpy as np
import openai
import polars as pl
from attrs import Factory, define, field
from dotenv import load_dotenv
from polars.exceptions import SchemaError
from rouge_score import rouge_scorer  # type: ignore
from scipy.optimize import linear_sum_assignment  # type: ignore
from typing_extensions import Protocol

from astra_tool_sandbox.common.evaluation_utils import (
    find_entity_in_execution_context_by_id,
    format_flat_entities_for_prompt,
)
from astra_tool_sandbox.common.execution_context import (
    DatabaseNamespace,
    ExecutionContext,
    RoleType,
)
from astra_tool_sandbox.common.tool_trace_extractors import ToolTraceExtractorType
from astra_tool_sandbox.common.utils import (
    NOT_GIVEN,
    all_logging_disabled,
    flatten_list,
    is_close,
    is_phone_number,
    normalize_phone_number,
    normalize_text_for_matching,
)

LOGGER = getLogger(__name__)


class ColumnSimilarityMeasureType(Protocol):
    """Callable type def for column similarity measure functions

    Each similarity measure takes a dataframe, column to calculate similarity on and value,
    to return a Dataframe representing similarity between each row in the dataframe and the value
    Similarities are [0, 1] real values.
    """

    def __call__(
        self,
        dataframe: pl.DataFrame,
        column_name: str,
        value: Any,
        atol_dict: Optional[dict[str, float]] = None,
    ) -> pl.DataFrame: ...


def column_is_not_null(
    dataframe: pl.DataFrame,
    column_name: str,
    value: Any,
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    """A 0/1 similarity indicating whether the column value is NOT null
    Useful for identifying whether the agents attach a file to an email.

    Args:
        dataframe:      DataFrame to evaluate
        column_name:    Name of the column to check for null values

    Returns:
        A DataFrame with a similarity score: 1 if the column value is not null, 0 if it is null
    """
    return dataframe.select(
        pl.col(column_name).is_not_null().cast(pl.Float32).alias("similarity")
    )


def column_exact_match_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: Any,
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    """A 0/1 similarity based on exact match with phone number normalization.

    Args:
        dataframe:      Dataframe to calculate similarity on
        column_name:    Column name to compare
        value:          Value the column should compare against
        atol_dict:      Absolute tolerance for each argument

    Returns:
        A Dataframe containing similarity score. 0 for no match, 1 for match
    """
    if value is not None:
        # Normalize phone numbers if detected
        if isinstance(value, str) and is_phone_number(value):
            normalized_value = normalize_phone_number(value)
            return dataframe.select(
                pl.when(pl.col(column_name).is_not_null())
                .then(
                    pl.col(column_name)
                    .map_elements(
                        lambda x: normalize_phone_number(x)
                        if isinstance(x, str) and is_phone_number(x)
                        else x,
                        return_dtype=pl.Utf8,
                    )
                    .eq(normalized_value)
                )
                .otherwise(False)
                .cast(pl.Float32)
                .alias("similarity")
            )
        elif isinstance(value, str):
            # Fold typographic Unicode punctuation on both sides so straight
            # vs curly apostrophes / quotes / dashes / ellipsis do not miss.
            normalized_value = normalize_text_for_matching(value)
            return dataframe.select(
                pl.when(pl.col(column_name).is_not_null())
                .then(
                    pl.col(column_name)
                    .map_elements(
                        normalize_text_for_matching,
                        return_dtype=pl.Utf8,
                    )
                    .eq(normalized_value)
                )
                .otherwise(False)
                .cast(pl.Float32)
                .alias("similarity")
            )
        else:
            return dataframe.select(
                pl.col(column_name).eq(value).cast(pl.Float32).alias("similarity")
            )
    else:
        return dataframe.select(
            pl.col(column_name).is_null().cast(pl.Float32).alias("similarity")
        )


def column_list_match_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: list[Any],
    exact: bool = True,
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    """
    A 0/1 similarity based on list match with phone number normalization:
        - exact=True: require exact match (order-insensitive)
        - exact=False: require that `value` is a subset of the column list

    Args:
        dataframe:      DataFrame to calculate similarity on
        column_name:    Name of list-valued column
        value:          List to match against
        exact:          Whether to require exact match (True) or subset match (False)
        atol_dict:      Unused

    Returns:
        A DataFrame with column 'similarity': 1.0 or 0.0 per row
    """
    if value is not None:
        # Normalize phone numbers in the value list if detected
        normalized_value = []
        for item in value:
            if isinstance(item, str) and is_phone_number(item):
                normalized_value.append(normalize_phone_number(item))
            else:
                normalized_value.append(item)

        value_set = set(normalized_value)
        value_sorted = sorted(normalized_value)

        def match_fn(x: tuple[Optional[list[Any]]]) -> float:
            col_list = x[0] or []
            # Normalize phone numbers in the column list if detected
            normalized_col_list = []
            for item in col_list:
                if isinstance(item, str) and is_phone_number(item):
                    normalized_col_list.append(normalize_phone_number(item))
                else:
                    normalized_col_list.append(item)

            if exact:
                return float(sorted(normalized_col_list) == value_sorted)
            else:
                return float(value_set.issubset(set(normalized_col_list)))

        return (
            dataframe.select(pl.col(column_name))
            .map_rows(function=match_fn, return_dtype=pl.Float64)
            .select(pl.col("map").cast(pl.Float32).alias("similarity"))
        )
    else:
        return dataframe.select(
            pl.col(column_name).is_null().cast(pl.Float32).alias("similarity")
        )


def column_list_exact_match_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: Any,
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    return column_list_match_similarity(
        dataframe=dataframe,
        column_name=column_name,
        value=value,
        exact=True,
        atol_dict=atol_dict,
    )


def column_list_subset_match_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: Any,
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    return column_list_match_similarity(
        dataframe=dataframe,
        column_name=column_name,
        value=value,
        exact=False,
        atol_dict=atol_dict,
    )


# def column_list_exact_match_similarity(
#     dataframe: pl.DataFrame,
#     column_name: str,
#     value: Any,
#     atol_dict: Optional[dict[str, float]] = None,
# ) -> pl.DataFrame:
#     """A 0/1 similarity based on exact match for List fields.

#     Args:
#         dataframe:      Dataframe to calculate similarity on
#         column_name:    Column name to compare, should be List[Any]
#         value:          List value to match against
#         atol_dict:      Unused

#     Returns:
#         A Dataframe containing similarity score. 0 for no match, 1 for match
#     """
#     if value is not None:
#         # Enable different order
#         def match_list(x: tuple[Optional[list[Any]]]) -> float:
#             return float(sorted(x[0] or []) == sorted(value))

#         return (
#             dataframe.select(pl.col(column_name))
#             .map_rows(function=match_list, return_dtype=pl.Float32)
#             .select(pl.col("map").alias("similarity"))
#         )
#     else:
#         return dataframe.select(
#             pl.col(column_name).is_null().cast(pl.Float32).alias("similarity")
#         )


def column_close_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: Any,
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    """A 0/1 similarity based on how close values are.

    Only works on int / float, and requires atol_dict.

    Args:
        dataframe:      Dataframe to calculate similarity on
        column_name:    Column name to compare
        value:          Value the column should compare against
        atol_dict:      Absolute tolerance for each argument

    Returns:
        A Dataframe containing similarity score. 0 for no match, 1 for match
    """
    assert isinstance(value, (int, float)) and atol_dict is not None

    def check_close(x: tuple[Optional[str]]) -> float:
        """UDF checking if x [0] is close to value

        Args:
            x:  single value tuple containing a tool trace

        Returns:
            0 / 1 match score
        """
        if is_close(value=value, reference=x[0], atol=atol_dict.get(column_name, None)):
            return 1
        return 0

    return (
        dataframe.select(pl.col(column_name))
        .map_rows(function=check_close, return_dtype=pl.Float64)
        .select(pl.col("map").cast(pl.Float32).alias("similarity"))
    )


def column_one_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: Any,
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    """A similarity that always returns 1 as similarity score

    Args:
        dataframe:      Dataframe to calculate similarity on
        column_name:    Column name to compare
        value:          Value the column should compare against
        atol_dict:      Absolute tolerance for each argument

    Returns:
        A Dataframe containing similarity score. 0 for no match, 1 for match
    """
    return dataframe.with_columns(pl.lit(1.0).alias("similarity")).select("similarity")


def column_str_contains_any_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: tuple[str, ...],
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    """
    0/1 similarity: Checks if any string in `value` tuple appears as a substring in the target column.

    Args:
        dataframe:      DataFrame to evaluate
        column_name:    Name of the string column to search in
        value:          A tuple of acceptable substrings (e.g., ("7:30", "19:30"))
        atol_dict:      Unused

    Returns:
        A DataFrame with a single column "similarity" containing 1.0 if matched, else 0.0
    """
    if value is not None:
        normalized_values = tuple(normalize_text_for_matching(v).lower() for v in value)

        def contains_any(x: tuple[str]) -> float:
            text = normalize_text_for_matching(x[0] or "").lower()
            return float(any(v in text for v in normalized_values))

        return (
            dataframe.select(pl.col(column_name))
            .map_rows(function=contains_any, return_dtype=pl.Float64)
            .select(pl.col("map").cast(pl.Float32).alias("similarity"))
        )
    else:
        return dataframe.select(
            pl.col(column_name).is_null().cast(pl.Float32).alias("similarity")
        )


def column_word_contains_any_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: tuple[str, ...],
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    """
    0/1 similarity: Checks if any whole word/phrase in `value` tuple appears in the target column.

    Uses word boundaries for matching. Punctuation at start/end of search values is stripped,
    but internal punctuation is preserved (e.g., "don't", "well-done").

    Args:
        dataframe:      DataFrame to evaluate
        column_name:    Name of the string column to search in
        value:          A tuple of acceptable words/phrases (e.g., ("no", "yes", "maybe"))
        atol_dict:      Unused

    Returns:
        A DataFrame with a single column "similarity" containing 1.0 if matched, else 0.0

    Examples:
        - value=("no", "yes") matches "no", "yes", "No!" but NOT "not", "eyes"
        - value=("don't", "can't") matches "don't know", "I can't" with apostrophes preserved
    """
    if value is not None:

        def word_contains_any(x: tuple[str]) -> float:
            text = normalize_text_for_matching(x[0] or "").lower()
            for v in value:
                # Normalize first so curly apostrophes fold to ASCII before
                # we strip peripheral punctuation; preserve internal.
                clean_value = (
                    normalize_text_for_matching(v).lower().strip(string.punctuation)
                )
                # Create word boundary pattern
                pattern = r"\b" + re.escape(clean_value) + r"\b"
                if re.search(pattern, text):
                    return 1.0
            return 0.0

        return (
            dataframe.select(pl.col(column_name))
            .map_rows(function=word_contains_any, return_dtype=pl.Float64)
            .select(pl.col("map").cast(pl.Float32).alias("similarity"))
        )
    else:
        return dataframe.select(
            pl.col(column_name).is_null().cast(pl.Float32).alias("similarity")
        )


def column_str_contains_all_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: tuple[str, ...],
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    """
    0/1 similarity: Checks if ALL strings in `value` appear as substrings in the target column (case-insensitive).
    """
    if value:
        normalized_values = tuple(normalize_text_for_matching(v).lower() for v in value)

        def contains_all(x: tuple[str]) -> float:
            text = normalize_text_for_matching(x[0] or "").lower()
            return float(all(v in text for v in normalized_values))

        return (
            dataframe.select(pl.col(column_name))
            .map_rows(function=contains_all, return_dtype=pl.Float64)
            .select(pl.col("map").cast(pl.Float32).alias("similarity"))
        )
    else:
        return dataframe.select(pl.lit(0.0).cast(pl.Float32).alias("similarity"))


def column_list_tuple_subset_contains_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: list[tuple[Any, ...]],
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    """
    0/1 similarity with phone number normalization: For each tuple in `value`, at least one element must appear in the column list.
    The column list must also not contain any extra values outside those in the union of all tuples.

    Args:
        dataframe:      DataFrame to evaluate
        column_name:    Column with List[Any] values
        value:          List of tuples — at least one from each tuple must appear
        atol_dict:      Unused

    Returns:
        A DataFrame with a "similarity" column: 1.0 if match, 0.0 if not
    """
    """
    0/1 similarity: For each tuple in `value`, at least one element must appear in the column list.
    Extra items in the column are allowed.
    """
    if value is not None:
        # Normalize phone numbers in the value tuples if detected
        normalized_value = []
        for group in value:
            normalized_group = []
            for item in group:
                if isinstance(item, str) and is_phone_number(item):
                    normalized_group.append(normalize_phone_number(item))
                else:
                    normalized_group.append(item)
            normalized_value.append(tuple(normalized_group))

        def match_fn(x: tuple[Optional[list[Any]]]) -> float:
            col_list = x[0] or []
            # Normalize phone numbers in the column list if detected
            normalized_col_list = []
            for item in col_list:
                if isinstance(item, str) and is_phone_number(item):
                    normalized_col_list.append(normalize_phone_number(item))
                else:
                    normalized_col_list.append(item)

            col_set = set(normalized_col_list)

            all_groups_satisfied = all(
                any(item in col_set for item in group) for group in normalized_value
            )

            return float(all_groups_satisfied)

        return (
            dataframe.select(pl.col(column_name))
            .map_rows(function=match_fn, return_dtype=pl.Float64)
            .select(pl.col("map").cast(pl.Float32).alias("similarity"))
        )
    else:
        return dataframe.select(
            pl.col(column_name).is_null().cast(pl.Float32).alias("similarity")
        )


def column_list_tuple_contains_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: list[tuple[Any, ...]],
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    """
    0/1 similarity with phone number normalization: For each tuple in `value`, at least one element must appear in the column list.
    The column list must also contain only values from the union of all tuples.
    """
    if value is not None:
        # Normalize phone numbers in the value tuples if detected
        normalized_value = []
        for group in value:
            normalized_group = []
            for item in group:
                if isinstance(item, str) and is_phone_number(item):
                    normalized_group.append(normalize_phone_number(item))
                else:
                    normalized_group.append(item)
            normalized_value.append(tuple(normalized_group))

        # Create valid items set from normalized values
        valid_items = set(item for group in normalized_value for item in group)

        def match_fn(x: tuple[Optional[list[Any]]]) -> float:
            col_list = x[0] or []
            # Normalize phone numbers in the column list if detected
            normalized_col_list = []
            for item in col_list:
                if isinstance(item, str) and is_phone_number(item):
                    normalized_col_list.append(normalize_phone_number(item))
                else:
                    normalized_col_list.append(item)

            col_set = set(normalized_col_list)

            all_groups_satisfied = all(
                any(item in col_set for item in group) for group in normalized_value
            )

            only_valid_items = col_set.issubset(valid_items)

            return float(all_groups_satisfied and only_valid_items)

        return (
            dataframe.select(pl.col(column_name))
            .map_rows(function=match_fn, return_dtype=pl.Float64)
            .select(pl.col("map").cast(pl.Float32).alias("similarity"))
        )
    else:
        return dataframe.select(
            pl.col(column_name).is_null().cast(pl.Float32).alias("similarity")
        )


def _require_str_value(measure_name: str, column_name: str, value: Any) -> None:
    """Reject a non-string target value for a string-only containment measure.

    `normalize_text_for_matching` deliberately passes non-strings through
    unchanged, so a list/tuple target would otherwise reach `.lower()` and raise
    an opaque `AttributeError` from deep inside grading. A milestone that lists
    alternative phrasings wants `column_str_contains_any_similarity` instead.
    """
    if not isinstance(value, str):
        raise TypeError(
            f"{measure_name} requires a string value but got "
            f"{type(value).__name__} for column {column_name!r}: {value!r}. "
            "For a list/tuple of acceptable phrasings use "
            "column_str_contains_any_similarity (any-of) or "
            "column_str_contains_all_similarity (all-of); for a list-valued "
            "column use column_list_exact_match_similarity."
        )


def column_contains_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: Any,
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    """A 0/1 similarity whether the value is contained in column value string

    Args:
        dataframe:      Dataframe to calculate similarity on
        column_name:    Column name to compare, must contain string
        value:          Value the column should compare against, must be string value
        atol_dict:      Absolute tolerance for each argument

    Returns:
        A Dataframe containing similarity score. 0 if the column value do not contain target value, 1 if it does
    """
    """A 0/1 similarity whether the value is contained in column value string (case-insensitive for strings only)."""
    if value is None:
        raise ValueError("Value must be provided for containment check.")
    _require_str_value("column_contains_similarity", column_name, value)

    normalized_value = normalize_text_for_matching(value).lower()
    normalized_col = (
        pl.col(column_name)
        .cast(pl.Utf8, strict=False)
        .map_elements(normalize_text_for_matching, return_dtype=pl.Utf8)
        .str.to_lowercase()
    )

    return dataframe.select(
        normalized_col.str.contains(normalized_value, literal=True)
        .fill_null(False)  # nulls -> no match
        .cast(pl.Float32)
        .alias("similarity")
    )


def _parse_iso_datetime(value: Any) -> Optional[datetime]:
    """Parse an ISO 8601 string into a datetime, returning None when it is not parseable."""
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def column_datetime_window_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: Any,
    atol_dict: Optional[dict[str, float]] = None,
    max_minutes: float = 30.0,
) -> pl.DataFrame:
    """A 0/1 similarity whether the column datetime falls within [value, value + max_minutes].

    Creation timestamps come from the agent, not from the sandbox: every create / modify tool
    takes ``creation_datetime_iso`` as a required argument and there is no clock to default it
    from. Grading one with ``column_contains_similarity`` therefore tests timestamp formatting
    to the minute, which fails any agent that spends sandbox time on lookups before acting.
    This measure accepts the window legitimate behaviour occupies while still rejecting
    backdating, which is otherwise ungraded.

    Args:
        dataframe:      Dataframe to calculate similarity on
        column_name:    Column name to compare, must contain an ISO 8601 datetime string
        value:          Expected datetime (the scenario's own reference time), ISO 8601 string
        atol_dict:      Absolute tolerance for each argument. Unused by this measure
        max_minutes:    Size of the accepted window after ``value``, in minutes

    Returns:
        A Dataframe containing similarity score. 1 when the column datetime lies within
        [value, value + max_minutes], 0 otherwise -- including when the column value is null
        or cannot be parsed, since a malformed agent timestamp must score 0 rather than abort
        the scenario.

    Raises:
        ValueError: When ``value`` is not a parseable ISO 8601 datetime. That is an authoring
                    error in the scenario rather than agent behaviour, so it is surfaced loudly
                    instead of silently failing every trajectory.
    """
    _require_str_value("column_datetime_window_similarity", column_name, value)
    lower_bound = _parse_iso_datetime(value)
    if lower_bound is None:
        raise ValueError(
            "column_datetime_window_similarity expects an ISO 8601 datetime target for "
            f"column {column_name!r}, got {value!r}"
        )
    upper_bound = lower_bound + timedelta(minutes=max_minutes)

    def within_window(observed: Optional[str]) -> float:
        parsed = _parse_iso_datetime(observed)
        if parsed is None:
            return 0.0
        # Align awareness before comparing so a naive timestamp on either side does not raise.
        # When both are aware the comparison is on absolute instants, so the same moment
        # rendered in a different UTC offset still matches.
        lower, upper = lower_bound, upper_bound
        if parsed.tzinfo is None and lower.tzinfo is not None:
            parsed = parsed.replace(tzinfo=lower.tzinfo)
        elif parsed.tzinfo is not None and lower.tzinfo is None:
            lower = lower.replace(tzinfo=parsed.tzinfo)
            upper = upper.replace(tzinfo=parsed.tzinfo)
        return float(lower <= parsed <= upper)

    return dataframe.select(
        pl.col(column_name)
        .cast(pl.Utf8, strict=False)
        .map_elements(within_window, return_dtype=pl.Float32)
        .fill_null(0.0)  # nulls -> no match
        .alias("similarity")
    )


def column_word_contains_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: Any,
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    """A 0/1 similarity whether the whole word is contained in column value string (case-insensitive).

    Punctuation at the start/end of the search value is stripped, but internal punctuation is preserved.
    Uses word boundaries to ensure whole-word/phrase matching.
    For substring matching, use column_contains_similarity instead.

    Args:
        dataframe:      Dataframe to calculate similarity on
        column_name:    Column name to compare, must contain string
        value:          Value/word/phrase the column should compare against, must be string value
        atol_dict:      Absolute tolerance for each argument

    Returns:
        A Dataframe containing similarity score. 0 if no match, 1 if the whole word/phrase is contained

    Examples:
        - "No." matches "no", "No", "no.", "No!" (whole word, punctuation stripped)
        - "not" does NOT match "no" (different whole word)
        - "test" does NOT match "testing" or "contest" (subword, not whole word)
        - "don't" matches "don't", "Don't!", "don't." (internal apostrophe preserved)
        - "test case" matches "test case", "Test Case." (whole phrase)
    """
    if value is None:
        raise ValueError("Value must be provided for containment check.")
    _require_str_value("column_word_contains_similarity", column_name, value)

    # Normalize first so curly apostrophes fold to ASCII before we strip
    # peripheral punctuation; preserve internal punctuation.
    clean_value = normalize_text_for_matching(value).lower().strip(string.punctuation)
    pattern = r"\b" + re.escape(clean_value) + r"\b"

    normalized_col = (
        pl.col(column_name)
        .cast(pl.Utf8, strict=False)
        .map_elements(normalize_text_for_matching, return_dtype=pl.Utf8)
        .str.to_lowercase()
    )

    return dataframe.select(
        normalized_col.str.contains(pattern)
        .fill_null(False)  # nulls -> no match
        .cast(pl.Float32)
        .alias("similarity")
    )


def column_tool_trace_exact_match_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: Any,
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    """A 0/1 similarity whether a tool trace matches a provided trace.

    Function name and argument in provided trace is always matched. Arguments not provided are ignored

    Provided trace can be a list of possible traces, in which case a match is found
    if any of the provided traces matches.

    Args:
        dataframe:      Dataframe to calculate similarity on
        column_name:    Column name to compare, must contain string
        value:          Json dumped 1 or a list of tool traces.
        atol_dict:      Absolute tolerance for each argument

    Returns:
        A Dataframe containing similarity score. 0 if the column value do not contain target value, 1 if it does
    """
    trace: Union[dict[str, Any], list[dict[str, Any]]] = json.loads(value)
    # Normalize into a list of possible golden traces
    golden_traces: list[dict[str, Any]] = (
        [trace] if not isinstance(trace, Sequence) else list(trace)
    )

    def match_trace(x: tuple[Optional[str]]) -> float:
        """UDF calculating trace matching score

        Args:
            x:  single value tuple containing a tool trace

        Returns:
            0 / 1 match score
        """
        if x[0] is None:
            return 0.0
        # If any trace matches any golden trace, return 1
        for golden_trace in golden_traces:
            for tool_trace_json in x[0]:
                tool_trace = json.loads(tool_trace_json)
                if tool_trace["tool_name"] == golden_trace["tool_name"] and all(
                    is_close(
                        tool_trace["arguments"].get(argument_name, NOT_GIVEN),
                        golden_trace["arguments"][argument_name],
                        atol=atol_dict.get(argument_name, None)
                        if atol_dict is not None
                        else None,
                    )
                    for argument_name in golden_trace["arguments"]
                ):
                    return 1.0
        return 0.0

    return (
        dataframe.select(pl.col(column_name))
        .map_rows(function=match_trace, return_dtype=pl.Float64)
        .select(pl.col("map").cast(pl.Float32).alias("similarity"))
    )


def column_tool_trace_partial_arguments_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: Any,
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    """A 0/1 similarity whether a tool trace partially matches a provided trace.

    Function name must match. Arguments in provided trace must match, other arguments ignored.

    Args:
        dataframe:      Dataframe to calculate similarity on
        column_name:    Column name to compare, must contain string
        value:          Json dumped 1 or a list of tool traces.
        atol_dict:      Absolute tolerance for each argument

    Returns:
        A Dataframe containing similarity score. 0 if no match, 1 if match
    """
    trace = json.loads(value)
    golden_traces = [trace] if not isinstance(trace, Sequence) else list(trace)

    def match_partial_trace(x: tuple[Optional[list[str]]]) -> float:
        raw = x[0]
        # print(f">>> match_partial_trace got raw={raw!r}")

        if not raw:
            return 0.0

        # normalize: support both list[str] and str
        if isinstance(raw, str):
            tool_trace_list = [raw]
        elif isinstance(raw, list):
            tool_trace_list = raw
        else:
            return 0.0  # unexpected type
        # print(f"tool_trace_list raw: {raw} (type: {type(raw)})")

        for tool_trace_json in tool_trace_list:
            try:
                # print(f"    Trying to load: {tool_trace_json}")
                tool_trace = json.loads(tool_trace_json)
            except Exception as e:
                # print(f"    ❌ Failed to load JSON: {e}")
                continue
            for golden_trace in golden_traces:
                if tool_trace.get("tool_name") != golden_trace.get("tool_name"):
                    continue  # <- critical: skip if tool_name doesn't match

                tool_arguments = tool_trace.get("arguments", {})
                golden_arguments = golden_trace.get("arguments", {})

                # print("--- Matching trace ---")
                # print("Actual tool name:", tool_trace.get("tool_name"))
                # print("Expected tool name:", golden_trace.get("tool_name"))
                # print("Actual arguments:", tool_arguments)
                # print("Expected arguments:", golden_arguments)

                # for arg_name, expected_value in golden_arguments.items():
                #     actual_value = tool_arguments.get(arg_name, NOT_GIVEN)
                #     print(
                #         f"> Comparing {arg_name}: actual = {actual_value!r}, expected = {expected_value!r}"
                #     )
                #     print(f"> Match result: {is_close(actual_value, expected_value)}")

                if all(
                    is_close(
                        tool_arguments.get(arg_name, NOT_GIVEN),
                        expected_value,
                        atol=atol_dict.get(arg_name, None) if atol_dict else None,
                    )
                    for arg_name, expected_value in golden_arguments.items()
                ):
                    # print("All matched!")

                    return 1.0
        return 0.0

    similarity_series = dataframe.select(pl.col(column_name)).map_rows(
        function=match_partial_trace, return_dtype=pl.Float64
    )

    result_df = pl.DataFrame(
        {"similarity": similarity_series.to_series().cast(pl.Float32)}
    )
    # print(f"Final returned similarity: {result_df}")
    return result_df


def column_rouge_l_similarity(
    dataframe: pl.DataFrame,
    column_name: str,
    value: Any,
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    """Similarity defined by ROUGE score. Only applicable for string values

    Args:
        dataframe:      Dataframe to calculate similarity on
        column_name:    Column name to compare, must contain string
        value:          Value the column should compare against, must be string value
        atol_dict:      Absolute tolerance for each argument

    Returns:
        A Dataframe containing similarity score.
    """
    with all_logging_disabled():
        scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
        # Fold typographic punctuation so tokenization treats curly and
        # straight apostrophes / quotes / dashes as the same token.
        normalized_value = normalize_text_for_matching(value)

        def rouge_l_score(x: tuple[str]) -> float:
            """UDF calculating rouge L

            Args:
                x:  single value tuple containing the column in question

            Returns:
                float rouge L f score
            """
            return cast(
                float,
                scorer.score(
                    target=normalized_value,
                    prediction=normalize_text_for_matching(x[0]),
                )["rougeL"].fmeasure,
            )

        return (
            dataframe.select(pl.col(column_name))
            .map_rows(function=rouge_l_score, return_dtype=pl.Float64)
            .select(pl.col("map").cast(pl.Float32).alias("similarity"))
        )


class SnapshotSimilarityMeasureType(Protocol):
    """Callable type def for snapshot similarity measure functions

    Each similarity measure takes a snapshot, target dataframe, column similarities and reference snapshot
    to return a float representing similarity between snapshot and other specified constraints
    Similarities are [0, 1] real values.
    """

    def __call__(
        self,
        snapshot: pl.DataFrame,
        target_dataframe: Optional[pl.DataFrame] = None,
        column_similarities: Optional[Dict[str, ColumnSimilarityMeasureType]] = None,
        reference_snapshot: Optional[pl.DataFrame] = None,
        **kwargs: Union[str, ToolTraceExtractorType],
    ) -> float: ...


def snapshot_similarity(
    snapshot: pl.DataFrame,
    target_dataframe: Optional[pl.DataFrame] = None,
    column_similarities: Optional[Dict[str, ColumnSimilarityMeasureType]] = None,
    reference_snapshot: Optional[pl.DataFrame] = None,
    **kwargs: Union[str, ToolTraceExtractorType],
) -> float:
    """Measures the similarity between each database snapshot and a target_dataframe.

        1. If the number of rows, or column names doesn't match, similarity is always 0
        2. Within each snapshot, calculate a similarity between each row in the target and each row in the snapshot
            2.1 Row-wise similarity is determined by the geo mean of column similarities
            2.2 Only columns provided in target_dataframe was considered
        3. Find a 1 to 1 mapping between snapshot rows and target rows that maximizes geo mean of row similarities.
            Said geo mean is the snapshot similarity

    Args:
        snapshot:                   The dataframe snapshot to calculate similarity for
        target_dataframe:           The dataframe to calculate similarity with
        column_similarities:        A dictionary of column name to column-wise similarity measure
        reference_snapshot:         Not utilized by this similarity

    Returns:
        A [0, 1] similarity score between target_dataframe and snapshot
    """
    assert target_dataframe is not None and column_similarities is not None
    # print(f"Snapshot: {snapshot}")
    # print(f"Target Dataframe: {target_dataframe}")

    # Check for row number and columns
    if snapshot.select(pl.len())["len"][0] != target_dataframe.select(pl.len())["len"][
        0
    ] or set(target_dataframe.columns) - set(snapshot.columns):
        # print(f"Snapshot: {snapshot}")
        # print(f"Target Dataframe: {target_dataframe}")

        return 0.0
    # Create N * N cost matrix (- log similarity). This ensures when assignment cost is minimized
    # through hungarian algorithm, row-wise geo metric mean of similarity is maximized
    cost_matrix: list[np.ndarray[Any, np.dtype[np.float64]]] = []
    for row in target_dataframe.to_dicts():
        # - log similarity and column-wise geo mean
        column_cost_df = pl.concat(
            [
                column_similarities[column_name](
                    dataframe=snapshot,
                    column_name=column_name,
                    value=value,
                ).select(-pl.col("similarity").log().alias(f"similarity_{i}"))
                for i, (column_name, value) in enumerate(row.items())
            ],
            how="horizontal",
        )
        cost_matrix.append(
            column_cost_df.select(
                pl.mean_horizontal(*column_cost_df.columns).alias("mean")
            )["mean"].to_numpy()
        )
    numpy_cost_matrix = np.stack(cost_matrix, axis=0)
    try:
        # Solve for assignment that minimizes cost matrix
        row_ind, col_ind = linear_sum_assignment(numpy_cost_matrix)
    except ValueError:
        # cost matrix is infeasible (always results in inf). Return 0
        return 0
    # Calculate similarity
    return cast(float, np.exp(-numpy_cost_matrix[row_ind, col_ind].mean()).tolist())


def addition_similarity(
    snapshot: pl.DataFrame,
    target_dataframe: Optional[pl.DataFrame] = None,
    column_similarities: Optional[Dict[str, ColumnSimilarityMeasureType]] = None,
    reference_snapshot: Optional[pl.DataFrame] = None,
    **kwargs: Union[str, ToolTraceExtractorType],
) -> float:
    """Measures the similarity between each database snapshot and a target_dataframe, if the snapshot is supposed to
    be derived from adding target_dataframe onto reference_snapshot

        1. If snapshot does not fully contain reference_snapshot, similarity is always 0
        2. If it does, the anti join of the two is compared against target_dataframe using snapshot_similarity

    Args:
        snapshot:                   The dataframe snapshot to calculate similarity for
        target_dataframe:           The dataframe to calculate similarity with
        column_similarities:        A dictionary of column name to column-wise similarity measure
        reference_snapshot:         When similarity is 1,
                                    snapshot should be the result of adding target_dataframe into reference_snapshot

    Returns:
        A [0, 1] similarity score between target_dataframe and snapshot
    """
    assert reference_snapshot is not None
    assert (
        target_dataframe is not None
        # and column_similarities is not None
        # and reference_snapshot is not None
    )
    assert column_similarities is not None

    # print(f"Snapshot -------------")
    # print(f"Reference_snapshot: {reference_snapshot}")
    # print(f"snapshot: {snapshot}")

    # Drop sandbox_message_index
    # Fill null with zero to prevent join failure
    snapshot = snapshot.drop("sandbox_message_index", strict=False).fill_null(0)

    # reference_snapshot = reference_snapshot.drop("sandbox_message_index").fill_null(0)
    target_dataframe = target_dataframe.fill_null(strategy="zero")
    target_dataframe = target_dataframe.fill_null(0)

    # # # NOTE: Debug purposes

    id_columns = [
        col
        for col in snapshot.columns
        if (
            "id" in col and snapshot.schema[col] == pl.Utf8
        )  # or ("datetime_iso" in col)
    ]
    # Joining on an empty key list makes polars panic (arg_sort_multiple over 0
    # keys). When the snapshot has no id column to identify entities by, fall back
    # to matching on the columns shared by both frames. Domain-DB snapshots always
    # carry an id column in practice, so this only guards the id-less case.
    join_columns = id_columns or [
        col for col in snapshot.columns if col in reference_snapshot.columns
    ]
    added_rows = snapshot.join(reference_snapshot, on=join_columns, how="anti")

    # print(f"ADDED rows: {added_rows.select(target_dataframe.columns)}")
    # print(f"Target Dataframe: {target_dataframe}")

    reference_len = reference_snapshot.select(pl.len()).item()
    if reference_len > 0:
        snapshot_overlap_len = (
            snapshot.join(reference_snapshot, on=join_columns, how="inner")
            .select(pl.len())
            .item()
        )
        if snapshot_overlap_len != reference_len:
            return 0
    else:
        # print("⚠️ Reference snapshot is empty")
        pass

    # print(f"!!!! passed earlier check, reference got {reference_snapshot.select(pl.len())['len'][0]} rows, snapshot got {snapshot.select(pl.len())['len'][0]} rows")
    # print(f"and snapshot after joining got {snapshot.join(reference_snapshot, on=snapshot.columns, how='inner').select(pl.len())['len'][0]} rows")

    return snapshot_similarity(
        added_rows.select(target_dataframe.columns),
        target_dataframe=target_dataframe,
        column_similarities=column_similarities,
        reference_snapshot=reference_snapshot,
    )


def removal_similarity(
    snapshot: pl.DataFrame,
    target_dataframe: Optional[pl.DataFrame] = None,
    column_similarities: Optional[Dict[str, ColumnSimilarityMeasureType]] = None,
    reference_snapshot: Optional[pl.DataFrame] = None,
    **kwargs: Union[str, ToolTraceExtractorType],
) -> float:
    """Measures the similarity between each database snapshot and a target_dataframe, if the snapshot is supposed to
    be derived from removing target_dataframe from reference_snapshot

        This can be implemented by swapping snapshot, reference_snapshot and calling addition_similarity

    Args:
        snapshot:                   The dataframe snapshot to calculate similarity for
        target_dataframe:           The dataframe to calculate similarity with
        column_similarities:        A dictionary of column name to column-wise similarity measure
        reference_snapshot:         When similarity is 1,
                                    snapshot should be the result of removing target_dataframe from reference_snapshot

    Returns:
        A [0, 1] similarity score between target_dataframe and snapshot
    """
    assert (
        target_dataframe is not None
        and column_similarities is not None
        and reference_snapshot is not None
    )
    return addition_similarity(
        snapshot=reference_snapshot,
        target_dataframe=target_dataframe,
        column_similarities=column_similarities,
        reference_snapshot=snapshot,
    )


def update_similarity(
    snapshot: pl.DataFrame,
    target_dataframe: Optional[pl.DataFrame] = None,
    column_similarities: Optional[Dict[str, ColumnSimilarityMeasureType]] = None,
    reference_snapshot: Optional[pl.DataFrame] = None,
    **kwargs: Union[str, ToolTraceExtractorType],
) -> float:
    """Measures the similarity between each database snapshot and a target_dataframe, if the snapshot is supposed to
    be derived from updating the same of number entries from reference_snapshot into target_dataframe
        1. If snapshot and reference_snapshot doesn't match in row count, similarity is always 0
        2. If the number of different rows between snapshot and reference_snapshot doesn't match target_dataframe
            similarity is always 0
        2. If it does, the anti join of the two is compared against target_dataframe using snapshot_similarity
    Args:
        snapshot:                   The dataframe snapshot to calculate similarity for
        target_dataframe:           The dataframe to calculate similarity with
        column_similarities:        A dictionary of column name to column-wise similarity measure
        reference_snapshot:         When similarity is 1,
                                    snapshot should be the result of adding target_dataframe into reference_snapshot
    Returns:
        A [0, 1] similarity score between target_dataframe and snapshot
    """
    assert target_dataframe is not None
    assert column_similarities is not None
    assert reference_snapshot is not None

    # Drop sandbox_message_index
    # Fill null with zero to prevent join failure
    # snapshot = snapshot.drop("sandbox_message_index").fill_null(strategy="zero")
    snapshot = snapshot.drop("sandbox_message_index", strict=False).fill_null(0)

    # reference_snapshot = reference_snapshot.drop("sandbox_message_index").fill_null(
    #     strategy="zero"
    # )
    reference_snapshot = reference_snapshot.drop(
        "sandbox_message_index", strict=False
    ).fill_null(0)
    # target_dataframe = target_dataframe.fill_null(strategy="zero")
    target_dataframe = target_dataframe.fill_null(0)

    join_columns = [
        col
        for col in snapshot.columns
        if (("id" in col) or ("datetime" in col)) and snapshot.schema[col] == pl.Utf8
    ]

    # Step 1: Ensure row count matches
    if (
        reference_snapshot.select(pl.len())["len"][0]
        != snapshot.select(pl.len())["len"][0]
    ):
        # print("update similarity breaks here")
        return 0

    # breakpoint()
    # print(
    #     f"Updated rows: {snapshot.join(reference_snapshot, on=join_columns, how='anti').select(target_dataframe.columns)}"
    # )
    # print(f"target dataframe: {target_dataframe}")
    # print(f"snapshot: {snapshot.select(target_dataframe.columns)}")
    # print(f"reference : {reference_snapshot.select(target_dataframe.columns)}")

    return snapshot_similarity(
        snapshot.join(reference_snapshot, on=join_columns, how="anti").select(
            target_dataframe.columns
        ),
        target_dataframe=target_dataframe,
        column_similarities=column_similarities,
        reference_snapshot=reference_snapshot,
    )


def _exact(a: pl.Series, b: pl.Series) -> pl.Series:
    return (a == b).cast(pl.Float64)


def contains_presence_similarity(
    snapshot: pl.DataFrame,
    target_dataframe: Optional[pl.DataFrame] = None,
    column_similarities: Optional[Dict[str, ColumnSimilarityMeasureType]] = None,
    reference_snapshot: Optional[pl.DataFrame] = None,
    **kwargs: Union[str, bool, ToolTraceExtractorType],
) -> float:
    """
    Loose 'contains' check:
      - Ignore deletions/other rows.
      - Score how well `snapshot` contains `target_dataframe` rows.
      - If `require_added=True` and `reference_snapshot` is given, only accept matches
        from rows that are new in `snapshot` vs `reference_snapshot` (but do NOT enforce
        snapshot ⊇ reference; deletions are allowed).

    Score = coverage * quality in [0,1]
      coverage = fraction of target rows that have a match
      quality  = mean per-column similarity over matched rows
    """
    assert target_dataframe is not None
    assert snapshot is not None
    assert column_similarities is not None

    require_added: bool = bool(kwargs.get("require_added", False))
    # Basic cleaning similar to your original
    if "sandbox_message_index" in snapshot.columns:
        snapshot = snapshot.drop("sandbox_message_index", strict=False)
    snapshot = snapshot.fill_null(0)
    target = target_dataframe.fill_null(strategy="zero").fill_null(0)

    # 1) Columns check: target columns must be a subset of candidate columns
    #    (snapshot_similarity requires exact column match; here we relax to subset)
    if set(target.columns) - set(snapshot.columns):
        return 0.0

    # Choose id columns if not given
    id_columns = [
        col
        for col in snapshot.columns
        if (
            "id" in col and snapshot.schema[col] == pl.Utf8
        )  # or ("datetime_iso" in col)
    ]

    # 2) Prepare candidate rows (optionally only the "added" part)
    if require_added and reference_snapshot is not None:
        if not id_columns:
            # No way to anti-join sensibly; fall back to whole snapshot
            candidate = snapshot
        else:
            candidate = snapshot.join(reference_snapshot, on=id_columns, how="anti")
    else:
        candidate = snapshot

    # If no candidates, containment fails
    if candidate.height == 0 or target.height == 0:
        return float(target.height == 0)  # empty target -> trivially 1.0

    # Keep only columns needed for scoring (like snapshot_similarity)
    candidate = candidate.select(target.columns)

    # # NOTE: Debug
    # print(f"Target Dataframe: {target}")
    # print(f"id columns: {id_columns}")
    # print(f"candidate dataframe: {candidate}")

    # 3) Build the rectangular cost matrix: rows=target, cols=candidate
    #    Cost = -log(similarity).
    cost_rows: list[np.ndarray[Any, np.dtype[np.float64]]] = []

    for row in target.to_dicts():
        # column-wise similarities for this target row against all candidate rows
        per_col_costs = []
        for i, (col_name, value) in enumerate(row.items()):
            # # NOTE: Debug
            # print(f"Target column: {col_name}, Value {value}")
            # print(f"Candidate: {candidate.select(pl.col(col_name))}")

            sim_df = column_similarities[col_name](
                dataframe=candidate,
                column_name=col_name,
                value=value,
            ).select((-pl.col("similarity").log()).alias(f"sim_{i}_cost"))
            # # NOTE: Debug
            # print(f"Column: {col_name}, Similarity: {sim_df}")
            per_col_costs.append(sim_df)

        # Geo-mean over columns via mean(log(sim)) trick -> arithmetic mean of the per-col costs
        col_cost_df = pl.concat(per_col_costs, how="horizontal")
        mean_cost = col_cost_df.select(
            pl.mean_horizontal(*col_cost_df.columns).alias("mean_cost")
        )["mean_cost"].to_numpy()
        cost_rows.append(mean_cost)

    numpy_cost = np.stack(cost_rows, axis=0)  # shape: [N_target, M_candidate]

    # 4) Solve assignment: one candidate per target (rectangular is fine)
    try:
        row_ind, col_ind = linear_sum_assignment(numpy_cost)
    except ValueError:
        return 0.0

    # 5) Convert mean cost back to similarity with exp(-mean_cost) like your function
    selected_costs = numpy_cost[row_ind, col_ind]
    return float(np.exp(-selected_costs.mean()))


def not_contains_presence_similarity(
    snapshot: pl.DataFrame,
    target_dataframe: Optional[pl.DataFrame] = None,
    column_similarities: Optional[Dict[str, ColumnSimilarityMeasureType]] = None,
    reference_snapshot: Optional[pl.DataFrame] = None,
    **kwargs: Union[str, bool, ToolTraceExtractorType],
) -> float:
    """
    Loose 'not contains' check:
      - Returns high score if `snapshot` does NOT contain rows from `target_dataframe`.
      - Symmetric to `contains_presence_similarity`.

    Example:
      If snapshot avoids all target rows -> score = 1.0
      If snapshot contains some target rows -> partial penalty
      If snapshot contains all target rows -> score = 0.0
    """
    require_added: bool = bool(kwargs.get("require_added", False))
    presence_score = contains_presence_similarity(
        snapshot=snapshot,
        target_dataframe=target_dataframe,
        column_similarities=column_similarities,
        reference_snapshot=reference_snapshot,
        require_added=require_added,
    )
    return 1.0 - presence_score


def tool_trace_dependant_similarity(
    snapshot: pl.DataFrame,
    target_dataframe: Optional[pl.DataFrame] = None,
    column_similarities: Optional[Dict[str, ColumnSimilarityMeasureType]] = None,
    reference_snapshot: Optional[pl.DataFrame] = None,
    **kwargs: Union[str, ToolTraceExtractorType],
) -> float:
    """A special similarity only intended to be used for SANDBOX database. Allows one to extract values
    from the tool_trace in reference_snapshot, and fill into target_dataframe. Extractors are allowed to return
    multiple "normalized" version of extracted value, a similarity will be calculated for each, and return the max.

    Args:
        snapshot:               The dataframe snapshot to calculate similarity for
        target_dataframe:       The dataframe to calculate similarity with. Either content or tool_trace column is
                                incomplete, requires value extracted from reference_snapshot to fill in
        column_similarities:    A dictionary of column name to column-wise similarity measure
        reference_snapshot:     Contains tool_trace we wish to extract value from
        **kwargs:               Should contain keyword argument "fill_to", indicating which column to fill extracted
                                value into. Can only choose from Literal["tool_trace", "content"].
                                    - In the case of "tool_trace", extracted values are supplied as kwargs into tool
                                        trace arguments
                                    - In the case of "content", extracted values are supplied to str.format
                                Should contain keyword argument "extractor" of type ToolTraceExtractorType.
                                An extractor function taking 1 tool trace as input, and returns a list of dictionary,
                                containing multiple normalized form of extracted values.
                                Each normalized extracted value will be provided to target_dataframe,
                                calculate similarity, and the max of all normalized forms is taken as final similarity.

    Returns:

    """
    assert (
        target_dataframe is not None
        and column_similarities is not None
        and reference_snapshot is not None
    )
    # Check schema to make sure we are working with SANDBOX database. Allows sandbox_message_index to be dropped
    for current_snapshot in (snapshot, reference_snapshot):
        schema = {**current_snapshot.schema}
        # Add sandbox_message_index if dropped
        schema.update(
            {
                "sandbox_message_index": ExecutionContext.dbs_schemas[
                    DatabaseNamespace.SANDBOX
                ]["sandbox_message_index"]
            }
        )
        if (
            schema != ExecutionContext.dbs_schemas[DatabaseNamespace.SANDBOX]
            or current_snapshot.select(pl.len())["len"][0] != 1
        ):
            raise SchemaError(
                "tool_trace_dependant_similarity can only be used with SANDBOX database with only 1 row"
            )
    # Check kwargs
    if "fill_to" not in kwargs:
        raise KeyError(
            "fill_to kwarg of type Literal['tool_trace', 'content'] "
            "must be provided to tool_trace_dependant_similarity. "
        )
    fill_to = cast(Literal["tool_trace", "content"], kwargs["fill_to"])
    if fill_to not in ("tool_trace", "content"):
        raise ValueError("fill_to must be of type Literal['tool_trace', 'content']")
    if "extractor" not in kwargs:
        raise KeyError(
            "extractor kwarg of type ToolTraceExtractorType "
            "must be provided to tool_trace_dependant_similarity. "
        )
    extractor = cast(ToolTraceExtractorType, kwargs["extractor"])
    # Start extraction
    if reference_snapshot["tool_trace"][0] is None:
        return 0
    tool_traces = cast(
        List[Dict[Literal["tool_name", "arguments", "result"], Any]],
        [json.loads(x) for x in reference_snapshot["tool_trace"][0]],
    )
    # Extract values from all tool traces in snapshot
    extracted_values: List[Dict[str, Any]] = []
    for tool_trace in tool_traces:
        try:
            extracted_values.extend(extractor(tool_trace))
        except (KeyError, IndexError, TypeError, ValueError):
            pass
    # Find the best possible matches
    similarity: float = 0.0
    try:
        for extracted_value in extracted_values:
            # When filling in extracted_value, we consider the following options:
            #   1. Any extracted_value can fill in any trace
            #   2. If an extracted_value overrides an existing kwarg in the trace,
            #       consider the existing kwarg as well.
            if fill_to == "tool_trace":
                trace: Union[dict[str, Any], list[dict[str, Any]]] = json.loads(
                    target_dataframe["tool_trace"][0]
                )
                # Normalize into a list of possible candidate traces
                candidate_traces: list[dict[str, Any]] = (
                    [trace] if not isinstance(trace, Sequence) else list(trace)
                )
                filled_traces: list[dict[str, Any]] = []
                # Filling extracted value to all candidate traces
                for candidate_trace in candidate_traces:
                    # Prefer arguments in extracted_value
                    current_trace = deepcopy(candidate_trace)
                    current_trace["arguments"].update(extracted_value)
                    filled_traces.append(current_trace)
                    # Prefer arguments in candidate_trace
                    current_trace = deepcopy(candidate_trace)
                    extracted_arguments = deepcopy(extracted_value)
                    extracted_arguments.update(current_trace["arguments"])
                    current_trace["arguments"] = extracted_arguments
                    filled_traces.append(current_trace)
                similarity = max(
                    similarity,
                    snapshot_similarity(
                        snapshot=snapshot,
                        target_dataframe=target_dataframe.with_columns(
                            pl.lit(json.dumps(filled_traces, ensure_ascii=False)).alias(
                                "tool_trace"
                            )
                        ),
                        column_similarities=column_similarities,
                        reference_snapshot=reference_snapshot,
                    ),
                )
            elif fill_to == "content":
                candidate_content = cast(str, target_dataframe["content"][0])
                candidate_content = candidate_content.format(**extracted_value)
                similarity = max(
                    similarity,
                    snapshot_similarity(
                        snapshot=snapshot,
                        target_dataframe=target_dataframe.with_columns(
                            pl.lit(candidate_content).alias("content")
                        ),
                        column_similarities=column_similarities,
                        reference_snapshot=reference_snapshot,
                    ),
                )
    except (IndexError, KeyError):
        return 0.0
    return similarity


def column_tool_trace_matches_tool_names(
    dataframe: pl.DataFrame,
    column_name: str,
    value: Any,
    target_tools: list[str],
    atol_dict: Optional[dict[str, float]] = None,
) -> pl.DataFrame:
    def matches_tool(row: tuple[Optional[list[str]]]) -> float:
        tool_trace_list = row[0]  # Unpack single column value
        if not tool_trace_list:
            return 0.0
        for tool_trace_json in tool_trace_list:
            try:
                tool_trace = json.loads(tool_trace_json)
                if tool_trace.get("tool_name") in target_tools:
                    return 1.0
            except Exception:
                continue
        return 0.0

    return (
        dataframe.select(pl.col(column_name))
        .map_rows(function=matches_tool, return_dtype=pl.Float64)
        .select(pl.col("map").cast(pl.Float32).alias("similarity"))
    )


def print_mismatched_rows(
    snapshot: pl.DataFrame, reference_snapshot: pl.DataFrame
) -> None:
    """Print mismatched rows between snapshot and reference using pure Polars, avoiding non-sortable columns."""
    try:
        if snapshot.shape != reference_snapshot.shape:
            print(
                f"⚠️ Shape mismatch: snapshot = {snapshot.shape}, reference = {reference_snapshot.shape}"
            )

        # Only keep sortable columns (exclude List type, Struct, etc.)
        sortable_columns = [
            col
            for col in snapshot.columns
            if snapshot.schema[col] not in [pl.List(pl.Utf8), pl.List, pl.Struct]
        ]
        common_columns = list(set(sortable_columns) & set(reference_snapshot.columns))

        snapshot_aligned = snapshot.select(common_columns).sort(by=common_columns)
        reference_aligned = reference_snapshot.select(common_columns).sort(
            by=common_columns
        )

        for i in range(snapshot_aligned.height):
            row_snapshot = snapshot_aligned.row(i)
            row_reference = reference_aligned.row(i)
            if row_snapshot != row_reference:
                print(f"❌ Row {i} mismatch:")
                print(f"   🔸 Snapshot : {row_snapshot}")
                print(f"   🔹 Reference: {row_reference}")

    except Exception as e:
        print("🚨 Error during mismatch detection:", e)


def guardrail_similarity(
    snapshot: pl.DataFrame,
    target_dataframe: Optional[pl.DataFrame] = None,
    column_similarities: Optional[Dict[str, ColumnSimilarityMeasureType]] = None,
    reference_snapshot: Optional[pl.DataFrame] = None,
    **kwargs: Union[str, ToolTraceExtractorType],
) -> float:
    """Similarity which ensures snapshot is identical to reference. Returns 0 otherwise

    Args:
        snapshot:                   The dataframe snapshot to calculate similarity for
        target_dataframe:           Not utilized by this similarity
        column_similarities:        Not utilized by this similarity
        reference_snapshot:         When similarity is 1,
                                    snapshot identical to reference_snapshot

    Returns:
        A [0, 1] similarity score between target_dataframe and snapshot
    """
    assert reference_snapshot is not None
    # # NOTE: Debug
    # if not snapshot.equals(reference_snapshot):
    #     print("❌ Guardrail mismatch detected!")
    #     print_mismatched_rows(snapshot, reference_snapshot)
    return float(snapshot.equals(reference_snapshot))


# Default similarity measures for each column
_default_dbs_column_similarities: dict[str, dict[str, ColumnSimilarityMeasureType]] = {
    DatabaseNamespace.SANDBOX: {
        "sandbox_message_index": column_exact_match_similarity,
        "sender": column_exact_match_similarity,
        "recipient": column_exact_match_similarity,
        "content": column_rouge_l_similarity,
        "openai_tool_call_id": column_one_similarity,
        "openai_function_name": column_one_similarity,
        "conversation_active": column_exact_match_similarity,
        "tool_call_exception": column_one_similarity,
        "thinking_tokens": column_one_similarity,
        "reasoning_token_count": column_one_similarity,
        "tool_trace": column_tool_trace_exact_match_similarity,
        "visible_to": column_exact_match_similarity,
    },
    DatabaseNamespace.SETTING: {
        "sandbox_message_index": column_exact_match_similarity,
        "device_id": column_exact_match_similarity,
        "cellular": column_exact_match_similarity,
        "wifi": column_exact_match_similarity,
        "location_service": column_exact_match_similarity,
        "low_battery_mode": column_exact_match_similarity,
        "latitude": column_exact_match_similarity,
        "longitude": column_exact_match_similarity,
    },
    DatabaseNamespace.CONTACT: {
        "sandbox_message_index": column_exact_match_similarity,
        "person_id": column_exact_match_similarity,
        "first_name": column_exact_match_similarity,
        "last_name": column_exact_match_similarity,
        "alias": column_exact_match_similarity,
        "full_name": column_exact_match_similarity,
        "phone_number": column_exact_match_similarity,
        "email": column_exact_match_similarity,
        "relationship": column_rouge_l_similarity,
        "address": column_exact_match_similarity,
        "company": column_rouge_l_similarity,
        "job_title": column_rouge_l_similarity,
        "birthday": column_exact_match_similarity,
        "is_self": column_exact_match_similarity,
        "creation_datetime_iso": column_contains_similarity,
    },
    DatabaseNamespace.PHONE: {
        "sandbox_message_index": column_exact_match_similarity,
        "phone_call_id": column_exact_match_similarity,
        "call_type": column_exact_match_similarity,
        "caller_address": column_exact_match_similarity,
        "caller_id": column_exact_match_similarity,
        "receiver_address": column_exact_match_similarity,
        "receiver_id": column_exact_match_similarity,
        "voice_mail_transcription": column_rouge_l_similarity,
        "creation_datetime_iso": column_contains_similarity,
        "duration_in_hms": column_exact_match_similarity,
    },
    DatabaseNamespace.MESSAGING: {
        "sandbox_message_index": column_exact_match_similarity,
        "conversation_id": column_exact_match_similarity,
        "conversation_name": column_exact_match_similarity,
        "message_id": column_exact_match_similarity,
        "sender_person_id": column_exact_match_similarity,
        "sender_address": column_exact_match_similarity,
        "participants_ids": column_list_exact_match_similarity,
        "participants_addresses": column_list_exact_match_similarity,
        "content": column_rouge_l_similarity,
        "creation_datetime_iso": column_contains_similarity,
        "status": column_exact_match_similarity,
    },
    DatabaseNamespace.REMINDER: {
        "sandbox_message_index": column_exact_match_similarity,
        "reminder_id": column_exact_match_similarity,
        "content": column_rouge_l_similarity,
        "creation_timestamp": column_exact_match_similarity,
        "reminder_timestamp": column_exact_match_similarity,
        "latitude": column_exact_match_similarity,
        "longitude": column_exact_match_similarity,
    },
    DatabaseNamespace.CALENDAR: {
        "sandbox_message_index": column_exact_match_similarity,
        "calendar_name": column_exact_match_similarity,
        "calendar_event_id": column_exact_match_similarity,
        "calendar_event_name": column_rouge_l_similarity,
        "start_datetime_iso": column_contains_similarity,
        "end_datetime_iso": column_contains_similarity,
        "attendees_ids": column_list_exact_match_similarity,
        "attendees_names": column_list_exact_match_similarity,
        "location": column_exact_match_similarity,
        "reminder_time_ahead": column_exact_match_similarity,
        "organizer_id": column_exact_match_similarity,
        "organizer_name": column_exact_match_similarity,
        "meeting_url": column_exact_match_similarity,
        "creation_datetime_iso": column_contains_similarity,
        "notes": column_rouge_l_similarity,
    },
    DatabaseNamespace.EMAIL: {
        "sandbox_message_index": column_exact_match_similarity,
        "thread_id": column_exact_match_similarity,
        "email_id": column_exact_match_similarity,
        "subject": column_rouge_l_similarity,
        "sender_id": column_exact_match_similarity,
        "sender_address": column_exact_match_similarity,
        "recipients_ids": column_list_exact_match_similarity,
        "recipients_addresses": column_list_exact_match_similarity,
        "cc_ids": column_list_exact_match_similarity,
        "cc_addresses": column_list_exact_match_similarity,
        "bcc_ids": column_list_exact_match_similarity,
        "bcc_addresses": column_list_exact_match_similarity,
        "creation_datetime_iso": column_contains_similarity,
        "body": column_rouge_l_similarity,
        "attachments": column_list_exact_match_similarity,
        "status": column_exact_match_similarity,
    },
    DatabaseNamespace.WHATSAPP: {
        "sandbox_message_index": column_exact_match_similarity,
        "conversation_id": column_exact_match_similarity,
        "conversation_name": column_rouge_l_similarity,
        "message_id": column_exact_match_similarity,
        "participants_names": column_list_exact_match_similarity,
        "participants_addresses": column_list_exact_match_similarity,
        "sender_name": column_exact_match_similarity,
        "sender_address": column_exact_match_similarity,
        "content": column_rouge_l_similarity,
        "creation_datetime_iso": column_contains_similarity,
        "status": column_exact_match_similarity,
    },
}


@define
class SnapshotConstraint:
    """Constraints between 2 snapshots. These are (optionally) pairwise similarity constraints that are
    applied between 2 milestones and their corresponding snapshots. This constraint should provide a [0, 1]
    constraint score.

    """

    # Which database should this constraint be applied to
    database_namespace: DatabaseNamespace
    # Snapshot constraint function
    snapshot_constraint: SnapshotSimilarityMeasureType
    # Index to the reference milestone node index. The snapshot this milestone maps to is supplied to.
    # Since SnapshotConstraint always lives in a milestone. The milestone's own index is implied
    reference_milestone_node_index: Optional[int] = None
    # Target dataframe to compare against
    target_dataframe: Optional[pl.DataFrame] = None
    # Column similarity measure. if None, uses default values defined in Evaluation
    column_similarity_measure: Optional[Dict[str, ColumnSimilarityMeasureType]] = None
    # Strictly checking presence in added rows. By default it False, checking presence in the final snapshot
    require_added: Optional[bool] = False

    def __attrs_post_init__(self) -> None:
        """Fill in default values for column_similarity_measure

        Returns:

        """
        column_similarity_measure: Dict[str, ColumnSimilarityMeasureType] = deepcopy(
            _default_dbs_column_similarities[self.database_namespace]
        )
        # When similarity measure is provided, override default for provided entries
        if self.column_similarity_measure is not None:
            column_similarity_measure.update(self.column_similarity_measure)
        self.column_similarity_measure = column_similarity_measure


@define
class Milestone:
    """Constraints defining a milestone"""

    # A List of similarity constraints. All these constraints are applied to databases of the same sandbox_message_index
    snapshot_constraints: List[SnapshotConstraint]
    # One can enforce some database should not have changed comparing to reference. These constraints are called
    # guardrails. By default, when guardrail_database_list is None, guardrail is applied to all non
    # SANDBOX databases that doesn't have an associated SnapshotConstraint in this milestone.
    # Reference is chosen from all reference milestones listed in snapshot_constraints
    guardrail_database_list: Optional[List[DatabaseNamespace]] = None
    # Alternative way to specify guardrail. database listed here will be excluded. Cannot be set with
    # guardrail_database_list at the same time
    guardrail_database_exclusion_list: Optional[List[DatabaseNamespace]] = None

    def __attrs_post_init__(self) -> None:
        """Set default guardrail_database_list

        Returns:

        """
        if (
            self.guardrail_database_list is not None
            and self.guardrail_database_exclusion_list is not None
        ):
            raise ValueError(
                "Only one of guardrail_database_list, guardrail_database_exclusion_list should be set"
            )
        if self.guardrail_database_list is None:
            self.guardrail_database_list = cast(
                List[DatabaseNamespace], list(DatabaseNamespace)
            )
        if self.guardrail_database_exclusion_list is not None:
            self.guardrail_database_list = [
                x
                for x in self.guardrail_database_list
                if x not in self.guardrail_database_exclusion_list
            ]


class Minefield(Milestone):
    """Minefields are the opposite of Milestones.

    A Minefield defines conversation / world state that absolutely shouldn't happen
    in a trajectory. Minefields form a minefield_dag. If a minefield_dag matched with non-zero
    similarity, the entire trajectory is nullified.

    This is particularly useful for Insufficient Information category, where certain tools should
    never be called.
    """


@define
class CachedSimilarityCalculator:
    """Given a fully played out execution_context, attempt to calculate & cache similarity scores

    Each SnapshotConstraint depends on two snapshots, the current snapshot and a reference snapshot.
    Remember that only when database was updated do we create a new snapshot. Meaning for each database,
    snapshot index can be divided into buckets where snapshot within said bucket does not change.
    For a SnapshotConstraint, for all combinations of current snapshot and a reference snapshot that falls into
    the same bucket combination, similarity score should be the same. We take advantage of this to build a cache
    system for SnapshotConstraint
    """

    # The execution_context containing full rollout
    execution_context: ExecutionContext
    # Milestone / Minefield to calculate similarity for
    milestone: Milestone
    # Bucket boundary, constructed in post_init. Adjacent pairs of indices form a left inclusive right exclusive bucket
    database_bucket_boundary: Dict[DatabaseNamespace, List[int]] = field(init=False)
    # Cache for SnapshotConstraint
    snapshot_constraint_similarity_cache: List[
        Dict[Tuple[int, Optional[int]], float]
    ] = field(init=False)
    # Index of the first snapshot, contains initial world state. reference_milestone_node_index == -1 refers to this.
    first_user_message_snapshot_index: int = field(init=False)

    def __attrs_post_init__(self) -> None:
        """Build similarity cache for each SnapshotConstraint within milestone

        Returns:

        """
        # Construct bucket boundary according to execution context
        database_bucket_boundary: Dict[DatabaseNamespace, List[int]] = {}
        for database_namespace in DatabaseNamespace:
            # Make sure not to drop headguard to ensure empty snapshots are represented
            database = self.execution_context.get_database(
                namespace=database_namespace,
                get_all_history_snapshots=True,
                drop_sandbox_message_index=False,
                drop_headguard=False,
            )
            database_bucket_boundary[database_namespace] = (
                database.select(pl.col("sandbox_message_index"))
                .unique()["sandbox_message_index"]
                .to_list()
            )
        self.database_bucket_boundary = database_bucket_boundary
        # Initialize cache
        self.snapshot_constraint_similarity_cache = [
            {} for _ in range(len(self.milestone.snapshot_constraints))
        ]
        # Initialize according to execution context

        self.first_user_message_snapshot_index: int = (
            self.execution_context.first_user_sandbox_message_index
        )

        # # NOTE: Debug
        # print(f"\n📍 first_user_message_snapshot_index = {self.first_user_message_snapshot_index}")
        # Walk backwards to find the last snapshot before tool traces are applied

        # for i in reversed(range(self.execution_context.first_user_sandbox_message_index)):
        #     snapshot = self.execution_context.get_database(
        #         namespace=DatabaseNamespace.PHONE,
        #         sandbox_message_index=i,
        #     )
        #     if snapshot.is_empty():
        #         print(f"at sandbox_message_index: {i}, PHONE is empty")
        #         self.first_user_message_snapshot_index = i
        #         break
        #     print(f"at sandbox_message_index: {i}, PHONE is not empty, {snapshot}")

    def calculate_similarity(
        self,
        current_snapshot_index: int,
        milestone_snapshot_mapping: Dict[int, Tuple[int, float]],
    ) -> float:
        """Calculate milestone similarity given the current snapshot index and previous mappings

        Caching happens automatically. Calculates Geometric mean of all SnapshotConstraint similarities.
        Guardrail constraints are an exception. If all guardrail constraint similarities are 1, they are all excluded
        from the mean, in order not to meaninglessly bump up similarity scoring.

        Args:
            current_snapshot_index:         The snapshot this current milestone maps to
            milestone_snapshot_mapping:     A dict of milestone -> snapshot mapping of all previous snapshots

        Returns:
            Similarity score for the current milestone given existing mapping
        """

        # # NOTE: Debug
        def get_func_name(func: Union[Callable[..., Any], functools.partial]) -> str:  # type: ignore
            if hasattr(func, "__name__"):
                return func.__name__
            elif isinstance(func, functools.partial):
                return f"partial({get_func_name(func.func)})"
            return str(func)

        # print(f"📍 current_snapshot_index = {current_snapshot_index}")

        similarity: float = 1
        similarity_count: int = 0
        # -1 maps to first snapshot by default. Add entry for None -> None to help with cases where
        # reference snapshot doesn't exist (reference_milestone_node_index == None)
        # Mypy does not allow assigning a `dict[K, V]` to a variable of type
        # `dict[Optional[K], V]` so we use a cast.
        patched_snapshot_mapping = {
            **cast(
                dict[Optional[int], tuple[Optional[int], float]],
                milestone_snapshot_mapping,
            ),
            -1: (self.first_user_message_snapshot_index, 0),
            None: (None, 0),
        }

        # NOTE: Debug
        # print(patched_snapshot_mapping.keys())

        for constraint, cache in zip(
            self.milestone.snapshot_constraints,
            self.snapshot_constraint_similarity_cache,
        ):
            # Find snapshots
            try:
                reference_snapshot_index, _ = patched_snapshot_mapping[
                    constraint.reference_milestone_node_index
                ]
            except KeyError:
                # `_add_guardrail_constraints` auto-injects constraints whose
                # `reference_milestone_node_index` points at each predecessor
                # milestone. When `_dfs` speculates on a not-yet-assigned
                # dependent, the temp mapping it passes in doesn't yet contain
                # every predecessor of that dependent — so those auto-guardrails
                # look up a milestone that isn't mapped. Skip the constraint
                # rather than crash the evaluator: during lookahead we can't
                # score it, and if it fires during a real (non-lookahead) call
                # then dropping one unresolvable constraint is better than
                # tanking the whole scenario with an uncaught KeyError.
                LOGGER.debug(
                    "Skipping snapshot constraint: reference milestone "
                    "node index %s is not in mapping (keys=%s).",
                    constraint.reference_milestone_node_index,
                    sorted(
                        k for k in patched_snapshot_mapping.keys() if isinstance(k, int)
                    ),
                )
                continue
            # # NOTE: debug
            # print("📍 Reference snapshot index:", reference_snapshot_index)
            # print(f"📎 Getting reference snapshot at index {reference_snapshot_index}")
            # print(self.execution_context.get_database(namespace=constraint.database_namespace,
            #             sandbox_message_index=reference_snapshot_index))

            # Create cache key. (current_snapshot_index, reference_snapshot_index)
            cache_key = (current_snapshot_index, reference_snapshot_index)
            if cache_key not in cache:
                current_snapshot, reference_snapshot = (
                    self.execution_context.get_database(
                        namespace=constraint.database_namespace,
                        sandbox_message_index=current_snapshot_index,
                    ).clone(),
                    self.execution_context.get_database(
                        namespace=constraint.database_namespace,
                        sandbox_message_index=reference_snapshot_index,
                    ).clone()
                    if reference_snapshot_index is not None
                    else None,
                )
                cache[cache_key] = constraint.snapshot_constraint(
                    snapshot=current_snapshot,
                    target_dataframe=constraint.target_dataframe,
                    column_similarities=constraint.column_similarity_measure,
                    reference_snapshot=reference_snapshot,
                )

                # # NOTE: Debug
                # print(
                #     f"🔎 Constraint: {get_func_name(constraint.snapshot_constraint)}, value: {cache[cache_key]}"
                # )

            # Multiply accumulation
            similarity *= cache[cache_key]
            # print("🔍 type of cache value = ", type(cache[cache_key]), cache[cache_key])

            # Exclude guardrails from similarity count. Since guardrails are 0 / 1, no adjustment needs to be made
            # on accumulation
            similarity_count += int(
                constraint.snapshot_constraint is not guardrail_similarity
            )
        # Return geometric mean
        return math.pow(similarity, 1 / similarity_count)


def get_effective_turn_count(sandbox_database: pl.DataFrame) -> int:
    """Calculate effective turn count.

    If the execution context ended with exception, sets turn count to None.
    Else, exclude
        1. System messages
        2. User <-> ExecutionEnvironment
        3. User simulator few shot messages (denoted by visible_to == [RoleType.USER])
    Calculate remaining turn counts

    Args:
        sandbox_database:  Sandbox database

    Returns:
        Effective count.
    """
    # Exclude all
    # 1. System messages
    # 2. User <-> ExecutionEnvironment
    # 3. User simulator few shot messages (denoted by visible_to == [RoleType.USER])
    system_message_filter = pl.col("sender") != RoleType.SYSTEM
    user_exec_env_filter = ~(
        (
            (pl.col("sender") == RoleType.USER)
            & (pl.col("recipient") == RoleType.EXECUTION_ENVIRONMENT)
        )
        | (
            (pl.col("sender") == RoleType.EXECUTION_ENVIRONMENT)
            & (pl.col("recipient") == RoleType.USER)
        )
    )
    user_sim_few_shot_filter = pl.col("visible_to") != [RoleType.USER]
    filtered_df = sandbox_database.filter(
        system_message_filter & user_exec_env_filter & user_sim_few_shot_filter
    )
    if filtered_df.is_empty():
        return 0
    return cast(
        int,
        filtered_df.with_columns(pl.len())["len"][0],
    )


# The six PIM databases' retrieval tools. get_all_* dumps the whole table; search_* is the
# targeted counterpart. Used by compute_retrieval_efficiency (deterministic tool-use metric).
GET_ALL_RETRIEVAL_TOOLS = {
    "get_all_emails",
    "get_all_contacts",
    "get_all_calendars",
    "get_all_messages",
    "get_all_whatsapp_messages",
    "get_all_phone_calls",
}
SEARCH_RETRIEVAL_TOOLS = {
    "search_emails",
    "search_contacts",
    "search_calendar_events",
    "search_messages",
    "search_whatsapp_messages",
    "search_phonecall_logs",
}


def compute_retrieval_efficiency(sandbox_database: pl.DataFrame) -> dict[str, Any]:
    """Deterministic retrieval-tool-use metric derived from the trajectory `tool_trace`.

    Over the PIM retrieval tools only (get_all_* dumps and their search_* counterparts),
    counts `get_all_*` calls and *failed* `search_*` calls (empty result = a query that
    missed), and returns:
        retrieval_efficiency = 1 - (get_all + failed_search) / total_retrieval_calls
    Pure single-hit search -> 1.0; dumping and/or many empty searches -> lower.
    `retrieval_efficiency` is None (N/A) when the scenario made no retrieval calls, so it
    can be excluded from mean aggregation rather than counted as 1.0.
    """
    get_all_count = 0
    failed_search_count = 0
    total_retrieval = 0
    if "tool_trace" in sandbox_database.columns:
        for tool_trace_list in sandbox_database.get_column("tool_trace").to_list():
            if not tool_trace_list:
                continue
            for tool_trace_json in tool_trace_list:
                try:
                    entry = json.loads(tool_trace_json)
                except Exception:
                    continue
                name = entry.get("tool_name", "")
                if name in GET_ALL_RETRIEVAL_TOOLS:
                    get_all_count += 1
                    total_retrieval += 1
                elif name in SEARCH_RETRIEVAL_TOOLS:
                    total_retrieval += 1
                    if not entry.get("result"):  # empty list / None => query missed
                        failed_search_count += 1
    efficiency = (
        None
        if total_retrieval == 0
        else 1.0 - (get_all_count + failed_search_count) / total_retrieval
    )
    return {
        "retrieval_get_all_count": get_all_count,
        "retrieval_failed_search_count": failed_search_count,
        "retrieval_efficiency": efficiency,
    }


def compute_failure_mode_counts(
    sandbox_database: pl.DataFrame,
    tool_allow_list: Optional[list[str]] = None,
    agent_to_execution_facing_tool_name: Optional[dict[str, str]] = None,
    recorded_unavailable_tool_calls: int = 0,
) -> dict[str, Any]:
    """Deterministic counts of two agent failure modes that are otherwise invisible.

    Both are recoverable -- the scenario continues and is scored on merit -- which is
    exactly why they need counting: nothing else in the summary distinguishes a run that
    hit them from a run that did not.

    ``empty_agent_turn_count``
        Dialog turns where the agent said nothing. This used to surface as a provider
        `BadRequestError` crash (an empty text block is rejected by some APIs); now that it
        is survivable, the scenario simply scores ~0 on `task_completion` with no stated
        reason, so without this counter a run can lose several percent of its scenarios to
        one cause and look merely mediocre.

    ``hallucinated_tool_call_count``
        Calls to a tool that was not in the agent's schema, i.e. the model inventing a
        capability. Decided against `tool_allow_list` rather than by matching exception
        text. The allow list already contains `end_conversation`, so it is the complete set
        of names the agent was permitted to call, and every requested call is compared
        against it.

        This is deliberately not inferred from exceptions. The same failure has surfaced as
        `NameError: ... is not an available tool` (the current shim) and as
        `KeyError: ... is not a known allowed tool` (pre-recovery, and still the user
        simulator), so message matching needed a growing list of markers and silently
        undercounted whenever the wording moved. Worse, exceptions only exist for
        *recovered* calls, so a call that crashed the scenario was invisible. Comparing the
        requested name against the allow list catches both, because the request is recorded
        whatever happened next.

        Names are resolved through the caller-supplied agent->execution mapping before
        comparison (passed as data rather than read from the global context, so this stays
        a pure function of its arguments), because `openai_function_name` holds the
        AGENT-facing name and the allow list holds execution-facing ones. Without that,
        every call in a `TOOL_NAME_SCRAMBLED` scenario would be counted. An unknown name
        resolves to itself, so genuine invention still falls outside the list.

        Read the count as "called something not on the menu", not as a measure of
        hallucination severity: a call can name a real ASTRA tool that simply was not on
        this scenario's restricted toolset, and such scenarios often still score well.

        `tool_allow_list` of None means unrestricted (see `get_available_tools`), so nothing
        can be out of bounds and the count is 0.
    """
    empty_agent_turns = 0
    hallucinated_tool_calls = 0

    cols = set(sandbox_database.columns)
    if {"sender", "recipient", "content"} <= cols:
        dialog = sandbox_database.filter(
            (pl.col("sender") == RoleType.AGENT)
            & (pl.col("recipient") == RoleType.USER)
        )
        for content in dialog.get_column("content").to_list():
            if content is None or not str(content).strip():
                empty_agent_turns += 1

    if (
        tool_allow_list is not None
        and {
            "sender",
            "recipient",
            "openai_function_name",
        }
        <= cols
    ):
        allowed = set(tool_allow_list)
        scrambled_to_actual = agent_to_execution_facing_tool_name or {}
        requests = sandbox_database.filter(
            (pl.col("sender") == RoleType.AGENT)
            & (pl.col("recipient") == RoleType.EXECUTION_ENVIRONMENT)
        )
        for requested in requests.get_column("openai_function_name").to_list():
            if requested is None:
                continue
            name = str(requested)
            if scrambled_to_actual.get(name, name) not in allowed:
                hallucinated_tool_calls += 1

    # The scan can only see requests whose message reached the SANDBOX database. Anything
    # that aborted the scenario earlier left no row, so take the tally recorded at the
    # point of detection as a floor. They count the same events, hence max() rather than a
    # sum; an older artifact carries no tally and falls back to the scan alone.
    return {
        "empty_agent_turn_count": empty_agent_turns,
        "hallucinated_tool_call_count": max(
            hallucinated_tool_calls, recorded_unavailable_tool_calls
        ),
    }


@define
class EvaluationResult:
    """Contains results about milestone mapping, coarse / finegrained similarity"""

    # ith object in this list contains (snapshot_index, similarity score) for ith milestone
    milestone_mapping: OrderedDict[int, Tuple[int, float]] = Factory(OrderedDict)
    # ith object in this list contains (snapshot_index, similarity score) for ith minefield
    minefield_mapping: OrderedDict[int, Tuple[int, float]] = Factory(OrderedDict)
    # The arithmetic mean similarity score across all milestones
    milestone_similarity: float = 0
    # The arithmetic mean similarity score across all minefields
    minefield_similarity: float = 0
    # Similarity combining minefield_similarity and milestone_similarity.
    # It is set in __attrs_post_init__
    similarity: float = field(init=False)
    # Total turn count, excluding system messages
    turn_count: int = 0
    # Deterministic retrieval-tool-use metrics (see compute_retrieval_efficiency).
    # retrieval_efficiency is None (N/A) when the scenario made no retrieval calls.
    retrieval_get_all_count: int = 0
    retrieval_failed_search_count: int = 0
    retrieval_efficiency: Optional[float] = None
    # Recoverable agent failure modes (see compute_failure_mode_counts). Both are
    # survivable, so nothing else in the summary reveals that a run hit them.
    empty_agent_turn_count: int = 0
    hallucinated_tool_call_count: int = 0

    def __attrs_post_init__(self) -> None:
        # Combine milestone and minefield. If minefield_similarity != 0, nullify everything.
        self.similarity = (
            int(self.minefield_similarity == 0) * self.milestone_similarity
        )


@define
class MilestoneMatcher:
    """Defines Milestone / Minefield for a test scenario, and provide utilities for matching against a trajectory."""

    # A list of milestones. Index of milestones in this list shall be the node index in the milestone DAG
    milestones: Union[list[Milestone], list[Minefield]] = Factory(list)
    # Milestone edge list. If it is None, will construct a linked list between milestones by default
    edge_list: Optional[list[tuple[int, int]]] = None
    # Milestone DAG, constructed in post init
    milestone_dag: "networkx.DiGraph[int]" = field(init=False)
    # Maximum DFS iterations to prevent timeout on pathological inputs
    max_dfs_iterations: int = 100000
    #: Wall-clock budget for the DFS. The iteration cap alone does not bound runtime: when
    #: few milestones match, `current_best_similarity_sum` prunes poorly and the search fans
    #: out, so a weak model can spend unbounded time here — precisely the case where losing
    #: the scenario hurts most. A deadline degrades to the same best-effort mapping the
    #: iteration cap already produces, so grading always returns a score.
    max_dfs_seconds: float = 120.0
    _dfs_deadline: Optional[float] = field(init=False, default=None)
    # Iteration counter (reset per compute_mapping_and_similarity call)
    _dfs_iteration_count: int = field(init=False, default=0)
    # Reverse mapping: milestone_index -> list of milestones that have reference_milestone_node_index pointing to it
    _dependents_map: dict[int, list[int]] = field(init=False, factory=dict)

    def _build_dependents_map(self) -> None:
        """Build reverse mapping: milestone -> milestones that reference it via reference_milestone_node_index"""
        self._dependents_map = {i: [] for i in range(len(self.milestones))}
        for i, milestone in enumerate(self.milestones):
            for constraint in milestone.snapshot_constraints:
                ref_idx = constraint.reference_milestone_node_index
                if ref_idx is not None and ref_idx >= 0:
                    if ref_idx not in self._dependents_map:
                        self._dependents_map[ref_idx] = []
                    if i not in self._dependents_map[ref_idx]:
                        self._dependents_map[ref_idx].append(i)

    def _add_guardrail_constraints(self) -> None:
        """Add guardrail constraints to existing milestones

        Guardrails are applied between current milestone and its reference nodes, as well as its predecessors.

        Returns:

        """
        for i in self.milestone_dag.nodes:
            # Guardrails are applied between current milestone and its reference nodes, as well as
            # its predecessors
            reference_nodes = {
                constraint.reference_milestone_node_index
                for constraint in self.milestones[i].snapshot_constraints
                if constraint.reference_milestone_node_index is not None
            }
            predecessor_nodes = set(self.milestone_dag.predecessors(i))
            # The `cast` is necessary because somehow Mypy does not understand that we
            # explicitly checked the case where
            # `self.milestones[i].guardrail_database_list is None`.
            guardrail_database_set = (
                set()
                if self.milestones[i].guardrail_database_list is None
                else set(
                    cast(
                        list[DatabaseNamespace],
                        self.milestones[i].guardrail_database_list,
                    )
                )
            )
            # Remove sandbox and database that have been constrained in current milestone, reference and predecessor
            guardrail_database_set.discard(DatabaseNamespace.SANDBOX)
            for j in {i} | reference_nodes | predecessor_nodes:
                for constraint in self.milestones[j].snapshot_constraints:
                    if constraint.snapshot_constraint != guardrail_similarity:
                        guardrail_database_set.discard(constraint.database_namespace)
            for reference_milestone_node_index, database_namespace in itertools.product(
                reference_nodes | predecessor_nodes, guardrail_database_set
            ):
                self.milestones[i].snapshot_constraints.append(
                    SnapshotConstraint(
                        reference_milestone_node_index=reference_milestone_node_index,
                        database_namespace=database_namespace,
                        snapshot_constraint=guardrail_similarity,
                    )
                )

    def __attrs_post_init__(self) -> None:
        if self.edge_list is None:
            # NOTE: Linked List Fallback - too restrictive
            self.edge_list = [(i, i + 1) for i in range(len(self.milestones) - 1)]

        self.milestone_dag = networkx.DiGraph(self.edge_list)
        self.milestone_dag.add_nodes_from(range(len(self.milestones)))

        # Add guardrail constraints
        self._add_guardrail_constraints()

        # Build dependents map for lookahead optimization in DFS
        self._build_dependents_map()

    def _dfs(
        self,
        assigned_mapping: OrderedDict[int, Tuple[int, float]],
        similarity_calculators: List[CachedSimilarityCalculator],
        assigned_similarity_sum: float,
        remaining_graph: "networkx.DiGraph[int]",
        current_best_similarity_sum: float,
        min_snapshot_index: int,
        max_snapshot_index: int,
    ) -> Tuple[OrderedDict[int, Tuple[int, float]], float]:
        """Solve for best mapping using dfs + max heap

        Prunes a branch if there's no chance for the branch to match better than current best similarity.

        Args:
            assigned_mapping:               Current already assigned mappings.
            similarity_calculators:         Similarity calculator which computes milestone similarity.
                                            against trajectory. Automatically caches seen similarities.
            assigned_similarity_sum:        Sum of similarity scores across already assigned milestones.
            remaining_graph:                Remaining milestones dag.
            current_best_similarity_sum:    Currently known best similarity sum. Used to prune branches.
            min_snapshot_index:             Minimum snapshot index to match to
            max_snapshot_index:             Maximum snapshot index to match to

        Returns:
            Best assigned mapping and best sum similarity score across milestones
        """
        # Increment iteration counter and check limit
        self._dfs_iteration_count += 1
        if self._dfs_iteration_count > self.max_dfs_iterations or (
            self._dfs_deadline is not None and time.monotonic() > self._dfs_deadline
        ):
            # Return current best-effort result to prevent timeout
            # Fill remaining milestones with 0.0 similarity
            fallback_mapping = deepcopy(assigned_mapping)
            last_snapshot = (
                assigned_mapping[next(reversed(assigned_mapping))][0]
                if assigned_mapping
                else min_snapshot_index
            )
            for m in remaining_graph.nodes():
                fallback_mapping[m] = (last_snapshot, 0.0)
            return fallback_mapping, assigned_similarity_sum

        # DFS end, return
        if networkx.number_of_nodes(remaining_graph) == 0:
            return assigned_mapping, assigned_similarity_sum
        # The most recent assignment. Next assignment must larger than this
        last_assigned_snapshot_index = (
            assigned_mapping[next(reversed(assigned_mapping))][0]
            if assigned_mapping
            else min_snapshot_index
        )
        # Best mapping and best similarity sum across all possible next mappings
        best_assigned_mapping: OrderedDict[int, Tuple[int, float]] = OrderedDict()
        best_assigned_similarity_sum: float = -1
        # Max heap for milestone / snapshot pairs.
        # Each element is (-effective_sim, milestone_index, snapshot_index, base_sim)
        # effective_sim includes lookahead bonus for ordering; base_sim is actual similarity for assignment
        max_heap: List[Tuple[float, int, int, float]] = []

        # ✅ Only consider milestones with in-degree 0
        for milestone_index, in_degree in remaining_graph.in_degree():
            if in_degree > 0:
                continue
            # 🚫 Skip milestone if any parent has similarity == 0
            parents = list(self.milestone_dag.predecessors(milestone_index))
            if any(
                parent not in assigned_mapping or assigned_mapping[parent][1] == 0.0
                for parent in parents
            ):
                continue
            for snapshot_index in reversed(
                range(last_assigned_snapshot_index, max_snapshot_index + 1)
            ):
                base_sim = similarity_calculators[milestone_index].calculate_similarity(
                    current_snapshot_index=snapshot_index,
                    milestone_snapshot_mapping=assigned_mapping,
                )

                # Compute lookahead bonus from dependent milestones
                lookahead_bonus = 0.0
                dependents = self._dependents_map.get(milestone_index, [])
                if dependents:
                    # Create temporary mapping with current milestone assigned
                    temp_mapping = {
                        **assigned_mapping,
                        milestone_index: (snapshot_index, base_sim),
                    }
                    for dep_idx in dependents:
                        if dep_idx in remaining_graph:
                            # Find best possible similarity for dependent milestone
                            best_dep_sim = 0.0
                            for dep_snapshot in range(
                                snapshot_index, max_snapshot_index + 1
                            ):
                                dep_sim = similarity_calculators[
                                    dep_idx
                                ].calculate_similarity(
                                    current_snapshot_index=dep_snapshot,
                                    milestone_snapshot_mapping=temp_mapping,
                                )
                                best_dep_sim = max(best_dep_sim, dep_sim)
                                # Early exit if we found perfect match
                                if best_dep_sim >= 1.0:
                                    break
                            lookahead_bonus += best_dep_sim

                effective_sim = base_sim + lookahead_bonus

                # # # NOTE: Debug
                # if base_sim > 1e-6:
                #     print(
                #         f"🔥 DFS recording: Milestone {milestone_index} -> Snapshot {snapshot_index} with base_sim {base_sim}, lookahead_bonus {lookahead_bonus}"
                #     )

                heapq.heappush(
                    max_heap,
                    (-effective_sim, milestone_index, snapshot_index, base_sim),
                )

        # # NOTE: Debug
        # if max_heap:
        #     print(f"\nHeap before popping (at DFS level {len(assigned_mapping)}):")
        #     for similarity, milestone_index, snapshot_index in max_heap:
        #         print(
        #             f"  Milestone {milestone_index} -> Snapshot {snapshot_index} with similarity {-similarity}"
        #         )

        # Skip milestones that have only 0.0 base_sim *and* have children
        filtered_heap: List[Tuple[float, int, int, float]] = []
        for neg_eff_sim, milestone_idx, snapshot_idx, base_sim in max_heap:
            if base_sim > 0.0:
                filtered_heap.append(
                    (neg_eff_sim, milestone_idx, snapshot_idx, base_sim)
                )
            else:
                # Check if this milestone has children — skip if it blocks others
                if list(self.milestone_dag.successors(milestone_idx)):
                    continue
                else:
                    # Leaf milestone with no match — still allow 0 similarity
                    filtered_heap.append(
                        (neg_eff_sim, milestone_idx, snapshot_idx, base_sim)
                    )

        max_heap = filtered_heap

        # ⚠️ No valid assignments possible for any milestone — return 0.0 for all remaining
        if not max_heap and networkx.number_of_nodes(remaining_graph) > 0:
            fallback_mapping = deepcopy(assigned_mapping)
            for m in remaining_graph.nodes():
                fallback_mapping[m] = (last_assigned_snapshot_index, 0.0)
            return fallback_mapping, assigned_similarity_sum

        # ✅ Always proceed, even if all similarities are 0.0
        while max_heap:
            neg_eff_sim, milestone_index, snapshot_index, base_sim = heapq.heappop(
                max_heap
            )
            sim = base_sim  # Use base_sim for actual assignment, not effective_sim

            # Prune if even the max possible score can't beat current best
            if (
                assigned_similarity_sum + sim + remaining_graph.number_of_nodes() - 1
                <= best_assigned_similarity_sum
            ):
                continue

            new_mapping = deepcopy(assigned_mapping)
            new_mapping[milestone_index] = (snapshot_index, sim)

            new_graph = remaining_graph.copy()
            new_graph.remove_node(milestone_index)

            recursive_mapping, recursive_score = self._dfs(
                new_mapping,
                similarity_calculators,
                assigned_similarity_sum + sim,
                new_graph,
                max(current_best_similarity_sum, best_assigned_similarity_sum),
                min_snapshot_index,
                max_snapshot_index,
            )

            if recursive_score > best_assigned_similarity_sum:
                best_assigned_mapping = recursive_mapping
                best_assigned_similarity_sum = recursive_score

        # 📌 If we couldn't find a better path, but still have unassigned milestones, return 0.0 similarity for them
        if not best_assigned_mapping and assigned_mapping:
            remaining_milestones = list(remaining_graph.nodes())
            fallback_mapping = deepcopy(assigned_mapping)
            for m in remaining_milestones:
                # Pick a default snapshot to attach (you can use last_assigned_snapshot_index or a dummy like -1)
                fallback_mapping[m] = (last_assigned_snapshot_index, 0.0)
            return fallback_mapping, assigned_similarity_sum

        return best_assigned_mapping, best_assigned_similarity_sum

    def compute_mapping_and_similarity(
        self, execution_context: ExecutionContext
    ) -> Tuple[OrderedDict[int, Tuple[int, float]], Optional[float]]:
        """Calculate milestone / minefield mapping and similarity against a trajectory.

        The best matches between milestones and execution_context
        are found by maximizing the total arithmatic mean of similarity score, under the constraint that milestones
        sorted based on sandbox_message_index should be one of the possible topological sorts of milestone_dag
        Milestone and snapshots form a 1:1 mapping.

        Since many Milestones (like guardrail) depends on the matching snapshot of other milestones,
        I couldn't think of a very quick solution to this. Here we implement a brute force solution
        with an adequate amount of pruning + memorization. Should revisit this if this is too slow.

        Args:
            execution_context:      ExecutionContext containing the trajectory to be evaluated.


        Returns:
            An EvaluationResult object containing the mean similarity, as well as milestone mapping and finegrained
            similarity. When no milestones are found, return None as similarity and an empty dict.

        """
        # When milestone_dag is empty, default to perfect score
        if networkx.number_of_nodes(self.milestone_dag) == 0:
            return OrderedDict(), None
        # Construct similarity calculators. These calculators have caching built in
        milestone_similarity_calculators: List[CachedSimilarityCalculator] = [
            CachedSimilarityCalculator(
                execution_context=execution_context, milestone=milestone
            )
            for milestone in self.milestones
        ]
        # Minimum / Maximum snapshot index to match to
        min_snapshot_index: int = execution_context.first_user_sandbox_message_index
        max_snapshot_index: int = execution_context.max_sandbox_message_index
        # Reset iteration counter before DFS
        self._dfs_iteration_count = 0
        self._dfs_deadline = time.monotonic() + self.max_dfs_seconds
        # Brute force DFS
        milestone_mapping, milestone_similarity_sum = self._dfs(
            assigned_mapping=OrderedDict(),
            similarity_calculators=milestone_similarity_calculators,
            assigned_similarity_sum=0,
            remaining_graph=self.milestone_dag,
            current_best_similarity_sum=0,
            min_snapshot_index=min_snapshot_index,
            max_snapshot_index=max_snapshot_index,
        )
        milestone_similarity = milestone_similarity_sum / len(self.milestones)
        return milestone_mapping, milestone_similarity


@define
class Evaluation:
    """Defining the process needed for evaluating a completed ExecutionContext"""

    # A Milestone Matcher. Contains milestone definition for this Evaluation, as well as utilities for matching
    # milestones against a trajectory
    milestone_matcher: MilestoneMatcher = Factory(MilestoneMatcher)
    # A Minefield Matcher. Contains minefield definition for this Evaluation, as well as utilities for matching
    # minefields against a trajectory
    minefield_matcher: MilestoneMatcher = Factory(MilestoneMatcher)

    def evaluate(
        self, execution_context: ExecutionContext, max_turn_count: int
    ) -> EvaluationResult:
        """Evaluate a completed ExecutionContext

        Calculate Milestone and Minefield similarities, combine them.
        Calculate effective turn count.

        Args:
            execution_context:      ExecutionContext to be evaluated
            max_turn_count:         Maximum number of turns allowed. Overrides turn count when the session ended
                                    with an exception

        Returns:
            An EvaluationResult object containing the mean similarity, as well as milestone mapping and finegrained
            similarity

        Raises:
            IndexError: No Milestone found
        """
        milestone_mapping, milestone_similarity = (
            self.milestone_matcher.compute_mapping_and_similarity(
                execution_context=execution_context
            )
        )
        # If no milestones are found, the default milestone_similarity is 1
        milestone_similarity = (
            1 if milestone_similarity is None else milestone_similarity
        )

        minefield_mapping, minefield_similarity = (
            self.minefield_matcher.compute_mapping_and_similarity(
                execution_context=execution_context
            )
        )
        # If no minefields are found, the default minefield_similarity is 0
        minefield_similarity = (
            0 if minefield_similarity is None else minefield_similarity
        )

        # Calculate turn count
        sandbox_history = execution_context.get_database(
            DatabaseNamespace.SANDBOX, get_all_history_snapshots=True
        )
        turn_count = get_effective_turn_count(sandbox_history)
        # Deterministic retrieval-tool-use metrics (get_all dumps / failed searches)
        retrieval_metrics = compute_retrieval_efficiency(sandbox_history)
        # Recoverable failure modes that would otherwise leave no trace in the summary.
        failure_counts = compute_failure_mode_counts(
            sandbox_history,
            tool_allow_list=execution_context.tool_allow_list,
            agent_to_execution_facing_tool_name=(
                execution_context.get_agent_to_execution_facing_tool_name()
            ),
            recorded_unavailable_tool_calls=len(
                execution_context.unavailable_tool_requests
            ),
        )
        # Sort mapping according to milestone index
        return EvaluationResult(
            milestone_mapping=OrderedDict(sorted(milestone_mapping.items())),
            minefield_mapping=minefield_mapping,
            milestone_similarity=milestone_similarity,
            minefield_similarity=minefield_similarity,
            turn_count=turn_count,
            retrieval_get_all_count=retrieval_metrics["retrieval_get_all_count"],
            retrieval_failed_search_count=retrieval_metrics[
                "retrieval_failed_search_count"
            ],
            retrieval_efficiency=retrieval_metrics["retrieval_efficiency"],
            empty_agent_turn_count=failure_counts["empty_agent_turn_count"],
            hallucinated_tool_call_count=failure_counts["hallucinated_tool_call_count"],
        )


@define
class EvaluationLLMResult:
    """Contains results about LLM evaluated reasons and scores"""

    # review_reason: A short paragraph explaining whether the assistant correctly interpreted the user's intent, used tools properly, and retrieved the necessary information.
    review_reason: Optional[str] = None
    # tool_call_capability: Integer score from 0 to 2. Did the assistant use the right tools with appropriate parameters?
    tool_call_capability: Optional[int] = None
    # information_retrieval_capability: Integer score from 0 to 2. Did the assistant extract and interpret the relevant information correctly from tool outputs?
    information_retrieval_capability: Optional[int] = None
    # task_completion: Integer score from 0 to 2. Did the assistant give a correct and complete response to the user?
    task_completion: Optional[int] = None
    # conversation_efficiency: Integer score from 0 to 2. Did the assistant complete the task efficiently without unnecessary clarification questions or detours?
    conversation_efficiency: Optional[int] = None
    # no_hallucination_score: Integer score from 0 to 2. Did the assistant avoid hallucinations and ground all statements in tool output or user-provided context?
    no_hallucination_score: Optional[int] = None


_JUDGE_DIMENSIONS = (
    "tool_call_capability",
    "information_retrieval_capability",
    "task_completion",
    "conversation_efficiency",
    "no_hallucination_score",
)

#: How many times to re-ask when the judge returns a reply that is missing a scored
#: dimension. Separate from the SDK's own transport-level retry, which does not see a
#: well-formed HTTP 200 carrying an incomplete object.
JUDGE_MAX_INCOMPLETE_ATTEMPTS = 3


def _judge_scores_are_complete(
    payload: Optional[Dict[str, Any]], logger_name: str = "EvaluationLLM"
) -> bool:
    """Whether every scored dimension came back as a valid 0-2 integer.

    A judge can return a full review and only some of the dimensions, silently
    omitting one -- including `task_completion`, the headline metric. The result
    would then be written with a None for it, so the score is lost rather than
    retried. Check before accepting a reply.
    """
    if not payload:
        return False
    missing = [
        dimension
        for dimension in _JUDGE_DIMENSIONS
        if not isinstance(payload.get(dimension), int)
        or isinstance(payload.get(dimension), bool)
        or not 0 <= cast(int, payload.get(dimension)) <= 2
    ]
    if missing:
        getLogger(__name__).warning(
            "%s: judge reply omitted or malformed for %s",
            logger_name,
            ", ".join(missing),
        )
        return False
    return True


def _parse_judge_json(
    content: Optional[str], logger_name: str = "EvaluationLLM"
) -> Optional[Dict[str, Any]]:
    """Parse the judge's reply, tolerating a fenced or prose-wrapped JSON object.

    The prompt asks for bare JSON, but a single stray ```json fence or preamble used
    to raise JSONDecodeError and lose the scenario outright. Returning None instead
    leaves it unjudged and counted, which is recoverable; raising is not.
    """
    if not content:
        return None
    text = content.strip()
    try:
        return cast(Dict[str, Any], json.loads(text))
    except json.JSONDecodeError:
        pass
    # Fall back to the outermost {...} block, which covers fences and preambles.
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        try:
            return cast(Dict[str, Any], json.loads(text[start : end + 1]))
        except json.JSONDecodeError:
            pass
    getLogger(__name__).warning(
        "%s: judge reply was not JSON; leaving the scenario unjudged. Got: %s",
        logger_name,
        text[:200],
    )
    return None


def eval_llm_prompt(eval_task: dict[str, Any]) -> str:
    reasoning_chain = eval_task.get("reasoning", "")
    success_conditions = eval_task["success_conditions"]

    # The only tools the assistant could call. Scenarios deliberately expose a narrow
    # subset, so judging tool selection without this list means guessing at the menu:
    # a tool the judge expects may simply never have been offered, and an unavailable
    # tool call is otherwise only visible when it happens to error.
    available_tools_prompt = (
        f"""
--- Tools Available: the ONLY tools the assistant could call ---
{sorted(eval_task['available_tools'])}

Judge tool selection against exactly this list.
- Calling anything not on it is a fabricated capability — score it under
  no_hallucination_score, per the invented-tools rule in its rubric below. Weigh it under
  tool_call_capability too, but as one wrong call among however many the assistant made:
  an unavailable call the assistant then recovers from is not the same as a trajectory of
  entirely wrong tool choices.
- Do NOT expect or require a tool that is absent from it; the assistant had no way to
  call one. Judge the best available approach instead.
"""
        if eval_task.get("available_tools")
        else ""
    )

    # The rubric below assumes a completed interaction — it asks for a final
    # confirmation message and reserves task_completion=2 for fully completing the
    # task. A trajectory that was cut short has no final turn, so without this the
    # judge would score every truncated run near zero and the scores would carry no
    # information about how far the agent actually got. Kept as its own labelled
    # section so truncated and complete evaluations stay distinguishable.
    stopped_early_prompt = (
        f"""
–––––––––––––––––––––––––––––––––
IMPORTANT — This trajectory is INCOMPLETE.

The run was cut short by a `{eval_task['stopped_early_reason']}` in the benchmark
harness, not by any decision of the assistant. The conversation therefore ends
abruptly and there is no final confirmation message to the user.

Grade against the WHOLE task, not just the fragment you can see. The human reasoning
and success conditions above describe the full tool path the task required; the
trajectory below covers only part of it.

- `tool_call_capability` must reflect coverage of that full path, not the local
  correctness of the few calls that happened. A handful of correct calls that cover
  a small part of the required work is roughly a 1, not a 2. Reserve 2 for a
  trajectory that had substantially worked through the required tool path before
  being cut off. Judging only the visible turns in isolation systematically
  over-scores heavily truncated runs, because a short fragment is easy to get right.
- Same for `information_retrieval_capability`: score what was retrieved against what
  the task needed, not against what the fragment happened to ask for.
- `no_hallucination_score` is the exception — it IS local. Ungrounded statements are
  equally wrong whether or not the run was cut short, so judge it on the turns that
  happened and do not discount it for incompleteness.
- `task_completion` should reflect how much of the task was actually accomplished at
  the cut-off, which for an early truncation is usually 0.
- Do not penalise the assistant for the missing final confirmation message itself,
  and do not invent failures for steps it had no opportunity to reach.
–––––––––––––––––––––––––––––––––
"""
        if eval_task.get("stopped_early_reason")
        else ""
    )

    contact_prompt = (
        f"""
## Contact: a flat list of contact dictionaries.
    {format_flat_entities_for_prompt(eval_task.get('contacts'))}
    """
        if eval_task.get("contacts")
        else None
    )

    calendar_prompt = (
        f"""
## Calendar: a flat list of event dictionaries.
    {format_flat_entities_for_prompt(eval_task.get('calendars'))}
    """
        if eval_task.get("calendars")
        else None
    )

    email_prompt = (
        f"""
## Emails: each block between `---` represents a full email thread, which is a list of emails formatted as dictionaries.
    {format_flat_entities_for_prompt(eval_task.get('emails'))}
    """
        if eval_task.get("emails")
        else None
    )

    message_prompt = (
        f"""
## Messages: each block between `---` represents a full message thread, which is a list of messages formatted as dictionaries.
    {format_flat_entities_for_prompt(eval_task.get('messages'))}
    """
        if eval_task.get("messages")
        else None
    )

    whatsapp_message_prompt = (
        f"""
## Whatsapp Messages: each block between `---` represents a full whatsapp message thread, which is a list of whatsapp messages formatted as dictionaries.
    {format_flat_entities_for_prompt(eval_task.get('whatsapp_messages'))}
    """
        if eval_task.get("whatsapp_messages")
        else None
    )

    phonecall_prompt = (
        f"""
## Phone logs: each block between `---` represents a full phone log, which is a list of phone call histories formatted as dictionaries.
    {format_flat_entities_for_prompt(eval_task.get('phonecalls'))}
    """
        if eval_task.get("phonecalls")
        else None
    )

    entities_prompt = [
        entity_prompt
        for entity_prompt in (
            contact_prompt,
            calendar_prompt,
            email_prompt,
            message_prompt,
            whatsapp_message_prompt,
            phonecall_prompt,
        )
        if entity_prompt
    ]
    return f"""You are evaluating whether the assistant successfully completed a user's request using tool calls and reasoning.

You are provided with:
- The user query
- The user's underlying goal
- Annotator-selected personal context that is relevant for task completion (a subset of the user's full personal data, e.g., contacts, calendar events, emails, messages, WhatsApp messages, phone call logs if available)
- A set of success conditions (i.e., what must be true for the task to be considered complete)
- Human-provided chain-of-thought reasoning, but do not evaluate whether the assistant matched the human reasoning; use it only as reference for understanding the task.
- The full trajectory of messages and tool calls exchanged during the task
- Entities that were created, retrieved, or referenced during tool use or assistant responses

Evaluation Guidelines:
- Be concise, factual, and grounded in the trajectory.
- Each score must be an integer: 0, 1, or 2.
- A perfect score (2) means the assistant's actions were accurate, relevant, and aligned with the user's intent and the success conditions.
- A clear failure should receive a score of 0.
- Do not reward verbosity, creativity, or tone — only correctness and completeness matter.
- Do not penalize harmless stylistic differences, politeness, directness, or non-essential variations in wording.
- Output only the specified JSON format, with no extra text.

You are given:

--- Reference Time: When the query taking place in the protagonist timeline ---
{eval_task['reference_time_str']}

--- User Query: First user query in the conversation ---
{eval_task['query']}

--- User Goal: The user's intention ---
{eval_task['user_goal_prompt']}

--- Annotator-Selected Personal Context Relevant to the Task ---
{format_flat_entities_for_prompt(entities_prompt)}

--- Success Conditions: What must be true for the task to be considered complete ---
{format_flat_entities_for_prompt(success_conditions)}

--- Human Reasoning: Human-provided reasoning to complete the task ---
{reasoning_chain}

--- Conversation History: Full trajectory of tool calls and messages exchanged ---
{format_flat_entities_for_prompt(eval_task['conversation_history'])}
{available_tools_prompt}{stopped_early_prompt}

--- Entities Created or Retrieved or Referenced During the Task by the assistant ---
{format_flat_entities_for_prompt(eval_task['mentioned_entities'])}

–––––––––––––––––––––––––––––––––
You are a strict grader. Follow the instructions **exactly**.

### Evaluation Considerations

When deciding each score (0, 1, or 2), evaluate the following aspects of the assistant's performance:

1. **Intent Match**
   - Did the assistant understand and satisfy the user's literal request and underlying goal?
   - Intent match should primarily influence `task_completion`.

2. **No Collateral Damage**
   - Were only the items the user explicitly asked to modify changed?
   - Unrequested deletions, edits, or creations count as errors.
   - Note: `creation_datetime_iso` automatically updates when an entry is modified; this is expected and should match the reference time.

3. **Correct Tool Selection**
   - Were the correct tools used?
   - Were parameters appropriate and grounded in the user request?

4. **Correct Data Interpretation**
   - Did the assistant accurately read and use tool outputs?
   - No invented fields, mismatched items, or misinterpreted results.

5. **Accurate and Honest Confirmation**
   - Did the assistant clearly and truthfully state what actions were performed?
   - The final natural language response must reflect actual tool calls.

### CATEGORY DEFINITIONS AND SCORING RULES

review_reason:
- A short paragraph summarizing whether the assistant understood the user's intent,
  used tools correctly, retrieved information correctly, and completed the task.
- Be factual and concise.

### SCORE THE FIVE DIMENSIONS INDEPENDENTLY

Each dimension measures a different thing, and each must be decided on its own evidence.

Before assigning a score, ask: what in THIS trajectory speaks to THIS dimension specifically?
An assistant can read every tool result correctly and still fail the task; it can reach the
right answer through a clumsy tool path; it can complete the task while inventing one detail.
Score what each dimension actually asks about, and let the scores agree or differ as the
evidence dictates — do not carry a judgment on one dimension over to the others, and do not
adjust a score to be consistent with the others.

### SCORING RUBRICS (0–2)

tool_call_capability (0–2):
This dimension is about CORRECTNESS: did the assistant pick the right tool for the job and
call it with appropriate, well-grounded parameters? Efficiency is a secondary consideration
within that — it can cost a point, but it can never be the reason a score is 0, and a
correct, well-parameterised call is never worse than a 1.
- 2: Right tool(s) for the task, parameters correct and grounded in the request or in earlier
     tool output. Retrieval is reasonably targeted.
- 1: Right tool(s), but with issues: minor parameter errors, clearly redundant/unnecessary
     calls, or an unavailable/wrong call that the assistant then corrected and worked past.
- 0: The tool path as a whole was wrong — wrong tool for the task, or parameters wrong enough
     that the calls could not do what the task needed.
- Score the trajectory as a whole, not its worst single call. One bad call among several
  correct ones, recovered from and followed by a successful path, is a 1 — not a 0. Reserve 0
  for an assistant whose tool use did not get there.
- IMPORTANT: get_all_* is only a fault when a targeted search_* *would have worked*. Judge the
  choice on the information available to the assistant at the time, not with hindsight. In all of
  the following, get_all_* is the CORRECT tool and the score stays 2:
  - Enumeration or counting: "how many contacts do I have?", "list all my events".
  - Establishing that something does NOT exist, or that a detail is missing. A targeted search
    returning nothing does not prove absence — it is also what a wrong query looks like — so
    scanning the full set is the only sound way to answer "is there any…?", "did I ever…?", or
    "is X mentioned anywhere?". This applies to any task whose correct answer is "no" or "that
    information is not available".
  - Recovering from targeted searches that already returned nothing. Falling back to get_all_*
    after an empty search_* is correct diligence, not inefficiency.
  Only treat get_all_* as inefficiency (score 1) when the assistant had a specific entity in
  mind and enough information to search for it directly, and dumped the database instead. Even
  then it is at most a 1, never a 0 — an inefficient route to the right data is not a wrong
  tool choice.

information_retrieval_capability (0–2):
- 2: Correct extraction and interpretation of all relevant information from tool outputs.
- 1: Partially correct extraction; minor misreadings or omissions.
- 0: Major misinterpretation, fabricated details, or failure to use tool results.
- This dimension is about READING what the tools returned. Score it independently of whether
  the task itself succeeded: an assistant can read every result correctly and still fail the
  task, or misread a result and still stumble onto the right answer.

task_completion (0–2):
- 2: Fully and correctly completes the task and meets all explicit user requirements.
- 1: Partially completes the task; small errors or omissions.
- 0: Does not complete the task, contradicts the user's request, or gives an incorrect output.
- GROUNDING REQUIREMENT: a correct-looking answer that no successful tool call supports is a
  guess, not a completion. If the assistant asserts specific facts (a name, time, place, value)
  that appear in no successful tool result and were not supplied by the user, cap this at 1 —
  however plausible or even correct the answer turns out to be. Reaching the right answer by
  luck is not task completion.
- Correctly reporting that information is MISSING is a completion, not a failure. When the
  success conditions call for "the information is not available" or an answer of "no", an
  assistant that establishes this and says so plainly scores 2.

conversation_efficiency (0–2):
- 2: Completes the task in one or very few steps without unnecessary clarification questions or detours. Only asks for clarification when the request is genuinely ambiguous or missing required information that cannot be inferred from context.
- 1: Minor inefficiency (e.g., an unnecessary clarification, a redundant step, or a slightly longer interaction) but still reasonably efficient overall.
- 0: Multiple unnecessary turns, redundant questions, or inefficient behavior that meaningfully delays task completion.
  Examples:
  - If the user's request is already fully specified and the assistant asks a clarification question → lower score.
  - If the request is ambiguous and no information in the user's personal context resolves it, a clarification question is appropriate → do *not* penalize.
- Judge the number of CONVERSATIONAL turns with the user, not the number of tool calls. Several
  tool calls inside one turn is normal and efficient. Thorough retrieval is not a detour; only
  count steps that made the user wait or answer something they need not have.

no_hallucination_score (0–2):
- 2: No hallucinations; all statements are grounded in tool output or user-provided context.
- 1: Small or harmless hallucination with no effect on correctness.
- 0: Major hallucination or fabricated information that affects correctness.
- Saying "I could not find X" when the tools genuinely returned nothing is NOT a hallucination —
  it is an accurate report. Only score down for content the assistant invented or asserted
  beyond what the tool results and the user support.
- Hallucination covers INVENTED TOOLS and INVENTED ARGUMENTS as well as invented prose.
  Calling a tool the assistant was never given, or passing it a value nobody supplied, is
  fabrication just as much as stating a false fact to the user:
  - A tool name that exists nowhere in the list and is not a real tool at all (e.g. inventing
    `get_events` when only `get_all_calendars` and `search_calendar_events` were offered) is a
    fabrication → 0.
  - A real tool name that was simply not offered for this scenario is a lesser error — the
    assistant misremembered the menu rather than inventing a capability → at most 1.
  - A FACTUAL argument the assistant made up rather than retrieved — a recipient address, a
    phone number, an entity id, a date/time, a location — is a fabrication, and a worse one
    when passed to a write tool (`send_*`, `create_*`, `modify_*`, `remove_*`), because it
    acts on the fabrication instead of merely saying it. Score 0 when such a value appears in
    no tool result and was not given by the user.
  - Judge only values that had to be LOOKED UP. Content the assistant is expected to compose —
    an email body, a message, a subject line, an event title — is its job to write, not
    something it can hallucinate by inventing. Judge composed text on whether it misstates
    facts, not on whether its wording appears somewhere earlier.
  - A plausible-looking value that happens to be WRONG (the right kind of thing, but not the
    one the context supports — e.g. addressing the reply to the wrong participant) is a
    misreading rather than an invention: that belongs to
    `information_retrieval_capability`, and to this dimension only if the assistant then
    asserts it to the user as fact.
  This is scored independently of `tool_call_capability`. The two dimensions are answering
  different questions: "was this the right tool, called competently?" and "did the assistant
  make something up?"

### SPECIAL RULE FOR DESTRUCTIVE ACTIONS

If the assistant performed an irreversible or destructive action (e.g., deleting a calendar event)
without explicit user request OR without resolving ambiguity,
treat this as a serious error when scoring:
- tool_call_capability
- task_completion
- no_hallucination_score

### EVIDENCE REQUIREMENT

When writing `review_reason`, reference at least one `sandbox_message_index` for each major judgment (e.g., intent match, tool choice, task success).
Examples:
- "✓ Intent match: see index 17 (create_calendar_event … 'Review Writing')"
- "✗ Unrequested deletion: see indices 13–16 (remove_calendar_event …)"

### OUTPUT SCHEMA

Output **only** the following JSON object (no extra text):

{{
  "review_reason": "...",
  "tool_call_capability": 0,
  "information_retrieval_capability": 0,
  "task_completion": 0,
  "conversation_efficiency": 0,
  "no_hallucination_score": 0
}}

""".strip()


@define
class EvaluationLLM:
    """Defining the process needed for evaluating a completed ExecutionContext via LLM judge against reasoning and success conditions"""

    # Reasoning Monologue on chain-of-chain for the agent to complete the task
    reasoning: Optional[str] = None
    # User facing minimal success criteria for the success of the interactions
    success_conditions: Optional[List[Dict[str, str]]] = None
    # Annotator-Selected Personal Context Relevant to the Task
    related_entities: Optional[Dict[str, List[Any]]] = None

    def build_eval_task(
        self,
        execution_context: ExecutionContext,
        stopped_early_reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        sandbox_messages = execution_context._dbs["SANDBOX"].to_dicts()

        reference_time_message = next(
            (
                m
                for m in sandbox_messages
                if m["sender"] == "SYSTEM" and "Today is " in m["content"]
            ),
            None,
        )
        reference_time_index = (
            reference_time_message["sandbox_message_index"]
            if reference_time_message
            else 0
        )
        user_goal_message = next(
            (
                m
                for m in sandbox_messages
                if m["sender"] == "SYSTEM"
                and "You are no longer an assistant." in m["content"]
                and m["sandbox_message_index"] > reference_time_index
            ),
            None,
        )
        user_goal = ""
        if user_goal_message:
            content = user_goal_message["content"]
            user_goal = content[
                content.find("You are User A") : content.find(
                    "You do not have any more information."
                )
            ]
            if "You are User A" in user_goal:
                user_goal_dry = (". ".join(user_goal.split(".")[1:])).strip()
            else:
                user_goal_dry = user_goal

        user_queries = [
            m
            for m in sandbox_messages
            if m["sender"] == "USER"
            and m["sandbox_message_index"] > reference_time_index
        ]

        first_user_query = user_queries[0]["content"] if user_queries else ""
        first_user_query_index = (
            user_queries[0]["sandbox_message_index"] if user_queries else 0
        )
        conversation_history = [
            m
            for m in sandbox_messages
            if m["sandbox_message_index"] >= first_user_query_index
        ]

        execution_context_dbs_to_dicts = execution_context.to_dict().get("_dbs", {})

        mentioned_entities_ids_with_tool_call = []
        for message in conversation_history:
            if (
                (message.get("sender") == "EXECUTION_ENVIRONMENT")
                and (message.get("recipient") == "AGENT")
                and isinstance(message.get("tool_trace"), list)
            ):
                for tool_trace_str in message["tool_trace"]:
                    tool_trace = json.loads(tool_trace_str)
                    if ("search" in tool_trace.get("tool_name")) or (
                        "get_all" in tool_trace.get("tool_name")
                        or ("end_conversation" == tool_trace.get("tool_name"))
                    ):
                        continue
                    result_entity_id = tool_trace.get("result")
                    # print(f'entity found {tool_trace}')
                    if result_entity_id:
                        result_mentioned_entity = (
                            find_entity_in_execution_context_by_id(
                                result_entity_id,
                                dbs_to_search=execution_context_dbs_to_dicts,
                            )
                        )
                        mentioned_entities_ids_with_tool_call.append(
                            {
                                "sandbox_message_index": message.get(
                                    "sandbox_message_index"
                                ),
                                "tool_name": tool_trace.get("tool_name"),
                                "result_entity_id": result_entity_id,
                                "result_entity_content": result_mentioned_entity,
                            }
                        )
                    else:
                        # check entity id mentionedin arguments
                        arguments = tool_trace.get("arguments")
                        arguments_entity_ids = [
                            param_value
                            for param_name, param_value in arguments.items()
                            if "_id" in param_name and param_value
                        ]
                        arguments_mentioned_entity = [
                            find_entity_in_execution_context_by_id(
                                entity_id, dbs_to_search=execution_context_dbs_to_dicts
                            )
                            for entity_id in flatten_list(arguments_entity_ids)
                        ]

                        mentioned_entities_ids_with_tool_call.append(
                            {
                                "sandbox_message_index": message.get(
                                    "sandbox_message_index"
                                ),
                                "tool_name": tool_trace.get("tool_name"),
                                "argument_entity_id": flatten_list(
                                    arguments_entity_ids
                                ),
                                "argument_entity_content": arguments_mentioned_entity,
                            }
                        )

        task = {
            "reference_time_str": reference_time_message["content"]
            if reference_time_message
            else "",
            "user_goal": user_goal_dry,
            "user_goal_prompt": user_goal,
            "query": first_user_query,
            "conversation_history": conversation_history,
            "mentioned_entities": mentioned_entities_ids_with_tool_call,
            "success_conditions": self.success_conditions,
            "reasoning": self.reasoning,
            # Exception type that cut the trajectory short, so the judge can grade
            # progress-so-far instead of penalising a missing final turn. None for a
            # normal run.
            "stopped_early_reason": stopped_early_reason,
            # The tools the agent was actually offered, i.e. the scenario's
            # tool_allow_list after filtering. Without this the judge has to infer
            # the menu from the trajectory, which means it can only notice an
            # unavailable tool reactively (when a call errors) and may penalise the
            # agent for not using something that was never on offer.
            "available_tools": sorted(
                execution_context.get_available_tools(scrambling_allowed=True)
            ),
        }
        if self.related_entities:
            task.update(self.related_entities)
        return task

    def check_llm_performance(
        self, eval_task: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        prompt = eval_llm_prompt(eval_task)
        # `required` in the schema is only a hint, so a reply can come back with a
        # dimension missing. The SDK's own retry covers transport errors, not this, so
        # retry the incomplete reply here before giving up and leaving the scenario
        # unjudged.
        for attempt in range(JUDGE_MAX_INCOMPLETE_ATTEMPTS):
            result = self._judge_once(prompt)
            if _judge_scores_are_complete(result, logger_name=self.__class__.__name__):
                return result
            if attempt == JUDGE_MAX_INCOMPLETE_ATTEMPTS - 1:
                getLogger(__name__).warning(
                    "%s: judge reply still incomplete after %d attempts; leaving the "
                    "scenario unjudged",
                    self.__class__.__name__,
                    JUDGE_MAX_INCOMPLETE_ATTEMPTS,
                )
        return None

    def _judge_once(self, prompt: str) -> Optional[dict[str, Any]]:
        """Score one trajectory with a single judge call."""
        load_dotenv()
        system_prompt = "You are a JSON-generating assistant for task evaluation."
        # Public-API LLM grader. Backend is selectable via ASTRA_LLM_EVAL_BACKEND
        # ("openai" default, or "anthropic"); both use public endpoints only.
        backend = os.getenv("ASTRA_LLM_EVAL_BACKEND", "openai").lower()
        content: Optional[str]
        if backend == "anthropic":
            import anthropic

            anthropic_client = anthropic.Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
            anthropic_response = anthropic_client.messages.create(
                model=os.getenv("ASTRA_LLM_EVAL_MODEL", "claude-opus-4-8"),
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}],
            )
            block = (
                anthropic_response.content[0] if anthropic_response.content else None
            )
            content = getattr(block, "text", None)
        else:
            openai_client = openai.OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url="https://api.openai.com/v1",
                timeout=300,
            )
            openai_response = openai_client.chat.completions.create(
                model=os.getenv("ASTRA_LLM_EVAL_MODEL", "o3-2025-04-16"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
            )
            content = openai_response.choices[0].message.content
        return _parse_judge_json(content)

    def prepare_eval_task(
        self,
        execution_context: ExecutionContext,
        stopped_early_reason: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Build the judge input without calling the LLM, or None if judging is off.

        Split out from `evaluate` so the expensive half can run somewhere else. The
        cheap half needs the live ExecutionContext, which only exists inside the
        worker that played the scenario; the returned dict is plain data and carries
        everything the judge needs, so the LLM calls can be batched in the parent
        process after the scenario pool has drained. That keeps the judge out of the
        per-scenario timeout window.
        """
        if not self.reasoning and not self.success_conditions:
            # No ground truth to judge against — llm_evaluation is off.
            return None
        return self.build_eval_task(execution_context, stopped_early_reason)

    @staticmethod
    def score_eval_task(eval_task: Optional[Dict[str, Any]]) -> EvaluationLLMResult:
        """Score a prepared judge input. Safe to call outside the scenario worker.

        Static because the caller runs after the scenario pool has drained and holds
        only the plain-data eval task, not the EvaluationLLM that produced it.
        `check_llm_performance` reads no instance state.
        """
        eval_result = (
            EvaluationLLM().check_llm_performance(eval_task)
            if eval_task is not None
            else None
        )
        if eval_result:
            return EvaluationLLMResult(
                review_reason=eval_result.get("review_reason"),
                tool_call_capability=eval_result.get("tool_call_capability"),
                information_retrieval_capability=eval_result.get(
                    "information_retrieval_capability"
                ),
                task_completion=eval_result.get("task_completion"),
                conversation_efficiency=eval_result.get("conversation_efficiency"),
                no_hallucination_score=eval_result.get("no_hallucination_score"),
            )
        return EvaluationLLMResult()

    def evaluate(
        self,
        execution_context: ExecutionContext,
        stopped_early_reason: Optional[str] = None,
    ) -> EvaluationLLMResult:
        """Evaluate a completed ExecutionContext

        Calculate Milestone and Minefield similarities, combine them.
        Calculate effective turn count.

        Args:
            execution_context:      ExecutionContext to be evaluated
            stopped_early_reason:   Exception type that cut the trajectory short, so the
                                    judge grades progress-so-far instead of penalising a
                                    missing final turn. None for a normal run.

        Returns:
            An EvaluationLLMResult object containing the mean similarity, as well as milestone mapping and finegrained
            similarity

        Raises:
            IndexError: No Milestone found
        """
        if not self.reasoning and not self.success_conditions:
            # skip LLM eval since ground truth information is missing
            eval_result = None
        else:
            eval_task = self.build_eval_task(execution_context, stopped_early_reason)
            eval_result = self.check_llm_performance(eval_task)

        if eval_result:
            return EvaluationLLMResult(
                review_reason=eval_result.get("review_reason"),
                tool_call_capability=eval_result.get("tool_call_capability"),
                information_retrieval_capability=eval_result.get(
                    "information_retrieval_capability"
                ),
                task_completion=eval_result.get("task_completion"),
                conversation_efficiency=eval_result.get("conversation_efficiency"),
                no_hallucination_score=eval_result.get("no_hallucination_score"),
            )
        else:
            return EvaluationLLMResult(
                review_reason=None,
                tool_call_capability=None,
                information_retrieval_capability=None,
                task_completion=None,
                conversation_efficiency=None,
                no_hallucination_score=None,
            )


def compute_milestone_completion_score(
    milestones: Sequence["Milestone"],
    milestone_mapping: "OrderedDict[int, Tuple[int, float]]",
    minefield_similarity: float = 0,
) -> Optional[float]:
    """Mean similarity across milestones tagged ``response_generation`` or ``payload_generation``.

    Mirrors the notebook-level metric in
    ``notebooks/update_complexity_levels_from_trajectories.py``: a milestone
    contributes its score when any of its snapshot constraints either targets
    the user (``response_generation``) or writes sandbox state via an
    addition/removal/update/contains similarity (``payload_generation``). A
    milestone carrying both tags contributes twice, matching the notebook's
    list-concatenation semantics.

    A triggered minefield nullifies the score, the same way it nullifies
    ``EvaluationResult.similarity``: an agent that did something forbidden did not
    complete the task, however much of it the milestones credit. ``None`` still wins
    over that, because a scenario with no tagged milestone has no completion metric
    to nullify and must stay out of the aggregates rather than entering them as 0.

    Returns ``None`` when no milestone in the scenario carries either tag.
    """
    _PAYLOAD_CONSTRAINTS = {
        "addition_similarity",
        "removal_similarity",
        "update_similarity",
        "contains_presence_similarity",
        "not_contains_presence_similarity",
    }

    def _constraint_name(constraint: SnapshotConstraint) -> str:
        snap = constraint.snapshot_constraint
        if hasattr(snap, "func"):
            return str(snap.func.__name__)
        if hasattr(snap, "__name__"):
            return str(snap.__name__)
        return str(snap)

    def _recipient(constraint: SnapshotConstraint) -> str:
        if not isinstance(constraint.target_dataframe, pl.DataFrame):
            return "unknown"
        try:
            r = constraint.target_dataframe["recipient"][0]
        except Exception:
            return "unknown"
        return r.name.lower() if isinstance(r, RoleType) else str(r).lower()

    # The resume path reads the mapping back out of execution_context.json, where JSON
    # has turned every milestone index into a string. Keyed lookups below would all miss
    # and the score would come back None for every resumed scenario.
    mapping_by_index = {int(key): value for key, value in milestone_mapping.items()}

    scores: List[float] = []
    for milestone_idx, milestone in enumerate(milestones):
        entry = mapping_by_index.get(milestone_idx)
        if entry is None:
            continue
        _, score = entry
        tags: set[str] = set()
        for constraint in milestone.snapshot_constraints:
            if _recipient(constraint) == "user":
                tags.add("response_generation")
            elif _constraint_name(constraint) in _PAYLOAD_CONSTRAINTS:
                tags.add("payload_generation")
        if "response_generation" in tags:
            scores.append(score)
        if "payload_generation" in tags:
            scores.append(score)
    if not scores:
        return None
    if minefield_similarity != 0:
        return 0.0
    return sum(scores) / len(scores)


def milestone_tagger(extensions: List[Any], output_dir: Path) -> None:
    from astra_tool_sandbox.common.scenario import ScenarioExtension

    if not all(isinstance(ext, ScenarioExtension) for ext in extensions):
        raise TypeError("All items in extensions must be ScenarioExtension")

    """Helper function to get the tags for each scenario"""

    def extract_constraint_name(constraint: SnapshotConstraint) -> str:
        if hasattr(constraint.snapshot_constraint, "func"):
            return str(constraint.snapshot_constraint.func.__name__)
        elif hasattr(constraint.snapshot_constraint, "__name__"):
            return str(constraint.snapshot_constraint.__name__)
        else:
            return str(constraint.snapshot_constraint)

    def extract_recipient(df: pl.DataFrame) -> str:
        try:
            recipient_val = df["recipient"][0]
            if isinstance(recipient_val, RoleType):
                return recipient_val.name.lower()
            return str(recipient_val).lower()
        except Exception:
            return "unknown"

    scenario_milestone_category_mapping: Dict[str, Any] = {}
    scenario_tags: Dict[str, Any] = {}
    for scenario in extensions:
        scenario_name = scenario.name
        scenario_milestone_category_mapping[scenario_name] = {}
        scenario_tags[scenario_name] = scenario.tags
        for i, milestone in enumerate(scenario.milestones):
            snapshot_constraint_names = []
            recipients = []

            for constraint in milestone.snapshot_constraints:
                snapshot_constraint_names.append(extract_constraint_name(constraint))
                if isinstance(constraint.target_dataframe, pl.DataFrame):
                    recipients.append(extract_recipient(constraint.target_dataframe))

            scenario_milestone_category_mapping[scenario_name][str(i)] = {
                "snapshot_constraints": snapshot_constraint_names,
                "recipient": recipients,
            }

    milestone_category: Dict[str, Any] = {}

    for scenario_name, mapped_scenario in scenario_milestone_category_mapping.items():
        milestone_category[scenario_name] = {}
        milestone_category[scenario_name]["scenario_tags"] = scenario_tags[
            scenario_name
        ]
        for milestone_id, mapped_milestone in mapped_scenario.items():
            tags = set()
            for mapped_constraint, recipient in zip(
                mapped_milestone["snapshot_constraints"], mapped_milestone["recipient"]
            ):
                if recipient == "user":
                    tags.add("response_generation")
                elif mapped_constraint in [
                    "addition_similarity",
                    "removal_similarity",
                    "update_similarity",
                    "contains_presence_similarity",
                    "not_contains_presence_similarity",
                ]:
                    tags.add("payload_generation")
                elif mapped_constraint == "tool_trace_dependant_similarity":
                    tags.add("retrieval")
                else:
                    tags.add("tool_calling")

            milestone_category[scenario_name][milestone_id] = sorted(tags)

    # Trailing newline so the regenerated file matches what the
    # end-of-file-fixer pre-commit hook expects.
    content = json.dumps(milestone_category, indent=4) + "\n"
    output_path = Path(output_dir) / "milestone_tags.json"
    # Only write when the tags changed: this runs every time scenarios load, and the
    # package directory may be read-only (or a pip-managed install that must not gain
    # untracked files).
    if output_path.exists() and output_path.read_text() == content:
        return
    try:
        output_path.write_text(content)
    except OSError as e:
        LOGGER.warning("Could not write %s: %s", output_path, e)
