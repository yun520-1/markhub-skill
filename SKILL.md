---
name: markhub
description: 独立版智能媒体生成中心 - 不依赖 ComfyUI，直接使用本地模型生成图片，支持自动下载模型、自动配置、智能错误解决
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3", "git", "cmake"], "python_packages": ["requests", "PIL", "numpy", "psutil"] },
      }
  }
---

# MarkHub - 独立版智能媒体生成中心

**完全独立运行** - 不依赖 ComfyUI 服务器，直接使用本地模型生成图片

## 核心功能

- **🖼️ 独立图片生成** - 不依赖 ComfyUI，直接使用 stable-diffusion.cpp
- **🤖 全自动** - 自动下载模型、自动配置环境、自动生成
- **🔧 智能错误解决** - 自动搜索 GitHub 和 ClawHub 找解决方案
- **📊 质量验证** - 清晰度/亮度/对比度检查
- **📦 批量生成** - 一键生成多张图片
- **📈 资源监控** - CPU/内存实时显示
- **⬇️ 自动下载模型** - 一键下载所有必需模型
- **✅ 质量保证** - 完整的质量验证和错误处理

## 快速开始

### 一键安装

```bash
# 1. 安装 stable-diffusion.cpp
python3 markhub_standalone.py --install-sd-cpp

# 2. 下载模型
python3 markhub_standalone.py --download-models

# 3. 生成图片
python3 markhub_standalone.py -p "A beautiful cosmic goddess"
```

### 命令行选项

```bash
# 检查安装状态
python3 markhub_standalone.py --check

# 下载所有模型
python3 markhub_standalone.py --download-models

# 安装 stable-diffusion.cpp
python3 markhub_standalone.py --install-sd-cpp

# 生成单张图片
python3 markhub_standalone.py \
  -p "A magnificent cosmic goddess" \
  -t "宇宙女神" \
  -W 2048 -H 1024 \
  -s 20 -c 7.0

# 全自动生成
python3 markhub_standalone.py
```

### Python API

```python
from markhub_standalone import MarkHub

hub = MarkHub()

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

# 全自动生成
hub.auto_generate(preset="default")
```

## 配置

### 默认参数

- **分辨率：** 2048x1024 (高清)
- **步数：** 20
- **CFG：** 7.0
- **Sampler：** euler

### 模型存储

所有模型自动下载到：`~/.markhub/models/`

- `z_image_turbo-Q8_0.gguf` (~6.7GB)
- `Qwen3-4B-Q8_0.gguf` (~4.0GB)
- `ae.safetensors` (~0.3GB)

## 智能错误解决

遇到问题时，自动：
1. 分析错误信息
2. 搜索 GitHub Issues
3. 搜索 ClawHub Skills
4. 提供常见解决方案

## 质量验证标准

| 指标 | 标准 | 说明 |
|------|------|------|
| 亮度 | 20-240 | 避免过暗或过亮 |
| 对比度 | >30 | 确保图像清晰 |
| 文件大小 | >100KB | 确保完整性 |

## 许可证

MIT-0
