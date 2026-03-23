#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from evaluation_bundle import (
    classify_evaluation_scope,
    copy_repo_snapshot,
    make_run_id,
    normalize_repo_text,
    run_codex_exec,
    run_subprocess,
    write_json,
    write_text,
)


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
DEFAULT_SOURCE_REPO = ROOT.parent / "wind-agent"
DEFAULT_ARTIFACT_ROOT = ROOT / "artifacts" / "evaluation" / "wind-agent"
PROJECT_ID = "wind-agent"
TASK_ID = "orientation-only"
OPTIONAL_EXCLUDE_NAMES = {
    ".cache",
    "node_modules",
    "outputs",
}
OPTIONAL_EXCLUDE_FILES = {
    ".env",
}

SHARED_PROMPT_BODY = """You are evaluating the current engineering state of the wind-agent repository.

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
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the first frozen-bundle wind-agent evaluation.")
    parser.add_argument("--source-repo", default=str(DEFAULT_SOURCE_REPO))
    parser.add_argument("--artifact-root", default=str(DEFAULT_ARTIFACT_ROOT))
    parser.add_argument("--run-id")
    parser.add_argument("--model")
    parser.add_argument("--sandbox", default="read-only", choices=["read-only", "workspace-write", "danger-full-access"])
    parser.add_argument("--memory-limit", type=int, default=12)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--prepare-only", action="store_true")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def git_output(snapshot_dir: Path, *args: str) -> str:
    completed = run_subprocess(["git", "-C", str(snapshot_dir), *args], cwd=ROOT)
    if completed.returncode != 0:
        raise RuntimeError(f"git command failed: {' '.join(args)}\n{completed.stderr}")
    return completed.stdout.strip()


def source_git_output(source_repo: Path, *args: str) -> str:
    completed = run_subprocess(["git", "-C", str(source_repo), *args], cwd=ROOT)
    if completed.returncode != 0:
        raise RuntimeError(f"git command failed on source repo: {' '.join(args)}\n{completed.stderr}")
    return completed.stdout.strip()


def should_exclude_top_level_path(source_repo: Path, relative_path: str) -> bool:
    output = source_git_output(source_repo, "ls-files", "--", relative_path)
    return output.strip() == ""


def resolve_snapshot_exclusions(source_repo: Path) -> tuple[set[str], set[str]]:
    excluded_names = set()
    excluded_files = set()
    for name in OPTIONAL_EXCLUDE_NAMES:
        if should_exclude_top_level_path(source_repo, name):
            excluded_names.add(name)
    for name in OPTIONAL_EXCLUDE_FILES:
        if should_exclude_top_level_path(source_repo, name):
            excluded_files.add(name)
    return excluded_names, excluded_files


def freeze_task(bundle_dir: Path) -> str:
    task_text = f"""# Wind-Agent Evaluation Task

Task id: `{TASK_ID}`
Project id: `{PROJECT_ID}`
Type: orientation-only

## Goal

Measure whether a fresh headless Codex instance recovers the current
`wind-agent` engineering state more accurately and with lower recovery cost when
it starts from a `session-memory` handoff packet.

## Constraints

- Do not modify files.
- Do not write code.
- Do not run destructive commands.
- Use only repository state and artifacts available inside the frozen snapshot.

## Success Condition

Produce one concise repo-specific report with these sections:

1. Active Round
2. Validated Facts
3. Scope Drift
4. Top Risks
5. Recommended Next Steps
6. First Files To Read

## Shared Prompt Body

