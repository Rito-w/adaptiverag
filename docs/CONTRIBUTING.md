# AdaptiveRAG 贡献指南

我们欢迎对 AdaptiveRAG 的贡献！本文档提供了为项目贡献的指导原则。

## 🚀 开始

### 开发环境设置

1. **Fork 仓库**
   ```bash
   git clone https://github.com/your-username/adaptiverag.git
   cd adaptiverag
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows 系统: venv\Scripts\activate
   ```

3. **安装开发依赖**
   ```bash
   pip install -e ".[dev]"
   ```

4. **安装 pre-commit 钩子**
   ```bash
   pre-commit install
   ```

## 📝 开发指南

### 代码风格

我们使用以下工具来维护代码质量：

- **Black**: 代码格式化
- **isort**: 导入排序
- **flake8**: 代码检查
- **mypy**: 类型检查

运行所有检查：
```bash
black .
isort .
flake8 .
mypy adaptive_rag/
```

### 测试

提交前运行测试：
```bash
pytest tests/
python quick_test.py
```

### 文档

- 为新函数/类更新文档字符串
- 为所有函数添加类型提示
- 如果添加新功能，请更新 README.md

## 🔄 贡献流程

### 1. 创建 Issue

开始工作前，创建一个 issue 描述：
- 您要解决的问题
- 您提出的解决方案
- 任何破坏性更改

### 2. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或者
git checkout -b fix/your-bug-fix
```

### 3. 进行更改

- 编写清晰、有文档的代码
- 为新功能添加测试
- 确保所有测试通过
- 遵循现有代码风格

### 4. 提交更改

使用约定式提交消息：
```bash
git commit -m "feat: add new retrieval method"
git commit -m "fix: resolve memory leak in cache"
git commit -m "docs: update API documentation"
```

### 5. 提交 Pull Request

- 填写 PR 模板
- 链接到相关 issues
- 确保 CI 通过
- 请求维护者审查

## 🧪 贡献类型

### Bug 修复
- 修复现有功能
- 添加回归测试
- 如需要，更新文档

### 新功能
- 实现新的检索方法
- 添加评估指标
- 扩展配置选项

### 文档
- 改进 README
- 添加教程
- 修复错别字和澄清说明

### 性能改进
- 优化现有代码
- 添加基准测试
- 分析内存使用

## 📋 Pull Request 检查清单

- [ ] 代码遵循项目风格指南
- [ ] 测试在本地通过
- [ ] 为新功能添加了新测试
- [ ] 文档已更新
- [ ] CHANGELOG.md 已更新（如适用）
- [ ] 无破坏性更改（或已清楚记录）

## 🐛 报告 Bug

报告 bug 时，请包含：

1. **环境详情**
   - Python 版本
   - 操作系统
   - 包版本

2. **重现步骤**
   - 最小代码示例
   - 预期与实际行为
   - 错误消息/堆栈跟踪

3. **附加上下文**
   - 截图（如适用）
   - 相关 issues

## 💡 功能请求

对于功能请求，请提供：

1. **用例描述**
   - 它解决什么问题？
   - 谁会受益？

2. **建议解决方案**
   - 它应该如何工作？
   - API 设计想法

3. **考虑的替代方案**
   - 其他方法
   - 为什么这种方法更好

## 📞 获取帮助

- **GitHub Issues**: 用于 bug 和功能请求
- **Discussions**: 用于问题和一般讨论
- **Email**: 用于私人咨询

## 🏆 认可

贡献者将：
- 列在 CONTRIBUTORS.md 中
- 在发布说明中提及
- 在学术论文中获得认可（如适用）

## 📄 许可证

通过贡献，您同意您的贡献将在 MIT 许可证下授权。

---

感谢您对 AdaptiveRAG 的贡献！🎉
