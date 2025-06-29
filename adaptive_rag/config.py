#!/usr/bin/env python3
"""
=== 智能自适应 RAG 配置模块 ===

基于 FlashRAG 的配置系统，扩展支持自适应检索配置
"""

import os
import yaml
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


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


@dataclass
class AdaptiveRAGConfig:
    """智能自适应 RAG 总配置"""
    
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


# 示例配置文件内容
EXAMPLE_CONFIG_YAML = """
# 智能自适应 RAG 配置示例

# 基础配置
device: "cuda"
batch_size: 4
max_input_length: 2048

# 模型路径
model_paths:
  dense_retriever: "/root/autodl-tmp/models/e5-base-v2"
  generator: "/root/autodl-tmp/models/qwen1.5-1.8b"
  reranker: "/root/autodl-tmp/models/bge-reranker-v2-m3"

# 检索策略配置
retrieval_plan_config:
  task_specific_weights:
    factual:
      keyword: 0.7
      dense: 0.2
      web: 0.1
    semantic:
      keyword: 0.2
      dense: 0.7
      web: 0.1

# 相关度评分配置
relevance_score_config:
  score_weights:
    semantic: 0.3
    factual: 0.3
    temporal: 0.1
    entity: 0.2
    diversity: 0.1

# 调试配置
debug_mode: true
save_intermediate_results: true
log_level: "DEBUG"
"""


if __name__ == "__main__":
    # 测试配置系统
    config = create_default_config()
    print("默认配置创建成功")
    
    # 保存示例配置
    with open("adaptive_rag_config.yaml", "w") as f:
        f.write(EXAMPLE_CONFIG_YAML)
    print("示例配置文件已保存")
