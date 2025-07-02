# 🔬 AdaptiveRAG 真实模型使用指南

## 📋 概述

现在 AdaptiveRAG 支持使用真实的模型和数据，让您能够直观地看到模块开关的实际效果！不再是简单的模拟数据，而是真正的：

- 🔍 **真实检索器**：BM25关键词检索 + SentenceTransformer密集检索
- 🎯 **真实重排序器**：基于查询匹配度的智能重排序
- ✨ **真实生成器**：使用 Transformer 模型生成回答
- 📊 **真实数据**：包含AI相关知识的文档库

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装真实模型所需的依赖
python3 adaptiverag/install_real_model_deps.py
```

### 2. 测试模块效果

```bash
# 运行对比测试，看到不同模块组合的实际效果
python3 adaptiverag/test_real_model_effects.py
```

### 3. 启动 WebUI

```bash
# 启动带真实模型的 WebUI
source /etc/network_turbo
conda activate flexrag
cd /root/my_project

python3 adaptiverag/launch_webui_with_module_control.py --port 7863 --host 0.0.0.0
```

### 4. 体验真实效果

1. 访问：`http://your-server:7863`
2. 点击 **🎛️ 模块控制** 标签页
3. 点击 **🔬 真实模型测试** 标签页
4. 输入查询，观察不同模块组合的实际效果！

## 🔍 真实模型 vs 模拟模型

### 🎭 之前的模拟模型
```python
# 模拟检索
def simulate_retrieval(query):
    return [
        {"title": "模拟文档1", "content": "模拟内容..."},
        {"title": "模拟文档2", "content": "模拟内容..."}
    ]

# 模拟生成
def simulate_generation(query):
    return f"这是对'{query}'的模拟回答"
```

### 🔬 现在的真实模型
```python
# 真实BM25检索
def real_keyword_retrieval(query):
    scores = self.bm25.get_scores(query.split())
    return real_documents_with_scores

# 真实密集检索
def real_dense_retrieval(query):
    query_embedding = self.embedding_model.encode([query])
    similarities = cosine_similarity(query_embedding, document_embeddings)
    return real_documents_with_similarities

# 真实生成
def real_generation(query, contexts):
    prompt = f"基于以下信息回答：{contexts}\n问题：{query}"
    return self.transformer_model.generate(prompt)
```

## 🎯 模块效果对比

现在您可以直观地看到不同模块的实际效果：

### 🔍 仅关键词检索
- **特点**：基于词汇匹配，适合精确查询
- **效果**：找到包含查询关键词的文档
- **示例**：查询"人工智能"会找到标题或内容中包含这些词的文档

### 🧠 仅密集检索  
- **特点**：基于语义相似性，适合概念查询
- **效果**：找到语义相关的文档，即使不包含确切关键词
- **示例**：查询"AI"也能找到"人工智能"相关的文档

### 🔗 混合检索
- **特点**：结合关键词和语义检索的优势
- **效果**：更全面的检索结果
- **示例**：既能精确匹配又能语义扩展

### 🎯 启用重排序
- **特点**：根据查询相关性重新排序检索结果
- **效果**：最相关的文档排在前面
- **示例**：相同的检索结果，但顺序更合理

### ⚡ 完整流程
- **特点**：任务分解 + 混合检索 + 重排序 + 生成
- **效果**：最全面和智能的处理
- **示例**：复杂查询被分解，多角度检索，智能生成

## 📊 实际测试结果示例

```
🔍 测试查询: 什么是人工智能？

🔍 仅关键词检索:
  ⏱️ 耗时: 0.05s | 📄 检索文档: 3个 | 📋 处理步骤: 2个
  💬 答案: 基于检索到的信息，人工智能（AI）是计算机科学的一个分支...

🧠 仅密集检索:
  ⏱️ 耗时: 0.12s | 📄 检索文档: 3个 | 📋 处理步骤: 2个  
  💬 答案: 根据语义相似的文档，人工智能涉及创建智能系统...

🔗 混合检索:
  ⏱️ 耗时: 0.15s | 📄 检索文档: 6个 | 📋 处理步骤: 2个
  💬 答案: 综合多种检索结果，人工智能是一个综合性领域...

🎯 混合检索+重排序:
  ⏱️ 耗时: 0.18s | 📄 检索文档: 6个 | 📋 处理步骤: 3个
  💬 答案: 基于重排序后的高质量文档，人工智能的定义更加准确...

⚡ 完整流程:
  ⏱️ 耗时: 0.25s | 📄 检索文档: 6个 | 📋 处理步骤: 5个
  💬 答案: 通过任务分解和全流程处理，提供最全面的AI解释...
```

