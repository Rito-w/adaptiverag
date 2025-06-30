# 📦 Installation Guide

This guide will help you install AdaptiveRAG and its dependencies.

## 🔧 Prerequisites

Before installing AdaptiveRAG, make sure you have:

- **Python 3.8+**: AdaptiveRAG requires Python 3.8 or higher
- **PyTorch 1.9+**: For neural network components
- **CUDA (optional)**: For GPU acceleration
- **Git**: For development installation

### Check Your Python Version

```bash
python --version
# Should show Python 3.8.0 or higher
```

## 🚀 Quick Install

### Option 1: Install from PyPI (Recommended)

```bash
pip install adaptiverag
```

### Option 2: Install from GitHub

```bash
pip install git+https://github.com/Rito-w/adaptiverag.git
```

## 🛠️ Development Installation

For development or to get the latest features:

### 1. Clone the Repository

```bash
git clone https://github.com/Rito-w/adaptiverag.git
cd adaptiverag
```

### 2. Create Virtual Environment (Recommended)

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n adaptiverag python=3.9
conda activate adaptiverag
```

### 3. Install in Development Mode

```bash
# Basic installation
pip install -e .

# With development dependencies
pip install -e ".[dev]"

# With all optional dependencies
pip install -e ".[dev,docs,experiments]"
```

## 📦 Optional Dependencies

AdaptiveRAG has several optional dependency groups:

### Development Dependencies
```bash
pip install "adaptiverag[dev]"
```
Includes: pytest, black, isort, flake8, mypy, pre-commit

### Documentation Dependencies
```bash
pip install "adaptiverag[docs]"
```
Includes: sphinx, sphinx-rtd-theme, myst-parser

### Experiment Dependencies
```bash
pip install "adaptiverag[experiments]"
```
Includes: matplotlib, seaborn, plotly, jupyter

### All Dependencies
```bash
pip install "adaptiverag[dev,docs,experiments]"
```

## 🔗 FlexRAG Integration

For FlexRAG integration (optional but recommended):

```bash
# Install FlexRAG
pip install flexrag

# Or from source
git clone https://github.com/ictnlp/FlexRAG.git
cd FlexRAG
pip install -e .
```

## ✅ Verify Installation

### Basic Verification

```python
import adaptive_rag
print(f"AdaptiveRAG version: {adaptive_rag.__version__}")
```

### Test Core Components

```python
from adaptive_rag.config import AdaptiveRAGConfig
from adaptive_rag.evaluation.baseline_methods import create_baseline_method

# Test configuration
config = AdaptiveRAGConfig()
print(f"Default dataset: {config['dataset_name']}")

# Test baseline methods
method = create_baseline_method("naive_rag", {"retrieval_topk": 5})
print(f"Method created: {method.__class__.__name__}")
```

### Run Quick Test

```bash
cd adaptiverag
python quick_test.py
```

Expected output:
```
🧪 AdaptiveRAG 快速测试 (FlexRAG环境)
============================================================
✅ 基本功能 测试通过
✅ FlashRAG集成 测试通过
✅ FlexRAG组件 测试通过
✅ 迷你实验 测试通过
🎯 测试结果: 4/4 通过
🎉 所有测试通过！AdaptiveRAG实验框架准备就绪
```

## 🐛 Troubleshooting

### Common Issues

#### 1. PyTorch Installation Issues

```bash
# For CPU-only installation
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# For CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

#### 2. FAISS Installation Issues

```bash
# For CPU-only
pip install faiss-cpu

# For GPU (if you have CUDA)
pip install faiss-gpu
```

#### 3. Permission Errors

```bash
# Use --user flag
pip install --user adaptiverag

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate
pip install adaptiverag
```

#### 4. Dependency Conflicts

```bash
# Create fresh environment
conda create -n adaptiverag-clean python=3.9
conda activate adaptiverag-clean
pip install adaptiverag
```

### Environment-Specific Instructions

#### Google Colab

```python
!pip install adaptiverag
!pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### Jupyter Notebook

```bash
# Install in notebook
!pip install adaptiverag

# Restart kernel after installation
```

#### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install adaptiverag

COPY . .
CMD ["python", "your_script.py"]
```

## 🔄 Updating AdaptiveRAG

### Update from PyPI

```bash
pip install --upgrade adaptiverag
```

### Update Development Installation

```bash
cd adaptiverag
git pull origin main
pip install -e .
```

## 🎯 Next Steps

After successful installation:

1. **Read the [Quick Start Guide](quickstart.md)**
2. **Explore the [Architecture Overview](architecture.md)**
3. **Try the [Experiments](experiments.md)**
4. **Check out the [API Reference](api/)**

## 📞 Getting Help

If you encounter issues:

1. **Check the [Troubleshooting Guide](troubleshooting.md)**
2. **Search [GitHub Issues](https://github.com/Rito-w/adaptiverag/issues)**
3. **Ask in [GitHub Discussions](https://github.com/Rito-w/adaptiverag/discussions)**
4. **Contact the maintainers**

---

**🎉 Welcome to AdaptiveRAG! You're ready to start building intelligent retrieval-augmented generation systems.**
