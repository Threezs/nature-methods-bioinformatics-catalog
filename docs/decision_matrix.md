# 方法决策矩阵

`data/method_decision_matrix.csv` 把每个条目压缩成五个使用前问题：科研问题是什么、真正的实验单位是什么、应该和什么 baseline 比、需要什么资源/证据、以及明确不能回答什么。

## 使用规则

1. 先按问题筛选，不按“模型最新”筛选。
2. `experimental_unit` 决定统计汇总层级。细胞级模型输出通常要回到 sample/donor/section/replicate 后才能进入条件比较。
3. `baseline` 不是装饰项；没有 baseline 就无法判断近期模型是否真的增加信息。
4. `minimum_evidence` 是运行前的硬门槛。缺少 checkpoint、reference、chemistry 或 shared key 时，保持 `manifest-only`。
5. `not_for` 是结果解释边界，写进阅读卡片和结果说明，避免把预测/聚类/benchmark 排名升级为机制结论。

## 典型选择

| 数据/问题 | 首选路线 | 第二步 |
|---|---|---|
| APAP/IR scRNA-seq | input audit → transform → feature selection | 有时间/velocity 先验再用 CellRank；状态密度问题再用 Mellon |
| CRLM 空间组学 | input audit → spatial baseline | Nicheformer 或 MISO；多模态选择用 SCMMIB/scMultiBench |
| 长读长转录组 | Bambu transcript discovery | satuRn DTU；若是 direct-RNA 修饰则转 NaRMBench |
| 跨物种 atlas | ortholog/reference audit | SATURN/UCE，并报告 protein/vocabulary coverage |
| 蛋白靶点和药物优先级 | expression + PPI + context metadata audit | PINNACLE；报告网络版本、上下文分层和 held-out 指标 |
| 多模态复杂分支轨迹 | shared cell ID + root/direction audit | PHLOWER；与 CellRank/graph baseline 比较 branch stability |
| 跨平台空间组学 | element/coordinate/unit/serialization audit | SpatialData；再进入 Nicheformer、MISO 或传统空间邻域分析 |

矩阵只用于形成可审计的候选方案；最终结果仍需项目自己的样本量、重复、外部验证和实验设计支持。
