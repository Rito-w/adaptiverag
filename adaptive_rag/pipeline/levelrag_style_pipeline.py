#!/usr/bin/env python3
"""
=== LevelRAG 风格的分层管道 ===

借鉴 LevelRAG 的两阶段设计，结合 FlexRAG 的组件生态
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SubQuery:
    """子查询"""
    content: str
    query_type: str
    priority: float = 1.0
    dependencies: List[str] = None


@dataclass
class SearchResult:
    """搜索结果"""
    sub_query: SubQuery
    documents: List[Dict[str, Any]]
    confidence: float
    metadata: Dict[str, Any] = None


class LevelRAGStylePipeline:
    """
    LevelRAG 风格的分层管道
    
    第一阶段：高级搜索器 - 查询分解和规划
    第二阶段：低级搜索器 - 具体检索和聚合
    """
    
    def __init__(self, config):
        self.config = config
        
        # 高级组件：查询分析和分解
        from ..task_decomposer import TaskDecomposer
        from ..retrieval_planner import RetrievalPlanner
        
        self.task_decomposer = TaskDecomposer(config)
        self.retrieval_planner = RetrievalPlanner(config)
        
        # 低级组件：具体检索器
        from ..multi_retriever import MultiModalRetriever
        self.multi_retriever = MultiModalRetriever(config)
        
        logger.info("LevelRAG 风格管道初始化完成")
    
    def search(self, query: str, context: str = "") -> Dict[str, Any]:
        """
        主搜索方法 - 实现两阶段搜索
        
        Args:
            query: 用户查询
            context: 可选上下文
            
        Returns:
            搜索结果和元数据
        """
        logger.info(f"开始 LevelRAG 风格搜索: {query}")
        
        # === 第一阶段：高级搜索器 ===
        # 1. 查询分解
        subtasks = self.task_decomposer.decompose_query(query)
        logger.info(f"查询分解完成，生成 {len(subtasks)} 个子任务")
        
        # 2. 检索策略规划
        plans = self.retrieval_planner.plan_retrieval_strategy(subtasks)
        logger.info(f"检索策略规划完成")
        
        # === 第二阶段：低级搜索器 ===
        search_results = []
        
        for subtask in subtasks:
            plan = plans[subtask.id]
            
            # 3. 执行具体检索
            documents = self.multi_retriever.adaptive_retrieve(subtask, plan)
            
            # 4. 构建搜索结果
            result = SearchResult(
                sub_query=SubQuery(
                    content=subtask.content,
                    query_type=subtask.task_type.value,
                    priority=subtask.priority
                ),
                documents=[{
                    "content": doc.content,
                    "score": doc.score,
                    "retriever_type": doc.retriever_type,
                    "metadata": doc.metadata
                } for doc in documents],
                confidence=plan.confidence,
                metadata={
                    "plan": {
                        "weights": plan.weights,
                        "top_k": plan.top_k_per_retriever,
                        "fusion_method": plan.fusion_method
                    },
                    "subtask_info": {
                        "entities": subtask.entities,
                        "temporal_info": subtask.temporal_info
                    }
                }
            )
            
            search_results.append(result)
            logger.info(f"子任务 '{subtask.content}' 检索完成，获得 {len(documents)} 个文档")
        
        # === 结果聚合和后处理 ===
        final_result = self._aggregate_results(query, search_results)
        
        logger.info(f"LevelRAG 风格搜索完成")
        return final_result
    
    def _aggregate_results(self, original_query: str, search_results: List[SearchResult]) -> Dict[str, Any]:
        """聚合搜索结果"""
        
        # 收集所有文档
        all_documents = []
        for result in search_results:
            for doc in result.documents:
                doc["sub_query"] = result.sub_query.content
                doc["sub_query_type"] = result.sub_query.query_type
                doc["sub_query_priority"] = result.sub_query.priority
                all_documents.append(doc)
        
        # 按分数排序
        all_documents.sort(key=lambda x: x["score"], reverse=True)
        
        # 去重（简单实现）
        unique_documents = []
        seen_content = set()
        
        for doc in all_documents:
            content_key = doc["content"][:200]  # 使用前200字符作为去重键
            if content_key not in seen_content:
                seen_content.add(content_key)
                unique_documents.append(doc)
        
        # 构建最终结果
        return {
            "original_query": original_query,
            "search_results": search_results,
            "aggregated_documents": unique_documents[:20],  # 返回前20个
            "metadata": {
                "total_sub_queries": len(search_results),
                "total_documents": len(all_documents),
                "unique_documents": len(unique_documents),
                "pipeline_type": "levelrag_style"
            }
        }
    
    def get_step_by_step_explanation(self, query: str) -> Dict[str, Any]:
        """
        获取 step-by-step 的执行解释
        类似 LevelRAG 的可解释性
        """
        
        # 分解查询
        subtasks = self.task_decomposer.decompose_query(query)
        plans = self.retrieval_planner.plan_retrieval_strategy(subtasks)
        
        explanation = {
            "query": query,
            "steps": [
                {
                    "step": 1,
                    "name": "查询分析与分解",
                    "description": f"将复杂查询分解为 {len(subtasks)} 个子任务",
                    "details": [
                        {
                            "subtask_id": st.id,
                            "content": st.content,
                            "type": st.task_type.value,
                            "priority": st.priority,
                            "entities": st.entities
                        }
                        for st in subtasks
                    ]
                },
                {
                    "step": 2,
                    "name": "检索策略规划",
                    "description": "为每个子任务制定个性化检索策略",
                    "details": [
                        {
                            "subtask_id": plan_id,
                            "weights": plan.weights,
                            "top_k": plan.top_k_per_retriever,
                            "confidence": plan.confidence
                        }
                        for plan_id, plan in plans.items()
                    ]
                },
                {
                    "step": 3,
                    "name": "多模态检索",
                    "description": "使用不同检索器获取相关文档"
                },
                {
                    "step": 4,
                    "name": "结果聚合",
                    "description": "智能聚合和去重，生成最终结果"
                }
            ]
        }
        
        return explanation


if __name__ == "__main__":
    # 测试 LevelRAG 风格管道
    from ..config import create_default_config
    
    config = create_default_config()
    pipeline = LevelRAGStylePipeline(config)
    
    # 测试查询
    test_query = "Which magazine was started first Arthur's Magazine or First for Women?"
    
    # 获取执行解释
    explanation = pipeline.get_step_by_step_explanation(test_query)
    print("Step-by-step 执行计划:")
    for step in explanation["steps"]:
        print(f"步骤 {step['step']}: {step['name']}")
        print(f"  描述: {step['description']}")
        if "details" in step:
            print(f"  详情: {len(step['details'])} 项")
    
    # 执行搜索
    result = pipeline.search(test_query)
    print(f"\n搜索完成:")
    print(f"- 子查询数: {result['metadata']['total_sub_queries']}")
    print(f"- 总文档数: {result['metadata']['total_documents']}")
    print(f"- 去重后: {result['metadata']['unique_documents']}")
