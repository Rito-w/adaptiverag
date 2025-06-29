#!/usr/bin/env python3
"""
=== FlexRAG 集成重排序器 ===

深度集成 FlexRAG 的重排序器组件
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)

# 导入统一的数据结构
from ..retriever.flexrag_integrated_retriever import RetrievedContext

# 尝试导入 FlexRAG 组件
try:
    from flexrag.ranker import RANKERS, RankerConfig, HFCrossEncoderRanker
    FLEXRAG_AVAILABLE = True
except ImportError:
    logger.warning("FlexRAG 未安装，将使用模拟重排序实现")
    FLEXRAG_AVAILABLE = False


@dataclass
class RankingResult:
    """重排序结果"""
    query: str
    ranked_contexts: List[RetrievedContext]
    ranker_type: str
    ranking_time: float
    metadata: Dict[str, Any] = None


class FlexRAGIntegratedRanker:
    """
    集成 FlexRAG 重排序器的自适应重排序器
    
    支持多种重排序策略：
    1. Cross-Encoder 重排序
    2. ColBERT 重排序  
    3. GPT 重排序
    4. 多重排序器融合
    """
    
    def __init__(self, config):
        self.config = config
        self.rankers = {}
        self.fallback_mode = not FLEXRAG_AVAILABLE
        
        if FLEXRAG_AVAILABLE:
            self._init_flexrag_rankers()
        else:
            self._init_fallback_rankers()
        
        logger.info(f"FlexRAG 集成重排序器初始化完成 (FlexRAG可用: {FLEXRAG_AVAILABLE})")
    
    def _init_flexrag_rankers(self):
        """初始化 FlexRAG 重排序器"""
        try:
            ranker_configs = getattr(self.config, 'ranker_configs', {})

            for name, config_dict in ranker_configs.items():
                try:
                    # 检查是否使用模拟实现
                    if config_dict.get("ranker_type") == "mock" or not FLEXRAG_AVAILABLE:
                        self.rankers[name] = self._create_mock_ranker(name)
                        logger.info(f"✅ 使用模拟重排序器: {name}")
                    else:
                        ranker_config = RankerConfig(**config_dict)
                        ranker = RANKERS.load(ranker_config)
                        self.rankers[name] = ranker
                        logger.info(f"✅ 成功加载 FlexRAG 重排序器: {name}")

                except Exception as e:
                    logger.warning(f"⚠️ 加载重排序器 {name} 失败: {e}，将使用模拟实现")
                    self.rankers[name] = self._create_mock_ranker(name)

            # 如果没有成功加载任何重排序器，使用模拟实现
            if not self.rankers:
                logger.warning("未能加载任何重排序器，使用模拟实现")
                self._init_fallback_rankers()

        except Exception as e:
            logger.error(f"初始化重排序器失败: {e}")
            self._init_fallback_rankers()
    
    def _init_fallback_rankers(self):
        """初始化回退重排序器（模拟实现）"""
        self.rankers = {
            "cross_encoder": self._create_mock_ranker("cross_encoder"),
            "colbert": self._create_mock_ranker("colbert")
        }
        logger.info("使用模拟重排序器实现")
    
    def _create_mock_ranker(self, ranker_type: str):
        """创建模拟重排序器"""
        class MockRanker:
            def __init__(self, rtype):
                self.ranker_type = rtype
                self.reserve_num = 10
            
            def rank(self, query: str, candidates: List[RetrievedContext]):
                """模拟重排序"""
                import random
                
                # 模拟重排序：添加一些随机性，但保持大致的相关性顺序
                ranked_candidates = candidates.copy()
                
                # 为每个候选项计算新的分数
                for i, ctx in enumerate(ranked_candidates):
                    # 基础分数 + 一些随机性
                    base_score = ctx.score
                    random_factor = random.uniform(0.8, 1.2)
                    position_penalty = i * 0.05  # 位置越靠后，分数略微降低
                    
                    new_score = base_score * random_factor - position_penalty
                    ctx.score = max(0.1, new_score)
                    
                    # 更新元数据
                    if ctx.metadata is None:
                        ctx.metadata = {}
                    ctx.metadata["reranked_by"] = self.ranker_type
                    ctx.metadata["original_score"] = base_score
                
                # 按新分数排序
                ranked_candidates.sort(key=lambda x: x.score, reverse=True)
                
                # 返回前 reserve_num 个结果
                return ranked_candidates[:self.reserve_num]
        
        return MockRanker(ranker_type)
    
    def adaptive_rank(
        self,
        query: str,
        contexts: List[RetrievedContext],
        strategy: Dict[str, Any]
    ) -> RankingResult:
        """
        自适应重排序主方法
        
        Args:
            query: 查询字符串
            contexts: 待重排序的上下文列表
            strategy: 重排序策略配置
            
        Returns:
            RankingResult: 重排序结果
        """
        start_time = time.time()
        
        # 解析策略配置
        ranker_name = strategy.get("ranker", "cross_encoder")
        enable_multi_ranker = strategy.get("enable_multi_ranker", False)
        final_top_k = strategy.get("final_top_k", 10)
        
        if enable_multi_ranker:
            # 多重排序器融合
            ranked_contexts = self._multi_ranker_fusion(query, contexts, strategy)
        else:
            # 单一重排序器
            ranked_contexts = self._single_ranker_process(query, contexts, ranker_name)
        
        # 限制最终结果数量
        final_contexts = ranked_contexts[:final_top_k]
        
        ranking_time = time.time() - start_time
        
        result = RankingResult(
            query=query,
            ranked_contexts=final_contexts,
            ranker_type=ranker_name if not enable_multi_ranker else "multi_ranker",
            ranking_time=ranking_time,
            metadata={
                "strategy": strategy,
                "original_count": len(contexts),
                "final_count": len(final_contexts),
                "flexrag_mode": not self.fallback_mode
            }
        )
        
        logger.info(f"重排序完成: {len(contexts)} -> {len(final_contexts)} 个结果，耗时 {ranking_time:.3f}s")
        return result
    
    def _single_ranker_process(
        self,
        query: str,
        contexts: List[RetrievedContext],
        ranker_name: str
    ) -> List[RetrievedContext]:
        """单一重排序器处理"""
        
        if ranker_name not in self.rankers:
            logger.warning(f"重排序器 {ranker_name} 不存在，使用默认排序")
            return contexts
        
        ranker = self.rankers[ranker_name]
        
        try:
            if FLEXRAG_AVAILABLE and hasattr(ranker, 'rank'):
                # 使用 FlexRAG 重排序器
                ranking_result = ranker.rank(query, contexts)
                return ranking_result.candidates
            else:
                # 使用模拟重排序器
                return ranker.rank(query, contexts)
                
        except Exception as e:
            logger.error(f"重排序器 {ranker_name} 执行失败: {e}")
            return contexts
    
    def _multi_ranker_fusion(
        self,
        query: str,
        contexts: List[RetrievedContext],
        strategy: Dict[str, Any]
    ) -> List[RetrievedContext]:
        """多重排序器融合"""
        
        ranker_weights = strategy.get("ranker_weights", {
            "cross_encoder": 0.6,
            "colbert": 0.4
        })
        
        # 收集所有重排序结果
        ranker_results = {}
        
        for ranker_name, weight in ranker_weights.items():
            if weight > 0 and ranker_name in self.rankers:
                try:
                    ranked_contexts = self._single_ranker_process(query, contexts, ranker_name)
                    ranker_results[ranker_name] = {
                        "contexts": ranked_contexts,
                        "weight": weight
                    }
                    logger.debug(f"重排序器 {ranker_name} 完成，权重: {weight}")
                    
                except Exception as e:
                    logger.error(f"重排序器 {ranker_name} 失败: {e}")
        
        if not ranker_results:
            logger.warning("所有重排序器都失败，返回原始顺序")
            return contexts
        
        # 融合重排序结果
        return self._fuse_ranking_results(ranker_results)
    
    def _fuse_ranking_results(self, ranker_results: Dict[str, Dict]) -> List[RetrievedContext]:
        """融合多个重排序器的结果"""
        
        # 为每个上下文计算融合分数
        context_scores = {}
        
        for ranker_name, result_data in ranker_results.items():
            contexts = result_data["contexts"]
            weight = result_data["weight"]
            
            for rank, ctx in enumerate(contexts):
                ctx_id = id(ctx)
                
                if ctx_id not in context_scores:
                    context_scores[ctx_id] = {
                        "context": ctx,
                        "total_score": 0,
                        "ranker_scores": {}
                    }
                
                # 计算位置分数 (排名越靠前分数越高)
                position_score = 1.0 / (rank + 1)
                weighted_score = position_score * weight
                
                context_scores[ctx_id]["total_score"] += weighted_score
                context_scores[ctx_id]["ranker_scores"][ranker_name] = {
                    "rank": rank,
                    "position_score": position_score,
                    "weighted_score": weighted_score
                }
        
        # 按融合分数排序
        sorted_items = sorted(
            context_scores.values(),
            key=lambda x: x["total_score"],
            reverse=True
        )
        
        # 更新上下文的元数据
        fused_contexts = []
        for item in sorted_items:
            ctx = item["context"]
            if ctx.metadata is None:
                ctx.metadata = {}
            
            ctx.metadata["fusion_score"] = item["total_score"]
            ctx.metadata["ranker_scores"] = item["ranker_scores"]
            ctx.metadata["reranked_by"] = "multi_ranker_fusion"
            
            fused_contexts.append(ctx)
        
        return fused_contexts
    
    def get_ranker_info(self) -> Dict[str, Any]:
        """获取重排序器信息"""
        info = {
            "flexrag_available": FLEXRAG_AVAILABLE,
            "fallback_mode": self.fallback_mode,
            "loaded_rankers": list(self.rankers.keys()),
            "ranker_types": {}
        }
        
        for name, ranker in self.rankers.items():
            if hasattr(ranker, 'ranker_type'):
                info["ranker_types"][name] = ranker.ranker_type
            else:
                info["ranker_types"][name] = "mock"
        
        return info


if __name__ == "__main__":
    # 测试集成重排序器
    from ...config import FlexRAGIntegratedConfig
    
    config = FlexRAGIntegratedConfig()
    ranker = FlexRAGIntegratedRanker(config)
    
    # 创建测试上下文
    test_contexts = [
        RetrievedContext(
            content=f"这是测试文档 {i}，包含关于人工智能的内容...",
            score=1.0 - i * 0.1,
            metadata={"doc_id": f"test_{i}"}
        )
        for i in range(5)
    ]
    
    # 测试重排序
    strategy = {
        "ranker": "cross_encoder",
        "enable_multi_ranker": True,
        "ranker_weights": {"cross_encoder": 0.6, "colbert": 0.4},
        "final_top_k": 3
    }
    
    result = ranker.adaptive_rank(
        query="What is artificial intelligence?",
        contexts=test_contexts,
        strategy=strategy
    )
    
    print(f"重排序结果:")
    print(f"- 查询: {result.query}")
    print(f"- 结果数: {len(result.ranked_contexts)}")
    print(f"- 重排序时间: {result.ranking_time:.3f}s")
    print(f"- 重排序器信息: {ranker.get_ranker_info()}")
    
    for i, ctx in enumerate(result.ranked_contexts, 1):
        print(f"\n{i}. 分数: {ctx.score:.3f}")
        print(f"   内容: {ctx.content[:50]}...")
        print(f"   元数据: {ctx.metadata}")
