#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

from kernel.assemble_context import clean_section_text, parse_h2_sections
from kernel.build_index import parse_frontmatter, split_frontmatter


ROOT = Path(__file__).resolve().parent.parent
PRODUCT_DOC_PATH = ROOT / "PRODUCT.md"
CANONICAL_PRODUCT_DOCS = (
    ROOT / "ARCHITECTURE.md",
    ROOT / "CONTROL_SYSTEM.md",
    ROOT / "DESIGN_PRINCIPLES.md",
    ROOT / "IMPLEMENTATION_PLAN.md",
    ROOT / "STATE_MACHINE.md",
    ROOT / "TRANSITION_COMMANDS.md",
)
REQUIRED_PRODUCT_META_KEYS = (
    "product_name",
    "product_category",
    "product_approach",
    "positioning_phrase",
    "automation_scope",
    "autonomy_boundary",
    "current_stage",
    "target_user_segments",
    "canonical_semantics_surfaces",
)
REQUIRED_PRODUCT_SECTIONS = (
    "Product Definition",
    "Target Users",
    "User Pain",
    "Product Promise",
    "Current Capabilities",
    "Product Boundaries",
    "Product To Semantics Path",
    "Current Stage",
    "Roadmap",
)


def normalize_phrase(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def load_product_doc() -> tuple[dict[str, object], dict[str, str]]:
    if not PRODUCT_DOC_PATH.exists():
        raise SystemExit(f"product doc not found: {PRODUCT_DOC_PATH}")
    text = PRODUCT_DOC_PATH.read_text(encoding="utf-8")
    frontmatter_text, _body = split_frontmatter(text)
    meta = parse_frontmatter(frontmatter_text)
    sections = parse_h2_sections(clean_section_text(PRODUCT_DOC_PATH, strip_heading=False, strip_yaml=True))
    return meta, sections


def require_product_meta(meta: dict[str, object], key: str) -> object:
    value = meta.get(key)
    if isinstance(value, list):
        if not value:
            raise SystemExit(f"PRODUCT.md is missing required frontmatter key `{key}`")
        return value
    if not str(value or "").strip():
        raise SystemExit(f"PRODUCT.md is missing required frontmatter key `{key}`")
    return value


def product_positioning_phrase() -> str:
    meta, _sections = load_product_doc()
    return str(require_product_meta(meta, "positioning_phrase")).strip()


def product_automation_scope() -> str:
    meta, _sections = load_product_doc()
    return str(require_product_meta(meta, "automation_scope")).strip()


def product_autonomy_boundary() -> str:
    meta, _sections = load_product_doc()
    return str(require_product_meta(meta, "autonomy_boundary")).strip()

