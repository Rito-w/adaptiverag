"""
WebUI 样式工具
"""


def get_custom_css() -> str:
    """获取自定义CSS样式"""
    return """
    /* Gradio 容器和主内容区域应占据全宽，移除最大宽度限制和自动边距 */
    .gradio-container, .main, .container {
        max-width: none !important; /* 移除最大宽度限制 */
        margin: 0 !important; /* 移除自动边距 */
        padding: 0 !important; /* 移除内边距，确保内容贴边 */
    }

    .tab-nav {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 8px 8px 0 0;
    }

    /* 按钮样式优化 */
    .primary-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border: none;
        color: white;
        border-radius: 6px;
        transition: all 0.3s ease;
    }

    .primary-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    /* 确保整个页面无留白 */
    body {
        margin: 0 !important; /* 移除自动边距 */
        max-width: none !important; /* 移除最大宽度限制 */
        padding: 0 !important; /* 移除内边距 */
    }

    /* 标题区域居中 */
    .title-container {
        text-align: center;
        margin: 0; /* 调整为0，让它自己控制宽度 */
        padding: 30px 20px; /* 增加上下内边距，左右保持一致 */
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        width: 100%; /* 确保标题容器也占据全宽 */
        box-sizing: border-box; /* 确保 padding 不会增加总宽度 */
    }

    /* 标签页样式优化 */
    .tab-item {
        border-radius: 8px;
        margin: 2px;
        flex-grow: 1; /* 让标签页项目等宽分布 */
    }

    /* 输入框和按钮样式优化 */
    .gr-textbox, .gr-slider {
        border-radius: 6px;
        border: 1px solid #e1e5e9;
    }

    .gr-button {
        border-radius: 6px;
        transition: all 0.3s ease;
    }

    /* 响应式设计 */
    @media (max-width: 768px) {
        .gradio-container, .main, .container {
            max-width: 100% !important;
            padding: 10px !important;
        }

        .title-container {
            margin: 0; /* 调整为0 */
            padding: 15px;
        }
    }
    """ 