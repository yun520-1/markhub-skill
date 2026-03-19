---
name: markhub-v5
description: MarkHub v5.0 - 智能 ComfyUI 远程控制系统，自动读取工作流、自动选择模型、智能参数优化
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3", "curl"], "python_packages": ["requests", "websocket-client"] },
      }
  }
---

# MarkHub v5.0 - 智能 ComfyUI 远程控制系统

**全自动 AI 创作 - 自动工作流 · 自动模型 · 智能优化**

## 核心功能

- **🤖 自动读取工作流** - 智能发现 ComfyUI 所有可用工作流
- **🎯 自动选择模型** - 根据任务类型选择最佳模型
- **🔍 智能搜索** - HuggingFace/GitHub/Civitai 最佳实践
- **⚙️ 参数优化** - 自动调整步数、CFG、分辨率
- **🎨 文生图** - SDXL/Flux/SD3 等主流模型
- **🖼️ 图生图** - Img2Img/Inpaint/Outpaint
- **🎬 文生视频** - LTX-Video/CogVideo/HunyuanVideo
- **📹 图生视频** - I2V/首尾帧控制
- **🌐 远程控制** - 支持 HTTPS 远程 ComfyUI
- **🔄 错误恢复** - 自动重试和错误处理

## 快速开始

### 安装
```bash
bash install_v5.sh
```

### 生成图片
```bash
python3 markhub_v5_core.py -p "A beautiful woman, cinematic lighting"
```

### 生成视频
```bash
python3 markhub_v5_core.py -p "A woman dancing" --video --duration 10
```

### 自动模式
```bash
python3 markhub_v5_core.py -p "A cat playing" --auto
```

## 配置

- **默认 ComfyUI:** `https://wp08.unicorn.org.cn:19329`
- **输出目录:** `~/Videos/MarkHub/`
- **视频时长:** 10 秒（可自定义）

## 参数说明

| 参数 | 说明 |
|------|------|
| `--url` | ComfyUI 地址 |
| `-p, --prompt` | 提示词（必需） |
| `-m, --model` | 模型名称 |
| `-n, --negative` | 负面提示词 |
| `--image` | 生成图片 |
| `--video` | 生成视频 |
| `--auto` | 自动模式 |
| `--duration` | 视频时长（秒） |

## 输出

- **图片:** `~/Videos/MarkHub/MarkHub_*.png`
- **视频:** `~/Videos/MarkHub/MarkHub_Video_*.mp4`

## 智能特性

### 1. 工作流自动发现
自动扫描 ComfyUI 节点，识别支持的工作流类型

### 2. 模型智能搜索
搜索 HuggingFace/GitHub，获取最佳实践参数

### 3. 参数自动优化
根据模型类型自动调整分辨率、步数、CFG 等

### 4. 错误自动恢复
超时重试、队列监控、失败降级

## 示例

### 高质量风景
```bash
python3 markhub_v5_core.py \
  -p "Beautiful landscape, mountains, lake, golden hour, 4k" \
  -m "sd_xl_base_1.0.safetensors"
```

### 舞蹈视频
```bash
python3 markhub_v5_core.py \
  -p "A woman dancing gracefully, flowing dress" \
  --video --duration 10
```

## 相关链接

- GitHub: https://github.com/yun520-1/markhub-skill
- ClawHub: https://clawhub.ai/yun520-1/markhub
