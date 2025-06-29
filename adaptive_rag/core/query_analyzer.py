#!/usr/bin/env python3
"""
=== 查询分析器 - LLM 驱动的智能分析 ===

借鉴 LevelRAG 的核心创新：
1. 使用 LLM 进行查询分解，而非正则表达式
2. 支持上下文感知的动态分解
3. 智能识别查询类型和复杂度
"""

import re
import os
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

# 导入标准库和第三方库
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

logger = logging.getLogger(__name__)


class QueryType(Enum):
    """查询类型枚举"""
    FACTUAL = "factual"          # 事实性问题
    COMPARATIVE = "comparative"   # 比较性问题
    TEMPORAL = "temporal"        # 时间相关问题
    CAUSAL = "causal"           # 因果关系问题
    SUMMARY = "summary"         # 摘要任务
    COMPLEX = "complex"         # 复杂多跳问题


class QueryComplexity(Enum):
    """查询复杂度枚举"""
    SIMPLE = "simple"           # 简单查询
    MODERATE = "moderate"       # 中等复杂度
    COMPLEX = "complex"         # 复杂查询


@dataclass
class SubQuery:
    """子查询数据结构"""
    content: str
    query_type: QueryType
    priority: float = 1.0
    confidence: float = 0.8
    dependencies: List[str] = None


@dataclass
class AnalysisResult:
    """查询分析结果"""
    original_query: str
    query_type: QueryType
    complexity: QueryComplexity
    sub_queries: List[SubQuery]
    keywords: List[str]
    entities: List[str]
    confidence: float


