# MarkHub v3.2 - Z-Image Standalone AI Image Generator

[![GitHub](https://img.shields.io/badge/GitHub-yun520--1/markhub--skill-blue)](https://github.com/yun520-1/markhub-skill)
[![ClawHub](https://img.shields.io/badge/ClawHub-markhub-green)](https://clawhub.ai/yun520-1/markhub)
[![Version](https://img.shields.io/badge/version-3.2.0-orange)](https://github.com/yun520-1/markhub-skill/releases)
[![License](https://img.shields.io/badge/License-MIT--0-yellow)](LICENSE)

**One-Click Installation · Cross-Platform · Auto Deployment** - Deploy and generate your first AI image in 10 minutes

---

## ✨ What's New in v3.2.0

### 🚀 One-Click Installer
- **New Installation Experience** - Complete deployment with a single command
- **Cross-Platform Support** - macOS / Windows (WSL) / Linux
- **Auto Hardware Detection** - Intelligently enable Metal/CUDA acceleration
- **Auto Model Download** - 11GB models automatically downloaded (with progress bar)
- **Test Image Generation** - Automatically generate verification image after installation

### 📦 Core Features
- **🖼️ Z-Image Model** - Latest generation high-quality image generation model
- **⚡ Metal/CUDA Acceleration** - Native optimization for Apple Silicon and NVIDIA GPU
- **💾 Memory Optimization** - CPU/GPU intelligent separation, reduced VRAM usage
- **📦 Standalone** - No ComfyUI server dependency
- **🔧 Smart Error Resolution** - Auto search GitHub and ClawHub

---

## 🚀 Quick Start

### One-Click Installation (Recommended)

**Complete deployment in 10 minutes with a single command:**

```bash
curl -fsSL https://raw.githubusercontent.com/yun520-1/markhub-skill/main/install.sh | bash
```

**Installation process automatically:**
1. ✅ Check system environment (Python/cmake)
2. ✅ Install required dependencies
3. ✅ Detect hardware acceleration (Metal/CUDA)
4. ✅ Download model files (~11GB, with progress bar)
5. ✅ Generate test image to verify installation

**Estimated time:** 10-30 minutes (mainly depends on network speed)

---

### Step-by-Step Installation

#### Step 1: Install Dependencies

```bash
# macOS (Apple Silicon)
CMAKE_ARGS="-DSD_METAL=ON" pip3 install stable-diffusion-cpp-python

# Linux (NVIDIA GPU)
CMAKE_ARGS="-DSD_CUDA=ON" pip3 install stable-diffusion-cpp-python

# Generic version
pip3 install stable-diffusion-cpp-python
```

#### Step 2: Download Models

```bash
# Use download script
python3 scripts/download_models.py

# Or manual download
# Visit: https://huggingface.co/yun520-1/z-image-turbo
```

#### Step 3: Test

```bash
python3 markhub_v3.py -p "A beautiful woman" -t "test"
```

---

## 📦 Model Files

### Required Models

| File | Size | Path | Description |
|------|------|------|-------------|
| z_image_turbo-Q8_0.gguf | ~6.7GB | `unet/` | Main model |
| Qwen3-4B-Q8_0.gguf | ~4.0GB | `text_encoders/` | Text encoder |
| ae.safetensors | ~0.3GB | `vae/` | VAE decoder |

**Total:** ~11GB

### Download Methods

#### Method A: Auto Download (Recommended)
```bash
python3 scripts/download_models.py
```

#### Method B: Manual Download
1. Visit HuggingFace: https://huggingface.co/yun520-1/z-image-turbo
2. Download 3 files to corresponding directories
3. Verify: `python3 scripts/download_models.py --save-checksums`

#### Method C: Mirror (Recommended for China users)
```bash
# Use Aliyun mirror
export HF_ENDPOINT=https://hf-mirror.com
python3 scripts/download_models.py
```

---

## 🎨 Usage

### Command Line

```bash
# Basic usage
python3 markhub_v3.py -p "prompt" -t "image_name"

# Custom resolution
python3 markhub_v3.py -p "A beautiful landscape" -W 1024 -H 1024 -t "landscape"

# Custom steps
python3 markhub_v3.py -p "A cat" -s 20 -t "cat"

# Fixed random seed
python3 markhub_v3.py -p "A dog" --seed 42 -t "dog"

# Check installation
python3 markhub_v3.py --check
```

### Python API

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

---

## ⚙️ Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `-p, --prompt` | Required | Prompt text |
| `-t, --title` | output | Output filename |
| `-W, --width` | 768 | Image width |
| `-H, --height` | 768 | Image height |
| `-s, --steps` | 15 | Sampling steps |
| `-c, --cfg` | 1.0 | CFG scale (Z-Image-Turbo recommends 1.0) |
| `--seed` | -1 | Random seed (-1=random) |
| `--check` | - | Check installation status |
| `--help` | - | Show help information |

---

## 📊 Performance Reference

### Apple M1 Pro
| Resolution | Steps | Time |
|------------|-------|------|
| 512x512 | 10 | ~2 min |
| 768x768 | 15 | ~4-5 min |
| 1024x1024 | 20 | ~8-10 min |

### NVIDIA RTX 3060 (CUDA)
| Resolution | Steps | Time |
|------------|-------|------|
| 512x512 | 10 | ~1 min |
| 768x768 | 15 | ~2-3 min |
| 1024x1024 | 20 | ~5-6 min |

### CPU (Intel i7)
| Resolution | Steps | Time |
|------------|-------|------|
| 512x512 | 10 | ~8 min |
| 768x768 | 15 | ~15-20 min |

---

## 🔧 Troubleshooting

### Q1: Installation Failed - cmake Error

**Solution:**
```bash
# macOS
brew install cmake

# Ubuntu/Debian
sudo apt-get install cmake

# CentOS/RHEL
sudo yum install cmake
```

---

### Q2: Model Download Too Slow

**Solution:**
```bash
# Use mirror
export HF_ENDPOINT=https://hf-mirror.com
python3 scripts/download_models.py

# Or use multi-threaded download
pip3 install huggingface-hub[hf_transfer]
export HF_HUB_ENABLE_HF_TRANSFER=1
python3 scripts/download_models.py
```

---

### Q3: Out of Memory During Generation

**Solution:**
```python
# Edit markhub_v3.py, enable CPU offload
sd = StableDiffusion(
    ...,
    offload_params_to_cpu=True,
    keep_clip_on_cpu=True,
    keep_vae_on_cpu=True,
)
```

Or reduce resolution:
```bash
python3 markhub_v3.py -p "..." -W 512 -H 512
```

---

### Q4: Slow Generation

**Optimization Tips:**
1. Ensure hardware acceleration is enabled (Metal/CUDA)
2. Reduce sampling steps (default 15, try 10)
3. Reduce resolution (768x768 → 512x512)
4. Close other applications using VRAM

---

### Q5: Windows Installation

**Method 1: Use WSL (Recommended)**
```bash
# Install WSL
wsl --install

# Run installation script in WSL
curl -fsSL https://raw.githubusercontent.com/yun520-1/markhub-skill/main/install.sh | bash
```

**Method 2: Use Git Bash**
1. Install Git for Windows (includes Git Bash)
2. Install Python 3.8+
3. Run installation script in Git Bash

---

## 📝 Project Structure

```
markhub-skill/
├── install.sh                    # One-click installer
├── markhub_v3.py                 # Main program
├── scripts/
│   ├── download_models.py        # Model downloader
│   └── install.sh                # Installer (old version)
├── configs/
│   └── sdxl_config.json          # SDXL configuration
├── README.md                     # English documentation
├── README_CN.md                  # Chinese documentation
├── SKILL.md                      # ClawHub skill description
├── skill.json                    # Skill configuration
└── LICENSE                       # License
```

---

## 🎬 Changelog

### v3.2.0 (2026-03-19)
- ✅ **One-Click Installer** - Cross-platform auto deployment
- ✅ **Auto Model Download** - With progress bar and resume support
- ✅ **Smart Hardware Detection** - Auto enable Metal/CUDA acceleration
- ✅ **Test Image Generation** - Auto verification after installation
- ✅ **Optimized Error Messages** - More user-friendly error information
- ✅ **Mirror Support** - Aliyun mirror acceleration

### v3.1.0 (2026-03-18)
- ✅ Cross-platform output path (~/Pictures/MarkHub/)
- ✅ Memory optimization (CPU/GPU intelligent separation)
- ✅ Local model auto detection

### v3.0.0 (2026-03-18)
- ✅ Use Z-Image-Turbo model
- ✅ Use stable-diffusion-cpp-python
- ✅ Metal acceleration optimization
- ✅ Standalone, no ComfyUI dependency

---

## 📖 Documentation

- **Chinese:** [README_CN.md](README_CN.md)
- **ClawHub:** https://clawhub.ai/yun520-1/markhub
- **HuggingFace:** https://huggingface.co/yun520-1/z-image-turbo
- **Issues:** https://github.com/yun520-1/markhub-skill/issues

---

## 💡 Prompt Examples

### Landscape
```
A beautiful landscape with mountains and lake, golden hour, cinematic lighting, highly detailed
```

### Portrait
```
A beautiful woman with long black hair, traditional Chinese dress, cherry blossoms, soft lighting, digital art
```

### Animal
```
A cute cat sitting on a windowsill, sunlight, fluffy fur, highly detailed, 8k
```

### Sci-Fi
```
A futuristic city with flying cars, neon lights, cyberpunk style, night scene, highly detailed
```

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

- **Report Bugs:** https://github.com/yun520-1/markhub-skill/issues
- **Feature Requests:** https://github.com/yun520-1/markhub-skill/discussions

---

## 📄 License

MIT-0

---

## 👤 Author

yun520-1

---

## 🙏 Acknowledgments

Thanks to:
- [stable-diffusion-cpp-python](https://github.com/leejet/stable-diffusion.cpp)
- [Hugging Face](https://huggingface.co/)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)

---

**Making AI art simple, everyone can create!** 🎨✨
