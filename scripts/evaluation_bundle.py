#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


DEFAULT_EXCLUDED_NAMES = {
    ".cache",
    "artifacts",
    "git_repos",
    "node_modules",
    "venv",
    ".venv",
}
DEFAULT_EXCLUDED_FILE_NAMES: set[str] = set()
DEFAULT_EXCLUDED_PREFIXES = (
    "tmpclaude-",
)
SEARCH_MARKERS = ("rg ", "ripgrep", "grep ", "findstr", "select-string")
FILE_READ_MARKERS = ("get-content", "cat ", "type ", "sed ", "more ", "less ", "head ", "tail ")


@dataclass
class ExecMetrics:
    command_count: int
    search_count: int
    file_read_count: int
    last_message: str


@dataclass
class ExecResult:
    command: list[str]
    duration_seconds: float
    exit_code: int
    stderr_text: str
    metrics: ExecMetrics


def make_run_id(prefix: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    return f"{timestamp}-{prefix}"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: object) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def classify_evaluation_scope(system_root: Path, source_repo: Path) -> dict[str, object]:
    system_root = system_root.resolve()
    source_repo = source_repo.resolve()
    target_kind = "self-project" if source_repo == system_root else "external-project"
    certification_scope = "bootstrap-only" if target_kind == "self-project" else "external-target"
    if target_kind == "self-project":
        warning = (
            "This run is suitable for dogfooding and bootstrap only. "
            "Do not treat it as serious external evidence of product benefit."
        )
    else:
        warning = (
            "This run targets an external project, so it is eligible to count as "
            "serious evaluation evidence if the frozen bundle and scoring rules stay fixed."
        )
    return {
        "system_root": str(system_root),
        "source_repo": str(source_repo),
        "target_kind": target_kind,
        "agent_separation": "fresh-headless-instance",
        "certification_scope": certification_scope,
        "warning": warning,
    }


def classify_host_adoption_blockers(project_id: str, blocked_paths: list[str]) -> dict[str, object]:
    normalized_paths: list[str] = []
    for path in blocked_paths:
        rendered = str(path).replace("\\", "/").strip()
        if not rendered:
            continue
        while rendered.startswith("./"):
            rendered = rendered[2:]
        normalized_paths.append(rendered)
    bootstrap_control_prefix = f"projects/{project_id}/"

    bucket_order = (
        "hook_installation_paths",
        "host_governance_paths",
        "host_support_paths",
        "repo_scope_paths",
    )
    buckets: dict[str, list[str]] = {key: [] for key in bucket_order}

    for path in normalized_paths:
        if path in {".githooks/pre-commit", ".githooks/pre-push", "githooks/pre-commit", "githooks/pre-push"}:
            buckets["hook_installation_paths"].append(path)
            continue
        if path.startswith(bootstrap_control_prefix):
            buckets["host_governance_paths"].append(path)
            continue
        if (
            path.startswith(".claude/")
            or path.startswith("claude/")
            or path.startswith("cross-project/")
            or path.startswith("index/")
        ):
            buckets["host_support_paths"].append(path)
            continue
        buckets["repo_scope_paths"].append(path)

    meanings = {
        "hook_installation_paths": "repo-local hook installation side effects created by kernel bootstrap or hook refresh",
        "host_governance_paths": "host-governance projected or support files created under the adopted project namespace",
        "host_support_paths": "host-side support surfaces not yet covered by the adopted round/task boundary",
        "repo_scope_paths": "real source-repo dirty paths that remain outside the adopted round/task boundary",
    }

    return {
        "counts": {key: len(value) for key, value in buckets.items()},
        "buckets": buckets,
        "meanings": meanings,
        "has_repo_scope_gap": bool(buckets["repo_scope_paths"]),
    }


def source_git_output(source_repo: Path, *args: str) -> str:
    completed = run_subprocess(["git", "-C", str(source_repo), *args], cwd=source_repo.parent)
    if completed.returncode != 0:
        raise RuntimeError(f"git command failed on source repo: {' '.join(args)}\n{completed.stderr}")
    return completed.stdout.strip()


def should_exclude_top_level_path(source_repo: Path, relative_path: str) -> bool:
    output = source_git_output(source_repo, "ls-files", "--", relative_path)
    return output.strip() == ""


