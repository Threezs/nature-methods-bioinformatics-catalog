# Nature Methods Bioinformatics Catalog

这是一个偏 R、兼有 Python 的近期生信方法目录。每个条目都记录论文、官方代码、输入输出、适用条件和可以直接复制到科研项目中的入口。

## 先用哪一个

| 问题 | 入口 | 语言 | 适用边界 |
|---|---|---|---|
| 单细胞 count 矩阵怎么变换、PCA 前怎么做 | `R/01_single_cell_transformations.R` | R | 预处理比较；不要把 PCA 结果直接当生物学结论 |
| 单细胞整合前选多少基因 | `R/02_feature_selection_benchmark.R` | R | HVG、批次感知 HVG、lineage marker 的可审计选择 |
| 长读长 RNA-seq 发现和定量新转录本 | `R/03_bambu_long_read.R` | R | 需要 BAM、GTF 和 genome FASTA |
| transcript usage / DTU | `R/04_satuRn_dtu.R` | R | 需要 transcript counts、transcript-to-gene 表和重复样本 |
| 细胞命运、pseudotime、RNA velocity、多视图 | `python/01_cellrank2_template.py` | Python | 需要 `.h5ad` 和 CellRank/scVelo 环境 |
| 单细胞多组学/扰动的 foundation model | `python/02_scgpt_embedding_template.py` | Python | 需要自行下载 checkpoint；权重许可单独核对 |
| 单细胞 embedding、扰动和药物反应 | `python/03_scFoundation_embedding_template.py` | Python | 需要 GPU/大内存时再启用 |
| 把单细胞表达映射到空间 niche | `python/04_nicheformer_template.py` | Python | 空间转录组或 dissociated scRNA-seq；研究性方法 |
| nascent/mature RNA 的生物物理模型 | `python/05_monod_template.py` | Python | 需要匹配的 nascent/mature count；不是常规 bulk DE 替代品 |

## 方法来源

- Ahlmann-Eltze & Huber (2023), *Comparison of transformations for single-cell RNA-seq data*, **Nature Methods**, DOI `10.1038/s41592-023-01814-1`; 代码和补充材料见 Zenodo `10.5281/zenodo.7504146`。
- Weiler et al. (2024), *CellRank 2: unified fate mapping in multiview single-cell data*, **Nature Methods**, DOI `10.1038/s41592-024-02303-9`; 官方代码是 [theislab/cellrank](https://github.com/theislab/cellrank)。
- Cui et al. (2024), *scGPT: toward building a foundation model for single-cell multi-omics using generative AI*, **Nature Methods**, DOI `10.1038/s41592-024-02201-0`; 官方代码是 [bowang-lab/scGPT](https://github.com/bowang-lab/scGPT)。
- Hao et al. (2024), *Large-scale foundation model on single-cell transcriptomics*, **Nature Methods**, DOI `10.1038/s41592-024-02305-7`; 官方代码是 [biomap-research/scFoundation](https://github.com/biomap-research/scFoundation)。
- Zappia et al. (2025), *Feature selection methods affect the performance of scRNA-seq data integration and querying*, **Nature Methods**, DOI `10.1038/s41592-025-02624-3`, PMID `40082610`; 复现实验仓库见 [atlas-feature-selection-benchmark_single_cell_RNA-seq](https://github.com/truong128/atlas-feature-selection-benchmark_single_cell_RNA-seq)。
- Chen et al. (2023), *Context-aware transcript quantification from long-read RNA-seq data with Bambu*, **Nature Methods**, DOI `10.1038/s41592-023-01908-w`; 官方代码是 [GoekeLab/bambu](https://github.com/GoekeLab/bambu)。
- Gilis et al. (2021), *Scalable Analysis of Differential Transcript Usage for Bulk and Single-Cell RNA-sequencing Applications*, DOI `10.12688/f1000research.51749.1`; R/Bioconductor 包是 [statOmics/satuRn](https://github.com/statOmics/satuRn)。
- Gorin et al. (2025), *Monod: model-based discovery and integration through fitting stochastic transcriptional dynamics to single-cell sequencing data*, **Nature Methods**, DOI `10.1038/s41592-025-02832-x`; 官方代码是 [pachterlab/monod](https://github.com/pachterlab/monod) 和 [pachterlab/monod_examples](https://github.com/pachterlab/monod_examples)。
- Tejada-Lapuerta et al. (2025), *Nicheformer: a foundation model for single-cell and spatial omics*, **Nature Methods**, DOI `10.1038/s41592-025-02814-z`; 官方代码是 [theislab/nicheformer](https://github.com/theislab/nicheformer)。

完整字段见 [`catalog.csv`](catalog.csv)，方法选择和限制见 [`docs/method_selection.md`](docs/method_selection.md)。

## 开箱即用约定

1. 先把真实数据的路径、物种、基因组版本、实验单位和对比写进 `config/methods.yml`。
2. R 方法优先使用 `renv` 或 Bioconductor 固定版本；Python 方法固定 conda/uv 环境和 checkpoint 哈希。
3. 任何 foundation model 只保存下载地址、版本和校验值，不把大权重直接提交到 Git。
4. 所有方法先在 `data/mock/` 上跑通，再换成真实数据；完整输出表和运行日志都要保存。
5. 方法论文的 benchmark 结果是选择依据，不等于对你的组织、物种或样本量的保证。

## 与我的其他仓库

- [bioinformatics-methods-cookbook](https://github.com/Threezs/bioinformatics-methods-cookbook)：项目内可复用的 edgeR/ORA/GSEA/TF activity 配方。
- [rnaseq-analysis-template](https://github.com/Threezs/rnaseq-analysis-template)：APAP 24h bulk RNA-seq 的主分析骨架。
- [bioinformatics-literature-workbench](https://github.com/Threezs/bioinformatics-literature-workbench)：论文、claim、数据集和阅读笔记。
- [research-evidence-notebook](https://github.com/Threezs/research-evidence-notebook)：把论文证据和机制假设分层保存。
- [research-project-index](https://github.com/Threezs/research-project-index)：全部仓库和项目状态入口。

