#!/usr/bin/env python3
"""
=== AdaptiveRAG 基准测试运行器 ===

借鉴 FlashRAG 的评估框架，为 AdaptiveRAG 设计的综合评估系统
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

import pandas as pd
from tqdm import tqdm

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EvaluationResult:
    """评估结果数据结构"""
    method_name: str
    dataset_name: str
    exact_match: float
    f1_score: float
    rouge_l: float
    bert_score: float
    avg_retrieval_time: float
    avg_generation_time: float
    avg_total_time: float
    memory_usage_mb: float
    num_samples: int
    timestamp: str


@dataclass
class BenchmarkConfig:
    """基准测试配置"""
    datasets: List[str]
    methods: List[str]
    output_dir: str
    max_samples: Optional[int] = None
    save_predictions: bool = True
    compute_bert_score: bool = True

    def get(self, key: str, default=None):
        """字典式访问方法"""
        return getattr(self, key, default)


class DatasetLoader:
    """数据集加载器 - 借鉴 FlashRAG 的数据集接口"""
    
    SUPPORTED_DATASETS = {
        # 单跳问答
        "natural_questions": "nq",
        "trivia_qa": "trivia",
        "ms_marco": "msmarco",
        
        # 多跳推理
        "hotpot_qa": "hotpot",
        "2wiki_multihop": "2wiki",
        "musique": "musique",
        
        # 对话问答
        "quac": "quac",
        "coqa": "coqa",
        
        # 开放域问答
        "web_questions": "webq",
        "entity_questions": "entityq"
    }
    
    def __init__(self, data_dir: str = "./data/benchmarks"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def load_dataset(self, dataset_name: str, split: str = "test") -> List[Dict[str, Any]]:
        """加载指定数据集"""
        if dataset_name not in self.SUPPORTED_DATASETS:
            raise ValueError(f"不支持的数据集: {dataset_name}")
        
        dataset_file = self.data_dir / f"{dataset_name}_{split}.jsonl"
        
        if not dataset_file.exists():
            logger.warning(f"数据集文件不存在: {dataset_file}")
            return self._create_mock_dataset(dataset_name)
        
        data = []
        with open(dataset_file, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line.strip()))
        
        logger.info(f"加载数据集 {dataset_name}: {len(data)} 个样本")
        return data
    
    def _create_mock_dataset(self, dataset_name: str) -> List[Dict[str, Any]]:
        """创建模拟数据集用于测试"""
        logger.info(f"创建模拟数据集: {dataset_name}")
        
        if "hotpot" in dataset_name:
            # 多跳推理样本
            return [
                {
                    "id": f"mock_hotpot_{i}",
                    "question": f"What is the connection between entity A and entity B in context {i}?",
                    "answer": f"The connection is through intermediate entity C{i}.",
                    "supporting_facts": [f"fact_{i}_1", f"fact_{i}_2"],
                    "type": "multi_hop"
                }
                for i in range(50)
            ]
        elif "natural" in dataset_name:
            # 单跳问答样本
            return [
                {
                    "id": f"mock_nq_{i}",
                    "question": f"What is the capital of country {i}?",
                    "answer": f"Capital{i}",
                    "type": "single_hop"
                }
                for i in range(50)
            ]
        else:
            # 通用样本
            return [
                {
                    "id": f"mock_{dataset_name}_{i}",
                    "question": f"Sample question {i} for {dataset_name}",
                    "answer": f"Sample answer {i}",
                    "type": "general"
                }
                for i in range(50)
            ]


class MetricsCalculator:
    """评估指标计算器 - 集成 FlashRAG 的评估指标"""

    def __init__(self):
        """初始化评估指标计算器"""
        # 尝试导入 FlashRAG 评估指标
        self.flashrag_available = False
        try:
            from flashrag.evaluator.metrics import EM, F1_Score, Rouge_L
            self.flashrag_em = EM({})
            self.flashrag_f1 = F1_Score({})
            self.flashrag_rouge = Rouge_L({})
            self.flashrag_available = True
            logger.info("✅ FlashRAG 评估指标可用")
        except ImportError:
            logger.warning("⚠️ FlashRAG 评估指标不可用，使用内置实现")

        # 尝试导入 BERTScore
        self.bertscore_available = False
        try:
            from bert_score import score
            self.bertscore_available = True
            logger.info("✅ BERTScore 可用")
        except ImportError:
            logger.warning("⚠️ BERTScore 不可用，使用近似实现")
    
    def calculate_exact_match(self, predictions: List[str], references: List[str]) -> float:
        """计算精确匹配率"""
        if self.flashrag_available:
            try:
                # 使用 FlashRAG 的 EM 计算
                mock_data = self._create_mock_data(predictions, references)
                result, _ = self.flashrag_em.calculate_metric(mock_data)
                return result.get('exact_match', 0.0)
            except Exception as e:
                logger.warning(f"FlashRAG EM 计算失败，使用内置实现: {e}")

        # 内置实现
        if len(predictions) != len(references):
            raise ValueError("预测和参考答案数量不匹配")

        exact_matches = 0
        for pred, ref in zip(predictions, references):
            ref_list = [ref] if isinstance(ref, str) else ref
            if any(self._normalize_answer(pred) == self._normalize_answer(r) for r in ref_list):
                exact_matches += 1
        return exact_matches / len(predictions)

    def _create_mock_data(self, predictions: List[str], references: List[str]):
        """创建模拟数据结构用于 FlashRAG 评估"""
        mock_data = []
        for pred, ref in zip(predictions, references):
            mock_item = type('MockItem', (), {
                'pred': pred,
                'golden_answers': [ref] if isinstance(ref, str) else ref
            })()
            mock_data.append(mock_item)

        return type('MockDataset', (), {'data': mock_data})()

    def _normalize_answer(self, answer: str) -> str:
        """标准化答案文本 - 借鉴 FlashRAG 的标准化方法"""
        import re
        import string

        # 转小写
        answer = answer.lower()

        # 移除标点符号
        answer = answer.translate(str.maketrans('', '', string.punctuation))

        # 移除冠词
        answer = re.sub(r'\b(a|an|the)\b', ' ', answer)

        # 移除多余空格
        answer = re.sub(r'\s+', ' ', answer).strip()

        return answer

    def calculate_f1_score(self, predictions: List[str], references: List[str]) -> float:
        """计算 F1 分数"""
        if self.flashrag_available:
            try:
                # 使用 FlashRAG 的 F1 计算
                mock_data = self._create_mock_data(predictions, references)
                result, _ = self.flashrag_f1.calculate_metric(mock_data)
                return result.get('f1_score', 0.0)
            except Exception as e:
                logger.warning(f"FlashRAG F1 计算失败，使用内置实现: {e}")

        # 内置实现
        total_f1 = 0.0

        for pred, ref in zip(predictions, references):
            pred_tokens = set(pred.lower().split())
            ref_tokens = set(ref.lower().split())

            if len(pred_tokens) == 0 and len(ref_tokens) == 0:
                f1 = 1.0
            elif len(pred_tokens) == 0 or len(ref_tokens) == 0:
                f1 = 0.0
            else:
                common = len(pred_tokens & ref_tokens)
                precision = common / len(pred_tokens)
                recall = common / len(ref_tokens)
                f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

            total_f1 += f1

        return total_f1 / len(predictions)
    
    def calculate_rouge_l(self, predictions: List[str], references: List[str]) -> float:
        """计算 ROUGE-L 分数"""
        if self.flashrag_available:
            try:
                # 使用 FlashRAG 的 ROUGE-L 计算
                mock_data = self._create_mock_data(predictions, references)
                result, _ = self.flashrag_rouge.calculate_metric(mock_data)
                return result.get('rouge-l', 0.0)
            except Exception as e:
                logger.warning(f"FlashRAG ROUGE-L 计算失败，使用内置实现: {e}")

        # 内置实现 - 简化的 ROUGE-L 计算
        total_rouge = 0.0

        for pred, ref in zip(predictions, references):
            pred_words = pred.lower().split()
            ref_words = ref.lower().split()

            # 简化的最长公共子序列
            lcs_length = self._lcs_length(pred_words, ref_words)

            if len(ref_words) == 0:
                rouge_l = 0.0
            else:
                recall = lcs_length / len(ref_words)
                precision = lcs_length / len(pred_words) if len(pred_words) > 0 else 0.0
                rouge_l = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

            total_rouge += rouge_l

        return total_rouge / len(predictions)
    
    def _lcs_length(self, seq1: List[str], seq2: List[str]) -> int:
        """计算最长公共子序列长度"""
        m, n = len(seq1), len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]
    
    def calculate_bert_score(self, predictions: List[str], references: List[str]) -> float:
        """计算 BERTScore"""
        if self.bertscore_available:
            try:
                from bert_score import score
                # 使用真实的 BERTScore
                P, R, F1 = score(predictions, references, lang="en", verbose=False)
                return F1.mean().item()
            except Exception as e:
                logger.warning(f"BERTScore 计算失败，使用近似实现: {e}")

        # 近似实现 - 基于词汇重叠
        total_score = 0.0

        for pred, ref in zip(predictions, references):
            pred_tokens = set(pred.lower().split())
            ref_tokens = set(ref.lower().split())

            if len(ref_tokens) == 0:
                score = 0.0
            else:
                overlap = len(pred_tokens & ref_tokens)
                score = overlap / max(len(pred_tokens), len(ref_tokens))

            total_score += score

        return total_score / len(predictions)


class BenchmarkRunner:
    """基准测试运行器 - 集成 FlashRAG 数据集和评估"""

    def __init__(self, config: BenchmarkConfig):
        self.config = config
        self.dataset_loader = DatasetLoader()
        self.metrics_calculator = MetricsCalculator()
        self.results = []

        # 创建输出目录
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 初始化数据集下载器
        from .dataset_downloader import DatasetDownloader
        self.dataset_downloader = DatasetDownloader(str(self.dataset_loader.data_dir))
    
    def run_benchmark(self):
        """运行完整的基准测试"""
        logger.info("🚀 开始运行 AdaptiveRAG 基准测试")
        logger.info(f"数据集: {self.config.datasets}")
        logger.info(f"方法: {self.config.methods}")
        
        for dataset_name in self.config.datasets:
            for method_name in self.config.methods:
                logger.info(f"\n📊 评估 {method_name} 在 {dataset_name} 上的性能")
                
                try:
                    result = self._evaluate_method_on_dataset(method_name, dataset_name)
                    self.results.append(result)
                    logger.info(f"✅ 完成评估: EM={result.exact_match:.3f}, F1={result.f1_score:.3f}")
                    
                except Exception as e:
                    logger.error(f"❌ 评估失败: {e}")
                    continue
        
        # 保存结果
        self._save_results()
        logger.info(f"🎉 基准测试完成！结果保存在: {self.output_dir}")
    
    def _evaluate_method_on_dataset(self, method_name: str, dataset_name: str) -> EvaluationResult:
        """在指定数据集上评估指定方法"""
        # 尝试从 FlashRAG 加载数据集
        dataset = self._load_dataset_with_fallback(dataset_name)

        if self.config.max_samples:
            dataset = dataset[:self.config.max_samples]

        # 初始化方法
        method = self._load_method(method_name)

        # 运行评估
        predictions = []
        retrieval_times = []
        generation_times = []
        total_times = []

        for sample in tqdm(dataset, desc=f"评估 {method_name}"):
            start_time = time.time()

            # 运行方法
            if hasattr(method, 'answer'):
                # FlexRAG 集成助手使用 answer 方法
                assistant_result = method.answer(sample["question"])
                result = {
                    "answer": assistant_result.answer,
                    "retrieval_time": sum(r.retrieval_time for r in assistant_result.retrieval_results),
                    "generation_time": assistant_result.generation_result.generation_time if assistant_result.generation_result else 0.0
                }
            else:
                # 其他方法使用 process_query
                result = method.process_query(sample["question"])

            end_time = time.time()

            predictions.append(result["answer"])
            retrieval_times.append(result.get("retrieval_time", 0.0))
            generation_times.append(result.get("generation_time", 0.0))
            total_times.append(end_time - start_time)

        # 计算指标
        references = [sample["answer"] for sample in dataset]

        exact_match = self.metrics_calculator.calculate_exact_match(predictions, references)
        f1_score = self.metrics_calculator.calculate_f1_score(predictions, references)
        rouge_l = self.metrics_calculator.calculate_rouge_l(predictions, references)

        bert_score = 0.0
        if self.config.compute_bert_score:
            bert_score = self.metrics_calculator.calculate_bert_score(predictions, references)

        # 创建结果
        result = EvaluationResult(
            method_name=method_name,
            dataset_name=dataset_name,
            exact_match=exact_match,
            f1_score=f1_score,
            rouge_l=rouge_l,
            bert_score=bert_score,
            avg_retrieval_time=sum(retrieval_times) / len(retrieval_times),
            avg_generation_time=sum(generation_times) / len(generation_times),
            avg_total_time=sum(total_times) / len(total_times),
            memory_usage_mb=0.0,  # TODO: 实现内存监控
            num_samples=len(dataset),
            timestamp=datetime.now().isoformat()
        )

        # 保存预测结果
        if self.config.save_predictions:
            self._save_predictions(method_name, dataset_name, predictions, references)

        return result

    def _load_dataset_with_fallback(self, dataset_name: str) -> List[Dict[str, Any]]:
        """加载数据集，优先使用 FlashRAG，失败时使用本地数据"""
        # 首先尝试加载本地数据集
        try:
            dataset = self.dataset_loader.load_dataset(dataset_name)
            if dataset:
                logger.info(f"✅ 从本地加载数据集: {dataset_name}")
                return dataset
        except Exception as e:
            logger.warning(f"本地数据集加载失败: {e}")

        # 尝试从 FlashRAG 下载数据集
        logger.info(f"📥 尝试从 FlashRAG 下载数据集: {dataset_name}")
        if self.dataset_downloader.download_flashrag_dataset(dataset_name, "test"):
            try:
                dataset = self.dataset_loader.load_dataset(dataset_name)
                if dataset:
                    logger.info(f"✅ 从 FlashRAG 加载数据集: {dataset_name}")
                    return dataset
            except Exception as e:
                logger.error(f"FlashRAG 数据集加载失败: {e}")

        # 最后使用模拟数据集
        logger.warning(f"⚠️ 使用模拟数据集: {dataset_name}")
        return self.dataset_loader._create_mock_dataset(dataset_name)
        
        # 初始化方法
        method = self._load_method(method_name)
        
        # 运行评估
        predictions = []
        retrieval_times = []
        generation_times = []
        total_times = []
        
        for sample in tqdm(dataset, desc=f"评估 {method_name}"):
            start_time = time.time()
            
            # 运行方法
            if hasattr(method, 'answer'):
                # FlexRAG 集成助手使用 answer 方法
                assistant_result = method.answer(sample["question"])
                result = {
                    "answer": assistant_result.answer,
                    "retrieval_time": sum(r.retrieval_time for r in assistant_result.retrieval_results),
                    "generation_time": assistant_result.generation_result.generation_time if assistant_result.generation_result else 0.0
                }
            else:
                # 其他方法使用 process_query
                result = method.process_query(sample["question"])
            
            end_time = time.time()
            
            predictions.append(result["answer"])
            retrieval_times.append(result.get("retrieval_time", 0.0))
            generation_times.append(result.get("generation_time", 0.0))
            total_times.append(end_time - start_time)
        
        # 计算指标
        references = [sample["answer"] for sample in dataset]
        
        exact_match = self.metrics_calculator.calculate_exact_match(predictions, references)
        f1_score = self.metrics_calculator.calculate_f1_score(predictions, references)
        rouge_l = self.metrics_calculator.calculate_rouge_l(predictions, references)
        
        bert_score = 0.0
        if self.config.compute_bert_score:
            bert_score = self.metrics_calculator.calculate_bert_score(predictions, references)
        
        # 创建结果
        result = EvaluationResult(
            method_name=method_name,
            dataset_name=dataset_name,
            exact_match=exact_match,
            f1_score=f1_score,
            rouge_l=rouge_l,
            bert_score=bert_score,
            avg_retrieval_time=sum(retrieval_times) / len(retrieval_times),
            avg_generation_time=sum(generation_times) / len(generation_times),
            avg_total_time=sum(total_times) / len(total_times),
            memory_usage_mb=0.0,  # TODO: 实现内存监控
            num_samples=len(dataset),
            timestamp=datetime.now().isoformat()
        )
        
        # 保存预测结果
        if self.config.save_predictions:
            self._save_predictions(method_name, dataset_name, predictions, references)
        
        return result
    
    def _load_method(self, method_name: str):
        """加载指定的方法"""
        if method_name == "adaptive_rag":
            # 加载 AdaptiveRAG 方法
            try:
                from ..core.flexrag_integrated_assistant import FlexRAGIntegratedAssistant
                from ..config import create_flexrag_integrated_config

                config = create_flexrag_integrated_config()
                return FlexRAGIntegratedAssistant(config)
            except ImportError as e:
                logger.error(f"❌ 无法加载 AdaptiveRAG: {e}")
                raise

        elif method_name in ["naive_rag", "self_rag", "raptor"]:
            # 加载基线方法
            from .baseline_methods import create_baseline_method

            # 创建基线方法配置
            baseline_config = {
                "retrieval_topk": self.config.get("retrieval_topk", 5),
                "max_tokens": self.config.get("max_tokens", 256),
                "max_iterations": 3,
                "tree_depth": 3,
                "reflection_threshold": 0.7,
                "cluster_size": 5
            }

            return create_baseline_method(method_name, baseline_config)

        elif method_name.startswith("adaptive_rag_"):
            # 消融研究方法
            return self._load_ablation_method(method_name)

        else:
            raise ValueError(f"不支持的方法: {method_name}")

    def _load_ablation_method(self, method_name: str):
        """加载消融研究方法"""
        # 解析消融方法名称
        ablation_type = method_name.replace("adaptive_rag_", "")

        try:
            from ..core.flexrag_integrated_assistant import FlexRAGIntegratedAssistant
            from ..config import create_flexrag_integrated_config

            # 创建带有消融设置的配置
            config = create_flexrag_integrated_config()

            # 根据消融类型修改配置
            if ablation_type == "no_decomposition":
                config.adaptive_retrieval["enable_task_decomposition"] = False
            elif ablation_type == "no_planning":
                config.adaptive_retrieval["enable_strategy_planning"] = False
            elif ablation_type == "single_retriever":
                config.adaptive_retrieval["enable_multi_retriever"] = False
            elif ablation_type == "no_reranking":
                config.adaptive_retrieval["enable_reranking"] = False

            return FlexRAGIntegratedAssistant(config)

        except ImportError as e:
            logger.error(f"❌ 无法加载消融方法 {method_name}: {e}")
            raise

        else:
            raise ValueError(f"不支持的方法: {method_name}")
    
    def _create_mock_method(self, method_name: str):
        """创建模拟方法用于测试"""
        class MockMethod:
            def __init__(self, name):
                self.name = name

            def process_query(self, query: str) -> Dict[str, Any]:
                # 模拟处理延迟
                time.sleep(0.1)

                return {
                    "answer": f"Mock answer from {self.name} for: {query[:50]}...",
                    "retrieval_time": 0.05,
                    "generation_time": 0.05
                }

        return MockMethod(method_name)
    
    def _save_predictions(self, method_name: str, dataset_name: str, 
                         predictions: List[str], references: List[str]):
        """保存预测结果"""
        predictions_file = self.output_dir / f"{method_name}_{dataset_name}_predictions.jsonl"
        
        with open(predictions_file, 'w', encoding='utf-8') as f:
            for i, (pred, ref) in enumerate(zip(predictions, references)):
                json.dump({
                    "id": i,
                    "prediction": pred,
                    "reference": ref
                }, f, ensure_ascii=False)
                f.write('\n')
    
    def _save_results(self):
        """保存评估结果"""
        logger.info("💾 保存实验结果")

        # 过滤有效结果
        valid_results = [result for result in self.results if result is not None]

        if not valid_results:
            logger.warning("⚠️ 没有有效结果可保存")
            return

        # 保存详细结果
        results_file = self.output_dir / "evaluation_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(result) for result in valid_results], f,
                     ensure_ascii=False, indent=2)

        # 保存汇总表格
        df = pd.DataFrame([asdict(result) for result in valid_results])
        summary_file = self.output_dir / "evaluation_summary.csv"
        df.to_csv(summary_file, index=False)
        
        # 创建性能对比表
        self._create_performance_table()
    
    def _create_performance_table(self):
        """创建性能对比表"""
        df = pd.DataFrame([asdict(result) for result in self.results])
        
        # 按方法和数据集分组
        pivot_table = df.pivot_table(
            index='method_name',
            columns='dataset_name',
            values=['exact_match', 'f1_score', 'avg_total_time'],
            aggfunc='mean'
        )
        
        # 保存对比表
        comparison_file = self.output_dir / "method_comparison.csv"
        pivot_table.to_csv(comparison_file)
        
        logger.info(f"性能对比表保存在: {comparison_file}")


def main():
    """主函数 - 运行基准测试"""
    config = BenchmarkConfig(
        datasets=["natural_questions", "hotpot_qa", "trivia_qa"],
        methods=["adaptive_rag", "naive_rag", "self_rag"],
        output_dir="./evaluation_results",
        max_samples=100,  # 测试时使用小样本
        save_predictions=True,
        compute_bert_score=True
    )
    
    runner = BenchmarkRunner(config)
    runner.run_benchmark()


if __name__ == "__main__":
    main()
