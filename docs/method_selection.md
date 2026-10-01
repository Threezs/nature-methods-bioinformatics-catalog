# 方法选择和边界

## R-first 路径

### 单细胞预处理

先用 `R/01_single_cell_transformations.R` 比较至少两种变换，再固定一种进入 PCA、邻居图和整合。推荐把原始整数矩阵永远保留，并记录 library size、过滤规则、变换、缩放和随机种子。shifted-log、log1p-CPM 和 Pearson residuals 解决的问题不同，不能只按 UMAP 好看来选。

### 整合和 query mapping

`R/02_feature_selection_benchmark.R` 提供 HVG、批次感知 HVG 和 lineage marker 的可审计实现。大规模 atlas 或 reference/query 项目，先固定 feature-selection 规则，再比较 Harmony、scVI 或 Seurat 等整合器；不要在每个 query 上重新挑一套特征。

### 长读长和转录本层面

Bambu 适合从已比对的长读长 BAM 中做 context-aware transcript discovery/quantification。satuRn 适合在 transcript counts 已经可靠的前提下做 DTU。两者都需要 transcript-to-gene 关系、参考版本和样本级重复；单个样本不能支持可靠的组间推断。

### 跨物种单细胞

SATURN (`python/06_saturn_template.py`) 用蛋白 embedding 和表达共同学习跨物种细胞空间。先核对物种、gene/protein coverage、标签一致性和 checkpoint，再比较 marker-based label transfer 等可解释基线。\n\nUCE (`python/07_uce_manifest.py`) 提供零样本的单细胞表示，可用于新物种或新组织的 embedding 和标签迁移。把它当作外部表示分支，保留原始表达和可解释 baseline，并记录 checkpoint、词表覆盖和物种元数据。

## Python/模型路径

CellRank 2 应该在已有邻居图、pseudotime、RNA velocity 或时间点信息后使用。先检查不同 kernel 的 terminal states 和 fate probabilities 是否稳定，再把 lineage-correlated genes 当作候选机制线索。

scGPT、scFoundation、Nicheformer 和 Monod 都应被当作扩展分析。它们的 checkpoint、GPU、训练数据、版本和权重许可要单独登记；每次运行要和简单可解释 baseline（PCA/nearest-neighbor、edgeR/DESeq2 或经典 CellRank）比较。

## 适合 APAP/IR/CRLM 项目的组合

1. bulk RNA-seq：沿用 `rnaseq-analysis-template` 的 edgeR QL 主分析；这些近期方法主要作为单细胞、转录本和解释层补充。
2. 若有 full-length RNA-seq：先 Bambu，再 satuRn 做 transcript usage；报告 NDR、过滤、转录本版本和 biological replicate。
3. 若有 scRNA-seq：先变换和 feature selection 审计，再做整合；CellRank 2 仅在有明确状态变化假设时使用。
4. 若想尝试 foundation model：先把 checkpoint 和模型输出当作附加结果，不替代主统计模型；对小样本 APAP 研究尤其要避免把预训练 embedding 当作独立验证。

## 结果审计清单

- 输入矩阵是否为原始整数 count，行列方向是否明确？
- biological replicate、batch、condition 是否进入设计或分层验证？
- 过滤和 feature selection 是否在 reference/query 之间保持一致？
- 人鼠 ortholog、基因组版本、GTF 版本和 transcript version 是否记录？
- foundation model 是否记录 checkpoint URL、版本、SHA-256、显存和推理参数？
- 是否保存完整结果、失败日志、软件版本和可重复命令？
