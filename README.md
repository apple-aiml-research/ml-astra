# ASTRA-bench: Evaluating Tool-Use Agent Reasoning and Action Planning with Personal User Context

This software project accompanies the research paper, [ASTRA-bench: Evaluating Tool-Use Agent Reasoning and Action Planning with Personal User Context](https://arxiv.org/abs/2603.01357).

  Next-generation AI assistants need to juggle vast personal context, invoke external tools, and reason over multi-step plans --- yet most benchmarks still cast assistance as a context-free, single-turn exercise. We present ASTRA (Assistant Skills in Tool-use, Reasoning and Action-planning), the first benchmark to combine time-evolving, high-realism personal data with an interactive toolbox and human-authored complex user intents. Over 2,000 scenario examples with distinct and complex user intents are handcrafted from hundreds of time-stamped events from five simulated protagonists, alongside five non-English variants (German, French, Spanish, Chinese, Japanese) for multilingual assessment. Each example requires an agent to interpret private state, issue tool calls, and satisfy stringent automated checks. Released under CC BY-NC-ND with full datasets, an auto-evaluator, and reproducibility scripts, ASTRA aims to accelerate research toward trustworthy, plan-centric intelligent assistants.

## Getting started
### Installation
1. Install your favorite Python virtual environment manager. ASTRA supports Python 3.9–3.12; we recommend 3.11. For example, using the arm64 (Apple Silicon) version of Miniforge3: https://github.com/conda-forge/miniforge/releases/latest .

2. Create a virtual environment:
```bash
conda create -n astra-sandbox python=3.11
conda activate astra-sandbox
```

3. Install the dependencies with:
```bash
pip install .                     # core: scoring engine + scenarios + OpenAI models
pip install '.[agent-all]'        # core + all agent backends (Anthropic, Gemini)
pip install -e '.[agent-all,dev]' # for development and local editing
```

Test installation by running the `test` scenarios with GPT-4o as the agent while you play the user yourself (`--user Cli`). This needs an OpenAI API key; `--llm_evaluation` additionally grades each run with an LLM judge (also via `OPENAI_API_KEY`, see [Evaluation](#evaluation)). `-p 1` runs the scenarios one at a time so they can read your terminal input:
```bash
env OPENAI_API_KEY=<YOUR_OPENAI_API_KEY> astra_tool_sandbox --user Cli --agent GPT_4_o_2024_11_20 --tags test --llm_evaluation -p 1
```

4. (Optional) Contributing to this repo: Setup pre-commit hooks. Includes multiple linters
```bash
pre-commit install --hook-type pre-commit
```

5. (Optional) If some hooks are too slow and you would wish to skip them, you can do so with `SKIP` env variable. For example
```bash
SKIP="mypy" git commit -m "temporary commit that might not pass mypy"
```
### Execution
#### Required configuration for the different agent roles:

The following table shows the required environment variables to set depending on the agent type:

| Agent Type                  | Category     | ANTHROPIC_API_KEY | OPENAI_API_KEY | DEEPSEEK_API_KEY | DASHSCOPE_API_KEY | GOOGLE_CLOUD_PROJECT | GOOGLE_CLOUD_REGION |
| --------------------------- | :----------: | :---------------: | :------------: | :--------------: | :---------------: | :------------------: | :-----------------: |
| GPT_o_3_2025_04_16          | Proprietary  |                   | ✅             |                  |                   |                      |                     |
| GPT_4_1_2025_04_14          | Proprietary  |                   | ✅             |                  |                   |                      |                     |
| GPT_5_1_2025_11_13          | Proprietary  |                   | ✅             |                  |                   |                      |                     |
| Claude_4_5_Opus             | Proprietary  | ✅                |                |                  |                   |                      |                     |
| Claude_4_5_Haiku            | Proprietary  | ✅                |                |                  |                   |                      |                     |
| Claude_4_6_V1_Opus          | Proprietary  | ✅                |                |                  |                   |                      |                     |
| Claude_4_7_Opus             | Proprietary  | ✅                |                |                  |                   |                      |                     |
| Claude_4_8_Opus             | Proprietary  | ✅                |                |                  |                   |                      |                     |
| DeepSeek_v3                 | Open-source  |                   |                | ✅               |                   |                      |                     |
| Qwen_8B                     | Open-source  |                   |                |                  | ✅                |                      |                     |
| Qwen_32B                    | Open-source  |                   |                |                  | ✅                |                      |                     |
| Cli                         | Human        |                   |                |                  |                   |                      |                     |

The user simulator is an LLM that plays the role of the human user. The recommended user simulator is `GPT_4_1_2025_04_14`, which requires `OPENAI_API_KEY`. You can also use `Cli` to interact with the agent manually; pass `-p 1` with it, because by default scenarios run in parallel worker processes, which cannot read your terminal input.

#### Example command for a single scenario
It is recommended to just set the environment variables for the command that is running as opposed to exporting them e.g. in your `~/.bashrc` file. This makes it less likely to accidentally use stale environment variables. Here is an example command to run an ASTRA scenario using GPT-4.1 as the user simulator and Claude 4.5 Opus as the agent:
```
env ANTHROPIC_API_KEY=<YOUR_ANTHROPIC_API_KEY> OPENAI_API_KEY=<YOUR_OPENAI_API_KEY> astra_tool_sandbox --user GPT_4_1_2025_04_14 --agent Claude_4_8_Opus --scenarios get_contact_count_DAWEI_SHEN
```

Artifacts will be stored under the `data` folder within the repository's root directory. You can for example take a look at `data/agent_<agent-model>_user_<user-model>_<timestamp>/result_summary.json` to view the evaluation results. The full dialog of each scenario is stored within a `trajectories` subdirectory, e.g. `data/agent_<agent-model>_user_<user-model>_<timestamp>/trajectories/get_contact_count_DAWEI_SHEN/conversation.json`.

#### Hosting open source models
Open source models can be hosted using [vLLM's OpenAI Compatible Server](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html). Here is an example to serve a model:
```
pip install vllm
python3 -m vllm.entrypoints.openai.api_server --model <model-name>
```
Note that when serving a model for the first time it may be necessary to set the Hugging Face token using the `HF_TOKEN` environment variable:
```
env HF_TOKEN=<YOUR_HF_TOKEN> python3 -m vllm.entrypoints.openai.api_server --model <model-name>
```
Depending on your GPU you may have to explicitly set the `dtype` with e.g. `--dtype=half`. By default, the above command will host an OpenAI compatible server at http://0.0.0.0:8000. The following lines of Python code can be used to quickly test that the server can be reached:
```python
import openai
openai_client = openai.OpenAI(api_key="EMPTY", base_url="http://0.0.0.0:8000/v1")
print(openai_client.models.list())
```
On success, this should print the models hosted by the server. Note that these instructions assume that the client and server run on the same compute instance. If the server is running on a different compute instance, the compute instance running the client can use SSH port forwarding to access the server.

To point ASTRA's OpenAI roles at that server rather than at `api.openai.com`, pass `base_url` (and, if the served model name differs from the role's default, `model_name`) when constructing the role:
```python
from astra_tool_sandbox.roles.openai_api_agent import OpenAIAPIAgent

agent = OpenAIAPIAgent(
    base_url="http://0.0.0.0:8000/v1",
    model_name="<model-name>",
)
```
`OpenAIAPIUser` takes the same three keyword arguments. An explicit `base_url` is honoured verbatim, so it is not overridden by `OPENAI_BASE_URL`. `api_key` defaults to the placeholder `"EMPTY"`, which such servers ignore but the OpenAI client requires.

#### Example command for running all scenarios
By default, if `--scenarios` is not provided all scenarios will be executed. Here is an example command using GPT-4.1 as both the user simulator and agent:
```
astra_tool_sandbox --user GPT_4_1_2025_04_14 --agent GPT_4_1_2025_04_14
```
#### Example command for running scenarios with tags
By default, if `--tags` and `--scenarios` is not provided all scenarios will be executed. Here is an example command using GPT-4.1 as both the user simulator and agent to run scenarios with tags (`test` and `email`) provided.

```
astra_tool_sandbox --user GPT_4_1_2025_04_14 --agent GPT_4_1_2025_04_14 --tags test email
```

Here is another example command to run scenarios with tags (`DAWEI_SHEN`) provided, corresponding to the protagonist Dawei Shen.

```
astra_tool_sandbox --user GPT_4_1_2025_04_14 --agent GPT_4_1_2025_04_14 --tags DAWEI_SHEN
```


## Documentation

The following sections introduce the core design and concepts.

### Protagonists

ASTRA scenarios are grounded in 5 simulated protagonists, each with a distinct personal context (contacts, calendars, emails, messages, reminders, etc.):

| Protagonist      | Tag              |
| ---------------- | ---------------- |
| Dawei Shen       | `DAWEI_SHEN`     |
| Emily Rose       | `EMILY_ROSE`     |
| John Quinn       | `JOHN_QUINN`     |
| Theo Appleseed   | `THEO_APPLESEED` |
| Lucas Garcia     | `LUCAS_GARCIA`   |

Each protagonist's scenarios are stored under `astra_tool_sandbox/scenarios/astra_v1/<PROTAGONIST_NAME>/`. To run all scenarios for a specific protagonist, use the `--tags` flag:
```
astra_tool_sandbox --user GPT_4_1_2025_04_14 --agent Claude_4_5_Opus --tags DAWEI_SHEN
```

### Complexity Dimensions

Each scenario is annotated along three complexity axes and two challenging scenario types:

**Complexity Axes** (each rated low / moderate / high):
- **Informational Complexity** -- how much information the user provides and the agent must track
- **Referential Complexity** -- the degree of indirect references, coreferences, or ambiguous entity mentions
- **Functional Complexity** -- the number and depth of tool calls required to complete the task

**Challenging Scenario Types:**
- **Misinformation** -- the user provides incorrect information; the agent must detect and handle it
- **Insufficient Context** -- necessary tools or information are deliberately withheld; the agent should recognize it cannot complete the task rather than hallucinate

Scenarios are tagged with values like `informational_complexity_moderate`, `referential_complexity_high`, `misinformation_yes`, `insufficient_context_no`, etc.

### Execution context
The execution context stores the complete state of the tool sandbox. More specifically, the tools, dialog history between the different roles and the world state. It also stores a snapshot of the state at every turn, which is used for introspection and evaluation. The world state consists of:
- a contact book
- a messaging database (storing text messages)
- an email database
- a calendar database
- a WhatsApp messaging database
- a phone call database

### Tools
The implemented tools are a set of highly composable, explicitly or implicitly dependent Python functions, creating complex reasoning challenges. Tools can manipulate the world state through the execution context. Here is an example tool:
```
@register_as_tool(visible_to=(RoleType.AGENT,))
@typechecked
def remove_contact(person_id: str) -> None:
    """Remove an existing contact person to contact database.

    Args:
        person_id:      String format unique identifier of the person to be deleted

    Returns:

    Raises:
        NoDataError:    If the provided person_id was not found
    """
    validate_type(person_id, "person_id", str)

    current_context = get_current_context()
    current_context.remove_from_database(
        namespace=DatabaseNamespace.CONTACT, predicate=pl.col("person_id") == person_id
    )
```
A Python function is registered as a tool with the `register_as_tool` decorator. Note that when defining a scenario the developer can decide which tools should be visible to the agent. You can find the available tools [here](astra_tool_sandbox%2Ftools).

### Roles
The roles interacting in the tool sandbox are the system, user, agent and execution environment. This is more generic than the usual chat and agent roles commonly used in proprietary APIs. The interaction between the roles is based on a message passing system. Each message specifies the sender, recipient and to which roles it is visible to.

#### User
The user represents a human interacting with an agent hoping to complete a task. The user role decides when the task is complete by using the `end_conversation` tool, which is the only tool available to the user. The user can be a real human or it can be simulated by an agent.

#### Agent
The agent initially receives a message from the user in natural language specifying the task to be completed. The agent can then decide to respond to the user (e.g. asking for clarification) or send a tool use request to the execution environment. The following agents have been evaluated in the paper:

**Proprietary Models:**
- GPT-o3, GPT-4.1 ([OpenAI](https://platform.openai.com/docs/models))
- Claude 4.5 Opus, Claude 4.5 Haiku ([Anthropic](https://www.anthropic.com/claude))

**Open-Source Models:**
- DeepSeek-V3 ([DeepSeek](https://www.deepseek.com))
- Qwen3 30B-A3B, Qwen3 30B-A3B-Instruct, Qwen3 235B-A22B ([Alibaba](https://github.com/QwenLM/Qwen))

**Other:**
- Human via CLI

The agents are defined [here](astra_tool_sandbox%2Froles).

#### Execution environment
The execution environment executes tool calls requested by the agent. The implementation is based on Python's [code.InteractiveConsole](https://docs.python.org/3.9/library/code.html#code.InteractiveConsole) module. The tool result is captured via `stdout` and potential exceptions are captured via `stderr`. This is similar to executing code in a Jupyter notebook. If an exception occurs it is communicated back to the agent such that it can refine its tool call and try again.
Note that the code is executed directly on the host machine and not in e.g. a sandbox like a docker container. At the moment this is acceptable since
- we do not allow the agent to run arbitrary Python code, but it can only select from the tools we have implemented
- we have full control over which tools exist and how they are implemented

However, with the current implementation a developer could get quite sad if we added a new `rm_dir` tool and the agent requests a tool call like `rm_dir("/")`.

### Scenario
Scenarios are defined in Python as extensions to a base setup. One can think of the base setup as the initial device state. The example below is illustrative of the `ScenarioExtension` API (the `set_cellular_service_status` tool is not part of ASTRA's toolset); see [Evaluation](#evaluation) for a real ASTRA scenario.
```
ScenarioExtension(
    name="cellular_off",
    base_scenario=base_scenarios["base"],
    messages=[
        {
            "sender": RoleType.SYSTEM,
            "recipient": RoleType.USER,
            "content": USER_INSTRUCTION + "Turn off cellular service",
        },
        {
            "sender": RoleType.USER,
            "recipient": RoleType.AGENT,
            "content": "Turn off cellular",
        },
    ],
    tool_allow_list=["set_cellular_service_status"],
    milestones=[
        Milestone(
            snapshot_constraints=[
                SnapshotConstraint(
                    database_namespace=DatabaseNamespace.SETTING,
                    snapshot_constraint=snapshot_similarity,
                    target_dataframe=pl.DataFrame(
                        {
                            "cellular": False,
                        }
                    ),
                )
            ]
        ),
        Milestone(
            snapshot_constraints=[
                SnapshotConstraint(
                    database_namespace=DatabaseNamespace.SANDBOX,
                    snapshot_constraint=snapshot_similarity,
                    target_dataframe=pl.DataFrame(
                        {
                            "sender": RoleType.AGENT,
                            "recipient": RoleType.USER,
                            "content": "Cellular service is turned off",
                        }
                    ),
                )
            ]
        ),
    ],
)
```
#### Tool augmentations
Note that several tool augmentations are supported:
- adding tools not needed to complete the task (distraction tools)
- scrambling the tool name (i.e. renaming the tool to something less informative `set_cellular_service_status` to `settings_0` forcing the agent to use the docstring when deciding which tool to use)
- removing the argument descriptions of the tools
- renaming the arguments in the docstring (e.g. `arg_0` instead of `phone_number`)
- removing the argument type hints forcing the agent to guess the data type or figuring it out through trial and error

#### Scenario categories
The scenarios are categorized in order to gain insight into what agents can handle well. Note that a scenario can belong to multiple categories at the same time. The categories are:
- Single/multiple tool call. This is based on how many tool uses are needed to achieve the task.
- Single/multiple user turn. If a user provides all necessary information in the initial message to the agent then the scenario is considered a single turn scenario.
- State dependency. These are categories where successful tool execution depends on the world state (e.g. enabling some setting using another tool before being able to use the tool to perform the user's task). In these cases there is an implicit dependency between tools / a tool and the world state, which the agent needs to discover through trial and error.
- Canonicalization. This category is for scenarios where natural language information needs to be transformed into its corresponding canonical form. In some cases the agent can directly do this (e.g. converting `1k` to `1000`), but in other cases it requires a tool (e.g. converting `this Friday` to `14th of June 2024`).
- Insufficient information. In these scenarios necessary tools or information are held back on purpose such that the agent is unable to perform the user's task. The motivation is to see if the agent can identify that it is unable to complete the task or if it instead hallucinates tools or tool arguments.

### Evaluation

ASTRA uses two complementary evaluation approaches: **milestone-based evaluation** and **LLM-based evaluation**.

#### LLM-based evaluation metrics

An LLM evaluator scores each scenario trajectory on the following dimensions:

| Metric                              | Scale | Description |
| ----------------------------------- | :---: | ----------- |
| Task Completion                     | 0--2  | Did the assistant give a correct and complete response to the user? |
| Tool Call Capability                | 0--2  | Did the assistant use the right tools with appropriate parameters? |
| Information Retrieval Capability    | 0--2  | Did the assistant extract and interpret relevant information correctly from tool outputs? |
| Conversation Efficiency             | 0--2  | Did the assistant avoid unnecessary turns and complete the task concisely? |
| No Hallucination Score              | 0--2  | Did the assistant avoid fabricating information not grounded in tool outputs or user input? |

The LLM judge runs entirely over public APIs and is configurable via environment variables:

- `ASTRA_LLM_EVAL_BACKEND` — `openai` (default) or `anthropic`.
- `ASTRA_LLM_EVAL_MODEL` — overrides the grader model (defaults: `o3-2025-04-16` for OpenAI, `claude-opus-4-8` for Anthropic). Set e.g. `gpt-4o-mini` for a cheaper run.

The OpenAI backend uses `OPENAI_API_KEY` (against `api.openai.com`); the Anthropic backend uses `ANTHROPIC_API_KEY` (against `api.anthropic.com`). Pass `--llm_evaluation` on the CLI to enable it.

#### Milestone-based evaluation (Milestone Similarity / Completion Score)

Many different trajectories could lead to the same outcome. There could be different tools that can complete the task,
the agent could fail to complete and ask the user for additional input, or figure things out with the execution environment
through trial and error. This makes evaluation extra difficult for an interactive environment. However, between all these
possibilities, there's often a few **_critical milestones_** we need to hit in order to complete the task.

Milestones are further tagged as **payload generation** (tool calls that modify state or produce data) or **response generation** (the agent's final reply to the user), enabling fine-grained analysis of where models succeed or fail.

For example, consider the scenario `get_calendar_involve_vick_DAWEI_SHEN` from the protagonist Dawei Shen:
- The user asks: "Get all my scheduled calendar events involve Vick"
- Dawei Shen's calendar contains one event: "Cycling Trip with Vick" (attendee: Vick Li)

Given the tools available, we know a few things must happen:

0. **_First_**, the agent must call a calendar retrieval tool (`search_calendar_events` or `get_all_calendars`) to find events involving Vick
1. **_After 0_**, the tool result should contain the "Cycling Trip with Vick" event -- verified via `tool_trace_dependant_similarity` which checks the tool output contains a matching calendar event

We don't know exactly when these milestones shall happen, but we know they must happen in this order at some point
in the trajectory. This is the general design principle of our evaluation. To make this a little more formal


1. Evaluation criteria is defined with a Milestone DAG. Directional edges define the sequential order of each milestone.
   In the example above, the edges would be `[(0, 1)]`
2. Each milestone contains multiple similarity measures, calculating the [0, 1] similarity between this milestone
   and each step in the trajectory. Similarity measures are allowed to depend on other milestones. These similarities include:
   1. snapshot_similarity: How close is a database to a target database
   2. addition_similarity: How close is a database to a target database, if the target database was derived from adding
      k target rows into a reference database
   3. removal_similarity: How close is a database to a target database, if the target database was derived from removing
      k target rows from a reference database
   4. update_similarity: How close is a database to a target database, if the target database was derived from updating
      k target rows in a reference database
   5. tool_trace_dependant_similarity: How close is a database to a target database, if the target database includes
      values extracted from the tool_trace of a reference database
   6. guardrail_similarity: The database should be identical to a reference database, otherwise this similarity is 0
3. Each milestone similarity further breaks down into column-wise similarity, which can be **_exact_match_**, **_rouge_l_**
   etc. Allowing for more customization in matching logic
4. Milestone similarity is derived by calculating the geometric mean of all its similarity measures.
   1. Geo mean ensures if 1 exact matching similarity returns 0, the whole milestone similarity is 0.
5. An optimal match between milestones and trajectory is found by maximizing the arithmetic mean of all milestone similarities
   under the constraint that matched milestone order should be one possible topological sort of the Milestone DAG.

The milestones for the `get_calendar_involve_vick_DAWEI_SHEN` scenario (from `astra_tool_sandbox/scenarios/astra_v1/DAWEI_SHEN/dawei_shen_scenarios.py`) can be described as follows

```python
milestones = [
    # Milestone 0: Agent must call a calendar retrieval tool
    Milestone(
        snapshot_constraints=[
            SnapshotConstraint(
                database_namespace=DatabaseNamespace.SANDBOX,
                snapshot_constraint=snapshot_similarity,
                target_dataframe=pl.DataFrame(
                    {
                        "sender": RoleType.EXECUTION_ENVIRONMENT,
                        "recipient": RoleType.AGENT,
                        "tool_trace": "",  # Value not used in similarity calculation
                    }
                ),
                column_similarity_measure={
                    "tool_trace": partial(
                        column_tool_trace_matches_tool_names,
                        target_tools=[
                            "search_calendar_events",
                            "get_all_calendars",
                        ],
                    )
                },
            )
        ]
    ),
    # Milestone 1: Tool result must contain the "Cycling Trip with Vick" event
    Milestone(
        snapshot_constraints=[
            SnapshotConstraint(
                database_namespace=DatabaseNamespace.SANDBOX,
                snapshot_constraint=partial(
                    tool_trace_dependant_similarity,
                    fill_to="content",
                    extractor=cast(
                        ToolTraceExtractorType,
                        partial(
                            result_list_match_existence_extractor,
                            match_conditions={
                                "calendar_event_name": {
                                    "value": "Cycling Trip with Vick",
                                    "partial": True,
                                }
                            },
                        ),
                    ),
                ),
                target_dataframe=pl.DataFrame(
                    {
                        "sender": RoleType.EXECUTION_ENVIRONMENT,
                        "recipient": RoleType.AGENT,
                        "content": "{matched}",
                    }
                ),
                column_similarity_measure={
                    "content": column_one_similarity,
                },
                reference_milestone_node_index=0,
            )
        ]
    ),
]
# Milestone 1 depends on milestone 0
edge_list = [(0, 1)]
```
Here's an example trajectory collected from `deepseek-chat` (DeepSeek-V3), as well as the evaluation results
```
shape: (14, 8)
+-------------------+-------------------+------------------+------------------+------------------+------------------+------------------+------------------+
| sandbox_message_i | sender            | recipient        | content          | openai_function_ | tool_call_except | tool_trace       | visible_to       |
| ndex              | ---               | ---              | ---              | name             | ion              | ---              | ---              |
| ---               | enum              | enum             | str              | ---              | ---              | list[str]        | list[enum]       |
| i32               |                   |                  |                  | str              | str              |                  |                  |
+=========================================================================================================================================================+
| ...               | SYSTEM            | ...              | (system setup    | ...              | ...              | ...              | ...              |
|                   |                   |                  | messages omitted |                  |                  |                  |                  |
|                   |                   |                  | for brevity)     |                  |                  |                  |                  |
|-------------------+-------------------+------------------+------------------+------------------+------------------+------------------+------------------|
| 4                 | USER              | AGENT            | Get all my       | null             | null             | null             | null             |
|                   |                   |                  | scheduled        |                  |                  |                  |                  |
|                   |                   |                  | calendar events  |                  |                  |                  |                  |
|                   |                   |                  | involve Vick     |                  |                  |                  |                  |
|-------------------+-------------------+------------------+------------------+------------------+------------------+------------------+------------------|
| 5                 | AGENT             | EXECUTION_ENVIRO | search_calendar_ | search_calendar_ | null             | null             | ["AGENT",        |
|                   |                   | NMENT            | events(attendees | events           |                  |                  | "EXECUTION_ENVI  |
|                   |                   |                  | =['Vick'])       |                  |                  |                  | RONMENT"]        |
|-------------------+-------------------+------------------+------------------+------------------+------------------+------------------+------------------|
| 6                 | EXECUTION_ENVIRON | AGENT            | []               | search_calendar_ | null             | ["{"tool_name":  | ["EXECUTION_ENVI |
|                   | MENT              |                  |                  | events           |                  | "search_calendar | RONMENT",        |
|                   |                   |                  |                  |                  |                  | _events", ...    | "AGENT"]         |
|                   |                   |                  |                  |                  |                  | "result": []}"]  |                  |
|-------------------+-------------------+------------------+------------------+------------------+------------------+------------------+------------------|
| 7                 | AGENT             | EXECUTION_ENVIRO | get_all_calendar | get_all_calendar | null             | null             | ["AGENT",        |
|                   |                   | NMENT            | s()              | s                |                  |                  | "EXECUTION_ENVI  |
|                   |                   |                  |                  |                  |                  |                  | RONMENT"]        |
|-------------------+-------------------+------------------+------------------+------------------+------------------+------------------+------------------|
| 8                 | EXECUTION_ENVIRON | AGENT            | [{'calendar_name | get_all_calendar | null             | ["{"tool_name":  | ["EXECUTION_ENVI |
|                   | MENT              |                  | ': 'personal',   | s                |                  | "get_all_calenda | RONMENT",        |
|                   |                   |                  | 'calendar_event_ |                  |                  | rs", ...         | "AGENT"]         |
|                   |                   |                  | name': 'Cycling  |                  |                  | "Cycling Trip    |                  |
|                   |                   |                  | Trip with Vick', |                  |                  | with Vick"       |                  |
|                   |                   |                  |  ...             |                  |                  | ...}]"}"]        |                  |
|                   |                   |                  | 'attendees_names |                  |                  |                  |                  |
|                   |                   |                  | ': ['Dawei Shen' |                  |                  |                  |                  |
|                   |                   |                  | , 'Vick Li']}]   |                  |                  |                  |                  |
|-------------------+-------------------+------------------+------------------+------------------+------------------+------------------+------------------|
| 9                 | AGENT             | USER             | I found one      | null             | null             | null             | ["AGENT",        |
|                   |                   |                  | calendar event   |                  |                  |                  | "USER"]          |
|                   |                   |                  | involving Vick:  |                  |                  |                  |                  |
|                   |                   |                  | **Cycling Trip   |                  |                  |                  |                  |
|                   |                   |                  | with Vick**      |                  |                  |                  |                  |
|                   |                   |                  | Dec 1, 2024      |                  |                  |                  |                  |
|                   |                   |                  | 7:00-10:00 AM    |                  |                  |                  |                  |
|                   |                   |                  | Local Café, Napa |                  |                  |                  |                  |
|                   |                   |                  | Valley, CA       |                  |                  |                  |                  |
|-------------------+-------------------+------------------+------------------+------------------+------------------+------------------+------------------|
| 10-13             | USER / AGENT /    | ...              | (end_conversation| ...              | ...              | ...              | ...              |
|                   | EXEC_ENV          |                  | sequence)        |                  |                  |                  |                  |
+-------------------+-------------------+------------------+------------------+------------------+------------------+------------------+------------------+
```

`milestone_mapping` contains a dictionary of `milestone_index: (corresponding_turn_index, milestone_similarity)`
```json
{
   "name": "get_calendar_involve_vick_DAWEI_SHEN",
   "categories": [
       "MULTIPLE_TOOL_CALL",
       "SINGLE_USER_TURN"
   ],
   "tags": [
       "DAWEI_SHEN",
       "calendar"
   ],
   "similarity": 1.0,
   "turn_count": 7,
   "milestone_mapping": {
       "0": [
           8,
           1.0
       ],
       "1": [
           8,
           1.0
       ]
   }
}
```

### How to Add a new tool
New tools live under `astra_tool_sandbox/tools/`. Add a module exposing tool functions and they are auto-discovered by `astra_tool_sandbox.common.tool_discovery`.

### Gymnasium environment

`astra_tool_sandbox.gymnasium_env.AstraGymnasiumEnv` exposes an ASTRA scenario as a plain [`gymnasium.Env`](https://gymnasium.farama.org/), for harnesses that already own their agent loop (LLM sampling, tool-calling scaffolding, retries) and just need `reset()` / `step()` primitives.

```bash
pip install -e '.[gymnasium]'
```

```python
from astra_tool_sandbox.gymnasium_env import AstraGymnasiumEnv

env = AstraGymnasiumEnv(scenario_tags=["test"])   # or desired_scenario_names=[...]
observation, info = env.reset()

# REQUIRED: forward these to your model. See the warning below.
system_messages = info["system_messages"]

for _ in range(30):
    action = your_policy(system_messages, observation)   # text, optionally with a ```python block
    observation, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        break

print(reward, info["turn_count"], info["hallucinated_tool_call_count"])
```

An action is text. If it contains a ` ```python ` block, that block is executed against the scenario's tool sandbox; otherwise it is treated as a natural-language reply to the user. Calling `end_conversation()` from a code block finishes the episode. `env.tool_specs()` returns `{name: ToolSpec(name, description, parameters)}` with OpenAI-function-shaped `parameters`, and `env.openai_tools()` returns the same thing in OpenAI `tools=` form, so you can build your own tool documentation without importing ASTRA internals.

#### Forward `info["system_messages"]` to your model

These messages carry the assistant instructions and, critically, the scenario's clock:

```
Today is Saturday, December 7, 2024. Current time (ISO format): 2024-12-07T08:05:00.
```

They are the *only* source of that date. Scenarios are set in the past, `starting_context.reference_time` is `None` for them, no time tool is exposed, and nothing in ASTRA mocks the clock. A model left to write its own `datetime.now()` — which the sandbox will happily execute — reads the real clock and answers for the wrong day. `get_add_calendar_DAWEI_SHEN`, for instance, requires `start_datetime_iso=2024-12-07T10:00:00` for a task phrased "at 10am today", and scores 0.0 without it. ASTRA's own agent role reads these from the execution context during `Scenario.play()`; a harness has to be handed them explicitly, which is what `reset()`'s `info` (and `env.system_messages`) is for.

#### Choosing which scenario an episode plays

`reset()` rotates through the resolved catalog in a fixed round-robin order. To play a specific one without building a new env, name it in gymnasium's `options`:

```python
env.reset(options={"scenario_name": "get_contact_count_DAWEI_SHEN"})
```

The name must be in the catalog resolved at construction (`env.scenario_names` lists it) — resolving is expensive, so pass a filter broad enough to cover what you will ask for. A named `reset()` does not advance the round-robin cursor, so interleaving targeted episodes leaves the rotation order intact.

#### Options

| Option | Default | Effect |
|---|---|---|
| `similarity_threshold` | `None` | `None` makes the terminal reward the raw `similarity` score. Set it for a binary reward: `success_reward` when `similarity >= threshold`, else `0.0`. |
| `success_reward` | `1.0` | Terminal reward on success when `similarity_threshold` is set. Unused otherwise. |
| `exclude_nl_reply_milestones` | `False` | Drop milestones that grade the agent's natural-language reply, scoring purely on tool-call/database effects. For harnesses with no LLM user simulator to receive that reply. Not a no-op: 1,224 of 2,428 scenarios carry an AGENT→USER milestone. |
| `max_messages` | scenario's own | Episode step budget. |
| `max_unsuccessful_user_responses` | `3` | Consecutive natural-language actions before the guardrail ends the episode. |

#### Limitations

- **`step()` is not bounded by a timeout.** ASTRA runs model-generated Python in-process via `code.InteractiveConsole`, so a pathological snippet can hang. Any harness driving untrusted code must supply its own bound.
- **`observation_space.contains()` is advisory, not a validator.** The charset is `string.printable`, while real scenario content includes accented Latin, em-dashes, curly quotes and emoji. Do not gate rollouts on it, and expect `gymnasium.utils.env_checker` to complain.
- **Only one env may be stepping per process.** ASTRA's execution context is a process global, so two concurrent episodes in one process would corrupt each other's databases. Vectorise across processes (e.g. `gymnasium.vector.AsyncVectorEnv`), never within one.
- **Resolving the catalog is expensive**: 2,428 scenarios / ~92s / ~950MB unfiltered, versus 14 / 2.4s for `scenario_tags=["test"]`. The adapter resolves once at construction, so always pass a filter.
- **`scenario_tags` and `desired_scenario_names` cannot be combined** — ASTRA's filter unions rather than intersects them, so the adapter rejects the pair up front rather than failing later with a misleading empty-list `KeyError`.


## License

The code in this repository is released under the [Apple Sample Code License](LICENSE). The accompanying ASTRA dataset (scenarios and simulated protagonist data) is released under [CC BY-NC-ND 4.0](LICENSE_DATA).

## Citation

Paper: [ASTRA-bench: Evaluating Tool-Use Agent Reasoning and Action Planning with Personal User Context](https://arxiv.org/abs/2603.01357) (arXiv:2603.01357).

> Xiu, Z., Sun, D.Q., Cheng, K., Patel, M., Date, J., Zhang, Y., Lu, J., Attia, O., Vemulapalli, R., Tuzel, O., Cao, M. and Bengio, S., 2026. Astra-bench: Evaluating tool-use agent reasoning and action planning with personal user context. arXiv preprint arXiv:2603.01357.

To cite _ASTRA_:
```text
@misc{xiu2026astrabench,
      title={{ASTRA}-bench: Evaluating Tool-Use Agent Reasoning and Action Planning with Personal User Context},
      author={Zidi Xiu and David Q. Sun and Kevin Cheng and Maitrik Patel and Josh Date and Yizhe Zhang and Jiarui Lu and Omar Attia and Raviteja Vemulapalli and Oncel Tuzel and Meng Cao and Samy Bengio},
      eprint={2603.01357},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2603.01357},
}
```
