# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
from __future__ import annotations

import calendar
import datetime
import functools
import json
import logging
import re
import unicodedata
import uuid
from contextlib import contextmanager
from inspect import getsource, isfunction, signature
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    List,
    Literal,
    Optional,
    TypeVar,
    Union,
)
from zoneinfo import ZoneInfo

import polars as pl
from decorator import decorate
from rapidfuzz import fuzz, process, utils
from strenum import StrEnum
from typing_extensions import Protocol

from astra_tool_sandbox.common.execution_context import (
    DatabaseNamespace,
    RoleType,
    get_current_context,
    new_context_with_attribute,
)
from astra_tool_sandbox.common.tool_discovery import ToolBackend

T = TypeVar("T")

LOGGER = logging.getLogger(__name__)


def normalize_notgiven(x: Union[str, NotGiven]) -> Optional[str]:
    return None if isinstance(x, NotGiven) else x


# Typographic -> ASCII fold used before string-similarity matching so that
# LLM output containing curly apostrophes / quotes / dashes / ellipsis matches
# milestone expected strings authored with plain ASCII punctuation. Kept
# minimal and semantic-preserving: does not strip punctuation ("he'll" stays
# distinct from "hell") and does not change case.
_PUNCT_FOLD_TABLE = str.maketrans(
    {
        "‘": "'",  # left single quotation mark
        "’": "'",  # right single quotation mark (curly apostrophe)
        "‚": "'",  # single low-9 quotation mark
        "‛": "'",  # single high-reversed-9 quotation mark
        "′": "'",  # prime
        "“": '"',  # left double quotation mark
        "”": '"',  # right double quotation mark
        "„": '"',  # double low-9 quotation mark
        "″": '"',  # double prime
        "–": "-",  # en dash
        "—": "-",  # em dash
        "−": "-",  # minus sign
        "…": "...",  # horizontal ellipsis
        " ": " ",  # non-breaking space
        " ": " ",  # narrow no-break space
        " ": " ",  # thin space
    }
)


#: Markdown emphasis runs. Agents routinely bold the very value a milestone grades
#: ("**7:00 PM**", "***Two Hearts with one Stone***"), which breaks a contiguous
#: substring check for a purely presentational reason. Stripping the markers from both
#: sides compares content to content. Applied only to `*`, `_` and backtick runs, so
#: prose punctuation is untouched.
_MARKDOWN_EMPHASIS = re.compile(r"[*_`]+")

#: Ordinal suffixes on day numbers: "February 14th, 1991" vs a milestone target of
#: "February 14, 1991". The suffix carries no information the target lacks, and folding
#: it on both sides makes the two forms comparable. Bounded to 1-2 digits so it cannot
#: touch identifiers.
_ORDINAL_SUFFIX = re.compile(r"\b(\d{1,2})(st|nd|rd|th)\b", re.IGNORECASE)


def normalize_text_for_matching(text: Any) -> Any:
    """Fold typographic Unicode punctuation to ASCII for string similarity.

    Applied to both the expected value and the observed column content before
    comparison. NFKC first (handles fullwidth / ligature compatibility forms),
    then an explicit table for common typographic punctuation (NFKC alone does
    not fold U+2019 curly apostrophe). Non-string inputs pass through
    unchanged so callers can apply this unconditionally.

    Also strips markdown emphasis and folds ordinal day suffixes. Both are
    presentational: scenarios where the LLM judge scored a full pass but the milestones
    scored zero have failed for no other reason than `**5** emails` not containing
    `5 email`, or `February 14th, 1991` not containing `February 14, 1991`. Applied to
    expected and observed alike, so it can only make equivalent forms compare equal.
    """
    if not isinstance(text, str):
        return text
    folded = unicodedata.normalize("NFKC", text).translate(_PUNCT_FOLD_TABLE)
    folded = _MARKDOWN_EMPHASIS.sub("", folded)
    return _ORDINAL_SUFFIX.sub(r"\1", folded)


