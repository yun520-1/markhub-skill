# MarkHub 独立版使用指南

## 🎯 快速开始（3 步完成）

### 第 1 步：安装 stable-diffusion.cpp

```bash
python3 markhub_standalone.py --install-sd-cpp
```

这将：
- 克隆 stable-diffusion.cpp 仓库
- 使用 CMake 配置（启用 Metal GPU 加速）
- 编译生成 `sd-cli` 工具

预计用时：5-10 分钟

### 第 2 步：下载模型

```bash
python3 markhub_standalone.py --download-models
```

这将下载 3 个模型文件（共约 11GB）：
- `z_image_turbo-Q8_0.gguf` (~6.7GB) - UNet 模型
- `Qwen3-4B-Q8_0.gguf` (~4.0GB) - CLIP 模型
- `ae.safetensors` (~0.3GB) - VAE 模型

预计用时：10-30 分钟（取决于网络速度）

### 第 3 步：生成图片

```bash
python3 markhub_standalone.py
```

默认生成"宇宙女神"图片，分辨率 2048x1024。

---

## 📖 完整命令参考

### 安装和配置

```bash
# 检查安装状态
python3 markhub_standalone.py --check

# 安装 stable-diffusion.cpp
python3 markhub_standalone.py --install-sd-cpp

# 下载所有模型
python3 markhub_standalone.py --download-models

# 运行测试
python3 test_standalone.py
```

### 生成图片

```bash
# 使用默认参数生成
python3 markhub_standalone.py

# 自定义提示词
python3 markhub_standalone.py -p "A beautiful landscape"

# 完整参数
python3 markhub_standalone.py \
  -p "A magnificent cosmic goddess floating in deep space" \
  -t "宇宙女神" \
  -W 2048 \
  -H 1024 \
  -s 20 \
  -c 7.0 \
  --seed 12345
```

### 参数说明

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--prompt` | `-p` | 无 | 提示词（必需） |
| `--title` | `-t` | "image" | 输出文件标题 |
| `--width` | `-W` | 2048 | 图片宽度 |
| `--height` | `-H` | 1024 | 图片高度 |
| `--steps` | `-s` | 20 | 采样步数 |
| `--cfg` | `-c` | 7.0 | CFG 引导值 |
| `--seed` | 无 | -1 | 随机种子（-1=随机） |
| `--check` | 无 | 无 | 检查安装状态 |
| `--download-models` | 无 | 无 | 下载所有模型 |
| `--install-sd-cpp` | 无 | 无 | 安装 stable-diffusion.cpp |

---

## 🎨 提示词示例

### 人物

```bash
# 宇宙女神
python3 markhub_standalone.py \
  -p "A magnificent cosmic goddess floating in deep space, surrounded by nebulae and stars, galaxy dress, cosmic energy, ethereal beauty, divine light, universe background, nebula clouds, stardust, celestial aura, hyperdetailed, cinematic lighting, 8k quality" \
  -t "宇宙女神"

# 月光女神
python3 markhub_standalone.py \
  -p "A beautiful moon goddess standing on a crescent moon, wearing a flowing silver dress made of moonlight, long silvery hair glowing with lunar energy, serene expression, surrounded by stars and night sky, ethereal beauty, divine light, magical atmosphere, hyperdetailed, cinematic lighting, 8k quality" \
  -t "月光女神"

# 人像摄影
python3 markhub_standalone.py \
  -p "Beautiful portrait, professional photography, studio lighting, high quality, detailed, soft focus, natural makeup, elegant pose" \
  -t "人像"
```

### 风景

```bash
# 日落
python3 markhub_standalone.py \
  -p "Beautiful landscape, sunset over mountains, lake reflection, golden hour, cinematic, high quality, detailed, warm colors, peaceful atmosphere" \
  -t "日落"

# 雪山
python3 markhub_standalone.py \
  -p "Majestic snow mountain peak, blue sky, clouds, pristine nature, winter landscape, photorealistic, detailed, 8k quality" \
  -t "雪山"
```

### 艺术

```bash
# 抽象艺术
python3 markhub_standalone.py \
  -p "Abstract art, colorful, artistic, creative, flowing shapes, vibrant colors, modern art style, high quality, detailed" \
  -t "抽象艺术"

# 赛博朋克
python3 markhub_standalone.py \
  -p "Cyberpunk city, neon lights, futuristic buildings, flying cars, rain, reflections, dark atmosphere, sci-fi, detailed, 8k quality" \
  -t "赛博朋克城市"
