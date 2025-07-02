#!/usr/bin/env python3
"""
=== 真实模型查询标签页 ===

展示真实模型和模块开关的实际效果
"""

import gradio as gr
import logging
from typing import Dict, List, Any
import json

logger = logging.getLogger(__name__)


def create_real_model_query_tab(engine) -> gr.Tab:
    """创建真实模型查询标签页"""
    
    with gr.Tab("🔬 真实模型测试", elem_id="real-model-query-tab") as tab:
        
        # 标题和说明
        gr.Markdown("""
        # 🔬 真实模型效果测试
        
        在这里您可以测试真实的检索器、重排序器和生成器，直观看到模块开关的实际效果。
        
        **💡 使用提示：**
        1. 先在"🎛️ 模块控制"标签页中配置模块
        2. 在下方输入查询，观察不同模块组合的效果
        3. 对比启用/禁用不同模块时的结果差异
        """)
        
        with gr.Row():
            # 左侧：查询输入和控制
            with gr.Column(scale=1):
                gr.Markdown("### 🔍 查询输入")
                
                query_input = gr.Textbox(
                    label="输入您的查询",
                    placeholder="例如：什么是人工智能？",
                    lines=2
                )
                
                with gr.Row():
                    submit_btn = gr.Button(
                        "🚀 执行查询",
                        variant="primary",
                        size="lg"
                    )
                    
                    clear_btn = gr.Button(
                        "🗑️ 清空",
                        variant="secondary"
                    )
                
                # 当前模块状态显示
                gr.Markdown("### 📊 当前模块状态")
                current_modules = gr.HTML(
                    value=_get_current_modules_html(engine),
                    elem_id="current-modules-status"
                )
                
                refresh_modules_btn = gr.Button(
                    "🔄 刷新模块状态",
                    variant="secondary",
                    size="sm"
                )
            
            # 右侧：结果显示
            with gr.Column(scale=2):
                gr.Markdown("### 📋 处理结果")
                
                # 处理步骤
                processing_steps = gr.HTML(
                    value="<div class='info-box'>等待查询输入...</div>",
                    elem_id="processing-steps"
                )
                
                # 检索结果
                with gr.Accordion("🔍 检索结果详情", open=False):
                    retrieval_results = gr.JSON(
                        label="检索到的文档",
                        value={}
                    )
                
                # 重排序结果
                with gr.Accordion("🎯 重排序结果", open=False):
                    reranking_results = gr.JSON(
                        label="重排序后的文档",
                        value={}
                    )
                
                # 最终答案
                gr.Markdown("### ✨ 生成的答案")
                final_answer = gr.Textbox(
                    label="最终回答",
                    lines=5,
                    interactive=False
                )
                
                # 性能指标
                performance_metrics = gr.HTML(
                    value="",
                    elem_id="performance-metrics"
                )
        
        gr.Markdown("---")
        
        # 对比测试区域
        gr.Markdown("### 🔄 模块对比测试")
        gr.Markdown("快速测试不同模块组合的效果差异")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("**🎯 预设测试1：仅关键词检索**")
                test1_btn = gr.Button("测试：只用关键词检索", variant="secondary")
                test1_result = gr.Textbox(label="结果1", lines=3, interactive=False)
            
            with gr.Column():
                gr.Markdown("**🧠 预设测试2：仅密集检索**")
                test2_btn = gr.Button("测试：只用密集检索", variant="secondary")
                test2_result = gr.Textbox(label="结果2", lines=3, interactive=False)
            
            with gr.Column():
                gr.Markdown("**⚡ 预设测试3：完整流程**")
                test3_btn = gr.Button("测试：完整流程", variant="secondary")
                test3_result = gr.Textbox(label="结果3", lines=3, interactive=False)
        
        # 事件处理
        _setup_real_model_events(
            engine, query_input, submit_btn, clear_btn,
            current_modules, refresh_modules_btn,
            processing_steps, retrieval_results, reranking_results,
            final_answer, performance_metrics,
            test1_btn, test1_result, test2_btn, test2_result,
            test3_btn, test3_result
        )
    
    return tab


