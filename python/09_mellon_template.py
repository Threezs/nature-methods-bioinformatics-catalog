#!/usr/bin/env python3
"""Prepare an auditable Mellon cell-state density manifest.

The actual density estimation is delegated to the pinned official Mellon package.
This lightweight entry point verifies the representation and optional metadata
before a model-specific environment is started.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Mellon cell-state density manifest")
    parser.add_argument("--embedding", required=True, help="CSV/TSV or array file containing a cell representation")
    parser.add_argument("--metadata", default=None, help="optional cell metadata with time/sample labels")
    parser.add_argument("--representation", default="high_dimensional_embedding")
    parser.add_argument("--output", default="mellon_manifest.json")
    args = parser.parse_args()

    embedding = Path(args.embedding)
    metadata = Path(args.metadata) if args.metadata else None
    if not embedding.exists():
        parser.error(f"missing embedding: {embedding}")
    if metadata is not None and not metadata.exists():
        parser.error(f"missing metadata: {metadata}")

    manifest = {
        "method": "Mellon",
        "paper_doi": "10.1038/s41592-024-02302-w",
        "official_repo": "https://github.com/settylab/Mellon",
        "docs": "https://mellon.readthedocs.io/en/latest/",
        "embedding": str(embedding),
        "metadata": str(metadata) if metadata is not None else None,
        "representation": args.representation,
        "execution_mode": "manifest-only; run the pinned official Mellon package next",
        "outputs_expected": ["cell_state_density", "gene_change_scores", "optional_temporal_interpolation"],
        "interpretation_note": "density describes occupancy of a chosen representation; it is not a causal lineage probability",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
