#!/bin/bash
# MarkHub 镜像加速安装脚本

set -e

echo "======================================================================"
echo "🚀 MarkHub 镜像加速安装"
echo "======================================================================"

# 设置 HuggingFace 镜像
export HF_ENDPOINT=https://hf-mirror.com
echo "✅ HuggingFace 镜像：$HF_ENDPOINT"

# Git 镜像列表
GIT_MIRRORS=(
    "https://hub.fastgit.org/leejet/stable-diffusion.cpp.git"
    "https://github.com/leejet/stable-diffusion.cpp.git"
)

# 安装 stable-diffusion.cpp
echo ""
echo "📦 安装 stable-diffusion.cpp..."

if [ -d "$HOME/stable-diffusion.cpp" ]; then
    echo "✅ 已存在，跳过"
else
    cloned=false
    for mirror in "${GIT_MIRRORS[@]}"; do
        echo "  尝试镜像：$mirror"
        if git clone --depth 1 "$mirror" "$HOME/stable-diffusion.cpp" 2>/dev/null; then
            echo "  ✅ 克隆成功"
            cloned=true
            break
        else
            echo "  ❌ 失败"
        fi
    done
    
    if [ "$cloned" = false ]; then
        echo "❌ 所有镜像都失败"
        exit 1
    fi
fi

# 编译
echo ""
echo "⚙️  编译 stable-diffusion.cpp..."

cd "$HOME/stable-diffusion.cpp"
mkdir -p build && cd build

if [ ! -f "bin/sd-cli" ]; then
    cmake .. -DSD_METAL=ON
    make -j$(sysctl -n hw.ncpu)
    echo "✅ 编译完成"
else
    echo "✅ 已编译"
fi

echo ""
echo "======================================================================"
echo "✅ stable-diffusion.cpp 安装完成"
echo "   位置：$HOME/stable-diffusion.cpp/build/bin/sd-cli"
echo "======================================================================"

# 下载模型
echo ""
echo "⬇️  下载模型..."

cd ~/.jvs/.openclaw/workspace/skills/markhub
python3 markhub_independent.py --download-models

echo ""
echo "======================================================================"
echo "✅ 所有组件安装完成"
echo ""
echo "测试生成:"
echo "  python3 markhub_independent.py -p 'A test image' -W 512 -H 512"
echo "======================================================================"
