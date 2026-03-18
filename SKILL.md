---
name: markhub
description: MarkHub v3 - Z-Image 独立版智能媒体生成中心，使用 stable-diffusion-cpp-python，Metal 加速
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3", "git", "cmake"], "python_packages": ["stable-diffusion-cpp-python", "PIL", "numpy"] },
      }
  }
---

# MarkHub v3 - Z-Image 独立版智能媒体生成中心

**完全独立运行** - 不依赖 ComfyUI 服务器，使用 z_image 模型和 stable-diffusion-cpp-python

## 核心功能

- **🖼️ Z-Image 模型** - 最新一代高质量图像生成
- **⚡ Metal 加速** - Apple Silicon 原生优化
- **🔧 智能错误解决** - 自动搜索 GitHub 和 ClawHub 找解决方案
- **💾 内存优化** - CPU/GPU 智能分离，降低显存占用
- **📦 本地模型检测** - 自动使用已下载的模型
- **✅ 质量保证** - 完整的验证和错误处理

## 快速开始

### 安装依赖

```bash
# macOS Metal 加速
CMAKE_ARGS="-DSD_METAL=ON" pip3 install stable-diffusion-cpp-python
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
python3 generate_beauty.py

# 或 Python API
from stable_diffusion_cpp import StableDiffusion
sd = StableDiffusion(
    diffusion_model_path="unet/z_image_turbo-Q8_0.gguf",
    llm_path="text_encoders/Qwen3-4B-Q8_0.gguf",
    vae_path="vae/ae.safetensors",
)
output = sd.generate_image(prompt="A beautiful woman", width=768, height=768, cfg_scale=1.0)
output[0].save("output.png")
```

## 配置

### 默认参数

- **分辨率：** 768x768 (优化内存)
- **步数：** 15
- **CFG：** 1.0 (Z-Image-Turbo 推荐)
- **Sampler：** Euler

## 智能错误解决

遇到问题时，自动：
1. 分析错误信息
2. 搜索 GitHub Issues
3. 搜索 ClawHub Skills
4. 提供常见解决方案

## 许可证

MIT-0