class QueryAnalyzer:
    """
    查询分析器 - 使用 LLM 进行智能分析
    
    核心功能：
    1. 查询类型识别
    2. 复杂度评估
    3. LLM 驱动的查询分解
    4. 关键词和实体提取
    """
    
    def __init__(self, cfg):
        self.cfg = cfg

        # 初始化 LLM 相关变量
        self.llm = None
        self.llm_type = None
        self._llm_pipeline = None

        # 尝试初始化 OpenAI
        if OPENAI_AVAILABLE and hasattr(cfg, 'openai_api_key') and cfg.openai_api_key:
            try:
                self.openai_client = openai.OpenAI(api_key=cfg.openai_api_key)
                self.llm_type = "openai"
                logger.info("OpenAI LLM 初始化成功")
            except Exception as e:
                logger.warning(f"OpenAI LLM 初始化失败: {e}")

        # 不在初始化时加载本地模型，而是延迟加载
        if not self.llm_type:
            logger.info("将使用延迟加载的 Qwen 模型进行 LLM 分解")

        # 加载分解提示模板
        self._init_prompts()
    
    def _init_prompts(self):
        """初始化提示模板 - 借鉴 LevelRAG"""
        # 无上下文分解提示
        self.decompose_prompt = """Please identify the external knowledge necessary to answer the following question. If multiple concurrent pieces of external knowledge are needed, list them all. If the required external knowledge is interdependent, list only the initial piece of external knowledge needed.

Examples:
Question: Which magazine was started first Arthur's Magazine or First for Women?
Answer: [1] When Arthur's Magazine was founded.
[2] When First for Women was founded.

Question: What nationality was Henry Valentine Miller's wife?
Answer: [1] Who was Henry Valentine Miller's wife?

Question: Are director of film Move (1970 Film) and director of film Méditerranée (1963 Film) from the same country?
Answer: [1] Who direct the film Move (1970 Film)?
[2] Who direct the film Méditerranée (1963 Film)?

Question: {query}
Answer: """
        
        # 有上下文分解提示
        self.decompose_with_context_prompt = """Please first indicate the additional knowledge needed to answer the following question. If the question can be answered without external knowledge, answer "No additional information is required".

Examples:
Question: Which magazine was started first Arthur's Magazine or First for Women?
Context: Arthur's Magazine was started in the 19th century. First for Women was started in 1989.
Answer: No additional information is required.

Question: What nationality was Henry Valentine Miller's wife?
Context: Henry Valentine Miller's wife is June Miller.
Answer: [1] What nationality was June Miller?

Question: {query}
Context: {context}
Answer: """
    
    def analyze_query(self, query: str, context: str = "") -> AnalysisResult:
        """
        主要的查询分析方法
        
        Args:
            query: 用户查询
            context: 可选的上下文信息
            
        Returns:
            AnalysisResult: 分析结果
        """
        logger.info(f"开始分析查询: {query}")
        
        # 1. 识别查询类型
        query_type = self._identify_query_type(query)
        
        # 2. 评估复杂度
        complexity = self._assess_complexity(query)
        
        # 3. 提取关键词和实体
        keywords = self._extract_keywords(query)
        entities = self._extract_entities(query)
        
        # 4. LLM 驱动的查询分解
        sub_queries = self._decompose_query(query, context)
        
        # 5. 计算置信度
        confidence = self._calculate_confidence(query_type, complexity, sub_queries)
        
        result = AnalysisResult(
            original_query=query,
            query_type=query_type,
            complexity=complexity,
            sub_queries=sub_queries,
            keywords=keywords,
            entities=entities,
            confidence=confidence
        )
        
        logger.info(f"查询分析完成: {result}")
        return result
    
    def _identify_query_type(self, query: str) -> QueryType:
        """识别查询类型"""
        query_lower = query.lower()
        
        # 比较性问题
        if any(word in query_lower for word in ["compare", "vs", "versus", "difference", "better", "worse"]):
            return QueryType.COMPARATIVE
        
        # 时间相关问题
        if any(word in query_lower for word in ["when", "first", "before", "after", "history", "timeline"]):
            return QueryType.TEMPORAL
        
        # 因果关系问题
        if any(word in query_lower for word in ["why", "how", "cause", "reason", "because", "due to"]):
            return QueryType.CAUSAL
        
        # 摘要任务
        if any(word in query_lower for word in ["summarize", "summary", "main points", "overview"]):
            return QueryType.SUMMARY
        
        # 复杂多跳问题（包含多个实体或关系）
        if len(self._extract_entities(query)) > 2 or "director of" in query_lower:
            return QueryType.COMPLEX
        
        # 默认为事实性问题
        return QueryType.FACTUAL
    
    def _assess_complexity(self, query: str) -> QueryComplexity:
        """评估查询复杂度"""
        # 简单指标
        word_count = len(query.split())
        entity_count = len(self._extract_entities(query))
        
        # 复杂度指标
        complexity_indicators = [
            "director of" in query.lower(),
            "nationality" in query.lower() and "'s" in query,
            " or " in query and "first" in query.lower(),
            word_count > 15,
            entity_count > 3
        ]
        
        complexity_score = sum(complexity_indicators)
        
        if complexity_score >= 3:
            return QueryComplexity.COMPLEX
        elif complexity_score >= 1:
            return QueryComplexity.MODERATE
        else:
            return QueryComplexity.SIMPLE
    
    def _extract_keywords(self, query: str) -> List[str]:
        """提取关键词"""
        # 简单的关键词提取
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "was", "are", "were", "what", "who", "when", "where", "why", "how"}
        
        words = re.findall(r'\b\w+\b', query.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords[:10]  # 返回前10个关键词
    
    def _extract_entities(self, query: str) -> List[str]:
        """提取实体（简单实现）"""
        # 提取大写开头的词组
        entities = re.findall(r'\b[A-Z][a-zA-Z\s]+(?=\s|$|[,.])', query)
        
        # 清理和过滤
        cleaned_entities = []
        for entity in entities:
            entity = entity.strip()
            if len(entity) > 2 and entity not in ["What", "Who", "When", "Where", "Why", "How"]:
                cleaned_entities.append(entity)
        
        return cleaned_entities
    
    def _decompose_query(self, query: str, context: str = "") -> List[SubQuery]:
        """LLM 驱动的查询分解"""
        # 首先尝试使用真实 LLM
        llm_result = self._decompose_with_real_llm(query, context)
        if llm_result:
            return llm_result

        # 回退到规则分解
        logger.warning("LLM 分解失败，使用规则回退")
        return self._rule_based_decompose(query)

    def _decompose_with_real_llm(self, query: str, context: str = "") -> List[SubQuery]:
        """使用真实 LLM 进行分解"""
        try:
            # 初始化 LLM（如果还没有）
            if not hasattr(self, '_llm_pipeline') or not self._llm_pipeline:
                success = self._init_qwen_model()
                if not success:
                    return []

            # 构建 LevelRAG 风格的提示
            prompt = self._build_decomposition_prompt(query, context)

            # 调用 LLM
            response = self._call_qwen_model(prompt)

            # 解析响应
            sub_queries = self._parse_llm_decomposition(response, query)

            logger.info(f"LLM 分解成功: {len(sub_queries)} 个子查询")
            return sub_queries

        except Exception as e:
            logger.error(f"真实 LLM 分解失败: {e}")
            return []

    def _call_openai_llm(self, prompt: str) -> str:
        """调用 OpenAI API"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.1
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API 调用失败: {e}")
            return ""

    def _call_local_llm(self, prompt: str) -> str:
        """调用本地 LLM"""
        try:
            outputs = self.llm(prompt, max_new_tokens=200, temperature=0.1, do_sample=True)
            generated_text = outputs[0]['generated_text']

            # 移除原始提示，只保留生成的部分
            if prompt in generated_text:
                response = generated_text.replace(prompt, "").strip()
            else:
                response = generated_text.strip()

            return response
        except Exception as e:
            logger.error(f"本地 LLM 调用失败: {e}")
            return ""

    def _init_qwen_model(self) -> bool:
        """初始化 Qwen 模型"""
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
            import torch

            model_path = "/root/autodl-tmp/models/qwen1.5-1.8b"

            if not os.path.exists(model_path):
                logger.error(f"Qwen 模型路径不存在: {model_path}")
                return False

            logger.info(f"正在初始化 Qwen 模型: {model_path}")

            # 加载 tokenizer
            tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

            # 加载模型
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else "cpu",
                trust_remote_code=True
            )

            # 创建 pipeline
            self._llm_pipeline = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=200,
                temperature=0.1,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )

            logger.info("✅ Qwen 模型初始化成功")
            return True

        except Exception as e:
            logger.error(f"Qwen 模型初始化失败: {e}")
            return False

    def _build_decomposition_prompt(self, query: str, context: str = "") -> str:
        """构建分解提示（LevelRAG 风格）"""
        if context:
            prompt = f"""Please first indicate the additional knowledge needed to answer the following question based on the given context. If the question can be answered without external knowledge, answer "No additional information is required".

Context: {context}

Question: {query}

Additional knowledge needed:
1."""
        else:
            prompt = f"""Please identify the external knowledge necessary to answer the following question. Break it down into specific sub-questions that need to be answered first.

Question: {query}

Sub-questions:
1."""

        return prompt

    def _call_qwen_model(self, prompt: str) -> str:
        """调用 Qwen 模型"""
        try:
            outputs = self._llm_pipeline(prompt)
            generated_text = outputs[0]['generated_text']

            # 提取生成的部分
            if prompt in generated_text:
                response = generated_text.replace(prompt, "").strip()
            else:
                response = generated_text.strip()

            return response

        except Exception as e:
            logger.error(f"Qwen 模型调用失败: {e}")
            return ""

    def _parse_llm_decomposition(self, response: str, original_query: str) -> List[SubQuery]:
        """解析 LLM 分解响应"""
        if "No additional information is required" in response:
            logger.info("LLM 判断无需分解")
            return []

        sub_queries = []

        # 解析编号的子查询
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 匹配编号格式：1. 2. 3. 等
            import re
            match = re.match(r'^\d+\.\s*(.+)', line)
            if match:
                content = match.group(1).strip()
                if content and len(content) > 5:  # 过滤太短的查询
                    sub_query = SubQuery(
                        content=content,
                        query_type=self._identify_query_type(content),
                        priority=0.9,  # LLM 生成的子查询优先级较高
                        confidence=0.85
                    )
                    sub_queries.append(sub_query)

        # 如果没有找到编号格式，尝试其他解析方法
        if not sub_queries:
            # 查找包含问号的句子
            sentences = response.replace('\n', ' ').split('.')
            for sentence in sentences:
                sentence = sentence.strip()
                if '?' in sentence and len(sentence) > 10:
                    sub_query = SubQuery(
                        content=sentence,
                        query_type=self._identify_query_type(sentence),
                        priority=0.8,
                        confidence=0.75
                    )
                    sub_queries.append(sub_query)

        return sub_queries[:3]  # 最多返回3个子查询
    
    def _parse_decomposition_response(self, response: str, original_query: str) -> List[SubQuery]:
        """解析 LLM 分解响应"""
        if "No additional information is required" in response:
            return []
        
        # 提取编号的子查询
        pattern = r'\[(\d+)\]\s*([^\[\n]+)'
        matches = re.findall(pattern, response)
        
        sub_queries = []
        for i, (num, content) in enumerate(matches):
            sub_query = SubQuery(
                content=content.strip(),
                query_type=self._identify_query_type(content),
                priority=1.0 - i * 0.1,  # 优先级递减
                dependencies=[]
            )
            sub_queries.append(sub_query)
        
        return sub_queries
    
    def _rule_based_decompose(self, query: str) -> List[SubQuery]:
        """基于规则的分解回退"""
        query_lower = query.lower()
        sub_queries = []
        
        # 比较性问题分解
        if "compare" in query_lower or " vs " in query_lower:
            entities = self._extract_entities(query)
            if len(entities) >= 2:
                for i, entity in enumerate(entities[:2]):
                    sub_query = SubQuery(
                        content=f"What is {entity}?",
                        query_type=QueryType.FACTUAL,
                        priority=0.9 - i * 0.1
                    )
                    sub_queries.append(sub_query)
        
        # 时间比较问题分解
        elif "first" in query_lower and " or " in query_lower:
            entities = self._extract_entities(query)
            if len(entities) >= 2:
                for i, entity in enumerate(entities[:2]):
                    sub_query = SubQuery(
                        content=f"When was {entity} founded?",
                        query_type=QueryType.TEMPORAL,
                        priority=0.9 - i * 0.1
                    )
                    sub_queries.append(sub_query)
        
        return sub_queries
    
    def _calculate_confidence(self, query_type: QueryType, complexity: QueryComplexity, sub_queries: List[SubQuery]) -> float:
        """计算分析置信度"""
        base_confidence = 0.8
        
        # 根据复杂度调整
        if complexity == QueryComplexity.SIMPLE:
            base_confidence += 0.1
        elif complexity == QueryComplexity.COMPLEX:
            base_confidence -= 0.1
        
        # 根据分解结果调整
        if sub_queries:
            base_confidence += 0.1
        
        # 根据 LLM 可用性调整
        if not self.llm:
            base_confidence -= 0.2
        
        return max(0.0, min(1.0, base_confidence))
