#!/usr/bin/env python3
"""
=== Web UI process_query 测试 ===

专门测试 Web UI 的 process_query 方法
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_webui_process_query():
    """测试 Web UI 的 process_query 方法"""
    print("🧪 测试 Web UI process_query 方法...")
    
    try:
        from adaptive_rag.webui.interface import AdaptiveRAGEngine
        
        # 初始化引擎
        engine = AdaptiveRAGEngine()
        print("✅ 引擎初始化成功")
        
        # 测试查询处理
        test_query = "hello world"
        print(f"🔍 测试查询: {test_query}")
        
        result = engine.process_query(test_query)
        
        print(f"✅ 查询处理成功")
        print(f"   返回类型: {type(result)}")
        print(f"   返回字段: {list(result.keys())}")
        
        # 检查必要字段
        required_fields = ['query', 'answer', 'processing_time', 'subtasks', 'retrieval_results']
        missing_fields = [field for field in required_fields if field not in result]
        
        if missing_fields:
            print(f"⚠️ 缺少字段: {missing_fields}")
        else:
            print("✅ 所有必要字段都存在")
        
        # 详细检查每个字段
        print(f"\n📋 字段详情:")
        for key, value in result.items():
            print(f"   {key}: {type(value)} - {str(value)[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_webui_interface_function():
    """测试 Web UI 接口函数"""
    print("\n🌐 测试 Web UI 接口函数...")
    
    try:
        from adaptive_rag.webui.interface import AdaptiveRAGEngine
        
        # 初始化引擎
        engine = AdaptiveRAGEngine()
        
        # 模拟 process_search 函数的逻辑
        query = "test query"
        show_details = True
        max_results = 5
        
        print(f"🔍 模拟处理查询: {query}")
        
        # 初始化组件
        engine.initialize_components()
        
        # 处理查询
        result = engine.process_query(query, show_details)
        
        print(f"✅ 查询处理成功")
        print(f"   结果类型: {type(result)}")
        print(f"   结果字段: {list(result.keys())}")
        
        # 检查是否有 plans 字段
        if 'plans' in result:
            print(f"⚠️ 发现 plans 字段: {result['plans']}")
        else:
            print(f"✅ 没有 plans 字段，这是正确的")
        
        # 模拟 Web UI 中的处理逻辑
        print(f"\n📊 模拟 Web UI 处理:")
        
        # 计算总结果数
        total_docs = 0
        if 'retrieval_results' in result:
            total_docs = sum(len(r.contexts) for r in result['retrieval_results'])
            print(f"   总文档数: {total_docs}")
        
        # 任务分解信息
        task_info = {"subtasks": []}
        if 'subtasks' in result and result['subtasks']:
            task_info["subtasks"] = [
                {
                    "id": getattr(st, 'id', f"task_{i}"),
                    "content": getattr(st, 'content', str(st)),
                    "type": str(getattr(st, 'task_type', 'unknown'))
                }
                for i, st in enumerate(result['subtasks'])
            ]
            print(f"   任务信息: {len(task_info['subtasks'])} 个子任务")
        
        # 检索策略信息
        strategy_info = {"retrieval_results": []}
        if 'retrieval_results' in result:
            strategy_info["retrieval_results"] = [
                {
                    "query": r.query,
                    "contexts_count": len(r.contexts),
                    "retrieval_time": r.retrieval_time
                }
                for r in result['retrieval_results']
            ]
            print(f"   策略信息: {len(strategy_info['retrieval_results'])} 个检索结果")
        
        print(f"✅ Web UI 处理逻辑测试成功")
        
        return True
        
    except Exception as e:
        print(f"❌ Web UI 接口测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("🧪 Web UI process_query 专项测试")
    print("=" * 50)
    
    tests = [
        ("process_query 方法", test_webui_process_query),
        ("Web UI 接口函数", test_webui_interface_function)
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
        print("🎉 所有测试通过！Web UI process_query 工作正常")
    else:
        print("⚠️ 部分测试失败，需要进一步检查")


if __name__ == "__main__":
    main()
