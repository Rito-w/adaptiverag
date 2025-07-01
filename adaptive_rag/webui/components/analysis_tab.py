"""
分析可视化标签页组件
"""

import gradio as gr
from typing import Dict, Any


def create_analysis_tab(engine) -> Dict[str, gr.Component]:
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