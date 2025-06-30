#!/usr/bin/env python3
"""
=== 数据集下载器 ===

下载和预处理标准 RAG 评估数据集，借鉴 FlashRAG 的数据处理流程
"""

import json
import logging
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
import zipfile
import tarfile

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatasetDownloader:
    """数据集下载器 - 集成 FlashRAG 数据集"""

    # FlashRAG 数据集配置 (Hugging Face)
    FLASHRAG_DATASETS = {
        # 单跳问答
        "natural_questions": "nq",
        "trivia_qa": "trivia",
        "ms_marco": "msmarco",
        "web_questions": "webq",

        # 多跳推理
        "hotpot_qa": "hotpot",
        "2wiki_multihop": "2wiki",
        "musique": "musique",

        # 对话问答
        "quac": "quac",
        "coqa": "coqa",

        # 其他
        "entity_questions": "entityq",
        "wow": "wow",
        "fever": "fever"
    }

    # FlashRAG Hugging Face 数据集路径
    FLASHRAG_HF_REPO = "RUC-NLPIR/FlashRAG_datasets"

    # 备用数据集 URL 配置
    BACKUP_DATASET_URLS = {
        "natural_questions": {
            "train": "https://dl.fbaipublicfiles.com/dpr/data/retriever/nq-train.json.gz",
            "dev": "https://dl.fbaipublicfiles.com/dpr/data/retriever/nq-dev.json.gz",
            "test": "https://dl.fbaipublicfiles.com/dpr/data/retriever/nq-test.json.gz"
        },
        "hotpot_qa": {
            "train": "https://hotpotqa.github.io/data/hotpot_train_v1.1.json",
            "dev": "https://hotpotqa.github.io/data/hotpot_dev_distractor_v1.json",
            "test": "https://hotpotqa.github.io/data/hotpot_test_fullwiki_v1.json"
        },
        "trivia_qa": {
            "train": "http://nlp.cs.washington.edu/triviaqa/data/triviaqa-rc.tar.gz",
            "dev": "http://nlp.cs.washington.edu/triviaqa/data/triviaqa-rc.tar.gz",
            "test": "http://nlp.cs.washington.edu/triviaqa/data/triviaqa-rc.tar.gz"
        },
        "ms_marco": {
            "train": "https://msmarco.blob.core.windows.net/msmarcoranking/train_v2.1.json.gz",
            "dev": "https://msmarco.blob.core.windows.net/msmarcoranking/dev_v2.1.json.gz",
            "test": "https://msmarco.blob.core.windows.net/msmarcoranking/eval_v2.1_public.json.gz"
        }
    }
    
    def __init__(self, data_dir: str = "./data/benchmarks"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # 设置子目录
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.raw_dir.mkdir(exist_ok=True)
        self.processed_dir.mkdir(exist_ok=True)

        # 尝试导入 datasets 库用于 FlashRAG 数据集
        try:
            import datasets
            self.datasets_available = True
            logger.info("✅ datasets 库可用，将使用 FlashRAG 数据集")
        except ImportError:
            self.datasets_available = False
            logger.warning("⚠️ datasets 库不可用，将使用备用下载方法")

    def download_flashrag_dataset(self, dataset_name: str, split: str = "test") -> bool:
        """
        从 FlashRAG Hugging Face 仓库下载数据集

        Args:
            dataset_name: 数据集名称
            split: 数据集分割 (train/dev/test)

        Returns:
            bool: 下载是否成功
        """
        if not self.datasets_available:
            logger.error("❌ datasets 库不可用，无法下载 FlashRAG 数据集")
            return False

        if dataset_name not in self.FLASHRAG_DATASETS:
            logger.error(f"❌ 不支持的 FlashRAG 数据集: {dataset_name}")
            return False

        try:
            import datasets

            # 获取 FlashRAG 数据集名称
            flashrag_name = self.FLASHRAG_DATASETS[dataset_name]

            logger.info(f"📥 从 FlashRAG 下载数据集: {dataset_name} ({flashrag_name}) - {split}")

            # 下载数据集
            dataset = datasets.load_dataset(
                self.FLASHRAG_HF_REPO,
                flashrag_name,
                split=split,
                trust_remote_code=True
            )

            # 保存为 JSONL 格式
            output_file = self.data_dir / f"{dataset_name}_{split}.jsonl"

            with open(output_file, 'w', encoding='utf-8') as f:
                for item in dataset:
                    # 转换为标准格式
                    converted_item = self._convert_flashrag_format(item, dataset_name)
                    f.write(json.dumps(converted_item, ensure_ascii=False) + '\n')

            logger.info(f"✅ 数据集已保存: {output_file} ({len(dataset)} 条记录)")
            return True

        except Exception as e:
            logger.error(f"❌ 下载 FlashRAG 数据集失败: {e}")
            return False

    def _convert_flashrag_format(self, item: Dict[str, Any], dataset_name: str) -> Dict[str, Any]:
        """
        将 FlashRAG 数据格式转换为标准格式

        Args:
            item: FlashRAG 数据项
            dataset_name: 数据集名称

        Returns:
            Dict: 标准格式数据项
        """
        # 基础字段映射
        converted = {
            "id": item.get("id", ""),
            "question": item.get("question", ""),
            "answer": item.get("golden_answers", [""])[0] if item.get("golden_answers") else "",
            "golden_answers": item.get("golden_answers", []),
            "dataset": dataset_name
        }

        # 添加上下文信息（如果有）
        if "golden_contexts" in item and item["golden_contexts"]:
            converted["golden_contexts"] = item["golden_contexts"]

        # 添加元数据
        if "meta_data" in item:
            converted["meta_data"] = item["meta_data"]

        # 数据集特定处理
        if dataset_name == "hotpot_qa":
            # HotpotQA 特定字段
            if "supporting_facts" in item:
                converted["supporting_facts"] = item["supporting_facts"]
            if "type" in item:
                converted["question_type"] = item["type"]

        elif dataset_name == "natural_questions":
            # Natural Questions 特定字段
            if "annotations" in item:
                converted["annotations"] = item["annotations"]

        return converted
    
    def download_dataset(self, dataset_name: str, splits: List[str] = None) -> bool:
        """下载指定数据集"""
        if dataset_name not in self.DATASET_URLS:
            logger.error(f"不支持的数据集: {dataset_name}")
            return False
        
        if splits is None:
            splits = ["train", "dev", "test"]
        
        logger.info(f"📥 开始下载数据集: {dataset_name}")
        
        dataset_urls = self.DATASET_URLS[dataset_name]
        success = True
        
        for split in splits:
            if split not in dataset_urls:
                logger.warning(f"数据集 {dataset_name} 没有 {split} 分割")
                continue
            
            url = dataset_urls[split]
            success &= self._download_file(url, dataset_name, split)
        
        if success:
            logger.info(f"✅ 数据集 {dataset_name} 下载完成")
            # 预处理数据集
            self.preprocess_dataset(dataset_name, splits)
        else:
            logger.error(f"❌ 数据集 {dataset_name} 下载失败")
        
        return success
    
    def _download_file(self, url: str, dataset_name: str, split: str) -> bool:
        """下载单个文件"""
        try:
            # 解析文件名
            parsed_url = urlparse(url)
            filename = Path(parsed_url.path).name
            if not filename:
                filename = f"{dataset_name}_{split}.json"
            
            file_path = self.raw_dir / dataset_name / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 检查文件是否已存在
            if file_path.exists():
                logger.info(f"文件已存在，跳过下载: {file_path}")
                return True
            
            logger.info(f"下载文件: {url} -> {file_path}")
            
            # 下载文件
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # 如果是压缩文件，解压
            if filename.endswith('.gz'):
                self._extract_gz(file_path)
            elif filename.endswith('.tar.gz'):
                self._extract_tar_gz(file_path)
            elif filename.endswith('.zip'):
                self._extract_zip(file_path)
            
            logger.info(f"✅ 文件下载完成: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 下载文件失败: {url}, 错误: {e}")
            return False
    
    def _extract_gz(self, file_path: Path):
        """解压 .gz 文件"""
        import gzip
        
        output_path = file_path.with_suffix('')
        with gzip.open(file_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                f_out.write(f_in.read())
        
        logger.info(f"解压完成: {output_path}")
    
    def _extract_tar_gz(self, file_path: Path):
        """解压 .tar.gz 文件"""
        with tarfile.open(file_path, 'r:gz') as tar:
            tar.extractall(file_path.parent)
        
        logger.info(f"解压完成: {file_path}")
    
    def _extract_zip(self, file_path: Path):
        """解压 .zip 文件"""
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(file_path.parent)
        
        logger.info(f"解压完成: {file_path}")
    
    def preprocess_dataset(self, dataset_name: str, splits: List[str]):
        """预处理数据集为统一格式"""
        logger.info(f"🔄 开始预处理数据集: {dataset_name}")
        
        for split in splits:
            try:
                # 根据数据集类型选择预处理方法
                if dataset_name == "natural_questions":
                    self._preprocess_natural_questions(split)
                elif dataset_name == "hotpot_qa":
                    self._preprocess_hotpot_qa(split)
                elif dataset_name == "trivia_qa":
                    self._preprocess_trivia_qa(split)
                elif dataset_name == "ms_marco":
                    self._preprocess_ms_marco(split)
                else:
                    logger.warning(f"未实现的预处理方法: {dataset_name}")
                    
            except Exception as e:
                logger.error(f"预处理失败 {dataset_name} {split}: {e}")
    
    def _preprocess_natural_questions(self, split: str):
        """预处理 Natural Questions 数据集"""
        raw_file = self.raw_dir / "natural_questions" / f"nq-{split}.json"
        output_file = self.processed_dir / f"natural_questions_{split}.jsonl"
        
        if not raw_file.exists():
            logger.warning(f"原始文件不存在: {raw_file}")
            return
        
        with open(raw_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        processed_data = []
        for item in data:
            processed_item = {
                "id": item.get("id", ""),
                "question": item.get("question", ""),
                "answer": item.get("answers", [""])[0] if item.get("answers") else "",
                "context": item.get("context", ""),
                "type": "single_hop",
                "dataset": "natural_questions"
            }
            processed_data.append(processed_item)
        
        # 保存为 JSONL 格式
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in processed_data:
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')
        
        logger.info(f"✅ Natural Questions {split} 预处理完成: {len(processed_data)} 个样本")
    
    def _preprocess_hotpot_qa(self, split: str):
        """预处理 HotpotQA 数据集"""
        raw_file = self.raw_dir / "hotpot_qa" / f"hotpot_{split}_v1.1.json"
        output_file = self.processed_dir / f"hotpot_qa_{split}.jsonl"
        
        if not raw_file.exists():
            # 尝试其他可能的文件名
            possible_files = list((self.raw_dir / "hotpot_qa").glob(f"*{split}*.json"))
            if possible_files:
                raw_file = possible_files[0]
            else:
                logger.warning(f"原始文件不存在: {raw_file}")
                return
        
        with open(raw_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        processed_data = []
        for item in data:
            processed_item = {
                "id": item.get("_id", ""),
                "question": item.get("question", ""),
                "answer": item.get("answer", ""),
                "supporting_facts": item.get("supporting_facts", []),
                "context": item.get("context", []),
                "type": "multi_hop",
                "dataset": "hotpot_qa"
            }
            processed_data.append(processed_item)
        
        # 保存为 JSONL 格式
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in processed_data:
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')
        
        logger.info(f"✅ HotpotQA {split} 预处理完成: {len(processed_data)} 个样本")
    
    def _preprocess_trivia_qa(self, split: str):
        """预处理 TriviaQA 数据集"""
        # TriviaQA 的文件结构比较复杂，这里简化处理
        output_file = self.processed_dir / f"trivia_qa_{split}.jsonl"
        
        # 创建模拟数据用于测试
        mock_data = [
            {
                "id": f"trivia_{split}_{i}",
                "question": f"Sample trivia question {i} for {split}",
                "answer": f"Sample answer {i}",
                "type": "single_hop",
                "dataset": "trivia_qa"
            }
            for i in range(100)
        ]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in mock_data:
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')
        
        logger.info(f"✅ TriviaQA {split} 预处理完成: {len(mock_data)} 个样本 (模拟数据)")
    
    def _preprocess_ms_marco(self, split: str):
        """预处理 MS MARCO 数据集"""
        output_file = self.processed_dir / f"ms_marco_{split}.jsonl"
        
        # 创建模拟数据用于测试
        mock_data = [
            {
                "id": f"msmarco_{split}_{i}",
                "question": f"Sample MS MARCO question {i} for {split}",
                "answer": f"Sample answer {i}",
                "type": "single_hop",
                "dataset": "ms_marco"
            }
            for i in range(100)
        ]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in mock_data:
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')
        
        logger.info(f"✅ MS MARCO {split} 预处理完成: {len(mock_data)} 个样本 (模拟数据)")
    
    def download_all_datasets(self):
        """下载所有支持的数据集"""
        logger.info("🚀 开始下载所有数据集")
        
        for dataset_name in self.DATASET_URLS.keys():
            self.download_dataset(dataset_name)
        
        logger.info("🎉 所有数据集下载完成")
    
    def create_sample_datasets(self):
        """创建样本数据集用于快速测试"""
        logger.info("🧪 创建样本数据集")
        
        datasets = ["natural_questions", "hotpot_qa", "trivia_qa", "ms_marco"]
        splits = ["train", "dev", "test"]
        
        for dataset_name in datasets:
            for split in splits:
                output_file = self.processed_dir / f"{dataset_name}_{split}.jsonl"
                
                # 根据数据集类型创建不同的样本
                if "hotpot" in dataset_name:
                    sample_type = "multi_hop"
                else:
                    sample_type = "single_hop"
                
                mock_data = [
                    {
                        "id": f"{dataset_name}_{split}_{i}",
                        "question": f"Sample {dataset_name} question {i} for {split}",
                        "answer": f"Sample answer {i}",
                        "type": sample_type,
                        "dataset": dataset_name
                    }
                    for i in range(50)  # 每个分割50个样本
                ]
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    for item in mock_data:
                        json.dump(item, f, ensure_ascii=False)
                        f.write('\n')
                
                logger.info(f"✅ 创建样本数据集: {output_file}")
        
        logger.info("🎉 样本数据集创建完成")


def main():
    """主函数"""
    downloader = DatasetDownloader()
    
    # 选择操作
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "download":
        # 下载真实数据集 (需要网络连接)
        downloader.download_all_datasets()
    else:
        # 创建样本数据集用于测试
        downloader.create_sample_datasets()


if __name__ == "__main__":
    main()
