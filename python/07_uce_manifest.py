#!/usr/bin/env python3
"""Prepare an auditable UCE zero-shot embedding manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description="Create a UCE zero-shot embedding manifest")
    p.add_argument("--input-h5ad", required=True, help="Input AnnData path")
    p.add_argument("--checkpoint", required=True, help="Pinned UCE checkpoint path or URI")
    p.add_argument("--species", default="record_in_config", help="Species label for the input dataset")
    p.add_argument("--output", default="uce_manifest.json")
    args = p.parse_args()
    input_path = Path(args.input_h5ad)
    checkpoint_path = Path(args.checkpoint)
    if not input_path.exists():
        p.error(f"missing input AnnData: {input_path}")
    if not checkpoint_path.exists() and "://" not in args.checkpoint:
        p.error(f"missing checkpoint path (or provide a URI): {checkpoint_path}")
    manifest = {
        "method": "UCE",
        "paper_doi": "10.1038/s41586-026-10689-z",
        "official_repo": "https://github.com/snap-stanford/UCE",
        "pmid": "42420460",
        "input_h5ad": str(input_path),
        "species": args.species,
        "checkpoint": str(checkpoint_path) if "://" not in args.checkpoint else args.checkpoint,
        "execution_mode": "manifest-only; run the pinned official UCE workflow next",
        "next_step": "Run the pinned official UCE embedding workflow after validating gene identifiers, protein-token coverage, and species metadata.",
    }
    out = Path(args.output)
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
