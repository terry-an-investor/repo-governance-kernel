# Active Objective

- Objective id: `obj-2026-03-23-0002`
- Phase: `execution`
- Status: `active`

## Problem

Fresh coding sessions, side reviewers, and architecture helpers do not fail
mainly because they lack raw history. They fail because they do not know the
active objective line, temporary compromises, and current control boundaries of
the project.

## Success Criteria

- The system preserves project direction across sessions and interruptions.
- A fresh session can recover active objective, pivot lineage, and current
  workaround debt quickly.
- Retrieval and assembly prefer the active control line over raw recency.
- The schema stays project-agnostic while remaining useful for real software
  work.

## Non-Goals

- Generic personal memory product.
- Embedding-first memory stack in phase 1.
- Prompt-only reviewer personas without project-aware control state.

## Why Now

The project has already proven a file-first memory path. The next bottleneck is
control: preventing drift, dirty workaround accumulation, and stale objectives
from steering future sessions.

## Current Risks

- The control model may remain doc-only unless scripts consume it soon.
- Objective and pivot objects could become verbose notes instead of operational
  inputs.
- Real project samples are still limited, so some control semantics may need
  correction once more projects are onboarded.
