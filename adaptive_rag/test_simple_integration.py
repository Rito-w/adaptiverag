#!/usr/bin/env python3
"""
=== 简单集成测试 ===

测试 FlexRAG 集成的基本功能
"""

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 创建简单的测试上下文类
class TestRetrievedContext:
    def __init__(self, content, score, metadata=None):
        self.content = content
        self.score = score
        self.metadata = metadata or {}

def test_config():
    """测试配置系统"""
    print("🧪 测试配置系统...")
    
    try:
        from adaptive_rag.config import create_flexrag_integrated_config, FLEXRAG_AVAILABLE
        
        print(f"FlexRAG 可用性: {FLEXRAG_AVAILABLE}")
        
        config = create_flexrag_integrated_config()
        print("✅ FlexRAG 集成配置创建成功")
        print(f"   设备: {config.device}")
        print(f"   批次大小: {config.batch_size}")
        print(f"   检索器配置数: {len(config.retriever_configs)}")
        print(f"   重排序器配置数: {len(config.ranker_configs)}")
        print(f"   生成器配置数: {len(config.generator_configs)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_retriever():
    """测试检索器"""
    print("\n🔍 测试检索器...")
    
    try:
        from adaptive_rag.config import create_flexrag_integrated_config
        from adaptive_rag.modules.retriever.flexrag_integrated_retriever import FlexRAGIntegratedRetriever
        
        config = create_flexrag_integrated_config()
        retriever = FlexRAGIntegratedRetriever(config)
        
        info = retriever.get_retriever_info()
        print("✅ 检索器初始化成功")
        print(f"   FlexRAG 可用: {info['flexrag_available']}")
        print(f"   回退模式: {info['fallback_mode']}")
        print(f"   加载的检索器: {info['loaded_retrievers']}")
        
        # 测试检索
        strategy = {
            "weights": {"keyword": 0.5, "dense": 0.5},
            "fusion_method": "weighted_sum"
        }
        
        result = retriever.adaptive_retrieve("test query", strategy, top_k=3)
        print(f"   检索测试成功: {len(result.contexts)} 个结果")
        
        return True
        
    except Exception as e:
        print(f"❌ 检索器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ranker():
    """测试重排序器"""
    print("\n🎯 测试重排序器...")
    
    try:
        from adaptive_rag.config import create_flexrag_integrated_config
        from adaptive_rag.modules.refiner.flexrag_integrated_ranker import FlexRAGIntegratedRanker

        
        config = create_flexrag_integrated_config()
        ranker = FlexRAGIntegratedRanker(config)
        
        info = ranker.get_ranker_info()
        print("✅ 重排序器初始化成功")
        print(f"   FlexRAG 可用: {info['flexrag_available']}")
        print(f"   回退模式: {info['fallback_mode']}")
        print(f"   加载的重排序器: {info['loaded_rankers']}")
        
        # 创建测试上下文
        test_contexts = [
            TestRetrievedContext(
                content=f"测试文档 {i}，包含相关信息...",
                score=1.0 - i * 0.1,
                metadata={"doc_id": f"test_{i}"}
            )
            for i in range(3)
        ]
        
        strategy = {
            "ranker": "cross_encoder",
            "final_top_k": 2
        }
        
        result = ranker.adaptive_rank("test query", test_contexts, strategy)
        print(f"   重排序测试成功: {len(result.ranked_contexts)} 个结果")
        
        return True
        
    except Exception as e:
        print(f"❌ 重排序器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_generator():
    """测试生成器"""
    print("\n✨ 测试生成器...")
    
    try:
        from adaptive_rag.config import create_flexrag_integrated_config
        from adaptive_rag.modules.generator.flexrag_integrated_generator import FlexRAGIntegratedGenerator

        
        config = create_flexrag_integrated_config()
        generator = FlexRAGIntegratedGenerator(config)
        
        info = generator.get_generator_info()
        print("✅ 生成器初始化成功")
        print(f"   FlexRAG 可用: {info['flexrag_available']}")
        print(f"   回退模式: {info['fallback_mode']}")
        print(f"   加载的生成器: {info['loaded_generators']}")
        
        # 创建测试上下文
        test_contexts = [
            TestRetrievedContext(
                content="人工智能是计算机科学的一个分支...",
                score=0.9,
                metadata={"doc_id": "ai_1"}
            )
        ]
        
        strategy = {
            "generator": "main_generator",
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        result = generator.adaptive_generate("What is AI?", test_contexts, strategy)
        print(f"   生成测试成功: {len(result.answer)} 字符")
        print(f"   答案预览: {result.answer[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 生成器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_assistant():
    """测试完整助手"""
    print("\n🤖 测试完整助手...")
    
    try:
        from adaptive_rag.config import create_flexrag_integrated_config
        from adaptive_rag.core.flexrag_integrated_assistant import FlexRAGIntegratedAssistant
        
        config = create_flexrag_integrated_config()
        assistant = FlexRAGIntegratedAssistant(config)
        
        info = assistant.get_system_info()
        print("✅ 助手初始化成功")
        print(f"   助手类型: {info['assistant_type']}")
        print(f"   FlexRAG 可用: {info['flexrag_available']}")
        print(f"   支持功能: {', '.join(info['supported_features'])}")
        
        # 测试问答
        result = assistant.answer("What is machine learning?")
        print(f"   问答测试成功:")
        print(f"     查询: {result.query}")
        print(f"     答案长度: {len(result.answer)} 字符")
        print(f"     子任务数: {len(result.subtasks)}")
        print(f"     总耗时: {result.total_time:.3f}s")
        print(f"     答案预览: {result.answer[:80]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 助手测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("🧪 FlexRAG 集成简单测试")
    print("=" * 50)
    
    tests = [
        ("配置系统", test_config),
        ("检索器", test_retriever),
        ("重排序器", test_ranker),
        ("生成器", test_generator),
        ("完整助手", test_assistant)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
    
    print(f"\n{'='*50}")
    print("📊 测试结果总结:")
    
    passed = 0
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{len(results)} 个测试通过")
    
    if passed == len(results):
        print("🎉 所有测试通过！FlexRAG 集成工作正常")
    else:
        print("⚠️ 部分测试失败，请检查错误信息")
    
    print(f"\n💡 下一步:")
    print(f"   1. 如果测试通过，可以运行: python main.py webui")
    print(f"   2. 如果有失败，请检查 FlexRAG 安装: pip install flexrag")
    print(f"   3. 查看详细文档: FLEXRAG_INTEGRATION.md")


if __name__ == "__main__":
    main()
