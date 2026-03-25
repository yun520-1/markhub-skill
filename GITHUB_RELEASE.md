# 🎉 MarkHub v8.0 发布 - 完全本地化 AI 短视频创作系统

**发布日期**: 2026-03-25  
**版本**: v8.0.0  
**类型**: 重大更新

---

## 🚀 主要特性

### 完全本地化
- ✅ **无远程依赖** - 完全离线运行，无需联网
- ✅ **隐私保护** - 所有数据本地处理，不上传云端
- ✅ **无需 API Key** - 默认本地模式，无 API 泄露风险
- ✅ **本地 AI** - 支持 Ollama/LM Studio 本地大模型

### 核心功能
- ✅ **文案自动生成** - 本地 AI 生成视频文案
- ✅ **素材智能匹配** - 本地素材库管理
- ✅ **字幕自动生成** - 本地 Whisper 字幕
- ✅ **语音合成** - 本地 Piper TTS
- ✅ **批量生成** - 一次生成多个视频
- ✅ **多尺寸支持** - 竖屏 9:16/横屏 16:9/方形 1:1

### 安全特性
- ✅ **无远程依赖** - 不依赖任何远程服务器
- ✅ **隐私保护** - 数据完全本地
- ✅ **版权合规** - 严格审核素材来源
- ✅ **配置安全** - 支持环境变量和加密存储

---

## 📦 安装方法

### 方法 1: 从 ClawHub 安装（推荐）

```bash
clawhub install markhub-v8
```

### 方法 2: 源码安装

```bash
# 1. 克隆仓库
git clone https://github.com/yun520-1/markhub-skill.git
cd markhub-skill/markhub-v8

# 2. 安装依赖
pip install requests pillow numpy edge-tts openai-whisper ffmpeg-python

# 3. 安装本地 AI（可选）
pip install stable-diffusion-cpp-python

# 4. 安装本地语音（可选）
pip install piper-tts

# 5. 配置
cp config.example.toml config.toml
# 编辑配置文件

# 6. 运行
python3 markhub_v8.py -p "生命的意义是什么" --offline
```

---

## 🎯 快速开始

### 完全离线模式

```bash
# 无需联网，完全本地生成
python3 markhub_v8.py \
  -p "3 个习惯让你更自信" \
  --aspect portrait \
  --duration 30 \
  --offline
```

### 使用本地 AI

```bash
# 1. 安装 Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. 下载模型
ollama pull qwen2.5:7b

# 3. 生成视频
python3 markhub_v8.py \
  -p "如何保持积极心态" \
  --local-llm \
  --offline
```

### 批量生成

```bash
# 创建 subjects.txt 文件
echo "生命的意义
为什么要运动
如何学习新技能" > subjects.txt

# 批量生成
python3 markhub_v8.py --batch subjects.txt --offline
```

---

## ⚙️ 配置说明

### 完全本地模式（推荐）

```toml
# config.toml
[app]
offline_mode = true

[llm]
mode = "local"
local_model = "qwen2.5:7b"
local_url = "http://localhost:11434"

[tts]
mode = "local"
voice = "zh-CN-Xiaoxiao"

[materials]
local_library = "~/Videos/Materials"
```

### 混合模式（可选）

```toml
[app]
offline_mode = false
prefer_local = true

[llm]
mode = "hybrid"
local_model = "qwen2.5:7b"

[llm.backup]
provider = "deepseek"
api_key = "${DEEPSEEK_API_KEY}"
```

---

## 📊 输出规格

### 视频尺寸

| 尺寸 | 分辨率 | 用途 |
|------|--------|------|
| **竖屏 9:16** | 1080×1920 | 抖音/TikTok/Reels |
| **横屏 16:9** | 1920×1080 | YouTube/B 站/西瓜 |
| **方形 1:1** | 1080×1080 | Instagram/朋友圈 |

### 视频格式

- **编码**: H.264
- **封装**: MP4
- **帧率**: 24/30/60 FPS
- **音频**: AAC 128kbps

---

## 🔒 安全与合规

### 隐私保护

