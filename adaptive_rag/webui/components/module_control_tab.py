#!/usr/bin/env python3
"""
=== 模块控制标签页 ===

提供可视化的模块开关控制界面
"""

import gradio as gr
import logging
from typing import Dict, List, Tuple, Any
import yaml
from pathlib import Path

logger = logging.getLogger(__name__)


def create_module_control_tab(engine) -> gr.Tab:
    """创建模块控制标签页"""
    
    with gr.Tab("🎛️ 模块控制", elem_id="module-control-tab") as tab:
        
        # 标题和说明
        gr.Markdown("""
        # 🎛️ AdaptiveRAG 模块控制中心
        
        在这里您可以实时控制各个模块的启用状态，系统会根据您的设置动态调整功能。
        """)
        
        # 预设配置选择
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 🚀 快速配置")
                preset_dropdown = gr.Dropdown(
                    choices=["basic_mode", "performance_mode", "experimental_mode", "custom"],
                    value="performance_mode",
                    label="预设模式",
                    info="选择预设配置或自定义"
                )
                
                apply_preset_btn = gr.Button(
                    "应用预设配置",
                    variant="primary",
                    elem_classes=["primary-button"]
                )
                
                save_config_btn = gr.Button(
                    "保存当前配置",
                    variant="secondary"
                )
                
                load_config_btn = gr.Button(
                    "重新加载配置",
                    variant="secondary"
                )
            
            with gr.Column(scale=2):
                gr.Markdown("### 📊 系统状态")
                system_status = gr.HTML(
                    value=_get_system_status_html(engine),
                    elem_id="system-status"
                )
        
        gr.Markdown("---")
        
        # 模块控制面板
        gr.Markdown("### 🔧 模块控制面板")
        
        # 核心处理模块
        with gr.Accordion("🧩 核心处理模块", open=True):
            with gr.Row():
                task_decomposer = gr.Checkbox(
                    label="任务分解器",
                    value=True,
                    info="将复杂查询分解为子任务"
                )
                retrieval_planner = gr.Checkbox(
                    label="检索规划器",
                    value=True,
                    info="制定检索策略和权重分配"
                )
                multi_retriever = gr.Checkbox(
                    label="多重检索系统",
                    value=True,
                    info="并行执行多种检索方法"
                )
            
            with gr.Row():
                context_reranker = gr.Checkbox(
                    label="上下文重排器",
                    value=True,
                    info="优化检索结果排序"
                )
                adaptive_generator = gr.Checkbox(
                    label="自适应生成器",
                    value=True,
                    info="生成最终响应"
                )
        
        # 智能分析模块
        with gr.Accordion("🧠 智能分析模块", open=False):
            with gr.Row():
                query_analyzer = gr.Checkbox(
                    label="查询分析器",
                    value=True,
                    info="分析查询复杂度和类型"
                )
                strategy_router = gr.Checkbox(
                    label="策略路由器",
                    value=True,
                    info="动态选择最优检索策略"
                )
                performance_optimizer = gr.Checkbox(
                    label="性能优化器",
                    value=True,
                    info="持续优化系统性能"
                )
            
            with gr.Row():
                intelligent_strategy_learner = gr.Checkbox(
                    label="智能策略学习器",
                    value=False,
                    info="从历史数据学习最优策略（实验性）"
                )
                multi_dimensional_optimizer = gr.Checkbox(
                    label="多维度优化器",
                    value=False,
                    info="多维度决策优化（实验性）"
                )
                resource_aware_optimizer = gr.Checkbox(
                    label="资源感知优化器",
                    value=False,
                    info="资源感知优化（实验性）"
                )
        
        # 检索器模块
        with gr.Accordion("🔍 检索器模块", open=False):
            with gr.Row():
                keyword_retriever = gr.Checkbox(
                    label="关键词检索器",
                    value=True,
                    info="基于关键词的检索"
                )
                dense_retriever = gr.Checkbox(
                    label="密集检索器",
                    value=True,
                    info="基于密集向量的检索"
                )
                web_retriever = gr.Checkbox(
                    label="网络检索器",
                    value=False,
                    info="实时网络搜索（需要API）"
                )
                hybrid_retriever = gr.Checkbox(
                    label="混合检索器",
                    value=True,
                    info="混合检索方法"
                )
        
        # 重排序模块
        with gr.Accordion("🎯 重排序模块", open=False):
            with gr.Row():
                cross_encoder_ranker = gr.Checkbox(
                    label="交叉编码器重排",
                    value=True,
                    info="深度交互重排序"
                )
                colbert_ranker = gr.Checkbox(
                    label="ColBERT重排",
                    value=False,
                    info="高效后期交互（需要模型）"
                )
                gpt_ranker = gr.Checkbox(
                    label="GPT重排",
                    value=False,
                    info="LLM智能重排（需要API）"
                )
        
        # 生成器模块
        with gr.Accordion("✨ 生成器模块", open=False):
            with gr.Row():
                template_generator = gr.Checkbox(
                    label="模板生成器",
                    value=True,
                    info="基于模板的生成"
                )
                freeform_generator = gr.Checkbox(
                    label="自由形式生成器",
                    value=True,
                    info="自由形式生成"
                )
                dialogue_generator = gr.Checkbox(
                    label="对话生成器",
                    value=False,
                    info="对话生成（实验性）"
                )
        
        # 评估和缓存模块
        with gr.Accordion("📊 评估和缓存模块", open=False):
            with gr.Row():
                fact_verification = gr.Checkbox(
                    label="事实验证",
                    value=False,
                    info="事实验证（实验性）"
                )
                confidence_estimation = gr.Checkbox(
                    label="置信度估计",
                    value=True,
                    info="置信度估计"
                )
                result_analyzer = gr.Checkbox(
                    label="结果分析器",
                    value=True,
                    info="结果分析"
                )
            
            with gr.Row():
                semantic_cache = gr.Checkbox(
                    label="语义缓存",
                    value=True,
                    info="语义缓存"
                )
                predictive_cache = gr.Checkbox(
                    label="预测性缓存",
                    value=False,
                    info="预测性缓存（实验性）"
                )
        
        # 用户体验和调试模块
        with gr.Accordion("🎨 用户体验和调试模块", open=False):
            with gr.Row():
                personalization = gr.Checkbox(
                    label="个性化",
                    value=False,
                    info="个性化（实验性）"
                )
                multimodal_support = gr.Checkbox(
                    label="多模态支持",
                    value=False,
                    info="多模态支持（实验性）"
                )
                debug_mode = gr.Checkbox(
                    label="调试模式",
                    value=False,
                    info="调试模式"
                )
            
            with gr.Row():
                performance_monitoring = gr.Checkbox(
                    label="性能监控",
                    value=True,
                    info="性能监控"
                )
                logging_enhanced = gr.Checkbox(
                    label="增强日志",
                    value=True,
                    info="增强日志"
                )
        
        gr.Markdown("---")
        
        # 操作按钮
        with gr.Row():
            apply_changes_btn = gr.Button(
                "🚀 应用更改",
                variant="primary",
                size="lg",
                elem_classes=["primary-button"]
            )
            reset_btn = gr.Button(
                "🔄 重置为默认",
                variant="secondary",
                size="lg"
            )
        
        # 状态显示
        operation_status = gr.HTML(
            value="<div class='status-ready'>✅ 系统就绪，等待配置更改</div>",
            elem_id="operation-status"
        )
        
        # 收集所有模块控件
        module_controls = {
            "task_decomposer": task_decomposer,
            "retrieval_planner": retrieval_planner,
            "multi_retriever": multi_retriever,
            "context_reranker": context_reranker,
            "adaptive_generator": adaptive_generator,
            "query_analyzer": query_analyzer,
            "strategy_router": strategy_router,
            "performance_optimizer": performance_optimizer,
            "intelligent_strategy_learner": intelligent_strategy_learner,
            "multi_dimensional_optimizer": multi_dimensional_optimizer,
            "resource_aware_optimizer": resource_aware_optimizer,
            "keyword_retriever": keyword_retriever,
            "dense_retriever": dense_retriever,
            "web_retriever": web_retriever,
            "hybrid_retriever": hybrid_retriever,
            "cross_encoder_ranker": cross_encoder_ranker,
            "colbert_ranker": colbert_ranker,
            "gpt_ranker": gpt_ranker,
            "template_generator": template_generator,
            "freeform_generator": freeform_generator,
            "dialogue_generator": dialogue_generator,
            "fact_verification": fact_verification,
            "confidence_estimation": confidence_estimation,
            "result_analyzer": result_analyzer,
            "semantic_cache": semantic_cache,
            "predictive_cache": predictive_cache,
            "personalization": personalization,
            "multimodal_support": multimodal_support,
            "debug_mode": debug_mode,
            "performance_monitoring": performance_monitoring,
            "logging_enhanced": logging_enhanced
        }
        
        # 事件处理
        _setup_module_control_events(
            engine, module_controls, preset_dropdown,
            apply_preset_btn, apply_changes_btn, reset_btn,
            save_config_btn, load_config_btn,
            system_status, operation_status
        )
    
    return tab


