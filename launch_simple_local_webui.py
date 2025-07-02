#!/usr/bin/env python3
"""
=== 简化版本地模型 WebUI ===

专门用于解决界面加载问题的简化版本
"""

import sys
import argparse
import os
import gradio as gr
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def create_simple_interface():
    """创建简化的界面"""
    
    # 尝试导入本地模型引擎
    try:
        from adaptive_rag.webui.engines.local_model_engine import LocalModelEngine
        engine = LocalModelEngine()
        print("✅ 本地模型引擎加载成功")
        engine_loaded = True
    except Exception as e:
        print(f"❌ 本地模型引擎加载失败: {e}")
        engine = None
        engine_loaded = False
    
    # 创建简化界面
    with gr.Blocks(
        title="🏠 AdaptiveRAG 本地模型版",
        theme=gr.themes.Soft()
    ) as demo:
        
        # 标题
        gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h1>🏠 AdaptiveRAG 本地模型版</h1>
            <p>使用 /root/autodl-tmp 下的真实模型和数据</p>
        </div>
        """)
        
        # 状态显示
        if engine_loaded:
            status_html = """
            <div style="background: #d4edda; padding: 15px; border-radius: 8px; margin: 10px 0;">
                <h3>✅ 系统状态</h3>
                <ul>
                    <li>🤖 Qwen2.5-1.5B-Instruct: 已加载</li>
                    <li>🎯 BGE-reranker-base: 已加载</li>
                    <li>📊 HotpotQA数据: 1000个文档已加载</li>
                    <li>🔍 BM25索引: 已缓存</li>
                </ul>
            </div>
            """
        else:
            status_html = """
            <div style="background: #f8d7da; padding: 15px; border-radius: 8px; margin: 10px 0;">
                <h3>❌ 系统状态</h3>
                <p>本地模型引擎加载失败，请检查配置</p>
            </div>
            """
        
        gr.HTML(status_html)
        
        # 查询测试区域
        with gr.Row():
            with gr.Column():
                query_input = gr.Textbox(
                    label="输入查询",
                    placeholder="例如：什么是人工智能？",
                    lines=2
                )
                
                with gr.Row():
                    submit_btn = gr.Button("🔍 提交查询", variant="primary")
                    clear_btn = gr.Button("🗑️ 清空")
        
        # 结果显示区域
        with gr.Row():
            with gr.Column():
                result_output = gr.Textbox(
                    label="查询结果",
                    lines=10,
                    interactive=False
                )
                
                details_output = gr.JSON(
                    label="详细信息",
                    visible=False
                )
        
        # 模块控制区域
        if engine_loaded:
            with gr.Accordion("🎛️ 模块控制", open=False):
                with gr.Row():
                    task_decomposer = gr.Checkbox(label="任务分解器", value=True)
                    keyword_retriever = gr.Checkbox(label="关键词检索", value=True)
                    dense_retriever = gr.Checkbox(label="密集检索", value=False)
                    context_reranker = gr.Checkbox(label="重排序器", value=True)
                    adaptive_generator = gr.Checkbox(label="生成器", value=True)
                
                update_modules_btn = gr.Button("🔄 更新模块配置")
        
        # 事件处理
        def process_query(query):
            if not engine_loaded:
                return "❌ 引擎未加载，无法处理查询", {}
            
            if not query.strip():
                return "⚠️ 请输入查询内容", {}
            
            try:
                result = engine.process_query_with_modules(query)
                
                # 格式化输出
                answer = result.get('generated_answer', '无法生成答案')
                steps = result.get('steps', [])
                total_time = result.get('total_time', 0)
                
                formatted_result = f"""
🤖 生成答案：
{answer}

📋 处理步骤：
{chr(10).join([f"• {step}" for step in steps])}

⏱️ 处理时间：{total_time:.2f}秒
                """
                
                return formatted_result.strip(), result
                
            except Exception as e:
                return f"❌ 处理失败: {str(e)}", {"error": str(e)}
        
        def update_modules(task_dec, keyword_ret, dense_ret, context_rer, adaptive_gen):
            if not engine_loaded:
                return "❌ 引擎未加载"
            
            try:
                config = {
                    "task_decomposer": task_dec,
                    "keyword_retriever": keyword_ret,
                    "dense_retriever": dense_ret,
                    "context_reranker": context_rer,
                    "adaptive_generator": adaptive_gen
                }
                
                success = engine.update_module_config(config)
                if success:
                    enabled_count = sum(config.values())
                    return f"✅ 模块配置已更新，启用 {enabled_count} 个模块"
                else:
                    return "❌ 模块配置更新失败"
                    
            except Exception as e:
                return f"❌ 更新失败: {str(e)}"
        
        def clear_inputs():
            return "", "", {}
        
        # 绑定事件
        submit_btn.click(
            fn=process_query,
            inputs=[query_input],
            outputs=[result_output, details_output]
        )
        
        clear_btn.click(
            fn=clear_inputs,
            outputs=[query_input, result_output, details_output]
        )
        
        if engine_loaded:
            update_modules_btn.click(
                fn=update_modules,
                inputs=[task_decomposer, keyword_retriever, dense_retriever, context_reranker, adaptive_generator],
                outputs=[gr.Textbox(label="更新状态", visible=True)]
            )
    
    return demo


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="启动简化版 AdaptiveRAG 本地模型 WebUI")
    parser.add_argument("--port", type=int, default=7864, help="端口号")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="主机地址")
    parser.add_argument("--share", action="store_true", help="创建公共链接")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    
    args = parser.parse_args()
    
    print("🏠 启动简化版 AdaptiveRAG 本地模型 WebUI")
    print("=" * 60)
    print(f"🌐 服务地址: http://{args.host}:{args.port}")
    print(f"🔧 调试模式: {'开启' if args.debug else '关闭'}")
    print("=" * 60)
    
    try:
        # 创建界面
        demo = create_simple_interface()
        
        # 启动服务
        print("🚀 启动 Gradio 服务...")
        demo.launch(
            server_name=args.host,
            server_port=args.port,
            share=args.share,
            debug=args.debug,
            show_error=True,
            quiet=False
        )
        
    except KeyboardInterrupt:
        print("\n👋 用户中断，正在关闭服务...")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
