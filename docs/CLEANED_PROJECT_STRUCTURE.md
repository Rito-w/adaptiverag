# 📁 AdaptiveRAG 项目结构（整理后）

## 🎯 整理说明

已删除重复、过时和不必要的文件，保持项目结构清晰简洁。

## 📂 整理后的目录结构

```
adaptiverag/
├── adaptive_rag/                    # 主要代码包
│   ├── __init__.py                 # 包初始化
│   ├── config.py                   # 配置管理
│   ├── main.py                     # 主入口
│   │
│   ├── core/                       # 核心模块 ⭐
│   │   ├── __init__.py
│   │   ├── adaptive_assistant.py           # 完整版自适应助手
│   │   ├── simplified_adaptive_assistant.py # 简化版助手（立即可用）
│   │   ├── intelligent_strategy_learner.py  # 智能策略学习器
│   │   ├── performance_optimizer.py        # 性能优化器
│   │   ├── multi_dimensional_optimizer.py  # 多维度决策优化器
│   │   ├── query_analyzer.py              # 查询分析器
│   │   ├── strategy_router.py             # 策略路由器
│   │   ├── hybrid_retriever.py            # 混合检索器
│   │   └── flexrag_integrated_assistant.py # FlexRAG集成版本
│   │
│   ├── evaluation/                 # 评估模块 ⭐
│   │   ├── enhanced_evaluator.py          # 增强评估器（自适应指标）
│   │   ├── baseline_methods.py            # 基线方法（含TurboRAG, LevelRAG）
│   │   ├── benchmark_runner.py            # 基准测试运行器
│   │   ├── dataset_downloader.py          # 数据集下载器
│   │   ├── result_analyzer.py             # 结果分析器
│   │   └── ablation_analyzer.py           # 消融分析器
│   │
│   ├── modules/                    # FlexRAG 兼容模块
│   │   ├── retriever/             # 检索器模块
│   │   ├── generator/             # 生成器模块
│   │   ├── evaluator/             # 评估器模块
│   │   ├── query_analyzer/        # 查询分析模块
│   │   ├── judger/                # 判断器模块
│   │   └── refiner/               # 精化器模块
│   │
│   ├── pipeline/                   # 流水线
│   │   ├── adaptive_pipeline.py           # 自适应流水线
│   │   └── levelrag_style_pipeline.py     # LevelRAG风格流水线
│   │
│   ├── data_processing/            # 数据处理
│   │   ├── dataset_loader.py              # 数据集加载器
│   │   └── corpus_builder.py              # 语料库构建器
│   │
│   ├── utils/                      # 工具函数
│   │   ├── logger.py                      # 日志工具
│   │   ├── model_loader.py                # 模型加载器
│   │   └── helper_functions.py            # 辅助函数
│   │
│   ├── config/                     # 配置文件
│   │   ├── adaptive_config.yaml           # 自适应配置
│   │   ├── adaptive_strategy_config.yaml  # 策略配置
│   │   └── basic_config.yaml              # 基础配置
│   │
│   ├── data/                       # 数据文件
│   │   ├── sample_corpus.jsonl            # 示例语料
│   │   ├── general_knowledge.jsonl        # 通用知识
│   │   └── e5_Flat.index                  # 向量索引
│   │
│   └── webui/                      # Web 界面
│       └── interface.py                   # 界面实现
│
├── docs/                           # 文档
│   ├── index.html                  # 文档主页（Docsify）
│   ├── _sidebar.md                 # 侧边栏
│   ├── README.md                   # 文档说明
│   ├── architecture.md             # 架构文档
│   ├── installation.md             # 安装指南
│   ├── quickstart.md               # 快速开始
│   ├── experiments.md              # 实验文档
│   └── diagrams.md                 # 图表说明
│
├── papers/                         # 参考论文 📚
│   ├── FlashRAG.pdf
│   ├── LevelRAG.pdf
│   ├── TurBoRAG.pdf
│   └── ...
│
├── experiments/                    # 实验结果
├── scripts/                        # 脚本文件
├── tests/                          # 测试文件
│
├── run_experiments.py              # 完整实验运行脚本
├── run_feasible_experiments.py     # 可行性实验脚本 ⭐
├── test_enhanced_features.py       # 增强功能测试脚本 ⭐
├── requirements.txt                # 依赖列表
├── setup.py                        # 安装脚本
├── README.md                       # 项目说明
└── ...
```

