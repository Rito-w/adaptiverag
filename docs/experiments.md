# 🧪 实验框架

AdaptiveRAG 包含一个受 FlashRAG 启发的综合实验框架，专为严格的学术评估和与最先进方法的比较而设计。

## 🎯 框架概览

我们的实验框架提供：

- **标准化评估**: 兼容 FlashRAG 数据集和指标
- **基线比较**: 主要 RAG 方法的实现
- **消融研究**: 详细的组件贡献分析
- **可重现结果**: 可配置的学术研究实验

## 🚀 快速开始

### 运行您的第一个实验

```bash
# 使用样本数据快速测试
python quick_test.py

# 运行简单实验
python run_experiments.py quick --sample-data

# 在标准数据集上进行完整评估
python run_experiments.py full

# 消融研究
python run_experiments.py ablation
```

### 基本配置

```python
from adaptive_rag.evaluation import BenchmarkRunner, BenchmarkConfig

config = BenchmarkConfig(
    datasets=["natural_questions", "hotpot_qa"],
    methods=["adaptive_rag", "naive_rag", "self_rag"],
    output_dir="./experiments/my_experiment",
    max_samples=100,
    save_predictions=True,
    compute_bert_score=True
)

runner = BenchmarkRunner(config)
runner.run_benchmark()
```

## 📊 支持的数据集

### Single-hop QA
- **Natural Questions**: Real questions from Google search
- **TriviaQA**: Trivia questions with evidence documents
- **MS MARCO**: Microsoft machine reading comprehension
- **WebQuestions**: Questions answerable from Freebase

### Multi-hop Reasoning
- **HotpotQA**: Multi-hop reasoning over Wikipedia
- **2WikiMultihopQA**: Two-hop reasoning questions
- **MuSiQue**: Multi-hop questions requiring composition

### Conversational QA
- **QuAC**: Question Answering in Context
- **CoQA**: Conversational Question Answering

## 🔍 Evaluation Metrics

### Primary Metrics
- **Exact Match (EM)**: Exact string match with gold answer
- **F1 Score**: Token-level F1 score
- **ROUGE-L**: Longest common subsequence
- **BERTScore**: Semantic similarity using BERT embeddings

### Efficiency Metrics
- **Retrieval Time**: Average time for document retrieval
- **Generation Time**: Average time for response generation
- **Total Time**: End-to-end response time
- **Memory Usage**: Peak memory consumption

### Quality Metrics
- **Relevance Score**: Retrieved document relevance
- **Coherence Score**: Response coherence and fluency
- **Factual Accuracy**: Factual correctness of responses

## 🏗️ Baseline Methods

### Implemented Baselines

#### 1. Naive RAG
Simple retrieve-then-generate approach:
```python
class NaiveRAG:
    def process_query(self, question):
        # 1. Retrieve top-k documents
        docs = self.retriever.retrieve(question, k=5)
        
        # 2. Generate response
        response = self.generator.generate(question, docs)
        return response
```

#### 2. Self-RAG
Self-reflective RAG with iterative refinement:
```python
class SelfRAG:
    def process_query(self, question):
        for iteration in range(self.max_iterations):
            # Retrieve documents
            docs = self.retriever.retrieve(question)
            
            # Generate response
            response = self.generator.generate(question, docs)
            
            # Self-reflection
            confidence = self.reflect(question, response, docs)
            if confidence > self.threshold:
                break
                
            # Additional retrieval if needed
            question = self.refine_query(question, response)
        
        return response
```

#### 3. RAPTOR
Recursive abstractive processing:
```python
class RAPTOR:
    def process_query(self, question):
        # Build hierarchical document tree
        tree = self.build_document_tree()
        
        # Hierarchical retrieval
        docs = self.hierarchical_retrieve(question, tree)
        
        # Generate response
        response = self.generator.generate(question, docs)
        return response
```

## 🔬 Ablation Studies

### Component Analysis

Our ablation framework analyzes the contribution of each AdaptiveRAG component:

#### 1. Task Decomposition Ablation
```bash
python run_experiments.py ablation --component task_decomposition
```

Compares:
- **Full AdaptiveRAG**: With task decomposition
- **No Decomposition**: Direct query processing

#### 2. Strategy Planning Ablation
```bash
python run_experiments.py ablation --component strategy_planning
```

Compares:
- **Adaptive Planning**: Dynamic strategy selection
- **Fixed Strategy**: Single retrieval method

#### 3. Multi-Retriever Ablation
```bash
python run_experiments.py ablation --component multi_retriever
```

Compares:
- **Multi-Retriever**: Fusion of multiple methods
- **Single Retriever**: Individual retrieval methods

#### 4. Reranking Ablation
```bash
python run_experiments.py ablation --component reranking
```

Compares:
- **With Reranking**: Context optimization
- **Without Reranking**: Direct retrieval results

### Complete Ablation Study

