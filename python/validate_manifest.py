#!/usr/bin/env python3
"""Dependency-light checks used by CI and before replacing mock data."""
from __future__ import annotations

import csv
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
        "id", "title", "year", "doi", "scope", "language", "turnkey_entrypoint",
        "readiness", "execution_mode", "validation_status", "mock_input",
    }
    if not rows or not required.issubset(rows[0]):
        raise SystemExit("catalog.csv is missing required columns")
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate method id")
    for row in rows:
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
    for row in function_rows:
        if row["method_id"] not in known_ids:
            raise SystemExit(f"unknown method in function_index.csv: {row['method_id']}")
    reject_literal_backslash_newline([
        ROOT / "README.md",
        ROOT / "catalog.csv",
        ROOT / "data/function_index.csv",
        ROOT / "data/utility_templates.csv",
        ROOT / "config/methods.yml",
    ])
    print(f"OK: {len(rows)} paper methods, {len(utility_rows)} utility templates, and function index are valid")


if __name__ == "__main__":
    main()
