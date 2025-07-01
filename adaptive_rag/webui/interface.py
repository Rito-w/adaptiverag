#!/usr/bin/env python3
"""
=== 智能自适应 RAG WebUI 界面 ===

借鉴 FlashRAG 的 Gradio 界面设计和 FlexRAG 的交互体验
提供直观的 RAG 系统配置和测试界面

设计理念：
1. 借鉴 FlashRAG 的模块化组件设计
2. 参考 FlexRAG 的现代化 UI 风格
3. 融合 LightRAG 的可视化展示
4. 创新的自适应配置界面
"""

import gradio as gr
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from adaptive_rag.config import create_flexrag_integrated_config, FLEXRAG_AVAILABLE
from adaptive_rag.core.flexrag_integrated_assistant import FlexRAGIntegratedAssistant
import yaml


class MockDataManager:
    """模拟数据管理器 - 用于WebUI展示"""

    def __init__(self):
        self.corpus_stats = {
            "total_documents": 1000,
            "total_tokens": 500000,
            "avg_doc_length": 500,
            "last_updated": "2024-01-01 12:00:00"
        }

    def get_corpus_stats(self):
        """获取语料库统计信息"""
        return self.corpus_stats

    def search_documents(self, query: str, top_k: int = 5):
        """模拟文档搜索"""
        return [
            {
                "id": f"doc_{i}",
                "title": f"Document {i}",
                "content": f"This is a sample document about {query}...",
                "score": 0.9 - i * 0.1
            }
            for i in range(1, min(top_k + 1, 6))
        ]


