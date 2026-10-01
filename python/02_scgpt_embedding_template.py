#!/usr/bin/env python3
"""Minimal scGPT launcher; model checkpoints are intentionally external to Git."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_manifest(input_h5ad: Path, checkpoint_dir: Path, output: Path, task: str) -> dict:
    if not input_h5ad.exists():
        raise FileNotFoundError(input_h5ad)
    if not checkpoint_dir.exists():
        raise FileNotFoundError(checkpoint_dir)
    return {
        "method": "scGPT",
        "task": task,
        "input_h5ad": str(input_h5ad),
        "checkpoint_dir": str(checkpoint_dir),
        "official_repo": "https://github.com/bowang-lab/scGPT",
        "paper_doi": "10.1038/s41592-024-02201-0",
        "status": "checkpoint-dependent; run the official task notebook after reviewing model license",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("results/scgpt_manifest.json"))
    parser.add_argument("--task", choices=["annotation", "integration", "perturbation", "embedding"], default="embedding")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(build_manifest(args.input, args.checkpoint_dir, args.output, args.task), indent=2) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
