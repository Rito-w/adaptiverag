#!/usr/bin/env python3
"""
=== 模块概览标签页组件 ===

展示各个优化模块的状态和功能
"""

import gradio as gr
from typing import Dict, Any


def create_module_overview_tab(engine) -> Dict[str, Any]:
    """创建模块概览标签页"""
    
    with gr.Tab("🏗️ 模块概览") as module_tab:
        gr.HTML("<h2>📋 AdaptiveRAG 核心模块架构</h2>")

        # 模块状态概览
        with gr.Row():
            with gr.Column():
                gr.HTML("<h3>🧩 核心模块状态</h3>")
                module_status = gr.JSON(
                    value=engine.get_module_status(),
                    label="模块状态"
                )

            with gr.Column():
                gr.HTML("<h3>🔧 优化模块详情</h3>")
                optimization_details = gr.JSON(
                    value={
                        "资源感知优化器": {
                            "功能": "动态资源监控和自适应策略调整",
                            "创新点": "实时资源状态感知，自动调整检索策略",
                            "应用场景": "高负载环境、资源受限场景"
                        },
                        "多维度优化器": {
                            "功能": "多目标优化和策略权衡分析",
                            "创新点": "准确性、延迟、成本、用户满意度的多维度平衡",
                            "应用场景": "复杂查询、多目标优化需求"
                        },
                        "性能优化器": {
                            "功能": "缓存优化和性能监控",
                            "创新点": "智能缓存策略，性能指标实时监控",
                            "应用场景": "高频查询、性能敏感应用"
                        }
                    },
                    label="优化模块详情"
                )

        # 模块流程图
        gr.HTML("""
        <h3>🔄 增强处理流程</h3>
        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div style="text-align: center; margin: 10px;">
                    <div style="background: #667eea; color: white; padding: 10px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;">📝</div>
                    <strong>查询分析</strong>
                </div>
                <div style="font-size: 24px; color: #667eea;">→</div>
                <div style="text-align: center; margin: 10px;">
                    <div style="background: #764ba2; color: white; padding: 10px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;">🔍</div>
                    <strong>资源感知优化</strong>
                </div>
                <div style="font-size: 24px; color: #764ba2;">→</div>
                <div style="text-align: center; margin: 10px;">
                    <div style="background: #667eea; color: white; padding: 10px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;">⚖️</div>
                    <strong>多维度优化</strong>
                </div>
                <div style="font-size: 24px; color: #667eea;">→</div>
                <div style="text-align: center; margin: 10px;">
                    <div style="background: #764ba2; color: white; padding: 10px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;">🚀</div>
                    <strong>性能优化检索</strong>
                </div>
                <div style="font-size: 24px; color: #764ba2;">→</div>
                <div style="text-align: center; margin: 10px;">
                    <div style="background: #667eea; color: white; padding: 10px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px;">🤖</div>
                    <strong>智能生成</strong>
                </div>
            </div>
        </div>
        """)

        # 模块性能统计
        with gr.Row():
            with gr.Column():
                gr.HTML("<h3>📊 模块性能统计</h3>")
                performance_stats = gr.JSON(
                    value=engine.get_performance_metrics(),
                    label="性能统计"
                )

            with gr.Column():
                gr.HTML("<h3>🎯 模块使用统计</h3>")
                usage_stats = gr.JSON(
                    value={
                        "资源感知优化器": {
                            "调用次数": 0,
                            "平均响应时间": "0.0ms",
                            "成功率": "100%"
                        },
                        "多维度优化器": {
                            "调用次数": 0,
                            "平均响应时间": "0.0ms",
                            "成功率": "100%"
                        },
                        "性能优化器": {
                            "缓存命中率": "0%",
                            "平均查询时间": "0.0ms",
                            "内存使用": "0MB"
                        }
                    },
                    label="使用统计"
                )

        # 刷新按钮
        refresh_modules_btn = gr.Button("🔄 刷新模块状态", variant="secondary")

    return {
        "module_tab": module_tab,
        "module_status": module_status,
        "optimization_details": optimization_details,
        "performance_stats": performance_stats,
        "usage_stats": usage_stats,
        "refresh_modules_btn": refresh_modules_btn
    }


def refresh_module_status(engine):
    """刷新模块状态"""
    try:
        return engine.get_module_status()
    except Exception as e:
        return {"error": f"获取模块状态失败: {str(e)}"}


def refresh_performance_stats(engine):
    """刷新性能统计"""
    try:
        return engine.get_performance_metrics()
    except Exception as e:
        return {"error": f"获取性能统计失败: {str(e)}"} 