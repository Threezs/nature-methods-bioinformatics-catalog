# satuRn wrapper for transcript usage / DTU.
# Gilis et al., doi:10.12688/f1000research.51749.1.

make_satuRn_object <- function(counts, metadata, tx_info, formula = ~ 0 + group) {
    if (!requireNamespace("SummarizedExperiment", quietly = TRUE)) {
        stop("Install SummarizedExperiment before running this function")
    }
    required <- c("isoform_id", "gene_id")
    if (!all(required %in% colnames(tx_info))) stop("tx_info needs isoform_id and gene_id")
    if (!identical(rownames(counts), tx_info$isoform_id)) {
        tx_info <- tx_info[match(rownames(counts), tx_info$isoform_id), , drop = FALSE]
    }
    if (anyNA(tx_info$isoform_id)) stop("every count row needs a transcript annotation")
    se <- SummarizedExperiment::SummarizedExperiment(
        assays = list(counts = as.matrix(counts)),
        colData = S4Vectors::DataFrame(metadata),
        rowData = S4Vectors::DataFrame(tx_info)
    )
    SummarizedExperiment::metadata(se)$formula <- formula
    se
}

run_satuRn <- function(se, contrasts, outdir = "results/satuRn", formula = ~ 0 + group) {
    if (!requireNamespace("satuRn", quietly = TRUE)) stop("Install satuRn from Bioconductor")
    if (!requireNamespace("BiocParallel", quietly = TRUE)) stop("Install BiocParallel")
    dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
    fitted <- satuRn::fitDTU(
        object = se,
        formula = formula,
        parallel = FALSE,
        BPPARAM = BiocParallel::bpparam(),
        verbose = TRUE
    )
    # forceEmpirical is available in some development versions but is not
    # present in the current Bioconductor release. Keep the stable call here.
    tested <- satuRn::testDTU(
        object = fitted,
        contrasts = contrasts,
        diagplot1 = TRUE,
        diagplot2 = TRUE,
        sort = FALSE
    )
    saveRDS(tested, file.path(outdir, "satuRn_tested.rds"))
    invisible(tested)
}

# Example:
# se <- make_satuRn_object(counts, metadata, tx_info)
# design <- model.matrix(~ 0 + group, data = metadata)
# colnames(design) <- levels(factor(metadata$group))
# L <- limma::makeContrasts(APAP - Control, levels = design)
# run_satuRn(se, L)
