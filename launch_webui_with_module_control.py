#!/usr/bin/env python3
"""
=== 启动带模块控制的 WebUI ===

启动集成了模块控制功能的 AdaptiveRAG WebUI
"""

import sys
import argparse
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from adaptive_rag.webui.enhanced_main_interface import create_enhanced_interface


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="启动 AdaptiveRAG WebUI (带模块控制)")
    parser.add_argument("--port", type=int, default=7863, help="端口号")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="主机地址")
    parser.add_argument("--config-path", type=str, 
                       default="adaptiverag/configs/real_config_enhanced.yaml", 
                       help="配置文件路径")
    parser.add_argument("--share", action="store_true", help="创建公共链接")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    
    args = parser.parse_args()
    
    print("🚀 启动 AdaptiveRAG WebUI (增强版 - 带模块控制)")
    print("=" * 80)
    print(f"📋 配置文件: {args.config_path}")
    print(f"🌐 服务地址: http://{args.host}:{args.port}")
    print(f"🔧 调试模式: {'开启' if args.debug else '关闭'}")
    print(f"🌍 公共分享: {'开启' if args.share else '关闭'}")
    print("=" * 80)
    
    try:
        # 创建界面
        print("🎨 创建 WebUI 界面...")
        demo = create_enhanced_interface(args.config_path)
        print("✅ 界面创建成功")
        
        # 启动服务
        print("🚀 启动 Gradio 服务...")
        print("\n💡 新功能亮点:")
        print("   🎛️ 模块控制 - 实时开启/关闭各个功能模块")
        print("   🔬 真实模型 - 使用真实的检索器、重排序器和生成器")
        print("   📊 资源监控 - 实时监控系统资源使用情况")
        print("   ⚡ 性能优化 - 多维度性能优化和策略调整")
        print("   🔧 配置管理 - 支持预设模式和自定义配置")
        print("\n🎯 使用建议:")
        print("   1. 首先访问 '🎛️ 模块控制' 标签页配置所需模块")
        print("   2. 选择合适的预设模式或自定义配置")
        print("   3. 在 '🔬 真实模型测试' 标签页中体验真实效果")
        print("   4. 对比不同模块组合的实际差异")
        print("   5. 通过 '📊 资源监控' 观察系统性能")
        print("\n🔍 模块效果对比:")
        print("   • 关键词检索 vs 密集检索 - 看到不同检索策略的效果")
        print("   • 启用/禁用重排序 - 观察结果质量的变化")
        print("   • 完整流程 vs 简化流程 - 体验处理深度的差异")
        
        print(f"\n🌐 访问地址: http://localhost:{args.port}")
        print("   按 Ctrl+C 停止服务")
        print("=" * 80)
        
        demo.launch(
            server_name=args.host,
            server_port=args.port,
            share=args.share,
            debug=args.debug,
            show_error=True
        )
        
    except KeyboardInterrupt:
        print("\n👋 用户中断，正在关闭服务...")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
