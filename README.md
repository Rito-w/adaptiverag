# 🧠 AdaptiveRAG: Intelligent Adaptive Retrieval-Augmented Generation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

AdaptiveRAG is an intelligent retrieval-augmented generation system that dynamically adapts its retrieval strategy based on query complexity and context requirements. It integrates multiple retrieval methods and uses LLM-driven analysis for optimal performance.

## 🌟 Key Features

- **🧠 Intelligent Query Analysis**: LLM-driven query understanding and task decomposition
- **🔄 Adaptive Retrieval Strategy**: Dynamic selection of optimal retrieval methods
- **🔗 Multi-Retriever Fusion**: Seamless integration of keyword, dense, and web retrieval
- **📊 Comprehensive Evaluation**: Extensive benchmarking against state-of-the-art methods
- **🔧 FlexRAG Integration**: Deep integration with FlexRAG components for stability
- **📈 Experimental Framework**: Complete evaluation pipeline for academic research

## 🏗️ Architecture

```
AdaptiveRAG Pipeline:
Query → Task Decomposition → Strategy Planning → Multi-Retrieval → Reranking → Generation
```

### Core Components

1. **Task Decomposer**: Breaks down complex queries into manageable subtasks
2. **Retrieval Planner**: Selects optimal retrieval strategies based on query type
3. **Multi-Retriever**: Fuses results from multiple retrieval methods
4. **Context Reranker**: Optimizes retrieved context for generation
5. **Adaptive Generator**: Produces high-quality responses

## 📦 Installation

### Prerequisites
- Python 3.8+
- PyTorch 1.9+
- CUDA (optional, for GPU acceleration)

### Quick Install
```bash
git clone https://github.com/your-username/adaptiverag.git
cd adaptiverag
pip install -r requirements.txt
```

### Development Install
```bash
git clone https://github.com/your-username/adaptiverag.git
cd adaptiverag
pip install -e .
```

## 🚀 Quick Start

### Basic Usage
```python
from adaptive_rag import AdaptiveRAG

# Initialize AdaptiveRAG
rag = AdaptiveRAG()

# Process a query
result = rag.answer("What are the latest developments in quantum computing?")
print(result.answer)
```

### Configuration
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

## 🧪 Experiments

### Quick Test
```bash
python quick_test.py
```

### Run Experiments
```bash
# Quick experiment with sample data
python run_experiments.py quick --sample-data

# Full evaluation
python run_experiments.py full

# Ablation study
python run_experiments.py ablation

# Efficiency analysis
python run_experiments.py efficiency
```

### Generate Paper Results
```bash
python run_experiments.py paper
```

## 📊 Benchmarks

AdaptiveRAG has been evaluated on multiple datasets:

| Dataset | EM | F1 | ROUGE-L | BERTScore |
|---------|----|----|---------|-----------|
| Natural Questions | - | - | - | - |
| HotpotQA | - | - | - | - |
| TriviaQA | - | - | - | - |
| MS MARCO | - | - | - | - |

*Results will be updated after running full experiments*

## 📁 Project Structure

```
adaptiverag/
├── adaptive_rag/              # Core AdaptiveRAG implementation
│   ├── core/                  # Core components
│   ├── modules/               # Individual modules
│   ├── pipeline/              # Pipeline implementations
│   ├── evaluation/            # Evaluation framework
│   ├── config/                # Configuration files
│   └── utils/                 # Utility functions
├── experiments/               # Experiment results
├── data/                      # Dataset storage
├── docs/                      # Documentation
├── tests/                     # Unit tests
├── scripts/                   # Utility scripts
└── requirements.txt           # Dependencies
```

## 🔧 Configuration

AdaptiveRAG supports flexible configuration through YAML files and Python dictionaries:

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

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [Configuration Reference](docs/configuration.md)
- [API Documentation](docs/api.md)
- [Experiment Guide](docs/experiments.md)
- [FlexRAG Integration](adaptive_rag/FLEXRAG_INTEGRATION.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/your-username/adaptiverag.git
cd adaptiverag
pip install -e ".[dev]"
pre-commit install
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📖 Citation

If you use AdaptiveRAG in your research, please cite:

```bibtex
@article{adaptiverag2024,
  title={AdaptiveRAG: Intelligent Adaptive Retrieval-Augmented Generation},
  author={Your Name},
  journal={arXiv preprint arXiv:2024.xxxxx},
  year={2024}
}
```

## 🙏 Acknowledgments

- [FlashRAG](https://github.com/RUC-NLPIR/FlashRAG) for experimental methodology
- [FlexRAG](https://github.com/ictnlp/FlexRAG) for component integration
- [LevelRAG](https://github.com/microsoft/LevelRAG) for architectural inspiration

## 📞 Contact

- **Author**: Your Name
- **Email**: your.email@example.com
- **GitHub**: [@your-username](https://github.com/your-username)

---

**🎯 AdaptiveRAG: Making RAG systems truly adaptive and intelligent!**
