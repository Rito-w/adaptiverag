# 🏠 AdaptiveRAG - 本地模型版

> 智能自适应检索增强生成系统，支持真实的本地模型和模块化控制

[![GitHub](https://img.shields.io/github/license/Rito-w/adaptiverag)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![WebUI](https://img.shields.io/badge/WebUI-Gradio-orange.svg)](https://gradio.app)

## 🚀 快速启动 WebUI

### 📋 前置要求

- Python 3.8+
- CUDA GPU（推荐）
- 本地模型文件（Qwen、BGE、E5等）

### ⚡ 一键启动

```bash
# 1. 激活环境
source /etc/network_turbo
conda activate flexrag
cd /root/my_project/adaptiverag

# 2. 检查资源（可选）
python3 check_local_resources.py

# 3. 启动WebUI（选择一种）
# 简化版（推荐新手）
python3 launch_simple_local_webui.py --port 7865 --host 0.0.0.0

# 完整版（功能全面）
python3 launch_local_model_webui.py --port 7863 --host 0.0.0.0
```

### 🌐 访问界面

启动后访问：
- **简化版**: `http://your-server:7865`
- **完整版**: `http://your-server:7863`

## 🎯 核心特性

### ✅ **真实本地模型支持**
- 🤖 **Qwen2.5-1.5B-Instruct**: 生成模型
- 🎯 **BGE-reranker-base**: 重排序模型
- 🔍 **E5-base-v2**: 嵌入模型
- 📊 **HotpotQA数据**: 真实问答数据集

### 🎛️ **模块化控制系统**
- **任务分解器**: 将复杂查询分解为子任务
- **关键词检索**: BM25算法进行精确匹配
- **密集检索**: 语义向量检索
- **上下文重排序**: BGE模型重新排序结果
- **自适应生成**: Qwen模型生成智能回答

### 🔄 **真实效果对比**
每个模块的开关都会产生**实际的、可观察的差异**：

```
配置A（基础）：
✅ 任务分解 + ✅ 关键词检索 + ❌ 重排序 + ✅ 生成
→ 基础检索 + Qwen生成

配置B（完整）：
✅ 任务分解 + ✅ 关键词检索 + ✅ 重排序 + ✅ 生成
→ 检索 + BGE重排序 + Qwen生成

您可以清楚地看到两种配置的实际差异！
```

## 📁 项目结构

```
adaptiverag/
├── 🚀 launch_simple_local_webui.py     # 简化版启动器
├── 🚀 launch_local_model_webui.py      # 完整版启动器
├── 🔍 check_local_resources.py         # 资源检查工具
├── 📦 install_real_model_deps.py       # 依赖安装
├── 📁 adaptive_rag/                    # 核心代码
│   ├── core/                           # 模块管理器
│   ├── modules/                        # 功能模块
│   ├── webui/                          # Web界面
│   │   └── engines/local_model_engine.py  # 本地模型引擎
│   └── config/                         # 配置系统
├── 📁 configs/
│   └── real_config_enhanced.yaml       # 主配置文件
└── 📁 docs/                           # 文档（支持GitHub Actions）
```

## 🛠️ 安装配置

### 1. 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装额外依赖（如需要）
python3 install_real_model_deps.py
```

### 2. 准备本地模型

确保您的模型文件在正确位置：

```
/root/autodl-tmp/models/
├── Qwen2.5-1.5B-Instruct/    # 生成模型
├── bge-reranker-base/        # 重排序模型
└── e5-base-v2/              # 嵌入模型

/root/autodl-tmp/flashrag_real_data/
├── hotpotqa_dev.jsonl       # 问答数据
└── cache/                   # 缓存目录
```

### 3. 检查资源

```bash
python3 check_local_resources.py
```

## 🎮 使用指南

### 基础使用

1. **启动WebUI**：选择简化版或完整版
2. **输入查询**：如"什么是机器学习？"
3. **观察结果**：查看处理步骤和生成答案
4. **调整模块**：开关不同模块，对比效果

### 高级功能

- **模块控制**: 实时配置不同功能模块
- **性能监控**: 查看处理时间和资源使用
- **结果分析**: 详细的处理流程展示
- **配置管理**: 自定义模型和数据路径

## 🔧 故障排除

### 常见问题

1. **模型加载失败**
   ```bash
   # 检查模型文件
   ls -la /root/autodl-tmp/models/Qwen2.5-1.5B-Instruct/
   ```

2. **端口被占用**
   ```bash
   # 使用不同端口
   python3 launch_simple_local_webui.py --port 7866 --host 0.0.0.0
   ```

3. **显存不足**
   ```bash
   # 使用更小的模型或调整配置
   # 编辑 configs/real_config_enhanced.yaml
   ```

### 获取帮助

```bash
# 查看启动选项
python3 launch_simple_local_webui.py --help

# 启用调试模式
python3 launch_simple_local_webui.py --debug
```

## 📊 性能特点

- **本地化**: 完全离线运行，无需网络
- **模块化**: 灵活的功能组合
- **真实效果**: 每个模块产生实际差异
- **高效缓存**: 智能索引缓存，加速后续使用
- **GPU加速**: 支持CUDA加速推理

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可证。

## 🔗 相关链接

- [详细文档](docs/) - 完整的技术文档
- [GitHub Actions](../../actions) - 自动化部署
- [Issues](../../issues) - 问题反馈

---

🎉 **现在就开始体验真正的本地模型驱动的AdaptiveRAG系统吧！**
