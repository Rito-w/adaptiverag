#!/usr/bin/env python3
"""
=== AdaptiveRAG 论文实验脚本 ===

执行完整的论文实验，包括主要对比、消融研究和效率分析
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from adaptive_rag.evaluation.benchmark_runner import BenchmarkRunner, BenchmarkConfig
from adaptive_rag.evaluation.ablation_analyzer import AblationAnalyzer
from adaptive_rag.config import AdaptiveRAGConfig

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PaperExperimentRunner:
    """论文实验运行器"""

    def __init__(self, output_dir: str = "/root/autodl-tmp/adaptiverag_experiments",
                 data_dir: str = "/root/autodl-tmp/adaptiverag_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 实验配置
        self.datasets = {
            "single_hop": ["natural_questions", "trivia_qa", "ms_marco"],
            "multi_hop": ["hotpot_qa", "2wiki_multihop", "musique"],
            "conversational": ["quac", "coqa"]
        }
        
        self.baseline_methods = [
            "naive_rag",
            "self_rag", 
            "raptor",
            "rag_fusion",
            "hyde"
        ]
        
        self.ablation_methods = [
            "adaptive_rag",                    # 完整方法
            "adaptive_rag_no_decomposition",   # 无任务分解
            "adaptive_rag_no_planning",        # 无策略规划
            "adaptive_rag_single_retriever",   # 单一检索器
            "adaptive_rag_no_reranking",       # 无重排序
            "adaptive_rag_minimal"             # 最小配置
        ]
        
        self.metrics = ["exact_match", "f1_score", "rouge_l", "bert_score"]
        
    def run_main_comparison(self, sample_size: int = 1000):
        """运行主要对比实验"""
        logger.info("🚀 开始主要对比实验")
        
        results = {}
        
        for category, datasets in self.datasets.items():
            logger.info(f"📊 处理 {category} 数据集")
            
            for dataset in datasets:
                logger.info(f"  📚 数据集: {dataset}")
                
                # 配置实验
                config = BenchmarkConfig(
                    datasets=[dataset],
                    methods=["adaptive_rag"] + self.baseline_methods,
                    output_dir=str(self.output_dir / "main_comparison" / dataset),
                    max_samples=sample_size,
                    save_predictions=True,
                    compute_bert_score=True
                )
                
                # 运行实验
                runner = BenchmarkRunner(config)
                dataset_results = runner.run_benchmark()
                
                results[dataset] = dataset_results
                
                # 保存中间结果
                self._save_intermediate_results(
                    results, 
                    self.output_dir / "main_comparison" / "intermediate_results.json"
                )
        
        # 保存最终结果
        self._save_final_results(results, "main_comparison")
        logger.info("✅ 主要对比实验完成")
        
        return results
    
    def run_ablation_study(self, sample_size: int = 500):
        """运行消融研究"""
        logger.info("🔬 开始消融研究")
        
        # 选择代表性数据集
        test_datasets = ["natural_questions", "hotpot_qa"]
        results = {}
        
        for dataset in test_datasets:
            logger.info(f"📚 消融研究数据集: {dataset}")
            
            # 配置消融实验
            config = BenchmarkConfig(
                datasets=[dataset],
                methods=self.ablation_methods,
                output_dir=str(self.output_dir / "ablation_study" / dataset),
                max_samples=sample_size,
                save_predictions=True,
                compute_bert_score=True
            )
            
            # 运行实验
            runner = BenchmarkRunner(config)
            dataset_results = runner.run_benchmark()
            
            results[dataset] = dataset_results
        
        # 分析消融结果
        analyzer = AblationAnalyzer(str(self.output_dir / "ablation_study"))
        ablation_analysis = analyzer.analyze_component_contribution()
        
        # 生成可视化
        analyzer.generate_visualization(ablation_analysis)
        analyzer.generate_report(ablation_analysis)
        
        # 保存结果
        self._save_final_results(results, "ablation_study")
        logger.info("✅ 消融研究完成")
        
        return results, ablation_analysis
    
    def run_efficiency_analysis(self, sample_size: int = 200):
        """运行效率分析"""
        logger.info("⚡ 开始效率分析")
        
        # 效率测试配置
        efficiency_methods = ["adaptive_rag", "self_rag", "naive_rag"]
        test_dataset = "natural_questions"
        
        results = {}
        
        for method in efficiency_methods:
            logger.info(f"⏱️ 测试方法: {method}")
            
            config = BenchmarkConfig(
                datasets=[test_dataset],
                methods=[method],
                output_dir=str(self.output_dir / "efficiency_analysis" / method),
                max_samples=sample_size,
                save_predictions=False,  # 节省时间
                compute_bert_score=False  # 节省时间
            )
            
            runner = BenchmarkRunner(config)
            method_results = runner.run_benchmark()
            
            results[method] = method_results
        
        # 分析效率结果
        efficiency_report = self._analyze_efficiency(results)
        
        # 保存结果
        self._save_final_results(results, "efficiency_analysis")
        self._save_efficiency_report(efficiency_report)
        
        logger.info("✅ 效率分析完成")
        
        return results, efficiency_report
    
    def run_statistical_analysis(self, results: Dict[str, Any]):
        """运行统计显著性分析"""
        logger.info("📈 开始统计分析")
        
        from adaptive_rag.evaluation.statistical_analyzer import StatisticalAnalyzer
        
        analyzer = StatisticalAnalyzer()
        statistical_results = {}
        
        for dataset, dataset_results in results.items():
            logger.info(f"📊 分析数据集: {dataset}")
            
            # 提取AdaptiveRAG和基线方法的分数
            adaptive_scores = self._extract_scores(dataset_results, "adaptive_rag")
            
            dataset_stats = {}
            for baseline in self.baseline_methods:
                if baseline in dataset_results:
                    baseline_scores = self._extract_scores(dataset_results, baseline)
                    
                    # t检验
                    p_value = analyzer.paired_t_test(adaptive_scores, baseline_scores)
                    
                    # 效应量
                    effect_size = analyzer.cohens_d(adaptive_scores, baseline_scores)
                    
                    dataset_stats[baseline] = {
                        "p_value": p_value,
                        "effect_size": effect_size,
                        "significant": p_value < 0.05
                    }
            
            statistical_results[dataset] = dataset_stats
        
        # 保存统计结果
        self._save_statistical_results(statistical_results)
        
        logger.info("✅ 统计分析完成")
        return statistical_results
    
    def generate_paper_tables(self, results: Dict[str, Any]):
        """生成论文表格"""
        logger.info("📋 生成论文表格")
        
        # 主要结果表格
        main_table = self._create_main_results_table(results)
        
        # 消融研究表格
        ablation_table = self._create_ablation_table(results)
        
        # 效率对比表格
        efficiency_table = self._create_efficiency_table(results)
        
        # 保存表格
        tables = {
            "main_results": main_table,
            "ablation_study": ablation_table,
            "efficiency_analysis": efficiency_table
        }
        
        self._save_paper_tables(tables)
        
        logger.info("✅ 论文表格生成完成")
        return tables
    
    def _save_intermediate_results(self, results: Dict, filepath: Path):
        """保存中间结果"""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    def _save_final_results(self, results: Dict, experiment_type: str):
        """保存最终结果"""
        output_file = self.output_dir / f"{experiment_type}_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"💾 结果已保存: {output_file}")
    
    def _analyze_efficiency(self, results: Dict) -> Dict:
        """分析效率结果"""
        efficiency_report = {}
        
        for method, method_results in results.items():
            if method_results:
                result = method_results[0]  # 假设只有一个数据集
                
                efficiency_report[method] = {
                    "avg_retrieval_time": result.avg_retrieval_time,
                    "avg_generation_time": result.avg_generation_time,
                    "avg_total_time": result.avg_total_time,
                    "memory_usage_mb": result.memory_usage_mb,
                    "throughput": 60 / result.avg_total_time if result.avg_total_time > 0 else 0
                }
        
        return efficiency_report
    
    def _save_efficiency_report(self, report: Dict):
        """保存效率报告"""
        output_file = self.output_dir / "efficiency_report.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    
    def _extract_scores(self, results: List, method: str) -> List[float]:
        """提取指定方法的分数"""
        for result in results:
            if result.method_name == method:
                return [result.exact_match, result.f1_score, result.rouge_l]
        return []
    
    def _save_statistical_results(self, results: Dict):
        """保存统计结果"""
        output_file = self.output_dir / "statistical_analysis.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    
    def _create_main_results_table(self, results: Dict) -> str:
        """创建主要结果表格"""
        # 这里实现LaTeX表格生成逻辑
        return "LaTeX table for main results"
    
    def _create_ablation_table(self, results: Dict) -> str:
        """创建消融研究表格"""
        return "LaTeX table for ablation study"
    
    def _create_efficiency_table(self, results: Dict) -> str:
        """创建效率对比表格"""
        return "LaTeX table for efficiency analysis"
    
    def _save_paper_tables(self, tables: Dict):
        """保存论文表格"""
        output_file = self.output_dir / "paper_tables.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tables, f, indent=2, ensure_ascii=False)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="AdaptiveRAG 论文实验")
    parser.add_argument("--experiment", choices=["all", "main", "ablation", "efficiency"], 
                       default="all", help="实验类型")
    parser.add_argument("--sample_size", type=int, default=1000, help="样本大小")
    parser.add_argument("--output_dir", default="./experiments/paper_results", help="输出目录")
    
    args = parser.parse_args()
    
    # 创建实验运行器
    runner = PaperExperimentRunner(args.output_dir)
    
    logger.info("🚀 开始 AdaptiveRAG 论文实验")
    logger.info(f"📁 输出目录: {args.output_dir}")
    logger.info(f"📊 样本大小: {args.sample_size}")
    
    results = {}
    
    if args.experiment in ["all", "main"]:
        main_results = runner.run_main_comparison(args.sample_size)
        results["main_comparison"] = main_results
    
    if args.experiment in ["all", "ablation"]:
        ablation_results, ablation_analysis = runner.run_ablation_study(args.sample_size // 2)
        results["ablation_study"] = ablation_results
    
    if args.experiment in ["all", "efficiency"]:
        efficiency_results, efficiency_report = runner.run_efficiency_analysis(args.sample_size // 5)
        results["efficiency_analysis"] = efficiency_results
    
    # 统计分析
    if "main_comparison" in results:
        statistical_results = runner.run_statistical_analysis(results["main_comparison"])
        results["statistical_analysis"] = statistical_results
    
    # 生成论文表格
    paper_tables = runner.generate_paper_tables(results)
    
    logger.info("🎉 所有实验完成！")
    logger.info(f"📄 结果保存在: {args.output_dir}")
    
    # 生成实验总结
    summary = {
        "experiment_date": datetime.now().isoformat(),
        "sample_size": args.sample_size,
        "experiments_run": list(results.keys()),
        "output_directory": args.output_dir
    }
    
    summary_file = Path(args.output_dir) / "experiment_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎯 实验总结已保存: {summary_file}")


if __name__ == "__main__":
    main()
