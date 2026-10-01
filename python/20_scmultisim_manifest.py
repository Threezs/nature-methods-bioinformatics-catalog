#!/usr/bin/env python3
"""Prepare an auditable scMultiSim simulation manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


MODALITIES = ("rna", "atac", "velocity", "spatial")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create an scMultiSim multi-omics and spatial simulation manifest"
    )
    parser.add_argument(
        "--tree",
        required=True,
        help="cell differential tree or population structure input",
    )
    parser.add_argument(
        "--grn",
        required=True,
        help="gene regulatory network input",
    )
    parser.add_argument(
        "--modalities",
        nargs="+",
        choices=MODALITIES,
        default=("rna", "atac"),
        help="modalities to record for the planned simulation",
    )
    parser.add_argument(
        "--spatial",
        help="optional spatial-coordinate or cell-cell-interaction configuration",
    )
    parser.add_argument(
        "--batch-effects",
        action="store_true",
        help="include batch-effect simulation in the declared plan",
    )
    parser.add_argument("--seed", type=int, help="simulation seed to record")
    parser.add_argument("--output", default="scmultisim_manifest.json")
    args = parser.parse_args()

    required = [Path(args.tree), Path(args.grn)]
    if args.spatial:
        required.append(Path(args.spatial))
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        parser.error("missing scMultiSim inputs: " + ", ".join(missing))
    if "spatial" in args.modalities and not args.spatial:
        parser.error("--spatial is required when the spatial modality is selected")
    if "velocity" in args.modalities and "rna" not in args.modalities:
        parser.error("RNA modality is required when velocity is selected")

    manifest = {
        "method": "scMultiSim",
        "paper_doi": "10.1038/s41592-025-02651-0",
        "official_repo": "https://github.com/ZhangLabGT/scMultiSim",
        "bioconductor_package": "scMultiSim",
        "tree": str(Path(args.tree)),
        "grn": str(Path(args.grn)),
        "modalities": list(args.modalities),
        "spatial": args.spatial,
        "batch_effects": args.batch_effects,
        "seed": args.seed,
        "execution_mode": "manifest-only; run the pinned Bioconductor scMultiSim workflow after fixing biological factors, technical noise, modality relationships and benchmark splits",
        "outputs_expected": [
            "simulated paired or modality-specific count matrices",
            "optional spliced/unspliced, spatial-location and cell-cell-interaction ground truth",
            "known cell structure, GRN, batch and technical-noise truth for method evaluation",
        ],
        "interpretation_note": "simulation ground truth is controlled by the declared tree, GRN, interaction and noise parameters; benchmark conclusions are conditional on those assumptions and do not replace experimental validation",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
