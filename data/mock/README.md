# Mock 数据范围

当前 mock 目录提供轻量、非生物学真实性保证的 CSV：

- `scrna_counts.csv`：10 个基因 × 8 个细胞的非负整数矩阵；
- `scrna_metadata.csv`：cell ID、condition、batch 和 sample ID；当前示例为 4 个样本、每个样本 2 个细胞。
- `cell_scores.csv`：用于演示 fate/embedding 分数如何汇总回 sample level。
- `cell_embedding.csv`：8 个细胞的合成高维表示，用于 Mellon manifest smoke test。
- `multimodal_dataset_manifest.csv`：用于 MISO/SCMMIB 的共享 key、模态和坐标约定示例。
- `narmbench_reads.fastq` 与 `narmbench_reference.fa`：仅用于 NaRMBench manifest smoke test 的合成占位输入，不可用于真实修饰检测。
- `protein_network.tsv` 与 `context_metadata.csv`：用于 PINNACLE manifest smoke test 的小型网络和 cell-type/tissue 上下文占位输入，不可用于蛋白功能或药物结论。

它们可以用于：

- `R/00_input_audit.R` 的输入和 ID 顺序检查；
- `python/00_input_audit.py` 的 CSV smoke test；
- `R/01_single_cell_transformations.R` 和 `R/02_feature_selection_benchmark.R` 的函数级示例。
- `R/05_sample_level_summary.R` 和 `python/08_sample_level_summary.py` 的样本级汇总 smoke test。
- `python/09_mellon_template.py`、`python/10_miso_manifest.py` 和 `python/11_scmmib_manifest.py` 的依赖轻 manifest smoke test。
- `python/12_scmultibench_manifest.py`、`python/13_narmbench_manifest.py` 和 `python/14_pinnacle_manifest.py` 的依赖轻 manifest smoke test。

它们不能代替完整方法输入。CellRank 2 需要 AnnData、neighbors、pseudotime 或 velocity layers；Bambu 需要 genome-aligned BAM/GTF/FASTA；satuRn 需要 transcript counts、tx2gene 和 biological replicates；foundation model、SATURN、Nicheformer、Monod、UCE 和 PINNACLE 需要各自的官方格式、网络/checkpoint 或 config。请以 `catalog.csv` 的 `execution_mode`、`validation_status` 和 `mock_input` 为准。
