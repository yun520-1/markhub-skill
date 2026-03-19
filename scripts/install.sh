#!/bin/bash
set -e

# MarkHub v4 一键安装脚本
# 目标：5 分钟内部署完成并生成第一张图片

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 全局变量
MARKHUB_VERSION="4.0.0"
MODEL_ROOT="$HOME/Documents/lmd_data_root/apps/ComfyUI/models"
OUTPUT_DIR="$HOME/Pictures/MarkHub"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 打印横幅
print_banner() {
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════╗"
    echo "║                                            ║"
    echo "║     🎨 MarkHub v${MARKHUB_VERSION} 一键安装程序          ║"
    echo "║                                            ║"
    echo "║     5 分钟快速部署，立即开始 AI 绘画！         ║"
    echo "║                                            ║"
    echo "╚════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 打印步骤
print_step() {
    echo -e "\n${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}\n"
}

# 打印成功
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# 打印警告
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# 打印错误
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查命令是否存在
check_command() {
    if command -v "$1" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

# 步骤 1：检查 Python
check_python() {
    print_step "步骤 1/6: 检查 Python 环境"
    
    if check_command python3; then
        PYTHON_VERSION=$(python3 --version)
        print_success "已安装：$PYTHON_VERSION"
    else
        print_error "Python3 未安装"
        echo ""
        echo "请安装 Python 3.8 或更高版本："
        echo "  macOS:  brew install python@3.11"
        echo "  Ubuntu: sudo apt install python3 python3-pip"
        echo "  Windows: 从 https://python.org 下载"
        exit 1
    fi
}

# 步骤 2：检查并安装 cmake
install_cmake() {
    print_step "步骤 2/6: 检查 cmake"
    
    if check_command cmake; then
        CMAKE_VERSION=$(cmake --version | head -n1)
        print_success "已安装：$CMAKE_VERSION"
    else
        print_warning "cmake 未安装，正在安装..."
        
        # macOS
        if [[ "$OSTYPE" == "darwin"* ]]; then
            if check_command brew; then
                brew install cmake
            else
                print_error "Homebrew 未安装"
                echo "请先安装 Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
                exit 1
            fi
        # Linux
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            if check_command apt-get; then
                sudo apt-get update && sudo apt-get install -y cmake
            elif check_command yum; then
                sudo yum install -y cmake
            else
                print_error "不支持的 Linux 发行版，请手动安装 cmake"
                exit 1
            fi
        else
            print_warning "未知操作系统，请手动安装 cmake"
        fi
        
        print_success "cmake 安装完成"
    fi
}

# 步骤 3：检测硬件加速
detect_hardware() {
    print_step "步骤 3/6: 检测硬件加速"
    
    CMAKE_ARGS=""
    
    # macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        CHIP=$(uname -m)
        if [[ "$CHIP" == "arm64" ]]; then
            print_success "检测到 Apple Silicon (M1/M2/M3)，启用 Metal 加速"
            CMAKE_ARGS="-DSD_METAL=ON"
        else
            print_warning "检测到 Intel Mac，使用通用版本（速度较慢）"
        fi
    # Linux
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # 检查 NVIDIA GPU
        if check_command nvidia-smi; then
            print_success "检测到 NVIDIA GPU，启用 CUDA 加速"
            CMAKE_ARGS="-DSD_CUDA=ON"
        else
            print_warning "未检测到 NVIDIA GPU，使用 CPU 版本"
        fi
    fi
    
    if [[ -n "$CMAKE_ARGS" ]]; then
        echo -e "  编译参数：${YELLOW}$CMAKE_ARGS${NC}"
    fi
}

# 步骤 4：安装 Python 依赖
install_dependencies() {
    print_step "步骤 4/6: 安装 Python 依赖"
    
    # 升级 pip
    print_warning "升级 pip..."
    python3 -m pip install --upgrade pip --quiet
    
    # 安装 stable-diffusion-cpp-python
    print_warning "安装 stable-diffusion-cpp-python（约 2-5 分钟）..."
    
    if [[ -n "$CMAKE_ARGS" ]]; then
        CMAKE_ARGS="$CMAKE_ARGS" pip3 install stable-diffusion-cpp-python
    else
        pip3 install stable-diffusion-cpp-python
    fi
    
    # 安装其他依赖
    print_warning "安装其他依赖..."
    pip3 install pillow numpy huggingface-hub --quiet
    
    print_success "依赖安装完成"
}

# 步骤 5：下载模型
download_models() {
    print_step "步骤 5/6: 下载模型文件"
    
    # 创建目录
    mkdir -p "$MODEL_ROOT"/{unet,text_encoders,vae}
    
    echo "模型下载路径：$MODEL_ROOT"
    echo ""
    
    # 使用 Python 脚本下载（带进度条）
    python3 - << 'PYTHON_SCRIPT'
from huggingface_hub import hf_hub_download
from pathlib import Path
import sys

model_root = Path.home() / "Documents/lmd_data_root/apps/ComfyUI/models"

models = [
    ("unet", "z_image_turbo-Q8_0.gguf", "yun520-1/z-image-turbo"),
    ("text_encoders", "Qwen3-4B-Q8_0.gguf", "yun520-1/z-image-turbo"),
    ("vae", "ae.safetensors", "yun520-1/z-image-turbo"),
]

for dir_name, filename, repo in models:
    dest_dir = model_root / dir_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📥 下载 {filename}...")
    
    try:
        file_path = hf_hub_download(
            repo_id=repo,
            filename=filename,
            local_dir=dest_dir,
            resume_download=True,
        )
        size_gb = Path(file_path).stat().st_size / (1024**3)
        print(f"✅ {dir_name}: {filename} ({size_gb:.2f} GB)")
    except Exception as e:
        print(f"❌ 下载失败：{e}")
        print(f"   请手动下载模型文件到：{dest_dir}")
        sys.exit(1)

print("\n✅ 所有模型下载完成！")
PYTHON_SCRIPT
    
    if [[ $? -ne 0 ]]; then
        print_error "模型下载失败"
        echo ""
        echo "请手动下载模型文件："
        echo "  1. 访问 https://huggingface.co/yun520-1/z-image-turbo"
        echo "  2. 下载以下文件到对应目录："
        echo "     - unet/z_image_turbo-Q8_0.gguf"
        echo "     - text_encoders/Qwen3-4B-Q8_0.gguf"
        echo "     - vae/ae.safetensors"
        exit 1
    fi
}

# 步骤 6：验证安装并生成测试图片
test_installation() {
    print_step "步骤 6/6: 验证安装并生成测试图片"
    
    # 创建输出目录
    mkdir -p "$OUTPUT_DIR"
    
    # 复制 markhub_v3.py 到工作目录（如果不存在）
    if [[ ! -f "$SCRIPT_DIR/markhub_v3.py" ]]; then
        print_warning "未找到 markhub_v3.py，请手动下载"
        echo "下载地址：https://github.com/yun520-1/markhub-skill"
    fi
    
    # 运行测试
    print_warning "生成测试图片..."
    
    cd "$SCRIPT_DIR"
    python3 markhub_v3.py -p "A beautiful sunset over mountains, golden hour, cinematic lighting" -t "test_installation"
    
    if [[ $? -eq 0 ]]; then
        print_success "测试图片生成成功！"
        echo ""
        echo "图片位置：$OUTPUT_DIR/markhub_test_installation.png"
    else
        print_error "测试图片生成失败"
        echo "请检查日志获取更多信息"
    fi
}

# 打印完成信息
print_summary() {
    print_step "🎉 安装完成！"
    
    echo -e "${GREEN}"
    echo "╔════════════════════════════════════════════╗"
    echo "║                                            ║"
    echo "║     ✅ MarkHub v${MARKHUB_VERSION} 安装成功！           ║"
    echo "║                                            ║"
    echo "╚════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo ""
    echo "📁 输出目录：$OUTPUT_DIR"
    echo "📂 模型目录：$MODEL_ROOT"
    echo ""
    echo "🚀 使用方法："
    echo ""
    echo "  # 生成图片"
    echo "  python3 markhub_v3.py -p \"你的提示词\" -t \"图片名称\""
    echo ""
    echo "  # 查看帮助"
    echo "  python3 markhub_v3.py --help"
    echo ""
    echo "  # 检查安装状态"
    echo "  python3 markhub_v3.py --check"
    echo ""
    echo "📖 更多文档：https://github.com/yun520-1/markhub-skill"
    echo ""
}

# 主函数
main() {
    print_banner
    
    # 检查是否已安装
    if [[ -f "$SCRIPT_DIR/markhub_v3.py" ]]; then
        echo -e "${YELLOW}⚠️  检测到已安装的文件${NC}"
        echo ""
        read -p "是否继续安装？这将覆盖现有文件 [y/N]: " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "安装已取消"
            exit 0
        fi
    fi
    
    # 执行安装步骤
    check_python
    install_cmake
    detect_hardware
    install_dependencies
    download_models
    test_installation
    
    # 打印总结
    print_summary
}

# 运行主函数
main "$@"
