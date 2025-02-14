"""
Generic Agent configuration reader
"""
from typing import Any
import os
import yaml

from pydantic import BaseModel, Field

from crewai import Agent, Task, Crew, Process

from genericsuite_asdt.llm import get_llm_model_object
from genericsuite_asdt.utils.datetime import get_current_date_time
from genericsuite_asdt.utils.app_logger import log_debug, log_error
from genericsuite_asdt.utils.utilities import get_default_resultset

# Uncomment the following line to use an example of a custom tool
# from genericsuite_asdt.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool

DEBUG = False


class SerperDevToolSchemaForPydanticV3(BaseModel):
    """
    Input for SerperDevTool. This is to fix the error:
    site-packages/crewai/tools/tool_usage.py:162: PydanticDeprecatedSince20:
    The `schema` method is deprecated; use `model_json_schema` instead.
    Deprecated in Pydantic V2.0 to be removed in V3.0.
    See Pydantic V2 Migration Guide at
      https://errors.pydantic.dev/2.10/migration/
    acceptable_args = tool.args_schema.schema()["properties"].keys()
      # type: ignore
      # Item "None" of "type[BaseModel] | None" has no attribute "schema"
    """
    search_query: str = Field(
        ..., description="Mandatory search query you want to use to search"
                         " the internet"
    )
    properties: str = Field(
        ..., description="Optional properties to use to filter the search"
                         " results"
    )


# Loading Tools
search_tool = SerperDevTool(
    args_schema=SerperDevToolSchemaForPydanticV3
)


def get_other_options(
    options,
    manager_agent: Agent = None,
    manager_agent_llm: Any = None,
    planning_agent_llm: Any = None
):
    """
    Helper function to get the other options
    """
    result = get_default_resultset()
    result["error_message"] = None

    result["options"] = dict(options)
    result["options"]["verbose"] = True
    result["options"]["debug"] = DEBUG
    # result["options"]["memory"] = True

    if os.environ.get('CREWAI_USE_MANAGER_AGENT', "true") == "true":
        if not manager_agent:
            result["error_message"] = "manager_agent is not set"
            return result
        # https://docs.crewai.com/how-to/Your-Own-Manager-Agent
        result["options"]["manager_agent"] = manager_agent
        result["options"]["manager_llm"] = manager_agent_llm

    if os.environ.get('CREWAI_USE_PLANNING_AGENT', "true") == "true":
        # Enable planning feature for the crew
        result["options"]["planning"] = True
        result["options"]["planning_llm"] = planning_agent_llm

    process_type = os.environ.get('CREWAI_CREW_PROCESS', "hierarchical")
    if process_type == "hierarchical":
        # In case you wanna use that instead
        # https://docs.crewai.com/how-to/Hierarchical/
        result["options"]["process"] = Process.hierarchical
    else:
        result["options"]["process"] = Process.sequential

    _ = DEBUG and log_debug(
        ">> GET_OTHER_OPTIONS | "
        f"\n| result: {result}"
    )
    return result