## 🎛️ WebUI 使用指南

### 模块控制标签页
1. **预设配置**：快速选择基础/高性能/实验模式
2. **精细控制**：单独开关每个模块
3. **实时应用**：配置立即生效，无需重启

### 真实模型测试标签页
1. **查询输入**：输入您的问题
2. **处理结果**：查看详细的处理步骤
3. **检索详情**：展开查看具体的检索文档
4. **对比测试**：一键测试不同模块组合

### 效果对比功能
- **预设测试1**：仅关键词检索
- **预设测试2**：仅密集检索  
- **预设测试3**：完整流程
- **实时对比**：同一查询的不同处理结果

## 🔧 技术实现

### 真实组件架构
```python
class RealModelEngine:
    def __init__(self):
        # 真实的嵌入模型
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # 真实的生成模型
        self.tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-small')
        self.generator = AutoModelForCausalLM.from_pretrained('microsoft/DialoGPT-small')
        
        # 真实的BM25检索器
        self.bm25 = BM25Okapi(tokenized_documents)
        
        # 真实的文档库
        self.documents = load_real_documents()
```

### 模块化处理流程
```python
def process_query_with_modules(self, query):
    result = {"steps": [], "retrieval_results": []}
    
    # 根据模块配置执行不同步骤
    if self.is_module_enabled("task_decomposer"):
        subtasks = self.real_task_decomposition(query)
        result["steps"].append("任务分解完成")
    
    if self.is_module_enabled("keyword_retriever"):
        keyword_docs = self.real_keyword_retrieval(query)
        result["retrieval_results"].extend(keyword_docs)
        result["steps"].append("关键词检索完成")
    
    if self.is_module_enabled("dense_retriever"):
        dense_docs = self.real_dense_retrieval(query)
        result["retrieval_results"].extend(dense_docs)
        result["steps"].append("密集检索完成")
    
    # ... 更多模块处理
    
    return result
```

## 💡 使用建议

### 开发测试
- 使用**基础模式**：快速验证功能
- 启用**调试模式**：查看详细日志
- 关闭**实验性功能**：避免不稳定因素

### 生产环境
- 使用**高性能模式**：平衡效果和性能
- 启用**性能监控**：观察系统状态
- 根据需求**自定义配置**：优化特定场景

### 研究实验
- 使用**实验模式**：测试所有功能
- 启用**所有模块**：获得最全面的处理
- 对比**不同组合**：分析各模块贡献

## 🐛 故障排除

### 常见问题

1. **模型加载失败**
   ```bash
   # 检查依赖安装
   python3 -c "import torch, transformers, sentence_transformers"
   
   # 重新安装依赖
   python3 adaptiverag/install_real_model_deps.py
   ```

2. **内存不足**
   ```python
   # 使用更小的模型
   model_name = "microsoft/DialoGPT-small"  # 而不是 large
   
   # 减少批次大小
   batch_size = 1
   ```

3. **检索结果为空**
   ```python
   # 检查文档库是否加载
   print(f"文档数量: {len(self.documents)}")
   
   # 检查BM25初始化
   print(f"BM25可用: {self.components.get('bm25') is not None}")
   ```

### 性能优化

1. **GPU加速**：确保CUDA可用
2. **模型缓存**：首次加载后会缓存
3. **批处理**：多个查询一起处理
4. **模块选择**：根据需求禁用不必要的模块

---

🎉 **现在您可以真正体验 AdaptiveRAG 的模块化威力了！**

每个模块的开关都会产生实际的效果变化，不再是简单的界面展示。
