# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
import json
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional

from astra_tool_sandbox.common.execution_context import (
    DatabaseNamespace,
)

# Load scenarios for Milestones and DAG


# Get generated/modified/removed entities
def normalize_json_str(s: str) -> str:
    return s.strip("\"'")  # removes both ' and " from the ends


def extract_milestones_and_edges(
    scenarios_script_full_path: Path, scenario_name: str
) -> tuple[str, Optional[str], Optional[str]]:
    with open(scenarios_script_full_path, "r", encoding="utf-8") as f:
        scenarios_raw_lines = f.readlines()

    scenario_found = False
    milestones_started = False
    collecting_edges = False
    minefield_started = False
    milestone_lines = []
    minefield_lines = []
    edge_lines: list[Any] = []
    milestone_bracket_level = 0
    edge_bracket_level = 0
    minefield_bracket_level = 0
    scenario_parenthesis_level = 0

    for line in scenarios_raw_lines:
        if not scenario_found and scenario_name in line:
            # print(f"scenario found: {line}")
            scenario_found = True
            continue

        # the next scenario is found!
        if (
            scenario_found
            and scenario_name not in line
            and "ScenarioExtension(" in line
        ):
            # print("Next scenario Found")
            scenario_found = False
            break

        if scenario_found:
            # Detect start of milestones=
            if not milestones_started and "milestones=" in line.replace(" ", ""):
                # print("Milestones Started")
                milestones_started = True
                milestone_bracket_level = line.count("[") - line.count("]")
                milestone_lines.append(line)
                # print(f"milestone line: {line}")
                continue

            # Collect milestone lines
            if milestones_started:
                milestone_lines.append(line)
                milestone_bracket_level += line.count("[") - line.count("]")
                # print(f"milestone_bracket_level: {milestone_bracket_level}, milestone line: {line}")
                if milestone_bracket_level <= 0:
                    milestones_started = False
                continue  # Don't allow edge_list detection inside milestone collection

            # Detect start of milestone_edge_list=
            if not collecting_edges and "milestone_edge_list=" in line.replace(" ", ""):
                if "milestone_edge_list=None" in line:
                    edge_lines = []
                    continue
                # print("Edgelist Started")

                edge_bracket_level = line.count("[") - line.count("]")
                # print("Appending edge_lines", line)
                edge_lines.append(line)

                if edge_bracket_level == 0:
                    # when milestone edge list are in one line
                    collecting_edges = False
                    continue
                collecting_edges = True
                continue

            # Collect edge list lines
            if collecting_edges:
                edge_bracket_level += line.count("[") - line.count("]")
                # print(f"edge_bracket_level: {edge_bracket_level}, milestone line: {line}")
                edge_lines.append(line)

                if edge_bracket_level <= 0:
                    collecting_edges = False  # Done collecting

                continue

            # Detect start of minefields=
            # if "minefields=" in line:
            # print("Minefields found in line")

            if not minefield_started and "minefields=" in line.replace(" ", ""):
                minefield_started = True
                minefield_bracket_level = line.count("[") - line.count("]")
                minefield_lines.append(line)
                # print(f"minefield line: {line}")
                continue

            # Collect minefield lines
            if minefield_started:
                minefield_lines.append(line)
                minefield_bracket_level += line.count("[") - line.count("]")
                # print(f"minefield_bracket_level: {minefield_bracket_level}, minefield line: {line}")
                if minefield_bracket_level <= 0:
                    minefield_started = False
                continue  # Don't allow edge_list detection inside minefield collection

    if not milestone_lines:
        raise ValueError(f"Could not extract milestones for scenario: {scenario_name}")

    # Trim the leading 'milestones=' and 'milestone_edge_list=' and Trim the ending unncessary strings
    if "=" in milestone_lines[0]:
        milestone_lines[0] = milestone_lines[0][milestone_lines[0].index("=") + 1 :]

    milestone_lines[-1] = milestone_lines[-1][: -milestone_lines[-1][::-1].index("]")]

    if edge_lines:
        if "=" in edge_lines[0]:
            edge_lines[0] = edge_lines[0][edge_lines[0].index("=") + 1 :]

        # find the last item contains ']'
        close_idx_list = [
            edge_line_idx
            for edge_line_idx, edge_line in enumerate(edge_lines)
            if "]" in edge_line
        ]
        if close_idx_list:
            close_idx = close_idx_list[-1]
            if "]" in edge_lines[close_idx]:
                edge_lines[close_idx] = edge_lines[close_idx][
                    : -edge_lines[close_idx][::-1].index("]")
                ]

            edge_lines = edge_lines[: (close_idx + 1)]
        elif len(edge_lines) == 1 and "None" in edge_lines[0]:
            edge_lines = ["None"]
    else:
        # if no milestone_edge_list exists
        edge_lines = ["None"]

    milestones_text = textwrap.dedent("".join(milestone_lines)).strip()
    edge_list_text = (
        textwrap.dedent("".join(edge_lines)).strip() if edge_lines else None
    )
    if edge_list_text:
        edge_list_text = (
            edge_list_text[:-1] if edge_list_text[-1] == "," else edge_list_text
        )

    if minefield_lines:
        # Trim the leading 'minefields=' and 'minefield_edge_list=' and Trim the ending unncessary strings
        if "=" in minefield_lines[0]:
            minefield_lines[0] = minefield_lines[0][minefield_lines[0].index("=") + 1 :]

        minefield_lines[-1] = minefield_lines[-1][
            : -minefield_lines[-1][::-1].index("]")
        ]

    minefields_text = (
        textwrap.dedent("".join(minefield_lines)).strip() if minefield_lines else None
    )

    return milestones_text, edge_list_text, minefields_text


