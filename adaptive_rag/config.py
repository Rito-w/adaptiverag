#!/usr/bin/env python3
"""
=== 智能自适应 RAG 配置模块 ===

深度集成 FlexRAG 组件的配置系统
"""

import os
import yaml
import random
import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

# 导入 FlexRAG 组件配置
try:
    from flexrag.retriever import RetrieverConfig, RETRIEVERS
    from flexrag.ranker import RankerConfig, RANKERS
    from flexrag.models import GeneratorConfig, EncoderConfig, GENERATORS, ENCODERS
    FLEXRAG_AVAILABLE = True
except ImportError:
    print("⚠️ FlexRAG 未安装，将使用简化配置")
    FLEXRAG_AVAILABLE = False


@dataclass
class ModuleToggleConfig:
    """模块开关配置 - 精细控制每个模块的启用状态"""

    # === 核心处理模块 ===
    task_decomposer: bool = True              # 任务分解器
    retrieval_planner: bool = True            # 检索规划器
    multi_retriever: bool = True              # 多重检索系统
    context_reranker: bool = True             # 上下文重排器
    adaptive_generator: bool = True           # 自适应生成器

    # === 智能分析模块 ===
    query_analyzer: bool = True               # 查询分析器
    strategy_router: bool = True              # 策略路由器
    performance_optimizer: bool = True        # 性能优化器
    intelligent_strategy_learner: bool = False # 智能策略学习器（实验性）
    multi_dimensional_optimizer: bool = False # 多维度优化器（实验性）
    resource_aware_optimizer: bool = False    # 资源感知优化器（实验性）

    # === 检索器模块 ===
    keyword_retriever: bool = True            # 关键词检索器
    dense_retriever: bool = True              # 密集检索器
    web_retriever: bool = False               # 网络检索器（需要API）
    hybrid_retriever: bool = True             # 混合检索器

    # === 重排序模块 ===
    cross_encoder_ranker: bool = True         # 交叉编码器重排
    colbert_ranker: bool = False              # ColBERT重排（需要模型）
    gpt_ranker: bool = False                  # GPT重排（需要API）

    # === 生成器模块 ===
    template_generator: bool = True           # 模板生成器
    freeform_generator: bool = True           # 自由形式生成器
    dialogue_generator: bool = False          # 对话生成器（实验性）

    # === 评估模块 ===
    fact_verification: bool = False           # 事实验证（实验性）
    confidence_estimation: bool = True        # 置信度估计
    result_analyzer: bool = True              # 结果分析器

    # === 缓存模块 ===
    semantic_cache: bool = True               # 语义缓存
    predictive_cache: bool = False            # 预测性缓存（实验性）

    # === 用户体验模块 ===
    personalization: bool = False             # 个性化（实验性）
    multimodal_support: bool = False          # 多模态支持（实验性）

    # === 调试和监控模块 ===
    debug_mode: bool = False                  # 调试模式
    performance_monitoring: bool = True       # 性能监控
    logging_enhanced: bool = True             # 增强日志


@dataclass
class SubTaskConfig:
    """子任务配置"""
    type: str = "factual"  # factual, semantic, temporal, comparative
    priority: float = 1.0
    max_decompose_depth: int = 3
    enable_entity_extraction: bool = True
    enable_temporal_analysis: bool = True


@dataclass
class RetrievalPlanConfig:
    """检索策略配置"""
    # 检索器权重配置
    default_weights: Dict[str, float] = field(default_factory=lambda: {
        "keyword": 0.33,
        "dense": 0.33, 
        "web": 0.34
    })
    
    # 任务类型特定权重
    task_specific_weights: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        "factual": {"keyword": 0.7, "dense": 0.2, "web": 0.1},
        "semantic": {"keyword": 0.2, "dense": 0.7, "web": 0.1},
        "temporal": {"keyword": 0.3, "dense": 0.2, "web": 0.5},
        "comparative": {"keyword": 0.4, "dense": 0.4, "web": 0.2}
    })
    
    # 每个检索器的 top-k 配置
    top_k_config: Dict[str, int] = field(default_factory=lambda: {
        "keyword": 10,
        "dense": 10,
        "web": 5
    })