- ✅ 所有数据本地处理
- ✅ 不上传任何内容到云端
- ✅ 不收集用户信息
- ✅ 不追踪使用行为

### 版权合规

- ✅ 本地素材库（用户自备版权）
- ✅ CC0 无版权素材
- ✅ 开源音乐和字体
- ✅ 明确用户责任

### 禁止行为

- ❌ 生成侵权内容
- ❌ 生成违法内容
- ❌ 侵犯他人肖像权
- ❌ 违反法律法规

---

## 🆚 与 v7.0 对比

| 特性 | v7.0 | v8.0 | 改进 |
|------|------|------|------|
| **ComfyUI 远程** | ✅ | ❌ | 去除风险 |
| **远程依赖** | 是 | 否 | ✅ |
| **API Key 必需** | 是 | 否 | ✅ |
| **隐私保护** | 中 | 高 | ✅ |
| **安全风险** | 中 | 低 | ✅ |
| **离线使用** | 部分 | 完全 | ✅ |

---

## 📝 依赖要求

### 系统要求

- **操作系统**: Windows 10+ / macOS 11+ / Linux
- **Python**: 3.11+
- **CPU**: 4 核或以上（推荐 8 核）
- **内存**: 4GB 或以上（推荐 8GB）
- **磁盘**: 10GB 可用空间
- **GPU**: 非必须（推荐用于本地 AI）

### Python 依赖

```txt
requests
pillow
numpy
edge-tts (可选)
openai-whisper (可选)
piper-tts (可选)
stable-diffusion-cpp-python (可选)
```

### 系统依赖

- **FFmpeg**: 视频处理
- **Ollama**: 本地大模型（可选）

---

## 🐛 常见问题

### Q1: 如何完全离线使用？

**A**: 配置本地模式并使用 `--offline` 参数：

```toml
[app]
offline_mode = true

[llm]
mode = "local"
local_model = "qwen2.5:7b"
```

```bash
python3 markhub_v8.py -p "test" --offline
```

### Q2: 本地模型如何安装？

**A**: 使用 Ollama：

```bash
# 安装 Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 下载模型
ollama pull qwen2.5:7b

# 配置
[llm]
mode = "local"
local_model = "qwen2.5:7b"
```

### Q3: 如何组织本地素材？

**A**: 创建素材库目录：

```bash
mkdir -p ~/Videos/Materials/{Videos,Images,Music}
```

```toml
[materials]
local_library = "~/Videos/Materials"
auto_organize = true
```

---

## 📚 文档链接

- **完整文档**: [SKILL.md](SKILL.md)
- **升级报告**: [UPGRADE_REPORT.md](UPGRADE_REPORT.md)
- **GitHub**: https://github.com/yun520-1/markhub-skill
- **ClawHub**: https://clawhub.ai/yun520-1/markhub-v8

---

## 🎯 使用示例

### 励志短视频

```bash
python3 markhub_v8.py \
  -p "3 个习惯让你更自信" \
  --aspect portrait \
  --duration 30 \
  --offline
```

### 知识分享视频

```bash
python3 markhub_v8.py \
  -p "量子力学入门" \
  --aspect landscape \
  --duration 120 \
  --local-llm
```

### 旅行日记

```bash
python3 markhub_v8.py \
  -p "云南旅行日记" \
  --local-footage ~/Videos/Yunnan/ \
  --bgm ~/Music/travel.mp3
```

---

## 🙏 致谢

感谢以下开源项目：

- **Ollama** - 本地大模型运行
- **Piper TTS** - 本地语音合成
- **Whisper** - 本地字幕生成
- **FFmpeg** - 视频处理
- **Stable Diffusion** - 本地 AI 图像生成

---

## 📄 许可证

MIT License

---

## 🎉 开始使用

```bash
# 安装
clawhub install markhub-v8

# 使用
python3 markhub_v8.py -p "生命的意义是什么" --offline
```

**祝你使用愉快！** 🚀

---

**发布者**: 1 号小虫子  
**发布日期**: 2026-03-25  
**GitHub**: https://github.com/yun520-1/markhub-skill/releases/tag/v8.0.0
