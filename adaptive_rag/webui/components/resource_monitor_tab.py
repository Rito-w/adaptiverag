#!/usr/bin/env python3
"""
=== 资源监控标签页组件 ===

展示资源感知优化的实时监控功能
"""

import gradio as gr
from typing import Dict, Any


def create_resource_monitor_tab(engine) -> Dict[str, gr.Component]:
    """创建资源监控标签页"""
    
    with gr.Tab("📊 资源监控") as resource_tab:
        gr.HTML("<h2>🔍 实时资源监控</h2>")

        with gr.Row():
            with gr.Column():
                gr.HTML("<h3>💻 系统资源状态</h3>")
                resource_status = gr.JSON(
                    label="资源状态",
                    value={}
                )

                # 资源指标可视化
                gr.HTML("<h3>📈 资源使用趋势</h3>")
                resource_chart = gr.Plot(
                    label="资源使用趋势"
                )

            with gr.Column():
                gr.HTML("<h3>⚙️ 优化策略</h3>")
                optimization_strategy = gr.JSON(
                    label="当前优化策略",
                    value={}
                )

                # 优化模式选择
                gr.HTML("<h3>🎯 优化模式</h3>")
                optimization_mode = gr.Radio(
                    choices=["performance", "efficiency", "balanced", "conservative"],
                    value="balanced",
                    label="选择优化模式",
                    info="性能优先：最大化性能；效率优先：优化资源使用；平衡模式：性能和效率平衡；保守模式：最小化资源使用"
                )

                # 资源阈值设置
                gr.HTML("<h3>⚡ 资源阈值设置</h3>")
                with gr.Row():
                    cpu_warning = gr.Slider(
                        minimum=50, maximum=95, value=80, step=5,
                        label="CPU警告阈值 (%)"
                    )
                    cpu_critical = gr.Slider(
                        minimum=80, maximum=99, value=95, step=1,
                        label="CPU临界阈值 (%)"
                    )
                
                with gr.Row():
                    memory_warning = gr.Slider(
                        minimum=50, maximum=95, value=85, step=5,
                        label="内存警告阈值 (%)"
                    )
                    memory_critical = gr.Slider(
                        minimum=80, maximum=99, value=95, step=1,
                        label="内存临界阈值 (%)"
                    )

        # 资源使用详情
        with gr.Row():
            with gr.Column():
                gr.HTML("<h3>📊 资源使用详情</h3>")
                resource_details = gr.JSON(
                    label="详细资源信息",
                    value={}
                )

            with gr.Column():
                gr.HTML("<h3>🎯 优化建议</h3>")
                optimization_suggestions = gr.HTML(
                    value="<p>等待资源数据...</p>",
                    label="优化建议"
                )

        # 控制按钮
        with gr.Row():
            refresh_resource_btn = gr.Button("🔄 刷新资源状态", variant="secondary")
            update_thresholds_btn = gr.Button("⚡ 更新阈值", variant="primary")
            clear_cache_btn = gr.Button("🗑️ 清空缓存", variant="secondary")

        # 状态信息
        status_info = gr.Textbox(
            label="状态信息",
            value="资源监控已启动",
            interactive=False
        )

    return {
        "resource_tab": resource_tab,
        "resource_status": resource_status,
        "resource_chart": resource_chart,
        "optimization_strategy": optimization_strategy,
        "optimization_mode": optimization_mode,
        "cpu_warning": cpu_warning,
        "cpu_critical": cpu_critical,
        "memory_warning": memory_warning,
        "memory_critical": memory_critical,
        "resource_details": resource_details,
        "optimization_suggestions": optimization_suggestions,
        "refresh_resource_btn": refresh_resource_btn,
        "update_thresholds_btn": update_thresholds_btn,
        "clear_cache_btn": clear_cache_btn,
        "status_info": status_info
    }


def update_resource_status(engine):
    """更新资源状态"""
    try:
        analytics = engine.get_resource_analytics()
        return analytics
    except Exception as e:
        return {"error": f"获取资源状态失败: {str(e)}"}


def update_optimization_suggestions(resource_status):
    """更新优化建议"""
    if not resource_status or "error" in resource_status:
        return "<p>无法获取资源状态</p>"
    
    current_status = resource_status.get('current_status', {})
    current_metrics = resource_status.get('current_metrics', {})
    
    suggestions = []
    
    # CPU建议
    cpu_status = current_status.get('cpu', 'normal')
    cpu_usage = current_metrics.get('cpu_usage', 0)
    if cpu_status == 'critical':
        suggestions.append("🔴 <strong>CPU使用率过高</strong>：建议切换到保守模式或减少并发查询")
    elif cpu_status == 'warning':
        suggestions.append("🟡 <strong>CPU使用率较高</strong>：建议使用效率优先模式")
    
    # 内存建议
    memory_status = current_status.get('memory', 'normal')
    memory_usage = current_metrics.get('memory_usage', 0)
    if memory_status == 'critical':
        suggestions.append("🔴 <strong>内存使用率过高</strong>：建议清空缓存或重启系统")
    elif memory_status == 'warning':
        suggestions.append("🟡 <strong>内存使用率较高</strong>：建议减少批次大小")
    
    # GPU建议
    gpu_status = current_status.get('gpu', 'normal')
    gpu_usage = current_metrics.get('gpu_usage', 0)
    if gpu_status == 'critical':
        suggestions.append("🔴 <strong>GPU使用率过高</strong>：建议禁用GPU加速")
    elif gpu_status == 'warning':
        suggestions.append("🟡 <strong>GPU使用率较高</strong>：建议减少GPU密集型操作")
    
    # 资源充足时的建议
    if all(status == 'normal' for status in current_status.values()):
        suggestions.append("🟢 <strong>资源充足</strong>：可以使用性能优先模式获得最佳体验")
    
    if not suggestions:
        suggestions.append("📊 <strong>系统运行正常</strong>：当前资源使用在合理范围内")
    
    return "<br>".join(suggestions)


def update_thresholds(engine, cpu_warn, cpu_crit, mem_warn, mem_crit):
    """更新资源阈值"""
    try:
        from adaptive_rag.core.resource_aware_optimizer import ResourceThresholds
        
        thresholds = ResourceThresholds(
            cpu_warning=cpu_warn,
            cpu_critical=cpu_crit,
            memory_warning=mem_warn,
            memory_critical=mem_crit
        )
        
        if hasattr(engine, 'optimization_modules') and 'resource_aware' in engine.optimization_modules:
            engine.optimization_modules['resource_aware'].update_thresholds(thresholds)
            return "✅ 资源阈值已更新"
        else:
            return "❌ 资源感知优化器不可用"
    except Exception as e:
        return f"❌ 更新阈值失败: {str(e)}"


def clear_cache(engine):
    """清空缓存"""
    try:
        if hasattr(engine, 'optimization_modules') and 'performance' in engine.optimization_modules:
            engine.optimization_modules['performance'].clear_caches()
            return "✅ 缓存已清空"
        else:
            return "❌ 性能优化器不可用"
    except Exception as e:
        return f"❌ 清空缓存失败: {str(e)}" 