# R-first implementation of practical transformations discussed by
# Ahlmann-Eltze & Huber (Nature Methods 2023, doi:10.1038/s41592-023-01814-1).
# Input: raw integer genes x cells matrix. Output: transformed matrix.

transform_counts <- function(counts,
                             method = c("log1p_cpm", "shifted_log", "pearson_residuals"),
                             target_sum = 1e4,
                             y0 = 1,
                             residual_clip = 5) {
    method <- match.arg(method)
    counts <- as.matrix(counts)
    storage.mode(counts) <- "double"
    if (any(!is.finite(counts)) || any(counts < 0)) {
        stop("counts must be finite and non-negative")
    }
    if (any(abs(counts - round(counts)) > 1e-8)) {
        warning("counts are not integer-valued; verify that this is intended")
    }
    lib_size <- colSums(counts)
    if (any(lib_size <= 0)) stop("every cell must have a positive library size")
    cpm <- sweep(counts, 2, lib_size, "/") * target_sum

    if (method == "log1p_cpm") return(log1p(cpm))
    if (method == "shifted_log") return(log2(cpm + y0))

    # A transparent Poisson Pearson-residual baseline. This is a reusable
    # implementation, not a claim to reproduce every residual model variant.
    expected <- outer(rowSums(counts), lib_size / sum(lib_size))
    residuals <- (counts - expected) / sqrt(expected + 1e-8)
    residuals <- pmax(pmin(residuals, residual_clip), -residual_clip)
    residuals
}

run_transformation_panel <- function(counts, methods = c("log1p_cpm", "shifted_log", "pearson_residuals")) {
    setNames(lapply(methods, function(m) transform_counts(counts, method = m)), methods)
}

# Example:
# counts <- as.matrix(read.csv("data/mock/scrna_counts.csv", row.names = 1, check.names = FALSE))
# panel <- run_transformation_panel(counts)
# saveRDS(panel, "results/transformation_panel.rds")
