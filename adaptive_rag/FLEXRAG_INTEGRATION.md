# FlexRAG 深度集成指南

## 🎯 概述

AdaptiveRAG 现已深度集成 FlexRAG 组件，提供更强大、更稳定的 RAG 功能。通过集成 FlexRAG 的成熟组件，我们避免了重复造轮子，显著提升了系统的稳定性和性能。

## 🚀 主要优势

### 1. **组件成熟度**
- ✅ 使用 FlexRAG 经过验证的检索器、重排序器、生成器
- ✅ 减少自研组件的潜在 bug 和不稳定性
- ✅ 享受 FlexRAG 社区的持续更新和优化

### 2. **功能丰富性**
- 🔍 **多种检索器**: BM25、Dense、Hybrid、Web Search
- 🎯 **智能重排序**: Cross-Encoder、ColBERT、多重排序器融合
- ✨ **灵活生成**: HuggingFace、OpenAI、本地模型支持
- 🔧 **统一配置**: 一套配置管理所有组件

### 3. **自适应增强**
- 🧠 保留原有的 LLM 驱动查询分析
- 📋 保留任务分解和策略规划能力
- 🎪 结合 FlexRAG 组件实现更强的自适应性

## 📦 安装要求

### 基础安装
```bash
# 安装 AdaptiveRAG
cd adaptiverag/adaptive_rag
pip install -r requirements.txt
```

### FlexRAG 集成（推荐）
```bash
# 安装 FlexRAG（获得完整功能）
pip install flexrag

# 或者从源码安装
git clone https://github.com/flexrag/flexrag.git
cd flexrag
pip install -e .
```

### 可选依赖
```bash
# 用于更好的重排序
pip install sentence-transformers

# 用于 OpenAI 集成
pip install openai

# 用于 Web 搜索
pip install google-search-results
```

## 🎮 使用方式

### 1. 命令行启动

#### Web UI 模式
```bash
# 原始自适应模式
python main.py webui --mode adaptive

# FlexRAG 深度集成模式（推荐）
python main.py webui --mode flexrag --port 7860

# 混合模式
python main.py webui --mode hybrid
```

#### 测试模式
```bash
# 完整集成测试
python main.py test-flexrag

# 测试特定组件
python main.py test-flexrag --component retriever
python main.py test-flexrag --component ranker
python main.py test-flexrag --component generator
python main.py test-flexrag --component assistant
```

### 2. 编程接口

#### 快速开始
```python
from adaptive_rag.config import get_config_for_mode
from adaptive_rag.core.flexrag_integrated_assistant import FlexRAGIntegratedAssistant

# 创建 FlexRAG 集成配置
config = get_config_for_mode("flexrag")

# 初始化助手
assistant = FlexRAGIntegratedAssistant(config)

# 使用助手回答问题
result = assistant.answer("What is machine learning?")
print(result.answer)
```

#### 自定义策略
```python
# 自定义检索策略
custom_strategy = {
    "retrieval_top_k": 15,
    "enable_reranking": True,
    "ranking_strategy": {
        "ranker": "cross_encoder",
        "enable_multi_ranker": True,
        "ranker_weights": {"cross_encoder": 0.7, "colbert": 0.3},
        "final_top_k": 8
    },
    "generation_strategy": {
        "generator": "openai_generator",  # 使用 OpenAI
        "prompt_template": "step_by_step",
        "max_tokens": 300,
        "temperature": 0.1
    }
}

result = assistant.answer("Compare AI and ML", custom_strategy)
```

### 3. 组件级使用

#### 独立使用检索器
```python
from adaptive_rag.modules.retriever.flexrag_integrated_retriever import FlexRAGIntegratedRetriever

retriever = FlexRAGIntegratedRetriever(config)

strategy = {
    "weights": {"keyword": 0.4, "dense": 0.4, "web": 0.2},
    "fusion_method": "rrf"
}

result = retriever.adaptive_retrieve("AI query", strategy)
```

#### 独立使用重排序器
```python
from adaptive_rag.modules.refiner.flexrag_integrated_ranker import FlexRAGIntegratedRanker

ranker = FlexRAGIntegratedRanker(config)

strategy = {
    "ranker": "cross_encoder",
    "enable_multi_ranker": True,
    "final_top_k": 5
}

result = ranker.adaptive_rank("query", contexts, strategy)
```

