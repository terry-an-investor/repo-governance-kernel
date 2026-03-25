#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
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
                    "status": "error",
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


def git_head(cwd: Path) -> str:
    return run([GIT_EXE, "rev-parse", "HEAD"], cwd=cwd).stdout.strip()


def ls_remote_map(remote: str, refs: list[str]) -> dict[str, str]:
    completed = run([GIT_EXE, "ls-remote", remote, *refs], cwd=ROOT)
    resolved: dict[str, str] = {}
    for line in completed.stdout.splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        sha, ref = cleaned.split("\t", 1)
        resolved[ref.strip()] = sha.strip()
    return resolved


def release_json(repo: str, tag: str) -> dict[str, object]:
    completed = run(
        [
            "gh",
            "release",
            "view",
            tag,
            "--repo",
            repo,
            "--json",
            "tagName,name,isDraft,isPrerelease,url,targetCommitish,assets",
        ],
        cwd=ROOT,
    )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"gh release view returned invalid json: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit("gh release view returned non-object json")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify that one version is really published on origin as branch push, tag, and GitHub Release."
    )
    parser.add_argument("--repo", required=True, help="GitHub repo in owner/name form.")
    parser.add_argument("--version", required=True, help="Version string such as 0.1.0a4.")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--branch", default="master")
    parser.add_argument(
        "--expected-sha",
        default="",
        help="Expected release commit SHA. Defaults to local HEAD.",
    )
    parser.add_argument(
        "--require-branch-head",
        action="store_true",
        help="Require the remote branch head to equal the expected release commit. Use during the release cut before later commits advance the branch.",
    )
    parser.add_argument(
        "--asset",
        action="append",
        default=[],
        help="Expected release asset filename. Repeat for each expected asset.",
    )
    parsed = parser.parse_args()

    expected_sha = parsed.expected_sha.strip() or git_head(ROOT)
    version = parsed.version.strip()
    tag = f"v{version}"
    branch_ref = f"refs/heads/{parsed.branch.strip()}"
    tag_ref = f"refs/tags/{tag}"
    deref_ref = f"{tag_ref}^{{}}"

    remote_refs = ls_remote_map(parsed.remote.strip(), [branch_ref, tag_ref, deref_ref])
    branch_sha = remote_refs.get(branch_ref, "")
    tag_object_sha = remote_refs.get(tag_ref, "")
    tag_commit_sha = remote_refs.get(deref_ref, "")

    if not branch_sha:
        raise SystemExit(f"remote branch ref missing: {branch_ref}")
    if not tag_object_sha:
        raise SystemExit(f"remote tag ref missing: {tag_ref}")
    if not tag_commit_sha:
        raise SystemExit(f"remote dereferenced tag ref missing: {deref_ref}")
    if parsed.require_branch_head and branch_sha != expected_sha:
        raise SystemExit(
            f"remote branch head mismatch: expected {expected_sha}, observed {branch_sha}"
        )
    if tag_commit_sha != expected_sha:
        raise SystemExit(
            f"remote release tag commit mismatch: expected {expected_sha}, observed {tag_commit_sha}"
        )

    release_payload = release_json(parsed.repo.strip(), tag)
    observed_tag = str(release_payload.get("tagName") or "").strip()
    if observed_tag != tag:
        raise SystemExit(f"GitHub Release tag mismatch: expected {tag}, observed {observed_tag}")
    if bool(release_payload.get("isDraft")):
        raise SystemExit(f"GitHub Release {tag} is still draft")
    if bool(release_payload.get("isPrerelease")):
        raise SystemExit(f"GitHub Release {tag} is marked prerelease")

    assets = release_payload.get("assets")
    if not isinstance(assets, list):
        raise SystemExit("GitHub Release assets payload missing or invalid")
    observed_assets = sorted(
        str(item.get("name") or "").strip()
        for item in assets
        if isinstance(item, dict) and str(item.get("name") or "").strip()
    )
    expected_assets = sorted(str(item).strip() for item in parsed.asset if str(item).strip())
    missing_assets = [item for item in expected_assets if item not in observed_assets]
    if missing_assets:
        raise SystemExit(f"GitHub Release missing expected assets: {', '.join(missing_assets)}")

    result = {
        "status": "ok",
        "repo": parsed.repo.strip(),
        "version": version,
        "tag": tag,
        "expected_sha": expected_sha,
        "remote_branch": {
            "name": branch_ref,
            "sha": branch_sha,
        },
        "remote_tag": {
            "name": tag_ref,
            "object_sha": tag_object_sha,
            "commit_sha": tag_commit_sha,
        },
        "github_release": {
            "name": release_payload.get("name"),
            "tag": observed_tag,
            "url": release_payload.get("url"),
            "target_commitish": release_payload.get("targetCommitish"),
            "asset_names": observed_assets,
        },
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
