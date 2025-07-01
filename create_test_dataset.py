#!/usr/bin/env python3
"""
=== 创建小型测试数据集 ===

创建一个小的 HotpotQA 风格的测试数据集用于验证 AdaptiveRAG
"""

import json
import logging
from pathlib import Path

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_hotpotqa_test_data():
    """创建小型 HotpotQA 测试数据"""
    
    # 创建测试数据目录
    test_data_dir = Path("/root/autodl-tmp/test_data")
    test_data_dir.mkdir(exist_ok=True)
    
    # HotpotQA 风格的测试数据
    hotpotqa_samples = [
        {
            "id": "hotpot_test_1",
            "question": "What is the capital of the country where the Eiffel Tower is located?",
            "golden_answers": ["Paris"],
            "type": "multi_hop",
            "metadata": {
                "dataset": "hotpotqa",
                "split": "test"
            }
        },
        {
            "id": "hotpot_test_2", 
            "question": "Who is the author of the book that features the character Sherlock Holmes?",
            "golden_answers": ["Arthur Conan Doyle", "Sir Arthur Conan Doyle"],
            "type": "multi_hop",
            "metadata": {
                "dataset": "hotpotqa",
                "split": "test"
            }
        },
        {
            "id": "hotpot_test_3",
            "question": "What is the programming language created by the founder of Python?",
            "golden_answers": ["Python"],
            "type": "multi_hop", 
            "metadata": {
                "dataset": "hotpotqa",
                "split": "test"
            }
        },
        {
            "id": "hotpot_test_4",
            "question": "In which year was the university founded where Albert Einstein taught?",
            "golden_answers": ["1754", "1754 (Columbia)", "1879 (Princeton)"],
            "type": "multi_hop",
            "metadata": {
                "dataset": "hotpotqa", 
                "split": "test"
            }
        },
        {
            "id": "hotpot_test_5",
            "question": "What is the largest city in the state where Microsoft headquarters is located?",
            "golden_answers": ["Seattle"],
            "type": "multi_hop",
            "metadata": {
                "dataset": "hotpotqa",
                "split": "test"
            }
        }
    ]
    
    # 保存测试数据
    output_file = test_data_dir / "hotpotqa_test.jsonl"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in hotpotqa_samples:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    logger.info(f"✅ 创建了 {len(hotpotqa_samples)} 条 HotpotQA 测试数据")
    logger.info(f"📁 保存到: {output_file}")
    
    return str(output_file)

def create_simple_corpus():
    """创建简单的知识库用于检索"""
    
    test_data_dir = Path("/root/autodl-tmp/test_data")
    
    # 简单的知识库文档
    corpus_docs = [
        {
            "id": "doc_1",
            "title": "Eiffel Tower",
            "contents": "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel."
        },
        {
            "id": "doc_2", 
            "title": "France",
            "contents": "France is a country in Western Europe. Its capital and largest city is Paris. France is known for its culture, cuisine, and landmarks like the Eiffel Tower."
        },
        {
            "id": "doc_3",
            "title": "Sherlock Holmes",
            "contents": "Sherlock Holmes is a fictional detective created by British author Sir Arthur Conan Doyle. The character first appeared in 1887."
        },
        {
            "id": "doc_4",
            "title": "Arthur Conan Doyle", 
            "contents": "Sir Arthur Conan Doyle was a British writer and physician. He is most famous for creating the character Sherlock Holmes."
        },
        {
            "id": "doc_5",
            "title": "Python Programming",
            "contents": "Python is a high-level programming language created by Guido van Rossum. It was first released in 1991."
        },
        {
            "id": "doc_6",
            "title": "Guido van Rossum",
            "contents": "Guido van Rossum is a Dutch programmer who created the Python programming language. He was Python's lead developer until 2018."
        },
        {
            "id": "doc_7",
            "title": "Albert Einstein",
            "contents": "Albert Einstein was a theoretical physicist. He taught at Princeton University and Columbia University during his career in America."
        },
        {
            "id": "doc_8",
            "title": "Princeton University", 
            "contents": "Princeton University is a private research university in Princeton, New Jersey. It was founded in 1746."
        },
        {
            "id": "doc_9",
            "title": "Microsoft Corporation",
            "contents": "Microsoft Corporation is an American technology company headquartered in Redmond, Washington. It was founded by Bill Gates and Paul Allen."
        },
        {
            "id": "doc_10",
            "title": "Washington State",
            "contents": "Washington is a state in the Pacific Northwest region of the United States. Its largest city is Seattle, and the capital is Olympia."
        }
    ]
    
    # 保存语料库
    corpus_file = test_data_dir / "test_corpus.jsonl"
    
    with open(corpus_file, 'w', encoding='utf-8') as f:
        for doc in corpus_docs:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    
    logger.info(f"✅ 创建了 {len(corpus_docs)} 条语料库文档")
    logger.info(f"📁 保存到: {corpus_file}")
    
    return str(corpus_file)

def main():
    """主函数"""
    logger.info("🎯 创建测试数据集")
    
    # 创建测试数据
    test_data_file = create_hotpotqa_test_data()
    corpus_file = create_simple_corpus()
    
    logger.info("✅ 测试数据集创建完成!")
    logger.info(f"📊 测试数据: {test_data_file}")
    logger.info(f"📚 语料库: {corpus_file}")

if __name__ == "__main__":
    main()
