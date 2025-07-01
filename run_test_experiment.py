#!/usr/bin/env python3
"""
=== AdaptiveRAG 测试实验 ===

在小型 HotpotQA 数据集上测试 AdaptiveRAG 的性能
"""

import sys
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Any

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_test_data():
    """加载测试数据"""
    test_file = Path("/root/autodl-tmp/test_data/hotpotqa_test.jsonl")
    
    if not test_file.exists():
        logger.error(f"测试数据文件不存在: {test_file}")
        return []
    
    test_data = []
    with open(test_file, 'r', encoding='utf-8') as f:
        for line in f:
            test_data.append(json.loads(line.strip()))
    
    logger.info(f"📊 加载了 {len(test_data)} 条测试数据")
    return test_data

def load_corpus():
    """加载语料库"""
    corpus_file = Path("/root/autodl-tmp/test_data/test_corpus.jsonl")
    
    if not corpus_file.exists():
        logger.error(f"语料库文件不存在: {corpus_file}")
        return []
    
    corpus = []
    with open(corpus_file, 'r', encoding='utf-8') as f:
        for line in f:
            corpus.append(json.loads(line.strip()))
    
    logger.info(f"📚 加载了 {len(corpus)} 条语料库文档")
    return corpus

def simple_keyword_retrieval(query: str, corpus: List[Dict], top_k: int = 3) -> List[Dict]:
    """简单的关键词检索"""
    query_words = set(query.lower().split())
    
    # 计算每个文档的相关性分数
    scored_docs = []
    for doc in corpus:
        content = (doc.get('title', '') + ' ' + doc.get('contents', '')).lower()
        content_words = set(content.split())
        
        # 简单的词重叠分数
        overlap = len(query_words.intersection(content_words))
        if overlap > 0:
            scored_docs.append((overlap, doc))
    
    # 按分数排序并返回top_k
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored_docs[:top_k]]

def simple_rag_baseline(question: str, corpus: List[Dict]) -> Dict[str, Any]:
    """简单的 RAG 基线方法"""
    start_time = time.time()
    
    # 检索相关文档
    retrieved_docs = simple_keyword_retrieval(question, corpus, top_k=3)
    retrieval_time = time.time() - start_time
    
    # 简单的答案生成（基于规则）
    gen_start = time.time()
    
    # 合并检索到的文档内容
    context = " ".join([doc.get('contents', '') for doc in retrieved_docs])
    
    # 简单的答案提取逻辑
    answer = "Based on the retrieved information: " + context[:100] + "..."
    
    generation_time = time.time() - gen_start
    total_time = time.time() - start_time
    
    return {
        "answer": answer,
        "retrieved_docs": retrieved_docs,
        "retrieval_time": retrieval_time,
        "generation_time": generation_time,
        "total_time": total_time,
        "method": "simple_rag"
    }

def adaptive_rag_method(question: str, corpus: List[Dict]) -> Dict[str, Any]:
    """AdaptiveRAG 方法（简化版）"""
    start_time = time.time()
    
    # 第一步：查询分析
    analysis_start = time.time()
    
    # 简单的查询复杂度分析
    query_words = question.lower().split()
    complexity_score = min(len(query_words) / 10.0, 1.0)  # 基于长度的复杂度
    
    # 检测是否是多跳查询
    multi_hop_indicators = ['where', 'who', 'what', 'when', 'which', 'author', 'creator', 'founder']
    is_multi_hop = any(indicator in question.lower() for indicator in multi_hop_indicators)
    
    analysis_time = time.time() - analysis_start
    
    # 第二步：自适应检索策略
    retrieval_start = time.time()
    
    if is_multi_hop and complexity_score > 0.5:
        # 复杂查询：使用更多文档
        top_k = 5
        logger.info(f"🧠 检测到复杂多跳查询，使用扩展检索 (top_k={top_k})")
    else:
        # 简单查询：使用较少文档
        top_k = 3
        logger.info(f"🔍 检测到简单查询，使用标准检索 (top_k={top_k})")
    
    retrieved_docs = simple_keyword_retrieval(question, corpus, top_k=top_k)
    retrieval_time = time.time() - retrieval_start
    
    # 第三步：自适应生成
    gen_start = time.time()
    
    # 根据查询类型调整生成策略
    context = " ".join([doc.get('contents', '') for doc in retrieved_docs])
    
    if is_multi_hop:
        answer = f"Multi-hop reasoning result: {context[:150]}..."
    else:
        answer = f"Direct answer: {context[:100]}..."
    
    generation_time = time.time() - gen_start
    total_time = time.time() - start_time
    
    return {
        "answer": answer,
        "retrieved_docs": retrieved_docs,
        "query_analysis": {
            "complexity_score": complexity_score,
            "is_multi_hop": is_multi_hop,
            "analysis_time": analysis_time
        },
        "retrieval_time": retrieval_time,
        "generation_time": generation_time,
        "total_time": total_time,
        "method": "adaptive_rag"
    }

