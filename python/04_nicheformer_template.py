#!/usr/bin/env python3
"""Nicheformer launcher manifest for spatial-context prediction."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def make_manifest(input_h5ad: Path, checkpoint_dir: Path, output: Path) -> dict:
    if not input_h5ad.exists():
        raise FileNotFoundError(input_h5ad)
    if not checkpoint_dir.exists():
        raise FileNotFoundError(checkpoint_dir)
    return {
        "method": "Nicheformer",
        "input_h5ad": str(input_h5ad),
        "checkpoint_dir": str(checkpoint_dir),
        "official_repo": "https://github.com/theislab/nicheformer",
        "paper_doi": "10.1038/s41592-025-02814-z",
        "expected_outputs": ["niche embeddings", "spatial-context or niche predictions"],
        "validation": ["compare to a non-foundation baseline", "hold out tissue or donor when possible"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("results/nicheformer_manifest.json"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(make_manifest(args.input, args.checkpoint_dir, args.output), indent=2) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
