# AGENT.md

# Automation Repository

## Purpose

This repository contains the company's internal AI automation platform.

The goal is to build AI agents that automate the founder's daily work, increase execution speed, and reduce repetitive tasks. These agents are **internal-only** and are not part of the customer-facing product.

Customer-facing AI agents will live in a separate repository.

---

# Vision

Create an AI workforce that can assist with every major business function while always keeping the founder in control of important decisions.

The system should evolve from simple assistants into autonomous agents capable of planning, executing, validating, and improving their own work.

---

# Initial Business Areas

The first version focuses on sales.

Future areas include:

- Marketing
- CRM
- Operations
- Finance
- Hiring
- Customer Success
- Product Management
- Engineering

---

# Long-Term Goal

The founder should eventually be able to issue commands such as:

"Find me 30 qualified furniture dealers."

"Prepare personalized outreach."

"Review today's pipeline."

"Summarize all replies."

"Schedule follow-ups."

"Research this company."

The system should execute these tasks with minimal supervision while requesting approval before irreversible actions.

---

# Core Principles

1. Human approval before sending emails.

2. Every important decision must be traceable.

3. Agents validate their own work.

4. Never hallucinate facts.

5. Use deterministic code whenever possible.

6. Use LLM reasoning only when necessary.

7. Build reusable components.

8. Keep architecture modular.

9. Every action should be logged.

10. Every agent should have measurable success criteria.

---

# Architecture

The system is composed of specialized agents coordinated by an orchestrator.

Example:

Founder

↓

Orchestrator

↓

Lead Research Agent

Validation Agent

Outreach Agent

CRM Agent

Founder Briefing Agent

Each agent owns one responsibility.

Agents share state but should remain loosely coupled.

---

# Agent Philosophy

An agent is goal-driven.

Each agent:

- receives a goal
- plans work
- executes tools
- validates results
- retries when necessary
- reports completion

Agents should not blindly execute fixed workflows.

---

# Validation

Every important output must be validated.

Examples:

Lead Research

- company exists
- website reachable
- industry matches ICP
- confidence score acceptable

Email

- personalized
- factual
- no hallucinations
- clear CTA

CRM

- duplicate detection
- status consistency
- follow-up exists

Validation failures should trigger retries or human review.

---

# Current Roadmap

Phase 1

Internal sales automation

- Lead Research Agent
- Validation Agent
- Outreach Agent
- CRM Agent
- Founder Briefing Agent

Phase 2

Marketing automation

Phase 3

Operations automation

Phase 4

Finance automation

Phase 5

Cross-agent collaboration

---

# Technology

Language

Python 3.13+

Primary Model

Open-weight models (Qwen preferred)

Database

PostgreSQL

Development

GitHub

GitHub Desktop

VS Code

Architecture

Graph-based orchestration

Structured state

Persistent memory

Typed models

---

# Coding Standards

- PEP 8
- Type hints
- Dataclasses or Pydantic where appropriate
- Small focused modules
- Comprehensive logging
- Unit tests for business logic
- No duplicated logic
- Clear docstrings
- Dependency injection where practical

---

# Repository Goal

This repository should become the company's internal automation platform.

It should automate repetitive work while remaining reliable, explainable, maintainable, and easy to extend.

Every design decision should prioritize long-term maintainability over short-term convenience.