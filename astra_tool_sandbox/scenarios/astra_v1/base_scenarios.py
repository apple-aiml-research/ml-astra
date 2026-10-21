# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
from pathlib import Path
from typing import Dict, List, Optional

import polars as pl

from astra_tool_sandbox.common.execution_context import DatabaseNamespace
from astra_tool_sandbox.common.scenario import Scenario
from astra_tool_sandbox.common.tool_discovery import ToolBackend
from astra_tool_sandbox.common.utils import (
    deterministic_uuid,
)
from astra_tool_sandbox.scenarios.astra_v1.load_astra_v1_entities import (
    astra_v1_to_calendar_event,
    astra_v1_to_contact,
    astra_v1_to_emails,
    astra_v1_to_messages,
    astra_v1_to_phonecall,
    astra_v1_to_whatsapp_messages,
    convert_empty_values_to_none,
    load_and_concatenate_json_files,
)
from astra_tool_sandbox.scenarios.astra_v1.load_protagonist import (
    load_character_jsons_paths,
)
from astra_tool_sandbox.scenarios.astra_v1.protagonists import ProtagonistName
from astra_tool_sandbox.scenarios.base_scenario import create_base_scenario


def load_jsons_to_scenario(
    scenario: Scenario,
    paths: List[Path],
    plot_ids: List[str],
    database_name: DatabaseNamespace,
    ref_df: Optional[pl.DataFrame] = None,
) -> Scenario:
    """Conversion of the jsons into a polars dataframe rows

    Args:
        scenario: Destination scenario to be added
        paths:  List of jsons paths to combine
        plot_ids: List of plot_ids to load
        ref_df: Optional existing Polars DataFrame to search for certain information


    Returns:
        A list or rows that is ready for polars add_to_dataframe actions
    """
    jsons = load_and_concatenate_json_files(paths, plot_ids)
    # existing_entries = scenario.starting_context._dbs[database_name]
    if database_name == DatabaseNamespace.MESSAGING:
        if ref_df is None:
            raise ValueError("contact_db is required for MESSAGING data")
        rows = astra_v1_to_messages(
            [convert_empty_values_to_none(messaging_json) for messaging_json in jsons],
            contact_db=ref_df,
        )
    elif database_name == DatabaseNamespace.CALENDAR:
        if ref_df is None:
            raise ValueError("contact_db is required for CALENDAR data")
        rows = [
            astra_v1_to_calendar_event(
                **convert_empty_values_to_none(calendar_json), contact_db=ref_df
            )
            for calendar_json in jsons
        ]
    elif database_name == DatabaseNamespace.EMAIL:
        if ref_df is None:
            raise ValueError("contact_db is required for EMAIL data")
        rows = astra_v1_to_emails(
            [convert_empty_values_to_none(email_json) for email_json in jsons],
            contact_db=ref_df,
        )
    elif database_name == DatabaseNamespace.WHATSAPP:
        if ref_df is None:
            raise ValueError("contact_db is required for whatsapp data")
        self_full_name = ref_df.filter(pl.col("is_self"))[0, "full_name"]
        self_email = ref_df.filter(pl.col("is_self"))[0, "email"]
        self_phone_number = ref_df.filter(pl.col("is_self"))[0, "phone_number"]
        rows = astra_v1_to_whatsapp_messages(
            jsons,
            self_full_name=self_full_name,
            self_email=self_email,
            self_phone_number=self_phone_number,
        )
    elif database_name == DatabaseNamespace.PHONE:
        if ref_df is None:
            raise ValueError("contact_db is required for PHONE data")
        rows = [
            astra_v1_to_phonecall(
                **convert_empty_values_to_none(phonecall_json), contact_db=ref_df
            )
            for phonecall_json in jsons
        ]
    else:
        raise ValueError("In valid database namespace")

    scenario.starting_context.add_to_database(
        namespace=database_name,
        rows=rows,
    )
    return scenario