```python
ablation_methods = [
    "adaptive_rag",                    # Full method
    "adaptive_rag_no_decomposition",   # No task decomposition
    "adaptive_rag_no_planning",        # No strategy planning
    "adaptive_rag_single_retriever",   # Single retriever only
    "adaptive_rag_no_reranking",       # No reranking
    "naive_rag",                       # Baseline comparison
]

config = BenchmarkConfig(
    datasets=["natural_questions", "hotpot_qa"],
    methods=ablation_methods,
    output_dir="./experiments/ablation_study"
)
```

## 📈 Results Analysis

### Automated Analysis

The framework includes automated analysis tools:

```python
from adaptive_rag.evaluation import AblationAnalyzer

analyzer = AblationAnalyzer("./experiments/ablation_study")
results = analyzer.analyze_component_contribution()

# Generate visualizations
analyzer.generate_visualization(results)

# Create analysis report
analyzer.generate_report(results)
```

### Performance Comparison

Example results table:

| Method | Dataset | EM | F1 | ROUGE-L | Time (s) |
|--------|---------|----|----|---------|----------|
| AdaptiveRAG | NQ | **0.52** | **0.66** | **0.71** | 2.3 |
| - No Decomposition | NQ | 0.48 | 0.62 | 0.68 | 1.8 |
| - No Planning | NQ | 0.45 | 0.59 | 0.65 | 1.9 |
| - Single Retriever | NQ | 0.41 | 0.55 | 0.61 | 1.2 |
| - No Reranking | NQ | 0.49 | 0.63 | 0.69 | 1.7 |
| Naive RAG | NQ | 0.38 | 0.51 | 0.58 | 1.0 |

### Statistical Significance

```python
from adaptive_rag.evaluation import StatisticalAnalysis

analyzer = StatisticalAnalysis()

# Perform t-test
p_value = analyzer.t_test(
    adaptive_rag_scores, 
    baseline_scores
)

# Effect size calculation
effect_size = analyzer.cohens_d(
    adaptive_rag_scores, 
    baseline_scores
)

print(f"p-value: {p_value:.4f}")
print(f"Effect size: {effect_size:.4f}")
```

## 🔧 Configuration Options

### Experiment Configuration

```yaml
# experiment_config.yaml
experiment:
  name: "adaptive_rag_evaluation"
  description: "Comprehensive evaluation of AdaptiveRAG"
  
datasets:
  - name: "natural_questions"
    split: ["test"]
    max_samples: 1000
  - name: "hotpot_qa"
    split: ["test"]
    max_samples: 500

methods:
  - name: "adaptive_rag"
    config:
      enable_task_decomposition: true
      enable_strategy_planning: true
      retrieval_topk: 10
  - name: "naive_rag"
    config:
      retrieval_topk: 5

evaluation:
  metrics: ["exact_match", "f1_score", "rouge_l", "bert_score"]
  save_predictions: true
  compute_statistical_significance: true

output:
  save_dir: "./experiments/comprehensive_eval"
  generate_plots: true
  generate_report: true
```

### Advanced Configuration

```python
from adaptive_rag.config import ExperimentConfig

config = ExperimentConfig(
    # Data settings
    data_dir="/root/autodl-tmp/data",
    datasets=["natural_questions", "hotpot_qa"],
    test_sample_num=1000,
    random_sample=False,
    
    # Method settings
    methods=["adaptive_rag", "self_rag", "naive_rag"],
    
    # Evaluation settings
    metrics=["exact_match", "f1_score", "rouge_l"],
    compute_bert_score=True,
    
    # Output settings
    save_dir="./experiments/my_experiment",
    save_predictions=True,
    save_intermediate_data=True,
    
    # Reproducibility
    seed=2024,
    
    # Performance
    batch_size=4,
    num_workers=2
)
```

## 📊 Visualization

### Performance Plots

```python
from adaptive_rag.evaluation import ResultVisualizer

visualizer = ResultVisualizer()

# Performance comparison
visualizer.plot_performance_comparison(
    results_dict, 
    metrics=["exact_match", "f1_score"],
    save_path="./plots/performance_comparison.png"
)

# Ablation analysis
visualizer.plot_ablation_analysis(
    ablation_results,
    save_path="./plots/ablation_analysis.png"
)

# Efficiency analysis
visualizer.plot_efficiency_analysis(
    timing_results,
    save_path="./plots/efficiency_analysis.png"
)
```

## 🎯 Best Practices

### Experimental Design

1. **Use Multiple Datasets**: Test on diverse datasets for generalizability
2. **Include Baselines**: Compare against established methods
3. **Statistical Testing**: Ensure statistical significance
4. **Ablation Studies**: Understand component contributions
5. **Error Analysis**: Analyze failure cases

### Reproducibility

1. **Fix Random Seeds**: Ensure reproducible results
2. **Document Configuration**: Save all experimental settings
3. **Version Control**: Track code and data versions
4. **Environment Documentation**: Record system specifications

### Reporting

1. **Clear Metrics**: Report standard evaluation metrics
2. **Statistical Significance**: Include confidence intervals
3. **Efficiency Analysis**: Report computational costs
4. **Qualitative Analysis**: Include example outputs

---

This experimental framework enables rigorous evaluation of AdaptiveRAG and fair comparison with existing methods, supporting both research and practical applications.
