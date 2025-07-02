#!/usr/bin/env python3
"""
=== 模块管理器 ===

根据配置动态启用和禁用各个模块
"""

import logging
from typing import Dict, Any, Optional, List, Type
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ModuleInfo:
    """模块信息"""
    name: str
    enabled: bool
    instance: Optional[Any] = None
    dependencies: List[str] = None
    description: str = ""


class ModuleManager:
    """
    模块管理器
    
    负责根据配置动态管理各个模块的生命周期
    """
    
    def __init__(self, config):
        self.config = config
        self.modules: Dict[str, ModuleInfo] = {}
        self.module_registry: Dict[str, Type] = {}
        self.initialized = False
        
        # 注册所有可用模块
        self._register_modules()
    
    def _register_modules(self):
        """注册所有可用模块"""
        
        # 核心处理模块
        self.module_registry.update({
            "task_decomposer": self._get_task_decomposer_class(),
            "retrieval_planner": self._get_retrieval_planner_class(),
            "multi_retriever": self._get_multi_retriever_class(),
            "context_reranker": self._get_context_reranker_class(),
            "adaptive_generator": self._get_adaptive_generator_class(),
        })
        
        # 智能分析模块
        self.module_registry.update({
            "query_analyzer": self._get_query_analyzer_class(),
            "strategy_router": self._get_strategy_router_class(),
            "performance_optimizer": self._get_performance_optimizer_class(),
            "intelligent_strategy_learner": self._get_intelligent_strategy_learner_class(),
            "multi_dimensional_optimizer": self._get_multi_dimensional_optimizer_class(),
            "resource_aware_optimizer": self._get_resource_aware_optimizer_class(),
        })
        
        # 检索器模块
        self.module_registry.update({
            "keyword_retriever": self._get_keyword_retriever_class(),
            "dense_retriever": self._get_dense_retriever_class(),
            "web_retriever": self._get_web_retriever_class(),
            "hybrid_retriever": self._get_hybrid_retriever_class(),
        })
        
        # 重排序模块
        self.module_registry.update({
            "cross_encoder_ranker": self._get_cross_encoder_ranker_class(),
            "colbert_ranker": self._get_colbert_ranker_class(),
            "gpt_ranker": self._get_gpt_ranker_class(),
        })
        
        # 生成器模块
        self.module_registry.update({
            "template_generator": self._get_template_generator_class(),
            "freeform_generator": self._get_freeform_generator_class(),
            "dialogue_generator": self._get_dialogue_generator_class(),
        })
        
        # 评估模块
        self.module_registry.update({
            "fact_verification": self._get_fact_verification_class(),
            "confidence_estimation": self._get_confidence_estimation_class(),
            "result_analyzer": self._get_result_analyzer_class(),
        })
        
        # 缓存模块
        self.module_registry.update({
            "semantic_cache": self._get_semantic_cache_class(),
            "predictive_cache": self._get_predictive_cache_class(),
        })
    
    def initialize_modules(self):
        """根据配置初始化模块"""
        if self.initialized:
            logger.warning("模块已经初始化，跳过重复初始化")
            return
        
        logger.info("🚀 开始初始化 AdaptiveRAG 模块...")
        
        # 获取模块配置
        modules_config = getattr(self.config, 'modules', None)
        if not modules_config:
            logger.warning("未找到模块配置，使用默认配置")
            return
        
        # 初始化每个模块
        for module_name, module_class in self.module_registry.items():
            enabled = getattr(modules_config, module_name, False)
            
            module_info = ModuleInfo(
                name=module_name,
                enabled=enabled,
                description=self._get_module_description(module_name)
            )
            
            if enabled and module_class:
                try:
                    # 初始化模块实例
                    module_info.instance = module_class(self.config)
                    logger.info(f"✅ {module_name} 模块已启用")
                except Exception as e:
                    logger.error(f"❌ {module_name} 模块初始化失败: {e}")
                    module_info.enabled = False
            else:
                logger.info(f"⏸️ {module_name} 模块已禁用")
            
            self.modules[module_name] = module_info
        
        # 检查模块依赖
        self._check_dependencies()
        
        self.initialized = True
        logger.info("🎉 模块初始化完成")
    
    def get_module(self, module_name: str) -> Optional[Any]:
        """获取模块实例"""
        if module_name in self.modules:
            module_info = self.modules[module_name]
            if module_info.enabled and module_info.instance:
                return module_info.instance
        return None
    
    def is_module_enabled(self, module_name: str) -> bool:
        """检查模块是否启用"""
        if module_name in self.modules:
            return self.modules[module_name].enabled
        return False
    
    def get_enabled_modules(self) -> List[str]:
        """获取所有启用的模块名称"""
        return [
            name for name, info in self.modules.items()
            if info.enabled and info.instance
        ]
    
    def get_module_status(self) -> Dict[str, Dict[str, Any]]:
        """获取所有模块的状态"""
        status = {}
        for name, info in self.modules.items():
            status[name] = {
                "enabled": info.enabled,
                "initialized": info.instance is not None,
                "description": info.description
            }
        return status
    
    def _check_dependencies(self):
        """检查模块依赖关系"""
        # 检查多重检索系统的依赖
        if self.is_module_enabled("multi_retriever"):
            retrievers = ["keyword_retriever", "dense_retriever", "web_retriever", "hybrid_retriever"]
            enabled_retrievers = [r for r in retrievers if self.is_module_enabled(r)]
            
            if not enabled_retrievers:
                logger.warning("⚠️ 多重检索系统已启用但没有启用任何检索器")
        
        # 检查上下文重排器的依赖
        if self.is_module_enabled("context_reranker"):
            rankers = ["cross_encoder_ranker", "colbert_ranker", "gpt_ranker"]
            enabled_rankers = [r for r in rankers if self.is_module_enabled(r)]
            
            if not enabled_rankers:
                logger.warning("⚠️ 上下文重排器已启用但没有启用任何重排序器")
    
    def _get_module_description(self, module_name: str) -> str:
        """获取模块描述"""
        descriptions = {
            "task_decomposer": "将复杂查询分解为子任务",
            "retrieval_planner": "制定检索策略和权重分配",
            "multi_retriever": "并行执行多种检索方法",
            "context_reranker": "优化检索结果排序",
            "adaptive_generator": "生成最终响应",
            "query_analyzer": "分析查询复杂度和类型",
            "strategy_router": "动态选择最优检索策略",
            "performance_optimizer": "持续优化系统性能",
            "intelligent_strategy_learner": "从历史数据学习最优策略",
            "multi_dimensional_optimizer": "多维度决策优化",
            "resource_aware_optimizer": "资源感知优化",
            "keyword_retriever": "基于关键词的检索",
            "dense_retriever": "基于密集向量的检索",
            "web_retriever": "实时网络搜索",
            "hybrid_retriever": "混合检索方法",
            "cross_encoder_ranker": "交叉编码器重排序",
            "colbert_ranker": "ColBERT重排序",
            "gpt_ranker": "GPT重排序",
            "template_generator": "基于模板的生成",
            "freeform_generator": "自由形式生成",
            "dialogue_generator": "对话生成",
            "fact_verification": "事实验证",
            "confidence_estimation": "置信度估计",
            "result_analyzer": "结果分析",
            "semantic_cache": "语义缓存",
            "predictive_cache": "预测性缓存"
        }
        return descriptions.get(module_name, "未知模块")
    
    # 模块类获取方法（这些方法返回实际的模块类）
    def _get_task_decomposer_class(self):
        try:
            from ..task_decomposer import TaskDecomposer
            return TaskDecomposer
        except ImportError:
            return None
    
    def _get_retrieval_planner_class(self):
        try:
            from ..retrieval_planner import RetrievalPlanner
            return RetrievalPlanner
        except ImportError:
            return None
    
    def _get_multi_retriever_class(self):
        try:
            from ..multi_retriever import MultiRetriever
            return MultiRetriever
        except ImportError:
            return None
    
    def _get_context_reranker_class(self):
        try:
            from ..modules.refiner.flexrag_integrated_ranker import FlexRAGIntegratedRanker
            return FlexRAGIntegratedRanker
        except ImportError:
            return None
    
    def _get_adaptive_generator_class(self):
        try:
            from ..modules.generator.flexrag_integrated_generator import FlexRAGIntegratedGenerator
            return FlexRAGIntegratedGenerator
        except ImportError:
            return None
    
    def _get_query_analyzer_class(self):
        try:
            from .query_analyzer import QueryAnalyzer
            return QueryAnalyzer
        except ImportError:
            return None
    
    def _get_strategy_router_class(self):
        try:
            from .strategy_router import StrategyRouter
            return StrategyRouter
        except ImportError:
            return None
    
    def _get_performance_optimizer_class(self):
        try:
            from .performance_optimizer import PerformanceOptimizer
            return PerformanceOptimizer
        except ImportError:
            return None
    
    def _get_intelligent_strategy_learner_class(self):
        try:
            from .intelligent_strategy_learner import IntelligentStrategyLearner
            return IntelligentStrategyLearner
        except ImportError:
            return None
    
    def _get_multi_dimensional_optimizer_class(self):
        try:
            from .multi_dimensional_optimizer import MultiDimensionalOptimizer
            return MultiDimensionalOptimizer
        except ImportError:
            return None
    
    def _get_resource_aware_optimizer_class(self):
        try:
            from .resource_aware_optimizer import ResourceAwareOptimizer
            return ResourceAwareOptimizer
        except ImportError:
            return None
    
    # 其他模块类获取方法（简化版，返回None表示使用模拟实现）
    def _get_keyword_retriever_class(self): return None
    def _get_dense_retriever_class(self): return None
    def _get_web_retriever_class(self): return None
    def _get_hybrid_retriever_class(self): return None
    def _get_cross_encoder_ranker_class(self): return None
    def _get_colbert_ranker_class(self): return None
    def _get_gpt_ranker_class(self): return None
    def _get_template_generator_class(self): return None
    def _get_freeform_generator_class(self): return None
    def _get_dialogue_generator_class(self): return None
    def _get_fact_verification_class(self): return None
    def _get_confidence_estimation_class(self): return None
    def _get_result_analyzer_class(self): return None
    def _get_semantic_cache_class(self): return None
    def _get_predictive_cache_class(self): return None