def parse_duration_to_hms(text: str) -> str:
    # Lowercase and normalize
    text = text.lower().strip()
    # Pre-check: already in HH:mm:ss format
    if re.fullmatch(r"\d{1,2}:\d{2}:\d{2}", text):
        return text  # assumed valid format like "01:30:00"

    # Match patterns
    hours = minutes = seconds = 0

    h_match = re.search(r"(\d+)\s*(h|hour|hours)", text)
    m_match = re.search(r"(\d+)\s*(m|minute|minutes)", text)
    s_match = re.search(r"(\d+)\s*(s|second|seconds)", text)

    if h_match:
        hours = int(h_match.group(1))
        matched = True
    if m_match:
        minutes = int(m_match.group(1))
        matched = True
    if s_match:
        seconds = int(s_match.group(1))
        matched = True

    if not matched:
        raise ValueError(
            f"Failed to parse duration string: '{text}'. "
            "Expected format like 'HH:mm:ss', '30 minutes', '1 hour 5 minutes', or '2h 5m'."
        )
    td = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    total_seconds = int(td.total_seconds())

    # Format to HH:mm:ss
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02}:{m:02}:{s:02}"


def is_phone_number(s: str) -> bool:
    """
    Checks if a string is a valid phone number.

    Accepts formats like:
    - +1 555-234-5678
    - +44 20 7946 0958
    - 555-234-5678-9012
    - 1234567890
    - 55589012345678 (continuous digits)
    - 1(555) 234-5678-9012 (with parentheses)

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string matches a phone number pattern.
    """
    # Original pattern for formatted phone numbers (spaces, hyphens)
    formatted_pattern = re.compile(r"^\+?\d{1,3}?([ -]?\d{2,4}){2,5}$")

    # Pattern for parentheses format like 1(555) 234-5678-9012
    parentheses_pattern = re.compile(
        r"^\+?\d{1,3}?\(\d{3}\)[ -]?\d{3}[ -]?\d{4}([ -]?\d{4})?$"
    )

    # New pattern for continuous digit strings (7-15 digits, optionally starting with +)
    continuous_pattern = re.compile(r"^\+?\d{7,15}$")

    return bool(
        formatted_pattern.match(s)
        or parentheses_pattern.match(s)
        or continuous_pattern.match(s)
    )


def normalize_phone_number(phone: str) -> str:
    """
    Normalize a phone number by extracting only digits.

    This function removes all non-digit characters from a phone number,
    allowing for flexible matching regardless of formatting.

    Args:
        phone (str): The phone number to normalize.

    Returns:
        str: The normalized phone number containing only digits.

    Examples:
        "+1 555-890-1234-5678" -> "15558901234567"
        "+155589012345678" -> "155589012345678"
        "55589012345678" -> "55589012345678"
    """
    if not isinstance(phone, str):
        return ""
    # Extract only digits
    return "".join(c for c in phone if c.isdigit())


def normalize_phone_number_filter(
    dataframe: pl.DataFrame, column_name: str, value: str, **kwargs: Any
) -> pl.DataFrame:
    """Custom filter that normalizes phone numbers before exact matching.

    Args:
        dataframe: Polars DataFrame to filter
        column_name: Name of the column containing phone numbers
        value: Phone number value to match against
        **kwargs: Additional keyword arguments (unused)

    Returns:
        Filtered dataframe with normalized phone number matching
    """
    import polars as pl

    if value is None:
        return dataframe.filter(pl.col(column_name).is_null())

    if is_phone_number(value):
        normalized_value = normalize_phone_number(value)
        return dataframe.filter(
            pl.col(column_name).map_elements(
                lambda x: normalize_phone_number(x)
                if isinstance(x, str) and is_phone_number(x)
                else x,
                return_dtype=pl.Utf8,
            )
            == normalized_value
        )
    else:
        return dataframe.filter(pl.col(column_name) == value)