def named_base_scenarios(
    protagonist_name: ProtagonistName,
    preferred_tool_backend: ToolBackend,
    single_turn_user_simulator: bool = False,
    add_user_simulator_few_shot_examples: bool = False,
) -> Dict[str, Scenario]:
    """Define the base scenario containing boilerplate info other scenarios could expand upon

    Note that this scenario does not contain Evaluation, and is in complete.

    Args:
        protagonist_name: Which protagonist context to load from
        preferred_tool_backend: Which backend should be chosen in face of conflicting tool names.
        single_turn_user_similator: Whether it's multi-turn set up. By default it's False

    Returns:
        A Dict containing scenario name and scenario
    """
    ## NOTE: For debugging purposes
    # if single_turn_user_simulator:
    #     print("Single Turn Scenario Loaded")
    # else:
    #     print("Multi-Turn Scenario Loaded")

    scenario = create_base_scenario(
        preferred_tool_backend,
        single_turn_user_simulator=single_turn_user_simulator,
        add_user_simulator_few_shot_examples=add_user_simulator_few_shot_examples,
    )

    # Load paths for protagonist
    astra_v1_paths = load_character_jsons_paths(protagonist_name)
    base_astra_v1_path = astra_v1_paths["base"]

    # Update the basic settings
    scenario.starting_context.add_to_database(
        namespace=DatabaseNamespace.SETTING,
        rows=[
            {
                "sandbox_message_index": 0,
                "device_id": deterministic_uuid(payload="my phone"),
                "cellular": True,
                "wifi": True,
                "location_service": True,
                "low_battery_mode": False,
                "latitude": 37.334606,
                "longitude": -122.009102,
            },
        ],
    )
    # Adding contact information
    contact_jsons = load_and_concatenate_json_files(
        file_paths=base_astra_v1_path.contact_paths,
        plot_ids=base_astra_v1_path.plot_ids,
    )
    contact_rows = [
        astra_v1_to_contact(**convert_empty_values_to_none(json_))
        for json_ in contact_jsons
    ]
    contact_db = pl.DataFrame(contact_rows)

    scenario.starting_context.add_to_database(
        namespace=DatabaseNamespace.CONTACT,
        rows=contact_rows,
    )
    scenario = load_jsons_to_scenario(
        scenario=scenario,
        paths=base_astra_v1_path.phonecall_paths,
        plot_ids=base_astra_v1_path.plot_ids,
        database_name=DatabaseNamespace.PHONE,
        ref_df=contact_db,
    )
    scenario = load_jsons_to_scenario(
        scenario=scenario,
        paths=base_astra_v1_path.messaging_paths,
        plot_ids=base_astra_v1_path.plot_ids,
        database_name=DatabaseNamespace.MESSAGING,
        ref_df=contact_db,
    )
    scenario = load_jsons_to_scenario(
        scenario=scenario,
        paths=base_astra_v1_path.calendar_paths,
        plot_ids=base_astra_v1_path.plot_ids,
        database_name=DatabaseNamespace.CALENDAR,
        ref_df=contact_db,
    )

    scenario = load_jsons_to_scenario(
        scenario=scenario,
        paths=base_astra_v1_path.email_paths,
        plot_ids=base_astra_v1_path.plot_ids,
        database_name=DatabaseNamespace.EMAIL,
        ref_df=contact_db,
    )

    scenario = load_jsons_to_scenario(
        scenario=scenario,
        paths=base_astra_v1_path.whatsapp_paths,
        plot_ids=base_astra_v1_path.plot_ids,
        database_name=DatabaseNamespace.WHATSAPP,
        ref_df=contact_db,
    )

    # # end_conversation should always be allowed
    # scenario.starting_context.tool_allow_list = ["end_conversation"]
    # Base scenario
    scenarios: Dict[str, Scenario] = dict()
    scenarios = {"base": scenario}

    return scenarios
