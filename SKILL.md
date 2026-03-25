# MarkHub v8.0 - 本地 AI 短视频创作系统

**完全本地化 · 无远程依赖 · 无安全风险 · 隐私保护**

## 🎯 核心功能

### AI 短视频生成
- ✅ **文案自动生成** - 本地/云端 AI 大模型生成视频文案
- ✅ **素材智能匹配** - 无版权视频/图片素材库
- ✅ **字幕自动生成** - Edge TTS/Whisper 字幕
- ✅ **语音合成** - 多种语音引擎
- ✅ **背景音乐** - 无版权音乐库
- ✅ **批量生成** - 一次生成多个视频
- ✅ **多尺寸支持** - 竖屏 9:16、横屏 16:9、方形 1:1

### 本地 AI 创作
- ✅ **文生图** - SD-Turbo/SDXL-Turbo 快速生成
- ✅ **图生图** - 图片编辑和增强
- ✅ **文生视频** - 多帧合成短视频
- ✅ **完全本地** - 无需联网即可使用

### 安全特性
- ✅ **无远程依赖** - 不依赖任何远程服务器
- ✅ **隐私保护** - 所有数据本地处理
- ✅ **无 API 泄露风险** - 敏感信息本地存储
- ✅ **版权合规** - 严格审核素材来源

## 📦 系统架构

```
MarkHub v8.0
├── 文案生成层
│   ├── 本地模型（Ollama/LM Studio）
│   ├── 云端 API（可选：DeepSeek/Qwen/OpenAI）
│   └── 文案模板库
├── 素材匹配层
│   ├── 本地素材库（用户自备）
│   ├── Pexels API（可选）
│   ├── Pixabay API（可选）
│   └── Unsplash API（可选）
├── 语音合成层
│   ├── Edge TTS（免费，需联网）
│   ├── 本地 TTS（Piper/Mimic3）
│   └── 离线语音包
├── 字幕生成层
│   ├── Edge 字幕（快速）
│   ├── Whisper 本地字幕
│   └── 字幕样式定制
├── 视频合成层
│   ├── FFmpeg 合成
│   ├── 转场效果
│   └── 音画同步
└── 本地 AI 层
    ├── SD-Turbo/SDXL-Turbo
    ├── 文生图/图生图
    └── 文生视频
```

## 🚀 快速开始

### 安装依赖

```bash
# 1. 基础依赖
pip install requests pillow numpy

# 2. 语音合成（可选联网）
pip install edge-tts

# 3. 本地语音（离线）
pip install piper-tts

# 4. 字幕生成（本地）
pip install openai-whisper

# 5. 视频处理
brew install ffmpeg  # macOS
apt install ffmpeg   # Linux

# 6. 本地 AI（可选）
pip install stable-diffusion-cpp-python
```

### 配置文件

创建 `config.toml`：

```toml
# 大模型配置（可选云端或本地）
[llm]
# 本地模式（推荐，隐私保护）
mode = "local"
local_model = "qwen2.5:7b"
local_url = "http://localhost:11434"

# 云端模式（可选）
# mode = "cloud"
# provider = "deepseek"
# api_key = "your_api_key"

# 素材配置（可选在线或本地）
[materials]
# 本地素材库（推荐）
local_library = "~/Videos/Materials"

# 在线 API（可选，需要时启用）
# pexels_api_keys = []
# pixabay_api_key = ""
# unsplash_api_key = ""

# 语音配置
[tts]
# 本地语音（离线）
mode = "local"
voice = "zh-CN-Xiaoxiao"

# Edge TTS（需联网）
# mode = "edge"
# voice = "zh-CN-XiaoxiaoNeural"

# 字幕配置
[subtitle]
mode = "whisper"  # whisper/edge
language = "zh"
font = "SimHei"
font_size = 48

# 视频配置
[video]
default_aspect = "portrait"
default_duration = 60
fps = 30
output_dir = "~/Videos/MarkHub"
```

### 生成视频

```bash
# 完全本地模式（无需联网）
python3 markhub_v8.py -p "生命的意义是什么" --offline

# 使用本地 AI 生成文案
python3 markhub_v8.py -p "如何保持积极心态" --local-llm

# 使用本地素材库
python3 markhub_v8.py -p "旅行日记" --local-footage

# 批量生成（本地处理）
python3 markhub_v8.py --batch subjects.txt --offline

# 自动模式（优先本地）
python3 markhub_v8.py -p "为什么要运动" --auto
```

## 🎨 使用方式

### 方式 1: 命令行（推荐）

```bash
# 竖屏短视频（抖音/TikTok）
python3 markhub_v8.py \
  -p "3 个习惯让你更自信" \
  --aspect portrait \
  --duration 30 \
  --offline

# 横屏长视频（YouTube/B 站）
python3 markhub_v8.py \
  -p "量子力学入门" \
  --aspect landscape \
  --duration 120 \
  --local-llm
```

