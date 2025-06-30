# 🚀 GitHub Pages 设置指南

本指南将帮助你为AdaptiveRAG项目启用GitHub Pages，实现自动化文档部署。

## 📋 前提条件

- ✅ GitHub仓库已创建
- ✅ 代码已推送到main分支
- ✅ docs目录和GitHub Actions工作流已配置

## 🔧 启用GitHub Pages

### 步骤1: 进入仓库设置

1. 打开你的GitHub仓库: `https://github.com/Rito-w/adaptiverag`
2. 点击仓库顶部的 **Settings** 标签
3. 在左侧菜单中找到 **Pages** 选项

### 步骤2: 配置Pages源

1. 在 **Source** 部分，选择 **GitHub Actions**
2. 不要选择 "Deploy from a branch"
3. 保存设置

![GitHub Pages Settings](https://docs.github.com/assets/cb-49755/mw-1440/images/help/pages/publishing-source-drop-down.webp)

### 步骤3: 触发首次部署

1. 对docs目录进行任何小修改
2. 提交并推送到main分支：
   ```bash
   git add docs/
   git commit -m "docs: trigger initial GitHub Pages deployment"
   git push origin main
   ```

### 步骤4: 检查部署状态

1. 进入仓库的 **Actions** 标签
2. 查看 "📚 Deploy Documentation" 工作流
3. 等待部署完成（通常需要1-3分钟）

## 🌐 访问文档网站

部署完成后，你的文档将在以下地址可用：

**🔗 文档网站**: `https://rito-w.github.io/adaptiverag/`

> 📝 **注意**: 首次部署可能需要几分钟才能生效

## 🔍 故障排除

### 常见问题

#### 1. 页面显示404错误
**原因**: GitHub Pages尚未启用或部署失败
**解决方案**:
- 检查Pages设置是否正确
- 查看Actions工作流是否成功
- 确认main分支有docs目录

#### 2. 工作流失败
**原因**: 权限或配置问题
**解决方案**:
- 检查仓库的Actions权限设置
- 确认工作流文件语法正确
- 查看错误日志详情

#### 3. 样式或功能异常
**原因**: 资源加载失败或配置错误
**解决方案**:
- 检查浏览器控制台错误
- 验证CDN资源链接
- 确认Docsify配置正确

### 检查清单

- [ ] GitHub Pages已启用
- [ ] 选择了"GitHub Actions"作为源
- [ ] 工作流文件存在: `.github/workflows/docs.yml`
- [ ] docs目录包含必要文件
- [ ] 最新代码已推送到main分支

## ⚙️ 高级配置

### 自定义域名（可选）

如果你有自己的域名，可以配置自定义域名：

1. 在Pages设置中添加自定义域名
2. 在域名DNS设置中添加CNAME记录
3. 等待DNS传播完成

### 强制HTTPS

GitHub Pages默认支持HTTPS，建议启用：

1. 在Pages设置中勾选 "Enforce HTTPS"
2. 确保所有资源链接使用HTTPS

### 分支保护

为了保护main分支，可以设置分支保护规则：

1. 进入仓库设置 → Branches
2. 添加分支保护规则
3. 要求状态检查通过

## 📊 监控和维护

### 部署监控

- 每次推送后检查Actions状态
- 设置邮件通知获取部署结果
- 定期检查网站可用性

### 内容更新

- 定期更新文档内容
- 检查链接有效性
- 优化图片和资源大小

### 性能优化

- 使用CDN加速资源加载
- 压缩图片和文件
- 启用浏览器缓存

## 🎯 最佳实践

### 1. 文档结构
```
docs/
├── index.html          # 主配置文件
├── README.md           # 首页内容
├── _sidebar.md         # 导航菜单
├── _navbar.md          # 顶部菜单
├── _coverpage.md       # 封面页
└── _media/             # 媒体文件
```

### 2. 提交规范
```bash
# 文档更新
git commit -m "docs: update installation guide"

# 新增页面
git commit -m "docs: add API reference"

# 修复问题
git commit -m "docs: fix broken links"
```

### 3. 版本管理
- 为重要更新创建标签
- 维护更新日志
- 使用语义化版本号

## 🔗 相关资源

- [GitHub Pages 官方文档](https://docs.github.com/en/pages)
- [Docsify 官方文档](https://docsify.js.org/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Mermaid 图表语法](https://mermaid.js.org/)

## 📞 获取帮助

如果遇到问题，可以：

1. 查看GitHub Pages官方故障排除指南
2. 检查仓库的Issues页面
3. 在GitHub Discussions中提问
4. 联系项目维护者

---

🎉 **恭喜！你的AdaptiveRAG文档网站现在已经可以通过GitHub Pages访问了！**
