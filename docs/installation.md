# 📦 安装指南

本指南将帮助您安装 AdaptiveRAG 及其依赖项。

## 🔧 前置要求

在安装 AdaptiveRAG 之前，请确保您具备：

- **Python 3.8+**: AdaptiveRAG 需要 Python 3.8 或更高版本
- **PyTorch 1.9+**: 用于神经网络组件
- **CUDA (可选)**: 用于 GPU 加速
- **Git**: 用于开发安装

### 检查您的 Python 版本

```bash
python --version
# 应显示 Python 3.8.0 或更高版本
```

## 🚀 快速安装

### 选项 1: 从 PyPI 安装 (推荐)

```bash
pip install adaptiverag
```

### 选项 2: 从 GitHub 安装

```bash
pip install git+https://github.com/Rito-w/adaptiverag.git
```

## 🛠️ 开发安装

用于开发或获取最新功能：

### 1. 克隆仓库

```bash
git clone https://github.com/Rito-w/adaptiverag.git
cd adaptiverag
```

### 2. 创建虚拟环境 (推荐)

```bash
# 使用 venv
python -m venv venv
source venv/bin/activate  # Windows 系统: venv\Scripts\activate

# 或使用 conda
conda create -n adaptiverag python=3.9
conda activate adaptiverag
```

### 3. 以开发模式安装

```bash
# 基础安装
pip install -e .

# 包含开发依赖
pip install -e ".[dev]"

# 包含所有可选依赖
pip install -e ".[dev,docs,experiments]"
```

## 📦 可选依赖

AdaptiveRAG 有几个可选的依赖组：

### 开发依赖
```bash
pip install "adaptiverag[dev]"
```
包含: pytest, black, isort, flake8, mypy, pre-commit

### 文档依赖
```bash
pip install "adaptiverag[docs]"
```
包含: sphinx, sphinx-rtd-theme, myst-parser

### 实验依赖
```bash
pip install "adaptiverag[experiments]"
```
包含: matplotlib, seaborn, plotly, jupyter

### 所有依赖
```bash
pip install "adaptiverag[dev,docs,experiments]"
```

## 🔗 FlexRAG 集成

FlexRAG 集成 (可选但推荐)：

```bash
# 安装 FlexRAG
pip install flexrag

# 或从源码安装
git clone https://github.com/ictnlp/FlexRAG.git
cd FlexRAG
pip install -e .
```

## ✅ 验证安装

### 基础验证

```python
import adaptive_rag
print(f"AdaptiveRAG 版本: {adaptive_rag.__version__}")
```

### 测试核心组件

```python
from adaptive_rag.config import AdaptiveRAGConfig
from adaptive_rag.evaluation.baseline_methods import create_baseline_method

# 测试配置
config = AdaptiveRAGConfig()
print(f"默认数据集: {config['dataset_name']}")

# 测试基线方法
method = create_baseline_method("naive_rag", {"retrieval_topk": 5})
print(f"方法已创建: {method.__class__.__name__}")
```

### 运行快速测试

```bash
cd adaptiverag
python quick_test.py
```

预期输出:
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

## 🐛 故障排除

### 常见问题

#### 1. PyTorch 安装问题

```bash
# 仅 CPU 安装
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

#### 2. FAISS 安装问题

```bash
# 仅 CPU
pip install faiss-cpu

# GPU (如果您有 CUDA)
pip install faiss-gpu
```

#### 3. 权限错误

```bash
# 使用 --user 标志
pip install --user adaptiverag

# 或使用虚拟环境 (推荐)
python -m venv venv
source venv/bin/activate
pip install adaptiverag
```

#### 4. 依赖冲突

```bash
# 创建全新环境
conda create -n adaptiverag-clean python=3.9
conda activate adaptiverag-clean
pip install adaptiverag
```

### 特定环境说明

#### Google Colab

```python
!pip install adaptiverag
!pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### Jupyter Notebook

```bash
# 在 notebook 中安装
!pip install adaptiverag

# 安装后重启内核
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

## 🔄 更新 AdaptiveRAG

### 从 PyPI 更新

```bash
pip install --upgrade adaptiverag
```

### 更新开发安装

```bash
cd adaptiverag
git pull origin main
pip install -e .
```

## 🎯 下一步

安装成功后：

1. **阅读 [快速开始指南](quickstart.md)**
2. **探索 [架构概览](architecture.md)**
3. **尝试 [实验](experiments.md)**
4. **查看 [API 参考](api/)**

## 📞 获取帮助

如果遇到问题：

1. **查看 [故障排除指南](troubleshooting.md)**
2. **搜索 [GitHub Issues](https://github.com/Rito-w/adaptiverag/issues)**
3. **在 [GitHub Discussions](https://github.com/Rito-w/adaptiverag/discussions) 中提问**
4. **联系维护者**

---

**🎉 欢迎使用 AdaptiveRAG！您已准备好开始构建智能检索增强生成系统。**