@dataclass
class RelevanceScoreConfig:
    """相关度评分配置"""
    # 评分维度权重
    score_weights: Dict[str, float] = field(default_factory=lambda: {
        "semantic": 0.3,
        "factual": 0.3,
        "temporal": 0.1,
        "entity": 0.2,
        "diversity": 0.1
    })
    
    # 任务类型特定权重
    task_specific_score_weights: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        "factual": {"semantic": 0.3, "factual": 0.4, "temporal": 0.1, "entity": 0.15, "diversity": 0.05},
        "semantic": {"semantic": 0.5, "factual": 0.2, "temporal": 0.1, "entity": 0.1, "diversity": 0.1},
        "temporal": {"semantic": 0.2, "factual": 0.2, "temporal": 0.4, "entity": 0.1, "diversity": 0.1},
        "comparative": {"semantic": 0.25, "factual": 0.25, "temporal": 0.1, "entity": 0.2, "diversity": 0.2}
    })


@dataclass
class ContextAggregationConfig:
    """上下文聚合配置"""
    max_primary_contexts: int = 3
    max_supporting_contexts: int = 5
    max_background_contexts: int = 2
    
    # 相关度阈值
    primary_threshold: float = 0.8
    supporting_threshold: float = 0.5
    
    # 去重配置
    similarity_threshold: float = 0.85
    enable_conflict_resolution: bool = True


# 首先定义基础配置类（保持向后兼容）
@dataclass
class AdaptiveRAGConfig:
    """智能自适应 RAG 总配置（原始版本）"""

    # 基础配置
    device: str = "cuda"
    batch_size: int = 4
    max_input_length: int = 2048

    # 模型路径配置 - 使用 adaptive_rag 内部相对路径
    model_paths: Dict[str, str] = field(default_factory=lambda: {
        "keyword_retriever": "bm25",
        "dense_retriever": "./adaptive_rag/models/e5-base-v2",
        "generator": "./adaptive_rag/models/qwen1.5-1.8b",
        "reranker": "./adaptive_rag/models/bge-reranker-base"
    })

    # 数据路径配置 - 使用 adaptive_rag 内部数据
    data_paths: Dict[str, str] = field(default_factory=lambda: {
        "corpus_path": "./adaptive_rag/data/general_knowledge.jsonl",
        "index_path": "./adaptive_rag/data/e5_Flat.index"
    })

    # 任务类型特定权重
    task_specific_weights: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        "factual": {"keyword": 0.7, "dense": 0.2, "web": 0.1},
        "semantic": {"keyword": 0.2, "dense": 0.7, "web": 0.1},
        "temporal": {"keyword": 0.3, "dense": 0.2, "web": 0.5},
        "comparative": {"keyword": 0.4, "dense": 0.4, "web": 0.2}
    })

    # 生成配置
    generation_params: Dict[str, Any] = field(default_factory=lambda: {
        "do_sample": True,
        "max_tokens": 256,
        "temperature": 0.7,
        "top_p": 0.9
    })

    # 评估配置
    metrics: List[str] = field(default_factory=lambda: ["em", "f1", "acc"])

    # 调试配置
    debug_mode: bool = False
    save_intermediate_results: bool = True
    log_level: str = "INFO"


