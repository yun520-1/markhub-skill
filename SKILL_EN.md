---
name: markhub
description: MarkHub v3 - Z-Image Standalone AI Image Generator with stable-diffusion-cpp-python and Metal acceleration
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3", "git", "cmake"], "python_packages": ["stable-diffusion-cpp-python", "PIL", "numpy"] },
      }
  }
---

# MarkHub v3 - Z-Image Standalone AI Image Generator

**Fully standalone** - No ComfyUI server dependency, powered by Z-Image model and stable-diffusion-cpp-python

## Core Features

- **🖼️ Z-Image Model** - Next-generation high-quality image generation
- **⚡ Metal Acceleration** - Native Apple Silicon optimization
- **🔧 Smart Error Resolution** - Auto-searches GitHub and ClawHub for solutions
- **💾 Memory Optimized** - Smart CPU/GPU separation for reduced VRAM usage
- **📦 Local Model Detection** - Auto-detects downloaded models
- **✅ Quality Assurance** - Complete validation and error handling

## Quick Start

### Install Dependencies

```bash
# macOS Metal Acceleration
CMAKE_ARGS="-DSD_METAL=ON" pip3 install stable-diffusion-cpp-python
```

### Model Preparation

Models are auto-detected from local path: `~/Documents/lmd_data_root/apps/ComfyUI/models/`

Required models:
- `unet/z_image_turbo-Q8_0.gguf` (~6.7GB)
- `text_encoders/Qwen3-4B-Q8_0.gguf` (~4.0GB)
- `vae/ae.safetensors` (~0.3GB)

### Generate Images

```bash
# Use example script
python3 markhub_v3.py

# Or Python API
from stable_diffusion_cpp import StableDiffusion
sd = StableDiffusion(
    diffusion_model_path="unet/z_image_turbo-Q8_0.gguf",
    llm_path="text_encoders/Qwen3-4B-Q8_0.gguf",
    vae_path="vae/ae.safetensors",
)
output = sd.generate_image(prompt="A beautiful woman", width=768, height=768, cfg_scale=1.0)
output[0].save("output.png")
```

## Configuration

### Default Parameters

- **Resolution:** 768x768 (Memory optimized)
- **Steps:** 15
- **CFG:** 1.0 (Z-Image-Turbo recommended)
- **Sampler:** Euler

## Smart Error Resolution

When encountering issues, automatically:
1. Analyzes error messages
2. Searches GitHub Issues
3. Searches ClawHub Skills
4. Provides common solutions

## License

MIT-0
