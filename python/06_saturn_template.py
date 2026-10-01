#!/usr/bin/env python3
"""Prepare an auditable SATURN cross-species integration manifest.

This wrapper deliberately does not download protein-language-model weights or launch
training. It validates the input contract and writes a JSON manifest that can be
handed to the official snap-stanford/SATURN workflow.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description="Create a SATURN cross-species run manifest")
    p.add_argument("--species", nargs="+", required=True, help="Species names in the same order as --adata")
    p.add_argument("--adata", nargs="+", required=True, help="AnnData paths, one per species")
    p.add_argument("--protein-embeddings", required=True, help="Directory or archive of protein embeddings")
    p.add_argument("--output", default="saturn_manifest.json")
    args = p.parse_args()
    if len(args.species) != len(args.adata):
        p.error("--species and --adata must have the same number of values")
    adata_paths = [Path(x) for x in args.adata]
    missing = [str(path) for path in adata_paths if not path.exists()]
    embedding_path = Path(args.protein_embeddings)
    if not embedding_path.exists():
        missing.append(str(embedding_path))
    if missing:
        p.error("missing SATURN inputs: " + ", ".join(missing))
    manifest = {
        "method": "SATURN",
        "paper_doi": "10.1038/s41592-024-02191-z",
        "official_repo": "https://github.com/snap-stanford/SATURN",
        "zenodo": "https://doi.org/10.5281/zenodo.10258201",
        "species": args.species,
        "adata": [str(path) for path in adata_paths],
        "protein_embeddings": str(embedding_path),
        "execution_mode": "manifest-only; run the pinned official SATURN workflow next",
        "next_step": "Run the pinned official SATURN training/evaluation workflow after validating gene IDs, labels, and protein embedding coverage.",
    }
    out = Path(args.output)
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