### 方式 2: Python API

```python
from markhub_v8 import generate_video

# 本地模式（离线）
result = generate_video(
    subject="如何学习新技能",
    aspect="portrait",
    duration=60,
    offline=True
)

print(f"视频路径：{result['video_path']}")

# 批量生成
subjects = ["生命的意义", "金钱的作用", "为什么要运动"]
for subject in subjects:
    result = generate_video(subject=subject, offline=True)
    print(f"{subject}: {result['video_path']}")
```

### 方式 3: 本地 Web 界面

```bash
# 启动本地 Web UI（无需联网）
python3 markhub_v8.py --webui --offline

# 访问浏览器
http://localhost:8501
```

## 🔒 安全特性

### 1. 无远程依赖

**完全本地化**:
- ✅ 文案生成：本地 Ollama/LM Studio
- ✅ 语音合成：本地 Piper/Mimic3
- ✅ 字幕生成：本地 Whisper
- ✅ 素材匹配：本地素材库
- ✅ 视频合成：本地 FFmpeg
- ❌ 不依赖任何远程服务器
- ❌ 不需要 API Key
- ❌ 不会泄露隐私

### 2. 隐私保护

**数据安全**:
- ✅ 所有数据本地存储
- ✅ 不上传任何内容到云端
- ✅ 不收集用户信息
- ✅ 不追踪使用行为
- ✅ 加密存储敏感配置

### 3. 版权合规

**素材来源**:
- ✅ 本地素材库（用户自备版权）
- ✅ CC0 无版权素材（可选）
- ✅ 开源音乐库
- ✅ 开源字体
- ❌ 不使用未授权素材

### 4. 配置安全

**敏感信息管理**:
```toml
# 推荐：使用环境变量
[llm]
api_key = "${DEEPSEEK_API_KEY}"  # 从环境变量读取

# 或使用加密存储
[security]
encrypt_config = true
```

## 📝 配置说明

### 本地模式（推荐）

```toml
# 完全离线模式
[app]
offline_mode = true

# 本地大模型
[llm]
mode = "local"
local_model = "qwen2.5:7b"
local_url = "http://localhost:11434"

# 本地语音
[tts]
mode = "local"
voice = "zh-CN-Xiaoxiao"

# 本地素材
[materials]
local_library = "~/Videos/Materials"
```

### 混合模式（可选）

```toml
# 本地优先，云端备用
[app]
offline_mode = false
prefer_local = true

# 本地模型
[llm]
mode = "hybrid"
local_model = "qwen2.5:7b"

# 云端备用
[llm.backup]
provider = "deepseek"
api_key = "${DEEPSEEK_API_KEY}"

# 本地语音
[tts]
mode = "local"

# Edge 备用
[tts.backup]
mode = "edge"
```

### 素材管理

```toml
# 本地素材库
[materials]
local_library = "~/Videos/Materials"
auto_organize = true

# 素材分类
[materials.categories]
videos = "~/Videos/Materials/Videos"
images = "~/Videos/Materials/Images"
music = "~/Videos/Materials/Music"

# 自动标签
[materials.auto_tag]
enabled = true
model = "clip-vit-base"
```

## 🎬 完整工作流

```
1. 输入主题
   ↓
2. 本地 AI 生成文案
   ├─ Ollama/LM Studio
   ├─ 文案分段
   └─ 关键词提取
   ↓
3. 本地素材匹配
   ├─ 本地素材库搜索
   ├─ 智能排序
   └─ 自动选择
   ↓
4. 本地语音合成
   ├─ Piper TTS
   ├─ 语速调节
   └─ 情感控制
   ↓
5. 本地字幕生成
   ├─ Whisper 本地
   ├─ 时间轴对齐
   └─ 样式定制
   ↓
6. 本地视频合成
   ├─ FFmpeg
   ├─ 转场效果
   └─ 音画同步
   ↓
7. 本地输出
   ├─ 多尺寸渲染
   ├─ 质量优化
   └─ 自动保存
```

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
- **码率**: 5-20 Mbps（可调）
- **音频**: AAC 128kbps

### 字幕格式

- **格式**: SRT/ASS（可选）
- **编码**: UTF-8
- **字体**: 可自定义
- **位置**: 底部/顶部/居中

## ⚖️ 版权与法律

### ✅ 合规使用

本系统严格遵守法律法规：

1. **素材来源**
   - 本地素材库（用户自备版权）
   - CC0 无版权素材（可选）
   - 开源素材库

2. **音乐使用**
   - 本地音乐（用户自备）
   - 开源音乐库
   - CC0 音乐

3. **字体使用**
   - 开源字体（思源黑体等）
   - 系统默认字体

4. **隐私保护**
   - 所有数据本地处理
   - 不上传任何内容
   - 不收集用户信息

### ❌ 禁止行为

