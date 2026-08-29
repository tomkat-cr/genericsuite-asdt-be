# CLAUDE.md

This file provides guidance to AI Coding Assistants (Claude Code, Gemini CLI, Cursor, Antigravity, etc.) when working with code in this repository.

## Project Overview

GenericSuite Agentic Software Development Team (ASDT) is a multi-agent AI system that orchestrates AI agents to collaborate on software development tasks (coding, testing, architecture, DevOps, etc.). The repo supports multiple agent frameworks: **CrewAI** (primary) and **CamelAI** (LangGraph, and Smolagents planned).

## Repository Structure

The repo uses a **nested Poetry project** layout:

- `genericsuite_asdt/crewai/` — CrewAI implementation (its own `pyproject.toml`)
- `genericsuite_asdt/camelai/` — CamelAI implementation (its own `pyproject.toml`)
- Root `pyproject.toml` — Top-level package (meta / shared)
- `scripts/` — Shell orchestration scripts

Each framework subdirectory is an independent Poetry project that must be installed separately.

## Commands

All commands are run from the **repo root** via `make` or by cd-ing into the framework subdirectory.

### Install

```bash
make crewai_install      # poetry install inside genericsuite_asdt/crewai/
make camelai_install     # poetry install inside genericsuite_asdt/camelai/
```

### Test

```bash
make test                # runs crewai_test
make crewai_test         # pytest inside genericsuite_asdt/crewai/

# Single test file / pattern (from crewai subdirectory):
cd genericsuite_asdt/crewai && poetry run pytest tests/ -v -k "test_name"
```

### Run agents

```bash
# CLI (crew execution)
make crewai_run PROJECT="my-project" TOPIC="implement feature X"

# API server (FastAPI on port 8001)
make crewai_api
```

### Build / dependency management

```bash
make build               # poetry build (root)
make lock                # poetry lock (root)
make update              # poetry update (root)
```

The shell scripts `scripts/run_crewai_agents.sh` and `scripts/run_camelai_agents.sh` are the canonical entrypoints invoked by the Makefile.

## Environment Setup

Copy `.env.example` → `.env` inside the relevant framework directory and configure:

- LLM provider API keys: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GROQ_API_KEY`, etc.
- `OLLAMA_BASE_URL` (defaults to `http://localhost:11434` for local dev)
- `SERPER_API_KEY` — web search via SerperDevTool
- LLM selection env vars control which provider/model is used per agent role

Default local setup uses **Ollama**.

## Architecture

### CrewAI implementation (`genericsuite_asdt/crewai/genericsuite_asdt/`)

| File | Purpose |
|------|---------|
| `main.py` | Entry points: `run()`, `stream_run()`, `train()`, `test()`, `replay()` |
| `crew.py` | `GenericsuiteAsdtCrew` — assembles agents and tasks from YAML |
| `generic_agents.py` | Reads YAML configs; generic agent/task factory |
| `llm.py` | LLM provider abstraction — maps env vars to LiteLLM/CrewAI LLM instances |
| `api.py` | FastAPI app with `/generate` streaming endpoint |

Configuration lives in `config/agents.yaml` (agent roles, goals, backstories, LLM selection) and `config/tasks.yaml` (task definitions, context dependencies, output files).

### Agent roles defined in `agents.yaml`

Senior Software Engineer, QA Engineer, Test Engineer, Software Architect, Frontend Developer, Backend Developer, DevOps Engineer, UI/UX Designer — each can have a distinct LLM provider/model.

### LLM abstraction (`llm.py`)

Supports: OpenAI, Anthropic, Google Gemini, Ollama, HuggingFace, Groq, Together AI, OpenRouter, Bedrock, Vertex AI. Provider is selected via environment variables; the abstraction returns a CrewAI-compatible LLM object.

### Tools (`genericsuite_asdt/tools/`)

Custom CrewAI tools extend `BaseTool`. `SerperDevTool` provides web search. Tools are attached to agents in `crew.py`.

### Utilities (`genericsuite_asdt/utils/`)

- `app_logger.py` — structured logging
- `utilities.py` — result set helpers, input normalization, LLM provider/name resolution
- `monitoring.py` — OpenLIT observability integration

### API streaming flow

`api.py` `/generate` → `stream_run()` in `main.py` → `GenericsuiteAsdtCrew().crew().kickoff_async()` → streams token events via `StreamingResponse`.

## Important Notes

- The files `AGENTS.md`, `GEMINI.md`, etc. (if present) have only a referece to `@CLAUDE.md` — edit only `CLAUDE.md`.
- Skills live in `.ai/skills/` (source of truth); symlinked under `.agents/skills/`, `.claude/skills/`, `.codex/skills/`, `.gemini/skills/`, and `.devin/skills/`.
