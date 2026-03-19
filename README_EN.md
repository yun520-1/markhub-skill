# MarkHub v3 - Z-Image Standalone AI Image Generator

[![GitHub](https://img.shields.io/badge/GitHub-yun520--1/markhub--skill-blue)](https://github.com/yun520-1/markhub-skill)
[![ClawHub](https://img.shields.io/badge/ClawHub-markhub-green)](https://clawhub.ai/yun520-1/markhub)
[![License](https://img.shields.io/badge/License-MIT--0-yellow)](LICENSE)

**Standalone AI image generation** - No ComfyUI dependency, powered by Z-Image model and stable-diffusion-cpp-python

## ✨ Key Features

- **🖼️ Z-Image Model** - Next-generation high-quality image generation
- **⚡ Metal Acceleration** - Native Apple Silicon optimization
- **💾 Memory Optimized** - Smart CPU/GPU memory separation
- **📦 Local Model Detection** - Auto-detects downloaded models
- **🔧 Smart Error Resolution** - Auto-searches GitHub and ClawHub

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# macOS (Metal Acceleration)
CMAKE_ARGS="-DSD_METAL=ON" pip3 install stable-diffusion-cpp-python

# Linux (CUDA)
CMAKE_ARGS="-DSD_CUDA=ON" pip3 install stable-diffusion-cpp-python

# Generic version
pip3 install stable-diffusion-cpp-python
```

### 2. Prepare Models

Models are auto-detected from: `~/Documents/lmd_data_root/apps/ComfyUI/models/`

Required model files:
- `unet/z_image_turbo-Q8_0.gguf` (~6.7GB)
- `text_encoders/Qwen3-4B-Q8_0.gguf` (~4.0GB)
- `vae/ae.safetensors` (~0.3GB)

### 3. Generate Images

```bash
# Generate with default settings
python3 markhub_v3.py

# Custom prompt
python3 markhub_v3.py -p "A beautiful cosmic goddess" -t "goddess"

# High resolution
python3 markhub_v3.py -p "A magnificent landscape" -W 1024 -H 1024 -s 20

# Check installation
python3 markhub_v3.py --check
```

## 📖 Python API

```python
from markhub_v3 import generate_image, check_installation, check_models

# Check environment
if not check_installation():
    exit(1)

if not check_models():
    exit(1)

# Generate image
generate_image(
    prompt="A beautiful woman with long black hair",
    title="beauty",
    width=768,
    height=768,
    steps=15,
    cfg=1.0,
    seed=-1  # Random seed
)
```

## ⚙️ Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| width | 768 | Image width |
| height | 768 | Image height |
| steps | 15 | Sampling steps |
| cfg | 1.0 | CFG scale (Z-Image-Turbo recommended) |
| seed | -1 | Random seed (-1=random) |

## 🔧 Troubleshooting

### Installation Failed

Ensure cmake and python3 are installed:
```bash
brew install cmake  # macOS
```

### Out of Memory

Reduce resolution or enable CPU offloading:
```python
StableDiffusion(
    ...,
    offload_params_to_cpu=True,
    keep_clip_on_cpu=True,
    keep_vae_on_cpu=True,
)
```

### Slow Generation

- Ensure Metal/CUDA acceleration is enabled
- Reduce resolution or steps
- Close other GPU-intensive applications

## 📊 Performance Reference

**Apple M1 Pro:**
- 768x768, 15 steps: ~4-5 minutes
- 1024x1024, 20 steps: ~8-10 minutes

## 📝 Changelog

### v3.0.0 (2026-03-18)
- ✅ Z-Image-Turbo model support
- ✅ Migrated to stable-diffusion-cpp-python
- ✅ Metal acceleration optimization
- ✅ Memory optimization (CPU/GPU separation)
- ✅ Local model auto-detection

### v2.0.0
- Standalone operation without ComfyUI
- Automatic model download
- Smart error resolution

## 📄 License

MIT-0

## 👤 Author

yun520-1

## 🔗 Links

- GitHub: https://github.com/yun520-1/markhub-skill
- ClawHub: https://clawhub.ai/yun520-1/markhub
