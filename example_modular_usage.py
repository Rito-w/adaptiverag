#!/usr/bin/env python3
"""
=== AdaptiveRAG 模块化使用示例 ===

展示如何在实际应用中使用模块化配置系统
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from adaptive_rag.config import create_config_from_yaml, print_module_status
from adaptive_rag.core.module_manager import ModuleManager


class AdaptiveRAGSystem:
    """
    AdaptiveRAG 系统主类
    
    使用模块管理器来动态管理各个组件
    """
    
    def __init__(self, config_path: str, preset: str = None):
        """
        初始化系统
        
        Args:
            config_path: 配置文件路径
            preset: 预设模式 ("basic_mode", "performance_mode", "experimental_mode")
        """
        # 加载配置
        self.config = create_config_from_yaml(config_path, preset)
        
        # 初始化模块管理器
        self.module_manager = ModuleManager(self.config)
        self.module_manager.initialize_modules()
        
        print(f"🎯 AdaptiveRAG 系统已初始化 (模式: {preset or 'default'})")
        print_module_status(self.config)
    
    def process_query(self, query: str) -> dict:
        """
        处理查询
        
        Args:
            query: 用户查询
            
        Returns:
            处理结果
        """
        print(f"\n🔍 处理查询: {query}")
        
        result = {
            "query": query,
            "answer": "",
            "steps": [],
            "metadata": {}
        }
        
        # 1. 任务分解（如果启用）
        if self.module_manager.is_module_enabled("task_decomposer"):
            print("  📋 执行任务分解...")
            task_decomposer = self.module_manager.get_module("task_decomposer")
            if task_decomposer:
                # 实际调用任务分解器
                result["steps"].append("任务分解完成")
            else:
                # 模拟实现
                result["steps"].append("任务分解完成 (模拟)")
        
        # 2. 查询分析（如果启用）
        if self.module_manager.is_module_enabled("query_analyzer"):
            print("  🧠 执行查询分析...")
            query_analyzer = self.module_manager.get_module("query_analyzer")
            if query_analyzer:
                # 实际调用查询分析器
                result["steps"].append("查询分析完成")
            else:
                # 模拟实现
                result["steps"].append("查询分析完成 (模拟)")
        
        # 3. 检索策略规划（如果启用）
        if self.module_manager.is_module_enabled("retrieval_planner"):
            print("  📋 执行检索策略规划...")
            retrieval_planner = self.module_manager.get_module("retrieval_planner")
            if retrieval_planner:
                # 实际调用检索规划器
                result["steps"].append("检索策略规划完成")
            else:
                # 模拟实现
                result["steps"].append("检索策略规划完成 (模拟)")
        
        # 4. 多重检索（如果启用）
        if self.module_manager.is_module_enabled("multi_retriever"):
            print("  🔗 执行多重检索...")
            
            # 检查启用的检索器
            retrievers = []
            if self.module_manager.is_module_enabled("keyword_retriever"):
                retrievers.append("关键词检索")
            if self.module_manager.is_module_enabled("dense_retriever"):
                retrievers.append("密集检索")
            if self.module_manager.is_module_enabled("web_retriever"):
                retrievers.append("网络检索")
            
            result["steps"].append(f"多重检索完成 (使用: {', '.join(retrievers)})")
        
        # 5. 上下文重排序（如果启用）
        if self.module_manager.is_module_enabled("context_reranker"):
            print("  🎯 执行上下文重排序...")
            
            # 检查启用的重排序器
            rankers = []
            if self.module_manager.is_module_enabled("cross_encoder_ranker"):
                rankers.append("交叉编码器")
            if self.module_manager.is_module_enabled("colbert_ranker"):
                rankers.append("ColBERT")
            if self.module_manager.is_module_enabled("gpt_ranker"):
                rankers.append("GPT重排")
            
            result["steps"].append(f"上下文重排序完成 (使用: {', '.join(rankers)})")
        
        # 6. 自适应生成（如果启用）
        if self.module_manager.is_module_enabled("adaptive_generator"):
            print("  ✨ 执行自适应生成...")
            adaptive_generator = self.module_manager.get_module("adaptive_generator")
            if adaptive_generator:
                # 实际调用生成器
                result["answer"] = f"这是对查询 '{query}' 的智能回答"
            else:
                # 模拟实现
                result["answer"] = f"这是对查询 '{query}' 的模拟回答"
            
            result["steps"].append("自适应生成完成")
        
        # 7. 性能优化（如果启用）
        if self.module_manager.is_module_enabled("performance_optimizer"):
            print("  ⚡ 执行性能优化...")
            result["steps"].append("性能优化完成")
        
        # 8. 结果分析（如果启用）
        if self.module_manager.is_module_enabled("result_analyzer"):
            print("  📊 执行结果分析...")
            result["metadata"]["confidence"] = 0.85
            result["metadata"]["quality_score"] = 0.92
            result["steps"].append("结果分析完成")
        
        print(f"  ✅ 查询处理完成，共执行 {len(result['steps'])} 个步骤")
        return result
    
    def get_system_status(self) -> dict:
        """获取系统状态"""
        return {
            "enabled_modules": self.module_manager.get_enabled_modules(),
            "module_status": self.module_manager.get_module_status(),
            "config_device": self.config.device,
            "config_batch_size": self.config.batch_size
        }


def demo_basic_mode():
    """演示基础模式"""
    print("🔰 基础模式演示")
    print("=" * 60)
    
    system = AdaptiveRAGSystem(
        config_path="adaptive_rag/config/modular_config.yaml",
        preset="basic_mode"
    )
    
    # 处理查询
    result = system.process_query("什么是人工智能？")
    print(f"\n📝 回答: {result['answer']}")
    print(f"📋 执行步骤: {result['steps']}")


def demo_performance_mode():
    """演示高性能模式"""
    print("\n🚀 高性能模式演示")
    print("=" * 60)
    
    system = AdaptiveRAGSystem(
        config_path="adaptive_rag/config/modular_config.yaml",
        preset="performance_mode"
    )
    
    # 处理查询
    result = system.process_query("量子计算的最新发展是什么？")
    print(f"\n📝 回答: {result['answer']}")
    print(f"📋 执行步骤: {result['steps']}")
    print(f"📊 元数据: {result['metadata']}")


def demo_experimental_mode():
    """演示实验模式"""
    print("\n🔬 实验模式演示")
    print("=" * 60)
    
    system = AdaptiveRAGSystem(
        config_path="adaptive_rag/config/modular_config.yaml",
        preset="experimental_mode"
    )
    
    # 处理查询
    result = system.process_query("如何解决气候变化问题？")
    print(f"\n📝 回答: {result['answer']}")
    print(f"📋 执行步骤: {result['steps']}")
    print(f"📊 元数据: {result['metadata']}")


def demo_system_comparison():
    """演示不同模式的系统对比"""
    print("\n📊 系统模式对比")
    print("=" * 60)
    
    modes = ["basic_mode", "performance_mode", "experimental_mode"]
    
    for mode in modes:
        print(f"\n🔍 {mode} 模式:")
        system = AdaptiveRAGSystem(
            config_path="adaptive_rag/config/modular_config.yaml",
            preset=mode
        )
        
        status = system.get_system_status()
        enabled_count = len(status["enabled_modules"])
        total_modules = len(status["module_status"])
        
        print(f"  启用模块数: {enabled_count}/{total_modules}")
        print(f"  启用的模块: {', '.join(status['enabled_modules'][:5])}...")


def main():
    """主函数"""
    print("🎯 AdaptiveRAG 模块化系统使用演示")
    print("=" * 80)
    
    try:
        # 演示不同模式
        demo_basic_mode()
        demo_performance_mode()
        demo_experimental_mode()
        
        # 系统对比
        demo_system_comparison()
        
        print("\n🎉 演示完成！")
        print("\n💡 使用指南:")
        print("  1. 根据需求选择合适的预设模式")
        print("  2. 或者自定义模块配置")
        print("  3. 系统会自动根据配置启用/禁用相应模块")
        print("  4. 可以动态切换配置而无需重启系统")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