```text
{SHARED_PROMPT_BODY.rstrip()}
```
"""
    write_text(bundle_dir / "task.md", task_text)
    return task_text


def build_treatment_packet(bundle_dir: Path, source_repo: Path, memory_limit: int) -> str:
    raw_packet_path = bundle_dir / "treatment-packet.raw.md"
    command = [
        sys.executable,
        str(SCRIPTS / "assemble_context.py"),
        "--project-id",
        PROJECT_ID,
        "--memory-limit",
        str(memory_limit),
        "--output",
        str(raw_packet_path),
    ]
    completed = run_subprocess(command, cwd=ROOT)
    if completed.returncode != 0:
        raise RuntimeError(f"failed to assemble treatment packet\n{completed.stderr}")

    raw_text = raw_packet_path.read_text(encoding="utf-8")
    normalized_text = normalize_repo_text(raw_text, source_repo)
    write_text(bundle_dir / "treatment-packet.md", normalized_text)
    return normalized_text


def parse_status_paths(status_text: str) -> list[str]:
    paths: list[str] = []
    for raw_line in status_text.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        payload = line[3:] if len(line) > 3 else line
        if " -> " in payload:
            payload = payload.split(" -> ", 1)[1]
        paths.append(payload.replace("\\", "/"))
    return paths


def build_ground_truth(bundle_dir: Path, snapshot_dir: Path, source_repo: Path) -> dict[str, object]:
    active = load_json(snapshot_dir / ".round" / "active.json")
    validation = load_json(snapshot_dir / ".round" / "last_live_validation.json")
    progress = load_json(snapshot_dir / ".round" / "progress.json")

    head = git_output(snapshot_dir, "rev-parse", "HEAD")
    status_text = git_output(snapshot_dir, "status", "--short", "--untracked-files=all")
    shortstat = git_output(snapshot_dir, "diff", "--shortstat")
    modified_paths = parse_status_paths(status_text)

    allowed_paths = [str(value) for value in active.get("allowed_paths", [])]
    drift_paths = [
        path
        for path in modified_paths
        if not any(path.startswith(allowed_path) for allowed_path in allowed_paths)
    ]
    progress_status = str(((progress.get("latest") or {}).get("status")) or "")

    expected_first_files = [
        ".round/active.json",
        ".round/last_live_validation.json",
        ".round/progress.json",
        "docs/ARCHITECTURE.md",
    ]
    preferred_drift_prefixes = ("native/", "src/native/", "src/cli/", "package.json", "src/wind/")
    preferred_drift_paths = [
        path
        for path in drift_paths
        if path.startswith(preferred_drift_prefixes) or path == "package.json"
    ]
    for candidate in preferred_drift_paths + drift_paths:
        if candidate not in expected_first_files:
            expected_first_files.append(candidate)
        if len(expected_first_files) >= 5:
            break

    top_risks: list[str] = []
    if drift_paths:
        top_risks.append("round contract drift")
        top_risks.append("validation coverage drift")
    if progress_status == "initialized":
        top_risks.append("governance drift")
    if not top_risks:
        top_risks.append("current snapshot appears aligned with the declared round")

    recommended_next_steps: list[str] = []
    if drift_paths:
        recommended_next_steps.append("reconcile or split the round so the contract matches the real worktree")
        recommended_next_steps.append("validate the broadened seams in small slices instead of extrapolating from one live pass")
    else:
        recommended_next_steps.append("confirm the current clean snapshot still matches the intended round boundary")
    if progress_status == "initialized":
        recommended_next_steps.append("refresh round progress and other governance artifacts after scope is honest")
    else:
        recommended_next_steps.append("keep round governance artifacts aligned with the actual validation state")

    evaluation_scope = classify_evaluation_scope(ROOT, source_repo)
    ground_truth = {
        "task_id": TASK_ID,
        "project_id": PROJECT_ID,
        "head": head,
        "round_id": active.get("round_id"),
        "validation_status": validation.get("status"),
        "validation_claim": validation.get("claim"),
        "validation_command": validation.get("command"),
        "allowed_paths": allowed_paths,
        "modified_paths": modified_paths,
        "drift_paths": drift_paths,
        "progress_status": progress_status,
        "diff_shortstat": shortstat or "clean worktree",
        "expected_first_files": expected_first_files[:5],
        "top_risks": top_risks,
        "recommended_next_steps": recommended_next_steps,
        "evaluation_scope": evaluation_scope,
    }

    ground_truth_text = render_ground_truth(ground_truth)
    write_text(bundle_dir / "ground-truth.md", ground_truth_text)
    return ground_truth


def render_ground_truth(ground_truth: dict[str, object]) -> str:
    drift_paths = ground_truth["drift_paths"]
    modified_paths = ground_truth["modified_paths"]
    expected_first_files = ground_truth["expected_first_files"]
    top_risks = ground_truth["top_risks"]
    recommended_next_steps = ground_truth["recommended_next_steps"]
    lines = [
        "# Ground Truth",
        "",
        f"Task id: `{ground_truth['task_id']}`",
        f"Project id: `{ground_truth['project_id']}`",
        f"HEAD: `{ground_truth['head']}`",
        "",
        "## Evaluation Scope",
        "",
        f"- Target kind: `{ground_truth['evaluation_scope']['target_kind']}`",
        f"- Agent separation: `{ground_truth['evaluation_scope']['agent_separation']}`",
        f"- Certification scope: `{ground_truth['evaluation_scope']['certification_scope']}`",
        f"- Warning: {ground_truth['evaluation_scope']['warning']}",
        "",
        "## Required Facts",
        "",
        f"- Active round id: `{ground_truth['round_id']}`",
        f"- Validation status: `{ground_truth['validation_status']}`",
        f"- Validation command: `{ground_truth['validation_command']}`",
        f"- Diff shortstat: `{ground_truth['diff_shortstat']}`",
        f"- Progress status: `{ground_truth['progress_status']}`",
        "",
        "## Allowed Paths",
        "",
    ]
    for path in ground_truth["allowed_paths"]:
        lines.append(f"- `{path}`")
    lines.extend(["", "## Modified Paths", ""])
    if modified_paths:
        for path in modified_paths:
            lines.append(f"- `{path}`")
    else:
        lines.append("- _none_")
    lines.extend(["", "## Scope Drift Paths", ""])
    if drift_paths:
        for path in drift_paths:
            lines.append(f"- `{path}`")
    else:
        lines.append("- _none_")
    lines.extend(["", "## Expected Risks", ""])
    for risk in top_risks:
        lines.append(f"- {risk}")
    lines.extend(["", "## Expected Next Steps", ""])
    for step in recommended_next_steps:
        lines.append(f"- {step}")
    lines.extend(["", "## Useful First Files", ""])
    for path in expected_first_files:
        lines.append(f"- `{path}`")
    lines.append("")
    return "\n".join(lines)


def build_control_prompt(task_text: str) -> str:
    return f"{SHARED_PROMPT_BODY.rstrip()}\n"


def build_treatment_prompt(packet_text: str) -> str:
    return (
        "Read this handoff packet first and use it as your initial orientation context:\n\n"
        f"{packet_text.rstrip()}\n\n"
        f"{SHARED_PROMPT_BODY.rstrip()}\n"
    )


def score_required_checks(last_message: str, ground_truth: dict[str, object]) -> dict[str, bool]:
    lower = last_message.lower()
    first_file_hits = sum(1 for path in ground_truth["expected_first_files"] if str(path).lower() in lower)
    drift_hits = sum(1 for path in ground_truth["drift_paths"] if str(path).lower() in lower)
    drift_paths = list(ground_truth["drift_paths"])
    if drift_paths:
        next_steps_check = (
            any(token in lower for token in ("split the round", "amend the round", "reconcile", "scope"))
            and any(token in lower for token in ("validate", "test", "progress", "governance"))
        )
    else:
        next_steps_check = any(token in lower for token in ("confirm", "refresh", "progress", "governance", "archive"))
    if drift_paths:
        scope_drift_check = drift_hits > 0 or ("drift" in lower and "scope" in lower) or ("exceed" in lower and "round" in lower)
    else:
        scope_drift_check = any(
            token in lower
            for token in (
                "clean worktree",
                "worktree is clean",
                "no scope drift",
                "within the declared scope",
                "artifacts are internally inconsistent",
                "governance progress was not refreshed",
                "handoff packet does not match",
            )
        )
    risk_marker_groups = []
    for risk in ground_truth["top_risks"]:
        markers = {str(risk).lower()}
        if risk == "governance drift":
            markers.update(
                {
                    "governance state is unreliable",
                    "artifacts are internally inconsistent",
                    "progress was not refreshed",
                    "old preflight/gate reports",
                }
            )
        if risk == "round contract drift":
            markers.update(
                {
                    "scope drift",
                    "outside the declared scope",
                    "handoff packet does not match",
                }
            )
        if risk == "validation coverage drift":
            markers.update(
                {
                    "validation coverage",
                    "stale validation coverage",
                    "live pass is only partially auditable",
                }
            )
        risk_marker_groups.append(markers)
    return {
        "correct_round_id": str(ground_truth["round_id"]).lower() in lower,
        "prepared_context_validation": (
            "prepared" in lower
            and "query_surface" in lower
            and any(token in lower for token in ("reuse", "reused", "reusable", "consumer path"))
        ),
        "scope_drift": scope_drift_check,
        "risk_recognition": any(any(marker in lower for marker in markers) for markers in risk_marker_groups),
        "next_steps": next_steps_check,
        "first_files": first_file_hits >= 3,
    }


def count_wrong_inferences(last_message: str, ground_truth: dict[str, object]) -> int:
    lower = last_message.lower()
    wrong = 0
    has_drift = bool(ground_truth["drift_paths"])
    clean_claim = any(token in lower for token in ("clean worktree", "worktree is clean", "no scope drift", "within the declared scope"))
    if has_drift and clean_claim:
        wrong += 1
    if not has_drift and any(token in lower for token in ("scope drift", "outside the declared scope", "exceeds the declared round scope")):
        wrong += 1
    if any(token in lower for token in ("no validation", "not validated", "validation has not run")):
        wrong += 1
    if ground_truth["progress_status"] == "initialized" and "progress" in lower and "initialized" not in lower and "stale" not in lower and "drift" not in lower:
        wrong += 1
    round_candidates = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+){2,}", lower)
    if round_candidates and str(ground_truth["round_id"]).lower() not in lower:
        wrong += 1
    return wrong


def render_score_markdown(run_id: str, ground_truth: dict[str, object], results: dict[str, dict[str, object]]) -> str:
    evaluation_scope = ground_truth["evaluation_scope"]
    lines = [
        "# Score",
        "",
        f"Run id: `{run_id}`",
        f"Task id: `{ground_truth['task_id']}`",
        f"Project id: `{ground_truth['project_id']}`",
        f"Snapshot HEAD: `{ground_truth['head']}`",
        "",
        "## Evaluation Scope",
        "",
        f"- Target kind: `{evaluation_scope['target_kind']}`",
        f"- Agent separation: `{evaluation_scope['agent_separation']}`",
        f"- Certification scope: `{evaluation_scope['certification_scope']}`",
        f"- Warning: {evaluation_scope['warning']}",
        "",
    ]
    for arm_name in ("control", "treatment"):
        result = results[arm_name]
        checks = result["checks"]
        lines.extend(
            [
                f"## {arm_name.title()}",
                "",
                f"- Exit code: `{result['exit_code']}`",
                f"- Time to orientation: `{result['time_to_orientation']:.2f}s`",
                f"- State recall accuracy: `{result['state_recall_accuracy']}/{len(checks)}`",
                f"- Omission count: `{result['omission_count']}`",
                f"- Wrong inference count: `{result['wrong_inference_count']}`",
                "- Recovery cost:",
                f"  - commands: `{result['command_count']}`",
                f"  - searches: `{result['search_count']}`",
                f"  - file reads: `{result['file_read_count']}`",
                f"- Result: `{result['result']}`",
                "",
                "### Check Breakdown",
                "",
            ]
        )
        for name, passed in checks.items():
            status = "pass" if passed else "miss"
            lines.append(f"- `{name}`: `{status}`")
        lines.extend(
            [
                "",
                "### Last Message",
                "",
                result["last_message"].rstrip() or "_empty_",
                "",
            ]
        )
        if result["stderr_text"]:
            lines.extend(
                [
                    "### Stderr",
                    "",
                    "```text",
                    result["stderr_text"].rstrip(),
                    "```",
                    "",
                ]
            )

    lines.extend(
        [
            "## Decision",
            "",
            render_decision(ground_truth, results),
            "",
        ]
    )
    return "\n".join(lines)


def render_decision(ground_truth: dict[str, object], results: dict[str, dict[str, object]]) -> str:
    control = results["control"]
    treatment = results["treatment"]
    certification_scope = str(ground_truth["evaluation_scope"]["certification_scope"])
    treatment_better = (
        treatment["state_recall_accuracy"] >= control["state_recall_accuracy"]
        and treatment["wrong_inference_count"] <= control["wrong_inference_count"]
        and treatment["time_to_orientation"] <= control["time_to_orientation"]
    )
    if treatment_better:
        if certification_scope == "bootstrap-only":
            return "Treatment is a bootstrap-only win on this run. It can guide product iteration, but it does not count as serious external validation."
        return "Treatment is a provisional external-target win on this run because it preserved or improved recall while not increasing wrong inference count."
    return "Treatment is not yet a clear win on this run. Inspect the packet, prompt, scoring notes, and evaluation-scope classification before claiming benefit."


def summarize_arm(exec_result, ground_truth: dict[str, object]) -> dict[str, object]:
    checks = score_required_checks(exec_result.metrics.last_message, ground_truth)
    state_recall_accuracy = sum(1 for passed in checks.values() if passed)
    omission_count = len(checks) - state_recall_accuracy
    wrong_inference_count = count_wrong_inferences(exec_result.metrics.last_message, ground_truth)
    result_label = "success"
    if exec_result.exit_code != 0:
        result_label = "fail"
    elif omission_count > 2 or wrong_inference_count > 1:
        result_label = "partial"
    return {
        "exit_code": exec_result.exit_code,
        "time_to_orientation": exec_result.duration_seconds,
        "state_recall_accuracy": state_recall_accuracy,
        "omission_count": omission_count,
        "wrong_inference_count": wrong_inference_count,
        "command_count": exec_result.metrics.command_count,
        "search_count": exec_result.metrics.search_count,
        "file_read_count": exec_result.metrics.file_read_count,
        "last_message": exec_result.metrics.last_message,
        "stderr_text": exec_result.stderr_text,
        "checks": checks,
        "result": result_label,
    }


def main() -> int:
    args = parse_args()
    source_repo = Path(args.source_repo).resolve()
    artifact_root = Path(args.artifact_root).resolve()
    run_id = args.run_id or make_run_id("wind-agent-eval")

    run_dir = artifact_root / run_id
    bundle_dir = run_dir / "bundle"
    snapshot_dir = bundle_dir / "snapshot"
    if run_dir.exists():
        raise SystemExit(f"run directory already exists: {run_dir}")

    run_dir.mkdir(parents=True, exist_ok=False)
    bundle_dir.mkdir(parents=True, exist_ok=False)

    excluded_names, excluded_files = resolve_snapshot_exclusions(source_repo)
    snapshot_meta = copy_repo_snapshot(
        source_repo,
        snapshot_dir,
        excluded_names=excluded_names,
        excluded_file_names=excluded_files,
    )
    task_text = freeze_task(bundle_dir)
    packet_text = build_treatment_packet(bundle_dir, source_repo, args.memory_limit)
    ground_truth = build_ground_truth(bundle_dir, snapshot_dir, source_repo)

    run_config = {
        "run_id": run_id,
        "project_id": PROJECT_ID,
        "task_id": TASK_ID,
        "source_repo": str(source_repo),
        "evaluation_scope": classify_evaluation_scope(ROOT, source_repo),
        "snapshot_dir": str(snapshot_dir),
        "sandbox": args.sandbox,
        "model": args.model,
        "memory_limit": args.memory_limit,
        "timeout_seconds": args.timeout_seconds,
        "snapshot_meta": snapshot_meta,
    }
    write_json(bundle_dir / "run-config.json", run_config)

    control_prompt = build_control_prompt(task_text)
    treatment_prompt = build_treatment_prompt(packet_text)
    write_text(run_dir / "control.prompt.txt", control_prompt)
    write_text(run_dir / "treatment.prompt.txt", treatment_prompt)

    if args.prepare_only:
        print(f"prepared bundle: {run_dir}")
        return 0

    control_result = run_codex_exec(
        prompt_text=control_prompt,
        snapshot_dir=snapshot_dir,
        jsonl_path=run_dir / "control.jsonl",
        last_message_path=run_dir / "control.last.txt",
        model=args.model,
        sandbox=args.sandbox,
        timeout_seconds=args.timeout_seconds,
    )
    write_text(run_dir / "control.stderr.txt", control_result.stderr_text)

    treatment_result = run_codex_exec(
        prompt_text=treatment_prompt,
        snapshot_dir=snapshot_dir,
        jsonl_path=run_dir / "treatment.jsonl",
        last_message_path=run_dir / "treatment.last.txt",
        model=args.model,
        sandbox=args.sandbox,
        timeout_seconds=args.timeout_seconds,
    )
    write_text(run_dir / "treatment.stderr.txt", treatment_result.stderr_text)

    results = {
        "control": summarize_arm(control_result, ground_truth),
        "treatment": summarize_arm(treatment_result, ground_truth),
    }
    score_text = render_score_markdown(run_id, ground_truth, results)
    write_text(run_dir / "score.md", score_text)

    print(f"completed run: {run_dir}")
    print(f"control recall: {results['control']['state_recall_accuracy']}/6")
    print(f"treatment recall: {results['treatment']['state_recall_accuracy']}/6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
