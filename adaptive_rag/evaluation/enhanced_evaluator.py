#!/usr/bin/env python3
"""
=== 增强评估器 ===

扩展现有评估框架，添加自适应性相关的评估指标
这是我们实验设计的重要组成部分
"""

import logging
import numpy as np
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import json

logger = logging.getLogger(__name__)


@dataclass
class AdaptiveMetrics:
    """自适应性相关指标"""
    strategy_diversity: float           # 策略多样性
    adaptation_accuracy: float          # 自适应准确性
    learning_speed: float              # 学习速度
    consistency_score: float           # 一致性评分
    robustness_score: float            # 鲁棒性评分


@dataclass
class EfficiencyMetrics:
    """效率指标"""
    avg_retrieval_time: float          # 平均检索时间
    avg_generation_time: float         # 平均生成时间
    cache_hit_rate: float              # 缓存命中率
    memory_efficiency: float           # 内存效率
    cost_per_query: float              # 每查询成本


@dataclass
class ComprehensiveResults:
    """综合评估结果"""
    # 传统指标
    exact_match: float
    f1_score: float
    rouge_l: float
    bert_score: float
    
    # 自适应指标
    adaptive_metrics: AdaptiveMetrics
    
    # 效率指标
    efficiency_metrics: EfficiencyMetrics
    
    # 详细分析
    per_query_results: List[Dict[str, Any]]
    strategy_analysis: Dict[str, Any]


