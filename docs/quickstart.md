# 🚀 Quick Start Guide

Get up and running with AdaptiveRAG in just a few minutes!

## 📋 Prerequisites

Make sure you have AdaptiveRAG installed. If not, see the [Installation Guide](installation.md).

```bash
pip install adaptiverag
```

## 🎯 Basic Usage

### Your First AdaptiveRAG Query

```python
from adaptive_rag import AdaptiveRAG

# Initialize AdaptiveRAG with default settings
rag = AdaptiveRAG()

# Ask a question
result = rag.answer("What are the latest developments in quantum computing?")

# Print the response
print("Answer:", result.answer)
print("Sources:", len(result.sources))
print("Processing time:", result.processing_time)
```

### Understanding the Response

The `answer()` method returns a response object with:

- **`answer`**: The generated response text
- **`sources`**: List of retrieved documents used
- **`processing_time`**: Time taken to process the query
- **`retrieval_results`**: Detailed retrieval information
- **`generation_result`**: Generation metadata

## ⚙️ Configuration

### Basic Configuration

```python
from adaptive_rag.config import AdaptiveRAGConfig

# Create custom configuration
config = AdaptiveRAGConfig(
    dataset_name="natural_questions",
    retrieval_topk=10,
    enable_task_decomposition=True,
    enable_reranking=True
)

# Initialize with custom config
rag = AdaptiveRAG(config)
```

### YAML Configuration

Create a config file `my_config.yaml`:

```yaml
# AdaptiveRAG Configuration
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

Load the configuration:

```python
from adaptive_rag.config import AdaptiveRAGConfig

config = AdaptiveRAGConfig(config_file_path="my_config.yaml")
rag = AdaptiveRAG(config)
```

## 🧪 Running Experiments

### Quick Test

```bash
# Test the framework
python quick_test.py
```

### Simple Experiment

```python
from adaptive_rag.evaluation import BenchmarkRunner, BenchmarkConfig

# Configure experiment
config = BenchmarkConfig(
    datasets=["natural_questions"],
    methods=["adaptive_rag", "naive_rag"],
    output_dir="./my_experiment",
    max_samples=10,  # Small test
    save_predictions=True
)

# Run experiment
runner = BenchmarkRunner(config)
runner.run_benchmark()
```

### Command Line Experiments

```bash
# Quick experiment with sample data
python run_experiments.py quick --sample-data

# Full evaluation
python run_experiments.py full

# Ablation study
python run_experiments.py ablation
```

## 🔧 Advanced Usage

### Custom Retrieval Strategy

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

### Batch Processing

```python
questions = [
    "What is machine learning?",
    "How does neural network training work?",
    "What are the applications of NLP?"
]

results = []
for question in questions:
    result = rag.answer(question)
    results.append({
        "question": question,
        "answer": result.answer,
        "confidence": result.confidence_score
    })

# Print results
for i, result in enumerate(results):
    print(f"\nQ{i+1}: {result['question']}")
    print(f"A{i+1}: {result['answer']}")
    print(f"Confidence: {result['confidence']:.2f}")
```

### Using with FlexRAG Components

```python
from adaptive_rag.config import AdaptiveRAGConfig

# Enable FlexRAG integration
config = AdaptiveRAGConfig(
    flexrag_integration=True,
    retriever_types=['bm25', 'dpr', 'contriever'],
    ranker_types=['cross_encoder', 'colbert'],
    generator_types=['t5', 'gpt']
)

rag = AdaptiveRAG(config)
```

## 📊 Evaluation and Analysis

### Evaluate on Standard Datasets

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

# Print summary
for result in results:
    print(f"Dataset: {result.dataset_name}")
    print(f"Exact Match: {result.exact_match:.3f}")
    print(f"F1 Score: {result.f1_score:.3f}")
    print(f"ROUGE-L: {result.rouge_l:.3f}")
    print("---")
```

### Compare with Baselines

```python
config = BenchmarkConfig(
    datasets=["natural_questions"],
    methods=["adaptive_rag", "naive_rag", "self_rag"],
    output_dir="./comparison_results",
    max_samples=50
)

runner = BenchmarkRunner(config)
runner.run_benchmark()

# Results will be saved in ./comparison_results/
```

## 🌐 Web Interface

Launch the interactive web interface:

```bash
cd adaptive_rag/webui
python interface.py --host 0.0.0.0 --port 7860
```

Then open your browser to `http://localhost:7860` to use the graphical interface.

## 📈 Monitoring and Debugging

### Enable Debug Mode

```python
config = AdaptiveRAGConfig(
    debug_mode=True,
    log_level="DEBUG",
    save_intermediate_results=True
)

rag = AdaptiveRAG(config)
```

### Access Intermediate Results

```python
result = rag.answer("What is artificial intelligence?")

# Check task decomposition
if hasattr(result, 'task_decomposition'):
    print("Subtasks:", result.task_decomposition.subtasks)

# Check retrieval strategy
if hasattr(result, 'retrieval_strategy'):
    print("Strategy:", result.retrieval_strategy.selected_methods)

# Check retrieved documents
for i, doc in enumerate(result.sources[:3]):
    print(f"Doc {i+1}: {doc.title}")
    print(f"Score: {doc.score:.3f}")
    print(f"Content: {doc.content[:100]}...")
    print("---")
```

## 🎯 Common Use Cases

### 1. Question Answering

```python
# Factual questions
result = rag.answer("What is the capital of France?")

# Complex reasoning
result = rag.answer("Compare the environmental impact of solar and wind energy.")

# Recent information
result = rag.answer("What are the latest developments in AI safety?")
```

### 2. Research Assistant

```python
# Literature review
result = rag.answer("Summarize recent advances in transformer architectures.")

# Technical explanations
result = rag.answer("Explain the attention mechanism in neural networks.")
```

### 3. Educational Support

```python
# Concept explanation
result = rag.answer("Explain quantum entanglement in simple terms.")

# Problem solving
result = rag.answer("How do you solve quadratic equations?")
```

## 🔗 Next Steps

Now that you're up and running:

1. **Explore the [Architecture](architecture.md)** to understand how AdaptiveRAG works
2. **Read the [Experiments Guide](experiments.md)** for detailed evaluation
3. **Check the [API Reference](api/)** for advanced usage
4. **Join the [Community](https://github.com/Rito-w/adaptiverag/discussions)** for support and discussions

## 📞 Getting Help

- 📖 **Documentation**: Browse the full documentation
- 🐛 **Issues**: Report bugs on [GitHub Issues](https://github.com/Rito-w/adaptiverag/issues)
- 💬 **Discussions**: Ask questions in [GitHub Discussions](https://github.com/Rito-w/adaptiverag/discussions)
- 📧 **Email**: Contact the maintainers

---

**🎉 You're all set! Start building amazing RAG applications with AdaptiveRAG!**
