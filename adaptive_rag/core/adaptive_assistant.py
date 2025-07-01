#!/usr/bin/env python3
"""
=== Adaptive Assistant - 基于 FlexRAG 的自适应助手 ===

真正借鉴 LevelRAG 的创新：
1. 继承 FlexRAG 的 BasicAssistant
2. 集成 LLM 驱动的查询分析
3. 实现动态策略路由
4. 支持智能混合检索
"""

import logging
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

# 导入标准库
from dataclasses import dataclass as dc_dataclass

# 定义数据结构（替代 FlexRAG 的数据结构）
@dc_dataclass
class RetrievedContext:
    """检索到的上下文"""
    content: str
    score: float
    metadata: Dict[str, Any] = None

@dc_dataclass
class QueryResult:
    """查询结果"""
    query: str
    answer: str
    retrieved_contexts: List[RetrievedContext]
    metadata: Dict[str, Any] = None

from .query_analyzer import QueryAnalyzer
from .strategy_router import StrategyRouter
from .hybrid_retriever import HybridRetriever
from .intelligent_strategy_learner import IntelligentStrategyLearner, PerformanceMetrics
from .performance_optimizer import PerformanceOptimizer
from .multi_dimensional_optimizer import MultiDimensionalOptimizer, OptimizationObjective, ResourceConstraints

logger = logging.getLogger(__name__)


@dataclass
class AdaptiveConfig:
    """自适应助手配置"""
    # 基础配置
    model_name: str = "openai/gpt-4"
    max_tokens: int = 2048
    temperature: float = 0.1
    
    # 查询分析配置
    enable_query_decomposition: bool = True
    max_decomposition_depth: int = 3
    decomposition_threshold: int = 50  # token 数量阈值
    
    # 策略路由配置
    enable_dynamic_routing: bool = True
    default_keyword_weight: float = 0.3
    default_vector_weight: float = 0.7
    
    # 混合检索配置
    enable_hybrid_retrieval: bool = True
    max_retrieved_docs: int = 20
    final_docs_count: int = 5
    
    # 聚合配置
    relevance_weight: float = 0.7
    diversity_weight: float = 0.3
    redundancy_threshold: float = 0.85


