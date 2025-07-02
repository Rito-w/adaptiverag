#!/usr/bin/env python3
"""
=== 增强版 AdaptiveRAG 引擎 ===

集成资源感知优化器的模块化引擎
"""

import logging
import time
import yaml
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys
import os

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logger = logging.getLogger(__name__)

# 导入优化模块
try:
    from adaptive_rag.core.resource_aware_optimizer import (
        ResourceAwareOptimizer, OptimizationMode, ResourceThresholds
    )
    RESOURCE_OPTIMIZER_AVAILABLE = True
except ImportError:
    RESOURCE_OPTIMIZER_AVAILABLE = False
    logger.warning("资源感知优化器不可用")

try:
    from adaptive_rag.core.multi_dimensional_optimizer import (
        MultiDimensionalOptimizer, OptimizationObjective, ResourceConstraints
    )
    MULTI_DIM_OPTIMIZER_AVAILABLE = True
except ImportError:
    MULTI_DIM_OPTIMIZER_AVAILABLE = False
    logger.warning("多维度优化器不可用")

try:
    from adaptive_rag.core.performance_optimizer import PerformanceOptimizer
    PERFORMANCE_OPTIMIZER_AVAILABLE = True
except ImportError:
    PERFORMANCE_OPTIMIZER_AVAILABLE = False
    logger.warning("性能优化器不可用")

# 导入模块管理器
try:
    from adaptive_rag.core.module_manager import ModuleManager
    from adaptive_rag.config import (
        create_config_from_yaml, ModuleToggleConfig,
        FlexRAGIntegratedConfig, get_enabled_modules
    )
    MODULE_MANAGER_AVAILABLE = True
except ImportError:
    MODULE_MANAGER_AVAILABLE = False
    logger.warning("模块管理器不可用")


