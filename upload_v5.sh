#!/bin/bash
# MarkHub v5.0 上传脚本 - ClawHub + GitHub

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║     🚀 MarkHub v5.0 发布脚本                              ║"
    echo "║                                                          ║"
    echo "║     上传到 ClawHub + GitHub                               ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "\n${BLUE}══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}══════════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查 Git
check_git() {
    print_step "检查 Git"
    
    if ! command -v git &> /dev/null; then
        print_error "Git 未安装"
        exit 1
    fi
    
    print_success "Git: $(git --version)"
}

# 上传到 ClawHub
upload_clawhub() {
    print_step "上传到 ClawHub"
    
    echo "方式 1: 使用 ClawHub CLI"
    echo "方式 2: 网页上传"
    echo ""
    
    if command -v npx &> /dev/null; then
        echo "使用 ClawHub CLI 上传..."
        echo ""
        
        # 创建临时发布包
        TEMP_DIR=$(mktemp -d)
        cp markhub_v5_core.py install_v5.sh skill_v5.json SKILL_V5.md README_V5.md requirements_v5.txt "$TEMP_DIR/"
        
        cd "$TEMP_DIR"
        
        # 上传
        echo "运行：npx clawhub@latest publish"
        npx clawhub@latest publish . || {
            echo ""
            print_error "ClawHub CLI 上传失败"
            echo ""
            echo "请使用网页上传："
            echo "  1. 访问：https://clawhub.ai/yun520-1/markhub"
            echo "  2. 登录账号"
            echo "  3. 创建/更新技能"
            echo "  4. 上传文件"
            echo ""
        }
        
        # 清理
        cd - > /dev/null
        rm -rf "$TEMP_DIR"
    else
        print_warning "npx 未安装"
        echo ""
        echo "请使用网页上传到 ClawHub："
        echo "  1. 访问：https://clawhub.ai/yun520-1/markhub"
        echo "  2. 登录账号"
        echo "  3. 上传技能包"
        echo ""
    fi
}

# 上传到 GitHub
upload_github() {
    print_step "上传到 GitHub"
    
    echo "选择上传方式："
    echo "  1) 使用 Git 推送（推荐）"
    echo "  2) 使用 GitHub CLI"
    echo "  3) 跳过 GitHub"
    echo ""
    read -p "选择 [1-3]: " -n 1 -re
    echo
    
    case $REPLY in
        1)
            if [[ -d ".git" ]]; then
                echo ""
                echo "使用 Git 推送..."
                echo ""
                
                git add markhub_v5_core.py install_v5.sh skill_v5.json SKILL_V5.md README_V5.md requirements_v5.txt RELEASE_REPORT_V5.md 2>/dev/null || true
                git commit -m "Release MarkHub v5.0 - Intelligent ComfyUI Remote Control" || echo "无变更"
                git push origin main
                
                print_success "代码已推送到 GitHub"
            else
                print_error "不是 Git 仓库"
            fi
            ;;
        2)
            if command -v gh &> /dev/null; then
                echo ""
                echo "使用 GitHub CLI 创建 Release..."
                echo ""
                
                gh release create "v5.0.0" \
                    --repo "yun520-1/markhub-skill" \
                    --title "MarkHub v5.0 - Intelligent ComfyUI Control" \
                    --notes "Full release with intelligent workflow discovery, auto-optimization, and remote control." \
                    markhub-v5-complete.zip \
                    || print_warning "GitHub CLI 失败，请手动创建 Release"
                
                print_success "GitHub Release 已创建"
            else
                print_error "GitHub CLI 未安装"
            fi
            ;;
        3)
            echo "跳过 GitHub"
            ;;
        *)
            print_error "无效选择"
            ;;
    esac
}

# 打印总结
print_summary() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                          ║${NC}"
    echo -e "${GREEN}║     ✅ MarkHub v5.0 发布完成！                             ║${NC}"
    echo -e "${GREEN}║                                                          ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    echo "📦 发布包：markhub-v5-complete.zip"
    echo ""
    echo "🔗 链接："
    echo "  GitHub: https://github.com/yun520-1/markhub-skill"
    echo "  ClawHub: https://clawhub.ai/yun520-1/markhub"
    echo ""
    
    echo "🚀 安装命令："
    echo "  bash install_v5.sh"
    echo ""
    
    echo "📖 使用："
    echo "  # 生成图片"
    echo "  python3 markhub_v5_core.py -p \"A beautiful woman\""
    echo ""
    echo "  # 生成视频"
    echo "  python3 markhub_v5_core.py -p \"A dancing woman\" --video"
    echo ""
    echo "  # 自动模式"
    echo "  python3 markhub_v5_core.py -p \"A cat playing\" --auto"
    echo ""
}

# 主函数
main() {
    print_banner
    
    echo "本脚本将上传 MarkHub v5.0 到："
    echo "  - ClawHub"
    echo "  - GitHub（可选）"
    echo ""
    
    read -p "是否继续？[Y/n]: " -n 1 -re
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "发布已取消"
        exit 0
    fi
    
    echo ""
    echo "开始发布..."
    echo ""
    
    check_git
    upload_clawhub
    upload_github
    
    print_summary
    
    echo -e "${GREEN}══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}发布完成！🎉${NC}"
    echo -e "${GREEN}══════════════════════════════════════════════════════════${NC}"
    echo ""
}

main "$@"
