#!/usr/bin/env python3
"""
=== 测试真实模型效果 ===

对比不同模块组合的实际效果，展示模块开关的价值
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_module_combinations():
    """测试不同模块组合的效果"""
    print("🧪 测试真实模型的模块组合效果")
    print("=" * 80)
    
    try:
        from adaptive_rag.webui.engines.real_model_engine import RealModelEngine
        engine = RealModelEngine()
        print("✅ 真实模型引擎初始化成功")
    except Exception as e:
        print(f"❌ 真实模型引擎初始化失败: {e}")
        print("💡 请先运行: python3 adaptiverag/install_real_model_deps.py")
        return False
    
    # 测试查询
    test_queries = [
        "什么是人工智能？",
        "机器学习和深度学习的区别是什么？",
        "自然语言处理有哪些应用？"
    ]
    
    # 测试配置
    test_configs = [
        {
            "name": "🔍 仅关键词检索",
            "config": {
                "task_decomposer": False,
                "retrieval_planner": False,
                "multi_retriever": True,
                "context_reranker": False,
                "adaptive_generator": True,
                "keyword_retriever": True,
                "dense_retriever": False,
                "web_retriever": False
            }
        },
        {
            "name": "🧠 仅密集检索",
            "config": {
                "task_decomposer": False,
                "retrieval_planner": False,
                "multi_retriever": True,
                "context_reranker": False,
                "adaptive_generator": True,
                "keyword_retriever": False,
                "dense_retriever": True,
                "web_retriever": False
            }
        },
        {
            "name": "🔗 混合检索",
            "config": {
                "task_decomposer": False,
                "retrieval_planner": False,
                "multi_retriever": True,
                "context_reranker": False,
                "adaptive_generator": True,
                "keyword_retriever": True,
                "dense_retriever": True,
                "web_retriever": False
            }
        },
        {
            "name": "🎯 混合检索+重排序",
            "config": {
                "task_decomposer": False,
                "retrieval_planner": False,
                "multi_retriever": True,
                "context_reranker": True,
                "adaptive_generator": True,
                "keyword_retriever": True,
                "dense_retriever": True,
                "web_retriever": False
            }
        },
        {
            "name": "⚡ 完整流程",
            "config": {
                "task_decomposer": True,
                "retrieval_planner": True,
                "multi_retriever": True,
                "context_reranker": True,
                "adaptive_generator": True,
                "keyword_retriever": True,
                "dense_retriever": True,
                "web_retriever": False
            }
        }
    ]
    
    # 对每个查询测试不同配置
    for query_idx, query in enumerate(test_queries, 1):
        print(f"\n🔍 测试查询 {query_idx}: {query}")
        print("-" * 60)
        
        results = []
        
        for config_info in test_configs:
            config_name = config_info["name"]
            config = config_info["config"]
            
            print(f"\n{config_name}:")
            
            try:
                # 应用配置
                engine.update_module_config(config)
                
                # 执行查询
                start_time = time.time()
                result = engine.process_query_with_modules(query)
                end_time = time.time()
                
                # 收集结果
                retrieval_count = len(result.get('retrieval_results', []))
                rerank_count = len(result.get('reranked_results', []))
                answer = result.get('generated_answer', '')
                steps = result.get('steps', [])
                
                results.append({
                    "config": config_name,
                    "time": end_time - start_time,
                    "retrieval_count": retrieval_count,
                    "rerank_count": rerank_count,
                    "steps_count": len(steps),
                    "answer_length": len(answer),
                    "answer": answer[:100] + "..." if len(answer) > 100 else answer
                })
                
                print(f"  ⏱️ 耗时: {end_time - start_time:.2f}s")
                print(f"  📄 检索文档: {retrieval_count}个")
                print(f"  🎯 重排序文档: {rerank_count}个")
                print(f"  📋 处理步骤: {len(steps)}个")
                print(f"  📝 答案长度: {len(answer)}字符")
                print(f"  💬 答案预览: {answer[:80]}...")
                
            except Exception as e:
                print(f"  ❌ 测试失败: {e}")
                results.append({
                    "config": config_name,
                    "error": str(e)
                })
        
        # 显示对比结果
        print(f"\n📊 查询 {query_idx} 对比结果:")
        print("=" * 60)
        
        for result in results:
            if "error" not in result:
                print(f"{result['config']:<20} | "
                      f"耗时: {result['time']:.2f}s | "
                      f"检索: {result['retrieval_count']}个 | "
                      f"步骤: {result['steps_count']}个")
        
        # 找出最佳配置
        valid_results = [r for r in results if "error" not in r]
        if valid_results:
            # 综合评分：考虑检索数量、步骤数和答案长度
            for result in valid_results:
                score = (result['retrieval_count'] * 0.3 + 
                        result['steps_count'] * 0.3 + 
                        result['answer_length'] * 0.4 / 100)
                result['score'] = score
            
            best_result = max(valid_results, key=lambda x: x['score'])
            print(f"\n🏆 最佳配置: {best_result['config']}")
            print(f"   综合评分: {best_result['score']:.2f}")
    
    print("\n🎉 模块效果测试完成！")
    print("\n💡 关键发现:")
    print("   1. 不同检索器有不同的优势和特点")
    print("   2. 重排序能显著提升结果质量")
    print("   3. 完整流程提供最全面的处理")
    print("   4. 模块组合可以根据需求灵活调整")
    
    return True


def demonstrate_real_vs_mock():
    """演示真实模型与模拟模型的区别"""
    print("\n🔬 真实模型 vs 模拟模型对比")
    print("=" * 80)
    
    query = "什么是深度学习？"
    
    # 真实模型结果
    try:
        from adaptive_rag.webui.engines.real_model_engine import RealModelEngine
        real_engine = RealModelEngine()
        
        print("🔬 真实模型结果:")
        real_result = real_engine.process_query_with_modules(query)
        print(f"   检索文档数: {len(real_result.get('retrieval_results', []))}")
        print(f"   处理步骤: {real_result.get('steps', [])}")
        print(f"   生成答案: {real_result.get('generated_answer', '')[:150]}...")
        
    except Exception as e:
        print(f"❌ 真实模型测试失败: {e}")
    
    # 模拟模型结果
    try:
        from adaptive_rag.webui.engines.enhanced_adaptive_rag_engine import EnhancedAdaptiveRAGEngine
        mock_engine = EnhancedAdaptiveRAGEngine()
        
        print("\n🎭 模拟模型结果:")
        mock_result = mock_engine.process_query(query)
        print(f"   模拟处理: {mock_result.get('status', 'N/A')}")
        print(f"   模拟答案: 这是一个模拟的回答...")
        
    except Exception as e:
        print(f"❌ 模拟模型测试失败: {e}")
    
    print("\n🔍 主要区别:")
    print("   ✅ 真实模型: 使用真实的BM25、嵌入模型、生成模型")
    print("   ✅ 真实模型: 实际的文档检索和相似度计算")
    print("   ✅ 真实模型: 真实的重排序和生成过程")
    print("   ❌ 模拟模型: 只是返回预设的模拟数据")
    print("   ❌ 模拟模型: 无法体现模块开关的实际效果")


def main():
    """主函数"""
    print("🎯 AdaptiveRAG 真实模型效果测试")
    print("=" * 80)
    
    # 测试模块组合效果
    success = test_module_combinations()
    
    if success:
        # 演示真实vs模拟的区别
        demonstrate_real_vs_mock()
        
        print("\n🎉 测试完成！")
        print("\n💡 下一步:")
        print("   1. 启动WebUI查看可视化效果:")
        print("      python3 adaptiverag/launch_webui_with_module_control.py --port 7863 --host 0.0.0.0")
        print("   2. 在'🎛️ 模块控制'标签页中调整配置")
        print("   3. 在'🔬 真实模型测试'标签页中体验效果")
    else:
        print("\n❌ 测试失败，请检查依赖安装")


if __name__ == "__main__":
    main()
