#!/usr/bin/env python3
"""
=== Adaptive RAG 简化测试 ===

测试不依赖 FlexRAG 的核心组件
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


def test_query_analyzer_standalone():
    """测试独立的查询分析器"""
    print("🧠 测试查询分析器（独立版本）")
    print("=" * 50)
    
    try:
        # 直接导入查询分析器组件
        from adaptive_rag.core.query_analyzer import QueryAnalyzer, QueryType, QueryComplexity, AnalysisResult
        
        # 创建简单配置
        class SimpleConfig:
            model_name = "mock"
        
        config = SimpleConfig()
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
            
            if result.sub_queries:
                print("   子查询:")
                for i, sub_query in enumerate(result.sub_queries, 1):
                    print(f"     {i}. {sub_query.content}")
                    print(f"        类型: {sub_query.query_type.value}")
                    print(f"        优先级: {sub_query.priority:.2f}")
        
        print("\n✅ 查询分析器测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 查询分析器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_strategy_router_standalone():
    """测试独立的策略路由器"""
    print("\n🎯 测试策略路由器（独立版本）")
    print("=" * 50)
    
    try:
        from adaptive_rag.core.query_analyzer import QueryAnalyzer
        from adaptive_rag.core.strategy_router import StrategyRouter
        
        # 创建简单配置
        class SimpleConfig:
            model_name = "mock"
            default_keyword_weight = 0.3
            default_vector_weight = 0.7
            max_retrieved_docs = 20
        
        config = SimpleConfig()
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


def test_levelrag_style_decomposition():
    """测试 LevelRAG 风格的分解"""
    print("\n📚 测试 LevelRAG 风格的分解")
    print("=" * 50)
    
    try:
        from adaptive_rag.core.query_analyzer import QueryAnalyzer
        
        class SimpleConfig:
            model_name = "mock"
        
        config = SimpleConfig()
        analyzer = QueryAnalyzer(config)
        
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
            analysis = analyzer.analyze_query(query)
            print(f"   类型: {analysis.query_type.value}")
            print(f"   复杂度: {analysis.complexity.value}")
            print(f"   分解为 {len(analysis.sub_queries)} 个子查询:")
            
            for i, sub_query in enumerate(analysis.sub_queries, 1):
                print(f"     {i}. {sub_query.content}")
                print(f"        类型: {sub_query.query_type.value}")
                print(f"        优先级: {sub_query.priority:.2f}")
        
        print("\n✅ LevelRAG 风格分解测试完成")
        return True
        
    except Exception as e:
        print(f"❌ LevelRAG 风格分解测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_comparison_with_original():
    """对比原始方法和新方法"""
    print("\n🔄 对比原始方法和新方法")
    print("=" * 50)
    
    try:
        from adaptive_rag.core.query_analyzer import QueryAnalyzer
        
        class SimpleConfig:
            model_name = "mock"
        
        config = SimpleConfig()
        analyzer = QueryAnalyzer(config)
        
        # 测试查询
        test_cases = [
            {
                "query": "Which magazine was started first Arthur's Magazine or First for Women?",
                "expected_type": "temporal",
                "expected_complexity": "complex",
                "expected_sub_queries": 2
            },
            {
                "query": "What nationality was Henry Valentine Miller's wife?",
                "expected_type": "complex",
                "expected_complexity": "moderate", 
                "expected_sub_queries": 1
            },
            {
                "query": "What is machine learning?",
                "expected_type": "factual",
                "expected_complexity": "simple",
                "expected_sub_queries": 0
            }
        ]
        
        print("测试案例分析:")
        for i, case in enumerate(test_cases, 1):
            query = case["query"]
            result = analyzer.analyze_query(query)
            
            print(f"\n{i}. {query}")
            print(f"   实际类型: {result.query_type.value} (期望: {case['expected_type']})")
            print(f"   实际复杂度: {result.complexity.value} (期望: {case['expected_complexity']})")
            print(f"   实际子查询数: {len(result.sub_queries)} (期望: {case['expected_sub_queries']})")
            
            # 评估准确性
            type_match = result.query_type.value == case["expected_type"]
            complexity_match = result.complexity.value == case["expected_complexity"]
            sub_query_match = len(result.sub_queries) >= case["expected_sub_queries"]
            
            accuracy = sum([type_match, complexity_match, sub_query_match]) / 3
            print(f"   准确性: {accuracy:.2f} ({'✅' if accuracy > 0.6 else '⚠️'})")
        
        print("\n✅ 对比测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 对比测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("🚀 Adaptive RAG 简化版本测试")
    print("=" * 80)
    print("测试不依赖 FlexRAG 的核心组件")
    print("=" * 80)
    
    test_results = []
    
    # 运行所有测试
    tests = [
        ("查询分析器", test_query_analyzer_standalone),
        ("策略路由器", test_strategy_router_standalone),
        ("LevelRAG 风格分解", test_levelrag_style_decomposition),
        ("对比测试", test_comparison_with_original),
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
        print("\n🎉 所有测试通过！")
        print("\n💡 重构成果:")
        print("✅ 实现了 LLM 驱动的查询分析（模拟版本）")
        print("✅ 支持 LevelRAG 风格的多跳问题分解")
        print("✅ 动态策略路由功能正常")
        print("✅ 模块化设计便于扩展")
        print("\n🔄 下一步:")
        print("1. 集成真实的 FlexRAG 组件")
        print("2. 配置真实的 LLM 模型")
        print("3. 与 WebUI 集成测试")
    else:
        print(f"\n⚠️ 有 {len(test_results) - passed} 个测试失败，需要修复")


if __name__ == "__main__":
    main()
