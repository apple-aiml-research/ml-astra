# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
import copy
import inspect
from textwrap import dedent
from typing import Any, Dict, List, cast

import pytest

from astra_tool_sandbox.common.execution_context import (
    ScenarioCategories,
    new_context_with_attribute,
)
from astra_tool_sandbox.common.tool_conversion import (
    convert_to_openai_tool,
    maybe_scramble_arg_description,
    maybe_scramble_arg_type,
    maybe_scramble_tool_description,
)
from astra_tool_sandbox.common.tool_discovery import ToolBackend, get_all_tools
from astra_tool_sandbox.tools.contact import add_contact, modify_contact


@pytest.mark.parametrize("tool_backend", ToolBackend)
def test_converting_all_tools(tool_backend: ToolBackend) -> None:
    """Ensure that all our tools can be converted to the OpenAI tool format."""
    name_to_tool = get_all_tools(preferred_tool_backend=tool_backend)
    for tool in name_to_tool.values():
        openai_tool = convert_to_openai_tool(tool)
        assert "function" == openai_tool["type"]
        function = openai_tool["function"]
        assert function is not None
        assert function["name"] is not None
        assert function["description"] is not None
        assert "object" == function["parameters"]["type"]

        # Ensure that each parameter has a type and a description.
        params_properties = cast(Dict[str, Any], function["parameters"]["properties"])
        for param in params_properties.values():
            assert param["type"] is not None
            assert param["description"] is not None

        # Ensure that all required parameters are part of the properties entry.
        for required_param_name in cast(List[Any], function["parameters"]["required"]):
            assert params_properties[required_param_name] is not None


# Make sure some of our more complicated tools are being converted as expected
def test_convert_to_openai_tool() -> None:
    # Strip None
    add_contact_expected: dict[str, Any] = {
        "type": "function",
        "function": {
            "name": "add_contact",
            "description": (
                "Add a new contact person to contact database. Entries with "
                "identical information are allowed,\n"
                "and will be assigned different person_ids."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "creation_datetime_iso": {
                        "type": "string",
                        "description": "Required. ISO 8601 formatted timestamp "
                        "indicating when the contact was created.",
                    },
                    "first_name": {
                        "type": "string",
                        "description": "Optional. First Name of contact person",
                    },
                    "last_name": {
                        "type": "string",
                        "description": "Optional. Last Name of contact person",
                    },
                    "full_name": {
                        "type": "string",
                        "description": "Optional. Full Name of contact person if both "
                        "first and last name not provided",
                    },
                    "alias": {
                        "type": "string",
                        "description": "Optional. Alias of contact person",
                    },
                    "phone_number": {
                        "type": "string",
                        "description": "Optional. Phone number of contact person",
                    },
                    "email": {
                        "type": "string",
                        "description": "Optional. Email of contact person",
                    },
                    "relationship": {
                        "type": "string",
                        "description": "Optional. Relationship between user and this "
                        "contact",
                    },
                    "address": {
                        "type": "string",
                        "description": "Optional. addresss of contact person",
                    },
                    "company": {
                        "type": "string",
                        "description": "Optional. company of contact person",
                    },
                    "job_title": {
                        "type": "string",
                        "description": "Optional. job title of contact person",
                    },
                    "is_self": {
                        "type": "boolean",
                        "description": "Optional. Defaults to False. Should be set to "
                        "True if the contact corresponds to the current user.",
                    },
                    "birthday": {
                        "type": "string",
                        "description": "Optional. Birthday of contact person in "
                        '"YYYY-MM-DD".',
                    },
                },
                "required": ["creation_datetime_iso"],
            },
        },
    }
    assert convert_to_openai_tool(add_contact) == add_contact_expected

    # Strip NotGiven
    assert convert_to_openai_tool(modify_contact) == {
        "type": "function",
        "function": {
            "name": "modify_contact",
            "description": "Modify a contact entry with new information provided",
            "parameters": {
                "type": "object",
                "properties": {
                    "person_id": {
                        "type": "string",
                        "description": "String unique identifier for the contact "
                        "person",
                    },
                    "creation_datetime_iso": {
                        "type": "string",
                        "description": "ISO 8601 formatted string of the current date "
                        "and time.",
                    },
                    "first_name": {
                        "type": "string",
                        "description": "Optional. New First Name of contact person",
                    },
                    "last_name": {
                        "type": "string",
                        "description": "Optional. New Last Name of contact person",
                    },
                    "full_name": {
                        "type": "string",
                        "description": "Optional. New Full name of contact person",
                    },
                    "alias": {
                        "type": "string",
                        "description": "Optional. New Alias of contact person",
                    },
                    "phone_number": {
                        "type": "string",
                        "description": "Optional. New Phone number of contact person",
                    },
                    "email": {
                        "type": "string",
                        "description": "Optional. New Email of contact person",
                    },
                    "relationship": {
                        "type": "string",
                        "description": "Optional, New relationship between user and "
                        "this contact",
                    },
                    "address": {
                        "type": "string",
                        "description": "Optional. New addresss of contact person",
                    },
                    "company": {
                        "type": "string",
                        "description": "Optional. New company of contact person",
                    },
                    "job_title": {
                        "type": "string",
                        "description": "Optional. New job_title of contact person",
                    },
                    "is_self": {
                        "type": "boolean",
                        "description": "Optional. Defaults to False. Should be set to "
                        "True if the contact corresponds to the current user.",
                    },
                    "birthday": {
                        "type": "string",
                        "description": "Optional. New Birth day of contact person in "
                        '"YYYY-MM-DD"',
                    },
                },
                "required": ["person_id", "creation_datetime_iso"],
            },
        },
    }

    # Remove description: TOOL_DESCRIPTION_SCRAMBLED empties the top-level tool
    # description but leaves every parameter untouched.
    with new_context_with_attribute(
        tool_augmentation_list=[ScenarioCategories.TOOL_DESCRIPTION_SCRAMBLED]
    ):
        expected = copy.deepcopy(add_contact_expected)
        expected["function"]["description"] = ""
        assert convert_to_openai_tool(add_contact) == expected

    # Remove argument description: ARG_DESCRIPTION_SCRAMBLED drops every parameter
    # description while keeping the top-level tool description and the types.
    with new_context_with_attribute(
        tool_augmentation_list=[ScenarioCategories.ARG_DESCRIPTION_SCRAMBLED]
    ):
        expected = copy.deepcopy(add_contact_expected)
        properties = cast(
            Dict[str, Any], expected["function"]["parameters"]["properties"]
        )
        for prop in properties.values():
            prop.pop("description", None)
        assert convert_to_openai_tool(add_contact) == expected

    # Remove argument type: ARG_TYPE_SCRAMBLED drops every parameter type while
    # keeping the descriptions.
    with new_context_with_attribute(
        tool_augmentation_list=[ScenarioCategories.ARG_TYPE_SCRAMBLED]
    ):
        expected = copy.deepcopy(add_contact_expected)
        properties = cast(
            Dict[str, Any], expected["function"]["parameters"]["properties"]
        )
        for prop in properties.values():
            prop.pop("type", None)
        assert convert_to_openai_tool(add_contact) == expected


