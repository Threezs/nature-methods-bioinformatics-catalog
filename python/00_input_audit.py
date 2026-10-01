#!/usr/bin/env python3
"""Create a dependency-light audit manifest before method-specific analysis."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def audit_path(input_path: Path) -> dict:
    if not input_path.exists():
        raise FileNotFoundError(input_path)
    result = {
        "input": str(input_path),
        "suffix": input_path.suffix.lower(),
        "bytes": input_path.stat().st_size,
        "exists": True,
        "next_checks": [
            "confirm observation unit and feature identifiers",
            "record species, genome build, annotation release, and batch",
            "confirm biological replicates and condition labels",
        ],
    }
    if input_path.suffix.lower() in {".csv", ".tsv"}:
        delimiter = "\t" if input_path.suffix.lower() == ".tsv" else ","
        with input_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle, delimiter=delimiter)
            header = next(reader, [])
            result["header_columns"] = len(header)
            result["header_preview"] = header[:10]
            result["data_rows_sampled"] = sum(1 for _ in zip(range(100), reader))
    elif input_path.suffix.lower() == ".h5ad":
        result["note"] = "AnnData structure will be checked by scanpy in the method-specific environment"
    else:
        result["note"] = "file exists; assay-specific parser is required"
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Write a reproducible input audit manifest")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("results/input_audit.json"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit_path(args.input), indent=2) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
