#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass

from kernel.public_flow_contracts import describe_public_flow_contract_catalog


PUBLIC_SURFACE_RELEASED_VERSION = "0.1.0b0"
PUBLIC_SURFACE_SOURCE_LINE_TARGET_VERSION = "0.1.0b1"
PUBLIC_SURFACE_FROZEN_SINCE_VERSION = "0.1.0b0"


@dataclass(frozen=True)
class PublicSurfaceEntry:
    name: str
    kind: str
    stability: str
    summary: str


def _public_commands() -> tuple[PublicSurfaceEntry, ...]:
    return (
        PublicSurfaceEntry(
            name="describe-config",
            kind="command",
            stability="public-beta",
            summary="Explain resolved repo_root and project_id config sources.",
        ),
        PublicSurfaceEntry(
            name="describe-public-surface",
            kind="command",
            stability="public-beta",
            summary="Expose the machine-readable public beta package contract.",
        ),
        PublicSurfaceEntry(
            name="audit-control-state",
            kind="command",
            stability="public-beta",
            summary="Audit governed control truth without mutation.",
        ),
        PublicSurfaceEntry(
            name="enforce-worktree",
            kind="command",
            stability="public-beta",
            summary="Check that the live worktree still matches active control truth.",
        ),
        PublicSurfaceEntry(
            name="bootstrap-repo",
            kind="command",
            stability="public-beta",
            summary="Bootstrap the minimum governed host surface in one git repo.",
        ),
        PublicSurfaceEntry(
            name="onboard-repo",
            kind="bundle",
            stability="public-beta",
            summary="Open the first honest control line for a governed host repo.",
        ),
        PublicSurfaceEntry(
            name="onboard-repo-from-intent",
            kind="intent-wrapper",
            stability="public-beta",
            summary="Compile one bounded repo-initialization request into onboard-repo.",
        ),
        PublicSurfaceEntry(
            name="assess-external-target-once",
            kind="bundle",
            stability="public-beta",
            summary="Run one bounded external-target assessment through governed commands.",
        ),
        PublicSurfaceEntry(
            name="assess-external-target-from-intent",
            kind="intent-wrapper",
            stability="public-beta",
            summary="Compile one bounded external-target assessment request into the governed workflow.",
        ),
    )


def _package_internal_commands() -> tuple[PublicSurfaceEntry, ...]:
    return (
        PublicSurfaceEntry(
            name="assess-host-adoption",
            kind="command",
            stability="package-internal",
            summary="Lower-level shadow assessment primitive consumed by higher-level public workflows.",
        ),
        PublicSurfaceEntry(
            name="draft-external-target-shadow-scope",
            kind="command",
            stability="package-internal",
            summary="Lower-level drafting primitive for external-target shadow setup.",
        ),
        PublicSurfaceEntry(
            name="execute-adjudication-followups",
            kind="command",
            stability="package-internal",
            summary="Owner-layer adjudication executor, not part of the frozen public beta promise.",
        ),
    )


def _repo_owned_agent_wrappers() -> tuple[dict[str, object], ...]:
    return (
        {
            "name": "use-repo-governance-kernel",
            "distribution": "source-repository",
            "path": "skills/use-repo-governance-kernel/SKILL.md",
            "summary": "Repo-owned agent wrapper for bounded onboarding and one-time external-target assessment.",
        },
    )


def _host_local_surfaces() -> tuple[str, ...]:
    return (
        "scripts/",
        "state/session-memory/",
        ".githooks/",
        ".github/workflows/",
        "repo-local smoke and evaluation harnesses",
    )


def describe_public_surface() -> dict[str, object]:
    return {
        "target_version": PUBLIC_SURFACE_RELEASED_VERSION,
        "released_version": PUBLIC_SURFACE_RELEASED_VERSION,
        "source_line_target_version": PUBLIC_SURFACE_SOURCE_LINE_TARGET_VERSION,
        "frozen_since_version": PUBLIC_SURFACE_FROZEN_SINCE_VERSION,
        "status": "public-beta-b0",
        "public_commands": [asdict(entry) for entry in _public_commands()],
        "package_internal_commands": [asdict(entry) for entry in _package_internal_commands()],
        "repo_owned_agent_wrappers": list(_repo_owned_agent_wrappers()),
        "host_local_surfaces": list(_host_local_surfaces()),
        "stable_public_flow_results": describe_public_flow_contract_catalog(),
        "contract_notes": [
            "public commands are the intended direct beta entrypoints for users and agent callers in the 0.1.0b0 line",
            "the current public beta release version is 0.1.0b0 and the frozen surface now includes package-facing inspection commands as well as the bounded workflow commands",
            "the current b0 stable public flow contract exports both top-level result fields and the minimum stable nested subcontracts for flow_contract and intent_compilation",
            "the same descriptor now also records the source-line b1 next-stable subcontract set for execution and postconditions without pretending that b1 is already released",
            "the remaining b1-target candidate subcontracts keep the deeper evidence projections explicit so agents and smokes can stop inferring them from payload examples",
            "package-internal commands remain implemented owner-layer surfaces but are not the frozen public beta compatibility promise",
            "repo-owned agent wrappers package the same bounded surfaces without widening authority",
            "host-local surfaces remain evidence or adapter layers rather than package contract",
        ],
    }
