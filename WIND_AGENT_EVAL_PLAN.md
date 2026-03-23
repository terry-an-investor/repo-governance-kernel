# Wind-Agent Evaluation Plan

Date: 2026-03-23
Scope: Headless control-vs-treatment evaluation with `codex exec`

## Goal

Use `wind-agent` as the first serious external evaluation target for
`session-memory`.

The purpose is to test whether a fresh headless Codex instance can recover the
current engineering state of `wind-agent` more accurately and with lower
recovery cost when it starts from a `session-memory` handoff packet.

## Design Summary

The repeated problem class is:

- evaluating fresh-session recovery on a repo whose live working state keeps
  moving

The missing reusable primitive is:

- one frozen `wind-agent` evaluation bundle

The lowest honest owner layer is:

- `session-memory` evaluation tooling and artifacts
- not ad hoc logic inside `wind-agent`

So this experiment should not be "run two prompts against the live repo".

It should be:

1. freeze one copied `wind-agent` snapshot
2. freeze one task and one scorer ground truth against that snapshot
3. generate one treatment packet from `session-memory`
4. run control and treatment headlessly against the same snapshot
5. score both arms from the same fixed rubric

## Why `wind-agent`

`wind-agent` is a better evaluation target than `session-memory` itself because:

- it is actively changing
- it contains real architecture drift and validation history
- it has meaningful current-state complexity
- it matches the original user pain point more closely

In particular, `wind-agent` already has:

- an active round contract
- real validation artifacts
- a dirty worktree
- canonical architecture docs
- evolving owner-layer debt

That makes it a credible test of session continuity.

## Fairness Standard

The experiment is only fair if control and treatment differ in one thing only:

- control does not receive the `session-memory` handoff packet
- treatment receives the `session-memory` handoff packet first

Everything else should be held fixed:

- same repository snapshot
- same task prompt
- same model
- same sandbox mode
- same approval mode
- same writable directories
- same scoring sheet prepared before results are read

## Evaluation Bundle Layout

For each run, materialize:

```text
artifacts/evaluation/wind-agent/<run-id>/
├── bundle/
│   ├── snapshot/
│   ├── task.md
│   ├── ground-truth.md
│   ├── treatment-packet.md
│   └── run-config.json
├── control.prompt.txt
├── control.jsonl
├── control.last.txt
├── treatment.prompt.txt
├── treatment.jsonl
├── treatment.last.txt
└── score.md
```

This layout matters because it keeps the frozen evaluation object separate from
the run outputs derived from it.

## Snapshot Rule

Do not evaluate against a moving repo.

Before running either arm, freeze one evaluation snapshot of `wind-agent`.

Preferred options:

1. exact copied working tree snapshot
   - best when you want current dirty state included
2. fixed commit worktree
   - best when you want cleaner reproducibility

For the first evaluation, prefer a copied working tree snapshot so the test
reflects the real current state that a new session would face.

The snapshot should be created once, then mounted read-only for both arms.

Do not point `codex exec` at the live `C:/Users/terryzzb/Desktop/wind-agent`
tree after the bundle is frozen.

## Recommended First Experiment

Start with an orientation-only task.

Do not start with a code-changing task.

Why:

- it isolates recovery quality from implementation skill
- it avoids mutating the source repo during evaluation
- it makes scoring much easier

### Task

Ask the agent to produce a structured recovery report that answers:

- what is the active round
- what has been validated already
- where the current worktree exceeds the declared round scope
- what the top 3 current risks are
- what the next 3 concrete steps should be
- which 5 files should be read first

This task directly measures the value of handoff memory.

## Prompt Design

Use the same prompt body for both arms.

### Shared Prompt Body

```text
You are evaluating the current engineering state of the wind-agent repository.

Do not modify files.
Do not write code.
Do not run destructive commands.

Your task is to recover the current project state and produce a structured report with these sections:

1. Active Round
2. Validated Facts
3. Scope Drift
4. Top Risks
5. Recommended Next Steps
6. First Files To Read

Requirements:
- Be concrete and repo-specific.
- Use only information you can justify from the repository state and artifacts available in the workspace.
- Keep the final answer concise but precise.
```

### Control Prompt

Use the shared prompt body only.

### Treatment Prompt

Prepend this block before the shared prompt body:

```text
Read this handoff packet first and use it as your initial orientation context:

<paste assembled session-memory packet here>
```

The rest of the prompt must remain identical.

The treatment packet should be a compact orientation artifact, not a raw source
dump.
If the packet wins only because it inlines too much repo text, the experiment is
not proving real memory quality.