def _get_system_status_html(engine) -> str:
    """获取系统状态HTML"""
    try:
        # 获取当前模块状态
        if hasattr(engine, 'module_manager'):
            enabled_modules = engine.module_manager.get_enabled_modules()
            total_modules = len(engine.module_manager.modules)
            enabled_count = len(enabled_modules)
        else:
            enabled_count = 15  # 默认值
            total_modules = 31
        
        status_html = f"""
        <div class="system-status-card">
            <h4>🎯 系统概览</h4>
            <div class="status-item">
                <span class="status-label">启用模块:</span>
                <span class="status-value">{enabled_count}/{total_modules}</span>
            </div>
            <div class="status-item">
                <span class="status-label">启用率:</span>
                <span class="status-value">{enabled_count/total_modules*100:.1f}%</span>
            </div>
            <div class="status-item">
                <span class="status-label">系统状态:</span>
                <span class="status-value status-ready">🟢 就绪</span>
            </div>
        </div>
        """
        return status_html
    except Exception as e:
        return f"<div class='error'>状态获取失败: {e}</div>"


def _setup_module_control_events(engine, module_controls, preset_dropdown,
                                apply_preset_btn, apply_changes_btn, reset_btn,
                                save_config_btn, load_config_btn,
                                system_status, operation_status):
    """设置模块控制事件"""
    
    def apply_preset(preset_name):
        """应用预设配置"""
        try:
            # 预设配置映射
            presets = {
                "basic_mode": {
                    "task_decomposer": True, "retrieval_planner": True, "multi_retriever": True,
                    "context_reranker": False, "adaptive_generator": True, "query_analyzer": True,
                    "strategy_router": False, "performance_optimizer": True, "intelligent_strategy_learner": False,
                    "multi_dimensional_optimizer": False, "resource_aware_optimizer": False,
                    "keyword_retriever": True, "dense_retriever": True, "web_retriever": False, "hybrid_retriever": True,
                    "cross_encoder_ranker": False, "colbert_ranker": False, "gpt_ranker": False,
                    "template_generator": True, "freeform_generator": True, "dialogue_generator": False,
                    "fact_verification": False, "confidence_estimation": True, "result_analyzer": True,
                    "semantic_cache": True, "predictive_cache": False, "personalization": False,
                    "multimodal_support": False, "debug_mode": False, "performance_monitoring": True, "logging_enhanced": True
                },
                "performance_mode": {
                    "task_decomposer": True, "retrieval_planner": True, "multi_retriever": True,
                    "context_reranker": True, "adaptive_generator": True, "query_analyzer": True,
                    "strategy_router": True, "performance_optimizer": True, "intelligent_strategy_learner": False,
                    "multi_dimensional_optimizer": False, "resource_aware_optimizer": False,
                    "keyword_retriever": True, "dense_retriever": True, "web_retriever": True, "hybrid_retriever": True,
                    "cross_encoder_ranker": True, "colbert_ranker": False, "gpt_ranker": False,
                    "template_generator": True, "freeform_generator": True, "dialogue_generator": False,
                    "fact_verification": False, "confidence_estimation": True, "result_analyzer": True,
                    "semantic_cache": True, "predictive_cache": False, "personalization": False,
                    "multimodal_support": False, "debug_mode": False, "performance_monitoring": True, "logging_enhanced": True
                },
                "experimental_mode": {
                    module: True for module in module_controls.keys()
                }
            }
            
            if preset_name in presets:
                preset_config = presets[preset_name]
                updates = []
                for module_name, control in module_controls.items():
                    updates.append(gr.update(value=preset_config.get(module_name, False)))
                
                status_msg = f"<div class='status-success'>✅ 已应用 {preset_name} 预设配置</div>"
                updates.append(status_msg)
                return updates
            else:
                return [gr.update() for _ in module_controls] + ["<div class='status-error'>❌ 未知的预设配置</div>"]
                
        except Exception as e:
            logger.error(f"应用预设配置失败: {e}")
            return [gr.update() for _ in module_controls] + [f"<div class='status-error'>❌ 应用预设失败: {e}</div>"]
    
    def apply_module_changes(*module_states):
        """应用模块更改"""
        try:
            # 更新引擎配置
            module_config = dict(zip(module_controls.keys(), module_states))

            if hasattr(engine, 'update_module_config'):
                success = engine.update_module_config(module_config)
                if not success:
                    return "<div class='status-error'>❌ 模块配置更新失败</div>", _get_system_status_html(engine)

            enabled_count = sum(1 for state in module_states if state)
            total_count = len(module_states)

            # 显示详细的模块变更信息
            enabled_modules = [name for name, state in zip(module_controls.keys(), module_states) if state]
            disabled_modules = [name for name, state in zip(module_controls.keys(), module_states) if not state]

            status_msg = f"""
            <div class='status-success'>
                ✅ 配置已更新！启用模块: {enabled_count}/{total_count}
                <br><strong>启用的模块:</strong> {', '.join(enabled_modules[:5])}{'...' if len(enabled_modules) > 5 else ''}
                <br><strong>禁用的模块:</strong> {', '.join(disabled_modules[:5])}{'...' if len(disabled_modules) > 5 else ''}
                <br><em>现在可以在查询标签页中测试效果！</em>
            </div>
            """
            system_status_html = _get_system_status_html(engine)

            return status_msg, system_status_html

        except Exception as e:
            logger.error(f"应用模块更改失败: {e}")
            return f"<div class='status-error'>❌ 更新失败: {e}</div>", _get_system_status_html(engine)
    
    def reset_to_default():
        """重置为默认配置"""
        try:
            # 重置为性能模式
            return apply_preset("performance_mode")
        except Exception as e:
            logger.error(f"重置配置失败: {e}")
            return [gr.update() for _ in module_controls] + [f"<div class='status-error'>❌ 重置失败: {e}</div>"]
    
    # 绑定事件
    apply_preset_btn.click(
        fn=apply_preset,
        inputs=[preset_dropdown],
        outputs=list(module_controls.values()) + [operation_status]
    )
    
    apply_changes_btn.click(
        fn=apply_module_changes,
        inputs=list(module_controls.values()),
        outputs=[operation_status, system_status]
    )
    
    reset_btn.click(
        fn=reset_to_default,
        outputs=list(module_controls.values()) + [operation_status]
    )
