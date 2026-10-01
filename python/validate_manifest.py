#!/usr/bin/env python3
"""Dependency-light checks used by CI and before replacing mock data."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    rows = list(csv.DictReader((ROOT / "catalog.csv").open(newline="")))
    required = {"id", "title", "year", "doi", "scope", "language", "turnkey_entrypoint"}
    if not rows or not required.issubset(rows[0]):
        raise SystemExit("catalog.csv is missing required columns")
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate method id")
    for row in rows:
        entry = ROOT / row["turnkey_entrypoint"]
        if not entry.exists():
            raise SystemExit(f"missing entrypoint: {entry}")
    print(f"OK: {len(rows)} methods and all entrypoints are present")


if __name__ == "__main__":
    main()
