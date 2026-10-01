# Dependency-light input checks for a gene x cell or gene x sample count matrix.
# This script validates the data contract before any method-specific analysis.

`%||%` <- function(x, y) if (is.null(x)) y else x

audit_count_matrix <- function(counts, require_integer = FALSE) {
    counts <- as.matrix(counts)
    if (length(dim(counts)) != 2L || nrow(counts) == 0L || ncol(counts) == 0L) {
        stop("counts must be a non-empty two-dimensional matrix")
    }
    if (is.null(rownames(counts)) || is.null(colnames(counts))) {
        warning("counts should have both feature names and observation names")
    }
    storage.mode(counts) <- "double"
    if (any(!is.finite(counts))) stop("counts contains NA, NaN, or Inf")
    if (any(counts < 0)) stop("counts contains negative values")
    if (require_integer && any(abs(counts - round(counts)) > 1e-8)) {
        stop("counts must be integer-valued for this workflow")
    }
    lib_size <- colSums(counts)
    detected <- colSums(counts > 0)
    data.frame(
        observation = colnames(counts) %||% seq_len(ncol(counts)),
        library_size = as.numeric(lib_size),
        detected_features = as.numeric(detected),
        zero_fraction = as.numeric(1 - detected / nrow(counts)),
        row.names = NULL,
        check.names = FALSE
    )
}

audit_metadata <- function(metadata, expected_n = NULL, id_column = NULL, expected_ids = NULL) {
    metadata <- as.data.frame(metadata, stringsAsFactors = FALSE)
    if (nrow(metadata) == 0L) stop("metadata has no rows")
    if (!is.null(expected_n) && nrow(metadata) != expected_n) {
        stop("metadata row count does not match the count matrix observations")
    }
    if (!is.null(id_column)) {
        if (!id_column %in% names(metadata)) stop("id_column is missing from metadata")
        if (anyDuplicated(metadata[[id_column]])) stop("metadata IDs must be unique")
        if (!is.null(expected_ids)) {
            observed_ids <- as.character(metadata[[id_column]])
            expected_ids <- as.character(expected_ids)
            if (!identical(observed_ids, expected_ids)) {
                stop("metadata IDs must match count matrix columns in the same order")
            }
        }
    }
    missing_fraction <- vapply(metadata, function(x) {
        is_missing <- is.na(x)
        if (is.character(x)) is_missing <- is_missing | x == ""
        mean(is_missing)
    }, numeric(1))
    data.frame(
        field = names(metadata),
        class = vapply(metadata, function(x) class(x)[1], character(1)),
        n_unique = vapply(metadata, function(x) length(unique(x[!is.na(x)])), integer(1)),
        missing_fraction = as.numeric(missing_fraction),
        row.names = NULL,
        check.names = FALSE
    )
}

write_input_audit <- function(counts, metadata, output_dir = "results/input_audit", id_column = "cell_id") {
    dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
    count_report <- audit_count_matrix(counts)
    use_id <- if (id_column %in% names(metadata)) id_column else NULL
    metadata_report <- audit_metadata(
        metadata,
        expected_n = ncol(counts),
        id_column = use_id,
        expected_ids = if (!is.null(use_id)) colnames(counts) else NULL
    )
    write.csv(count_report, file.path(output_dir, "count_matrix_audit.csv"), row.names = FALSE)
    write.csv(metadata_report, file.path(output_dir, "metadata_audit.csv"), row.names = FALSE)
    invisible(list(counts = count_report, metadata = metadata_report))
}

# Example:
# counts <- as.matrix(read.csv("data/mock/scrna_counts.csv", row.names = 1, check.names = FALSE))
# metadata <- read.csv("data/mock/scrna_metadata.csv", stringsAsFactors = FALSE)
# write_input_audit(counts, metadata)
