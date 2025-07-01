#!/usr/bin/env python3
"""
=== 增强版主界面 ===

集成资源感知优化和所有模块功能的完整界面
"""

import gradio as gr
import logging
from pathlib import Path
import sys

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# 导入组件
from .components import (
    create_basic_tab,
    create_query_tab,
    create_analysis_tab,
    create_resource_monitor_tab,
    create_module_overview_tab
)

# 导入引擎
from .engines import EnhancedAdaptiveRAGEngine

logger = logging.getLogger(__name__)


def create_enhanced_interface(config_path: str = "real_config.yaml") -> gr.Blocks:
    """创建增强版主界面"""

    # 初始化增强引擎
    engine = EnhancedAdaptiveRAGEngine(config_path)

    # 自定义 CSS
    custom_css = """
    .gradio-container, .main, .container {
        max-width: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .tab-nav {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 8px 8px 0 0;
    }

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

    body {
        margin: 0 !important;
        max-width: none !important;
        padding: 0 !important;
    }

    .title-container {
        text-align: center;
        margin: 0;
        padding: 30px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        width: 100%;
        box-sizing: border-box;
    }

    .module-card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }

    .resource-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }

    .resource-normal { background-color: #28a745; }
    .resource-warning { background-color: #ffc107; }
    .resource-critical { background-color: #dc3545; }

    .tab-item {
        border-radius: 8px;
        margin: 2px;
        flex-grow: 1;
    }

    .gr-textbox, .gr-slider {
        border-radius: 6px;
        border: 1px solid #e1e5e9;
    }

    .gr-button {
        border-radius: 6px;
        transition: all 0.3s ease;
    }

    @media (max-width: 768px) {
        .gradio-container, .main, .container {
            max-width: 100% !important;
            padding: 10px !important;
        }

        .title-container {
            margin: 0;
            padding: 15px;
        }
    }
    """

    with gr.Blocks(
        title="🧠 增强版智能自适应 RAG 系统",
        css=custom_css
    ) as demo:

        # 标题和介绍
        gr.HTML("""
        <div class="title-container">
            <h1 style="margin: 0 0 10px 0; font-size: 2.5em; font-weight: 700;">
                🧠 增强版智能自适应 RAG 系统
            </h1>
            <h3 style="margin: 0 0 15px 0; font-size: 1.3em; font-weight: 400; opacity: 0.9;">
                集成资源感知优化、多维度决策和性能优化的完整系统
            </h3>
            <p style="margin: 0; font-size: 1em; opacity: 0.8; line-height: 1.6;">
                实时资源监控、自适应策略调整、多目标优化，展示完整的 AdaptiveRAG 创新功能
            </p>
        </div>
        """)

        # 创建标签页
        with gr.Tabs():
            # 模块概览标签页
            module_components = create_module_overview_tab(engine)
            
            # 资源监控标签页
            resource_components = create_resource_monitor_tab(engine)
            
            # 基础配置标签页
            basic_components = create_basic_tab(engine)
            
            # 智能检索标签页
            query_components = create_query_tab(engine)
            
            # 结果分析标签页
            analysis_components = create_analysis_tab(engine)

        # 绑定事件处理函数
        bind_events(engine, module_components, resource_components, 
                   basic_components, query_components, analysis_components)

    return demo


