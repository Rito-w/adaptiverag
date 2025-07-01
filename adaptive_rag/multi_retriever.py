#!/usr/bin/env python3Add comment更多操作
"""
=== 多模态检索器 ===

集成多种检索方法的统一检索器
"""

import logging
from typing import Dict, List, Any
from dataclasses import dataclass
from adaptive_rag.task_decomposer import SubTask
from adaptive_rag.retrieval_planner import RetrievalPlan

logger = logging.getLogger(__name__)


@dataclass
class RetrievedDocument:
    """检索到的文档"""
    content: str
    score: float
    retriever_type: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class MultiModalRetriever:
    """多模态检索器"""
    
    def __init__(self, config, data_manager=None):
        self.config = config

        # 初始化各种检索器
        self.keyword_retriever = None
        self.dense_retriever = None
        self.web_retriever = None

        # 使用传入的数据管理器或创建新的
        if data_manager is not None:
            self.data_manager = data_manager
            logger.info("MultiModalRetriever 使用共享的数据管理器")
        else:
            # 初始化数据管理器
            from adaptive_rag.data_manager import DataManager
            self.data_manager = DataManager(config)

            # 立即加载数据
            doc_count = self.data_manager.load_corpus()
            logger.info(f"MultiModalRetriever 加载了 {doc_count} 个文档")

        logger.info("MultiModalRetriever 初始化完成")
    
    def adaptive_retrieve(self, subtask: SubTask, plan: RetrievalPlan) -> List[RetrievedDocument]:
        """自适应检索"""
        all_documents = []
        
        # 关键词检索
        if plan.weights.get("keyword", 0) > 0:
            keyword_docs = self._keyword_retrieve(subtask, plan)
            all_documents.extend(keyword_docs)
        
        # 向量检索
        if plan.weights.get("dense", 0) > 0:
            dense_docs = self._dense_retrieve(subtask, plan)
            all_documents.extend(dense_docs)
        
        # Web 检索
        if plan.weights.get("web", 0) > 0:
            web_docs = self._web_retrieve(subtask, plan)
            all_documents.extend(web_docs)
        
        # 融合结果
        fused_documents = self._fuse_results(all_documents, plan)
        
        logger.info(f"为子任务 '{subtask.content}' 检索到 {len(fused_documents)} 个文档")
        return fused_documents
    
    def _keyword_retrieve(self, subtask: SubTask, plan: RetrievalPlan) -> List[RetrievedDocument]:
        """关键词检索"""
        try:
            # 使用数据管理器进行搜索
            top_k = plan.top_k_per_retriever.get("keyword", 5)
            documents = self.data_manager.search_documents(subtask.content, top_k=top_k)
            
            retrieved_docs = []
            for i, doc in enumerate(documents):
                # 计算基于关键词的评分
                score = max(0.1, 1.0 - i * 0.1)  # 简单的排名评分
                
                retrieved_doc = RetrievedDocument(
                    content=doc.content,
                    score=score * plan.weights.get("keyword", 0.33),
                    retriever_type="keyword",
                    metadata={
                        "title": doc.title,
                        "source": doc.source,
                        "doc_id": doc.id
                    }
                )
                retrieved_docs.append(retrieved_doc)
            
            return retrieved_docs
            
        except Exception as e:
            logger.error(f"关键词检索失败: {e}")
            return []
    
    def _dense_retrieve(self, subtask: SubTask, plan: RetrievalPlan) -> List[RetrievedDocument]:
        """向量检索"""
        try:
            # 模拟向量检索
            top_k = plan.top_k_per_retriever.get("dense", 5)
            documents = self.data_manager.search_documents(subtask.content, top_k=top_k)
            
            retrieved_docs = []
            for i, doc in enumerate(documents):
                # 模拟语义相似度评分
                score = max(0.2, 0.9 - i * 0.1)  # 向量检索通常有更高的基础分
                
                retrieved_doc = RetrievedDocument(
                    content=doc.content,
                    score=score * plan.weights.get("dense", 0.33),
                    retriever_type="dense",
                    metadata={
                        "title": doc.title,
                        "source": doc.source,
                        "doc_id": doc.id,
                        "semantic_score": score
                    }
                )
                retrieved_docs.append(retrieved_doc)
            
            return retrieved_docs
            
        except Exception as e:
            logger.error(f"向量检索失败: {e}")
            return []
    
    def _web_retrieve(self, subtask: SubTask, plan: RetrievalPlan) -> List[RetrievedDocument]:
        """Web 检索"""
        try:
            # 模拟 Web 检索
            top_k = plan.top_k_per_retriever.get("web", 3)
            
            # 简单模拟：从现有文档中选择一些作为"web"结果
            documents = self.data_manager.search_documents(subtask.content, top_k=top_k)
            
            retrieved_docs = []
            for i, doc in enumerate(documents):
                score = max(0.15, 0.7 - i * 0.15)  # Web 检索评分
                
                retrieved_doc = RetrievedDocument(
                    content=doc.content,
                    score=score * plan.weights.get("web", 0.34),
                    retriever_type="web",
                    metadata={
                        "title": doc.title,
                        "source": "web_search",
                        "doc_id": f"web_{doc.id}",
                        "web_score": score
                    }
                )
                retrieved_docs.append(retrieved_doc)
            
            return retrieved_docs
            
        except Exception as e:
            logger.error(f"Web 检索失败: {e}")
            return []
    
    def _fuse_results(self, documents: List[RetrievedDocument], plan: RetrievalPlan) -> List[RetrievedDocument]:
        """融合检索结果"""
        if plan.fusion_method == "weighted_sum":
            # 按加权分数排序
            sorted_docs = sorted(documents, key=lambda x: x.score, reverse=True)
        elif plan.fusion_method == "rank_fusion":
            # 实现排名融合
            sorted_docs = self._rank_fusion(documents)
        else:
            # 默认按分数排序
            sorted_docs = sorted(documents, key=lambda x: x.score, reverse=True)
        
        # 去重
        unique_docs = self._deduplicate(sorted_docs)
        
        # 返回前 N 个结果
        max_results = sum(plan.top_k_per_retriever.values())
        return unique_docs[:max_results]
    
    def _rank_fusion(self, documents: List[RetrievedDocument]) -> List[RetrievedDocument]:
        """排名融合算法"""
        # 简单的排名融合实现
        retriever_docs = {}
        
        # 按检索器分组
        for doc in documents:
            if doc.retriever_type not in retriever_docs:
                retriever_docs[doc.retriever_type] = []
            retriever_docs[doc.retriever_type].append(doc)
        
        # 为每个检索器的结果排序
        for retriever_type in retriever_docs:
            retriever_docs[retriever_type].sort(key=lambda x: x.score, reverse=True)
        
        # 计算融合分数
        fused_docs = {}
        for retriever_type, docs in retriever_docs.items():
            for rank, doc in enumerate(docs):
                doc_key = doc.content[:100]  # 使用内容前100字符作为键
                if doc_key not in fused_docs:
                    fused_docs[doc_key] = doc
                    fused_docs[doc_key].score = 0
                
                # RRF (Reciprocal Rank Fusion) 公式
                fused_docs[doc_key].score += 1.0 / (rank + 1)
        
        return sorted(fused_docs.values(), key=lambda x: x.score, reverse=True)
    
    def _deduplicate(self, documents: List[RetrievedDocument]) -> List[RetrievedDocument]:
        """去重"""
        seen_content = set()
        unique_docs = []
        
        for doc in documents:
            # 使用内容的前200字符作为去重键
            content_key = doc.content[:200]
            if content_key not in seen_content:
                seen_content.add(content_key)
                unique_docs.append(doc)
        
        return unique_docs
    
    def get_retriever_stats(self) -> Dict[str, Any]:
        """获取检索器统计信息"""
        return {
            "keyword_retriever": "active" if self.keyword_retriever else "simulated",
            "dense_retriever": "active" if self.dense_retriever else "simulated",
            "web_retriever": "active" if self.web_retriever else "simulated",
            "data_manager": "active"
        }


if __name__ == "__main__":
    # 测试多模态检索器
    from adaptive_rag.config import create_default_config
    from adaptive_rag.task_decomposer import TaskDecomposer, SubTask, TaskType
    from adaptive_rag.retrieval_planner import RetrievalPlanner
    
    config = create_default_config()
    decomposer = TaskDecomposer(config)
    planner = RetrievalPlanner(config)
    retriever = MultiModalRetriever(config)
    
    # 创建测试子任务
    subtask = SubTask(
        id="test_1",
        content="What is machine learning?",
        task_type=TaskType.FACTUAL,
        priority=0.9,
        entities=["machine learning"]
    )
    
    # 创建检索计划
    plan = planner._create_plan_for_task(subtask)
    
    # 执行检索
    results = retriever.adaptive_retrieve(subtask, plan)
    
    print(f"检索结果 ({len(results)} 个文档):")
    for i, doc in enumerate(results, 1):
        print(f"{i}. [{doc.retriever_type}] 分数: {doc.score:.3f}")
        print(f"   内容: {doc.content[:100]}...")
        print()