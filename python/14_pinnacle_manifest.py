#!/usr/bin/env python3
"""Prepare an auditable PINNACLE single-cell protein-context manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a PINNACLE context-aware protein-biology manifest"
    )
    parser.add_argument(
        "--expression",
        required=True,
        help="single-cell expression matrix or AnnData file used for cell contexts",
    )
    parser.add_argument(
        "--ppi-network",
        required=True,
        help="protein-protein interaction/network edge table",
    )
    parser.add_argument(
        "--context-metadata",
        required=True,
        help="cell-type/tissue context table keyed to the expression input",
    )
    parser.add_argument(
        "--checkpoint",
        help="optional pinned PINNACLE checkpoint; weights are never downloaded by this helper",
    )
    parser.add_argument(
        "--task",
        choices=("protein_representation", "target_prioritization", "drug_repurposing"),
        default="protein_representation",
    )
    parser.add_argument("--output", default="pinnacle_manifest.json")
    args = parser.parse_args()

    expression = Path(args.expression)
    ppi_network = Path(args.ppi_network)
    context_metadata = Path(args.context_metadata)
    missing = [
        str(path)
        for path in (expression, ppi_network, context_metadata)
        if not path.exists()
    ]
    if args.checkpoint and not Path(args.checkpoint).exists():
        missing.append(args.checkpoint)
    if missing:
        parser.error("missing PINNACLE inputs: " + ", ".join(missing))

    manifest = {
        "method": "PINNACLE",
        "paper_doi": "10.1038/s41592-024-02341-3",
        "official_repo": "https://github.com/mims-harvard/PINNACLE",
        "expression": str(expression),
        "ppi_network": str(ppi_network),
        "context_metadata": str(context_metadata),
        "checkpoint": args.checkpoint,
        "task": args.task,
        "execution_mode": "manifest-only; run the pinned official workflow after auditing context and network versions",
        "outputs_expected": [
            "context-aware protein/cell representations",
            "zero-shot target prioritization or drug-repurposing scores when requested",
            "held-out task metrics and context-stratified diagnostics",
        ],
        "interpretation_note": "context-aware representations support prioritization hypotheses; they do not establish causal protein function or therapeutic efficacy",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
