#!/usr/bin/env python3
"""
=== 增强功能测试脚本 ===

测试新添加的智能学习、性能优化、多维度决策等功能
"""

import sys
import logging
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_intelligent_strategy_learner():
    """测试智能策略学习器"""
    logger.info("🧠 测试智能策略学习器")
    
    try:
        from adaptive_rag.core.intelligent_strategy_learner import IntelligentStrategyLearner, QueryComplexityAnalyzer
        
        # 初始化
        config = {}
        learner = IntelligentStrategyLearner(config)
        
        # 测试查询复杂度分析
        test_queries = [
            "What is the capital of France?",  # 简单事实查询
            "How does machine learning work and what are its applications?",  # 复杂推理查询
            "Compare Python and Java programming languages in terms of performance and ease of use",  # 比较查询
        ]
        
        for query in test_queries:
            logger.info(f"📝 分析查询: {query}")
            
            # 预测最优策略
            strategy_prediction = learner.predict_optimal_strategy(query)
            
            logger.info(f"🎯 推荐策略: {strategy_prediction['strategy_config']}")
            logger.info(f"🔍 查询特征: 复杂度={strategy_prediction['query_features'].complexity_score:.3f}, "
                       f"类型={strategy_prediction['query_features'].question_type}")
            logger.info(f"📊 置信度: {strategy_prediction['confidence']:.3f}")
            logger.info(f"💭 推理: {strategy_prediction['reasoning']}")
            logger.info("")
        
        logger.info("✅ 智能策略学习器测试完成")
        
    except Exception as e:
        logger.error(f"❌ 智能策略学习器测试失败: {e}")


def test_performance_optimizer():
    """测试性能优化器"""
    logger.info("⚡ 测试性能优化器")
    
    try:
        from adaptive_rag.core.performance_optimizer import PerformanceOptimizer
        
        # 初始化
        config = {
            'query_cache_size': 100,
            'doc_cache_size': 200
        }
        optimizer = PerformanceOptimizer(config)
        
        # 模拟检索函数
        def mock_retrieval_func(query):
            import time
            time.sleep(0.1)  # 模拟检索时间
            return [f"Document {i} for {query}" for i in range(3)]
        
        # 测试缓存优化
        test_query = "What is artificial intelligence?"
        
        logger.info(f"📝 测试查询: {test_query}")
        
        # 第一次检索 (缓存未命中)
        start_time = time.time()
        result1 = optimizer.optimize_retrieval(
            test_query, "dense", 5, mock_retrieval_func, test_query
        )
        time1 = time.time() - start_time
        logger.info(f"🔍 第一次检索时间: {time1:.3f}s (缓存未命中)")
        
        # 第二次检索 (缓存命中)
        start_time = time.time()
        result2 = optimizer.optimize_retrieval(
            test_query, "dense", 5, mock_retrieval_func, test_query
        )
        time2 = time.time() - start_time
        logger.info(f"🔍 第二次检索时间: {time2:.3f}s (缓存命中)")
        
        # 获取性能指标
        metrics = optimizer.get_performance_metrics()
        logger.info(f"📊 缓存命中率: {metrics.cache_hit_rate:.3f}")
        logger.info(f"📊 平均检索时间: {metrics.avg_retrieval_time:.3f}s")
        
        # 获取缓存统计
        cache_stats = optimizer.get_cache_statistics()
        logger.info(f"📊 缓存统计: {cache_stats}")
        
        logger.info("✅ 性能优化器测试完成")
        
    except Exception as e:
        logger.error(f"❌ 性能优化器测试失败: {e}")


def test_multi_dimensional_optimizer():
    """测试多维度决策优化器"""
    logger.info("🎯 测试多维度决策优化器")
    
    try:
        from adaptive_rag.core.multi_dimensional_optimizer import (
            MultiDimensionalOptimizer, OptimizationObjective, ResourceConstraints
        )
        
        # 初始化
        config = {}
        optimizer = MultiDimensionalOptimizer(config)
        
        # 模拟查询特征
        query_features = {
            'complexity_score': 0.7,
            'entity_count': 3,
            'token_count': 15,
            'question_type': 'reasoning'
        }
        
        # 可用策略
        available_strategies = [
            {'keyword': 0.6, 'dense': 0.3, 'web': 0.1},  # 关键词优先
            {'keyword': 0.2, 'dense': 0.7, 'web': 0.1},  # 语义优先
            {'keyword': 0.3, 'dense': 0.3, 'web': 0.4},  # Web优先
        ]
        
        # 测试不同优化目标
        objectives = [
            OptimizationObjective.ACCURACY,
            OptimizationObjective.SPEED,
            OptimizationObjective.COST,
            OptimizationObjective.BALANCED
        ]
        
        for objective in objectives:
            logger.info(f"🎯 优化目标: {objective.value}")
            
            optimal_strategy = optimizer.optimize_strategy(
                query_features=query_features,
                available_strategies=available_strategies,
                objective=objective
            )
            
            logger.info(f"📈 最优策略: {optimal_strategy.config}")
            logger.info(f"📊 预测性能: 准确性={optimal_strategy.predicted_performance.accuracy:.3f}, "
                       f"延迟={optimal_strategy.predicted_performance.latency_ms:.0f}ms, "
                       f"成本=${optimal_strategy.predicted_performance.cost:.4f}")
            logger.info("")
        
        logger.info("✅ 多维度决策优化器测试完成")
        
    except Exception as e:
        logger.error(f"❌ 多维度决策优化器测试失败: {e}")


