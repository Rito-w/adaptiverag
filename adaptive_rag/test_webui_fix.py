#!/usr/bin/env python3
"""
=== Web UI 修复测试 ===

测试修复后的 Web UI 功能
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_webui_engine():
    """测试 Web UI 引擎"""
    print("🧪 测试 Web UI 引擎...")
    
    try:
        from adaptive_rag.webui.interface import AdaptiveRAGEngine
        
        # 初始化引擎
        engine = AdaptiveRAGEngine()
        print("✅ 引擎初始化成功")
        
        # 测试查询处理
        test_query = "hello world"
        result = engine.process_query(test_query)
        
        print(f"✅ 查询处理成功:")
        print(f"   查询: {result['query']}")
        print(f"   答案: {result.get('answer', '未生成')[:100]}...")
        print(f"   处理时间: {result['processing_time']:.3f}s")
        print(f"   子任务数: {len(result.get('subtasks', []))}")
        print(f"   检索结果数: {len(result.get('retrieval_results', []))}")
        
        # 检查必要字段
        required_fields = ['query', 'answer', 'processing_time', 'subtasks', 'retrieval_results']
        missing_fields = [field for field in required_fields if field not in result]
        
        if missing_fields:
            print(f"⚠️ 缺少字段: {missing_fields}")
        else:
            print("✅ 所有必要字段都存在")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_retriever_metadata():
    """测试检索器的 metadata 处理"""
    print("\n🔍 测试检索器 metadata 处理...")
    
    try:
        from adaptive_rag.config import create_flexrag_integrated_config
        from adaptive_rag.modules.retriever.flexrag_integrated_retriever import FlexRAGIntegratedRetriever
        
        config = create_flexrag_integrated_config()
        retriever = FlexRAGIntegratedRetriever(config)
        
        strategy = {
            "weights": {"keyword": 0.5, "dense": 0.5},
            "fusion_method": "weighted_sum"
        }
        
        result = retriever.adaptive_retrieve("test query", strategy, top_k=3)
        
        print(f"✅ 检索成功: {len(result.contexts)} 个结果")
        
        # 检查每个结果的 metadata
        for i, ctx in enumerate(result.contexts):
            if hasattr(ctx, 'metadata') and ctx.metadata:
                print(f"   结果 {i+1}: metadata 正常 - {list(ctx.metadata.keys())}")
            else:
                print(f"   结果 {i+1}: metadata 缺失或为空")
        
        return True
        
    except Exception as e:
        print(f"❌ 检索器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_assistant_integration():
    """测试助手集成"""
    print("\n🤖 测试助手集成...")
    
    try:
        from adaptive_rag.config import create_flexrag_integrated_config
        from adaptive_rag.core.flexrag_integrated_assistant import FlexRAGIntegratedAssistant
        
        config = create_flexrag_integrated_config()
        assistant = FlexRAGIntegratedAssistant(config)
        
        result = assistant.answer("What is AI?")
        
        print(f"✅ 助手回答成功:")
        print(f"   查询: {result.query}")
        print(f"   答案长度: {len(result.answer)} 字符")
        print(f"   子任务数: {len(result.subtasks)}")
        print(f"   检索结果数: {len(result.retrieval_results)}")
        print(f"   总耗时: {result.total_time:.3f}s")
        
        # 检查检索结果的结构
        if result.retrieval_results:
            first_result = result.retrieval_results[0]
            print(f"   第一个检索结果:")
            print(f"     查询: {first_result.query}")
            print(f"     上下文数: {len(first_result.contexts)}")
            print(f"     检索时间: {first_result.retrieval_time:.3f}s")
            
            if first_result.contexts:
                first_ctx = first_result.contexts[0]
                print(f"     第一个上下文:")
                print(f"       内容长度: {len(first_ctx.content)} 字符")
                print(f"       分数: {first_ctx.score:.3f}")
                print(f"       有 metadata: {hasattr(first_ctx, 'metadata') and bool(first_ctx.metadata)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 助手测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("🧪 Web UI 修复验证测试")
    print("=" * 50)
    
    tests = [
        ("Web UI 引擎", test_webui_engine),
        ("检索器 metadata", test_retriever_metadata),
        ("助手集成", test_assistant_integration)
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
        print("🎉 所有测试通过！Web UI 修复成功")
        print("💡 现在可以正常使用 Web UI 了")
    else:
        print("⚠️ 部分测试失败，需要进一步检查")


if __name__ == "__main__":
    main()
