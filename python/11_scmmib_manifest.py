#!/usr/bin/env python3
"""Prepare an auditable SCMMIB benchmark manifest.

SCMMIB is a benchmark/evaluation resource rather than one integration model.
The manifest records the task and dataset description before the official
benchmark pipeline is run.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a SCMMIB benchmark manifest")
    parser.add_argument("--dataset-manifest", required=True, help="CSV/JSON/YAML description of datasets and modalities")
    parser.add_argument("--task", choices=("paired", "unpaired", "mosaic"), required=True)
    parser.add_argument("--output", default="scmmib_manifest.json")
    args = parser.parse_args()

    dataset_manifest = Path(args.dataset_manifest)
    if not dataset_manifest.exists():
        parser.error(f"missing dataset manifest: {dataset_manifest}")

    manifest = {
        "method": "SCMMIB",
        "paper_doi": "10.1038/s41592-025-02737-9",
        "official_repo": "https://github.com/bm2-lab/SCMMI_Benchmark",
        "pipeline_repo": "https://github.com/bm2-lab/SCMMIB_pipeline",
        "dataset_manifest": str(dataset_manifest),
        "task": args.task,
        "execution_mode": "manifest-only; run the pinned official benchmark pipeline next",
        "metrics_to_record": ["accuracy", "robustness", "scalability"],
        "interpretation_note": "benchmark rankings are task- and modality-specific; they do not identify a universally best integrator",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
