#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

from assemble_context import (
    clean_section_text,
    extract_current_task_anchor,
    extract_frontmatter_scalars,
    inspect_live_workspace,
    parse_h2_sections,
    parse_keyed_bullets,
    read_text,
)
from build_index import parse_evidence_refs, parse_frontmatter, parse_string_list, split_frontmatter


ROOT = Path(__file__).resolve().parent.parent
OPEN_ROUND_STATUSES = {"draft", "active", "blocked", "validation_pending"}


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def strip_wrapping_quotes(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in {'"', "'"}:
        return stripped[1:-1]
    return stripped


def normalize_scalar_metadata(value: object) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        return str(value).strip()

    normalized = value.strip()
    if not normalized:
        return ""

    for _ in range(3):
        if len(normalized) < 2 or normalized[0] != normalized[-1] or normalized[0] not in {'"', "'"}:
            break
        if normalized[0] == '"':
            try:
                loaded = json.loads(normalized)
            except json.JSONDecodeError:
                normalized = strip_wrapping_quotes(normalized)
                continue
            if isinstance(loaded, str):
                normalized = loaded.strip()
                continue
        normalized = strip_wrapping_quotes(normalized)
        break

    return strip_wrapping_quotes(normalized).strip()


def timestamp_now() -> datetime:
    return datetime.now().astimezone()


def slugify(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    return lowered.strip("-") or "round"


def safe_file_stem(value: str, *, max_length: int = 120) -> str:
    cleaned = value.strip().replace("\\", "-").replace("/", "-")
    if len(cleaned) <= max_length:
        return cleaned
    digest = hashlib.sha1(cleaned.encode("utf-8")).hexdigest()[:10]
    keep = max_length - len(digest) - 1
    return f"{cleaned[:keep].rstrip('-')}-{digest}"


def project_dir(project_id: str) -> Path:
    return ROOT / "projects" / project_id


def active_objective_path(project_id: str) -> Path:
    return project_dir(project_id) / "control" / "active-objective.md"


def active_round_path(project_id: str) -> Path:
    return project_dir(project_id) / "control" / "active-round.md"


def pivot_log_path(project_id: str) -> Path:
    return project_dir(project_id) / "control" / "pivot-log.md"


def exception_ledger_path(project_id: str) -> Path:
    return project_dir(project_id) / "control" / "exception-ledger.md"


def rounds_dir(project_id: str) -> Path:
    return project_dir(project_id) / "memory" / "rounds"


def objectives_dir(project_id: str) -> Path:
    return project_dir(project_id) / "memory" / "objectives"


def pivots_dir(project_id: str) -> Path:
    return project_dir(project_id) / "memory" / "pivots"


def exception_contracts_dir(project_id: str) -> Path:
    return project_dir(project_id) / "memory" / "exception-contracts"


def transition_events_dir(project_id: str) -> Path:
    return project_dir(project_id) / "memory" / "transition-events"


def adjudications_dir(project_id: str) -> Path:
    return project_dir(project_id) / "memory" / "adjudications"


def load_current_task_anchor(project_id: str) -> dict[str, str]:
    current_task_path = project_dir(project_id) / "current" / "current-task.md"
    if not current_task_path.exists():
        return {}
    sections = parse_h2_sections(clean_section_text(current_task_path, strip_heading=True, strip_yaml=False))
    return extract_current_task_anchor(sections)


def resolve_anchor(project_id: str) -> dict[str, str]:
    anchor = load_current_task_anchor(project_id)
    live_workspace = inspect_live_workspace(anchor)
    if live_workspace.get("status") == "available":
        anchor["workspace_root"] = live_workspace.get("workspace_root", anchor.get("workspace_root", ""))
        anchor["branch"] = live_workspace.get("branch", anchor.get("branch", ""))
        anchor["git_sha"] = live_workspace.get("git_sha", anchor.get("git_sha", ""))
    return anchor


def load_active_objective(project_id: str) -> tuple[dict[str, str], dict[str, str]]:
    path = active_objective_path(project_id)
    if not path.exists():
        return {}, {}
    cleaned = clean_section_text(path, strip_heading=True, strip_yaml=False)
    lines = []
    for line in cleaned.splitlines():
        if line.startswith("## "):
            break
        lines.append(line)
    preface = parse_keyed_bullets("\n".join(lines))
    sections = parse_h2_sections(cleaned)
    return preface, sections


def load_active_round(project_id: str) -> tuple[dict[str, str], dict[str, str]]:
    path = active_round_path(project_id)
    if not path.exists():
        return {}, {}
    cleaned = clean_section_text(path, strip_heading=True, strip_yaml=False)
    lines = []
    for line in cleaned.splitlines():
        if line.startswith("## "):
            break
        lines.append(line)
    preface = parse_keyed_bullets("\n".join(lines))
    sections = parse_h2_sections(cleaned)
    return preface, sections


def render_bullet_list(items: list[str], *, empty_text: str = "_none recorded_") -> str:
    cleaned = [item.strip() for item in items if item.strip()]
    if not cleaned:
        return empty_text
    rendered_items: list[str] = []
    for item in cleaned:
        lines = [line.strip() for line in item.splitlines() if line.strip()]
        if not lines:
            continue
        rendered_items.append(f"- {lines[0]}")
        for continuation in lines[1:]:
            rendered_items.append(f"  {continuation}")
    return "\n".join(rendered_items)


def parse_bullet_list(text: str) -> list[str]:
    items: list[str] = []
    current_lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped.startswith("- "):
            if current_lines:
                items.append("\n".join(current_lines).strip())
            current_lines = [stripped[2:].strip()]
            continue
        if current_lines and stripped:
            current_lines.append(stripped)
    if current_lines:
        items.append("\n".join(current_lines).strip())
    return items


def normalize_section_text(text: str) -> str:
    value = text.strip()
    return "" if value in {"", "_none recorded_"} else value


def merged_tags(existing: list[str], *, drop: set[str] | None = None, add: list[str] | None = None) -> list[str]:
    dropped = {item.strip() for item in (drop or set()) if item.strip()}
    additions = [item.strip() for item in (add or []) if item.strip()]
    seen: set[str] = set()
    result: list[str] = []
    for tag in existing:
        cleaned = str(tag).strip()
        if not cleaned or cleaned in dropped or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
    for tag in additions:
        if not tag or tag in seen:
            continue
        seen.add(tag)
        result.append(tag)
    return result


def build_round_frontmatter(
    *,
    round_id: str,
    title: str,
    status: str,
    project_id: str,
    objective_id: str,
    anchor: dict[str, str],
    paths: list[str],
    created_at: str | None = None,
    evidence_refs: list[dict[str, str]] | None = None,
    tags: list[str] | None = None,
    confidence: str = "high",
    phase: str = "execution",
) -> str:
    return build_memory_frontmatter(
        item_id=round_id,
        memory_type="round-contract",
        title=title,
        status=status,
        project_id=project_id,
        anchor=anchor,
        paths=paths,
        created_at=created_at,
        evidence_refs=evidence_refs,
        tags=tags,
        confidence=confidence,
        phase=phase,
        objective_id=objective_id,
    )


def build_memory_frontmatter(
    *,
    item_id: str,
    memory_type: str,
    title: str,
    status: str,
    project_id: str,
    anchor: dict[str, str],
    paths: list[str],
    created_at: str | None = None,
    evidence_refs: list[dict[str, str]] | None = None,
    tags: list[str] | None = None,
    confidence: str = "high",
    phase: str = "",
    objective_id: str = "",
    pivot_id: str = "",
    supersedes: list[str] | None = None,
    superseded_by: list[str] | None = None,
    extra_fields: dict[str, object] | None = None,
) -> str:
    now = timestamp_now().isoformat(timespec="seconds")
    created_value = created_at or now
    evidence_refs = evidence_refs or []
    tags = tags or []
    supersedes = supersedes or []
    superseded_by = superseded_by or []
    extra_fields = extra_fields or {}
    normalized_title = normalize_scalar_metadata(title)
    normalized_confidence = normalize_scalar_metadata(confidence) or "high"
    normalized_phase = normalize_scalar_metadata(phase)
    lines = [
        "---",
        f"id: {item_id}",
        f"type: {memory_type}",
        f"title: {yaml_quote(normalized_title)}",
        f"status: {status}",
        f"project_id: {project_id}",
        f"workspace_id: {anchor.get('workspace_id', '')}",
        f"workspace_root: {anchor.get('workspace_root', '')}",
        f"branch: {anchor.get('branch', '')}",
        f"git_sha: {anchor.get('git_sha', '')}",
        "paths:",
    ]
    if paths:
        for path in paths:
            lines.append(f"  - {path}")
    else:
        lines.append("  - .")
    lines.append("thread_ids: []")
    if evidence_refs:
        lines.append("evidence_refs:")
        for entry in evidence_refs:
            evidence_type = normalize_scalar_metadata(entry.get("type", ""))
            ref = normalize_scalar_metadata(entry.get("ref", ""))
            if not ref:
                continue
            lines.append(f"  - type: {evidence_type}")
            lines.append(f"    ref: {ref}")
    else:
        lines.append("evidence_refs: []")
    if tags:
        lines.append("tags:")
        for tag in tags:
            tag_value = normalize_scalar_metadata(tag)
            if tag_value:
                lines.append(f"  - {tag_value}")
    else:
        lines.append("tags: []")
    lines.extend(
        [
            f"confidence: {normalized_confidence}",
            f"created_at: {created_value}",
            f"updated_at: {now}",
        ]
    )
    if objective_id:
        lines.append(f"objective_id: {objective_id}")
    if pivot_id:
        lines.append(f"pivot_id: {pivot_id}")
    if normalized_phase:
        lines.append(f"phase: {normalized_phase}")
    for key, raw_value in extra_fields.items():
        normalized_key = str(key).strip()
        if not normalized_key:
            continue
        if isinstance(raw_value, list):
            cleaned_items = [normalize_scalar_metadata(item) for item in raw_value if normalize_scalar_metadata(item)]
            if cleaned_items:
                lines.append(f"{normalized_key}:")
                for item in cleaned_items:
                    lines.append(f"  - {yaml_quote(item)}")
            else:
                lines.append(f"{normalized_key}: []")
            continue
        normalized_value = normalize_scalar_metadata(raw_value)
        if normalized_value:
            lines.append(f"{normalized_key}: {yaml_quote(normalized_value)}")
        else:
            lines.append(f"{normalized_key}: \"\"")
    if supersedes:
        lines.append("supersedes:")
        for item in supersedes:
            item_value = normalize_scalar_metadata(item)
            if item_value:
                lines.append(f"  - {item_value}")
    else:
        lines.append("supersedes: []")
    if superseded_by:
        lines.append("superseded_by:")
        for item in superseded_by:
            item_value = normalize_scalar_metadata(item)
            if item_value:
                lines.append(f"  - {item_value}")
    else:
        lines.append("superseded_by: []")
    lines.extend(
        [
            "---",
            "",
        ]
    )
    return "\n".join(lines)


def render_round_file(
    *,
    round_id: str,
    title: str,
    status: str,
    project_id: str,
    objective_id: str,
    anchor: dict[str, str],
    paths: list[str],
    created_at: str | None,
    evidence_refs: list[dict[str, str]] | None,
    tags: list[str] | None,
    confidence: str,
    phase: str,
    summary: str,
    scope_items: list[str],
    deliverable: str,
    validation_plan: str,
    risks: list[str],
    blockers: list[str],
    status_notes: str,
) -> str:
    frontmatter = build_round_frontmatter(
        round_id=round_id,
        title=title,
        status=status,
        project_id=project_id,
        objective_id=objective_id,
        anchor=anchor,
        paths=paths,
        created_at=created_at,
        evidence_refs=evidence_refs,
        tags=tags,
        confidence=confidence,
        phase=phase,
    )
    body_parts = [
        frontmatter,
        "## Summary\n",
        summary.strip() or "_none recorded_",
        "",
        "## Scope\n",
        render_bullet_list(scope_items),
        "",
        "## Deliverable\n",
        deliverable.strip() or "_none recorded_",
        "",
        "## Validation Plan\n",
        validation_plan.strip() or "_none recorded_",
        "",
        "## Active Risks\n",
        render_bullet_list(risks),
        "",
        "## Blockers\n",
        render_bullet_list(blockers),
        "",
        "## Status Notes\n",
        status_notes.strip() or "_none recorded_",
        "",
    ]
    return "\n".join(body_parts).strip() + "\n"


def render_objective_file(
    *,
    objective_id: str,
    title: str,
    status: str,
    project_id: str,
    anchor: dict[str, str],
    paths: list[str],
    created_at: str | None,
    evidence_refs: list[dict[str, str]] | None,
    tags: list[str] | None,
    confidence: str,
    phase: str,
    supersedes: list[str] | None,
    superseded_by: list[str] | None,
    summary: str,
    problem: str,
    success_criteria: list[str],
    non_goals: list[str],
    why_now: str,
    current_risks: list[str],
    supersession_notes: str,
) -> str:
    frontmatter = build_memory_frontmatter(
        item_id=objective_id,
        memory_type="objective",
        title=title,
        status=status,
        project_id=project_id,
        anchor=anchor,
        paths=paths,
        created_at=created_at,
        evidence_refs=evidence_refs,
        tags=tags,
        confidence=confidence,
        phase=phase,
        supersedes=supersedes,
        superseded_by=superseded_by,
    )
    body_parts = [
        frontmatter,
        "## Summary\n",
        summary.strip() or "_none recorded_",
        "",
        "## Problem\n",
        problem.strip() or "_none recorded_",
        "",
        "## Success Criteria\n",
        render_bullet_list(success_criteria),
        "",
        "## Non-Goals\n",
        render_bullet_list(non_goals),
        "",
        "## Why Now\n",
        why_now.strip() or "_none recorded_",
        "",
        "## Current Phase\n",
        phase.strip() or "_none recorded_",
        "",
        "## Active Risks\n",
        render_bullet_list(current_risks),
        "",
        "## Supersession Notes\n",
        supersession_notes.strip() or "_none recorded_",
        "",
    ]
    return "\n".join(body_parts).strip() + "\n"


def render_pivot_file(
    *,
    pivot_id: str,
    title: str,
    status: str,
    project_id: str,
    objective_id: str,
    anchor: dict[str, str],
    paths: list[str],
    created_at: str | None,
    evidence_refs: list[dict[str, str]] | None,
    tags: list[str] | None,
    confidence: str,
    phase: str,
    supersedes: list[str] | None,
    superseded_by: list[str] | None,
    summary: str,
    pivot_type: str,
    trigger: str,
    change_summary: str,
    identity_rationale: str,
    previous_objective: str,
    new_objective: str,
    evidence: list[str],
    decisions_retained: list[str],
    assumptions_invalidated: list[str],
    next_control_changes: list[str],
) -> str:
    frontmatter = build_memory_frontmatter(
        item_id=pivot_id,
        memory_type="pivot",
        title=title,
        status=status,
        project_id=project_id,
        anchor=anchor,
        paths=paths,
        created_at=created_at,
        evidence_refs=evidence_refs,
        tags=tags,
        confidence=confidence,
        phase=phase,
        objective_id=objective_id,
        supersedes=supersedes,
        superseded_by=superseded_by,
    )
    body_parts = [
        frontmatter,
        "## Summary\n",
        summary.strip() or "_none recorded_",
        "",
        "## Pivot Type\n",
        pivot_type.strip() or "_none recorded_",
        "",
        "## Trigger\n",
        trigger.strip() or "_none recorded_",
        "",
        "## Change Summary\n",
        change_summary.strip() or "_none recorded_",
        "",
        "## Identity Rationale\n",
        identity_rationale.strip() or "_none recorded_",
        "",
        "## Previous Objective\n",
        previous_objective.strip() or "_none recorded_",
        "",
        "## New Objective\n",
        new_objective.strip() or "_none recorded_",
        "",
        "## Evidence\n",
        render_bullet_list(evidence),
        "",
        "## Decisions Retained\n",
        render_bullet_list(decisions_retained),
        "",
        "## Assumptions Invalidated\n",
        render_bullet_list(assumptions_invalidated),
        "",
        "## Next Control Changes\n",
        render_bullet_list(next_control_changes),
        "",
    ]
    return "\n".join(body_parts).strip() + "\n"


def render_adjudication_file(
    *,
    adjudication_id: str,
    title: str,
    status: str,
    project_id: str,
    objective_id: str,
    anchor: dict[str, str],
    paths: list[str],
    created_at: str | None,
    evidence_refs: list[dict[str, str]] | None,
    tags: list[str] | None,
    confidence: str,
    phase: str,
    summary: str,
    conflict_set: list[str],
    adjudication_question: str,
    verdict: str,
    objects_retained: list[str],
    objects_invalidated: list[str],
    required_follow_up_transitions: list[str],
    executor_followups: list[str] | None,
    evidence: list[str],
    round_title: str = "",
    round_scope_items: list[str] | None = None,
    round_scope_paths: list[str] | None = None,
    round_deliverable: str = "",
    round_validation_plan: str = "",
    round_risks: list[str] | None = None,
    round_blockers: list[str] | None = None,
    round_status_note: str = "",
) -> str:
    round_scope_items = round_scope_items or []
    round_scope_paths = round_scope_paths or []
    round_risks = round_risks or []
    round_blockers = round_blockers or []
    executor_followups = executor_followups or []
    extra_fields: dict[str, object] = {
        "round_scope_items": round_scope_items,
        "round_scope_paths": round_scope_paths,
        "round_risks": round_risks,
        "round_blockers": round_blockers,
        "executor_followups": executor_followups,
    }
    if round_title.strip():
        extra_fields["round_title"] = round_title
    if round_deliverable.strip():
        extra_fields["round_deliverable"] = round_deliverable
    if round_validation_plan.strip():
        extra_fields["round_validation_plan"] = round_validation_plan
    if round_status_note.strip():
        extra_fields["round_status_note"] = round_status_note
    frontmatter = build_memory_frontmatter(
        item_id=adjudication_id,
        memory_type="adjudication",
        title=title,
        status=status,
        project_id=project_id,
        anchor=anchor,
        paths=paths,
        created_at=created_at,
        evidence_refs=evidence_refs,
        tags=tags,
        confidence=confidence,
        phase=phase,
        objective_id=objective_id,
        extra_fields=extra_fields,
    )
    body_parts = [
        frontmatter,
        "## Summary\n",
        summary.strip() or "_none recorded_",
        "",
        "## Conflict Set\n",
        render_bullet_list(conflict_set),
        "",
        "## Adjudication Question\n",
        adjudication_question.strip() or "_none recorded_",
        "",
        "## Verdict\n",
        verdict.strip() or "_none recorded_",
        "",
        "## Objects Retained\n",
        render_bullet_list(objects_retained),
        "",
        "## Objects Invalidated\n",
        render_bullet_list(objects_invalidated),
        "",
        "## Required Follow-Up Transitions\n",
        render_bullet_list(required_follow_up_transitions),
        "",
        "## Evidence\n",
        render_bullet_list(evidence),
        "",
    ]
    return "\n".join(body_parts).strip() + "\n"


def render_exception_contract_file(
    *,
    exception_contract_id: str,
    title: str,
    status: str,
    project_id: str,
    objective_id: str,
    pivot_id: str,
    anchor: dict[str, str],
    paths: list[str],
    created_at: str | None,
    evidence_refs: list[dict[str, str]] | None,
    tags: list[str] | None,
    confidence: str,
    phase: str,
    summary: str,
    reason: str,
    temporary_behavior: str,
    risk: str,
    exit_condition: str,
    owner_scope: list[str],
    evidence: list[str],
    resolution: str,
) -> str:
    frontmatter = build_memory_frontmatter(
        item_id=exception_contract_id,
        memory_type="exception-contract",
        title=title,
        status=status,
        project_id=project_id,
        anchor=anchor,
        paths=paths,
        created_at=created_at,
        evidence_refs=evidence_refs,
        tags=tags,
        confidence=confidence,
        phase=phase,
        objective_id=objective_id,
        pivot_id=pivot_id,
    )
    body_parts = [
        frontmatter,
        "## Summary\n",
        summary.strip() or "_none recorded_",
        "",
        "## Reason\n",
        reason.strip() or "_none recorded_",
        "",
        "## Temporary Behavior\n",
        temporary_behavior.strip() or "_none recorded_",
        "",
        "## Risk\n",
        risk.strip() or "_none recorded_",
        "",
        "## Exit Condition\n",
        exit_condition.strip() or "_none recorded_",
        "",
        "## Owner Scope\n",
        render_bullet_list(owner_scope),
        "",
        "## Evidence\n",
        render_bullet_list(evidence),
        "",
        "## Resolution\n",
        resolution.strip() or "_none recorded_",
        "",
    ]
    return "\n".join(body_parts).strip() + "\n"


def render_exception_ledger_file(project_id: str) -> str:
    records = load_all_exception_contracts(project_id)
    grouped: dict[str, list[tuple[Path, dict[str, object], dict[str, str]]]] = {
        "active": [],
        "retired": [],
        "invalidated": [],
    }
    for record in records:
        _path, meta, _sections = record
        status = str(meta.get("status") or "").strip()
        if status in grouped:
            grouped[status].append(record)

    def render_group(records: list[tuple[Path, dict[str, object], dict[str, str]]]) -> str:
        if not records:
            return "- None recorded yet."
        lines: list[str] = []
        for _path, meta, sections in records:
            contract_id = str(meta.get("id") or "").strip()
            title = str(meta.get("title") or contract_id).strip() or contract_id
            objective_id = str(meta.get("objective_id") or "").strip()
            pivot_id = str(meta.get("pivot_id") or "").strip()
            exit_condition = summarize_line(sections.get("Exit Condition", ""))
            resolution = summarize_line(sections.get("Resolution", ""))
            owner_scope = parse_bullet_list(sections.get("Owner Scope", ""))
            lines.append(f"- `{contract_id}`: {title}")
            if objective_id:
                lines.append(f"  - objective: `{objective_id}`")
            if owner_scope:
                lines.append(f"  - owner scope: {normalize_phrase(owner_scope[0])}")
            if exit_condition != "_none recorded_":
                lines.append(f"  - exit condition: {exit_condition}")
            if pivot_id:
                lines.append(f"  - pivot: `{pivot_id}`")
            if resolution != "_none recorded_":
                lines.append(f"  - resolution: {resolution}")
        return "\n".join(lines)

    parts = [
        "# Exception Ledger",
        "",
        "## Active",
        "",
        render_group(grouped["active"]),
        "",
        "## Retired",
        "",
        render_group(grouped["retired"]),
        "",
        "## Invalidated",
        "",
        render_group(grouped["invalidated"]),
        "",
    ]
    return "\n".join(parts).strip() + "\n"


def render_active_objective_file(
    *,
    objective_id: str,
    phase: str,
    status: str,
    problem: str,
    success_criteria: list[str],
    non_goals: list[str],
    why_now: str,
    current_risks: list[str],
) -> str:
    parts = [
        "# Active Objective",
        "",
        f"- Objective id: `{objective_id}`",
        f"- Phase: `{phase}`",
        f"- Status: `{status}`",
        "",
        "## Problem",
        "",
        problem.strip() or "_none recorded_",
        "",
        "## Success Criteria",
        "",
        render_bullet_list(success_criteria),
        "",
        "## Non-Goals",
        "",
        render_bullet_list(non_goals),
        "",
        "## Why Now",
        "",
        why_now.strip() or "_none recorded_",
        "",
        "## Current Risks",
        "",
        render_bullet_list(current_risks),
        "",
    ]
    return "\n".join(parts).strip() + "\n"


def render_active_round_file(
    *,
    round_id: str,
    objective_id: str,
    status: str,
    scope_items: list[str],
    deliverable: str,
    validation_plan: str,
    risks: list[str],
    blockers: list[str],
) -> str:
    parts = [
        "# Active Round",
        "",
        f"- Round id: `{round_id}`",
        f"- Objective id: `{objective_id}`",
        f"- Status: `{status}`",
        "",
        "## Scope",
        "",
        render_bullet_list(scope_items),
        "",
        "## Deliverable",
        "",
        deliverable.strip() or "_none recorded_",
        "",
        "## Validation Plan",
        "",
        validation_plan.strip() or "_none recorded_",
        "",
        "## Active Risks",
        "",
        render_bullet_list(risks),
        "",
        "## Blockers",
        "",
        render_bullet_list(blockers),
        "",
    ]
    return "\n".join(parts).strip() + "\n"


def record_sort_key(path: Path, meta: dict[str, object]) -> str:
    updated_at = str(meta.get("updated_at") or "").strip()
    created_at = str(meta.get("created_at") or "").strip()
    return updated_at or created_at or path.name


def locate_round_file(project_id: str, round_id: str) -> Path | None:
    directory = rounds_dir(project_id)
    if not directory.exists():
        return None
    for path in sorted(directory.glob("*.md")):
        values = extract_frontmatter_scalars(read_text(path), ["id"])
        if values.get("id") == round_id:
            return path
    return None


def locate_objective_file(project_id: str, objective_id: str) -> Path | None:
    directory = objectives_dir(project_id)
    if not directory.exists():
        return None
    for path in sorted(directory.glob("*.md")):
        values = extract_frontmatter_scalars(read_text(path), ["id"])
        if values.get("id") == objective_id:
            return path
    return None


def locate_exception_contract_file(project_id: str, exception_contract_id: str) -> Path | None:
    directory = exception_contracts_dir(project_id)
    if not directory.exists():
        return None
    for path in sorted(directory.glob("*.md")):
        values = extract_frontmatter_scalars(read_text(path), ["id"])
        if values.get("id") == exception_contract_id:
            return path
    return None


def locate_pivot_file(project_id: str, pivot_id: str) -> Path | None:
    directory = pivots_dir(project_id)
    if not directory.exists():
        return None
    for path in sorted(directory.glob("*.md")):
        values = extract_frontmatter_scalars(read_text(path), ["id"])
        if values.get("id") == pivot_id:
            return path
    return None


def load_round_file(path: Path) -> tuple[dict[str, object], dict[str, str]]:
    text = read_text(path)
    frontmatter_text, _body = split_frontmatter(text)
    meta = parse_frontmatter(frontmatter_text)
    for key in ["id", "title", "status", "project_id", "workspace_id", "workspace_root", "branch", "git_sha", "objective_id", "created_at", "confidence", "phase"]:
        if key in meta:
            meta[key] = normalize_scalar_metadata(meta[key])
    meta["paths"] = parse_string_list(meta.get("paths"))
    normalized_tags: list[str] = []
    for item in parse_string_list(meta.get("tags")):
        normalized_tag = normalize_scalar_metadata(item)
        if normalized_tag:
            normalized_tags.append(normalized_tag)
    meta["tags"] = normalized_tags

    normalized_evidence_refs: list[dict[str, str]] = []
    for entry in parse_evidence_refs(meta.get("evidence_refs", [])):
        normalized_ref = normalize_scalar_metadata(entry.get("ref", ""))
        if not normalized_ref:
            continue
        normalized_evidence_refs.append(
            {
                "type": normalize_scalar_metadata(entry.get("type", "")),
                "ref": normalized_ref,
            }
        )
    meta["evidence_refs"] = normalized_evidence_refs
    sections = parse_h2_sections(clean_section_text(path, strip_heading=False, strip_yaml=True))
    return meta, sections


def load_objective_file(path: Path) -> tuple[dict[str, object], dict[str, str]]:
    text = read_text(path)
    frontmatter_text, _body = split_frontmatter(text)
    meta = parse_frontmatter(frontmatter_text)
    for key in [
        "id",
        "title",
        "status",
        "project_id",
        "workspace_id",
        "workspace_root",
        "branch",
        "git_sha",
        "created_at",
        "confidence",
        "phase",
    ]:
        if key in meta:
            meta[key] = normalize_scalar_metadata(meta[key])
    meta["paths"] = parse_string_list(meta.get("paths"))
    meta["tags"] = [normalize_scalar_metadata(item) for item in parse_string_list(meta.get("tags")) if normalize_scalar_metadata(item)]
    meta["supersedes"] = [normalize_scalar_metadata(item) for item in parse_string_list(meta.get("supersedes")) if normalize_scalar_metadata(item)]
    meta["superseded_by"] = [normalize_scalar_metadata(item) for item in parse_string_list(meta.get("superseded_by")) if normalize_scalar_metadata(item)]
    normalized_evidence_refs: list[dict[str, str]] = []
    for entry in parse_evidence_refs(meta.get("evidence_refs", [])):
        normalized_ref = normalize_scalar_metadata(entry.get("ref", ""))
        if not normalized_ref:
            continue
        normalized_evidence_refs.append(
            {
                "type": normalize_scalar_metadata(entry.get("type", "")),
                "ref": normalized_ref,
            }
        )
    meta["evidence_refs"] = normalized_evidence_refs
    sections = parse_h2_sections(clean_section_text(path, strip_heading=False, strip_yaml=True))
    return meta, sections


def objective_record_payload(meta: dict[str, object], sections: dict[str, str]) -> dict[str, object]:
    return {
        "title": str(meta.get("title") or str(meta.get("id") or "")).strip(),
        "status": str(meta.get("status") or "").strip(),
        "paths": [str(item).strip() for item in meta.get("paths", []) if str(item).strip()],
        "created_at": str(meta.get("created_at") or "").strip(),
        "evidence_refs": [entry for entry in meta.get("evidence_refs", []) if isinstance(entry, dict)],
        "tags": [str(item).strip() for item in meta.get("tags", []) if str(item).strip()],
        "confidence": str(meta.get("confidence") or "high").strip() or "high",
        "phase": str(meta.get("phase") or "").strip(),
        "supersedes": [str(item).strip() for item in meta.get("supersedes", []) if str(item).strip()],
        "superseded_by": [str(item).strip() for item in meta.get("superseded_by", []) if str(item).strip()],
        "summary": normalize_section_text(sections.get("Summary", "")),
        "problem": normalize_section_text(sections.get("Problem", "")),
        "success_criteria": parse_bullet_list(sections.get("Success Criteria", "")),
        "non_goals": parse_bullet_list(sections.get("Non-Goals", "")),
        "why_now": normalize_section_text(sections.get("Why Now", "")),
        "current_risks": parse_bullet_list(sections.get("Active Risks", "")),
        "supersession_notes": normalize_section_text(sections.get("Supersession Notes", "")),
    }


def load_pivot_file(path: Path) -> tuple[dict[str, object], dict[str, str]]:
    text = read_text(path)
    frontmatter_text, _body = split_frontmatter(text)
    meta = parse_frontmatter(frontmatter_text)
    for key in [
        "id",
        "title",
        "status",
        "project_id",
        "workspace_id",
        "workspace_root",
        "branch",
        "git_sha",
        "created_at",
        "confidence",
        "phase",
        "objective_id",
    ]:
        if key in meta:
            meta[key] = normalize_scalar_metadata(meta[key])
    meta["paths"] = parse_string_list(meta.get("paths"))
    meta["tags"] = [normalize_scalar_metadata(item) for item in parse_string_list(meta.get("tags")) if normalize_scalar_metadata(item)]
    meta["supersedes"] = [normalize_scalar_metadata(item) for item in parse_string_list(meta.get("supersedes")) if normalize_scalar_metadata(item)]
    meta["superseded_by"] = [normalize_scalar_metadata(item) for item in parse_string_list(meta.get("superseded_by")) if normalize_scalar_metadata(item)]
    normalized_evidence_refs: list[dict[str, str]] = []
    for entry in parse_evidence_refs(meta.get("evidence_refs", [])):
        normalized_ref = normalize_scalar_metadata(entry.get("ref", ""))
        if not normalized_ref:
            continue
        normalized_evidence_refs.append(
            {
                "type": normalize_scalar_metadata(entry.get("type", "")),
                "ref": normalized_ref,
            }
        )
    meta["evidence_refs"] = normalized_evidence_refs
    sections = parse_h2_sections(clean_section_text(path, strip_heading=False, strip_yaml=True))
    return meta, sections


def load_exception_contract_file(path: Path) -> tuple[dict[str, object], dict[str, str]]:
    text = read_text(path)
    frontmatter_text, _body = split_frontmatter(text)
    meta = parse_frontmatter(frontmatter_text)
    for key in [
        "id",
        "title",
        "status",
        "project_id",
        "workspace_id",
        "workspace_root",
        "branch",
        "git_sha",
        "created_at",
        "confidence",
        "phase",
        "objective_id",
        "pivot_id",
    ]:
        if key in meta:
            meta[key] = normalize_scalar_metadata(meta[key])
    meta["paths"] = parse_string_list(meta.get("paths"))
    meta["tags"] = [normalize_scalar_metadata(item) for item in parse_string_list(meta.get("tags")) if normalize_scalar_metadata(item)]
    normalized_evidence_refs: list[dict[str, str]] = []
    for entry in parse_evidence_refs(meta.get("evidence_refs", [])):
        normalized_ref = normalize_scalar_metadata(entry.get("ref", ""))
        if not normalized_ref:
            continue
        normalized_evidence_refs.append(
            {
                "type": normalize_scalar_metadata(entry.get("type", "")),
                "ref": normalized_ref,
            }
        )
    meta["evidence_refs"] = normalized_evidence_refs
    sections = parse_h2_sections(clean_section_text(path, strip_heading=False, strip_yaml=True))
    return meta, sections


def load_adjudication_file(path: Path) -> tuple[dict[str, object], dict[str, str]]:
    text = read_text(path)
    frontmatter_text, _body = split_frontmatter(text)
    meta = parse_frontmatter(frontmatter_text)
    for key in [
        "id",
        "title",
        "status",
        "project_id",
        "workspace_id",
        "workspace_root",
        "branch",
        "git_sha",
        "created_at",
        "confidence",
        "phase",
        "objective_id",
        "round_title",
        "round_deliverable",
        "round_validation_plan",
        "round_status_note",
    ]:
        if key in meta:
            meta[key] = normalize_scalar_metadata(meta[key])
    meta["paths"] = parse_string_list(meta.get("paths"))
    meta["tags"] = [normalize_scalar_metadata(item) for item in parse_string_list(meta.get("tags")) if normalize_scalar_metadata(item)]
    meta["round_scope_items"] = [normalize_scalar_metadata(item) for item in parse_string_list(meta.get("round_scope_items")) if normalize_scalar_metadata(item)]
    meta["round_scope_paths"] = [normalize_scalar_metadata(item) for item in parse_string_list(meta.get("round_scope_paths")) if normalize_scalar_metadata(item)]
    meta["round_risks"] = [normalize_scalar_metadata(item) for item in parse_string_list(meta.get("round_risks")) if normalize_scalar_metadata(item)]
    meta["round_blockers"] = [normalize_scalar_metadata(item) for item in parse_string_list(meta.get("round_blockers")) if normalize_scalar_metadata(item)]
    meta["executor_followups"] = [normalize_scalar_metadata(item) for item in parse_string_list(meta.get("executor_followups")) if normalize_scalar_metadata(item)]
    normalized_evidence_refs: list[dict[str, str]] = []
    for entry in parse_evidence_refs(meta.get("evidence_refs", [])):
        normalized_ref = normalize_scalar_metadata(entry.get("ref", ""))
        if not normalized_ref:
            continue
        normalized_evidence_refs.append(
            {
                "type": normalize_scalar_metadata(entry.get("type", "")),
                "ref": normalized_ref,
            }
        )
    meta["evidence_refs"] = normalized_evidence_refs
    sections = parse_h2_sections(clean_section_text(path, strip_heading=False, strip_yaml=True))
    return meta, sections


def load_all_objectives(project_id: str) -> list[tuple[Path, dict[str, object], dict[str, str]]]:
    directory = objectives_dir(project_id)
    if not directory.exists():
        return []
    records: list[tuple[Path, dict[str, object], dict[str, str]]] = []
    for path in sorted(directory.glob("*.md")):
        meta, sections = load_objective_file(path)
        records.append((path, meta, sections))
    records.sort(key=lambda record: str(record[1].get("created_at") or record[0].name))
    return records


def load_all_rounds(project_id: str) -> list[tuple[Path, dict[str, object], dict[str, str]]]:
    directory = rounds_dir(project_id)
    if not directory.exists():
        return []
    records: list[tuple[Path, dict[str, object], dict[str, str]]] = []
    for path in sorted(directory.glob("*.md")):
        meta, sections = load_round_file(path)
        records.append((path, meta, sections))
    records.sort(key=lambda record: str(record[1].get("created_at") or record[0].name))
    return records


def load_all_pivots(project_id: str) -> list[tuple[Path, dict[str, object], dict[str, str]]]:
    directory = pivots_dir(project_id)
    if not directory.exists():
        return []
    records: list[tuple[Path, dict[str, object], dict[str, str]]] = []
    for path in sorted(directory.glob("*.md")):
        meta, sections = load_pivot_file(path)
        records.append((path, meta, sections))
    records.sort(key=lambda record: str(record[1].get("created_at") or record[0].name), reverse=True)
    return records


def load_all_exception_contracts(project_id: str) -> list[tuple[Path, dict[str, object], dict[str, str]]]:
    directory = exception_contracts_dir(project_id)
    if not directory.exists():
        return []
    records: list[tuple[Path, dict[str, object], dict[str, str]]] = []
    for path in sorted(directory.glob("*.md")):
        meta, sections = load_exception_contract_file(path)
        records.append((path, meta, sections))
    records.sort(key=lambda record: record_sort_key(record[0], record[1]), reverse=True)
    return records


def load_all_adjudications(project_id: str) -> list[tuple[Path, dict[str, object], dict[str, str]]]:
    directory = adjudications_dir(project_id)
    if not directory.exists():
        return []
    records: list[tuple[Path, dict[str, object], dict[str, str]]] = []
    for path in sorted(directory.glob("*.md")):
        meta, sections = load_adjudication_file(path)
        records.append((path, meta, sections))
    records.sort(key=lambda record: str(record[1].get("created_at") or record[0].name), reverse=True)
    return records


def find_objectives_by_status(
    project_id: str,
    *,
    statuses: set[str] | None = None,
) -> list[tuple[Path, dict[str, object], dict[str, str]]]:
    allowed_statuses = {status.strip() for status in (statuses or set()) if status.strip()}
    matches: list[tuple[Path, dict[str, object], dict[str, str]]] = []
    for record in load_all_objectives(project_id):
        _path, meta, _sections = record
        status = str(meta.get("status") or "").strip()
        if allowed_statuses and status not in allowed_statuses:
            continue
        matches.append(record)
    return matches


def find_rounds(
    project_id: str,
    *,
    objective_id: str = "",
    statuses: set[str] | None = None,
) -> list[tuple[Path, dict[str, object], dict[str, str]]]:
    target_objective_id = objective_id.strip()
    allowed_statuses = {status.strip() for status in (statuses or set()) if status.strip()}
    matches: list[tuple[Path, dict[str, object], dict[str, str]]] = []
    for record in load_all_rounds(project_id):
        _path, meta, _sections = record
        round_objective_id = str(meta.get("objective_id") or "").strip()
        status = str(meta.get("status") or "").strip()
        if target_objective_id and round_objective_id != target_objective_id:
            continue
        if allowed_statuses and status not in allowed_statuses:
            continue
        matches.append(record)
    return matches


def find_exception_contracts(
    project_id: str,
    *,
    objective_id: str = "",
    statuses: set[str] | None = None,
) -> list[tuple[Path, dict[str, object], dict[str, str]]]:
    target_objective_id = objective_id.strip()
    allowed_statuses = {status.strip() for status in (statuses or set()) if status.strip()}
    matches: list[tuple[Path, dict[str, object], dict[str, str]]] = []
    for record in load_all_exception_contracts(project_id):
        _path, meta, _sections = record
        contract_objective_id = str(meta.get("objective_id") or "").strip()
        status = str(meta.get("status") or "").strip()
        if target_objective_id and contract_objective_id != target_objective_id:
            continue
        if allowed_statuses and status not in allowed_statuses:
            continue
        matches.append(record)
    return matches


def active_exception_contract_records(
    project_id: str,
    *,
    objective_id: str = "",
) -> list[tuple[Path, dict[str, object], dict[str, str]]]:
    return find_exception_contracts(project_id, objective_id=objective_id, statuses={"active"})


def select_active_objective_record(
    project_id: str,
) -> tuple[tuple[Path, dict[str, object], dict[str, str]] | None, list[str]]:
    active_records = find_objectives_by_status(project_id, statuses={"active"})
    issues: list[str] = []
    if len(active_records) > 1:
        rendered_ids = ", ".join(
            f"`{str(meta.get('id') or path.stem)}`"
            for path, meta, _sections in active_records
        )
        issues.append(f"multiple durable active objectives exist: {rendered_ids}")
        return None, issues
    if len(active_records) == 1:
        return active_records[0], issues
    return None, issues


def select_open_round_record(
    project_id: str,
) -> tuple[tuple[Path, dict[str, object], dict[str, str]] | None, list[str]]:
    open_rounds = find_rounds(project_id, statuses=OPEN_ROUND_STATUSES)
    issues: list[str] = []
    if len(open_rounds) > 1:
        rendered_ids = ", ".join(
            f"`{str(meta.get('id') or path.stem)}` ({str(meta.get('status') or 'unknown').strip()})"
            for path, meta, _sections in open_rounds
        )
        issues.append(f"multiple durable open rounds exist: {rendered_ids}")
        return None, issues
    if len(open_rounds) == 1:
        return open_rounds[0], issues
    return None, issues


def resolve_active_objective_record(
    project_id: str,
    *,
    objective_id: str = "",
    require_control_projection: bool = True,
) -> tuple[Path, dict[str, object], dict[str, str], str]:
    active_objective_preface, _active_objective_sections = load_active_objective(project_id)
    control_objective_id = str(active_objective_preface.get("objective id", "")).strip()
    control_status = str(active_objective_preface.get("status", "")).strip()
    target_objective_id = objective_id.strip() or control_objective_id

    if require_control_projection and not control_objective_id:
        raise SystemExit(
            f"missing active objective control state in `{active_objective_path(project_id)}`; "
            "repair control state before rewriting the active objective line"
        )
    if not target_objective_id:
        raise SystemExit("missing objective id; pass --objective-id or maintain control/active-objective.md")
    if require_control_projection and target_objective_id != control_objective_id:
        raise SystemExit(
            f"requested objective `{target_objective_id}` does not match control active objective `{control_objective_id}`"
        )
    if require_control_projection and control_status and control_status != "active":
        raise SystemExit(f"active objective control state is not active; found `{control_status}`")

    active_record, issues = select_active_objective_record(project_id)
    if issues:
        raise SystemExit(
            "cannot resolve one authoritative durable active objective: " + "; ".join(issues)
        )
    if active_record is None:
        raise SystemExit("no durable active objective exists")

    path, meta, sections = active_record
    durable_objective_id = str(meta.get("id") or path.stem).strip()
    durable_status = str(meta.get("status") or "").strip()
    if target_objective_id != durable_objective_id:
        raise SystemExit(
            f"requested objective `{target_objective_id}` does not match durable active objective `{durable_objective_id}`"
        )
    if durable_status != "active":
        raise SystemExit(
            f"active objective rewrite requires durable status `active`; found `{durable_status or 'unknown'}`"
        )
    return path, meta, sections, durable_objective_id


def extract_first_inline_id(text: str) -> str:
    match = re.search(r"`([^`]+)`", text)
    return match.group(1).strip() if match else ""


def summarize_line(text: str) -> str:
    cleaned = " ".join(part.strip() for part in text.splitlines() if part.strip())
    return cleaned or "_none recorded_"


def normalize_phrase(text: str) -> str:
    summary = summarize_line(text)
    if summary == "_none recorded_":
        return summary
    return summary.rstrip(" .")


def render_pivot_log_file(project_id: str) -> str:
    objective_records = load_all_objectives(project_id)
    pivot_records = load_all_pivots(project_id)
    active_objective_id = ""
    active_objective_title = ""
    for _path, meta, _sections in objective_records:
        if str(meta.get("status") or "") == "active":
            active_objective_id = str(meta.get("id") or "")
            active_objective_title = str(meta.get("title") or "")
            break

    parts = [
        "# Pivot Log",
        "",
        "## Active Lineage",
        "",
    ]
    if active_objective_id:
        parts.append(f"- `{active_objective_id}`")
        parts.append(f"  - active objective: {active_objective_title or active_objective_id}")
        for _path, meta, sections in pivot_records:
            if str(meta.get("objective_id") or "") != active_objective_id:
                continue
            pivot_type = normalize_phrase(sections.get("Pivot Type", ""))
            pivot_label = pivot_type.lower()
            if pivot_label.endswith("pivot"):
                parts.append(f"  - entered via {pivot_label} `{meta.get('id', '')}`")
            else:
                parts.append(f"  - entered via {pivot_label} pivot `{meta.get('id', '')}`")
            break
    else:
        parts.append("_none recorded_")

    parts.extend(["", "## Recent Pivots", ""])
    if pivot_records:
        for _path, meta, sections in pivot_records:
            pivot_id = str(meta.get("id") or "")
            pivot_type = normalize_phrase(sections.get("Pivot Type", ""))
            previous_objective_id = extract_first_inline_id(sections.get("Previous Objective", ""))
            next_objective_id = str(meta.get("objective_id") or "") or extract_first_inline_id(sections.get("New Objective", ""))
            trigger = summarize_line(sections.get("Trigger", ""))
            parts.append(f"- `{pivot_id}`")
            parts.append(f"  - type: `{pivot_type.lower()}`")
            if previous_objective_id:
                parts.append(f"  - from: `{previous_objective_id}`")
            if next_objective_id:
                parts.append(f"  - to: `{next_objective_id}`")
            parts.append(f"  - trigger: {trigger}")
    else:
        parts.append("_none recorded_")

    parts.extend(["", "## Historical Objectives", ""])
    historical_objectives = [
        (meta, sections)
        for _path, meta, sections in objective_records
        if str(meta.get("status") or "") != "active"
    ]
    if historical_objectives:
        for meta, _sections in historical_objectives:
            objective_id = str(meta.get("id") or "")
            title = str(meta.get("title") or objective_id)
            superseded_by = [str(item).strip() for item in meta.get("superseded_by", []) if str(item).strip()]
            parts.append(f"- `{objective_id}`")
            parts.append(f"  - {title}")
            if superseded_by:
                parts.append(f"  - superseded by `{superseded_by[0]}`")
            elif str(meta.get("status") or "") != "active":
                parts.append(f"  - status: `{meta.get('status', '')}`")
    else:
        parts.append("_none recorded_")

    parts.append("")
    return "\n".join(parts).strip() + "\n"


def build_transition_event_file(
    *,
    project_id: str,
    command_name: str,
    title: str,
    anchor: dict[str, str],
    previous_state: str,
    next_state: str,
    guards: list[str],
    side_effects: list[str],
    evidence: list[str],
    target_ids: list[str],
) -> tuple[str, str]:
    timestamp = timestamp_now()
    slug = slugify(f"{command_name}-{title}")
    event_id = f"trans-{timestamp.strftime('%Y-%m-%d-%H%M%S')}-{slug}"
    normalized_target_ids = [target_id.strip() for target_id in target_ids if target_id.strip()]
    frontmatter = [
        "---",
        f"id: {event_id}",
        "type: transition-event",
        f"title: {yaml_quote(title)}",
        "status: recorded",
        f"project_id: {project_id}",
        f"workspace_id: {anchor.get('workspace_id', '')}",
        f"workspace_root: {anchor.get('workspace_root', '')}",
        f"branch: {anchor.get('branch', '')}",
        f"git_sha: {anchor.get('git_sha', '')}",
        "paths:",
    ]
    if normalized_target_ids:
        for target_id in normalized_target_ids:
            frontmatter.append(f"  - {target_id}")
    else:
        frontmatter.append("  - .")
    frontmatter.extend(
        [
            "thread_ids: []",
            "evidence_refs: []",
            "tags:",
            "  - transition-event",
            f"  - {command_name}",
            "confidence: high",
            f"created_at: {timestamp.isoformat(timespec='seconds')}",
            f"updated_at: {timestamp.isoformat(timespec='seconds')}",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
        ]
    )
    body = [
        "\n".join(frontmatter),
        "## Summary\n",
        title,
        "",
        "## Command\n",
        command_name,
        "",
        "## Previous State\n",
        previous_state,
        "",
        "## Next State\n",
        next_state,
        "",
        "## Guards\n",
        render_bullet_list(guards),
        "",
        "## Side Effects\n",
        render_bullet_list(side_effects),
        "",
        "## Evidence\n",
        render_bullet_list(evidence),
        "",
    ]
    return event_id, "\n".join(body).strip() + "\n"


def _relative_to_project_parent(path: Path, project_path: Path) -> str:
    try:
        return path.relative_to(project_path.parent).as_posix()
    except ValueError:
        return path.as_posix()


def apply_transition_writes(
    project_id: str,
    writes: list[dict[str, object]],
) -> list[str]:
    project_path = project_dir(project_id)
    if not project_path.exists():
        raise SystemExit(f"project directory not found: {project_path}")

    side_effects: list[str] = []
    for entry in writes:
        raw_path = entry.get("path")
        if not isinstance(raw_path, Path):
            raw_path = Path(str(raw_path))
        path = raw_path
        label = str(entry.get("label") or "file").strip()
        text = entry.get("text")
        if callable(text):
            text = text()
        existed_before = path.exists()
        relative_path = _relative_to_project_parent(path, project_path)

        if text is None:
            if existed_before:
                path.unlink()
                side_effects.append(f"removed {label} `{relative_path}`")
            continue

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(text), encoding="utf-8")
        verb = "updated" if existed_before else "wrote"
        side_effects.append(f"{verb} {label} `{relative_path}`")
    return side_effects


def write_transition_event(
    *,
    project_id: str,
    command_name: str,
    title: str,
    anchor: dict[str, str],
    previous_state: str,
    next_state: str,
    guards: list[str],
    side_effects: list[str],
    evidence: list[str],
    target_ids: list[str],
    file_stem: str,
) -> tuple[str, Path]:
    event_id, event_text = build_transition_event_file(
        project_id=project_id,
        command_name=command_name,
        title=title,
        anchor=anchor,
        previous_state=previous_state,
        next_state=next_state,
        guards=guards,
        side_effects=side_effects,
        evidence=evidence,
        target_ids=target_ids,
    )
    event_path = transition_events_dir(project_id) / f"{safe_file_stem(file_stem)}.md"
    event_path.parent.mkdir(parents=True, exist_ok=True)
    event_path.write_text(event_text, encoding="utf-8")
    return event_id, event_path


def apply_transition_transaction(
    *,
    project_id: str,
    writes: list[dict[str, object]],
    command_name: str,
    title: str,
    anchor: dict[str, str],
    previous_state: str,
    next_state: str,
    guards: list[str],
    evidence: list[str],
    target_ids: list[str],
    event_file_stem: str,
) -> tuple[list[str], str, Path]:
    side_effects = apply_transition_writes(project_id, writes)
    event_id, event_path = write_transition_event(
        project_id=project_id,
        command_name=command_name,
        title=title,
        anchor=anchor,
        previous_state=previous_state,
        next_state=next_state,
        guards=guards,
        side_effects=side_effects,
        evidence=evidence,
        target_ids=target_ids,
        file_stem=event_file_stem,
    )
    return side_effects, event_id, event_path