def find_entity_in_execution_context_by_id(
    entity_id: str, dbs_to_search: Dict[str, Any]
) -> List[Dict[str, Any]]:
    if not dbs_to_search:
        raise ValueError("input execution context is empty")
    entity_prefix = entity_id.split("-")[0]
    db_to_search = None
    if entity_prefix == "email":
        db_to_search = dbs_to_search.get("EMAIL") or dbs_to_search.get(
            DatabaseNamespace.EMAIL
        )
    elif entity_prefix == "contacts":
        db_to_search = dbs_to_search.get("CONTACT") or dbs_to_search.get(
            DatabaseNamespace.CONTACT
        )
    elif (entity_prefix == "conversation") or (entity_prefix == "messages"):
        db_to_search = dbs_to_search.get("MESSAGING") or dbs_to_search.get(
            DatabaseNamespace.MESSAGING
        )
    elif entity_prefix == "calendar":
        db_to_search = dbs_to_search.get("CALENDAR") or dbs_to_search.get(
            DatabaseNamespace.CALENDAR
        )
    elif entity_prefix == "phone":
        db_to_search = dbs_to_search.get("PHONE") or dbs_to_search.get(
            DatabaseNamespace.PHONE
        )
    elif entity_prefix == "whatsapp":
        db_to_search = dbs_to_search.get("WHATSAPP") or dbs_to_search.get(
            DatabaseNamespace.WHATSAPP
        )
    else:
        raise NotImplementedError(f"{entity_prefix} hasn't been implemented")

    if db_to_search:
        id_fields = [item for item in list(db_to_search[0].keys()) if "_id" in item]
        return [
            entity
            for entity in db_to_search
            for id_field in id_fields
            if entity.get(id_field) and (entity_id in entity.get(id_field))
        ]
    else:
        return []


def format_flat_entities_for_prompt(
    entities: Optional[List[Any]],
) -> Optional[str]:
    """
    Formats a list of flat entities (e.g., calendar events, contacts) into a prompt-friendly string.
    Each entity is rendered as pretty-printed JSON, separated by blank lines.
    """
    if not entities:
        return "None"
    prompt_lines = []
    for entity in entities:
        prompt_lines.append("---")
        # Case 1: the entity is already a dict → pretty-print with json.dumps
        if isinstance(entity, dict):
            prompt_lines.append(json.dumps(entity, indent=2))

        # Case 2: the entity is a string
        elif isinstance(entity, str):
            # Try to parse it as JSON so we still get nice indentation
            try:
                prompt_lines.append(json.dumps(json.loads(entity), indent=2))
            except json.JSONDecodeError:
                # Not valid JSON; just indent every line by two spaces
                prompt_lines.append(textwrap.indent(entity, "  "))

        # Fallback: stringify and indent
        else:
            prompt_lines.append(textwrap.indent(str(entity), "  "))

        prompt_lines.append("")  # Separate entities with a blank line

    return "\n".join(prompt_lines)
