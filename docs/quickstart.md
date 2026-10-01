# 15 分钟快速上手

目标是先把输入、环境和运行记录固定下来，再把真实数据接入正确的运行层级。这个仓库当前明确区分四种状态：`smoke-tested`（依赖轻、可用 mock 做基本检查）、`baseline-function`（函数代码和输入契约可检查）、`manifest-only`（只准备官方模型运行配置）、`integration-required`（需要真实 BAM/AnnData/checkpoint/参考文件）。不能把 manifest 或语法检查理解为模型推理已经完成。

## 1. 建议的项目目录

```text
my-project/
├── data/
│   ├── raw/                 # 原始矩阵、FASTQ/BAM、原始 AnnData
│   ├── reference/           # GTF、FASTA、ortholog 表、gene vocabulary
│   └── processed/           # 只保存可追溯的中间数据
├── config/
│   ├── project.yml          # 物种、版本、路径、对比和 checkpoint
│   └── samples.csv          # 一个样本一行，避免只用文件名推断分组
├── scripts/                 # 复制本仓库的入口并固定参数
├── results/                 # 表格、图、模型输出
├── logs/                    # 命令、版本、错误和运行时间
└── README.md                # 本项目的研究问题和结果解释
```

## 2. R 路径

适合表达变换、feature selection、Bambu、satuRn 和 PINNACLE 的可解释 PPI/network baseline。先安装与项目匹配的 R/Bioconductor 版本，并把 `sessionInfo()` 写入日志。

```r
source("R/00_input_audit.R")
source("R/01_single_cell_transformations.R")
counts <- as.matrix(read.csv("data/processed/counts.csv", row.names = 1, check.names = FALSE))
metadata <- read.csv("config/samples.csv", stringsAsFactors = FALSE)
audit_count_matrix(counts, require_integer = TRUE)
audit_metadata(metadata, expected_n = ncol(counts), id_column = "cell_id", expected_ids = colnames(counts))
panel <- run_transformation_panel(counts)
saveRDS(panel, "results/transformation_panel.rds")
writeLines(capture.output(sessionInfo()), "logs/R_sessionInfo.txt")
```

PINNACLE 的 R-first 参照可以直接使用 base R：

```r
source("R/06_protein_context_baseline.R")
edges <- read.delim("data/mock/protein_network.tsv", stringsAsFactors = FALSE)
write_ppi_network_baseline(edges, "results/ppi_network_baseline.csv")
```

说明：`R/01` 的 Pearson residuals 是透明的 Poisson 基线实现，用来比较几何变化，不声称替代所有专用残差模型。正式论文要报告具体变换、过滤和缩放规则。

## 3. Python 路径

