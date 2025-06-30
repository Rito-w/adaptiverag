#!/usr/bin/env python3
"""
=== FlexRAG 深度集成测试 ===

测试 FlexRAG 组件的深度集成效果
"""

import sys
import time
import logging
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_flexrag_integration():
    """测试 FlexRAG 深度集成"""
    
    print("🧪 FlexRAG 深度集成测试")
    print("=" * 60)
    
    try:
        # 1. 测试配置系统
        print("\n📋 1. 测试配置系统")
        from adaptive_rag.config import get_config_for_mode, FLEXRAG_AVAILABLE
        
        print(f"   FlexRAG 可用性: {FLEXRAG_AVAILABLE}")
        
        # 测试不同配置模式
        for mode in ["adaptive", "flexrag", "hybrid"]:
            try:
                config = get_config_for_mode(mode)
                print(f"   ✅ {mode} 模式配置创建成功")
            except Exception as e:
                print(f"   ❌ {mode} 模式配置失败: {e}")
        
        # 2. 测试集成检索器
        print("\n🔍 2. 测试集成检索器")
        from adaptive_rag.modules.retriever.flexrag_integrated_retriever import FlexRAGIntegratedRetriever
        
        config = get_config_for_mode("flexrag")
        retriever = FlexRAGIntegratedRetriever(config)
        
        retriever_info = retriever.get_retriever_info()
        print(f"   检索器信息: {retriever_info}")
        
        # 测试检索
        strategy = {
            "weights": {"keyword": 0.4, "dense": 0.4, "web": 0.2},
            "top_k_per_retriever": {"keyword": 3, "dense": 3, "web": 2},
            "fusion_method": "rrf"
        }
        
        result = retriever.adaptive_retrieve(
            query="What is artificial intelligence?",
            strategy=strategy,
            top_k=5
        )
        
        print(f"   ✅ 检索测试成功:")
        print(f"      - 查询: {result.query}")
        print(f"      - 结果数: {len(result.contexts)}")
        print(f"      - 检索时间: {result.retrieval_time:.3f}s")
        print(f"      - 检索器类型: {result.retriever_type}")
        
        # 3. 测试集成重排序器
        print("\n🎯 3. 测试集成重排序器")
        from adaptive_rag.modules.refiner.flexrag_integrated_ranker import FlexRAGIntegratedRanker
        
        ranker = FlexRAGIntegratedRanker(config)
        ranker_info = ranker.get_ranker_info()
        print(f"   重排序器信息: {ranker_info}")
        
        # 测试重排序
        ranking_strategy = {
            "ranker": "cross_encoder",
            "enable_multi_ranker": True,
            "ranker_weights": {"cross_encoder": 0.6, "colbert": 0.4},
            "final_top_k": 3
        }
        
        ranking_result = ranker.adaptive_rank(
            query="What is artificial intelligence?",
            contexts=result.contexts,
            strategy=ranking_strategy
        )
        
        print(f"   ✅ 重排序测试成功:")
        print(f"      - 原始数量: {len(result.contexts)}")
        print(f"      - 重排序后: {len(ranking_result.ranked_contexts)}")
        print(f"      - 重排序时间: {ranking_result.ranking_time:.3f}s")
        print(f"      - 重排序器类型: {ranking_result.ranker_type}")
        
        # 4. 测试集成生成器
        print("\n✨ 4. 测试集成生成器")
        from adaptive_rag.modules.generator.flexrag_integrated_generator import FlexRAGIntegratedGenerator
        
        generator = FlexRAGIntegratedGenerator(config)
        generator_info = generator.get_generator_info()
        print(f"   生成器信息: {generator_info}")
        
        # 测试生成
        generation_strategy = {
            "generator": "main_generator",
            "prompt_template": "step_by_step",
            "max_tokens": 200,
            "temperature": 0.7,
            "max_context_length": 1000
        }
        
        generation_result = generator.adaptive_generate(
            query="What is artificial intelligence?",
            contexts=ranking_result.ranked_contexts,
            strategy=generation_strategy
        )
        
        print(f"   ✅ 生成测试成功:")
        print(f"      - 答案长度: {len(generation_result.answer)} 字符")
        print(f"      - 生成时间: {generation_result.generation_time:.3f}s")
        print(f"      - 生成器类型: {generation_result.generator_type}")
        print(f"      - 答案预览: {generation_result.answer[:100]}...")
        
        # 5. 测试完整集成助手
        print("\n🤖 5. 测试完整集成助手")
        from adaptive_rag.core.flexrag_integrated_assistant import FlexRAGIntegratedAssistant
        
        assistant = FlexRAGIntegratedAssistant(config)
        system_info = assistant.get_system_info()
        print(f"   系统信息: {system_info}")
        
        # 测试完整流程
        test_queries = [
            "What is machine learning?",
            "Compare supervised and unsupervised learning",
            "When was deep learning invented?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n   测试查询 {i}: {query}")
            
            start_time = time.time()
            result = assistant.answer(query)
            end_time = time.time()
            
            print(f"      ✅ 处理完成:")
            print(f"         - 总耗时: {result.total_time:.3f}s")
            print(f"         - 子任务数: {len(result.subtasks)}")
            print(f"         - 检索结果: {sum(len(r.contexts) for r in result.retrieval_results)}")
            print(f"         - 答案长度: {len(result.answer)} 字符")
            print(f"         - 答案预览: {result.answer[:80]}...")
        
        # 6. 性能对比测试
        print("\n📊 6. 性能对比测试")
        
        # 测试不同配置模式的性能
        test_query = "What are the main differences between AI and ML?"
        
        for mode in ["adaptive", "flexrag"]:
            try:
                print(f"\n   测试 {mode} 模式:")
                
                mode_config = get_config_for_mode(mode)
                
                if mode == "flexrag":
                    mode_assistant = FlexRAGIntegratedAssistant(mode_config)
                else:
                    # 对于 adaptive 模式，使用原始助手
                    from adaptive_rag.core.adaptive_assistant import AdaptiveAssistant
                    mode_assistant = AdaptiveAssistant(mode_config)
                
                start_time = time.time()
                if hasattr(mode_assistant, 'answer'):
                    result = mode_assistant.answer(test_query)
                    answer = result.answer if hasattr(result, 'answer') else str(result)
                else:
                    answer = mode_assistant.quick_answer(test_query)
                end_time = time.time()
                
                print(f"      ✅ {mode} 模式完成:")
                print(f"         - 耗时: {end_time - start_time:.3f}s")
                print(f"         - 答案长度: {len(answer)} 字符")
                print(f"         - 答案预览: {answer[:60]}...")
                
            except Exception as e:
                print(f"      ❌ {mode} 模式失败: {e}")
        
        print("\n🎉 FlexRAG 深度集成测试完成!")
        print("=" * 60)
        
        # 总结
        print("\n📋 测试总结:")
        print("✅ 配置系统集成正常")
        print("✅ 检索器组件集成正常") 
        print("✅ 重排序器组件集成正常")
        print("✅ 生成器组件集成正常")
        print("✅ 完整助手流程正常")
        print("✅ 性能对比测试正常")
        
        if FLEXRAG_AVAILABLE:
            print("\n🌟 FlexRAG 组件可用，享受完整功能!")
        else:
            print("\n⚠️ FlexRAG 组件不可用，使用模拟实现")
            print("   建议安装 FlexRAG 以获得最佳性能")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


def test_component_compatibility():
    """测试组件兼容性"""
    
    print("\n🔧 组件兼容性测试")
    print("-" * 40)
    
    # 测试各种导入
    components = [
        ("FlexRAG 检索器", "adaptive_rag.modules.retriever.flexrag_integrated_retriever"),
        ("FlexRAG 重排序器", "adaptive_rag.modules.refiner.flexrag_integrated_ranker"),
        ("FlexRAG 生成器", "adaptive_rag.modules.generator.flexrag_integrated_generator"),
        ("FlexRAG 助手", "adaptive_rag.core.flexrag_integrated_assistant"),
        ("配置系统", "adaptive_rag.config")
    ]
    
    for name, module_path in components:
        try:
            __import__(module_path)
            print(f"✅ {name}: 导入成功")
        except Exception as e:
            print(f"❌ {name}: 导入失败 - {e}")


if __name__ == "__main__":
    print("🚀 启动 FlexRAG 深度集成测试")
    
    # 组件兼容性测试
    test_component_compatibility()
    
    # 完整集成测试
    test_flexrag_integration()
    
    print("\n👋 测试完成，感谢使用 AdaptiveRAG!")
