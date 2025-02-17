"""
GenericsuiteAsdt crew class
"""
import os

from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task

from genericsuite_asdt.utils.datetime import get_current_date_time
from genericsuite_asdt.utils.app_logger import log_error

from genericsuite_asdt.llm import get_llm_model_object
from genericsuite_asdt.generic_agents import (
    GenericAgentConfig,
    search_tool,
    get_other_options,
)

DEBUG = True


@CrewBase
class GenericsuiteAsdtCrew:
    """
    GenericsuiteAsdt crew class
    """

    agents_config = os.environ.get("CREWAI_AGENTS_CONFIG_FILE",
                                   "config/agents.yaml")
    tasks_config = os.environ.get("CREWAI_TASK_CONFIG_FILE",
                                  "config/tasks.yaml")

    llm = get_llm_model_object()
    manager_agent_llm = get_llm_model_object("manager")
    coding_agent_llm = get_llm_model_object("coding")
    reasoning_agent_llm = get_llm_model_object("reasoning")
    planning_agent_llm = get_llm_model_object("planning")

    date_time = get_current_date_time()

    # Agents

    @agent
    def senior_software_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["senior_software_engineer"],
            llm=self.coding_agent_llm,
        )

    @agent
    def software_quality_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["software_quality_engineer"],
            llm=self.llm,
        )

    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["test_engineer"],
            llm=self.coding_agent_llm,
        )

    @agent
    def project_architect(self) -> Agent:
        return Agent(
            config=self.agents_config["project_architect"],
            # llm=self.llm,
            llm=self.reasoning_agent_llm,
        )

    @agent
    def frontend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config["frontend_developer"],
            llm=self.coding_agent_llm,
        )

    @agent
    def backend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config["backend_developer"],
            llm=self.coding_agent_llm,
        )

    @agent
    def devops_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["devops_specialist"],
            llm=self.llm,
        )

    @agent
    def ui_ux_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["ui_ux_specialist"],
            llm=self.llm,
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            llm=self.llm,
            # tools=[MyCustomTool()],
            # Example of custom tool, loaded on the beginning of file
            tools=[search_tool],
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["reporting_analyst"],
            llm=self.llm,
        )

    @agent
    def business_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["business_analyst"],
            llm=self.reasoning_agent_llm,
        )

    @agent
    def creative_innovative_team(self) -> Agent:
        return Agent(
            config=self.agents_config["creative_innovative_team"],
            llm=self.reasoning_agent_llm,
        )

    # Define the manager agent
    def manager(self):
        return Agent(
            config=self.agents_config["manager"],
            llm=self.manager_agent_llm,
        )

    # Tasks

    # @task
    # def ideation_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["ideation_task"],
    #         # input_file="project_and_topic.md",
    #         output_file=f"./outputs/{self.date_time}_030_ideation.md",
    #     )

    # @task
    # def business_analysis_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["business_analysis_task"],
    #         # input_file="ideation.md",
    #         output_file=f"./outputs/{self.date_time}_040_business_analysis.md",
    #     )

    @task
    def feature_addition_task(self) -> Task:
        return Task(
            config=self.tasks_config["feature_addition_task"],
            output_file=f"./outputs/{self.date_time}_050_feature_addition.md",
        )

    @task
    def bug_fixing_task(self) -> Task:
        return Task(
            config=self.tasks_config["bug_fixing_task"],
            output_file=f"./outputs/{self.date_time}_060_bug_fixing.md",
        )

    @task
    def testing_task(self) -> Task:
        return Task(
            config=self.tasks_config["testing_task"],
            output_file=f"./outputs/{self.date_time}_070_testing.md",
        )

    @task
    def frontend_development_task(self) -> Task:
        return Task(
            config=self.tasks_config["frontend_development_task"],
            output_file=f"./outputs/{self.date_time}_080_frontend_dev.md",
        )

    @task
    def backend_development_task(self) -> Task:
        return Task(
            config=self.tasks_config["backend_development_task"],
            output_file=f"./outputs/{self.date_time}_090_backend_dev.md",
        )

    @task
    def devops_task(self) -> Task:
        return Task(
            config=self.tasks_config["devops_task"],
            output_file=f"./outputs/{self.date_time}_100_devops.md",
        )

    @task
    def ui_ux_task(self) -> Task:
        return Task(
            config=self.tasks_config["ui_ux_task"],
            output_file=f"./outputs/{self.date_time}_110_ui_ux.md",
        )

    # @task
    # def research_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["research_task"],
    #         output_file=f"./outputs/{self.date_time}_120_research.md",
    #     )

    # @task
    # def reporting_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["reporting_task"],
    #         output_file=f"./outputs/{self.date_time}_130_report.md",
    #     )

    @task
    def final_report(self) -> Task:
        return Task(
            config=self.tasks_config["final_report"],
            output_file=f"./outputs/{self.date_time}_120_final_report.md",
        )

    # Crew

    @crew
    def crew(self) -> Crew:
        """
        Creates the GenericsuiteAsdt crew
        """
        options = {
            "agents": self.agents,
            "tasks": self.tasks,
        }
        other_options = get_other_options(
            options,
            self.manager(),
            self.manager_agent_llm,
            self.planning_agent_llm)
        if other_options.get("error_message"):
            self.error_message = other_options["error_message"]
            log_error(self.error_message)
            return None
        options = dict(other_options["options"])

        return Crew(**options)


class GsAutoGeneratedCrew:
    def crew(self) -> Crew:
        """
        Creates the GenericsuiteAsdt crew
        """
        gac = GenericAgentConfig()
        return gac.get_crew()
