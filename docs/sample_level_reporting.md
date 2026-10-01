# 细胞级方法如何回到样本级结论

CellRank、embedding、niche prediction 和细胞比例都是以细胞为单位输出的。APAP、IR 或 CRLM 的条件比较通常以动物、患者或 donor 为实验单位，不能把数千个细胞直接当成数千个独立重复。

## 最低数据要求

每个细胞至少要有：

- `sample_id` 或 `donor_id`；
- `condition`；
- `batch`（如果有）；
- 细胞类型或状态标签；
- 方法输出，例如 fate probability、embedding score 或 niche score。

## CellRank fate probability 的样本级汇总

先将 `fate_probabilities.csv` 与细胞 metadata 按 cell ID 合并，然后按 sample/donor 汇总均值、中位数或预先定义的阳性比例。组间统计使用样本级表，而不是原始细胞行。

```r
fate <- read.csv("results/cellrank2/fate_probabilities.csv", row.names = 1, check.names = FALSE)
meta <- read.csv("config/cell_metadata.csv", stringsAsFactors = FALSE)
source("R/05_sample_level_summary.R")
sample_level <- summarize_cell_scores(fate, meta)
write.csv(sample_level, "results/cellrank2/fate_sample_level.csv", row.names = FALSE)
```

Python 的无 pandas 版本是 `python/08_sample_level_summary.py`，可以直接处理 CellRank 导出的 CSV。

如果只有两个或三个 sample，样本级估计会很不稳定；应该把结果写成效应方向和不确定性，并用独立实验验证，而不是只报告细胞级 P 值。

## embedding 和 niche score

embedding 本身通常不是直接的组间检验对象。先固定下游任务，例如：

1. reference/query label transfer 的 macro-F1、balanced accuracy 或 held-out accuracy；
2. 同一 sample 内的细胞状态比例或预先定义的 score；
3. donor-level 的分类/回归模型，明确协变量和交叉验证方式。

Nicheformer 或其他空间模型的输出要保留 spot/cell ID、切片、患者/动物和坐标；先检查同一 donor 内的空间重复，再解释组间差异。

## 报告表的最少字段

```text
sample_id,donor_id,condition,batch,n_cells,method_output,summary_rule,uncertainty,validation_status
S01,M01,Control,B1,320,0.18,mean,future,open
```

这个文件应与方法输出、运行 manifest 和结果解释文件放在同一个 `results/` 子目录，保证任何一个结论都能追溯到样本级数据。
