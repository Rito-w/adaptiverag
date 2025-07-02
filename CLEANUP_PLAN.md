# 🧹 AdaptiveRAG 代码清理计划

## 📊 当前状态分析

### ✅ **核心工作组件（保留）**
```
adaptiverag/
├── adaptive_rag/
│   ├── core/                    # 核心模块管理器
│   ├── modules/                 # 各功能模块
│   ├── config/                  # 配置系统
│   ├── webui/                   # Web界面
│   │   ├── engines/
│   │   │   └── local_model_engine.py  # 本地模型引擎 ⭐
│   │   ├── components/          # UI组件
│   │   └── enhanced_main_interface.py # 主界面 ⭐
│   └── utils/                   # 工具函数
├── configs/                     # 配置文件
├── launch_simple_local_webui.py # 简化启动器 ⭐
├── launch_local_model_webui.py  # 本地模型启动器 ⭐
├── check_local_resources.py     # 资源检查 ⭐
└── LOCAL_MODEL_SETUP.md         # 使用指南 ⭐
```

### 🗑️ **可以清理的文件**

#### **1. 测试和实验文件**
```
❌ test_*.py                     # 各种测试文件
❌ demo_*.py                     # 演示文件
❌ experiments/                  # 实验目录
❌ test_data/                    # 测试数据
❌ tests/                        # 单元测试
```

#### **2. 重复和过时的启动器**
```
❌ run_webui.py                  # 旧版启动器
❌ launch_webui_with_module_control.py  # 重复启动器
❌ quick_start.py                # 快速启动（已被替代）
❌ example_modular_usage.py      # 示例文件
```

#### **3. 文档和论文**
```
❌ papers/                       # PDF论文文件
❌ docs/                         # 详细文档（保留核心README）
```

#### **4. 过时的配置和脚本**
```
❌ scripts/                      # 安装脚本（已有新版本）
❌ data/benchmarks/              # 基准测试数据
❌ configs/real_config.yaml      # 旧版配置（保留enhanced版本）
```

#### **5. 缓存和日志文件**
```
❌ __pycache__/                  # Python缓存
❌ *.log                         # 日志文件
❌ adaptive_rag.log              # 运行日志
```

## 🎯 **清理后的精简结构**

```
adaptiverag/
├── adaptive_rag/                # 核心代码
│   ├── __init__.py
│   ├── core/                    # 模块管理器
│   ├── modules/                 # 功能模块
│   ├── config/                  # 配置系统
│   ├── webui/                   # Web界面
│   └── utils/                   # 工具函数
├── configs/
│   └── real_config_enhanced.yaml # 主配置文件
├── launch_simple_local_webui.py  # 简化启动器
├── launch_local_model_webui.py   # 完整启动器
├── check_local_resources.py      # 资源检查
├── install_real_model_deps.py    # 依赖安装
├── LOCAL_MODEL_SETUP.md          # 使用指南
├── WEBUI_STATUS.md               # 状态报告
├── requirements.txt              # 依赖列表
├── setup.py                     # 安装脚本
└── README.md                    # 主要说明
```

## 🚀 **清理步骤**

### **第1步：删除测试和实验文件**
- 删除所有 `test_*.py` 文件
- 删除 `experiments/` 目录
- 删除 `test_data/` 目录
- 删除 `tests/` 目录

### **第2步：删除重复启动器**
- 删除 `run_webui.py`
- 删除 `launch_webui_with_module_control.py`
- 删除 `quick_start.py`
- 删除 `example_modular_usage.py`

### **第3步：删除文档和论文**
- 删除 `papers/` 目录
- 删除 `docs/` 目录（保留核心README）

### **第4步：删除过时配置**
- 删除 `scripts/` 目录
- 删除 `data/benchmarks/`
- 删除 `configs/real_config.yaml`

### **第5步：清理缓存**
- 删除所有 `__pycache__/` 目录
- 删除所有 `.log` 文件

## 📋 **保留的核心文件清单**

### **启动器（3个）**
1. `launch_simple_local_webui.py` - 简化版WebUI
2. `launch_local_model_webui.py` - 完整版WebUI  
3. `check_local_resources.py` - 资源检查

### **配置（1个）**
1. `configs/real_config_enhanced.yaml` - 主配置文件

### **文档（3个）**
1. `LOCAL_MODEL_SETUP.md` - 使用指南
2. `WEBUI_STATUS.md` - 状态报告
3. `README.md` - 主要说明

### **核心代码**
1. `adaptive_rag/` - 完整的核心代码目录
2. `requirements.txt` - 依赖列表
3. `setup.py` - 安装脚本

## 💾 **预计节省空间**

- **删除论文PDF**: ~50MB
- **删除实验数据**: ~20MB
- **删除测试文件**: ~10MB
- **删除文档**: ~5MB
- **删除缓存**: ~5MB

**总计节省**: ~90MB

## ⚠️ **注意事项**

1. **备份重要文件**: 清理前确保重要配置已备份
2. **保留工作配置**: 不要删除当前正在使用的配置文件
3. **测试清理后**: 确保清理后系统仍能正常启动
4. **渐进式清理**: 分步骤进行，每步后测试功能

## 🎯 **清理后的优势**

1. **代码更清晰**: 只保留核心功能代码
2. **维护更简单**: 减少不必要的文件
3. **部署更快**: 更小的代码库
4. **理解更容易**: 清晰的项目结构

---

**准备开始清理吗？我们可以逐步进行，确保每一步都不影响系统正常运行。**
