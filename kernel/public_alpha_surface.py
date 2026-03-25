#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass


PUBLIC_ALPHA_TARGET_VERSION = "0.1.0a3"


@dataclass(frozen=True)
class PublicAlphaEntry:
    name: str
    kind: str
    stability: str
    summary: str


def _public_commands() -> tuple[PublicAlphaEntry, ...]:
    return (
        PublicAlphaEntry(
            name="audit-control-state",
            kind="command",
            stability="public-alpha",
            summary="Audit governed control truth without mutation.",
        ),
        PublicAlphaEntry(
            name="enforce-worktree",
            kind="command",
            stability="public-alpha",
            summary="Check that the live worktree still matches active control truth.",
        ),
        PublicAlphaEntry(
            name="bootstrap-repo",
            kind="command",
            stability="public-alpha",
            summary="Bootstrap the minimum governed host surface in one git repo.",
        ),
        PublicAlphaEntry(
            name="onboard-repo",
            kind="bundle",
            stability="public-alpha",
            summary="Open the first honest control line for a governed host repo.",
        ),
        PublicAlphaEntry(
            name="onboard-repo-from-intent",
            kind="intent-wrapper",
            stability="public-alpha",
            summary="Compile one bounded repo-initialization request into onboard-repo.",
        ),
        PublicAlphaEntry(
            name="assess-external-target-once",
            kind="bundle",
            stability="public-alpha",
            summary="Run one bounded external-target assessment through governed commands.",
        ),
        PublicAlphaEntry(
            name="assess-external-target-from-intent",
            kind="intent-wrapper",
            stability="public-alpha",
            summary="Compile one bounded external-target assessment request into the governed workflow.",
        ),
    )


def _package_internal_commands() -> tuple[PublicAlphaEntry, ...]:
    return (
        PublicAlphaEntry(
            name="assess-host-adoption",
            kind="command",
            stability="package-internal",
            summary="Lower-level shadow assessment primitive consumed by higher-level workflows.",
        ),
        PublicAlphaEntry(
            name="draft-external-target-shadow-scope",
            kind="command",
            stability="package-internal",
            summary="Lower-level drafting primitive for external-target shadow setup.",
        ),
        PublicAlphaEntry(
            name="execute-adjudication-followups",
            kind="command",
            stability="package-internal",
            summary="Owner-layer adjudication executor, not part of the frozen public alpha promise.",
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


def describe_public_alpha_surface() -> dict[str, object]:
    return {
        "target_version": PUBLIC_ALPHA_TARGET_VERSION,
        "status": "frozen-for-a3",
        "public_alpha_commands": [asdict(entry) for entry in _public_commands()],
        "package_internal_commands": [asdict(entry) for entry in _package_internal_commands()],
        "repo_owned_agent_wrappers": list(_repo_owned_agent_wrappers()),
        "host_local_surfaces": list(_host_local_surfaces()),
        "contract_notes": [
            "public-alpha commands are the intended direct entrypoints for users and agent callers",
            "package-internal commands remain implemented owner-layer surfaces but are not the frozen public alpha compatibility promise",
            "repo-owned agent wrappers package the same bounded surfaces without widening authority",
            "host-local surfaces remain evidence or adapter layers rather than package contract",
        ],
    }
