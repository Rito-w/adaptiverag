#!/usr/bin/env python3
"""
=== 消融实验分析器 ===

分析 AdaptiveRAG 各组件的贡献度和性能影响
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AblationAnalyzer:
    """消融实验分析器"""
    
    def __init__(self, results_dir: str = "./experiments/ablation_study"):
        self.results_dir = Path(results_dir)
        self.results_data = {}
        self.component_mapping = {
            "adaptive_rag": "完整方法",
            "adaptive_rag_no_decomposition": "无任务分解",
            "adaptive_rag_no_planning": "无策略规划", 
            "adaptive_rag_single_retriever": "单一检索器",
            "adaptive_rag_no_reranking": "无重排序",
            "naive_rag": "朴素基线",
            "self_rag": "Self-RAG基线"
        }
    
    def load_results(self):
        """加载所有实验结果"""
        logger.info("📊 加载消融实验结果")
        
        # 查找所有结果文件
        result_files = list(self.results_dir.rglob("*.json"))
        
        for result_file in result_files:
            try:
                with open(result_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 解析文件路径获取实验信息
                relative_path = result_file.relative_to(self.results_dir)
                experiment_name = relative_path.parts[0] if len(relative_path.parts) > 1 else "unknown"
                
                if experiment_name not in self.results_data:
                    self.results_data[experiment_name] = []
                
                self.results_data[experiment_name].append({
                    "file": str(result_file),
                    "data": data
                })
                
            except Exception as e:
                logger.warning(f"⚠️ 无法加载结果文件 {result_file}: {e}")
        
        logger.info(f"✅ 加载了 {len(self.results_data)} 个实验的结果")
    
    def analyze_component_contribution(self) -> Dict[str, Any]:
        """分析各组件的贡献度"""
        logger.info("🔍 分析组件贡献度")
        
        if not self.results_data:
            self.load_results()
        
        analysis_results = {}
        
        # 分析每个实验
        for exp_name, exp_results in self.results_data.items():
            logger.info(f"📈 分析实验: {exp_name}")
            
            exp_analysis = self._analyze_single_experiment(exp_results)
            analysis_results[exp_name] = exp_analysis
        
        return analysis_results
    
    def _analyze_single_experiment(self, exp_results: List[Dict]) -> Dict[str, Any]:
        """分析单个实验的结果"""
        
        # 提取性能指标
        performance_data = []
        
        for result in exp_results:
            data = result["data"]
            
            if isinstance(data, list):
                # 处理结果列表
                for item in data:
                    performance_data.append(self._extract_metrics(item))
            else:
                # 处理单个结果
                performance_data.append(self._extract_metrics(data))
        
        if not performance_data:
            return {"error": "无有效数据"}
        
        # 创建 DataFrame 进行分析
        df = pd.DataFrame(performance_data)
        
        # 按方法分组计算平均性能
        if "method_name" in df.columns:
            method_performance = df.groupby("method_name").agg({
                "exact_match": "mean",
                "f1_score": "mean", 
                "rouge_l": "mean",
                "avg_total_time": "mean"
            }).round(4)
            
            # 计算相对于完整方法的性能变化
            baseline_performance = self._get_baseline_performance(method_performance)
            relative_performance = self._calculate_relative_performance(
                method_performance, baseline_performance
            )
            
            return {
                "method_performance": method_performance.to_dict(),
                "relative_performance": relative_performance,
                "baseline_method": baseline_performance["method"] if baseline_performance else None
            }
        
        return {"error": "缺少方法名称信息"}
    
    def _extract_metrics(self, result_item: Dict) -> Dict[str, Any]:
        """提取性能指标"""
        return {
            "method_name": result_item.get("method_name", "unknown"),
            "dataset_name": result_item.get("dataset_name", "unknown"),
            "exact_match": result_item.get("exact_match", 0.0),
            "f1_score": result_item.get("f1_score", 0.0),
            "rouge_l": result_item.get("rouge_l", 0.0),
            "bert_score": result_item.get("bert_score", 0.0),
            "avg_retrieval_time": result_item.get("avg_retrieval_time", 0.0),
            "avg_generation_time": result_item.get("avg_generation_time", 0.0),
            "avg_total_time": result_item.get("avg_total_time", 0.0),
            "num_samples": result_item.get("num_samples", 0)
        }
    
    def _get_baseline_performance(self, method_performance: pd.DataFrame) -> Optional[Dict]:
        """获取基线性能（完整方法）"""
        if "adaptive_rag" in method_performance.index:
            baseline = method_performance.loc["adaptive_rag"]
            return {
                "method": "adaptive_rag",
                "performance": baseline.to_dict()
            }
        return None
    
    def _calculate_relative_performance(self, method_performance: pd.DataFrame, 
                                      baseline: Optional[Dict]) -> Dict[str, Any]:
        """计算相对性能变化"""
        if not baseline:
            return {}
        
        baseline_perf = baseline["performance"]
        relative_changes = {}
        
        for method in method_performance.index:
            if method == baseline["method"]:
                continue
            
            method_perf = method_performance.loc[method]
            changes = {}
            
            for metric in ["exact_match", "f1_score", "rouge_l"]:
                if metric in baseline_perf and baseline_perf[metric] > 0:
                    change = (method_perf[metric] - baseline_perf[metric]) / baseline_perf[metric]
                    changes[metric] = round(change * 100, 2)  # 转换为百分比
                else:
                    changes[metric] = 0.0
            
            # 时间变化（越小越好）
            if "avg_total_time" in baseline_perf and baseline_perf["avg_total_time"] > 0:
                time_change = (method_perf["avg_total_time"] - baseline_perf["avg_total_time"]) / baseline_perf["avg_total_time"]
                changes["time_change"] = round(time_change * 100, 2)
            
            relative_changes[method] = changes
        
        return relative_changes
    
    def generate_visualization(self, analysis_results: Dict[str, Any], 
                             output_dir: str = "./experiments/ablation_study/plots"):
        """生成可视化图表"""
        logger.info("📊 生成可视化图表")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 1. 组件贡献度对比图
        self._plot_component_contribution(analysis_results, output_path)
        
        # 2. 性能-效率权衡图
        self._plot_performance_efficiency_tradeoff(analysis_results, output_path)
        
        # 3. 数据集特定分析
        self._plot_dataset_specific_analysis(analysis_results, output_path)
        
        logger.info(f"✅ 可视化图表已保存到: {output_path}")
    
    def _plot_component_contribution(self, analysis_results: Dict, output_path: Path):
        """绘制组件贡献度图"""
        try:
            # 提取完整消融实验的数据
            if "complete_ablation" in analysis_results:
                data = analysis_results["complete_ablation"]
                
                if "relative_performance" in data:
                    relative_perf = data["relative_performance"]
                    
                    # 准备数据
                    methods = []
                    em_changes = []
                    f1_changes = []
                    
                    for method, changes in relative_perf.items():
                        methods.append(self.component_mapping.get(method, method))
                        em_changes.append(changes.get("exact_match", 0))
                        f1_changes.append(changes.get("f1_score", 0))
                    
                    # 创建图表
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
                    
                    # EM 变化
                    bars1 = ax1.bar(methods, em_changes, color='skyblue', alpha=0.7)
                    ax1.set_title('组件消融对 Exact Match 的影响')
                    ax1.set_ylabel('性能变化 (%)')
                    ax1.axhline(y=0, color='red', linestyle='--', alpha=0.5)
                    ax1.tick_params(axis='x', rotation=45)
                    
                    # F1 变化
                    bars2 = ax2.bar(methods, f1_changes, color='lightcoral', alpha=0.7)
                    ax2.set_title('组件消融对 F1 Score 的影响')
                    ax2.set_ylabel('性能变化 (%)')
                    ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
                    ax2.tick_params(axis='x', rotation=45)
                    
                    plt.tight_layout()
                    plt.savefig(output_path / "component_contribution.png", dpi=300, bbox_inches='tight')
                    plt.close()
                    
        except Exception as e:
            logger.warning(f"⚠️ 无法生成组件贡献度图: {e}")
    
    def _plot_performance_efficiency_tradeoff(self, analysis_results: Dict, output_path: Path):
        """绘制性能-效率权衡图"""
        # 实现性能vs效率的散点图
        pass
    
    def _plot_dataset_specific_analysis(self, analysis_results: Dict, output_path: Path):
        """绘制数据集特定分析图"""
        # 实现不同数据集上的性能对比
        pass
    
    def generate_report(self, analysis_results: Dict[str, Any], 
                       output_file: str = "./experiments/ablation_study/detailed_analysis_report.md"):
        """生成详细分析报告"""
        logger.info("📝 生成详细分析报告")
        
        report_content = self._create_report_content(analysis_results)
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"✅ 详细分析报告已保存: {output_path}")
    
    def _create_report_content(self, analysis_results: Dict[str, Any]) -> str:
        """创建报告内容"""
        content = """# AdaptiveRAG 消融实验详细分析报告

## 实验概述

本报告详细分析了 AdaptiveRAG 各组件的贡献度和性能影响。

## 主要发现

"""
        
        # 添加具体分析结果
        for exp_name, exp_data in analysis_results.items():
            content += f"\n### {exp_name} 实验结果\n\n"
            
            if "relative_performance" in exp_data:
                content += "#### 相对性能变化\n\n"
                for method, changes in exp_data["relative_performance"].items():
                    method_name = self.component_mapping.get(method, method)
                    content += f"- **{method_name}**:\n"
                    content += f"  - Exact Match: {changes.get('exact_match', 0):+.2f}%\n"
                    content += f"  - F1 Score: {changes.get('f1_score', 0):+.2f}%\n"
                    content += f"  - ROUGE-L: {changes.get('rouge_l', 0):+.2f}%\n\n"
        
        content += """
## 结论

[基于实验结果的结论将在这里补充]

## 建议

[基于分析的改进建议将在这里补充]
"""
        
        return content


if __name__ == "__main__":
    # 测试消融分析器
    analyzer = AblationAnalyzer()
    results = analyzer.analyze_component_contribution()
    analyzer.generate_visualization(results)
    analyzer.generate_report(results)
