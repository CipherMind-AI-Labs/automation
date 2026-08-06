# ARCHITECTURE.md

# Automation Platform Architecture

## Purpose

This document defines the technical architecture of the internal automation platform.

The architecture should support:

- modular development
- independent agents
- graph-based orchestration
- shared state
- human approvals
- persistent memory
- extensibility

The implementation should evolve without changing the architectural principles.

---

# High-Level Architecture

```
                    Founder
                       │
                       ▼
               Orchestrator Agent
                       │
      ┌────────────────┼────────────────┐
      │                │                │
      ▼                ▼                ▼
 Lead Research    Validation      Outreach
     Agent           Agent          Agent
      │                │                │
      └────────────┬───┴────────────────┘
                   │
                   ▼
               CRM Agent
                   │
                   ▼
          Founder Briefing Agent
```

The orchestrator coordinates work.

Specialized agents perform individual responsibilities.

Agents communicate through shared state.

---

# Design Principles

## Single Responsibility

Each agent owns exactly one business capability.

Example

Lead Research Agent

Responsibilities

- research companies
- identify contacts
- gather company information

Not responsible for

- email writing
- CRM updates
- follow-ups

---

## Shared State

Agents never communicate directly.

Instead they read and update a shared state.

Example

```
LeadState

company

contacts

research_summary

validation

crm_status

email_draft

activity_log
```

The orchestrator passes this state between agents.

---

## Goal Driven Execution

Every agent receives

- current state
- goal

Example

Goal

```
Produce one qualified lead.
```

The agent decides

- which tools to call
- what information is missing
- whether another attempt is needed

---

# Intelligence Boundary

The platform separates reasoning from execution.

LLMs are responsible for:

- planning
- research
- summarization
- writing
- qualitative validation
- decision making
- extracting structured information

Python is responsible for:

- database operations
- API calls
- browser automation
- calculations
- scheduling
- deterministic validation
- persistence
- logging
- external integrations

Deterministic Validation

Performed by Python.

Examples

- duplicate detection
- required fields
- email format
- CRM integrity
- scheduling

Reasoning Validation

Performed by an LLM.

Examples

- research completeness
- email quality
- personalization
- summary quality
- confidence assessment

LLMs never become the source of truth.

Python and the database remain the authoritative source for system state and facts.
---

# Validation

Every major step must be validated.

Example

Lead Research

Success Criteria

✓ company identified

✓ website verified

✓ industry matches ICP

✓ confidence > threshold

Otherwise

Retry

or

Escalate for manual review

---

# Human Approval

Certain actions require approval.

Examples

- sending emails
- deleting records
- modifying customer data
- bulk operations

Everything else may execute automatically.

---

# Agent Lifecycle

Every agent follows the same lifecycle.

```
Receive Goal
        │
        ▼
LLM Planning
        │
        ▼
Python Tool Execution
        │
        ▼
LLM Reasoning
        │
        ▼
Validation
   ├── Python Rules
   └── LLM Review
        │
        ▼
Success?
   ├── Yes
   └── Retry
        │
        ▼
Persist State
        │
        ▼
Complete
```

---

# Tools

Agents do not implement business logic.

They use tools.

Examples

Browser Tool

Database Tool

Email Tool

Calendar Tool

Search Tool

Document Tool

LLM Tool

Logging Tool

Notification Tool

Each tool should have a well-defined interface.

---

# Memory

Three memory layers.

## Working Memory

Current execution only.

---

## Session Memory

Persists until workflow completes.

---

## Persistent Memory

Stored in database.

Examples

Lead history

Email history

Meeting history

Previous interactions

Agent metrics

---

# Workflow Model

The platform uses graph-based execution.

Each node

- performs one task
- validates output
- determines next node

Example

```
Research

↓

Validation

↓

Pass?

├── Yes

↓

Find Contact

└── No

↓

Retry Research
```

---

# Logging

Every execution records

- timestamps
- agent
- tool calls
- inputs
- outputs
- validation results
- retries
- execution time

Nothing should execute silently.

---

# Error Handling

Every failure belongs to one category.

Recoverable

Retry automatically.

Temporary

Retry later.

Permanent

Escalate.

Human Required

Pause workflow.

---

# Repository Structure

```
automation/

    agents/
    orchestrator/
    workflows/
    tools/
    models/
    memory/
    prompts/
    config/
    services/
    database/
    integrations/
    logs/
    tests/
    docs/
```

---

# Current Agents

Lead Research Agent

Validation Agent

Outreach Agent

CRM Agent

Founder Briefing Agent

---

# Future Agents

Marketing Agent

Proposal Agent

Finance Agent

Meeting Agent

Hiring Agent

Operations Agent

Product Agent

Customer Success Agent

Analytics Agent

---

# Engineering Guidelines

Business logic belongs inside agents.

External systems belong inside tools.

State belongs inside models.

Configuration belongs inside config.

Never hardcode credentials.

Avoid circular dependencies.

Prefer composition over inheritance.

Keep modules small.

Every public function should be typed.

Every important decision should be logged.

Every workflow should be reproducible.

---

# Long-Term Goal

The automation platform should become the operational layer of the company.

New agents should be added without modifying existing agents.

The architecture should remain modular, testable, observable, and maintainable as the number of agents and workflows grows.