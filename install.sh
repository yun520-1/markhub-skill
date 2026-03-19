#!/bin/bash
set -e

# ============================================================================
# MarkHub v3.2.0 一键安装脚本
# 全平台自动部署 - macOS / Windows (WSL) / Linux
# 目标：10 分钟内完成安装并生成测试图片
# ============================================================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# 全局变量
MARKHUB_VERSION="3.2.0"
MODEL_ROOT="$HOME/Documents/lmd_data_root/apps/ComfyUI/models"
OUTPUT_DIR="$HOME/Pictures/MarkHub"
TEMP_DIR=$(mktemp -d)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$TEMP_DIR/markhub_install.log"

# 统计信息
START_TIME=$(date +%s)
TOTAL_SIZE_GB=11

# 打印横幅
print_banner() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║     🎨 MarkHub v${MARKHUB_VERSION} - 一键安装程序                        ║"
    echo "║                                                              ║"
    echo "║     AI 图像生成 · 全平台支持 · 自动部署                              ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

# 打印步骤
print_step() {
    echo -e "\n${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC} ${WHITE}$(printf '%-60s' "$1")${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}\n"
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

# 打印进度条
print_progress() {
    local current=$1
    local total=$2
    local description=$3
    
    local percentage=$((current * 100 / total))
    local filled=$((percentage / 2))
    local empty=$((50 - filled))
    
    local bar=""
    for ((i=0; i<filled; i++)); do bar+="█"; done
    for ((i=0; i<empty; i++)); do bar+="░"; done
    
    printf "\r${CYAN}[%s] %3d%% - %s${NC}" "$bar" "$percentage" "$description"
}

# 记录日志
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 清理函数
cleanup() {
    if [[ -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
    fi
}

trap cleanup EXIT

# 检查命令是否存在
check_command() {
    command -v "$1" &> /dev/null
}

# 获取系统信息
get_system_info() {
    local os_type=""
    local arch=""
    local gpu=""
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        os_type="macOS"
        arch=$(uname -m)
        if [[ "$arch" == "arm64" ]]; then
            gpu="Apple Silicon"
        else
            gpu="Intel"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        os_type="Linux"
        arch=$(uname -m)
        if check_command nvidia-smi; then
            gpu="NVIDIA GPU"
        else
            gpu="CPU"
        fi
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        os_type="Windows"
        arch="x86_64"
        gpu="Unknown"
    else
        os_type="Unknown"
        arch="Unknown"
        gpu="Unknown"
    fi
    
    echo "$os_type | $arch | $gpu"
}

# ============================================================================
# 步骤 1: 系统检查
# ============================================================================
check_system() {
    print_step "步骤 1/7: 检查系统环境"
    
    local sys_info=$(get_system_info)
    echo -e "  系统信息：${CYAN}$sys_info${NC}"
    log "System: $sys_info"
    
    # 检查 Python
    if check_command python3; then
        local py_version=$(python3 --version 2>&1)
        print_success "Python: $py_version"
        log "Python: $py_version"
    else
        print_error "Python 3 未安装"
        echo ""
        echo "请安装 Python 3.8 或更高版本："
        echo "  macOS:  brew install python@3.11"
        echo "  Ubuntu: sudo apt install python3 python3-pip"
        echo "  Windows: 从 https://python.org 下载"
        exit 1
    fi
    
    # 检查 pip
    if check_command pip3; then
        print_success "pip3: $(pip3 --version | head -n1)"
    else
        print_warning "pip3 未安装，尝试安装..."
        python3 -m ensurepip --upgrade 2>/dev/null || true
    fi
    
    # 检查 git
    if check_command git; then
        print_success "Git: $(git --version)"
    else
        print_warning "Git 未安装（可选，用于更新）"
    fi
    
    echo ""
}

# ============================================================================
# 步骤 2: 安装 cmake
# ============================================================================
install_cmake() {
    print_step "步骤 2/7: 检查 cmake"
    
    if check_command cmake; then
        local cmake_version=$(cmake --version | head -n1)
        print_success "已安装：$cmake_version"
        log "CMake: $cmake_version"
    else
        print_warning "cmake 未安装，正在安装..."
        log "Installing cmake..."
        
        if [[ "$OSTYPE" == "darwin"* ]]; then
            if check_command brew; then
                echo "  使用 Homebrew 安装..."
                brew install cmake >> "$LOG_FILE" 2>&1
            else
                print_error "Homebrew 未安装"
                echo ""
                echo "安装 Homebrew:"
                echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
                exit 1
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            if check_command apt-get; then
                echo "  使用 apt 安装..."
                sudo apt-get update >> "$LOG_FILE" 2>&1
                sudo apt-get install -y cmake >> "$LOG_FILE" 2>&1
            elif check_command yum; then
                echo "  使用 yum 安装..."
                sudo yum install -y cmake >> "$LOG_FILE" 2>&1
            else
                print_error "不支持的 Linux 发行版"
                echo "请手动安装 cmake"
                exit 1
            fi
        else
            print_error "不支持的操作系统"
            exit 1
        fi
        
        print_success "cmake 安装完成"
        log "CMake installed successfully"
    fi
    
    echo ""
}

# ============================================================================
# 步骤 3: 检测硬件加速
# ============================================================================
detect_hardware() {
    print_step "步骤 3/7: 检测硬件加速"
    
    CMAKE_ARGS=""
    ACCELERATION=""
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        local chip=$(uname -m)
        if [[ "$chip" == "arm64" ]]; then
            print_success "检测到 Apple Silicon (M1/M2/M3)"
            ACCELERATION="Metal"
            CMAKE_ARGS="-DSD_METAL=ON"
            log "Hardware: Apple Silicon with Metal"
        else
            print_warning "检测到 Intel Mac"
            ACCELERATION="CPU"
            log "Hardware: Intel Mac"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if check_command nvidia-smi; then
            print_success "检测到 NVIDIA GPU"
            ACCELERATION="CUDA"
            CMAKE_ARGS="-DSD_CUDA=ON"
            log "Hardware: NVIDIA GPU with CUDA"
        else
            print_warning "未检测到 NVIDIA GPU"
            ACCELERATION="CPU"
            log "Hardware: CPU only"
        fi
    fi
    
    if [[ -n "$CMAKE_ARGS" ]]; then
        echo -e "  加速方式：${GREEN}$ACCELERATION${NC}"
        echo -e "  编译参数：${YELLOW}$CMAKE_ARGS${NC}"
    else
        echo -e "  加速方式：${YELLOW}CPU (速度较慢)${NC}"
    fi
    
    echo ""
}

# ============================================================================
# 步骤 4: 创建目录结构
# ============================================================================
create_directories() {
    print_step "步骤 4/7: 创建目录结构"
    
    # 模型目录
    mkdir -p "$MODEL_ROOT"/{unet,text_encoders,vae}
    print_success "模型目录：$MODEL_ROOT"
    log "Model directory: $MODEL_ROOT"
    
    # 输出目录
    mkdir -p "$OUTPUT_DIR"
    print_success "输出目录：$OUTPUT_DIR"
    log "Output directory: $OUTPUT_DIR"
    
    echo ""
}

# ============================================================================
# 步骤 5: 安装 Python 依赖
# ============================================================================
install_dependencies() {
    print_step "步骤 5/7: 安装 Python 依赖"
    
    # 升级 pip
    echo -e "  ${CYAN}升级 pip...${NC}"
    python3 -m pip install --upgrade pip --quiet >> "$LOG_FILE" 2>&1
    print_success "pip 已升级"
    
    # 安装 huggingface-hub（用于下载模型）
    echo -e "  ${CYAN}安装 huggingface-hub...${NC}"
    pip3 install huggingface-hub --quiet >> "$LOG_FILE" 2>&1
    print_success "huggingface-hub 已安装"
    
    # 安装 stable-diffusion-cpp-python
    echo -e "  ${CYAN}安装 stable-diffusion-cpp-python (约 2-5 分钟)...${NC}"
    log "Installing stable-diffusion-cpp-python..."
    
    if [[ -n "$CMAKE_ARGS" ]]; then
        CMAKE_ARGS="$CMAKE_ARGS" pip3 install stable-diffusion-cpp-python >> "$LOG_FILE" 2>&1
    else
        pip3 install stable-diffusion-cpp-python >> "$LOG_FILE" 2>&1
    fi
    
    if [[ $? -eq 0 ]]; then
        print_success "stable-diffusion-cpp-python 安装完成"
        log "stable-diffusion-cpp-python installed"
    else
        print_error "安装失败"
        echo ""
        echo "查看日志：$LOG_FILE"
        echo ""
        echo "常见解决方案："
        echo "  1. 确保已安装 cmake"
        echo "  2. 确保 Python 版本 >= 3.8"
        echo "  3. 尝试手动安装：pip3 install stable-diffusion-cpp-python"
        exit 1
    fi
    
    # 安装其他依赖
    echo -e "  ${CYAN}安装其他依赖...${NC}"
    pip3 install pillow numpy --quiet >> "$LOG_FILE" 2>&1
    print_success "其他依赖已安装"
    
    echo ""
}

# ============================================================================
# 步骤 6: 下载模型文件
# ============================================================================
download_models() {
    print_step "步骤 6/7: 下载模型文件 (总计约 ${TOTAL_SIZE_GB}GB)"
    
    echo ""
    echo "  需要下载 3 个模型文件："
    echo "  ┌─────────────────────────────────────────────────────────┐"
    echo "  │ [1/3] z_image_turbo-Q8_0.gguf    ~6.7GB (10-20 分钟)    │"
    echo "  │ [2/3] Qwen3-4B-Q8_0.gguf         ~4.0GB (5-10 分钟)     │"
    echo "  │ [3/3] ae.safetensors             ~0.3GB (1-2 分钟)      │"
    echo "  └─────────────────────────────────────────────────────────┘"
    echo ""
    echo "  预计总耗时：15-30 分钟（取决于网络速度）"
    echo ""
    
    # 使用 Python 下载
    python3 - << 'PYTHON_SCRIPT'
from huggingface_hub import hf_hub_download
from pathlib import Path
import sys
import time

model_root = Path.home() / "Documents/lmd_data_root/apps/ComfyUI/models"

models = [
    ("unet", "z_image_turbo-Q8_0.gguf", "yun520-1/z-image-turbo", 6.7),
    ("text_encoders", "Qwen3-4B-Q8_0.gguf", "yun520-1/z-image-turbo", 4.0),
    ("vae", "ae.safetensors", "yun520-1/z-image-turbo", 0.3),
]

def print_progress(filename, current, total):
    percentage = int(current * 100 / total) if total > 0 else 0
    bar_length = 40
    filled = int(bar_length * current / total) if total > 0 else 0
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f'\r    [{bar}] {percentage:3d}% ', end='', flush=True)

for i, (dir_name, filename, repo, size_gb) in enumerate(models, 1):
    dest_dir = model_root / dir_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = dest_dir / filename
    
    # 检查是否已存在
    if file_path.exists():
        actual_size = file_path.stat().st_size / (1024**3)
        print(f"\n  ⏭️  [{i}/3] {filename}")
        print(f"      已存在：{actual_size:.2f}GB")
        continue
    
    print(f"  📥 [{i}/3] 下载 {filename}...")
    
    try:
        # 使用回调显示进度（简化版）
        downloaded_path = hf_hub_download(
            repo_id=repo,
            filename=filename,
            local_dir=dest_dir,
            resume_download=True,
            force_download=False,
        )
        
        downloaded_size = Path(downloaded_path).stat().st_size / (1024**3)
        print(f"\r    ✅ 完成 ({downloaded_size:.2f}GB)          ")
        
    except Exception as e:
        print(f"\n    ❌ 下载失败：{e}")
        print(f"\n  请手动下载：")
        print(f"  1. 访问 https://huggingface.co/yun520-1/z-image-turbo")
        print(f"  2. 下载 {filename} 到 {dest_dir}")
        sys.exit(1)

print("\n\n  ✅ 所有模型下载完成！")
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
    
    # 验证模型文件
    echo ""
    echo "  验证模型文件..."
    local all_exist=true
    for model_info in "unet:z_image_turbo-Q8_0.gguf:6.7" "text_encoders:Qwen3-4B-Q8_0.gguf:4.0" "vae:ae.safetensors:0.3"; do
        IFS=':' read -r dir filename expected_size <<< "$model_info"
        local file_path="$MODEL_ROOT/$dir/$filename"
        if [[ -f "$file_path" ]]; then
            local actual_size=$(du -h "$file_path" | cut -f1)
            echo -e "    ${GREEN}✅${NC} $dir/$filename ($actual_size)"
        else
            echo -e "    ${RED}❌${NC} $dir/$filename (未找到)"
            all_exist=false
        fi
    done
    
    if [[ "$all_exist" == "false" ]]; then
        print_error "部分模型文件缺失"
        exit 1
    fi
    
    log "Models downloaded successfully"
    echo ""
}

# ============================================================================
# 步骤 7: 生成测试图片
# ============================================================================
generate_test_image() {
    print_step "步骤 7/7: 生成测试图片"
    
    echo "  正在加载模型..."
    echo "  预计耗时：2-5 分钟（首次加载较慢）"
    echo ""
    
    # 创建测试脚本
    cat > "$TEMP_DIR/test_generate.py" << 'PYTHON_TEST'
import sys
from pathlib import Path

# 添加 markhub 路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    from markhub_v3 import generate_image, check_installation, check_models
    
    print("  检查安装状态...")
    if not check_installation():
        print("  ❌ 安装检查失败")
        sys.exit(1)
    
    print("  检查模型文件...")
    if not check_models():
        print("  ❌ 模型检查失败")
        sys.exit(1)
    
    print("  开始生成测试图片...")
    print("  提示词：A beautiful cosmic goddess, long flowing hair, stars and nebula, digital art")
    print("  分辨率：768x768, 15 步")
    print("")
    
    success = generate_image(
        prompt="A beautiful cosmic goddess, long flowing hair, stars and nebula, digital art, cinematic lighting",
        title="test_installation",
        width=768,
        height=768,
        steps=15,
        cfg=1.0,
        seed=42  # 固定种子，可复现
    )
    
    if success:
        output_dir = Path.home() / "Pictures" / "MarkHub"
        print(f"\n  ✅ 测试图片生成成功！")
        print(f"  📁 保存位置：{output_dir}/markhub_test_installation.png")
        sys.exit(0)
    else:
        print("\n  ❌ 生成失败")
        sys.exit(1)
        
except Exception as e:
    print(f"\n  ❌ 错误：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYTHON_TEST
    
    # 运行测试
    cd "$SCRIPT_DIR"
    python3 "$TEMP_DIR/test_generate.py"
    
    if [[ $? -eq 0 ]]; then
        print_success "测试图片生成成功"
        log "Test image generated successfully"
    else
        print_warning "测试图片生成失败（可手动重试）"
        log "Test image generation failed"
    fi
    
    echo ""
}

# ============================================================================
# 打印完成总结
# ============================================================================
print_summary() {
    local end_time=$(date +%s)
    local duration=$((end_time - START_TIME))
    local minutes=$((duration / 60))
    local seconds=$((duration % 60))
    
    print_step "🎉 安装完成！"
    
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║     ✅ MarkHub v${MARKHUB_VERSION} 安装成功！                           ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo ""
    echo "📊 安装统计："
    echo "  ⏱️  总耗时：${minutes}分${seconds}秒"
    echo "  📦 模型大小：${TOTAL_SIZE_GB}GB"
    echo "  📁 输出目录：$OUTPUT_DIR"
    echo "  📂 模型目录：$MODEL_ROOT"
    echo ""
    
    # 检查测试图片
    local test_image="$OUTPUT_DIR/markhub_test_installation.png"
    if [[ -f "$test_image" ]]; then
        echo -e "${GREEN}🖼️  测试图片已生成：${NC}"
        echo "  $test_image"
        echo ""
    fi
    
    echo "🚀 使用方法："
    echo ""
    echo "  # 生成图片（自定义提示词）"
    echo "  python3 markhub_v3.py -p \"你的提示词\" -t \"图片名称\""
    echo ""
    echo "  # 示例"
    echo "  python3 markhub_v3.py -p \"A beautiful landscape\" -t \"landscape\""
    echo ""
    echo "  # 查看帮助"
    echo "  python3 markhub_v3.py --help"
    echo ""
    echo "  # 检查安装状态"
    echo "  python3 markhub_v3.py --check"
    echo ""
    
    echo "📖 文档："
    echo "  GitHub: https://github.com/yun520-1/markhub-skill"
    echo "  ClawHub: https://clawhub.ai/yun520-1/markhub"
    echo ""
    
    echo "💡 提示："
    echo "  - 首次运行会加载模型（约 1-2 分钟）"
    echo "  - 后续运行会更快"
    echo "  - 图片保存在 ~/Pictures/MarkHub/"
    echo ""
    
    log "Installation completed in ${minutes}m${seconds}s"
}

# ============================================================================
# 主函数
# ============================================================================
main() {
    print_banner
    
    # 欢迎信息
    echo "欢迎使用 MarkHub 一键安装程序！"
    echo ""
    echo "本脚本将自动："
    echo "  1. 检查系统环境（Python/cmake）"
    echo "  2. 安装必要依赖"
    echo "  3. 检测硬件加速（Metal/CUDA）"
    echo "  4. 下载模型文件（约 11GB）"
    echo "  5. 生成测试图片"
    echo ""
    echo "预计耗时：10-30 分钟（主要取决于网络速度）"
    echo ""
    
    # 确认安装
    read -p "是否继续安装？[Y/n]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "安装已取消"
        exit 0
    fi
    
    echo ""
    echo "开始安装..."
    echo ""
    
    # 执行安装步骤
    check_system
    install_cmake
    detect_hardware
    create_directories
    install_dependencies
    download_models
    generate_test_image
    
    # 打印总结
    print_summary
    
    # 完成
    echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}安装完成！享受你的 AI 绘画之旅！ 🎨✨${NC}"
    echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"
    echo ""
}

# 运行主函数
main "$@"