@ASSISTANTS("adaptive", config_class=AdaptiveConfig)
class AdaptiveAssistant(BasicAssistant):
    """
    自适应 RAG 助手 - 基于 FlexRAG 框架
    
    核心创新：
    1. LLM 驱动的查询分析和分解
    2. 动态策略路由
    3. 智能混合检索
    4. 多维度聚合
    """
    
    def __init__(self, cfg: AdaptiveConfig):
        """初始化自适应助手"""
        super().__init__(cfg)
        self.cfg = cfg

        # 初始化核心组件
        self.query_analyzer = QueryAnalyzer(cfg)
        self.strategy_router = StrategyRouter(cfg)
        self.hybrid_retriever = HybridRetriever(cfg)

        # 初始化新的智能组件
        self.intelligent_learner = IntelligentStrategyLearner(cfg)
        self.performance_optimizer = PerformanceOptimizer(cfg.__dict__)
        self.multi_dim_optimizer = MultiDimensionalOptimizer(cfg.__dict__)

        # 性能统计
        self.query_count = 0
        self.total_processing_time = 0.0

        logger.info("AdaptiveAssistant 初始化完成 (包含智能学习组件)")
    
    def answer(self, query: str, optimization_objective: OptimizationObjective = OptimizationObjective.BALANCED, **kwargs) -> QueryResult:
        """
        主要的问答方法 - 实现智能自适应 RAG 流程

        增强流程：
        1. 智能查询分析和复杂度评估
        2. 多维度策略优化
        3. 性能优化的混合检索
        4. 智能聚合和生成
        5. 性能反馈学习
        """
        start_time = time.time()
        logger.info(f"开始处理查询: {query}")

        try:
            # 第一步：智能查询分析
            analysis_result = self.query_analyzer.analyze_query(query)

            # 第二步：智能策略学习和预测
            strategy_prediction = self.intelligent_learner.predict_optimal_strategy(query)
            query_features = strategy_prediction['query_features']

            # 第三步：多维度策略优化
            available_strategies = [
                strategy_prediction['strategy_config'],
                {'keyword': 0.6, 'dense': 0.3, 'web': 0.1},  # 保守策略
                {'keyword': 0.2, 'dense': 0.7, 'web': 0.1},  # 激进策略
            ]

            optimal_strategy = self.multi_dim_optimizer.optimize_strategy(
                query_features=query_features.__dict__,
                available_strategies=available_strategies,
                objective=optimization_objective,
                constraints=kwargs.get('constraints')
            )

            logger.info(f"选择策略: {optimal_strategy.config}, 置信度: {strategy_prediction['confidence']:.3f}")

            # 第四步：性能优化的检索
            def retrieval_func():
                return self.hybrid_retriever.retrieve(
                    query=query,
                    analysis_result=analysis_result,
                    strategy={'strategy': optimal_strategy.config}
                )

            retrieved_contexts = self.performance_optimizer.optimize_query_processing(
                query=query,
                strategy_config=optimal_strategy.config,
                processing_func=retrieval_func
            )

            logger.info(f"检索完成，获得 {len(retrieved_contexts)} 个文档")

            # 第五步：生成答案
            answer = self._generate_answer(query, retrieved_contexts)

            # 第六步：记录性能并学习
            processing_time = time.time() - start_time
            self._record_performance(query, optimal_strategy.config, processing_time, answer)

            # 构建增强结果
            result = QueryResult(
                query=query,
                answer=answer,
                retrieved_contexts=retrieved_contexts,
                metadata={
                    "analysis_result": analysis_result,
                    "strategy": optimal_strategy.config,
                    "query_features": query_features.__dict__,
                    "predicted_performance": optimal_strategy.predicted_performance.__dict__,
                    "processing_time": processing_time,
                    "optimization_objective": optimization_objective.value,
                    "assistant_type": "intelligent_adaptive"
                }
            )

            self.query_count += 1
            self.total_processing_time += processing_time

            logger.info(f"查询处理完成，耗时: {processing_time:.3f}s")
            return result
            
        except Exception as e:
            logger.error(f"查询处理失败: {e}")
            # 回退到基础助手
            return super().answer(query, **kwargs)
    
    def _generate_answer(self, query: str, contexts: List[RetrievedContext]) -> str:
        """
        生成答案 - 使用 FlexRAG 的生成能力
        """
        try:
            # 构建上下文字符串
            context_str = self._format_contexts(contexts)
            
            # 构建提示
            prompt = self._build_generation_prompt(query, context_str)
            
            # 使用 FlexRAG 的模型生成答案
            response = self.model.generate(prompt)
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"答案生成失败: {e}")
            return f"抱歉，在处理您的问题时遇到了错误：{str(e)}"
    
    def _format_contexts(self, contexts: List[RetrievedContext]) -> str:
        """格式化检索到的上下文"""
        if not contexts:
            return "没有找到相关信息。"
        
        formatted_contexts = []
        for i, ctx in enumerate(contexts, 1):
            formatted_contexts.append(f"[文档 {i}] {ctx.content}")
        
        return "\n\n".join(formatted_contexts)
    
    def _build_generation_prompt(self, query: str, context: str) -> str:
        """构建生成提示"""
        prompt = f"""基于以下上下文信息，回答用户的问题。

上下文信息：
{context}

用户问题：{query}

请基于上下文信息提供准确、有用的回答。如果上下文信息不足以回答问题，请说明这一点。

回答："""
        
        return prompt
    
    def get_analysis_result(self, query: str) -> Dict[str, Any]:
        """获取查询分析结果（用于调试和展示）"""
        return self.query_analyzer.analyze_query(query)
    
    def get_strategy(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """获取策略路由结果（用于调试和展示）"""
        return self.strategy_router.route_strategy(analysis_result)
    
    def get_retrieval_results(self, query: str, strategy: Dict[str, Any]) -> List[RetrievedContext]:
        """获取检索结果（用于调试和展示）"""
        analysis_result = self.query_analyzer.analyze_query(query)
        return self.hybrid_retriever.retrieve(query, analysis_result, strategy)

    def _record_performance(self, query: str, strategy_config: Dict[str, float],
                           processing_time: float, answer: str):
        """记录性能用于学习"""
        try:
            # 简化的性能评估 (实际应用中需要更复杂的评估)
            performance = PerformanceMetrics(
                accuracy=0.8,  # 需要实际评估
                latency=processing_time,
                cost=0.05,     # 需要实际计算
                user_satisfaction=0.8  # 需要用户反馈
            )

            self.intelligent_learner.record_performance(query, strategy_config, performance)
        except Exception as e:
            logger.warning(f"性能记录失败: {e}")

    def get_performance_analytics(self) -> Dict[str, Any]:
        """获取性能分析"""
        optimizer_metrics = self.performance_optimizer.get_performance_metrics()
        cache_stats = self.performance_optimizer.get_cache_statistics()

        return {
            "query_count": self.query_count,
            "avg_processing_time": self.total_processing_time / max(self.query_count, 1),
            "cache_metrics": optimizer_metrics.__dict__,
            "cache_statistics": cache_stats,
            "learning_history_size": len(self.intelligent_learner.performance_history),
            "model_trained": self.intelligent_learner.is_trained
        }

    def optimize_for_objective(self, objective: OptimizationObjective):
        """为特定目标优化系统"""
        logger.info(f"系统优化目标设置为: {objective.value}")
        # 可以在这里调整系统参数

    def warmup_system(self, sample_queries: List[str]):
        """系统预热"""
        logger.info("开始系统预热...")
        self.performance_optimizer.warmup_cache(
            sample_queries,
            self.hybrid_retriever,
            self._generate_answer
        )
        logger.info("系统预热完成")

    def save_learning_state(self, path: str):
        """保存学习状态"""
        self.intelligent_learner.save_model(path)
        logger.info(f"学习状态已保存到: {path}")

    def load_learning_state(self, path: str):
        """加载学习状态"""
        self.intelligent_learner.load_model(path)
        logger.info(f"学习状态已从 {path} 加载")


# 便捷函数
def create_adaptive_assistant(config_path: Optional[str] = None) -> AdaptiveAssistant:
    """创建自适应助手的便捷函数"""
    if config_path:
        # 从配置文件加载
        from flexrag.utils.configure import configure
        cfg = configure(config_path)
    else:
        # 使用默认配置
        cfg = AdaptiveConfig()
    
    return AdaptiveAssistant(cfg)


# 示例用法
if __name__ == "__main__":
    # 创建助手
    assistant = create_adaptive_assistant()
    
    # 测试查询
    test_queries = [
        "What is machine learning?",
        "Compare artificial intelligence and machine learning",
        "Which magazine was started first Arthur's Magazine or First for Women?",
        "Summarize the main points about the 2020 US election"
    ]
    
    for query in test_queries:
        print(f"\n查询: {query}")
        result = assistant.answer(query)
        print(f"答案: {result.answer}")
        print(f"使用文档数: {len(result.retrieved_contexts)}")
