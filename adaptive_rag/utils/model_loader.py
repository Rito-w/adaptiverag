import os
import yaml
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import SentenceTransformer
# from dashscope import Generation # 假设通义千问使用dashscope SDK
# from modelscope.pipelines import pipeline # 假设通义千问模型使用modelscope

from adaptive_rag.utils.logger import get_logger

logger = get_logger(__name__)

class ModelLoader:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.loaded_models = {} # 缓存已加载的模型

    def _load_config(self, config_path: str):
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def load_llm(self, model_name: str = None):
        """
        加载并返回一个LLM实例。
        根据配置选择不同的LLM提供商（如通义千问、OpenAI）。
        """
        if model_name is None:
            model_name = self.config['llm']['default_model']

        if model_name in self.loaded_models:
            return self.loaded_models[model_name]

        llm_config = None
        for provider, config in self.config['llm']['providers'].items():
            if provider in model_name.lower() or model_name.lower() == config.get('model_name', '').lower().split('-')[0]:
                llm_config = config
                break

        if llm_config is None:
            raise ValueError(f"Unsupported LLM model: {model_name}. Please check your config/basic_config.yaml.")

        logger.info(f"Loading LLM: {model_name} from provider: {provider}")

        # 根据提供商加载LLM
        if "qwen" in provider:
            # 假设使用ModelScope或DashScope加载通义千问
            # 如果是本地模型，可能需要transformers
            try:
                # 示例：使用transformers加载本地Qwen模型
                tokenizer = AutoTokenizer.from_pretrained(llm_config['model_path'], trust_remote_code=True)
                model = AutoModel.from_pretrained(llm_config['model_path'], trust_remote_code=True).eval()
                # 在实际项目中，这里可能需要一个封装LLM交互的类
                # 例如：return QwenLLM(tokenizer, model)
                llm_instance = (tokenizer, model) # 简单示例，实际应是LLM类实例
                logger.warning("Qwen local model loading is a placeholder. You might need to adjust based on specific Qwen serving setup (e.g., vLLM, FastChat).")
            except ImportError:
                logger.error("Could not import necessary libraries for Qwen. Make sure dashscope or modelscope is installed if needed.")
                raise
            except Exception as e:
                logger.error(f"Error loading Qwen local model: {e}")
                raise
        elif "openai" in provider:
            from openai import OpenAI
            client = OpenAI(api_key=llm_config['api_key'])
            # 封装 OpenAI 交互
            llm_instance = client # 简单示例，实际应是LLM类实例
        else:
            raise NotImplementedError(f"LLM provider '{provider}' not implemented yet.")

        self.loaded_models[model_name] = llm_instance
        return llm_instance

    def load_embedding_model(self, model_name: str = None):
        """
        加载并返回一个嵌入模型实例。
        """
        if model_name is None:
            model_name = self.config['retriever']['default_dense_model']

        if model_name in self.loaded_models:
            return self.loaded_models[model_name]

        logger.info(f"Loading Embedding Model: {model_name}")
        try:
            model = SentenceTransformer(model_name)
        except Exception as e:
            logger.error(f"Error loading embedding model {model_name}: {e}")
            raise

        self.loaded_models[model_name] = model
        return model

    def load_reranker_model(self, model_name: str = None):
        """
        加载并返回一个重排序模型实例。
        """
        if model_name is None:
            model_name = self.config['refiner']['default_reranker_model']

        if model_name in self.loaded_models:
            return self.loaded_models[model_name]

        logger.info(f"Loading Reranker Model: {model_name}")
        try:
            # 重排序模型通常也是SentenceTransformer或HuggingFace模型
            model = SentenceTransformer(model_name) # 假设使用SentenceTransformer
            # 或者使用transformers库加载
            # tokenizer = AutoTokenizer.from_pretrained(model_name)
            # model = AutoModelForSequenceClassification.from_pretrained(model_name)
        except Exception as e:
            logger.error(f"Error loading reranker model {model_name}: {e}")
            raise

        self.loaded_models[model_name] = model
        return model

    # 可以添加其他模型加载方法，例如：
    # def load_sparse_retriever_backend(self, backend_name: str = None):
    #     """
    #     加载稀疏检索后端 (如Pyserini或bm25s)。
    #     """
    #     if backend_name is None:
    #         backend_name = self.config['retriever']['default_sparse_model']
    #     # ... 根据backend_name加载并返回实例
    #     pass 