def bind_events(engine, module_components, resource_components, 
               basic_components, query_components, analysis_components):
    """绑定事件处理函数"""
    
    # 模块概览事件
    module_components["refresh_modules_btn"].click(
        fn=lambda: engine.get_module_status(),
        outputs=[module_components["module_status"]]
    )

    # 资源监控事件
    def update_resource_status():
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
        if cpu_status == 'critical':
            suggestions.append("🔴 <strong>CPU使用率过高</strong>：建议切换到保守模式或减少并发查询")
        elif cpu_status == 'warning':
            suggestions.append("🟡 <strong>CPU使用率较高</strong>：建议使用效率优先模式")
        
        # 内存建议
        memory_status = current_status.get('memory', 'normal')
        if memory_status == 'critical':
            suggestions.append("🔴 <strong>内存使用率过高</strong>：建议清空缓存或重启系统")
        elif memory_status == 'warning':
            suggestions.append("🟡 <strong>内存使用率较高</strong>：建议减少批次大小")
        
        # GPU建议
        gpu_status = current_status.get('gpu', 'normal')
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

    def update_thresholds(cpu_warn, cpu_crit, mem_warn, mem_crit):
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

    def clear_cache():
        """清空缓存"""
        try:
            if hasattr(engine, 'optimization_modules') and 'performance' in engine.optimization_modules:
                engine.optimization_modules['performance'].clear_caches()
                return "✅ 缓存已清空"
            else:
                return "❌ 性能优化器不可用"
        except Exception as e:
            return f"❌ 清空缓存失败: {str(e)}"

    # 绑定资源监控事件
    resource_components["refresh_resource_btn"].click(
        fn=update_resource_status,
        outputs=[resource_components["resource_status"]]
    )

    resource_components["update_thresholds_btn"].click(
        fn=update_thresholds,
        inputs=[
            resource_components["cpu_warning"],
            resource_components["cpu_critical"],
            resource_components["memory_warning"],
            resource_components["memory_critical"]
        ],
        outputs=[resource_components["status_info"]]
    )

    resource_components["clear_cache_btn"].click(
        fn=clear_cache,
        outputs=[resource_components["status_info"]]
    )

    # 智能检索事件
    def process_query(query, show_details_flag, opt_mode):
        """处理查询"""
        if not query.strip():
            return {}, "请输入有效的查询", {}, {}

        result = engine.process_query(query, show_details_flag, opt_mode)

        # 提取处理流程信息
        flow_info = {}
        for stage_name, stage_data in result["stages"].items():
            flow_info[stage_name] = {
                "处理时间": f"{stage_data.get('processing_time', 0):.3f}s",
                "状态": stage_data.get('status', '✅ 完成')
            }

        flow_info["总处理时间"] = f"{result['total_time']:.3f}s"
        flow_info["处理方法"] = result.get('method', 'unknown')

        # 提取生成的答案
        answer = result.get("answer", "")

        # 提取检索结果
        docs = result.get("retrieved_docs", {})

        # 提取优化信息
        opt_info = result.get("optimization_info", {})

        return flow_info, answer, docs, opt_info

    def clear_inputs():
        """清空输入"""
        return "", {}, "", {}, {}

    # 绑定查询事件
    query_components["search_btn"].click(
        fn=process_query,
        inputs=[
            query_components["query_input"],
            query_components["show_details"],
            resource_components["optimization_mode"]
        ],
        outputs=[
            query_components["process_flow"],
            query_components["generated_answer"],
            query_components["retrieved_docs"],
            query_components["optimization_info"]
        ]
    )

    query_components["clear_btn"].click(
        fn=clear_inputs,
        outputs=[
            query_components["query_input"],
            query_components["process_flow"],
            query_components["generated_answer"],
            query_components["retrieved_docs"],
            query_components["optimization_info"]
        ]
    )


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="启动增强版 AdaptiveRAG WebUI")
    parser.add_argument("--port", type=int, default=7863, help="服务端口")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="服务主机")
    parser.add_argument("--config-path", type=str, default="real_config.yaml", help="配置文件路径")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    parser.add_argument("--share", action="store_true", help="创建公共链接")

    args = parser.parse_args()

    logger.info("🚀 启动增强版 AdaptiveRAG WebUI")
    logger.info(f"📍 地址: http://{args.host}:{args.port}")
    logger.info(f"📁 配置文件: {args.config_path}")
    logger.info(f"🔧 调试模式: {args.debug}")

    # 检查配置文件
    if not Path(args.config_path).exists():
        logger.error(f"❌ 配置文件不存在: {args.config_path}")
        return

    # 创建并启动 WebUI
    demo = create_enhanced_interface(args.config_path)

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
            logger.error(f"❌ 端口 {args.port} 被占用")
            logger.info(f"💡 尝试使用其他端口:")

            # 自动尝试其他端口
            for port in range(args.port + 1, args.port + 10):
                try:
                    logger.info(f"🔄 尝试端口 {port}...")
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
                logger.error(f"❌ 无法找到可用端口，请手动指定端口")
        else:
            raise e


if __name__ == "__main__":
    main() 