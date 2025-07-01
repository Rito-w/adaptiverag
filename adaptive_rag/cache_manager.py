#!/usr/bin/env python3Add comment更多操作
"""
=== 缓存管理器 ===

提供查询结果缓存和模型缓存功能
"""

import os
import json
import pickle
import hashlib
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CacheManager:
    """缓存管理器"""
    
    def __init__(self, cache_dir: str = "/root/autodl-tmp/rag_project/cache"):
        self.cache_dir = cache_dir
        self.query_cache_dir = os.path.join(cache_dir, "queries")
        self.model_cache_dir = os.path.join(cache_dir, "models")
        
        # 创建缓存目录
        os.makedirs(self.query_cache_dir, exist_ok=True)
        os.makedirs(self.model_cache_dir, exist_ok=True)
        
        # 缓存配置
        self.max_cache_age = timedelta(hours=24)  # 24小时过期
        self.max_cache_size = 1000  # 最大缓存条目数
        
        logger.info(f"CacheManager 初始化完成，缓存目录: {cache_dir}")
    
    def _get_cache_key(self, query: str, config_hash: str = "") -> str:
        """生成缓存键"""
        content = f"{query}_{config_hash}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_query_cache(self, query: str, config_hash: str = "") -> Optional[Dict[str, Any]]:
        """获取查询缓存"""
        cache_key = self._get_cache_key(query, config_hash)
        cache_file = os.path.join(self.query_cache_dir, f"{cache_key}.json")
        
        if not os.path.exists(cache_file):
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # 检查缓存是否过期
            cache_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.now() - cache_time > self.max_cache_age:
                os.remove(cache_file)
                return None
            
            logger.info(f"命中查询缓存: {query[:50]}...")
            return cache_data['result']
            
        except Exception as e:
            logger.error(f"读取查询缓存失败: {e}")
            return None
    
    def set_query_cache(self, query: str, result: Dict[str, Any], config_hash: str = ""):
        """设置查询缓存"""
        try:
            cache_key = self._get_cache_key(query, config_hash)
            cache_file = os.path.join(self.query_cache_dir, f"{cache_key}.json")
            
            cache_data = {
                'query': query,
                'result': result,
                'timestamp': datetime.now().isoformat(),
                'config_hash': config_hash
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"保存查询缓存: {query[:50]}...")
            
            # 清理过期缓存
            self._cleanup_expired_cache()
            
        except Exception as e:
            logger.error(f"保存查询缓存失败: {e}")
    
    def _cleanup_expired_cache(self):
        """清理过期缓存"""
        try:
            cache_files = os.listdir(self.query_cache_dir)
            current_time = datetime.now()
            
            for cache_file in cache_files:
                if not cache_file.endswith('.json'):
                    continue
                
                file_path = os.path.join(self.query_cache_dir, cache_file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        cache_data = json.load(f)
                    
                    cache_time = datetime.fromisoformat(cache_data['timestamp'])
                    if current_time - cache_time > self.max_cache_age:
                        os.remove(file_path)
                        logger.debug(f"删除过期缓存: {cache_file}")
                        
                except Exception as e:
                    logger.warning(f"处理缓存文件 {cache_file} 失败: {e}")
                    
        except Exception as e:
            logger.error(f"清理缓存失败: {e}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        try:
            query_cache_files = [f for f in os.listdir(self.query_cache_dir) if f.endswith('.json')]
            
            total_size = 0
            for cache_file in query_cache_files:
                file_path = os.path.join(self.query_cache_dir, cache_file)
                total_size += os.path.getsize(file_path)
            
            return {
                'query_cache_count': len(query_cache_files),
                'total_cache_size_mb': total_size / (1024 * 1024),
                'cache_dir': self.cache_dir,
                'max_cache_age_hours': self.max_cache_age.total_seconds() / 3600
            }
            
        except Exception as e:
            logger.error(f"获取缓存统计失败: {e}")
            return {}
    
    def clear_cache(self):
        """清空所有缓存"""
        try:
            import shutil
            if os.path.exists(self.cache_dir):
                shutil.rmtree(self.cache_dir)
            
            os.makedirs(self.query_cache_dir, exist_ok=True)
            os.makedirs(self.model_cache_dir, exist_ok=True)
            
            logger.info("缓存已清空")
            
        except Exception as e:
            logger.error(f"清空缓存失败: {e}")


# 全局缓存管理器实例
_cache_manager = None

def get_cache_manager() -> CacheManager:
    """获取全局缓存管理器"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager


if __name__ == "__main__":
    # 测试缓存管理器
    cache_manager = CacheManager()
    
    # 测试查询缓存
    test_query = "What is machine learning?"
    test_result = {
        "query_type": "factual",
        "sub_queries": ["Define machine learning"],
        "documents": ["doc1", "doc2"]
    }
    
    # 保存缓存
    cache_manager.set_query_cache(test_query, test_result)
    
    # 读取缓存
    cached_result = cache_manager.get_query_cache(test_query)
    print(f"缓存测试: {cached_result is not None}")
    
    # 获取统计信息
    stats = cache_manager.get_cache_stats()
    print(f"缓存统计: {stats}")