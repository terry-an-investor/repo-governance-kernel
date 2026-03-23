# Active Round

- Round id: `round-2026-03-23-0001`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- freeze the transition command surface
- extend canonical paths for round and transition objects
- pressure-test the design with one real `active-round` sample

## Deliverable

Produce a coherent state-machine command architecture that defines:

- the future command names
- their guards
- their side effects
- the canonical files they own

## Validation Plan

- canonical docs stay mutually consistent
- schema paths match the command-surface design
- the project has one real active-round sample under the new layout

## Active Risks

- Round semantics can drift into fiction if no real round object exists.
- The command surface can overreach if too many transitions are frozen before
  the first implementation slice.

## Blockers

- No enforced transition engine exists yet.
