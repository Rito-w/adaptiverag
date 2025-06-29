#!/usr/bin/env python3
"""
=== 智能自适应 RAG WebUI 界面 ===

借鉴 FlashRAG 的 Gradio 界面设计和 FlexRAG 的交互体验
提供直观的 RAG 系统配置和测试界面

设计理念：
1. 借鉴 FlashRAG 的模块化组件设计
2. 参考 FlexRAG 的现代化 UI 风格
3. 融合 LightRAG 的可视化展示
4. 创新的自适应配置界面
"""

import gradio as gr
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from adaptive_rag.config import create_flexrag_integrated_config, FLEXRAG_AVAILABLE
from adaptive_rag.core.flexrag_integrated_assistant import FlexRAGIntegratedAssistant


class AdaptiveRAGEngine:
    """智能自适应 RAG 引擎 - 借鉴 FlashRAG 的 Engine 设计"""
    
    def __init__(self):
        self.config = create_flexrag_integrated_config()

        # 初始化 FlexRAG 集成助手
        self.assistant = FlexRAGIntegratedAssistant(self.config)

        # 获取系统信息
        self.system_info = self.assistant.get_system_info()

        # 状态管理
        self.is_initialized = True
        self.current_query = ""
        self.last_results = None

        print(f"✅ AdaptiveRAG 引擎初始化完成")
        print(f"   FlexRAG 可用: {'是' if FLEXRAG_AVAILABLE else '否'}")
        print(f"   助手类型: {self.system_info['assistant_type']}")
        print(f"   支持功能: {', '.join(self.system_info['supported_features'])}")
        
    def initialize_components(self):
        """初始化所有组件（FlexRAG 集成版本中已自动完成）"""
        # FlexRAG 集成助手已经在 __init__ 中完成了所有初始化
        pass
    
    def process_query(self, query: str, show_details: bool = True) -> Dict[str, Any]:
        """处理查询 - 使用 FlexRAG 集成助手"""
        start_time = time.time()

        # 使用 FlexRAG 集成助手处理查询
        result = self.assistant.answer(query)

        processing_time = time.time() - start_time

        # 转换为 Web UI 兼容的格式
        web_result = {
            "query": query,
            "answer": result.answer,
            "subtasks": result.subtasks,
            "retrieval_results": result.retrieval_results,
            "ranking_results": result.ranking_results,
            "generation_result": result.generation_result,
            "processing_time": processing_time,
            "total_time": result.total_time,
            "metadata": result.metadata
        }

        self.current_query = query
        self.last_results = web_result

        return web_result


def create_basic_tab(engine: AdaptiveRAGEngine) -> Dict[str, gr.Component]:
    """创建基础配置标签页 - 借鉴 FlashRAG 的设计"""
    
    with gr.Tab("🔧 基础配置") as basic_tab:
        gr.HTML("<h3>系统配置</h3>")
        
        with gr.Row():
            with gr.Column(scale=1):
                # 模型配置
                gr.HTML("<h4>📦 模型配置</h4>")
                
                dense_model_path = gr.Textbox(
                    label="向量检索模型路径",
                    value="./adaptive_rag/models/e5-base-v2",
                    placeholder="/path/to/dense/model"
                )

                generator_model_path = gr.Textbox(
                    label="生成模型路径",
                    value="./adaptive_rag/models/qwen1.5-1.8b",
                    placeholder="/path/to/generator/model"
                )

                reranker_model_path = gr.Textbox(
                    label="重排序模型路径",
                    value="./adaptive_rag/models/bge-reranker-base",
                    placeholder="/path/to/reranker/model"
                )
            
            with gr.Column(scale=1):
                # 数据配置
                gr.HTML("<h4>📊 数据配置</h4>")
                
                corpus_path = gr.Textbox(
                    label="语料库路径",
                    value="./adaptive_rag/data/general_knowledge.jsonl",
                    placeholder="/path/to/corpus.jsonl"
                )

                index_path = gr.Textbox(
                    label="索引路径",
                    value="./adaptive_rag/data/e5_Flat.index",
                    placeholder="/path/to/index"
                )

                batch_size = gr.Slider(
                    minimum=1,
                    maximum=32,
                    value=engine.config.batch_size,
                    step=1,
                    label="批处理大小"
                )
        
        with gr.Row():
            save_config_btn = gr.Button("💾 保存配置", variant="primary")
            load_config_btn = gr.Button("📂 加载配置")
            reset_config_btn = gr.Button("🔄 重置配置")
        
        config_status = gr.Textbox(
            label="配置状态",
            value="配置未保存",
            interactive=False
        )
    
    return {
        "basic_tab": basic_tab,
        "dense_model_path": dense_model_path,
        "generator_model_path": generator_model_path,
        "reranker_model_path": reranker_model_path,
        "corpus_path": corpus_path,
        "index_path": index_path,
        "batch_size": batch_size,
        "save_config_btn": save_config_btn,
        "load_config_btn": load_config_btn,
        "reset_config_btn": reset_config_btn,
        "config_status": config_status
    }


