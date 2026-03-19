# MarkHub v3.0 发布指南

## 当前状态

✅ **本地准备完成**
- Git commit 已完成
- 技能包已打包：`markhub-v3.zip`
- 所有文件已更新

⏳ **等待网络恢复**
- GitHub 推送暂时失败（网络问题）
- ClawHub 登录暂时失败（网络问题）

## 手动发布步骤

### 方法 1: 推送到 GitHub

```bash
cd /Users/apple/.jvs/.openclaw/workspace/skills/markhub

# 推送到 GitHub
git push origin main

# 验证推送
git log --oneline -5
```

**仓库地址:** https://github.com/yun520-1/markhub-skill

### 方法 2: 发布到 ClawHub

```bash
# 登录 ClawHub
npx clawhub@latest login

# 发布技能
npx clawhub@latest publish /Users/apple/.jvs/.openclaw/workspace/skills/markhub \
  --slug markhub \
  --name "MarkHub v3 - Z-Image 独立版" \
  --version 3.0.0 \
  --changelog "Z-Image 模型支持，stable-diffusion-cpp-python，Metal 加速优化"
```

**技能地址:** https://clawhub.ai/yun520-1/markhub

### 方法 3: 使用 GitHub 网页上传

1. 访问 https://github.com/yun520-1/markhub-skill
2. 点击 "Upload files"
3. 上传 `markhub-v3.zip` 内容
4. 或者使用 GitHub Desktop 推送

## 文件清单

发布时应包含以下文件：

```
markhub/
├── SKILL.md              # 技能说明（必需）
├── skill.json            # 技能配置（必需）
├── markhub_v3.py         # 主程序
├── README.md             # 使用说明
├── CHANGELOG.md          # 更新日志
├── configs/
│   └── sdxl_config.json
├── install_with_mirror.sh
└── quick_install_sd_cpp.sh
```

## 版本信息

- **版本:** 3.0.0
- **作者:** yun520-1
- **许可证:** MIT-0
- **发布日期:** 2026-03-18

## 更新内容

### v3.0.0 重大更新

- ✅ Z-Image-Turbo 模型支持
- ✅ stable-diffusion-cpp-python 后端
- ✅ Metal 加速 (Apple Silicon)
- ✅ CPU/GPU 内存智能分离
- ✅ 本地模型自动检测
- ✅ 优化配置 (CFG 1.0, 15 步，768x768)

## 测试验证

发布后测试：

```bash
# 安装技能
npx clawhub@latest install yun520-1/markhub

# 检查安装
python3 markhub_v3.py --check

# 生成测试图片
python3 markhub_v3.py -p "A beautiful woman" -t "test"
```

## 网络问题排查

如果持续无法连接：

1. **检查网络连接**
   ```bash
   ping github.com
   ping clawhub.ai
   ```

2. **使用代理**
   ```bash
   export https_proxy=http://127.0.0.1:7890
   export http_proxy=http://127.0.0.1:7890
   ```

3. **使用 Git 镜像**
   ```bash
   git remote set-url origin https://gitclone.com/github.com/yun520-1/markhub-skill.git
   git push origin main
   ```

## 联系支持

- GitHub Issues: https://github.com/yun520-1/markhub-skill/issues
- ClawHub: https://clawhub.ai/support

---

**最后更新:** 2026-03-18 22:20
**状态:** 等待网络恢复后推送
