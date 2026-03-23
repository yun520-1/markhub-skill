#!/bin/bash
# MarkHub v6.5.0 发布脚本 - GitHub + ClawHub

set -e

VERSION="6.5.0"
REPO_NAME="markhub-skill"
SKILL_DIR="$HOME/.jvs/.openclaw/workspace/skills/markhub"
RELEASE_ZIP="markhub-v${VERSION}-release.zip"

echo "============================================================"
echo "  🚀 MarkHub v${VERSION} 发布脚本"
echo "============================================================"
echo ""

cd "$SKILL_DIR"

# 创建发布包
echo "📦 创建发布包..."
rm -f "$RELEASE_ZIP"

# 排除的文件
EXCLUDE=(
  ".git"
  ".DS_Store"
  "*.zip"
  "node_modules"
  "__pycache__"
  "*.pyc"
  ".github"
)

# 构建排除参数
EXCLUDE_ARGS=""
for item in "${EXCLUDE[@]}"; do
  EXCLUDE_ARGS="$EXCLUDE_ARGS --exclude=$item"
done

# 创建 zip
zip -r "$RELEASE_ZIP" . $EXCLUDE_ARGS -x "*.git*" > /dev/null 2>&1

if [ -f "$RELEASE_ZIP" ]; then
  SIZE=$(ls -lh "$RELEASE_ZIP" | awk '{print $5}')
  echo "✅ 发布包创建成功：$RELEASE_ZIP ($SIZE)"
else
  echo "❌ 发布包创建失败"
  exit 1
fi

echo ""
echo "📤 推送到 GitHub..."
git add -A
git commit -m "release: v${VERSION}" --allow-empty || true
git push origin main

echo ""
echo "✅ GitHub 推送成功"
echo ""

# 创建 GitHub Release
echo "📋 创建 GitHub Release v${VERSION}..."
if command -v gh &> /dev/null; then
  if gh release view "v${VERSION}" &> /dev/null; then
    echo "⚠️  Release v${VERSION} 已存在，删除旧版本..."
    gh release delete "v${VERSION}" --cleanup-tag --yes || true
  fi
  
  gh release create "v${VERSION}" \
    "$RELEASE_ZIP" \
    --title "MarkHub v${VERSION} - Zopia AI Video + ComfyNexus" \
    --notes "
## 🎬 新功能

### Zopia AI Video 集成
- 完整的 AI 视频制作流程：剧本→角色→分镜→视频
- 4 个预设配置：anime_standard, realistic_3d, pixar_cartoon, vertical_short
- Agent 对话工作流支持
- 多轮会话管理
- 积分余额查询

### ComfyNexus 集成
- 环境管理：Python/PyTorch 版本检测、环境快照
- 插件管理：列表、更新、冲突检测、GitHub 搜索
- 性能优化：本地操作 < 3ms 响应时间

### 新增模块
- modules/comfynexus/environment_manager.py - 环境管理
- modules/comfynexus/plugin_manager.py - 插件管理
- modules/zopia/zopia_client.py - Zopia API 客户端

## 📊 性能指标

- 本地操作响应时间：< 3ms
- 环境信息检测：< 100ms
- 创建快照：< 200ms
- GitHub 搜索：1-3 秒

## 📁 文件

- markhub_v6_1.py - 主程序
- markhub_core.py - ComfyUI 核心
- modules/ - 新增模块目录
- SKILL.md - 技能文档

## 🔗 链接

- GitHub: https://github.com/yun520-1/markhub-skill
- ClawHub: https://clawhub.ai/skill/markhub
" \
    --draft=false \
    --prerelease=false

  echo "✅ GitHub Release 创建成功!"
  echo "📁 https://github.com/$(gh api user | jq -r .login)/$REPO_NAME/releases/tag/v${VERSION}"
else
  echo "⚠️  GitHub CLI 未安装，跳过 Release 创建"
  echo "   请手动访问 GitHub 创建 Release"
fi

echo ""
echo "============================================================"
echo "  ✅ MarkHub v${VERSION} 发布完成!"
echo "============================================================"
echo ""
echo "📊 统计信息:"
echo "   - 文件数：$(find . -type f ! -path './.git/*' ! -path './node_modules/*' | wc -l | tr -d ' ')"
echo "   - 发布包：$RELEASE_ZIP ($SIZE)"
echo "   - 版本：v${VERSION}"
echo ""
echo "🔗 访问链接:"
echo "   - GitHub: https://github.com/yun520-1/$REPO_NAME"
echo "   - Release: https://github.com/yun520-1/$REPO_NAME/releases/tag/v${VERSION}"
echo ""
echo "💡 下一步:"
echo "   1. 检查 GitHub Release 页面"
echo "   2. 验证发布包完整性"
echo "   3. 更新 ClawHub (如果需要)"
echo ""
