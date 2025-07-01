"""
使用真实配置的 AdaptiveRAG 引擎
"""

import time
import yaml
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from adaptive_rag.config import create_flexrag_integrated_config, FLEXRAG_AVAILABLE
from adaptive_rag.core.flexrag_integrated_assistant import FlexRAGIntegratedAssistant
from .mock_data_manager import MockDataManager


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