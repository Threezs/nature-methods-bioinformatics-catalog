# 把方法目录变成可复用科研项目

建议把本仓库作为“方法层”，把真实数据和论文结论放在独立项目仓库。这样同一个方法可以服务 APAP、IR、CRLM 和其他项目，不会因为换数据而覆盖原始证据。

## 三层结构

```text
项目仓库
├── 研究问题层：假设、主要终点、对比、样本和排除标准
├── 分析方法层：本仓库的 R/Python 入口、参数和环境
└── 证据解释层：结果表、图、论文 claim、限制和实验验证
```

### 研究问题层

在项目 README 开头写出一句可检验的问题，例如“APAP 24 h 是否改变肝细胞到中性粒细胞募集相关的状态程序”。随后固定主要比较、观察单位、重复和排除规则。不要先跑模型再从图里挑问题。

### 分析方法层

每次运行都保存：入口脚本、配置文件、软件版本、随机种子、输入文件哈希、输出文件清单和失败日志。方法目录只提供模板，不替项目决定样本量、对比或生物学解释。

### 证据解释层

把结果分成主分析、支持分析、探索分析和待验证假设。对于人鼠映射、先验网络、foundation model 和配体-受体结果，单独记录映射规则和证据等级。

## 推荐的最小文件

```text
README.md
config/project.yml
config/samples.csv
scripts/run_input_audit.R
scripts/run_method.R
results/tables/
results/figures/
logs/
evidence/claims.csv
evidence/references.bib
```

## `claims.csv` 最少字段

```text
claim_id,claim,source_result,evidence_level,alternative_explanation,next_validation,status
C001,APAP increases a hepatocyte stress program,results/tables/program_activity.csv,support,cell-composition shift,protein assay,open
```

这张表把“观察到的结果”和“准备写进论文的结论”分开，特别适合管理 STAT3、NF-κB、SAA、S100A8/A9、LCN2 等机制链条。

