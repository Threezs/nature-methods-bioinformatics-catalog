#!/usr/bin/env python3
"""Prepare an auditable MISO multimodal spatial-omics manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a MISO spatial multimodal manifest")
    parser.add_argument("--omics", nargs="+", required=True, help="one or more aligned omics matrices/features")
    parser.add_argument("--image-features", default=None, help="optional aligned histology/image feature file")
    parser.add_argument("--spot-metadata", default=None, help="optional spot/cell metadata table")
    parser.add_argument("--output", default="miso_manifest.json")
    args = parser.parse_args()

    omics = [Path(item) for item in args.omics]
    missing = [str(path) for path in omics if not path.exists()]
    image_features = Path(args.image_features) if args.image_features else None
    spot_metadata = Path(args.spot_metadata) if args.spot_metadata else None
    for path in (image_features, spot_metadata):
        if path is not None and not path.exists():
            missing.append(str(path))
    if missing:
        parser.error("missing MISO inputs: " + ", ".join(missing))

    manifest = {
        "method": "MISO",
        "paper_doi": "10.1038/s41592-024-02574-2",
        "official_repo": "https://github.com/kpcoleman/miso",
        "omics": [str(path) for path in omics],
        "image_features": str(image_features) if image_features is not None else None,
        "spot_metadata": str(spot_metadata) if spot_metadata is not None else None,
        "execution_mode": "manifest-only; run the pinned Python 3.7/Git-LFS official workflow next",
        "outputs_expected": ["multimodal_embedding", "spatial_clusters", "modality_integration_diagnostics"],
        "input_contract": "all modalities must share an explicit spot/cell key and coordinate convention",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
