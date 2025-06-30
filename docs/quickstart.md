# 🚀 快速开始指南

只需几分钟即可启动并运行 AdaptiveRAG！

## 📋 前置要求

确保您已安装 AdaptiveRAG。如果没有，请参见 [安装指南](installation.md)。

```bash
pip install adaptiverag
```

## 🎯 基本用法

### 您的第一个 AdaptiveRAG 查询

```python
from adaptive_rag import AdaptiveRAG

# 使用默认设置初始化 AdaptiveRAG
rag = AdaptiveRAG()

# 提出问题
result = rag.answer("量子计算的最新发展是什么？")

# 打印响应
print("答案:", result.answer)
print("来源:", len(result.sources))
print("处理时间:", result.processing_time)
```

### 理解响应

`answer()` 方法返回一个响应对象，包含：

- **`answer`**: 生成的响应文本
- **`sources`**: 使用的检索文档列表
- **`processing_time`**: 处理查询所用时间
- **`retrieval_results`**: 详细的检索信息
- **`generation_result`**: 生成元数据

## ⚙️ 配置

### 基本配置

```python
from adaptive_rag.config import AdaptiveRAGConfig

# 创建自定义配置
config = AdaptiveRAGConfig(
    dataset_name="natural_questions",
    retrieval_topk=10,
    enable_task_decomposition=True,
    enable_reranking=True
)

# 使用自定义配置初始化
rag = AdaptiveRAG(config)
```

### YAML 配置

创建配置文件 `my_config.yaml`：

```yaml
# AdaptiveRAG 配置
dataset_name: "hotpot_qa"
retrieval_topk: 15
adaptive_retrieval:
  enable_task_decomposition: true
  enable_strategy_planning: true
  enable_multi_retriever: true
  enable_reranking: true

generation_params:
  max_tokens: 256
  temperature: 0.1
```

加载配置：

```python
from adaptive_rag.config import AdaptiveRAGConfig

config = AdaptiveRAGConfig(config_file_path="my_config.yaml")
rag = AdaptiveRAG(config)
```

## 🧪 运行实验

### 快速测试

```bash
# 测试框架
python quick_test.py
```

### 简单实验

```python
from adaptive_rag.evaluation import BenchmarkRunner, BenchmarkConfig

# 配置实验
config = BenchmarkConfig(
    datasets=["natural_questions"],
    methods=["adaptive_rag", "naive_rag"],
    output_dir="./my_experiment",
    max_samples=10,  # 小规模测试
    save_predictions=True
)

# 运行实验
runner = BenchmarkRunner(config)
runner.run_benchmark()
```

### 命令行实验

```bash
# 使用样本数据的快速实验
python run_experiments.py quick --sample-data

# 完整评估
python run_experiments.py full

# 消融研究
python run_experiments.py ablation
```

## 🔧 高级用法

### 自定义检索策略

```python
from adaptive_rag.config import AdaptiveRAGConfig

config = AdaptiveRAGConfig(
    adaptive_retrieval={
        "enable_task_decomposition": True,
        "enable_strategy_planning": True,
        "enable_multi_retriever": True,
        "enable_reranking": True
    },
    strategy_planning={
        "task_specific_weights": {
            "factual": {"keyword": 0.7, "dense": 0.2, "web": 0.1},
            "semantic": {"keyword": 0.2, "dense": 0.7, "web": 0.1}
        }
    }
)

rag = AdaptiveRAG(config)
```

### 批量处理

```python
questions = [
    "什么是机器学习？",
    "神经网络训练是如何工作的？",
    "自然语言处理有哪些应用？"
]

results = []
for question in questions:
    result = rag.answer(question)
    results.append({
        "question": question,
        "answer": result.answer,
        "confidence": result.confidence_score
    })

# 打印结果
for i, result in enumerate(results):
    print(f"\n问题{i+1}: {result['question']}")
    print(f"答案{i+1}: {result['answer']}")
    print(f"置信度: {result['confidence']:.2f}")
```

### 与 FlexRAG 组件一起使用