@dataclass
class FlexRAGIntegratedConfig:
    """深度集成 FlexRAG 的配置类"""

    # === 模块开关配置 ===
    modules: ModuleToggleConfig = field(default_factory=ModuleToggleConfig)

    # 基础配置
    device: str = "cuda"
    batch_size: int = 4
    max_input_length: int = 2048

    # FlexRAG 检索器配置（简化版，主要使用模拟实现）
    retriever_configs: Dict[str, Any] = field(default_factory=lambda: {
        "keyword_retriever": {
            "retriever_type": "mock",
            "config": {
                "retriever_path": "./adaptive_rag/data/keyword_index"
            }
        },
        "dense_retriever": {
            "retriever_type": "mock",
            "config": {
                "retriever_path": "./adaptive_rag/data/dense_index"
            }
        },
        "web_retriever": {
            "retriever_type": "mock",
            "config": {
                "search_engine": "google"
            }
        }
    })

    # FlexRAG 重排序器配置（简化版）
    ranker_configs: Dict[str, Any] = field(default_factory=lambda: {
        "cross_encoder": {
            "ranker_type": "mock",
            "config": {
                "model_name": "BAAI/bge-reranker-base",
                "reserve_num": 10
            }
        },
        "colbert": {
            "ranker_type": "mock",
            "config": {
                "model_name": "colbert-ir/colbertv2.0",
                "reserve_num": 10
            }
        }
    })

    # FlexRAG 生成器配置（简化版）
    generator_configs: Dict[str, Any] = field(default_factory=lambda: {
        "main_generator": {
            "generator_type": "mock",
            "config": {
                "model_path": "./adaptive_rag/models/qwen1.5-1.8b",
                "model_type": "causal_lm"
            }
        },
        "openai_generator": {
            "generator_type": "mock",
            "config": {
                "model_name": "gpt-3.5-turbo",
                "api_key": "${OPENAI_API_KEY}"
            }
        }
    })

    # FlexRAG 编码器配置
    encoder_configs: Dict[str, Any] = field(default_factory=lambda: {
        "dense_encoder": {
            "encoder_type": "sentence_transformer",
            "sentence_transformer_config": {
                "model_name": "sentence-transformers/all-MiniLM-L6-v2",
                "device": "cuda"
            }
        },
        "openai_encoder": {
            "encoder_type": "openai",
            "openai_config": {
                "model_name": "text-embedding-ada-002",
                "api_key": "${OPENAI_API_KEY}"
            }
        }
    })
    
    # 子模块配置
    subtask_config: SubTaskConfig = field(default_factory=SubTaskConfig)
    retrieval_plan_config: RetrievalPlanConfig = field(default_factory=RetrievalPlanConfig)
    relevance_score_config: RelevanceScoreConfig = field(default_factory=RelevanceScoreConfig)
    context_aggregation_config: ContextAggregationConfig = field(default_factory=ContextAggregationConfig)
    
    # 生成配置
    generation_params: Dict[str, Any] = field(default_factory=lambda: {
        "do_sample": True,
        "max_tokens": 256,
        "temperature": 0.7,
        "top_p": 0.9
    })
    
    # 评估配置
    metrics: List[str] = field(default_factory=lambda: ["em", "f1", "acc"])
    
    # 调试配置
    debug_mode: bool = False
    save_intermediate_results: bool = True
    log_level: str = "INFO"


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: Optional[str] = None, config_dict: Optional[Dict] = None):
        self.config = AdaptiveRAGConfig()
        
        # 从文件加载配置
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
        
        # 从字典更新配置
        if config_dict:
            self.update_from_dict(config_dict)
    
    def load_from_file(self, config_file: str):
        """从 YAML 文件加载配置"""
        with open(config_file, 'r', encoding='utf-8') as f:
            file_config = yaml.safe_load(f)
        self.update_from_dict(file_config)
    
    def update_from_dict(self, config_dict: Dict):
        """从字典更新配置"""
        for key, value in config_dict.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
    
    def save_to_file(self, config_file: str):
        """保存配置到文件"""
        config_dict = self.to_dict()
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        def convert_dataclass(obj):
            if hasattr(obj, '__dataclass_fields__'):
                return {k: convert_dataclass(v) for k, v in obj.__dict__.items()}
            elif isinstance(obj, dict):
                return {k: convert_dataclass(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_dataclass(item) for item in obj]
            else:
                return obj
        
        return convert_dataclass(self.config)
    
    def get_config(self) -> AdaptiveRAGConfig:
        """获取配置对象"""
        return self.config
    
    def __getitem__(self, key):
        """支持字典式访问"""
        return getattr(self.config, key)
    
    def __setitem__(self, key, value):
        """支持字典式设置"""
        setattr(self.config, key, value)


def get_project_root() -> str:
    """获取项目根目录"""
    current_dir = os.path.dirname(os.path.abspath(__file__))  # adaptive_rag 目录
    return os.path.dirname(current_dir)  # 项目根目录

def resolve_path(path: str) -> str:
    """解析路径，支持相对路径和绝对路径"""
    if os.path.isabs(path):
        return path
    else:
        # 相对路径基于项目根目录，规范化路径
        resolved = os.path.join(get_project_root(), path)
        return os.path.normpath(resolved)

def create_default_config() -> AdaptiveRAGConfig:
    """创建默认配置"""
    config = AdaptiveRAGConfig()

    # 解析模型路径
    for key, path in config.model_paths.items():
        if key != "keyword_retriever":  # bm25 不需要路径解析
            config.model_paths[key] = resolve_path(path)

    # 解析数据路径
    for key, path in config.data_paths.items():
        config.data_paths[key] = resolve_path(path)

    return config


def load_config(config_file: Optional[str] = None, config_dict: Optional[Dict] = None) -> AdaptiveRAGConfig:
    """加载配置的便捷函数"""
    manager = ConfigManager(config_file, config_dict)
    return manager.get_config()


# ===== 实验配置系统 (借鉴 FlashRAG) =====

@dataclass
class ExperimentConfig:
    """实验配置 - 借鉴 FlashRAG 的实验设计"""

    # 环境设置
    data_dir: str = "./data/benchmarks"
    save_dir: str = "./experiments"
    gpu_id: str = "0"
    seed: int = 2024

    # 数据集设置
    dataset_name: str = "natural_questions"
    split: List[str] = field(default_factory=lambda: ["test"])
    test_sample_num: Optional[int] = None  # None 表示使用全部数据
    random_sample: bool = False

    # 保存设置
    save_intermediate_data: bool = True
    save_predictions: bool = True
    save_note: str = "adaptive_rag_experiment"

    # 评估设置
    metrics: List[str] = field(default_factory=lambda: [
        "exact_match", "f1_score", "rouge_l", "bert_score"
    ])
    compute_bert_score: bool = True

    # 方法设置
    method_name: str = "adaptive_rag"
    baseline_methods: List[str] = field(default_factory=lambda: [
        "naive_rag", "self_rag"
    ])


@dataclass
class DatasetConfig:
    """数据集配置 - 兼容 FlashRAG 数据格式"""

    # 支持的数据集映射 (FlashRAG 格式)
    DATASET_MAPPING = {
        # 单跳问答
        "natural_questions": "nq",
        "trivia_qa": "trivia",
        "ms_marco": "msmarco",

        # 多跳推理
        "hotpot_qa": "hotpot",
        "2wiki_multihop": "2wiki",
        "musique": "musique",

        # 对话问答
        "quac": "quac",
        "coqa": "coqa",

        # 开放域问答
        "web_questions": "webq",
        "entity_questions": "entityq"
    }

    # 数据集路径配置
    dataset_path: str = "./data/benchmarks"
    corpus_path: str = "./data/corpus/wiki_2021.jsonl"
    index_path: str = "./data/indexes"

    # 数据处理配置
    max_context_length: int = 512
    max_question_length: int = 256
    max_answer_length: int = 128


# 示例配置文件内容 (借鉴 FlashRAG 格式)
EXAMPLE_CONFIG_YAML = """
# ===== AdaptiveRAG 实验配置 (借鉴 FlashRAG) =====

# ------------------------------------------------环境设置------------------------------------------------#
# 数据和输出目录路径
data_dir: "data/benchmarks/"
save_dir: "experiments/"

gpu_id: "0"
dataset_name: "natural_questions"  # data_dir 中的数据集名称
split: ["test"]  # 要加载的数据集分割 (例如 train,dev,test)

# 测试采样配置
test_sample_num: ~  # 测试样本数量 (仅在 dev/test 分割中有效), 如果为 None, 测试所有样本
random_sample: false  # 是否随机采样测试样本

# 可重现性种子
seed: 2024

# 是否保存中间数据
save_intermediate_data: true
save_predictions: true
save_note: "adaptive_rag_experiment"

# ------------------------------------------------检索设置------------------------------------------------#
# 检索方法配置
retrieval_method: "adaptive"  # 检索方法名称或路径
retrieval_model_path: ~  # 检索模型路径
index_path: ~  # 如果未提供则自动设置
corpus_path: ~  # 语料库路径，'.jsonl' 格式存储文档

# 检索参数
retrieval_topk: 20  # 检索的文档数量
final_context_count: 5  # 最终使用的上下文数量

# ------------------------------------------------生成设置------------------------------------------------#
# 生成器配置
generator_model: "qwen1.5-1.8b"  # 生成器模型名称
generator_model_path: ~  # 生成器模型路径
framework: "hf"  # 使用的框架 (hf/vllm)

# 生成参数
generation_params:
  max_tokens: 256
  temperature: 0.1
  top_p: 0.9
  do_sample: false

# ------------------------------------------------评估设置------------------------------------------------#
# 评估指标
metrics: ["exact_match", "f1_score", "rouge_l", "bert_score"]
compute_bert_score: true

# ------------------------------------------------AdaptiveRAG 特定设置------------------------------------------------#
# 自适应检索策略
adaptive_retrieval:
  enable_task_decomposition: true
  enable_strategy_planning: true
  enable_multi_retriever: true
  enable_reranking: true

# 任务分解配置
task_decomposition:
  max_subtasks: 5
  decomposition_threshold: 0.7

# 策略规划配置
strategy_planning:
  task_specific_weights:
    factual:
      keyword: 0.7
      dense: 0.2
      web: 0.1
    semantic:
      keyword: 0.2
      dense: 0.7
      web: 0.1
    multi_hop:
      keyword: 0.3
      dense: 0.5
      web: 0.2

# 重排序配置
reranking:
  reranker_model: "bge-reranker-base"
  reranker_model_path: ~
  rerank_topk: 10

# 调试配置
debug_mode: false
log_level: "INFO"
"""


# ===== 配置加载器 (借鉴 FlashRAG Config 类) =====

class AdaptiveRAGConfig:
    """AdaptiveRAG 配置加载器 - 借鉴 FlashRAG 的 Config 类设计"""

    def __init__(self, config_file_path=None, config_dict=None):
        """
        初始化配置

        Args:
            config_file_path: YAML 配置文件路径
            config_dict: 配置字典 (优先级高于文件)
        """
        if config_dict is None:
            config_dict = {}

        # 加载配置
        self.file_config = self._load_file_config(config_file_path)
        self.variable_config = config_dict
        self.external_config = self._merge_external_config()
        self.internal_config = self._get_internal_config()
        self.final_config = self._get_final_config()

        # 验证和设置
        self._check_final_config()
        self._set_additional_keys()
        self._init_device()
        self._set_seed()
        self._prepare_directories()

    def _load_file_config(self, config_file_path):
        """加载 YAML 配置文件"""
        if config_file_path is None:
            return {}

        if not os.path.exists(config_file_path):
            print(f"⚠️ 配置文件不存在: {config_file_path}")
            return {}

        with open(config_file_path, 'r', encoding='utf-8') as f:
            try:
                config = yaml.safe_load(f)
                return config if config is not None else {}
            except yaml.YAMLError as e:
                print(f"❌ YAML 配置文件解析错误: {e}")
                return {}

    def _merge_external_config(self):
        """合并外部配置"""
        external_config = {}
        external_config.update(self.file_config)
        external_config.update(self.variable_config)  # 变量配置优先级更高
        return external_config

    def _get_internal_config(self):
        """获取内部默认配置"""
        return {
            # 基础设置
            "device": "cuda",
            "seed": 2024,
            "batch_size": 4,

            # 路径设置
            "data_dir": "./data/benchmarks",
            "save_dir": "./experiments",
            "corpus_path": "./data/corpus/wiki_2021.jsonl",
            "index_path": "./data/indexes",

            # 数据集设置
            "dataset_name": "natural_questions",
            "split": ["test"],
            "test_sample_num": None,
            "random_sample": False,

            # 检索设置
            "retrieval_method": "adaptive",
            "retrieval_topk": 20,
            "final_context_count": 5,

            # 生成设置
            "generator_model": "qwen1.5-1.8b",
            "framework": "hf",
            "generation_params": {
                "max_tokens": 256,
                "temperature": 0.1,
                "top_p": 0.9,
                "do_sample": False
            },

            # 评估设置
            "metrics": ["exact_match", "f1_score", "rouge_l"],
            "compute_bert_score": True,

            # 保存设置
            "save_intermediate_data": True,
            "save_predictions": True,
            "save_note": "adaptive_rag_experiment",

            # AdaptiveRAG 特定设置
            "adaptive_retrieval": {
                "enable_task_decomposition": True,
                "enable_strategy_planning": True,
                "enable_multi_retriever": True,
                "enable_reranking": True
            },

            # 调试设置
            "debug_mode": False,
            "log_level": "INFO"
        }

    def _get_final_config(self):
        """获取最终配置"""
        final_config = {}
        final_config.update(self.internal_config)
        final_config.update(self.external_config)
        return final_config

    def _check_final_config(self):
        """检查和修正最终配置"""
        # 检查 split 配置
        split = self.final_config.get("split")
        if split is None:
            split = ["test"]
        if isinstance(split, str):
            split = [split]
        self.final_config["split"] = split

        # 检查路径配置
        data_dir = self.final_config.get("data_dir", "./data/benchmarks")
        save_dir = self.final_config.get("save_dir", "./experiments")

        # 设置数据集路径
        dataset_name = self.final_config.get("dataset_name", "natural_questions")
        dataset_path = os.path.join(data_dir, dataset_name)
        self.final_config["dataset_path"] = dataset_path

        # 设置保存路径
        save_note = self.final_config.get("save_note", "experiment")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(save_dir, f"{save_note}_{timestamp}")
        self.final_config["save_path"] = save_path

    def _set_additional_keys(self):
        """设置额外的键值"""
        # 设置时间戳
        self.final_config["timestamp"] = datetime.datetime.now().isoformat()

        # 设置实验 ID
        import uuid
        self.final_config["experiment_id"] = str(uuid.uuid4())[:8]

    def _init_device(self):
        """初始化设备"""
        import torch

        device = self.final_config.get("device", "cuda")
        if device == "cuda" and not torch.cuda.is_available():
            print("⚠️ CUDA 不可用，切换到 CPU")
            device = "cpu"

        self.final_config["device"] = device

        # 设置 GPU ID
        gpu_id = self.final_config.get("gpu_id", "0")
        if device == "cuda":
            os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

    def _set_seed(self):
        """设置随机种子"""
        seed = self.final_config.get("seed", 2024)

        import random
        import numpy as np
        import torch

        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

    def _prepare_directories(self):
        """准备目录"""
        # 创建保存目录
        save_path = self.final_config.get("save_path")
        if save_path:
            os.makedirs(save_path, exist_ok=True)

        # 创建数据目录
        data_dir = self.final_config.get("data_dir")
        if data_dir:
            os.makedirs(data_dir, exist_ok=True)

    def __getitem__(self, key):
        """字典式访问"""
        return self.final_config[key]

    def __setitem__(self, key, value):
        """字典式设置"""
        self.final_config[key] = value

    def get(self, key, default=None):
        """获取配置值"""
        return self.final_config.get(key, default)

    def update(self, config_dict):
        """更新配置"""
        self.final_config.update(config_dict)

    def save_config(self, save_path=None):
        """保存配置到文件"""
        if save_path is None:
            save_path = os.path.join(self.final_config["save_path"], "config.yaml")

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.final_config, f, default_flow_style=False, allow_unicode=True)

        print(f"✅ 配置已保存到: {save_path}")