def test_maybe_scramble_tool_description() -> None:
    # Scrambling the tool description strips everything before the "Args:" block,
    # leaving the argument/return/raises sections intact. Derive the expectation
    # from the live docstring so it stays correct as the wording evolves.
    extracted_docstring = inspect.getdoc(add_contact)
    assert extracted_docstring is not None
    expected = extracted_docstring[extracted_docstring.index("Args:") :]
    assert (
        maybe_scramble_tool_description(
            extracted_docstring,
            tool_augmentation_list=[ScenarioCategories.TOOL_DESCRIPTION_SCRAMBLED],
        )
        == expected
    )


def test_maybe_scramble_arg_description() -> None:
    docstring = """
    Add a new contact person to contact database. Entries with identical information are allowed,
    and will be assigned different person_ids.

    Args:

    Returns:
        String format unique identifier for the contact person, this can be passed to other functions
        which require a unique identifier for this contact person

    Raises:
        DuplicateError:     When self entry already exists, and we are adding a new one
    """
    # Without context
    extracted_docstring = inspect.getdoc(add_contact)
    assert extracted_docstring is not None
    assert (
        maybe_scramble_arg_description(
            extracted_docstring,
            tool_augmentation_list=[ScenarioCategories.ARG_DESCRIPTION_SCRAMBLED],
        )
        == dedent(docstring).strip()
    )


def test_maybe_scramble_arg_type() -> None:
    for parameter in maybe_scramble_arg_type(
        list(inspect.signature(add_contact).parameters.values()),
        tool_augmentation_list=[ScenarioCategories.ARG_TYPE_SCRAMBLED],
    ):
        assert parameter.annotation is type(None)
