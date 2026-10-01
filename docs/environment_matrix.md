# 环境和资源矩阵

近期方法的依赖不能全部塞进一个环境。最稳妥的做法是：一个轻量验证环境、一个 R/Bioconductor 环境、一个 CellRank 环境，以及每个 foundation model 按官方仓库固定的独立环境。

| 功能/方法 | 建议环境 | 典型资源 | 外部文件 | 入口状态 |
|---|---|---|---|---|
| 输入审计和 sample summary | Python 标准库；R base | CPU、内存低 | CSV/TSV、metadata | 可直接 smoke test |
| 变换和透明 feature ranking | R + base；正式 HVG 加 scran/scuttle | CPU | raw count、batch | baseline-function |
| Bambu | R + Bioconductor bambu | 依 BAM 大小而定 | genome-aligned BAM、GTF、FASTA | 需要参考文件 |
| satuRn | R + Bioconductor satuRn、limma、SummarizedExperiment | CPU/多核 | transcript counts、tx2gene、重复样本 | 需要 transcript 输入 |
| CellRank 2 | Python + scanpy + cellrank + scvelo（若用 velocity） | CPU 可运行；大数据建议更多内存 | h5ad、neighbors、pseudotime 或 Ms/velocity layers | runtime-required |
| Mellon | 官方 Python Mellon 环境 | CPU/GPU 取决于 representation 和细胞数 | 高维 cell representation、可选时间 metadata | 当前只生成 manifest |
| scGPT/scFoundation | 官方 Python 环境 | 通常需要 GPU/大内存 | h5ad/counts、checkpoint | 当前只生成 manifest |
| Nicheformer | 官方 Python 环境 | GPU 推荐 | spatial/context AnnData、checkpoint | 当前只生成 manifest |
| MISO | 官方仓库 Python 3.7 环境；Git-LFS | 小于万 spot 的训练可先 CPU/GPU 试跑；图像特征提取更重 | 多模态空间数据、对齐图像特征、ViT 权重 | 当前只生成 manifest |
| SCMMIB | 官方 benchmark/pipeline 环境 | 依任务规模而定，需记录 CPU/GPU/内存 | paired/unpaired/mosaic 数据集和任务清单 | 当前只生成 manifest |
| scMultiBench | 官方 scMultiBench 环境 | 多任务 benchmark 需记录 CPU/GPU/内存和 split | multimodal datasets、任务清单和评估配置 | 当前只生成 manifest |
| NaRMBench | 官方 nanopore/修饰工具环境 | basecalling/alignment/retraining 可能需要 GPU、大磁盘和长运行时间 | direct-RNA reads、reference、RNA002/RNA004、ground truth | 当前只生成 manifest |
| Monod | 官方 monod + monod_examples 环境 | CPU/GPU 取决于拟合规模 | nascent/mature 数据、官方 config | 当前只生成 manifest |
| SATURN | 官方 SATURN 环境 | GPU、较大内存 | 多物种 AnnData、protein embeddings | 当前只生成 manifest |
| UCE | 官方 UCE 环境 | GPU 推荐 | AnnData、checkpoint、gene/protein vocabulary | 当前只生成 manifest |

## 建议的环境分层

### A. 轻量验证环境

只用于检查 CSV、metadata、manifest、目录和参数，不安装大模型：

```bash
python -m venv .venv
source .venv/bin/activate
python python/validate_manifest.py
make smoke-python
```

### B. R/Bioconductor 环境

在项目仓库中用 `renv` 锁定 R、CRAN 和 Bioconductor 版本。正式使用 Bambu 或 satuRn 前，先把 package version、Bioconductor release 和 `sessionInfo()` 写入日志。

```r
renv::init()
BiocManager::install(c("scran", "scuttle", "bambu", "satuRn"))
renv::snapshot()
```

### C. Python 方法环境

CellRank、scGPT、scFoundation、Nicheformer、Monod、SATURN 和 UCE 的依赖可能互相冲突。按官方仓库的 `environment.yml`、`requirements.txt` 或安装说明单独建环境，不要为了方便把所有模型装在一个环境里。

## 每次运行都要记录

- `python --version` 或 `R.version.string`；
- 完整包列表：`pip freeze`、`conda env export` 或 `renv.lock`；
- 官方仓库的 commit/tag；
- checkpoint 下载地址、版本、SHA-256 和许可证；
- GPU 型号、显存、CPU 核数和随机种子；
- 输入文件哈希、输出文件清单和失败日志。

只要其中一个字段缺失，就把结果标为“不可完全复现”，不要只根据图形外观宣称已经复现论文方法。
