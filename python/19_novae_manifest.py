#!/usr/bin/env python3
"""Prepare an auditable Novae spatial-domain analysis manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


TASKS = (
    "domain_inference",
    "batch_correction",
    "svg_analysis",
    "pathway_analysis",
    "architecture",
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a Novae spatial-domain and tissue-architecture manifest"
    )
    parser.add_argument(
        "--inputs",
        nargs="+",
        required=True,
        help="spatial transcriptomics/AnnData/table or image-derived feature paths",
    )
    parser.add_argument(
        "--task",
        choices=TASKS,
        default="domain_inference",
        help="single Novae task to record",
    )
    parser.add_argument(
        "--checkpoint",
        help="optional pinned checkpoint path or URI; weights are never downloaded by this helper",
    )
    parser.add_argument(
        "--gene-panel",
        help="optional gene-panel or feature-list file used to audit cross-panel transfer",
    )
    parser.add_argument("--platform", help="optional spatial platform or tissue label")
    parser.add_argument("--output", default="novae_manifest.json")
    args = parser.parse_args()

    inputs = [Path(item) for item in args.inputs]
    missing = [str(path) for path in inputs if not path.exists()]
    if args.gene_panel and not Path(args.gene_panel).exists():
        missing.append(args.gene_panel)
    if missing:
        parser.error("missing Novae inputs: " + ", ".join(missing))

    manifest = {
        "method": "Novae",
        "paper_doi": "10.1038/s41592-025-02899-6",
        "official_repo": "https://github.com/prism-oncology/novae",
        "inputs": [str(path) for path in inputs],
        "task": args.task,
        "checkpoint": args.checkpoint,
        "gene_panel": args.gene_panel,
        "platform": args.platform,
        "execution_mode": "manifest-only; run the pinned official workflow after fixing spatial elements, gene-panel coverage, batch labels and held-out validation",
        "outputs_expected": [
            "single-cell or spot-level spatial domain assignments",
            "optional batch-corrected representation and cross-panel transfer diagnostics",
            "spatially variable genes/pathways and tissue-architecture summaries",
        ],
        "interpretation_note": "domain assignments, SVGs and pathway scores are model-dependent summaries; inspect tissue registration, batch effects and independent biological validation before claiming mechanism",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