def normalize_phone_numbers_in_list_filter(
    dataframe: pl.DataFrame, column_name: str, value: Any, **kwargs: Any
) -> pl.DataFrame:
    """Custom filter that normalizes phone numbers in lists before matching.

    Combines phone number normalization with sublist filtering to handle both
    phone numbers and other addresses (like emails).

    Args:
        dataframe: Polars DataFrame to filter
        column_name: Name of the column containing lists of phone numbers/addresses
        value: List of phone numbers/addresses to match against
        **kwargs: Additional keyword arguments (unused)

    Returns:
        Filtered dataframe with normalized phone number list matching
    """
    import polars as pl

    # Handle case where value is None
    if value is None:
        return dataframe.filter(pl.col(column_name).is_null())

    # Normalize the search list (phone numbers and lowercase for other addresses)
    normalized_search_set = set()
    for address in value:
        if isinstance(address, str) and is_phone_number(address):
            normalized_search_set.add(normalize_phone_number(address))
        else:
            normalized_search_set.add(
                address.lower() if isinstance(address, str) else address
            )

    # Use Polars expression to filter
    def check_contains_all(addresses_series: Any) -> bool:
        # addresses_series is a Series containing a list of addresses
        if addresses_series is None:
            return False

        # Normalize each address in the row
        normalized_row_set = set()
        for addr in addresses_series:
            if isinstance(addr, str) and is_phone_number(addr):
                normalized_row_set.add(normalize_phone_number(addr))
            else:
                normalized_row_set.add(addr.lower() if isinstance(addr, str) else addr)

        # Check if search set is subset of row set
        return normalized_search_set.issubset(normalized_row_set)

    return dataframe.filter(
        pl.col(column_name).map_elements(check_contains_all, return_dtype=pl.Boolean)
    )


def is_email_address(s: str) -> bool:
    """
    Checks if a string is a valid email address.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string is an email address, False otherwise.
    """
    email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    return bool(email_pattern.match(s))


def sorted_unique(items: Iterable[Optional[str]]) -> List[str]:
    """
    Combine, deduplicate, filter out None, and sort a list of items.

    Args:
        items: An iterable of optional items (e.g. list with possible duplicates or None)

    Returns:
        A sorted list with unique, non-None items.
    """
    return sorted({item for item in items if item is not None})


def generate_date_surface_forms(
    date_iso: str,
) -> list[str]:
    """
    Given an ISO date string, returns common surface forms like:
    - February 14
    - Feb 14
    - 14 February
    - 14 Feb
    - 02/14
    - 2/14
    - Feb. 14
    - 14th of February
    """
    try:
        dt = datetime.datetime.fromisoformat(date_iso)
        month_full = dt.strftime("%B")  # February
        month_abbr = dt.strftime("%b")  # Feb
        month_abbr_dot = month_abbr + "."
        day = dt.day
        day_padded = dt.strftime("%d")  # 14
        day_ordinal = f"{day}th"

        return [
            f"{month_full} {day}",  # February 14
            f"{month_abbr} {day}",  # Feb 14
            f"{month_abbr_dot} {day}",  # Feb. 14
            f"{day} {month_full}",  # 14 February
            f"{day} {month_abbr}",  # 14 Feb
            f"{day_padded}/{dt.month:02d}",  # 14/02 (reversed but can be added if needed)
            f"{dt.month:02d}/{day_padded}",  # 02/14
            f"{dt.month}/{day}",  # 2/14
            f"{day_ordinal} of {month_full}",  # 14th of February
        ]
    except Exception:
        return []


def load_str_time_to_timestamp(
    datetime_: Optional[str], time_zone_info: str = "America/Los_Angeles"
) -> Optional[float]:
    if not datetime_:
        return None

    dt: datetime.datetime
    try:
        dt = datetime.datetime.fromisoformat(datetime_).replace(
            tzinfo=ZoneInfo(time_zone_info)
        )
    except ValueError:
        dt = datetime.datetime.strptime(datetime_, "%Y-%m-%dT%H:%M:%SZ")
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo(time_zone_info))

    return dt.timestamp()


def load_str_time_to_datetime(
    datetime_: Optional[str], time_zone_info: str = "America/Los_Angeles"
) -> Optional[datetime.datetime]:
    if datetime_:
        try:
            datetime_output = datetime.datetime.fromisoformat(datetime_)
        except ValueError:
            datetime_output = datetime.datetime.strptime(
                datetime_, "%Y-%m-%dT%H:%M:%SZ"
            )
        if datetime_output.tzinfo is None:
            datetime_output = datetime_output.replace(tzinfo=ZoneInfo(time_zone_info))
        return datetime_output
    else:
        return None