- 生成侵权内容
- 生成违法内容
- 侵犯他人肖像权
- 侵犯他人商标权
- 违反当地法律法规

### 📜 用户责任

用户需对生成内容负责：
- 确保文案不侵权
- 确保使用的素材有授权
- 确保音乐使用合规
- 遵守平台发布规则

## 🐛 常见问题

### Q1: 如何完全离线使用？

**A**: 配置本地模式：

```toml
[app]
offline_mode = true

[llm]
mode = "local"
local_model = "qwen2.5:7b"

[tts]
mode = "local"
```

```bash
# 使用时添加 --offline 参数
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

### Q3: 本地语音如何安装？

**A**: 使用 Piper TTS：

```bash
# 安装 Piper
pip install piper-tts

# 下载语音模型
piper-download zh-CN-Xiaoxiao

# 配置
[tts]
mode = "local"
voice = "zh-CN-Xiaoxiao"
```

### Q4: 如何组织本地素材？

**A**: 自动整理：

```toml
[materials]
local_library = "~/Videos/Materials"
auto_organize = true

[materials.categories]
videos = "~/Videos/Materials/Videos"
images = "~/Videos/Materials/Images"
music = "~/Videos/Materials/Music"
```

### Q5: Whisper 模型下载

**A**: 手动下载：

```bash
# 使用镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple openai-whisper

# 或使用离线包
wget https://example.com/whisper-1.tar.gz
pip install whisper-1.tar.gz
```

## 📈 性能优化

### 加速技巧

1. **使用 SSD 存储**
   ```toml
   [video]
   output_dir = "/path/to/ssd/MarkHub"
   ```

2. **降低分辨率**
   ```bash
   python3 markhub_v8.py -p "test" --width 720 --height 1280
   ```

3. **批量处理**
   ```bash
   python3 markhub_v8.py --batch subjects.txt --parallel 3
   ```

4. **使用 GPU 加速**
   ```toml
   [video]
   use_gpu = true
   ```

### 资源占用

| 操作 | CPU | 内存 | GPU |
|------|-----|------|-----|
| 文案生成 | 中 | 中 | 无 |
| 素材匹配 | 低 | 低 | 无 |
| 语音合成 | 低 | 低 | 无 |
| 字幕生成 | 高 | 中 | 可选 |
| 视频合成 | 高 | 高 | 可选 |
| 本地 AI | 中 | 中 | 推荐 |

## 🎯 最佳实践

### 1. 本地素材管理

```bash
# 创建素材库目录结构
mkdir -p ~/Videos/Materials/{Videos,Images,Music}

# 按类别组织
~/Videos/Materials/Videos/{Nature,City,People,Technology}
~/Videos/Materials/Images/{Landscape,Portrait,Abstract}
~/Videos/Materials/Music/{Upbeat,Calm,Serious}
```

### 2. 文案优化

```python
# 好文案
"3 个简单习惯，让你更自信"

# 差文案
"自信"  # 太宽泛
```

### 3. 语音选择

| 场景 | 推荐语音 |
|------|---------|
| 励志视频 | zh-CN-Xiaoxiao |
| 知识分享 | zh-CN-Yunxi |
| 轻松内容 | zh-CN-Xiaoyi |
| 严肃内容 | zh-CN-Yunjian |

### 4. 背景音乐

| 内容类型 | 音乐风格 |
|----------|---------|
| 励志 | Upbeat/Motivational |
| 知识 | Calm/Focus |
| 轻松 | Acoustic/Happy |
| 严肃 | Ambient/Serious |

## 📚 相关资源

### 本地 AI

- **Ollama**: https://ollama.ai/
- **LM Studio**: https://lmstudio.ai/
- **Stable Diffusion**: https://github.com/AbdBarho/stable-diffusion-cpp-python

### 本地语音

- **Piper TTS**: https://github.com/rhasspy/piper
- **Mimic3**: https://github.com/MycroftAI/mimic3

### 字幕生成

- **Whisper**: https://github.com/openai/whisper
- **FFmpeg**: https://ffmpeg.org/

### 素材管理

- **本地素材库**: 用户自备
- **CC0 素材**: https://cc0.cn/
- **开源音乐**: https://freemusicarchive.org/

## 📄 许可证

MIT License

## 🙏 致谢

- **Ollama** - 本地大模型运行
- **Piper TTS** - 本地语音合成
- **Whisper** - 本地字幕生成
- **FFmpeg** - 视频处理
- **Stable Diffusion** - 本地 AI 图像生成

---

**版本**: v8.0.0  
**创建时间**: 2026-03-25 12:47  
**作者**: 1 号小虫子  
**GitHub**: https://github.com/yun520-1/markhub-skill  
**ClawHub**: https://clawhub.ai/yun520-1/markhub

**核心原则**: 完全本地化 · 无远程依赖 · 隐私保护 · 版权合规
