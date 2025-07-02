#!/usr/bin/env python3
"""
=== 检查本地资源 ===

检查 /root/autodl-tmp 目录下的模型和数据资源
"""

import os
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_directory_structure():
    """检查目录结构"""
    print("🔍 检查 /root/autodl-tmp 目录结构")
    print("=" * 60)
    
    base_dir = Path("/root/autodl-tmp")
    if not base_dir.exists():
        print("❌ /root/autodl-tmp 目录不存在")
        return False
    
    # 检查主要目录
    directories = {
        "models": "模型目录",
        "flashrag_real_data": "FlashRAG数据目录",
        "adaptiverag_data": "AdaptiveRAG数据目录"
    }
    
    for dir_name, description in directories.items():
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"✅ {description}: {dir_path}")
            # 显示目录大小
            try:
                size = sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
                size_gb = size / (1024**3)
                print(f"   大小: {size_gb:.2f} GB")
            except Exception as e:
                print(f"   大小: 无法计算 ({e})")
        else:
            print(f"⚠️ {description}: {dir_path} (不存在)")
    
    return True


def check_models():
    """检查模型文件"""
    print("\n🤖 检查模型文件")
    print("=" * 60)
    
    models_dir = Path("/root/autodl-tmp/models")
    if not models_dir.exists():
        print("❌ 模型目录不存在")
        return False
    
    # 预期的模型
    expected_models = {
        "e5-base-v2": "嵌入模型",
        "bge-reranker-base": "重排序模型", 
        "Qwen2.5-1.5B-Instruct": "生成模型(小)",
        "Qwen2.5-7B-Instruct": "生成模型(大)",
        "Qwen1.5-1.8B-Chat": "对话模型"
    }
    
    found_models = []
    for model_name, description in expected_models.items():
        model_path = models_dir / model_name
        if model_path.exists():
            print(f"✅ {description}: {model_path}")
            
            # 检查关键文件
            key_files = ["config.json", "pytorch_model.bin", "tokenizer.json"]
            missing_files = []
            for file_name in key_files:
                if not (model_path / file_name).exists():
                    missing_files.append(file_name)
            
            if missing_files:
                print(f"   ⚠️ 缺少文件: {', '.join(missing_files)}")
            else:
                print(f"   ✅ 模型文件完整")
                found_models.append(model_name)
        else:
            print(f"❌ {description}: {model_path} (不存在)")
    
    print(f"\n📊 模型统计: 找到 {len(found_models)}/{len(expected_models)} 个模型")
    return len(found_models) > 0


def check_data():
    """检查数据文件"""
    print("\n📊 检查数据文件")
    print("=" * 60)
    
    data_dir = Path("/root/autodl-tmp/flashrag_real_data")
    if not data_dir.exists():
        print("❌ 数据目录不存在")
        return False
    
    # 预期的数据文件
    expected_data = {
        "hotpotqa_dev.jsonl": "HotpotQA开发集",
        "hotpotqa_train.jsonl": "HotpotQA训练集",
        "triviaqa_dev.jsonl": "TriviaQA开发集",
        "nq_dev.jsonl": "Natural Questions开发集"
    }
    
    found_data = []
    for file_name, description in expected_data.items():
        file_path = data_dir / file_name
        if file_path.exists():
            print(f"✅ {description}: {file_path}")
            
            # 检查文件大小和行数
            try:
                size_mb = file_path.stat().st_size / (1024**2)
                with open(file_path, 'r', encoding='utf-8') as f:
                    line_count = sum(1 for _ in f)
                print(f"   大小: {size_mb:.2f} MB, 行数: {line_count}")
                found_data.append(file_name)
            except Exception as e:
                print(f"   ⚠️ 读取失败: {e}")
        else:
            print(f"❌ {description}: {file_path} (不存在)")
    
    print(f"\n📊 数据统计: 找到 {len(found_data)}/{len(expected_data)} 个数据文件")
    return len(found_data) > 0


def check_sample_data():
    """检查数据样本"""
    print("\n🔍 检查数据样本")
    print("=" * 60)
    
    data_files = [
        "/root/autodl-tmp/flashrag_real_data/hotpotqa_dev.jsonl",
        "/root/autodl-tmp/flashrag_real_data/triviaqa_dev.jsonl"
    ]
    
    for file_path in data_files:
        if os.path.exists(file_path):
            print(f"\n📄 {os.path.basename(file_path)} 样本:")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f):
                        if i >= 2:  # 只显示前2个样本
                            break
                        data = json.loads(line.strip())
                        print(f"  样本 {i+1}:")
                        for key, value in list(data.items())[:3]:  # 只显示前3个字段
                            if isinstance(value, str) and len(value) > 100:
                                value = value[:100] + "..."
                            print(f"    {key}: {value}")
                        print()
            except Exception as e:
                print(f"  ❌ 读取失败: {e}")


