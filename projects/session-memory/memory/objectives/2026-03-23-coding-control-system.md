---
id: obj-2026-03-23-0002
type: objective
title: Coding control system built on a memory substrate
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 0d603f3e2ed77feed60c71812169593f982cbaad
paths:
  - CONTROL_SYSTEM.md
  - DESIGN_PRINCIPLES.md
  - ARCHITECTURE.md
  - SCHEMA.md
  - IMPLEMENTATION_PLAN.md
  - projects/session-memory/control/
thread_ids: []
evidence_refs:
  - type: doc
    ref: C:/Users/terryzzb/Desktop/session-memory/CONTROL_SYSTEM.md
  - type: doc
    ref: C:/Users/terryzzb/Desktop/session-memory/SCHEMA.md
  - type: note
    ref: C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/current/current-task.md
tags:
  - objective
  - control-system
  - active
confidence: high
created_at: 2026-03-23T21:10:00+08:00
updated_at: 2026-03-23T21:10:00+08:00
supersedes:
  - obj-2026-03-23-0001
superseded_by: []
phase: execution
---

## Summary

The project should evolve from a memory-focused handoff system into a coding
control system that uses memory as its storage substrate.

## Problem

The real user pain is not only recovering facts. It is preserving direction,
containing temporary hacks, supporting project-aware review, and handling pivot
without losing provenance.

## Success Criteria

- active objective and pivot lineage are first-class
- context assembly prefers active control state over raw recency
- temporary workarounds are tracked separately from target design
- reviewer or side-session contexts can be compiled from project control state

## Non-Goals

- generic role prompts without durable project knowledge
- replacing git or project docs
- broad semantic retrieval before file workflow proves itself

## Why Now

The file-first memory path is already proven enough to expose the real next
bottleneck: objective drift, uncontrolled workaround debt, and fresh sessions
that still lack an explicit control line.

## Current Phase

Execution. The objective is clear enough to guide implementation, but the
control layer still needs to be wired into scripts and evaluation.

## Active Risks

- The system can still regress into a memory-only framing if control objects do
  not become operational inputs.
- Overfitting the schema to one project's governance remains a risk.

## Supersession Notes

This objective replaces the narrower memory-and-handoff framing while retaining
its file-first storage and retrieval foundation.