```python
from adaptive_rag.config import AdaptiveRAGConfig

# 启用 FlexRAG 集成
config = AdaptiveRAGConfig(
    flexrag_integration=True,
    retriever_types=['bm25', 'dpr', 'contriever'],
    ranker_types=['cross_encoder', 'colbert'],
    generator_types=['t5', 'gpt']
)

rag = AdaptiveRAG(config)
```

## 📊 评估和分析

### 在标准数据集上评估

```python
from adaptive_rag.evaluation import BenchmarkRunner, BenchmarkConfig

config = BenchmarkConfig(
    datasets=["natural_questions", "hotpot_qa"],
    methods=["adaptive_rag"],
    output_dir="./evaluation_results",
    max_samples=100,
    compute_bert_score=True
)

runner = BenchmarkRunner(config)
results = runner.run_benchmark()

# 打印摘要
for result in results:
    print(f"数据集: {result.dataset_name}")
    print(f"精确匹配: {result.exact_match:.3f}")
    print(f"F1 分数: {result.f1_score:.3f}")
    print(f"ROUGE-L: {result.rouge_l:.3f}")
    print("---")
```

### 与基线方法比较

```python
config = BenchmarkConfig(
    datasets=["natural_questions"],
    methods=["adaptive_rag", "naive_rag", "self_rag"],
    output_dir="./comparison_results",
    max_samples=50
)

runner = BenchmarkRunner(config)
runner.run_benchmark()

# 结果将保存在 ./comparison_results/ 中
```

## 🌐 Web 界面

启动交互式 Web 界面：

```bash
cd adaptive_rag/webui
python interface.py --host 0.0.0.0 --port 7860
```

然后在浏览器中打开 `http://localhost:7860` 使用图形界面。

## 📈 监控和调试

### 启用调试模式

```python
config = AdaptiveRAGConfig(
    debug_mode=True,
    log_level="DEBUG",
    save_intermediate_results=True
)

rag = AdaptiveRAG(config)
```

### 访问中间结果

```python
result = rag.answer("什么是人工智能？")

# 检查任务分解
if hasattr(result, 'task_decomposition'):
    print("子任务:", result.task_decomposition.subtasks)

# 检查检索策略
if hasattr(result, 'retrieval_strategy'):
    print("策略:", result.retrieval_strategy.selected_methods)

# 检查检索到的文档
for i, doc in enumerate(result.sources[:3]):
    print(f"文档 {i+1}: {doc.title}")
    print(f"分数: {doc.score:.3f}")
    print(f"内容: {doc.content[:100]}...")
    print("---")
```

## 🎯 常见用例

### 1. 问答

```python
# 事实性问题
result = rag.answer("法国的首都是什么？")

# 复杂推理
result = rag.answer("比较太阳能和风能的环境影响。")

# 最新信息
result = rag.answer("AI 安全领域的最新发展是什么？")
```

### 2. 研究助手

```python
# 文献综述
result = rag.answer("总结 Transformer 架构的最新进展。")

# 技术解释
result = rag.answer("解释神经网络中的注意力机制。")
```

### 3. 教育支持

```python
# 概念解释
result = rag.answer("用简单的术语解释量子纠缠。")

# 问题解决
result = rag.answer("如何解二次方程？")
```

## 🔗 下一步

现在您已经启动并运行：

1. **探索 [架构](architecture.md)** 了解 AdaptiveRAG 的工作原理
2. **阅读 [实验指南](experiments.md)** 进行详细评估
3. **查看 [API 参考](api/)** 了解高级用法
4. **加入 [社区](https://github.com/Rito-w/adaptiverag/discussions)** 获得支持和讨论

## 📞 获取帮助

- 📖 **文档**: 浏览完整文档
- 🐛 **问题**: 在 [GitHub Issues](https://github.com/Rito-w/adaptiverag/issues) 报告错误
- 💬 **讨论**: 在 [GitHub Discussions](https://github.com/Rito-w/adaptiverag/discussions) 提问
- 📧 **邮箱**: 联系维护者

---

**🎉 您已准备就绪！开始使用 AdaptiveRAG 构建出色的 RAG 应用程序！**
