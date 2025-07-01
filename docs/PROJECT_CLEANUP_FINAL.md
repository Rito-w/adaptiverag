# 项目整理总结

## 📋 整理内容

### 删除的文件
已删除以下不必要的测试和重复文件：
- `test_*.py` - 各种测试文件
- `run_enhanced_webui_*.py` - 重复的启动脚本
- `webui_*.py` - 重复的WebUI实现
- `run_*_experiment.py` - 实验脚本
- `download_*.py` - 下载脚本
- `quick_test.py` - 快速测试文件

### 保留的核心文件
- `adaptive_rag/` - 核心模块目录
- `real_config.yaml` - 基础真实配置
- `real_config_enhanced.yaml` - 增强真实配置
- `download_models.py` - 模型下载脚本
- `requirements.txt` - 依赖文件
- `README.md` - 项目说明

## 🚀 启动方式

### 1. 统一启动脚本（推荐）
```bash
# 基础模式
python run_webui.py --mode basic

# 真实配置模式
python run_webui.py --mode real-config

# 指定端口
python run_webui.py --port 8080

# 创建公共链接
python run_webui.py --share

# 仅检查环境
python run_webui.py --check-only
```

### 2. 快速启动脚本
```bash
# 快速启动（自动选择最佳模式）
python quick_start.py
```

## 🌐 自动代理配置

启动脚本会自动配置以下代理设置：

### AutoDL学术加速
- 自动检测并启用 `/etc/network_turbo`
- 适用于AutoDL云服务器环境

### 环境变量设置
```bash
# 代理设置
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
ALL_PROXY=socks5://127.0.0.1:7890

# HuggingFace镜像
HF_ENDPOINT=https://hf-mirror.com
HF_HUB_ENABLE_HF_TRANSFER=1
HF_HUB_DISABLE_TELEMETRY=1
```

## 📁 项目结构

```
adaptiverag/
├── adaptive_rag/           # 核心模块
│   ├── webui/             # WebUI界面
│   ├── core/              # 核心引擎
│   ├── config/            # 配置管理
│   └── ...
├── run_webui.py           # 统一启动脚本
├── quick_start.py         # 快速启动脚本
├── real_config.yaml       # 基础配置
├── real_config_enhanced.yaml # 增强配置
├── download_models.py     # 模型下载
├── requirements.txt       # 依赖文件
└── README.md             # 项目说明
```

## 🔧 功能特性

### 启动脚本特性
1. **自动代理配置** - 自动设置网络代理和HuggingFace镜像
2. **依赖检查** - 启动前检查所有必需依赖
3. **端口检测** - 自动查找可用端口
4. **错误处理** - 详细的错误信息和恢复建议
5. **多种模式** - 支持基础模式和真实配置模式

### WebUI特性
1. **模块化设计** - 清晰的模块分离
2. **真实配置支持** - 使用真实的检索器和生成器
3. **响应式界面** - 现代化的UI设计
4. **详细监控** - 完整的处理流程展示

## 💡 使用建议

1. **首次使用**：运行 `python run_webui.py --check-only` 检查环境
2. **开发测试**：使用 `python quick_start.py` 快速启动
3. **生产部署**：使用 `python run_webui.py --mode real-config`
4. **网络问题**：确保代理配置正确，或使用 `--no-proxy` 跳过代理

## 🐛 故障排除

### 常见问题
1. **端口被占用**：脚本会自动查找可用端口
2. **依赖缺失**：运行 `pip install -r requirements.txt`
3. **网络超时**：检查代理配置或使用镜像源
4. **配置错误**：检查 `real_config_enhanced.yaml` 文件

### 日志查看
启动时会显示详细的日志信息，包括：
- 依赖检查结果
- 代理配置状态
- 端口使用情况
- 错误详细信息

## 📈 性能优化

1. **使用真实配置模式**：获得最佳性能
2. **启用GPU加速**：确保CUDA环境正确配置
3. **优化批处理大小**：根据硬件调整配置
4. **使用SSD存储**：提高模型加载速度

---

**整理完成时间**：2024年12月
**整理内容**：删除冗余文件，统一启动脚本，添加自动代理配置 