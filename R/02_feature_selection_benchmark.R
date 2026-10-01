# Practical, auditable feature-selection helpers inspired by
# Zappia et al. (Nature Methods 2025, doi:10.1038/s41592-025-02624-3).
#
# The dependency-light functions below are transparent baselines. They rank
# features by variance or mean effect; they are not a full replacement for
# scran/Seurat feature-selection implementations. Optional scran integration
# is provided at the end of the file.

log1p_cpm <- function(counts, target_sum = 1e4) {
    counts <- as.matrix(counts)
    lib <- colSums(counts)
    if (any(lib <= 0)) stop("all cells must have positive library size")
    log1p(sweep(counts, 2, lib, "/") * target_sum)
}

rank_variable_features <- function(counts, n_top_genes = 2000, batch = NULL, min_cells = 3) {
    x <- log1p_cpm(counts)
    detected <- rowSums(counts > 0)
    keep <- detected >= min_cells
    x <- x[keep, , drop = FALSE]
    if (is.null(batch)) {
        score <- apply(x, 1, var)
    } else {
        batch <- factor(batch)
        if (length(batch) != ncol(x)) stop("batch must match cell columns")
        score <- rowMeans(sapply(levels(batch), function(b) {
            idx <- batch == b
            if (sum(idx) < 2) return(rep(NA_real_, nrow(x)))
            apply(x[, idx, drop = FALSE], 1, var)
        }), na.rm = TRUE)
    }
    score[!is.finite(score)] <- -Inf
    n <- min(n_top_genes, length(score))
    selected <- names(sort(score, decreasing = TRUE))[seq_len(n)]
    data.frame(gene = selected, variance_score = unname(score[selected]), row.names = NULL)
}

# Descriptive group mean-effect candidates. This is not replicate-aware
# differential expression and should not be used as a substitute for a
# sample-level statistical model.
rank_group_mean_effect <- function(counts, labels, n_per_group = 100) {
    x <- log1p_cpm(counts)
    labels <- factor(labels)
    if (length(labels) != ncol(x)) stop("labels must match cell columns")
    out <- lapply(levels(labels), function(g) {
        in_group <- labels == g
        effect <- rowMeans(x[, in_group, drop = FALSE]) - rowMeans(x[, !in_group, drop = FALSE])
        n <- min(n_per_group, length(effect))
        data.frame(group = g, gene = names(sort(effect, decreasing = TRUE))[seq_len(n)],
                   effect = sort(effect, decreasing = TRUE)[seq_len(n)])
    })
    do.call(rbind, out)
}

# Backward-compatible aliases. Prefer the explicit names above in new work.
select_hvg <- rank_variable_features
rank_lineage_mean_effect <- rank_group_mean_effect
select_lineage_markers <- rank_group_mean_effect

# Optional model-based HVG selection. Supply a SingleCellExperiment with a
# suitable logcounts assay (for example after scuttle::logNormCounts()).
select_hvg_scran <- function(sce, n_top_genes = 2000, block = NULL) {
    if (!requireNamespace("scran", quietly = TRUE)) {
        stop("Install scran from Bioconductor for model-based HVG selection")
    }
    dec <- scran::modelGeneVar(sce, block = block)
    genes <- scran::getTopHVGs(dec, n = n_top_genes)
    dec[match(genes, rownames(dec)), c("bio", "total", "p.value", "FDR"), drop = FALSE]
}

# Example:
# counts <- as.matrix(read.csv("data/mock/scrna_counts.csv", row.names = 1, check.names = FALSE))
# meta <- read.csv("data/mock/scrna_metadata.csv")
# ranked <- rank_variable_features(counts, n_top_genes = 2000, batch = meta$batch)
# group_effects <- rank_group_mean_effect(counts, meta$condition)
