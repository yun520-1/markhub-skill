#!/bin/bash
# MarkHub GitHub 发布脚本

set -e

REPO_NAME="markhub-skill"
REPO_DESC="MarkHub - 智能媒体生成中心 | AI-powered image and video generation tool"
SKILL_DIR="$HOME/.jvs/.openclaw/workspace/skills/markhub"

echo "🚀 MarkHub GitHub 发布脚本"
echo "================================"
echo ""

cd "$SKILL_DIR"

# 检查 gh 是否安装
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI 未安装"
    echo "请运行：brew install gh"
    exit 1
fi

# 检查是否已登录
echo "📋 检查 GitHub 登录状态..."
if ! gh auth status &> /dev/null; then
    echo "⚠️  未登录 GitHub，正在引导登录..."
    gh auth login
fi

echo "✅ GitHub 登录成功"
echo ""

# 检查远程仓库是否存在
echo "🔍 检查远程仓库..."
if gh repo view "$REPO_NAME" &> /dev/null; then
    echo "⚠️  仓库 $REPO_NAME 已存在"
    read -p "是否删除并重新创建？(y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        gh repo delete "$REPO_NAME" --confirm
        echo "✅ 已删除旧仓库"
    else
        echo "❌ 取消发布"
        exit 1
    fi
fi

# 创建新仓库
echo "📦 创建新仓库：$REPO_NAME"
gh repo create "$REPO_NAME" \
    --description "$REPO_DESC" \
    --public \
    --source=. \
    --remote=origin \
    --push

echo ""
echo "✅ 发布成功！"
echo ""
echo "📁 仓库地址：https://github.com/$(gh api user | jq -r .login)/$REPO_NAME"
echo ""
echo "💡 下一步："
echo "   1. 访问仓库页面"
echo "   2. 添加许可证（推荐 MIT）"
echo "   3. 添加主题标签：ai, image-generation, comfyui"
echo ""
