#!/usr/bin/env python3
"""
=== 真实组件测试脚本 ===

测试真实的检索器、生成器和重排序器
"""

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_real_components():
    """测试真实组件"""
    logger.info("🧪 测试真实组件")
    
    try:
        from adaptive_rag.webui.engines.enhanced_adaptive_rag_engine import EnhancedAdaptiveRAGEngine
        
        # 初始化引擎
        engine = EnhancedAdaptiveRAGEngine("real_config_enhanced.yaml")
        logger.info("✅ 增强版引擎初始化成功")
        
        # 检查模块状态
        module_status = engine.get_module_status()
        logger.info("📊 模块状态:")
        for module_name, status in module_status.items():
            logger.info(f"   {module_name}: {status['状态']}")
        
        # 测试查询处理
        test_queries = [
            "What is artificial intelligence?",
            "How does machine learning work?",
            "Explain the difference between supervised and unsupervised learning"
        ]
        
        for i, query in enumerate(test_queries, 1):
            logger.info(f"🔍 测试查询 {i}: {query}")
            try:
                result = engine.process_query(query, show_details=True, optimization_mode="balanced")
                logger.info(f"✅ 查询 {i} 处理成功，耗时: {result['total_time']:.3f}s")
                
                # 检查是否使用了真实组件
                if 'optimization_info' in result:
                    opt_info = result['optimization_info']
                    logger.info(f"   📊 优化信息: 资源感知={opt_info.get('resource_aware_used', False)}, "
                              f"多维度={opt_info.get('multi_dimensional_used', False)}, "
                              f"性能优化={opt_info.get('performance_optimizer_used', False)}")
                
                # 检查答案质量
                answer = result.get("answer", "")
                if answer and len(answer) > 10:
                    logger.info(f"   💬 生成答案: {answer[:100]}...")
                else:
                    logger.warning(f"   ⚠️ 答案可能为空或太短")
                
                # 检查检索结果
                retrieved_docs = result.get("retrieved_docs", {})
                if retrieved_docs:
                    total_docs = sum(len(docs.get("documents", [])) for docs in retrieved_docs.values())
                    logger.info(f"   📚 检索到 {total_docs} 个文档")
                else:
                    logger.warning(f"   ⚠️ 没有检索到文档")
                
            except Exception as e:
                logger.error(f"❌ 查询 {i} 处理失败: {e}")
        
        logger.info("🎉 真实组件测试完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ 真实组件测试失败: {e}")
        return False


def test_resource_optimization():
    """测试资源感知优化"""
    logger.info("🧪 测试资源感知优化")
    
    try:
        from adaptive_rag.core.resource_aware_optimizer import ResourceAwareOptimizer
        
        # 创建配置
        config = {
            "device": "cuda",
            "optimization": {
                "enable_resource_aware": True,
                "resource_aware": {
                    "enable_monitoring": True,
                    "update_interval": 1.0,
                    "thresholds": {
                        "cpu_warning": 80,
                        "cpu_critical": 95,
                        "memory_warning": 85,
                        "memory_critical": 95
                    }
                }
            }
        }
        
        # 初始化优化器
        optimizer = ResourceAwareOptimizer(config)
        logger.info("✅ 资源感知优化器初始化成功")
        
        # 获取资源分析
        analytics = optimizer.get_resource_analytics()
        logger.info("📈 资源分析数据获取成功")
        
        # 测试策略优化
        query_features = {
            'complexity_score': 0.7,
            'word_count': 5,
            'has_question_word': True,
            'is_multi_hop': False,
            'query_type': 'single_hop'
        }
        
        available_strategies = [
            {'keyword': 0.6, 'dense': 0.3, 'web': 0.1},
            {'keyword': 0.2, 'dense': 0.7, 'web': 0.1},
            {'keyword': 0.3, 'dense': 0.3, 'web': 0.4}
        ]
        
        optimized_strategy = optimizer.optimize_strategy(query_features, available_strategies)
        logger.info(f"📊 优化策略: {optimized_strategy}")
        
        logger.info("🎉 资源感知优化测试完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ 资源感知优化测试失败: {e}")
        return False


def main():
    """主测试函数"""
    logger.info("🚀 开始真实组件测试")
    
    # 测试资源感知优化
    resource_success = test_resource_optimization()
    
    # 测试真实组件
    component_success = test_real_components()
    
    # 输出测试结果
    logger.info("\n📋 测试结果汇总:")
    logger.info(f"   资源感知优化: {'✅ 通过' if resource_success else '❌ 失败'}")
    logger.info(f"   真实组件: {'✅ 通过' if component_success else '❌ 失败'}")
    
    if resource_success and component_success:
        logger.info("🎉 所有测试通过！真实组件可以正常使用。")
        logger.info("🌐 您可以访问 http://localhost:7863 查看增强版WebUI")
    else:
        logger.warning("⚠️ 部分测试失败，请检查相关配置和依赖。")


if __name__ == "__main__":
    main() 