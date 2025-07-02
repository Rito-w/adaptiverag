#!/usr/bin/env python3
"""
=== 智能自适应 RAG WebUI 统一启动脚本 ===

功能特性：
1. 自动配置网络代理（AutoDL学术加速）
2. 支持多种启动模式（基础版、真实配置版）
3. 自动端口检测和重试
4. 详细的启动日志和状态显示

使用方法：
python run_webui.py --mode basic          # 基础模式
python run_webui.py --mode real-config    # 真实配置模式
python run_webui.py --port 8080          # 指定端口
python run_webui.py --share              # 创建公共链接
"""

import os
import sys
import time
import subprocess
import argparse
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def setup_network_proxy():
    """自动配置网络代理"""
    print("🌐 配置网络代理...")
    
    # 检查是否在AutoDL环境中
    if os.path.exists("/etc/network_turbo"):
        try:
            # 启用AutoDL学术加速
            result = subprocess.run(
                ["source", "/etc/network_turbo"],
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✅ AutoDL学术加速已启用")
            else:
                print("⚠️ AutoDL学术加速启用失败，尝试手动设置环境变量")
        except Exception as e:
            print(f"⚠️ 启用AutoDL学术加速时出错: {e}")
    
    # 设置环境变量
    proxy_env_vars = {
        'HTTP_PROXY': 'http://127.0.0.1:7890',
        'HTTPS_PROXY': 'http://127.0.0.1:7890',
        'http_proxy': 'http://127.0.0.1:7890',
        'https_proxy': 'http://127.0.0.1:7890',
        'ALL_PROXY': 'socks5://127.0.0.1:7890',
        'all_proxy': 'socks5://127.0.0.1:7890'
    }
    
    # 检查代理是否可用
    for var, value in proxy_env_vars.items():
        if not os.environ.get(var):
            os.environ[var] = value
            print(f"🔧 设置环境变量: {var}={value}")
    
    # 设置HuggingFace相关环境变量
    hf_vars = {
        'HF_ENDPOINT': 'https://hf-mirror.com',
        'HF_HUB_ENABLE_HF_TRANSFER': '1',
        'HF_HUB_DISABLE_TELEMETRY': '1'
    }
    
    for var, value in hf_vars.items():
        if not os.environ.get(var):
            os.environ[var] = value
            print(f"🔧 设置HuggingFace环境变量: {var}={value}")
    
    print("✅ 网络代理配置完成")

def check_dependencies():
    """检查依赖项"""
    print("🔍 检查依赖项...")
    
    required_packages = [
        'gradio',
        'torch',
        'transformers',
        'sentence_transformers',
        'faiss',
        'numpy',
        'pandas',
        'yaml'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖项: {', '.join(missing_packages)}")
        print("💡 请运行: pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖项已安装")
    return True

def check_config_files():
    """检查配置文件"""
    print("📁 检查配置文件...")
    
    config_files = [
        "real_config.yaml",
        "real_config_enhanced.yaml"
    ]
    
    missing_files = []
    for config_file in config_files:
        if not os.path.exists(config_file):
            missing_files.append(config_file)
    
    if missing_files:
        print(f"⚠️ 缺少配置文件: {', '.join(missing_files)}")
        print("💡 将使用默认配置")
    else:
        print("✅ 配置文件检查完成")
    
    return True

def find_available_port(start_port=7860, max_attempts=10):
    """查找可用端口"""
    import socket
    
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    
    return None

def launch_webui(mode='basic', port=7860, host='0.0.0.0', share=False, debug=False):
    """启动WebUI"""
    print(f"🚀 启动WebUI - 模式: {mode}")
    print(f"📍 地址: http://{host}:{port}")
    print(f"🔧 调试模式: {debug}")
    print(f"🌐 公共链接: {share}")
    
    try:
        # 导入WebUI模块
        from adaptive_rag.webui.interface import create_ui, create_ui_with_real_config
        
        # 根据模式选择UI
        if mode == 'real-config':
            print("📋 使用真实配置模式")
            demo = create_ui_with_real_config("real_config_enhanced.yaml")
        else:
            print("📋 使用基础模式")
            demo = create_ui()
        
        # 启动WebUI
        demo.launch(
            server_name=host,
            server_port=port,
            share=share,
            debug=debug,
            show_error=True,
            quiet=False
        )
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="智能自适应 RAG WebUI 启动脚本")
    parser.add_argument("--mode", type=str, default="basic", 
                       choices=["basic", "real-config"],
                       help="启动模式: basic(基础模式) 或 real-config(真实配置模式)")
    parser.add_argument("--port", type=int, default=7860, help="服务端口")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="服务主机")
    parser.add_argument("--share", action="store_true", help="创建公共链接")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    parser.add_argument("--no-proxy", action="store_true", help="不配置代理")
    parser.add_argument("--check-only", action="store_true", help="仅检查环境，不启动")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🧠 智能自适应 RAG WebUI 启动器")
    print("=" * 60)
    
    # 检查依赖项
    if not check_dependencies():
        sys.exit(1)
    
    # 检查配置文件
    check_config_files()
    
    # 配置网络代理
    if not args.no_proxy:
        setup_network_proxy()
    
    # 仅检查模式
    if args.check_only:
        print("✅ 环境检查完成")
        return
    
    # 查找可用端口
    available_port = find_available_port(args.port)
    if available_port is None:
        print(f"❌ 无法找到可用端口 (尝试范围: {args.port}-{args.port+9})")
        sys.exit(1)
    
    if available_port != args.port:
        print(f"⚠️ 端口 {args.port} 被占用，使用端口 {available_port}")
        args.port = available_port
    
    # 启动WebUI
    print("\n" + "=" * 60)
    success = launch_webui(
        mode=args.mode,
        port=args.port,
        host=args.host,
        share=args.share,
        debug=args.debug
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 