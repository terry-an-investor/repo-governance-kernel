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


def rounds_dir(project_id: str) -> Path:
    return project_dir(project_id) / "memory" / "rounds"


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
    return "\n".join(f"- {item}" for item in cleaned)


def parse_bullet_list(text: str) -> list[str]:
    items: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("- "):
            items.append(line[2:].strip())
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
    now = timestamp_now().isoformat(timespec="seconds")
    created_value = created_at or now
    evidence_refs = evidence_refs or []
    tags = tags or ["round", "control-plane"]
    normalized_title = normalize_scalar_metadata(title)
    normalized_confidence = normalize_scalar_metadata(confidence) or "high"
    normalized_phase = normalize_scalar_metadata(phase) or "execution"
    lines = [
        "---",
        f"id: {round_id}",
        "type: round-contract",
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
            f"objective_id: {objective_id}",
            f"phase: {normalized_phase}",
            "supersedes: []",
            "superseded_by: []",
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


def locate_round_file(project_id: str, round_id: str) -> Path | None:
    directory = rounds_dir(project_id)
    if not directory.exists():
        return None
    for path in sorted(directory.glob("*.md")):
        values = extract_frontmatter_scalars(read_text(path), ["id"])
        if values.get("id") == round_id:
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
