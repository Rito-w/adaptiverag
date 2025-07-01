"""
智能自适应 RAG 引擎 - 借鉴 FlashRAG 的 Engine 设计
"""

import time
from typing import Dict, Any
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from adaptive_rag.config import create_flexrag_integrated_config, FLEXRAG_AVAILABLE
from adaptive_rag.core.flexrag_integrated_assistant import FlexRAGIntegratedAssistant
from .mock_data_manager import MockDataManager


class AdaptiveRAGEngine:
    """智能自适应 RAG 引擎 - 借鉴 FlashRAG 的 Engine 设计"""
    
    def __init__(self):
        self.config = create_flexrag_integrated_config()

        # 初始化 FlexRAG 集成助手
        self.assistant = FlexRAGIntegratedAssistant(self.config)

        # 获取系统信息
        self.system_info = self.assistant.get_system_info()

        # 状态管理
        self.is_initialized = True
        self.current_query = ""
        self.last_results = None

        # 添加数据管理器（模拟）
        self.data_manager = MockDataManager()

        print(f"✅ AdaptiveRAG 引擎初始化完成")
        print(f"   FlexRAG 可用: {'是' if FLEXRAG_AVAILABLE else '否'}")
        print(f"   助手类型: {self.system_info['assistant_type']}")
        print(f"   支持功能: {', '.join(self.system_info['supported_features'])}")
        
    def initialize_components(self):
        """初始化所有组件（FlexRAG 集成版本中已自动完成）"""
        # FlexRAG 集成助手已经在 __init__ 中完成了所有初始化
        pass
    
    def process_query(self, query: str, show_details: bool = True) -> Dict[str, Any]:
        """处理查询 - 使用 FlexRAG 集成助手"""
        start_time = time.time()

        # 使用 FlexRAG 集成助手处理查询
        result = self.assistant.answer(query)

        processing_time = time.time() - start_time

        # 转换为 Web UI 兼容的格式
        web_result = {
            "query": query,
            "answer": result.answer,
            "subtasks": result.subtasks,
            "retrieval_results": result.retrieval_results,
            "ranking_results": result.ranking_results,
            "generation_result": result.generation_result,
            "processing_time": processing_time,
            "total_time": result.total_time,
            "metadata": result.metadata
        }

        self.current_query = query
        self.last_results = web_result

        return web_result 