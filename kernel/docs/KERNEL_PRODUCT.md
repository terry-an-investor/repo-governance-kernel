# Kernel Product

Date: 2026-03-24
Scope: reusable repo-governance kernel definition

## Product Definition

The kernel is a reusable repo-governance core.

It owns:

- explicit control objects
- legal transition semantics
- audit and enforcement runtime
- bounded registry-owned execution

It does not own:

- one specific repository's product narrative
- dogfood sample history
- repo-local smoke or evaluation workflows

## Core Objects

- objective
- round
- task-contract
- exception-contract
- adjudication

## Execution Boundary

The kernel supports bounded registry-owned execution.

It is not a general autonomous rewrite engine.

## Canonical Implementation Surfaces

- `kernel/transition_specs.py`
- `kernel/round_control.py`
- `kernel/control_enforcement.py`
- `kernel/resolver_runtime.py`
- `kernel/executor_command_builder.py`
- `kernel/executor_runtime.py`
- `kernel/audit_control_state.py`
- `kernel/cli.py`
- `kernel/commands/`
