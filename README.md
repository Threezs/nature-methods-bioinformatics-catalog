# Nature Methods Bioinformatics Catalog

这是一个以 R 为主、兼有 Python 的近期生信方法工具箱。它的组织方式是“先按科研功能选方法，再按输入数据和证据等级决定是否运行”，不是把论文简单堆在一起。

## 先看这三个文件

1. [`docs/function_map.md`](docs/function_map.md)：按问题选择方法，例如预处理、轨迹、空间 niche、跨物种、长读长和 DTU。
2. [`docs/quickstart.md`](docs/quickstart.md)：从输入审计、环境记录到最小运行的完整步骤。
3. [`docs/project_layout.md`](docs/project_layout.md)：把方法模板接入 APAP、IR、CRLM 等真实科研项目的目录和证据结构。
4. [`docs/sample_level_reporting.md`](docs/sample_level_reporting.md)：把 CellRank、embedding 和 niche 的细胞级输出汇总回 sample/donor 实验单位。
5. [`templates/method_run_manifest.yml`](templates/method_run_manifest.yml)：每次运行要固定的输入、版本、checkpoint、baseline 和限制。
6. [`docs/environment_matrix.md`](docs/environment_matrix.md)：R、Python、GPU、参考文件和 checkpoint 的环境分层。

## 功能导航

| 我想解决的问题 | 入口 | 语言 | 输入 | 主要输出 | 推荐级别 |
|---|---|---|---|---|---|
| 先检查数据和样本关系 | `R/00_input_audit.R` / `python/00_input_audit.py` | R/Python | count 矩阵、metadata 或 AnnData | 输入审计报告和运行 manifest | 必做 |
| 把细胞级结果汇总回 sample/donor | `R/05_sample_level_summary.R` / `python/08_sample_level_summary.py` | R/Python | fate/embedding/niche 分数 + metadata | 样本级结果表 | 条件比较前必做 |
| 单细胞 count 如何变换 | `R/01_single_cell_transformations.R` | R | gene × cell 原始整数矩阵 | 多种变换矩阵、PCA-ready features | 主分析候选 |
| 整合前如何做特征排序 | `R/02_feature_selection_benchmark.R` | R | count、batch、细胞标签 | variance ranking；可选 scran HVG；分组候选表 | 主分析候选 |
| 细胞命运、pseudotime、velocity | `python/01_cellrank2_template.py` | Python | `.h5ad`、邻居图、pseudotime/velocity | fate probability、terminal state | 支持分析 |
| 细胞状态密度和时间连续化 | `python/09_mellon_template.py` | Python | 高维 cell representation，可选时间/样本 metadata | cell-state density、gene-change score、时间插值 | 探索/支持分析 |
| 预训练模型做 embedding/注释 | `python/02_scgpt_embedding_template.py` | Python | `.h5ad`、checkpoint | embedding、注释或扰动预测 manifest | 探索分析 |
| 大规模单细胞表示或药物反应 | `python/03_scFoundation_embedding_template.py` | Python | `.h5ad`、checkpoint、GPU | embedding、任务预测审计 | 探索分析 |
| 空间组织环境和 niche | `python/04_nicheformer_template.py` | Python | 空间或上下文单细胞数据 | niche embedding、context prediction | 探索/支持分析 |
| 多模态空间组学整合 | `python/10_miso_manifest.py` | Python | 对齐的空间组学模态，可选图像特征 | multimodal embedding、spatial clusters | 探索分析 |
| 比较多模态整合器 | `python/11_scmmib_manifest.py` | Python | 数据集 manifest、paired/unpaired/mosaic 任务 | accuracy、robustness、scalability | 评估工具 |
| 多任务多模态整合评估 | `python/12_scmultibench_manifest.py` | Python | 数据集 manifest、任务列表 | reduction/batch/clustering 等任务指标 | 评估工具 |
| nascent/mature 转录动力学 | `python/05_monod_template.py` | Python | nascent 和 mature counts | kinetic parameters、模型不确定性 | 专题分析 |
| 多物种整合和标签迁移 | `python/06_saturn_template.py` | Python | 多物种 AnnData、蛋白 embedding | 跨物种 embedding、标签迁移 | 探索分析 |
| 零样本细胞 embedding | `python/07_uce_manifest.py` | Python | AnnData、UCE checkpoint | zero-shot embedding manifest | 探索分析 |
| 长读长新转录本发现 | `R/03_bambu_long_read.R` | R | BAM、GTF、genome FASTA | novel/known transcript counts | 主分析候选 |
| transcript usage / DTU | `R/04_satuRn_dtu.R` | R | transcript counts、注释、重复样本 | DTU FDR、usage 结果 | 主/支持分析 |
| nanopore RNA 修饰检测评估 | `python/13_narmbench_manifest.py` | Python | nanopore reads、reference、chemistry | site-level detection、PR、定量审计 | 专题分析 |

