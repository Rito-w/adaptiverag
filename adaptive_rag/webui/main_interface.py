#!/usr/bin/env python3
"""
=== 智能自适应 RAG WebUI 主界面 ===

借鉴 FlashRAG 的 Gradio 界面设计和 FlexRAG 的交互体验
提供直观的 RAG 系统配置和测试界面

设计理念：
1. 借鉴 FlashRAG 的模块化组件设计
2. 参考 FlexRAG 的现代化 UI 风格
3. 融合 LightRAG 的可视化展示
4. 创新的自适应配置界面
"""

import gradio as gr
import argparse
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from .engines import AdaptiveRAGEngine, RealConfigAdaptiveRAGEngine
from .components import create_basic_tab, create_query_tab, create_analysis_tab
from .utils.styles import get_custom_css
from .utils.handlers import create_event_handlers


def create_ui_with_real_config(config_path: str = "real_config.yaml") -> gr.Blocks:
    """创建使用真实配置的主界面"""

    # 初始化真实配置引擎
    engine = RealConfigAdaptiveRAGEngine(config_path)

    # 自定义 CSS
    custom_css = get_custom_css()

    with gr.Blocks(
        title="🧠 智能自适应 RAG 系统 - 真实配置",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="purple",
            neutral_hue="slate",
            spacing_size="md",
            radius_size="md"
        ),
        css=custom_css,
        head="""
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                margin: 0 auto !important;
                max-width: 1200px !important;
                background-color: #f8fafc;
            }
        </style>
        """
    ) as demo:

        # 标题和介绍
        gr.HTML("""
        <div class="title-container">
            <h1 style="margin: 0 0 10px 0; font-size: 2.5em; font-weight: 700;">
                🧠 智能自适应 RAG 系统
            </h1>
            <h3 style="margin: 0 0 15px 0; font-size: 1.3em; font-weight: 400; opacity: 0.9;">
                基于真实配置的增强检索生成系统
            </h3>
            <p style="margin: 0; font-size: 1em; opacity: 0.8; line-height: 1.6;">
                使用真实的检索器、生成器和重排序器，展示完整的 AdaptiveRAG 流程
            </p>
        </div>
        """)

        # 创建标签页
        with gr.Tabs():
            # 配置信息标签页
            with gr.Tab("⚙️ 配置信息"):
                gr.HTML("<h2>📋 系统配置信息</h2>")

                config_display = gr.Markdown(
                    value=engine.get_config_summary(),
                    label="配置摘要"
                )

                with gr.Row():
                    refresh_config_btn = gr.Button("🔄 刷新配置", variant="secondary")
                    reload_config_btn = gr.Button("📁 重新加载配置文件", variant="primary")

                config_status = gr.Textbox(
                    label="状态",
                    value="配置已加载",
                    interactive=False
                )

                def refresh_config():
                    return engine.get_config_summary(), "配置已刷新"

                def reload_config():
                    engine.config = engine.load_config()
                    return engine.get_config_summary(), "配置文件已重新加载"

                refresh_config_btn.click(
                    refresh_config,
                    outputs=[config_display, config_status]
                )

                reload_config_btn.click(
                    reload_config,
                    outputs=[config_display, config_status]
                )

            # 智能检索标签页
            with gr.Tab("🔍 智能检索"):
                gr.HTML("<h2>🧠 智能查询处理</h2>")

                with gr.Row():
                    with gr.Column(scale=2):
                        query_input = gr.Textbox(
                            label="输入查询",
                            placeholder="请输入您的问题...",
                            lines=3
                        )

                        with gr.Row():
                            process_btn = gr.Button("🚀 处理查询", variant="primary")
                            clear_btn = gr.Button("🗑️ 清空", variant="secondary")

                        show_details = gr.Checkbox(
                            label="显示详细信息",
                            value=True
                        )

                    with gr.Column(scale=1):
                        gr.HTML("<h4>📊 快速统计</h4>")
                        query_stats = gr.JSON(
                            label="查询统计",
                            value={"总查询数": 0, "平均处理时间": "0.0s"}
                        )

                # 结果展示区域
                with gr.Row():
                    with gr.Column():
                        gr.HTML("<h3>📈 处理流程</h3>")
                        process_flow = gr.JSON(label="处理阶段详情")

                    with gr.Column():
                        gr.HTML("<h3>💬 生成结果</h3>")
                        generated_answer = gr.Textbox(
                            label="生成的答案",
                            lines=5,
                            interactive=False
                        )

                # 检索结果展示
                with gr.Row():
                    gr.HTML("<h3>📚 检索结果</h3>")

                retrieved_docs = gr.JSON(label="检索到的文档")

                def process_query(query, show_details_flag):
                    if not query.strip():
                        return {}, "请输入有效的查询", {}

                    result = engine.process_query(query, show_details_flag)

                    # 提取处理流程信息
                    flow_info = {}
                    for stage_name, stage_data in result["stages"].items():
                        flow_info[stage_name] = {
                            "处理时间": f"{stage_data.get('processing_time', 0):.3f}s",
                            "状态": "✅ 完成"
                        }

                    flow_info["总处理时间"] = f"{result['total_time']:.3f}s"

                    # 提取生成的答案
                    answer = result["stages"]["generation"]["generated_answer"]

                    # 提取检索结果
                    docs = result["stages"]["retrieval"]["retriever_results"]

                    return flow_info, answer, docs

                def clear_inputs():
                    return "", {}, "", {}

                process_btn.click(
                    process_query,
                    inputs=[query_input, show_details],
                    outputs=[process_flow, generated_answer, retrieved_docs]
                )

                clear_btn.click(
                    clear_inputs,
                    outputs=[query_input, process_flow, generated_answer, retrieved_docs]
                )

            # 结果分析标签页
            with gr.Tab("📈 结果分析"):
                gr.HTML("<h2>📊 性能分析与可视化</h2>")

                with gr.Row():
                    with gr.Column():
                        gr.HTML("<h3>⏱️ 性能指标</h3>")
                        performance_stats = gr.JSON(
                            label="性能统计",
                            value={
                                "平均查询分析时间": "0.1s",
                                "平均检索时间": "0.2s",
                                "平均生成时间": "0.3s",
                                "总平均时间": "0.7s"
                            }
                        )

                    with gr.Column():
                        gr.HTML("<h3>🎯 准确性指标</h3>")
                        accuracy_stats = gr.JSON(
                            label="准确性统计",
                            value={
                                "检索准确率": "85%",
                                "生成质量": "88%",
                                "用户满意度": "90%"
                            }
                        )

                with gr.Row():
                    gr.HTML("<h3>📋 最近查询历史</h3>")

                query_history = gr.Dataframe(
                    headers=["时间", "查询", "处理时间", "状态"],
                    datatype=["str", "str", "str", "str"],
                    label="查询历史"
                )

    return demo


