#!/bin/bash
# MarkHub v6.1 Installation Script
# English | 中文

set -e

echo "=========================================="
echo "🎨 MarkHub v6.1 - Installation"
echo "=========================================="

# 1. Check Python
echo ""
echo "📦 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 not found"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION"

# 2. Check FFmpeg
echo ""
echo "📦 Checking FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  Warning: FFmpeg not found"
    echo "   Install:"
    echo "   macOS:  brew install ffmpeg"
    echo "   Linux: apt install ffmpeg"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    FFMPEG_VERSION=$(ffmpeg -version | head -n1)
    echo "✅ $FFMPEG_VERSION"
fi

# 3. Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."

echo "   - stable-diffusion-cpp-python (this may take a few minutes)..."
pip3 install stable-diffusion-cpp-python --quiet

echo "   - pillow..."
pip3 install pillow --quiet

echo "   - numpy..."
pip3 install numpy --quiet

echo "✅ Python dependencies installed"

# 4. Create directories
echo ""
echo "📁 Creating directories..."
mkdir -p ~/Videos/MarkHub
mkdir -p ~/.markhub/models
echo "✅ Directories created"
echo "   Output: ~/Videos/MarkHub"
echo "   Models: ~/.markhub/models"

# 5. Test installation
echo ""
echo "🧪 Testing installation..."
python3 -c "
try:
    from stable_diffusion_cpp import StableDiffusion
    print('✅ stable-diffusion-cpp-python installed')
except ImportError as e:
    print(f'⚠️  stable-diffusion-cpp-python failed: {e}')
    print('   Run: pip3 install stable-diffusion-cpp-python')

try:
    from PIL import Image
    print('✅ pillow installed')
except ImportError:
    print('❌ pillow failed')

try:
    import numpy
    print('✅ numpy installed')
except ImportError:
    print('❌ numpy failed')
"

# 6. Complete
echo ""
echo "=========================================="
echo "✅ Installation complete!"
echo "=========================================="
echo ""
echo "📖 Usage:"
echo "   python3 markhub_v6_1.py -p \"A beautiful woman\""
echo ""
echo "📚 Documentation:"
echo "   cat README.md        # English"
echo "   cat README_CN.md     # 中文"
echo ""
echo "🎯 Next steps:"
echo "   1. Test: python3 markhub_v6_1.py -p \"test\""
echo "   2. Check models: cat SKILL.md | grep -A10 \"Available Models\""
echo ""
