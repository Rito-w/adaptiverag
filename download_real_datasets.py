#!/usr/bin/env python3
"""
=== 使用 FlashRAG 下载真实数据集 ===

下载标准的 QA 数据集用于 AdaptiveRAG 实验
"""

import os
import sys
import logging
from pathlib import Path
import json

# 添加 FlashRAG 路径
sys.path.insert(0, str(Path(__file__).parent.parent / "FlashRAG"))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def download_flashrag_datasets():
    """使用 FlashRAG 下载标准数据集"""
    try:
        from flashrag.config import Config
        from flashrag.dataset import Dataset
        import datasets
        
        logger.info("🚀 开始下载 FlashRAG 标准数据集")
        
        # 数据保存目录
        data_dir = Path("/root/autodl-tmp/flashrag_real_data")
        data_dir.mkdir(exist_ok=True)
        
        # 要下载的数据集（使用正确的名称）
        dataset_configs = {
            "hotpotqa": {
                "name": "hotpotqa",
                "hf_name": "RUC-NLPIR/FlashRAG_datasets",
                "subset": "hotpotqa"
            },
            "triviaqa": {
                "name": "triviaqa",
                "hf_name": "RUC-NLPIR/FlashRAG_datasets",
                "subset": "triviaqa"
            },
            "msmarco-qa": {
                "name": "msmarco-qa",
                "hf_name": "RUC-NLPIR/FlashRAG_datasets",
                "subset": "msmarco-qa"
            },
            "squad": {
                "name": "squad",
                "hf_name": "RUC-NLPIR/FlashRAG_datasets",
                "subset": "squad"
            }
        }
        
        for dataset_key, config in dataset_configs.items():
            logger.info(f"📊 下载数据集: {config['name']}")
            
            try:
                # 下载数据集
                dataset = datasets.load_dataset(
                    config["hf_name"], 
                    config["subset"],
                    cache_dir=str(data_dir / "cache")
                )
                
                # 保存为 JSONL 格式
                for split in ["train", "dev", "test"]:
                    if split in dataset:
                        output_file = data_dir / f"{config['name']}_{split}.jsonl"

                        logger.info(f"📝 处理 {split} 数据...")
                        items_written = 0

                        with open(output_file, 'w', encoding='utf-8') as f:
                            for i, item in enumerate(dataset[split]):
                                # 转换为标准格式
                                standard_item = {
                                    "id": item.get("id", f"{config['name']}_{split}_{i}"),
                                    "question": item.get("question", ""),
                                    "golden_answers": item.get("golden_answers", []),
                                    "metadata": {
                                        "dataset": config["name"],
                                        "split": split
                                    }
                                }
                                f.write(json.dumps(standard_item, ensure_ascii=False) + '\n')
                                items_written += 1

                        logger.info(f"✅ 保存 {items_written} 条 {split} 数据到: {output_file}")
                        
            except Exception as e:
                logger.error(f"❌ 下载 {config['name']} 失败: {e}")
                continue
        
        logger.info("🎉 所有数据集下载完成!")
        return str(data_dir)
        
    except ImportError as e:
        logger.error(f"❌ 导入 FlashRAG 失败: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ 下载数据集失败: {e}")
        return None

def download_huggingface_datasets():
    """直接从 Hugging Face 下载标准数据集"""
    try:
        import datasets
        
        logger.info("🚀 从 Hugging Face 下载标准数据集")
        
        # 数据保存目录
        data_dir = Path("/root/autodl-tmp/hf_real_data")
        data_dir.mkdir(exist_ok=True)
        
        # 标准数据集配置（避免大数据集）
        hf_datasets = {
            "squad": {
                "path": "squad",
                "name": None
            },
            "squad_v2": {
                "path": "squad_v2",
                "name": None
            }
        }
        
        for dataset_name, config in hf_datasets.items():
            logger.info(f"📊 下载数据集: {dataset_name}")
            
            try:
                # 下载数据集
                if config["name"]:
                    dataset = datasets.load_dataset(
                        config["path"], 
                        config["name"],
                        cache_dir=str(data_dir / "cache")
                    )
                else:
                    dataset = datasets.load_dataset(
                        config["path"],
                        cache_dir=str(data_dir / "cache")
                    )
                
                # 保存为 JSONL 格式
                for split_name, split_data in dataset.items():
                    output_file = data_dir / f"{dataset_name}_{split_name}.jsonl"
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        for i, item in enumerate(split_data):
                            # 转换为标准格式
                            if dataset_name == "natural_questions":
                                standard_item = {
                                    "id": item.get("id", f"nq_{split_name}_{i}"),
                                    "question": item.get("question", {}).get("text", ""),
                                    "golden_answers": [ans["text"] for ans in item.get("annotations", {}).get("short_answers", [])],
                                    "metadata": {
                                        "dataset": dataset_name,
                                        "split": split_name
                                    }
                                }
                            elif dataset_name == "squad":
                                standard_item = {
                                    "id": item.get("id", f"squad_{split_name}_{i}"),
                                    "question": item.get("question", ""),
                                    "golden_answers": [ans["text"] for ans in item.get("answers", {}).get("text", [])],
                                    "metadata": {
                                        "dataset": dataset_name,
                                        "split": split_name,
                                        "context": item.get("context", "")
                                    }
                                }
                            else:
                                # 通用格式
                                standard_item = {
                                    "id": f"{dataset_name}_{split_name}_{i}",
                                    "question": str(item.get("query", item.get("question", ""))),
                                    "golden_answers": item.get("answers", []),
                                    "metadata": {
                                        "dataset": dataset_name,
                                        "split": split_name,
                                        "original_item": item
                                    }
                                }
                            
                            f.write(json.dumps(standard_item, ensure_ascii=False) + '\n')
                    
                    logger.info(f"✅ 保存 {split_name} 数据到: {output_file}")
                    
            except Exception as e:
                logger.error(f"❌ 下载 {dataset_name} 失败: {e}")
                continue
        
        logger.info("🎉 Hugging Face 数据集下载完成!")
        return str(data_dir)
        
    except ImportError as e:
        logger.error(f"❌ 导入 datasets 库失败: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ 下载数据集失败: {e}")
        return None

def main():
    """主函数"""
    logger.info("🎯 开始下载真实数据集")

    # 启用学术加速
    logger.info("🚀 启用学术加速...")
    os.system("source /etc/network_turbo")

    # 首先尝试 FlashRAG 数据集
    flashrag_path = download_flashrag_datasets()

    # 然后尝试 Hugging Face 数据集
    hf_path = download_huggingface_datasets()
    
    if flashrag_path or hf_path:
        logger.info("✅ 数据集下载成功!")
        if flashrag_path:
            logger.info(f"📁 FlashRAG 数据路径: {flashrag_path}")
        if hf_path:
            logger.info(f"📁 Hugging Face 数据路径: {hf_path}")
    else:
        logger.error("❌ 所有数据集下载都失败了")

if __name__ == "__main__":
    main()
