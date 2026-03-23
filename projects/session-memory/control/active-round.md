# Active Round

- Round id: `round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Add executor_plan_contracts to adjudication durable records so higher-level bounded rewrite intent lives in durable truth instead of prompt text.
- Implement compile-adjudication-executor-plan and teach execute-adjudication-followups to compile supported plan contracts before running explicit followups.
- Validate that adjudication smoke and full phase-1 smoke pass when the fixture uses plan contracts instead of hand-authored low-level rewrite payloads.

## Deliverable

A bounded adjudication plan compiler that expands supported durable plan contracts into explicit executor followups and is validated on targeted adjudication smoke plus full phase-1 smoke.

## Validation Plan

Run adjudication followup smoke on plan-contract input, rerun full phase-1 smoke, then rerun audit-control-state and enforce-worktree on the real project.

## Active Risks

- The compiler could quietly overwrite explicit executor payloads instead of merging and deduplicating them.
- Plan-contract support could grow into another hidden orchestration layer unless supported shapes stay explicit and bounded.

## Blockers

_none recorded_
