#!/usr/bin/env python3
"""
=== FlexRAG 集成生成器 ===

深度集成 FlexRAG 的生成器组件
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)

# 导入统一的数据结构
from ..retriever.flexrag_integrated_retriever import RetrievedContext

# 尝试导入 FlexRAG 组件
try:
    from flexrag.models import GENERATORS, GeneratorConfig, HFGenerator, OpenAIGenerator
    FLEXRAG_AVAILABLE = True
except ImportError:
    logger.warning("FlexRAG 未安装，将使用模拟生成实现")
    FLEXRAG_AVAILABLE = False


@dataclass
class GenerationResult:
    """生成结果"""
    query: str
    answer: str
    generator_type: str
    generation_time: float
    used_contexts: List[RetrievedContext]
    metadata: Dict[str, Any] = None


class FlexRAGIntegratedGenerator:
    """
    集成 FlexRAG 生成器的自适应生成器
    
    支持多种生成策略：
    1. HuggingFace 模型生成
    2. OpenAI API 生成
    3. 本地 VLLM 生成
    4. 多生成器融合
    """
    
    def __init__(self, config):
        self.config = config
        self.generators = {}
        self.fallback_mode = not FLEXRAG_AVAILABLE
        
        if FLEXRAG_AVAILABLE:
            self._init_flexrag_generators()
        else:
            self._init_fallback_generators()
        
        logger.info(f"FlexRAG 集成生成器初始化完成 (FlexRAG可用: {FLEXRAG_AVAILABLE})")
    
    def _init_flexrag_generators(self):
        """初始化 FlexRAG 生成器"""
        try:
            generator_configs = getattr(self.config, 'generator_configs', {})

            for name, config_dict in generator_configs.items():
                try:
                    # 检查是否使用模拟实现
                    if config_dict.get("generator_type") == "mock" or not FLEXRAG_AVAILABLE:
                        self.generators[name] = self._create_mock_generator(name)
                        logger.info(f"✅ 使用模拟生成器: {name}")
                    else:
                        generator_config = GeneratorConfig(**config_dict)
                        generator = GENERATORS.load(generator_config)
                        self.generators[name] = generator
                        logger.info(f"✅ 成功加载 FlexRAG 生成器: {name}")

                except Exception as e:
                    logger.warning(f"⚠️ 加载生成器 {name} 失败: {e}，将使用模拟实现")
                    self.generators[name] = self._create_mock_generator(name)

            # 如果没有成功加载任何生成器，使用模拟实现
            if not self.generators:
                logger.warning("未能加载任何生成器，使用模拟实现")
                self._init_fallback_generators()

        except Exception as e:
            logger.error(f"初始化生成器失败: {e}")
            self._init_fallback_generators()
    
    def _init_fallback_generators(self):
        """初始化回退生成器（模拟实现）"""
        self.generators = {
            "main_generator": self._create_mock_generator("main"),
            "openai_generator": self._create_mock_generator("openai")
        }
        logger.info("使用模拟生成器实现")
    
    def _create_mock_generator(self, generator_type: str):
        """创建模拟生成器"""
        class MockGenerator:
            def __init__(self, gtype):
                self.generator_type = gtype
            
            def generate(self, prompt: str, **kwargs) -> str:
                """模拟生成"""
                max_tokens = kwargs.get("max_tokens", 256)
                
                # 模拟生成回答
                if "what is" in prompt.lower():
                    answer = f"根据提供的上下文信息，这是一个关于定义的问题。基于{self.generator_type}生成器的分析..."
                elif "compare" in prompt.lower():
                    answer = f"通过对比分析，我们可以看到两者之间的主要区别在于...（{self.generator_type}生成）"
                elif "when" in prompt.lower():
                    answer = f"根据时间相关的信息，这个事件发生在...（{self.generator_type}生成）"
                else:
                    answer = f"基于提供的上下文，我的回答是...（{self.generator_type}生成器生成的模拟回答）"
                
                # 限制长度
                if len(answer) > max_tokens:
                    answer = answer[:max_tokens] + "..."
                
                return answer
        
        return MockGenerator(generator_type)
    
    def adaptive_generate(
        self,
        query: str,
        contexts: List[RetrievedContext],
        strategy: Dict[str, Any]
    ) -> GenerationResult:
        """
        自适应生成主方法
        
        Args:
            query: 查询字符串
            contexts: 检索到的上下文列表
            strategy: 生成策略配置
            
        Returns:
            GenerationResult: 生成结果
        """
        start_time = time.time()
        
        # 解析策略配置
        generator_name = strategy.get("generator", "main_generator")
        enable_multi_generator = strategy.get("enable_multi_generator", False)
        max_tokens = strategy.get("max_tokens", 256)
        temperature = strategy.get("temperature", 0.7)
        
        # 构建提示词
        prompt = self._build_prompt(query, contexts, strategy)
        
        if enable_multi_generator:
            # 多生成器融合
            answer = self._multi_generator_fusion(prompt, strategy)
        else:
            # 单一生成器
            answer = self._single_generator_process(prompt, generator_name, {
                "max_tokens": max_tokens,
                "temperature": temperature
            })
        
        generation_time = time.time() - start_time
        
        result = GenerationResult(
            query=query,
            answer=answer,
            generator_type=generator_name if not enable_multi_generator else "multi_generator",
            generation_time=generation_time,
            used_contexts=contexts,
            metadata={
                "strategy": strategy,
                "prompt_length": len(prompt),
                "context_count": len(contexts),
                "flexrag_mode": not self.fallback_mode
            }
        )
        
        logger.info(f"生成完成: {len(answer)} 字符，耗时 {generation_time:.3f}s")
        return result
    
    def _build_prompt(
        self,
        query: str,
        contexts: List[RetrievedContext],
        strategy: Dict[str, Any]
    ) -> str:
        """构建生成提示词"""
        
        prompt_template = strategy.get("prompt_template", "default")
        max_context_length = strategy.get("max_context_length", 2000)
        
        # 选择最相关的上下文
        selected_contexts = self._select_contexts(contexts, max_context_length)
        
        if prompt_template == "default":
            # 默认提示词模板
            context_text = "\n\n".join([
                f"文档 {i+1}: {ctx.content}"
                for i, ctx in enumerate(selected_contexts)
            ])
            
            prompt = f"""请基于以下上下文信息回答问题。