def load_str_time_to_datetime_iso_8601(
    datetime_: Optional[str], time_zone_info: str = "America/Los_Angeles"
) -> Optional[str]:
    if not datetime_:
        return None

    tz = ZoneInfo(time_zone_info)

    try:
        dt = datetime.datetime.fromisoformat(datetime_)
        if dt.tzinfo is not None:
            return dt.astimezone(tz).isoformat()
    except ValueError:
        # Try parsing UTC format with 'Z'
        try:
            dt = datetime.datetime.strptime(datetime_, "%Y-%m-%dT%H:%M:%SZ")
            dt = dt.replace(tzinfo=ZoneInfo("UTC")).astimezone(tz)
            return dt.isoformat()
        except ValueError:
            raise ValueError(f"Unrecognized datetime format: {datetime_}")

    # At this point, dt is naive — assume it's in local time of the given timezone
    dt = dt.replace(tzinfo=tz)
    return dt.isoformat()


def ymd_to_posix(date_str: str) -> float:
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    dt_timestamp = dt.timestamp()
    dt_timestamp = (
        dt_timestamp // 1e6 if len(str(int(dt_timestamp))) == 16 else dt_timestamp
    )
    return dt_timestamp


def flatten_list(nested_list: List[Any]) -> List[Any]:
    if all(not isinstance(item, list) for item in nested_list):
        return nested_list
    return [e for sublist in nested_list for e in sublist]


def format_date_string(
    reference_time_str: str, time_zone_info: str = "America/Los_Angeles"
) -> str:
    try:
        reference_time = datetime.datetime.fromisoformat(reference_time_str)
    except ValueError:
        try:
            reference_time = datetime.datetime.strptime(
                reference_time_str, "%Y-%m-%d %H:%M:%S"
            )
        except ValueError:
            raise ValueError("Reference time is not in correst ISO8601 format")
    if reference_time.tzinfo is None:
        # raise ValueError("Reference time must include timezone information")
        reference_time.replace(tzinfo=ZoneInfo(time_zone_info))
    # Remove microsecond to simplify ISO8601 representation.
    reference_time = reference_time.replace(microsecond=0)
    weekday = calendar.day_name[reference_time.weekday()]
    month = calendar.month_name[reference_time.month]
    return f"Today is {weekday}, {month} {reference_time.day}, {reference_time.year}.\n Current time (ISO format): {reference_time.isoformat()}."


# Taken from openai._types
# Sentinel class used until PEP 0661 is accepted
class NotGiven:
    """
    A sentinel singleton class used to distinguish omitted keyword arguments
    from those passed in with the value None (which may have different behavior).

    For example:

    ```py
    def search(
        a: Union[int, NotGiven, None] = NotGiven(),
        b: Union[int, NotGiven, None] = NotGiven(),
    ): ...


    search(a=1, b=2)  # Search in database with constraint a == 1, b==2
    search(a=None, b=3)  # Search in database with constraint a == None, b==3
    search(b=4)  # Search in database with constraint b==4
    ```
    """

    def __bool__(self) -> Literal[False]:
        return False

    def __repr__(self) -> str:
        return "NOT_GIVEN"


NOT_GIVEN = NotGiven()


class DataframeFilterMethodType(Protocol):
    """Callable type def for Dataframe filtering functions."""

    def __call__(
        self,
        dataframe: pl.DataFrame,
        column_name: str,
        value: Any,
        **kwargs: Union[int, Any],
    ) -> pl.DataFrame: ...


def exact_match_filter_dataframe(
    dataframe: pl.DataFrame, column_name: str, value: Any, **kwargs: Union[int, Any]
) -> pl.DataFrame:
    """Filter dataframe by exact matching value on 1 column

    Args:
    ----
        dataframe:      Dataframe to filter
        column_name:    Name of column
        value:          Value to match against

    Returns:
    -------
        Filtered dataframe

    """
    return dataframe.filter(pl.col(column_name) == value)


def lt_eq_filter_dataframe(
    dataframe: pl.DataFrame, column_name: str, value: Any, **kwargs: Union[int, Any]
) -> pl.DataFrame:
    """Filter dataframe for rows whose column_name are less than or equal to value. The value must implement __lt__.

    Args:
    ----
        dataframe:      Dataframe to filter
        column_name:    Name of column
        value:          Upperbound of column value

    Returns:
    -------
        Filtered dataframe

    """
    return dataframe.filter(pl.col(column_name) <= value)


