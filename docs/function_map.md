# 按科研功能选择方法

这个目录按“我现在要回答什么问题”组织，而不是按论文发表年份组织。先确认研究问题，再确认输入数据和实验单位，最后选择方法。方法的热图、UMAP 或 embedding 不能替代实验设计和样本级统计。

## 一张选择表

| 科研功能 | 你手里的数据 | 首选入口 | 备用/扩展 | 主要输出 | 什么时候不要用 |
|---|---|---|---|---|---|
| 输入审计和样本关系检查 | count 矩阵、metadata、AnnData | `R/00_input_audit.R` 或 `python/00_input_audit.py` | 手工检查 library size、重复和缺失值 | 可审计的输入报告 | 没有样本级信息时不要直接进入组间推断 |
| 单细胞表达变换 | 原始 gene × cell 整数矩阵 | `R/01_single_cell_transformations.R` | log1p-CPM、shifted-log、Pearson residuals 并行比较 | PCA-ready matrix、变换比较报告 | 不要根据 UMAP 外观单独决定变换 |
| 特征排序、可选正式 HVG 和分组候选 marker | count 矩阵、batch、细胞标签 | `R/02_feature_selection_benchmark.R` | 默认透明 variance ranking；可选 `select_hvg_scran()` | feature table、选择分数 | 默认函数不是 replicate-aware DE；不要把均值效应写成机制证据 |
| 轨迹、命运和终末状态 | `.h5ad`、邻居图、pseudotime 或 velocity | `python/01_cellrank2_template.py` | CellRank 2 的多 kernel 比较 | fate probabilities、terminal states | 没有状态变化先验时不要把 fate probability 当成事实 |
| 细胞状态密度和时间连续化 | 高维 cell representation，可选时间点/样本 metadata | `python/09_mellon_template.py` | diffusion/PCA 表示上的密度 baseline | cell-state density、gene-change score、时间连续化 | 密度是表示空间中的占据，不是因果 lineage 或细胞比例 |
| 多模态复杂分支轨迹 | 两种以上共享 cell ID 的模态、cell metadata、可选 root/terminal labels | `python/15_phlower_manifest.py` | CellRank、graph/trajectory baseline | trajectory/edge-flow embeddings、分化树、候选调控因子 | 没有方向、根节点或跨模态对齐时，不要解释成已证实谱系 |
| 预训练 embedding、注释和扰动预测 | `.h5ad`/表达矩阵、checkpoint | `python/02_scgpt_embedding_template.py` | scFoundation、UCE | embedding、annotation 或 perturbation prediction | 小样本时不能把 embedding 当作独立统计证据 |
| 大规模单细胞表示和药物反应 | `.h5ad`、模型权重、GPU | `python/03_scFoundation_embedding_template.py` | scGPT、PCA/scVI baseline | embedding、任务预测 | 没有固定 checkpoint、显存和 baseline 时不宜直接用于论文主结论 |
| 单细胞/组织上下文的蛋白表示和靶点优先级 | 表达矩阵/AnnData、PPI 网络、cell-type/tissue metadata | `python/14_pinnacle_manifest.py` | PPI/network baseline、任务特异分类/排序模型 | context-aware protein/cell representation、target/drug prioritization | 网络版本、上下文标签或 held-out 评估缺失时，不要解释成因果蛋白功能或疗效 |
| R 版 PPI/network 可解释基线 | PPI edge table（可带权重） | `R/06_protein_context_baseline.R` | 节点 degree、weighted degree、任务特异排序 | protein degree/weighted-degree 表 | 没有 protein-level context 标签时不能冒充上下文模型 |
| 空间 niche 和组织环境 | 空间转录组或带空间上下文的单细胞数据 | `python/04_nicheformer_template.py` | 传统邻域统计、空间配体-受体分析 | niche embedding、context prediction | 域偏移明显或没有空间验证时只能作为探索结果 |
| 多模态空间组学整合 | 共享 spot/cell key 的多种空间组学和图像特征 | `python/10_miso_manifest.py` | MISO 与传统 modality-specific clustering | multimodal embedding、spatial clusters | 模态未对齐、坐标约定不一致或旧环境无法固定时不要运行 |
| 空间数据结构和跨平台互操作 | SpatialData/Zarr、表、图像、labels、shapes、points | `python/16_spatialdata_manifest.py` | 平台原生 reader、坐标/配准 QC | 统一元素、坐标变换和读写审计 | 不能自动修复分割、配准、单位或生物混杂；先完成元素与坐标审计 |
| 通用序列/表格/距离/多样性/系统发育工具 | FASTA/FASTQ、BIOM/TSV、metadata、distance matrix 或 Newick | `python/17_scikit_bio_manifest.py` | assay-specific parser、统计 baseline 和样本级设计 | 格式感知对象、距离/多样性/分类/系统发育输出 | 不要把通用算法默认成实验设计或生物机制；先固定输入格式和 metadata |
| 空间域聚类和方法共识 | 多平台空间数据、聚类输出、坐标、方法配置、可选 expert labels | `python/18_saccelerator_manifest.py` | 平台原生聚类、ARI/NMI 与 CHAOS/PAS/entropy 并行比较 | 跨数据集指标、共识聚类、方法分歧和专家复核区域 | 手工标签不自动是真值；不能把共识或高分直接写成组织机制 |
| 空间 foundation model、域和组织架构 | 空间转录组/AnnData、可选 gene panel、checkpoint 和批次信息 | `python/19_novae_manifest.py` | 空间邻域/domain baseline、held-out section、marker/图像验证 | spot/cell domain、SVG/pathway、批次校正表示和组织架构摘要 | 没有 registration、panel coverage、batch split 或正交 marker 验证时不要写成稳定组织机制 |
| 多模态、空间和速度数据模拟 | cell differential tree、GRN、可选空间交互和 batch 参数 | `python/20_scmultisim_manifest.py` | 负/正模拟、经验 sanity check 和固定 benchmark split | paired RNA/ATAC、spliced/unspliced、空间位置及已知 truth | 模拟参数和真实数据不匹配时，不要把 benchmark 排名外推成真实组织结论 |
| 选择多模态整合器 | paired、unpaired 或 mosaic 数据集清单 | `python/11_scmmib_manifest.py` | SCMMIB benchmark | accuracy、robustness、scalability | benchmark 排名依赖任务和模态，不能直接视为普适排名 |
| 多任务多模态整合评估 | 数据集清单和一个或多个任务 | `python/12_scmultibench_manifest.py` | scMultiBench | reduction、batch、clustering、classification、imputation、feature selection、spatial registration 指标 | 任务、模态、数据集和 split 不同，不能只引用一个总排名 |
| nascent/mature 转录动力学 | nascent 与 mature count 矩阵、官方 config | `python/05_monod_template.py` | 先做数据匹配和模型比较；当前入口只生成 manifest | kinetic parameters、uncertainty（由官方包产生） | 不能当作常规 bulk DE 或普通 RNA velocity 的直接替代 |
| 跨物种整合和标签迁移 | 多物种 AnnData、蛋白 embedding | `python/06_saturn_template.py` | UCE；先做 ortholog/QC 审计 | universal embedding、跨物种标签 | 基因同源关系和蛋白覆盖率没有记录时不要解释跨物种差异 |
| 零样本跨物种 embedding | AnnData、UCE checkpoint、基因/蛋白词表 | `python/07_uce_manifest.py` | SATURN、经典 reference mapping | zero-shot embedding、annotation transfer | checkpoint、词表覆盖和物种元数据缺失时不能复现 |
| 长读长转录本发现和定量 | BAM、GTF、genome FASTA | `R/03_bambu_long_read.R` | 记录参考版本和比对参数 | novel/known transcript counts | BAM、GTF 和 genome 不匹配时不要运行 |
| transcript usage / DTU | transcript counts、transcript-to-gene、重复样本 | `R/04_satuRn_dtu.R` | 基因层面 DE 作为并行分析 | DTU FDR、usage plot | 单个样本或每个基因只有一个 isoform 时不支持可靠 DTU |
| nanopore RNA 修饰检测 | direct-RNA reads、reference、chemistry | `python/13_narmbench_manifest.py` | NaRMBench 的 preprocessing/retraining/evaluation | site-level detection、PR、quantification、biological validity | RNA002/RNA004、训练数据和非 m6A 修饰的校准不能混为一谈 |

