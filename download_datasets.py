#!/usr/bin/env python3
"""
下载和准备实验数据集
"""

import os
import json
import logging
from pathlib import Path
from datasets import load_dataset
import torch

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据目录
DATA_DIR = "/root/autodl-tmp/adaptiverag_data"
os.makedirs(DATA_DIR, exist_ok=True)

def download_natural_questions():
    """下载Natural Questions数据集"""
    logger.info("📚 下载 Natural Questions 数据集...")
    
    try:
        # 下载验证集（较小，适合测试）
        dataset = load_dataset("natural_questions", split="validation[:1000]")
        
        # 转换为我们需要的格式
        processed_data = []
        for item in dataset:
            if item['annotations']['short_answers']:
                # 提取问题和答案
                question = item['question']['text']
                
                # 获取短答案
                short_answers = item['annotations']['short_answers'][0]
                if short_answers:
                    answer_start = short_answers[0]['start_token']
                    answer_end = short_answers[0]['end_token']
                    
                    # 从文档中提取答案文本
                    document_tokens = item['document']['tokens']
                    answer_tokens = document_tokens[answer_start:answer_end]
                    answer = ' '.join([token['token'] for token in answer_tokens])
                    
                    processed_data.append({
                        "question": question,
                        "answer": answer,
                        "context": ' '.join([token['token'] for token in document_tokens[:500]])  # 前500个token作为上下文
                    })
        
        # 保存处理后的数据
        output_file = Path(DATA_DIR) / "natural_questions.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Natural Questions 下载完成: {len(processed_data)} 条数据")
        logger.info(f"📁 保存位置: {output_file}")
        
        return len(processed_data)
        
    except Exception as e:
        logger.error(f"❌ Natural Questions 下载失败: {e}")
        return 0

def download_hotpot_qa():
    """下载HotpotQA数据集"""
    logger.info("📚 下载 HotpotQA 数据集...")
    
    try:
        # 下载验证集
        dataset = load_dataset("hotpot_qa", "distractor", split="validation[:500]")
        
        processed_data = []
        for item in dataset:
            question = item['question']
            answer = item['answer']
            
            # 合并所有上下文
            context_parts = []
            for title, sentences in zip(item['context']['title'], item['context']['sentences']):
                context_parts.append(f"{title}: {' '.join(sentences)}")
            
            context = ' '.join(context_parts)
            
            processed_data.append({
                "question": question,
                "answer": answer,
                "context": context[:2000]  # 限制上下文长度
            })
        
        # 保存数据
        output_file = Path(DATA_DIR) / "hotpot_qa.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ HotpotQA 下载完成: {len(processed_data)} 条数据")
        logger.info(f"📁 保存位置: {output_file}")
        
        return len(processed_data)
        
    except Exception as e:
        logger.error(f"❌ HotpotQA 下载失败: {e}")
        return 0

def download_squad():
    """下载SQuAD数据集作为备选"""
    logger.info("📚 下载 SQuAD 数据集...")
    
    try:
        dataset = load_dataset("squad", split="validation[:500]")
        
        processed_data = []
        for item in dataset:
            processed_data.append({
                "question": item['question'],
                "answer": item['answers']['text'][0] if item['answers']['text'] else "",
                "context": item['context']
            })
        
        output_file = Path(DATA_DIR) / "squad.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ SQuAD 下载完成: {len(processed_data)} 条数据")
        logger.info(f"📁 保存位置: {output_file}")
        
        return len(processed_data)
        
    except Exception as e:
        logger.error(f"❌ SQuAD 下载失败: {e}")
        return 0

def create_sample_dataset():
    """创建一个小样本数据集用于快速测试"""
    logger.info("📚 创建样本数据集...")
    
    sample_data = [
        {
            "question": "What is the capital of France?",
            "answer": "Paris",
            "context": "France is a country in Western Europe. Its capital and largest city is Paris, which is located in the north-central part of the country."
        },
        {
            "question": "Who wrote Romeo and Juliet?",
            "answer": "William Shakespeare",
            "context": "Romeo and Juliet is a tragedy written by William Shakespeare early in his career about two young star-crossed lovers whose deaths ultimately reconcile their feuding families."
        },
        {
            "question": "What is the largest planet in our solar system?",
            "answer": "Jupiter",
            "context": "Jupiter is the fifth planet from the Sun and the largest in the Solar System. It is a gas giant with a mass one-thousandth that of the Sun, but two-and-a-half times that of all the other planets in the Solar System combined."
        },
        {
            "question": "In which year did World War II end?",
            "answer": "1945",
            "context": "World War II ended in 1945 with the surrender of Germany in May and Japan in September following the atomic bombings of Hiroshima and Nagasaki."
        },
        {
            "question": "What is the chemical symbol for gold?",
            "answer": "Au",
            "context": "Gold is a chemical element with the symbol Au (from Latin: aurum) and atomic number 79, making it one of the higher atomic number elements that occur naturally."
        }
    ]
    
    output_file = Path(DATA_DIR) / "sample_qa.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✅ 样本数据集创建完成: {len(sample_data)} 条数据")
    logger.info(f"📁 保存位置: {output_file}")
    
    return len(sample_data)

def main():
    """主函数"""
    logger.info("🚀 开始下载数据集")
    logger.info(f"📁 数据目录: {DATA_DIR}")
    
    # 检查GPU
    if torch.cuda.is_available():
        logger.info(f"🎮 GPU可用: {torch.cuda.get_device_name(0)}")
    else:
        logger.warning("⚠️ GPU不可用，将使用CPU")
    
    total_downloaded = 0
    
    # 1. 创建样本数据集（快速测试用）
    total_downloaded += create_sample_dataset()
    
    # 2. 下载SQuAD（相对容易下载）
    total_downloaded += download_squad()
    
    # 3. 尝试下载Natural Questions
    total_downloaded += download_natural_questions()
    
    # 4. 尝试下载HotpotQA
    total_downloaded += download_hotpot_qa()
    
    # 总结
    logger.info("\n" + "="*60)
    logger.info("📊 数据集下载总结")
    logger.info("="*60)
    logger.info(f"📁 数据目录: {DATA_DIR}")
    logger.info(f"📈 总计下载: {total_downloaded} 条数据")
    
    # 列出所有下载的文件
    data_files = list(Path(DATA_DIR).glob("*.json"))
    logger.info(f"📄 数据文件: {len(data_files)} 个")
    for file in data_files:
        file_size = file.stat().st_size / 1024  # KB
        logger.info(f"  - {file.name}: {file_size:.1f} KB")
    
    if total_downloaded > 0:
        logger.info("✅ 数据集准备完成，可以开始实验！")
    else:
        logger.error("❌ 没有成功下载任何数据集")
    
    return total_downloaded > 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
