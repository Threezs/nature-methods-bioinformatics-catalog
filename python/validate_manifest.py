#!/usr/bin/env python3
"""Dependency-light checks used by CI and before replacing mock data."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def reject_literal_backslash_newline(paths: list[Path]) -> None:
    for path in paths:
        if path.exists() and "\\n" in path.read_text(encoding="utf-8"):
            raise SystemExit(f"literal backslash-n found in {path}")


def main() -> None:
    rows = read_csv(ROOT / "catalog.csv")
    required = {
        "id", "title", "year", "journal", "doi", "scope", "language", "official_repo",
        "input", "output", "turnkey_entrypoint",
        "readiness", "execution_mode", "validation_status", "mock_input",
    }
    if not rows or not required.issubset(rows[0]):
        raise SystemExit("catalog.csv is missing required columns")
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate method id")
    for row in rows:
        if not row["title"] or not row["scope"] or not row["input"] or not row["output"]:
            raise SystemExit(f"catalog row has an empty contract field: {row['id']}")
        if not row["official_repo"].startswith(("https://", "http://")):
            raise SystemExit(f"official_repo is not a URL: {row['id']}")
        if row["execution_mode"] not in {
            "baseline-function", "runtime-required", "manifest-only",
            "package+reference-required", "package+transcript-inputs-required",
        }:
            raise SystemExit(f"unknown execution_mode: {row['id']} -> {row['execution_mode']}")
        entry = ROOT / row["turnkey_entrypoint"]
        if not entry.exists():
            raise SystemExit(f"missing entrypoint: {entry}")
    utility_rows = read_csv(ROOT / "data/utility_templates.csv")
    utility_required = {"id", "entrypoint", "language", "readiness"}
    if not utility_rows or not utility_required.issubset(utility_rows[0]):
        raise SystemExit("utility_templates.csv is missing required columns")
    for row in utility_rows:
        if not (ROOT / row["entrypoint"]).exists():
            raise SystemExit(f"missing utility entrypoint: {row['entrypoint']}")
    function_rows = read_csv(ROOT / "data/function_index.csv")
    known_ids = set(ids) | {row["id"] for row in utility_rows}
    function_ids = {row["method_id"] for row in function_rows}
    missing_function_rows = set(ids) - function_ids
    if missing_function_rows:
        raise SystemExit(f"paper method missing from function_index.csv: {sorted(missing_function_rows)}")
    for row in function_rows:
        if row["method_id"] not in known_ids:
            raise SystemExit(f"unknown method in function_index.csv: {row['method_id']}")
    decision_rows = read_csv(ROOT / "data/method_decision_matrix.csv")
    decision_required = {"method_id", "question", "experimental_unit", "baseline", "compute_profile", "minimum_evidence", "not_for"}
    if not decision_rows or not decision_required.issubset(decision_rows[0]):
        raise SystemExit("method_decision_matrix.csv is missing required columns")
    decision_ids = {row["method_id"] for row in decision_rows}
    missing_decision_rows = set(ids) - decision_ids
    if missing_decision_rows:
        raise SystemExit(f"paper method missing from method_decision_matrix.csv: {sorted(missing_decision_rows)}")
    for row in decision_rows:
        if row["method_id"] not in set(ids):
            raise SystemExit(f"unknown method in decision matrix: {row['method_id']}")
    taxonomy_text = (ROOT / "config/function_taxonomy.yml").read_text(encoding="utf-8")
    taxonomy_ids = set(re.findall(r"[A-Z][A-Z0-9_]+_20[0-9]{2}|UTILITY_[A-Z0-9_]+", taxonomy_text))
    unknown_taxonomy_ids = taxonomy_ids - known_ids
    if unknown_taxonomy_ids:
        raise SystemExit(f"unknown method in function taxonomy: {sorted(unknown_taxonomy_ids)}")
    reject_literal_backslash_newline([
        ROOT / "README.md",
        ROOT / "catalog.csv",
        ROOT / "data/function_index.csv",
        ROOT / "data/utility_templates.csv",
        ROOT / "data/method_decision_matrix.csv",
        ROOT / "config/methods.yml",
    ])
    print(f"OK: {len(rows)} paper methods, {len(utility_rows)} utility templates, function index, taxonomy, and decision matrix are valid")


if __name__ == "__main__":
    main()
