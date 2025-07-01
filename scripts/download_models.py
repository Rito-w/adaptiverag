#!/usr/bin/env python3
"""
=== 下载真实模型 ===

下载 AdaptiveRAG 需要的真实检索和生成模型
"""

import os
import sys
import logging
from pathlib import Path
import subprocess

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_mirror():
    """设置 Hugging Face 镜像加速"""
    logger.info("🚀 设置 Hugging Face 镜像加速...")
    
    # 设置环境变量
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
    
    # 设置 git 配置
    try:
        subprocess.run(["git", "config", "--global", "url.https://hf-mirror.com/.insteadOf", "https://huggingface.co/"], 
                      check=True, capture_output=True)
        logger.info("✅ Git 镜像配置成功")
    except subprocess.CalledProcessError as e:
        logger.warning(f"⚠️ Git 镜像配置失败: {e}")

def download_model_with_git(model_name: str, save_dir: str):
    """使用 git 下载模型"""
    model_dir = Path(save_dir) / model_name.split('/')[-1]
    
    if model_dir.exists():
        logger.info(f"📁 模型已存在: {model_dir}")
        return str(model_dir)
    
    logger.info(f"📥 下载模型: {model_name}")
    
    # 创建目录
    model_dir.parent.mkdir(parents=True, exist_ok=True)
    
    # 使用 git clone 下载
    repo_url = f"https://hf-mirror.com/{model_name}"
    
    try:
        # 使用 git clone 下载
        cmd = ["git", "clone", repo_url, str(model_dir)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            logger.info(f"✅ 模型下载成功: {model_dir}")
            return str(model_dir)
        else:
            logger.error(f"❌ Git clone 失败: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        logger.error(f"❌ 下载超时: {model_name}")
        return None
    except Exception as e:
        logger.error(f"❌ 下载失败: {e}")
        return None

def download_model_with_huggingface_hub(model_name: str, save_dir: str):
    """使用 huggingface_hub 下载模型"""
    try:
        from huggingface_hub import snapshot_download
        
        model_dir = Path(save_dir) / model_name.split('/')[-1]
        
        if model_dir.exists():
            logger.info(f"📁 模型已存在: {model_dir}")
            return str(model_dir)
        
        logger.info(f"📥 使用 huggingface_hub 下载: {model_name}")
        
        # 下载模型
        downloaded_path = snapshot_download(
            repo_id=model_name,
            cache_dir=save_dir,
            local_dir=str(model_dir),
            local_dir_use_symlinks=False
        )
        
        logger.info(f"✅ 模型下载成功: {downloaded_path}")
        return downloaded_path
        
    except ImportError:
        logger.warning("⚠️ huggingface_hub 未安装，尝试其他方法")
        return None
    except Exception as e:
        logger.error(f"❌ huggingface_hub 下载失败: {e}")
        return None

def download_model(model_name: str, save_dir: str):
    """下载模型（尝试多种方法）"""
    logger.info(f"🎯 开始下载模型: {model_name}")
    
    # 方法1: 使用 huggingface_hub
    result = download_model_with_huggingface_hub(model_name, save_dir)
    if result:
        return result
    
    # 方法2: 使用 git clone
    result = download_model_with_git(model_name, save_dir)
    if result:
        return result
    
    logger.error(f"❌ 所有下载方法都失败了: {model_name}")
    return None

def download_all_models():
    """下载所有需要的模型"""
    logger.info("🚀 开始下载 AdaptiveRAG 所需的模型")
    
    # 启用学术加速
    logger.info("🌐 启用学术加速...")
    os.system("source /etc/network_turbo")
    
    # 设置镜像
    setup_mirror()
    
    # 模型保存目录
    models_dir = Path("/root/autodl-tmp/models")
    models_dir.mkdir(exist_ok=True)
    
    # 需要下载的模型列表
    models_to_download = [
        {
            "name": "intfloat/e5-base-v2",
            "description": "E5 密集检索模型",
            "priority": "high"
        },
        {
            "name": "BAAI/bge-reranker-base", 
            "description": "BGE 重排序模型",
            "priority": "high"
        },
        {
            "name": "Qwen/Qwen1.5-1.8B-Chat",
            "description": "Qwen 1.5 生成模型",
            "priority": "medium"
        }
    ]
    
    # 下载结果
    download_results = {}
    
    for model_info in models_to_download:
        model_name = model_info["name"]
        description = model_info["description"]
        priority = model_info["priority"]
        
        logger.info(f"\n📦 下载 {description} ({model_name})")
        logger.info(f"🔥 优先级: {priority}")
        
        try:
            result = download_model(model_name, str(models_dir))
            download_results[model_name] = {
                "success": result is not None,
                "path": result,
                "description": description
            }
            
            if result:
                logger.info(f"✅ {description} 下载成功")
            else:
                logger.error(f"❌ {description} 下载失败")
                
        except Exception as e:
            logger.error(f"❌ {description} 下载异常: {e}")
            download_results[model_name] = {
                "success": False,
                "path": None,
                "description": description,
                "error": str(e)
            }
    
    # 汇总结果
    logger.info("\n📊 下载结果汇总:")
    success_count = 0
    total_count = len(models_to_download)
    
    for model_name, result in download_results.items():
        status = "✅" if result["success"] else "❌"
        logger.info(f"   {status} {result['description']}: {model_name}")
        if result["success"]:
            logger.info(f"      📁 路径: {result['path']}")
            success_count += 1
        elif "error" in result:
            logger.info(f"      ❌ 错误: {result['error']}")
    
    logger.info(f"\n🎯 下载完成: {success_count}/{total_count} 成功")
    
    if success_count > 0:
        logger.info("✅ 至少有一些模型下载成功，可以开始实验")
    else:
        logger.error("❌ 所有模型下载都失败了")
    
    return download_results

def install_dependencies():
    """安装必要的依赖"""
    logger.info("📦 安装必要的依赖...")
    
    dependencies = [
        "huggingface_hub",
        "sentence-transformers",
        "transformers",
        "torch",
        "faiss-cpu"
    ]
    
    for dep in dependencies:
        try:
            logger.info(f"📥 安装 {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                          check=True, capture_output=True)
            logger.info(f"✅ {dep} 安装成功")
        except subprocess.CalledProcessError as e:
            logger.warning(f"⚠️ {dep} 安装失败: {e}")

def main():
    """主函数"""
    logger.info("🎯 AdaptiveRAG 模型下载器")
    
    # 安装依赖
    install_dependencies()
    
    # 下载模型
    results = download_all_models()
    
    # 生成配置更新建议
    logger.info("\n📝 配置文件更新建议:")
    logger.info("请在 real_config.yaml 中更新以下路径:")
    
    for model_name, result in results.items():
        if result["success"]:
            model_key = model_name.split('/')[-1]
            logger.info(f"   {model_key}: {result['path']}")

if __name__ == "__main__":
    main()