def test_enhanced_evaluator():
    """测试增强评估器"""
    logger.info("📊 测试增强评估器")
    
    try:
        from adaptive_rag.evaluation.enhanced_evaluator import EnhancedEvaluator
        
        # 初始化
        config = {}
        evaluator = EnhancedEvaluator(config)
        
        # 模拟评估结果
        mock_results = [
            {
                'query': 'What is AI?',
                'ground_truth': 'Artificial Intelligence',
                'prediction': 'AI is artificial intelligence',
                'query_type': 'factual',
                'processing_time': 0.5,
                'strategy_used': {'keyword': 0.6, 'dense': 0.3, 'web': 0.1}
            },
            {
                'query': 'How does ML work?',
                'ground_truth': 'Machine learning uses algorithms',
                'prediction': 'ML works by learning from data',
                'query_type': 'reasoning',
                'processing_time': 0.8,
                'strategy_used': {'keyword': 0.2, 'dense': 0.7, 'web': 0.1}
            }
        ]
        
        # 计算传统指标
        traditional_metrics = evaluator._calculate_traditional_metrics(mock_results, [])
        logger.info(f"📊 传统指标: EM={traditional_metrics['exact_match']:.3f}, "
                   f"F1={traditional_metrics['f1_score']:.3f}")
        
        # 计算自适应指标
        adaptive_metrics = evaluator._calculate_adaptive_metrics(mock_results, [])
        logger.info(f"📊 自适应指标: 多样性={adaptive_metrics.strategy_diversity:.3f}, "
                   f"准确性={adaptive_metrics.adaptation_accuracy:.3f}")
        
        logger.info("✅ 增强评估器测试完成")
        
    except Exception as e:
        logger.error(f"❌ 增强评估器测试失败: {e}")


def test_baseline_methods():
    """测试基线方法"""
    logger.info("🔬 测试基线方法")
    
    try:
        from adaptive_rag.evaluation.baseline_methods import create_baseline_method
        
        config = {
            "retrieval_topk": 5,
            "max_tokens": 256,
            "max_iterations": 2,
            "tree_depth": 3
        }
        
        test_question = "What is the capital of France?"
        
        # 测试新添加的基线方法
        methods_to_test = ["turbo_rag", "level_rag"]
        
        for method_name in methods_to_test:
            logger.info(f"📊 测试 {method_name}")
            
            method = create_baseline_method(method_name, config)
            result = method.process_query(test_question)
            
            logger.info(f"✅ 答案: {result['answer']}")
            logger.info(f"⏱️ 检索时间: {result['retrieval_time']:.3f}s")
            logger.info(f"⏱️ 生成时间: {result['generation_time']:.3f}s")
            logger.info(f"⏱️ 总时间: {result['total_time']:.3f}s")
            
            if 'cache_hit_rate' in result:
                logger.info(f"💾 缓存命中率: {result['cache_hit_rate']:.3f}")
            
            logger.info("")
        
        logger.info("✅ 基线方法测试完成")
        
    except Exception as e:
        logger.error(f"❌ 基线方法测试失败: {e}")


def test_adaptive_assistant_integration():
    """测试自适应助手的集成功能"""
    logger.info("🤖 测试自适应助手集成")
    
    try:
        from adaptive_rag.core.adaptive_assistant import AdaptiveAssistant
        from adaptive_rag.config import AdaptiveConfig
        from adaptive_rag.core.multi_dimensional_optimizer import OptimizationObjective
        
        # 初始化
        config = AdaptiveConfig()
        assistant = AdaptiveAssistant(config)
        
        # 测试查询
        test_queries = [
            "What is machine learning?",
            "Compare Python and Java",
        ]
        
        # 测试不同优化目标
        objectives = [OptimizationObjective.BALANCED, OptimizationObjective.SPEED]
        
        for objective in objectives:
            logger.info(f"🎯 测试优化目标: {objective.value}")
            
            for query in test_queries:
                logger.info(f"📝 查询: {query}")
                
                try:
                    result = assistant.answer(query, optimization_objective=objective)
                    
                    logger.info(f"✅ 答案: {result.answer[:100]}...")
                    logger.info(f"📈 策略: {result.metadata.get('strategy', {})}")
                    logger.info(f"⏱️ 处理时间: {result.metadata.get('processing_time', 0):.3f}s")
                    logger.info(f"🎯 优化目标: {result.metadata.get('optimization_objective', 'unknown')}")
                    
                except Exception as e:
                    logger.error(f"❌ 查询处理失败: {e}")
                
                logger.info("")
        
        # 获取性能分析
        analytics = assistant.get_performance_analytics()
        logger.info(f"📊 性能分析: {analytics}")
        
        logger.info("✅ 自适应助手集成测试完成")
        
    except Exception as e:
        logger.error(f"❌ 自适应助手集成测试失败: {e}")


def main():
    """主函数"""
    logger.info("🚀 开始测试增强功能")
    
    # 运行所有测试
    test_intelligent_strategy_learner()
    test_performance_optimizer()
    test_multi_dimensional_optimizer()
    test_enhanced_evaluator()
    test_baseline_methods()
    test_adaptive_assistant_integration()
    
    logger.info("🎉 所有增强功能测试完成!")


if __name__ == "__main__":
    main()
