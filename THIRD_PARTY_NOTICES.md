# 第三方来源与许可

`TranAD/main.py`、`preprocess.py`、`src/`、原依赖清单及 `LICENSE` 来自本地保存的 [imperial-qore/TranAD](https://github.com/imperial-qore/TranAD) 代码副本。其许可证为 BSD-3-Clause，版权声明及完整条款保留在 [TranAD/LICENSE](TranAD/LICENSE)。没有把该模型和基础训练实现宣称为本项目原创。

本地副本的确切上游提交尚未核定，因此这里不填写未经确认的 commit SHA，也不声称与上游当前默认分支逐字一致。`docs/source_manifest.json` 提供所用本地源文件的 SHA256。

上游工作：Shreshth Tuli、Giuliano Casale、Nicholas R. Jennings，TranAD: Deep Transformer Networks for Anomaly Detection in Multivariate Time Series Data，PVLDB 15(6)，2022。

`src/pot.py` 中标注直接取自 OmniAnomaly 的预测调整逻辑保留原注释；其他基础实现亦沿用上游随附内容和声明。使用者应遵守相关上游许可。

本项目新增和整理的部分主要为 notebook 实验组合、对比增强路径、输出整理和项目说明。新增部分暂未指定统一开源许可证；仓库公开可读不表示对所有内容授予任意使用许可。第三方代码继续适用其原许可证。

数据集适用各自许可和访问条款，本仓库不重新分发数据。
