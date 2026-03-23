#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


@dataclass(frozen=True)
class SmokeSpec:
    name: str
    script_name: str
    fixture_project_ids: tuple[str, ...]
    parallel_safe: bool
    shared_resources: tuple[str, ...]
    description: str

    @property
    def script_path(self) -> Path:
        return SCRIPTS / self.script_name

    @property
    def fixture_paths(self) -> tuple[Path, ...]:
        return tuple(ROOT / "projects" / project_id for project_id in self.fixture_project_ids)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["script_path"] = str(self.script_path)
        payload["fixture_paths"] = [str(path) for path in self.fixture_paths]
        return payload


SMOKE_SPECS: tuple[SmokeSpec, ...] = (
    SmokeSpec(
        name="adjudication_followups",
        script_name="smoke_adjudication_followups.py",
        fixture_project_ids=("__adjudication_followups_smoke__", "__adjudication_phase_bundle_smoke__"),
        parallel_safe=False,
        shared_resources=("repo_worktree_fixture_projects",),
        description="Validate bounded adjudication follow-up execution across round, exception-contract, and phase-bootstrap bundles.",
    ),
    SmokeSpec(
        name="exception_contracts",
        script_name="smoke_exception_contracts.py",
        fixture_project_ids=("__exception_contract_smoke__",),
        parallel_safe=False,
        shared_resources=("repo_worktree_fixture_projects",),
        description="Validate activate, retire, and invalidate exception-contract transitions on a disposable fixture project.",
    ),
    SmokeSpec(
        name="guarded_exception_enforcement",
        script_name="smoke_guarded_exception_enforcement.py",
        fixture_project_ids=("__guarded_exception_enforcement_smoke__",),
        parallel_safe=False,
        shared_resources=("repo_worktree_fixture_projects",),
        description="Validate guarded exception-path enforcement on a disposable fixture project.",
    ),
    SmokeSpec(
        name="objective_line",
        script_name="smoke_objective_line.py",
        fixture_project_ids=("__objective_line_smoke__",),
        parallel_safe=False,
        shared_resources=("repo_worktree_fixture_projects",),
        description="Validate soft-pivot and close-objective behavior on a disposable fixture project.",
    ),
    SmokeSpec(
        name="phase_scope_controls",
        script_name="smoke_phase_scope_controls.py",
        fixture_project_ids=("__phase_scope_control_smoke__",),
        parallel_safe=False,
        shared_resources=("repo_worktree_fixture_projects",),
        description="Validate explicit phase transitions and round-scope refresh on a disposable fixture project.",
    ),
    SmokeSpec(
        name="transition_engine",
        script_name="smoke_transition_engine.py",
        fixture_project_ids=("__transition_engine_smoke__",),
        parallel_safe=False,
        shared_resources=("repo_worktree_fixture_projects",),
        description="Validate shared transition-engine behavior on a disposable fixture project.",
    ),
)


SMOKE_SPEC_BY_NAME = {spec.name: spec for spec in SMOKE_SPECS}


def validate_manifest() -> None:
    seen_names: set[str] = set()
    seen_fixture_ids: set[str] = set()
    for spec in SMOKE_SPECS:
        if spec.name in seen_names:
            raise SystemExit(f"duplicate smoke spec name `{spec.name}`")
        seen_names.add(spec.name)
        if not spec.script_path.exists():
            raise SystemExit(f"smoke script not found for `{spec.name}`: {spec.script_path}")
        for fixture_id in spec.fixture_project_ids:
            if fixture_id in seen_fixture_ids:
                raise SystemExit(f"duplicate smoke fixture project id `{fixture_id}` in manifest")
            seen_fixture_ids.add(fixture_id)


def select_smoke_specs(names: list[str] | None = None) -> list[SmokeSpec]:
    validate_manifest()
    if not names:
        return list(SMOKE_SPECS)
    selected: list[SmokeSpec] = []
    for name in names:
        normalized = name.strip()
        if not normalized:
            continue
        spec = SMOKE_SPEC_BY_NAME.get(normalized)
        if spec is None:
            raise SystemExit(f"unknown smoke `{normalized}`; available smokes: {', '.join(sorted(SMOKE_SPEC_BY_NAME))}")
        selected.append(spec)
    return selected
