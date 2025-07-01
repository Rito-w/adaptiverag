#!/usr/bin/env python3
"""
=== 快速启动脚本 ===

用于快速启动和测试WebUI，包含自动代理配置
"""

import os
import sys
import subprocess
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def setup_proxy():
    """快速设置代理"""
    print("🌐 设置网络代理...")
    
    # AutoDL学术加速
    if os.path.exists("/etc/network_turbo"):
        try:
            subprocess.run("source /etc/network_turbo", shell=True, check=True)
            print("✅ AutoDL学术加速已启用")
        except:
            print("⚠️ AutoDL学术加速启用失败")
    
    # 设置环境变量
    os.environ.setdefault('HF_ENDPOINT', 'https://hf-mirror.com')
    os.environ.setdefault('HF_HUB_ENABLE_HF_TRANSFER', '1')
    print("✅ 代理配置完成")

def main():
    """主函数"""
    print("🚀 快速启动智能自适应 RAG WebUI")
    
    # 设置代理
    setup_proxy()
    
    # 导入并启动
    try:
        from adaptive_rag.webui.interface import create_ui_with_real_config
        
        print("📋 使用真实配置模式启动...")
        demo = create_ui_with_real_config("real_config_enhanced.yaml")
        
        print("🌐 启动WebUI...")
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            debug=True,
            show_error=True
        )
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("💡 尝试基础模式...")
        
        try:
            from adaptive_rag.webui.interface import create_ui
            demo = create_ui()
            demo.launch(
                server_name="0.0.0.0",
                server_port=7860,
                share=False,
                debug=True,
                show_error=True
            )
        except Exception as e2:
            print(f"❌ 基础模式也失败: {e2}")

if __name__ == "__main__":
    main() 