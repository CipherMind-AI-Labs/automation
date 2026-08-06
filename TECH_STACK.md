# TECH_STACK.md

# Technology Stack

## Purpose

This document defines the approved technology stack for the Automation platform.

The goals are:

- simplicity
- maintainability
- extensibility
- low operational cost
- vendor independence

New dependencies should only be introduced when they provide a clear architectural benefit.

---

# Core Principles

- LLMs for reasoning
- Python for execution
- Open-source whenever practical
- Open-weight language models
- Strong typing
- Modular architecture
- Local-first development
- Cloud-ready deployment

---

# Programming Language

## Python

Version

Python 3.13+

Reason

- mature AI ecosystem
- excellent tooling
- large community
- ideal for automation
- strong support for async workflows

---

# Package Management

## uv

Purpose

Package management

Dependency resolution

Virtual environments

Reason

Fast

Reliable

Modern replacement for pip + venv

---

# Agent Framework

## LangGraph

Purpose

Graph-based orchestration

Reason

- stateful workflows
- branching
- retry loops
- checkpoints
- human-in-the-loop
- production-ready

LangGraph is used only for orchestration.

Business logic belongs inside agents.

---

# Inference Runtime

The system should remain independent of the underlying inference runtime.

Development may use

- Ollama
- llama.cpp

Production may use

- vLLM
- other OpenAI-compatible inference servers

Changing runtimes should require configuration changes only.

Reason

Run models locally

No API cost

Privacy

Model flexibility

---

# Language Models

Primary Model

Qwen 3

Recommended Size

4B–8B depending on available hardware.

The model should be configurable.

The architecture must support multiple models simultaneously.

Future additions

- Gemma
- Mistral
- Llama

---

# Database

PostgreSQL

Purpose

Persistent storage

Reasons

- reliable
- scalable
- mature
- excellent Python support

SQLite may be used for local development.

---

# ORM

SQLAlchemy

Reason

Mature

Flexible

Well tested

---

# Data Validation

Pydantic

Purpose

Configuration

Validation

Typed models

---

# Browser Automation

Playwright

Purpose

Website interaction

Form filling

Authentication

Lead research

Reasons

Reliable

Modern

Excellent async support

---

# HTTP Client

httpx

Reason

Async support

Modern API

---

# Email

Gmail API

Future

Microsoft Graph API

Emails should never be sent directly through SMTP.

---

# Search

Initially

Manual browser automation

Future

Search API providers

The search provider should be abstracted behind a common interface.

---

# Logging

Python logging

Future

OpenTelemetry

Logfire

Every workflow must be traceable.

---

# Configuration

Environment variables

.env

No secrets inside source code.

---

# Testing

pytest

Coverage

Business logic

Tools

Workflow execution

---

# Code Quality

ruff

Formatting

linting

Static analysis

---

# Type Checking

mypy

Every public API should be typed.

---

# Documentation

Markdown

Architecture Decision Records (future)

---

# Version Control

Git

GitHub

GitHub Desktop

---

# Development Environment

VS Code

GitHub Desktop

Docker Desktop (future)

---

# Dependency Policy

Every dependency must satisfy at least one of the following:

- removes significant complexity
- improves reliability
- improves maintainability
- becomes part of the core architecture

Avoid adding libraries that only save a few lines of code.

---

# Future Technologies

Possible additions

Redis

Celery

Temporal

LiteLLM

OpenTelemetry

S3-compatible object storage

These are not part of the initial implementation.

---

# Technologies Explicitly Avoided

Avoid introducing technologies solely because they are popular.

Examples include:

- unnecessary microservices
- multiple databases
- multiple agent frameworks
- framework-specific business logic
- tightly coupled vendor APIs

The architecture should remain portable.

---

# Technology Review

Technology decisions should be reviewed periodically.

New technologies should be adopted only when they provide measurable benefits over the existing stack.

---

# LLM Usage Policy

LLMs should be used only for tasks requiring reasoning.

Examples

- planning
- writing
- summarization
- research
- qualitative evaluation
- extraction

LLMs should not be used for deterministic operations.

Examples

- SQL queries
- duplicate detection
- calculations
- scheduling
- API orchestration
- persistence

Prefer Python whenever a deterministic solution exists.

---

# Hardware Strategy

Development

CPU-first development should be supported.

Recommended models

4B–8B

Future

The architecture should support GPU acceleration without requiring application changes.

Inference runtimes should remain interchangeable.