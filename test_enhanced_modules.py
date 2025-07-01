#!/usr/bin/env python3
"""
=== 增强版模块测试脚本 ===

测试资源感知优化和其他模块功能
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


def test_enhanced_engine():
    """测试增强版引擎"""
    logger.info("🧪 测试增强版 AdaptiveRAG 引擎")
    
    try:
        from adaptive_rag.webui.engines.enhanced_adaptive_rag_engine import EnhancedAdaptiveRAGEngine
        
        # 初始化引擎
        engine = EnhancedAdaptiveRAGEngine("real_config.yaml")
        logger.info("✅ 增强版引擎初始化成功")
        
        # 测试模块状态
        module_status = engine.get_module_status()
        logger.info("📊 模块状态:")
        for module_name, status in module_status.items():
            logger.info(f"   {module_name}: {status['状态']}")
        
        # 测试查询处理
        test_query = "What is artificial intelligence?"
        logger.info(f"🔍 测试查询: {test_query}")
        
        result = engine.process_query(test_query, show_details=True, optimization_mode="balanced")
        logger.info(f"✅ 查询处理成功，耗时: {result['total_time']:.3f}s")
        
        # 检查优化信息
        if 'optimization_info' in result:
            opt_info = result['optimization_info']
            logger.info(f"📊 优化信息: 资源感知={opt_info.get('resource_aware_used', False)}, "
                      f"多维度={opt_info.get('multi_dimensional_used', False)}, "
                      f"性能优化={opt_info.get('performance_optimizer_used', False)}")
        
        logger.info("🎉 增强版引擎测试完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ 增强版引擎测试失败: {e}")
        return False


def main():
    """主测试函数"""
    logger.info("🚀 开始增强版模块测试")
    
    # 测试增强版引擎
    success = test_enhanced_engine()
    
    if success:
        logger.info("🎉 增强版引擎测试通过！WebUI 可以正常使用。")
    else:
        logger.error("❌ 增强版引擎测试失败，请检查相关依赖和配置。")


if __name__ == "__main__":
    main() 