适合 CellRank 2、Mellon、PHLOWER、foundation model、PINNACLE、SpatialData、scikit-bio、Nicheformer、MISO、SCMMIB、scMultiBench、NaRMBench、Monod、SATURN 和 UCE。先创建隔离环境，再记录 Python、包版本、网络版本和 checkpoint。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python python/00_input_audit.py --input data/processed/your_dataset.h5ad --output results/input_audit.json
python python/01_cellrank2_template.py --input data/processed/your_dataset.h5ad --output results/cellrank2 --kernel pseudotime
python python/07_uce_manifest.py --input-h5ad data/processed/your_dataset.h5ad --checkpoint models/uce_checkpoint.pt --output results/uce_manifest.json
python python/09_mellon_template.py --embedding results/pca_embedding.csv --metadata config/cell_metadata.csv --output results/mellon_manifest.json
python python/10_miso_manifest.py --omics data/processed/spatial_rna.csv data/processed/spatial_atac.csv --spot-metadata config/spot_metadata.csv --output results/miso_manifest.json
python python/11_scmmib_manifest.py --dataset-manifest templates/multimodal_dataset_manifest.csv --task paired --output results/scmmib_manifest.json
python python/12_scmultibench_manifest.py --dataset-manifest templates/multimodal_dataset_manifest.csv --tasks dimension_reduction clustering --output results/scmultibench_manifest.json
python python/13_narmbench_manifest.py --reads data/mock/narmbench_reads.fastq --reference data/mock/narmbench_reference.fa --chemistry both --output results/narmbench_manifest.json
python python/14_pinnacle_manifest.py --expression data/processed/your_dataset.h5ad --ppi-network data/reference/protein_network.tsv --context-metadata config/context_metadata.csv --task target_prioritization --output results/pinnacle_manifest.json
python python/15_phlower_manifest.py --modalities data/processed/rna.h5ad data/processed/atac.h5ad --cell-metadata config/cell_metadata.csv --root-label progenitor --task both --output results/phlower_manifest.json
python python/16_spatialdata_manifest.py --datasets data/processed/spatialdata.zarr --elements table image labels shapes --coordinate-system tissue --platform Xenium --output results/spatialdata_manifest.json
python python/17_scikit_bio_manifest.py --inputs data/processed/reads.fasta data/processed/metadata.tsv --operation sequence --format FASTA --output results/scikit_bio_manifest.json
python python/08_sample_level_summary.py --scores results/cellrank2/fate_probabilities.csv --metadata config/cell_metadata.csv --output results/cellrank2/fate_sample_level.csv
python -m pip freeze > logs/python_freeze.txt
```

foundation model、Mellon、PHLOWER、PINNACLE、SpatialData、scikit-bio、MISO、SCMMIB、scMultiBench、NaRMBench、SATURN 和 Monod 的 manifest 脚本不会偷偷下载权重、PPI 网络或启动训练；它们只核对输入并写出可审计的下一步。SpatialData 入口还会把元素类型、坐标系、平台和存储路径固定下来，但不会自动完成读写、配准或 segmentation；scikit-bio 入口会固定操作和格式，但不会自动决定实验设计或统计检验。这样可以避免把大文件、不可复现的网络下载和未经核对的模型许可混进主分析。需要真实推理、读写或 benchmark 时，按 `catalog.csv` 的 `execution_mode` 安装官方包并保留运行日志。

## 4. 换成真实数据前必须填的字段

在 `config/methods.yml` 或项目自己的配置中明确记录：

- 物种、基因组版本、GTF/FASTA 版本和 gene/transcript ID 规则；
- 原始矩阵是否为整数 count，行是 gene 还是 cell；
- sample、donor、batch、condition 和 biological replicate；
- 过滤阈值、feature selection 规则、随机种子和 contrast；
- checkpoint 下载地址、版本、SHA-256、显存、推理参数和许可证；
- 输出文件、失败日志、运行命令和软件版本。

## 5. 什么时候算“已经跑通”

- **smoke-tested：** 输入审计、mock CSV、manifest 和 CLI 参数检查都通过。
- **baseline-function：** R 函数可以在本地 R/Bioconductor 环境执行，且输出表符合预期。
- **integration-required：** Bambu、satuRn 和 CellRank 需要真实格式的输入，不能用当前两个 mock CSV 代替。
- **manifest-only：** scGPT、scFoundation、Mellon、PHLOWER、PINNACLE、SpatialData、scikit-bio、Nicheformer、MISO、SCMMIB、scMultiBench、NaRMBench、Monod、SATURN 和 UCE 当前只生成配置/审计文件，官方推理、读写或 benchmark 步骤要在固定环境中继续完成。

## 6. 结果解释的最低要求

每个结果文件旁边保存一个短说明，回答四个问题：

1. 这个结果的统计或模型对象是什么？
2. 输入数据的实验单位是什么？
3. 结果支持哪一个具体结论，不能支持哪一个结论？
4. 下一步需要什么独立验证？

例如，CellRank 的 fate probability 可以作为状态转移假设的证据，但不能单独证明细胞真的发生了谱系转换。对 APAP/IR 条件比较时，必须保留 sample/donor 字段并在样本层面汇总；foundation model 的 embedding 可以用于下游分类或相似度分析，但不能自动替代差异表达和样本级统计。
