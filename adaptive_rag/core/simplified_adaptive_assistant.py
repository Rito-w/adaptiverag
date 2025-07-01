#!/usr/bin/env python3
"""
=== 简化版自适应助手 ===

立即可用的版本，不依赖训练数据
重点展示框架完整性和工程价值
"""

import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class QueryFeatures:
    """查询特征"""
    complexity_score: float
    entity_count: int
    token_count: int
    question_type: str
    has_comparison: bool
    has_temporal: bool


@dataclass
class PerformanceRecord:
    """性能记录"""
    query: str
    strategy: Dict[str, float]
    accuracy: float
    latency: float
    timestamp: float


class SimplifiedQueryAnalyzer:
    """简化的查询分析器"""
    
    def __init__(self):
        self.question_patterns = {
            'factual': ['what', 'who', 'where', 'when'],
            'reasoning': ['why', 'how', 'explain'],
            'comparison': ['compare', 'versus', 'difference', 'better'],
            'enumeration': ['list', 'enumerate', 'name']
        }
    
    def analyze_query(self, query: str) -> QueryFeatures:
        """分析查询特征"""
        tokens = query.lower().split()
        
        # 计算复杂度
        complexity = min(len(tokens) / 20.0, 1.0)  # 基于长度
        
        # 实体计数（简化：大写开头的词）
        entities = sum(1 for word in query.split() if word[0].isupper())
        
        # 问题类型识别
        question_type = 'general'
        for qtype, patterns in self.question_patterns.items():
            if any(pattern in query.lower() for pattern in patterns):
                question_type = qtype
                break
        
        # 特殊模式检测
        has_comparison = any(word in query.lower() for word in ['compare', 'versus', 'vs'])
        has_temporal = any(word in query.lower() for word in ['when', 'before', 'after'])
        
        return QueryFeatures(
            complexity_score=complexity,
            entity_count=entities,
            token_count=len(tokens),
            question_type=question_type,
            has_comparison=has_comparison,
            has_temporal=has_temporal
        )


class RuleBasedStrategySelector:
    """基于规则的策略选择器"""
    
    def __init__(self):
        # 预定义策略模板
        self.strategy_templates = {
            'factual': {'keyword': 0.7, 'dense': 0.2, 'web': 0.1},
            'reasoning': {'keyword': 0.3, 'dense': 0.6, 'web': 0.1},
            'comparison': {'keyword': 0.4, 'dense': 0.4, 'web': 0.2},
            'enumeration': {'keyword': 0.6, 'dense': 0.3, 'web': 0.1},
            'general': {'keyword': 0.4, 'dense': 0.4, 'web': 0.2}
        }
        
        # 性能历史（用于未来的学习）
        self.performance_history: List[PerformanceRecord] = []
    
    def select_strategy(self, query_features: QueryFeatures) -> Dict[str, float]:
        """选择检索策略"""
        # 基础策略
        base_strategy = self.strategy_templates.get(
            query_features.question_type, 
            self.strategy_templates['general']
        ).copy()
        
        # 根据特征调整
        if query_features.complexity_score > 0.7:
            # 复杂查询增加语义检索
            base_strategy['dense'] += 0.1
            base_strategy['keyword'] -= 0.05
            base_strategy['web'] -= 0.05
        
        if query_features.entity_count > 3:
            # 多实体查询增加关键词检索
            base_strategy['keyword'] += 0.1
            base_strategy['dense'] -= 0.05
            base_strategy['web'] -= 0.05
        
        if query_features.has_comparison:
            # 比较查询需要更多样化的信息
            base_strategy['web'] += 0.1
            base_strategy['keyword'] -= 0.05
            base_strategy['dense'] -= 0.05
        
        # 归一化
        total = sum(base_strategy.values())
        for key in base_strategy:
            base_strategy[key] /= total
        
        return base_strategy
    
    def record_performance(self, query: str, strategy: Dict[str, float], 
                          accuracy: float, latency: float):
        """记录性能（为未来学习做准备）"""
        record = PerformanceRecord(
            query=query,
            strategy=strategy,
            accuracy=accuracy,
            latency=latency,
            timestamp=time.time()
        )
        self.performance_history.append(record)
        
        # 保持历史记录在合理范围内
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]


class SimplePerformanceOptimizer:
    """简化的性能优化器"""
    
    def __init__(self, cache_size: int = 100):
        self.query_cache = {}
        self.cache_size = cache_size
        self.cache_hits = 0
        self.total_queries = 0
    
    def get_cached_result(self, query: str) -> Optional[Any]:
        """获取缓存结果"""
        self.total_queries += 1
        if query in self.query_cache:
            self.cache_hits += 1
            return self.query_cache[query]
        return None
    
    def cache_result(self, query: str, result: Any):
        """缓存结果"""
        if len(self.query_cache) >= self.cache_size:
            # 简单的FIFO清理
            oldest_key = next(iter(self.query_cache))
            del self.query_cache[oldest_key]
        
        self.query_cache[query] = result
    
    def get_cache_hit_rate(self) -> float:
        """获取缓存命中率"""
        return self.cache_hits / max(self.total_queries, 1)


