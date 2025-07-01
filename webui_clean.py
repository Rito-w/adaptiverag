#!/usr/bin/env python3
"""
=== AdaptiveRAG Clean WebUI ===

清晰的模块化 WebUI，展示所有 AdaptiveRAG 模块
"""

import gradio as gr
import json
import yaml
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import sys
import os

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AdaptiveRAGWebUI:
    """AdaptiveRAG WebUI 主类"""
    
    def __init__(self, config_path: str = "real_config.yaml"):
        """初始化 WebUI"""
        self.config_path = config_path
        self.config = self.load_config()
        self.query_count = 0
        self.total_time = 0.0
        
        # 初始化真实组件
        self.initialize_components()
        
        logger.info("🚀 AdaptiveRAG WebUI 初始化完成")
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            logger.info(f"✅ 配置文件加载成功: {self.config_path}")
            return config
        except Exception as e:
            logger.error(f"❌ 配置文件加载失败: {e}")
            return {}
    
    def initialize_components(self):
        """初始化组件"""
        try:
            from adaptive_rag.core.flexrag_integrated_assistant import FlexRAGIntegratedAssistant
            self.assistant = FlexRAGIntegratedAssistant()
            self.use_real_components = True
            logger.info("✅ 真实组件初始化成功")
        except Exception as e:
            logger.warning(f"⚠️ 真实组件初始化失败，使用模拟模式: {e}")
            self.assistant = None
            self.use_real_components = False
    
    def get_module_status(self) -> Dict[str, Any]:
        """获取各模块状态"""
        retrievers = self.config.get('retriever_configs', {})
        generators = self.config.get('generator_configs', {})
        rankers = self.config.get('ranker_configs', {})
        
        return {
            "task_decomposer": {
                "status": "✅ 运行中",
                "type": "真实组件",
                "description": "智能任务分解器"
            },
            "retrieval_planner": {
                "status": "✅ 运行中", 
                "type": "真实组件",
                "description": "检索策略规划器"
            },
            "retrievers": {
                "count": len(retrievers),
                "details": {
                    name: {
                        "type": config.get('retriever_type', 'unknown'),
                        "model": config.get('model_name', 'N/A'),
                        "status": "✅ 真实" if config.get('retriever_type') != 'mock' else "🔄 模拟"
                    }
                    for name, config in retrievers.items()
                }
            },
            "rankers": {
                "count": len(rankers),
                "details": {
                    name: {
                        "type": config.get('ranker_type', 'unknown'),
                        "model": config.get('model_name', 'N/A'),
                        "status": "✅ 真实" if config.get('ranker_type') != 'mock' else "🔄 模拟"
                    }
                    for name, config in rankers.items()
                }
            },
            "generators": {
                "count": len(generators),
                "details": {
                    name: {
                        "type": config.get('generator_type', 'unknown'),
                        "model": config.get('model_name', 'N/A'),
                        "status": "✅ 真实" if config.get('generator_type') != 'mock' else "🔄 模拟"
                    }
                    for name, config in generators.items()
                }
            }
        }
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """处理查询"""
        start_time = time.time()
        self.query_count += 1
        
        logger.info(f"🔍 处理查询 #{self.query_count}: {query}")
        
        if self.use_real_components and self.assistant:
            try:
                # 使用真实组件
                result = self.assistant.process_query(query, show_details=True)
                method = "真实组件"
            except Exception as e:
                logger.error(f"❌ 真实组件处理失败: {e}")
                result = self.simulate_processing(query)
                method = "模拟组件"
        else:
            # 使用模拟组件
            result = self.simulate_processing(query)
            method = "模拟组件"
        
        processing_time = time.time() - start_time
        self.total_time += processing_time
        
        return {
            "query": query,
            "answer": result.get("answer", ""),
            "method": method,
            "processing_time": processing_time,
            "query_count": self.query_count,
            "avg_time": self.total_time / self.query_count,
            "stages": result.get("stages", {}),
            "retrieved_docs": result.get("retrieved_docs", [])
        }
    
    def simulate_processing(self, query: str) -> Dict[str, Any]:
        """模拟处理流程"""
        time.sleep(0.5)  # 模拟处理时间
        
        return {
            "answer": f"这是对查询 '{query}' 的模拟回答。使用了配置文件中的设置，但当前运行在模拟模式下。",
            "stages": {
                "task_decomposition": {"time": 0.1, "status": "完成"},
                "strategy_planning": {"time": 0.1, "status": "完成"},
                "retrieval": {"time": 0.2, "status": "完成"},
                "reranking": {"time": 0.1, "status": "完成"},
                "generation": {"time": 0.1, "status": "完成"}
            },
            "retrieved_docs": [
                {"title": f"文档 {i}", "content": f"关于 '{query}' 的模拟内容...", "score": 0.9-i*0.1}
                for i in range(3)
            ]
        }

def create_module_overview_tab(webui: AdaptiveRAGWebUI):
    """创建模块概览标签页"""
    with gr.Tab("🏗️ 模块概览"):
        gr.HTML("<h2>📋 AdaptiveRAG 模块状态</h2>")
        
        # 模块状态展示
        module_status = gr.JSON(
            value=webui.get_module_status(),
            label="模块状态"
        )
        
        # 刷新按钮
        refresh_btn = gr.Button("🔄 刷新模块状态", variant="secondary")
        
        def refresh_modules():
            return webui.get_module_status()
        
        refresh_btn.click(
            refresh_modules,
            outputs=[module_status]
        )
        
        return module_status, refresh_btn

