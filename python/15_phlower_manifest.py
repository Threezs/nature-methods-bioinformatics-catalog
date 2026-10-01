#!/usr/bin/env python3
"""Prepare an auditable PHLOWER multimodal trajectory manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a PHLOWER multimodal branching-trajectory manifest"
    )
    parser.add_argument(
        "--modalities",
        nargs="+",
        required=True,
        help="two or more aligned modality files (CSV/TSV/AnnData or official formats)",
    )
    parser.add_argument(
        "--cell-metadata",
        required=True,
        help="cell metadata table with shared cell IDs and optional labels",
    )
    parser.add_argument(
        "--root-label",
        help="optional root/progenitor label used to orient the trajectory",
    )
    parser.add_argument(
        "--terminal-labels",
        nargs="+",
        help="optional terminal-state labels to audit against inferred branches",
    )
    parser.add_argument(
        "--task",
        choices=("branching_trajectory", "regulator_prioritization", "both"),
        default="both",
    )
    parser.add_argument("--output", default="phlower_manifest.json")
    args = parser.parse_args()

    if len(args.modalities) < 2:
        parser.error("PHLOWER requires at least two modalities")
    modalities = [Path(item) for item in args.modalities]
    metadata = Path(args.cell_metadata)
    missing = [str(path) for path in modalities + [metadata] if not path.exists()]
    if missing:
        parser.error("missing PHLOWER inputs: " + ", ".join(missing))

    manifest = {
        "method": "PHLOWER",
        "paper_doi": "10.1038/s41592-025-02870-5",
        "official_repo": "https://github.com/CostaLab/phlower",
        "modalities": [str(path) for path in modalities],
        "cell_metadata": str(metadata),
        "root_label": args.root_label,
        "terminal_labels": args.terminal_labels or [],
        "task": args.task,
        "execution_mode": "manifest-only; run the pinned official workflow after checking shared cell IDs and trajectory orientation",
        "outputs_expected": [
            "multimodal trajectory and edge-flow embeddings",
            "complex branching differentiation tree",
            "candidate transcriptional regulator scores when requested",
        ],
        "interpretation_note": "branching trajectories and regulator scores are hypotheses; direction, root choice and multimodal alignment require independent validation",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