class SimplifiedAdaptiveAssistant:
    """简化版自适应助手 - 立即可用"""
    
    def __init__(self, config):
        self.config = config
        
        # 初始化组件
        self.query_analyzer = SimplifiedQueryAnalyzer()
        self.strategy_selector = RuleBasedStrategySelector()
        self.performance_optimizer = SimplePerformanceOptimizer()
        
        # 统计信息
        self.query_count = 0
        self.total_processing_time = 0.0
        self.strategy_usage = defaultdict(int)
        
        logger.info("SimplifiedAdaptiveAssistant 初始化完成")
    
    def answer(self, query: str, **kwargs) -> Dict[str, Any]:
        """主要的问答方法"""
        start_time = time.time()
        self.query_count += 1
        
        logger.info(f"处理查询: {query}")
        
        # 1. 检查缓存
        cached_result = self.performance_optimizer.get_cached_result(query)
        if cached_result:
            logger.info("缓存命中")
            return cached_result
        
        # 2. 查询分析
        query_features = self.query_analyzer.analyze_query(query)
        logger.info(f"查询特征: 类型={query_features.question_type}, "
                   f"复杂度={query_features.complexity_score:.3f}")
        
        # 3. 策略选择
        strategy = self.strategy_selector.select_strategy(query_features)
        logger.info(f"选择策略: {strategy}")
        
        # 记录策略使用
        strategy_key = f"{query_features.question_type}_{max(strategy, key=strategy.get)}"
        self.strategy_usage[strategy_key] += 1
        
        # 4. 模拟检索和生成（实际应用中替换为真实实现）
        retrieved_docs = self._mock_retrieval(query, strategy)
        answer = self._mock_generation(query, retrieved_docs)
        
        # 5. 性能记录
        processing_time = time.time() - start_time
        self.total_processing_time += processing_time
        
        # 模拟准确性评分（实际应用中需要真实评估）
        mock_accuracy = 0.8  # 占位符
        
        self.strategy_selector.record_performance(
            query, strategy, mock_accuracy, processing_time
        )
        
        # 6. 构建结果
        result = {
            'query': query,
            'answer': answer,
            'strategy': strategy,
            'query_features': query_features.__dict__,
            'processing_time': processing_time,
            'retrieved_docs_count': len(retrieved_docs),
            'cache_hit': False
        }
        
        # 7. 缓存结果
        self.performance_optimizer.cache_result(query, result)
        
        logger.info(f"查询处理完成，耗时: {processing_time:.3f}s")
        return result
    
    def _mock_retrieval(self, query: str, strategy: Dict[str, float]) -> List[str]:
        """模拟检索过程"""
        # 根据策略权重模拟不同的检索时间
        retrieval_time = (
            strategy['keyword'] * 0.1 +
            strategy['dense'] * 0.3 +
            strategy['web'] * 0.5
        )
        time.sleep(retrieval_time)
        
        # 返回模拟文档
        return [f"Document {i} for query: {query[:30]}..." for i in range(5)]
    
    def _mock_generation(self, query: str, docs: List[str]) -> str:
        """模拟生成过程"""
        time.sleep(0.2)  # 模拟生成时间
        return f"Simplified adaptive answer for: {query[:50]}... (using {len(docs)} documents)"
    
    def get_analytics(self) -> Dict[str, Any]:
        """获取分析数据"""
        return {
            'query_count': self.query_count,
            'avg_processing_time': self.total_processing_time / max(self.query_count, 1),
            'cache_hit_rate': self.performance_optimizer.get_cache_hit_rate(),
            'strategy_usage': dict(self.strategy_usage),
            'performance_history_size': len(self.strategy_selector.performance_history),
            'total_processing_time': self.total_processing_time
        }
    
    def export_training_data(self) -> List[Dict[str, Any]]:
        """导出训练数据（为未来ML训练做准备）"""
        training_data = []
        for record in self.strategy_selector.performance_history:
            # 重新分析查询特征
            features = self.query_analyzer.analyze_query(record.query)
            
            training_data.append({
                'query': record.query,
                'query_features': features.__dict__,
                'strategy': record.strategy,
                'accuracy': record.accuracy,
                'latency': record.latency,
                'timestamp': record.timestamp
            })
        
        return training_data
    
    def get_strategy_effectiveness(self) -> Dict[str, Dict[str, float]]:
        """分析策略有效性"""
        strategy_stats = defaultdict(lambda: {'count': 0, 'avg_accuracy': 0.0, 'avg_latency': 0.0})
        
        for record in self.strategy_selector.performance_history:
            # 简化的策略标识
            dominant_retriever = max(record.strategy, key=record.strategy.get)
            key = f"{dominant_retriever}_dominant"
            
            stats = strategy_stats[key]
            stats['count'] += 1
            stats['avg_accuracy'] = (stats['avg_accuracy'] * (stats['count'] - 1) + record.accuracy) / stats['count']
            stats['avg_latency'] = (stats['avg_latency'] * (stats['count'] - 1) + record.latency) / stats['count']
        
        return dict(strategy_stats)
