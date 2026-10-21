# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
import os
from pathlib import Path
from typing import Any, Dict

from astra_tool_sandbox.common.constants import PACKAGE_DIR
from astra_tool_sandbox.scenarios.astra_v1.protagonist_data_paths import (
    ProtagonistOperaPaths,
)
from astra_tool_sandbox.scenarios.astra_v1.protagonists import ProtagonistName

# from astra_tool_sandbox.scenarios.opera._opera_data_path import (
#     StateOperaPaths,
# )

# def get_all_available_protagonists_base_ctx(protagonist_root_path: Path = PACKAGE_DIR/"scenarios"/"opera") -> Dict[str, ProtagonistOperaPaths]:
#     """ List all available protagonists and the relative data paths """
#     protagonists = [f for f in os.listdir(protagonist_root_path) if os.path.isdir(protagonist_root_path/f) and "ctx_data" in os.listdir(protagonist_root_path/f)]
#     ProtagonistOperaPaths


# Define get_astra_v1_paths function here
def get_astra_v1_paths(root_path: Path, paths: list[Path]) -> ProtagonistOperaPaths:
    """Helper function to load state opera paths."""
    paths = paths or [Path("ctx_data")]

    astra_v1_paths = ProtagonistOperaPaths(
        base_paths=[str(root_path / path_) for path_ in paths]
    )
    return astra_v1_paths


def load_character_jsons_paths(character_name: ProtagonistName) -> Dict[str, Any]:
    """Get the jsons with the given name of the character.

    Args:
        character_name:  Name of the dataset to get.

    Returns:
        The dataset.
    """
    if character_name in [p.value for p in ProtagonistName]:
        charater_root_path = PACKAGE_DIR / "scenarios" / "astra_v1" / character_name
        full_plots = [
            d
            for d in os.listdir(charater_root_path)
            if os.path.isdir(os.path.join(charater_root_path, d))
            if d not in ("raw_annotated_files", "__pycache__")
        ]
        character_plots = {}

        # Iterate through the list to build the dictionary
        for item in full_plots:
            if item == "ctx_data":
                plot_key = "base"
            else:
                # Extract the specific case by removing the 'ctx_data_' prefix
                plot_key = item.replace("ctx_data_", "")
            character_plots[plot_key] = get_astra_v1_paths(
                root_path=charater_root_path, paths=[Path(item)]
            )

        return character_plots
    raise RuntimeError(f"Protagonist '{character_name}' does not exist.")
