# CHANGELOG

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/) and [Keep a Changelog](http://keepachangelog.com/).



## Unreleased
---

### New

### Changes

### Fixes

### Breaks


## 0.1.0 (2025-02-08)
---

### New
Add LLM selection and configuration using environment variables, and including OpenAI, Google, Ollama, Anthropic, Hugging Face, Groq, NVIDIA, X AI, Together AI, AI/ML API and OpenRouter [GS-168].
Add the ideation task to generate ideas for the "AIstronauts-Space Agents on a mission hackathon" from lablab.ai [GS-55].
Add different environment variables for coding, reasoning, planning and management llms and models, so normal agents, manager agent and planning agent can use them [GS-168].
Add the planning agent, so the code generation actions are fired and iterated [GS-168].
Add "openlit" monitoring tool [GS-168].
Add "agentops" monitoring tool [GS-168].
Add generate output files on each task [GS-168].
Add automatic generation of the crew, agents and tasks directly from the yml files with no need to specify decorated class and methods [GS-168].

### Changes
Change: remove the genericuiste dependency.

### Fixes
Fix the agents and task prompts to effectively work as a team [GS-168].


## 0.0.1 (2024-09-15)
---

### New
Project creation during the "AI Agents Hack With Lablab.ai and MindsDB" hackathon.
