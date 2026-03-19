#!/bin/bash
# MarkHub v3 发布脚本

set -e

SKILL_DIR="$HOME/.jvs/.openclaw/workspace/skills/markhub"
GITHUB_REPO="yun520-1/markhub-skill"
CLAWHUB_REPO="yun520-1/markhub"

echo "🚀 MarkHub v3.0 发布脚本"
echo "================================"
echo ""

cd "$SKILL_DIR"

# 1. 打包文件
echo "📦 打包技能文件..."
rm -f markhub-v3.zip
zip -r markhub-v3.zip \
    SKILL.md \
    skill.json \
    markhub_v3.py \
    README.md \
    CHANGELOG.md \
    configs/ \
    install_with_mirror.sh \
    quick_install_sd_cpp.sh \
    -x "*.git*" \
    -x "*.png" \
    -x "*.pyc"

echo "✅ 打包完成：markhub-v3.zip"
echo ""

# 2. 发布到 GitHub
echo "📤 发布到 GitHub..."
echo "   仓库：https://github.com/$GITHUB_REPO"
echo ""
echo "   手动执行："
echo "   cd $SKILL_DIR"
echo "   git push origin main"
echo ""

# 3. 发布到 ClawHub
echo "📤 发布到 ClawHub..."
echo "   技能：https://clawhub.ai/$CLAWHUB_REPO"
echo ""
echo "   手动执行："
echo "   npx clawhub@latest publish"
echo ""

# 4. 显示摘要
echo "================================"
echo "✅ 发布准备完成！"
echo ""
echo "📋 下一步操作："
echo "   1. 检查网络连接后执行：git push origin main"
echo "   2. 使用 ClawHub CLI 发布：npx clawhub@latest publish"
echo ""
echo "📁 技能包位置：$SKILL_DIR/markhub-v3.zip"
echo ""
