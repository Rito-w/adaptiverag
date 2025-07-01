#!/usr/bin/env python3Add comment更多操作
"""
=== 智能任务分解器 ===

基于 FlashRAG 架构，实现智能的多维度任务分解
借鉴 LevelRAG 的问题分解思路，增强自适应能力
"""

import re
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# 借鉴 FlashRAG 的日志系统
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskType(Enum):
    """任务类型枚举"""
    FACTUAL = "factual"          # 事实性问题
    SEMANTIC = "semantic"        # 语义问题
    TEMPORAL = "temporal"        # 时间相关问题
    COMPARATIVE = "comparative"  # 比较性问题
    CAUSAL = "causal"           # 因果关系问题
    SPATIAL = "spatial"         # 空间相关问题


@dataclass
class SubTask:
    """子任务数据结构"""
    id: str
    content: str
    task_type: TaskType
    priority: float = 1.0
    entities: List[str] = None
    relations: List[str] = None
    temporal_info: Dict[str, Any] = None
    parent_task_id: Optional[str] = None
    
    def __post_init__(self):
        if self.entities is None:
            self.entities = []
        if self.relations is None:
            self.relations = []
        if self.temporal_info is None:
            self.temporal_info = {}


class TaskDecomposer:
    """智能任务分解器"""
    
    def __init__(self, config):
        self.config = config
        self.subtask_config = config.subtask_config
        
        # 初始化分解规则
        self.decompose_patterns = self._init_decompose_patterns()
        self.entity_patterns = self._init_entity_patterns()
        self.temporal_patterns = self._init_temporal_patterns()
        
        logger.info("TaskDecomposer 初始化完成")
    
    def _init_decompose_patterns(self) -> Dict[TaskType, List[Dict]]:
        """初始化分解模式"""
        return {
            TaskType.FACTUAL: [
                {
                    "pattern": r"what is (.*?)\?",
                    "template": "Define {entity}",
                    "priority": 0.9
                },
                {
                    "pattern": r"who is (.*?)\?",
                    "template": "Get information about {entity}",
                    "priority": 0.9
                }
            ],
            TaskType.COMPARATIVE: [
                {
                    "pattern": r"(.*?) vs (.*?)",
                    "template": ["Get information about {entity1}", "Get information about {entity2}"],
                    "priority": 0.8
                },
                {
                    "pattern": r"compare (.*?) and (.*?)",
                    "template": ["Analyze {entity1}", "Analyze {entity2}"],
                    "priority": 0.8
                }
            ],
            TaskType.TEMPORAL: [
                {
                    "pattern": r"when (.*?)\?",
                    "template": "Find temporal information about {event}",
                    "priority": 0.9
                },
                {
                    "pattern": r"(.*?) in (\d{4})",
                    "template": "Find information about {event} in {year}",
                    "priority": 0.7
                }
            ]
        }
    
    def _init_entity_patterns(self) -> List[str]:
        """初始化实体识别模式"""
        return [
            r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",  # 人名
            r"\b[A-Z][a-zA-Z\s]+(?:Inc|Corp|Ltd|Company)\b",  # 公司名
            r"\b\d{4}\b",  # 年份
            r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b"  # 专有名词
        ]
    
    def _init_temporal_patterns(self) -> List[str]:
        """初始化时间模式"""
        return [
            r"\b\d{4}\b",  # 年份
            r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b",
            r"\b\d{1,2}/\d{1,2}/\d{4}\b",  # 日期格式
            r"\b(?:before|after|during|since|until)\b"  # 时间关系词
        ]
    
    def decompose_query(self, query: str) -> List[SubTask]:
        """分解查询为子任务"""
        logger.info(f"开始分解查询: {query}")
        
        # 1. 识别任务类型
        task_type = self._identify_task_type(query)
        logger.info(f"识别的任务类型: {task_type.value}")
        
        # 2. 提取实体和关系
        entities = self._extract_entities(query)
        temporal_info = self._extract_temporal_info(query)
        
        # 3. 基于模式分解
        subtasks = self._pattern_based_decompose(query, task_type, entities, temporal_info)
        
        # 4. 如果没有匹配的模式，使用通用分解
        if not subtasks:
            subtasks = self._generic_decompose(query, task_type, entities, temporal_info)
        
        logger.info(f"分解完成，生成 {len(subtasks)} 个子任务")
        return subtasks
    
    def _identify_task_type(self, query: str) -> TaskType:
        """识别任务类型"""
        query_lower = query.lower()
        
        # 比较性关键词
        comparative_keywords = ["compare", "vs", "versus", "difference", "similar", "contrast"]
        if any(keyword in query_lower for keyword in comparative_keywords):
            return TaskType.COMPARATIVE
        
        # 时间性关键词
        temporal_keywords = ["when", "before", "after", "during", "since", "until", "first", "last"]
        if any(keyword in query_lower for keyword in temporal_keywords):
            return TaskType.TEMPORAL
        
        # 因果关系关键词
        causal_keywords = ["why", "because", "cause", "reason", "result", "effect"]
        if any(keyword in query_lower for keyword in causal_keywords):
            return TaskType.CAUSAL
        
        # 事实性关键词
        factual_keywords = ["what", "who", "where", "which", "define", "explain"]
        if any(keyword in query_lower for keyword in factual_keywords):
            return TaskType.FACTUAL
        
        # 默认为语义类型
        return TaskType.SEMANTIC
    
    def _extract_entities(self, query: str) -> List[str]:
        """提取实体"""
        entities = []
        for pattern in self.entity_patterns:
            matches = re.findall(pattern, query)
            entities.extend(matches)
        
        # 去重并过滤
        entities = list(set(entities))
        entities = [e for e in entities if len(e) > 2]  # 过滤太短的实体
        
        return entities
    
    def _extract_temporal_info(self, query: str) -> Dict[str, Any]:
        """提取时间信息"""
        temporal_info = {}
        
        for pattern in self.temporal_patterns:
            matches = re.findall(pattern, query)
            if matches:
                if pattern == r"\b\d{4}\b":
                    temporal_info["years"] = matches
                elif "before|after|during|since|until" in pattern:
                    temporal_info["relations"] = matches
                else:
                    temporal_info["dates"] = matches
        
        return temporal_info
    
    def _pattern_based_decompose(self, query: str, task_type: TaskType, entities: List[str], temporal_info: Dict) -> List[SubTask]:
        """基于模式的分解"""
        subtasks = []
        
        if task_type not in self.decompose_patterns:
            return subtasks
        
        patterns = self.decompose_patterns[task_type]
        
        for pattern_info in patterns:
            pattern = pattern_info["pattern"]
            template = pattern_info["template"]
            priority = pattern_info["priority"]
            
            match = re.search(pattern, query.lower())
            if match:
                if isinstance(template, list):
                    # 多个子任务
                    for i, tmpl in enumerate(template):
                        content = self._format_template(tmpl, match, entities)
                        subtask = SubTask(
                            id=f"subtask_{len(subtasks)}",
                            content=content,
                            task_type=task_type,
                            priority=priority,
                            entities=entities,
                            temporal_info=temporal_info
                        )
                        subtasks.append(subtask)
                else:
                    # 单个子任务
                    content = self._format_template(template, match, entities)
                    subtask = SubTask(
                        id=f"subtask_{len(subtasks)}",
                        content=content,
                        task_type=task_type,
                        priority=priority,
                        entities=entities,
                        temporal_info=temporal_info
                    )
                    subtasks.append(subtask)
                
                break  # 找到匹配的模式就停止
        
        return subtasks
    
    def _format_template(self, template: str, match, entities: List[str]) -> str:
        """格式化模板"""
        content = template
        
        # 替换匹配的组
        for i, group in enumerate(match.groups()):
            content = content.replace(f"{{entity{i+1}}}", group)
            content = content.replace("{entity}", group)
            content = content.replace("{event}", group)
            content = content.replace("{year}", group)
        
        return content
    
    def _generic_decompose(self, query: str, task_type: TaskType, entities: List[str], temporal_info: Dict) -> List[SubTask]:
        """通用分解方法"""
        subtasks = []
        
        # 为每个实体创建一个子任务
        for i, entity in enumerate(entities):
            subtask = SubTask(
                id=f"subtask_{i}",
                content=f"Get information about {entity}",
                task_type=TaskType.FACTUAL,
                priority=0.7,
                entities=[entity],
                temporal_info=temporal_info
            )
            subtasks.append(subtask)
        
        # 如果没有实体，创建一个通用子任务
        if not subtasks:
            subtask = SubTask(
                id="subtask_0",
                content=query,
                task_type=task_type,
                priority=1.0,
                entities=entities,
                temporal_info=temporal_info
            )
            subtasks.append(subtask)
        
        return subtasks
    
    def get_decomposition_summary(self, subtasks: List[SubTask]) -> Dict[str, Any]:
        """获取分解摘要"""
        task_types = {}
        total_priority = 0
        
        for subtask in subtasks:
            task_type = subtask.task_type.value
            task_types[task_type] = task_types.get(task_type, 0) + 1
            total_priority += subtask.priority
        
        return {
            "total_subtasks": len(subtasks),
            "task_types": task_types,
            "average_priority": total_priority / len(subtasks) if subtasks else 0,
            "entities_count": len(set(entity for subtask in subtasks for entity in subtask.entities))
        }


if __name__ == "__main__":
    # 测试任务分解器
    from config import create_default_config
    
    config = create_default_config()
    decomposer = TaskDecomposer(config)
    
    # 测试查询
    test_queries = [
        "What is machine learning?",
        "Compare Python and Java programming languages",
        "When was the first computer invented?",
        "Who is the founder of Microsoft?"
    ]
    
    for query in test_queries:
        print(f"\n查询: {query}")
        subtasks = decomposer.decompose_query(query)
        
        for subtask in subtasks:
            print(f"  子任务: {subtask.content}")
            print(f"  类型: {subtask.task_type.value}")
            print(f"  优先级: {subtask.priority}")
            print(f"  实体: {subtask.entities}")
        
        summary = decomposer.get_decomposition_summary(subtasks)
        print(f"  摘要: {summary}")