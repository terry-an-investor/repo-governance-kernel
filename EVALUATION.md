# Session Memory Evaluation

Date: 2026-03-23
Scope: Controlled recovery experiments across evolving projects

## Goal

Evaluate whether `session-memory` actually improves fresh-session recovery for
coding work instead of only feeling helpful.

The primary question is:

Can a new coding-agent session recover the correct project state faster and with
fewer mistakes when it starts from `session-memory` artifacts?

## Evaluation Principle

`session-memory` may dogfood itself, but it must not self-certify by narrative
alone.

Use controlled comparisons.

The default comparison is:

- control:
  - a fresh session starts from the repo and ordinary code/doc inspection only
- treatment:
  - a fresh session starts by reading the assembled `session-memory` handoff
    packet first, then may inspect the repo

## Primary Capability Under Test

Phase 1 should be judged mainly on recovery quality, not on abstract search
quality.

The main capability questions are:

- handoff quality
  - does the packet let a fresh session state the current task correctly
- continuity quality
  - does it reduce repeated file/history exploration
- decision preservation
  - does it preserve important architecture boundaries
- retrieval usefulness
  - does the indexed memory help locate the right durable items quickly

## Experiment Shape

### Frozen Evaluation Bundle

The repeated problem class is:

- comparing fresh-session recovery fairly on a repo that is still moving

The missing reusable primitive is:

- one frozen `evaluation bundle` that both arms consume unchanged

The lowest honest owner layer is:

- `session-memory` evaluation tooling and artifacts
- not the target repo being evaluated

Each experiment should first materialize one bundle containing:

- `snapshot/`
  - one frozen copied repo tree or fixed-commit worktree
- `task.md`
  - exact prompt, constraints, and success condition
- `ground-truth.md`
  - facts the scorer will treat as correct for that snapshot
- `treatment-packet.md`
  - assembled `session-memory` handoff packet used only by treatment
- `score-template.md`
  - rubric and metric sheet fixed before either run
- `run-config.json`
  - model, sandbox, approval mode, writable roots, and output paths

Control and treatment must read from the same bundle.

Do not let either arm read directly from a live mutable repo after the bundle is
frozen.

### 1. Choose one bounded task slice

A task slice should be:

- real
- small enough to finish in one round
- ambiguous enough that context recovery actually matters

Good examples:

- add the first real `memory_links` sample
- tighten `assemble_context.py` output again
- change query result formatting without violating phase-1 boundaries

Bad examples:

- trivial typo fixes
- tasks that require no project state recovery

### 2. Freeze the task statement first

Before starting either arm:

- write the exact task prompt
- write the expected constraints
- write the expected success condition
- freeze the repo snapshot that will be mounted for both arms
- freeze the scorer's ground truth against that same snapshot

Do not rewrite the task after seeing results.

### 3. Run two fresh-session arms

#### Control Arm

The fresh session may use:

- repo files
- git status
- code search
- docs

The fresh session may not start from:

- assembled session packet
- pre-selected memory recall output
- treatment-only hints hidden in the scoring notes

#### Treatment Arm

The fresh session starts from:

- `uv run python scripts/session_memory.py assemble --project-id <project_id> --output <artifact>`

After reading the packet, it may use:

- repo files
- git status
- code search
- docs
- explicit `session-memory` recall commands

The treatment arm still uses the same frozen snapshot as control.
The packet is the only allowed difference.

### 4. Record objective measurements

Record at least:

- `time_to_orientation`
  - how long until the session can correctly describe current goal, risks, and
    next steps
- `time_to_first_valid_change`
  - how long until the first correct code or doc change lands
- `state_recall_accuracy`
  - how many key facts were recovered correctly
- `omission_count`
  - how many key facts were missed
- `wrong_inference_count`
  - how many incorrect assumptions were made
- `recovery_cost`
  - number of extra files opened, searches run, or commands issued to regain
    context

### 5. Record qualitative notes separately

Also record:

- where the packet helped
- where it was noisy
- which parts were redundant
- which missing memory items should have existed but did not

Do not let qualitative notes replace the metrics above.

## Minimum Scoring Template

For each arm, capture:

```text
task_id:
project_id:
arm: control | treatment
time_to_orientation:
time_to_first_valid_change:
state_recall_accuracy:
omission_count:
wrong_inference_count:
recovery_cost:
result: success | partial | fail
notes:
```

## Success Criteria

`session-memory` is helping if the treatment arm usually shows:

- lower `time_to_orientation`
- lower `recovery_cost`
- equal or lower `wrong_inference_count`
- equal or higher `state_recall_accuracy`

It is not enough for treatment to feel nicer.

It should measurably improve recovery while preserving correctness.

## Known Evaluation Biases

Watch for these failure modes:

- the task is too easy, so memory does not matter
- the packet is bloated, so success only comes from copying large source text
- the evaluator already knows the expected answer
- the treatment arm gets a different task than control
- schema or retrieval rules change during the experiment

## Current Default Experiment

Recommended near-term experiment:

- project:
  - `session-memory`
- task:
  - add the first real linked-memory sample using `supersedes` or
    `superseded_by`
- control:
  - fresh session without assembled packet
- treatment:
  - fresh session starts from
    `artifacts/session-memory/session-context-smoke.md`

This experiment is good because:

- it requires recovering current phase-1 boundaries
- it requires locating the right schema and builder files
- it is easy to score for correctness

## External Project Evaluation

For serious validation, prefer an external actively changing project rather than
`session-memory` itself.

Recommended shape:

- use a copied working-tree snapshot when current dirty state matters
- start with orientation-only tasks before code-changing tasks
- score recovery quality first, implementation quality second

`wind-agent` is the first target because it has real scope drift, live
validation history, and durable architecture debt that a fresh session must
recover correctly.

## Result Handling

Experiment results should produce durable memory only when they reveal a stable
lesson.

Examples:

- a new cross-project pattern if treatment repeatedly reduces recovery cost
- a failure record if the packet repeatedly causes the same bad inference
- a decision record if one assembly rule proves consistently superior
