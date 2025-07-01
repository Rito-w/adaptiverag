#!/usr/bin/env python3
"""
=== 多维度决策优化器 ===

同时考虑准确性、延迟、成本、用户满意度等多个维度
这是我们相对于其他方法的核心差异化优势
"""

import logging
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import time

logger = logging.getLogger(__name__)


class OptimizationObjective(Enum):
    """优化目标"""
    ACCURACY = "accuracy"           # 准确性优先
    SPEED = "speed"                # 速度优先  
    COST = "cost"                  # 成本优先
    BALANCED = "balanced"          # 平衡优化
    USER_SATISFACTION = "satisfaction"  # 用户满意度优先


@dataclass
class ResourceConstraints:
    """资源约束"""
    max_latency_ms: float = 5000.0      # 最大延迟(毫秒)
    max_cost_per_query: float = 0.1     # 每查询最大成本
    max_memory_mb: float = 1000.0       # 最大内存使用
    max_api_calls: int = 10             # 最大API调用次数


@dataclass
class PerformanceDimensions:
    """性能维度"""
    accuracy: float = 0.0               # 准确性 [0-1]
    latency_ms: float = 0.0            # 延迟(毫秒)
    cost: float = 0.0                  # 成本
    memory_mb: float = 0.0             # 内存使用
    user_satisfaction: float = 0.0      # 用户满意度 [0-1]
    api_calls: int = 0                 # API调用次数


@dataclass
class StrategyOption:
    """策略选项"""
    name: str
    config: Dict[str, Any]
    predicted_performance: PerformanceDimensions
    feasible: bool = True              # 是否满足约束条件