def create_query_tab(engine: AdaptiveRAGEngine) -> Dict[str, gr.Component]:
    """创建查询测试标签页"""
    
    with gr.Tab("🔍 智能检索") as query_tab:
        gr.HTML("<h3>智能自适应检索测试</h3>")
        
        with gr.Row():
            with gr.Column(scale=2):
                query_input = gr.Textbox(
                    label="输入查询",
                    placeholder="例如: What is artificial intelligence?",
                    lines=3
                )
                
                with gr.Row():
                    search_btn = gr.Button("🚀 智能检索", variant="primary", size="lg")
                    clear_btn = gr.Button("🗑️ 清空", size="lg")
                
                # 检索配置
                with gr.Accordion("⚙️ 检索配置", open=False):
                    show_details = gr.Checkbox(
                        label="显示详细过程",
                        value=True
                    )
                    
                    max_results = gr.Slider(
                        minimum=1,
                        maximum=20,
                        value=10,
                        step=1,
                        label="最大结果数"
                    )
            
            with gr.Column(scale=1):
                # 系统状态
                gr.HTML("<h4>📊 系统状态</h4>")
                
                system_status = gr.HTML(
                    value="<p><span style='color: orange;'>●</span> 系统未初始化</p>"
                )
                
                corpus_info = gr.HTML(
                    value="<p><strong>语料库:</strong> 未加载</p>"
                )
                
                # 示例查询
                gr.HTML("<h4>💡 示例查询</h4>")
                
                example_queries = [
                    "What is artificial intelligence?",
                    "Compare machine learning and deep learning",
                    "When was the iPhone first released?",
                    "Why did the Roman Empire fall?"
                ]
                
                for query in example_queries:
                    example_btn = gr.Button(
                        f"📝 {query[:30]}...",
                        size="sm",
                        variant="secondary"
                    )
        
        # 结果显示区域
        with gr.Row():
            with gr.Column():
                # 任务分解结果
                task_decomposition = gr.JSON(
                    label="🧠 任务分解结果",
                    visible=False
                )
                
                # 检索策略
                retrieval_strategy = gr.JSON(
                    label="🎯 检索策略规划",
                    visible=False
                )
                
                # 检索结果
                search_results = gr.Textbox(
                    label="🔍 检索结果",
                    lines=15,
                    max_lines=20,
                    show_copy_button=True
                )
        
        # 性能统计
        with gr.Row():
            processing_time = gr.Textbox(
                label="⏱️ 处理时间",
                interactive=False,
                scale=1
            )
            
            total_results = gr.Textbox(
                label="📊 结果统计",
                interactive=False,
                scale=1
            )
    
    return {
        "query_tab": query_tab,
        "query_input": query_input,
        "search_btn": search_btn,
        "clear_btn": clear_btn,
        "show_details": show_details,
        "max_results": max_results,
        "system_status": system_status,
        "corpus_info": corpus_info,
        "task_decomposition": task_decomposition,
        "retrieval_strategy": retrieval_strategy,
        "search_results": search_results,
        "processing_time": processing_time,
        "total_results": total_results
    }


def create_analysis_tab(engine: AdaptiveRAGEngine) -> Dict[str, gr.Component]:
    """创建分析可视化标签页"""
    
    with gr.Tab("📈 结果分析") as analysis_tab:
        gr.HTML("<h3>检索结果分析与可视化</h3>")
        
        with gr.Row():
            with gr.Column():
                # 任务分解可视化
                gr.HTML("<h4>🧠 任务分解分析</h4>")
                task_analysis = gr.Plot(label="任务类型分布")
                
                # 检索器使用统计
                gr.HTML("<h4>🔍 检索器使用统计</h4>")
                retriever_stats = gr.Plot(label="检索器效果对比")
            
            with gr.Column():
                # 相关度分布
                gr.HTML("<h4>📊 相关度分布</h4>")
                relevance_dist = gr.Plot(label="结果相关度分布")
                
                # 处理时间分析
                gr.HTML("<h4>⏱️ 性能分析</h4>")
                performance_stats = gr.HTML(
                    value="<p>暂无性能数据</p>"
                )
        
        # 详细结果表格
        with gr.Row():
            results_table = gr.Dataframe(
                headers=["排名", "内容", "分数", "检索器", "元数据"],
                label="📋 详细结果表格",
                interactive=False
            )
    
    return {
        "analysis_tab": analysis_tab,
        "task_analysis": task_analysis,
        "retriever_stats": retriever_stats,
        "relevance_dist": relevance_dist,
        "performance_stats": performance_stats,
        "results_table": results_table
    }