## ⭐ 核心文件说明

### 🚀 立即可用（无需训练）
- `adaptive_rag/core/simplified_adaptive_assistant.py` - 简化版自适应助手
- `run_feasible_experiments.py` - 可行性实验脚本
- `test_enhanced_features.py` - 功能测试脚本

### 🧠 完整功能（支持学习）
- `adaptive_rag/core/adaptive_assistant.py` - 完整自适应助手
- `adaptive_rag/core/intelligent_strategy_learner.py` - 智能学习器
- `adaptive_rag/core/performance_optimizer.py` - 性能优化器
- `adaptive_rag/core/multi_dimensional_optimizer.py` - 多维度优化器

### 📊 增强评估
- `adaptive_rag/evaluation/enhanced_evaluator.py` - 自适应性评估指标
- `adaptive_rag/evaluation/baseline_methods.py` - 基线方法（含最新方法）

## 🗑️ 已删除的文件

### 重复和过时的代码文件：
- ❌ `adaptive_rag/cache_manager.py` → 整合到 `performance_optimizer.py`
- ❌ `adaptive_rag/data_manager.py` → 整合到 `data_processing/`
- ❌ `adaptive_rag/multi_retriever.py` → 整合到 `hybrid_retriever.py`
- ❌ `adaptive_rag/retrieval_planner.py` → 整合到 `strategy_router.py`
- ❌ `adaptive_rag/task_decomposer.py` → 整合到 `query_analyzer.py`
- ❌ `adaptive_rag/test_*.py` → 整合到根目录测试文件

### 重复的文档：
- ❌ `GITHUB_PAGES_SETUP.md` (重复)
- ❌ `docs/github-pages-setup.md` (重复)
- ❌ `adaptive_rag/FLEXRAG_INTEGRATION.md` (重复)
- ❌ `adaptive_rag/README.md` (重复)
- ❌ `adaptive_rag/requirements.txt` (重复)

### 缓存文件：
- ❌ `adaptive_rag/__pycache__/` (Python缓存)
- ❌ `adaptive_rag/core/__pycache__/` (Python缓存)
- ❌ `adaptive_rag/evaluation/__pycache__/` (Python缓存)

## 🚀 快速开始

### 1. 立即测试（推荐）
```bash
# 测试增强功能
python test_enhanced_features.py

# 运行可行性实验
python run_feasible_experiments.py
```

### 2. 完整实验
```bash
# 快速实验
python run_experiments.py --experiment quick

# 完整实验
python run_experiments.py --experiment full
```

### 3. 查看文档
```bash
cd docs
python -m http.server 3000
# 访问 http://localhost:3000
```

## 📊 文件优先级

### 🔥 高优先级（立即可用）
1. `run_feasible_experiments.py` - 可行性实验
2. `adaptive_rag/core/simplified_adaptive_assistant.py` - 简化版系统
3. `adaptive_rag/evaluation/enhanced_evaluator.py` - 增强评估
4. `adaptive_rag/evaluation/baseline_methods.py` - 基线方法

### 🔧 中优先级（完整功能）
1. `adaptive_rag/core/adaptive_assistant.py` - 完整系统
2. `adaptive_rag/core/intelligent_strategy_learner.py` - 智能学习
3. `adaptive_rag/core/performance_optimizer.py` - 性能优化
4. `run_experiments.py` - 完整实验

### 📚 低优先级（支持功能）
1. `docs/` - 文档系统
2. `papers/` - 参考论文
3. `adaptive_rag/webui/` - Web界面
4. `tests/` - 测试文件

## 🎯 整理效果

✅ **文件数量减少**: 删除了 10+ 个重复和过时文件  
✅ **结构更清晰**: 核心功能突出，层次分明  
✅ **立即可用**: 简化版本无需训练即可运行  
✅ **扩展性好**: 完整版本支持学习和优化  
✅ **文档完善**: 保留了完整的文档系统  

现在项目结构更加清晰，重点突出，便于开发、测试和维护！