class MultiDimensionalOptimizer:
    """多维度决策优化器"""
    
    def __init__(self, config):
        self.config = config
        
        # 默认权重配置
        self.objective_weights = {
            OptimizationObjective.ACCURACY: {
                'accuracy': 0.6, 'latency': 0.1, 'cost': 0.1, 
                'memory': 0.1, 'satisfaction': 0.1
            },
            OptimizationObjective.SPEED: {
                'accuracy': 0.2, 'latency': 0.5, 'cost': 0.1, 
                'memory': 0.1, 'satisfaction': 0.1
            },
            OptimizationObjective.COST: {
                'accuracy': 0.2, 'latency': 0.1, 'cost': 0.5, 
                'memory': 0.1, 'satisfaction': 0.1
            },
            OptimizationObjective.BALANCED: {
                'accuracy': 0.3, 'latency': 0.2, 'cost': 0.2, 
                'memory': 0.1, 'satisfaction': 0.2
            },
            OptimizationObjective.USER_SATISFACTION: {
                'accuracy': 0.2, 'latency': 0.2, 'cost': 0.1, 
                'memory': 0.1, 'satisfaction': 0.4
            }
        }
        
        # 性能预测模型 (简化版，可以后续用ML替换)
        self.performance_models = self._initialize_performance_models()
        
        logger.info("MultiDimensionalOptimizer 初始化完成")
    
    def optimize_strategy(self, 
                         query_features: Dict[str, Any],
                         available_strategies: List[Dict[str, Any]],
                         objective: OptimizationObjective = OptimizationObjective.BALANCED,
                         constraints: Optional[ResourceConstraints] = None) -> StrategyOption:
        """
        多维度策略优化
        
        Args:
            query_features: 查询特征
            available_strategies: 可用策略列表
            objective: 优化目标
            constraints: 资源约束
            
        Returns:
            StrategyOption: 最优策略选项
        """
        if constraints is None:
            constraints = ResourceConstraints()
        
        # 1. 为每个策略预测性能
        strategy_options = []
        for i, strategy in enumerate(available_strategies):
            predicted_perf = self._predict_performance(query_features, strategy)
            
            option = StrategyOption(
                name=f"strategy_{i}",
                config=strategy,
                predicted_performance=predicted_perf,
                feasible=self._check_feasibility(predicted_perf, constraints)
            )
            strategy_options.append(option)
        
        # 2. 过滤不可行的策略
        feasible_options = [opt for opt in strategy_options if opt.feasible]
        if not feasible_options:
            logger.warning("没有可行的策略，使用最佳不可行策略")
            feasible_options = strategy_options
        
        # 3. 多目标优化
        optimal_strategy = self._multi_objective_optimization(
            feasible_options, objective, constraints
        )
        
        logger.info(f"选择策略: {optimal_strategy.name}, 目标: {objective.value}")
        return optimal_strategy
    
    def _predict_performance(self, query_features: Dict[str, Any], 
                           strategy: Dict[str, Any]) -> PerformanceDimensions:
        """预测策略性能"""
        # 简化的性能预测模型
        # 实际应用中可以用训练好的ML模型替换
        
        complexity = query_features.get('complexity_score', 0.5)
        token_count = query_features.get('token_count', 10)
        
        # 基于策略权重预测性能
        keyword_weight = strategy.get('keyword', 0.0)
        dense_weight = strategy.get('dense', 0.0)
        web_weight = strategy.get('web', 0.0)
        
        # 准确性预测
        accuracy = self._predict_accuracy(complexity, keyword_weight, dense_weight, web_weight)
        
        # 延迟预测
        latency_ms = self._predict_latency(token_count, keyword_weight, dense_weight, web_weight)
        
        # 成本预测
        cost = self._predict_cost(keyword_weight, dense_weight, web_weight)
        
        # 内存预测
        memory_mb = self._predict_memory(token_count, dense_weight)
        
        # 用户满意度预测 (基于准确性和延迟)
        satisfaction = self._predict_satisfaction(accuracy, latency_ms)
        
        # API调用次数预测
        api_calls = self._predict_api_calls(keyword_weight, dense_weight, web_weight)
        
        return PerformanceDimensions(
            accuracy=accuracy,
            latency_ms=latency_ms,
            cost=cost,
            memory_mb=memory_mb,
            user_satisfaction=satisfaction,
            api_calls=api_calls
        )
    
    def _predict_accuracy(self, complexity: float, kw_weight: float, 
                         dense_weight: float, web_weight: float) -> float:
        """预测准确性"""
        # 基于复杂度和检索器权重的简化模型
        base_accuracy = 0.7
        
        # 复杂查询更适合dense检索
        if complexity > 0.7:
            accuracy_boost = dense_weight * 0.2
        else:
            accuracy_boost = kw_weight * 0.15
        
        # Web检索对某些查询有帮助
        web_boost = web_weight * 0.1
        
        return min(base_accuracy + accuracy_boost + web_boost, 1.0)
    
    def _predict_latency(self, token_count: int, kw_weight: float, 
                        dense_weight: float, web_weight: float) -> float:
        """预测延迟"""
        # 基础延迟
        base_latency = 500.0  # 500ms
        
        # 不同检索器的延迟特征
        kw_latency = kw_weight * 200.0      # 关键词检索较快
        dense_latency = dense_weight * 800.0  # 向量检索较慢
        web_latency = web_weight * 1500.0    # Web检索最慢
        
        # token数量影响
        token_factor = min(token_count / 50.0, 2.0)
        
        total_latency = (base_latency + kw_latency + dense_latency + web_latency) * token_factor
        return total_latency
    
    def _predict_cost(self, kw_weight: float, dense_weight: float, web_weight: float) -> float:
        """预测成本"""
        # 不同检索器的成本
        kw_cost = kw_weight * 0.01      # 关键词检索成本低
        dense_cost = dense_weight * 0.03  # 向量检索成本中等
        web_cost = web_weight * 0.05     # Web检索成本高
        
        return kw_cost + dense_cost + web_cost
    
    def _predict_memory(self, token_count: int, dense_weight: float) -> float:
        """预测内存使用"""
        base_memory = 50.0  # 50MB基础内存
        
        # 向量检索需要更多内存
        dense_memory = dense_weight * token_count * 2.0
        
        return base_memory + dense_memory
    
    def _predict_satisfaction(self, accuracy: float, latency_ms: float) -> float:
        """预测用户满意度"""
        # 基于准确性和延迟的满意度模型
        accuracy_factor = accuracy
        
        # 延迟惩罚
        if latency_ms < 1000:
            latency_factor = 1.0
        elif latency_ms < 3000:
            latency_factor = 0.8
        elif latency_ms < 5000:
            latency_factor = 0.6
        else:
            latency_factor = 0.3
        
        return accuracy_factor * latency_factor
    
    def _predict_api_calls(self, kw_weight: float, dense_weight: float, web_weight: float) -> int:
        """预测API调用次数"""
        calls = 0
        
        if kw_weight > 0:
            calls += 1
        if dense_weight > 0:
            calls += 2  # 向量检索可能需要多次调用
        if web_weight > 0:
            calls += 3  # Web检索通常需要多次调用
        
        return calls
    
    def _check_feasibility(self, performance: PerformanceDimensions, 
                          constraints: ResourceConstraints) -> bool:
        """检查策略是否满足约束条件"""
        if performance.latency_ms > constraints.max_latency_ms:
            return False
        if performance.cost > constraints.max_cost_per_query:
            return False
        if performance.memory_mb > constraints.max_memory_mb:
            return False
        if performance.api_calls > constraints.max_api_calls:
            return False
        
        return True
    
    def _multi_objective_optimization(self, options: List[StrategyOption], 
                                    objective: OptimizationObjective,
                                    constraints: ResourceConstraints) -> StrategyOption:
        """多目标优化"""
        weights = self.objective_weights[objective]
        
        best_option = None
        best_score = -float('inf')
        
        for option in options:
            perf = option.predicted_performance
            
            # 归一化性能指标
            normalized_accuracy = perf.accuracy
            normalized_latency = max(0, 1 - perf.latency_ms / 10000.0)  # 10秒为最大延迟
            normalized_cost = max(0, 1 - perf.cost / 1.0)  # 1.0为最大成本
            normalized_memory = max(0, 1 - perf.memory_mb / 2000.0)  # 2GB为最大内存
            normalized_satisfaction = perf.user_satisfaction
            
            # 计算加权评分
            score = (
                weights['accuracy'] * normalized_accuracy +
                weights['latency'] * normalized_latency +
                weights['cost'] * normalized_cost +
                weights['memory'] * normalized_memory +
                weights['satisfaction'] * normalized_satisfaction
            )
            
            # 约束惩罚
            if not option.feasible:
                score *= 0.5  # 不可行策略评分减半
            
            if score > best_score:
                best_score = score
                best_option = option
        
        return best_option if best_option else options[0]
    
    def _initialize_performance_models(self) -> Dict[str, Any]:
        """初始化性能预测模型"""
        # 这里可以加载预训练的ML模型
        # 目前使用简化的启发式模型
        return {
            'accuracy_model': None,
            'latency_model': None,
            'cost_model': None,
            'memory_model': None
        }
    
    def update_objective_weights(self, objective: OptimizationObjective, 
                               new_weights: Dict[str, float]):
        """更新目标权重"""
        # 确保权重和为1
        total = sum(new_weights.values())
        normalized_weights = {k: v/total for k, v in new_weights.items()}
        
        self.objective_weights[objective] = normalized_weights
        logger.info(f"更新 {objective.value} 目标权重: {normalized_weights}")
    
    def analyze_tradeoffs(self, options: List[StrategyOption]) -> Dict[str, Any]:
        """分析策略权衡"""
        if not options:
            return {}
        
        # 计算各维度的统计信息
        accuracies = [opt.predicted_performance.accuracy for opt in options]
        latencies = [opt.predicted_performance.latency_ms for opt in options]
        costs = [opt.predicted_performance.cost for opt in options]
        satisfactions = [opt.predicted_performance.user_satisfaction for opt in options]
        
        return {
            'accuracy_range': (min(accuracies), max(accuracies)),
            'latency_range': (min(latencies), max(latencies)),
            'cost_range': (min(costs), max(costs)),
            'satisfaction_range': (min(satisfactions), max(satisfactions)),
            'pareto_efficient': self._find_pareto_efficient(options)
        }
    
    def _find_pareto_efficient(self, options: List[StrategyOption]) -> List[str]:
        """找到帕累托有效的策略"""
        # 简化的帕累托效率分析
        efficient_options = []
        
        for i, option1 in enumerate(options):
            is_dominated = False
            
            for j, option2 in enumerate(options):
                if i != j and self._dominates(option2, option1):
                    is_dominated = True
                    break
            
            if not is_dominated:
                efficient_options.append(option1.name)
        
        return efficient_options
    
    def _dominates(self, option1: StrategyOption, option2: StrategyOption) -> bool:
        """检查option1是否支配option2"""
        perf1 = option1.predicted_performance
        perf2 = option2.predicted_performance
        
        # option1在所有维度上都不差于option2，且至少在一个维度上更好
        better_accuracy = perf1.accuracy >= perf2.accuracy
        better_latency = perf1.latency_ms <= perf2.latency_ms
        better_cost = perf1.cost <= perf2.cost
        better_satisfaction = perf1.user_satisfaction >= perf2.user_satisfaction
        
        all_better_or_equal = better_accuracy and better_latency and better_cost and better_satisfaction
        
        at_least_one_better = (
            perf1.accuracy > perf2.accuracy or
            perf1.latency_ms < perf2.latency_ms or
            perf1.cost < perf2.cost or
            perf1.user_satisfaction > perf2.user_satisfaction
        )
        
        return all_better_or_equal and at_least_one_better
