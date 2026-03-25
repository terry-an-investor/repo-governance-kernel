# Active Round

- Round id: `round-2026-03-25-0946-make-package-first-repo-onboarding-real`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Create one package-facing onboarding primitive so a fresh host repo can move from bare bootstrap into an honest first governance setup without hand-opening every control object.
- Keep the onboarding path bounded and registry-owned instead of adding a freeform setup orchestrator.
- Define the next release sequence so the package surface, config layering, and one-task entrypoints are planned as explicit alpha milestones instead of informal chat guidance.
- Land the first repo-owned agent packaging surface so onboarding and single assessment can be invoked through a bounded skill rather than only through raw CLI knowledge.

## Deliverable

One canonical version roadmap plus the first repo-owned agent skill showing how to initialize and evaluate repos through the bounded package surface.

## Validation Plan

Run audit_product_docs, audit-control-state, enforce-worktree, and one focused skill-oriented proof or command example after the roadmap and first agent packaging surface land.

## Active Risks

- If onboarding still depends on smoke-only setup helpers, the package-first story will remain repo-local rather than product-facing.
- If onboarding invents placeholder control objects on a clean repo or absorbs bootstrap side effects dishonestly, it will make the first governance state look smoother than it is.
- If agent packaging is left implicit, the product will continue to feel like an internal kernel even after onboarding and assessment surfaces already exist.
- If the roadmap stays only in chat, package-facing priorities will drift and alpha release work will remain reactive instead of versioned.

## Blockers

_none recorded_
