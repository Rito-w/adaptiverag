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
        
        logger.info("AdaptiveAssistant 初始化完成")
    
    def answer(self, query: str, **kwargs) -> QueryResult:
        """
        主要的问答方法 - 实现自适应 RAG 流程
        
        流程：
        1. 查询分析和分解
        2. 策略路由
        3. 混合检索
        4. 智能聚合
        5. 生成答案
        """
        logger.info(f"开始处理查询: {query}")
        
        try:
            # 第一步：查询分析和分解
            analysis_result = self.query_analyzer.analyze_query(query)
            logger.info(f"查询分析完成: {analysis_result}")
            
            # 第二步：策略路由
            strategy = self.strategy_router.route_strategy(analysis_result)
            logger.info(f"策略路由完成: {strategy}")
            
            # 第三步：混合检索
            retrieved_contexts = self.hybrid_retriever.retrieve(
                query=query,
                analysis_result=analysis_result,
                strategy=strategy
            )
            logger.info(f"检索完成，获得 {len(retrieved_contexts)} 个文档")
            
            # 第四步：生成答案（使用 FlexRAG 的生成能力）
            answer = self._generate_answer(query, retrieved_contexts)
            
            # 构建结果
            result = QueryResult(
                query=query,
                answer=answer,
                retrieved_contexts=retrieved_contexts,
                metadata={
                    "analysis_result": analysis_result,
                    "strategy": strategy,
                    "assistant_type": "adaptive"
                }
            )
            
            logger.info("查询处理完成")
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
