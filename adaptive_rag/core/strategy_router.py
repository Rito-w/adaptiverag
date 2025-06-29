#!/usr/bin/env python3
"""
=== 策略路由器 - 动态检索策略选择 ===

核心功能：
1. 根据查询分析结果动态选择检索策略
2. 智能调整关键词搜索和向量搜索的权重
3. 优化检索参数
"""

import logging
from typing import Dict, Any, List
from dataclasses import dataclass

from .query_analyzer import AnalysisResult, QueryType, QueryComplexity

logger = logging.getLogger(__name__)


@dataclass
class RetrievalStrategy:
    """检索策略数据结构"""
    keyword_weight: float       # 关键词搜索权重
    vector_weight: float        # 向量搜索权重
    max_docs: int              # 最大检索文档数
    rerank_enabled: bool       # 是否启用重排序
    diversity_factor: float    # 多样性因子
    strategy_name: str         # 策略名称
    confidence: float          # 策略置信度


class StrategyRouter:
    """
    策略路由器 - 动态选择最优检索策略
    
    根据查询分析结果，智能选择：
    1. 检索方法权重分配
    2. 检索参数优化
    3. 后处理策略
    """
    
    def __init__(self, cfg):
        self.cfg = cfg
        
        # 预定义策略模板
        self._init_strategy_templates()
        
        logger.info("StrategyRouter 初始化完成")
    
    def _init_strategy_templates(self):
        """初始化策略模板"""
        self.strategy_templates = {
            # 事实性问题策略
            QueryType.FACTUAL: {
                "simple": RetrievalStrategy(
                    keyword_weight=0.4,
                    vector_weight=0.6,
                    max_docs=10,
                    rerank_enabled=False,
                    diversity_factor=0.3,
                    strategy_name="factual_simple",
                    confidence=0.9
                ),
                "complex": RetrievalStrategy(
                    keyword_weight=0.3,
                    vector_weight=0.7,
                    max_docs=15,
                    rerank_enabled=True,
                    diversity_factor=0.4,
                    strategy_name="factual_complex",
                    confidence=0.8
                )
            },
            
            # 比较性问题策略
            QueryType.COMPARATIVE: {
                "simple": RetrievalStrategy(
                    keyword_weight=0.5,
                    vector_weight=0.5,
                    max_docs=12,
                    rerank_enabled=True,
                    diversity_factor=0.6,
                    strategy_name="comparative_simple",
                    confidence=0.85
                ),
                "complex": RetrievalStrategy(
                    keyword_weight=0.4,
                    vector_weight=0.6,
                    max_docs=20,
                    rerank_enabled=True,
                    diversity_factor=0.7,
                    strategy_name="comparative_complex",
                    confidence=0.8
                )
            },
            
            # 时间相关问题策略
            QueryType.TEMPORAL: {
                "simple": RetrievalStrategy(
                    keyword_weight=0.6,
                    vector_weight=0.4,
                    max_docs=10,
                    rerank_enabled=True,
                    diversity_factor=0.3,
                    strategy_name="temporal_simple",
                    confidence=0.9
                ),
                "complex": RetrievalStrategy(
                    keyword_weight=0.5,
                    vector_weight=0.5,
                    max_docs=15,
                    rerank_enabled=True,
                    diversity_factor=0.5,
                    strategy_name="temporal_complex",
                    confidence=0.85
                )
            },
            
            # 因果关系问题策略
            QueryType.CAUSAL: {
                "simple": RetrievalStrategy(
                    keyword_weight=0.3,
                    vector_weight=0.7,
                    max_docs=12,
                    rerank_enabled=True,
                    diversity_factor=0.4,
                    strategy_name="causal_simple",
                    confidence=0.8
                ),
                "complex": RetrievalStrategy(
                    keyword_weight=0.2,
                    vector_weight=0.8,
                    max_docs=18,
                    rerank_enabled=True,
                    diversity_factor=0.6,
                    strategy_name="causal_complex",
                    confidence=0.75
                )
            },
            
            # 摘要任务策略
            QueryType.SUMMARY: {
                "simple": RetrievalStrategy(
                    keyword_weight=0.4,
                    vector_weight=0.6,
                    max_docs=15,
                    rerank_enabled=True,
                    diversity_factor=0.8,
                    strategy_name="summary_simple",
                    confidence=0.85
                ),
                "complex": RetrievalStrategy(
                    keyword_weight=0.3,
                    vector_weight=0.7,
                    max_docs=25,
                    rerank_enabled=True,
                    diversity_factor=0.9,
                    strategy_name="summary_complex",
                    confidence=0.8
                )
            },
            
            # 复杂多跳问题策略
            QueryType.COMPLEX: {
                "simple": RetrievalStrategy(
                    keyword_weight=0.3,
                    vector_weight=0.7,
                    max_docs=18,
                    rerank_enabled=True,
                    diversity_factor=0.5,
                    strategy_name="complex_simple",
                    confidence=0.75
                ),
                "complex": RetrievalStrategy(
                    keyword_weight=0.2,
                    vector_weight=0.8,
                    max_docs=30,
                    rerank_enabled=True,
                    diversity_factor=0.7,
                    strategy_name="complex_complex",
                    confidence=0.7
                )
            }
        }
    
    def route_strategy(self, analysis_result: AnalysisResult) -> Dict[str, Any]:
        """
        主要的策略路由方法
        
        Args:
            analysis_result: 查询分析结果
            
        Returns:
            Dict: 包含策略信息的字典
        """
        logger.info(f"开始策略路由: {analysis_result.query_type}, {analysis_result.complexity}")
        
        # 1. 获取基础策略
        base_strategy = self._get_base_strategy(analysis_result)
        
        # 2. 计算动态权重
        dynamic_weights = self._calculate_dynamic_weights(analysis_result)

        # 3. 动态调整策略
        adjusted_strategy = self._adjust_strategy_with_weights(base_strategy, analysis_result, dynamic_weights)
        
        # 4. 构建完整策略信息
        strategy_info = {
            "strategy": adjusted_strategy,
            "query_type": analysis_result.query_type.value,
            "complexity": analysis_result.complexity.value,
            "sub_queries": [sq.content for sq in analysis_result.sub_queries],
            "routing_confidence": adjusted_strategy.confidence,
            "dynamic_weights": dynamic_weights,
            "weight_explanation": self._explain_weight_calculation(analysis_result, dynamic_weights),
            "metadata": {
                "original_strategy": base_strategy.strategy_name,
                "adjusted_strategy": adjusted_strategy.strategy_name,
                "keywords": analysis_result.keywords,
                "entities": analysis_result.entities
            }
        }
        
        logger.info(f"策略路由完成: {adjusted_strategy.strategy_name}")
        return strategy_info

    def _calculate_dynamic_weights(self, analysis_result: AnalysisResult) -> Dict[str, float]:
        """动态计算检索权重"""
        query_type = analysis_result.query_type
        complexity = analysis_result.complexity
        sub_queries = analysis_result.sub_queries
        keywords = analysis_result.keywords
        entities = analysis_result.entities

        # 基础权重
        base_weights = {
            "keyword": 0.33,
            "vector": 0.33,
            "hybrid": 0.34
        }

        # 根据查询类型调整
        if query_type == QueryType.FACTUAL:
            # 事实性查询偏向关键词搜索
            base_weights["keyword"] += 0.2
            base_weights["vector"] -= 0.1
            base_weights["hybrid"] -= 0.1
        elif query_type == QueryType.COMPARATIVE:
            # 比较性查询需要语义理解
            base_weights["vector"] += 0.2
            base_weights["keyword"] -= 0.1
            base_weights["hybrid"] -= 0.1
        elif query_type == QueryType.TEMPORAL:
            # 时间相关查询偏向混合搜索
            base_weights["hybrid"] += 0.2
            base_weights["keyword"] -= 0.1
            base_weights["vector"] -= 0.1

        # 根据复杂度调整
        if complexity == QueryComplexity.COMPLEX:
            # 复杂查询增加混合搜索权重
            base_weights["hybrid"] += 0.15
            base_weights["keyword"] -= 0.075
            base_weights["vector"] -= 0.075
        elif complexity == QueryComplexity.SIMPLE:
            # 简单查询偏向关键词搜索
            base_weights["keyword"] += 0.1
            base_weights["hybrid"] -= 0.05
            base_weights["vector"] -= 0.05

        # 根据子查询数量调整
        if len(sub_queries) > 2:
            # 多子查询增加混合搜索权重
            base_weights["hybrid"] += 0.1
            base_weights["keyword"] -= 0.05
            base_weights["vector"] -= 0.05

        # 根据实体数量调整
        if len(entities) > 3:
            # 多实体查询偏向关键词搜索
            base_weights["keyword"] += 0.1
            base_weights["vector"] -= 0.05
            base_weights["hybrid"] -= 0.05

        # 确保权重和为1
        total = sum(base_weights.values())
        for key in base_weights:
            base_weights[key] /= total

        return base_weights

    def _adjust_strategy_with_weights(self, base_strategy: RetrievalStrategy,
                                    analysis_result: AnalysisResult,
                                    dynamic_weights: Dict[str, float]) -> RetrievalStrategy:
        """使用动态权重调整策略"""
        # 创建新的策略对象
        adjusted_strategy = RetrievalStrategy(
            keyword_weight=dynamic_weights["keyword"],
            vector_weight=dynamic_weights["vector"],
            max_docs=base_strategy.max_docs,
            rerank_enabled=base_strategy.rerank_enabled,
            diversity_factor=base_strategy.diversity_factor,
            strategy_name=f"{base_strategy.strategy_name}_dynamic",
            confidence=base_strategy.confidence
        )

        # 根据分析结果进一步调整
        if analysis_result.complexity == QueryComplexity.COMPLEX:
            adjusted_strategy.max_docs = min(adjusted_strategy.max_docs + 5, 25)
            adjusted_strategy.diversity_factor = min(adjusted_strategy.diversity_factor + 0.1, 1.0)

        return adjusted_strategy

    def _explain_weight_calculation(self, analysis_result: AnalysisResult,
                                  dynamic_weights: Dict[str, float]) -> str:
        """解释权重计算过程"""
        explanation = f"动态权重分配 (关键词: {dynamic_weights['keyword']:.2f}, "
        explanation += f"向量: {dynamic_weights['vector']:.2f}, "
        explanation += f"混合: {dynamic_weights['hybrid']:.2f})\n"

        explanation += f"基于: 查询类型={analysis_result.query_type.value}, "
        explanation += f"复杂度={analysis_result.complexity.value}, "
        explanation += f"子查询数={len(analysis_result.sub_queries)}, "
        explanation += f"实体数={len(analysis_result.entities)}"

        return explanation
    
    def _get_base_strategy(self, analysis_result: AnalysisResult) -> RetrievalStrategy:
        """获取基础策略"""
        query_type = analysis_result.query_type
        complexity = analysis_result.complexity
        
        # 确定复杂度级别
        complexity_level = "complex" if complexity == QueryComplexity.COMPLEX else "simple"
        
        # 获取策略模板
        if query_type in self.strategy_templates:
            strategy_dict = self.strategy_templates[query_type]
            if complexity_level in strategy_dict:
                return strategy_dict[complexity_level]
        
        # 回退到默认策略
        return self._get_default_strategy()
    
    def _adjust_strategy(self, base_strategy: RetrievalStrategy, analysis_result: AnalysisResult) -> RetrievalStrategy:
        """动态调整策略"""
        # 复制基础策略
        adjusted = RetrievalStrategy(
            keyword_weight=base_strategy.keyword_weight,
            vector_weight=base_strategy.vector_weight,
            max_docs=base_strategy.max_docs,
            rerank_enabled=base_strategy.rerank_enabled,
            diversity_factor=base_strategy.diversity_factor,
            strategy_name=base_strategy.strategy_name + "_adjusted",
            confidence=base_strategy.confidence
        )
        
        # 根据子查询数量调整
        if analysis_result.sub_queries:
            sub_query_count = len(analysis_result.sub_queries)
            
            # 增加检索文档数
            adjusted.max_docs = min(adjusted.max_docs + sub_query_count * 3, 50)
            
            # 提高多样性因子
            adjusted.diversity_factor = min(adjusted.diversity_factor + 0.1, 1.0)
            
            # 启用重排序
            adjusted.rerank_enabled = True
        
        # 根据关键词数量调整权重
        keyword_count = len(analysis_result.keywords)
        if keyword_count > 5:
            # 关键词较多，提高关键词搜索权重
            adjusted.keyword_weight = min(adjusted.keyword_weight + 0.1, 0.8)
            adjusted.vector_weight = 1.0 - adjusted.keyword_weight
        elif keyword_count < 3:
            # 关键词较少，提高向量搜索权重
            adjusted.vector_weight = min(adjusted.vector_weight + 0.1, 0.9)
            adjusted.keyword_weight = 1.0 - adjusted.vector_weight
        
        # 根据实体数量调整
        entity_count = len(analysis_result.entities)
        if entity_count > 3:
            # 实体较多，增加检索文档数和多样性
            adjusted.max_docs = min(adjusted.max_docs + 5, 50)
            adjusted.diversity_factor = min(adjusted.diversity_factor + 0.15, 1.0)
        
        # 根据分析置信度调整策略置信度
        adjusted.confidence = (adjusted.confidence + analysis_result.confidence) / 2
        
        return adjusted
    
    def _get_default_strategy(self) -> RetrievalStrategy:
        """获取默认策略"""
        return RetrievalStrategy(
            keyword_weight=self.cfg.default_keyword_weight,
            vector_weight=self.cfg.default_vector_weight,
            max_docs=self.cfg.max_retrieved_docs,
            rerank_enabled=True,
            diversity_factor=0.5,
            strategy_name="default",
            confidence=0.6
        )
    
    def get_strategy_explanation(self, strategy_info: Dict[str, Any]) -> str:
        """获取策略解释（用于调试和展示）"""
        strategy = strategy_info["strategy"]
        
        explanation = f"""
策略选择解释：
- 策略名称: {strategy.strategy_name}
- 查询类型: {strategy_info["query_type"]}
- 复杂度: {strategy_info["complexity"]}
- 关键词搜索权重: {strategy.keyword_weight:.2f}
- 向量搜索权重: {strategy.vector_weight:.2f}
- 最大检索文档数: {strategy.max_docs}
- 重排序: {"启用" if strategy.rerank_enabled else "禁用"}
- 多样性因子: {strategy.diversity_factor:.2f}
- 策略置信度: {strategy.confidence:.2f}
"""
        
        if strategy_info.get("sub_queries"):
            explanation += f"- 子查询数量: {len(strategy_info['sub_queries'])}\n"
        
        return explanation.strip()