def gt_eq_filter_dataframe(
    dataframe: pl.DataFrame, column_name: str, value: Any, **kwargs: Union[int, Any]
) -> pl.DataFrame:
    """Filter dataframe for rows whose column_name are greater than or equal to value. The value must implement __gt__.

    Args:
    ----
        dataframe:      Dataframe to filter
        column_name:    Name of column
        value:          Lowerbound of column value

    Returns:
    -------
        Filtered dataframe

    """
    return dataframe.filter(pl.col(column_name) >= value)


def hms_to_seconds(hms: str) -> int:
    h, m, s = map(int, hms.split(":"))
    return h * 3600 + m * 60 + s


def gt_eq_duration_filter_dataframe(
    dataframe: pl.DataFrame,
    column_name: str,
    value: Any,
    **kwargs: Union[int, Any],
) -> pl.DataFrame:
    """
    Filters the DataFrame to only rows where the 'HH:mm:ss' duration in column_name >= value.

    Args:
    ----
        dataframe:      Polars DataFrame to filter
        column_name:    Name of column with 'HH:mm:ss' strings
        value:          Lower bound duration as string in 'HH:mm:ss' format
        **kwargs:       Unused (for signature consistency)

    Returns:
    -------
        Filtered DataFrame
    """
    if not isinstance(value, str) or not value.count(":") == 2:
        raise ValueError(f"Expected value in 'HH:mm:ss' format, got: {value}")

    min_seconds = hms_to_seconds(value)

    return (
        dataframe.with_columns(
            pl.col(column_name)
            .map_elements(hms_to_seconds, return_dtype=pl.Int64)
            .alias("__duration_sec")
        )
        .filter(pl.col("__duration_sec") >= min_seconds)
        .drop("__duration_sec")
    )


def lt_eq_duration_filter_dataframe(
    dataframe: pl.DataFrame,
    column_name: str,
    value: Any,
    **kwargs: Union[int, Any],
) -> pl.DataFrame:
    """
    Filters the DataFrame to only rows where the 'HH:mm:ss' duration in column_name <= value.

    Args:
    ----
        dataframe:      Polars DataFrame to filter
        column_name:    Name of column with 'HH:mm:ss' strings
        value:          Upper bound duration as string in 'HH:mm:ss' format
        **kwargs:       Unused (for signature consistency)

    Returns:
    -------
        Filtered DataFrame
    """
    if not isinstance(value, str) or not value.count(":") == 2:
        raise ValueError(f"Expected value in 'HH:mm:ss' format, got: {value}")

    max_seconds = hms_to_seconds(value)

    return (
        dataframe.with_columns(
            pl.col(column_name)
            .map_elements(hms_to_seconds, return_dtype=pl.Int64)
            .alias("__duration_sec")
        )
        .filter(pl.col("__duration_sec") <= max_seconds)
        .drop("__duration_sec")
    )


def exact_match_filter_dataframe_case_insensitive(
    dataframe: pl.DataFrame, column_name: str, value: Any, **kwargs: Union[int, Any]
) -> pl.DataFrame:
    """Filter dataframe by exact matching value on 1 column with insensitive cases

    Args:
    ----
        dataframe:      Dataframe to filter
        column_name:    Name of column
        value:          Value to match against

    Returns:
    -------
        Filtered dataframe

    """

    return dataframe.filter(pl.col(column_name).str.to_lowercase() == value.lower())


def subsequence_filter_dataframe(
    dataframe: pl.DataFrame, column_name: str, value: Any, **kwargs: Union[int, Any]
) -> pl.DataFrame:
    """Filter dataframe for rows that contains value as a subsequence in column_name

    Args:
    ----
        dataframe:      Dataframe to filter
        column_name:    Name of column
        value:          Value to match against

    Returns:
    -------
        Filtered dataframe

    """
    return dataframe.filter(pl.col(column_name).str.contains(str(value)))


# Define a helper function for case-insensitive subset check
def is_subset(row_list: list[str], subset: list[str]) -> bool:
    row_set = {x.lower() for x in row_list}  # Convert row elements to lowercase
    subset_set = {x.lower() for x in subset}  # Convert external list to lowercase
    return subset_set.issubset(row_set)  # Check if subset is contained in the row


