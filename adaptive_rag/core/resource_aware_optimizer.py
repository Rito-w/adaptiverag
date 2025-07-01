#!/usr/bin/env python3
"""
=== 资源感知优化器 ===

实现动态资源监控和自适应策略调整
这是我们在资源管理方面的创新点
"""

import logging
import time
import psutil
import threading
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import json
from collections import deque
import numpy as np

logger = logging.getLogger(__name__)


class ResourceType(Enum):
    """资源类型"""
    CPU = "cpu"
    MEMORY = "memory"
    GPU = "gpu"
    NETWORK = "network"
    STORAGE = "storage"


class OptimizationMode(Enum):
    """优化模式"""
    PERFORMANCE = "performance"      # 性能优先
    EFFICIENCY = "efficiency"        # 效率优先
    BALANCED = "balanced"           # 平衡模式
    CONSERVATIVE = "conservative"    # 保守模式


@dataclass
class ResourceMetrics:
    """资源指标"""
    cpu_usage: float = 0.0           # CPU使用率 [0-100]
    memory_usage: float = 0.0        # 内存使用率 [0-100]
    memory_available: float = 0.0    # 可用内存 (MB)
    gpu_usage: float = 0.0           # GPU使用率 [0-100]
    gpu_memory: float = 0.0          # GPU内存使用 (MB)
    network_io: float = 0.0          # 网络IO (MB/s)
    disk_io: float = 0.0             # 磁盘IO (MB/s)
    timestamp: float = 0.0           # 时间戳


@dataclass
class ResourceThresholds:
    """资源阈值"""
    cpu_warning: float = 80.0        # CPU警告阈值
    cpu_critical: float = 95.0       # CPU临界阈值
    memory_warning: float = 85.0     # 内存警告阈值
    memory_critical: float = 95.0    # 内存临界阈值
    gpu_warning: float = 80.0        # GPU警告阈值
    gpu_critical: float = 95.0       # GPU临界阈值
    network_warning: float = 50.0    # 网络警告阈值 (MB/s)
    disk_warning: float = 100.0      # 磁盘警告阈值 (MB/s)


@dataclass
class OptimizationStrategy:
    """优化策略"""
    name: str
    description: str
    resource_weights: Dict[str, float] = field(default_factory=dict)
    performance_weights: Dict[str, float] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    adaptive_rules: List[Dict[str, Any]] = field(default_factory=list)


class ResourceMonitor:
    """资源监控器"""
    
    def __init__(self, update_interval: float = 1.0):
        self.update_interval = update_interval
        self.metrics_history = deque(maxlen=100)  # 保留最近100个数据点
        self.is_monitoring = False
        self.monitor_thread = None
        self.lock = threading.Lock()
        
        # 初始化阈值
        self.thresholds = ResourceThresholds()
        
        logger.info("ResourceMonitor 初始化完成")
    
    def start_monitoring(self):
        """开始监控"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("资源监控已启动")
    
    def stop_monitoring(self):
        """停止监控"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        logger.info("资源监控已停止")
    
    def _monitor_loop(self):
        """监控循环"""
        while self.is_monitoring:
            try:
                metrics = self._collect_metrics()
                with self.lock:
                    self.metrics_history.append(metrics)
                
                time.sleep(self.update_interval)
            except Exception as e:
                logger.error(f"资源监控错误: {e}")
                time.sleep(self.update_interval)
    
    def _collect_metrics(self) -> ResourceMetrics:
        """收集资源指标"""
        # CPU使用率
        cpu_usage = psutil.cpu_percent(interval=0.1)
        
        # 内存使用情况
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        memory_available = memory.available / (1024 * 1024)  # MB
        
        # GPU使用情况 (如果可用)
        gpu_usage = 0.0
        gpu_memory = 0.0
        try:
            import pynvml
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            gpu_usage = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
            gpu_memory = pynvml.nvmlDeviceGetMemoryInfo(handle).used / (1024 * 1024)  # MB
        except ImportError:
            pass  # pynvml 未安装
        except Exception:
            pass  # GPU监控不可用
        
        # 网络IO
        network_io = 0.0
        try:
            net_io = psutil.net_io_counters()
            network_io = (net_io.bytes_sent + net_io.bytes_recv) / (1024 * 1024)  # MB
        except:
            pass
        
        # 磁盘IO
        disk_io = 0.0
        try:
            disk_io_counters = psutil.disk_io_counters()
            if disk_io_counters is not None:
                disk_io = (disk_io_counters.read_bytes + disk_io_counters.write_bytes) / (1024 * 1024)  # MB
        except Exception:
            pass
        
        return ResourceMetrics(
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            memory_available=memory_available,
            gpu_usage=gpu_usage,
            gpu_memory=gpu_memory,
            network_io=network_io,
            disk_io=disk_io,
            timestamp=time.time()
        )
    
    def get_current_metrics(self) -> ResourceMetrics:
        """获取当前资源指标"""
        with self.lock:
            if self.metrics_history:
                return self.metrics_history[-1]
            return self._collect_metrics()
    
    def get_metrics_history(self, window_seconds: float = 60.0) -> List[ResourceMetrics]:
        """获取历史指标"""
        with self.lock:
            current_time = time.time()
            return [
                metrics for metrics in self.metrics_history
                if current_time - metrics.timestamp <= window_seconds
            ]
    
    def check_resource_status(self) -> Dict[str, str]:
        """检查资源状态"""
        metrics = self.get_current_metrics()
        status = {}
        
        # CPU状态
        if metrics.cpu_usage >= self.thresholds.cpu_critical:
            status['cpu'] = 'critical'
        elif metrics.cpu_usage >= self.thresholds.cpu_warning:
            status['cpu'] = 'warning'
        else:
            status['cpu'] = 'normal'
        
        # 内存状态
        if metrics.memory_usage >= self.thresholds.memory_critical:
            status['memory'] = 'critical'
        elif metrics.memory_usage >= self.thresholds.memory_warning:
            status['memory'] = 'warning'
        else:
            status['memory'] = 'normal'
        
        # GPU状态
        if metrics.gpu_usage >= self.thresholds.gpu_critical:
            status['gpu'] = 'critical'
        elif metrics.gpu_usage >= self.thresholds.gpu_warning:
            status['gpu'] = 'warning'
        else:
            status['gpu'] = 'normal'
        
        return status