# ===== 便捷函数 =====

def create_experiment_config(config_file=None, **kwargs):
    """创建实验配置"""
    return AdaptiveRAGConfig(config_file_path=config_file, config_dict=kwargs)


def save_example_config(save_path="./adaptive_rag_config.yaml"):
    """保存示例配置文件"""
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(EXAMPLE_CONFIG_YAML)
    print(f"✅ 示例配置文件已保存到: {save_path}")


if __name__ == "__main__":
    # 测试配置系统
    print("🧪 测试 AdaptiveRAG 配置系统")

    # 创建配置
    config = create_experiment_config(
        dataset_name="natural_questions",
        test_sample_num=10,
        debug_mode=True
    )

    print(f"数据集: {config['dataset_name']}")
    print(f"设备: {config['device']}")
    print(f"保存路径: {config['save_path']}")

    # 保存示例配置
    save_example_config()


def create_flexrag_integrated_config() -> FlexRAGIntegratedConfig:
    """创建 FlexRAG 深度集成配置"""
    config = FlexRAGIntegratedConfig()

    # 解析检索器配置中的路径
    for retriever_name, retriever_config in config.retriever_configs.items():
        if "flex_config" in retriever_config:
            flex_config = retriever_config["flex_config"]
            if "retriever_path" in flex_config:
                flex_config["retriever_path"] = resolve_path(flex_config["retriever_path"])

    # 解析生成器配置中的路径
    for generator_name, generator_config in config.generator_configs.items():
        if "hf_config" in generator_config:
            hf_config = generator_config["hf_config"]
            if "model_path" in hf_config:
                hf_config["model_path"] = resolve_path(hf_config["model_path"])

    return config


