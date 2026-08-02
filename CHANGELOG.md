# CHANGELOG

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/) and [Keep a Changelog](http://keepachangelog.com/).



## [Unreleased] - YYYY-MM-DD

### Added

### Changed

### Fixed

### Removed

### Security


## [0.3.0] - 2026-07-15

### Added
- AGENTS.md, GEMINI.md, and CLAUDE.md files to provide context and instructions to AI Coding Assistants [GS-303].
- Add SAST testing [GS-315].
- `make upgrade`, `make crewai_upgrade`, and `make camelai_upgrade` commands to upgrade dependencies to the latest version and fix vulnerabilities [GS-219].

### Changed
- License changed to MIT [FA-244].
- Change documentation so LangGraph and Smolagents are planned, not supported yet [GS-327].
- Enhance Makefile and scripts for Python version management and upgrade commands [GS-219].
- Update dependencies in all Python projects pyproject.toml and poetry.lock for improved compatibility and security fixes [GS-219].

### Security
- Migrate to Python 3.14 [GS-337].

### Removed
- Remove outdated and empty requirements.txt file [GS-219].


## [0.2.0] - 2025-02-27

### Changed
- README typos and wording [GS-128].

### Security
- Update crewai, setuptools, fastapi, uvicorn, python-multipart, openlit, and pyyaml to the latest version to upgrade `uv` to 0.8.8 to fix "Interpretation Conflict", CVE-2025-54368 CWE-20 CWE-436
 [GS-219].


## [0.1.0] - 2025-02-17

### Added
- Add LLM selection and configuration using environment variables, and including OpenAI, Google, Ollama, Anthropic, Hugging Face, Groq, NVIDIA, X AI, Together AI, AI/ML API and OpenRouter [GS-128].
- Add the ideation task to generate ideas for the "AIstronauts-Space Agents on a mission hackathon" from lablab.ai [GS-55].
- Add different environment variables for coding, reasoning, planning and management llms and models, so normal agents, manager agent and planning agent can use them [GS-128].
- Add the planning agent, so the code generation actions are fired and iterated [GS-128].
- Add "openlit" monitoring tool [GS-128].
- Add "agentops" monitoring tool [GS-128].
- Add generate output files on each task [GS-128].
- Add automatic generation of the crew, agents and tasks directly from the yaml files with no wrappers (decorated class and methods) [GS-128].
- Add "allow_code_execution" to developer and automated testing agents [GS-128].
- Add reading-from-file feature to `project` and `topic` inputs (content enclosed by square brackets means it's a file path) [GS-128].
- Add "examples/instructions.md" to build the `project` input as a PRD file (Product Requirements Document) [GS-128].
- Add Camel-AI agent society to the agent libraries.

### Changed
- Change: remove the GenericSuite dependency.

### Fixed
- Fix the agents and task prompts to effectively work as a team [GS-128].


## [0.0.1] - 2024-09-15

### Added
- Project creation during the "AI Agents Hack With Lablab.ai and MindsDB" hackathon.
