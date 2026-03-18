#!/bin/bash
# 快速安装 stable-diffusion.cpp

set -e

SD_DIR="$HOME/stable-diffusion.cpp"
BUILD_DIR="$SD_DIR/build"

echo "🚀 快速安装 stable-diffusion.cpp"
echo "=================================="

# 检查是否已存在
if [ -f "$BUILD_DIR/bin/sd-cli" ]; then
    echo "✅ sd-cli 已安装：$BUILD_DIR/bin/sd-cli"
    exit 0
fi

# 浅克隆（更快）
if [ ! -d "$SD_DIR" ]; then
    echo "📦 克隆仓库（浅克隆）..."
    git clone --depth 1 https://github.com/leejet/stable-diffusion.cpp.git "$SD_DIR"
else
    echo "✅ 仓库已存在"
fi

# 创建构建目录
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

# CMake 配置
echo "⚙️  配置 CMake (启用 Metal GPU 加速)..."
cmake .. -DSD_METAL=ON

# 编译
echo "🔨 编译中... (这可能需要 5-10 分钟)"
make -j$(sysctl -n hw.ncpu)

echo ""
echo "✅ 安装完成！"
echo "   sd-cli 位置：$BUILD_DIR/bin/sd-cli"
echo ""
echo "测试运行:"
echo "   $BUILD_DIR/bin/sd-cli --help"
