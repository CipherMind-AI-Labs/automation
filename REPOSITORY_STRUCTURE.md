# REPOSITORY_STRUCTURE.md

# Repository Structure

## Purpose

This document defines the directory structure of the Automation repository.

The objectives are:

- clear separation of responsibilities
- high cohesion
- low coupling
- modular development
- predictable organization
- long-term maintainability

Every file should have one obvious location.

---

# Repository Overview

```
automation/

├── agents/
├── orchestrator/
├── workflows/
├── tools/
├── services/
├── state/
├── memory/
├── models/
├── prompts/
├── config/
├── database/
├── integrations/
├── utils/
├── tests/
├── docs/
├── scripts/
├── logs/
│
├── main.py
├── pyproject.toml
├── uv.lock
├── README.md
├── AGENT.md
├── ARCHITECTURE.md
├── TECH_STACK.md
└── REPOSITORY_STRUCTURE.md
```

---

# Directory Responsibilities

## agents/

Contains all business agents.

Each agent owns exactly one business capability.

Example

```
agents/

    lead_research/

    validation/

    outreach/

    crm/

    founder/
```

Each agent should contain only its own logic.

Agents should never directly depend on one another.

---

## orchestrator/

Responsible for coordinating agent execution.

Responsibilities

- graph execution
- routing
- retries
- workflow state transitions
- human approvals
- checkpoint management

No business logic belongs here.

---

## workflows/

Defines complete business workflows.

Examples

```
qualify_lead.py

outbound_campaign.py

daily_brief.py

weekly_pipeline_review.py
```

A workflow combines multiple agents into one business process.

---

## tools/

Contains deterministic tools used by agents.

Example

```
browser/

database/

email/

calendar/

filesystem/

llm/

notifications/

search/
```

Rules

Tools never contain business logic.

Tools should be reusable.

Tools should expose stable interfaces.

---

## services/

Application-level reusable services.

Examples

```
llm_service.py

logging_service.py

configuration_service.py

storage_service.py
```

Unlike tools, services coordinate infrastructure components.

---

## state/

Defines workflow state.

Examples

```
LeadState

CampaignState

WorkflowState
```

State is shared between agents.

Agents communicate only through state.

---

## memory/

Agent memory management.

Examples

```
working_memory/

session_memory/

persistent_memory/
```

This directory contains memory abstractions.

Persistent storage belongs in the database layer.

---

## models/

Application models.

Examples

```
Lead

Company

Contact

Campaign

Email

Task
```

Models represent business entities.

---

## prompts/

Prompt templates.

Example

```
lead_research.md

email_review.md

company_summary.md

daily_brief.md
```

Prompt text should never be hardcoded inside Python files.

---

## config/

Application configuration.

Examples

```
settings.py

models.py

logging.py
```

Environment-specific configuration belongs here.

---

## database/

Database implementation.

Examples

```
connection.py

repositories/

migrations/

seed.py
```

Only this directory should communicate directly with the database.

---

## integrations/

Third-party integrations.

Examples

```
gmail/

github/

linkedin/

notion/

slack/
```

Every external system should have its own integration module.

---

## utils/

General-purpose helper functions.

Avoid placing business logic here.

Utilities should remain small and reusable.

---

## tests/

Repository test suite.

Suggested organization

```
unit/

integration/

workflow/
```

Every business workflow should have tests.

---

## docs/

Project documentation.

Examples

```
architecture/

agents/

development/

decisions/
```

Technical documentation belongs here.

---

## scripts/

Development utilities.

Examples

```
initialize_database.py

reset_environment.py

generate_test_data.py
```

Scripts should not be imported by application code.

---

## logs/

Application logs.

Should never be committed to Git.

---

# Root Files

## main.py

Application entry point.

Responsible only for application startup.

---

## pyproject.toml

Project configuration.

Dependencies

Tool configuration

Package metadata

---

## README.md

Repository introduction.

Installation

Quick start

Development setup

---

## Documentation Files

The root documentation defines the engineering standards.

AGENT.md

Project mission and objectives.

ARCHITECTURE.md

System architecture.

TECH_STACK.md

Approved technologies.

REPOSITORY_STRUCTURE.md

Repository organization.

---

# Dependency Rules

Allowed

```
Workflow

↓

Orchestrator

↓

Agent

↓

Service

↓

Tool

↓

Integration
```

Not Allowed

- Tool calling Agent
- Tool calling Workflow
- Agent calling another Agent directly
- Integration accessing State
- Prompt importing Python modules

---

# Agent Rules

Every agent should contain:

```
agent.py

planner.py

validator.py

README.md
```

Optional

```
prompts/

examples/

tests/
```

Each agent should be independently testable.

---

# Tool Rules

Each tool should expose a single public interface.

Example

```
BrowserTool

EmailTool

DatabaseTool
```

Internal implementation details should remain private.

---

# Prompt Rules

Prompts are version-controlled assets.

Rules

- no inline prompts
- one responsibility per prompt
- descriptive filenames
- reusable across agents

---

# Logging Rules

Every workflow should log:

- start
- completion
- retries
- failures
- tool calls
- validation results

Logging should be centralized.

---

# Naming Conventions

Directories

snake_case

Python files

snake_case.py

Classes

PascalCase

Functions

snake_case

Constants

UPPER_CASE

Prompt files

snake_case.md

---

# Design Principles

- Single Responsibility Principle
- Composition over inheritance
- Dependency injection where appropriate
- Strong typing
- Small modules
- Deterministic execution where possible
- LLMs for reasoning
- Python for execution

---

# Future Expansion

This structure should support future additions without major refactoring.

Examples

- additional agents
- new workflows
- new integrations
- customer-facing automation (in a separate repository)
- distributed execution
- multiple inference backends

The repository structure should remain stable as the platform grows.