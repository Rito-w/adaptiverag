#!/usr/bin/env python3
"""
=== FlexRAG 深度集成演示 ===

展示 FlexRAG 深度集成的强大功能
"""

import sys
import time
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def demo_basic_usage():
    """演示基本使用方法"""
    
    print("🎯 FlexRAG 深度集成基本演示")
    print("=" * 50)
    
    try:
        from adaptive_rag.config import get_config_for_mode, FLEXRAG_AVAILABLE
        from adaptive_rag.core.flexrag_integrated_assistant import FlexRAGIntegratedAssistant
        
        print(f"FlexRAG 可用性: {'✅ 可用' if FLEXRAG_AVAILABLE else '❌ 不可用'}")
        
        # 创建配置和助手
        config = get_config_for_mode("flexrag")
        assistant = FlexRAGIntegratedAssistant(config)
        
        # 获取系统信息
        system_info = assistant.get_system_info()
        print(f"\n📊 系统信息:")
        print(f"   助手类型: {system_info['assistant_type']}")
        print(f"   初始化状态: {system_info['is_initialized']}")
        print(f"   支持功能: {', '.join(system_info['supported_features'])}")
        
        # 演示查询
        demo_queries = [
            "What is artificial intelligence?",
            "Compare machine learning and deep learning",
            "When was the transformer architecture invented?"
        ]
        
        print(f"\n🔍 演示查询处理:")
        
        for i, query in enumerate(demo_queries, 1):
            print(f"\n--- 查询 {i}: {query} ---")
            
            start_time = time.time()
            result = assistant.answer(query)
            end_time = time.time()
            
            print(f"✅ 处理完成 (耗时: {end_time - start_time:.2f}s)")
            print(f"📋 子任务数: {len(result.subtasks)}")
            print(f"🔍 检索结果: {sum(len(r.contexts) for r in result.retrieval_results)}")
            print(f"📝 答案长度: {len(result.answer)} 字符")
            print(f"💬 答案预览: {result.answer[:100]}...")
            
            # 显示性能统计
            if result.metadata and "stage_times" in result.metadata:
                times = result.metadata["stage_times"]
                print(f"⏱️ 性能统计:")
                print(f"   检索: {times.get('retrieval', 0):.3f}s")
                print(f"   重排序: {times.get('ranking', 0):.3f}s")
                print(f"   生成: {times.get('generation', 0):.3f}s")
        
        print(f"\n🎉 基本演示完成!")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()


def demo_advanced_features():
    """演示高级功能"""
    
    print("\n🚀 FlexRAG 深度集成高级演示")
    print("=" * 50)
    
    try:
        from adaptive_rag.config import get_config_for_mode
        from adaptive_rag.core.flexrag_integrated_assistant import FlexRAGIntegratedAssistant
        
        config = get_config_for_mode("flexrag")
        assistant = FlexRAGIntegratedAssistant(config)
        
        # 演示自定义策略
        print("\n🎯 演示自定义策略:")
        
        custom_strategies = [
            {
                "name": "高质量策略",
                "config": {
                    "retrieval_top_k": 15,
                    "enable_reranking": True,
                    "ranking_strategy": {
                        "ranker": "cross_encoder",
                        "enable_multi_ranker": True,
                        "ranker_weights": {"cross_encoder": 0.7, "colbert": 0.3},
                        "final_top_k": 8
                    },
                    "generation_strategy": {
                        "generator": "main_generator",
                        "prompt_template": "step_by_step",
                        "max_tokens": 300,
                        "temperature": 0.1
                    }
                }
            },
            {
                "name": "快速策略",
                "config": {
                    "retrieval_top_k": 5,
                    "enable_reranking": False,
                    "generation_strategy": {
                        "generator": "main_generator",
                        "prompt_template": "default",
                        "max_tokens": 150,
                        "temperature": 0.5
                    }
                }
            }
        ]
        
        test_query = "What are the main applications of artificial intelligence?"
        
        for strategy in custom_strategies:
            print(f"\n--- {strategy['name']} ---")
            
            start_time = time.time()
            result = assistant.answer(test_query, strategy['config'])
            end_time = time.time()
            
            print(f"⏱️ 耗时: {end_time - start_time:.2f}s")
            print(f"📊 结果质量指标:")
            print(f"   检索文档数: {sum(len(r.contexts) for r in result.retrieval_results)}")
            print(f"   最终上下文数: {len(result.generation_result.used_contexts) if result.generation_result else 0}")
            print(f"   答案长度: {len(result.answer)} 字符")
            print(f"💬 答案: {result.answer[:150]}...")
        
        # 演示过程解释
        print(f"\n🔍 演示过程解释:")
        explanation = assistant.explain_process(test_query)
        
        print(f"查询: {explanation['query']}")
        for step_name, step_info in explanation['process_explanation'].items():
            print(f"   {step_name}: {step_info['description']}")
        
        print(f"\n🎉 高级演示完成!")
        
    except Exception as e:
        print(f"❌ 高级演示失败: {e}")
        import traceback
        traceback.print_exc()