```

---

## 🐛 故障排除

### 问题 1: 模型下载失败

**错误信息：**
```
❌ 模型下载失败：Connection timeout
```

**解决方案：**
```bash
# 使用镜像站
export HF_ENDPOINT=https://hf-mirror.com
python3 markhub_standalone.py --download-models

# 或者手动下载
# 访问 https://huggingface.co/leejet/z_image_turbo-gguf
# 下载模型文件到 ~/.markhub/models/
```

### 问题 2: 编译失败

**错误信息：**
```
❌ make 失败：error: ...
```

**解决方案：**
```bash
# 安装 Xcode Command Line Tools
xcode-select --install

# 重新编译
python3 markhub_standalone.py --install-sd-cpp
```

### 问题 3: 内存不足

**错误信息：**
```
❌ 生成失败：out of memory
```

**解决方案：**
```bash
# 降低分辨率
python3 markhub_standalone.py -p "..." -W 1024 -H 512

# 减少步数
python3 markhub_standalone.py -p "..." -s 10
```

### 问题 4: 生成速度慢

**解决方案：**
```bash
# 使用更少的步数（10-15 步通常足够）
python3 markhub_standalone.py -p "..." -s 10

# 降低分辨率
python3 markhub_standalone.py -p "..." -W 1024 -H 512
```

### 问题 5: 图片质量问题

**问题：图片过暗**
```bash
# 在提示词中添加亮度相关描述
python3 markhub_standalone.py \
  -p "..., bright lighting, well-lit, vibrant colors" \
  -p "..."
```

**问题：图片模糊**
```bash
# 增加步数
python3 markhub_standalone.py -p "..." -s 25

# 提高 CFG 值
python3 markhub_standalone.py -p "..." -c 8.0
```

---

## 📊 性能参考

### 生成时间（Mac M 系列芯片）

| 分辨率 | 步数 | 预计时间 |
|--------|------|----------|
| 1024x512 | 10 | ~20 秒 |
| 1024x512 | 20 | ~40 秒 |
| 2048x1024 | 10 | ~45 秒 |
| 2048x1024 | 20 | ~90 秒 |

### 文件大小

| 分辨率 | 文件大小（约） |
|--------|----------------|
| 1024x512 | 0.5-1 MB |
| 2048x1024 | 2-4 MB |

---

## 🔧 高级配置

### 修改默认参数

编辑 `markhub_standalone.py` 中的 `Config` 类：

```python
class Config:
    # 默认分辨率
    DEFAULT_WIDTH = 2048
    DEFAULT_HEIGHT = 1024
    
    # 默认步数
    DEFAULT_STEPS = 20
    
    # 默认 CFG
    DEFAULT_CFG = 7.0
    
    # 默认 Sampler
    DEFAULT_SAMPLER = "euler"
```

### 修改模型存储位置

```python
class Config:
    # 修改为其他目录
    BASE_DIR = Path("/Volumes/ExternalDrive/.markhub")
```

### 添加自定义预设

编辑 `auto_generate` 方法：

```python
presets = {
    "my_custom": [
        {"title": "我的主题", "prompt": "你的提示词..."}
    ]
}
```

---

## 📁 目录结构

```
~/.markhub/
├── models/              # 模型文件
│   ├── z_image_turbo-Q8_0.gguf
│   ├── Qwen3-4B-Q8_0.gguf
│   └── ae.safetensors
├── logs/                # 日志文件
│   └── markhub_20260318.log
└── cache/               # 缓存文件

~/Downloads/markhub_output/  # 输出图片
├── 宇宙女神_20260318_093000.png
└── 月光女神_20260318_094500.png
```

---

## 📝 日志查看

```bash
# 查看最新日志
cat ~/.markhub/logs/markhub_$(date +%Y%m%d).log

# 实时查看日志
tail -f ~/.markhub/logs/markhub_$(date +%Y%m%d).log
```

---

## 🆘 获取帮助

### 智能错误解决

MarkHub 会自动搜索解决方案！当遇到错误时，查看输出中的：

```
💡 建议的解决方案:

  来自 GitHub:
    - [相关 Issue 标题]
      [Issue 链接]
  
  来自 常见解决方案:
    - [问题描述]
      [解决方法]
```

### 手动搜索

**GitHub Issues:**
https://github.com/leejet/stable-diffusion.cpp/issues

**ClawHub Skills:**
https://clawhub.ai/skills?q=image-generation

---

## 📞 支持

- **GitHub:** https://github.com/yun520-1/markhub-skill
- **ClawHub:** https://clawhub.ai/yun520-1/markhub
- **stable-diffusion.cpp:** https://github.com/leejet/stable-diffusion.cpp

---

## 📄 许可证

MIT-0 - 自由使用、修改、分发，无需署名
