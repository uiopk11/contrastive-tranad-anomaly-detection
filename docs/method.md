# 方法与代码导览

## 基础模型

`TranAD/src/models.py` 中的 `TranAD` 使用两阶段重构。第一阶段将窗口与零条件拼接后编码，产生重构；第二阶段把第一阶段平方误差作为条件，再编码并重构。训练损失由 `TranAD/main.py::backprop` 实现。

`convert_to_windows` 在时间索引 i 使用 i 之前的窗口，不含当前点；序列开头重复首行补齐。模型目标是窗口末行。因此应结合训练与打分代码理解索引，不能把窗口起点、窗口末点和原序列当前点混用。该历史行为在整理中保留。

## 冻结主干的对比增强

主入口为 `notebooks/02_frozen_cl_wadi.ipynb`。完成基线训练和评估后，冻结全部 TranAD 参数并设为 eval 模式，仅训练投影头。

1. 对同一正常训练窗口生成两个增强视图：高斯噪声 σ=0.01、按特征缩放 σ=0.05、遮蔽约 5% 特征。
2. 取 `model.encode` 返回的 memory，在时间维平均池化。
3. 投影头为 Linear → ReLU → Linear，输出 128 维向量。
4. 用归一化表示计算对称 InfoNCE；同一样本的两个视图是正对，同批其他样本作为负对。
5. 历史设置为 5 个 epoch、batch size 256、学习率 8e-4、temperature 0.2。

令训练归一化表示的均值再归一化为中心 c，对比异常分数为：

```text
s_cl(x) = 1 - cosine(z(x), c)
aligned_cl = (s_cl - mean_train_cl) / std_train_cl * std_train_base + mean_train_base
s_fused = (1 - alpha) * s_reconstruction + alpha * aligned_cl
```

中心和分数对齐统计量均来自训练序列。WADI 的初始融合权重为 0.10，后续 notebook 单元还进行 α=0.00…0.40、步长 0.02 的搜索。该搜索使用测试标签评价 F1，属于探索。

## 直接联合训练

`03_joint_cl_negative_case.ipynb` 保留重构损失与对比损失联合优化的历史路径。它会更新主干，必须在独立内核、独立基线模型上运行。不要先运行它再声称后续实验的主干仍是原基线。

清理版 `02_frozen_cl_wadi.ipynb` 已移除这个可选联合训练单元，避免“运行全部”时先改变主干再冻结。原保存输出仍仅作为历史证据，不因这个整理改动而自动获得新的有效性。

## 其他入口

- `04_frozen_cl_smap.ipynb`：SMAP P-1 的冻结主干和 α 搜索。
- `05_frozen_cl_smd.ipynb`：SMD machine-1-1 的对应流程。
- `06_transformer_baseline.ipynb`：独立 Encoder–Decoder 重构基线及平滑、段约束。
- `07_contrastive_transformer.ipynb`：独立 Transformer 加对比投影与联合损失。
- `08_contrastive_ablation.ipynb`：对比权重、增强和聚合方式探索；运行前检查训练/评估批次数限制。
- `09_two_stage_transformer_cl.ipynb`、`10_two_stage_transformer_cl_grid.ipynb`：独立两阶段模型变体，不等同于原 TranAD。
- `11_score_quantile_scan.ipynb`、`12_postprocess_search.ipynb`：依赖前序变量或生成分数文件的辅助实验，不能当独立完整训练入口。

各 notebook 有各自的数据处理与超参数，数字不能跨入口直接排名。
