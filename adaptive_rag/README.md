# Adaptive RAG Project - 基于 FlexRAG 重构版

这是一个基于 FlexRAG 框架重构的自适应检索增强生成（Adaptive RAG）项目。

## 🎯 核心创新

本项目借鉴 LevelRAG 的成功经验，基于 FlexRAG 成熟组件构建，专注于以下创新：

- **LLM 驱动的查询分析**：使用大语言模型进行智能问题分解，而非简单正则表达式
- **动态策略路由**：根据查询类型和复杂度自适应选择检索策略
- **智能混合检索**：动态调整关键词搜索和向量搜索的权重比例
- **多维度聚合**：平衡相关度和多样性的智能文档聚合

## 项目结构

```
adaptive_rag/
├── config/                  # 配置相关：存放所有组件的配置文件
│   ├── basic_config.yaml    # 基础配置，LLM和模块默认模型
│   └── adaptive_strategy_config.yaml # 自适应策略配置
├── data_processing/         # 数据处理：语料库预处理、数据集加载
│   └── corpus_builder.py
│   └── dataset_loader.py
├── modules/                 # 核心RAG模块的实现
│   ├── query_analyzer/      # 查询分析与分解模块
│   │   ├── query_decomposer.py
│   │   └── strategy_router.py
│   ├── retriever/           # 动态检索模块
│   │   ├── dense_retriever.py
│   │   ├── sparse_retriever.py
│   │   └── hybrid_retriever.py
│   ├── refiner/             # 重排序与聚合模块
│   │   ├── reranker.py
│   │   ├── aggregator.py
│   │   └── context_compressor.py
│   ├── generator/           # 生成模块
│   │   └── llm_generator.py
│   ├── evaluator/           # 评估模块
│   │   └── rag_metrics.py
│   └── judger/              # (可选) 判断器，例如用于自反思或决策
│       └── self_reflection_judger.py
├── pipeline/                # RAG流程的编排
│   └── adaptive_pipeline.py
├── utils/                   # 通用工具函数，如日志、模型加载助手
│   ├── logger.py
│   ├── model_loader.py
│   └── helper_functions.py
├── main.py                  # 项目入口文件
├── requirements.txt         # 项目依赖
└── README.md                # 项目说明
```

## 安装

1.  **克隆仓库**：
    ```bash
    git clone <your_repo_url>
    cd adaptive_rag
    ```

2.  **创建并激活 Conda 环境** (如果尚未):
    ```bash
    conda create -n adaptive_rag python=3.10 # 或者您喜欢的Python版本
    conda activate adaptive_rag
    ```

3.  **安装依赖**：
    ```bash
    pip install -r requirements.txt
    ```

## 配置

修改 `config/basic_config.yaml` 和 `config/adaptive_strategy_config.yaml` 文件，根据您的需求配置 LLM、模型路径、API 密钥和自适应策略。

## 运行示例

（待补充）

## 与 Web UI 集成

（待补充如何与现有 Web UI 集成的指导） 