完整的输入、限制、方法 ID 和官方代码见 [`catalog.csv`](catalog.csv)；功能机器可读规则见 [`config/function_taxonomy.yml`](config/function_taxonomy.yml)；通用模板见 [`data/utility_templates.csv`](data/utility_templates.csv)。

## 推荐的最短分析路径

```text
输入审计
  ↓
可解释 baseline（变换、PCA/HVG、经典统计模型）
  ↓
近期方法（CellRank、DTU、niche 或 foundation model）
  ↓
held-out/样本级评估
  ↓
证据分级和实验验证
```

对于 APAP/IR 小鼠单细胞，建议先运行 `00 → 01 → 02`，再根据是否有时间点、velocity 或明确状态先验决定是否使用 CellRank 2。对于 CRLM 空间问题，先做传统邻域或配体-受体 baseline，再把 Nicheformer 用作候选 niche 发现。对于长读长数据，先 Bambu，再 satuRn 做 DTU，并同时保留 gene-level 分析。

## 开箱即用约定

1. 原始数据永远保留；依赖轻的 baseline 先在 `data/mock/` 上做 smoke test，BAM/AnnData/checkpoint 方法按 `catalog.csv` 的运行状态接入真实格式。
2. 真实项目必须记录物种、基因组/注释版本、行列方向、sample/donor/batch/condition 和 biological replicate。
3. foundation model 只登记 checkpoint 的 URL、版本、SHA-256、许可和显存需求，不把大权重直接提交到 Git。
4. 所有近期方法都必须和一个可解释 baseline 使用相同的输入和评估分层；manifest 校验不等于模型推理完成。
5. 每个结果文件配一个说明：统计对象是什么、支持什么结论、不能支持什么结论、下一步如何验证。

## 运行示例

```bash
# Python：先做输入审计
python python/00_input_audit.py \
  --input data/mock/scrna_counts.csv \
  --output results/input_audit.json

# Python：CellRank 2 最小入口
python python/01_cellrank2_template.py \
  --input data/real/your_dataset.h5ad \
  --output results/cellrank2 \
  --kernel pseudotime

# Python：UCE 只生成可审计 manifest，不自动下载权重
python python/07_uce_manifest.py \
  --input-h5ad data/real/your_dataset.h5ad \
  --checkpoint models/uce_checkpoint.pt \
  --output results/uce_manifest.json
```

R 入口是可复用函数，示例见各脚本末尾和 [`docs/quickstart.md`](docs/quickstart.md)。细胞级方法的条件比较请先阅读 [`docs/sample_level_reporting.md`](docs/sample_level_reporting.md)。

## 近期方法范围

目录目前收录 16 个论文/评估条目和 4 个通用 R/Python 工具模板，覆盖 2021–2026 年的单细胞变换、feature selection、命运推断、cell-state density、foundation model、多模态空间组学、整合 benchmark、跨物种整合、长读长、DTU 和 nanopore RNA 修饰。新增的 Nature Methods 条目包括 Mellon、MISO、SCMMIB、scMultiBench 和 NaRMBench；它们目前都先生成可审计 manifest，实际模型/benchmark 运行仍需官方环境。

## 相关仓库

- [bioinformatics-methods-cookbook](https://github.com/Threezs/bioinformatics-methods-cookbook)：R 生信配方、edgeR/ORA/GSEA/TF activity 和近期方法索引。
- [bioinformatics-literature-workbench](https://github.com/Threezs/bioinformatics-literature-workbench)：论文、阅读卡片、BibTeX、claim 和证据记录。
- [rnaseq-analysis-template](https://github.com/Threezs/rnaseq-analysis-template)：APAP 24 h bulk RNA-seq 分析骨架。
- [research-evidence-notebook](https://github.com/Threezs/research-evidence-notebook)：把观察、解释、替代解释和验证实验分开保存。
- [research-project-index](https://github.com/Threezs/research-project-index)：所有科研仓库和当前阶段的总入口。

## 验证

```bash
python python/validate_manifest.py
python -m compileall -q python
```

GitHub Actions 会检查 catalog、Python 模板和 R 文件语法。R 方法需要在本地安装 R/Bioconductor 后运行；没有 R 环境时，至少先完成输入审计、配置检查和远程 CI 解析。
