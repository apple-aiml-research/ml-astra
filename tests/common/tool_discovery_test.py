# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
"""Unit tests for astra_tool_sandbox.common.tool_discovery"""

import pytest

import astra_tool_sandbox.tools
import astra_tool_sandbox.tools.messaging
from astra_tool_sandbox.common.tool_discovery import (
    ToolBackend,
    _extract_tools,
    find_tools_by_module,
)
from astra_tool_sandbox.common.utils import register_as_tool


def test_find_tools_by_module() -> None:
    # The messaging module defines/imports exactly these tools.
    assert set(
        find_tools_by_module(
            astra_tool_sandbox.tools.messaging, ToolBackend.DEFAULT
        ).keys()
    ) == {
        "send_message",
        "get_all_messages",
        "remove_message_or_conversation",
        "search_messages",
    }


def test_find_tools_by_module_with_duplicate() -> None:
    # Note: We cannot just take an existing function and modify its backend to introduce
    # a conflict, i.e.:
    #   astra_tool_sandbox.tools.rapid_api_search_tools.convert_currency.backend = (
    #      ToolBackend.DEFAULT
    #   )
    # The reason is that somehow this modification persists across different unit tests.
    # More specifically, with the above approach this test run fails:
    #   pytest tests/common/utils_test.py tests/smoke/smoke_test.py
    # because for some reason when running `smoke_test.py` the tool backend change still
    # persists and the test then fails with
    #   KeyError: 'Found 2 tools <function convert_currency at 0x1039de9d0> and
    #   <function convert_currency at 0x1039d38b0> sharing the same name
    #   convert_currency and backend DEFAULT'
    # Note the change still affects the original module even when creating a deep copy
    # of the module before modifying it with (presumably because the function is not
    # actually deepcopied):
    #   cloned_module = dill.copy(astra_tool_sandbox.tools)
    # Creating a Python module on the fly and adding duplicate functions is not
    # straightforward either. Thus, we only test the `_extract_tools` helper function
    # manually providing duplicate tools.
    @register_as_tool(backend=ToolBackend.DEFAULT)
    def do_nothing() -> None: ...

    @register_as_tool(backend=ToolBackend.DEFAULT)
    def do_nothing_dupe() -> None: ...

    with pytest.raises(KeyError, match=r".*tools.*same name.*backend.*"):
        _extract_tools([("do_nothing", do_nothing), ("do_nothing", do_nothing_dupe)])
