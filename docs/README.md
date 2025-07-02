# 🧠 AdaptiveRAG: 智能自适应检索增强生成系统

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

AdaptiveRAG 是一个智能的检索增强生成系统，能够根据查询复杂度和上下文需求动态调整检索策略。它集成了多种检索方法，并使用大语言模型驱动的分析来实现最佳性能。

## 🌟 核心特性

- **🧠 智能查询分析**: 基于大语言模型的查询理解和任务分解
- **🔄 自适应检索策略**: 动态选择最优检索方法
- **🔗 多检索器融合**: 无缝集成关键词、密集向量和网络检索
- **📊 全面评估**: 与最先进方法的广泛基准测试
- **🔧 FlexRAG 集成**: 与 FlexRAG 组件深度集成，确保稳定性
- **📈 实验框架**: 完整的学术研究评估流水线

## 🏗️ 系统架构

```
AdaptiveRAG 流水线:
查询 → 任务分解 → 策略规划 → 多重检索 → 重排序 → 生成
```

### 核心组件

1. **任务分解器**: 将复杂查询分解为可管理的子任务
2. **检索规划器**: 根据查询类型选择最优检索策略
3. **多重检索器**: 融合多种检索方法的结果
4. **上下文重排器**: 优化检索到的上下文用于生成
5. **自适应生成器**: 产生高质量的响应

## 📦 安装

### 前置要求
- Python 3.8+
- PyTorch 1.9+
- CUDA (可选，用于GPU加速)

### 快速安装
```bash
git clone https://github.com/your-username/adaptiverag.git
cd adaptiverag
pip install -r requirements.txt
```

### 开发安装
```bash
git clone https://github.com/your-username/adaptiverag.git
cd adaptiverag
pip install -e .
```

## 🚀 快速开始

### 基本用法
```python
from adaptive_rag import AdaptiveRAG

# 初始化 AdaptiveRAG
rag = AdaptiveRAG()

# 处理查询
result = rag.answer("量子计算的最新发展是什么？")
print(result.answer)
```

### 配置
```python
from adaptive_rag.config import AdaptiveRAGConfig

config = AdaptiveRAGConfig(
    dataset_name="natural_questions",
    retrieval_topk=10,
    enable_task_decomposition=True,
    enable_multi_retriever=True
)

rag = AdaptiveRAG(config)
```

## 🧪 实验

### 🎯 立即测试（推荐，无需训练数据）
```bash
# 测试增强功能
python test_enhanced_features.py

# 运行可行性实验
python run_feasible_experiments.py
```

### 🔬 完整实验
```bash
# 快速实验
python run_experiments.py --experiment quick

# 完整评估
python run_experiments.py --experiment full

# 消融研究
python run_experiments.py --experiment ablation

# 效率分析
python run_experiments.py efficiency
```

### 生成论文结果
```bash
python run_experiments.py paper
```

## 📊 基准测试

AdaptiveRAG 已在多个数据集上进行评估：

| 数据集 | EM | F1 | ROUGE-L | BERTScore |
|---------|----|----|---------|-----------|
| Natural Questions | - | - | - | - |
| HotpotQA | - | - | - | - |
| TriviaQA | - | - | - | - |
| MS MARCO | - | - | - | - |

*结果将在运行完整实验后更新*

## 📁 项目结构

```
adaptiverag/
├── adaptive_rag/              # AdaptiveRAG 核心实现
│   ├── core/                  # 核心组件
│   ├── modules/               # 独立模块
│   ├── pipeline/              # 流水线实现
│   ├── evaluation/            # 评估框架
│   ├── config/                # 配置文件
│   └── utils/                 # 工具函数
├── experiments/               # 实验结果
├── data/                      # 数据集存储
├── docs/                      # 文档
├── tests/                     # 单元测试
├── scripts/                   # 工具脚本
└── requirements.txt           # 依赖项
```

## 🔧 配置

AdaptiveRAG 支持通过 YAML 文件和 Python 字典进行灵活配置：

```yaml
# config.yaml
dataset_name: "natural_questions"
retrieval_topk: 10
adaptive_retrieval:
  enable_task_decomposition: true
  enable_strategy_planning: true
  enable_multi_retriever: true
  enable_reranking: true
```

## 📚 文档

- [安装指南](docs/installation.md)
- [配置参考](docs/configuration.md)
- [API 文档](docs/api.md)
- [实验指南](docs/experiments.md)
- [FlexRAG 集成](adaptive_rag/FLEXRAG_INTEGRATION.md)

## 🤝 贡献

我们欢迎贡献！请查看我们的[贡献指南](CONTRIBUTING.md)了解详情。

### 开发环境设置
```bash
git clone https://github.com/your-username/adaptiverag.git
cd adaptiverag
pip install -e ".[dev]"
pre-commit install
```

## 📄 许可证

本项目采用 MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件。

## 📖 引用

如果您在研究中使用 AdaptiveRAG，请引用：

```bibtex
@article{adaptiverag2024,
  title={AdaptiveRAG: Intelligent Adaptive Retrieval-Augmented Generation},
  author={Your Name},
  journal={arXiv preprint arXiv:2024.xxxxx},
  year={2024}
}
```

## 🙏 致谢

- [FlashRAG](https://github.com/RUC-NLPIR/FlashRAG) 提供实验方法论
- [FlexRAG](https://github.com/ictnlp/FlexRAG) 提供组件集成
- [LevelRAG](https://github.com/microsoft/LevelRAG) 提供架构灵感

## 📞 联系方式

- **作者**: Your Name
- **邮箱**: your.email@example.com
- **GitHub**: [@your-username](https://github.com/your-username)

---

**🎯 AdaptiveRAG: 让 RAG 系统真正自适应和智能！**