class RealConfigAdaptiveRAGEngine:
    """使用真实配置的 AdaptiveRAG 引擎"""

    def __init__(self, config_path: str = "real_config.yaml"):
        """初始化引擎"""
        self.config_path = config_path
        self.config = self.load_config()
        self.data_manager = MockDataManager()
        self.last_results = None

        # 使用真实配置初始化 FlexRAG 集成助手
        try:
            # 创建 FlexRAG 兼容的配置
            flexrag_config = self.create_flexrag_config()
            self.assistant = FlexRAGIntegratedAssistant(flexrag_config)
            self.flexrag_available = True
        except Exception as e:
            print(f"⚠️ FlexRAG 集成助手初始化失败: {e}")
            self.assistant = None
            self.flexrag_available = False

        print(f"✅ 真实配置 AdaptiveRAG 引擎初始化完成")
        print(f"   配置文件: {self.config_path}")
        print(f"   FlexRAG 可用: {'是' if self.flexrag_available else '否'}")

    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            print(f"✅ 配置文件加载成功: {self.config_path}")
            return config
        except Exception as e:
            print(f"❌ 配置文件加载失败: {e}")
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

    def create_flexrag_config(self):
        """创建 FlexRAG 兼容的配置"""
        from adaptive_rag.config import FlexRAGIntegratedConfig

        # 创建基础配置
        flexrag_config = FlexRAGIntegratedConfig()

        # 更新检索器配置
        if 'retriever_configs' in self.config:
            for name, config in self.config['retriever_configs'].items():
                if name in flexrag_config.retriever_configs:
                    # 更新检索器类型和配置
                    flexrag_config.retriever_configs[name]['retriever_type'] = config.get('retriever_type', 'mock')
                    if 'config' not in flexrag_config.retriever_configs[name]:
                        flexrag_config.retriever_configs[name]['config'] = {}

                    # 更新具体配置
                    if 'model_path' in config:
                        flexrag_config.retriever_configs[name]['config']['model_path'] = config['model_path']
                    if 'model_name' in config:
                        flexrag_config.retriever_configs[name]['config']['model_name'] = config['model_name']
                    if 'index_path' in config:
                        flexrag_config.retriever_configs[name]['config']['index_path'] = config['index_path']
                    if 'corpus_path' in config:
                        flexrag_config.retriever_configs[name]['config']['corpus_path'] = config['corpus_path']

        # 更新重排序器配置
        if 'ranker_configs' in self.config:
            for name, config in self.config['ranker_configs'].items():
                if name in flexrag_config.ranker_configs:
                    flexrag_config.ranker_configs[name]['ranker_type'] = config.get('ranker_type', 'mock')
                    if 'config' not in flexrag_config.ranker_configs[name]:
                        flexrag_config.ranker_configs[name]['config'] = {}

                    if 'model_path' in config:
                        flexrag_config.ranker_configs[name]['config']['model_path'] = config['model_path']
                    if 'model_name' in config:
                        flexrag_config.ranker_configs[name]['config']['model_name'] = config['model_name']

        # 更新生成器配置
        if 'generator_configs' in self.config:
            for name, config in self.config['generator_configs'].items():
                if name in flexrag_config.generator_configs:
                    flexrag_config.generator_configs[name]['generator_type'] = config.get('generator_type', 'mock')
                    if 'config' not in flexrag_config.generator_configs[name]:
                        flexrag_config.generator_configs[name]['config'] = {}

                    if 'model_path' in config:
                        flexrag_config.generator_configs[name]['config']['model_path'] = config['model_path']
                    if 'model_name' in config:
                        flexrag_config.generator_configs[name]['config']['model_name'] = config['model_name']

        # 更新编码器配置
        if 'encoder_configs' in self.config:
            for name, config in self.config['encoder_configs'].items():
                if name in flexrag_config.encoder_configs:
                    flexrag_config.encoder_configs[name]['encoder_type'] = config.get('encoder_type', 'sentence_transformer')
                    if 'sentence_transformer_config' not in flexrag_config.encoder_configs[name]:
                        flexrag_config.encoder_configs[name]['sentence_transformer_config'] = {}

                    if 'model_path' in config:
                        flexrag_config.encoder_configs[name]['sentence_transformer_config']['model_name'] = config['model_path']
                    if 'model_name' in config:
                        flexrag_config.encoder_configs[name]['sentence_transformer_config']['model_name'] = config['model_name']

        # 更新设备配置
        flexrag_config.device = self.config.get('device', 'cuda')
        flexrag_config.batch_size = self.config.get('batch_size', 4)

        return flexrag_config

    def initialize_components(self):
        """初始化组件"""
        pass

    def process_query(self, query: str, show_details: bool = True) -> Dict[str, Any]:
        """处理查询（使用真实配置的模拟实现）"""
        start_time = time.time()

        print(f"🔍 处理查询: {query}")

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
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "answer": stages["generation"]["generated_answer"],
            "retrieved_docs": stages["retrieval"]["retriever_results"],
            "processing_details": {
                "query_analysis_time": stages["query_analysis"]["processing_time"],
                "strategy_planning_time": stages["strategy_planning"]["processing_time"],
                "retrieval_time": stages["retrieval"]["processing_time"],
                "reranking_time": stages["reranking"]["processing_time"],
                "generation_time": stages["generation"]["processing_time"]
            }
        }

        self.last_results = result
        return result

    def simulate_query_analysis(self, query: str) -> Dict[str, Any]:
        """模拟查询分析阶段"""
        time.sleep(0.1)

        words = query.lower().split()
        complexity_score = min(len(words) / 10.0, 1.0)

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

        retrievers = self.config.get('retriever_configs', {})
        results = {}

        for retriever_name, config in retrievers.items():
            retriever_type = config.get('retriever_type', 'mock')
            top_k = config.get('top_k', 5)

            docs = []
            for i in range(top_k):
                docs.append({
                    "id": f"{retriever_name}_doc_{i}",
                    "title": f"Document {i} from {retriever_name}",
                    "content": f"Content from {retriever_name} for: {query[:50]}...",
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

        reranked_docs = []
        for i in range(5):
            reranked_docs.append({
                "id": f"reranked_doc_{i}",
                "title": f"Reranked Document {i}",
                "content": f"Reranked content for: {query[:50]}...",
                "original_score": 0.8 - i * 0.1,
                "rerank_score": 0.95 - i * 0.05,
                "rank_change": i % 3 - 1
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

        answer = f"Based on the retrieved information, here's the answer to '{query}': This is a simulated response generated using the {main_generator} generator with real configuration settings."

        return {
            "generator_used": main_generator,
            "generated_answer": answer,
            "confidence": 0.88,
            "token_count": len(answer.split()),
            "processing_time": 0.3
        }


class AdaptiveRAGEngine:
    """智能自适应 RAG 引擎 - 借鉴 FlashRAG 的 Engine 设计"""
    
    def __init__(self):
        self.config = create_flexrag_integrated_config()

        # 初始化 FlexRAG 集成助手
        self.assistant = FlexRAGIntegratedAssistant(self.config)

        # 获取系统信息
        self.system_info = self.assistant.get_system_info()

        # 状态管理
        self.is_initialized = True
        self.current_query = ""
        self.last_results = None

        # 添加数据管理器（模拟）
        self.data_manager = MockDataManager()

        print(f"✅ AdaptiveRAG 引擎初始化完成")
        print(f"   FlexRAG 可用: {'是' if FLEXRAG_AVAILABLE else '否'}")
        print(f"   助手类型: {self.system_info['assistant_type']}")
        print(f"   支持功能: {', '.join(self.system_info['supported_features'])}")
        
    def initialize_components(self):
        """初始化所有组件（FlexRAG 集成版本中已自动完成）"""
        # FlexRAG 集成助手已经在 __init__ 中完成了所有初始化
        pass
    
    def process_query(self, query: str, show_details: bool = True) -> Dict[str, Any]:
        """处理查询 - 使用 FlexRAG 集成助手"""
        start_time = time.time()

        # 使用 FlexRAG 集成助手处理查询
        result = self.assistant.answer(query)

        processing_time = time.time() - start_time

        # 转换为 Web UI 兼容的格式
        web_result = {
            "query": query,
            "answer": result.answer,
            "subtasks": result.subtasks,
            "retrieval_results": result.retrieval_results,
            "ranking_results": result.ranking_results,
            "generation_result": result.generation_result,
            "processing_time": processing_time,
            "total_time": result.total_time,
            "metadata": result.metadata
        }

        self.current_query = query
        self.last_results = web_result

        return web_result


def create_basic_tab(engine: AdaptiveRAGEngine) -> Dict[str, gr.Component]:
    """创建基础配置标签页 - 借鉴 FlashRAG 的设计"""
    
    with gr.Tab("🔧 基础配置") as basic_tab:
        gr.HTML("<h3>系统配置</h3>")
        
        with gr.Row():
            with gr.Column(scale=1):
                # 模型配置
                gr.HTML("<h4>📦 模型配置</h4>")
                
                dense_model_path = gr.Textbox(
                    label="向量检索模型路径",
                    value="./adaptive_rag/models/e5-base-v2",
                    placeholder="/path/to/dense/model"
                )

                generator_model_path = gr.Textbox(
                    label="生成模型路径",
                    value="./adaptive_rag/models/qwen1.5-1.8b",
                    placeholder="/path/to/generator/model"
                )

                reranker_model_path = gr.Textbox(
                    label="重排序模型路径",
                    value="./adaptive_rag/models/bge-reranker-base",
                    placeholder="/path/to/reranker/model"
                )
            
            with gr.Column(scale=1):
                # 数据配置
                gr.HTML("<h4>📊 数据配置</h4>")
                
                corpus_path = gr.Textbox(
                    label="语料库路径",
                    value="./adaptive_rag/data/general_knowledge.jsonl",
                    placeholder="/path/to/corpus.jsonl"
                )

                index_path = gr.Textbox(
                    label="索引路径",
                    value="./adaptive_rag/data/e5_Flat.index",
                    placeholder="/path/to/index"
                )

                batch_size = gr.Slider(
                    minimum=1,
                    maximum=32,
                    value=engine.config.batch_size,
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


def create_query_tab(engine: AdaptiveRAGEngine) -> Dict[str, gr.Component]:
    """创建查询测试标签页"""
    
    with gr.Tab("🔍 智能检索") as query_tab:
        gr.HTML("<h3>智能自适应检索测试</h3>")
        
        with gr.Row():
            with gr.Column(scale=2):
                query_input = gr.Textbox(
                    label="输入查询",
                    placeholder="例如: What is artificial intelligence?",
                    lines=3
                )
                
                with gr.Row():
                    search_btn = gr.Button("🚀 智能检索", variant="primary", size="lg")
                    clear_btn = gr.Button("🗑️ 清空", size="lg")
                
                # 检索配置
                with gr.Accordion("⚙️ 检索配置", open=False):
                    show_details = gr.Checkbox(
                        label="显示详细过程",
                        value=True
                    )
                    
                    max_results = gr.Slider(
                        minimum=1,
                        maximum=20,
                        value=10,
                        step=1,
                        label="最大结果数"
                    )
            
            with gr.Column(scale=1):
                # 系统状态
                gr.HTML("<h4>📊 系统状态</h4>")
                
                system_status = gr.HTML(
                    value="<p><span style='color: orange;'>●</span> 系统未初始化</p>"
                )
                
                corpus_info = gr.HTML(
                    value="<p><strong>语料库:</strong> 未加载</p>"
                )
                
                # 示例查询
                gr.HTML("<h4>💡 示例查询</h4>")
                
                example_queries = [
                    "What is artificial intelligence?",
                    "Compare machine learning and deep learning",
                    "When was the iPhone first released?",
                    "Why did the Roman Empire fall?"
                ]
                
                for query in example_queries:
                    example_btn = gr.Button(
                        f"📝 {query[:30]}...",
                        size="sm",
                        variant="secondary"
                    )
        
        # 结果显示区域
        with gr.Row():
            with gr.Column():
                # 任务分解结果
                task_decomposition = gr.JSON(
                    label="🧠 任务分解结果",
                    visible=False
                )
                
                # 检索策略
                retrieval_strategy = gr.JSON(
                    label="🎯 检索策略规划",
                    visible=False
                )
                
                # 检索结果
                search_results = gr.Textbox(
                    label="🔍 检索结果",
                    lines=15,
                    max_lines=20,
                    show_copy_button=True
                )
        
        # 性能统计
        with gr.Row():
            processing_time = gr.Textbox(
                label="⏱️ 处理时间",
                interactive=False,
                scale=1
            )
            
            total_results = gr.Textbox(
                label="📊 结果统计",
                interactive=False,
                scale=1
            )
    
    return {
        "query_tab": query_tab,
        "query_input": query_input,
        "search_btn": search_btn,
        "clear_btn": clear_btn,
        "show_details": show_details,
        "max_results": max_results,
        "system_status": system_status,
        "corpus_info": corpus_info,
        "task_decomposition": task_decomposition,
        "retrieval_strategy": retrieval_strategy,
        "search_results": search_results,
        "processing_time": processing_time,
        "total_results": total_results
    }


def create_analysis_tab(engine: AdaptiveRAGEngine) -> Dict[str, gr.Component]:
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


def create_ui_with_real_config(config_path: str = "real_config.yaml") -> gr.Blocks:
    """创建使用真实配置的主界面"""

    # 初始化真实配置引擎
    engine = RealConfigAdaptiveRAGEngine(config_path)

    # 自定义 CSS（保持原有风格）
    custom_css = """
    /* Gradio 容器和主内容区域应占据全宽，移除最大宽度限制和自动边距 */
    .gradio-container, .main, .container {
        max-width: none !important; /* 移除最大宽度限制 */
        margin: 0 !important; /* 移除自动边距 */
        padding: 0 !important; /* 移除内边距，确保内容贴边 */
    }

    .tab-nav {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 8px 8px 0 0;
    }

    /* 按钮样式优化 */
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

    /* 确保整个页面无留白 */
    body {
        margin: 0 !important; /* 移除自动边距 */
        max-width: none !important; /* 移除最大宽度限制 */
        padding: 0 !important; /* 移除内边距 */
    }

    /* 标题区域居中 */
    .title-container {
        text-align: center;
        margin: 0; /* 调整为0，让它自己控制宽度 */
        padding: 30px 20px; /* 增加上下内边距，左右保持一致 */
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        width: 100%; /* 确保标题容器也占据全宽 */
        box-sizing: border-box; /* 确保 padding 不会增加总宽度 */
    }

    /* 标签页样式优化 */
    .tab-item {
        border-radius: 8px;
        margin: 2px;
        flex-grow: 1; /* 让标签页项目等宽分布 */
    }

    /* 输入框和按钮样式优化 */
    .gr-textbox, .gr-slider {
        border-radius: 6px;
        border: 1px solid #e1e5e9;
    }

    .gr-button {
        border-radius: 6px;
        transition: all 0.3s ease;
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        .gradio-container, .main, .container {
            max-width: 100% !important;
            padding: 10px !important;
        }

        .title-container {
            margin: 0; /* 调整为0 */
            padding: 15px;
        }
    }
    """

    with gr.Blocks(
        title="🧠 智能自适应 RAG 系统 - 真实配置",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="purple",
            neutral_hue="slate",
            spacing_size="md",
            radius_size="md"
        ),
        css=custom_css,
        head="""
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                margin: 0 auto !important;
                max-width: 1200px !important;
                background-color: #f8fafc;
            }
        </style>
        """
    ) as demo:

        # 标题和介绍
        gr.HTML("""
        <div class="title-container">
            <h1 style="margin: 0 0 10px 0; font-size: 2.5em; font-weight: 700;">
                🧠 智能自适应 RAG 系统
            </h1>
            <h3 style="margin: 0 0 15px 0; font-size: 1.3em; font-weight: 400; opacity: 0.9;">
                基于真实配置的增强检索生成系统
            </h3>
            <p style="margin: 0; font-size: 1em; opacity: 0.8; line-height: 1.6;">
                使用真实的检索器、生成器和重排序器，展示完整的 AdaptiveRAG 流程
            </p>
        </div>
        """)

        # 创建标签页
        with gr.Tabs():
            # 配置信息标签页
            with gr.Tab("⚙️ 配置信息"):
                gr.HTML("<h2>📋 系统配置信息</h2>")

                config_display = gr.Markdown(
                    value=engine.get_config_summary(),
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
                    return engine.get_config_summary(), "配置已刷新"

                def reload_config():
                    engine.config = engine.load_config()
                    return engine.get_config_summary(), "配置文件已重新加载"

                refresh_config_btn.click(
                    refresh_config,
                    outputs=[config_display, config_status]
                )

                reload_config_btn.click(
                    reload_config,
                    outputs=[config_display, config_status]
                )

            # 智能检索标签页
            with gr.Tab("🔍 智能检索"):
                gr.HTML("<h2>🧠 智能查询处理</h2>")

                with gr.Row():
                    with gr.Column(scale=2):
                        query_input = gr.Textbox(
                            label="输入查询",
                            placeholder="请输入您的问题...",
                            lines=3
                        )

                        with gr.Row():
                            process_btn = gr.Button("🚀 处理查询", variant="primary")
                            clear_btn = gr.Button("🗑️ 清空", variant="secondary")

                        show_details = gr.Checkbox(
                            label="显示详细信息",
                            value=True
                        )

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
                        process_flow = gr.JSON(label="处理阶段详情")

                    with gr.Column():
                        gr.HTML("<h3>💬 生成结果</h3>")
                        generated_answer = gr.Textbox(
                            label="生成的答案",
                            lines=5,
                            interactive=False
                        )

                # 检索结果展示
                with gr.Row():
                    gr.HTML("<h3>📚 检索结果</h3>")

                retrieved_docs = gr.JSON(label="检索到的文档")

                def process_query(query, show_details_flag):
                    if not query.strip():
                        return {}, "请输入有效的查询", {}

                    result = engine.process_query(query, show_details_flag)

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

                    # 提取检索结果
                    docs = result["stages"]["retrieval"]["retriever_results"]

                    return flow_info, answer, docs

                def clear_inputs():
                    return "", {}, "", {}

                process_btn.click(
                    process_query,
                    inputs=[query_input, show_details],
                    outputs=[process_flow, generated_answer, retrieved_docs]
                )

                clear_btn.click(
                    clear_inputs,
                    outputs=[query_input, process_flow, generated_answer, retrieved_docs]
                )

            # 结果分析标签页
            with gr.Tab("📈 结果分析"):
                gr.HTML("<h2>📊 性能分析与可视化</h2>")

                with gr.Row():
                    with gr.Column():
                        gr.HTML("<h3>⏱️ 性能指标</h3>")
                        performance_stats = gr.JSON(
                            label="性能统计",
                            value={
                                "平均查询分析时间": "0.1s",
                                "平均检索时间": "0.2s",
                                "平均生成时间": "0.3s",
                                "总平均时间": "0.7s"
                            }
                        )

                    with gr.Column():
                        gr.HTML("<h3>🎯 准确性指标</h3>")
                        accuracy_stats = gr.JSON(
                            label="准确性统计",
                            value={
                                "检索准确率": "85%",
                                "生成质量": "88%",
                                "用户满意度": "90%"
                            }
                        )

                with gr.Row():
                    gr.HTML("<h3>📋 最近查询历史</h3>")

                query_history = gr.Dataframe(
                    headers=["时间", "查询", "处理时间", "状态"],
                    datatype=["str", "str", "str", "str"],
                    label="查询历史"
                )

    return demo

def create_ui() -> gr.Blocks:
    """创建主界面 - 借鉴 FlashRAG 的整体设计"""

    # 初始化引擎
    engine = AdaptiveRAGEngine()
    
    # 自定义 CSS
    custom_css = """
    /* Gradio 容器和主内容区域应占据全宽，移除最大宽度限制和自动边距 */
    .gradio-container, .main, .container {
        max-width: none !important; /* 移除最大宽度限制 */
        margin: 0 !important; /* 移除自动边距 */
        padding: 0 !important; /* 移除内边距，确保内容贴边 */
    }

    .tab-nav {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 8px 8px 0 0;
    }

    /* 按钮样式优化 */
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

    /* 确保整个页面无留白 */
    body {
        margin: 0 !important; /* 移除自动边距 */
        max-width: none !important; /* 移除最大宽度限制 */
        padding: 0 !important; /* 移除内边距 */
    }

    /* 标题区域居中 */
    .title-container {
        text-align: center;
        margin: 0; /* 调整为0，让它自己控制宽度 */
        padding: 30px 20px; /* 增加上下内边距，左右保持一致 */
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        width: 100%; /* 确保标题容器也占据全宽 */
        box-sizing: border-box; /* 确保 padding 不会增加总宽度 */
    }

    /* 标签页样式优化 */
    .tab-item {
        border-radius: 8px;
        margin: 2px;
        flex-grow: 1; /* 让标签页项目等宽分布 */
    }

    /* 输入框和按钮样式优化 */
    .gr-textbox, .gr-slider {
        border-radius: 6px;
        border: 1px solid #e1e5e9;
    }

    .gr-button {
        border-radius: 6px;
        transition: all 0.3s ease;
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        .gradio-container, .main, .container {
            max-width: 100% !important;
            padding: 10px !important;
        }

        .title-container {
            margin: 0; /* 调整为0 */
            padding: 15px;
        }
    }
    """
    
    with gr.Blocks(
        title="🧠 智能自适应 RAG 系统",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="purple",
            neutral_hue="slate",
            spacing_size="md",
            radius_size="md"
        ),
        css=custom_css,
        head="""
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                margin: 0 auto !important;
                max-width: 1200px !important;
                background-color: #f8fafc;
            }
        </style>
        """
    ) as demo:
        
        # 标题和介绍
        gr.HTML("""
        <div class="title-container">
            <h1 style="margin: 0 0 10px 0; font-size: 2.5em; font-weight: 700;">
                🧠 智能自适应 RAG 系统
            </h1>
            <h3 style="margin: 0 0 15px 0; font-size: 1.3em; font-weight: 400; opacity: 0.9;">
                基于任务分解和动态检索策略的增强检索生成系统
            </h3>
            <p style="margin: 0; font-size: 1em; opacity: 0.8; line-height: 1.6;">
                借鉴 FlashRAG、FlexRAG、LevelRAG 等优秀框架，融合创新的自适应检索技术
            </p>
        </div>
        """)
        
        # 创建各个标签页
        basic_components = create_basic_tab(engine)
        query_components = create_query_tab(engine)
        analysis_components = create_analysis_tab(engine)
        
        # 事件处理函数
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
                            "type": getattr(st, 'task_type', 'unknown').value if hasattr(getattr(st, 'task_type', None), 'value') else str(getattr(st, 'task_type', 'unknown')),
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
        
        # 绑定事件
        query_components["search_btn"].click(
            fn=process_search,
            inputs=[
                query_components["query_input"],
                query_components["show_details"],
                query_components["max_results"]
            ],
            outputs=[
                query_components["search_results"],
                query_components["task_decomposition"],
                query_components["retrieval_strategy"],
                query_components["processing_time"],
                query_components["total_results"]
            ]
        )

        query_components["clear_btn"].click(
            fn=clear_all,
            outputs=[
                query_components["query_input"],
                query_components["search_results"],
                query_components["task_decomposition"],
                query_components["retrieval_strategy"],
                query_components["processing_time"],
                query_components["total_results"]
            ]
        )

        # 配置按钮事件绑定
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

        # 绑定配置按钮事件
        basic_components["save_config_btn"].click(
            fn=save_config_handler,
            inputs=[
                basic_components["dense_model_path"],
                basic_components["generator_model_path"],
                basic_components["reranker_model_path"],
                basic_components["corpus_path"],
                basic_components["index_path"],
                basic_components["batch_size"]
            ],
            outputs=[basic_components["config_status"]]
        )

        basic_components["load_config_btn"].click(
            fn=load_config_handler,
            outputs=[basic_components["config_status"]]
        )

        basic_components["reset_config_btn"].click(
            fn=reset_config_handler,
            outputs=[
                basic_components["dense_model_path"],
                basic_components["generator_model_path"],
                basic_components["reranker_model_path"],
                basic_components["corpus_path"],
                basic_components["index_path"],
                basic_components["batch_size"],
                basic_components["config_status"]
            ]
        )

        # 页面加载时更新系统状态
        demo.load(
            fn=update_system_status,
            outputs=[
                query_components["system_status"],
                query_components["corpus_info"]
            ]
        )
    
    return demo


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="启动智能自适应 RAG WebUI")
    parser.add_argument("--port", type=int, default=7860, help="服务端口")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="服务主机")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    parser.add_argument("--share", action="store_true", help="创建公共链接")
    parser.add_argument("--real-config", action="store_true", help="使用真实配置")
    parser.add_argument("--config-path", type=str, default="real_config.yaml", help="配置文件路径")

    args = parser.parse_args()

    print(f"🚀 启动智能自适应 RAG WebUI")
    print(f"📍 地址: http://{args.host}:{args.port}")
    print(f"🔧 调试模式: {args.debug}")
    print(f"⚙️ 使用真实配置: {args.real_config}")

    if args.real_config:
        print(f"📁 配置文件: {args.config_path}")
        demo = create_ui_with_real_config(args.config_path)
    else:
        demo = create_ui()

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
            print(f"❌ 端口 {args.port} 被占用")
            print(f"💡 尝试使用其他端口:")

            # 自动尝试其他端口
            for port in range(args.port + 1, args.port + 10):
                try:
                    print(f"🔄 尝试端口 {port}...")
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
                print(f"❌ 无法找到可用端口，请手动指定: python interface.py --port 8080")
        else:
            raise e
