#!/usr/bin/env python3
"""
=== 真实模型引擎 ===

使用真实的模型和数据，让模块开关效果明显可见
"""

import logging
import time
import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logger = logging.getLogger(__name__)

# 导入模块管理器
try:
    from adaptive_rag.core.module_manager import ModuleManager
    from adaptive_rag.config import (
        create_config_from_yaml, ModuleToggleConfig, 
        FlexRAGIntegratedConfig, get_enabled_modules
    )
    MODULE_MANAGER_AVAILABLE = True
except ImportError:
    MODULE_MANAGER_AVAILABLE = False
    logger.warning("模块管理器不可用")

# 导入真实组件
try:
    import torch
    from sentence_transformers import SentenceTransformer
    from transformers import AutoTokenizer, AutoModelForCausalLM
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logger.warning("PyTorch组件不可用")

try:
    from rank_bm25 import BM25Okapi
    BM25_AVAILABLE = True
except ImportError:
    BM25_AVAILABLE = False
    logger.warning("BM25不可用")


class RealModelEngine:
    """真实模型引擎 - 使用真实的检索器、重排序器和生成器"""
    
    def __init__(self, config_path: str = "adaptive_rag/config/modular_config.yaml"):
        """初始化真实模型引擎"""
        logger.info("🚀 初始化真实模型引擎...")
        
        self.config_path = config_path
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # 初始化模块管理器
        self.initialize_module_manager()
        
        # 初始化真实组件
        self.initialize_real_components()
        
        # 加载真实数据
        self.load_real_data()
        
        logger.info("✅ 真实模型引擎初始化完成")
    
    def initialize_module_manager(self):
        """初始化模块管理器"""
        if MODULE_MANAGER_AVAILABLE:
            try:
                # 加载模块化配置
                if Path(self.config_path).exists():
                    self.modular_config = create_config_from_yaml(self.config_path, preset="performance_mode")
                else:
                    self.modular_config = FlexRAGIntegratedConfig()
                    self.modular_config.modules = ModuleToggleConfig()
                
                # 初始化模块管理器
                self.module_manager = ModuleManager(self.modular_config)
                self.module_manager.initialize_modules()
                
                logger.info("✅ 模块管理器初始化成功")
            except Exception as e:
                logger.error(f"❌ 模块管理器初始化失败: {e}")
                self.module_manager = None
                self.modular_config = None
        else:
            self.module_manager = None
            self.modular_config = None
    
    def initialize_real_components(self):
        """初始化真实组件"""
        self.components = {}
        
        # 初始化嵌入模型（用于密集检索）
        if TORCH_AVAILABLE:
            try:
                logger.info("📥 加载嵌入模型...")
                self.components['embedding_model'] = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("✅ 嵌入模型加载成功")
            except Exception as e:
                logger.error(f"❌ 嵌入模型加载失败: {e}")
                self.components['embedding_model'] = None
        
        # 初始化生成模型
        if TORCH_AVAILABLE:
            try:
                logger.info("📥 加载生成模型...")
                # 使用较小的模型以节省资源
                model_name = "microsoft/DialoGPT-small"
                self.components['tokenizer'] = AutoTokenizer.from_pretrained(model_name)
                self.components['generator'] = AutoModelForCausalLM.from_pretrained(model_name)
                
                # 设置pad_token
                if self.components['tokenizer'].pad_token is None:
                    self.components['tokenizer'].pad_token = self.components['tokenizer'].eos_token
                
                logger.info("✅ 生成模型加载成功")
            except Exception as e:
                logger.error(f"❌ 生成模型加载失败: {e}")
                self.components['tokenizer'] = None
                self.components['generator'] = None
    
    def load_real_data(self):
        """加载真实数据"""
        # 创建示例文档库
        self.documents = [
            {
                "id": "doc_1",
                "title": "人工智能基础",
                "content": "人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。这包括学习、推理、问题解决、感知和语言理解。"
            },
            {
                "id": "doc_2", 
                "title": "机器学习概述",
                "content": "机器学习是人工智能的一个子集，它使计算机能够在没有明确编程的情况下学习和改进。它基于算法和统计模型，使系统能够从数据中学习模式。"
            },
            {
                "id": "doc_3",
                "title": "深度学习技术",
                "content": "深度学习是机器学习的一个分支，使用多层神经网络来模拟人脑的工作方式。它在图像识别、自然语言处理和语音识别等领域取得了突破性进展。"
            },
            {
                "id": "doc_4",
                "title": "自然语言处理",
                "content": "自然语言处理（NLP）是人工智能的一个领域，专注于计算机与人类语言之间的交互。它包括文本分析、语言生成、机器翻译和情感分析等任务。"
            },
            {
                "id": "doc_5",
                "title": "计算机视觉",
                "content": "计算机视觉是人工智能的一个分支，使计算机能够理解和解释视觉信息。它涉及图像处理、物体检测、人脸识别和场景理解等技术。"
            }
        ]
        
        # 初始化BM25检索器
        if BM25_AVAILABLE:
            try:
                # 准备文档文本用于BM25
                doc_texts = [doc['content'] for doc in self.documents]
                tokenized_docs = [text.split() for text in doc_texts]
                self.components['bm25'] = BM25Okapi(tokenized_docs)
                logger.info("✅ BM25检索器初始化成功")
            except Exception as e:
                logger.error(f"❌ BM25检索器初始化失败: {e}")
                self.components['bm25'] = None
        
        # 预计算文档嵌入
        if self.components.get('embedding_model'):
            try:
                doc_texts = [doc['content'] for doc in self.documents]
                self.document_embeddings = self.components['embedding_model'].encode(doc_texts)
                logger.info("✅ 文档嵌入预计算完成")
            except Exception as e:
                logger.error(f"❌ 文档嵌入计算失败: {e}")
                self.document_embeddings = None
    
    def process_query_with_modules(self, query: str) -> Dict[str, Any]:
        """根据启用的模块处理查询"""
        start_time = time.time()
        result = {
            "query": query,
            "steps": [],
            "retrieval_results": [],
            "reranked_results": [],
            "generated_answer": "",
            "total_time": 0,
            "module_usage": {}
        }
        
        logger.info(f"🔍 处理查询: {query}")
        
        # 1. 任务分解（如果启用）
        if self.is_module_enabled("task_decomposer"):
            logger.info("📋 执行任务分解...")
            subtasks = self.real_task_decomposition(query)
            result["steps"].append(f"任务分解: 识别到 {len(subtasks)} 个子任务")
            result["module_usage"]["task_decomposer"] = True
        else:
            subtasks = [query]  # 不分解，直接使用原查询
            result["module_usage"]["task_decomposer"] = False
        
        # 2. 检索阶段
        all_retrieved_docs = []
        
        # 关键词检索（如果启用）
        if self.is_module_enabled("keyword_retriever"):
            logger.info("🔍 执行关键词检索...")
            keyword_docs = self.real_keyword_retrieval(query)
            all_retrieved_docs.extend(keyword_docs)
            result["steps"].append(f"关键词检索: 找到 {len(keyword_docs)} 个文档")
            result["module_usage"]["keyword_retriever"] = True
        else:
            result["module_usage"]["keyword_retriever"] = False
        
        # 密集检索（如果启用）
        if self.is_module_enabled("dense_retriever"):
            logger.info("🧠 执行密集检索...")
            dense_docs = self.real_dense_retrieval(query)
            all_retrieved_docs.extend(dense_docs)
            result["steps"].append(f"密集检索: 找到 {len(dense_docs)} 个文档")
            result["module_usage"]["dense_retriever"] = True
        else:
            result["module_usage"]["dense_retriever"] = False
        
        # 网络检索（如果启用）
        if self.is_module_enabled("web_retriever"):
            logger.info("🌐 执行网络检索...")
            web_docs = self.simulate_web_retrieval(query)  # 模拟网络检索
            all_retrieved_docs.extend(web_docs)
            result["steps"].append(f"网络检索: 找到 {len(web_docs)} 个文档")
            result["module_usage"]["web_retriever"] = True
        else:
            result["module_usage"]["web_retriever"] = False
        
        result["retrieval_results"] = all_retrieved_docs
        
        # 3. 重排序（如果启用）
        if self.is_module_enabled("context_reranker") and all_retrieved_docs:
            logger.info("🎯 执行上下文重排序...")
            reranked_docs = self.real_reranking(query, all_retrieved_docs)
            result["reranked_results"] = reranked_docs
            result["steps"].append(f"重排序: 重新排序 {len(reranked_docs)} 个文档")
            result["module_usage"]["context_reranker"] = True
        else:
            result["reranked_results"] = all_retrieved_docs[:5]  # 取前5个
            result["module_usage"]["context_reranker"] = False
        
        # 4. 生成（如果启用）
        if self.is_module_enabled("adaptive_generator"):
            logger.info("✨ 执行自适应生成...")
            answer = self.real_generation(query, result["reranked_results"])
            result["generated_answer"] = answer
            result["steps"].append("自适应生成: 生成最终答案")
            result["module_usage"]["adaptive_generator"] = True
        else:
            # 简单拼接检索结果
            contexts = [doc.get('content', '') for doc in result["reranked_results"][:3]]
            result["generated_answer"] = f"基于检索到的信息：{' '.join(contexts[:200])}..."
            result["module_usage"]["adaptive_generator"] = False
        
        result["total_time"] = time.time() - start_time
        logger.info(f"✅ 查询处理完成，耗时 {result['total_time']:.2f}s")
        
        return result
    
    def real_task_decomposition(self, query: str) -> List[str]:
        """真实的任务分解"""
        # 简单的基于关键词的任务分解
        if "什么是" in query or "介绍" in query:
            return [f"定义: {query}", f"特点: {query}", f"应用: {query}"]
        elif "如何" in query or "怎么" in query:
            return [f"方法: {query}", f"步骤: {query}", f"注意事项: {query}"]
        else:
            return [query]
    
    def real_keyword_retrieval(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """真实的关键词检索"""
        if not self.components.get('bm25'):
            return []
        
        try:
            # 使用BM25进行检索
            tokenized_query = query.split()
            scores = self.components['bm25'].get_scores(tokenized_query)
            
            # 获取top_k结果
            top_indices = scores.argsort()[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                if idx < len(self.documents):
                    doc = self.documents[idx].copy()
                    doc['score'] = float(scores[idx])
                    doc['retrieval_type'] = 'keyword'
                    results.append(doc)
            
            return results
        except Exception as e:
            logger.error(f"关键词检索失败: {e}")
            return []
    
    def real_dense_retrieval(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """真实的密集检索"""
        if not self.components.get('embedding_model') or self.document_embeddings is None:
            return []
        
        try:
            # 计算查询嵌入
            query_embedding = self.components['embedding_model'].encode([query])
            
            # 计算相似度
            from sklearn.metrics.pairwise import cosine_similarity
            similarities = cosine_similarity(query_embedding, self.document_embeddings)[0]
            
            # 获取top_k结果
            top_indices = similarities.argsort()[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                if idx < len(self.documents):
                    doc = self.documents[idx].copy()
                    doc['score'] = float(similarities[idx])
                    doc['retrieval_type'] = 'dense'
                    results.append(doc)
            
            return results
        except Exception as e:
            logger.error(f"密集检索失败: {e}")
            return []
    
    def simulate_web_retrieval(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        """模拟网络检索"""
        # 模拟网络搜索结果
        web_results = [
            {
                "id": f"web_{i}",
                "title": f"网络搜索结果 {i}: {query}",
                "content": f"这是来自网络的关于'{query}'的搜索结果 {i}。包含最新的相关信息。",
                "score": 0.8 - i * 0.1,
                "retrieval_type": "web",
                "url": f"https://example.com/result_{i}"
            }
            for i in range(top_k)
        ]
        return web_results
    
    def real_reranking(self, query: str, documents: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        """真实的重排序"""
        if not documents:
            return []
        
        try:
            # 简单的基于内容长度和查询匹配的重排序
            def rerank_score(doc):
                content = doc.get('content', '')
                title = doc.get('title', '')
                
                # 计算查询词在文档中的出现次数
                query_words = query.lower().split()
                content_lower = content.lower()
                title_lower = title.lower()
                
                content_matches = sum(1 for word in query_words if word in content_lower)
                title_matches = sum(1 for word in query_words if word in title_lower)
                
                # 综合评分：原始分数 + 匹配分数
                original_score = doc.get('score', 0)
                match_score = (title_matches * 2 + content_matches) / len(query_words)
                
                return original_score * 0.7 + match_score * 0.3
            
            # 重新排序
            reranked_docs = sorted(documents, key=rerank_score, reverse=True)
            
            # 更新分数
            for i, doc in enumerate(reranked_docs[:top_k]):
                doc['rerank_score'] = rerank_score(doc)
                doc['rerank_position'] = i + 1
            
            return reranked_docs[:top_k]
            
        except Exception as e:
            logger.error(f"重排序失败: {e}")
            return documents[:top_k]
    
    def real_generation(self, query: str, contexts: List[Dict[str, Any]]) -> str:
        """真实的生成"""
        if not self.components.get('generator') or not self.components.get('tokenizer'):
            # 回退到简单拼接
            if contexts:
                context_text = " ".join([ctx.get('content', '')[:100] for ctx in contexts[:3]])
                return f"基于检索到的信息，关于'{query}'：{context_text}..."
            else:
                return f"抱歉，没有找到关于'{query}'的相关信息。"
        
        try:
            # 构建提示词
            context_text = "\n".join([f"- {ctx.get('content', '')[:200]}" for ctx in contexts[:3]])
            prompt = f"基于以下信息回答问题：\n{context_text}\n\n问题：{query}\n回答："
            
            # 生成回答
            inputs = self.components['tokenizer'].encode(prompt, return_tensors='pt', max_length=512, truncation=True)
            
            with torch.no_grad():
                outputs = self.components['generator'].generate(
                    inputs,
                    max_length=inputs.shape[1] + 100,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.components['tokenizer'].eos_token_id
                )
            
            # 解码生成的文本
            generated_text = self.components['tokenizer'].decode(outputs[0], skip_special_tokens=True)
            
            # 提取回答部分
            if "回答：" in generated_text:
                answer = generated_text.split("回答：")[-1].strip()
            else:
                answer = generated_text[len(prompt):].strip()
            
            return answer if answer else "抱歉，无法生成合适的回答。"
            
        except Exception as e:
            logger.error(f"生成失败: {e}")
            # 回退到简单拼接
            if contexts:
                context_text = " ".join([ctx.get('content', '')[:100] for ctx in contexts[:3]])
                return f"基于检索到的信息，关于'{query}'：{context_text}..."
            else:
                return f"抱歉，生成过程中出现错误：{str(e)}"
    
    def is_module_enabled(self, module_name: str) -> bool:
        """检查模块是否启用"""
        if self.module_manager:
            return self.module_manager.is_module_enabled(module_name)
        return True  # 默认启用
    
    def update_module_config(self, module_config: Dict[str, bool]) -> bool:
        """更新模块配置"""
        try:
            if self.modular_config and hasattr(self.modular_config, 'modules'):
                # 更新模块开关配置
                for module_name, enabled in module_config.items():
                    if hasattr(self.modular_config.modules, module_name):
                        setattr(self.modular_config.modules, module_name, enabled)
                
                # 重新初始化模块管理器
                if self.module_manager:
                    self.module_manager = ModuleManager(self.modular_config)
                    self.module_manager.initialize_modules()
                
                logger.info(f"✅ 模块配置已更新，启用模块数: {sum(module_config.values())}")
                return True
            else:
                logger.warning("⚠️ 模块配置对象不可用")
                return False
        except Exception as e:
            logger.error(f"❌ 更新模块配置失败: {e}")
            return False
    
    def get_module_status(self) -> Dict[str, Any]:
        """获取模块状态"""
        try:
            if self.module_manager:
                status = self.module_manager.get_module_status()
                enabled_modules = self.module_manager.get_enabled_modules()
                
                return {
                    "module_status": status,
                    "enabled_modules": enabled_modules,
                    "enabled_count": len(enabled_modules),
                    "total_count": len(status),
                    "status": "✅ 真实模型引擎正常运行",
                    "components_available": {
                        "torch": TORCH_AVAILABLE,
                        "bm25": BM25_AVAILABLE,
                        "embedding_model": self.components.get('embedding_model') is not None,
                        "generator": self.components.get('generator') is not None
                    }
                }
            else:
                return {
                    "module_status": {},
                    "enabled_modules": [],
                    "enabled_count": 0,
                    "total_count": 0,
                    "status": "⚠️ 模块管理器不可用",
                    "components_available": {
                        "torch": TORCH_AVAILABLE,
                        "bm25": BM25_AVAILABLE
                    }
                }
        except Exception as e:
            logger.error(f"❌ 获取模块状态失败: {e}")
            return {
                "module_status": {},
                "enabled_modules": [],
                "enabled_count": 0,
                "total_count": 0,
                "status": f"❌ 获取状态失败: {e}",
                "components_available": {}
            }