## ⚙️ 配置详解

### FlexRAG 集成配置结构
```python
@dataclass
class FlexRAGIntegratedConfig:
    # 检索器配置
    retriever_configs: Dict[str, Any] = {
        "keyword_retriever": {
            "retriever_type": "flex",
            "flex_config": {
                "retriever_path": "./data/keyword_index",
                "indexes_merge_method": "rrf"
            }
        },
        "dense_retriever": {
            "retriever_type": "flex",
            "flex_config": {
                "retriever_path": "./data/dense_index"
            }
        }
    }
    
    # 重排序器配置
    ranker_configs: Dict[str, Any] = {
        "cross_encoder": {
            "ranker_type": "hf_cross_encoder",
            "hf_cross_encoder_config": {
                "model_name": "BAAI/bge-reranker-base"
            }
        }
    }
    
    # 生成器配置
    generator_configs: Dict[str, Any] = {
        "main_generator": {
            "generator_type": "hf",
            "hf_config": {
                "model_path": "./models/qwen1.5-1.8b"
            }
        },
        "openai_generator": {
            "generator_type": "openai",
            "openai_config": {
                "model_name": "gpt-3.5-turbo"
            }
        }
    }
```

### 环境变量配置
```bash
# OpenAI API 密钥
export OPENAI_API_KEY="your-api-key"

# Google 搜索 API（可选）
export GOOGLE_API_KEY="your-google-api-key"
export GOOGLE_CSE_ID="your-cse-id"
```

## 🔧 故障排除

### 1. FlexRAG 未安装
**现象**: 看到 "FlexRAG 未安装，将使用模拟实现" 警告

**解决方案**:
```bash
pip install flexrag
# 或
pip install git+https://github.com/flexrag/flexrag.git
```

### 2. 模型路径错误
**现象**: 模型加载失败

**解决方案**:
- 检查 `config.py` 中的模型路径
- 确保模型文件存在于指定位置
- 使用 `resolve_path()` 函数处理相对路径

### 3. 内存不足
**现象**: 加载大模型时内存溢出

**解决方案**:
```python
# 使用较小的模型
config.generator_configs["main_generator"]["hf_config"]["model_path"] = "smaller-model"

# 或使用 OpenAI API
config.generator_configs["openai_generator"]["openai_config"]["model_name"] = "gpt-3.5-turbo"
```

## 📊 性能对比

| 模式 | 检索质量 | 生成质量 | 稳定性 | 资源消耗 |
|------|----------|----------|--------|----------|
| **adaptive** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 低 |
| **flexrag** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 中 |
| **hybrid** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 中 |

## 🎯 最佳实践

### 1. 生产环境推荐
```python
# 使用 FlexRAG 模式获得最佳性能
config = get_config_for_mode("flexrag")

# 启用多重排序器提升质量
strategy = {
    "ranking_strategy": {
        "enable_multi_ranker": True,
        "ranker_weights": {"cross_encoder": 0.6, "colbert": 0.4}
    }
}
```

### 2. 开发测试推荐
```python
# 使用自适应模式快速迭代
config = get_config_for_mode("adaptive")

# 或使用混合模式平衡性能和速度
config = get_config_for_mode("hybrid")
```

### 3. 资源受限环境
```python
# 使用较小的模型
config.generator_configs["main_generator"]["hf_config"]["model_path"] = "qwen1.5-0.5b"

# 减少检索数量
strategy = {
    "retrieval_top_k": 5,
    "ranking_strategy": {"final_top_k": 3}
}
```

## 🔮 未来规划

- [ ] 支持更多 FlexRAG 组件
- [ ] 集成 FlexRAG 的评估框架
- [ ] 支持分布式部署
- [ ] 添加更多预训练模型
- [ ] 优化内存使用和推理速度

## 🤝 贡献指南

欢迎贡献代码和建议！请参考：
1. 提交 Issue 报告问题
2. Fork 项目并创建分支
3. 提交 Pull Request

## 📞 支持

如有问题，请：
1. 查看本文档的故障排除部分
2. 运行 `python main.py test-flexrag` 进行诊断
3. 提交 GitHub Issue

---

**享受 FlexRAG 深度集成带来的强大功能！** 🎉
