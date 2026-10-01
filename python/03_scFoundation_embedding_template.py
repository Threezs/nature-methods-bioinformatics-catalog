#!/usr/bin/env python3
"""scFoundation manifest and input audit; weights stay outside the repository."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def audit(input_h5ad: Path, checkpoint_dir: Path, output: Path) -> dict:
    if not input_h5ad.exists():
        raise FileNotFoundError(input_h5ad)
    if not checkpoint_dir.exists():
        raise FileNotFoundError(checkpoint_dir)
    return {
        "method": "scFoundation",
        "input_h5ad": str(input_h5ad),
        "checkpoint_dir": str(checkpoint_dir),
        "official_repo": "https://github.com/biomap-research/scFoundation",
        "paper_doi": "10.1038/s41592-024-02305-7",
        "recommended_baseline": "PCA or scVI with the same train/query split",
        "weights_required": True,
        "gpu_recommended": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("results/scfoundation_audit.json"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit(args.input, args.checkpoint_dir, args.output), indent=2) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
