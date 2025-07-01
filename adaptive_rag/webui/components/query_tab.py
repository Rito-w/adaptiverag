"""
查询测试标签页组件
"""

import gradio as gr
from typing import Dict, Any


def create_query_tab(engine) -> Dict[str, Any]:
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
                # 处理流程
                process_flow = gr.JSON(
                    label="📈 处理流程",
                    value={}
                )
                
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
            
            with gr.Column():
                # 生成的答案
                generated_answer = gr.Textbox(
                    label="💬 生成的答案",
                    lines=8,
                    interactive=False
                )
                
                # 检索到的文档
                retrieved_docs = gr.JSON(
                    label="📚 检索到的文档",
                    value={}
                )
                
                # 优化信息
                optimization_info = gr.JSON(
                    label="⚙️ 优化信息",
                    value={}
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
        "process_flow": process_flow,
        "task_decomposition": task_decomposition,
        "retrieval_strategy": retrieval_strategy,
        "search_results": search_results,
        "generated_answer": generated_answer,
        "retrieved_docs": retrieved_docs,
        "optimization_info": optimization_info,
        "processing_time": processing_time,
        "total_results": total_results
    } 