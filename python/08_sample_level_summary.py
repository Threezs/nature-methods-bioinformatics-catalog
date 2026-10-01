#!/usr/bin/env python3
"""Summarize cell-level scores by sample/donor without requiring pandas."""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def normalize_cell_column(fieldnames: list[str], requested: str) -> str:
    if requested in fieldnames:
        return requested
    if fieldnames and fieldnames[0] in {"", "index", "Unnamed: 0"}:
        return fieldnames[0]
    raise ValueError(f"cell ID column {requested!r} is missing")


def summarize(scores_path: Path, metadata_path: Path, output_path: Path,
              cell_id: str, sample_id: str, condition: str) -> None:
    score_fields, score_rows = read_rows(scores_path)
    meta_fields, meta_rows = read_rows(metadata_path)
    score_cell = normalize_cell_column(score_fields, cell_id)
    meta_cell = normalize_cell_column(meta_fields, cell_id)
    for field in (sample_id, condition):
        if field not in meta_fields:
            raise ValueError(f"metadata column {field!r} is missing")
    score_columns = [f for f in score_fields if f not in {score_cell, ""}]
    numeric_columns = []
    for field in score_columns:
        try:
            float(next((r[field] for r in score_rows if r[field] != ""), ""))
        except ValueError:
            continue
        numeric_columns.append(field)
    if not numeric_columns:
        raise ValueError("scores file has no numeric score columns")
    metadata_by_cell = {row[meta_cell]: row for row in meta_rows}
    grouped: dict[tuple[str, str], dict[str, list[float]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for row in score_rows:
        cell = row[score_cell]
        if cell not in metadata_by_cell:
            continue
        meta = metadata_by_cell[cell]
        key = (meta[sample_id], meta[condition])
        for field in numeric_columns:
            if row[field] != "":
                grouped[key][field].append(float(row[field]))
    if not grouped:
        raise ValueError("no cell IDs matched between scores and metadata")
    output_fields = [sample_id, condition, "n_cells_used"] + numeric_columns
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fields)
        writer.writeheader()
        for (sample, cond), values in sorted(grouped.items()):
            row = {sample_id: sample, condition: cond}
            row["n_cells_used"] = max((len(v) for v in values.values()), default=0)
            for field in numeric_columns:
                numbers = values[field]
                row[field] = sum(numbers) / len(numbers) if numbers else ""
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate cell scores to sample level")
    parser.add_argument("--scores", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("results/sample_level_summary.csv"))
    parser.add_argument("--cell-id", default="cell_id")
    parser.add_argument("--sample-id", default="sample_id")
    parser.add_argument("--condition", default="condition")
    args = parser.parse_args()
    summarize(args.scores, args.metadata, args.output, args.cell_id, args.sample_id, args.condition)
    print(args.output)


if __name__ == "__main__":
    main()