def get_config_for_mode(mode: str = "adaptive"):
    """根据模式获取配置

    Args:
        mode: 配置模式
            - "adaptive": 原始自适应配置
            - "flexrag": FlexRAG 深度集成配置
            - "hybrid": 混合配置
    """
    if mode == "flexrag":
        return create_flexrag_integrated_config()
    elif mode == "hybrid":
        # 混合配置：结合两种配置的优点
        base_config = create_default_config()
        flexrag_config = create_flexrag_integrated_config()

        # 这里可以实现配置合并逻辑
        return flexrag_config  # 暂时返回 FlexRAG 配置
    else:
        return create_default_config()


if __name__ == "__main__":
    # 测试配置系统
    print("🧪 测试配置系统")

    # 测试原始配置
    config = create_default_config()
    print("✅ 默认配置创建成功")

    # 测试 FlexRAG 集成配置
    if FLEXRAG_AVAILABLE:
        flexrag_config = create_flexrag_integrated_config()
        print("✅ FlexRAG 集成配置创建成功")
    else:
        print("⚠️ FlexRAG 未安装，跳过集成配置测试")

    # 测试配置模式选择
    for mode in ["adaptive", "flexrag", "hybrid"]:
        test_config = get_config_for_mode(mode)
        print(f"✅ {mode} 模式配置创建成功")

    # 保存示例配置
    with open("adaptive_rag_config.yaml", "w") as f:
        f.write(EXAMPLE_CONFIG_YAML)
    print("✅ 示例配置文件已保存")


