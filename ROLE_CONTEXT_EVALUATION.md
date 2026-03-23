# Role Context Evaluation

Date: 2026-03-23
Scope: Reviewer, architect, and orchestrator compiled-context evaluation

## Goal

Evaluate whether role-specific compiled contexts improve project-aware judgment,
not only generic orientation.

The question is not:

- can the agent summarize the repo at all

The real question is:

- does the compiled role context make the agent behave more like a project-aware
  reviewer, architect, or orchestrator

## Why A Separate Evaluation Track

Generic handoff packets answer:

- where the project is
- what changed
- what the next session should know first

Role contexts answer a different question:

- can the agent apply project control state correctly in a specialized task

That requires a different rubric.

## Bundle Shape

Each role evaluation should freeze one bundle:

```text
artifacts/evaluation/roles/<project_id>/<run-id>/
└── bundle/
    ├── snapshot/
    ├── role-context.md
    ├── task.md
    ├── score-template.md
    ├── scoring-notes.stub.md
    └── run-config.json
```

The bundle should be generated before either arm is run.

Current preparation command:

```bash
uv run python scripts/session_memory.py prepare-role-eval --project-id <project_id> --role <reviewer|architect|orchestrator>
```

## Control And Treatment

The fair comparison is:

- control:
  - fresh session reads the frozen repo snapshot and task only
- treatment:
  - fresh session reads the same frozen repo snapshot, task, and compiled
    `role-context.md`

Do not let treatment also receive the generic handoff packet unless that is a
separate explicitly tested condition.

## Reviewer Rubric

Reviewer context should be scored on:

- `finding_recall`
  - did it identify the most important real findings
- `finding_precision`
  - did it avoid generic or irrelevant comments
- `constraint_adherence`
  - did it review against constitution and active objective
- `workaround_detection`
  - did it notice temporary compromises or debt leakage
- `validation_gap_detection`
  - did it identify missing evidence or stale governance claims

Reviewer failure modes to watch:

- style-only review
- findings that ignore active objective
- hallucinated standards that are not project law
- missing the real project risk while nitpicking local trivia

## Architect Rubric

Architect context should be scored on:

- `invariant_alignment`
  - did it preserve active project constraints
- `tension_identification`
  - did it identify the real architectural pressure
- `recommendation_quality`
  - did it recommend a coherent direction
- `migration_realism`
  - are the proposed moves plausible from the current state
- `deferred_question_quality`
  - did it separate unresolved questions from immediate moves

Architect failure modes to watch:

- clean-slate redesigns that ignore current project state
- recommendations that violate explicit invariants
- generic architecture language without repo-specific leverage

## Orchestrator Rubric

Orchestrator context should be scored on:

- `scope_containment`
  - did it keep the next round bounded
- `ordering_quality`
  - were steps sequenced correctly
- `validation_gate_quality`
  - did it define evidence gates before expansion
- `deferred_idea_discipline`
  - did it keep side ideas out of the active round
- `round_contract_quality`
  - did it turn the state into an honest execution contract

Orchestrator failure modes to watch:

- broad rewrite plans
- no validation gates
- mixing exploration ideas into committed execution
- steps that do not serve the active objective

## Shared Metrics

Across all roles, also record:

- `wrong_inference_count`
- `recovery_cost`
- `evidence_citation_quality`
- `objective_alignment`

These keep the role rubric grounded in correctness.

## Certification Standard

Bootstrap role runs may help shape the product, but only external-target role
runs may count as serious validation evidence.

For the first serious role-context evaluations, use `wind-agent`.
