# MarkHub v2.0.0 - 独立版发布说明

## 🎉 重大更新

**MarkHub 现在完全独立运行，不再依赖 ComfyUI 服务器！**

---

## ✨ 新功能

### 1. 独立运行模式
- ❌ 不再需要 ComfyUI 服务器
- ✅ 直接使用 stable-diffusion.cpp 本地生成
- ✅ 所有模型自动下载到 `~/.markhub/models/`

### 2. 自动下载模型
```bash
python3 markhub_standalone.py --download-models
```
自动下载：
- z_image_turbo-Q8_0.gguf (~6.7GB)
- Qwen3-4B-Q8_0.gguf (~4.0GB)
- ae.safetensors (~0.3GB)

### 3. 自动安装 stable-diffusion.cpp
```bash
python3 markhub_standalone.py --install-sd-cpp
```
自动完成：
- Git 克隆仓库
- CMake 配置
- Make 编译（支持 Metal GPU 加速）

### 4. 智能错误解决 🧠
遇到问题时自动：
1. 分析错误信息
2. **搜索 GitHub Issues** 找解决方案
3. **搜索 ClawHub** 找相关技能
4. 提供常见错误的解决建议

**示例：**
```
❌ 生成失败：model file not found

💡 建议的解决方案:

  来自 GitHub:
    - Model loading issues in stable-diffusion.cpp
      https://github.com/leejet/stable-diffusion.cpp/issues/123
  
  来自 常见解决方案:
    - 模型文件未找到
      运行 'python3 markhub_api.py --download-models' 下载所需模型
```

### 5. 增强的命令行接口
```bash
# 检查安装状态
python3 markhub_standalone.py --check

# 下载所有模型
python3 markhub_standalone.py --download-models

# 安装 stable-diffusion.cpp
python3 markhub_standalone.py --install-sd-cpp

# 生成单张图片
python3 markhub_standalone.py \
  -p "A beautiful cosmic goddess" \
  -t "宇宙女神" \
  -W 2048 -H 1024 \
  -s 20 -c 7.0 \
  --seed 12345

# 全自动生成（默认）
python3 markhub_standalone.py
```

### 6. 资源监控
实时显示：
- CPU 使用率
- 内存使用量
- 生成进度

### 7. 质量验证
自动生成后验证：
- 尺寸检查
- 亮度检测（20-240）
- 对比度检测（>30）
- 文件大小检查（>100KB）

---

## 🔄 重大变更

### 从 v1.0.0 升级

**v1.0.0 (旧版):**
- ❌ 依赖 ComfyUI 服务器
- ❌ 模型放在 ComfyUI 目录
- ❌ 需要手动配置工作流

**v2.0.0 (新版):**
- ✅ 完全独立运行
- ✅ 模型自动管理在 `~/.markhub/models/`
- ✅ 一键安装和配置

### 文件变更

| 文件 | 状态 | 说明 |
|------|------|------|
| `markhub_standalone.py` | ✅ 新增 | 独立版主程序 |
| `markhub_api.py` | ⚠️ 保留 | ComfyUI API 版（兼容旧用户） |
| `markhub.py` | ⚠️ 保留 | 原始版本 |
| `SKILL.md` | ✅ 更新 | 反映新功能 |
| `skill.json` | ✅ 更新 | v2.0.0 |

---

## 📦 安装要求

### 系统要求
- macOS (支持 Metal GPU 加速)
- Python 3.8+
- Git
- CMake

### 自动安装依赖
```bash
# Python 依赖（自动安装）
pip install requests pillow numpy psutil

# 系统依赖（自动编译）
# - stable-diffusion.cpp (Metal 支持)
```

---

## 🚀 快速开始

### 全新安装
```bash
# 1. 克隆或安装技能
npx clawhub@latest install markhub

# 2. 安装 stable-diffusion.cpp
cd ~/.jvs/.openclaw/workspace/skills/markhub
python3 markhub_standalone.py --install-sd-cpp

# 3. 下载模型
python3 markhub_standalone.py --download-models

# 4. 生成第一张图片
python3 markhub_standalone.py -p "A beautiful cosmic goddess" -t "宇宙女神"
```

### 从 v1.0.0 升级
```bash
# 1. 更新技能
npx clawhub@latest update markhub

# 2. 下载新模型（如果需要）
python3 markhub_standalone.py --download-models

# 3. 开始使用独立版
python3 markhub_standalone.py
```

---

## 💡 使用示例

### 示例 1: 生成宇宙女神
```bash
python3 markhub_standalone.py \
  -p "A magnificent cosmic goddess floating in deep space, surrounded by nebulae and stars, galaxy dress, cosmic energy, ethereal beauty, divine light, universe background, nebula clouds, stardust, celestial aura, hyperdetailed, cinematic lighting, 8k quality" \
  -t "宇宙女神" \
  -W 2048 -H 1024
```

### 示例 2: 批量生成
```python
from markhub_standalone import MarkHub

hub = MarkHub()

prompts = [
    {"title": "宇宙女神", "prompt": "A cosmic goddess..."},
    {"title": "月光女神", "prompt": "A moon goddess..."},
    {"title": "风景日落", "prompt": "Beautiful landscape..."}
]

for item in prompts:
    hub.generate_image(item["prompt"], item["title"])
```

### 示例 3: 检查状态
```bash
python3 markhub_standalone.py --check
```

输出：
```
📦 检查模型文件...
  ✅ unet: z_image_turbo-Q8_0.gguf (6.73GB)
  ✅ clip: Qwen3-4B-Q8_0.gguf (3.99GB)
  ✅ vae: ae.safetensors (0.31GB)
✅ stable-diffusion.cpp 已安装
```

---

## 🐛 常见问题

### Q: 下载模型很慢怎么办？
A: 模型从 HuggingFace 下载，可以使用镜像：
```bash
# 使用镜像站（如果可用）
export HF_ENDPOINT=https://hf-mirror.com
python3 markhub_standalone.py --download-models
```

### Q: 编译 stable-diffusion.cpp 失败？
A: 确保安装了 Xcode Command Line Tools：
```bash
xcode-select --install
```

### Q: 生成速度慢？
A: 可以降低分辨率或步数：
```bash
python3 markhub_standalone.py -p "..." -W 1024 -H 512 -s 10
```

### Q: 遇到错误怎么办？
A: MarkHub 会自动搜索解决方案！查看输出中的 "💡 建议的解决方案" 部分。

---

## 📊 性能对比

| 任务 | v1.0.0 (ComfyUI) | v2.0.0 (独立) |
|------|------------------|---------------|
| 启动时间 | ~30 秒 | ~5 秒 |
| 内存占用 | ~8GB | ~6GB |
| 生成速度 (2048x1024, 20 步) | ~60 秒 | ~55 秒 |
| 配置复杂度 | 中 | 低 |

---

## 🔗 相关链接

- **GitHub:** https://github.com/yun520-1/markhub-skill
- **ClawHub:** https://clawhub.ai/yun520-1/markhub
- **stable-diffusion.cpp:** https://github.com/leejet/stable-diffusion.cpp

---

## 📝 许可证

MIT-0 - 自由使用、修改、分发，无需署名

---

**发布时间：** 2026-03-18  
**作者：** yun520-1  
**版本：** 2.0.0
