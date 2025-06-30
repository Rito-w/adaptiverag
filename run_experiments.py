#!/usr/bin/env python3
"""
=== AdaptiveRAG 实验运行脚本 ===

一键运行完整的基准测试实验，生成论文所需的实验结果
"""

import argparse
import logging
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from adaptive_rag.evaluation.dataset_downloader import DatasetDownloader
from adaptive_rag.evaluation.benchmark_runner import BenchmarkRunner, BenchmarkConfig

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_datasets(use_sample_data: bool = True):
    """设置数据集"""
    logger.info("📊 设置评估数据集")
    
    downloader = DatasetDownloader()
    
    if use_sample_data:
        # 使用样本数据进行快速测试
        logger.info("使用样本数据集进行测试")
        downloader.create_sample_datasets()
    else:
        # 下载真实数据集
        logger.info("下载真实数据集 (需要网络连接)")
        downloader.download_all_datasets()
    
    logger.info("✅ 数据集设置完成")


def run_quick_experiment():
    """运行快速实验 (用于开发和调试)"""
    logger.info("🚀 运行快速实验")
    
    config = BenchmarkConfig(
        datasets=["natural_questions", "hotpot_qa"],
        methods=["adaptive_rag", "naive_rag"],
        output_dir="./experiments/quick_test",
        max_samples=20,  # 只使用20个样本
        save_predictions=True,
        compute_bert_score=False  # 跳过 BERTScore 以节省时间
    )
    
    runner = BenchmarkRunner(config)
    runner.run_benchmark()
    
    logger.info("✅ 快速实验完成")


def run_full_experiment():
    """运行完整实验 (用于论文结果)"""
    logger.info("🚀 运行完整实验")
    
    config = BenchmarkConfig(
        datasets=[
            # 单跳问答
            "natural_questions",
            "trivia_qa", 
            "ms_marco",
            
            # 多跳推理
            "hotpot_qa",
            # "2wiki_multihop",  # 如果有的话
            # "musique",         # 如果有的话
        ],
        methods=[
            "adaptive_rag",      # 我们的方法
            "naive_rag",         # 朴素基线
            "self_rag",          # 高级基线
            # "raptor",          # 如果实现的话
            # "hyde",            # 如果实现的话
        ],
        output_dir="./experiments/full_evaluation",
        max_samples=None,  # 使用全部数据
        save_predictions=True,
        compute_bert_score=True
    )
    
    runner = BenchmarkRunner(config)
    runner.run_benchmark()
    
    logger.info("✅ 完整实验完成")


def run_ablation_study():
    """运行消融研究 - 详细分析各组件贡献"""
    logger.info("🔬 运行详细消融研究")

    # 完整的消融研究设计
    ablation_experiments = {
        # 1. 完整方法作为基准
        "full_method": {
            "methods": ["adaptive_rag"],
            "description": "完整的 AdaptiveRAG 方法"
        },

        # 2. 任务分解消融
        "task_decomposition": {
            "methods": [
                "adaptive_rag",
                "adaptive_rag_no_decomposition"
            ],
            "description": "任务分解组件的影响"
        },

        # 3. 策略规划消融
        "strategy_planning": {
            "methods": [
                "adaptive_rag",
                "adaptive_rag_no_planning"
            ],
            "description": "策略规划组件的影响"
        },

        # 4. 多检索器消融
        "multi_retriever": {
            "methods": [
                "adaptive_rag",
                "adaptive_rag_single_retriever"
            ],
            "description": "多检索器融合的影响"
        },

        # 5. 重排序消融
        "reranking": {
            "methods": [
                "adaptive_rag",
                "adaptive_rag_no_reranking"
            ],
            "description": "重排序组件的影响"
        },

        # 6. 完整消融对比
        "complete_ablation": {
            "methods": [
                "adaptive_rag",                    # 完整方法
                "adaptive_rag_no_decomposition",   # 无任务分解
                "adaptive_rag_no_planning",        # 无策略规划
                "adaptive_rag_single_retriever",   # 单一检索器
                "adaptive_rag_no_reranking",       # 无重排序
                "naive_rag",                       # 朴素基线
            ],
            "description": "完整的消融对比研究"
        }
    }

    # 运行各个消融实验
    for exp_name, exp_config in ablation_experiments.items():
        logger.info(f"\n🧪 运行消融实验: {exp_name}")
        logger.info(f"📝 描述: {exp_config['description']}")

        config = BenchmarkConfig(
            datasets=["natural_questions", "hotpot_qa"],
            methods=exp_config["methods"],
            output_dir=f"./experiments/ablation_study/{exp_name}",
            max_samples=100,  # 适中的样本数量
            save_predictions=True,
            compute_bert_score=True
        )

        runner = BenchmarkRunner(config)
        runner.run_benchmark()

        logger.info(f"✅ 消融实验 {exp_name} 完成")

    # 生成消融分析报告
    _generate_ablation_report()

    logger.info("✅ 详细消融研究完成")


