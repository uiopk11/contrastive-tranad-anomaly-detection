# 环境与运行指南

## 先检查代码副本

```bash
python -X utf8 scripts/verify_repository.py
python -X utf8 scripts/show_results.py
```

以上只需要 Python 标准库，检查语法、notebook 输出清理、文件清单与保存的指标记录；不会训练模型。

## 配置环境

历史来源未保存完整环境锁文件。本仓库不把上游旧版安装命令标成当前已验证环境。建议为此项目单独创建虚拟环境；先按操作系统和硬件从 [PyTorch 官方安装页](https://pytorch.org/get-started/locally/) 选择 PyTorch，再安装项目依赖：

```bash
python -m pip install -r requirements.txt
```

依赖版本是待验证范围而非精确锁定。基础源码顶层导入 DGL，即使只用 TranAD 也会触发该依赖。历史 notebook 曾使用 `torchdata==0.7.1` 解决 `torchdata.datapipes` 导入问题，但 DGL、GraphBolt、PyTorch、Python 的二进制兼容仍需单独核对；不要认为安装一个包能解决所有版本组合。

清理版 notebook 已移除自动 pip 安装行为。PyTorch 2.x 的 `is_causal` 参数适配仍在 notebook 中保留；不要在同一内核重复运行 monkey patch 单元。NumPy 2.x 不支持历史代码的 `ndarray.ptp()`，因此依赖约束暂设 `numpy<2`。

本次仅做静态验证和保存指标核对，未安装完整训练环境、未运行 WADI/SMAP/SMD 训练。

## 设置路径并启动

PowerShell 示例，在仓库根目录：

```powershell
$env:TRANAD_ROOT = (Resolve-Path .\TranAD).Path
$env:WADI_DATA_ROOT = 'D:\datasets\WADI.A2_19 Nov 2019'
python -m jupyterlab
```

其他系统设置等价环境变量。WADI 路径需换成自己的数据目录。打开 `notebooks/` 下入口后，从首个单元开始顺序运行。内核工作目录通常是 notebook 所在目录；若手动改变目录，应始终设置绝对 `TRANAD_ROOT` 和 `WADI_DATA_ROOT`。

## 推荐实验顺序

1. 用新内核运行 `01_tranad_wadi.ipynb`，检查数据形状、标签比例和基础分数。
2. 在另一份独立实验副本、新内核中运行 `02_frozen_cl_wadi.ipynb`。先基线、再冻结投影头、再固定 α=0.10 的融合。
3. α 搜索和后续最优值展示属于测试集探索；需要独立结果时，另划验证集选参并冻结所有选择，再评估未使用的测试集。
4. 运行 `03_joint_cl_negative_case.ipynb` 时也用独立副本和新内核，它会更改主干。
5. SMAP / SMD 分别使用 `04` / `05`，注意默认只覆盖一个实体。

`06`—`10` 是另外的 Transformer 系列实验，不共享上述精确协议。`11` 需要已有 `model`、loader、标签与打分变量；`12` 需要先生成 `baseline_scores_and_labels.npz`。它们适合在相同内核完成前序实验后探索，或手动加载相同协议的产物。

## 保存自己的复现实验

记录软件版本、数据来源与哈希、随机种子、切分、实体、训练行数、降采样、归一化统计量、阈值规则、参数选择数据集和指标定义。把本次新实验输出与 `results/historical/` 分开保存；后者仅代表原文件中保存过的 stdout。
