#!/usr/bin/env python3
"""
=== 混合检索器 - 基于 FlexRAG 的智能检索 ===

核心功能：
1. 集成 FlexRAG 的检索器
2. 动态权重分配的混合检索
3. 智能文档聚合和去重
4. 多维度相关性评分
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# 导入 FlexRAG 组件
from flexrag.retriever import FlexRetriever
# from flexrag.ranker import HFRanker  # 暂时注释掉，使用简化版本
from flexrag.utils.dataclasses import RetrievedContext

from .query_analyzer import AnalysisResult
from .strategy_router import RetrievalStrategy

logger = logging.getLogger(__name__)


@dataclass
class ScoredDocument:
    """评分文档数据结构"""
    content: str
    title: str
    doc_id: str
    keyword_score: float
    vector_score: float
    combined_score: float
    relevance_score: float
    diversity_score: float
    final_score: float


class HybridRetriever:
    """
    混合检索器 - 基于 FlexRAG 的智能检索
    
    核心功能：
    1. 关键词检索 + 向量检索
    2. 动态权重分配
    3. 智能聚合和去重
    4. 多维度评分
    """
    
    def __init__(self, cfg):
        self.cfg = cfg
        
        # 初始化 FlexRAG 检索器
        self._init_retrievers()
        
        # 初始化重排序器
        self._init_ranker()
        
        logger.info("HybridRetriever 初始化完成")
    
    def _init_retrievers(self):
        """初始化检索器"""
        try:
            # 这里需要根据实际的 FlexRAG 配置来初始化
            # 暂时使用模拟实现，后续替换为真实的 FlexRAG 检索器
            self.keyword_retriever = None  # FlexRetriever(keyword_config)
            self.vector_retriever = None   # FlexRetriever(vector_config)
            
            logger.warning("使用模拟检索器，需要配置真实的 FlexRAG 检索器")
            
        except Exception as e:
            logger.error(f"检索器初始化失败: {e}")
            self.keyword_retriever = None
            self.vector_retriever = None
    
    def _init_ranker(self):
        """初始化重排序器"""
        try:
            # 使用 FlexRAG 的重排序器
            self.ranker = None  # HFRanker(ranker_config)
            logger.warning("使用模拟重排序器，需要配置真实的 FlexRAG 重排序器")
            
        except Exception as e:
            logger.error(f"重排序器初始化失败: {e}")
            self.ranker = None
    
    def retrieve(self, query: str, analysis_result: AnalysisResult, strategy: Dict[str, Any]) -> List[RetrievedContext]:
        """
        主要的检索方法
        
        Args:
            query: 原始查询
            analysis_result: 查询分析结果
            strategy: 检索策略
            
        Returns:
            List[RetrievedContext]: 检索到的上下文列表
        """
        logger.info(f"开始混合检索: {query}")
        
        retrieval_strategy = strategy["strategy"]
        
        # 1. 执行多路检索
        all_documents = self._multi_retrieval(query, analysis_result, retrieval_strategy)
        
        # 2. 计算综合评分
        scored_documents = self._score_documents(all_documents, query, retrieval_strategy)
        
        # 3. 增强聚合算法 - 改进相关度和多样性平衡
        aggregated_documents = self._enhanced_aggregate_documents(scored_documents, retrieval_strategy, analysis_result, strategy)
        
        # 4. 重排序（如果启用）
        if retrieval_strategy.rerank_enabled and self.ranker:
            aggregated_documents = self._rerank_documents(aggregated_documents, query)
        
        # 5. 转换为 RetrievedContext 格式
        contexts = self._convert_to_contexts(aggregated_documents[:self.cfg.final_docs_count])
        
        logger.info(f"混合检索完成，返回 {len(contexts)} 个文档")
        return contexts
    
    def _multi_retrieval(self, query: str, analysis_result: AnalysisResult, strategy: RetrievalStrategy) -> List[ScoredDocument]:
        """多路检索"""
        all_documents = []
        
        # 1. 关键词检索
        if strategy.keyword_weight > 0:
            keyword_docs = self._keyword_retrieval(query, analysis_result, strategy)
            all_documents.extend(keyword_docs)
        
        # 2. 向量检索
        if strategy.vector_weight > 0:
            vector_docs = self._vector_retrieval(query, analysis_result, strategy)
            all_documents.extend(vector_docs)
        
        # 3. 子查询检索（如果有）
        if analysis_result.sub_queries:
            sub_query_docs = self._sub_query_retrieval(analysis_result.sub_queries, strategy)
            all_documents.extend(sub_query_docs)
        
        return all_documents
    
    def _keyword_retrieval(self, query: str, analysis_result: AnalysisResult, strategy: RetrievalStrategy) -> List[ScoredDocument]:
        """关键词检索"""
        # 模拟实现 - 实际应该使用 FlexRAG 的关键词检索器
        logger.info("执行关键词检索")
        
        # 构建关键词查询
        keywords = analysis_result.keywords + analysis_result.entities
        keyword_query = " ".join(keywords[:5])  # 使用前5个关键词
        
        # 模拟检索结果
        mock_results = [
            {"content": f"关键词检索结果 {i}: {keyword_query}", "title": f"文档 {i}", "doc_id": f"kw_{i}", "score": 0.8 - i * 0.1}
            for i in range(min(strategy.max_docs // 2, 10))
        ]
        
        # 转换为 ScoredDocument
        documents = []
        for result in mock_results:
            doc = ScoredDocument(
                content=result["content"],
                title=result["title"],
                doc_id=result["doc_id"],
                keyword_score=result["score"],
                vector_score=0.0,
                combined_score=0.0,
                relevance_score=0.0,
                diversity_score=0.0,
                final_score=0.0
            )
            documents.append(doc)
        
        return documents
    
    def _vector_retrieval(self, query: str, analysis_result: AnalysisResult, strategy: RetrievalStrategy) -> List[ScoredDocument]:
        """向量检索"""
        # 模拟实现 - 实际应该使用 FlexRAG 的向量检索器
        logger.info("执行向量检索")
        
        # 模拟检索结果
        mock_results = [
            {"content": f"向量检索结果 {i}: {query}", "title": f"向量文档 {i}", "doc_id": f"vec_{i}", "score": 0.9 - i * 0.05}
            for i in range(min(strategy.max_docs // 2, 10))
        ]
        
        # 转换为 ScoredDocument
        documents = []
        for result in mock_results:
            doc = ScoredDocument(
                content=result["content"],
                title=result["title"],
                doc_id=result["doc_id"],
                keyword_score=0.0,
                vector_score=result["score"],
                combined_score=0.0,
                relevance_score=0.0,
                diversity_score=0.0,
                final_score=0.0
            )
            documents.append(doc)
        
        return documents
    
    def _sub_query_retrieval(self, sub_queries, strategy: RetrievalStrategy) -> List[ScoredDocument]:
        """子查询检索"""
        logger.info(f"执行子查询检索，共 {len(sub_queries)} 个子查询")
        
        all_docs = []
        for i, sub_query in enumerate(sub_queries):
            # 模拟子查询检索
            mock_results = [
                {"content": f"子查询 {i} 结果 {j}: {sub_query.content}", "title": f"子查询文档 {i}_{j}", "doc_id": f"sub_{i}_{j}", "score": sub_query.priority * (0.8 - j * 0.1)}
                for j in range(3)  # 每个子查询返回3个结果
            ]
            
            for result in mock_results:
                doc = ScoredDocument(
                    content=result["content"],
                    title=result["title"],
                    doc_id=result["doc_id"],
                    keyword_score=result["score"] * 0.5,
                    vector_score=result["score"] * 0.5,
                    combined_score=0.0,
                    relevance_score=0.0,
                    diversity_score=0.0,
                    final_score=0.0
                )
                all_docs.append(doc)
        
        return all_docs
    
    def _score_documents(self, documents: List[ScoredDocument], query: str, strategy: RetrievalStrategy) -> List[ScoredDocument]:
        """计算文档综合评分"""
        logger.info(f"计算 {len(documents)} 个文档的综合评分")
        
        for doc in documents:
            # 1. 计算综合检索评分
            doc.combined_score = (
                doc.keyword_score * strategy.keyword_weight +
                doc.vector_score * strategy.vector_weight
            )
            
            # 2. 计算相关性评分（简单实现）
            doc.relevance_score = self._calculate_relevance(doc, query)
            
            # 3. 计算多样性评分（简单实现）
            doc.diversity_score = self._calculate_diversity(doc, documents)
            
            # 4. 计算最终评分
            doc.final_score = (
                doc.combined_score * 0.6 +
                doc.relevance_score * 0.3 +
                doc.diversity_score * 0.1
            )
        
        return documents
    
    def _calculate_relevance(self, doc: ScoredDocument, query: str) -> float:
        """计算相关性评分"""
        # 简单的相关性计算
        query_words = set(query.lower().split())
        doc_words = set(doc.content.lower().split())
        
        if not query_words:
            return 0.0
        
        intersection = query_words.intersection(doc_words)
        return len(intersection) / len(query_words)
    
    def _calculate_diversity(self, doc: ScoredDocument, all_docs: List[ScoredDocument]) -> float:
        """计算多样性评分"""
        # 简单的多样性计算 - 基于内容长度差异
        doc_length = len(doc.content)
        
        diversity_score = 0.5  # 基础分数
        
        # 与其他文档的差异性
        for other_doc in all_docs:
            if other_doc.doc_id != doc.doc_id:
                length_diff = abs(len(other_doc.content) - doc_length)
                diversity_score += min(length_diff / 1000, 0.1)  # 长度差异贡献
        
        return min(diversity_score, 1.0)
    
    def _aggregate_documents(self, documents: List[ScoredDocument], strategy: RetrievalStrategy) -> List[ScoredDocument]:
        """智能聚合和去重"""
        logger.info(f"聚合和去重 {len(documents)} 个文档")
        
        # 1. 按最终评分排序
        documents.sort(key=lambda x: x.final_score, reverse=True)
        
        # 2. 去重（基于内容相似度）
        unique_documents = []
        for doc in documents:
            is_duplicate = False
            for existing_doc in unique_documents:
                if self._is_duplicate(doc, existing_doc):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_documents.append(doc)
        
        # 3. 应用多样性过滤
        if strategy.diversity_factor > 0.5:
            unique_documents = self._apply_diversity_filter(unique_documents, strategy)
        
        logger.info(f"聚合完成，保留 {len(unique_documents)} 个文档")
        return unique_documents
    
    def _is_duplicate(self, doc1: ScoredDocument, doc2: ScoredDocument) -> bool:
        """检查是否为重复文档"""
        # 简单的重复检测 - 基于内容相似度
        content1_words = set(doc1.content.lower().split())
        content2_words = set(doc2.content.lower().split())
        
        if not content1_words or not content2_words:
            return False
        
        intersection = content1_words.intersection(content2_words)
        union = content1_words.union(content2_words)
        
        similarity = len(intersection) / len(union)
        return similarity > self.cfg.redundancy_threshold
    
    def _apply_diversity_filter(self, documents: List[ScoredDocument], strategy: RetrievalStrategy) -> List[ScoredDocument]:
        """应用多样性过滤"""
        if len(documents) <= strategy.max_docs:
            return documents
        
        # 选择多样性最高的文档
        selected = [documents[0]]  # 保留评分最高的
        
        for doc in documents[1:]:
            if len(selected) >= strategy.max_docs:
                break
            
            # 计算与已选文档的多样性
            avg_diversity = sum(self._calculate_pairwise_diversity(doc, selected_doc) for selected_doc in selected) / len(selected)
            
            if avg_diversity > strategy.diversity_factor:
                selected.append(doc)
        
        return selected
    
    def _calculate_pairwise_diversity(self, doc1: ScoredDocument, doc2: ScoredDocument) -> float:
        """计算两个文档之间的多样性"""
        # 简单实现 - 基于内容差异
        words1 = set(doc1.content.lower().split())
        words2 = set(doc2.content.lower().split())
        
        if not words1 or not words2:
            return 1.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        similarity = len(intersection) / len(union)
        return 1.0 - similarity
    
    def _rerank_documents(self, documents: List[ScoredDocument], query: str) -> List[ScoredDocument]:
        """重排序文档"""
        logger.info(f"重排序 {len(documents)} 个文档")
        
        # 模拟重排序 - 实际应该使用 FlexRAG 的重排序器
        # 这里简单地基于相关性重新排序
        documents.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return documents
    
    def _convert_to_contexts(self, documents: List[ScoredDocument]) -> List[RetrievedContext]:
        """转换为 RetrievedContext 格式"""
        contexts = []
        
        for doc in documents:
            context = RetrievedContext(
                content=doc.content,
                score=doc.final_score,
                metadata={
                    "title": doc.title,
                    "doc_id": doc.doc_id,
                    "keyword_score": doc.keyword_score,
                    "vector_score": doc.vector_score,
                    "relevance_score": doc.relevance_score,
                    "diversity_score": doc.diversity_score
                }
            )
            contexts.append(context)
        
        return contexts

    def _enhanced_aggregate_documents(self, scored_documents: List[ScoredDocument],
                                    retrieval_strategy: RetrievalStrategy,
                                    analysis_result: AnalysisResult,
                                    strategy_info: Dict[str, Any]) -> List[ScoredDocument]:
        """增强聚合算法 - 改进相关度和多样性平衡"""

        # 1. 去重处理
        unique_documents = self._deduplicate_documents(scored_documents)

        # 2. 多维度评分
        multi_scored_documents = self._multi_dimensional_scoring(unique_documents, analysis_result, strategy_info)

        # 3. 相关度和多样性平衡
        balanced_documents = self._balance_relevance_diversity(multi_scored_documents, retrieval_strategy)

        # 4. 动态选择最终文档
        final_documents = self._dynamic_document_selection(balanced_documents, retrieval_strategy, analysis_result)

        return final_documents

    def _deduplicate_documents(self, documents: List[ScoredDocument]) -> List[ScoredDocument]:
        """智能去重"""
        unique_docs = {}

        for doc in documents:
            # 使用内容哈希作为去重键
            content_hash = hash(doc.content[:200])  # 使用前200字符计算哈希

            if content_hash not in unique_docs:
                unique_docs[content_hash] = doc
            else:
                # 保留评分更高的文档
                if doc.score > unique_docs[content_hash].score:
                    unique_docs[content_hash] = doc

        return list(unique_docs.values())

    def _multi_dimensional_scoring(self, documents: List[ScoredDocument],
                                 analysis_result: AnalysisResult,
                                 strategy_info: Dict[str, Any]) -> List[ScoredDocument]:
        """多维度评分"""
        enhanced_documents = []

        for doc in documents:
            # 基础相关度评分
            relevance_score = doc.score

            # 实体匹配评分
            entity_score = self._calculate_entity_score(doc, analysis_result.entities)

            # 关键词匹配评分
            keyword_score = self._calculate_keyword_score(doc, analysis_result.keywords)

            # 查询类型特定评分
            type_score = self._calculate_type_specific_score(doc, analysis_result.query_type)

            # 综合评分
            final_score = (
                relevance_score * 0.4 +
                entity_score * 0.25 +
                keyword_score * 0.2 +
                type_score * 0.15
            )

            # 创建增强的文档对象
            enhanced_doc = ScoredDocument(
                content=doc.content,
                score=final_score,
                metadata={
                    **doc.metadata,
                    "relevance_score": relevance_score,
                    "entity_score": entity_score,
                    "keyword_score": keyword_score,
                    "type_score": type_score,
                    "enhanced": True
                }
            )
            enhanced_documents.append(enhanced_doc)

        return enhanced_documents

    def _calculate_entity_score(self, doc: ScoredDocument, entities: List[str]) -> float:
        """计算实体匹配评分"""
        if not entities:
            return 0.5  # 默认分数

        content_lower = doc.content.lower()
        matched_entities = 0

        for entity in entities:
            if entity.lower() in content_lower:
                matched_entities += 1

        return min(matched_entities / len(entities), 1.0)

    def _calculate_keyword_score(self, doc: ScoredDocument, keywords: List[str]) -> float:
        """计算关键词匹配评分"""
        if not keywords:
            return 0.5  # 默认分数

        content_lower = doc.content.lower()
        matched_keywords = 0

        for keyword in keywords:
            if keyword.lower() in content_lower:
                matched_keywords += 1

        return min(matched_keywords / len(keywords), 1.0)

    def _calculate_type_specific_score(self, doc: ScoredDocument, query_type: QueryType) -> float:
        """计算查询类型特定评分"""
        content_lower = doc.content.lower()

        if query_type == QueryType.FACTUAL:
            # 事实性查询偏好定义性内容
            factual_indicators = ["define", "definition", "is", "are", "means", "refers to"]
            score = sum(1 for indicator in factual_indicators if indicator in content_lower)
            return min(score / len(factual_indicators), 1.0)

        elif query_type == QueryType.COMPARATIVE:
            # 比较性查询偏好对比性内容
            comparative_indicators = ["compare", "contrast", "difference", "similar", "versus", "vs"]
            score = sum(1 for indicator in comparative_indicators if indicator in content_lower)
            return min(score / len(comparative_indicators), 1.0)

        elif query_type == QueryType.TEMPORAL:
            # 时间相关查询偏好时间信息
            temporal_indicators = ["when", "time", "date", "year", "before", "after", "during"]
            score = sum(1 for indicator in temporal_indicators if indicator in content_lower)
            return min(score / len(temporal_indicators), 1.0)

        return 0.5  # 默认分数

    def _balance_relevance_diversity(self, documents: List[ScoredDocument],
                                   strategy: RetrievalStrategy) -> List[ScoredDocument]:
        """平衡相关度和多样性"""
        if not documents:
            return documents

        # 按相关度排序
        sorted_docs = sorted(documents, key=lambda x: x.score, reverse=True)

        # 多样性选择
        selected_docs = []
        diversity_threshold = 0.8  # 相似度阈值

        for doc in sorted_docs:
            is_diverse = True

            # 检查与已选择文档的相似度
            for selected_doc in selected_docs:
                similarity = self._calculate_content_similarity(doc.content, selected_doc.content)
                if similarity > diversity_threshold:
                    is_diverse = False
                    break

            if is_diverse or len(selected_docs) < 3:  # 至少保证前3个文档
                selected_docs.append(doc)

            # 达到目标数量就停止
            if len(selected_docs) >= strategy.max_docs:
                break

        return selected_docs

    def _calculate_content_similarity(self, content1: str, content2: str) -> float:
        """计算内容相似度（简化版本）"""
        # 简单的词汇重叠相似度
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union)

    def _dynamic_document_selection(self, documents: List[ScoredDocument],
                                  strategy: RetrievalStrategy,
                                  analysis_result: AnalysisResult) -> List[ScoredDocument]:
        """动态选择最终文档"""
        # 根据查询复杂度调整文档数量
        target_count = strategy.max_docs

        if analysis_result.complexity == QueryComplexity.COMPLEX:
            target_count = min(target_count + 3, 20)  # 复杂查询增加文档数
        elif analysis_result.complexity == QueryComplexity.SIMPLE:
            target_count = max(target_count - 2, 3)   # 简单查询减少文档数

        # 根据子查询数量调整
        if len(analysis_result.sub_queries) > 2:
            target_count = min(target_count + 2, 20)

        return documents[:target_count]