def normalize_list(lst: list[str]) -> list[str]:
    return sorted([x.lower() for x in lst])


def split_element_in_list_by_space(list_of_strs: Any) -> List[str]:
    list_of_strs_spanned = list(list_of_strs)
    for str_ in list_of_strs:
        if not is_phone_number(str_):
            list_of_strs_spanned.extend(str_.split(" "))
    return list_of_strs_spanned


def sublist_filter_dataframe(
    dataframe: pl.DataFrame, column_name: str, value: Any, **kwargs: Union[int, Any]
) -> pl.DataFrame:
    """Filter dataframe for rows where value is a subset of the list in column_name.

    Args:
    ----
        dataframe:      Dataframe to filter.
        column_name:    Name of the column containing lists.
        value:          List of strings to match against.

    Returns:
    -------
        Filtered dataframe.
    """
    # # Filter the dataframe by checking if the column contains a superset of the provided value
    # return dataframe.filter(
    #     pl.col(column_name).map_elements(
    #         lambda row: is_subset(split_element_in_list_by_space(row), value), return_dtype=pl.Boolean
    #     )
    # )
    # Filter the dataframe by checking if the column contains a superset of the provided value
    return dataframe.filter(
        pl.col(column_name).map_elements(
            lambda row: is_subset(row, value), return_dtype=pl.Boolean
        )
    )


def sublist_partial_filter_dataframe(
    dataframe: pl.DataFrame, column_name: str, value: Any, **kwargs: Union[int, Any]
) -> pl.DataFrame:
    """Keep rows where EVERY queried element matches SOME element of the row's list,
    by case-insensitive substring or WRatio fuzzy score >= threshold. Preserves subset
    semantics (all queried elements must be present), but each element may match
    partially (e.g. first name 'Vick' matches stored 'Vick Li')."""
    threshold = kwargs.get("threshold", 80)
    queries = [str(v).lower() for v in value]

    def row_matches(row: Any) -> bool:
        items = [] if row is None else list(row)
        stored = [str(s).lower() for s in items]
        for q in queries:
            if not any((q in s) or (fuzz.WRatio(q, s) >= threshold) for s in stored):
                return False
        return True

    return dataframe.filter(
        pl.col(column_name).map_elements(row_matches, return_dtype=pl.Boolean)
    )


def range_filter_dataframe(
    dataframe: pl.DataFrame, column_name: str, value: Any, **kwargs: Union[int, Any]
) -> pl.DataFrame:
    """Filter dataframe for rows whose column_name value fits in a range. The value must implement __lt__ __gt__ __eq__
        __add__. Boundary included.

    Args:
    ----
        dataframe:      Dataframe to filter
        column_name:    Name of column
        value:          Lower or upperbound of the range
        **kwargs:       Must contain value_delta, value + value_delta provides the other end of the bound

    Returns:
    -------
        Filtered dataframe

    """
    try:
        value_delta = kwargs.get("value_delta")
    except KeyError:
        raise KeyError("**kwargs must contain 'value_delta'")
    lower_bound, upperbound = (
        min(value, value + value_delta),
        max(value, value + value_delta),
    )
    return dataframe.filter(
        (pl.col(column_name) >= lower_bound) & (pl.col(column_name) <= upperbound)
    )


def fuzzy_match_filter_dataframe(
    dataframe: pl.DataFrame, column_name: str, value: Any, **kwargs: Union[int, Any]
) -> pl.DataFrame:
    """Filter dataframe by fuzzy matching string value on 1 column. Backed by fuzz.WRatio

    Args:
    ----
        dataframe:      Dataframe to filter
        column_name:    Name of column
        value:          Value to match against
        **kwargs:       Additional kwargs for matching, for example
                        threshold for fuzz.WRatio, only entries above the threshold are selected

    Returns:
    -------
        Filtered dataframe
    """
    threshold = kwargs.get("threshold", 50)
    # Find the indices of top scored rows, process.extract returns a tuple of (string, score, index)
    # Note: limit=None ensures all matches above threshold are returned (default limit is 5)
    matches = process.extract(
        query=value,
        choices=dataframe.get_column(column_name),
        processor=utils.default_process,
        scorer=fuzz.WRatio,
        score_cutoff=threshold,
        limit=None,
    )
    return dataframe[[x[-1] for x in matches]]


