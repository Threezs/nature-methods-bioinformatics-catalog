# Mock 数据范围

当前 mock 目录提供两个轻量 CSV：

- `scrna_counts.csv`：10 个基因 × 8 个细胞的非负整数矩阵；
- `scrna_metadata.csv`：cell ID、condition、batch 和 sample ID；当前示例为 4 个样本、每个样本 2 个细胞。
- `cell_scores.csv`：用于演示 fate/embedding 分数如何汇总回 sample level。

它们可以用于：

- `R/00_input_audit.R` 的输入和 ID 顺序检查；
- `python/00_input_audit.py` 的 CSV smoke test；
- `R/01_single_cell_transformations.R` 和 `R/02_feature_selection_benchmark.R` 的函数级示例。
- `R/05_sample_level_summary.R` 和 `python/08_sample_level_summary.py` 的样本级汇总 smoke test。

它们不能代替完整方法输入。CellRank 2 需要 AnnData、neighbors、pseudotime 或 velocity layers；Bambu 需要 genome-aligned BAM/GTF/FASTA；satuRn 需要 transcript counts、tx2gene 和 biological replicates；foundation model、SATURN、Nicheformer、Monod 和 UCE 需要各自的官方格式、checkpoint 或 config。请以 `catalog.csv` 的 `execution_mode`、`validation_status` 和 `mock_input` 为准。