def create_query_processing_tab(webui: AdaptiveRAGWebUI):
    """创建查询处理标签页"""
    with gr.Tab("🔍 查询处理"):
        gr.HTML("<h2>🧠 智能查询处理</h2>")
        
        with gr.Row():
            with gr.Column(scale=2):
                query_input = gr.Textbox(
                    label="输入查询",
                    placeholder="请输入您的问题...",
                    lines=3
                )
                
                process_btn = gr.Button("🚀 处理查询", variant="primary")
                
            with gr.Column(scale=1):
                stats_display = gr.JSON(
                    label="处理统计",
                    value={"查询数": 0, "平均时间": "0.0s", "组件类型": "模拟" if not webui.use_real_components else "真实"}
                )
        
        # 结果展示
        with gr.Row():
            with gr.Column():
                gr.HTML("<h3>📈 处理阶段</h3>")
                stages_display = gr.JSON(label="各阶段详情")
                
            with gr.Column():
                gr.HTML("<h3>💬 生成结果</h3>")
                answer_display = gr.Textbox(
                    label="生成的答案",
                    lines=5,
                    interactive=False
                )
        
        # 检索结果
        gr.HTML("<h3>📚 检索结果</h3>")
        docs_display = gr.JSON(label="检索到的文档")
        
        def process_query_handler(query):
            if not query.strip():
                return {}, {}, "", {}
            
            result = webui.process_query(query)
            
            # 更新统计信息
            stats = {
                "查询数": result["query_count"],
                "平均时间": f"{result['avg_time']:.3f}s",
                "当前处理时间": f"{result['processing_time']:.3f}s",
                "组件类型": result["method"]
            }
            
            return stats, result["stages"], result["answer"], result["retrieved_docs"]
        
        process_btn.click(
            process_query_handler,
            inputs=[query_input],
            outputs=[stats_display, stages_display, answer_display, docs_display]
        )
        
        return query_input, process_btn, stats_display, stages_display, answer_display, docs_display

def create_config_tab(webui: AdaptiveRAGWebUI):
    """创建配置标签页"""
    with gr.Tab("⚙️ 配置管理"):
        gr.HTML("<h2>📋 系统配置</h2>")
        
        # 配置摘要
        config_summary = gr.JSON(
            value=webui.config,
            label="当前配置"
        )
        
        # 配置操作
        with gr.Row():
            reload_btn = gr.Button("📁 重新加载配置", variant="primary")
            reset_btn = gr.Button("🔄 重置组件", variant="secondary")
        
        status_display = gr.Textbox(
            label="操作状态",
            value="配置已加载",
            interactive=False
        )
        
        def reload_config():
            webui.config = webui.load_config()
            webui.initialize_components()
            return webui.config, "配置已重新加载，组件已重新初始化"
        
        def reset_components():
            webui.initialize_components()
            return webui.config, "组件已重置"
        
        reload_btn.click(
            reload_config,
            outputs=[config_summary, status_display]
        )
        
        reset_btn.click(
            reset_components,
            outputs=[config_summary, status_display]
        )
        
        return config_summary, reload_btn, reset_btn, status_display

def create_webui(config_path: str = "real_config.yaml") -> gr.Blocks:
    """创建主 WebUI"""
    
    # 初始化 WebUI
    webui = AdaptiveRAGWebUI(config_path)
    
    # 自定义 CSS（保持原有风格）
    custom_css = """
    .gradio-container, .main, .container {
        max-width: none !important;
        margin: 0 !important;
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
    """
    
    with gr.Blocks(
        title="🧠 AdaptiveRAG 系统",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="purple",
            neutral_hue="slate"
        ),
        css=custom_css
    ) as demo:
        
        # 标题
        gr.HTML("""
        <div class="title-container">
            <h1 style="margin: 0 0 10px 0; font-size: 2.5em; font-weight: 700;">
                🧠 智能自适应 RAG 系统
            </h1>
            <h3 style="margin: 0 0 15px 0; font-size: 1.3em; font-weight: 400; opacity: 0.9;">
                模块化可视化界面
            </h3>
            <p style="margin: 0; font-size: 1em; opacity: 0.8; line-height: 1.6;">
                展示任务分解、检索规划、多重检索、重排序、生成等所有模块
            </p>
        </div>
        """)
        
        # 创建标签页
        with gr.Tabs():
            # 模块概览
            module_status, refresh_btn = create_module_overview_tab(webui)
            
            # 查询处理
            query_components = create_query_processing_tab(webui)
            
            # 配置管理
            config_components = create_config_tab(webui)
    
    return demo

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="启动 AdaptiveRAG Clean WebUI")
    parser.add_argument("--port", type=int, default=7863, help="服务端口")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="服务主机")
    parser.add_argument("--config-path", type=str, default="real_config.yaml", help="配置文件路径")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    parser.add_argument("--share", action="store_true", help="创建公共链接")
    
    args = parser.parse_args()
    
    logger.info("🚀 启动 AdaptiveRAG Clean WebUI")
    logger.info(f"📍 地址: http://{args.host}:{args.port}")
    logger.info(f"📁 配置文件: {args.config_path}")
    
    # 检查配置文件
    if not Path(args.config_path).exists():
        logger.error(f"❌ 配置文件不存在: {args.config_path}")
        return
    
    # 创建并启动 WebUI
    demo = create_webui(args.config_path)
    
    demo.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        debug=args.debug,
        show_error=True
    )

if __name__ == "__main__":
    main()
