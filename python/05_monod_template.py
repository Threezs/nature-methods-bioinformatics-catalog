#!/usr/bin/env python3
"""Monod input manifest; fitting is delegated to the official package/examples."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def make_manifest(nascent: Path, mature: Path, output: Path, config: Path | None = None) -> dict:
    for path in (nascent, mature):
        if not path.exists():
            raise FileNotFoundError(path)
    if config is not None and not config.exists():
        raise FileNotFoundError(config)
    return {
        "method": "Monod",
        "nascent_counts": str(nascent),
        "mature_counts": str(mature),
        "config": str(config) if config is not None else None,
        "official_repo": "https://github.com/pachterlab/monod",
        "examples_repo": "https://github.com/pachterlab/monod_examples",
        "paper_doi": "10.1038/s41592-025-02832-x",
        "execution_mode": "manifest-only; run the pinned official Monod package/examples next",
        "modeling_note": "fit and compare stochastic transcription models; report uncertainty",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nascent", type=Path, required=True)
    parser.add_argument("--mature", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=None, help="optional official Monod config")
    parser.add_argument("--output", type=Path, default=Path("results/monod_manifest.json"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(make_manifest(args.nascent, args.mature, args.output, args.config), indent=2) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
