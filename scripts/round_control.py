#!/usr/bin/env python3
from __future__ import annotations

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


def project_dir(project_id: str) -> Path:
    return ROOT / "projects" / project_id


def active_objective_path(project_id: str) -> Path:
    return project_dir(project_id) / "control" / "active-objective.md"


def active_round_path(project_id: str) -> Path:
    return project_dir(project_id) / "control" / "active-round.md"


def pivot_log_path(project_id: str) -> Path:
    return project_dir(project_id) / "control" / "pivot-log.md"


def rounds_dir(project_id: str) -> Path:
    return project_dir(project_id) / "memory" / "rounds"


def objectives_dir(project_id: str) -> Path:
    return project_dir(project_id) / "memory" / "objectives"


def pivots_dir(project_id: str) -> Path:
    return project_dir(project_id) / "memory" / "pivots"


def transition_events_dir(project_id: str) -> Path:
    return project_dir(project_id) / "memory" / "transition-events"


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
    supersedes: list[str] | None = None,
    superseded_by: list[str] | None = None,
) -> str:
    now = timestamp_now().isoformat(timespec="seconds")
    created_value = created_at or now
    evidence_refs = evidence_refs or []
    tags = tags or []
    supersedes = supersedes or []
    superseded_by = superseded_by or []
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
    if normalized_phase:
        lines.append(f"phase: {normalized_phase}")
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


def select_active_objective_record(
    project_id: str,
) -> tuple[tuple[Path, dict[str, object], dict[str, str]] | None, list[str]]:
    objective_records = load_all_objectives(project_id)
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
    if objective_records:
        issues.append("durable objective history exists but no active objective is marked `active`")
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
    if target_ids:
        for target_id in target_ids:
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
