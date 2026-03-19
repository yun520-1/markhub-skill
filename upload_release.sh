#!/bin/bash
# MarkHub v3.2.0 上传脚本 - GitHub + ClawHub

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 配置
VERSION="3.2.0"
REPO_NAME="markhub-skill"
GITHUB_USER="yun520-1"
PACKAGE_FILE="markhub-v${VERSION}-release.zip"

print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║     🚀 MarkHub v${VERSION} 发布脚本                            ║"
    echo "║                                                              ║"
    echo "║     GitHub + ClawHub 同步上传                                 ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "\n${BLUE}══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}══════════════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查 Git
check_git() {
    print_step "步骤 1/5: 检查 Git"
    
    if ! command -v git &> /dev/null; then
        print_error "Git 未安装"
        exit 1
    fi
    
    print_success "Git: $(git --version)"
}

# 检查 GitHub CLI
check_gh() {
    print_step "步骤 2/5: 检查 GitHub CLI"
    
    if command -v gh &> /dev/null; then
        print_success "GitHub CLI: $(gh --version | head -n1)"
    else
        print_warning "GitHub CLI 未安装"
        echo ""
        echo "请安装 gh CLI:"
        echo "  macOS:  brew install gh"
        echo "  或者访问：https://cli.github.com/"
        echo ""
        echo "或者使用网页上传：https://github.com/new"
    fi
}

# 准备发布包
prepare_release() {
    print_step "步骤 3/5: 准备发布包"
    
    cd "$(dirname "$0")"
    
    if [[ -f "$PACKAGE_FILE" ]]; then
        print_success "发布包已存在：$PACKAGE_FILE"
        ls -lh "$PACKAGE_FILE"
    else
        print_error "发布包未找到：$PACKAGE_FILE"
        echo ""
        echo "请先运行打包命令："
        echo "  zip -r $PACKAGE_FILE install.sh markhub_v3.py scripts/ README.md README_CN.md SKILL.md skill.json RELEASE_NOTES_v3.2.0.md"
        exit 1
    fi
}

# 上传到 GitHub
upload_github() {
    print_step "步骤 4/5: 上传到 GitHub"
    
    echo "请选择上传方式："
    echo ""
    echo "  1) 使用 GitHub CLI (gh)"
    echo "  2) 使用 Git 推送"
    echo "  3) 手动网页上传"
    echo "  4) 跳过 GitHub"
    echo ""
    read -p "选择 [1-4]: " -n 1 -r
    echo
    
    case $REPLY in
        1)
            if command -v gh &> /dev/null; then
                echo ""
                echo "使用 GitHub CLI 创建 Release..."
                echo ""
                
                # 创建 release
                gh release create "v${VERSION}" \
                    --repo "${GITHUB_USER}/${REPO_NAME}" \
                    --title "MarkHub v${VERSION} - One-Click Installation" \
                    --notes-file "RELEASE_NOTES_v3.2.0.md" \
                    "$PACKAGE_FILE" \
                    || print_warning "GitHub CLI 上传失败，请手动上传"
                
                print_success "GitHub Release 已创建"
                echo "查看：https://github.com/${GITHUB_USER}/${REPO_NAME}/releases/tag/v${VERSION}"
            else
                print_error "GitHub CLI 未安装"
            fi
            ;;
        2)
            echo ""
            echo "使用 Git 推送..."
            echo ""
            
            if [[ -d ".git" ]]; then
                git add -A
                git commit -m "Release v${VERSION} - One-Click Installation" || true
                git push origin main || print_warning "Git 推送失败"
                print_success "代码已推送到 GitHub"
            else
                print_error "不是 Git 仓库"
                echo "请先初始化 Git 或克隆仓库"
            fi
            ;;
        3)
            echo ""
            echo "手动上传步骤："
            echo ""
            echo "  1. 访问：https://github.com/new"
            echo "  2. 创建仓库：${REPO_NAME}"
            echo "  3. 上传文件到仓库"
            echo "  4. 创建 Release: https://github.com/${GITHUB_USER}/${REPO_NAME}/releases/new"
            echo "  5. 标签：v${VERSION}"
            echo "  6. 上传：$PACKAGE_FILE"
            echo ""
            ;;
        4)
            echo "跳过 GitHub 上传"
            ;;
        *)
            print_error "无效选择"
            ;;
    esac
}

# 上传到 ClawHub
upload_clawhub() {
    print_step "步骤 5/5: 上传到 ClawHub"
    
    echo "ClawHub 上传方式："
    echo ""
    echo "  方式 1: 使用 ClawHub CLI"
    echo "  方式 2: 网页上传"
    echo ""
    
    if command -v npx &> /dev/null; then
        echo "使用 ClawHub CLI 上传..."
        echo ""
        
        # 解压包并上传
        TEMP_DIR=$(mktemp -d)
        unzip -q "$PACKAGE_FILE" -d "$TEMP_DIR"
        
        cd "$TEMP_DIR"
        
        # 上传到 ClawHub
        echo "运行：npx clawhub@latest publish"
        npx clawhub@latest publish || print_warning "ClawHub 上传失败，请手动上传"
        
        # 清理
        cd - > /dev/null
        rm -rf "$TEMP_DIR"
        
        print_success "ClawHub 上传完成"
        echo "查看：https://clawhub.ai/${GITHUB_USER}/${REPO_NAME}"
    else
        print_warning "npx 未安装，跳过 CLI 上传"
        echo ""
        echo "请手动上传到 ClawHub:"
        echo "  1. 访问：https://clawhub.ai/"
        echo "  2. 登录账号"
        echo "  3. 创建新技能"
        echo "  4. 上传技能包"
        echo ""
    fi
}

# 打印总结
print_summary() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                              ║${NC}"
    echo -e "${GREEN}║     ✅ MarkHub v${VERSION} 发布完成！                                    ║${NC}"
    echo -e "${GREEN}║                                                              ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    echo "📦 发布包：$PACKAGE_FILE"
    echo ""
    echo "🔗 链接："
    echo "  GitHub: https://github.com/${GITHUB_USER}/${REPO_NAME}"
    echo "  ClawHub: https://clawhub.ai/${GITHUB_USER}/${REPO_NAME}"
    echo "  HuggingFace: https://huggingface.co/${GITHUB_USER}/z-image-turbo"
    echo ""
    
    echo " 安装命令："
    echo "  curl -fsSL https://raw.githubusercontent.com/${GITHUB_USER}/${REPO_NAME}/main/install.sh | bash"
    echo ""
    
    echo "📝 下一步："
    echo "  1. 测试安装脚本（空白电脑）"
    echo "  2. 更新 HuggingFace 模型"
    echo "  3. 发布到社区"
    echo "  4. 收集用户反馈"
    echo ""
}

# 主函数
main() {
    print_banner
    
    echo "本脚本将帮助你将 MarkHub v${VERSION} 发布到："
    echo "  - GitHub"
    echo "  - ClawHub"
    echo ""
    
    read -p "是否继续？[Y/n]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "发布已取消"
        exit 0
    fi
    
    check_git
    check_gh
    prepare_release
    upload_github
    upload_clawhub
    print_summary
}

main "$@"