class ResourceAwareOptimizer:
    """资源感知优化器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # 初始化资源监控器
        self.resource_monitor = ResourceMonitor(
            update_interval=config.get('monitor_interval', 1.0)
        )
        
        # 优化策略
        self.optimization_strategies = self._initialize_strategies()
        self.current_strategy = self.optimization_strategies['balanced']
        
        # 性能历史
        self.performance_history = deque(maxlen=1000)
        
        # 自适应规则
        self.adaptive_rules = self._initialize_adaptive_rules()
        
        # 启动资源监控
        self.resource_monitor.start_monitoring()
        
        logger.info("ResourceAwareOptimizer 初始化完成")
    
    def _initialize_strategies(self) -> Dict[str, OptimizationStrategy]:
        """初始化优化策略"""
        return {
            'performance': OptimizationStrategy(
                name="性能优先",
                description="最大化系统性能，适合资源充足的情况",
                resource_weights={'cpu': 0.3, 'memory': 0.3, 'gpu': 0.4},
                performance_weights={'accuracy': 0.6, 'speed': 0.4},
                constraints={'max_latency': 2000, 'min_accuracy': 0.8}
            ),
            'efficiency': OptimizationStrategy(
                name="效率优先",
                description="优化资源使用效率，适合资源受限的情况",
                resource_weights={'cpu': 0.4, 'memory': 0.4, 'gpu': 0.2},
                performance_weights={'accuracy': 0.4, 'speed': 0.6},
                constraints={'max_latency': 5000, 'min_accuracy': 0.7}
            ),
            'balanced': OptimizationStrategy(
                name="平衡模式",
                description="在性能和效率之间取得平衡",
                resource_weights={'cpu': 0.33, 'memory': 0.33, 'gpu': 0.34},
                performance_weights={'accuracy': 0.5, 'speed': 0.5},
                constraints={'max_latency': 3000, 'min_accuracy': 0.75}
            ),
            'conservative': OptimizationStrategy(
                name="保守模式",
                description="最小化资源使用，适合高负载情况",
                resource_weights={'cpu': 0.5, 'memory': 0.4, 'gpu': 0.1},
                performance_weights={'accuracy': 0.3, 'speed': 0.7},
                constraints={'max_latency': 8000, 'min_accuracy': 0.6}
            )
        }
    
    def _initialize_adaptive_rules(self) -> List[Dict[str, Any]]:
        """初始化自适应规则"""
        return [
            {
                'condition': lambda metrics: metrics.cpu_usage > 90,
                'action': 'switch_to_conservative',
                'description': 'CPU使用率过高时切换到保守模式'
            },
            {
                'condition': lambda metrics: metrics.memory_usage > 90,
                'action': 'reduce_batch_size',
                'description': '内存使用率过高时减少批次大小'
            },
            {
                'condition': lambda metrics: metrics.gpu_usage > 95,
                'action': 'disable_gpu_acceleration',
                'description': 'GPU使用率过高时禁用GPU加速'
            },
            {
                'condition': lambda metrics: metrics.cpu_usage < 30 and metrics.memory_usage < 50,
                'action': 'switch_to_performance',
                'description': '资源充足时切换到性能模式'
            }
        ]
    
    def optimize_strategy(self, query_features: Dict[str, Any], 
                         available_strategies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """基于资源状态优化策略"""
        # 获取当前资源状态
        resource_status = self.resource_monitor.check_resource_status()
        current_metrics = self.resource_monitor.get_current_metrics()
        
        # 应用自适应规则
        self._apply_adaptive_rules(current_metrics)
        
        # 根据资源状态调整策略权重
        adjusted_strategies = self._adjust_strategies_by_resources(
            available_strategies, resource_status, current_metrics
        )
        
        # 选择最优策略
        optimal_strategy = self._select_optimal_strategy(
            adjusted_strategies, query_features, resource_status
        )
        
        # 记录性能数据
        self._record_performance(query_features, optimal_strategy, current_metrics)
        
        logger.info(f"资源感知优化: 选择策略 {optimal_strategy.get('name', 'unknown')}, "
                   f"资源状态: {resource_status}")
        
        return optimal_strategy
    
    def _apply_adaptive_rules(self, metrics: ResourceMetrics):
        """应用自适应规则"""
        for rule in self.adaptive_rules:
            if rule['condition'](metrics):
                action = rule['action']
                logger.info(f"应用自适应规则: {rule['description']}")
                
                if action == 'switch_to_conservative':
                    self.current_strategy = self.optimization_strategies['conservative']
                elif action == 'switch_to_performance':
                    self.current_strategy = self.optimization_strategies['performance']
                elif action == 'reduce_batch_size':
                    # 减少批次大小
                    pass
                elif action == 'disable_gpu_acceleration':
                    # 禁用GPU加速
                    pass
    
    def _adjust_strategies_by_resources(self, strategies: List[Dict[str, Any]], 
                                      resource_status: Dict[str, str],
                                      metrics: ResourceMetrics) -> List[Dict[str, Any]]:
        """根据资源状态调整策略"""
        adjusted_strategies = []
        
        for strategy in strategies:
            adjusted_strategy = strategy.copy()
            
            # 根据资源状态调整权重
            if resource_status.get('cpu') == 'critical':
                # CPU紧张时减少计算密集型操作
                if 'dense' in adjusted_strategy:
                    adjusted_strategy['dense'] *= 0.5
                if 'web' in adjusted_strategy:
                    adjusted_strategy['web'] *= 0.3
            
            if resource_status.get('memory') == 'critical':
                # 内存紧张时减少内存密集型操作
                if 'dense' in adjusted_strategy:
                    adjusted_strategy['dense'] *= 0.7
                if 'web' in adjusted_strategy:
                    adjusted_strategy['web'] *= 0.5
            
            if resource_status.get('gpu') == 'critical':
                # GPU紧张时减少GPU密集型操作
                if 'dense' in adjusted_strategy:
                    adjusted_strategy['dense'] *= 0.6
            
            # 重新归一化权重
            total_weight = sum(adjusted_strategy.values())
            if total_weight > 0:
                adjusted_strategy = {k: v/total_weight for k, v in adjusted_strategy.items()}
            
            adjusted_strategies.append(adjusted_strategy)
        
        return adjusted_strategies
    
    def _select_optimal_strategy(self, strategies: List[Dict[str, Any]], 
                               query_features: Dict[str, Any],
                               resource_status: Dict[str, str]) -> Dict[str, Any]:
        """选择最优策略"""
        if not strategies:
            return {}
        
        # 计算每个策略的评分
        strategy_scores = []
        for i, strategy in enumerate(strategies):
            score = self._calculate_strategy_score(strategy, query_features, resource_status)
            strategy_scores.append((score, i, strategy))
        
        # 选择评分最高的策略
        strategy_scores.sort(key=lambda x: x[0], reverse=True)
        best_score, best_index, best_strategy = strategy_scores[0]
        
        # 添加策略信息
        best_strategy['name'] = f"resource_optimized_strategy_{best_index}"
        best_strategy['score'] = best_score
        best_strategy['resource_status'] = resource_status
        
        return best_strategy
    
    def _calculate_strategy_score(self, strategy: Dict[str, Any], 
                                query_features: Dict[str, Any],
                                resource_status: Dict[str, str]) -> float:
        """计算策略评分"""
        score = 0.0
        
        # 基础评分 (基于策略权重)
        if 'dense' in strategy:
            score += strategy['dense'] * 0.4  # 语义检索权重
        if 'keyword' in strategy:
            score += strategy['keyword'] * 0.3  # 关键词检索权重
        if 'web' in strategy:
            score += strategy['web'] * 0.3  # Web检索权重
        
        # 资源状态调整
        resource_penalty = 0.0
        if resource_status.get('cpu') == 'critical':
            resource_penalty += 0.3
        elif resource_status.get('cpu') == 'warning':
            resource_penalty += 0.1
        
        if resource_status.get('memory') == 'critical':
            resource_penalty += 0.3
        elif resource_status.get('memory') == 'warning':
            resource_penalty += 0.1
        
        if resource_status.get('gpu') == 'critical':
            resource_penalty += 0.2
        elif resource_status.get('gpu') == 'warning':
            resource_penalty += 0.05
        
        # 应用资源惩罚
        score *= (1.0 - resource_penalty)
        
        # 查询特征调整
        complexity = query_features.get('complexity_score', 0.5)
        if complexity > 0.7 and 'dense' in strategy:
            score += 0.1  # 复杂查询偏好语义检索
        
        return max(0.0, score)
    
    def _record_performance(self, query_features: Dict[str, Any], 
                          strategy: Dict[str, Any], metrics: ResourceMetrics):
        """记录性能数据"""
        performance_data = {
            'timestamp': time.time(),
            'query_features': query_features,
            'strategy': strategy,
            'resource_metrics': {
                'cpu_usage': metrics.cpu_usage,
                'memory_usage': metrics.memory_usage,
                'gpu_usage': metrics.gpu_usage
            }
        }
        
        self.performance_history.append(performance_data)
    
    def get_resource_analytics(self) -> Dict[str, Any]:
        """获取资源分析数据"""
        current_metrics = self.resource_monitor.get_current_metrics()
        resource_status = self.resource_monitor.check_resource_status()
        metrics_history = self.resource_monitor.get_metrics_history(300)  # 最近5分钟
        
        if not metrics_history:
            return {}
        
        # 计算统计信息
        cpu_values = [m.cpu_usage for m in metrics_history]
        memory_values = [m.memory_usage for m in metrics_history]
        gpu_values = [m.gpu_usage for m in metrics_history]
        
        return {
            'current_status': resource_status,
            'current_metrics': {
                'cpu_usage': current_metrics.cpu_usage,
                'memory_usage': current_metrics.memory_usage,
                'memory_available': current_metrics.memory_available,
                'gpu_usage': current_metrics.gpu_usage,
                'gpu_memory': current_metrics.gpu_memory
            },
            'statistics': {
                'cpu_avg': np.mean(cpu_values),
                'cpu_max': np.max(cpu_values),
                'memory_avg': np.mean(memory_values),
                'memory_max': np.max(memory_values),
                'gpu_avg': np.mean(gpu_values) if gpu_values else 0.0,
                'gpu_max': np.max(gpu_values) if gpu_values else 0.0
            },
            'performance_history_size': len(self.performance_history),
            'current_strategy': self.current_strategy.name
        }
    
    def set_optimization_mode(self, mode: OptimizationMode):
        """设置优化模式"""
        if mode.value in self.optimization_strategies:
            self.current_strategy = self.optimization_strategies[mode.value]
            logger.info(f"优化模式已切换到: {mode.value}")
        else:
            logger.warning(f"未知的优化模式: {mode.value}")
    
    def update_thresholds(self, thresholds: ResourceThresholds):
        """更新资源阈值"""
        self.resource_monitor.thresholds = thresholds
        logger.info("资源阈值已更新")
    
    def cleanup(self):
        """清理资源"""
        self.resource_monitor.stop_monitoring()
        logger.info("ResourceAwareOptimizer 已清理") 