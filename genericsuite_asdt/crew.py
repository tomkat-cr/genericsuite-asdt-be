from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# from genericsuite_asdt.genericsuite.utils.app_logger import log_debug

from genericsuite_asdt.llm import get_llm_model_object


DEBUG = True


# Uncomment the following line to use an example of a custom tool
# from genericsuite_asdt.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool


@CrewBase
class GenericsuiteAsdtCrew:
    """GenericsuiteAsdt crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    llm = get_llm_model_object()
    manager_agent_llm = get_llm_model_object(True)

    # Agents

    @agent
    def senior_software_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["senior_software_engineer"],
            llm=self.llm,
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
            llm=self.llm,
        )

    @agent
    def project_architect(self) -> Agent:
        return Agent(
            config=self.agents_config["project_architect"],
            llm=self.llm,
        )

    @agent
    def frontend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config["frontend_developer"],
            llm=self.llm,
        )

    @agent
    def backend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config["backend_developer"],
            llm=self.llm,
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
            # tools=[MyCustomTool()],
            # Example of custom tool, loaded on the beginning of file
            llm=self.llm,
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["reporting_analyst"],
            llm=self.llm,
        )

    # Define the manager agent
    def manager(self):
        return Agent(
            config=self.agents_config["manager"],
            llm=self.manager_agent_llm,
        )

    # Tasks

    @task
    def feature_addition_task(self) -> Task:
        return Task(
            config=self.tasks_config["feature_addition_task"],
        )

    @task
    def bug_fixing_task(self) -> Task:
        return Task(
            config=self.tasks_config["bug_fixing_task"],
        )

    @task
    def testing_task(self) -> Task:
        return Task(
            config=self.tasks_config["testing_task"],
        )

    @task
    def frontend_development_task(self) -> Task:
        return Task(
            config=self.tasks_config["frontend_development_task"],
        )

    @task
    def backend_development_task(self) -> Task:
        return Task(
            config=self.tasks_config["backend_development_task"],
        )

    @task
    def devops_task(self) -> Task:
        return Task(
            config=self.tasks_config["devops_task"],
        )

    @task
    def ui_ux_task(self) -> Task:
        return Task(
            config=self.tasks_config["ui_ux_task"],
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config["reporting_task"],
            output_file="report.md"
        )

    # Crew

    @crew
    def crew(self) -> Crew:
        """Creates the GenericsuiteAsdt crew"""
        return Crew(
            agents=self.agents,  # Automatically created the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            verbose=True,
            # https://docs.crewai.com/how-to/Your-Own-Manager-Agent
            manager_agent=self.manager(),
            manager_llm=self.manager_agent_llm,
            # In case you wanna use that instead
            # https://docs.crewai.com/how-to/Hierarchical/
            process=Process.hierarchical,
            # process=Process.sequential,
        )
