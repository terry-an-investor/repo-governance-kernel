from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Mapping

from kernel.runtime_paths import REPO_ROOT_ENV_VAR, resolve_package_root


PROJECT_ID_ENV_VAR = "REPO_GOVERNANCE_PROJECT"
CONFIG_RESOLUTION_ENV_VAR = "REPO_GOVERNANCE_CONFIG_RESOLUTION"
CONFIG_DIRNAME = ".repo-governance-kernel"
USER_CONFIG_FILENAME = "config.json"
PROJECT_CONFIG_FILENAME = "project.json"
LOCAL_OVERRIDE_FILENAME = "local.json"


def _normalize_text(value: object) -> str:
    return str(value or "").strip()


def _runtime_env(env: Mapping[str, str] | None = None) -> Mapping[str, str]:
    return env if env is not None else os.environ


def resolve_user_home(env: Mapping[str, str] | None = None) -> Path:
    runtime_env = _runtime_env(env)
    candidate = _normalize_text(runtime_env.get("USERPROFILE")) or _normalize_text(runtime_env.get("HOME"))
    if candidate:
        return Path(candidate).expanduser().resolve()
    return Path.home().resolve()


def user_config_path(env: Mapping[str, str] | None = None) -> Path:
    return resolve_user_home(env) / CONFIG_DIRNAME / USER_CONFIG_FILENAME


def project_config_path(repo_root: Path) -> Path:
    return repo_root / CONFIG_DIRNAME / PROJECT_CONFIG_FILENAME


def local_override_path(repo_root: Path) -> Path:
    return repo_root / CONFIG_DIRNAME / LOCAL_OVERRIDE_FILENAME


def _load_json_config(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid config json: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"config file must contain one json object: {path}")
    normalized: dict[str, str] = {}
    for key, value in payload.items():
        normalized_key = _normalize_text(key)
        if not normalized_key:
            continue
        normalized_value = _normalize_text(value)
        if normalized_value:
            normalized[normalized_key] = normalized_value
    return normalized


def _discover_repo_root(cwd: Path) -> Path | None:
    current = cwd.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() or (candidate / "state").exists():
            return candidate
    return None


def _normalize_repo_root(value: str) -> str:
    if not value:
        return ""
    return str(Path(value).expanduser().resolve())


def resolve_runtime_config(
    *,
    explicit_repo_root: str = "",
    explicit_project_id: str = "",
    cwd: Path | None = None,
    env: Mapping[str, str] | None = None,
) -> dict[str, object]:
    runtime_env = _runtime_env(env)
    cwd_path = (cwd or Path.cwd()).resolve()

    user_path = user_config_path(runtime_env)
    user_config = _load_json_config(user_path)

    discovered_repo_root = _discover_repo_root(cwd_path)
    repo_root_resolution = {
        "flag": _normalize_repo_root(explicit_repo_root),
        "environment": _normalize_repo_root(runtime_env.get(REPO_ROOT_ENV_VAR, "")),
        "cwd_discovery": _normalize_repo_root(discovered_repo_root or ""),
        "user_config": _normalize_repo_root(user_config.get("repo_root", "")),
        "package_default": str(resolve_package_root()),
    }

    repo_root_value = ""
    repo_root_source = ""
    for source_name in ("flag", "environment", "cwd_discovery", "user_config", "package_default"):
        candidate = _normalize_text(repo_root_resolution[source_name])
        if not candidate:
            continue
        repo_root_value = candidate
        repo_root_source = source_name
        break

    repo_root_path = Path(repo_root_value).resolve()
    project_path = project_config_path(repo_root_path)
    local_path = local_override_path(repo_root_path)
    project_config = _load_json_config(project_path)
    local_override = _load_json_config(local_path)

    project_id_resolution = {
        "flag": _normalize_text(explicit_project_id),
        "environment": _normalize_text(runtime_env.get(PROJECT_ID_ENV_VAR, "")),
        "local_override": _normalize_text(local_override.get("project_id", "")),
        "project_config": _normalize_text(project_config.get("project_id", "")),
        "user_config": _normalize_text(user_config.get("project_id", "")),
        "unset": "",
    }

    project_id_value = ""
    project_id_source = "unset"
    for source_name in ("flag", "environment", "local_override", "project_config", "user_config"):
        candidate = project_id_resolution[source_name]
        if not candidate:
            continue
        project_id_value = candidate
        project_id_source = source_name
        break

    return {
        "status": "ok",
        "config_contract": {
            "scope": "repo-governance-kernel repo_root/project_id runtime resolution",
            "repo_root_precedence": [
                "flag",
                "environment",
                "cwd_discovery",
                "user_config",
                "package_default",
            ],
            "project_id_precedence": [
                "flag",
                "environment",
                "local_override",
                "project_config",
                "user_config",
                "unset",
            ],
            "env_vars": {
                "repo_root": REPO_ROOT_ENV_VAR,
                "project_id": PROJECT_ID_ENV_VAR,
            },
            "config_paths": {
                "user_config": str(user_path),
                "project_config": str(project_path),
                "local_override": str(local_path),
            },
            "notes": [
                "project and local config files are loaded only after repo_root is resolved",
                "project/local config currently resolve project_id, not repo_root",
            ],
        },
        "resolved": {
            "repo_root": str(repo_root_path),
            "project_id": project_id_value,
        },
        "sources": {
            "repo_root": repo_root_source,
            "project_id": project_id_source,
        },
        "layers": {
            "user_config": user_config,
            "project_config": project_config,
            "local_override": local_override,
        },
        "candidates": {
            "repo_root": repo_root_resolution,
            "project_id": project_id_resolution,
        },
    }
