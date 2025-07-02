#!/usr/bin/env python3
"""
=== WebUI 模块控制功能测试 ===

测试WebUI中的模块控制功能
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import gradio as gr
from adaptive_rag.webui.engines.enhanced_adaptive_rag_engine import EnhancedAdaptiveRAGEngine
from adaptive_rag.webui.components.module_control_tab import create_module_control_tab


def test_module_control_integration():
    """测试模块控制集成"""
    print("🧪 测试 WebUI 模块控制功能")
    print("=" * 60)
    
    # 创建引擎
    print("1. 初始化引擎...")
    try:
        engine = EnhancedAdaptiveRAGEngine("configs/real_config_enhanced.yaml")
        print("✅ 引擎初始化成功")
    except Exception as e:
        print(f"❌ 引擎初始化失败: {e}")
        return False
    
    # 测试模块状态获取
    print("\n2. 测试模块状态获取...")
    try:
        status = engine.get_module_status()
        print(f"✅ 模块状态获取成功")
        print(f"   启用模块数: {status['enabled_count']}/{status['total_count']}")
        print(f"   状态: {status['status']}")
    except Exception as e:
        print(f"❌ 模块状态获取失败: {e}")
        return False
    
    # 测试模块配置更新
    print("\n3. 测试模块配置更新...")
    try:
        test_config = {
            "task_decomposer": True,
            "retrieval_planner": True,
            "multi_retriever": True,
            "context_reranker": False,  # 禁用重排序
            "adaptive_generator": True,
            "query_analyzer": True,
            "strategy_router": False,   # 禁用策略路由
            "keyword_retriever": True,
            "dense_retriever": False,   # 只使用关键词检索
            "web_retriever": False,
            "semantic_cache": True,
            "debug_mode": True          # 启用调试模式
        }
        
        result = engine.update_module_config(test_config)
        if result:
            print("✅ 模块配置更新成功")
            
            # 验证更新后的状态
            new_status = engine.get_module_status()
            print(f"   更新后启用模块数: {new_status['enabled_count']}")
        else:
            print("❌ 模块配置更新失败")
            return False
    except Exception as e:
        print(f"❌ 模块配置更新异常: {e}")
        return False
    
    # 测试当前配置获取
    print("\n4. 测试当前配置获取...")
    try:
        current_config = engine.get_current_module_config()
        print(f"✅ 当前配置获取成功，包含 {len(current_config)} 个模块")
        
        # 显示部分配置
        enabled_modules = [name for name, enabled in current_config.items() if enabled]
        print(f"   启用的模块: {enabled_modules[:5]}...")
    except Exception as e:
        print(f"❌ 当前配置获取失败: {e}")
        return False
    
    print("\n✅ 所有测试通过！")
    return True


def create_test_interface():
    """创建测试界面"""
    print("🎨 创建测试界面...")
    
    # 初始化引擎
    engine = EnhancedAdaptiveRAGEngine("configs/real_config_enhanced.yaml")
    
    # 自定义CSS
    custom_css = """
    .gradio-container, .main, .container {
        max-width: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .system-status-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    .status-item {
        display: flex;
        justify-content: space-between;
        margin: 8px 0;
        padding: 5px 0;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }
    
    .status-success {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #c3e6cb;
    }
    
    .status-error {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #f5c6cb;
    }
    
    .primary-button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        font-weight: 600;
    }
    """
    
    with gr.Blocks(
        title="🎛️ AdaptiveRAG 模块控制测试",
        css=custom_css
    ) as demo:
        
        # 标题
        gr.HTML("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 12px; margin-bottom: 20px;">
            <h1 style="margin: 0; font-size: 2.5em;">🎛️ AdaptiveRAG 模块控制测试</h1>
            <p style="margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;">测试模块化配置和实时控制功能</p>
        </div>
        """)
        
        # 创建模块控制标签页
        module_control_tab = create_module_control_tab(engine)
        
        # 添加测试按钮
        with gr.Row():
            test_btn = gr.Button(
                "🧪 运行集成测试",
                variant="primary",
                size="lg"
            )
            
            test_result = gr.HTML(
                value="<div style='padding: 10px;'>点击按钮运行测试</div>"
            )
        
        def run_integration_test():
            """运行集成测试"""
            try:
                success = test_module_control_integration()
                if success:
                    return "<div class='status-success'>✅ 所有集成测试通过！模块控制功能正常工作。</div>"
                else:
                    return "<div class='status-error'>❌ 部分测试失败，请检查日志。</div>"
            except Exception as e:
                return f"<div class='status-error'>❌ 测试异常: {e}</div>"
        
        test_btn.click(
            fn=run_integration_test,
            outputs=[test_result]
        )
    
    return demo


def main():
    """主函数"""
    print("🎯 AdaptiveRAG WebUI 模块控制功能测试")
    print("=" * 80)
    
    # 运行基础测试
    print("📋 第一阶段：基础功能测试")
    success = test_module_control_integration()
    
    if success:
        print("\n🎨 第二阶段：启动测试界面")
        print("=" * 60)
        
        try:
            demo = create_test_interface()
            print("✅ 测试界面创建成功")
            
            print("\n🚀 启动 Gradio 界面...")
            print("   访问地址: http://localhost:7860")
            print("   按 Ctrl+C 停止服务")
            
            demo.launch(
                server_name="0.0.0.0",
                server_port=7860,
                share=False,
                debug=True
            )
            
        except Exception as e:
            print(f"❌ 界面启动失败: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\n❌ 基础测试失败，请先解决问题后再启动界面")


if __name__ == "__main__":
    main()
