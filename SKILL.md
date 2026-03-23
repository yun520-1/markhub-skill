---
name: markhub
description: MarkHub v6.5 - Local AI + ComfyUI + Zopia AI Video System
metadata:
  {
    "openclaw":
      {
        "requires": {
          "bins": ["python3", "ffmpeg", "git"],
          "python_packages": ["stable-diffusion-cpp-python", "pillow", "numpy", "requests"]
        }
      }
  }
---

# MarkHub v6.4 - Local AI + ComfyUI Management System

**ComfyNexus Integration · Environment Management · Plugin Control · Hardware Monitoring**

## Core Features

### 🎯 Local AI Creation
- ✅ **100% Local** - No internet required
- ✅ **No Legal Risks** - Only official open-source models
- ✅ **Text-to-Image** - SD-Turbo/SDXL-Turbo/SD-v1.5/SD-v2.1
- ✅ **Text-to-Video** - Multi-frame synthesis
- ✅ **Smart Optimization** - Auto-select best parameters

### 🔧 ComfyNexus Integration (NEW! v6.4)
- ✅ **Environment Management** - Python/PyTorch version detection, snapshots
- ✅ **Plugin Management** - List, update, conflict detection
- ✅ **Hardware Monitoring** - GPU/CPU/Memory/Disk real-time stats
- ✅ **Port Management** - Conflict detection, instance discovery
- ✅ **System Snapshots** - Environment backup and restore

### 🌐 ComfyUI Platform Support
- ✅ **Multi-Platform** - RunPod, Vast.ai, Local, etc.
- ✅ **Auto Detection** - Smart platform recognition
- ✅ **Failover** - Automatic platform switching

### 🎬 Zopia AI Video (NEW! v6.5)
- ✅ **Full Pipeline** - Screenplay → Character → Storyboard → Video
- ✅ **Agent Chat** - Natural language interaction
- ✅ **Multi-Session** - Multi-turn conversation support
- ✅ **4 Presets** - Anime/3D/Pixar/Vertical short video
- ✅ **Balance Query** - Real-time credit check

## Quick Start

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

## 🔧 ComfyNexus Tools (NEW! v6.4)

### Environment Management

```bash
# Check system info
python3 -m modules.comfynexus.environment_manager -a info

# Create environment snapshot
python3 -m modules.comfynexus.environment_manager -a snapshot -n "my-backup"

# List snapshots
python3 -m modules.comfynexus.environment_manager -a list-snapshots

# Check port availability
python3 -m modules.comfynexus.environment_manager -a check-port -p 8188

# Detect running ComfyUI instances
python3 -m modules.comfynexus.environment_manager -a detect-instances
```

### Plugin Management

```bash
# List installed plugins
python3 -m modules.comfynexus.plugin_manager -a list -c /path/to/ComfyUI

# Check for updates
python3 -m modules.comfynexus.plugin_manager -a check-updates -c /path/to/ComfyUI

# Update all plugins
python3 -m modules.comfynexus.plugin_manager -a update-all -c /path/to/ComfyUI

# Check conflicts
python3 -m modules.comfynexus.plugin_manager -a check-conflicts -c /path/to/ComfyUI

# Search GitHub for plugins
python3 -m modules.comfynexus.plugin_manager -a search -q "face enhancement" \
  -t your_github_token
```

### Example Output

```
============================================================
  ComfyNexus 环境信息
============================================================

🖥️  操作系统：Darwin 25.4.0

🐍 Python: 3.9.6
   路径：/Applications/Xcode.app/Contents/Developer/usr/bin/python3

🔦 PyTorch: 2.8.0
   CUDA: ❌  None

💾 内存：32.0 GB (可用：14.6 GB)

🚀 运行中的 ComfyUI 实例：无
```

---

## 🎬 Zopia AI Video (NEW! v6.5)

Zopia 是 AI 驱动的视频制作平台，通过自然语言对话完成全流程：剧本→角色→分镜→视频。

### Get Token

1. Visit https://zopia.ai/settings/api-tokens
2. Login and click "Generate New Token"
3. Copy token: `zopia-xxxxxxxxxxxx` (valid 30 days)

### Quick Start

