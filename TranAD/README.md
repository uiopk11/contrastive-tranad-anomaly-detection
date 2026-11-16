# TranAD 基础代码

本目录保存实验使用的 TranAD 基础实现，许可证见 [LICENSE](LICENSE)，来源说明见 [第三方说明](../THIRD_PARTY_NOTICES.md)。

项目入口、方法和环境配置请阅读 [根目录 README](../README.md) 与 [运行指南](../docs/reproduction.md)。独立 notebook 已包含 PyTorch 参数兼容补丁；直接执行这里的旧版 `main.py` 不会自动应用这些补丁。

`main.py` 的数据加载默认选择 SMAP P-1、MSL C-1 或 SMD machine-1-1。目录名不能被理解为已经覆盖全部实体。原代码包含多种其他模型和诊断工具，本项目整理与检查重点是 TranAD 和对比增强路径。