def _get_current_modules_html(engine) -> str:
    """获取当前模块状态HTML"""
    try:
        if hasattr(engine, 'get_module_status'):
            status = engine.get_module_status()
            enabled_modules = status.get('enabled_modules', [])
            enabled_count = status.get('enabled_count', 0)
            total_count = status.get('total_count', 0)
            
            # 按类别分组显示
            core_modules = [m for m in enabled_modules if m in ['task_decomposer', 'retrieval_planner', 'multi_retriever', 'context_reranker', 'adaptive_generator']]
            retrieval_modules = [m for m in enabled_modules if m in ['keyword_retriever', 'dense_retriever', 'web_retriever', 'hybrid_retriever']]
            
            html = f"""
            <div class="module-status-card">
                <h4>📊 模块状态概览</h4>
                <div class="status-summary">
                    <span class="status-badge">启用: {enabled_count}/{total_count}</span>
                </div>
                
                <div class="module-group">
                    <strong>🧩 核心模块:</strong><br>
                    {', '.join(core_modules) if core_modules else '无'}
                </div>
                
                <div class="module-group">
                    <strong>🔍 检索模块:</strong><br>
                    {', '.join(retrieval_modules) if retrieval_modules else '无'}
                </div>
                
                <div class="status-note">
                    <em>💡 在"模块控制"标签页中可以调整配置</em>
                </div>
            </div>
            """
            return html
        else:
            return "<div class='warning-box'>⚠️ 无法获取模块状态</div>"
    except Exception as e:
        return f"<div class='error-box'>❌ 状态获取失败: {e}</div>"


