# Bambu wrapper for context-aware long-read transcript discovery/quantification.
# Chen et al., Nature Methods 2023, doi:10.1038/s41592-023-01908-w.

run_bambu <- function(bam_files,
                      gtf,
                      genome_fasta,
                      outdir = "results/bambu",
                      ncore = 4,
                      ndr = 0.1,
                      stranded = FALSE) {
    if (!requireNamespace("bambu", quietly = TRUE)) {
        stop("Install bambu from Bioconductor before running this function")
    }
    if (!all(file.exists(bam_files))) stop("missing BAM file")
    if (!file.exists(gtf) || !file.exists(genome_fasta)) stop("missing GTF or genome FASTA")
    dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
    annotations <- bambu::prepareAnnotations(gtf)
    se <- bambu::bambu(
        reads = bam_files,
        annotations = annotations,
        genome = genome_fasta,
        ncore = ncore,
        NDR = ndr,
        stranded = stranded,
        verbose = TRUE
    )
    saveRDS(se, file.path(outdir, "bambu_transcripts.rds"))
    gene_se <- bambu::transcriptToGeneExpression(se)
    saveRDS(gene_se, file.path(outdir, "bambu_genes.rds"))
    invisible(list(transcript = se, gene = gene_se))
}

# Example:
# run_bambu(list.files("data/real/bam", "\\.bam$", full.names = TRUE),
#           "data/real/annotation.gtf", "data/real/genome.fa")
