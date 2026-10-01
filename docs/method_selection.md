# 方法选择和边界

## R-first 路径

### 单细胞预处理

先用 `R/01_single_cell_transformations.R` 比较至少两种变换，再固定一种进入 PCA、邻居图和整合。推荐把原始整数矩阵永远保留，并记录 library size、过滤规则、变换、缩放和随机种子。shifted-log、log1p-CPM 和 Pearson residuals 解决的问题不同，不能只按 UMAP 好看来选。

### 整合和 query mapping

`R/02_feature_selection_benchmark.R` 默认提供透明的方差排序和分组均值效应 baseline；它不等同于完整的 HVG 模型，也不替代 replicate-aware 差异表达。需要正式 HVG 时，使用脚本中的 `select_hvg_scran()`，先按 scran/scuttle 规则准备 `SingleCellExperiment` 和 logcounts。大规模 atlas 或 reference/query 项目，先固定 feature-selection 规则，再比较 Harmony、scVI 或 Seurat 等整合器；不要在每个 query 上重新挑一套特征。

### 长读长和转录本层面

Bambu 适合从已比对的长读长 BAM 中做 context-aware transcript discovery/quantification。satuRn 适合在 transcript counts 已经可靠的前提下做 DTU。两者都需要 transcript-to-gene 关系、参考版本和样本级重复；单个样本不能支持可靠的组间推断。

## Python/模型路径

CellRank 2 应该在已有 kNN 邻居图、pseudotime、RNA velocity 或时间点信息后使用。先检查不同 kernel 的 terminal states 和 fate probabilities 是否稳定，再把 lineage-correlated genes 当作候选机制线索。若要比较 APAP/IR 条件，必须保留 `sample_id`/`donor_id`，先在样本层面汇总 fate probability 或 terminal-state proportion，再做组间比较；细胞级输出不能直接当作独立重复。

scGPT、scFoundation、Nicheformer、Monod、SATURN 和 UCE 都应被当作扩展分析。当前目录中的这些入口主要生成并审计 manifest，实际模型推理仍需官方包、checkpoint、GPU/配置和版本锁定。每次运行要和简单可解释 baseline（PCA/nearest-neighbor、edgeR/DESeq2 或经典 CellRank）比较。

## 适合 APAP/IR/CRLM 项目的组合

1. bulk RNA-seq：沿用 `rnaseq-analysis-template` 的 edgeR QL 主分析；这些近期方法主要作为单细胞、转录本和解释层补充。
2. 若有 full-length RNA-seq：先 Bambu，再 satuRn 做 transcript usage；报告 NDR、过滤、转录本版本和 biological replicate。
3. 若有 scRNA-seq：先变换和 feature selection 审计，再做整合；CellRank 2 仅在有明确状态变化假设时使用。
4. 若想尝试 foundation model：先把 checkpoint 和模型输出当作附加结果，不替代主统计模型；对小样本 APAP 研究尤其要避免把预训练 embedding 当作独立验证。

## 结果审计清单

- 输入矩阵是否为原始整数 count，行列方向是否明确？
- biological replicate、batch、condition 是否进入设计或分层验证？
- 过滤和 feature selection 是否在 reference/query 之间保持一致？R/02 的方差排序是否被误写成正式 HVG？
- 人鼠 ortholog、基因组版本、GTF 版本和 transcript version 是否记录？
- foundation model 是否记录 checkpoint URL、版本、SHA-256、显存和推理参数？
- 细胞级 fate/embedding 结果是否按 sample/donor 汇总并做跨重复稳定性检查？
- 是否保存完整结果、失败日志、软件版本和可重复命令？
