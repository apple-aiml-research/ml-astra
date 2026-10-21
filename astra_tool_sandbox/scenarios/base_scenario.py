# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
from collections import defaultdict
from inspect import getmodule
from typing import Any, Callable, Dict, List

import astra_tool_sandbox.tools
from astra_tool_sandbox.common.execution_context import (
    DatabaseNamespace,
    RoleType,
)
from astra_tool_sandbox.common.message_conversion import UNAVAILABLE_TOOL_SHIM
from astra_tool_sandbox.common.scenario import Scenario

# from astra_tool_sandbox.toolbox.toolbox import Toolbox
from astra_tool_sandbox.common.tool_discovery import ToolBackend, find_tools_by_module
from astra_tool_sandbox.scenarios.astra_v1.protagonist_simulator_few_shot_examples import (
    named_user_simulator_few_shot_examples,
)


def create_base_scenario(
    preferred_tool_backend: ToolBackend,
    add_agent_system_prompt: bool = True,
    add_user_simulator_few_shot_examples: bool = True,
    single_turn_user_simulator: bool = False,
) -> Scenario:
    """Define the base scenario containing boilerplate info other scenarios could expand upon

    Note that this scenario does not contain Evaluation, and is incomplete.

    Args:
         preferred_tool_backend:  Which backend should be chosen in face of conflicting tool names.
         add_agent_system_prompt: Whether to add a system prompt for the agent to the
                                  sandbox message database.
         add_user_simulator_few_shot_examples: Whether to add few-shot examples for the
                                               user simulator to the sandbox message

         single_turn_user_simulator: Whether to enable multi-turn conversation.
    Returns:
        The base scenario.
    """
    # Find all available tools and form an import. Key is function name, value is function callable object
    tools: Dict[str, Callable[..., Any]] = find_tools_by_module(
        astra_tool_sandbox.tools, preferred_tool_backend=preferred_tool_backend
    )
    # Note that we delay initialization of some fields of the `ExecutionContext` to
    # avoid potentially doing "heavy work" for all scenarios while loading a dataset.
    # This delayed initialization will be triggered in `Scenario.prepare`.
    scenario = Scenario()
    # Set preferred backend
    scenario.starting_context.preferred_tool_backend = preferred_tool_backend
    # Turn on tool tracing
    scenario.starting_context.trace_tool = True
    # Add starting messages, and a representative few-shot example for user simulator
    user_simulator_few_shot_examples = named_user_simulator_few_shot_examples()
    # Create import statement
    # A dict with module name as key, A list of tool function name as value
    module_name_to_tool_names: Dict[str, List[str]] = defaultdict(list)
    for tool_name, tool_callable in tools.items():
        module = getmodule(tool_callable)
        assert module is not None
        module_name_to_tool_names[module.__name__].append(tool_name)
    import_statement: str = "import json\n"
    for module_name, tool_names in module_name_to_tool_names.items():
        import_statement += f"from {module_name} import {', '.join(tool_names)}\n"
    # Every tool is imported here regardless of the scenario's tool_allow_list — the
    # allow list is enforced when converting a tool call, not in this namespace. So a
    # call to a real-but-disallowed tool would otherwise just succeed. This shim is
    # what the converter routes such calls through: it keeps the generated code in the
    # normal `name(**params)` shape (so the reverse parser still works) while failing
    # deterministically and telling the agent what it may use instead.
    import_statement += UNAVAILABLE_TOOL_SHIM
    # Add starting messages.
    rows = [
        {
            "sender": RoleType.SYSTEM,
            "recipient": RoleType.EXECUTION_ENVIRONMENT,
            "content": import_statement,
        },
    ]

    if add_agent_system_prompt:
        SYSTEM_PROMPT = """
You are a helpful assistant equipped with tool-using abilities. Try your best to determine what values to plug into function calls based on the available information.

Tool Invocation Rules:
- You may call multiple tools within a single respond, including multiple write tools when they are independent.
- If a later tool call depends on the result of an earlier one (for example, needing an ID returned by a create call), issue those calls sequentially across multiple responds rather than in parallel.
- Assume all phone numbers are valid, regardless of format or length, as they may be anonymized or synthetic.
        """

        if not single_turn_user_simulator:
            rows += [
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.AGENT,
                    "content": SYSTEM_PROMPT
                    + "Don't make assumptions about what values to plug into functions. "
                    "Ask for clarification if a user request is ambiguous.",
                },
            ]
        else:
            rows += [
                {
                    "sender": RoleType.SYSTEM,
                    "recipient": RoleType.AGENT,
                    "content": SYSTEM_PROMPT
                    + "If the user's request is ambiguous, do not ask for clarification. Their input may be incorrect or incomplete. Proceed using your best judgment based on the available information and tools."
                    "You may use read-only tools to retrieve relevant user context (e.g., messages, emails, calendars, WhatsApp, etc.) before completing the task. If a `search_*` tool returns nothing, try using the corresponding `get_all_*` tool if available. "
                    "When asked to send a message or content, infer the user's intended communication channel using contextual clues such as prior conversations. If no such information is available, default to using the 'message' related tool."
                    "If you determine that key information is missing to complete the task, inform the user by saying 'key information is missing to complete this task.'"
                    "If you identify that the user has provided incorrect details, attempt to self-correct using available context and proceed with the task.",
                },
            ]

    if add_user_simulator_few_shot_examples:
        user_simulator_few_shot_examples = named_user_simulator_few_shot_examples()

        if not single_turn_user_simulator:
            rows += [
                *user_simulator_few_shot_examples[
                    "modify_contact_with_message_recency_multiple_user_turn"
                ]
            ]
        else:
            rows += [
                *user_simulator_few_shot_examples[
                    "modify_contact_with_message_recency_single_user_turn"
                ]
            ]

    scenario.starting_context.add_to_database(
        namespace=DatabaseNamespace.SANDBOX, rows=rows
    )
    # end_conversation should always be allowed
    scenario.starting_context.tool_allow_list = ["end_conversation"]
    return scenario
