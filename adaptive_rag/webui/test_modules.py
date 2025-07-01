#!/usr/bin/env python3
"""
测试模块拆分是否成功
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def test_imports():
    """测试所有模块的导入"""
    print("🧪 测试模块导入...")
    
    try:
        # 测试引擎模块
        from engines import AdaptiveRAGEngine, RealConfigAdaptiveRAGEngine, MockDataManager
        print("✅ 引擎模块导入成功")
        
        # 测试组件模块
        from components import create_basic_tab, create_query_tab, create_analysis_tab
        print("✅ 组件模块导入成功")
        
        # 测试工具模块
        from utils.styles import get_custom_css
        from utils.handlers import create_event_handlers
        print("✅ 工具模块导入成功")
        
        # 测试原始接口
        from interface import create_ui, create_ui_with_real_config
        print("✅ 原始接口导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_engine_creation():
    """测试引擎创建"""
    print("\n🧪 测试引擎创建...")
    
    try:
        from engines import AdaptiveRAGEngine, MockDataManager
        
        # 测试模拟数据管理器
        data_manager = MockDataManager()
        stats = data_manager.get_corpus_stats()
        print(f"✅ 模拟数据管理器创建成功: {stats['total_documents']} 个文档")
        
        # 测试主引擎（不初始化真实组件）
        print("⚠️ 跳过主引擎测试（需要真实配置）")
        
        return True
        
    except Exception as e:
        print(f"❌ 引擎创建失败: {e}")
        return False

def test_style_generation():
    """测试样式生成"""
    print("\n🧪 测试样式生成...")
    
    try:
        from utils.styles import get_custom_css
        
        css = get_custom_css()
        if css and len(css) > 100:
            print("✅ 样式生成成功")
            return True
        else:
            print("❌ 样式生成失败")
            return False
            
    except Exception as e:
        print(f"❌ 样式生成失败: {e}")
        return False

def test_handler_creation():
    """测试事件处理器创建"""
    print("\n🧪 测试事件处理器创建...")
    
    try:
        from utils.handlers import create_event_handlers
        from engines import MockDataManager
        
        # 创建模拟引擎
        class MockEngine:
            def __init__(self):
                self.data_manager = MockDataManager()
            
            def initialize_components(self):
                pass
            
            def process_query(self, query, show_details):
                return {"query": query, "answer": "测试答案"}
        
        engine = MockEngine()
        handlers = create_event_handlers(engine)
        
        if handlers and len(handlers) > 0:
            print("✅ 事件处理器创建成功")
            return True
        else:
            print("❌ 事件处理器创建失败")
            return False
            
    except Exception as e:
        print(f"❌ 事件处理器创建失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试模块拆分...\n")
    
    tests = [
        test_imports,
        test_engine_creation,
        test_style_generation,
        test_handler_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！模块拆分成功！")
        return True
    else:
        print("❌ 部分测试失败，请检查模块拆分")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 