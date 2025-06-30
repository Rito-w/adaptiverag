#!/usr/bin/env python3
"""
=== AdaptiveRAG 论文实验运行脚本 ===

在当前环境下运行完整的论文实验
"""

import os
import sys
import logging
from pathlib import Path

# 设置数据目录
DATA_DIR = "/root/autodl-tmp/adaptiverag_data"
EXPERIMENTS_DIR = "/root/autodl-tmp/adaptiverag_experiments"

# 确保目录存在
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(EXPERIMENTS_DIR, exist_ok=True)

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """设置实验环境"""
    logger.info("🔧 设置实验环境")
    
    # 添加项目路径
    sys.path.insert(0, str(Path(__file__).parent))
    
    # 设置环境变量
    os.environ['ADAPTIVERAG_DATA_DIR'] = DATA_DIR
    os.environ['ADAPTIVERAG_EXPERIMENTS_DIR'] = EXPERIMENTS_DIR
    
    logger.info(f"📁 数据目录: {DATA_DIR}")
    logger.info(f"📁 实验目录: {EXPERIMENTS_DIR}")

def run_quick_validation():
    """运行快速验证实验"""
    logger.info("🧪 运行快速验证实验")
    
    try:
        from adaptive_rag.evaluation.benchmark_runner import BenchmarkRunner, BenchmarkConfig
        
        # 创建小规模验证实验
        config = BenchmarkConfig(
            datasets=["natural_questions"],
            methods=["naive_rag", "self_rag"],
            output_dir=f"{EXPERIMENTS_DIR}/validation",
            max_samples=5,  # 只用5个样本快速验证
            save_predictions=True,
            compute_bert_score=False  # 跳过BERTScore节省时间
        )
        
        runner = BenchmarkRunner(config)
        results = runner.run_benchmark()
        
        logger.info("✅ 快速验证完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ 快速验证失败: {e}")
        return False

def run_main_experiments():
    """运行主要实验"""
    logger.info("🚀 开始主要实验")
    
    try:
        from adaptive_rag.evaluation.benchmark_runner import BenchmarkRunner, BenchmarkConfig
        
        # 1. 主要对比实验（小规模）
        logger.info("📊 运行主要对比实验")
        main_config = BenchmarkConfig(
            datasets=["natural_questions", "hotpot_qa"],
            methods=["adaptive_rag", "naive_rag", "self_rag"],
            output_dir=f"{EXPERIMENTS_DIR}/main_comparison",
            max_samples=50,  # 适中的样本数量
            save_predictions=True,
            compute_bert_score=True
        )
        
        main_runner = BenchmarkRunner(main_config)
        main_results = main_runner.run_benchmark()
        
        # 2. 消融研究
        logger.info("🔬 运行消融研究")
        ablation_config = BenchmarkConfig(
            datasets=["natural_questions"],
            methods=[
                "adaptive_rag",
                "adaptive_rag_no_decomposition", 
                "adaptive_rag_no_planning",
                "adaptive_rag_single_retriever",
                "adaptive_rag_no_reranking"
            ],
            output_dir=f"{EXPERIMENTS_DIR}/ablation_study",
            max_samples=30,  # 消融研究用较少样本
            save_predictions=True,
            compute_bert_score=False
        )
        
        ablation_runner = BenchmarkRunner(ablation_config)
        ablation_results = ablation_runner.run_benchmark()
        
        # 3. 效率分析
        logger.info("⚡ 运行效率分析")
        efficiency_config = BenchmarkConfig(
            datasets=["natural_questions"],
            methods=["adaptive_rag", "naive_rag"],
            output_dir=f"{EXPERIMENTS_DIR}/efficiency_analysis",
            max_samples=20,  # 效率测试用少量样本
            save_predictions=False,
            compute_bert_score=False
        )
        
        efficiency_runner = BenchmarkRunner(efficiency_config)
        efficiency_results = efficiency_runner.run_benchmark()
        
        logger.info("✅ 所有实验完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ 主要实验失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def analyze_results():
    """分析实验结果"""
    logger.info("📈 分析实验结果")
    
    try:
        # 查找结果文件
        result_files = list(Path(EXPERIMENTS_DIR).rglob("*.json"))
        logger.info(f"📄 找到 {len(result_files)} 个结果文件")
        
        for result_file in result_files:
            logger.info(f"  📋 {result_file.relative_to(Path(EXPERIMENTS_DIR))}")
        
        # 生成简单的结果总结
        summary_file = Path(EXPERIMENTS_DIR) / "experiment_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("AdaptiveRAG 实验结果总结\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"实验时间: {os.popen('date').read().strip()}\n")
            f.write(f"数据目录: {DATA_DIR}\n")
            f.write(f"实验目录: {EXPERIMENTS_DIR}\n\n")
            f.write("实验文件:\n")
            for result_file in result_files:
                f.write(f"  - {result_file.name}\n")
        
        logger.info(f"📄 实验总结已保存: {summary_file}")
        return True
        
    except Exception as e:
        logger.error(f"❌ 结果分析失败: {e}")
        return False

def main():
    """主函数"""
    logger.info("🎯 开始 AdaptiveRAG 论文实验")
    
    # 1. 设置环境
    setup_environment()
    
    # 2. 快速验证
    logger.info("\n" + "="*60)
    logger.info("第一步: 快速验证")
    logger.info("="*60)
    
    if not run_quick_validation():
        logger.error("❌ 快速验证失败，停止实验")
        return False
    
    # 3. 主要实验
    logger.info("\n" + "="*60)
    logger.info("第二步: 主要实验")
    logger.info("="*60)
    
    if not run_main_experiments():
        logger.error("❌ 主要实验失败")
        return False
    
    # 4. 结果分析
    logger.info("\n" + "="*60)
    logger.info("第三步: 结果分析")
    logger.info("="*60)
    
    if not analyze_results():
        logger.error("❌ 结果分析失败")
        return False
    
    # 5. 完成
    logger.info("\n" + "="*60)
    logger.info("🎉 所有实验完成！")
    logger.info("="*60)
    logger.info(f"📁 结果保存在: {EXPERIMENTS_DIR}")
    logger.info("📊 可以查看以下文件:")
    logger.info(f"  - {EXPERIMENTS_DIR}/experiment_summary.txt")
    logger.info(f"  - {EXPERIMENTS_DIR}/main_comparison/")
    logger.info(f"  - {EXPERIMENTS_DIR}/ablation_study/")
    logger.info(f"  - {EXPERIMENTS_DIR}/efficiency_analysis/")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