def substring_or_fuzzy_match_filter_dataframe(
    dataframe: pl.DataFrame, column_name: str, value: Any, **kwargs: Union[int, Any]
) -> pl.DataFrame:
    """Filter rows where `value` is a case-insensitive substring of the cell OR the
    fuzzy score meets the threshold. Union of both arms (broader recall): the substring
    arm guarantees keyword hits regardless of WRatio's length-scaling, the fuzzy arm
    (WRatio at a lower cutoff than a bare name match) tolerates typos/variants.
    """
    threshold = kwargs.get("threshold", 80)
    cells = dataframe.get_column(column_name).to_list()
    q = str(value).lower()
    keep = {
        i for i, cell in enumerate(cells) if cell is not None and q in str(cell).lower()
    }
    matches = process.extract(
        query=value,
        choices=dataframe.get_column(column_name),
        processor=utils.default_process,
        scorer=fuzz.WRatio,
        score_cutoff=threshold,
        limit=None,
    )
    keep |= {x[-1] for x in matches}
    return dataframe[sorted(keep)]


def filter_dataframe(
    dataframe: pl.DataFrame,
    filter_criteria: list[tuple[str, Any, DataframeFilterMethodType]],
) -> pl.DataFrame:
    """Filter dataframe given a filter method, column name and target value

    Args:
        dataframe:          Dataframe to filter
        filter_criteria:    A list of filter constraints on each column,
                                each tuple contains [column_name, value, filter_method]

    Returns:
        Filtered dataframe
    """
    if all(x[1] is NOT_GIVEN for x in filter_criteria):
        raise ValueError(
            f"No search criteria are given. At least one search criteria should be provided among "
            f"{tuple(x[0] for x in filter_criteria)}"
        )
    for column_name, filter_value, filter_method in filter_criteria:
        if filter_value is not NOT_GIVEN:
            dataframe = filter_method(
                dataframe=dataframe,
                column_name=column_name,
                value=filter_value,
            )
    return dataframe


def polars_multiply_columns_expression(column_names: list[str]) -> pl.Expr:
    """Returns a polars expression that multiplies all columns in column_names

    Args:
        column_names:   Columns to multiply

    Returns:
        A polars expression that multiplies all columns in column_names
    """
    expression = pl.col(column_names[0])
    for column_name in column_names[1:]:
        expression = expression.mul(pl.col(column_name))
    return expression


def add_tool_trace(
    f: Callable[..., Any],
    result: Any,
    *args: Union[NotGiven, Any],
    **kwargs: Union[NotGiven, Any],
) -> None:
    """Add the trace of a tool: tool_name, arguments, execution results into current message in execution_context

    Args:
        f:          Tool callable
        result:     Return value of tool
        *args:      Positional arguments of tool
        **kwargs:   Keyword arguments of tool

    """
    current_context = get_current_context()
    if current_context.trace_tool:
        # Add tool trace to current SANDBOX snapshot. Unfortunately polars doesn't support
        # Very complex objects, and we'll need to json dump the trace into string. This adds
        # a restriction on tool definition (must be json serializable)
        # Note that a trace won't exist if tool execution raised exception
        message_entry: pl.DataFrame = current_context.get_database(
            namespace=DatabaseNamespace.SANDBOX
        )
        existing_tool_trace_series: Optional[pl.Series] = message_entry["tool_trace"][0]
        if existing_tool_trace_series is None:
            existing_tool_trace: list[str] = []
        else:
            existing_tool_trace = existing_tool_trace_series.to_list()
        # Convert positional arguments into keyword arguments. Signature.parameters is an ordered dict
        argument_names = list(signature(f).parameters.keys())
        all_arguments = {argument_names[i]: args[i] for i in range(len(args))}
        all_arguments = {**all_arguments, **kwargs}
        # Skip sentinels
        all_arguments = {k: v for k, v in all_arguments.items() if v is not NOT_GIVEN}
        existing_tool_trace.append(
            json.dumps(
                {
                    "tool_name": f.__name__,
                    "arguments": all_arguments,
                    "result": result,
                },
                ensure_ascii=False,
            )
        )
        new_message_entry = message_entry.with_columns(
            pl.lit(pl.Series("tool_trace", [existing_tool_trace]))
        )
        current_context.update_database(
            namespace=DatabaseNamespace.SANDBOX, dataframe=new_message_entry
        )


