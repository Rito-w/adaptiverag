#!/usr/bin/env python3
"""
=== FlexRAG 深度集成助手 ===

统一管理所有 FlexRAG 集成组件的主助手类
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)

# 导入集成组件
from ..modules.retriever.flexrag_integrated_retriever import FlexRAGIntegratedRetriever
from ..modules.refiner.flexrag_integrated_ranker import FlexRAGIntegratedRanker
from ..modules.generator.flexrag_integrated_generator import FlexRAGIntegratedGenerator
from ..task_decomposer import TaskDecomposer
from ..retrieval_planner import RetrievalPlanner

# 导入统一的数据结构
from ..modules.retriever.flexrag_integrated_retriever import RetrievedContext

# 检查 FlexRAG 可用性
try:
    import flexrag
    FLEXRAG_AVAILABLE = True
except ImportError:
    FLEXRAG_AVAILABLE = False


@dataclass
class AdaptiveRAGResult:
    """自适应 RAG 完整结果"""
    query: str
    answer: str
    subtasks: List[Any]
    retrieval_results: List[Any]
    ranking_results: List[Any]
    generation_result: Any
    total_time: float
    metadata: Dict[str, Any] = None


class FlexRAGIntegratedAssistant:
    """
    FlexRAG 深度集成助手
    
    整合所有 FlexRAG 组件，提供完整的自适应 RAG 流程：
    1. 任务分解 (Task Decomposition)
    2. 检索策略规划 (Retrieval Planning)  
    3. 多模态检索 (Multi-modal Retrieval)
    4. 智能重排序 (Intelligent Reranking)
    5. 自适应生成 (Adaptive Generation)
    """
    
    def __init__(self, config):
        self.config = config
        
        # 初始化所有组件
        logger.info("🚀 初始化 FlexRAG 深度集成助手...")
        
        # 任务分解和规划组件
        self.task_decomposer = TaskDecomposer(config)
        self.retrieval_planner = RetrievalPlanner(config)
        
        # FlexRAG 集成组件
        self.retriever = FlexRAGIntegratedRetriever(config)
        self.ranker = FlexRAGIntegratedRanker(config)
        self.generator = FlexRAGIntegratedGenerator(config)
        
        # 系统状态
        self.is_initialized = True
        self.component_status = self._check_component_status()
        
        logger.info("✅ FlexRAG 深度集成助手初始化完成")
        logger.info(f"📊 组件状态: {self.component_status}")
    
    def _check_component_status(self) -> Dict[str, Any]:
        """检查所有组件状态"""
        return {
            "flexrag_available": FLEXRAG_AVAILABLE,
            "retriever_info": self.retriever.get_retriever_info(),
            "ranker_info": self.ranker.get_ranker_info(),
            "generator_info": self.generator.get_generator_info(),
            "task_decomposer": "active",
            "retrieval_planner": "active"
        }
    
    def answer(
        self,
        query: str,
        strategy_config: Optional[Dict[str, Any]] = None
    ) -> AdaptiveRAGResult:
        """
        主要的问答方法 - 完整的自适应 RAG 流程
        
        Args:
            query: 用户查询
            strategy_config: 可选的策略配置
            
        Returns:
            AdaptiveRAGResult: 完整的 RAG 结果
        """
        start_time = time.time()
        logger.info(f"🔍 开始处理查询: {query}")
        
        # 使用默认策略配置
        if strategy_config is None:
            strategy_config = self._get_default_strategy()
        
        try:
            # === 第一阶段：任务分解和策略规划 ===
            logger.info("📋 第一阶段：任务分解和策略规划")
            
            # 1. 任务分解
            subtasks = self.task_decomposer.decompose_query(query)
            logger.info(f"   分解为 {len(subtasks)} 个子任务")
            
            # 2. 检索策略规划
            retrieval_plans = self.retrieval_planner.plan_retrieval_strategy(subtasks)
            logger.info(f"   生成 {len(retrieval_plans)} 个检索计划")
            
            # === 第二阶段：多模态检索 ===
            logger.info("🔍 第二阶段：多模态检索")
            
            retrieval_results = []
            all_contexts = []
            
            for subtask in subtasks:
                plan = retrieval_plans[subtask.id]
                
                # 转换计划为检索策略
                retrieval_strategy = {
                    "weights": plan.weights,
                    "top_k_per_retriever": plan.top_k_per_retriever,
                    "fusion_method": plan.fusion_method
                }
                
                # 执行检索
                result = self.retriever.adaptive_retrieve(
                    query=subtask.content,
                    strategy=retrieval_strategy,
                    top_k=strategy_config.get("retrieval_top_k", 10)
                )
                
                retrieval_results.append(result)
                all_contexts.extend(result.contexts)
                
                logger.info(f"   子任务 '{subtask.content}' 检索到 {len(result.contexts)} 个文档")
            
            # === 第三阶段：智能重排序 ===
            logger.info("🎯 第三阶段：智能重排序")
            
            if strategy_config.get("enable_reranking", True) and all_contexts:
                ranking_strategy = strategy_config.get("ranking_strategy", {
                    "ranker": "cross_encoder",
                    "enable_multi_ranker": False,
                    "final_top_k": 10
                })
                
                ranking_result = self.ranker.adaptive_rank(
                    query=query,
                    contexts=all_contexts,
                    strategy=ranking_strategy
                )
                
                final_contexts = ranking_result.ranked_contexts
                ranking_results = [ranking_result]
                
                logger.info(f"   重排序完成，最终 {len(final_contexts)} 个文档")
            else:
                # 不使用重排序，直接按分数排序
                final_contexts = sorted(all_contexts, key=lambda x: x.score, reverse=True)
                final_contexts = final_contexts[:strategy_config.get("final_context_count", 10)]
                ranking_results = []
                
                logger.info(f"   跳过重排序，直接使用 {len(final_contexts)} 个文档")
            
            # === 第四阶段：自适应生成 ===
            logger.info("✨ 第四阶段：自适应生成")
            
            generation_strategy = strategy_config.get("generation_strategy", {
                "generator": "main_generator",
                "prompt_template": "default",
                "max_tokens": 256,
                "temperature": 0.7
            })
            
            generation_result = self.generator.adaptive_generate(
                query=query,
                contexts=final_contexts,
                strategy=generation_strategy
            )
            
            logger.info(f"   生成完成，答案长度: {len(generation_result.answer)} 字符")
            
            # === 构建最终结果 ===
            total_time = time.time() - start_time
            
            result = AdaptiveRAGResult(
                query=query,
                answer=generation_result.answer,
                subtasks=subtasks,
                retrieval_results=retrieval_results,
                ranking_results=ranking_results,
                generation_result=generation_result,
                total_time=total_time,
                metadata={
                    "strategy_config": strategy_config,
                    "component_status": self.component_status,
                    "stage_times": {
                        "total": total_time,
                        "generation": generation_result.generation_time,
                        "ranking": ranking_results[0].ranking_time if ranking_results else 0,
                        "retrieval": sum(r.retrieval_time for r in retrieval_results)
                    },
                    "document_counts": {
                        "total_retrieved": len(all_contexts),
                        "final_contexts": len(final_contexts),
                        "subtasks": len(subtasks)
                    }
                }
            )
            
            logger.info(f"🎉 查询处理完成，总耗时: {total_time:.3f}s")
            return result
            
        except Exception as e:
            logger.error(f"❌ 查询处理失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 返回错误结果
            return AdaptiveRAGResult(
                query=query,
                answer=f"抱歉，处理查询时出现错误：{str(e)}",
                subtasks=[],
                retrieval_results=[],
                ranking_results=[],
                generation_result=None,
                total_time=time.time() - start_time,
                metadata={"error": str(e)}
            )
    
    def _get_default_strategy(self) -> Dict[str, Any]:
        """获取默认策略配置"""
        return {
            "retrieval_top_k": 10,
            "enable_reranking": True,
            "final_context_count": 5,
            "ranking_strategy": {
                "ranker": "cross_encoder",
                "enable_multi_ranker": False,
                "final_top_k": 5
            },
            "generation_strategy": {
                "generator": "main_generator",
                "prompt_template": "default",
                "max_tokens": 256,
                "temperature": 0.7,
                "max_context_length": 2000
            }
        }
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        return {
            "assistant_type": "FlexRAG Integrated Assistant",
            "flexrag_available": FLEXRAG_AVAILABLE,
            "is_initialized": self.is_initialized,
            "component_status": self.component_status,
            "supported_features": [
                "Task Decomposition",
                "Retrieval Planning", 
                "Multi-modal Retrieval",
                "Intelligent Reranking",
                "Adaptive Generation"
            ]
        }
    
    def quick_answer(self, query: str) -> str:
        """快速回答（简化接口）"""
        result = self.answer(query)
        return result.answer
    
    def explain_process(self, query: str) -> Dict[str, Any]:
        """解释处理过程（用于调试和可视化）"""
        result = self.answer(query)
        
        return {
            "query": query,
            "process_explanation": {
                "step1_decomposition": {
                    "description": "将复杂查询分解为子任务",
                    "subtasks": [
                        {
                            "content": st.content,
                            "type": st.task_type.value,
                            "priority": st.priority
                        }
                        for st in result.subtasks
                    ]
                },
                "step2_retrieval": {
                    "description": "多模态检索相关文档",
                    "results": [
                        {
                            "query": r.query,
                            "document_count": len(r.contexts),
                            "retrieval_time": r.retrieval_time
                        }
                        for r in result.retrieval_results
                    ]
                },
                "step3_ranking": {
                    "description": "智能重排序优化结果",
                    "enabled": len(result.ranking_results) > 0,
                    "final_count": len(result.ranking_results[0].ranked_contexts) if result.ranking_results else 0
                },
                "step4_generation": {
                    "description": "基于上下文生成最终答案",
                    "generator_type": result.generation_result.generator_type if result.generation_result else "none",
                    "answer_length": len(result.answer)
                }
            },
            "performance": result.metadata.get("stage_times", {}),
            "final_answer": result.answer
        }


if __name__ == "__main__":
    # 测试 FlexRAG 集成助手
    from ..config import FlexRAGIntegratedConfig
    
    config = FlexRAGIntegratedConfig()
    assistant = FlexRAGIntegratedAssistant(config)
    
    # 测试查询
    test_query = "What is the difference between machine learning and deep learning?"
    
    print("🧪 测试 FlexRAG 集成助手")
    print(f"查询: {test_query}")
    print("=" * 60)
    
    # 获取系统信息
    system_info = assistant.get_system_info()
    print(f"系统信息: {system_info}")
    print()
    
    # 执行完整流程
    result = assistant.answer(test_query)
    
    print(f"📊 处理结果:")
    print(f"- 总耗时: {result.total_time:.3f}s")
    print(f"- 子任务数: {len(result.subtasks)}")
    print(f"- 检索结果数: {sum(len(r.contexts) for r in result.retrieval_results)}")
    print(f"- 最终答案: {result.answer[:200]}...")
    
    # 解释处理过程
    explanation = assistant.explain_process(test_query)
    print(f"\n🔍 处理过程解释:")
    for step, details in explanation["process_explanation"].items():
        print(f"- {step}: {details['description']}")