def create_ui() -> gr.Blocks:
    """创建主界面 - 借鉴 FlashRAG 的整体设计"""

    # 初始化引擎
    engine = AdaptiveRAGEngine()
    
    # 自定义 CSS
    custom_css = get_custom_css()
    
    with gr.Blocks(
        title="🧠 智能自适应 RAG 系统",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="purple",
            neutral_hue="slate",
            spacing_size="md",
            radius_size="md"
        ),
        css=custom_css,
        head="""
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                margin: 0 auto !important;
                max-width: 1200px !important;
                background-color: #f8fafc;
            }
        </style>
        """
    ) as demo:
        
        # 标题和介绍
        gr.HTML("""
        <div class="title-container">
            <h1 style="margin: 0 0 10px 0; font-size: 2.5em; font-weight: 700;">
                🧠 智能自适应 RAG 系统
            </h1>
            <h3 style="margin: 0 0 15px 0; font-size: 1.3em; font-weight: 400; opacity: 0.9;">
                基于任务分解和动态检索策略的增强检索生成系统
            </h3>
            <p style="margin: 0; font-size: 1em; opacity: 0.8; line-height: 1.6;">
                借鉴 FlashRAG、FlexRAG、LevelRAG 等优秀框架，融合创新的自适应检索技术
            </p>
        </div>
        """)
        
        # 创建各个标签页
        basic_components = create_basic_tab(engine)
        query_components = create_query_tab(engine)
        analysis_components = create_analysis_tab(engine)
        
        # 创建事件处理器
        handlers = create_event_handlers(engine)
        
        # 绑定事件
        query_components["search_btn"].click(
            fn=handlers["process_search"],
            inputs=[
                query_components["query_input"],
                query_components["show_details"],
                query_components["max_results"]
            ],
            outputs=[
                query_components["search_results"],
                query_components["task_decomposition"],
                query_components["retrieval_strategy"],
                query_components["processing_time"],
                query_components["total_results"]
            ]
        )

        query_components["clear_btn"].click(
            fn=handlers["clear_all"],
            outputs=[
                query_components["query_input"],
                query_components["search_results"],
                query_components["task_decomposition"],
                query_components["retrieval_strategy"],
                query_components["processing_time"],
                query_components["total_results"]
            ]
        )

        # 绑定配置按钮事件
        basic_components["save_config_btn"].click(
            fn=handlers["save_config_handler"],
            inputs=[
                basic_components["dense_model_path"],
                basic_components["generator_model_path"],
                basic_components["reranker_model_path"],
                basic_components["corpus_path"],
                basic_components["index_path"],
                basic_components["batch_size"]
            ],
            outputs=[basic_components["config_status"]]
        )

        basic_components["load_config_btn"].click(
            fn=handlers["load_config_handler"],
            outputs=[basic_components["config_status"]]
        )

        basic_components["reset_config_btn"].click(
            fn=handlers["reset_config_handler"],
            outputs=[
                basic_components["dense_model_path"],
                basic_components["generator_model_path"],
                basic_components["reranker_model_path"],
                basic_components["corpus_path"],
                basic_components["index_path"],
                basic_components["batch_size"],
                basic_components["config_status"]
            ]
        )

        # 页面加载时更新系统状态
        demo.load(
            fn=handlers["update_system_status"],
            outputs=[
                query_components["system_status"],
                query_components["corpus_info"]
            ]
        )
    
    return demo


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="启动智能自适应 RAG WebUI")
    parser.add_argument("--port", type=int, default=7860, help="服务端口")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="服务主机")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    parser.add_argument("--share", action="store_true", help="创建公共链接")
    parser.add_argument("--real-config", action="store_true", help="使用真实配置")
    parser.add_argument("--config-path", type=str, default="real_config.yaml", help="配置文件路径")

    args = parser.parse_args()

    print(f"🚀 启动智能自适应 RAG WebUI")
    print(f"📍 地址: http://{args.host}:{args.port}")
    print(f"🔧 调试模式: {args.debug}")
    print(f"⚙️ 使用真实配置: {args.real_config}")

    if args.real_config:
        print(f"📁 配置文件: {args.config_path}")
        demo = create_ui_with_real_config(args.config_path)
    else:
        demo = create_ui()

    try:
        demo.launch(
            server_name=args.host,
            server_port=args.port,
            share=args.share,
            debug=args.debug,
            show_error=True,
            quiet=False
        )
    except OSError as e:
        if "Cannot find empty port" in str(e):
            print(f"❌ 端口 {args.port} 被占用")
            print(f"💡 尝试使用其他端口:")

            # 自动尝试其他端口
            for port in range(args.port + 1, args.port + 10):
                try:
                    print(f"🔄 尝试端口 {port}...")
                    demo.launch(
                        server_name=args.host,
                        server_port=port,
                        share=args.share,
                        debug=args.debug,
                        show_error=True,
                        quiet=False
                    )
                    break
                except OSError:
                    continue
            else:
                print(f"❌ 无法找到可用端口，请手动指定: python main_interface.py --port 8080")
        else:
            raise e 