#!/usr/bin/env python3
"""
=== 数据管理器 ===

借鉴 FlashRAG 的数据集处理和 LightRAG 的文档管理
提供统一的数据接口和处理流程

设计理念：
1. 借鉴 FlashRAG 的数据集标准化处理
2. 参考 LightRAG 的文档分块和索引
3. 融合 GraphRAG 的结构化数据处理
4. 支持多种数据源和格式
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Iterator, Union
from dataclasses import dataclass, field
from pathlib import Path
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class Document:
    """文档数据结构 - 借鉴 FlashRAG 的设计"""
    id: str
    content: str
    title: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    source: str = ""
    timestamp: Optional[str] = None
    
    def __post_init__(self):
        if not self.id:
            # 自动生成 ID
            self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """生成文档 ID"""
        content_hash = hashlib.md5(self.content.encode()).hexdigest()
        return f"doc_{content_hash[:8]}"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "content": self.content,
            "title": self.title,
            "metadata": self.metadata,
            "source": self.source,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Document":
        """从字典创建文档"""
        return cls(
            id=data.get("id", ""),
            content=data.get("content", ""),
            title=data.get("title", ""),
            metadata=data.get("metadata", {}),
            source=data.get("source", ""),
            timestamp=data.get("timestamp")
        )


@dataclass
class QueryResult:
    """查询结果数据结构"""
    query: str
    documents: List[Document]
    scores: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)
    processing_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "query": self.query,
            "documents": [doc.to_dict() for doc in self.documents],
            "scores": self.scores,
            "metadata": self.metadata,
            "processing_time": self.processing_time
        }


class DataManager:
    """数据管理器 - 借鉴 FlashRAG 的数据处理架构"""
    
    def __init__(self, config):
        self.config = config
        self.documents: Dict[str, Document] = {}

        # 数据路径优先级：adaptive_rag 内部数据 > 项目根目录数据 > 外部数据 > 配置路径
        current_dir = os.path.dirname(os.path.abspath(__file__))  # adaptive_rag 目录
        project_root = os.path.dirname(current_dir)  # 项目根目录

        # 1. 优先使用 adaptive_rag 内部的数据
        adaptive_rag_data = os.path.join(current_dir, "data", "general_knowledge.jsonl")
        if os.path.exists(adaptive_rag_data):
            self.corpus_path = adaptive_rag_data
            logger.info(f"✅ 使用 adaptive_rag 内部数据: {adaptive_rag_data}")

        # 2. 使用项目根目录的数据
        elif os.path.exists(os.path.join(project_root, "data", "general_knowledge.jsonl")):
            self.corpus_path = os.path.join(project_root, "data", "general_knowledge.jsonl")
            logger.info(f"📂 使用项目根目录数据: {self.corpus_path}")

        # 3. 回退到外部 FlashRAG 数据
        elif os.path.exists("/root/autodl-tmp/rag_project/FlashRAG/examples/quick_start/indexes/general_knowledge.jsonl"):
            self.corpus_path = "/root/autodl-tmp/rag_project/FlashRAG/examples/quick_start/indexes/general_knowledge.jsonl"
            logger.info(f"🔗 使用外部 FlashRAG 数据: {self.corpus_path}")

        # 4. 使用 adaptive_rag 内部示例数据
        elif os.path.exists(os.path.join(current_dir, "data", "sample_corpus.jsonl")):
            self.corpus_path = os.path.join(current_dir, "data", "sample_corpus.jsonl")
            logger.info(f"📄 使用 adaptive_rag 示例数据: {self.corpus_path}")

        # 5. 使用项目根目录示例数据
        elif os.path.exists(os.path.join(project_root, "data", "sample_corpus.jsonl")):
            self.corpus_path = os.path.join(project_root, "data", "sample_corpus.jsonl")
            logger.info(f"📄 使用项目示例数据: {self.corpus_path}")

        # 6. 最后回退到配置路径
        else:
            config_path = getattr(config, 'corpus_path', './data/general_knowledge.jsonl')
            # 如果是相对路径，基于项目根目录解析
            if not os.path.isabs(config_path):
                self.corpus_path = os.path.join(project_root, config_path)
            else:
                self.corpus_path = config_path
            logger.info(f"⚙️ 使用配置数据路径: {self.corpus_path}")
        
        logger.info("DataManager 初始化完成")
    
    def load_corpus(self) -> int:
        """加载语料库"""
        if not os.path.exists(self.corpus_path):
            logger.warning(f"语料库文件不存在: {self.corpus_path}")
            return 0

        count = 0
        try:
            logger.info(f"开始加载语料库: {self.corpus_path}")
            with open(self.corpus_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if line.strip():
                        try:
                            data = json.loads(line.strip())
                            doc = self._parse_document(data)
                            if doc:
                                self.documents[doc.id] = doc
                                count += 1

                                # 每1000个文档打印一次进度
                                if count % 1000 == 0:
                                    logger.info(f"已加载 {count} 个文档...")

                        except json.JSONDecodeError as e:
                            logger.warning(f"第 {line_num} 行解析 JSON 失败: {e}")
                            continue
                        except Exception as e:
                            logger.warning(f"第 {line_num} 行处理失败: {e}")
                            continue

            logger.info(f"✅ 成功加载 {count} 个文档")
            return count

        except Exception as e:
            logger.error(f"加载语料库失败: {e}")
            return 0
    
    def _parse_document(self, data: Dict[str, Any]) -> Optional[Document]:
        """解析文档数据"""
        try:
            # FlashRAG 格式
            if 'contents' in data:
                doc_id = data.get('id', '')
                if not doc_id:
                    # 如果没有 ID，生成一个
                    import hashlib
                    doc_id = hashlib.md5(data['contents'].encode()).hexdigest()[:8]

                return Document(
                    id=doc_id,
                    content=data['contents'],
                    title=data.get('title', ''),
                    metadata=data.get('metadata', {}),
                    source='flashrag'
                )

            # 标准格式
            elif 'content' in data:
                return Document(
                    id=data.get('id', ''),
                    content=data['content'],
                    title=data.get('title', ''),
                    metadata=data.get('metadata', {}),
                    source=data.get('source', '')
                )

            else:
                # 尝试其他可能的字段名
                content_field = None
                for field in ['text', 'body', 'document', 'passage']:
                    if field in data:
                        content_field = field
                        break

                if content_field:
                    doc_id = data.get('id', '')
                    if not doc_id:
                        import hashlib
                        doc_id = hashlib.md5(data[content_field].encode()).hexdigest()[:8]

                    return Document(
                        id=doc_id,
                        content=data[content_field],
                        title=data.get('title', ''),
                        metadata=data.get('metadata', {}),
                        source='auto_detected'
                    )
                else:
                    logger.warning(f"未知的文档格式: {list(data.keys())}")
                    return None

        except Exception as e:
            logger.error(f"解析文档失败: {e}")
            return None
    
    def search_documents(self, query: str, top_k: int = 10) -> List[Document]:
        """搜索文档 - 简单的关键词匹配"""
        if not self.documents:
            logger.warning("没有加载的文档")
            return []
        
        # 简单的关键词匹配
        query_lower = query.lower()
        scored_docs = []
        
        for doc in self.documents.values():
            score = 0.0
            content_lower = doc.content.lower()
            title_lower = doc.title.lower()
            
            # 计算匹配分数
            for word in query_lower.split():
                if word in content_lower:
                    score += content_lower.count(word) * 1.0
                if word in title_lower:
                    score += title_lower.count(word) * 2.0  # 标题权重更高
            
            if score > 0:
                scored_docs.append((doc, score))
        
        # 按分数排序
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        # 返回前 top_k 个文档
        return [doc for doc, score in scored_docs[:top_k]]
    
    def get_document(self, doc_id: str) -> Optional[Document]:
        """获取指定文档"""
        return self.documents.get(doc_id)
    
    def add_document(self, document: Document) -> bool:
        """添加文档"""
        try:
            self.documents[document.id] = document
            return True
        except Exception as e:
            logger.error(f"添加文档失败: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return self.get_corpus_stats()

    def get_corpus_stats(self) -> Dict[str, Any]:
        """获取语料库统计信息"""
        total_docs = len(self.documents)
        total_chars = sum(len(doc.content) for doc in self.documents.values())
        avg_length = total_chars / total_docs if total_docs > 0 else 0
        
        sources = {}
        for doc in self.documents.values():
            source = doc.source or "unknown"
            sources[source] = sources.get(source, 0) + 1
        
        return {
            "total_documents": total_docs,
            "total_characters": total_chars,
            "average_length": avg_length,
            "sources": sources,
            "corpus_path": self.corpus_path
        }
    
    def export_documents(self, output_path: str, format: str = "jsonl") -> bool:
        """导出文档"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                if format == "jsonl":
                    for doc in self.documents.values():
                        f.write(json.dumps(doc.to_dict(), ensure_ascii=False) + '\n')
                elif format == "json":
                    docs_list = [doc.to_dict() for doc in self.documents.values()]
                    json.dump(docs_list, f, ensure_ascii=False, indent=2)
                else:
                    raise ValueError(f"不支持的格式: {format}")
            
            logger.info(f"成功导出 {len(self.documents)} 个文档到 {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"导出文档失败: {e}")
            return False


def create_sample_corpus(output_path: str, num_docs: int = 100):
    """创建示例语料库"""
    sample_docs = [
        {
            "id": f"sample_{i}",
            "content": f"这是第 {i} 个示例文档。它包含了关于人工智能、机器学习和深度学习的内容。",
            "title": f"示例文档 {i}",
            "metadata": {"category": "AI", "length": "short"},
            "source": "sample"
        }
        for i in range(num_docs)
    ]
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for doc in sample_docs:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    
    print(f"创建了包含 {num_docs} 个文档的示例语料库: {output_path}")


if __name__ == "__main__":
    # 测试数据管理器
    from config import create_default_config
    
    config = create_default_config()
    data_manager = DataManager(config)
    
    # 加载数据
    count = data_manager.load_corpus()
    print(f"加载了 {count} 个文档")
    
    # 获取统计信息
    stats = data_manager.get_statistics()
    print("统计信息:", stats)
    
    # 测试搜索
    results = data_manager.search_documents("machine learning", top_k=3)
    print(f"搜索结果: {len(results)} 个文档")