# ===== 模块化配置加载函数 =====

def load_modular_config_from_yaml(yaml_path: str) -> FlexRAGIntegratedConfig:
    """从模块化YAML配置文件加载配置"""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        yaml_config = yaml.safe_load(f)

    config = FlexRAGIntegratedConfig()

    # 加载模块开关配置
    if 'modules' in yaml_config:
        modules_config = yaml_config['modules']
        config.modules = ModuleToggleConfig(**modules_config)

    # 加载基础配置
    if 'basic' in yaml_config:
        basic_config = yaml_config['basic']
        config.device = basic_config.get('device', config.device)
        config.batch_size = basic_config.get('batch_size', config.batch_size)
        config.max_input_length = basic_config.get('max_input_length', config.max_input_length)

    return config


def apply_preset_config(config: FlexRAGIntegratedConfig, preset_name: str, yaml_config: dict) -> FlexRAGIntegratedConfig:
    """应用预设配置模式"""
    if 'presets' in yaml_config and preset_name in yaml_config['presets']:
        preset = yaml_config['presets'][preset_name]

        if 'modules' in preset:
            # 更新模块开关配置
            for module_name, enabled in preset['modules'].items():
                if hasattr(config.modules, module_name):
                    setattr(config.modules, module_name, enabled)

    return config