def demo_component_comparison():
    """演示组件对比"""
    
    print("\n📊 FlexRAG vs 原始组件对比演示")
    print("=" * 50)
    
    try:
        from adaptive_rag.config import get_config_for_mode
        
        test_query = "Explain the difference between supervised and unsupervised learning"
        
        # 测试不同模式
        modes = ["adaptive", "flexrag"]
        results = {}
        
        for mode in modes:
            print(f"\n--- 测试 {mode.upper()} 模式 ---")
            
            try:
                config = get_config_for_mode(mode)
                
                if mode == "flexrag":
                    from adaptive_rag.core.flexrag_integrated_assistant import FlexRAGIntegratedAssistant
                    assistant = FlexRAGIntegratedAssistant(config)
                else:
                    # 使用原始助手
                    from adaptive_rag.core.adaptive_assistant import AdaptiveAssistant
                    assistant = AdaptiveAssistant(config)
                
                start_time = time.time()
                
                if hasattr(assistant, 'answer'):
                    result = assistant.answer(test_query)
                    answer = result.answer if hasattr(result, 'answer') else str(result)
                    metadata = getattr(result, 'metadata', {})
                else:
                    answer = assistant.quick_answer(test_query)
                    metadata = {}
                
                end_time = time.time()
                
                results[mode] = {
                    "answer": answer,
                    "time": end_time - start_time,
                    "length": len(answer),
                    "metadata": metadata
                }
                
                print(f"✅ {mode} 模式完成:")
                print(f"   耗时: {results[mode]['time']:.3f}s")
                print(f"   答案长度: {results[mode]['length']} 字符")
                print(f"   答案预览: {answer[:100]}...")
                
            except Exception as e:
                print(f"❌ {mode} 模式失败: {e}")
                results[mode] = {"error": str(e)}
        
        # 对比总结
        print(f"\n📈 对比总结:")
        if "adaptive" in results and "flexrag" in results:
            adaptive_result = results["adaptive"]
            flexrag_result = results["flexrag"]
            
            if "error" not in adaptive_result and "error" not in flexrag_result:
                print(f"   性能对比:")
                print(f"     Adaptive: {adaptive_result['time']:.3f}s, {adaptive_result['length']} 字符")
                print(f"     FlexRAG:  {flexrag_result['time']:.3f}s, {flexrag_result['length']} 字符")
                
                if flexrag_result['time'] < adaptive_result['time']:
                    print(f"   🏆 FlexRAG 模式更快 ({adaptive_result['time']/flexrag_result['time']:.1f}x)")
                else:
                    print(f"   🏆 Adaptive 模式更快 ({flexrag_result['time']/adaptive_result['time']:.1f}x)")
                
                if flexrag_result['length'] > adaptive_result['length']:
                    print(f"   📝 FlexRAG 模式答案更详细")
                else:
                    print(f"   📝 Adaptive 模式答案更简洁")
        
        print(f"\n🎉 对比演示完成!")
        
    except Exception as e:
        print(f"❌ 对比演示失败: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主演示函数"""
    
    print("🎪 FlexRAG 深度集成完整演示")
    print("🔗 展示 AdaptiveRAG 与 FlexRAG 的深度集成效果")
    print("=" * 60)
    
    # 检查环境
    try:
        from adaptive_rag.config import FLEXRAG_AVAILABLE
        print(f"🔧 环境检查: FlexRAG {'✅ 可用' if FLEXRAG_AVAILABLE else '❌ 不可用'}")
        
        if not FLEXRAG_AVAILABLE:
            print("⚠️ FlexRAG 不可用，将使用模拟实现进行演示")
            print("💡 建议安装 FlexRAG 以获得完整功能: pip install flexrag")
        
    except Exception as e:
        print(f"❌ 环境检查失败: {e}")
        return
    
    # 运行演示
    try:
        # 基本功能演示
        demo_basic_usage()
        
        # 高级功能演示
        demo_advanced_features()
        
        # 组件对比演示
        demo_component_comparison()
        
        print(f"\n🎊 所有演示完成!")
        print(f"🌟 FlexRAG 深度集成为 AdaptiveRAG 带来了:")
        print(f"   ✅ 更稳定的组件")
        print(f"   ✅ 更丰富的功能")
        print(f"   ✅ 更好的性能")
        print(f"   ✅ 更强的可扩展性")
        
        print(f"\n💡 下一步建议:")
        print(f"   1. 运行 'python main.py webui --mode flexrag' 启动 Web UI")
        print(f"   2. 运行 'python main.py test-flexrag' 进行完整测试")
        print(f"   3. 查看 FLEXRAG_INTEGRATION.md 了解详细使用方法")
        
    except KeyboardInterrupt:
        print(f"\n👋 演示被用户中断")
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
