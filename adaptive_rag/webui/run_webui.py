#!/usr/bin/env python3
"""
智能自适应 RAG WebUI 启动器

简化的启动文件，用于快速启动 WebUI
"""

import argparse
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 导入原始接口文件（保持向后兼容）
from interface import create_ui, create_ui_with_real_config


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="启动智能自适应 RAG WebUI")
    parser.add_argument("--port", type=int, default=7860, help="服务端口")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="服务主机")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    parser.add_argument("--share", action="store_true", help="创建公共链接")
    parser.add_argument("--real-config", action="store_true", help="使用真实配置")
    parser.add_argument("--config-path", type=str, default="real_config.yaml", help="配置文件路径")

    args = parser.parse_args()

    print(f"🚀 启动智能自适应 RAG WebUI")
    print(f"📍 地址: http://{args.host}:{args.port}")
    print(f"🔧 调试模式: {args.debug}")
    print(f"⚙️ 使用真实配置: {args.real_config}")

    if args.real_config:
        print(f"📁 配置文件: {args.config_path}")
        demo = create_ui_with_real_config(args.config_path)
    else:
        demo = create_ui()

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
            print(f"❌ 端口 {args.port} 被占用")
            print(f"💡 尝试使用其他端口:")

            # 自动尝试其他端口
            for port in range(args.port + 1, args.port + 10):
                try:
                    print(f"🔄 尝试端口 {port}...")
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
                print(f"❌ 无法找到可用端口，请手动指定: python run_webui.py --port 8080")
        else:
            raise e


if __name__ == "__main__":
    main() 