# 🏠 AdaptiveRAG 本地模型配置指南

## 📋 概述

现在 AdaptiveRAG 支持使用您在 `/root/autodl-tmp` 目录下的本地模型和数据！这样您可以：

- 🏠 **使用本地模型**：Qwen、E5、BGE等您已下载的模型
- 📊 **使用真实数据**：HotpotQA、TriviaQA等真实数据集
- ⚡ **离线运行**：无需网络连接，完全本地化
- 💾 **智能缓存**：自动缓存索引，加速后续使用
- 🎛️ **真实效果**：模块开关产生实际的性能差异

## 🚀 快速开始

### 1. 检查本地资源

```bash
# 检查您的模型和数据是否就绪
python3 adaptiverag/check_local_resources.py
```

### 2. 安装依赖

```bash
# 安装必要的Python包
python3 adaptiverag/install_real_model_deps.py
```

### 3. 启动本地模型WebUI

```bash
# 激活环境
source /etc/network_turbo
conda activate flexrag
cd /root/my_project

# 启动本地模型版本
python3 adaptiverag/launch_local_model_webui.py --port 7863 --host 0.0.0.0
```

### 4. 体验本地模型效果

1. 访问：`http://your-server:7863`
2. 看到标题显示 **🏠 AdaptiveRAG 本地模型版**
3. 点击 **🎛️ 模块控制** 配置模块
4. 点击 **🔬 真实模型测试** 体验效果

## 📁 目录结构要求

您的 `/root/autodl-tmp` 目录应该包含：

```
/root/autodl-tmp/
├── models/                          # 模型目录
│   ├── e5-base-v2/                 # 嵌入模型 (推荐)
│   ├── bge-reranker-base/          # 重排序模型 (可选)
│   ├── Qwen2.5-1.5B-Instruct/     # 生成模型 (推荐)
│   ├── Qwen2.5-7B-Instruct/       # 大生成模型 (可选)
│   └── Qwen1.5-1.8B-Chat/         # 备用生成模型 (可选)
├── flashrag_real_data/             # 数据目录
│   ├── hotpotqa_dev.jsonl         # HotpotQA数据 (推荐)
│   ├── hotpotqa_train.jsonl       # 训练数据 (可选)
│   ├── triviaqa_dev.jsonl         # TriviaQA数据 (可选)
│   ├── nq_dev.jsonl               # Natural Questions (可选)
│   └── cache/                      # 缓存目录 (自动创建)
│       ├── bm25_index.pkl         # BM25索引缓存
│       ├── document_embeddings.npy # 文档嵌入缓存
│       └── ...                     # 其他缓存文件
└── test_results/                   # 输出目录 (自动创建)
```

## 🤖 支持的模型

### 嵌入模型 (用于密集检索)
- ✅ **e5-base-v2** (推荐)
- ✅ **bge-base-en-v1.5**
- ✅ **sentence-transformers/all-MiniLM-L6-v2**

### 重排序模型 (用于结果重排)
- ✅ **bge-reranker-base** (推荐)
- ✅ **cross-encoder/ms-marco-MiniLM-L-6-v2**

### 生成模型 (用于答案生成)
- ✅ **Qwen2.5-1.5B-Instruct** (推荐：平衡性能)
- ✅ **Qwen1.5-1.8B-Chat** (备选：更快速度)
- ✅ **Qwen2.5-7B-Instruct** (高质量：需要更多显存)

## 📊 支持的数据集

### 问答数据集
- ✅ **HotpotQA** (推荐：多跳推理)
- ✅ **TriviaQA** (备选：事实问答)
- ✅ **Natural Questions** (备选：自然问题)

### 数据格式
```json
// HotpotQA格式
{"question": "问题内容", "answer": "答案内容", "context": [...]}

// TriviaQA格式  
{"query": "查询内容", "golden_answers": ["答案1", "答案2"]}
```

## ⚙️ 配置说明

系统会自动检测您的本地资源并生成最优配置。您也可以手动编辑 `adaptive_rag/config/modular_config.yaml`：