上下文信息:
{context_text}

问题: {query}

请提供准确、详细的回答："""
        
        elif prompt_template == "step_by_step":
            # 步骤式提示词模板（借鉴 LevelRAG）
            context_text = "\n\n".join([
                f"[文档{i+1}] {ctx.content}"
                for i, ctx in enumerate(selected_contexts)
            ])
            
            prompt = f"""请按照以下步骤回答问题：

1. 首先分析问题的类型和要求
2. 从提供的文档中提取相关信息
3. 综合信息给出最终答案

提供的文档:
{context_text}

问题: {query}

请按步骤分析并回答："""
        
        elif prompt_template == "comparative":
            # 比较性问题模板
            context_text = "\n\n".join([
                f"资料 {i+1}: {ctx.content}"
                for i, ctx in enumerate(selected_contexts)
            ])
            
            prompt = f"""请基于提供的资料进行比较分析。

参考资料:
{context_text}

比较问题: {query}

请从多个维度进行对比分析："""
        
        else:
            # 自定义模板
            context_text = "\n".join([ctx.content for ctx in selected_contexts])
            prompt = strategy.get("custom_prompt", "").format(
                query=query,
                context=context_text
            )
        
        return prompt
    
    def _select_contexts(
        self,
        contexts: List[RetrievedContext],
        max_length: int
    ) -> List[RetrievedContext]:
        """选择最相关的上下文，控制总长度"""
        
        selected = []
        total_length = 0
        
        # 按分数排序，选择最相关的
        sorted_contexts = sorted(contexts, key=lambda x: x.score, reverse=True)
        
        for ctx in sorted_contexts:
            ctx_length = len(ctx.content)
            if total_length + ctx_length <= max_length:
                selected.append(ctx)
                total_length += ctx_length
            else:
                # 如果剩余空间不够，尝试截断
                remaining_space = max_length - total_length
                if remaining_space > 100:  # 至少保留100字符
                    truncated_ctx = RetrievedContext(
                        content=ctx.content[:remaining_space] + "...",
                        score=ctx.score,
                        metadata=ctx.metadata
                    )
                    selected.append(truncated_ctx)
                break
        
        return selected
    
    def _single_generator_process(
        self,
        prompt: str,
        generator_name: str,
        generation_params: Dict[str, Any]
    ) -> str:
        """单一生成器处理"""
        
        if generator_name not in self.generators:
            logger.warning(f"生成器 {generator_name} 不存在，使用默认生成器")
            generator_name = list(self.generators.keys())[0]
        
        generator = self.generators[generator_name]
        
        try:
            if FLEXRAG_AVAILABLE and hasattr(generator, 'generate'):
                # 使用 FlexRAG 生成器
                answer = generator.generate(prompt, **generation_params)
            else:
                # 使用模拟生成器
                answer = generator.generate(prompt, **generation_params)
            
            return answer
            
        except Exception as e:
            logger.error(f"生成器 {generator_name} 执行失败: {e}")
            return f"抱歉，生成过程中出现错误：{str(e)}"
    
    def _multi_generator_fusion(
        self,
        prompt: str,
        strategy: Dict[str, Any]
    ) -> str:
        """多生成器融合"""
        
        generator_weights = strategy.get("generator_weights", {
            "main_generator": 0.7,
            "openai_generator": 0.3
        })
        
        # 收集所有生成结果
        generator_results = []
        
        for generator_name, weight in generator_weights.items():
            if weight > 0 and generator_name in self.generators:
                try:
                    answer = self._single_generator_process(
                        prompt, 
                        generator_name, 
                        strategy.get("generation_params", {})
                    )
                    generator_results.append({
                        "generator": generator_name,
                        "answer": answer,
                        "weight": weight
                    })
                    logger.debug(f"生成器 {generator_name} 完成，权重: {weight}")
                    
                except Exception as e:
                    logger.error(f"生成器 {generator_name} 失败: {e}")
        
        if not generator_results:
            return "抱歉，所有生成器都失败了。"
        
        # 简单融合策略：选择权重最高的结果
        best_result = max(generator_results, key=lambda x: x["weight"])
        
        # 可以在这里实现更复杂的融合策略
        return best_result["answer"]
    
    def get_generator_info(self) -> Dict[str, Any]:
        """获取生成器信息"""
        info = {
            "flexrag_available": FLEXRAG_AVAILABLE,
            "fallback_mode": self.fallback_mode,
            "loaded_generators": list(self.generators.keys()),
            "generator_types": {}
        }
        
        for name, generator in self.generators.items():
            if hasattr(generator, 'generator_type'):
                info["generator_types"][name] = generator.generator_type
            else:
                info["generator_types"][name] = "mock"
        
        return info


if __name__ == "__main__":
    # 测试集成生成器
    from ...config import FlexRAGIntegratedConfig
    
    config = FlexRAGIntegratedConfig()
    generator = FlexRAGIntegratedGenerator(config)
    
    # 创建测试上下文
    test_contexts = [
        RetrievedContext(
            content="人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。",
            score=0.9,
            metadata={"doc_id": "ai_def_1"}
        ),
        RetrievedContext(
            content="机器学习是人工智能的一个子集，它使计算机能够在没有明确编程的情况下学习和改进。",
            score=0.8,
            metadata={"doc_id": "ml_def_1"}
        )
    ]
    
    # 测试生成
    strategy = {
        "generator": "main_generator",
        "prompt_template": "step_by_step",
        "max_tokens": 200,
        "temperature": 0.7,
        "max_context_length": 1000
    }
    
    result = generator.adaptive_generate(
        query="What is artificial intelligence?",
        contexts=test_contexts,
        strategy=strategy
    )
    
    print(f"生成结果:")
    print(f"- 查询: {result.query}")
    print(f"- 回答: {result.answer}")
    print(f"- 生成时间: {result.generation_time:.3f}s")
    print(f"- 生成器信息: {generator.get_generator_info()}")
