#!/usr/bin/env python3
"""
=== 增强版 WebUI 启动脚本 ===

启动集成资源感知优化的完整 WebUI
"""

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 导入增强版主界面
from adaptive_rag.webui.enhanced_main_interface import create_enhanced_interface
import gradio as gr
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="启动增强版 AdaptiveRAG WebUI")
    parser.add_argument("--port", type=int, default=7863, help="服务端口")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="服务主机")
    parser.add_argument("--config-path", type=str, default="real_config.yaml", help="配置文件路径")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    parser.add_argument("--share", action="store_true", help="创建公共链接")

    args = parser.parse_args()

    logger.info("🚀 启动增强版 AdaptiveRAG WebUI")
    logger.info(f"📍 地址: http://{args.host}:{args.port}")
    logger.info(f"📁 配置文件: {args.config_path}")
    logger.info(f"🔧 调试模式: {args.debug}")

    # 检查配置文件
    config_path = Path(args.config_path)
    if not config_path.exists():
        logger.error(f"❌ 配置文件不存在: {args.config_path}")
        return

    # 创建并启动 WebUI
    demo = create_enhanced_interface(str(config_path))

    try:
        demo.launch(
            server_name=args.host,
            server_port=args.port,
            share=args.share,
            debug=args.debug,
            show_error=True,
            quiet=False
        )
    except OSError as e:
        if "Cannot find empty port" in str(e):
            logger.error(f"❌ 端口 {args.port} 被占用")
            logger.info(f"💡 尝试使用其他端口:")

            # 自动尝试其他端口
            for port in range(args.port + 1, args.port + 10):
                try:
                    logger.info(f"🔄 尝试端口 {port}...")
                    demo.launch(
                        server_name=args.host,
                        server_port=port,
                        share=args.share,
                        debug=args.debug,
                        show_error=True,
                        quiet=False
                    )
                    break
                except OSError:
                    continue
            else:
                logger.error(f"❌ 无法找到可用端口，请手动指定端口")
        else:
            raise e


if __name__ == "__main__":
    main() 