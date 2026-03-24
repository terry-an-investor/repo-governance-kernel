#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from product_semantics import (
    CANONICAL_PRODUCT_DOCS,
    PRODUCT_DOC_PATH,
    REQUIRED_PRODUCT_META_KEYS,
    REQUIRED_PRODUCT_SECTIONS,
    load_product_doc,
    normalize_phrase,
    product_autonomy_boundary,
    product_automation_scope,
    product_positioning_phrase,
    require_product_meta,
)


def add_issue(
    issues: list[dict[str, object]],
    *,
    severity: str,
    code: str,
    message: str,
    evidence: list[str] | None = None,
) -> None:
    issues.append(
        {
            "severity": severity,
            "code": code,
            "message": message,
            "evidence": evidence or [],
        }
    )


def file_contains_phrase(path: Path, phrase: str) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return normalize_phrase(phrase) in normalize_phrase(text)


def audit_product_docs() -> dict[str, object]:
    issues: list[dict[str, object]] = []
    checks: list[str] = []

    meta, sections = load_product_doc()
    for key in REQUIRED_PRODUCT_META_KEYS:
        try:
            require_product_meta(meta, key)
        except SystemExit as exc:
            add_issue(
                issues,
                severity="error",
                code="missing_product_frontmatter_key",
                message=str(exc),
                evidence=[key],
            )
    checks.append("product doc frontmatter contract")

    missing_sections = [section for section in REQUIRED_PRODUCT_SECTIONS if section not in sections]
    if missing_sections:
        add_issue(
            issues,
            severity="error",
            code="missing_product_sections",
            message="PRODUCT.md is missing required canonical sections",
            evidence=missing_sections,
        )
    checks.append("product doc section contract")

    missing_doc_references: list[str] = []
    for path in CANONICAL_PRODUCT_DOCS:
        if not file_contains_phrase(path, "PRODUCT.md"):
            missing_doc_references.append(path.name)
    if missing_doc_references:
        add_issue(
            issues,
            severity="warning",
            code="canonical_docs_missing_product_reference",
            message="canonical docs should explicitly reference PRODUCT.md as the product truth source",
            evidence=missing_doc_references,
        )
    checks.append("canonical docs reference product doc")

    positioning_phrase = product_positioning_phrase()
    positioning_missing = [
        path.name
        for path in (
            Path("ARCHITECTURE.md"),
            Path("CONTROL_SYSTEM.md"),
            Path("DESIGN_PRINCIPLES.md"),
            Path("IMPLEMENTATION_PLAN.md"),
        )
        if not file_contains_phrase(PRODUCT_DOC_PATH.parent / path, positioning_phrase)
    ]
    if positioning_missing:
        add_issue(
            issues,
            severity="warning",
            code="canonical_docs_missing_positioning_phrase",
            message="major canonical docs should restate the canonical product positioning phrase from PRODUCT.md",
            evidence=positioning_missing,
        )
    checks.append("canonical docs share product positioning phrase")

    automation_scope = product_automation_scope()
    automation_docs_missing = [
        path.name
        for path in (
            Path("CONTROL_SYSTEM.md"),
            Path("STATE_MACHINE.md"),
            Path("TRANSITION_COMMANDS.md"),
        )
        if not file_contains_phrase(PRODUCT_DOC_PATH.parent / path, automation_scope)
    ]
    if automation_docs_missing:
        add_issue(
            issues,
            severity="warning",
            code="machine_semantic_docs_missing_automation_scope",
            message="machine-semantic docs should restate the automation scope declared in PRODUCT.md",
            evidence=automation_docs_missing,
        )
    checks.append("machine-semantic docs share automation scope")

    autonomy_boundary = product_autonomy_boundary()
    autonomy_docs_missing = [
        path.name
        for path in (
            Path("CONTROL_SYSTEM.md"),
            Path("STATE_MACHINE.md"),
            Path("TRANSITION_COMMANDS.md"),
        )
        if not file_contains_phrase(PRODUCT_DOC_PATH.parent / path, autonomy_boundary)
    ]
    if autonomy_docs_missing:
        add_issue(
            issues,
            severity="warning",
            code="machine_semantic_docs_missing_autonomy_boundary",
            message="machine-semantic docs should restate the autonomy boundary declared in PRODUCT.md",
            evidence=autonomy_docs_missing,
        )
    checks.append("machine-semantic docs share autonomy boundary")

    error_count = sum(1 for issue in issues if issue["severity"] == "error")
    warning_count = sum(1 for issue in issues if issue["severity"] == "warning")
    status = "blocked" if error_count else ("warn" if warning_count else "ok")
    return {
        "status": status,
        "summary": {
            "errors": error_count,
            "warnings": warning_count,
            "checks": checks,
        },
        "issues": issues,
    }


def main() -> int:
    result = audit_product_docs()
    print(json.dumps(result, ensure_ascii=True, indent=2))
    if int(result["summary"]["errors"]) or int(result["summary"]["warnings"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