class GenericAgentConfig():
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.error_message = None
        self.agents = {}
        self.tasks = {}

        self.agent_config_file = \
            self.config.get("agent_config_file",
                            os.environ.get("CREWAI_AGENTS_CONFIG_FILE",
                                           "config/agents.yaml"))
        self.task_config_file = \
            self.config.get("task_config_file",
                            os.environ.get("CREWAI_TASK_CONFIG_FILE",
                                           "config/tasks.yaml"))

        self.llm = get_llm_model_object()
        self.manager_agent_llm = get_llm_model_object("manager")
        self.coding_agent_llm = get_llm_model_object("coding")
        self.reasoning_agent_llm = get_llm_model_object("reasoning")
        self.planning_agent_llm = get_llm_model_object("planning")

        self.manager_agent = None

        self.date_time = get_current_date_time()

    def get_error_message(self):
        return self.error_message

    def get_agent_params(self, agent_config):
        agent_params = dict(agent_config)
        if not agent_params.get("llm"):
            agent_params["llm"] = self.llm
        else:
            if agent_params["llm"] == "manager":
                agent_params["llm"] = self.manager_agent_llm
            elif agent_params["llm"] == "coding":
                agent_params["llm"] = self.coding_agent_llm
            elif agent_params["llm"] == "reasoning":
                agent_params["llm"] = self.reasoning_agent_llm
            elif agent_params["llm"] == "planning":
                agent_params["llm"] = self.planning_agent_llm

        if agent_params.get("tools_list"):
            agent_params["tools"] = agent_params.get("tools_list")
            del agent_params["tools_list"]

        if agent_params.get("tools"):
            tools = []
            for tool in agent_params["tools"]:
                tool_obj = tool
                if tool == "SerperDevTool" or tool == "search_tool":
                    tool_obj = search_tool
                tools.append(tool_obj)
            agent_params["tools"] = tools

        if agent_params.get("role"):
            # To avoid errors like:
            # "Error executing tool. coworker mentioned not found, it must be
            # one of the following options:" followed by the agent role in
            # lowercase...
            agent_params["role"] = agent_params["role"].lower()

        return agent_params

    def get_task_output_file(self, task_name):
        self.task_sequence += 10
        task_no = f"{str(self.task_sequence).zfill(4)}"
        output_file = \
            f"./outputs/{self.date_time}_{task_no}_{task_name}.md"
        return output_file

    def get_task_params(self, task_name, task_config):
        task_params = dict(task_config)
        if not task_params.get("output_file"):
            task_params["output_file"] = \
                self.get_task_output_file(task_name)
        if task_params.get("agent"):
            task_params["agent"] = self.agents[task_params["agent"]]
        if task_params.get("context"):
            task_params["context"] = [
                self.tasks[context] for context
                in task_params["context"]]
        return task_params

    def get_agents(self) -> list:
        """
        Loads the agents from the agent config file.

        Returns:
            A list of agents.
        """
        if not self.agent_config_file:
            self.error_message = "agent_config_file is not set"
            return []

        try:
            with open(self.agent_config_file, "r") as f:
                agents_config = yaml.safe_load(f)
        except Exception as e:
            self.error_message = f"Could not load agents: {e}"
            return []

        if not agents_config:
            self.error_message = "Could not load agents: config is empty"
            return []

        agents = []
        for agent_name, agent_config in agents_config.items():
            agent_params = self.get_agent_params(agent_config)
            _ = DEBUG and log_debug(
                f">> Loading agent: {agent_name}"
                f"\n| agent_config: {agent_config}"
                f"\n| agent_params: {agent_params}")
            if agent_name == "manager":
                self.agents[agent_name] = Agent(**agent_params)
                self.manager_agent = self.agents[agent_name]
                continue
            self.agents[agent_name] = Agent(**agent_params)
            agents.append(self.agents[agent_name])
        return agents

    def get_tasks(self) -> list:
        if not self.task_config_file:
            self.error_message = "task_config_file is not set"
            return []
        try:
            with open(self.task_config_file, "r") as f:
                tasks_config = yaml.safe_load(f)
        except Exception as e:
            self.error_message = f"Could not load tasks: {e}"
            return []
        tasks = []
        self.task_sequence = 0
        for task_name, task_config in tasks_config.items():
            task_params = self.get_task_params(task_name, task_config)
            _ = DEBUG and log_debug(
                f">> Loading task: {task_name}"
                f"\n| task_config: {task_config}"
                f"\n| task_params: {task_params}")
            self.tasks[task_name] = Task(**task_params)
            tasks.append(self.tasks[task_name])
        return tasks

    def get_crew(self) -> Crew:
        _ = DEBUG and log_debug(
            "GenericAgentConfig.get_crew():"
            f"\n| Loading agents from: {self.agent_config_file}")

        agents = self.get_agents()
        if self.error_message:
            log_error(self.error_message)
            return None

        _ = DEBUG and log_debug(
            "GenericAgentConfig.get_crew():"
            f"\n| Loading tasks from: {self.task_config_file}")

        tasks = self.get_tasks()
        if self.error_message:
            log_error(self.error_message)
            return None

        options = {
            "agents": agents,
            "tasks": tasks,
        }
        other_options = get_other_options(
            options,
            self.manager_agent, 
            self.manager_agent_llm,
            self.planning_agent_llm)
        if other_options.get("error_message"):
            self.error_message = other_options["error_message"]
            log_error(self.error_message)
            return None
        options = dict(other_options["options"])

        _ = DEBUG and log_debug(
            "GenericAgentConfig.get_crew() calling Crew(**options)"
            f"\n| options: {options}")

        return Crew(**options)
