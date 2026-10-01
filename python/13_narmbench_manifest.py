#!/usr/bin/env python3
"""Prepare an auditable NaRMBench nanopore RNA-modification manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a NaRMBench RNA-modification benchmark manifest")
    parser.add_argument("--reads", nargs="+", required=True, help="FASTQ/FAST5/POD5-derived input files")
    parser.add_argument("--reference", required=True, help="reference transcriptome/genome used by the benchmark")
    parser.add_argument("--chemistry", choices=("RNA002", "RNA004", "both"), default="both")
    parser.add_argument("--modifications", nargs="+", default=["m6A", "Psi", "m5C", "A-to-I", "m7G", "m1A"])
    parser.add_argument("--output", default="narmbench_manifest.json")
    args = parser.parse_args()

    reads = [Path(item) for item in args.reads]
    reference = Path(args.reference)
    missing = [str(path) for path in reads if not path.exists()]
    if not reference.exists():
        missing.append(str(reference))
    if missing:
        parser.error("missing NaRMBench inputs: " + ", ".join(missing))

    manifest = {
        "method": "NaRMBench",
        "paper_doi": "10.1038/s41592-025-02974-y",
        "official_repo": "https://github.com/JiejunShi/NaRMBench",
        "reads": [str(path) for path in reads],
        "reference": str(reference),
        "chemistry": args.chemistry,
        "modifications": args.modifications,
        "execution_mode": "manifest-only; run preprocessing, retraining and evaluation in the pinned official workflow",
        "outputs_expected": ["site-level detection metrics", "precision-recall", "quantification and biological-validity checks"],
        "interpretation_note": "modification calls are chemistry- and training-dependent; report calibration and biological validation",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
