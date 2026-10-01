# Aggregate cell-level scores back to the biological experimental unit.
# Use this before comparing conditions for CellRank, embeddings, niche scores,
# cell proportions, or other cell-level model outputs.

summarize_cell_scores <- function(scores,
                                  metadata,
                                  sample_col = "sample_id",
                                  condition_col = "condition",
                                  cell_id_col = "cell_id",
                                  FUN = mean) {
    scores <- as.data.frame(scores, stringsAsFactors = FALSE)
    metadata <- as.data.frame(metadata, stringsAsFactors = FALSE)
    if (!cell_id_col %in% names(scores)) {
        scores[[cell_id_col]] <- rownames(scores)
    }
    required <- c(cell_id_col, sample_col, condition_col)
    if (!all(required %in% names(metadata))) {
        stop("metadata needs cell ID, sample ID, and condition columns")
    }
    if (anyDuplicated(metadata[[cell_id_col]])) stop("metadata cell IDs must be unique")
    score_cols <- setdiff(names(scores), cell_id_col)
    numeric_cols <- score_cols[vapply(scores[score_cols], is.numeric, logical(1))]
    if (length(numeric_cols) == 0L) stop("scores needs at least one numeric score column")
    meta <- metadata[, required, drop = FALSE]
    names(meta)[1] <- cell_id_col
    joined <- merge(meta, scores[, c(cell_id_col, numeric_cols), drop = FALSE],
                    by = cell_id_col, all = FALSE, sort = FALSE)
    if (nrow(joined) == 0L) stop("no cell IDs matched between scores and metadata")
    by_cols <- joined[, c(sample_col, condition_col), drop = FALSE]
    result <- aggregate(joined[numeric_cols], by = by_cols, FUN = FUN, na.rm = TRUE)
    counts <- aggregate(joined[[numeric_cols[1L]]],
                        by = by_cols,
                        FUN = function(x) sum(is.finite(x)))
    names(counts)[ncol(counts)] <- "n_cells_used"
    merge(result, counts, by = c(sample_col, condition_col), all = TRUE, sort = FALSE)
}

write_sample_level_summary <- function(scores, metadata,
                                       output = "results/sample_level_summary.csv",
                                       ...) {
    dir.create(dirname(output), recursive = TRUE, showWarnings = FALSE)
    result <- summarize_cell_scores(scores, metadata, ...)
    write.csv(result, output, row.names = FALSE)
    invisible(result)
}

# Example:
# scores <- read.csv("results/cellrank2/fate_probabilities.csv", row.names = 1,
#                    check.names = FALSE)
# metadata <- read.csv("data/mock/scrna_metadata.csv", stringsAsFactors = FALSE)
# write_sample_level_summary(scores, metadata)
