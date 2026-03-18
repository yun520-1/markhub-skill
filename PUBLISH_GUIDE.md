# MarkHub 技能发布指南 📦

## ✅ 已完成

- [x] 技能包结构创建
- [x] skill.json 配置
- [x] README.md 文档
- [x] 核心代码 (markhub_api.py, markhub.py)

## 📋 发布步骤

### 1. 发布到 ClawHub

**前提：** 需要 ClawHub 账号

```bash
# 登录 ClawHub
clawhub login

# 发布技能
cd ~/.jvs/.openclaw/workspace/skills
clawhub publish ./markhub \
  --slug markhub \
  --name "MarkHub - 智能媒体生成中心" \
  --version 1.0.0 \
  --changelog "初始版本：支持全自动图片/视频生成、质量验证、批量生成、资源监控"
```

**如果网络问题导致失败：**
- 检查网络连接
- 确认 ClawHub 账号已登录
- 联系 ClawHub 支持

### 2. 发布到 GitHub

**前提：** 需要 GitHub 账号

```bash
# 登录 GitHub CLI
gh auth login

# 创建新仓库
cd ~/.jvs/.openclaw/workspace/skills/markhub

# 初始化 git
git init
git add .
git commit -m "Initial commit: MarkHub v1.0.0"

# 创建远程仓库并推送
gh repo create markhub-skill --public --source=. --remote=origin --push
```

**或者手动创建：**

1. 访问 https://github.com/new
2. 仓库名：`markhub-skill`
3. 描述：`MarkHub - 智能媒体生成中心 | AI-powered image and video generation tool`
4. 设为 Public
5. 按提示推送代码：
   ```bash
   cd ~/.jvs/.openclaw/workspace/skills/markhub
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/markhub-skill.git
   git push -u origin main
   ```

### 3. 更新 skill.json 中的仓库 URL

发布后更新：
```json
"repository": {
  "type": "git",
  "url": "https://github.com/YOUR_USERNAME/markhub-skill"
}
```

## 🎯 安装测试

发布完成后，测试安装：

```bash
# 从 ClawHub 安装
clawhub install markhub

# 验证安装
clawhub list

# 使用技能
cd ~/.jvs/.openclaw/workspace/skills/markhub
python3 markhub_api.py
```

## 📝 版本更新

```bash
# 修改代码后
clawhub publish ./markhub \
  --slug markhub \
  --version 1.0.1 \
  --changelog "修复 bug，优化性能"
```

## 🔗 相关链接

- ClawHub: https://clawhub.com
- GitHub: https://github.com
- 技能包位置：`~/.jvs/.openclaw/workspace/skills/markhub`

## 💡 注意事项

1. **发布前检查：**
   - 确保所有文件已添加到技能包
   - 测试代码可以正常运行
   - README.md 包含完整使用说明

2. **版本管理：**
   - 使用语义化版本 (MAJOR.MINOR.PATCH)
   - 每次发布更新 changelog

3. **依赖管理：**
   - 在 skill.json 中声明所有依赖
   - 确保用户可以看到安装要求

---

**当前版本：** 1.0.0
**创建时间：** 2026-03-18
**作者：** mac 小虫子