```bash
# List projects
python3 -m modules.zopia -t zopia-xxxx -a list

# Create project
python3 -m modules.zopia -t zopia-xxxx -a create -n "My Video"

# Apply preset settings
python3 -m modules.zopia -t zopia-xxxx -a settings -b base_xxx --preset anime_standard

# Chat with Agent (generate screenplay)
python3 -m modules.zopia -t zopia-xxxx -a chat -b base_xxx -m "请生成一个校园青春题材的三幕剧本"

# Continue conversation (character design)
python3 -m modules.zopia -t zopia-xxxx -a chat -b base_xxx -s session_xxx -m "请为剧本中的主要角色生成详细设定"

# Check balance
python3 -m modules.zopia -t zopia-xxxx -a balance
```

### Available Presets

| Preset | Style | Aspect Ratio | Use Case |
|--------|-------|--------------|----------|
| **anime_standard** | 日本动画 | 16:9 | 标准动画视频 |
| **realistic_3d** | 3D CG 写实 | 16:9 | 写实 3D 视频 |
| **pixar_cartoon** | Pixar 卡通 | 16:9 | 卡通风格 |
| **vertical_short** | 日本动画 | 9:16 | 竖屏短视频 |

### Video Models

| Model | Method | Description |
|-------|--------|-------------|
| **kling_o3** ⭐ | n_grid | 多帧网格，连贯性好 |
| **vidu_q3_pro** ⭐ | n_grid | 高质量视频生成 |
| **kling_v3.0** | n_grid | Kling v3.0 |
| **seedance_1.5** | start_frame | 首帧驱动 |

### Workflow Example

```bash
# 1. Create project
python3 -m modules.zopia -t zopia-xxxx -a create -n "Campus Story"
# → base_id: base_xxx

# 2. Apply settings
python3 -m modules.zopia -t zopia-xxxx -a settings -b base_xxx --preset anime_standard

# 3. Generate screenplay
python3 -m modules.zopia -t zopia-xxxx -a chat -b base_xxx -m "请生成一个校园青春题材的三幕剧本"
# → session_id: session_xxx

# 4. Character design
python3 -m modules.zopia -t zopia-xxxx -a chat -b base_xxx -s session_xxx -m "请为剧本中的主要角色生成详细设定，包括设计图"

# 5. Storyboard
python3 -m modules.zopia -t zopia-xxxx -a chat -b base_xxx -s session_xxx -m "请为第一幕生成分镜表，列出所有镜头的景别和描述"

# 6. Generate video (3-5 shots at a time)
python3 -m modules.zopia -t zopia-xxxx -a chat -b base_xxx -s session_xxx -m "开始生成 shot1~shot3 的视频"
```

---

## Available Models

| Model | Type | Resolution | Steps | Size | Use Case |
|-------|------|------------|-------|------|----------|
| **sd-turbo** | txt2img | 512×512 | 1 | 1.4GB | Fast generation |
| **sdxl-turbo** | txt2img | 1024×1024 | 1 | 6GB | High-quality portraits |
| **stable-diffusion-v1-5** | txt2img | 512×512 | 20 | 4GB | General purpose |
| **stable-diffusion-v2-1** | txt2img | 768×768 | 20 | 5GB | High resolution |

## Parameters

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

## Output

- **Images:** `~/Videos/MarkHub/MarkHub_YYYYMMDD_HHMMSS.png`
- **Videos:** `~/Videos/MarkHub/MarkHub_Video_YYYYMMDD_HHMMSS.mp4`

## Examples

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

## Legal

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

## Troubleshooting

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

## Performance

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

## Files

- `markhub_v6_1.py` - Main program
- `README.md` - English documentation
- `README_CN.md` - Chinese documentation
- `SKILL.md` - This file
- `install.sh` - Installation script
- `clawhub.json` - ClawHub configuration

## Changelog

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

## License

MIT License

## Acknowledgments

- **Stability AI** - Open-source models
- **stable-diffusion-cpp-python** - C++ backend
- **FFmpeg** - Video synthesis

---

**Version:** v6.1.0  
**Release Date:** 2026-03-20  
**Author:** 1 号小虫子  
**GitHub:** https://github.com/yun520-1/markhub-skill
