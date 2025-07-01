"""
模拟数据管理器 - 用于WebUI展示
"""


class MockDataManager:
    """模拟数据管理器 - 用于WebUI展示"""

    def __init__(self):
        self.corpus_stats = {
            "total_documents": 1000,
            "total_tokens": 500000,
            "avg_doc_length": 500,
            "last_updated": "2024-01-01 12:00:00"
        }

    def get_corpus_stats(self):
        """获取语料库统计信息"""
        return self.corpus_stats

    def search_documents(self, query: str, top_k: int = 5):
        """模拟文档搜索"""
        return [
            {
                "id": f"doc_{i}",
                "title": f"Document {i}",
                "content": f"This is a sample document about {query}...",
                "score": 0.9 - i * 0.1
            }
            for i in range(1, min(top_k + 1, 6))
        ] 