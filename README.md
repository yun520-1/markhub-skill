# MarkHub v6.1 - Local AI Creation System

**English | [中文](README_CN.md)**

🎨 **Fully Local · No ComfyUI · No Legal Risks**

---

## 🌟 Features

- ✅ **100% Local** - No internet connection required
- ✅ **No ComfyUI** - Independent, no external dependencies
- ✅ **No Legal Risks** - Only official open-source models
- ✅ **Auto Model Management** - Download, cache, load automatically
- ✅ **Text-to-Image** - SD-Turbo/SDXL-Turbo/SD-v1.5/SD-v2.1
- ✅ **Image-to-Image** - Img2Img/Inpaint support
- ✅ **Text-to-Video** - Multi-frame synthesis
- ✅ **Smart Optimization** - Auto-select best parameters

---

## 🚀 Quick Start

### Installation

```bash
# 1. Install dependencies
pip install stable-diffusion-cpp-python pillow numpy

# 2. Install FFmpeg (for video)
brew install ffmpeg  # macOS
apt install ffmpeg   # Linux

# 3. Run
python3 markhub_v6_1.py -p "A beautiful woman"
```

### Generate Image

```bash
# Basic (SD-Turbo, 1 step)
python3 markhub_v6_1.py -p "A cat"

# High quality (SDXL-Turbo)
python3 markhub_v6_1.py -p "Portrait" -m sdxl-turbo

# Custom parameters
python3 markhub_v6_1.py -p "Landscape" --width 1024 --height 1024 --steps 30
```

### Generate Video

```bash
# 10 second video
python3 markhub_v6_1.py -p "Ocean waves" --video --duration 10

# Custom FPS
python3 markhub_v6_1.py -p "Sunset" --video --duration 5 --fps 30
```

### Auto Mode

```bash
# Auto-select best model
python3 markhub_v6_1.py -p "Portrait of a woman" --auto
```

---

## 📦 Available Models

| Model | Type | Resolution | Steps | Size | Use Case |
|-------|------|------------|-------|------|----------|
| **sd-turbo** | txt2img | 512×512 | 1 | 1.4GB | Fast generation |
| **sdxl-turbo** | txt2img | 1024×1024 | 1 | 6GB | High-quality portraits |
| **stable-diffusion-v1-5** | txt2img | 512×512 | 20 | 4GB | General purpose |
| **stable-diffusion-v2-1** | txt2img | 768×768 | 20 | 5GB | High resolution |

---

## 📝 Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `-p, --prompt` | Prompt (required) | - |
| `-n, --negative` | Negative prompt | "" |
| `-m, --model` | Model name | sd-turbo |
| `--video` | Generate video | False |
| `--duration` | Video duration (seconds) | 10 |
| `--fps` | Video FPS | 24 |
| `--auto` | Auto mode | False |
| `--width` | Image width | 512 |
| `--height` | Image height | 512 |
| `--steps` | Sampling steps | Auto |
| `--cfg` | CFG scale | Auto |
| `-o, --output` | Output path | Auto-generated |

---

## 📤 Output

- **Images:** `~/Videos/MarkHub/MarkHub_YYYYMMDD_HHMMSS.png`
- **Videos:** `~/Videos/MarkHub/MarkHub_Video_YYYYMMDD_HHMMSS.mp4`

---

## 🎯 Examples

### High-Quality Portrait

```bash
python3 markhub_v6_1.py \
  -p "Beautiful woman portrait, professional photography, studio lighting" \
  -m sdxl-turbo \
  --width 1024 \
  --height 1024
```

### Landscape

```bash
python3 markhub_v6_1.py \
  -p "Beautiful landscape, mountains, lake, sunset, 4k" \
  -m stable-diffusion-v2-1 \
  --width 768 \
  --height 768 \
  --steps 30
```

### Dance Video

```bash
python3 markhub_v6_1.py \
  -p "A woman dancing gracefully, flowing dress, cinematic" \
  --video \
  --duration 10 \
  --fps 24
```

### Auto Creation

```bash
python3 markhub_v6_1.py \
  -p "A cat playing with yarn" \
  --auto
```

---

## ⚖️ Legal

### ✅ Legal Use

This skill only uses official open-source models:
- **SD-Turbo** - Stability AI (Apache 2.0)
- **SDXL-Turbo** - Stability AI (Apache 2.0)
- **Stable Diffusion v1.5** - Stability AI (CreativeML Open RAIL-M)
- **Stable Diffusion v2.1** - Stability AI (CreativeML Open RAIL-M)

All models from official HuggingFace repositories, no legal risks.

### ❌ Prohibited Use

- Do not generate infringing content
- Do not generate illegal content
- Do not infringe portrait rights
- Comply with local laws

---

## 🔧 Troubleshooting

### Q: Model download failed

**A:** Check network or use mirror:

```bash
export HF_ENDPOINT=https://hf-mirror.com
python3 markhub_v6_1.py -p "test"
```

### Q: Out of memory

**A:** Use smaller model or resolution:

```bash
python3 markhub_v6_1.py -p "test" -m sd-turbo --width 256 --height 256
```

### Q: Slow generation

**A:** Use Turbo models:

```bash
python3 markhub_v6_1.py -p "test" -m sd-turbo
```

### Q: FFmpeg not found

**A:** Install FFmpeg:

```bash
brew install ffmpeg  # macOS
apt install ffmpeg   # Linux
```

---

## 📊 Performance

### Generation Speed (M2 Pro)

| Model | Resolution | Steps | Time/Image |
|-------|------------|-------|------------|
| SD-Turbo | 512×512 | 1 | ~2s |
| SDXL-Turbo | 1024×1024 | 1 | ~5s |
| SD-v1.5 | 512×512 | 20 | ~30s |
| SD-v2.1 | 768×768 | 20 | ~60s |

### Video Generation

| Duration | FPS | Frames | Total Time (SD-Turbo) |
|----------|-----|--------|----------------------|
| 5s | 24 | 120 | ~4min |
| 10s | 24 | 240 | ~8min |
| 10s | 30 | 300 | ~10min |

---

## 📁 Files

- `markhub_v6_1.py` - Main program
- `README.md` - This file (English)
- `README_CN.md` - Chinese documentation
- `SKILL.md` - Skill definition
- `install.sh` - Installation script
- `clawhub.json` - ClawHub configuration

---

## 🔄 Changelog

### v6.1 (2026-03-20)
- ✅ Complete rewrite with full English documentation
- ✅ Improved error handling
- ✅ Better model management
- ✅ Video generation optimization
- ✅ Auto model selection

### v6.0 (2026-03-20)
- ✅ Fully local version
- ✅ No ComfyUI dependency
- ✅ No legal risks

---

## 📄 License

MIT License

---

## 🙏 Acknowledgments

- **Stability AI** - Open-source models
- **stable-diffusion-cpp-python** - C++ backend
- **FFmpeg** - Video synthesis

---

**Version:** v6.1.0  
**Release Date:** 2026-03-20  
**Author:** 1 号小虫子  
**GitHub:** https://github.com/yun520-1/markhub-skill
