#!/bin/bash
# MarkHub v8.0 发布脚本
# 发布到 GitHub 和 ClawHub

set -e

SKILL_DIR="$HOME/.jvs/.openclaw/workspace/skills/markhub-v8"
cd "$SKILL_DIR"

echo "🚀 MarkHub v8.0 发布脚本"
echo "========================"
echo ""

# 检查必要工具
echo "📋 检查必要工具..."
if ! command -v git &> /dev/null; then
    echo "❌ 错误：需要 git"
    exit 1
fi

if ! command -v clawhub &> /dev/null; then
    echo "⚠️  警告：clawhub CLI 未安装"
fi

echo "✅ 工具检查完成"
echo ""

# 清理旧文件
echo "🧹 清理旧文件..."
rm -rf build/ dist/ *.egg-info __pycache__/
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
echo "✅ 清理完成"
echo ""

# Git 操作
echo "📦 Git 操作..."
if [ -d ".git" ]; then
    git add -A
    git commit -m "release: MarkHub v8.0 - 完全本地化版本" || echo "无更改"
    git tag -d v8.0.0 2>/dev/null || true
    git tag -a v8.0.0 -m "MarkHub v8.0 - 完全本地化 AI 短视频创作系统"
    echo "✅ Git 提交和标签完成"
else
    echo "⚠️  不是 git 仓库，跳过"
fi
echo ""

# 推送到 GitHub
echo "🌐 推送到 GitHub..."
if [ -d ".git" ]; then
    echo "   仓库：https://github.com/yun520-1/markhub-skill"
    echo "   请手动执行:"
    echo "   git push origin markhub-v8"
    echo "   git push origin v8.0.0"
else
    echo "⚠️  跳过推送"
fi
echo ""

# 发布到 ClawHub
echo "📤 发布到 ClawHub..."
if command -v clawhub &> /dev/null; then
    echo "   登录 ClawHub..."
    clawhub login || echo "   ⚠️  登录失败，请手动登录"
    
    echo "   发布技能..."
    clawhub publish . || echo "   ⚠️  发布失败，请检查配置"
else
    echo "⚠️  clawhub CLI 未安装"
    echo "   安装：npm install -g clawhub"
fi
echo ""

# 显示发布说明
echo "📋 发布说明"
echo "========================"
echo ""
echo "✅ MarkHub v8.0 特性:"
echo "   - 完全本地化运行"
echo "   - 无远程依赖"
echo "   - 隐私保护"
echo "   - 版权合规"
echo "   - 支持离线使用"
echo ""
echo "📦 发布位置:"
echo "   - GitHub: https://github.com/yun520-1/markhub-skill/tree/main/markhub-v8"
echo "   - ClawHub: https://clawhub.ai/yun520-1/markhub-v8"
echo ""
echo "🎯 使用命令:"
echo "   clawhub install markhub-v8"
echo ""
echo "🎉 发布完成！"
