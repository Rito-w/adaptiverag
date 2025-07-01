#!/usr/bin/env python3
"""
=== 性能优化模块 ===

借鉴 TurboRAG 的思想，实现缓存和性能优化
这是我们在效率方面的创新点
"""

import logging
import time
import hashlib
import pickle
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import OrderedDict
import threading
from functools import wraps

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """缓存条目"""
    data: Any
    timestamp: float
    access_count: int
    last_access: float
    size_bytes: int


@dataclass
class PerformanceMetrics:
    """性能指标"""
    cache_hit_rate: float
    avg_retrieval_time: float
    avg_generation_time: float
    memory_usage_mb: float
    total_queries: int


class LRUCache:
    """LRU缓存实现"""
    
    def __init__(self, max_size: int = 1000, max_memory_mb: int = 500):
        self.max_size = max_size
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.current_memory = 0
        self.lock = threading.RLock()
        
        # 统计信息
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存项"""
        with self.lock:
            if key in self.cache:
                entry = self.cache[key]
                entry.access_count += 1
                entry.last_access = time.time()
                # 移到末尾（最近使用）
                self.cache.move_to_end(key)
                self.hits += 1
                return entry.data
            else:
                self.misses += 1
                return None
    
    def put(self, key: str, data: Any, size_bytes: int = None):
        """添加缓存项"""
        if size_bytes is None:
            size_bytes = len(pickle.dumps(data))
        
        with self.lock:
            current_time = time.time()
            
            # 如果已存在，更新
            if key in self.cache:
                old_entry = self.cache[key]
                self.current_memory -= old_entry.size_bytes
            
            # 创建新条目
            entry = CacheEntry(
                data=data,
                timestamp=current_time,
                access_count=1,
                last_access=current_time,
                size_bytes=size_bytes
            )
            
            # 检查内存限制
            while (self.current_memory + size_bytes > self.max_memory_bytes or 
                   len(self.cache) >= self.max_size) and self.cache:
                self._evict_lru()
            
            self.cache[key] = entry
            self.current_memory += size_bytes
    
    def _evict_lru(self):
        """驱逐最少使用的项"""
        if self.cache:
            key, entry = self.cache.popitem(last=False)
            self.current_memory -= entry.size_bytes
    
    def get_hit_rate(self) -> float:
        """获取缓存命中率"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    def clear(self):
        """清空缓存"""
        with self.lock:
            self.cache.clear()
            self.current_memory = 0
            self.hits = 0
            self.misses = 0


class QueryCache:
    """查询结果缓存"""
    
    def __init__(self, max_size: int = 500):
        self.cache = LRUCache(max_size=max_size, max_memory_mb=200)
    
    def get_cache_key(self, query: str, strategy_config: Dict[str, Any]) -> str:
        """生成缓存键"""
        # 将查询和策略配置组合生成唯一键
        content = f"{query}_{str(sorted(strategy_config.items()))}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_cached_result(self, query: str, strategy_config: Dict[str, Any]) -> Optional[Any]:
        """获取缓存的查询结果"""
        key = self.get_cache_key(query, strategy_config)
        return self.cache.get(key)
    
    def cache_result(self, query: str, strategy_config: Dict[str, Any], result: Any):
        """缓存查询结果"""
        key = self.get_cache_key(query, strategy_config)
        self.cache.put(key, result)


class DocumentCache:
    """文档检索缓存 - 借鉴 TurboRAG 思想"""
    
    def __init__(self, max_size: int = 2000):
        self.cache = LRUCache(max_size=max_size, max_memory_mb=300)
        self.precomputed_embeddings = {}  # 预计算的文档嵌入
    
    def get_cache_key(self, query: str, retriever_type: str, top_k: int) -> str:
        """生成检索缓存键"""
        content = f"{query}_{retriever_type}_{top_k}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_cached_documents(self, query: str, retriever_type: str, top_k: int) -> Optional[List[Any]]:
        """获取缓存的检索结果"""
        key = self.get_cache_key(query, retriever_type, top_k)
        return self.cache.get(key)
    
    def cache_documents(self, query: str, retriever_type: str, top_k: int, documents: List[Any]):
        """缓存检索结果"""
        key = self.get_cache_key(query, retriever_type, top_k)
        self.cache.put(key, documents)
    
    def precompute_document_embeddings(self, documents: List[Any], embedder):
        """预计算文档嵌入 - TurboRAG 启发"""
        logger.info(f"开始预计算 {len(documents)} 个文档的嵌入")
        
        for doc in documents:
            doc_id = doc.get('id', str(hash(doc.get('content', ''))))
            if doc_id not in self.precomputed_embeddings:
                embedding = embedder.encode(doc.get('content', ''))
                self.precomputed_embeddings[doc_id] = embedding
        
        logger.info("文档嵌入预计算完成")


