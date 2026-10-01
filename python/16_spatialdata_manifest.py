#!/usr/bin/env python3
"""Prepare an auditable SpatialData spatial-omics data manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a SpatialData spatial-omics data interoperability manifest"
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        required=True,
        help="one or more SpatialData/Zarr, table, image, or platform-export paths",
    )
    parser.add_argument(
        "--elements",
        nargs="+",
        help="expected element names, for example table image labels points",
    )
    parser.add_argument(
        "--coordinate-system",
        help="expected shared coordinate-system name to audit before integration",
    )
    parser.add_argument(
        "--platform",
        help="optional source platform (Visium, Xenium, MERFISH, CosMx, etc.)",
    )
    parser.add_argument("--output", default="spatialdata_manifest.json")
    args = parser.parse_args()

    datasets = [Path(item) for item in args.datasets]
    missing = [str(path) for path in datasets if not path.exists()]
    if missing:
        parser.error("missing SpatialData inputs: " + ", ".join(missing))

    manifest = {
        "method": "SpatialData",
        "paper_doi": "10.1038/s41592-024-02212-x",
        "official_repo": "https://github.com/scverse/spatialdata",
        "datasets": [str(path) for path in datasets],
        "expected_elements": args.elements or [],
        "coordinate_system": args.coordinate_system,
        "platform": args.platform,
        "execution_mode": "manifest-only; validate element names, coordinate systems, units, and serialization before analysis",
        "outputs_expected": [
            "interoperable spatial elements and coordinate transforms",
            "platform-independent table/image/shape/label access",
            "audit trail for downstream spatial neighborhood or multimodal analysis",
        ],
        "interpretation_note": "a common data container improves interoperability but does not by itself correct segmentation, registration, or biological confounding",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
