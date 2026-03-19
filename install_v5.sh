#!/bin/bash
# MarkHub v5.0 一键安装脚本

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
    echo "║     🚀 MarkHub v5.0 安装程序                              ║"
    echo "║                                                          ║"
    echo "║     智能 ComfyUI 远程控制系统                               ║"
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

# 检查 Python
check_python() {
    print_step "检查 Python 环境"
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 未安装"
        exit 1
    fi
    
    print_success "Python: $(python3 --version)"
}

# 安装依赖
install_dependencies() {
    print_step "安装 Python 依赖"
    
    echo "  安装以下包："
    echo "  - requests (HTTP 客户端)"
    echo "  - websocket-client (WebSocket 支持)"
    echo ""
    
    python3 -m pip install --upgrade pip --quiet
    pip3 install requests websocket-client
    
    print_success "依赖安装完成"
}

# 设置权限
setup_permissions() {
    print_step "设置脚本权限"
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    chmod +x "$SCRIPT_DIR/markhub_v5_core.py"
    
    print_success "权限设置完成"
}

# 测试安装
test_installation() {
    print_step "测试安装"
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    cd "$SCRIPT_DIR"
    
    python3 -c "import requests; import websocket; print('✅ 依赖检查通过')"
    
    print_success "安装测试通过！"
}

# 打印总结
print_summary() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                          ║${NC}"
    echo -e "${GREEN}║     ✅ MarkHub v5.0 安装完成！                             ║${NC}"
    echo -e "${GREEN}║                                                          ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    echo "🚀 使用方法："
    echo ""
    echo "  # 生成图片"
    echo "  python3 markhub_v5_core.py -p \"A beautiful woman\""
    echo ""
    echo "  # 生成视频"
    echo "  python3 markhub_v5_core.py -p \"A dancing woman\" --video"
    echo ""
    echo "  # 自动模式"
    echo "  python3 markhub_v5_core.py -p \"A cat playing\" --auto"
    echo ""
    echo "  # 自定义 ComfyUI 地址"
    echo "  python3 markhub_v5_core.py -p \"...\" --url https://your-comfyui.com"
    echo ""
    
    echo "📁 输出目录：~/Videos/MarkHub/"
    echo ""
    echo "📖 文档：查看 README.md"
    echo ""
}

# 主函数
main() {
    print_banner
    
    echo "本脚本将安装 MarkHub v5.0 核心功能"
    echo ""
    echo "预计耗时：1-2 分钟"
    echo ""
    
    read -p "是否继续安装？[Y/n]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
    
    echo ""
    echo "开始安装..."
    echo ""
    
    check_python
    install_dependencies
    setup_permissions
    test_installation
    
    print_summary
    
    echo -e "${GREEN}══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}安装完成！享受智能 AI 创作！ 🎨✨${NC}"
    echo -e "${GREEN}══════════════════════════════════════════════════════════${NC}"
    echo ""
}

main "$@"
