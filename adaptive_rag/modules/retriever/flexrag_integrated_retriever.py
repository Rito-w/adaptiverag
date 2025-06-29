#!/usr/bin/env python3
"""
=== FlexRAG 集成检索器 ===

深度集成 FlexRAG 的检索器组件，提供统一的检索接口
"""

import logging
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# 定义统一的数据结构
class RetrievedContext:
    """统一的检索上下文类"""
    def __init__(self, content, score, metadata=None):
        self.content = content
        self.score = score
        self.metadata = metadata or {}

# 尝试导入 FlexRAG 组件
try:
    from flexrag.retriever import RETRIEVERS, RetrieverConfig, FlexRetriever
    FLEXRAG_AVAILABLE = True
except ImportError:
    logger.warning("FlexRAG 未安装，将使用模拟实现")
    FLEXRAG_AVAILABLE = False


@dataclass
class AdaptiveRetrievalResult:
    """自适应检索结果"""
    query: str
    contexts: List[RetrievedContext]
    retriever_type: str
    retrieval_time: float
    metadata: Dict[str, Any] = None


class FlexRAGIntegratedRetriever:
    """
    集成 FlexRAG 检索器的自适应检索器
    
    支持多种检索策略：
    1. 关键词检索 (BM25/Elasticsearch)
    2. 密集检索 (Dense/Vector)
    3. 混合检索 (Hybrid)
    4. Web 检索 (Web Search)
    """
    
    def __init__(self, config):
        self.config = config
        self.retrievers = {}
        self.fallback_mode = not FLEXRAG_AVAILABLE
        
        if FLEXRAG_AVAILABLE:
            self._init_flexrag_retrievers()
        else:
            self._init_fallback_retrievers()
        
        logger.info(f"FlexRAG 集成检索器初始化完成 (FlexRAG可用: {FLEXRAG_AVAILABLE})")
    
    def _init_flexrag_retrievers(self):
        """初始化 FlexRAG 检索器"""
        try:
            retriever_configs = getattr(self.config, 'retriever_configs', {})

            for name, config_dict in retriever_configs.items():
                try:
                    # 检查是否使用模拟实现
                    if config_dict.get("retriever_type") == "mock" or not FLEXRAG_AVAILABLE:
                        self.retrievers[name] = self._create_mock_retriever(name)
                        logger.info(f"✅ 使用模拟检索器: {name}")
                    else:
                        # 尝试创建 FlexRAG 检索器配置
                        retriever_config = RetrieverConfig(**config_dict)
                        retriever = RETRIEVERS.load(retriever_config)
                        self.retrievers[name] = retriever
                        logger.info(f"✅ 成功加载 FlexRAG 检索器: {name}")

                except Exception as e:
                    logger.warning(f"⚠️ 加载检索器 {name} 失败: {e}，将使用模拟实现")
                    self.retrievers[name] = self._create_mock_retriever(name)

            # 如果没有成功加载任何检索器，使用模拟实现
            if not self.retrievers:
                logger.warning("未能加载任何检索器，使用模拟实现")
                self._init_fallback_retrievers()

        except Exception as e:
            logger.error(f"初始化检索器失败: {e}")
            self._init_fallback_retrievers()
    
    def _init_fallback_retrievers(self):
        """初始化回退检索器（模拟实现）"""
        self.retrievers = {
            "keyword_retriever": self._create_mock_retriever("keyword"),
            "dense_retriever": self._create_mock_retriever("dense"),
            "web_retriever": self._create_mock_retriever("web")
        }
        logger.info("使用模拟检索器实现")
    
    def _create_mock_retriever(self, retriever_type: str):
        """创建模拟检索器"""
        class MockRetriever:
            def __init__(self, rtype):
                self.retriever_type = rtype
            
            def search(self, query: str, top_k: int = 10) -> List[RetrievedContext]:
                # 模拟检索结果
                results = []
                for i in range(min(top_k, 5)):
                    score = max(0.1, 1.0 - i * 0.15)
                    content = f"模拟{self.retriever_type}检索结果 {i+1}: 关于 '{query}' 的相关内容..."
                    
                    context = RetrievedContext(
                        content=content,
                        score=score,
                        metadata={
                            "retriever_type": self.retriever_type,
                            "doc_id": f"mock_{self.retriever_type}_{i}",
                            "source": "mock_corpus"
                        }
                    )

                    # 确保 metadata 属性存在
                    if not hasattr(context, 'metadata'):
                        context.metadata = {
                            "retriever_type": self.retriever_type,
                            "doc_id": f"mock_{self.retriever_type}_{i}",
                            "source": "mock_corpus"
                        }
                    results.append(context)
                
                return results
        
        return MockRetriever(retriever_type)
    
    def adaptive_retrieve(
        self, 
        query: str, 
        strategy: Dict[str, Any],
        top_k: int = 10
    ) -> AdaptiveRetrievalResult:
        """
        自适应检索主方法
        
        Args:
            query: 查询字符串
            strategy: 检索策略配置
            top_k: 返回结果数量
            
        Returns:
            AdaptiveRetrievalResult: 检索结果
        """
        import time
        start_time = time.time()
        
        # 解析策略配置
        weights = strategy.get("weights", {"keyword": 0.33, "dense": 0.33, "web": 0.34})
        retriever_top_k = strategy.get("top_k_per_retriever", {})
        fusion_method = strategy.get("fusion_method", "weighted_sum")
        
        all_contexts = []
        
        # 执行多种检索
        for retriever_name, weight in weights.items():
            if weight > 0 and retriever_name + "_retriever" in self.retrievers:
                retriever = self.retrievers[retriever_name + "_retriever"]
                k = retriever_top_k.get(retriever_name, top_k)
                
                try:
                    contexts = retriever.search(query, top_k=k)
                    
                    # 调整分数权重
                    for ctx in contexts:
                        ctx.score *= weight
                        if not hasattr(ctx, 'metadata') or ctx.metadata is None:
                            ctx.metadata = {}
                        ctx.metadata["retriever_weight"] = weight
                        ctx.metadata["original_retriever"] = retriever_name
                    
                    all_contexts.extend(contexts)
                    logger.debug(f"检索器 {retriever_name} 返回 {len(contexts)} 个结果")
                    
                except Exception as e:
                    logger.error(f"检索器 {retriever_name} 执行失败: {e}")
        
        # 融合结果
        fused_contexts = self._fuse_results(all_contexts, fusion_method, top_k)
        
        retrieval_time = time.time() - start_time
        
        result = AdaptiveRetrievalResult(
            query=query,
            contexts=fused_contexts,
            retriever_type="adaptive_hybrid",
            retrieval_time=retrieval_time,
            metadata={
                "strategy": strategy,
                "total_retrieved": len(all_contexts),
                "final_count": len(fused_contexts),
                "fusion_method": fusion_method,
                "flexrag_mode": not self.fallback_mode
            }
        )
        
        logger.info(f"自适应检索完成: {len(fused_contexts)} 个结果，耗时 {retrieval_time:.3f}s")
        return result
    
    def _fuse_results(
        self, 
        contexts: List[RetrievedContext], 
        method: str, 
        top_k: int
    ) -> List[RetrievedContext]:
        """融合检索结果"""
        
        if method == "weighted_sum":
            # 按加权分数排序
            sorted_contexts = sorted(contexts, key=lambda x: x.score, reverse=True)
        
        elif method == "rrf":
            # 倒数排名融合 (Reciprocal Rank Fusion)
            retriever_groups = {}
            for ctx in contexts:
                retriever = ctx.metadata.get("original_retriever", "unknown")
                if retriever not in retriever_groups:
                    retriever_groups[retriever] = []
                retriever_groups[retriever].append(ctx)
            
            # 为每个检索器的结果排序
            for retriever, group_contexts in retriever_groups.items():
                group_contexts.sort(key=lambda x: x.score, reverse=True)
            
            # 计算 RRF 分数
            rrf_scores = {}
            for retriever, group_contexts in retriever_groups.items():
                for rank, ctx in enumerate(group_contexts):
                    ctx_id = id(ctx)
                    if ctx_id not in rrf_scores:
                        rrf_scores[ctx_id] = {"context": ctx, "score": 0}
                    rrf_scores[ctx_id]["score"] += 1.0 / (rank + 60)  # RRF with k=60
            
            # 按 RRF 分数排序
            sorted_items = sorted(rrf_scores.values(), key=lambda x: x["score"], reverse=True)
            sorted_contexts = [item["context"] for item in sorted_items]
        
        else:
            # 默认按原始分数排序
            sorted_contexts = sorted(contexts, key=lambda x: x.score, reverse=True)
        
        # 去重
        unique_contexts = self._deduplicate_contexts(sorted_contexts)
        
        return unique_contexts[:top_k]
    
    def _deduplicate_contexts(self, contexts: List[RetrievedContext]) -> List[RetrievedContext]:
        """去重检索结果"""
        seen_content = set()
        unique_contexts = []
        
        for ctx in contexts:
            # 使用内容的前200字符作为去重键
            content_key = ctx.content[:200].strip()
            if content_key not in seen_content:
                seen_content.add(content_key)
                unique_contexts.append(ctx)
        
        return unique_contexts
    
    def get_retriever_info(self) -> Dict[str, Any]:
        """获取检索器信息"""
        info = {
            "flexrag_available": FLEXRAG_AVAILABLE,
            "fallback_mode": self.fallback_mode,
            "loaded_retrievers": list(self.retrievers.keys()),
            "retriever_types": {}
        }
        
        for name, retriever in self.retrievers.items():
            if hasattr(retriever, 'retriever_type'):
                info["retriever_types"][name] = retriever.retriever_type
            else:
                info["retriever_types"][name] = "mock"
        
        return info


if __name__ == "__main__":
    # 测试集成检索器
    from ...config import FlexRAGIntegratedConfig
    
    config = FlexRAGIntegratedConfig()
    retriever = FlexRAGIntegratedRetriever(config)
    
    # 测试检索
    strategy = {
        "weights": {"keyword": 0.4, "dense": 0.4, "web": 0.2},
        "top_k_per_retriever": {"keyword": 5, "dense": 5, "web": 3},
        "fusion_method": "rrf"
    }
    
    result = retriever.adaptive_retrieve(
        query="What is artificial intelligence?",
        strategy=strategy,
        top_k=10
    )
    
    print(f"检索结果:")
    print(f"- 查询: {result.query}")
    print(f"- 结果数: {len(result.contexts)}")
    print(f"- 检索时间: {result.retrieval_time:.3f}s")
    print(f"- 检索器信息: {retriever.get_retriever_info()}")
    
    for i, ctx in enumerate(result.contexts[:3], 1):
        print(f"\n{i}. 分数: {ctx.score:.3f}")
        print(f"   内容: {ctx.content[:100]}...")
        print(f"   元数据: {ctx.metadata}")