def evaluate_answer(predicted: str, golden_answers: List[str]) -> Dict[str, float]:
    """简单的答案评估"""
    predicted_lower = predicted.lower()
    
    # 检查是否包含任何正确答案
    exact_match = 0.0
    for golden in golden_answers:
        if golden.lower() in predicted_lower:
            exact_match = 1.0
            break
    
    # 简单的F1计算（基于词重叠）
    pred_words = set(predicted_lower.split())
    best_f1 = 0.0
    
    for golden in golden_answers:
        golden_words = set(golden.lower().split())
        if len(golden_words) == 0:
            continue
            
        overlap = len(pred_words.intersection(golden_words))
        precision = overlap / len(pred_words) if len(pred_words) > 0 else 0.0
        recall = overlap / len(golden_words) if len(golden_words) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        
        best_f1 = max(best_f1, f1)
    
    return {
        "exact_match": exact_match,
        "f1_score": best_f1
    }

def run_experiment():
    """运行实验"""
    logger.info("🚀 开始 AdaptiveRAG 测试实验")
    
    # 加载数据
    test_data = load_test_data()
    corpus = load_corpus()
    
    if not test_data or not corpus:
        logger.error("❌ 数据加载失败")
        return
    
    # 实验结果
    results = {
        "simple_rag": {"predictions": [], "metrics": []},
        "adaptive_rag": {"predictions": [], "metrics": []}
    }
    
    # 对每个测试样本运行两种方法
    for i, item in enumerate(test_data):
        question = item["question"]
        golden_answers = item["golden_answers"]
        
        logger.info(f"\n📝 测试样本 {i+1}/{len(test_data)}: {question}")
        
        # 简单RAG基线
        logger.info("🔍 运行简单RAG基线...")
        simple_result = simple_rag_baseline(question, corpus)
        simple_metrics = evaluate_answer(simple_result["answer"], golden_answers)
        
        results["simple_rag"]["predictions"].append(simple_result)
        results["simple_rag"]["metrics"].append(simple_metrics)
        
        logger.info(f"   📊 简单RAG - EM: {simple_metrics['exact_match']:.3f}, F1: {simple_metrics['f1_score']:.3f}")
        
        # AdaptiveRAG
        logger.info("🧠 运行AdaptiveRAG...")
        adaptive_result = adaptive_rag_method(question, corpus)
        adaptive_metrics = evaluate_answer(adaptive_result["answer"], golden_answers)
        
        results["adaptive_rag"]["predictions"].append(adaptive_result)
        results["adaptive_rag"]["metrics"].append(adaptive_metrics)
        
        logger.info(f"   📊 AdaptiveRAG - EM: {adaptive_metrics['exact_match']:.3f}, F1: {adaptive_metrics['f1_score']:.3f}")
    
    # 计算平均指标
    logger.info("\n📈 实验结果汇总:")
    
    for method_name, method_results in results.items():
        metrics = method_results["metrics"]
        avg_em = sum(m["exact_match"] for m in metrics) / len(metrics)
        avg_f1 = sum(m["f1_score"] for m in metrics) / len(metrics)
        avg_time = sum(p["total_time"] for p in method_results["predictions"]) / len(method_results["predictions"])
        
        logger.info(f"\n🎯 {method_name.upper()}:")
        logger.info(f"   📊 平均 EM: {avg_em:.3f}")
        logger.info(f"   📊 平均 F1: {avg_f1:.3f}")
        logger.info(f"   ⏱️  平均时间: {avg_time:.3f}s")
    
    # 保存结果
    output_dir = Path("/root/autodl-tmp/test_results")
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "experiment_results.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    logger.info(f"\n✅ 实验完成！结果保存到: {output_dir / 'experiment_results.json'}")

def main():
    """主函数"""
    run_experiment()

if __name__ == "__main__":
    main()