def register_as_tool(
    visible_to: Optional[tuple[RoleType]] = None,
    backend: ToolBackend = ToolBackend.DEFAULT,
) -> Callable[..., Any]:
    """Decorator factory, making decorator with arguments possible

    Args:
        visible_to:     Which roles are this tool visible to. Defaults to Agent.
        backend:        Backend implementation of the tool.

    Returns:
        decorator function
    """

    def internal_decorator(func: Callable[..., T]) -> Callable[..., T]:
        """Necessary to make decorator factory work. Returns a decorator which marks a function as tool,
        available for Roles to use

        Make use of decorator.decorate to keep function signature intact

        Args:
            func:   function to decorate

        Returns:
            decorated function
        """

        def _f(f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
            # Disable tracing for any tool call happened inside another tool's scope
            with new_context_with_attribute(trace_tool=False):
                result = f(*args, **kwargs)
            # Add tool trace to messages
            add_tool_trace(f, result, *args, **kwargs)
            return result

        dec = decorate(func, _f)
        setattr(dec, "is_tool", True)
        setattr(
            dec,
            "visible_to",
            visible_to if visible_to is not None else (RoleType.AGENT,),
        )
        setattr(dec, "backend", backend)
        return dec

    return internal_decorator


@contextmanager
def all_logging_disabled(highest_level: int = logging.CRITICAL) -> Iterator[None]:
    """A context manager that will prevent any logging messages
    triggered during the body from being processed.

    This is useful when a known package constantly emits necessary warnings.
    """
    previous_level = logging.root.manager.disable
    logging.disable(highest_level)
    try:
        yield
    finally:
        logging.disable(previous_level)


def attrs_serialize(inst: Any, field: Any, value: Any) -> Any:
    """Serialize troublesome values for attrs. Note almost all below are irreversible operations"""
    if isinstance(value, functools.partial):
        return value.func.__name__
    if isfunction(value):
        if value.__name__ == "<lambda>":
            return getsource(value).strip()
        else:
            return value.__name__
    if isinstance(value, pl.DataFrame):
        return value.to_dicts()
    if isinstance(value, StrEnum):
        return str(value)
    return value


def deterministic_uuid(payload: str) -> str:
    """Simple helper used to generate a deterministic uuid string

    Args:
        payload:    Payload string. Any uuid derived from the same payload is guaranteed to be the same

    Returns:
        String uuid
    """
    return str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name=payload))


def is_close(value: T, reference: T, atol: Optional[float] = None) -> bool:
    """Checks if value is close the reference.

    Allows for near identity comparison for different data types.

    In the case of float values, allow for a diff of at max atol.

    Args:
        value:      Value to compare.
        reference:  Value to compare against.
        atol:       Absolute tolerance, only needed for numerical values

    Returns:
        Boolean indicating if the values are close
    """
    if reference == "place_holder":
        return value not in (
            None,
            "",
            [],
            {},
            set(),
            NOT_GIVEN,
        )  # interpret "exists" as not-empty

    if (
        atol is not None
        and isinstance(value, (float, int))
        and isinstance(reference, (float, int))
    ):
        # Cast to satisfy mypy - isinstance checks above ensure these are numeric
        numeric_value = float(value)
        numeric_reference = float(reference)
        return abs(numeric_value - numeric_reference) <= atol

    return value == reference


def get_tomorrow_datetime() -> datetime.datetime:
    """Get a datetime object for exactly 1 day from now in the future.

    Returns:
        datetime object for exactly 1 day from now in the future.
    """
    return datetime.datetime.now() + datetime.timedelta(days=1)


def get_next_iso_weekday_datetime(next_iso_weekday: int) -> datetime.datetime:
    """Get a datetime object for next weekday.

    Args:
        next_iso_weekday:   1 based integer. 1 for Monday.

    Returns:
        datetime object for next weekday.
    """
    current_datetime = datetime.datetime.now()
    return current_datetime + datetime.timedelta(
        (next_iso_weekday - current_datetime.isoweekday()) % 7
    )
