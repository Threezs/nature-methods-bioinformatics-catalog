#!/usr/bin/env python3
"""CellRank 2 template with explicit inputs and a reproducible output bundle."""
from __future__ import annotations

import argparse
from pathlib import Path


def _require_neighbors(adata) -> None:
    if not ("connectivities" in adata.obsp or "distances" in adata.obsp):
        raise ValueError("compute a neighbors graph before running CellRank")


def run_cellrank(
    h5ad: Path,
    output: Path,
    kernel: str = "pseudotime",
    pseudotime_key: str = "dpt_pseudotime",
) -> None:
    try:
        import pandas as pd
        import scanpy as sc
        import cellrank as cr
    except ImportError as exc:
        raise SystemExit("Install scanpy and cellrank before running this template") from exc

    adata = sc.read_h5ad(h5ad)
    _require_neighbors(adata)
    if kernel == "pseudotime":
        if pseudotime_key not in adata.obs:
            raise ValueError(f"pseudotime kernel requires adata.obs[{pseudotime_key!r}]")
        transition_kernel = cr.kernels.PseudotimeKernel(
            adata, time_key=pseudotime_key
        ).compute_transition_matrix()
    elif kernel == "velocity":
        missing = [key for key in ("Ms", "velocity") if key not in adata.layers]
        if missing:
            raise ValueError(
                "velocity kernel requires adata.layers['Ms'] and "
                f"adata.layers['velocity']; missing {missing}"
            )
        transition_kernel = cr.kernels.VelocityKernel(
            adata, xkey="Ms", vkey="velocity"
        ).compute_transition_matrix()
    else:
        raise ValueError("kernel must be pseudotime or velocity")

    estimator = cr.estimators.GPCCA(transition_kernel)
    estimator.compute_macrostates()
    estimator.predict_terminal_states()
    estimator.compute_fate_probabilities()
    output.mkdir(parents=True, exist_ok=True)
    fate_probabilities = estimator.fate_probabilities
    fate_table = pd.DataFrame(
        fate_probabilities.X,
        index=adata.obs_names,
        columns=list(fate_probabilities.names),
    )
    fate_table.to_csv(output / "fate_probabilities.csv")
    adata.write(output / "cellrank2_annotated.h5ad")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True, help="input .h5ad")
    parser.add_argument("--output", type=Path, default=Path("results/cellrank2"))
    parser.add_argument("--kernel", choices=["pseudotime", "velocity"], default="pseudotime")
    parser.add_argument("--pseudotime-key", default="dpt_pseudotime")
    args = parser.parse_args()
    run_cellrank(args.input, args.output, args.kernel, args.pseudotime_key)


if __name__ == "__main__":
    main()