## `codex exec` Execution Shape

Use headless fresh instances:

```bash
codex exec --ephemeral --json -C <snapshot_dir> "<prompt>"
```

Recommended fixed options:

- `--ephemeral`
- `--json`
- `-C <snapshot_dir>`
- `-s workspace-write` or `-s read-only`
- `-a never`

For the first orientation-only experiment, prefer:

```bash
codex exec --ephemeral --json -s read-only -a never -C <snapshot_dir> "<prompt>"
```

The harness should also capture:

- process start/end timestamps
- non-zero exit status
- last assistant answer
- total command/search/file-open counts derivable from JSON events

## Output Capture

Store artifacts separately for control and treatment:

```text
artifacts/evaluation/wind-agent/<run-id>/
├── control.prompt.txt
├── control.jsonl
├── control.last.txt
├── treatment.prompt.txt
├── treatment.jsonl
├── treatment.last.txt
└── score.md
```

Recommended capture flags:

- `--json > control.jsonl`
- `-o control.last.txt`

## Harness Architecture

The concrete harness can stay small if it is split into five steps:

1. `freeze_snapshot`
   - copy the current `wind-agent` working tree into the bundle
   - exclude obvious noise only if the exclusion rules are declared in advance
2. `freeze_ground_truth`
   - read the copied snapshot and write `ground-truth.md`
   - do this before either arm is run
3. `prepare_prompts`
   - write `control.prompt.txt` and `treatment.prompt.txt`
   - treatment prepends `treatment-packet.md`, nothing else
4. `run_arm`
   - invoke `codex exec --ephemeral --json`
   - one function, two parameterizations
5. `score_run`
   - compare outputs against `ground-truth.md`
   - produce `score.md` with both raw metrics and short judgment

This keeps the reusable primitive at the right layer:

- evaluation machinery lives in `session-memory/scripts/`
- target-repo knowledge lives in bundle inputs and scoring notes

## Scoring Rubric

Score each arm on the same rubric.

### Required Questions

The result should be checked for:

- correct `round_id`
- correct validated fact about query prepared-context reuse
- correct recognition that the dirty worktree exceeds the active round scope
- correct recognition of at least one risk tied to scope drift or validation drift
- plausible next steps consistent with repo constraints
- useful first-file list

### Metrics

Record:

- `time_to_orientation`
  - wall-clock from process start to final answer
- `state_recall_accuracy`
  - how many required questions are answered correctly
- `omission_count`
  - how many required facts are missing
- `wrong_inference_count`
  - how many important incorrect claims appear
- `recovery_cost`
  - command count
  - file-read count
  - search count

### Suggested Scoring Table

```text
task_id:
run_id:
repo_snapshot:
arm: control | treatment
time_to_orientation:
state_recall_accuracy:
omission_count:
wrong_inference_count:
recovery_cost:
result: success | partial | fail
notes:
```

## Expected Ground Truth For First Run

The current handoff packet suggests the likely correct core facts include:

- active round id:
  - `query-surface-producer-consumer-contract`
- validated fact:
  - real query prepared-context reuse was already proven
- main drift:
  - current dirty worktree extends beyond the declared round scope
- key risks:
  - round contract drift
  - validation coverage drift
  - governance drift

This ground truth should be checked against the actual frozen snapshot used in
the experiment.

Write the final `ground-truth.md` from the frozen snapshot, not from the live
repo and not from memory alone.

## Second Experiment After Orientation

Only after one clean orientation-only run should we try a code-changing task.

Recommended second task:

- ask the agent to update `session-memory` artifacts for the current
  `wind-agent` state on a copied workspace

That second task measures not just orientation, but whether memory improves the
quality of the first valid change.

## Failure Modes To Watch

- treatment prompt leaks too much raw source text
- the snapshot differs between control and treatment
- the repo changes between runs
- the scorer changes criteria after reading outputs
- one arm gets extra hints

## Decision Rule

Treat the result as a meaningful win only if treatment shows:

- lower time to orientation
- lower recovery cost
- equal or lower wrong inference count
- equal or higher state recall accuracy

If treatment is faster but less accurate, it is not a clear success.

## What This Design Proves

If this experiment works, it proves something narrow but important:

- a fresh headless instance can recover `wind-agent` state better from a
  compact memory packet than from raw repo inspection alone

It does not yet prove:

- that embeddings are needed
- that code-changing tasks improve automatically
- that one packet shape is globally optimal
