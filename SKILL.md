---
name: markhub
description: 智能媒体生成中心 - 全自动图片和视频生成工具，支持 ComfyUI 后端，提供自动参数优化、批量生成、质量验证、资源监控等功能
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"], "python_packages": ["requests", "PIL", "numpy", "psutil"] },
      }
  }
---

# MarkHub - 智能媒体生成中心

全自动图片和视频生成工具，基于 ComfyUI 和 stable-diffusion.cpp

## 核心功能

- **🖼️ 图片生成** - 支持 Z-Image-Turbo 等模型
- **🎬 视频生成** - 支持 LTX2、Wan2.1 等模型
- **🤖 全自动** - 自动参数优化、自动生成、自动验证
- **📊 质量验证** - 清晰度/亮度/对比度/锐度检查
- **⏰ 定时任务** - 支持计划任务
- **📦 批量生成** - 一键生成多张图片
- **📈 资源监控** - CPU/GPU/内存实时显示
- **✅ 质量保证** - 无错位、无马赛克验证

## 快速开始

### 前置要求

1. **ComfyUI** - 已安装并运行
   ```bash
   cd ~/Documents/lmd_data_root/apps/ComfyUI
   ./venv/bin/python run.py --listen 127.0.0.1 --port 8188
   ```

2. **Python 依赖**
   ```bash
   pip3 install requests pillow numpy psutil
   ```

3. **模型文件** - 放置在 ComfyUI models 目录
   - `unet/z_image_turbo-Q8_0.gguf`
   - `text_encoders/Qwen3-4B-Q8_0.gguf`
   - `vae/ae.safetensors`

### 使用

#### 单张图片生成

```bash
python3 markhub_api.py
```

#### API 调用

```python
from markhub_api import MarkHubAPI

hub = MarkHubAPI()

# 生成单张图片
result = hub.generate_image(
    prompt="A magnificent cosmic goddess floating in deep space",
    title="宇宙女神",
    width=2048,
    height=1024,
    steps=20,
    cfg=7.0,
    validate=True
)
```

## 配置

默认输出尺寸：**2048x1024** (高清)

可在 `markhub_api.py` 中修改默认参数。

## 质量验证标准

| 指标 | 标准 | 说明 |
|------|------|------|
| 亮度 | 20-240 | 避免过暗或过亮 |
| 对比度 | >30 | 确保图像清晰 |
| 锐度 | >10 | 避免模糊 |
| 文件大小 | >100KB | 确保完整性 |

## 许可证

MIT-0
