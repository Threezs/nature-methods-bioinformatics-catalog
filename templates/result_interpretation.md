# 结果解释卡片

## 结果身份

- method_id:
- run_manifest:
- input_hash:
- output_file:
- software/checkpoint:

## 观察到的结果

用可复核的数值或文件描述结果，不先写机制结论。

## 支持的最小结论

这个结果最多支持什么？例如“某状态分数在 APAP 样本中升高”或“模型把这些细胞映射到相似 embedding 区域”。

## 不能直接推出的结论

记录不能由该分析单独证明的内容，例如因果关系、蛋白磷酸化、真实谱系转换或配体直接作用。

## 替代解释

- 细胞组成变化；
- batch、donor 或测序深度差异；
- reference/query feature mismatch；
- 先验网络或 checkpoint 域偏移；
- 统计模型与实验单位不一致。

## 下一步验证

- sample/donor-level re-analysis；
- orthogonal assay；
- perturbation 或 co-culture；
- 独立数据集复现；
- 预先定义的 held-out benchmark。

