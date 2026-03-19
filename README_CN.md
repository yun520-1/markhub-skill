# MarkHub v3.2 - Z-Image 独立版智能媒体生成中心

[![GitHub](https://img.shields.io/badge/GitHub-yun520--1/markhub--skill-blue)](https://github.com/yun520-1/markhub-skill)
[![ClawHub](https://img.shields.io/badge/ClawHub-markhub-green)](https://clawhub.ai/yun520-1/markhub)
[![Version](https://img.shields.io/badge/version-3.2.0-orange)](https://github.com/yun520-1/markhub-skill/releases)
[![License](https://img.shields.io/badge/License-MIT--0-yellow)](LICENSE)

**一键安装 · 全平台支持 · 自动部署** - 10 分钟内部署完成并生成第一张 AI 图片

---

## ✨ v3.2.0 新特性

### 🚀 一键安装脚本
- **全新安装体验** - 一条命令完成所有部署
- **全平台支持** - macOS / Windows (WSL) / Linux
- **自动硬件检测** - 智能启用 Metal/CUDA 加速
- **模型自动下载** - 11GB 模型文件自动获取（带进度条）
- **测试图片生成** - 安装完成后自动生成验证

### 📦 核心特性
- **🖼️ Z-Image 模型** - 最新一代高质量图像生成模型
- **⚡ Metal/CUDA 加速** - Apple Silicon 和 NVIDIA GPU 原生优化
- **💾 内存优化** - CPU/GPU 智能分离，降低显存占用
- **📦 独立运行** - 不依赖 ComfyUI 服务器
- **🔧 智能错误解决** - 自动搜索 GitHub 和 ClawHub

---

## 🚀 快速开始

### 一键安装（推荐）

**只需一条命令，10 分钟完成所有部署：**

```bash
curl -fsSL https://raw.githubusercontent.com/yun520-1/markhub-skill/main/install.sh | bash
```

**安装过程自动完成：**
1. ✅ 检查系统环境（Python/cmake）
2. ✅ 安装必要依赖
3. ✅ 检测硬件加速（Metal/CUDA）
4. ✅ 下载模型文件（约 11GB，带进度条）
5. ✅ 生成测试图片验证安装

**预计耗时：** 10-30 分钟（主要取决于网络速度）

---

### 分步安装

#### 步骤 1：安装依赖

```bash
# macOS (Apple Silicon)
CMAKE_ARGS="-DSD_METAL=ON" pip3 install stable-diffusion-cpp-python

# Linux (NVIDIA GPU)
CMAKE_ARGS="-DSD_CUDA=ON" pip3 install stable-diffusion-cpp-python

# 通用版本
pip3 install stable-diffusion-cpp-python
```

#### 步骤 2：下载模型

```bash
# 使用下载脚本
python3 scripts/download_models.py

# 或手动下载
# 访问：https://huggingface.co/yun520-1/z-image-turbo
```

#### 步骤 3：测试

```bash
python3 markhub_v3.py -p "A beautiful woman" -t "test"
```

---

## 📦 模型文件

### 必需模型

| 文件 | 大小 | 路径 | 说明 |
|------|------|------|------|
| z_image_turbo-Q8_0.gguf | ~6.7GB | `unet/` | 主模型 |
| Qwen3-4B-Q8_0.gguf | ~4.0GB | `text_encoders/` | 文本编码器 |
| ae.safetensors | ~0.3GB | `vae/` | VAE 解码器 |

**总计：** ~11GB

### 下载方式

#### 方式 A：自动下载（推荐）
```bash
python3 scripts/download_models.py
```

#### 方式 B：手动下载
1. 访问 HuggingFace: https://huggingface.co/yun520-1/z-image-turbo
2. 下载 3 个文件到对应目录
3. 运行验证：`python3 scripts/download_models.py --save-checksums`

#### 方式 C：国内镜像（推荐中国用户）
```bash
# 使用阿里云镜像
export HF_ENDPOINT=https://hf-mirror.com
python3 scripts/download_models.py
```

---

## 🎨 使用方法

### 命令行

```bash
# 基础用法
python3 markhub_v3.py -p "提示词" -t "图片名称"

# 自定义分辨率
python3 markhub_v3.py -p "A beautiful landscape" -W 1024 -H 1024 -t "landscape"

# 自定义步数
python3 markhub_v3.py -p "A cat" -s 20 -t "cat"

# 固定随机种子
python3 markhub_v3.py -p "A dog" --seed 42 -t "dog"

# 检查安装状态
python3 markhub_v3.py --check
```

### Python API

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

---

## ⚙️ 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-p, --prompt` | 必需 | 提示词 |
| `-t, --title` | output | 输出文件名 |
| `-W, --width` | 768 | 图像宽度 |
| `-H, --height` | 768 | 图像高度 |
| `-s, --steps` | 15 | 采样步数 |
| `-c, --cfg` | 1.0 | CFG 比例 (Z-Image-Turbo 推荐 1.0) |
| `--seed` | -1 | 随机种子 (-1=随机) |
| `--check` | - | 检查安装状态 |
| `--help` | - | 显示帮助信息 |

---

## 📊 性能参考

### Apple M1 Pro
| 分辨率 | 步数 | 耗时 |
|--------|------|------|
| 512x512 | 10 | ~2 分钟 |
| 768x768 | 15 | ~4-5 分钟 |
| 1024x1024 | 20 | ~8-10 分钟 |

### NVIDIA RTX 3060 (CUDA)
| 分辨率 | 步数 | 耗时 |
|--------|------|------|
| 512x512 | 10 | ~1 分钟 |
| 768x768 | 15 | ~2-3 分钟 |
| 1024x1024 | 20 | ~5-6 分钟 |

### CPU (Intel i7)
| 分辨率 | 步数 | 耗时 |
|--------|------|------|
| 512x512 | 10 | ~8 分钟 |
| 768x768 | 15 | ~15-20 分钟 |

---

## 🔧 常见问题

### Q1: 安装失败 - cmake 错误

**解决：**
```bash
# macOS
brew install cmake

# Ubuntu/Debian
sudo apt-get install cmake

# CentOS/RHEL
sudo yum install cmake
```

---

### Q2: 模型下载太慢

**解决：**
```bash
# 使用国内镜像
export HF_ENDPOINT=https://hf-mirror.com
python3 scripts/download_models.py

# 或使用多线程下载
pip3 install huggingface-hub[hf_transfer]
export HF_HUB_ENABLE_HF_TRANSFER=1
python3 scripts/download_models.py
```

---

### Q3: 生成图片时内存不足

**解决：**
```python
# 编辑 markhub_v3.py，启用 CPU 卸载
sd = StableDiffusion(
    ...,
    offload_params_to_cpu=True,
    keep_clip_on_cpu=True,
    keep_vae_on_cpu=True,
)
```

或降低分辨率：
```bash
python3 markhub_v3.py -p "..." -W 512 -H 512
```

---

### Q4: 生成速度慢

**优化建议：**
1. 确保启用硬件加速（Metal/CUDA）
2. 降低采样步数（默认 15 步，可尝试 10 步）
3. 降低分辨率（768x768 → 512x512）
4. 关闭其他占用显存的应用

---

### Q5: Windows 安装

**方法 1：使用 WSL（推荐）**
```bash
# 安装 WSL
wsl --install

# 在 WSL 中运行安装脚本
curl -fsSL https://raw.githubusercontent.com/yun520-1/markhub-skill/main/install.sh | bash
```

**方法 2：使用 Git Bash**
1. 安装 Git for Windows（包含 Git Bash）
2. 安装 Python 3.8+
3. 在 Git Bash 中运行安装脚本

---

## 📝 项目结构

```
markhub-skill/
├── install.sh                    # 一键安装脚本
├── markhub_v3.py                 # 主程序
├── scripts/
│   ├── download_models.py        # 模型下载器
│   └── install.sh                # 安装脚本（旧版）
├── configs/
│   └── sdxl_config.json          # SDXL 配置
├── README.md                     # 英文文档
├── README_CN.md                  # 中文文档（本文件）
├── SKILL.md                      # ClawHub 技能说明
├── skill.json                    # 技能配置
└── LICENSE                       # 许可证
```

---

## 🎬 更新日志

### v3.2.0 (2026-03-19)
- ✅ **一键安装脚本** - 全平台自动部署
- ✅ **模型自动下载** - 带进度条和断点续传
- ✅ **智能硬件检测** - 自动启用 Metal/CUDA 加速
- ✅ **测试图片生成** - 安装完成后自动验证
- ✅ **优化错误提示** - 更友好的错误信息
- ✅ **支持国内镜像** - 阿里云镜像加速

### v3.1.0 (2026-03-18)
- ✅ 跨平台输出路径（~/Pictures/MarkHub/）
- ✅ 内存优化（CPU/GPU 智能分离）
- ✅ 本地模型自动检测

### v3.0.0 (2026-03-18)
- ✅ 使用 Z-Image-Turbo 模型
- ✅ 使用 stable-diffusion-cpp-python
- ✅ Metal 加速优化
- ✅ 独立运行，不依赖 ComfyUI

---

## 📖 文档

- **英文文档:** [README.md](README.md)
- **ClawHub:** https://clawhub.ai/yun520-1/markhub
- **HuggingFace:** https://huggingface.co/yun520-1/z-image-turbo
- **问题反馈:** https://github.com/yun520-1/markhub-skill/issues

---

## 💡 提示词推荐

### 风景
```
A beautiful landscape with mountains and lake, golden hour, cinematic lighting, highly detailed
```

### 人物
```
A beautiful woman with long black hair, traditional Chinese dress, cherry blossoms, soft lighting, digital art
```

### 动物
```
A cute cat sitting on a windowsill, sunlight, fluffy fur, highly detailed, 8k
```

### 科幻
```
A futuristic city with flying cars, neon lights, cyberpunk style, night scene, highly detailed
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- **报告 Bug:** https://github.com/yun520-1/markhub-skill/issues
- **功能建议:** https://github.com/yun520-1/markhub-skill/discussions

---

## 📄 许可证

MIT-0

---

## 👤 作者

yun520-1

---

## 🙏 致谢

感谢以下项目：
- [stable-diffusion-cpp-python](https://github.com/leejet/stable-diffusion.cpp)
- [Hugging Face](https://huggingface.co/)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)

---

**让 AI 绘画变得简单，人人都能创作！** 🎨✨
