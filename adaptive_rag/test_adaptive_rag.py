#!/usr/bin/env python3
"""
=== Adaptive RAG 测试脚本 ===

测试基于 FlexRAG 重构后的 Adaptive RAG 系统
"""

import sys
import os
import logging
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_imports():
    """测试导入"""
    print("🔧 测试模块导入")
    print("=" * 50)
    
    try:
        # 测试 FlexRAG 导入
        from flexrag.assistant import BasicAssistant, ASSISTANTS
        from flexrag.utils.dataclasses import RetrievedContext, QueryResult
        print("✅ FlexRAG 导入成功")
        
        # 测试 Adaptive RAG 导入
        from adaptive_rag import (
            AdaptiveAssistant, AdaptiveConfig, create_adaptive_assistant,
            QueryAnalyzer, QueryType, QueryComplexity, AnalysisResult,
            StrategyRouter, RetrievalStrategy,
            HybridRetriever
        )
        print("✅ Adaptive RAG 导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False


def test_query_analyzer():
    """测试查询分析器"""
    print("\n🧠 测试查询分析器")
    print("=" * 50)
    
    try:
        from adaptive_rag import QueryAnalyzer, AdaptiveConfig
        
        # 创建配置
        config = AdaptiveConfig()
        analyzer = QueryAnalyzer(config)
        
        # 测试查询
        test_queries = [
            "What is machine learning?",
            "Compare artificial intelligence and machine learning",
            "Which magazine was started first Arthur's Magazine or First for Women?",
            "What nationality was Henry Valentine Miller's wife?",
            "Summarize the main points about the 2020 US election"
        ]
        
        for query in test_queries:
            print(f"\n📝 查询: {query}")
            result = analyzer.analyze_query(query)
            
            print(f"   类型: {result.query_type.value}")
            print(f"   复杂度: {result.complexity.value}")
            print(f"   子查询数: {len(result.sub_queries)}")
            print(f"   关键词: {result.keywords[:3]}")
            print(f"   置信度: {result.confidence:.2f}")
        
        print("\n✅ 查询分析器测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 查询分析器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_strategy_router():
    """测试策略路由器"""
    print("\n🎯 测试策略路由器")
    print("=" * 50)
    
    try:
        from adaptive_rag import QueryAnalyzer, StrategyRouter, AdaptiveConfig
        
        # 创建组件
        config = AdaptiveConfig()
        analyzer = QueryAnalyzer(config)
        router = StrategyRouter(config)
        
        # 测试查询
        query = "Compare machine learning and deep learning"
        
        # 分析查询
        analysis_result = analyzer.analyze_query(query)
        print(f"查询: {query}")
        print(f"分析结果: {analysis_result.query_type.value}, {analysis_result.complexity.value}")
        
        # 路由策略
        strategy_info = router.route_strategy(analysis_result)
        strategy = strategy_info["strategy"]
        
        print(f"\n策略信息:")
        print(f"   策略名称: {strategy.strategy_name}")
        print(f"   关键词权重: {strategy.keyword_weight:.2f}")
        print(f"   向量权重: {strategy.vector_weight:.2f}")
        print(f"   最大文档数: {strategy.max_docs}")
        print(f"   重排序: {'启用' if strategy.rerank_enabled else '禁用'}")
        print(f"   多样性因子: {strategy.diversity_factor:.2f}")
        print(f"   策略置信度: {strategy.confidence:.2f}")
        
        print("\n✅ 策略路由器测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 策略路由器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_hybrid_retriever():
    """测试混合检索器"""
    print("\n🔍 测试混合检索器")
    print("=" * 50)
    
    try:
        from adaptive_rag import QueryAnalyzer, StrategyRouter, HybridRetriever, AdaptiveConfig
        
        # 创建组件
        config = AdaptiveConfig()
        analyzer = QueryAnalyzer(config)
        router = StrategyRouter(config)
        retriever = HybridRetriever(config)
        
        # 测试查询
        query = "What is artificial intelligence?"
        
        # 分析和路由
        analysis_result = analyzer.analyze_query(query)
        strategy_info = router.route_strategy(analysis_result)
        
        print(f"查询: {query}")
        print(f"策略: {strategy_info['strategy'].strategy_name}")
        
        # 执行检索
        contexts = retriever.retrieve(query, analysis_result, strategy_info)
        
        print(f"\n检索结果:")
        print(f"   检索到 {len(contexts)} 个文档")
        
        for i, ctx in enumerate(contexts, 1):
            print(f"   {i}. 评分: {ctx.score:.3f}")
            print(f"      内容: {ctx.content[:100]}...")
            if ctx.metadata:
                print(f"      元数据: {list(ctx.metadata.keys())}")
        
        print("\n✅ 混合检索器测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 混合检索器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_adaptive_assistant():
    """测试自适应助手"""
    print("\n🤖 测试自适应助手")
    print("=" * 50)
    
    try:
        from adaptive_rag import create_adaptive_assistant
        
        # 创建助手
        assistant = create_adaptive_assistant()
        print("✅ 自适应助手创建成功")
        
        # 测试查询分析
        query = "Compare machine learning and deep learning"
        analysis_result = assistant.get_analysis_result(query)
        
        print(f"\n查询分析测试:")
        print(f"   查询: {query}")
        print(f"   类型: {analysis_result['query_type']}")
        print(f"   复杂度: {analysis_result['complexity']}")
        print(f"   子查询数: {len(analysis_result['sub_queries'])}")
        
        # 测试策略路由
        strategy = assistant.get_strategy(analysis_result)
        print(f"\n策略路由测试:")
        print(f"   策略名称: {strategy['strategy'].strategy_name}")
        print(f"   权重分配: 关键词 {strategy['strategy'].keyword_weight:.2f}, 向量 {strategy['strategy'].vector_weight:.2f}")
        
        # 测试检索
        contexts = assistant.get_retrieval_results(query, strategy)
        print(f"\n检索测试:")
        print(f"   检索到 {len(contexts)} 个文档")
        
        print("\n✅ 自适应助手测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 自适应助手测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_levelrag_style_queries():
    """测试 LevelRAG 风格的查询"""
    print("\n📚 测试 LevelRAG 风格的查询")
    print("=" * 50)
    
    try:
        from adaptive_rag import create_adaptive_assistant
        
        assistant = create_adaptive_assistant()
        
        # LevelRAG 论文中的典型多跳问题
        levelrag_queries = [
            "Which magazine was started first Arthur's Magazine or First for Women?",
            "What nationality was Henry Valentine Miller's wife?",
            "Are director of film Move (1970 Film) and director of film Méditerranée (1963 Film) from the same country?",
            "Who is Rhescuporis I (Odrysian)'s paternal grandfather?"
        ]
        
        for query in levelrag_queries:
            print(f"\n📝 LevelRAG 查询: {query}")
            
            # 分析查询
            analysis = assistant.get_analysis_result(query)
            print(f"   分解为 {len(analysis['sub_queries'])} 个子查询:")
            
            for i, sub_query in enumerate(analysis['sub_queries'], 1):
                print(f"     {i}. {sub_query.content}")
                print(f"        类型: {sub_query.query_type.value}")
                print(f"        优先级: {sub_query.priority:.2f}")
        
        print("\n✅ LevelRAG 风格查询测试完成")
        return True
        
    except Exception as e:
        print(f"❌ LevelRAG 风格查询测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("🚀 Adaptive RAG 基于 FlexRAG 重构测试")
    print("=" * 80)
    print("测试基于 FlexRAG 框架重构的 Adaptive RAG 系统")
    print("=" * 80)
    
    test_results = []
    
    # 运行所有测试
    tests = [
        ("模块导入", test_imports),
        ("查询分析器", test_query_analyzer),
        ("策略路由器", test_strategy_router),
        ("混合检索器", test_hybrid_retriever),
        ("自适应助手", test_adaptive_assistant),
        ("LevelRAG 风格查询", test_levelrag_style_queries),
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            test_results.append((test_name, False))
    
    # 总结结果
    print("\n\n📊 测试结果总结")
    print("=" * 50)
    
    passed = 0
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{len(test_results)} 个测试通过")
    
    if passed == len(test_results):
        print("\n🎉 所有测试通过！Adaptive RAG 基于 FlexRAG 重构成功！")
        print("\n💡 下一步:")
        print("1. 配置真实的 FlexRAG 检索器和重排序器")
        print("2. 集成到 WebUI 中")
        print("3. 使用真实数据进行测试")
    else:
        print(f"\n⚠️ 有 {len(test_results) - passed} 个测试失败，需要修复")


if __name__ == "__main__":
    main()
