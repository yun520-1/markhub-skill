# MarkHub v3 - Z-Image 独立版智能媒体生成中心

[![GitHub](https://img.shields.io/badge/GitHub-yun520--1/markhub--skill-blue)](https://github.com/yun520-1/markhub-skill)
[![ClawHub](https://img.shields.io/badge/ClawHub-markhub-green)](https://clawhub.ai/yun520-1/markhub)
[![License](https://img.shields.io/badge/License-MIT--0-yellow)](LICENSE)

**完全独立运行** - 不依赖 ComfyUI 服务器，使用 z_image 模型和 stable-diffusion-cpp-python

## ✨ 核心特性

- **🖼️ Z-Image 模型** - 最新一代高质量图像生成模型
- **⚡ Metal 加速** - Apple Silicon 原生优化，速度快
- **💾 内存优化** - CPU/GPU 智能分离，降低显存占用
- **📦 本地模型检测** - 自动使用已下载的模型
- **🔧 智能错误解决** - 自动搜索 GitHub 和 ClawHub

## 🚀 快速开始

### 1. 安装依赖

```bash
# macOS (Metal 加速)
CMAKE_ARGS="-DSD_METAL=ON" pip3 install stable-diffusion-cpp-python

# Linux (CUDA)
CMAKE_ARGS="-DSD_CUDA=ON" pip3 install stable-diffusion-cpp-python

# 通用版本
pip3 install stable-diffusion-cpp-python
```

### 2. 准备模型

模型自动检测本地路径：`~/Documents/lmd_data_root/apps/ComfyUI/models/`

必需模型文件：
- `unet/z_image_turbo-Q8_0.gguf` (~6.7GB)
- `text_encoders/Qwen3-4B-Q8_0.gguf` (~4.0GB)
- `vae/ae.safetensors` (~0.3GB)

### 3. 生成图片

```bash
# 使用默认配置生成
python3 markhub_v3.py

# 自定义提示词
python3 markhub_v3.py -p "A beautiful cosmic goddess" -t "goddess"

# 高分辨率
python3 markhub_v3.py -p "A magnificent landscape" -W 1024 -H 1024 -s 20

# 检查安装状态
python3 markhub_v3.py --check
```

## 📖 Python API

```python
from markhub_v3 import generate_image, check_installation, check_models

# 检查环境
if not check_installation():
    exit(1)

if not check_models():
    exit(1)

# 生成图片
generate_image(
    prompt="A beautiful woman with long black hair",
    title="beauty",
    width=768,
    height=768,
    steps=15,
    cfg=1.0,
    seed=-1  # 随机种子
)
```

## ⚙️ 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| width | 768 | 图像宽度 |
| height | 768 | 图像高度 |
| steps | 15 | 采样步数 |
| cfg | 1.0 | CFG 比例 (Z-Image-Turbo 推荐) |
| seed | -1 | 随机种子 (-1=随机) |

## 🔧 常见问题

### 安装失败

确保已安装 cmake 和 python3：
```bash
brew install cmake  # macOS
```

### 内存不足

降低分辨率或启用 CPU 卸载：
```python
StableDiffusion(
    ...,
    offload_params_to_cpu=True,
    keep_clip_on_cpu=True,
    keep_vae_on_cpu=True,
)
```

### 生成速度慢

- 确保启用 Metal/CUDA 加速
- 降低分辨率或步数
- 关闭其他占用显存的应用

## 📊 性能参考

**Apple M1 Pro:**
- 768x768, 15 步：~4-5 分钟
- 1024x1024, 20 步：~8-10 分钟

## 📝 更新日志

### v3.0.0 (2026-03-18)
- ✅ 使用 Z-Image-Turbo 模型
- ✅ 使用 stable-diffusion-cpp-python
- ✅ Metal 加速优化
- ✅ 内存优化 (CPU/GPU 分离)
- ✅ 本地模型自动检测

### v2.0.0
- 独立运行，不依赖 ComfyUI
- 自动下载模型
- 智能错误解决

## 📄 许可证

MIT-0

## 👤 作者

yun520-1

## 🔗 链接

- GitHub: https://github.com/yun520-1/markhub-skill
- ClawHub: https://clawhub.ai/yun520-1/markhub
