# Session Memory Evaluation

Date: 2026-03-23
Scope: Self-bootstrap and control experiments

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

#### Treatment Arm

The fresh session starts from:

- `uv run python scripts/session_memory.py assemble --project-id <project_id> --output <artifact>`

After reading the packet, it may use:

- repo files
- git status
- code search
- docs
- explicit `session-memory` recall commands

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

## Result Handling

Experiment results should produce durable memory only when they reveal a stable
lesson.

Examples:

- a new cross-project pattern if treatment repeatedly reduces recovery cost
- a failure record if the packet repeatedly causes the same bad inference
- a decision record if one assembly rule proves consistently superior