## 推荐的决策顺序

1. **先判定数据层级。** 只有 bulk count 时，优先使用现有 RNA-seq 主分析仓库；本目录主要补充单细胞、转录本和模型解释层。
2. **先做输入审计。** 确认行列方向、原始 count、样本/细胞 ID、batch、condition、物种、基因组版本和参考文件彼此一致。
3. **先用可解释方法建立基线。** 例如 log1p-CPM + PCA、HVG + classical integration、gene-level DE 或普通邻域统计。
4. **再加入近期方法。** 近期方法必须和 baseline 使用相同的输入、分层方式和评估指标，并保留 checkpoint、随机种子和软件版本。先查看 `catalog.csv` 的 `execution_mode` 和 `validation_status`，不要把 manifest 校验误读成模型已经完成推理。
5. **最后解释生物学。** 先写清楚方法输出是什么，再写“它支持哪一种生物学解释”；embedding 相似度、fate probability 和预测分数都不是实验验证。

## 针对常见项目的最短路径

### APAP/IR 小鼠单细胞

`00_input_audit → 01_transformations → 02_feature_selection → classical integration → CellRank 2（仅在有时间/velocity/状态先验时） → Mellon（需要状态密度/连续时间问题时）`。如果需要人鼠比较，再把 SATURN 或 UCE 作为扩展结果，并单独报告 ortholog 覆盖率。CellRank/Mellon 输出应按 sample/donor 汇总后再进行条件比较。

### CRLM 肿瘤微环境和空间问题

`00_input_audit → SpatialData 元素/坐标审计 → 01_transformations → 02_feature_selection → Nicheformer/MISO/Novae 或传统空间邻域分析 → 配体-受体/通路验证`。SpatialData 负责跨平台元素和坐标的可追踪组织，不代替 segmentation/registration QC；Nicheformer/MISO/Novae 的输出用于发现候选 niche、空间域和架构特征，不能单独证明配体直接改变了某个程序；多模态整合前先运行 SCMMIB 任务/数据集清单审计。

### 长读长或转录本机制

`Bambu transcript discovery/quantification → transcript QC → satuRn DTU → gene-level DE 和蛋白/功能验证`。每一步都要记录参考版本、转录本过滤、样本重复和 contrast。

### foundation model 试用

`baseline → input audit → checkpoint/network manifest → model inference → held-out evaluation → biological validation`。如果模型只产生 embedding，就必须预先定义下游任务和评价指标，不能只展示 UMAP。PINNACLE 还要把 PPI 网络版本和上下文标签粒度纳入审计。

## 结果分级建议

- **主分析：** 有明确实验设计、样本级重复、可解释统计模型和完整 QC 的结果。
- **支持分析：** 与主分析方向一致、但依赖模型或较强先验的结果，例如 CellRank fate probability、DTU 或空间 niche。
- **探索分析：** foundation model embedding、跨物种 zero-shot transfer、checkpoint 依赖的预测。
- **待验证假设：** 仅由相关性、embedding 相似度、富集分数或先验网络支持的机制。