def check_cache_directory():
    """检查缓存目录"""
    print("\n💾 检查缓存目录")
    print("=" * 60)
    
    cache_dir = Path("/root/autodl-tmp/flashrag_real_data/cache")
    if not cache_dir.exists():
        print(f"⚠️ 缓存目录不存在，将自动创建: {cache_dir}")
        try:
            cache_dir.mkdir(parents=True, exist_ok=True)
            print("✅ 缓存目录创建成功")
        except Exception as e:
            print(f"❌ 缓存目录创建失败: {e}")
            return False
    else:
        print(f"✅ 缓存目录存在: {cache_dir}")
    
    # 检查现有缓存文件
    cache_files = list(cache_dir.glob("*"))
    if cache_files:
        print(f"📁 现有缓存文件 ({len(cache_files)} 个):")
        for cache_file in cache_files[:5]:  # 只显示前5个
            size_mb = cache_file.stat().st_size / (1024**2)
            print(f"  - {cache_file.name}: {size_mb:.2f} MB")
        if len(cache_files) > 5:
            print(f"  ... 还有 {len(cache_files) - 5} 个文件")
    else:
        print("📁 缓存目录为空（首次运行时会自动生成）")
    
    return True


def generate_config_recommendation():
    """生成配置建议"""
    print("\n💡 配置建议")
    print("=" * 60)
    
    models_dir = Path("/root/autodl-tmp/models")
    data_dir = Path("/root/autodl-tmp/flashrag_real_data")
    
    # 检查可用的模型
    available_models = {}
    if (models_dir / "e5-base-v2").exists():
        available_models["embedding"] = "/root/autodl-tmp/models/e5-base-v2"
    if (models_dir / "bge-reranker-base").exists():
        available_models["reranker"] = "/root/autodl-tmp/models/bge-reranker-base"
    
    # 生成器模型优先级
    generator_options = [
        ("Qwen2.5-1.5B-Instruct", "推荐：平衡性能和速度"),
        ("Qwen1.5-1.8B-Chat", "备选：更快响应"),
        ("Qwen2.5-7B-Instruct", "高质量：需要更多显存")
    ]
    
    for model_name, description in generator_options:
        if (models_dir / model_name).exists():
            available_models["generator"] = f"/root/autodl-tmp/models/{model_name}"
            print(f"✅ 生成器: {model_name} ({description})")
            break
    
    # 检查可用的数据
    available_data = {}
    data_options = [
        ("hotpotqa_dev.jsonl", "推荐：多跳推理数据"),
        ("triviaqa_dev.jsonl", "备选：问答数据"),
        ("nq_dev.jsonl", "备选：自然问题")
    ]
    
    for file_name, description in data_options:
        if (data_dir / file_name).exists():
            available_data["corpus"] = f"/root/autodl-tmp/flashrag_real_data/{file_name}"
            print(f"✅ 数据集: {file_name} ({description})")
            break
    
    # 生成配置文件建议
    if available_models or available_data:
        print(f"\n📝 建议的配置 (adaptive_rag/config/modular_config.yaml):")
        print("```yaml")
        print("paths:")
        print("  models_dir: \"/root/autodl-tmp/models\"")
        print("  data_dir: \"/root/autodl-tmp\"")
        print("  flashrag_data_dir: \"/root/autodl-tmp/flashrag_real_data\"")
        print("  cache_dir: \"/root/autodl-tmp/flashrag_real_data/cache\"")
        print()
        if available_models.get("embedding"):
            print(f"retrievers:")
            print(f"  dense_retriever:")
            print(f"    model_name: \"{available_models['embedding']}\"")
        if available_models.get("generator"):
            print(f"generators:")
            print(f"  main_generator:")
            print(f"    model_name: \"{available_models['generator']}\"")
        if available_data.get("corpus"):
            print(f"data:")
            print(f"  corpus_path: \"{available_data['corpus']}\"")
        print("```")


def main():
    """主函数"""
    print("🔍 AdaptiveRAG 本地资源检查")
    print("=" * 80)
    
    # 检查目录结构
    if not check_directory_structure():
        return
    
    # 检查模型
    models_ok = check_models()
    
    # 检查数据
    data_ok = check_data()
    
    # 检查数据样本
    check_sample_data()
    
    # 检查缓存目录
    cache_ok = check_cache_directory()
    
    # 生成配置建议
    generate_config_recommendation()
    
    # 总结
    print(f"\n📊 检查结果总结")
    print("=" * 60)
    print(f"模型检查: {'✅ 通过' if models_ok else '❌ 失败'}")
    print(f"数据检查: {'✅ 通过' if data_ok else '❌ 失败'}")
    print(f"缓存检查: {'✅ 通过' if cache_ok else '❌ 失败'}")
    
    if models_ok and data_ok:
        print(f"\n🎉 资源检查完成！可以启动本地模型版本:")
        print(f"   python3 adaptiverag/launch_webui_with_module_control.py --port 7863 --host 0.0.0.0")
    else:
        print(f"\n⚠️ 部分资源缺失，系统将使用备用方案")
        print(f"   仍然可以启动，但可能使用在线模型或示例数据")


if __name__ == "__main__":
    main()
