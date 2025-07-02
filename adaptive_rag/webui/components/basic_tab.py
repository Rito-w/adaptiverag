"""
基础配置标签页 - 借鉴 FlashRAG 的设计
"""

import gradio as gr
from typing import Dict, Any
from adaptive_rag.config import create_flexrag_integrated_config


def create_basic_tab(engine) -> Dict[str, gr.Component]:
    """创建基础配置标签页 - 借鉴 FlashRAG 的设计"""
    
    with gr.Tab("🔧 基础配置") as basic_tab:
        gr.HTML("<h3>系统配置</h3>")
        
        with gr.Row():
            with gr.Column(scale=1):
                # 模型配置
                gr.HTML("<h4>📦 模型配置</h4>")
                
                # 兼容不同的配置对象
                def safe_get_config(key, default):
                    if hasattr(engine.config, 'get'):
                        return engine.config.get(key, default)
                    else:
                        return getattr(engine.config, key, default)

                dense_model_path = gr.Textbox(
                    label="向量检索模型路径",
                    value=safe_get_config('dense_model_path', "/root/autodl-tmp/models/e5-base-v2"),
                    placeholder="/path/to/dense/model"
                )

                generator_model_path = gr.Textbox(
                    label="生成模型路径",
                    value=safe_get_config('generator_model_path', "/root/autodl-tmp/models/Qwen2.5-1.5B-Instruct"),
                    placeholder="/path/to/generator/model"
                )

                reranker_model_path = gr.Textbox(
                    label="重排序模型路径",
                    value=safe_get_config('reranker_model_path', "/root/autodl-tmp/models/bge-reranker-base"),
                    placeholder="/path/to/reranker/model"
                )

            with gr.Column(scale=1):
                # 数据配置
                gr.HTML("<h4>📊 数据配置</h4>")

                corpus_path = gr.Textbox(
                    label="语料库路径",
                    value=safe_get_config('corpus_path', "/root/autodl-tmp/flashrag_real_data/hotpotqa_dev.jsonl"),
                    placeholder="/path/to/corpus.jsonl"
                )

                index_path = gr.Textbox(
                    label="索引路径",
                    value=safe_get_config('index_path', "/root/autodl-tmp/flashrag_real_data/cache/e5_Flat.index"),
                    placeholder="/path/to/index"
                )

                batch_size = gr.Slider(
                    minimum=1,
                    maximum=32,
                    value=safe_get_config('batch_size', 4),
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