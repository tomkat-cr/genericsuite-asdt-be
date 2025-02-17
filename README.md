# GenericSuite Agentic Software Development Team (ASDT)

Welcome to the GenericSuite Agentic Software Development Team (backend version).

This project provides a team of autonomous entities designed to solve software development problems using AI to make decisions, learn from interactions, and adapt to changing conditions without human intervention.

This project is powered by different Agentic Frameworks, like [CrewAI](https://crewai.com), [Camel AI](https://camel-ai.org), [LangGraph](https://www.langchain.com/langgraph) and [Smolagent](https://huggingface.co/docs/smolagents/index). With them, set up a multi-agent AI system is astraightforward, leveraging these powerful and flexible frameworks.

The goal is to enable AI Agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

- First, if you haven't already, install Poetry:

```bash
pip install poetry
```

- Clone the repository:

```bash
git clone https://github.com/tomkat-cr/genericsuite-asdt-be.git
cd genericsuite-asdt-be
```

- Navigate to your project directory and install the dependencies:

```bash
make crewai_install
make camelai_install
make langgraph_install
make smolagent_install
```

### Customizing

- Create the `.env` file:

```bash
cp .env.example .env
vi .env
```

- Add your `API_KEYs` into the `.env` file:

```env
# Serper API
# https://serper.dev/
SERPER_API_KEY=
#
# OpenAI
# https://platform.openai.com/api-keys
OPENAI_API_KEY=
#
# Google
# https://console.cloud.google.com/apis/credentials
GOOGLE_API_KEY=
# https://programmablesearchengine.google.com/
GOOGLE_CSE_ID=
#
# Together AI
TOGETHER_AI_API_KEY=
# OPENAI_API_BASE_URL=https://api.together.xyz/v1
#
# AI/ML API
AIMLAPI_API_KEY=
# OPENAI_API_BASE_URL=https://api.aimlapi.com
#
# OpenRouter
OPENROUTER_API_KEY=
# OPENAI_API_BASE_URL=https://openrouter.ai/api/v1
#
# Ollama
#OLLAMA_BASE_URL=localhost:11434
#
# Hugging Face
# https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY=
#
# Anthropic
# https://console.anthropic.com/settings/keys
ANTHROPIC_API_KEY=
#
# Groq
GROQ_API_KEY=
#
# Nvidia
NVIDIA_API_KEY=
#
# X AI
XAI_API_KEY=
```

- Define the LLM provider in the "LLM Provider Section":

```env
# LLM provider codes:
#   ollama
#   openai
#   anthropic
#   google
#   huggingface
#   groq
#   aimlapi
#   together_ai
#   openrouter
#   xai
#
#DEFAULT_LLM_PROVIDER=ollama
#DEFAULT_CODING_LLM_PROVIDER=ollama
#DEFAULT_MANAGER_LLM_PROVIDER=ollama
#DEFAULT_REASONING_LLM_PROVIDER=ollama
#DEFAULT_PLANNING_LLM_PROVIDER=openai
```

NOTE: By default, `Ollama` is used for all providers.

- Configure the models:

```env
# Refer to the Models Section in the .env file for more details...
```

- Set the agent team configurations:

    1. Copy `src/genericsuite_asdt/crewai/config/agents.yaml` to `config/agents.yaml` to define your agents
    2. Copy `src/genericsuite_asdt/crewai/config/tasks.yaml` to `config/tasks.yaml` to define your tasks

## Running the Project

To kickstart your AI agents and begin task execution, run this from the root folder of your project:

```bash
# CrewAI
PROJECT="Generate blog posts for the most updated articles of the last week" TOPIC="AI LLMs" make crewai_run
```

```bash
# CamelAI
PROJECT="[/path/to/instructions.md]" TOPIC="Project subject" make camelai_run
```

You can find a Product Requirements Document (PRD) template at: [examples/instructions.md](examples/instructions.md)

These commands initializes the genericsuite-asdt Crew, assembling the agents and assigning them tasks as defined in your configuration.

The examples, unmodified, will run the create a `outputs/*_final_report.md` file with the output of a research on LLMs.

## Understanding Your Crew

The genericsuite-asdt Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.


## Contributors

[Carlos J. Ramirez](https://www.linkedin.com/in/carlosjramirez/)

Please feel free to suggest improvements, report bugs, or make a contribution to the code.

## License

This project is licensed under the terms of the ISC license. See the [LICENSE](LICENSE) file for details.

## Credits

This project is developed and maintained by [Carlos J. Ramirez](https://www.linkedin.com/in/carlosjramirez/). For more information or to contribute to the project, visit [GenericSuite ASDT on GitHub](https://github.com/tomkat-cr/genericsuite-asdt-be).

Happy Coding!
