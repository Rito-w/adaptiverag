# 📁 AdaptiveRAG Project Structure

## 🏗️ Directory Overview

```
adaptiverag/
├── 📄 README.md                     # Project overview and quick start
├── 📄 LICENSE                       # MIT License
├── 📄 CONTRIBUTING.md               # Contribution guidelines
├── 📄 CHANGELOG.md                  # Version history and changes
├── 📄 setup.py                      # Package installation configuration
├── 📄 requirements.txt              # Python dependencies
├── 📄 .gitignore                    # Git ignore patterns
├── 📄 PROJECT_STRUCTURE.md          # This file
├── 📄 EXPERIMENT_FRAMEWORK_SUMMARY.md # Experimental framework summary
│
├── 🧠 adaptive_rag/                 # Core AdaptiveRAG implementation
│   ├── 📄 __init__.py
│   ├── 📄 config.py                 # Configuration system
│   ├── 📁 core/                     # Core components
│   │   ├── 📄 __init__.py
│   │   ├── 📄 flexrag_integrated_assistant.py
│   │   ├── 📄 task_decomposer.py
│   │   ├── 📄 retrieval_planner.py
│   │   └── 📄 context_reranker.py
│   ├── 📁 modules/                  # Individual modules
│   │   ├── 📄 __init__.py
│   │   ├── 📄 query_analyzer.py
│   │   ├── 📄 multi_retriever.py
│   │   └── 📄 adaptive_generator.py
│   ├── 📁 pipeline/                 # Pipeline implementations
│   │   ├── 📄 __init__.py
│   │   ├── 📄 adaptive_pipeline.py
│   │   └── 📄 evaluation_pipeline.py
│   ├── 📁 evaluation/               # Evaluation framework
│   │   ├── 📄 __init__.py
│   │   ├── 📄 benchmark_runner.py   # Main benchmark runner
│   │   ├── 📄 dataset_downloader.py # Dataset management
│   │   ├── 📄 baseline_methods.py   # Baseline implementations
│   │   ├── 📄 ablation_analyzer.py  # Ablation study tools
│   │   └── 📄 result_analyzer.py    # Result analysis
│   ├── 📁 webui/                    # Web interface
│   │   ├── 📄 __init__.py
│   │   ├── 📄 app.py
│   │   └── 📄 components.py
│   └── 📁 utils/                    # Utility functions
│       ├── 📄 __init__.py
│       ├── 📄 logging_utils.py
│       └── 📄 data_utils.py
│
├── 🧪 tests/                        # Test suite
│   ├── 📄 __init__.py
│   ├── 📄 test_config.py            # Configuration tests
│   ├── 📄 test_core.py              # Core component tests
│   ├── 📄 test_evaluation.py        # Evaluation framework tests
│   └── 📄 test_integration.py       # Integration tests
│
├── 📊 experiments/                  # Experiment results
│   ├── 📄 .gitkeep                  # Keep directory in git
│   ├── 📁 quick_test/               # Quick test results
│   ├── 📁 full_evaluation/          # Full evaluation results
│   ├── 📁 ablation_study/           # Ablation study results
│   └── 📁 paper_results/            # Academic paper results
│
├── 📚 docs/                         # Documentation
│   ├── 📄 installation.md           # Installation guide
│   ├── 📄 configuration.md          # Configuration reference
│   ├── 📄 api.md                    # API documentation
│   ├── 📄 experiments.md            # Experiment guide
│   └── 📄 architecture.md           # Architecture overview
│
├── 🔧 scripts/                      # Utility scripts
│   ├── 📄 setup_environment.sh      # Environment setup
│   ├── 📄 run_benchmarks.sh         # Benchmark runner
│   └── 📄 generate_paper_results.sh # Paper result generator
│
├── 📄 run_experiments.py            # Main experiment runner
└── 📄 quick_test.py                 # Quick functionality test
```

## 🎯 Key Components

### 1. Core Implementation (`adaptive_rag/`)
- **Configuration System**: Flexible YAML and dictionary-based configuration
- **Core Components**: Task decomposer, retrieval planner, context reranker
- **Modules**: Query analyzer, multi-retriever, adaptive generator
- **Pipeline**: End-to-end processing pipeline
- **Evaluation**: Comprehensive evaluation framework
- **WebUI**: Interactive web interface

### 2. Evaluation Framework (`adaptive_rag/evaluation/`)
- **Benchmark Runner**: Main evaluation orchestrator
- **Dataset Downloader**: Automatic dataset management
- **Baseline Methods**: Implementation of comparison methods
- **Ablation Analyzer**: Component contribution analysis
- **Result Analyzer**: Performance analysis and visualization

### 3. Experimental Infrastructure
- **Tests**: Comprehensive test suite for reliability
- **Scripts**: Automation and setup utilities
- **Documentation**: Complete project documentation
- **Experiments**: Organized result storage

## 📋 File Descriptions

### Core Files
- `README.md`: Project overview, installation, and usage
- `setup.py`: Python package configuration
- `requirements.txt`: Dependency specifications
- `run_experiments.py`: Main experiment execution script

### Configuration
- `adaptive_rag/config.py`: Centralized configuration management
- Support for YAML files and dictionary overrides
- Automatic environment setup and validation

### Evaluation
- `benchmark_runner.py`: Orchestrates all evaluation tasks
- `baseline_methods.py`: Naive RAG, Self-RAG, RAPTOR implementations
- `dataset_downloader.py`: FlashRAG dataset integration
- `ablation_analyzer.py`: Component contribution analysis

### Testing
- `tests/test_config.py`: Configuration system tests
- `quick_test.py`: Rapid functionality verification
- Comprehensive test coverage for all components

## 🚀 Usage Patterns

### Development Workflow
1. **Setup**: `scripts/setup_environment.sh`
2. **Test**: `python quick_test.py`
3. **Develop**: Edit core components
4. **Evaluate**: `python run_experiments.py`
5. **Commit**: Standard git workflow

### Experiment Workflow
1. **Configure**: Edit config files or use CLI args
2. **Run**: Execute experiment scripts
3. **Analyze**: Use built-in analysis tools
4. **Report**: Generate academic paper results

### Extension Points
- Add new retrieval methods in `modules/`
- Implement new baselines in `evaluation/baseline_methods.py`
- Create custom evaluation metrics in `evaluation/`
- Extend configuration in `config.py`

## 📊 Data Flow

```
Query → Task Decomposer → Retrieval Planner → Multi-Retriever → Context Reranker → Generator → Response
                                    ↓
                            Evaluation Framework
                                    ↓
                            Results & Analysis
```

## 🔧 Maintenance

### Regular Tasks
- Update dependencies in `requirements.txt`
- Add new tests for new features
- Update documentation for API changes
- Run full test suite before releases

### Release Process
1. Update `CHANGELOG.md`
2. Bump version in `setup.py`
3. Run full test suite
4. Create git tag
5. Push to repository

---

**🎯 This structure provides a solid foundation for AdaptiveRAG development, experimentation, and academic research!**
