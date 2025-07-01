#!/usr/bin/env python3Add comment更多操作
"""
=== 检索策略规划器 ===

基于任务分解结果，智能规划检索策略
"""

import logging
from typing import Dict, List, Any
from dataclasses import dataclass, field
from adaptive_rag.task_decomposer import SubTask, TaskType

logger = logging.getLogger(__name__)


@dataclass
class RetrievalPlan:
    """检索计划"""
    task_id: str
    weights: Dict[str, float] = field(default_factory=dict)
    top_k_per_retriever: Dict[str, int] = field(default_factory=dict)
    fusion_method: str = "weighted_sum"
    confidence: float = 0.8
    metadata: Dict[str, Any] = field(default_factory=dict)


class RetrievalPlanner:
    """检索策略规划器"""
    
    def __init__(self, config):
        self.config = config
        self.retrieval_plan_config = config.retrieval_plan_config
        logger.info("RetrievalPlanner 初始化完成")
    
    def plan_retrieval_strategy(self, subtasks: List[SubTask]) -> Dict[str, RetrievalPlan]:
        """为子任务规划检索策略"""
        plans = {}
        
        for subtask in subtasks:
            plan = self._create_plan_for_task(subtask)
            plans[subtask.id] = plan
        
        logger.info(f"为 {len(subtasks)} 个子任务创建了检索计划")
        return plans
    
    def _create_plan_for_task(self, subtask: SubTask) -> RetrievalPlan:
        """为单个任务创建检索计划"""
        task_type = subtask.task_type
        
        # 获取任务类型特定的权重
        if task_type in self.retrieval_plan_config.task_specific_weights:
            weights = self.retrieval_plan_config.task_specific_weights[task_type].copy()
        else:
            weights = self.retrieval_plan_config.default_weights.copy()
        
        # 获取 top-k 配置
        top_k_config = self.retrieval_plan_config.top_k_config.copy()
        
        # 根据任务优先级调整
        if subtask.priority > 0.8:
            # 高优先级任务增加检索数量
            for retriever in top_k_config:
                top_k_config[retriever] = int(top_k_config[retriever] * 1.2)
        
        # 根据实体数量调整
        if len(subtask.entities) > 3:
            # 多实体任务偏向关键词检索
            weights["keyword"] = min(weights["keyword"] + 0.1, 0.8)
            weights["dense"] = max(weights["dense"] - 0.05, 0.1)
            weights["web"] = max(weights["web"] - 0.05, 0.1)
        
        # 确保权重和为1
        total_weight = sum(weights.values())
        for key in weights:
            weights[key] /= total_weight
        
        plan = RetrievalPlan(
            task_id=subtask.id,
            weights=weights,
            top_k_per_retriever=top_k_config,
            fusion_method="weighted_sum",
            confidence=subtask.priority,
            metadata={
                "task_type": task_type.value,
                "entities": subtask.entities,
                "temporal_info": subtask.temporal_info
            }
        )
        
        return plan
    
    def update_plan_based_on_feedback(self, plan: RetrievalPlan, feedback: Dict[str, Any]) -> RetrievalPlan:
        """基于反馈更新检索计划"""
        # 这里可以实现基于用户反馈的计划调整逻辑
        return plan
    
    def get_plan_explanation(self, plan: RetrievalPlan) -> str:
        """获取计划解释"""
        explanation = f"检索计划 (任务ID: {plan.task_id}):\n"
        explanation += f"权重分配: {plan.weights}\n"
        explanation += f"检索数量: {plan.top_k_per_retriever}\n"
        explanation += f"融合方法: {plan.fusion_method}\n"
        explanation += f"置信度: {plan.confidence:.2f}"
        
        return explanation


if __name__ == "__main__":
    # 测试检索规划器
    from adaptive_rag.config import create_default_config
    from adaptive_rag.task_decomposer import TaskDecomposer
    
    config = create_default_config()
    decomposer = TaskDecomposer(config)
    planner = RetrievalPlanner(config)
    
    # 测试查询
    query = "Compare machine learning and deep learning"
    subtasks = decomposer.decompose_query(query)
    
    # 创建检索计划
    plans = planner.plan_retrieval_strategy(subtasks)
    
    print(f"为查询 '{query}' 创建了 {len(plans)} 个检索计划:")
    for task_id, plan in plans.items():
        print(f"\n{planner.get_plan_explanation(plan)}")