# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Helper function that supports tool_trace_dependant_similarity. Extract certain values from
a tool trace
"""

import datetime
from typing import Any, Dict, List, Literal, Optional

from typing_extensions import Protocol

from astra_tool_sandbox.common.utils import normalize_list


class ToolTraceExtractorType(Protocol):
    """Callable type def for tool trace extraction functions

    Takes a tool_trace as input, returns a List of possible normalizations of extracted dictionary values

    Errors should be caught inside the extractor, assuming input types could be invalid
    """

    def __call__(
        self,
        tool_trace: Dict[Literal["tool_name", "arguments", "result"], Any],
    ) -> List[Dict[str, Any]]: ...


def default_value_normalization(value: Any) -> List[str]:
    """Normalize objects into a List of surface forms. Normalization strategy varies depending on datatype

    Args:
        value:  Value to normalize

    Returns:
        List of normalized values
    """
    if isinstance(value, float):
        return [
            f"{value:.0f}",
            f"{value:.1f}",
            f"{value:.2f}",
            f"{value:.3f}",
        ]

    return [str(value)]


def search_weather_around_lat_lon_temperature_extractor(
    tool_trace: Dict[Literal["tool_name", "arguments", "result"], Any],
) -> List[Dict[str, Any]]:
    """Extractor that extracts temperate from search_weather_around_lat_lon tool trace

    Args:
        tool_trace:     tool_trace of search_weather_around_lat_lon

    Returns:
        a list of dict containing possible normalized forms of the temperature

    """
    try:
        temperature: float = float(tool_trace["result"]["current_temperature"])
        # Normalize into different precisions
        return [
            {"temperature": normalized_temperature}
            for normalized_temperature in default_value_normalization(temperature)
        ]
    except (KeyError, TypeError):
        return []


def result_to_timestamp0_extractor(
    tool_trace: dict[str, Any],
) -> list[dict[str, float]]:
    return [{"timestamp_0": float(tool_trace["result"])}]


def result_to_timestamp1_extractor(
    tool_trace: dict[str, Any],
) -> list[dict[str, float]]:
    return [{"timestamp_1": float(tool_trace["result"])}]


def days_extractor(tool_trace: dict[str, Any]) -> list[dict[str, int]]:
    return [{"days": int(tool_trace["result"]["days"])}]


def lat_lon_dict_extractor(tool_trace: dict[str, Any]) -> list[dict[str, Any]]:
    return [{k: tool_trace["result"][k] for k in ["latitude", "longitude"]}]


def current_temperature_extractor(tool_trace: dict[str, Any]) -> list[dict[str, float]]:
    return [
        {
            "amount": float(tool_trace["result"]["current_temperature"]),
        }
    ]


def result_to_temperature_extractor(
    tool_trace: dict[str, Any],
) -> list[dict[str, str]]:
    return [
        {"temperature": x}
        for x in default_value_normalization(float(tool_trace["result"]))
    ]


def result_to_reminder_timestamp_lowerbound_extractor(
    tool_trace: dict[str, Any],
) -> list[dict[str, Any]]:
    return [{"reminder_timestamp_lowerbound": float(tool_trace["result"])}]


def min_temperature_amount_extractor(
    tool_trace: dict[str, Any],
) -> list[dict[str, float]]:
    return [
        {
            "amount": float(tool_trace["result"]["min_temperature"]),
        }
    ]


def min_temperature_extractor(tool_trace: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {"min_temperature": x}
        for x in default_value_normalization(float(tool_trace["result"]))
    ]


def contact_name_extractor(
    tool_trace: dict[str, Any], full_name_to_check: str
) -> list[dict[str, str]]:
    """
    Check if contact full names exist in tool_trace['result'].

    Returns:
        matched or not
    """

    try:
        result_list = tool_trace["result"]
        if not isinstance(result_list, list):
            return []

        for contact in result_list:
            if contact.get("full_name") == full_name_to_check:
                return [{"matched": "True"}]
        return []
    except Exception:
        return []


def result_to_birthday_text_extractor(
    tool_trace: dict[str, Any],
) -> list[dict[str, str]]:
    try:
        result_list = tool_trace["result"]
        if not isinstance(result_list, list) or not result_list:
            return []

        birthday_raw = result_list[0].get("birthday")
        if not birthday_raw:
            return []

        dt = datetime.datetime.fromisoformat(birthday_raw)

        # Multiple common surface forms
        return [
            {"birthday": dt.strftime("%B %d")},  # February 14
            {"birthday": dt.strftime("%b %d")},  # Feb 14
            {"birthday": dt.strftime("%m/%d")},  # 02/14
            {"birthday": dt.strftime("%d %B")},  # 14 February
            {"birthday": dt.strftime("%d %b")},  # 14 Feb
        ]
    except Exception:
        return []


def result_list_match_existence_extractor(
    tool_trace: Dict[str, Any],
    match_conditions: Optional[Dict[str, Dict[str, Any]]] = None,
) -> List[Dict[str, str]]:
    """
    Matches if there exists any item in tool_trace['result'] satisfying all field match rules.

    Each match_conditions entry is:
        field_name: {
            "value": Any,         # value to match against
            "partial": bool       # if True, do partial match for list fields or strings
        }

    Returns [{"matched": True}] if at least one match exists, else []
    """
    try:
        result = tool_trace.get("result", [])
        if not isinstance(result, list):
            return []

        def item_matches(
            item: Dict[str, Any], match_conditions: Dict[str, Dict[str, Any]]
        ) -> bool:
            for field, condition in match_conditions.items():
                expected_value = condition["value"]
                allow_partial = condition.get("partial", False)
                actual_value = item.get(field)

                # Normalize list and str
                if isinstance(actual_value, list):
                    actual_value = normalize_list(actual_value)
                elif isinstance(actual_value, str):
                    actual_value = actual_value.lower()
                if isinstance(expected_value, list):
                    expected_value = normalize_list(expected_value)
                elif isinstance(expected_value, str):
                    expected_value = expected_value.lower()

                if allow_partial:
                    if isinstance(actual_value, list):
                        if isinstance(expected_value, list):
                            if not any(ev in actual_value for ev in expected_value):
                                return False
                        else:
                            if expected_value not in actual_value:
                                return False
                    elif isinstance(actual_value, str):
                        if str(expected_value) not in actual_value:
                            return False
                    else:
                        return False
                else:
                    if actual_value != expected_value:
                        return False

            return True

        if match_conditions:
            for item in result:
                if item_matches(item, match_conditions=match_conditions):
                    return [{"matched": "True"}]
            return []
        else:
            return [{"matched": "True"}] if result else []

    except Exception:
        return []


def result_list_match_count_extractor(
    tool_trace: Dict[str, Any],
    count_expected: int,
    match_conditions: Optional[Dict[str, Dict[str, Any]]] = None,
) -> List[Dict[str, str]]:
    """
    Matches items in tool_trace['result'] where each item satisfies all field match rules.

    Each match_conditions entry is:
        field_name: {
            "value": Any,         # value to match against
            "partial": bool       # if True, do partial match for list fields
        }
    if no match_conditions provided, will check the total counts.

    Returns [{"matched": True}] if number of matches == count_expected, else []
    """
    try:
        result = tool_trace.get("result", [])
        if not isinstance(result, list):
            return []

        def item_matches(
            item: Dict[str, Any], match_conditions: Dict[str, Dict[str, Any]]
        ) -> bool:
            for field, condition in match_conditions.items():
                expected_value = condition["value"]
                allow_partial = condition.get("partial", False)
                actual_value = item.get(field)
                # Normalize list and str
                if isinstance(actual_value, list):
                    actual_value = normalize_list(actual_value)
                elif isinstance(actual_value, str):
                    actual_value = actual_value.lower()
                if isinstance(expected_value, list):
                    expected_value = normalize_list(expected_value)
                elif isinstance(expected_value, str):
                    expected_value = expected_value.lower()

                if allow_partial:
                    if isinstance(actual_value, list):
                        if expected_value not in actual_value:
                            return False
                    elif isinstance(actual_value, str):
                        if expected_value not in actual_value:
                            return False
                    else:
                        return False
                else:
                    if actual_value != expected_value:
                        return False
            return True

        if match_conditions:
            count = sum(
                1
                for item in result
                if item_matches(item, match_conditions=match_conditions)
            )
        else:
            count = len(result)

        if count == count_expected:
            return [{"matched": "True"}]
        return []

    except Exception:
        return []