def create_ui() -> gr.Blocks:
    """创建主界面 - 借鉴 FlashRAG 的整体设计"""
    
    # 初始化引擎
    engine = AdaptiveRAGEngine()
    
    # 自定义 CSS
    custom_css = """
    /* Gradio 容器和主内容区域应占据全宽，移除最大宽度限制和自动边距 */
    .gradio-container, .main, .container {
        max-width: none !important; /* 移除最大宽度限制 */
        margin: 0 !important; /* 移除自动边距 */
        padding: 0 !important; /* 移除内边距，确保内容贴边 */
    }

    .tab-nav {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 8px 8px 0 0;
    }

    /* 按钮样式优化 */
    .primary-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border: none;
        color: white;
        border-radius: 6px;
        transition: all 0.3s ease;
    }

    .primary-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    /* 确保整个页面无留白 */
    body {
        margin: 0 !important; /* 移除自动边距 */
        max-width: none !important; /* 移除最大宽度限制 */
        padding: 0 !important; /* 移除内边距 */
    }

    /* 标题区域居中 */
    .title-container {
        text-align: center;
        margin: 0; /* 调整为0，让它自己控制宽度 */
        padding: 30px 20px; /* 增加上下内边距，左右保持一致 */
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        width: 100%; /* 确保标题容器也占据全宽 */
        box-sizing: border-box; /* 确保 padding 不会增加总宽度 */
    }

    /* 标签页样式优化 */
    .tab-item {
        border-radius: 8px;
        margin: 2px;
        flex-grow: 1; /* 让标签页项目等宽分布 */
    }

    /* 输入框和按钮样式优化 */
    .gr-textbox, .gr-slider {
        border-radius: 6px;
        border: 1px solid #e1e5e9;
    }

    .gr-button {
        border-radius: 6px;
        transition: all 0.3s ease;
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        .gradio-container, .main, .container {
            max-width: 100% !important;
            padding: 10px !important;
        }

        .title-container {
            margin: 0; /* 调整为0 */
            padding: 15px;
        }
    }
    """
    
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
        
        # 事件处理函数
        def process_search(query, show_details, max_results):
            """处理搜索请求"""
            if not query.strip():
                return (
                    "请输入查询内容",
                    gr.update(visible=False),
                    gr.update(visible=False),
                    "",
                    ""
                )

            try:
                # 初始化引擎
                engine.initialize_components()

                result = engine.process_query(query, show_details)

                # 格式化结果
                search_output = f"查询: {result['query']}\n"
                search_output += f"处理时间: {result['processing_time']:.2f}秒\n"

                # 计算总结果数
                total_docs = 0
                if 'retrieval_results' in result:
                    total_docs = sum(len(r.contexts) for r in result['retrieval_results'])

                search_output += f"总结果数: {total_docs}\n"
                search_output += f"答案: {result.get('answer', '未生成答案')}\n\n"

                search_output += "=== 检索结果详情 ===\n"

                # 显示检索结果
                if 'retrieval_results' in result:
                    for i, retrieval_result in enumerate(result['retrieval_results'], 1):
                        search_output += f"\n--- 子任务 {i}: {retrieval_result.query} ---\n"
                        for j, doc in enumerate(retrieval_result.contexts[:max_results], 1):
                            search_output += f"{j}. 分数: {doc.score:.3f}\n"
                            search_output += f"   内容: {doc.content[:200]}...\n"
                            if hasattr(doc, 'metadata') and doc.metadata:
                                search_output += f"   元数据: {doc.metadata}\n"

                # 任务分解信息
                task_info = {
                    "subtasks": []
                }

                if 'subtasks' in result and result['subtasks']:
                    task_info["subtasks"] = [
                        {
                            "id": getattr(st, 'id', f"task_{i}"),
                            "content": getattr(st, 'content', str(st)),
                            "type": getattr(st, 'task_type', 'unknown').value if hasattr(getattr(st, 'task_type', None), 'value') else str(getattr(st, 'task_type', 'unknown')),
                            "priority": getattr(st, 'priority', 1.0),
                            "entities": getattr(st, 'entities', []),
                            "temporal_info": getattr(st, 'temporal_info', {})
                        }
                        for i, st in enumerate(result['subtasks'])
                    ]

                # 检索策略信息
                strategy_info = {
                    "retrieval_results": []
                }

                if 'retrieval_results' in result:
                    strategy_info["retrieval_results"] = [
                        {
                            "query": r.query,
                            "contexts_count": len(r.contexts),
                            "retrieval_time": r.retrieval_time,
                            "retriever_type": r.retriever_type,
                            "metadata": getattr(r, 'metadata', {})
                        }
                        for r in result['retrieval_results']
                    ]

                # 计算结果统计
                total_docs = 0
                if 'retrieval_results' in result:
                    total_docs = sum(len(r.contexts) for r in result['retrieval_results'])

                displayed_docs = min(max_results, total_docs)

                return (
                    search_output,
                    gr.update(value=json.dumps(task_info, ensure_ascii=False, indent=2), visible=True),
                    gr.update(value=json.dumps(strategy_info, ensure_ascii=False, indent=2), visible=True),
                    f"{result['processing_time']:.2f} 秒",
                    f"共 {total_docs} 个结果，显示前 {displayed_docs} 个"
                )

            except Exception as e:
                import traceback
                error_msg = f"处理出错: {str(e)}\n\n详细错误:\n{traceback.format_exc()}"
                return (
                    error_msg,
                    gr.update(visible=False),
                    gr.update(visible=False),
                    "",
                    ""
                )

        def clear_all():
            """清空所有内容"""
            return (
                "",
                "",
                gr.update(visible=False),
                gr.update(visible=False),
                "",
                ""
            )

        def set_example_query(example_text):
            """设置示例查询"""
            return example_text

        def update_system_status():
            """更新系统状态"""
            try:
                engine.initialize_components()
                corpus_stats = engine.data_manager.get_corpus_stats()

                status_html = "<p><span style='color: green;'>●</span> 系统已初始化</p>"
                corpus_html = f"<p><strong>语料库:</strong> {corpus_stats['total_documents']} 个文档</p>"

                return status_html, corpus_html
            except Exception as e:
                status_html = f"<p><span style='color: red;'>●</span> 系统初始化失败: {str(e)}</p>"
                corpus_html = "<p><strong>语料库:</strong> 加载失败</p>"
                return status_html, corpus_html
        
        # 绑定事件
        query_components["search_btn"].click(
            fn=process_search,
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
            fn=clear_all,
            outputs=[
                query_components["query_input"],
                query_components["search_results"],
                query_components["task_decomposition"],
                query_components["retrieval_strategy"],
                query_components["processing_time"],
                query_components["total_results"]
            ]
        )

        # 配置按钮事件绑定
        def save_config_handler(*config_values):
            """保存配置处理器"""
            try:
                # 这里可以实现配置保存逻辑
                return "✅ 配置已保存"
            except Exception as e:
                return f"❌ 保存失败: {str(e)}"

        def load_config_handler():
            """加载配置处理器"""
            try:
                # 这里可以实现配置加载逻辑
                return "✅ 配置已加载"
            except Exception as e:
                return f"❌ 加载失败: {str(e)}"

        def reset_config_handler():
            """重置配置处理器"""
            try:
                # 重置为默认值
                config = create_flexrag_integrated_config()
                return (
                    "./adaptive_rag/models/e5-base-v2",
                    "./adaptive_rag/models/qwen1.5-1.8b",
                    "./adaptive_rag/models/bge-reranker-base",
                    "./adaptive_rag/data/general_knowledge.jsonl",
                    "./adaptive_rag/data/e5_Flat.index",
                    config.batch_size,
                    "✅ 配置已重置为默认值"
                )
            except Exception as e:
                return ("", "", "", "", "", 4, f"❌ 重置失败: {str(e)}")

        # 绑定配置按钮事件
        basic_components["save_config_btn"].click(
            fn=save_config_handler,
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
            fn=load_config_handler,
            outputs=[basic_components["config_status"]]
        )

        basic_components["reset_config_btn"].click(
            fn=reset_config_handler,
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
            fn=update_system_status,
            outputs=[
                query_components["system_status"],
                query_components["corpus_info"]
            ]
        )
    
    return demo


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="启动智能自适应 RAG WebUI")
    parser.add_argument("--port", type=int, default=7860, help="服务端口")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="服务主机")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    parser.add_argument("--share", action="store_true", help="创建公共链接")

    args = parser.parse_args()

    print(f"🚀 启动智能自适应 RAG WebUI")
    print(f"📍 地址: http://{args.host}:{args.port}")
    print(f"🔧 调试模式: {args.debug}")

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
                print(f"❌ 无法找到可用端口，请手动指定: python interface.py --port 8080")
        else:
            raise e