```yaml
# 路径配置
paths:
  models_dir: "/root/autodl-tmp/models"
  data_dir: "/root/autodl-tmp"
  flashrag_data_dir: "/root/autodl-tmp/flashrag_real_data"
  cache_dir: "/root/autodl-tmp/flashrag_real_data/cache"

# 检索器配置
retrievers:
  dense_retriever:
    model_name: "/root/autodl-tmp/models/e5-base-v2"
    device: "cuda"

# 生成器配置
generators:
  main_generator:
    model_name: "/root/autodl-tmp/models/Qwen2.5-1.5B-Instruct"
    device: "cuda"
    torch_dtype: "float16"

# 数据配置
data:
  corpus_path: "/root/autodl-tmp/flashrag_real_data/hotpotqa_dev.jsonl"
```

## 🎛️ 模块效果对比

使用本地模型后，您可以清楚地看到不同模块的实际效果：

### 🔍 检索器对比
```
查询: "什么是量子计算？"

仅关键词检索 (BM25):
- 找到包含"量子计算"关键词的文档
- 基于词汇匹配，精确但可能遗漏同义词

仅密集检索 (E5):
- 找到语义相关的文档，如"quantum computing"
- 基于语义理解，覆盖面更广

混合检索:
- 结合两种方法的优势
- 既有精确匹配又有语义扩展
```

### 🎯 重排序效果
```
启用重排序前:
1. 文档A (BM25分数: 0.8)
2. 文档B (E5分数: 0.9)  
3. 文档C (BM25分数: 0.7)

启用重排序后:
1. 文档B (重排序分数: 0.95) ← 更相关
2. 文档A (重排序分数: 0.85)
3. 文档C (重排序分数: 0.75)
```

### ✨ 生成器对比
```
简单拼接:
"基于检索到的信息：量子计算是一种计算方式..."

Qwen生成:
"量子计算是一种利用量子力学原理进行信息处理的计算模式。
与传统计算机使用比特不同，量子计算机使用量子比特(qubit)，
能够同时处于0和1的叠加态，从而实现并行计算..."
```

## 🔧 故障排除

### 常见问题

1. **模型加载失败**
   ```bash
   # 检查模型文件完整性
   ls -la /root/autodl-tmp/models/Qwen2.5-1.5B-Instruct/
   
   # 应该包含: config.json, pytorch_model.bin, tokenizer.json
   ```

2. **显存不足**
   ```yaml
   # 使用更小的模型
   generators:
     main_generator:
       model_name: "/root/autodl-tmp/models/Qwen1.5-1.8B-Chat"
       torch_dtype: "float16"  # 使用半精度
   ```

3. **数据加载失败**
   ```bash
   # 检查数据文件格式
   head -n 1 /root/autodl-tmp/flashrag_real_data/hotpotqa_dev.jsonl
   
   # 应该是有效的JSON格式
   ```

4. **缓存问题**
   ```bash
   # 清除缓存重新生成
   rm -rf /root/autodl-tmp/flashrag_real_data/cache/*
   ```

### 性能优化

1. **GPU加速**
   ```bash
   # 确保CUDA可用
   python3 -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
   ```

2. **内存优化**
   ```yaml
   # 限制数据量
   data:
     max_documents: 1000  # 限制加载的文档数量
   ```

3. **批处理优化**
   ```yaml
   basic:
     batch_size: 2  # 减少批次大小
   ```

## 📊 性能监控

启动后可以在WebUI中监控：

- **模型加载状态**：各个模型是否成功加载
- **数据统计**：加载的文档数量和大小
- **缓存状态**：索引缓存的生成和使用情况
- **处理时间**：各个模块的实际耗时
- **显存使用**：GPU内存占用情况

## 💡 最佳实践

1. **首次运行**：
   - 先运行资源检查脚本
   - 使用小数据集测试
   - 观察缓存生成过程

2. **生产使用**：
   - 启用所有可用模块
   - 使用完整数据集
   - 定期清理缓存

3. **开发调试**：
   - 启用调试模式
   - 使用小模型快速迭代
   - 监控资源使用情况

---

🎉 **现在您可以完全使用本地资源运行 AdaptiveRAG 了！**

每个模块的开关都会产生真实的效果变化，让您真正体验模块化RAG的威力。
