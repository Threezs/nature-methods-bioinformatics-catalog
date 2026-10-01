#!/usr/bin/env python3
"""Prepare an auditable scikit-bio general omics-tool manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a scikit-bio sequence/table analysis manifest"
    )
    parser.add_argument(
        "--inputs",
        nargs="+",
        required=True,
        help="sequence, feature-table, taxonomy, metadata, distance or tree paths",
    )
    parser.add_argument(
        "--operation",
        choices=("sequence", "table", "distance", "diversity", "taxonomy", "phylogeny"),
        required=True,
        help="planned scikit-bio operation family",
    )
    parser.add_argument("--format", dest="input_format", help="input format to pin (FASTQ, BIOM, TSV, Newick, etc.)")
    parser.add_argument("--output", default="scikit_bio_manifest.json")
    args = parser.parse_args()

    inputs = [Path(item) for item in args.inputs]
    missing = [str(path) for path in inputs if not path.exists()]
    if missing:
        parser.error("missing scikit-bio inputs: " + ", ".join(missing))

    manifest = {
        "method": "scikit-bio",
        "paper_doi": "10.1038/s41592-025-02981-z",
        "official_repo": "https://github.com/scikit-bio/scikit-bio",
        "inputs": [str(path) for path in inputs],
        "operation": args.operation,
        "input_format": args.input_format,
        "execution_mode": "manifest-only; install a pinned scikit-bio environment and validate identifiers, metadata and assay-specific assumptions before analysis",
        "outputs_expected": [
            "format-aware biological data objects",
            "sequence, distance, diversity, taxonomy or phylogeny outputs for the selected operation",
            "software/version/input-format record suitable for reproducible downstream analysis",
        ],
        "interpretation_note": "a general-purpose library provides algorithms and data structures; it does not choose an experimental design or make biological claims by itself",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
