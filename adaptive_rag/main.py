#!/usr/bin/env python3
"""
=== Adaptive RAG 主入口 ===

提供统一的入口点和命令行界面
"""

import argparse
import logging
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from adaptive_rag.config import create_flexrag_integrated_config, FLEXRAG_AVAILABLE
from adaptive_rag.webui.interface import create_ui


def setup_logging(level: str = "INFO"):
    """设置日志"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('adaptive_rag.log')
        ]
    )


def run_webui(args):
    """启动 Web UI"""
    print("🚀 启动 Adaptive RAG Web UI...")

    if FLEXRAG_AVAILABLE:
        print("✅ 使用 FlexRAG 深度集成模式")
    else:
        print("⚠️ FlexRAG 不可用，使用模拟实现")

    demo = create_ui()
    demo.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        debug=args.debug
    )


def run_flexrag_test(args):
    """运行 FlexRAG 集成测试"""
    print("🧪 运行 FlexRAG 深度集成测试...")

    from adaptive_rag.test_flexrag_integration import test_flexrag_integration, test_component_compatibility

    if args.component == "all":
        # 完整测试
        test_component_compatibility()
        test_flexrag_integration()
    else:
        # 特定组件测试
        print(f"🔍 测试组件: {args.component}")
        test_component_compatibility()

        # 这里可以添加特定组件的详细测试
        if args.component == "retriever":
            print("🔍 详细测试检索器组件...")
        elif args.component == "ranker":
            print("🎯 详细测试重排序器组件...")
        elif args.component == "generator":
            print("✨ 详细测试生成器组件...")
        elif args.component == "assistant":
            print("🤖 详细测试助手组件...")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Adaptive RAG - 智能自适应检索增强生成系统")

    # 全局参数
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])

    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # Web UI 命令
    webui_parser = subparsers.add_parser("webui", help="启动 Web UI")
    webui_parser.add_argument("--host", default="127.0.0.1", help="服务主机")
    webui_parser.add_argument("--port", type=int, default=7860, help="服务端口")
    webui_parser.add_argument("--share", action="store_true", help="创建公共链接")
    webui_parser.add_argument("--debug", action="store_true", help="调试模式")


    # FlexRAG 集成测试命令
    flexrag_test_parser = subparsers.add_parser("test-flexrag", help="测试 FlexRAG 深度集成")
    flexrag_test_parser.add_argument("--component", choices=["all", "retriever", "ranker", "generator", "assistant"],
                                   default="all", help="测试特定组件")

    args = parser.parse_args()

    # 设置日志
    setup_logging(args.log_level)

    # 执行命令
    if args.command == "webui":
        run_webui(args)
    elif args.command == "test-flexrag":
        run_flexrag_test(args)
    else:
        # 默认启动 Web UI
        print("🎯 未指定命令，启动 Web UI...")
        args.host = "127.0.0.1"
        args.port = 7860
        args.share = False
        args.debug = False
        run_webui(args)


if __name__ == "__main__":
    main()