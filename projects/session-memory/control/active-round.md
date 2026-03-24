# Active Round

- Round id: `round-2026-03-24-0817-thin-command-callers-so-registry-owns-static-transition-semantics`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Remove duplicated registry-owned guard/write/owner declarations from command caller sites.
- Keep shared owner-layer assertions authoritative while making callers express only runtime-specific inputs and context.

## Deliverable

Command callers no longer restate registry-owned static transition semantics; shared owner-layer helpers derive those declarations from the machine-readable registry.

## Validation Plan

Compile changed scripts, run targeted smoke coverage for objective/phase/round/exception domains, run real-project audit and enforce, then close the round and return the objective to paused.

## Active Risks

_none recorded_

## Blockers

_none recorded_
