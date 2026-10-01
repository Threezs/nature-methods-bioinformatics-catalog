#!/usr/bin/env python3
"""Prepare a scMultiBench multi-task integration benchmark manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


TASKS = (
    "dimension_reduction",
    "batch_correction",
    "clustering",
    "classification",
    "imputation",
    "feature_selection",
    "spatial_registration",
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a scMultiBench benchmark manifest")
    parser.add_argument("--dataset-manifest", required=True, help="CSV/JSON/YAML dataset and modality description")
    parser.add_argument("--tasks", nargs="+", choices=TASKS, required=True)
    parser.add_argument("--output", default="scmultibench_manifest.json")
    args = parser.parse_args()

    dataset_manifest = Path(args.dataset_manifest)
    if not dataset_manifest.exists():
        parser.error(f"missing dataset manifest: {dataset_manifest}")
    manifest = {
        "method": "scMultiBench",
        "paper_doi": "10.1038/s41592-025-02856-3",
        "official_repo": "https://github.com/PYangLab/scMultiBench",
        "zenodo": "https://doi.org/10.5281/zenodo.15385334",
        "dataset_manifest": str(dataset_manifest),
        "tasks": args.tasks,
        "execution_mode": "manifest-only; run the pinned official benchmark pipeline next",
        "integration_categories": ["vertical", "diagonal", "mosaic", "cross"],
        "interpretation_note": "metrics and rankings are conditional on task, modality, dataset and split",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
