# Practical, auditable feature-selection helpers inspired by
# Zappia et al. (Nature Methods 2025, doi:10.1038/s41592-025-02624-3).

log1p_cpm <- function(counts, target_sum = 1e4) {
    counts <- as.matrix(counts)
    lib <- colSums(counts)
    if (any(lib <= 0)) stop("all cells must have positive library size")
    log1p(sweep(counts, 2, lib, "/") * target_sum)
}

select_hvg <- function(counts, n_top_genes = 2000, batch = NULL, min_cells = 3) {
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
    data.frame(gene = selected, score = unname(score[selected]), row.names = NULL)
}

select_lineage_markers <- function(counts, labels, n_per_group = 100) {
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

# Example:
# counts <- as.matrix(read.csv("data/mock/scrna_counts.csv", row.names = 1, check.names = FALSE))
# meta <- read.csv("data/mock/scrna_metadata.csv")
# hvg <- select_hvg(counts, n_top_genes = 2000, batch = meta$batch)
# markers <- select_lineage_markers(counts, meta$condition)