def _setup_real_model_events(engine, query_input, submit_btn, clear_btn,
                            current_modules, refresh_modules_btn,
                            processing_steps, retrieval_results, reranking_results,
                            final_answer, performance_metrics,
                            test1_btn, test1_result, test2_btn, test2_result,
                            test3_btn, test3_result):
    """设置真实模型查询事件"""
    
    def process_query(query):
        """处理查询"""
        if not query.strip():
            return (
                "<div class='warning-box'>⚠️ 请输入查询内容</div>",
                {}, {}, "", ""
            )
        
        try:
            # 检查引擎是否有真实模型处理方法
            if hasattr(engine, 'process_query_with_modules'):
                result = engine.process_query_with_modules(query)
            else:
                # 回退到普通处理
                result = engine.process_query(query)
            
            # 处理步骤HTML
            steps_html = "<div class='steps-container'>"
            for i, step in enumerate(result.get('steps', []), 1):
                steps_html += f"<div class='step-item'>✅ 步骤{i}: {step}</div>"
            steps_html += "</div>"
            
            # 模块使用情况
            module_usage = result.get('module_usage', {})
            if module_usage:
                steps_html += "<div class='module-usage'><h4>📊 模块使用情况:</h4>"
                for module, used in module_usage.items():
                    status = "✅ 已使用" if used else "❌ 未使用"
                    steps_html += f"<span class='module-badge'>{module}: {status}</span>"
                steps_html += "</div>"
            
            # 性能指标
            total_time = result.get('total_time', 0)
            retrieval_count = len(result.get('retrieval_results', []))
            rerank_count = len(result.get('reranked_results', []))
            
            metrics_html = f"""
            <div class='metrics-card'>
                <h4>⚡ 性能指标</h4>
                <div class='metric-item'>总耗时: {total_time:.2f}s</div>
                <div class='metric-item'>检索文档: {retrieval_count}个</div>
                <div class='metric-item'>重排序文档: {rerank_count}个</div>
            </div>
            """
            
            return (
                steps_html,
                result.get('retrieval_results', {}),
                result.get('reranked_results', {}),
                result.get('generated_answer', ''),
                metrics_html
            )
            
        except Exception as e:
            logger.error(f"查询处理失败: {e}")
            return (
                f"<div class='error-box'>❌ 查询处理失败: {e}</div>",
                {}, {}, "", ""
            )
    
    def clear_all():
        """清空所有内容"""
        return (
            "",
            "<div class='info-box'>等待查询输入...</div>",
            {}, {}, "", "",
            "", "", ""
        )
    
    def refresh_modules():
        """刷新模块状态"""
        return _get_current_modules_html(engine)
    
    def test_keyword_only(query):
        """测试仅关键词检索"""
        if not query.strip():
            return "请先输入查询内容"
        
        try:
            # 临时配置：只启用关键词检索
            temp_config = {
                "task_decomposer": False,
                "retrieval_planner": False,
                "multi_retriever": True,
                "context_reranker": False,
                "adaptive_generator": True,
                "keyword_retriever": True,
                "dense_retriever": False,
                "web_retriever": False
            }
            
            # 保存当前配置
            if hasattr(engine, 'get_current_module_config'):
                original_config = engine.get_current_module_config()
            else:
                original_config = {}
            
            # 应用临时配置
            if hasattr(engine, 'update_module_config'):
                engine.update_module_config(temp_config)
            
            # 执行查询
            if hasattr(engine, 'process_query_with_modules'):
                result = engine.process_query_with_modules(query)
                answer = result.get('generated_answer', '无法生成答案')
            else:
                answer = "仅关键词检索模式（模拟）"
            
            # 恢复原配置
            if original_config and hasattr(engine, 'update_module_config'):
                engine.update_module_config(original_config)
            
            return f"🔍 关键词检索结果：{answer[:200]}..."
            
        except Exception as e:
            return f"测试失败: {e}"
    
    def test_dense_only(query):
        """测试仅密集检索"""
        if not query.strip():
            return "请先输入查询内容"
        
        try:
            # 临时配置：只启用密集检索
            temp_config = {
                "task_decomposer": False,
                "retrieval_planner": False,
                "multi_retriever": True,
                "context_reranker": False,
                "adaptive_generator": True,
                "keyword_retriever": False,
                "dense_retriever": True,
                "web_retriever": False
            }
            
            # 保存当前配置
            if hasattr(engine, 'get_current_module_config'):
                original_config = engine.get_current_module_config()
            else:
                original_config = {}
            
            # 应用临时配置
            if hasattr(engine, 'update_module_config'):
                engine.update_module_config(temp_config)
            
            # 执行查询
            if hasattr(engine, 'process_query_with_modules'):
                result = engine.process_query_with_modules(query)
                answer = result.get('generated_answer', '无法生成答案')
            else:
                answer = "仅密集检索模式（模拟）"
            
            # 恢复原配置
            if original_config and hasattr(engine, 'update_module_config'):
                engine.update_module_config(original_config)
            
            return f"🧠 密集检索结果：{answer[:200]}..."
            
        except Exception as e:
            return f"测试失败: {e}"
    
    def test_full_pipeline(query):
        """测试完整流程"""
        if not query.strip():
            return "请先输入查询内容"
        
        try:
            # 完整配置
            full_config = {
                "task_decomposer": True,
                "retrieval_planner": True,
                "multi_retriever": True,
                "context_reranker": True,
                "adaptive_generator": True,
                "keyword_retriever": True,
                "dense_retriever": True,
                "web_retriever": False  # 网络检索可选
            }
            
            # 保存当前配置
            if hasattr(engine, 'get_current_module_config'):
                original_config = engine.get_current_module_config()
            else:
                original_config = {}
            
            # 应用完整配置
            if hasattr(engine, 'update_module_config'):
                engine.update_module_config(full_config)
            
            # 执行查询
            if hasattr(engine, 'process_query_with_modules'):
                result = engine.process_query_with_modules(query)
                answer = result.get('generated_answer', '无法生成答案')
                steps_count = len(result.get('steps', []))
            else:
                answer = "完整流程模式（模拟）"
                steps_count = 5
            
            # 恢复原配置
            if original_config and hasattr(engine, 'update_module_config'):
                engine.update_module_config(original_config)
            
            return f"⚡ 完整流程结果（{steps_count}个步骤）：{answer[:200]}..."
            
        except Exception as e:
            return f"测试失败: {e}"
    
    # 绑定事件
    submit_btn.click(
        fn=process_query,
        inputs=[query_input],
        outputs=[processing_steps, retrieval_results, reranking_results, final_answer, performance_metrics]
    )
    
    clear_btn.click(
        fn=clear_all,
        outputs=[query_input, processing_steps, retrieval_results, reranking_results, final_answer, performance_metrics, test1_result, test2_result, test3_result]
    )
    
    refresh_modules_btn.click(
        fn=refresh_modules,
        outputs=[current_modules]
    )
    
    # 对比测试事件
    test1_btn.click(
        fn=test_keyword_only,
        inputs=[query_input],
        outputs=[test1_result]
    )
    
    test2_btn.click(
        fn=test_dense_only,
        inputs=[query_input],
        outputs=[test2_result]
    )
    
    test3_btn.click(
        fn=test_full_pipeline,
        inputs=[query_input],
        outputs=[test3_result]
    )
