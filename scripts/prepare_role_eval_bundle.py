#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from compile_role_context import (
    ROLE_CHOICES,
    compile_architect_context,
    compile_orchestrator_context,
    compile_reviewer_context,
)
from evaluation_bundle import (
    classify_evaluation_scope,
    copy_repo_snapshot,
    make_run_id,
    resolve_snapshot_exclusions,
    write_json,
    write_text,
)


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ARTIFACT_ROOT = ROOT / "artifacts" / "evaluation" / "roles"
OPTIONAL_EXCLUDE_NAMES = {
    ".cache",
    "node_modules",
    "outputs",
}
OPTIONAL_EXCLUDE_FILES = {
    ".env",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare a frozen role-context evaluation bundle.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--role", required=True, choices=ROLE_CHOICES)
    parser.add_argument("--source-repo")
    parser.add_argument("--artifact-root", default=str(DEFAULT_ARTIFACT_ROOT))
    parser.add_argument("--run-id")
    parser.add_argument("--memory-limit", type=int, default=6)
    return parser.parse_args()


def default_source_repo(project_id: str) -> Path:
    if project_id == "repo-governance-kernel":
        return ROOT
    return (ROOT.parent / project_id).resolve()


def build_role_context(project_dir: Path, project_id: str, role: str, memory_limit: int) -> str:
    if role == "reviewer":
        return compile_reviewer_context(project_dir, project_id, memory_limit)
    if role == "architect":
        return compile_architect_context(project_dir, project_id, memory_limit)
    return compile_orchestrator_context(project_dir, project_id, memory_limit)


def build_task(project_id: str, role: str) -> str:
    if role == "reviewer":
        return f"""# Role Evaluation Task

Project id: `{project_id}`
Role: `reviewer`
Type: `orientation-only`

## Goal

Evaluate whether the reviewer context helps a fresh session produce a findings-first
review that respects project rules, active objective, and current execution state.

## Constraints

- Do not modify files.
- Do not write code.
- Do not run destructive commands.
- Review the frozen snapshot only.
- Findings must be concrete and evidence-based.

## Required Output

Produce a concise review with these sections:

1. Findings
2. Evidence
3. Open Questions
4. Residual Risks

The review should prioritize:

- objective drift
- exception-contract leakage
- architecture invariant violations
- missing validation or stale governance claims
"""
    if role == "architect":
        return f"""# Role Evaluation Task

Project id: `{project_id}`
Role: `architect`
Type: `orientation-only`

## Goal

Evaluate whether the architect context helps a fresh session reason about
architecture direction without losing current project constraints.

## Constraints

- Do not modify files.
- Do not write code.
- Do not run destructive commands.
- Use only the frozen snapshot and provided context.

## Required Output

Produce a concise architecture note with these sections:

1. Tension Map
2. Invariants
3. Directional Recommendation
4. Migration Risks
5. Deferred Questions
"""
    return f"""# Role Evaluation Task

Project id: `{project_id}`
Role: `orchestrator`
Type: `orientation-only`

## Goal

Evaluate whether the orchestrator context helps a fresh session produce a
bounded execution contract instead of a vague plan.

## Constraints

- Do not modify files.
- Do not write code.
- Do not run destructive commands.
- Use only the frozen snapshot and provided context.

## Required Output

Produce a concise orchestration note with these sections:

1. Objective Alignment
2. Scope Boundary
3. Ordered Next Steps
4. Validation Gates
5. Deferred Ideas
6. Risks

The plan must avoid silent scope expansion.
"""


def build_score_template(project_id: str, role: str, evaluation_scope: dict[str, object]) -> str:
    common = [
        "# Score Template",
        "",
        f"Project id: `{project_id}`",
        f"Role: `{role}`",
        f"Target kind: `{evaluation_scope['target_kind']}`",
        f"Agent separation: `{evaluation_scope['agent_separation']}`",
        f"Certification scope: `{evaluation_scope['certification_scope']}`",
        "",
        "## Shared Metrics",
        "",
        "- `wrong_inference_count`",
        "- `recovery_cost`",
        "- `evidence_citation_quality`",
        "- `objective_alignment`",
        "",
    ]
    if role == "reviewer":
        role_lines = [
            "## Reviewer Metrics",
            "",
            "- `finding_recall`",
            "- `finding_precision`",
            "- `constraint_adherence`",
            "- `exception_contract_detection`",
            "- `validation_gap_detection`",
            "",
            "## Scoring Questions",
            "",
            "- Did the review identify the most important real findings first?",
            "- Did it avoid generic or style-only comments that ignore project priorities?",
            "- Did it use the constitution and active objective correctly?",
            "- Did it surface missing validation or stale governance where relevant?",
            "",
        ]
    elif role == "architect":
        role_lines = [
            "## Architect Metrics",
            "",
            "- `invariant_alignment`",
            "- `tension_identification`",
            "- `recommendation_quality`",
            "- `migration_realism`",
            "- `deferred_question_quality`",
            "",
            "## Scoring Questions",
            "",
            "- Did the note preserve active invariants instead of inventing a clean-slate rewrite?",
            "- Did it identify the actual architectural tension in the snapshot?",
            "- Were recommendations realistic for the current project phase?",
            "",
        ]
    else:
        role_lines = [
            "## Orchestrator Metrics",
            "",
            "- `scope_containment`",
            "- `ordering_quality`",
            "- `validation_gate_quality`",
            "- `deferred_idea_discipline`",
            "- `round_contract_quality`",
            "",
            "## Scoring Questions",
            "",
            "- Did the plan stay aligned with the active objective?",
            "- Did it define a bounded scope instead of a broad rewrite?",
            "- Did it include explicit validation gates?",
            "- Did it defer side ideas instead of absorbing them into the round?",
            "",
        ]
    footer = [
        "## Notes",
        "",
        "- Fill this after freezing the snapshot and before comparing control and treatment outputs.",
        "",
    ]
    return "\n".join(common + role_lines + footer) + "\n"


def build_scoring_notes_stub(project_id: str, role: str) -> str:
    return f"""# Scoring Notes Stub

Project id: `{project_id}`
Role: `{role}`

## Expected Key Facts

- Fill from the frozen snapshot before any scored run.

## Expected Failure Modes

- Fill with the mistakes a weak fresh session is likely to make.

## Evidence Anchors

- List the files or artifacts that justify the scoring call.
"""


def main() -> None:
    args = parse_args()
    project_dir = ROOT / "state" / args.project_id
    if not project_dir.exists():
        raise SystemExit(f"project directory not found: {project_dir}")

    source_repo = Path(args.source_repo).resolve() if args.source_repo else default_source_repo(args.project_id)
    if not source_repo.exists():
        raise SystemExit(f"source repo not found: {source_repo}")

    artifact_root = Path(args.artifact_root).resolve()
    run_id = args.run_id or make_run_id(f"{args.project_id}-{args.role}-role-eval")
    run_dir = artifact_root / args.project_id / run_id
    bundle_dir = run_dir / "bundle"
    snapshot_dir = bundle_dir / "snapshot"
    if run_dir.exists():
        raise SystemExit(f"run directory already exists: {run_dir}")

    run_dir.mkdir(parents=True, exist_ok=False)
    bundle_dir.mkdir(parents=True, exist_ok=False)

    excluded_names, excluded_files = resolve_snapshot_exclusions(
        source_repo,
        optional_excluded_names=OPTIONAL_EXCLUDE_NAMES,
        optional_excluded_files=OPTIONAL_EXCLUDE_FILES,
    )
    snapshot_meta = copy_repo_snapshot(
        source_repo,
        snapshot_dir,
        excluded_names=excluded_names,
        excluded_file_names=excluded_files,
    )
    evaluation_scope = classify_evaluation_scope(ROOT, source_repo)
    role_context = build_role_context(project_dir, args.project_id, args.role, args.memory_limit)
    task_text = build_task(args.project_id, args.role)
    score_template = build_score_template(args.project_id, args.role, evaluation_scope)
    scoring_notes = build_scoring_notes_stub(args.project_id, args.role)

    write_text(bundle_dir / "role-context.md", role_context)
    write_text(bundle_dir / "task.md", task_text)
    write_text(bundle_dir / "score-template.md", score_template)
    write_text(bundle_dir / "scoring-notes.stub.md", scoring_notes)

    run_config = {
        "project_id": args.project_id,
        "role": args.role,
        "run_id": run_id,
        "source_repo": str(source_repo),
        "snapshot_dir": str(snapshot_dir),
        "memory_limit": args.memory_limit,
        "evaluation_scope": evaluation_scope,
        "snapshot_meta": snapshot_meta,
    }
    write_json(bundle_dir / "run-config.json", run_config)

    print(f"prepared role-eval bundle: {run_dir}")


if __name__ == "__main__":
    main()