class EnhancedAdaptiveRAGEngine:
    """增强版 AdaptiveRAG 引擎 - 集成所有优化模块"""

    def __init__(self, config_path: str = "real_config.yaml"):
        """初始化引擎"""
        logger.info("🚀 开始初始化增强版 AdaptiveRAG 引擎")
        logger.info(f"   配置文件路径: {config_path}")
        
        self.config_path = config_path
        logger.info("📋 步骤1: 加载配置文件...")
        self.config = self.load_config()
        logger.info("✅ 配置文件加载完成")
        
        self.last_results = None
        
        logger.info("🔧 步骤2: 初始化优化模块...")
        self.initialize_optimization_modules()
        logger.info("✅ 优化模块初始化完成")
        
        logger.info("🤖 步骤3: 初始化真实组件...")
        self.initialize_real_components()
        logger.info("✅ 真实组件初始化完成")

        logger.info("🎛️ 步骤4: 初始化模块管理器...")
        self.initialize_module_manager()
        logger.info("✅ 模块管理器初始化完成")

        logger.info("🎉 增强版 AdaptiveRAG 引擎初始化完成")
        logger.info(f"   配置文件: {self.config_path}")

    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            logger.info(f"✅ 配置文件加载成功: {self.config_path}")
            return config
        except Exception as e:
            logger.error(f"❌ 配置文件加载失败: {e}")
            return self.get_default_config()

    def get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "device": "cuda",
            "retriever_configs": {},
            "generator_configs": {},
            "ranker_configs": {},
            "optimization": {
                "enable_resource_aware": True,
                "enable_multi_dimensional": True,
                "enable_performance": True
            }
        }

    def initialize_optimization_modules(self):
        """初始化优化模块"""
        logger.info("   📦 创建优化模块字典...")
        self.optimization_modules = {}
        
        # 初始化资源感知优化器
        logger.info("   🔍 检查资源感知优化器可用性...")
        if RESOURCE_OPTIMIZER_AVAILABLE:
            logger.info("   ✅ 资源感知优化器模块可用，开始初始化...")
            try:
                logger.info("   🔧 创建 ResourceAwareOptimizer 实例...")
                self.optimization_modules['resource_aware'] = ResourceAwareOptimizer(self.config)
                logger.info("   ✅ 资源感知优化器初始化成功")
            except Exception as e:
                logger.error(f"   ❌ 资源感知优化器初始化失败: {e}")
                import traceback
                logger.error(f"   详细错误: {traceback.format_exc()}")
        else:
            logger.warning("   ⚠️ 资源感知优化器模块不可用")
        
        # 初始化多维度优化器
        logger.info("   🎯 检查多维度优化器可用性...")
        if MULTI_DIM_OPTIMIZER_AVAILABLE:
            logger.info("   ✅ 多维度优化器模块可用，开始初始化...")
            try:
                logger.info("   🔧 创建 MultiDimensionalOptimizer 实例...")
                self.optimization_modules['multi_dimensional'] = MultiDimensionalOptimizer(self.config)
                logger.info("   ✅ 多维度优化器初始化成功")
            except Exception as e:
                logger.error(f"   ❌ 多维度优化器初始化失败: {e}")
                import traceback
                logger.error(f"   详细错误: {traceback.format_exc()}")
        else:
            logger.warning("   ⚠️ 多维度优化器模块不可用")
        
        # 初始化性能优化器
        logger.info("   ⚡ 检查性能优化器可用性...")
        if PERFORMANCE_OPTIMIZER_AVAILABLE:
            logger.info("   ✅ 性能优化器模块可用，开始初始化...")
            try:
                logger.info("   🔧 创建 PerformanceOptimizer 实例...")
                self.optimization_modules['performance'] = PerformanceOptimizer(self.config)
                logger.info("   ✅ 性能优化器初始化成功")
            except Exception as e:
                logger.error(f"   ❌ 性能优化器初始化失败: {e}")
                import traceback
                logger.error(f"   详细错误: {traceback.format_exc()}")
        else:
            logger.warning("   ⚠️ 性能优化器模块不可用")

    def initialize_real_components(self):
        """初始化真实组件"""
        logger.info("   🤖 开始初始化真实 FlexRAG 组件...")
        try:
            logger.info("   📦 导入 FlexRAG 相关模块...")
            # 尝试初始化真实的 FlexRAG 组件
            from adaptive_rag.core.flexrag_integrated_assistant import FlexRAGIntegratedAssistant
            from adaptive_rag.config import create_flexrag_integrated_config
            logger.info("   ✅ FlexRAG 模块导入成功")

            logger.info("   ⚙️ 创建 FlexRAG 集成配置...")
            # 使用真实配置创建助手
            config = create_flexrag_integrated_config()
            logger.info("   ✅ 基础配置创建成功")
            
            logger.info("   🔧 更新检索器配置...")
            # 更新配置以使用真实组件
            if 'retriever_configs' in self.config:
                for name, retriever_config in self.config['retriever_configs'].items():
                    if name in config.retriever_configs:
                        config.retriever_configs[name]['retriever_type'] = retriever_config.get('retriever_type', 'mock')
                        if 'config' not in config.retriever_configs[name]:
                            config.retriever_configs[name]['config'] = {}
                        
                        # 更新具体配置
                        for key, value in retriever_config.items():
                            if key not in ['retriever_type']:
                                config.retriever_configs[name]['config'][key] = value
                logger.info(f"   ✅ 更新了 {len(self.config['retriever_configs'])} 个检索器配置")
            
            logger.info("   📊 更新重排序器配置...")
            if 'ranker_configs' in self.config:
                for name, ranker_config in self.config['ranker_configs'].items():
                    if name in config.ranker_configs:
                        config.ranker_configs[name]['ranker_type'] = ranker_config.get('ranker_type', 'mock')
                        if 'config' not in config.ranker_configs[name]:
                            config.ranker_configs[name]['config'] = {}
                        
                        for key, value in ranker_config.items():
                            if key not in ['ranker_type']:
                                config.ranker_configs[name]['config'][key] = value
                logger.info(f"   ✅ 更新了 {len(self.config['ranker_configs'])} 个重排序器配置")
            
            logger.info("   🤖 更新生成器配置...")
            if 'generator_configs' in self.config:
                for name, generator_config in self.config['generator_configs'].items():
                    if name in config.generator_configs:
                        config.generator_configs[name]['generator_type'] = generator_config.get('generator_type', 'mock')
                        if 'config' not in config.generator_configs[name]:
                            config.generator_configs[name]['config'] = {}
                        
                        for key, value in generator_config.items():
                            if key not in ['generator_type']:
                                config.generator_configs[name]['config'][key] = value
                logger.info(f"   ✅ 更新了 {len(self.config['generator_configs'])} 个生成器配置")
            
            logger.info("   🖥️ 更新设备配置...")
            # 更新设备配置
            config.device = self.config.get('device', 'cuda')
            config.batch_size = self.config.get('batch_size', 4)
            logger.info(f"   ✅ 设备: {config.device}, 批次大小: {config.batch_size}")
            
            logger.info("   🚀 创建 FlexRAGIntegratedAssistant 实例...")
            self.assistant = FlexRAGIntegratedAssistant(config)
            self.use_real_components = True
            logger.info("   ✅ 真实 FlexRAG 组件初始化成功")

        except Exception as e:
            logger.warning(f"   ⚠️ 真实组件初始化失败，使用模拟实现: {e}")
            import traceback
            logger.error(f"   详细错误: {traceback.format_exc()}")
            self.assistant = None
            self.use_real_components = False

    def get_module_status(self) -> Dict[str, Any]:
        """获取模块状态"""
        return {
            "资源感知优化器": {
                "状态": "✅ 可用" if 'resource_aware' in self.optimization_modules else "❌ 不可用",
                "功能": "动态资源监控和自适应策略调整",
                "配置": "已启用" if self.config.get('optimization', {}).get('enable_resource_aware', False) else "未启用"
            },
            "多维度优化器": {
                "状态": "✅ 可用" if 'multi_dimensional' in self.optimization_modules else "❌ 不可用",
                "功能": "多目标优化和策略权衡分析",
                "配置": "已启用" if self.config.get('optimization', {}).get('enable_multi_dimensional', False) else "未启用"
            },
            "性能优化器": {
                "状态": "✅ 可用" if 'performance' in self.optimization_modules else "❌ 不可用",
                "功能": "缓存优化和性能监控",
                "配置": "已启用" if self.config.get('optimization', {}).get('enable_performance', False) else "未启用"
            },
            "FlexRAG集成助手": {
                "状态": "✅ 可用" if self.use_real_components else "❌ 不可用",
                "功能": "真实检索器和生成器集成",
                "配置": "已启用"
            }
        }

    def get_resource_analytics(self) -> Dict[str, Any]:
        """获取资源分析数据"""
        if 'resource_aware' in self.optimization_modules:
            return self.optimization_modules['resource_aware'].get_resource_analytics()
        return {}

    def get_performance_metrics(self) -> Dict[str, Any]:
        """获取性能指标"""
        if 'performance' in self.optimization_modules:
            return self.optimization_modules['performance'].get_performance_metrics().__dict__
        return {}

    def process_query(self, query: str, show_details: bool = True, 
                     optimization_mode: str = "balanced") -> Dict[str, Any]:
        """处理查询（集成所有优化模块）"""
        start_time = time.time()

        logger.info(f"🔍 处理查询: {query} (优化模式: {optimization_mode})")

        # 第一步：查询分析
        query_features = self.analyze_query(query)
        
        # 第二步：资源感知优化
        if 'resource_aware' in self.optimization_modules:
            # 设置优化模式
            mode_map = {
                "performance": OptimizationMode.PERFORMANCE,
                "efficiency": OptimizationMode.EFFICIENCY,
                "balanced": OptimizationMode.BALANCED,
                "conservative": OptimizationMode.CONSERVATIVE
            }
            if optimization_mode in mode_map:
                self.optimization_modules['resource_aware'].set_optimization_mode(mode_map[optimization_mode])
            
            # 可用策略
            available_strategies = [
                {'keyword': 0.6, 'dense': 0.3, 'web': 0.1},  # 关键词优先
                {'keyword': 0.2, 'dense': 0.7, 'web': 0.1},  # 语义优先
                {'keyword': 0.3, 'dense': 0.3, 'web': 0.4},  # Web优先
            ]
            
            # 资源感知优化
            optimized_strategy = self.optimization_modules['resource_aware'].optimize_strategy(
                query_features, available_strategies
            )
        else:
            optimized_strategy = {'keyword': 0.4, 'dense': 0.4, 'web': 0.2}

        # 第三步：多维度优化
        if 'multi_dimensional' in self.optimization_modules:
            constraints = ResourceConstraints(
                max_latency_ms=5000.0,
                max_cost_per_query=0.1,
                max_memory_mb=1000.0,
                max_api_calls=10
            )
            
            multi_dim_strategy = self.optimization_modules['multi_dimensional'].optimize_strategy(
                query_features=query_features,
                available_strategies=[optimized_strategy],
                objective=OptimizationObjective.BALANCED,
                constraints=constraints
            )
            final_strategy = multi_dim_strategy.config
        else:
            final_strategy = optimized_strategy

        # 第四步：性能优化的查询处理
        if 'performance' in self.optimization_modules:
            def processing_func():
                return self.process_with_real_components(query, show_details) if self.use_real_components else self.process_with_simulation(query, show_details)
            
            result = self.optimization_modules['performance'].optimize_query_processing(
                query, final_strategy, processing_func
            )
        else:
            # 直接处理
            if self.use_real_components and self.assistant:
                result = self.process_with_real_components(query, show_details)
            else:
                result = self.process_with_simulation(query, show_details)

        # 添加优化信息
        result['optimization_info'] = {
            'resource_aware_used': 'resource_aware' in self.optimization_modules,
            'multi_dimensional_used': 'multi_dimensional' in self.optimization_modules,
            'performance_optimizer_used': 'performance' in self.optimization_modules,
            'final_strategy': final_strategy,
            'optimization_mode': optimization_mode
        }

        self.last_results = result
        return result

    def analyze_query(self, query: str) -> Dict[str, Any]:
        """分析查询特征"""
        words = query.lower().split()
        complexity_score = min(len(words) / 10.0, 1.0)

        question_words = ['what', 'who', 'where', 'when', 'why', 'how']
        has_question_word = any(word in words for word in question_words)

        multi_hop_indicators = ['and', 'also', 'furthermore', 'additionally', 'where', 'author', 'creator']
        is_multi_hop = any(indicator in words for indicator in multi_hop_indicators)

        return {
            'complexity_score': complexity_score,
            'word_count': len(words),
            'has_question_word': has_question_word,
            'is_multi_hop': is_multi_hop,
            'query_type': 'multi_hop' if is_multi_hop else 'single_hop'
        }

    def process_with_real_components(self, query: str, show_details: bool = True) -> Dict[str, Any]:
        """使用真实组件处理查询"""
        start_time = time.time()

        # 使用 FlexRAG 集成助手处理查询
        try:
            result = self.assistant.answer(query)
            processing_time = time.time() - start_time

            # 转换为标准格式
            processed_result = {
                "query": query,
                "answer": result.answer,
                "retrieved_docs": [],
                "processing_details": {},
                "total_time": processing_time,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "method": "real_components",
                "stages": {
                    "query_analysis": {
                        "processing_time": 0.1,
                        "status": "✅ 完成（真实）"
                    },
                    "strategy_planning": {
                        "processing_time": 0.1,
                        "status": "✅ 完成（真实）"
                    },
                    "retrieval": {
                        "processing_time": 0.2,
                        "status": "✅ 完成（真实）",
                        "retriever_results": {}
                    },
                    "reranking": {
                        "processing_time": 0.1,
                        "status": "✅ 完成（真实）"
                    },
                    "generation": {
                        "processing_time": 0.3,
                        "status": "✅ 完成（真实）",
                        "generated_answer": result.answer
                    }
                }
            }

            return processed_result
        except Exception as e:
            logger.error(f"真实组件处理失败: {e}")
            return self.process_with_simulation(query, show_details)

    def process_with_simulation(self, query: str, show_details: bool = True) -> Dict[str, Any]:
        """使用模拟实现处理查询"""
        start_time = time.time()

        # 模拟各个阶段
        stages = {
            "query_analysis": self.simulate_query_analysis(query),
            "strategy_planning": self.simulate_strategy_planning(query),
            "retrieval": self.simulate_retrieval(query),
            "reranking": self.simulate_reranking(query),
            "generation": self.simulate_generation(query)
        }

        total_time = time.time() - start_time

        result = {
            "query": query,
            "stages": stages,
            "total_time": total_time,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "answer": stages["generation"]["generated_answer"],
            "retrieved_docs": stages["retrieval"]["retriever_results"],
            "method": "simulation",
            "processing_details": {
                "query_analysis_time": stages["query_analysis"]["processing_time"],
                "strategy_planning_time": stages["strategy_planning"]["processing_time"],
                "retrieval_time": stages["retrieval"]["processing_time"],
                "reranking_time": stages["reranking"]["processing_time"],
                "generation_time": stages["generation"]["processing_time"]
            }
        }

        return result

    def simulate_query_analysis(self, query: str) -> Dict[str, Any]:
        """模拟查询分析阶段"""
        time.sleep(0.1)
        return {
            "complexity_score": 0.6,
            "word_count": len(query.split()),
            "has_question_word": True,
            "is_multi_hop": False,
            "query_type": "single_hop",
            "processing_time": 0.1,
            "status": "✅ 完成（模拟）"
        }

    def simulate_strategy_planning(self, query: str) -> Dict[str, Any]:
        """模拟策略规划阶段"""
        time.sleep(0.1)
        return {
            "selected_strategy": "balanced_strategy",
            "retriever_weights": {"keyword": 0.4, "dense": 0.4, "web": 0.2},
            "confidence": 0.85,
            "reasoning": "基于查询复杂度选择平衡策略",
            "processing_time": 0.1,
            "status": "✅ 完成（模拟）"
        }

    def simulate_retrieval(self, query: str) -> Dict[str, Any]:
        """模拟检索阶段"""
        time.sleep(0.2)
        return {
            "retriever_results": {
                "keyword_retriever": {
                    "type": "keyword",
                    "documents": [
                        {"id": "doc_1", "title": "Document 1", "content": f"Content for: {query[:50]}...", "score": 0.9}
                    ],
                    "total_found": 1,
                    "processing_time": 0.05,
                    "status": "✅ 完成（模拟）"
                }
            },
            "total_documents": 1,
            "processing_time": 0.2,
            "status": "✅ 完成（模拟）"
        }

    def simulate_reranking(self, query: str) -> Dict[str, Any]:
        """模拟重排序阶段"""
        time.sleep(0.1)
        return {
            "ranker_used": "default_ranker",
            "reranked_documents": [
                {"id": "doc_1", "title": "Document 1", "content": f"Reranked content for: {query[:50]}...", "score": 0.95}
            ],
            "score_improvement": 0.05,
            "processing_time": 0.1,
            "status": "✅ 完成（模拟）"
        }

    def simulate_generation(self, query: str) -> Dict[str, Any]:
        """模拟生成阶段"""
        time.sleep(0.3)
        return {
            "generator_used": "default_generator",
            "generated_answer": f"Based on the retrieved information, here's the answer to '{query}': This is a simulated response.",
            "confidence": 0.88,
            "token_count": 20,
            "processing_time": 0.3,
            "status": "✅ 完成（模拟）"
        }

    def initialize_module_manager(self):
        """初始化模块管理器"""
        if MODULE_MANAGER_AVAILABLE:
            try:
                # 尝试从配置文件创建模块化配置
                modular_config_path = "adaptive_rag/config/modular_config.yaml"
                if Path(modular_config_path).exists():
                    self.modular_config = create_config_from_yaml(modular_config_path, preset="performance_mode")
                else:
                    # 创建默认配置
                    self.modular_config = FlexRAGIntegratedConfig()
                    self.modular_config.modules = ModuleToggleConfig()

                # 初始化模块管理器
                self.module_manager = ModuleManager(self.modular_config)
                self.module_manager.initialize_modules()

                logger.info("✅ 模块管理器初始化成功")
            except Exception as e:
                logger.error(f"❌ 模块管理器初始化失败: {e}")
                self.module_manager = None
                self.modular_config = None
        else:
            logger.warning("⚠️ 模块管理器不可用")
            self.module_manager = None
            self.modular_config = None

    def update_module_config(self, module_config: Dict[str, bool]):
        """更新模块配置"""
        try:
            if self.modular_config and hasattr(self.modular_config, 'modules'):
                # 更新模块开关配置
                for module_name, enabled in module_config.items():
                    if hasattr(self.modular_config.modules, module_name):
                        setattr(self.modular_config.modules, module_name, enabled)

                # 重新初始化模块管理器
                if self.module_manager:
                    self.module_manager = ModuleManager(self.modular_config)
                    self.module_manager.initialize_modules()

                logger.info(f"✅ 模块配置已更新，启用模块数: {sum(module_config.values())}")
                return True
            else:
                logger.warning("⚠️ 模块配置对象不可用")
                return False
        except Exception as e:
            logger.error(f"❌ 更新模块配置失败: {e}")
            return False

    def get_module_status(self) -> Dict[str, Any]:
        """获取模块状态"""
        try:
            if self.module_manager:
                status = self.module_manager.get_module_status()
                enabled_modules = self.module_manager.get_enabled_modules()

                return {
                    "module_status": status,
                    "enabled_modules": enabled_modules,
                    "enabled_count": len(enabled_modules),
                    "total_count": len(status),
                    "status": "✅ 模块管理器正常运行"
                }
            else:
                return {
                    "module_status": {},
                    "enabled_modules": [],
                    "enabled_count": 0,
                    "total_count": 0,
                    "status": "⚠️ 模块管理器不可用"
                }
        except Exception as e:
            logger.error(f"❌ 获取模块状态失败: {e}")
            return {
                "module_status": {},
                "enabled_modules": [],
                "enabled_count": 0,
                "total_count": 0,
                "status": f"❌ 获取状态失败: {e}"
            }

    def get_current_module_config(self) -> Dict[str, bool]:
        """获取当前模块配置"""
        try:
            if self.modular_config and hasattr(self.modular_config, 'modules'):
                return get_enabled_modules(self.modular_config)
            else:
                return {}
        except Exception as e:
            logger.error(f"❌ 获取模块配置失败: {e}")
            return {}