def _generate_ablation_report():
    """生成消融分析报告"""
    logger.info("📊 生成消融分析报告")

    # 这里可以添加结果分析和可视化代码
    # 例如：对比不同组件的性能贡献

    report_content = """
# AdaptiveRAG 消融研究报告

## 实验设计

本消融研究旨在分析 AdaptiveRAG 各组件的贡献度：

1. **任务分解 (Task Decomposition)**: LLM 驱动的查询分析和子任务分解
2. **策略规划 (Strategy Planning)**: 自适应检索策略选择
3. **多检索器融合 (Multi-Retriever)**: 关键词、密集、Web 检索的智能融合
4. **重排序 (Reranking)**: 检索结果的重新排序和筛选

## 实验结果

详细结果请查看各个实验目录下的结果文件。

## 分析结论

[待补充：基于实验结果的分析]

"""

    report_path = "./experiments/ablation_study/ablation_report.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    logger.info(f"📄 消融报告已保存: {report_path}")


def run_efficiency_analysis():
    """运行效率分析"""
    logger.info("⚡ 运行效率分析")
    
    config = BenchmarkConfig(
        datasets=["natural_questions"],  # 使用单一数据集
        methods=["adaptive_rag", "naive_rag", "self_rag"],
        output_dir="./experiments/efficiency_analysis",
        max_samples=100,
        save_predictions=False,  # 不保存预测以节省空间
        compute_bert_score=False  # 专注于时间分析
    )
    
    runner = BenchmarkRunner(config)
    runner.run_benchmark()
    
    logger.info("✅ 效率分析完成")


def generate_paper_results():
    """生成论文所需的所有结果"""
    logger.info("📝 生成论文结果")
    
    # 1. 设置数据集
    setup_datasets(use_sample_data=False)  # 使用真实数据
    
    # 2. 运行主要实验
    run_full_experiment()
    
    # 3. 运行消融研究
    run_ablation_study()
    
    # 4. 运行效率分析
    run_efficiency_analysis()
    
    logger.info("🎉 论文结果生成完成！")
    logger.info("📁 结果保存在 ./experiments/ 目录下")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="AdaptiveRAG 实验运行器")
    parser.add_argument(
        "experiment_type",
        choices=["quick", "full", "ablation", "efficiency", "paper"],
        help="实验类型"
    )
    parser.add_argument(
        "--sample-data",
        action="store_true",
        help="使用样本数据而不是真实数据集"
    )
    
    args = parser.parse_args()
    
    logger.info(f"🧪 开始运行 {args.experiment_type} 实验")
    
    try:
        if args.experiment_type == "quick":
            setup_datasets(use_sample_data=True)
            run_quick_experiment()
            
        elif args.experiment_type == "full":
            setup_datasets(use_sample_data=args.sample_data)
            run_full_experiment()
            
        elif args.experiment_type == "ablation":
            setup_datasets(use_sample_data=args.sample_data)
            run_ablation_study()
            
        elif args.experiment_type == "efficiency":
            setup_datasets(use_sample_data=args.sample_data)
            run_efficiency_analysis()
            
        elif args.experiment_type == "paper":
            generate_paper_results()
        
        logger.info("🎉 实验运行成功完成！")
        
        # 显示结果位置
        experiments_dir = Path("./experiments")
        if experiments_dir.exists():
            logger.info(f"📁 实验结果保存在: {experiments_dir.absolute()}")
            
            # 列出生成的文件
            for result_dir in experiments_dir.iterdir():
                if result_dir.is_dir():
                    logger.info(f"   📂 {result_dir.name}/")
                    for file in result_dir.iterdir():
                        if file.is_file():
                            logger.info(f"      📄 {file.name}")
        
    except Exception as e:
        logger.error(f"❌ 实验运行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
