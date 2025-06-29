#!/usr/bin/env python3
"""
=== Adaptive RAG - 基于 FlexRAG 的自适应检索增强生成 ===

核心组件：
- AdaptiveAssistant: 主要的自适应助手
- QueryAnalyzer: LLM 驱动的查询分析器
- StrategyRouter: 动态策略路由器
- HybridRetriever: 智能混合检索器
"""

# 暂时注释掉有问题的导入，使用简化版本
# from .core.adaptive_assistant import AdaptiveAssistant, AdaptiveConfig, create_adaptive_assistant
# from .core.query_analyzer import QueryAnalyzer, QueryType, QueryComplexity, AnalysisResult
# from .core.strategy_router import StrategyRouter, RetrievalStrategy
# from .core.hybrid_retriever import HybridRetriever

__version__ = "0.1.0"
__author__ = "Adaptive RAG Team"

__all__ = [
    # 暂时为空，等修复导入问题后再添加
]