def performance_monitor(func):
    """性能监控装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            
            # 记录性能指标
            duration = end_time - start_time
            logger.debug(f"{func.__name__} 执行时间: {duration:.3f}s")
            
            return result
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            logger.error(f"{func.__name__} 执行失败 (耗时: {duration:.3f}s): {e}")
            raise
    
    return wrapper


class PerformanceOptimizer:
    """性能优化器 - 主要类"""
    
    def __init__(self, config):
        self.config = config
        
        # 初始化缓存
        self.query_cache = QueryCache(max_size=config.get('query_cache_size', 500))
        self.document_cache = DocumentCache(max_size=config.get('doc_cache_size', 2000))
        
        # 性能统计
        self.performance_stats = {
            'total_queries': 0,
            'cache_hits': 0,
            'total_retrieval_time': 0.0,
            'total_generation_time': 0.0,
            'start_time': time.time()
        }
        
        # 预热缓存标志
        self.is_warmed_up = False
        
        logger.info("PerformanceOptimizer 初始化完成")
    
    @performance_monitor
    def optimize_retrieval(self, query: str, retriever_type: str, top_k: int, 
                          retriever_func, *args, **kwargs) -> List[Any]:
        """优化检索过程"""
        # 1. 尝试从缓存获取
        cached_docs = self.document_cache.get_cached_documents(query, retriever_type, top_k)
        if cached_docs is not None:
            logger.debug(f"缓存命中: {retriever_type} 检索")
            self.performance_stats['cache_hits'] += 1
            return cached_docs
        
        # 2. 执行实际检索
        start_time = time.time()
        documents = retriever_func(*args, **kwargs)
        retrieval_time = time.time() - start_time
        
        # 3. 缓存结果
        self.document_cache.cache_documents(query, retriever_type, top_k, documents)
        
        # 4. 更新统计
        self.performance_stats['total_retrieval_time'] += retrieval_time
        
        return documents
    
    @performance_monitor
    def optimize_query_processing(self, query: str, strategy_config: Dict[str, Any], 
                                 processing_func, *args, **kwargs) -> Any:
        """优化查询处理过程"""
        # 1. 尝试从缓存获取完整结果
        cached_result = self.query_cache.get_cached_result(query, strategy_config)
        if cached_result is not None:
            logger.debug("查询结果缓存命中")
            self.performance_stats['cache_hits'] += 1
            return cached_result
        
        # 2. 执行实际处理
        start_time = time.time()
        result = processing_func(*args, **kwargs)
        processing_time = time.time() - start_time
        
        # 3. 缓存结果
        self.query_cache.cache_result(query, strategy_config, result)
        
        # 4. 更新统计
        self.performance_stats['total_generation_time'] += processing_time
        self.performance_stats['total_queries'] += 1
        
        return result
    
    def warmup_cache(self, sample_queries: List[str], retriever, generator):
        """缓存预热 - 提升首次查询性能"""
        logger.info(f"开始缓存预热，使用 {len(sample_queries)} 个样本查询")
        
        for query in sample_queries:
            try:
                # 预热不同类型的检索
                for retriever_type in ['keyword', 'dense', 'web']:
                    if hasattr(retriever, f'{retriever_type}_retrieve'):
                        retriever_func = getattr(retriever, f'{retriever_type}_retrieve')
                        self.optimize_retrieval(query, retriever_type, 5, retriever_func, query)
                
                # 预热查询处理
                strategy_config = {'keyword': 0.4, 'dense': 0.4, 'web': 0.2}
                self.optimize_query_processing(
                    query, strategy_config, 
                    lambda: f"预热响应: {query}"
                )
                
            except Exception as e:
                logger.warning(f"预热查询失败: {query}, 错误: {e}")
        
        self.is_warmed_up = True
        logger.info("缓存预热完成")
    
    def get_performance_metrics(self) -> PerformanceMetrics:
        """获取性能指标"""
        total_queries = self.performance_stats['total_queries']
        runtime = time.time() - self.performance_stats['start_time']
        
        # 计算缓存命中率
        cache_hit_rate = (
            (self.query_cache.cache.get_hit_rate() + self.document_cache.cache.get_hit_rate()) / 2
        )
        
        # 计算平均时间
        avg_retrieval_time = (
            self.performance_stats['total_retrieval_time'] / max(total_queries, 1)
        )
        avg_generation_time = (
            self.performance_stats['total_generation_time'] / max(total_queries, 1)
        )
        
        # 估算内存使用
        memory_usage_mb = (
            (self.query_cache.cache.current_memory + self.document_cache.cache.current_memory) 
            / (1024 * 1024)
        )
        
        return PerformanceMetrics(
            cache_hit_rate=cache_hit_rate,
            avg_retrieval_time=avg_retrieval_time,
            avg_generation_time=avg_generation_time,
            memory_usage_mb=memory_usage_mb,
            total_queries=total_queries
        )
    
    def clear_caches(self):
        """清空所有缓存"""
        self.query_cache.cache.clear()
        self.document_cache.cache.clear()
        logger.info("所有缓存已清空")
    
    def get_cache_statistics(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        return {
            'query_cache': {
                'size': len(self.query_cache.cache.cache),
                'hit_rate': self.query_cache.cache.get_hit_rate(),
                'memory_mb': self.query_cache.cache.current_memory / (1024 * 1024)
            },
            'document_cache': {
                'size': len(self.document_cache.cache.cache),
                'hit_rate': self.document_cache.cache.get_hit_rate(),
                'memory_mb': self.document_cache.cache.current_memory / (1024 * 1024)
            },
            'precomputed_embeddings': len(self.document_cache.precomputed_embeddings)
        }
