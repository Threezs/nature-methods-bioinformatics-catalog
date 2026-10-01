#!/usr/bin/env python3
"""CellRank 2 template with explicit inputs and a reproducible output bundle."""
from __future__ import annotations

import argparse
from pathlib import Path


def run_cellrank(h5ad: Path, output: Path, kernel: str = "pseudotime") -> None:
    try:
        import scanpy as sc
        import cellrank as cr
    except ImportError as exc:
        raise SystemExit("Install scanpy and cellrank before running this template") from exc

    adata = sc.read_h5ad(h5ad)
    if kernel == "pseudotime":
        if "dpt_pseudotime" not in adata.obs:
            raise ValueError("pseudotime kernel requires adata.obs['dpt_pseudotime']")
        transition_kernel = cr.kernels.PseudotimeKernel(adata).compute_transition_matrix()
    elif kernel == "velocity":
        if "velocity" not in adata.layers:
            raise ValueError("velocity kernel requires adata.layers['velocity']")
        transition_kernel = cr.kernels.VelocityKernel(adata).compute_transition_matrix()
    else:
        raise ValueError("kernel must be pseudotime or velocity")

    estimator = cr.estimators.GPCCA(transition_kernel)
    estimator.compute_macrostates()
    estimator.predict_terminal_states()
    estimator.compute_fate_probabilities()
    output.mkdir(parents=True, exist_ok=True)
    estimator.fate_probabilities.to_csv(output / "fate_probabilities.csv")
    adata.write(output / "cellrank2_annotated.h5ad")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True, help="input .h5ad")
    parser.add_argument("--output", type=Path, default=Path("results/cellrank2"))
    parser.add_argument("--kernel", choices=["pseudotime", "velocity"], default="pseudotime")
    args = parser.parse_args()
    run_cellrank(args.input, args.output, args.kernel)


if __name__ == "__main__":
    main()