def create_config_from_yaml(yaml_path: str, preset: str = None) -> FlexRAGIntegratedConfig:
    """从 YAML 文件创建配置，支持预设模式"""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        yaml_config = yaml.safe_load(f)

    # 如果是模块化配置文件
    if 'modules' in yaml_config:
        config = load_modular_config_from_yaml(yaml_path)

        # 应用预设配置
        if preset:
            config = apply_preset_config(config, preset, yaml_config)

        return config

    # 兼容旧版配置文件
    config = FlexRAGIntegratedConfig()
    return config


def get_enabled_modules(config: FlexRAGIntegratedConfig) -> Dict[str, bool]:
    """获取启用的模块列表"""
    if hasattr(config, 'modules'):
        return {
            name: getattr(config.modules, name)
            for name in dir(config.modules)
            if not name.startswith('_')
        }
    return {}


def print_module_status(config: FlexRAGIntegratedConfig):
    """打印模块启用状态"""
    enabled_modules = get_enabled_modules(config)

    print("🔧 AdaptiveRAG 模块状态:")
    print("=" * 50)

    categories = {
        "核心处理模块": ["task_decomposer", "retrieval_planner", "multi_retriever", "context_reranker", "adaptive_generator"],
        "智能分析模块": ["query_analyzer", "strategy_router", "performance_optimizer", "intelligent_strategy_learner"],
        "检索器模块": ["keyword_retriever", "dense_retriever", "web_retriever", "hybrid_retriever"],
        "重排序模块": ["cross_encoder_ranker", "colbert_ranker", "gpt_ranker"],
        "生成器模块": ["template_generator", "freeform_generator", "dialogue_generator"],
        "评估模块": ["fact_verification", "confidence_estimation", "result_analyzer"],
        "缓存模块": ["semantic_cache", "predictive_cache"],
        "用户体验模块": ["personalization", "multimodal_support"],
        "调试监控模块": ["debug_mode", "performance_monitoring", "logging_enhanced"]
    }

    for category, modules in categories.items():
        print(f"\n📂 {category}:")
        for module in modules:
            if module in enabled_modules:
                status = "✅ 启用" if enabled_modules[module] else "❌ 禁用"
                print(f"  {module}: {status}")
