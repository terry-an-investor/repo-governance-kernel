#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE_FIXTURE_ROOT = ROOT / "artifacts" / "fixtures" / "bootstrap-host"
INSTALLED_FIXTURE_ROOT = ROOT / "artifacts" / "fixtures" / "bootstrap-host-installed"
INSTALL_ROOT = ROOT / "artifacts" / "fixtures" / "bootstrap-package-install"
SOURCE_PROJECT_ID = "bootstrap-host"
INSTALLED_PROJECT_ID = "bootstrap-host-installed"
GIT_EXE = "C:\\Program Files\\Git\\cmd\\git.exe"


def run(cmd: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(
            json.dumps(
                {
                    "cmd": cmd,
                    "cwd": str(cwd),
                    "returncode": completed.returncode,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                },
                ensure_ascii=True,
                indent=2,
            )
    )
    return completed


def project_version() -> str:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return str(pyproject["project"]["version"]).strip()


def ensure_clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def init_git_repo(path: Path) -> None:
    run([GIT_EXE, "init"], cwd=path)
    run([GIT_EXE, "config", "user.email", "fixture@example.com"], cwd=path)
    run([GIT_EXE, "config", "user.name", "Fixture Smoke"], cwd=path)


def assert_bootstrap_host(fixture_root: Path, project_id: str, *, bootstrap_payload: dict[str, object]) -> dict[str, object]:
    expected_paths = [
        fixture_root / ".githooks" / "pre-commit",
        fixture_root / ".githooks" / "pre-push",
        fixture_root / "projects" / project_id / "control" / "constitution.md",
        fixture_root / "projects" / project_id / "current" / "current-task.md",
        fixture_root / "projects" / project_id / "control" / "pivot-log.md",
        fixture_root / "projects" / project_id / "control" / "exception-ledger.md",
    ]
    missing = [str(path) for path in expected_paths if not path.exists()]
    if missing:
        raise SystemExit(f"bootstrap did not create expected paths: {', '.join(missing)}")

    hooks_path = run(
        [GIT_EXE, "config", "--get", "core.hooksPath"],
        cwd=fixture_root,
    ).stdout.strip().replace("\\", "/")
    expected_hooks_path = str(fixture_root / ".githooks").replace("\\", "/")
    if hooks_path != expected_hooks_path:
        raise SystemExit(f"unexpected hooksPath `{hooks_path}`; expected `{expected_hooks_path}`")

    constitution_text = (fixture_root / "projects" / project_id / "control" / "constitution.md").read_text(
        encoding="utf-8"
    )
    if "Audit Hooks" not in constitution_text:
        raise SystemExit("bootstrap constitution is missing audit hooks")

    return {
        "bootstrap": bootstrap_payload,
        "hooks_path": hooks_path,
    }


def bootstrap_and_audit(*, fixture_root: Path, project_id: str, python_executable: str) -> dict[str, object]:
    ensure_clean_dir(fixture_root)
    init_git_repo(fixture_root)

    bootstrap = run(
        [
            python_executable,
            "-m",
            "kernel.cli",
            "--repo-root",
            str(fixture_root),
            "bootstrap-repo",
            "--project-id",
            project_id,
        ],
        cwd=ROOT,
    )
    bootstrap_payload = json.loads(bootstrap.stdout)
    bootstrap_checks = assert_bootstrap_host(fixture_root, project_id, bootstrap_payload=bootstrap_payload)

    audit = run(
        [
            python_executable,
            "-m",
            "kernel.cli",
            "--repo-root",
            str(fixture_root),
            "audit-control-state",
            "--project-id",
            project_id,
        ],
        cwd=ROOT,
    )
    audit_payload = json.loads(audit.stdout)
    if audit_payload.get("status") == "blocked":
        raise SystemExit(
            json.dumps(
                {
                    "message": "bootstrap host audit is still blocked after bootstrap",
                    "audit": audit_payload,
                },
                ensure_ascii=True,
                indent=2,
            )
        )

    return {
        "project_id": project_id,
        "fixture_root": str(fixture_root),
        "bootstrap": bootstrap_checks["bootstrap"],
        "audit": audit_payload,
        "hooks_path": bootstrap_checks["hooks_path"],
    }


def prepare_installed_python() -> tuple[str, str]:
    ensure_clean_dir(INSTALL_ROOT)
    venv_root = INSTALL_ROOT / ".venv"
    run(["uv", "venv", str(venv_root)], cwd=ROOT)
    installed_python = venv_root / "Scripts" / "python.exe"
    if not installed_python.exists():
        raise SystemExit(f"expected installed python not found: {installed_python}")

    run(["uv", "build"], cwd=ROOT)
    version = project_version()
    wheel_path = ROOT / "dist" / f"repo_governance_kernel-{version}-py3-none-any.whl"
    if not wheel_path.exists():
        raise SystemExit(f"expected built wheel not found: {wheel_path}")

    run(
        [
            "uv",
            "pip",
            "install",
            "--python",
            str(installed_python),
            "--force-reinstall",
            str(wheel_path),
        ],
        cwd=ROOT,
    )
    help_output = run([str(installed_python), "-m", "kernel.cli", "--help"], cwd=ROOT)
    return str(installed_python), help_output.stdout


def main() -> int:
    source_host = bootstrap_and_audit(
        fixture_root=SOURCE_FIXTURE_ROOT,
        project_id=SOURCE_PROJECT_ID,
        python_executable=sys.executable,
    )
    installed_python, installed_help = prepare_installed_python()
    installed_host = bootstrap_and_audit(
        fixture_root=INSTALLED_FIXTURE_ROOT,
        project_id=INSTALLED_PROJECT_ID,
        python_executable=installed_python,
    )

    print(
        json.dumps(
            {
                "status": "ok",
                "version": project_version(),
                "source_bootstrap": source_host,
                "installed_bootstrap": installed_host,
                "installed_help_contains_bootstrap_repo": "bootstrap-repo" in installed_help,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
