# 智能自适应 RAG WebUI

借鉴 FlashRAG、FlexRAG、LevelRAG 等优秀框架的 WebUI 界面设计，提供直观的 RAG 系统配置和测试界面。

## 📁 目录结构

```
webui/
├── __init__.py
├── interface.py              # 原始接口文件（保持向后兼容）
├── run_webui.py             # 简化的启动文件
├── main_interface.py        # 新的主界面文件
├── engines/                 # 引擎模块
│   ├── __init__.py
│   ├── adaptive_rag_engine.py      # 主要 RAG 引擎
│   ├── real_config_engine.py       # 真实配置引擎
│   └── mock_data_manager.py        # 模拟数据管理器
├── components/              # UI 组件模块
│   ├── __init__.py
│   ├── basic_tab.py         # 基础配置标签页
│   ├── query_tab.py         # 查询测试标签页
│   └── analysis_tab.py      # 分析可视化标签页
└── utils/                   # 工具模块
    ├── __init__.py
    ├── styles.py            # 样式工具
    └── handlers.py          # 事件处理器
```

## 🚀 快速启动

### 方法1：使用原始接口（推荐）
```bash
cd adaptiverag/adaptive_rag/webui
python interface.py --port 7860
```

### 方法2：使用简化启动器
```bash
cd adaptiverag/adaptive_rag/webui
python run_webui.py --port 7860
```

### 方法3：使用真实配置
```bash
python interface.py --real-config --config-path real_config.yaml
```

## 📋 功能特性

### 🔧 基础配置
- 模型路径配置（检索器、生成器、重排序器）
- 数据路径配置（语料库、索引）
- 批处理大小设置
- 配置保存/加载/重置

### 🔍 智能检索
- 智能查询处理
- 任务分解展示
- 检索策略规划
- 详细结果展示
- 性能统计

### 📈 结果分析
- 任务分解可视化
- 检索器使用统计
- 相关度分布分析
- 性能指标展示
- 查询历史记录

## 🎨 设计理念

1. **模块化设计**：借鉴 FlashRAG 的组件化架构
2. **现代化 UI**：参考 FlexRAG 的界面风格
3. **可视化展示**：融合 LightRAG 的数据展示
4. **自适应配置**：创新的动态配置界面

## 🔧 开发说明

### 添加新组件
1. 在 `components/` 目录下创建新的组件文件
2. 在 `components/__init__.py` 中导入新组件
3. 在主界面中集成新组件

### 添加新引擎
1. 在 `engines/` 目录下创建新的引擎文件
2. 在 `engines/__init__.py` 中导入新引擎
3. 在主界面中使用新引擎

### 自定义样式
1. 修改 `utils/styles.py` 中的 CSS 样式
2. 或创建新的样式文件并在主界面中引用

## 📝 使用示例

### 基础使用
```python
from adaptive_rag.webui.interface import create_ui

# 创建界面
demo = create_ui()

# 启动服务
demo.launch(server_port=7860)
```

### 真实配置使用
```python
from adaptive_rag.webui.interface import create_ui_with_real_config

# 创建真实配置界面
demo = create_ui_with_real_config("config.yaml")

# 启动服务
demo.launch(server_port=7860)
```

## 🛠️ 命令行参数

- `--port`: 服务端口（默认：7860）
- `--host`: 服务主机（默认：0.0.0.0）
- `--debug`: 调试模式
- `--share`: 创建公共链接
- `--real-config`: 使用真实配置
- `--config-path`: 配置文件路径

## 🔗 相关项目

- [FlashRAG](https://github.com/RUC-GSAI/FlashRAG) - 快速检索增强生成
- [FlexRAG](https://github.com/THUDM/FlexRAG) - 灵活的检索增强生成
- [LevelRAG](https://github.com/THUDM/LevelRAG) - 分层检索增强生成

## 📄 许可证

本项目遵循 MIT 许可证。 