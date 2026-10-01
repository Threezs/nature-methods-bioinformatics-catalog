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

Mellon 适合回答“高维单细胞表示中哪些状态区域稠密/稀疏、状态密度如何随时间连续变化”这类问题。先固定表示（例如 PCA 或 diffusion representation）和邻域参数，再把 density 与细胞类型、时间点和 sample/donor 对照；不要把 density 当作 lineage probability，也不要把低密度状态直接写成稀有细胞比例。

scGPT、scFoundation、Nicheformer、Monod、SATURN、UCE 和 PINNACLE 都应被当作扩展分析。当前目录中的这些入口主要生成并审计 manifest，实际模型推理仍需官方包、checkpoint、GPU/配置和版本锁定。每次运行要和简单可解释 baseline（PCA/nearest-neighbor、edgeR/DESeq2、PPI/network baseline 或经典 CellRank）比较。

PINNACLE 适合把 cell type、tissue 和蛋白互作网络放进同一个上下文表示框架，用于候选蛋白、靶点或药物的优先级排序。使用前必须固定表达矩阵/AnnData 的版本、PPI 网络来源和版本、上下文标签粒度、checkpoint 哈希以及下游任务的 held-out split。结果是 context-aware representation 或 prioritization score，不能单独证明蛋白的因果功能、药物疗效或跨组织可迁移性。

MISO 和 SCMMIB 面向多模态场景。MISO 的第一步不是下载权重，而是确认所有模态共享 spot/cell key、坐标系和预处理版本；SCMMIB 用来按 paired/unpaired/mosaic 任务记录 accuracy、robustness、scalability，而不是替代一个具体整合器。MISO 当前官方仓库要求 Python 3.7 和 Git-LFS，因此目录只生成 manifest，不把旧环境伪装成已复现。

scMultiBench 是 SCMMIB 的互补路线：它把 dimension reduction、batch correction、clustering、classification、imputation、feature selection 和 spatial registration 分开评估，并区分 vertical/diagonal/mosaic/cross 结构。使用时先选定任务和 split，再报告任务级指标，不能把多个任务压成一个“最佳方法”。

NaRMBench 放在长读长 RNA 专题，而不是常规转录本定量路径。它用于比较 nanopore direct-RNA 修饰检测工具和 retraining 方案；RNA002/RNA004 chemistry、ground truth、重训练样本和 site-level calibration 都必须记录。结果只能支持“检测工具在该 chemistry/数据条件下的表现”，不能直接写成全转录组修饰机制。

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
