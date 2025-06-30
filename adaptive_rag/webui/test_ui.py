#!/usr/bin/env python3
"""
=== Web UI 测试脚本 ===

快速测试 Web 界面的居中效果和样式
"""

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_ui():
    """测试 UI 界面"""
    try:
        from adaptive_rag.webui.interface import create_ui
        
        print("🚀 启动 Web UI 测试...")
        print("📍 界面将在浏览器中打开")
        print("🎨 检查以下内容:")
        print("   ✅ 页面是否居中显示")
        print("   ✅ 最大宽度是否为 1200px")
        print("   ✅ 在不同屏幕尺寸下是否响应式")
        print("   ✅ 标题区域是否有渐变背景")
        print("   ✅ 按钮是否有悬停效果")
        
        # 创建界面
        demo = create_ui()
        
        # 启动界面
        demo.launch(
            server_name="127.0.0.1",
            server_port=7861,
            share=False,
            debug=True,
            show_error=True,
            quiet=False,
            inbrowser=True  # 自动在浏览器中打开
        )
        
    except Exception as e:
        print(f"❌ UI 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ui()
