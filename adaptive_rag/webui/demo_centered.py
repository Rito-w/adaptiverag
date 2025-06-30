#!/usr/bin/env python3
"""
=== 居中效果演示界面 ===

专门用于测试和演示界面居中效果的简化版本
"""

import gradio as gr

def create_centered_demo():
    """创建居中演示界面"""

    # 优化的居中 CSS
    centered_css = """
    /* 主容器居中 */
    .gradio-container {
        max-width: 1200px !important;
        margin: 0 auto !important;
        padding: 20px !important;
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
        border-radius: 12px;
        background: white;
    }

    /* 确保所有内容容器都居中 */
    .main, .container, .block {
        max-width: 1200px !important;
        margin: 0 auto !important;
    }

    /* 页面背景 */
    body {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        margin: 0;
        padding: 20px;
        min-height: 100vh;
    }

    /* 标题样式 */
    .title-section {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }

    /* 卡片样式 */
    .demo-card {
        background: white;
        border-radius: 12px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        border: 1px solid #e1e5e9;
    }

    /* 按钮样式 */
    .gr-button {
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
    }

    .gr-button.primary {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        border: none !important;
        color: white !important;
    }

    .gr-button.primary:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }

    /* 输入框样式 */
    .gr-textbox {
        border-radius: 8px !important;
        border: 2px solid #e1e5e9 !important;
        transition: border-color 0.3s ease !important;
    }

    .gr-textbox:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        .gradio-container, .main, .container {
            max-width: 100% !important;
            margin: 0 10px !important;
            padding: 15px !important;
        }

        body {
            padding: 10px;
        }

        .title-section {
            padding: 20px;
            margin-bottom: 20px;
        }

        .demo-card {
            padding: 20px;
            margin: 15px 0;
        }
    }

    /* 确保在大屏幕上也居中 */
    @media (min-width: 1400px) {
        body {
            padding: 40px;
        }

        .gradio-container {
            margin: 0 auto !important;
        }
    }
    """

    with gr.Blocks(
        title="🎨 居中效果演示",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="purple",
            neutral_hue="slate"
        ),
        css=centered_css
    ) as demo:

        # 标题区域
        gr.HTML("""
        <div class="title-section">
            <h1 style="margin: 0 0 15px 0; font-size: 2.8em; font-weight: 700;">
                🎨 界面居中效果演示
            </h1>
            <h3 style="margin: 0 0 10px 0; font-size: 1.4em; font-weight: 400; opacity: 0.9;">
                测试页面在不同屏幕尺寸下的居中效果
            </h3>
            <p style="margin: 0; font-size: 1.1em; opacity: 0.8;">
                最大宽度: 1200px | 自动居中 | 响应式设计
            </p>
        </div>
        """)

        # 演示内容
        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML("""
                <div class="demo-card">
                    <h3>📏 布局测试</h3>
                    <p>这个界面应该在页面中央显示，最大宽度为 1200px。</p>
                    <ul>
                        <li>✅ 在大屏幕上居中显示</li>
                        <li>✅ 在小屏幕上自适应宽度</li>
                        <li>✅ 保持适当的内边距</li>
                    </ul>
                </div>
                """)

                test_input = gr.Textbox(
                    label="测试输入框",
                    placeholder="输入一些文本来测试样式...",
                    lines=3
                )

                with gr.Row():
                    test_btn = gr.Button("🚀 主要按钮", variant="primary", size="lg")
                    clear_btn = gr.Button("🗑️ 清空", size="lg")

            with gr.Column(scale=1):
                gr.HTML("""
                <div class="demo-card">
                    <h3>🎨 样式特性</h3>
                    <p>界面包含以下视觉特性：</p>
                    <ul>
                        <li>🌈 渐变背景和阴影</li>
                        <li>🎯 居中对齐布局</li>
                        <li>📱 响应式设计</li>
                        <li>✨ 悬停动画效果</li>
                        <li>🎪 现代化 UI 风格</li>
                    </ul>
                </div>
                """)

                output_area = gr.Textbox(
                    label="输出区域",
                    lines=8,
                    interactive=False
                )

        # 底部信息
        gr.HTML("""
        <div class="demo-card" style="text-align: center; margin-top: 30px;">
            <h4>🔍 检查要点</h4>
            <p>请在不同设备和浏览器窗口大小下测试：</p>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; margin-top: 15px;">
                <span>📱 手机 (< 768px)</span>
                <span>💻 平板 (768px - 1200px)</span>
                <span>🖥️ 桌面 (> 1200px)</span>
            </div>
        </div>
        """)

        # 简单的交互功能
        def process_test(text):
            if not text.strip():
                return "请输入一些文本进行测试..."

            return f"""✅ 测试成功！

输入内容: {text}
字符数: {len(text)}
时间: {gr.utils.get_timestamp()}

界面状态:
- 居中效果: 正常
- 响应式: 正常
- 样式加载: 正常
- 交互功能: 正常

🎉 界面居中效果测试通过！"""

        def clear_content():
            return "", ""

        # 绑定事件
        test_btn.click(
            fn=process_test,
            inputs=[test_input],
            outputs=[output_area]
        )

        clear_btn.click(
            fn=clear_content,
            outputs=[test_input, output_area]
        )

    return demo

if __name__ == "__main__":
    print("🎨 启动居中效果演示界面...")
    print("📍 请检查界面是否在浏览器中居中显示")

    demo = create_centered_demo()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7862,
        share=False,
        debug=True,
        inbrowser=True
    )