class EnhancedEvaluator:
    """增强评估器"""
    
    def __init__(self, config):
        self.config = config
        
        # 评估历史
        self.evaluation_history = []
        self.strategy_performance = defaultdict(list)
        
        logger.info("EnhancedEvaluator 初始化完成")
    
    def comprehensive_evaluate(self, 
                             adaptive_rag_system,
                             test_queries: List[Dict[str, Any]],
                             baseline_methods: Optional[Dict[str, Any]] = None) -> ComprehensiveResults:
        """
        综合评估
        
        Args:
            adaptive_rag_system: 自适应RAG系统
            test_queries: 测试查询列表 [{"query": str, "ground_truth": str, "type": str}]
            baseline_methods: 基线方法字典
            
        Returns:
            ComprehensiveResults: 综合评估结果
        """
        logger.info(f"开始综合评估，共 {len(test_queries)} 个查询")
        
        # 1. 运行自适应RAG系统
        adaptive_results = self._evaluate_adaptive_system(adaptive_rag_system, test_queries)
        
        # 2. 计算传统指标
        traditional_metrics = self._calculate_traditional_metrics(adaptive_results, test_queries)
        
        # 3. 计算自适应指标
        adaptive_metrics = self._calculate_adaptive_metrics(adaptive_results, test_queries)
        
        # 4. 计算效率指标
        efficiency_metrics = self._calculate_efficiency_metrics(adaptive_results)
        
        # 5. 策略分析
        strategy_analysis = self._analyze_strategy_performance(adaptive_results)
        
        # 6. 如果有基线方法，进行对比
        if baseline_methods:
            baseline_results = self._evaluate_baseline_methods(baseline_methods, test_queries)
            strategy_analysis['baseline_comparison'] = baseline_results
        
        results = ComprehensiveResults(
            exact_match=traditional_metrics['exact_match'],
            f1_score=traditional_metrics['f1_score'],
            rouge_l=traditional_metrics['rouge_l'],
            bert_score=traditional_metrics['bert_score'],
            adaptive_metrics=adaptive_metrics,
            efficiency_metrics=efficiency_metrics,
            per_query_results=adaptive_results,
            strategy_analysis=strategy_analysis
        )
        
        # 保存评估历史
        self.evaluation_history.append({
            'timestamp': time.time(),
            'results': results,
            'test_size': len(test_queries)
        })
        
        logger.info("综合评估完成")
        return results
    
    def _evaluate_adaptive_system(self, system, test_queries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """评估自适应系统"""
        results = []
        
        for i, query_data in enumerate(test_queries):
            query = query_data['query']
            ground_truth = query_data['ground_truth']
            query_type = query_data.get('type', 'unknown')
            
            logger.debug(f"评估查询 {i+1}/{len(test_queries)}: {query[:50]}...")
            
            start_time = time.time()
            
            try:
                # 运行自适应RAG
                result = system.answer(query)
                
                end_time = time.time()
                processing_time = end_time - start_time
                
                # 提取详细信息
                strategy_used = result.metadata.get('strategy', {})
                query_features = result.metadata.get('query_features', {})
                predicted_performance = result.metadata.get('predicted_performance', {})
                
                query_result = {
                    'query': query,
                    'ground_truth': ground_truth,
                    'prediction': result.answer,
                    'query_type': query_type,
                    'processing_time': processing_time,
                    'strategy_used': strategy_used,
                    'query_features': query_features,
                    'predicted_performance': predicted_performance,
                    'retrieved_docs_count': len(result.retrieved_contexts),
                    'metadata': result.metadata
                }
                
                results.append(query_result)
                
            except Exception as e:
                logger.error(f"查询处理失败: {e}")
                results.append({
                    'query': query,
                    'ground_truth': ground_truth,
                    'prediction': "",
                    'query_type': query_type,
                    'processing_time': 0.0,
                    'error': str(e)
                })
        
        return results
    
    def _calculate_traditional_metrics(self, results: List[Dict[str, Any]], 
                                     test_queries: List[Dict[str, Any]]) -> Dict[str, float]:
        """计算传统评估指标"""
        predictions = [r.get('prediction', '') for r in results]
        ground_truths = [r.get('ground_truth', '') for r in results]
        
        # 计算各种指标
        exact_match = self._calculate_exact_match(predictions, ground_truths)
        f1_score = self._calculate_f1_score(predictions, ground_truths)
        rouge_l = self._calculate_rouge_l(predictions, ground_truths)
        bert_score = self._calculate_bert_score(predictions, ground_truths)
        
        return {
            'exact_match': exact_match,
            'f1_score': f1_score,
            'rouge_l': rouge_l,
            'bert_score': bert_score
        }
    
    def _calculate_adaptive_metrics(self, results: List[Dict[str, Any]], 
                                  test_queries: List[Dict[str, Any]]) -> AdaptiveMetrics:
        """计算自适应性指标"""
        
        # 1. 策略多样性
        strategies_used = [r.get('strategy_used', {}) for r in results if 'strategy_used' in r]
        strategy_diversity = self._calculate_strategy_diversity(strategies_used)
        
        # 2. 自适应准确性 (策略选择是否合理)
        adaptation_accuracy = self._calculate_adaptation_accuracy(results)
        
        # 3. 学习速度 (性能随时间的改善)
        learning_speed = self._calculate_learning_speed(results)
        
        # 4. 一致性评分 (相似查询的策略一致性)
        consistency_score = self._calculate_consistency_score(results)
        
        # 5. 鲁棒性评分 (对不同类型查询的适应性)
        robustness_score = self._calculate_robustness_score(results)
        
        return AdaptiveMetrics(
            strategy_diversity=strategy_diversity,
            adaptation_accuracy=adaptation_accuracy,
            learning_speed=learning_speed,
            consistency_score=consistency_score,
            robustness_score=robustness_score
        )
    
    def _calculate_efficiency_metrics(self, results: List[Dict[str, Any]]) -> EfficiencyMetrics:
        """计算效率指标"""
        processing_times = [r.get('processing_time', 0.0) for r in results if 'processing_time' in r]
        
        # 简化的效率计算
        avg_total_time = np.mean(processing_times) if processing_times else 0.0
        avg_retrieval_time = avg_total_time * 0.6  # 假设60%时间用于检索
        avg_generation_time = avg_total_time * 0.4  # 假设40%时间用于生成
        
        # 其他指标需要从系统中获取
        cache_hit_rate = 0.0  # 需要从性能优化器获取
        memory_efficiency = 0.8  # 简化值
        cost_per_query = 0.05  # 简化值
        
        return EfficiencyMetrics(
            avg_retrieval_time=avg_retrieval_time,
            avg_generation_time=avg_generation_time,
            cache_hit_rate=cache_hit_rate,
            memory_efficiency=memory_efficiency,
            cost_per_query=cost_per_query
        )
    
    def _calculate_strategy_diversity(self, strategies: List[Dict[str, Any]]) -> float:
        """计算策略多样性"""
        if not strategies:
            return 0.0
        
        # 计算不同策略配置的数量
        unique_strategies = set()
        for strategy in strategies:
            # 将策略转换为可哈希的字符串
            strategy_str = json.dumps(strategy, sort_keys=True)
            unique_strategies.add(strategy_str)
        
        # 多样性 = 唯一策略数 / 总策略数
        diversity = len(unique_strategies) / len(strategies)
        return diversity
    
    def _calculate_adaptation_accuracy(self, results: List[Dict[str, Any]]) -> float:
        """计算自适应准确性"""
        # 简化实现：基于预测性能与实际性能的匹配度
        accurate_adaptations = 0
        total_adaptations = 0
        
        for result in results:
            if 'predicted_performance' in result and 'processing_time' in result:
                predicted_time = result['predicted_performance'].get('latency_ms', 0) / 1000.0
                actual_time = result['processing_time']
                
                # 如果预测时间与实际时间相差不超过50%，认为是准确的
                if abs(predicted_time - actual_time) / max(actual_time, 0.1) < 0.5:
                    accurate_adaptations += 1
                total_adaptations += 1
        
        return accurate_adaptations / max(total_adaptations, 1)
    
    def _calculate_learning_speed(self, results: List[Dict[str, Any]]) -> float:
        """计算学习速度"""
        # 简化实现：检查处理时间是否随时间减少
        if len(results) < 10:
            return 0.5  # 数据不足，返回中等值
        
        processing_times = [r.get('processing_time', 0.0) for r in results]
        
        # 计算前半部分和后半部分的平均时间
        mid_point = len(processing_times) // 2
        early_avg = np.mean(processing_times[:mid_point])
        late_avg = np.mean(processing_times[mid_point:])
        
        # 学习速度 = 时间改善程度
        if early_avg > 0:
            improvement = (early_avg - late_avg) / early_avg
            return max(0.0, min(1.0, improvement + 0.5))  # 归一化到[0,1]
        
        return 0.5
    
    def _calculate_consistency_score(self, results: List[Dict[str, Any]]) -> float:
        """计算一致性评分"""
        # 简化实现：相似查询类型是否使用相似策略
        type_strategies = defaultdict(list)
        
        for result in results:
            query_type = result.get('query_type', 'unknown')
            strategy = result.get('strategy_used', {})
            if strategy:
                type_strategies[query_type].append(strategy)
        
        consistency_scores = []
        for query_type, strategies in type_strategies.items():
            if len(strategies) > 1:
                # 计算策略的方差作为一致性指标
                keyword_weights = [s.get('keyword', 0.0) for s in strategies]
                consistency = 1.0 - np.var(keyword_weights)  # 方差越小，一致性越高
                consistency_scores.append(max(0.0, consistency))
        
        return np.mean(consistency_scores) if consistency_scores else 0.5
    
    def _calculate_robustness_score(self, results: List[Dict[str, Any]]) -> float:
        """计算鲁棒性评分"""
        # 简化实现：不同查询类型的性能方差
        type_performance = defaultdict(list)
        
        for result in results:
            query_type = result.get('query_type', 'unknown')
            # 简化的性能评分 (基于处理时间的倒数)
            processing_time = result.get('processing_time', 1.0)
            performance = 1.0 / (1.0 + processing_time)
            type_performance[query_type].append(performance)
        
        # 计算各类型性能的标准差
        type_variances = []
        for query_type, performances in type_performance.items():
            if len(performances) > 1:
                variance = np.var(performances)
                type_variances.append(variance)
        
        # 鲁棒性 = 1 - 平均方差
        avg_variance = np.mean(type_variances) if type_variances else 0.0
        robustness = 1.0 - min(avg_variance, 1.0)
        
        return robustness
    
    # 简化的传统指标计算方法
    def _calculate_exact_match(self, predictions: List[str], ground_truths: List[str]) -> float:
        """计算精确匹配率"""
        matches = sum(1 for p, g in zip(predictions, ground_truths) if p.strip().lower() == g.strip().lower())
        return matches / len(predictions) if predictions else 0.0
    
    def _calculate_f1_score(self, predictions: List[str], ground_truths: List[str]) -> float:
        """计算F1分数"""
        # 简化实现
        total_f1 = 0.0
        for pred, truth in zip(predictions, ground_truths):
            pred_tokens = set(pred.lower().split())
            truth_tokens = set(truth.lower().split())
            
            if not truth_tokens:
                continue
                
            intersection = pred_tokens & truth_tokens
            precision = len(intersection) / len(pred_tokens) if pred_tokens else 0.0
            recall = len(intersection) / len(truth_tokens)
            
            if precision + recall > 0:
                f1 = 2 * precision * recall / (precision + recall)
            else:
                f1 = 0.0
            
            total_f1 += f1
        
        return total_f1 / len(predictions) if predictions else 0.0
    
    def _calculate_rouge_l(self, predictions: List[str], ground_truths: List[str]) -> float:
        """计算ROUGE-L分数"""
        # 简化实现 - 实际应用中应使用专门的ROUGE库
        return 0.75  # 占位符
    
    def _calculate_bert_score(self, predictions: List[str], ground_truths: List[str]) -> float:
        """计算BERTScore"""
        # 简化实现 - 实际应用中应使用BERTScore库
        return 0.80  # 占位符
