#!/usr/bin/env python3
"""
=== 安装真实模型依赖 ===

安装运行真实模型所需的依赖包
"""

import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def install_package(package_name: str, pip_name: str = None):
    """安装Python包"""
    if pip_name is None:
        pip_name = package_name
    
    try:
        __import__(package_name)
        logger.info(f"✅ {package_name} 已安装")
        return True
    except ImportError:
        logger.info(f"📦 正在安装 {pip_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
            logger.info(f"✅ {pip_name} 安装成功")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ {pip_name} 安装失败: {e}")
            return False


def main():
    """主函数"""
    logger.info("🚀 开始安装真实模型依赖...")
    
    # 必需的包列表
    packages = [
        ("torch", "torch"),
        ("transformers", "transformers"),
        ("sentence_transformers", "sentence-transformers"),
        ("rank_bm25", "rank-bm25"),
        ("sklearn", "scikit-learn"),
        ("numpy", "numpy"),
        ("gradio", "gradio"),
    ]
    
    success_count = 0
    total_count = len(packages)
    
    for package_name, pip_name in packages:
        if install_package(package_name, pip_name):
            success_count += 1
    
    logger.info(f"\n📊 安装结果: {success_count}/{total_count} 个包安装成功")
    
    if success_count == total_count:
        logger.info("🎉 所有依赖安装完成！")
        logger.info("\n💡 现在可以运行真实模型版本的WebUI:")
        logger.info("   python3 adaptiverag/launch_webui_with_module_control.py --port 7863 --host 0.0.0.0")
    else:
        logger.warning("⚠️ 部分依赖安装失败，可能影响真实模型功能")
        logger.info("💡 您仍然可以使用模拟版本的功能")


if __name__ == "__main__":
    main()
