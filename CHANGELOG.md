# CHANGELOG

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/) and [Keep a Changelog](http://keepachangelog.com/).



## Unreleased
---

### New

### Changes

### Fixes

### Breaks


## 0.1.0 (2025-02-17)
---

### New
Add LLM selection and configuration using environment variables, and including OpenAI, Google, Ollama, Anthropic, Hugging Face, Groq, NVIDIA, X AI, Together AI, AI/ML API and OpenRouter [GS-128].
Add the ideation task to generate ideas for the "AIstronauts-Space Agents on a mission hackathon" from lablab.ai [GS-55].
Add different environment variables for coding, reasoning, planning and management llms and models, so normal agents, manager agent and planning agent can use them [GS-128].
Add the planning agent, so the code generation actions are fired and iterated [GS-128].
Add "openlit" monitoring tool [GS-128].
Add "agentops" monitoring tool [GS-128].
Add generate output files on each task [GS-128].
Add automatic generation of the crew, agents and tasks directly from the yaml files with no wrappers (decorated class and methods) [GS-128].
Add "allow_code_execution" to developer and automated testing agents [GS-128].
Add reading-from-file feature to `project` and `topic` inputs (content enclosed by square brackets means it's a file path) [GS-128].
Add "examples/instructions.md" to build the `project` input as a PRD file (Product Requirements Document) [GS-128].
Add Camel-AI agent society to the agent libraries.

### Changes
Change: remove the GenericSuite dependency.

### Fixes
Fix the agents and task prompts to effectively work as a team [GS-128].


## 0.0.1 (2024-09-15)
---

### New
Project creation during the "AI Agents Hack With Lablab.ai and MindsDB" hackathon.
