#!/usr/bin/env python3
"""
=== AdaptiveRAG 模块化配置测试脚本 ===

演示如何使用模块化配置系统来控制各个模块的开启和关闭
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from adaptive_rag.config import (
    create_config_from_yaml, 
    print_module_status,
    get_enabled_modules,
    ModuleToggleConfig,
    FlexRAGIntegratedConfig
)


def test_basic_mode():
    """测试基础模式配置"""
    print("🧪 测试基础模式配置")
    print("=" * 60)
    
    config_path = "adaptive_rag/config/modular_config.yaml"
    config = create_config_from_yaml(config_path, preset="basic_mode")
    
    print_module_status(config)
    
    # 验证基础模式的特点
    enabled_modules = get_enabled_modules(config)
    assert enabled_modules.get("task_decomposer", False), "基础模式应启用任务分解器"
    assert not enabled_modules.get("web_retriever", True), "基础模式应禁用网络检索器"
    assert not enabled_modules.get("intelligent_strategy_learner", True), "基础模式应禁用实验性功能"
    
    print("✅ 基础模式配置测试通过")


def test_performance_mode():
    """测试高性能模式配置"""
    print("\n🚀 测试高性能模式配置")
    print("=" * 60)
    
    config_path = "adaptive_rag/config/modular_config.yaml"
    config = create_config_from_yaml(config_path, preset="performance_mode")
    
    print_module_status(config)
    
    # 验证高性能模式的特点
    enabled_modules = get_enabled_modules(config)
    assert enabled_modules.get("web_retriever", False), "高性能模式应启用网络检索器"
    assert enabled_modules.get("cross_encoder_ranker", False), "高性能模式应启用交叉编码器重排"
    assert enabled_modules.get("performance_optimizer", False), "高性能模式应启用性能优化器"
    
    print("✅ 高性能模式配置测试通过")


def test_experimental_mode():
    """测试实验模式配置"""
    print("\n🔬 测试实验模式配置")
    print("=" * 60)
    
    config_path = "adaptive_rag/config/modular_config.yaml"
    config = create_config_from_yaml(config_path, preset="experimental_mode")
    
    print_module_status(config)
    
    # 验证实验模式的特点
    enabled_modules = get_enabled_modules(config)
    assert enabled_modules.get("intelligent_strategy_learner", False), "实验模式应启用智能策略学习器"
    assert enabled_modules.get("multi_dimensional_optimizer", False), "实验模式应启用多维度优化器"
    assert enabled_modules.get("fact_verification", False), "实验模式应启用事实验证"
    
    print("✅ 实验模式配置测试通过")


def test_custom_config():
    """测试自定义配置"""
    print("\n⚙️ 测试自定义配置")
    print("=" * 60)
    
    # 创建自定义配置
    config = FlexRAGIntegratedConfig()
    
    # 自定义模块开关
    config.modules = ModuleToggleConfig(
        task_decomposer=True,
        retrieval_planner=True,
        multi_retriever=True,
        context_reranker=False,  # 禁用重排序
        adaptive_generator=True,
        query_analyzer=True,
        strategy_router=False,   # 禁用策略路由
        keyword_retriever=True,
        dense_retriever=False,   # 只使用关键词检索
        web_retriever=False,
        semantic_cache=True,
        debug_mode=True          # 启用调试模式
    )
    
    print_module_status(config)
    
    # 验证自定义配置
    enabled_modules = get_enabled_modules(config)
    assert enabled_modules.get("task_decomposer", False), "应启用任务分解器"
    assert not enabled_modules.get("context_reranker", True), "应禁用重排序器"
    assert not enabled_modules.get("dense_retriever", True), "应禁用密集检索器"
    assert enabled_modules.get("debug_mode", False), "应启用调试模式"
    
    print("✅ 自定义配置测试通过")


def test_module_dependency_check():
    """测试模块依赖检查"""
    print("\n🔗 测试模块依赖检查")
    print("=" * 60)
    
    config = FlexRAGIntegratedConfig()
    config.modules = ModuleToggleConfig(
        multi_retriever=True,
        keyword_retriever=False,  # 禁用所有检索器
        dense_retriever=False,
        web_retriever=False,
        hybrid_retriever=False
    )
    
    enabled_modules = get_enabled_modules(config)
    
    # 检查依赖关系
    if enabled_modules.get("multi_retriever", False):
        has_retriever = any([
            enabled_modules.get("keyword_retriever", False),
            enabled_modules.get("dense_retriever", False),
            enabled_modules.get("web_retriever", False),
            enabled_modules.get("hybrid_retriever", False)
        ])
        
        if not has_retriever:
            print("⚠️ 警告：启用了多重检索系统但没有启用任何检索器")
        else:
            print("✅ 模块依赖检查通过")
    
    print("✅ 模块依赖检查完成")


def demonstrate_config_switching():
    """演示配置切换"""
    print("\n🔄 演示配置切换")
    print("=" * 60)
    
    config_path = "adaptive_rag/config/modular_config.yaml"
    
    modes = ["basic_mode", "performance_mode", "experimental_mode"]
    
    for mode in modes:
        print(f"\n📋 切换到 {mode}:")
        config = create_config_from_yaml(config_path, preset=mode)
        enabled_modules = get_enabled_modules(config)
        
        # 统计启用的模块数量
        enabled_count = sum(1 for enabled in enabled_modules.values() if enabled)
        total_count = len(enabled_modules)
        
        print(f"  启用模块: {enabled_count}/{total_count}")
        print(f"  启用率: {enabled_count/total_count*100:.1f}%")
    
    print("✅ 配置切换演示完成")


def main():
    """主函数"""
    print("🎯 AdaptiveRAG 模块化配置系统测试")
    print("=" * 80)
    
    try:
        # 测试各种预设模式
        test_basic_mode()
        test_performance_mode()
        test_experimental_mode()
        
        # 测试自定义配置
        test_custom_config()
        
        # 测试模块依赖
        test_module_dependency_check()
        
        # 演示配置切换
        demonstrate_config_switching()
        
        print("\n🎉 所有测试通过！")
        print("\n💡 使用建议:")
        print("  - 开发阶段使用 basic_mode")
        print("  - 生产环境使用 performance_mode")
        print("  - 研究实验使用 experimental_mode")
        print("  - 特殊需求使用自定义配置")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
