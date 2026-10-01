#!/usr/bin/env python3
"""Prepare an auditable SACCELERATOR spatial-clustering manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a SACCELERATOR spatially aware clustering manifest"
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        required=True,
        help="one or more spatial count/metadata/coordinate or platform-export paths",
    )
    parser.add_argument(
        "--methods",
        nargs="+",
        help="method names or configuration files to compare",
    )
    parser.add_argument(
        "--metrics",
        nargs="+",
        choices=("ARI", "NMI", "CHAOS", "PAS", "spot_entropy", "consensus_entropy"),
        default=("ARI", "CHAOS", "PAS", "spot_entropy"),
        help="metrics to record; use spatial and spatially agnostic metrics together",
    )
    parser.add_argument(
        "--expert-labels",
        help="optional manual/expert annotation file; it is recorded as a comparison layer, not assumed truth",
    )
    parser.add_argument("--platform", help="optional platform or technology label")
    parser.add_argument("--output", default="saccelerator_manifest.json")
    args = parser.parse_args()

    datasets = [Path(item) for item in args.datasets]
    missing = [str(path) for path in datasets if not path.exists()]
    if args.expert_labels and not Path(args.expert_labels).exists():
        missing.append(args.expert_labels)
    if missing:
        parser.error("missing SACCELERATOR inputs: " + ", ".join(missing))

    if not any(metric in {"CHAOS", "PAS", "spot_entropy", "consensus_entropy"} for metric in args.metrics):
        parser.error("include at least one spatially aware metric")

    manifest = {
        "method": "SACCELERATOR",
        "paper_doi": "10.1038/s41592-026-03194-8",
        "official_repo": "https://github.com/SpatialHackathon/SACCELERATOR",
        "datasets": [str(path) for path in datasets],
        "methods": args.methods or [],
        "metrics": list(args.metrics),
        "expert_labels": args.expert_labels,
        "platform": args.platform,
        "execution_mode": "manifest-only; run the pinned official framework after fixing dataset splits, method versions, spatial metrics and expert-review protocol",
        "outputs_expected": [
            "method-level clustering outputs and spatially aware evaluation metrics",
            "cross-dataset/platform reproducibility and disagreement summaries",
            "consensus representation and high-entropy regions for expert review",
        ],
        "interpretation_note": "manual labels are comparison evidence rather than automatic ground truth; consensus or high metric scores do not establish tissue mechanism",
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
