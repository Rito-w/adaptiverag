#!/usr/bin/env python3
"""
=== AdaptiveRAG WebUI with Real Config ===

使用真实配置文件运行 AdaptiveRAG WebUI，可视化展示各个模块
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

class RealConfigAdaptiveRAG:
    """使用真实配置的 AdaptiveRAG 系统"""
    
    def __init__(self, config_path: str = "real_config.yaml"):
        """初始化系统"""
        self.config_path = config_path
        self.config = self.load_config()
        self.last_query_result = None
        
        logger.info("🚀 AdaptiveRAG 系统初始化完成")
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            logger.info(f"✅ 配置文件加载成功: {self.config_path}")
            return config
        except Exception as e:
            logger.error(f"❌ 配置文件加载失败: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "device": "cuda",
            "retriever_configs": {},
            "generator_configs": {},
            "ranker_configs": {}
        }
    
    def get_config_summary(self) -> str:
        """获取配置摘要"""
        summary = []
        summary.append("📋 **当前配置摘要**\n")
        
        # 基础设置
        summary.append(f"🖥️ **设备**: {self.config.get('device', 'N/A')}")
        summary.append(f"🔢 **批次大小**: {self.config.get('batch_size', 'N/A')}")
        summary.append(f"🎯 **数据集**: {self.config.get('dataset_name', 'N/A')}")
        
        # 检索器配置
        retrievers = self.config.get('retriever_configs', {})
        summary.append(f"\n🔍 **检索器配置** ({len(retrievers)} 个):")
        for name, config in retrievers.items():
            retriever_type = config.get('retriever_type', 'unknown')
            status = "✅ 真实" if retriever_type != "mock" else "🔄 模拟"
            summary.append(f"   • {name}: {retriever_type} {status}")
        
        # 生成器配置
        generators = self.config.get('generator_configs', {})
        summary.append(f"\n🤖 **生成器配置** ({len(generators)} 个):")
        for name, config in generators.items():
            generator_type = config.get('generator_type', 'unknown')
            status = "✅ 真实" if generator_type != "mock" else "🔄 模拟"
            summary.append(f"   • {name}: {generator_type} {status}")
        
        # 重排序器配置
        rankers = self.config.get('ranker_configs', {})
        summary.append(f"\n📊 **重排序器配置** ({len(rankers)} 个):")
        for name, config in rankers.items():
            ranker_type = config.get('ranker_type', 'unknown')
            status = "✅ 真实" if ranker_type != "mock" else "🔄 模拟"
            summary.append(f"   • {name}: {ranker_type} {status}")
        
        return "\n".join(summary)
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """处理查询（模拟实现，展示流程）"""
        start_time = time.time()
        
        logger.info(f"🔍 处理查询: {query}")
        
        # 模拟各个阶段
        stages = {
            "query_analysis": self.simulate_query_analysis(query),
            "strategy_planning": self.simulate_strategy_planning(query),
            "retrieval": self.simulate_retrieval(query),
            "reranking": self.simulate_reranking(query),
            "generation": self.simulate_generation(query)
        }
        
        total_time = time.time() - start_time
        
        result = {
            "query": query,
            "stages": stages,
            "total_time": total_time,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.last_query_result = result
        return result
    
    def simulate_query_analysis(self, query: str) -> Dict[str, Any]:
        """模拟查询分析阶段"""
        time.sleep(0.1)  # 模拟处理时间
        
        # 简单的查询分析
        words = query.lower().split()
        complexity_score = min(len(words) / 10.0, 1.0)
        
        # 检测查询类型
        question_words = ['what', 'who', 'where', 'when', 'why', 'how']
        has_question_word = any(word in words for word in question_words)
        
        multi_hop_indicators = ['and', 'also', 'furthermore', 'additionally']
        is_multi_hop = any(indicator in words for indicator in multi_hop_indicators)
        
        return {
            "complexity_score": complexity_score,
            "word_count": len(words),
            "has_question_word": has_question_word,
            "is_multi_hop": is_multi_hop,
            "query_type": "multi_hop" if is_multi_hop else "single_hop",
            "processing_time": 0.1
        }
    
    def simulate_strategy_planning(self, query: str) -> Dict[str, Any]:
        """模拟策略规划阶段"""
        time.sleep(0.1)
        
        # 根据查询类型选择策略
        analysis = self.simulate_query_analysis(query)
        
        if analysis["is_multi_hop"]:
            weights = {"keyword": 0.3, "dense": 0.5, "web": 0.2}
            strategy = "multi_hop_strategy"
        else:
            weights = {"keyword": 0.6, "dense": 0.3, "web": 0.1}
            strategy = "single_hop_strategy"
        
        return {
            "selected_strategy": strategy,
            "retriever_weights": weights,
            "confidence": 0.85,
            "reasoning": f"基于查询复杂度 {analysis['complexity_score']:.2f} 选择策略",
            "processing_time": 0.1
        }
    
    def simulate_retrieval(self, query: str) -> Dict[str, Any]:
        """模拟检索阶段"""
        time.sleep(0.2)
        
        # 模拟多个检索器的结果
        retrievers = self.config.get('retriever_configs', {})
        results = {}
        
        for retriever_name, config in retrievers.items():
            retriever_type = config.get('retriever_type', 'mock')
            top_k = config.get('top_k', 5)
            
            # 模拟检索结果
            docs = []
            for i in range(top_k):
                docs.append({
                    "id": f"{retriever_name}_doc_{i}",
                    "title": f"Document {i} from {retriever_name}",
                    "content": f"This is content from {retriever_name} retriever for query: {query[:50]}...",
                    "score": 0.9 - i * 0.1,
                    "source": retriever_name
                })
            
            results[retriever_name] = {
                "type": retriever_type,
                "documents": docs,
                "total_found": top_k,
                "processing_time": 0.05
            }
        
        return {
            "retriever_results": results,
            "total_documents": sum(len(r["documents"]) for r in results.values()),
            "processing_time": 0.2
        }
    
    def simulate_reranking(self, query: str) -> Dict[str, Any]:
        """模拟重排序阶段"""
        time.sleep(0.1)
        
        rankers = self.config.get('ranker_configs', {})
        
        # 模拟重排序结果
        reranked_docs = []
        for i in range(5):
            reranked_docs.append({
                "id": f"reranked_doc_{i}",
                "title": f"Reranked Document {i}",
                "content": f"Reranked content for: {query[:50]}...",
                "original_score": 0.8 - i * 0.1,
                "rerank_score": 0.95 - i * 0.05,
                "rank_change": i % 3 - 1  # -1, 0, 1
            })
        
        return {
            "ranker_used": list(rankers.keys())[0] if rankers else "default",
            "reranked_documents": reranked_docs,
            "score_improvement": 0.15,
            "processing_time": 0.1
        }
    
    def simulate_generation(self, query: str) -> Dict[str, Any]:
        """模拟生成阶段"""
        time.sleep(0.3)
        
        generators = self.config.get('generator_configs', {})
        main_generator = list(generators.keys())[0] if generators else "default"
        
        # 模拟生成的答案
        answer = f"Based on the retrieved information, here's the answer to '{query}': This is a simulated response generated using the {main_generator} generator with real configuration settings."
        
        return {
            "generator_used": main_generator,
            "generated_answer": answer,
            "confidence": 0.88,
            "token_count": len(answer.split()),
            "processing_time": 0.3
        }

def create_webui(config_path: str = "real_config.yaml") -> gr.Blocks:
    """创建 WebUI 界面"""
    
    # 初始化系统
    rag_system = RealConfigAdaptiveRAG(config_path)
    
    # 创建界面
    with gr.Blocks(
        title="AdaptiveRAG WebUI",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
        }
        """
    ) as demo:
        
        gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h1>🧠 AdaptiveRAG WebUI</h1>
            <p>智能自适应检索增强生成系统 - 使用真实配置</p>
        </div>
        """)
        
        # 创建标签页
        with gr.Tabs():
            # 配置信息标签页
            with gr.Tab("⚙️ 配置信息"):
                gr.HTML("<h2>📋 系统配置信息</h2>")
                
                config_display = gr.Markdown(
                    value=rag_system.get_config_summary(),
                    label="配置摘要"
                )
                
                with gr.Row():
                    refresh_config_btn = gr.Button("🔄 刷新配置", variant="secondary")
                    reload_config_btn = gr.Button("📁 重新加载配置文件", variant="primary")
                
                config_status = gr.Textbox(
                    label="状态",
                    value="配置已加载",
                    interactive=False
                )
                
                def refresh_config():
                    return rag_system.get_config_summary(), "配置已刷新"
                
                def reload_config():
                    rag_system.config = rag_system.load_config()
                    return rag_system.get_config_summary(), "配置文件已重新加载"
                
                refresh_config_btn.click(
                    refresh_config,
                    outputs=[config_display, config_status]
                )
                
                reload_config_btn.click(
                    reload_config,
                    outputs=[config_display, config_status]
                )
            
            # 查询测试标签页
            with gr.Tab("🔍 查询测试"):
                gr.HTML("<h2>🧠 智能查询处理</h2>")
                
                with gr.Row():
                    with gr.Column(scale=3):
                        query_input = gr.Textbox(
                            label="输入查询",
                            placeholder="请输入您的问题...",
                            lines=3
                        )
                        
                        process_btn = gr.Button("🚀 处理查询", variant="primary")
                        
                    with gr.Column(scale=1):
                        gr.HTML("<h4>📊 快速统计</h4>")
                        query_stats = gr.JSON(
                            label="查询统计",
                            value={"总查询数": 0, "平均处理时间": "0.0s"}
                        )
                
                # 结果展示区域
                with gr.Row():
                    with gr.Column():
                        gr.HTML("<h3>📈 处理流程</h3>")
                        process_flow = gr.JSON(label="处理阶段")
                        
                    with gr.Column():
                        gr.HTML("<h3>💬 生成结果</h3>")
                        generated_answer = gr.Textbox(
                            label="生成的答案",
                            lines=5,
                            interactive=False
                        )
                
                def process_query(query):
                    if not query.strip():
                        return {}, "请输入有效的查询"
                    
                    result = rag_system.process_query(query)
                    
                    # 提取处理流程信息
                    flow_info = {}
                    for stage_name, stage_data in result["stages"].items():
                        flow_info[stage_name] = {
                            "处理时间": f"{stage_data.get('processing_time', 0):.3f}s",
                            "状态": "✅ 完成"
                        }
                    
                    flow_info["总处理时间"] = f"{result['total_time']:.3f}s"
                    
                    # 提取生成的答案
                    answer = result["stages"]["generation"]["generated_answer"]
                    
                    return flow_info, answer
                
                process_btn.click(
                    process_query,
                    inputs=[query_input],
                    outputs=[process_flow, generated_answer]
                )
    
    return demo

def main():
    """主函数"""
    logger.info("🚀 启动 AdaptiveRAG WebUI")
    
    # 检查配置文件
    config_path = "real_config.yaml"
    if not Path(config_path).exists():
        logger.error(f"❌ 配置文件不存在: {config_path}")
        return
    
    # 创建并启动 WebUI
    demo = create_webui(config_path)
    
    logger.info("🌐 启动 WebUI 服务器...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )

if __name__ == "__main__":
    main()
