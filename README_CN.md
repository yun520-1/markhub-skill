# MarkHub v6.1 - 本地 AI 创作系统

**中文 | [English](README.md)**

🎨 **完全本地 · 不依赖 ComfyUI · 无法律风险**

---

## 🌟 核心特性

- ✅ **100% 本地运行** - 无需网络连接
- ✅ **无需 ComfyUI** - 独立运行，无外部依赖
- ✅ **无法律风险** - 只使用官方开源模型
- ✅ **自动模型管理** - 自动下载、缓存、加载
- ✅ **文生图** - SD-Turbo/SDXL-Turbo/SD-v1.5/SD-v2.1
- ✅ **图生图** - Img2Img/Inpaint 支持
- ✅ **文生视频** - 多帧合成视频
- ✅ **智能优化** - 自动选择最佳参数

---

## 🚀 快速开始

### 安装

```bash
# 1. 安装依赖
pip install stable-diffusion-cpp-python pillow numpy

# 2. 安装 FFmpeg（视频必需）
brew install ffmpeg  # macOS
apt install ffmpeg   # Linux

# 3. 运行
python3 markhub_v6_1.py -p "一位美丽的女性"
```

### 生成图片

```bash
# 基础用法（SD-Turbo，1 步）
python3 markhub_v6_1.py -p "一只猫"

# 高质量（SDXL-Turbo）
python3 markhub_v6_1.py -p "人像" -m sdxl-turbo

# 自定义参数
python3 markhub_v6_1.py -p "风景" --width 1024 --height 1024 --steps 30
```

### 生成视频

```bash
# 10 秒视频
python3 markhub_v6_1.py -p "海浪" --video --duration 10

# 自定义 FPS
python3 markhub_v6_1.py -p "日落" --video --duration 5 --fps 30
```

### 自动模式

```bash
# 自动选择最佳模型
python3 markhub_v6_1.py -p "一位女性的肖像" --auto
```

---

## 📦 可用模型

| 模型 | 类型 | 分辨率 | 步数 | 大小 | 用途 |
|------|------|--------|------|------|------|
| **sd-turbo** | txt2img | 512×512 | 1 | 1.4GB | 快速生成 |
| **sdxl-turbo** | txt2img | 1024×1024 | 1 | 6GB | 高质量人像 |
| **stable-diffusion-v1-5** | txt2img | 512×512 | 20 | 4GB | 通用 |
| **stable-diffusion-v2-1** | txt2img | 768×768 | 20 | 5GB | 高分辨率 |

---

## 📝 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-p, --prompt` | 提示词（必需） | - |
| `-n, --negative` | 负面提示词 | "" |
| `-m, --model` | 模型名称 | sd-turbo |
| `--video` | 生成视频 | False |
| `--duration` | 视频时长（秒） | 10 |
| `--fps` | 视频帧率 | 24 |
| `--auto` | 自动模式 | False |
| `--width` | 图片宽度 | 512 |
| `--height` | 图片高度 | 512 |
| `--steps` | 采样步数 | 自动 |
| `--cfg` | CFG 比例 | 自动 |
| `-o, --output` | 输出路径 | 自动生成 |

---

## 📤 输出

- **图片：** `~/Videos/MarkHub/MarkHub_YYYYMMDD_HHMMSS.png`
- **视频：** `~/Videos/MarkHub/MarkHub_Video_YYYYMMDD_HHMMSS.mp4`

---

## 🎯 示例

### 高质量人像

```bash
python3 markhub_v6_1.py \
  -p "美丽的女性肖像，专业摄影，摄影棚灯光" \
  -m sdxl-turbo \
  --width 1024 \
  --height 1024
```

### 风景图片

```bash
python3 markhub_v6_1.py \
  -p "美丽的风景，山脉，湖泊，日落，4k" \
  -m stable-diffusion-v2-1 \
  --width 768 \
  --height 768 \
  --steps 30
```

### 舞蹈视频

```bash
python3 markhub_v6_1.py \
  -p "优雅跳舞的女性，飘逸的裙子，电影感" \
  --video \
  --duration 10 \
  --fps 24
```

### 自动创作

```bash
python3 markhub_v6_1.py \
  -p "玩毛线的猫" \
  --auto
```

---

## ⚖️ 法律说明

### ✅ 合法使用

本技能只使用官方开源模型：
- **SD-Turbo** - Stability AI（Apache 2.0 许可）
- **SDXL-Turbo** - Stability AI（Apache 2.0 许可）
- **Stable Diffusion v1.5** - Stability AI（CreativeML Open RAIL-M）
- **Stable Diffusion v2.1** - Stability AI（CreativeML Open RAIL-M）

所有模型均来自 HuggingFace 官方仓库，无法律风险。

### ❌ 禁止使用

- 不要生成侵权内容
- 不要生成违法内容
- 不要侵犯肖像权
- 遵守当地法律法规

---

## 🔧 故障排除

### Q: 模型下载失败

**A:** 检查网络或使用镜像：

```bash
export HF_ENDPOINT=https://hf-mirror.com
python3 markhub_v6_1.py -p "测试"
```

### Q: 内存不足

**A:** 使用更小的模型或分辨率：

```bash
python3 markhub_v6_1.py -p "测试" -m sd-turbo --width 256 --height 256
```

### Q: 生成速度慢

**A:** 使用 Turbo 模型：

```bash
python3 markhub_v6_1.py -p "测试" -m sd-turbo
```

### Q: FFmpeg 未找到

**A:** 安装 FFmpeg：

```bash
brew install ffmpeg  # macOS
apt install ffmpeg   # Linux
```

---

## 📊 性能参考

### 生成速度（M2 Pro）

| 模型 | 分辨率 | 步数 | 单张时间 |
|------|--------|------|---------|
| SD-Turbo | 512×512 | 1 | ~2 秒 |
| SDXL-Turbo | 1024×1024 | 1 | ~5 秒 |
| SD-v1.5 | 512×512 | 20 | ~30 秒 |
| SD-v2.1 | 768×768 | 20 | ~60 秒 |

### 视频生成

| 时长 | FPS | 帧数 | 总时间（SD-Turbo） |
|------|-----|------|------------------|
| 5 秒 | 24 | 120 | ~4 分钟 |
| 10 秒 | 24 | 240 | ~8 分钟 |
| 10 秒 | 30 | 300 | ~10 分钟 |

---

## 📁 文件结构

- `markhub_v6_1.py` - 主程序
- `README.md` - 英文文档
- `README_CN.md` - 本文档（中文）
- `SKILL.md` - 技能定义
- `install.sh` - 安装脚本
- `clawhub.json` - ClawHub 配置

---

## 🔄 更新日志

### v6.1 (2026-03-20)
- ✅ 完整重写，全英文文档
- ✅ 改进错误处理
- ✅ 更好的模型管理
- ✅ 视频生成优化
- ✅ 自动模型选择

### v6.0 (2026-03-20)
- ✅ 完全本地版本
- ✅ 不依赖 ComfyUI
- ✅ 无法律风险

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- **Stability AI** - 开源模型
- **stable-diffusion-cpp-python** - C++ 后端
- **FFmpeg** - 视频合成

---

**版本：** v6.1.0  
**发布日期：** 2026-03-20  
**作者：** 1 号小虫子  
**GitHub:** https://github.com/yun520-1/markhub-skill
