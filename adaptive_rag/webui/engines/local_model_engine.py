#!/usr/bin/env python3
"""
=== 本地模型引擎 ===

使用 /root/autodl-tmp 目录下的真实模型和数据
"""

import logging
import time
import json
import os
import pickle
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
    from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel
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

try:
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("scikit-learn不可用")


class LocalModelEngine:
    """本地模型引擎 - 使用 /root/autodl-tmp 下的真实模型和数据"""
    
    def __init__(self, config_path: str = "adaptive_rag/config/modular_config.yaml"):
        """初始化本地模型引擎"""
        logger.info("🚀 初始化本地模型引擎...")
        
        self.config_path = config_path
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # 加载配置
        self.load_config()
        
        # 初始化模块管理器
        self.initialize_module_manager()
        
        # 初始化真实组件
        self.initialize_local_components()
        
        # 加载真实数据
        self.load_real_data()
        
        logger.info("✅ 本地模型引擎初始化完成")
    
    def load_config(self):
        """加载配置"""
        try:
            if Path(self.config_path).exists():
                self.config = create_config_from_yaml(self.config_path, preset="performance_mode")
                logger.info(f"✅ 配置文件加载成功: {self.config_path}")
            else:
                logger.warning(f"⚠️ 配置文件不存在: {self.config_path}")
                self.config = FlexRAGIntegratedConfig()
                self.config.modules = ModuleToggleConfig()
        except Exception as e:
            logger.error(f"❌ 配置加载失败: {e}")
            self.config = FlexRAGIntegratedConfig()
            self.config.modules = ModuleToggleConfig()
    
    def initialize_module_manager(self):
        """初始化模块管理器"""
        if MODULE_MANAGER_AVAILABLE:
            try:
                self.module_manager = ModuleManager(self.config)
                self.module_manager.initialize_modules()
                logger.info("✅ 模块管理器初始化成功")
            except Exception as e:
                logger.error(f"❌ 模块管理器初始化失败: {e}")
                self.module_manager = None
        else:
            self.module_manager = None
    
    def initialize_local_components(self):
        """初始化本地组件"""
        self.components = {}
        
        # 获取路径配置
        paths_config = getattr(self.config, 'paths', {})
        models_dir = paths_config.get('models_dir', '/root/autodl-tmp/models')
        
        # 初始化嵌入模型
        if TORCH_AVAILABLE:
            try:
                logger.info("📥 加载本地嵌入模型...")
                embedding_model_path = f"{models_dir}/e5-base-v2"

                if os.path.exists(embedding_model_path):
                    # 优先使用SentenceTransformer加载（适合e5模型）
                    try:
                        from sentence_transformers import SentenceTransformer
                        self.components['embedding_model'] = SentenceTransformer(embedding_model_path)
                        logger.info(f"✅ 本地嵌入模型(SentenceTransformer)加载成功: {embedding_model_path}")
                    except Exception as e:
                        logger.warning(f"⚠️ SentenceTransformer加载失败: {e}")
                        # 尝试使用标准Transformers加载
                        try:
                            self.components['embedding_tokenizer'] = AutoTokenizer.from_pretrained(embedding_model_path)
                            self.components['embedding_model'] = AutoModel.from_pretrained(
                                embedding_model_path,
                                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                                trust_remote_code=True
                            ).to(self.device)
                            logger.info(f"✅ 本地嵌入模型(Transformers)加载成功: {embedding_model_path}")
                        except Exception as e2:
                            logger.error(f"❌ Transformers加载也失败: {e2}")
                            self.components['embedding_model'] = None
                else:
                    # 回退到在线模型
                    logger.warning(f"⚠️ 本地模型不存在: {embedding_model_path}")
                    try:
                        from sentence_transformers import SentenceTransformer
                        self.components['embedding_model'] = SentenceTransformer('intfloat/e5-base-v2')
                        logger.info("✅ 在线嵌入模型加载成功")
                    except Exception as e:
                        logger.error(f"❌ 在线嵌入模型加载失败: {e}")
                        self.components['embedding_model'] = None

            except Exception as e:
                logger.error(f"❌ 嵌入模型加载失败: {e}")
                self.components['embedding_model'] = None
        
        # 初始化重排序模型
        if TORCH_AVAILABLE:
            try:
                logger.info("📥 加载本地重排序模型...")
                reranker_model_path = f"{models_dir}/bge-reranker-base"
                
                if os.path.exists(reranker_model_path):
                    self.components['reranker_tokenizer'] = AutoTokenizer.from_pretrained(reranker_model_path)
                    self.components['reranker_model'] = AutoModelForCausalLM.from_pretrained(
                        reranker_model_path,
                        torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
                    ).to(self.device)
                    logger.info(f"✅ 本地重排序模型加载成功: {reranker_model_path}")
                else:
                    logger.warning(f"⚠️ 本地重排序模型不存在: {reranker_model_path}")
                    self.components['reranker_model'] = None
                    
            except Exception as e:
                logger.error(f"❌ 重排序模型加载失败: {e}")
                self.components['reranker_model'] = None
        
        # 初始化生成模型
        if TORCH_AVAILABLE:
            try:
                logger.info("📥 加载本地生成模型...")
                generator_model_path = f"{models_dir}/Qwen2.5-1.5B-Instruct"
                
                if os.path.exists(generator_model_path):
                    try:
                        self.components['generator_tokenizer'] = AutoTokenizer.from_pretrained(
                            generator_model_path,
                            trust_remote_code=True
                        )
                        self.components['generator_model'] = AutoModelForCausalLM.from_pretrained(
                            generator_model_path,
                            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                            device_map="auto" if self.device == "cuda" else None,
                            trust_remote_code=True
                        )

                        # 设置pad_token
                        if self.components['generator_tokenizer'].pad_token is None:
                            self.components['generator_tokenizer'].pad_token = self.components['generator_tokenizer'].eos_token

                        logger.info(f"✅ 本地生成模型加载成功: {generator_model_path}")
                    except Exception as e:
                        logger.error(f"❌ 本地生成模型加载失败: {e}")
                        self.components['generator_model'] = None
                else:
                    logger.warning(f"⚠️ 本地生成模型不存在: {generator_model_path}")
                    # 尝试加载备用模型
                    backup_models = [
                        f"{models_dir}/Qwen1.5-1.8B-Chat",
                        f"{models_dir}/Qwen2.5-7B-Instruct"
                    ]

                    for backup_path in backup_models:
                        if os.path.exists(backup_path):
                            try:
                                self.components['generator_tokenizer'] = AutoTokenizer.from_pretrained(
                                    backup_path,
                                    trust_remote_code=True
                                )
                                self.components['generator_model'] = AutoModelForCausalLM.from_pretrained(
                                    backup_path,
                                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                                    device_map="auto" if self.device == "cuda" else None,
                                    trust_remote_code=True
                                )

                                if self.components['generator_tokenizer'].pad_token is None:
                                    self.components['generator_tokenizer'].pad_token = self.components['generator_tokenizer'].eos_token

                                logger.info(f"✅ 备用生成模型加载成功: {backup_path}")
                                break
                            except Exception as e:
                                logger.warning(f"⚠️ 备用模型加载失败: {backup_path}, {e}")
                                continue
                    else:
                        self.components['generator_model'] = None
                        
            except Exception as e:
                logger.error(f"❌ 生成模型加载失败: {e}")
                self.components['generator_model'] = None
    
    def load_real_data(self):
        """加载真实数据"""
        try:
            # 获取数据配置
            data_config = getattr(self.config, 'data', {})
            corpus_path = data_config.get('corpus_path', '/root/autodl-tmp/flashrag_real_data/hotpotqa_dev.jsonl')
            cache_dir = data_config.get('cache_dir', '/root/autodl-tmp/flashrag_real_data/cache')
            
            logger.info(f"📥 加载真实数据: {corpus_path}")
            
            # 确保缓存目录存在
            os.makedirs(cache_dir, exist_ok=True)
            
            # 加载数据集
            self.documents = []
            if os.path.exists(corpus_path):
                with open(corpus_path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f):
                        if i >= 1000:  # 限制数据量以节省内存
                            break
                        try:
                            data = json.loads(line.strip())
                            # 适配不同数据格式
                            if 'question' in data and 'answer' in data:
                                # HotpotQA格式
                                doc = {
                                    "id": f"doc_{i}",
                                    "title": data.get('question', '')[:100],
                                    "content": f"问题: {data.get('question', '')}\n答案: {data.get('answer', '')}",
                                    "metadata": data
                                }
                            elif 'query' in data and 'golden_answers' in data:
                                # TriviaQA格式
                                doc = {
                                    "id": f"doc_{i}",
                                    "title": data.get('query', '')[:100],
                                    "content": f"问题: {data.get('query', '')}\n答案: {', '.join(data.get('golden_answers', []))}",
                                    "metadata": data
                                }
                            else:
                                # 通用格式
                                doc = {
                                    "id": f"doc_{i}",
                                    "title": str(data)[:100],
                                    "content": str(data),
                                    "metadata": data
                                }
                            self.documents.append(doc)
                        except Exception as e:
                            logger.warning(f"跳过无效数据行 {i}: {e}")
                            continue
                
                logger.info(f"✅ 加载了 {len(self.documents)} 个文档")
            else:
                logger.warning(f"⚠️ 数据文件不存在: {corpus_path}")
                # 使用示例数据
                self.documents = self._create_sample_documents()
            
            # 初始化BM25检索器
            if BM25_AVAILABLE and self.documents:
                try:
                    bm25_cache_path = os.path.join(cache_dir, "bm25_index.pkl")
                    
                    if os.path.exists(bm25_cache_path):
                        # 加载缓存的BM25索引
                        with open(bm25_cache_path, 'rb') as f:
                            self.components['bm25'] = pickle.load(f)
                        logger.info("✅ BM25索引从缓存加载成功")
                    else:
                        # 创建新的BM25索引
                        doc_texts = [doc['content'] for doc in self.documents]
                        tokenized_docs = [text.split() for text in doc_texts]
                        self.components['bm25'] = BM25Okapi(tokenized_docs)
                        
                        # 保存到缓存
                        with open(bm25_cache_path, 'wb') as f:
                            pickle.dump(self.components['bm25'], f)
                        logger.info("✅ BM25索引创建并缓存成功")
                        
                except Exception as e:
                    logger.error(f"❌ BM25索引初始化失败: {e}")
                    self.components['bm25'] = None
            
            # 预计算文档嵌入
            if self.components.get('embedding_model') and self.documents:
                try:
                    embeddings_cache_path = os.path.join(cache_dir, "document_embeddings.npy")
                    
                    if os.path.exists(embeddings_cache_path):
                        # 加载缓存的嵌入
                        self.document_embeddings = np.load(embeddings_cache_path)
                        logger.info("✅ 文档嵌入从缓存加载成功")
                    else:
                        # 计算新的嵌入
                        doc_texts = [doc['content'] for doc in self.documents]
                        if hasattr(self.components['embedding_model'], 'encode'):
                            # SentenceTransformer模型
                            self.document_embeddings = self.components['embedding_model'].encode(doc_texts)
                        else:
                            # Transformers模型
                            self.document_embeddings = self._compute_embeddings_with_transformers(doc_texts)
                        
                        # 保存到缓存
                        np.save(embeddings_cache_path, self.document_embeddings)
                        logger.info("✅ 文档嵌入计算并缓存成功")
                        
                except Exception as e:
                    logger.error(f"❌ 文档嵌入计算失败: {e}")
                    self.document_embeddings = None
                    
        except Exception as e:
            logger.error(f"❌ 数据加载失败: {e}")
            self.documents = self._create_sample_documents()
            self.document_embeddings = None
    
    def _create_sample_documents(self):
        """创建示例文档"""
        return [
            {
                "id": "sample_1",
                "title": "人工智能基础",
                "content": "人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。",
                "metadata": {}
            },
            {
                "id": "sample_2",
                "title": "机器学习概述", 
                "content": "机器学习是人工智能的一个子集，它使计算机能够在没有明确编程的情况下学习和改进。",
                "metadata": {}
            },
            {
                "id": "sample_3",
                "title": "深度学习技术",
                "content": "深度学习是机器学习的一个分支，使用多层神经网络来模拟人脑的工作方式。",
                "metadata": {}
            }
        ]
    
    def _compute_embeddings_with_transformers(self, texts: List[str]) -> np.ndarray:
        """使用Transformers模型计算嵌入"""
        embeddings = []
        tokenizer = self.components['embedding_tokenizer']
        model = self.components['embedding_model']
        
        for text in texts:
            inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512).to(self.device)
            with torch.no_grad():
                outputs = model(**inputs)
                # 使用[CLS]标记的嵌入或平均池化
                embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
                embeddings.append(embedding[0])
        
        return np.array(embeddings)

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
            subtasks = [query]
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
            web_docs = self.simulate_web_retrieval(query)
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
            result["reranked_results"] = all_retrieved_docs[:5]
            result["module_usage"]["context_reranker"] = False

        # 4. 生成（如果启用）
        if self.is_module_enabled("adaptive_generator"):
            logger.info("✨ 执行自适应生成...")
            answer = self.real_generation(query, result["reranked_results"])
            result["generated_answer"] = answer
            result["steps"].append("自适应生成: 生成最终答案")
            result["module_usage"]["adaptive_generator"] = True
        else:
            contexts = [doc.get('content', '') for doc in result["reranked_results"][:3]]
            result["generated_answer"] = f"基于检索到的信息：{' '.join(contexts[:200])}..."
            result["module_usage"]["adaptive_generator"] = False

        result["total_time"] = time.time() - start_time
        logger.info(f"✅ 查询处理完成，耗时 {result['total_time']:.2f}s")

        return result

    def real_task_decomposition(self, query: str) -> List[str]:
        """真实的任务分解"""
        if "什么是" in query or "介绍" in query:
            return [f"定义: {query}", f"特点: {query}", f"应用: {query}"]
        elif "如何" in query or "怎么" in query:
            return [f"方法: {query}", f"步骤: {query}", f"注意事项: {query}"]
        else:
            return [query]

    def real_keyword_retrieval(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """真实的关键词检索"""
        if not self.components.get('bm25') or not self.documents:
            return []

        try:
            tokenized_query = query.split()
            scores = self.components['bm25'].get_scores(tokenized_query)

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

    def real_dense_retrieval(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """真实的密集检索"""
        if not self.components.get('embedding_model') or self.document_embeddings is None:
            return []

        try:
            # 计算查询嵌入
            if hasattr(self.components['embedding_model'], 'encode'):
                # SentenceTransformer模型
                query_embedding = self.components['embedding_model'].encode([query])
            else:
                # Transformers模型
                query_embedding = self._compute_embeddings_with_transformers([query])

            # 计算相似度
            if SKLEARN_AVAILABLE:
                similarities = cosine_similarity(query_embedding, self.document_embeddings)[0]
            else:
                # 手动计算余弦相似度
                query_norm = np.linalg.norm(query_embedding)
                doc_norms = np.linalg.norm(self.document_embeddings, axis=1)
                similarities = np.dot(query_embedding[0], self.document_embeddings.T) / (query_norm * doc_norms)

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
            # 使用基于匹配度的重排序
            return self._rerank_with_matching(query, documents, top_k)

        except Exception as e:
            logger.error(f"重排序失败: {e}")
            return documents[:top_k]

    def _rerank_with_matching(self, query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
        """基于匹配度的重排序"""
        def rerank_score(doc):
            content = doc.get('content', '')
            title = doc.get('title', '')

            query_words = query.lower().split()
            content_lower = content.lower()
            title_lower = title.lower()

            content_matches = sum(1 for word in query_words if word in content_lower)
            title_matches = sum(1 for word in query_words if word in title_lower)

            original_score = doc.get('score', 0)
            match_score = (title_matches * 2 + content_matches) / len(query_words)

            return original_score * 0.7 + match_score * 0.3

        reranked_docs = sorted(documents, key=rerank_score, reverse=True)

        for i, doc in enumerate(reranked_docs[:top_k]):
            doc['rerank_score'] = rerank_score(doc)
            doc['rerank_position'] = i + 1

        return reranked_docs[:top_k]

    def real_generation(self, query: str, contexts: List[Dict[str, Any]]) -> str:
        """真实的生成"""
        if not self.components.get('generator_model') or not self.components.get('generator_tokenizer'):
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
            tokenizer = self.components['generator_tokenizer']
            model = self.components['generator_model']

            inputs = tokenizer.encode(prompt, return_tensors='pt', max_length=1024, truncation=True)
            if self.device == "cuda":
                inputs = inputs.to(self.device)

            with torch.no_grad():
                outputs = model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 200,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    eos_token_id=tokenizer.eos_token_id
                )

            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

            # 提取回答部分
            if "回答：" in generated_text:
                answer = generated_text.split("回答：")[-1].strip()
            else:
                answer = generated_text[len(prompt):].strip()

            return answer if answer else "抱歉，无法生成合适的回答。"

        except Exception as e:
            logger.error(f"生成失败: {e}")
            if contexts:
                context_text = " ".join([ctx.get('content', '')[:100] for ctx in contexts[:3]])
                return f"基于检索到的信息，关于'{query}'：{context_text}..."
            else:
                return f"抱歉，生成过程中出现错误：{str(e)}"

    def is_module_enabled(self, module_name: str) -> bool:
        """检查模块是否启用"""
        if self.module_manager:
            return self.module_manager.is_module_enabled(module_name)
        return True

    def update_module_config(self, module_config: Dict[str, bool]) -> bool:
        """更新模块配置"""
        try:
            if self.config and hasattr(self.config, 'modules'):
                for module_name, enabled in module_config.items():
                    if hasattr(self.config.modules, module_name):
                        setattr(self.config.modules, module_name, enabled)

                if self.module_manager:
                    self.module_manager = ModuleManager(self.config)
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
                    "status": "✅ 本地模型引擎正常运行",
                    "components_available": {
                        "torch": TORCH_AVAILABLE,
                        "bm25": BM25_AVAILABLE,
                        "sklearn": SKLEARN_AVAILABLE,
                        "embedding_model": self.components.get('embedding_model') is not None,
                        "generator_model": self.components.get('generator_model') is not None,
                        "reranker_model": self.components.get('reranker_model') is not None,
                        "documents_count": len(self.documents) if hasattr(self, 'documents') else 0
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
                        "bm25": BM25_AVAILABLE,
                        "sklearn": SKLEARN_AVAILABLE
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

    def get_performance_metrics(self) -> Dict[str, Any]:
        """获取性能指标"""
        try:
            import psutil
            import torch

            # CPU和内存信息
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()

            # GPU信息
            gpu_info = {}
            if torch.cuda.is_available():
                gpu_info = {
                    "gpu_available": True,
                    "gpu_memory_allocated": torch.cuda.memory_allocated() / 1024**3,  # GB
                    "gpu_memory_reserved": torch.cuda.memory_reserved() / 1024**3,   # GB
                    "gpu_device_name": torch.cuda.get_device_name()
                }
            else:
                gpu_info = {"gpu_available": False}

            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used_gb": memory.used / 1024**3,
                "memory_total_gb": memory.total / 1024**3,
                "documents_loaded": len(self.documents) if hasattr(self, 'documents') else 0,
                "components_loaded": sum(1 for comp in self.components.values() if comp is not None),
                **gpu_info
            }
        except Exception as e:
            logger.error(f"获取性能指标失败: {e}")
            return {
                "cpu_percent": 0,
                "memory_percent": 0,
                "error": str(e)
            }

    def get_resource_usage(self) -> Dict[str, Any]:
        """获取资源使用情况"""
        return self.get_performance_metrics()

    def process_query(self, query: str) -> Dict[str, Any]:
        """兼容性方法：处理查询"""
        return self.process_query_with_modules(query)

    def get_current_module_config(self) -> Dict[str, bool]:
        """获取当前模块配置"""
        try:
            if self.config and hasattr(self.config, 'modules'):
                return {
                    name: getattr(self.config.modules, name, False)
                    for name in dir(self.config.modules)
                    if not name.startswith('_')
                }
            else:
                return {}
        except Exception as e:
            logger.error(f"❌ 获取模块配置失败: {e}")
            return {}
