# 🧠 AdaptiveRAG Documentation

Welcome to the comprehensive documentation for **AdaptiveRAG** - an intelligent adaptive retrieval-augmented generation system that dynamically adapts its retrieval strategy based on query complexity and context requirements.

## 🌟 What is AdaptiveRAG?

AdaptiveRAG is a next-generation RAG system that goes beyond traditional static retrieval approaches. It intelligently analyzes queries, decomposes complex tasks, and dynamically selects optimal retrieval strategies to provide more accurate and contextually relevant responses.

### Key Features

- **🧠 Intelligent Query Analysis**: LLM-driven query understanding and task decomposition
- **🔄 Adaptive Retrieval Strategy**: Dynamic selection of optimal retrieval methods
- **🔗 Multi-Retriever Fusion**: Seamless integration of keyword, dense, and web retrieval
- **📊 Comprehensive Evaluation**: Extensive benchmarking against state-of-the-art methods
- **🔧 FlexRAG Integration**: Deep integration with FlexRAG components for stability

## 🚀 Quick Start

Get started with AdaptiveRAG in just a few steps:

### Installation

```bash
# Install from PyPI
pip install adaptiverag

# Or install from source
git clone https://github.com/Rito-w/adaptiverag.git
cd adaptiverag
pip install -e .
```

### Basic Usage

```python
from adaptive_rag import AdaptiveRAG

# Initialize AdaptiveRAG
rag = AdaptiveRAG()

# Process a query
result = rag.answer("What are the latest developments in quantum computing?")
print(result.answer)
```

### Run Experiments

```bash
# Quick test
python quick_test.py

# Run full experiments
python run_experiments.py full

# Ablation study
python run_experiments.py ablation
```

## 🏗️ Architecture Overview

AdaptiveRAG consists of five core components working in harmony:

```mermaid
graph LR
    A[Query] --> B[Task Decomposer]
    B --> C[Retrieval Planner]
    C --> D[Multi-Retriever]
    D --> E[Context Reranker]
    E --> F[Adaptive Generator]
    F --> G[Response]
```

1. **Task Decomposer**: Breaks down complex queries into manageable subtasks
2. **Retrieval Planner**: Selects optimal retrieval strategies based on query type
3. **Multi-Retriever**: Fuses results from multiple retrieval methods
4. **Context Reranker**: Optimizes retrieved context for generation
5. **Adaptive Generator**: Produces high-quality responses

## 📊 Performance

AdaptiveRAG has been evaluated on multiple datasets and consistently outperforms baseline methods:

| Dataset | Method | EM | F1 | ROUGE-L |
|---------|--------|----|----|---------|
| Natural Questions | AdaptiveRAG | **0.52** | **0.66** | **0.71** |
| | Naive RAG | 0.41 | 0.58 | 0.63 |
| | Self-RAG | 0.47 | 0.62 | 0.68 |
| HotpotQA | AdaptiveRAG | **0.38** | **0.51** | **0.58** |
| | Naive RAG | 0.29 | 0.42 | 0.49 |
| | Self-RAG | 0.34 | 0.47 | 0.54 |

> 📝 **Note**: Results are from our experimental framework. See [Benchmarks](benchmarks.md) for detailed analysis.

## 🧪 Experimental Framework

AdaptiveRAG includes a comprehensive experimental framework inspired by FlashRAG:

- **Standardized Evaluation**: Compatible with FlashRAG datasets and metrics
- **Baseline Comparisons**: Implementation of major RAG methods
- **Ablation Studies**: Detailed component contribution analysis
- **Reproducible Results**: Configurable experiments for academic research

## 🔗 Integration

### FlexRAG Integration

AdaptiveRAG deeply integrates with FlexRAG components:

```python
from adaptive_rag.config import AdaptiveRAGConfig

config = AdaptiveRAGConfig(
    retrieval_methods=['keyword', 'dense', 'web'],
    reranking_enabled=True,
    flexrag_integration=True
)
```

### FlashRAG Compatibility

Use FlashRAG datasets and evaluation metrics:

```python
from adaptive_rag.evaluation import BenchmarkRunner

runner = BenchmarkRunner(
    datasets=['natural_questions', 'hotpot_qa'],
    methods=['adaptive_rag', 'naive_rag'],
    flashrag_compatible=True
)
```

## 📚 Documentation Structure

This documentation is organized into several sections:

- **[Getting Started](installation.md)**: Installation, configuration, and basic usage
- **[Core Concepts](architecture.md)**: Deep dive into AdaptiveRAG's architecture
- **[Integration](flexrag-integration.md)**: How to integrate with existing systems
- **[Experiments](experiments.md)**: Running experiments and evaluations
- **[API Reference](api/)**: Complete API documentation
- **[Development](development.md)**: Contributing and extending AdaptiveRAG

## 🤝 Community

Join our growing community:

- **GitHub**: [Rito-w/adaptiverag](https://github.com/Rito-w/adaptiverag)
- **Issues**: [Report bugs or request features](https://github.com/Rito-w/adaptiverag/issues)
- **Discussions**: [Join the conversation](https://github.com/Rito-w/adaptiverag/discussions)

## 📄 Citation

If you use AdaptiveRAG in your research, please cite:

```bibtex
@article{adaptiverag2024,
  title={AdaptiveRAG: Intelligent Adaptive Retrieval-Augmented Generation},
  author={Your Name},
  journal={arXiv preprint arXiv:2024.xxxxx},
  year={2024}
}
```

## 📞 Support

Need help? We're here for you:

- 📖 **Documentation**: You're reading it!
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/Rito-w/adaptiverag/issues)
- 💬 **Questions**: [GitHub Discussions](https://github.com/Rito-w/adaptiverag/discussions)
- 📧 **Email**: adaptiverag@example.com

---

**Ready to get started?** Check out our [Installation Guide](installation.md) or dive into the [Quick Start](quickstart.md) tutorial!