def resolve_snapshot_exclusions(
    source_repo: Path,
    *,
    optional_excluded_names: set[str] | None = None,
    optional_excluded_files: set[str] | None = None,
) -> tuple[set[str], set[str]]:
    excluded_names = set()
    excluded_files = set()
    for name in optional_excluded_names or set():
        if should_exclude_top_level_path(source_repo, name):
            excluded_names.add(name)
    for name in optional_excluded_files or set():
        if should_exclude_top_level_path(source_repo, name):
            excluded_files.add(name)
    return excluded_names, excluded_files


def copy_repo_snapshot(
    source_repo: Path,
    snapshot_dir: Path,
    *,
    excluded_names: set[str] | None = None,
    excluded_file_names: set[str] | None = None,
    excluded_prefixes: tuple[str, ...] | None = None,
) -> dict[str, object]:
    excluded_names = set(DEFAULT_EXCLUDED_NAMES) | set(excluded_names or set())
    excluded_file_names = set(DEFAULT_EXCLUDED_FILE_NAMES) | set(excluded_file_names or set())
    excluded_prefixes = DEFAULT_EXCLUDED_PREFIXES if excluded_prefixes is None else excluded_prefixes

    def ignore(_directory: str, names: list[str]) -> set[str]:
        skipped: set[str] = set()
        for name in names:
            if name in excluded_names or name in excluded_file_names:
                skipped.add(name)
                continue
            if any(name.startswith(prefix) for prefix in excluded_prefixes):
                skipped.add(name)
        return skipped

    shutil.copytree(source_repo, snapshot_dir, ignore=ignore)
    return {
        "excluded_names": sorted(excluded_names),
        "excluded_file_names": sorted(excluded_file_names),
        "excluded_prefixes": list(excluded_prefixes),
    }


def normalize_repo_text(text: str, source_repo: Path) -> str:
    root_posix = source_repo.resolve().as_posix()
    root_win = str(source_repo.resolve())
    normalized = text.replace(f"{root_posix}/", "")
    normalized = normalized.replace(f"{root_win}\\", "")
    normalized = normalized.replace(root_posix, ".")
    normalized = normalized.replace(root_win, ".")
    return normalized


def run_subprocess(command: list[str], *, cwd: Path, input_text: str | None = None, timeout_seconds: int | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd),
        input=input_text,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )


def run_codex_exec(
    *,
    prompt_text: str,
    snapshot_dir: Path,
    jsonl_path: Path,
    last_message_path: Path,
    model: str | None,
    sandbox: str,
    timeout_seconds: int,
) -> ExecResult:
    codex_executable = shutil.which("codex") or shutil.which("codex.cmd") or "codex"
    command = [
        codex_executable,
        "exec",
        "--ephemeral",
        "--json",
        "--color",
        "never",
        "-s",
        sandbox,
        "-C",
        str(snapshot_dir),
        "-o",
        str(last_message_path),
    ]
    if model:
        command.extend(["-m", model])
    command.append("-")

    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    with jsonl_path.open("w", encoding="utf-8") as stdout_handle:
        completed = subprocess.run(
            command,
            cwd=str(snapshot_dir),
            input=prompt_text,
            text=True,
            stdout=stdout_handle,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            check=False,
        )
    duration_seconds = time.perf_counter() - started
    metrics = summarize_exec_jsonl(jsonl_path, last_message_path)
    return ExecResult(
        command=command,
        duration_seconds=duration_seconds,
        exit_code=completed.returncode,
        stderr_text=completed.stderr,
        metrics=metrics,
    )


def summarize_exec_jsonl(jsonl_path: Path, last_message_path: Path) -> ExecMetrics:
    command_count = 0
    search_count = 0
    file_read_count = 0
    last_message = ""

    if jsonl_path.exists():
        for raw_line in jsonl_path.read_text(encoding="utf-8").splitlines():
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                event = json.loads(raw_line)
            except json.JSONDecodeError:
                continue
            if event.get("type") != "item.completed":
                continue
            item = event.get("item", {})
            item_type = item.get("type")
            if item_type == "command_execution":
                command_count += 1
                command_text = str(item.get("command", "")).lower()
                if any(marker in command_text for marker in SEARCH_MARKERS):
                    search_count += 1
                if any(marker in command_text for marker in FILE_READ_MARKERS):
                    file_read_count += 1
            if item_type == "agent_message":
                last_message = str(item.get("text", "")).strip()

    if not last_message and last_message_path.exists():
        last_message = last_message_path.read_text(encoding="utf-8").strip()

    return ExecMetrics(
        command_count=command_count,
        search_count=search_count,
        file_read_count=file_read_count,
        last_message=last_message,
    )
