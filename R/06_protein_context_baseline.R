# Dependency-light PPI/network baseline for PINNACLE-style target prioritization.
# This is an interpretable reference, not a replacement for the official model.

ppi_network_baseline <- function(edges,
                                 source_col = "protein_a",
                                 target_col = "protein_b",
                                 weight_col = "weight") {
    edges <- as.data.frame(edges, stringsAsFactors = FALSE)
    required <- c(source_col, target_col)
    if (!all(required %in% names(edges))) {
        stop("edges needs source and target protein columns")
    }
    if (nrow(edges) == 0L) stop("edges must contain at least one interaction")
    nodes <- sort(unique(c(as.character(edges[[source_col]]),
                           as.character(edges[[target_col]]))))
    source <- as.character(edges[[source_col]])
    target <- as.character(edges[[target_col]])
    degree <- tabulate(match(c(source, target), nodes), nbins = length(nodes))
    result <- data.frame(
        protein = nodes,
        degree = as.integer(degree),
        stringsAsFactors = FALSE
    )
    if (weight_col %in% names(edges)) {
        weights <- suppressWarnings(as.numeric(edges[[weight_col]]))
        if (any(!is.finite(weights))) stop("network weights must be finite numeric values")
        weighted <- numeric(length(nodes))
        source_sums <- tapply(weights, match(source, nodes), sum)
        target_sums <- tapply(weights, match(target, nodes), sum)
        weighted[as.integer(names(source_sums))] <-
            weighted[as.integer(names(source_sums))] + as.numeric(source_sums)
        weighted[as.integer(names(target_sums))] <-
            weighted[as.integer(names(target_sums))] + as.numeric(target_sums)
        result$weighted_degree <- as.numeric(weighted)
    }
    order_args <- list(-result$degree)
    if ("weighted_degree" %in% names(result)) {
        order_args[[length(order_args) + 1L]] <- -result$weighted_degree
    }
    order_args[[length(order_args) + 1L]] <- result$protein
    result[do.call(order, order_args), , drop = FALSE]
}

add_context_counts <- function(protein_scores,
                               context_metadata,
                               protein_col = "protein",
                               context_col = "cell_type") {
    protein_scores <- as.data.frame(protein_scores, stringsAsFactors = FALSE)
    context_metadata <- as.data.frame(context_metadata, stringsAsFactors = FALSE)
    if (!all(c(protein_col, context_col) %in% names(context_metadata))) {
        stop("context_metadata needs protein and context columns for context counts")
    }
    counts <- aggregate(
        context_metadata[[context_col]],
        by = list(protein = as.character(context_metadata[[protein_col]])),
        FUN = function(x) length(unique(as.character(x)))
    )
    names(counts)[2] <- "n_contexts"
    merge(protein_scores, counts, by = "protein", all.x = TRUE, sort = FALSE)
}

write_ppi_network_baseline <- function(edges,
                                       output = "results/ppi_network_baseline.csv",
                                       ...) {
    dir.create(dirname(output), recursive = TRUE, showWarnings = FALSE)
    result <- ppi_network_baseline(edges, ...)
    write.csv(result, output, row.names = FALSE)
    invisible(result)
}

# Example:
# edges <- read.delim("data/mock/protein_network.tsv", stringsAsFactors = FALSE)
# write_ppi_network_baseline(edges)
