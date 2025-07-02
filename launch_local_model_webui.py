#!/usr/bin/env python3
"""
=== 启动本地模型 WebUI ===

专门启动使用 /root/autodl-tmp 下模型和数据的 AdaptiveRAG WebUI
"""

import sys
import argparse
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def check_resources():
    """检查本地资源"""
    print("🔍 检查本地资源...")
    
    # 检查关键目录
    required_dirs = [
        "/root/autodl-tmp",
        "/root/autodl-tmp/models", 
        "/root/autodl-tmp/flashrag_real_data"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print("❌ 缺少必要目录:")
        for dir_path in missing_dirs:
            print(f"   {dir_path}")
        return False
    
    # 检查关键模型
    model_checks = [
        ("/root/autodl-tmp/models/e5-base-v2", "嵌入模型"),
        ("/root/autodl-tmp/models/Qwen2.5-1.5B-Instruct", "生成模型"),
        ("/root/autodl-tmp/models/Qwen1.5-1.8B-Chat", "备用生成模型")
    ]
    
    found_models = 0
    for model_path, description in model_checks:
        if os.path.exists(model_path):
            print(f"✅ {description}: {model_path}")
            found_models += 1
        else:
            print(f"⚠️ {description}: {model_path} (不存在)")
    
    # 检查数据文件
    data_checks = [
        ("/root/autodl-tmp/flashrag_real_data/hotpotqa_dev.jsonl", "HotpotQA数据"),
        ("/root/autodl-tmp/flashrag_real_data/triviaqa_dev.jsonl", "TriviaQA数据")
    ]
    
    found_data = 0
    for data_path, description in data_checks:
        if os.path.exists(data_path):
            print(f"✅ {description}: {data_path}")
            found_data += 1
        else:
            print(f"⚠️ {description}: {data_path} (不存在)")
    
    print(f"\n📊 资源统计:")
    print(f"   模型: {found_models}/{len(model_checks)}")
    print(f"   数据: {found_data}/{len(data_checks)}")
    
    return found_models > 0 or found_data > 0


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="启动 AdaptiveRAG 本地模型 WebUI")
    parser.add_argument("--port", type=int, default=7863, help="端口号")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="主机地址")
    parser.add_argument("--share", action="store_true", help="创建公共链接")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    parser.add_argument("--skip-check", action="store_true", help="跳过资源检查")
    
    args = parser.parse_args()
    
    print("🏠 启动 AdaptiveRAG 本地模型 WebUI")
    print("=" * 80)
    print(f"📋 使用本地资源: /root/autodl-tmp")
    print(f"🌐 服务地址: http://{args.host}:{args.port}")
    print(f"🔧 调试模式: {'开启' if args.debug else '关闭'}")
    print(f"🌍 公共分享: {'开启' if args.share else '关闭'}")
    print("=" * 80)
    
    # 检查资源（除非跳过）
    if not args.skip_check:
        if not check_resources():
            print("\n❌ 资源检查失败！")
            print("💡 建议:")
            print("   1. 运行资源检查: python3 adaptiverag/check_local_resources.py")
            print("   2. 确保模型和数据在正确位置")
            print("   3. 或使用 --skip-check 强制启动")
            return
        print("✅ 资源检查通过")
    else:
        print("⏭️ 跳过资源检查")
    
    try:
        # 导入并创建界面
        print("\n🎨 创建 WebUI 界面...")
        from adaptive_rag.webui.enhanced_main_interface import create_enhanced_interface
        
        # 使用本地模型配置
        config_path = "adaptive_rag/config/modular_config.yaml"
        demo = create_enhanced_interface(config_path)
        print("✅ 界面创建成功")
        
        # 启动服务
        print("🚀 启动 Gradio 服务...")
        print("\n💡 本地模型版本特色:")
        print("   🏠 使用您的本地Qwen模型进行生成")
        print("   🔍 使用您的本地E5模型进行嵌入检索")
        print("   📊 使用您的真实数据集 (HotpotQA/TriviaQA)")
        print("   🎛️ 模块开关产生真实的效果差异")
        print("   💾 自动缓存索引，加速后续使用")
        
        print("\n🎯 使用建议:")
        print("   1. 访问 '🎛️ 模块控制' 标签页配置模块")
        print("   2. 在 '🔬 真实模型测试' 标签页体验效果")
        print("   3. 对比不同模块组合的实际差异")
        print("   4. 观察本地模型的真实性能")
        
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
        print("\n🔧 故障排除:")
        print("   1. 检查依赖安装: python3 adaptiverag/install_real_model_deps.py")
        print("   2. 检查资源状态: python3 adaptiverag/check_local_resources.py")
        print("   3. 检查CUDA可用性: python3 -c 'import torch; print(torch.cuda.is_available())'")
        print("   4. 查看详细错误信息，启用调试模式: --debug")
        
        if args.debug:
            import traceback
            traceback.print_exc()
        
        sys.exit(1)


if __name__ == "__main__":
    main()
