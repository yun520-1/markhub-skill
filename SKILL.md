---
name: markhub
description: MarkHub v3.2 - Z-Image 独立版智能媒体生成中心，一键安装脚本支持全平台自动部署，Metal/CUDA 加速
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3", "git", "cmake"], "python_packages": ["stable-diffusion-cpp-python", "PIL", "numpy", "huggingface-hub"] },
      }
  }
---

# MarkHub v3.2 - Z-Image 独立版智能媒体生成中心

**一键安装 · 全平台支持 · 自动部署** - 10 分钟内部署完成并生成第一张 AI 图片

## 核心功能

- **🚀 一键安装** - 一条命令完成所有部署（macOS/Windows/Linux）
- **🖼️ Z-Image 模型** - 最新一代高质量图像生成
- **⚡ Metal/CUDA 加速** - Apple Silicon 和 NVIDIA GPU 原生优化
- **📦 模型自动下载** - 11GB 模型文件自动获取（带进度条）
- **🔧 智能错误解决** - 自动搜索 GitHub 和 ClawHub 找解决方案
- **💾 内存优化** - CPU/GPU 智能分离，降低显存占用
- **📦 本地模型检测** - 自动使用已下载的模型
- **✅ 测试图片生成** - 安装完成后自动生成验证
- **📁 跨平台输出** - 自动保存到 `~/Pictures/MarkHub/`，Windows/Linux/macOS 通用

## 快速开始

### 一键安装（推荐）

```bash
# 一条命令完成所有安装
curl -fsSL https://raw.githubusercontent.com/yun520-1/markhub-skill/main/install.sh | bash
```

### 分步安装

```bash
# macOS Metal 加速
CMAKE_ARGS="-DSD_METAL=ON" pip3 install stable-diffusion-cpp-python

# Linux CUDA 加速
CMAKE_ARGS="-DSD_CUDA=ON" pip3 install stable-diffusion-cpp-python
```

### 模型准备

模型自动检测本地路径：`~/Documents/lmd_data_root/apps/ComfyUI/models/`

必需模型：
- `unet/z_image_turbo-Q8_0.gguf` (~6.7GB)
- `text_encoders/Qwen3-4B-Q8_0.gguf` (~4.0GB)
- `vae/ae.safetensors` (~0.3GB)

### 生成图片

```bash
# 使用示例脚本
python3 markhub_v3.py -p "A beautiful cosmic goddess" -t "goddess"

# 或 Python API
from markhub_v3 import generate_image
generate_image(
    prompt="A beautiful woman with long black hair",
    title="beauty",
    width=768,
    height=768,
    steps=15,
    cfg=1.0,
)
# 输出自动保存到：~/Pictures/MarkHub/markhub_beauty.png
```

## 配置

### 默认参数

- **分辨率：** 768x768 (优化内存)
- **步数：** 15
- **CFG：** 1.0 (Z-Image-Turbo 推荐)
- **Sampler：** Euler

### 输出路径

- **默认目录：** `~/Pictures/MarkHub/`
- **跨平台兼容：** Windows / Linux / macOS 自动适配
- **自动创建：** 目录不存在时自动创建

## 智能错误解决

遇到问题时，自动：
1. 分析错误信息
2. 搜索 GitHub Issues
3. 搜索 ClawHub Skills
4. 提供常见解决方案

## 许可证

MIT-0
