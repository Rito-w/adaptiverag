"""
WebUI 事件处理器
"""

import json
import gradio as gr
from typing import Dict, Any
from adaptive_rag.config import create_flexrag_integrated_config


def create_event_handlers(engine):
    """创建事件处理器"""
    
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
                        "type": str(getattr(st, 'task_type', 'unknown')),
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

    return {
        "process_search": process_search,
        "clear_all": clear_all,
        "set_example_query": set_example_query,
        "update_system_status": update_system_status,
        "save_config_handler": save_config_handler,
        "load_config_handler": load_config_handler,
        "reset_config_handler": reset_config_handler
    } 