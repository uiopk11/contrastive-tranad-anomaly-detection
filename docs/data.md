# 数据与路径

仓库不分发原始数据、预处理传感器数组或模型权重。使用者需从数据提供方取得授权并按其条款使用。

## WADI

入口使用 WADI.A2_19 Nov 2019 对应的正常训练 CSV 与含点级标签的测试 CSV：

```text
<WADI_DATA_ROOT>/
  WADI_14days_new.csv
  WADI_attackdataLABLE.csv
```

设置环境变量 `WADI_DATA_ROOT` 为该目录的绝对路径。WADI 资料与申请方式参见 [iTrust 数据集页面](https://itrust.sutd.edu.sg/itrust-labs_datasets/dataset_info/#wadi)。

`01`、`02`、`03` 入口的 A2 分支：训练默认取前 200,000 行；测试默认跳过首行；去除列名前后空白；首三列之后的列作为传感器特征；缺失值填 0；每 10 行取一个点；训练和测试分别按各自 min/max 归一化。测试标签小于 0 表示攻击，再复制到各特征列。

**重要限制**：分别对测试集归一化利用了整段测试数据的统计量，属于离线、含测试分布信息的处理，不符合严格在线训练统计量固定的协议。复制标签也不代表获得了传感器级故障真值。

独立 Transformer 入口 `06`—`10` 使用另一套清洗/标准化与窗口流程。不要与 A2 TranAD 的降采样协议混为一谈。原 `preprocess.py` 还保留基于事件时间表的 WADI 分支，字段格式与 A2 两文件路径不同。

## SMAP 与 SMD

SMAP 原始结构预期为 `TranAD/data/SMAP_MSL/train/`、`test/` 和 `labeled_anomalies.csv`。来源见 [Telemanom](https://github.com/khundman/telemanom)。

SMD 原始结构预期为 `TranAD/data/SMD/train/`、`test/`、`test_label/`；部分上游预处理还读取 `interpretation_label/`。来源见 [OmniAnomaly](https://github.com/NetManAIOps/OmniAnomaly)。以 `preprocess.py` 实际读取的文件结构为准。

这些数据由使用者自行下载；不要仅因为存在实验入口就把数据直接提交到仓库。SMAP 入口在缺少预处理文件时调用预处理；SMD 入口应按 notebook 检查说明准备。`main.py::load_dataset` 默认只加载 P-1 / machine-1-1。

## 输出隔离

历史代码在 `TranAD/processed/`、`checkpoints/` 和绘图目录写入结果。先复制实验目录或另建 checkout，再运行不同方案，避免覆盖模型和处理结果。这些运行输出已由 `.gitignore` 排除。
