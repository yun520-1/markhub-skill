# MarkHub v5.0 - 智能 ComfyUI 远程控制

**全自动 AI 创作系统 - 自动读取工作流 · 自动选择模型 · 智能参数优化**

---

## ✨ 核心特性

### 🤖 智能化功能

- ✅ **自动读取工作流** - 智能发现 ComfyUI 所有可用工作流
- ✅ **自动选择模型** - 根据任务类型自动选择最佳模型
- ✅ **智能搜索** - 搜索 HuggingFace/GitHub/Civitai 最佳实践
- ✅ **参数优化** - 自动调整步数、CFG、分辨率等参数
- ✅ **错误恢复** - 自动重试和错误处理机制

### 🎨 生成能力

- ✅ **文生图** - SDXL、Flux、SD3 等主流模型
- ✅ **图生图** - Img2Img、Inpaint、Outpaint
- ✅ **文生视频** - LTX-Video、CogVideo、HunyuanVideo
- ✅ **图生视频** - I2V、首尾帧控制
- ✅ **远程控制** - 支持 HTTPS 远程 ComfyUI

---

## 🚀 快速开始

### 安装

```bash
cd ~/.jvs/.openclaw/workspace/skills/markhub
bash install_v5.sh
```

### 基础使用

#### 生成图片

```bash
python3 markhub_v5_core.py -p "A beautiful woman, cinematic lighting"
```

#### 生成视频

```bash
python3 markhub_v5_core.py -p "A woman dancing in the rain" --video --duration 10
```

#### 自动模式（推荐）

```bash
python3 markhub_v5_core.py -p "A cat playing with a ball" --auto
```

---

## ⚙️ 参数说明

### 基本参数

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--url` | | `https://wp08.unicorn.org.cn:19329` | ComfyUI 地址 |
| `--prompt` | `-p` | 必需 | 提示词 |
| `--model` | `-m` | 自动 | 模型名称 |
| `--negative` | `-n` | `""` | 负面提示词 |

### 模式选择

| 参数 | 说明 |
|------|------|
| `--image` | 强制生成图片 |
| `--video` | 强制生成视频 |
| `--auto` | 自动模式（智能选择） |

### 视频参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--duration` | `10` | 视频时长（秒） |

---

## 📋 使用示例

### 示例 1：高质量风景图片

```bash
python3 markhub_v5_core.py \
  -p "Beautiful landscape with mountains and lake, golden hour, cinematic lighting, 4k, highly detailed" \
  -m "sd_xl_base_1.0.safetensors"
```

### 示例 2：10 秒舞蹈视频

```bash
python3 markhub_v5_core.py \
  -p "A beautiful woman dancing gracefully, flowing dress, slow motion" \
  --video \
  --duration 10
```

### 示例 3：自动模式

```bash
python3 markhub_v5_core.py \
  -p "A cat playing with a ball, sunny day, cute" \
  --auto
```

系统会自动：
1. 检测用户需求（图片/视频）
2. 选择最佳模型
3. 优化参数
4. 生成并下载

---

## 🎯 智能功能详解

### 1️⃣ 自动工作流发现

系统会自动扫描远程 ComfyUI 的节点，识别支持的工作流类型：

```
✅ text2image: 文生图工作流
✅ image2image: 图生图工作流
✅ text2video: 文生视频工作流
✅ image2video: 图生视频工作流
✅ inpaint: 局部重绘
✅ controlnet: 姿态控制
```

### 2️⃣ 模型智能搜索

自动搜索模型的最佳实践：

**搜索来源：**
- HuggingFace - 模型信息、下载量、评分
- GitHub - 官方仓库、文档、示例
- Civitai - 社区评价、示例图片

**示例输出：**
```
🔍 搜索 HuggingFace: LTX-Video
✅ 匹配到推荐参数：
  - 分辨率：1024x512
  - 帧数：241 (10 秒)
  - 步数：25
  - CFG: 3.0
```

### 3️⃣ 参数自动优化

根据模型类型自动调整参数：

| 模型 | 分辨率 | 步数 | CFG | 采样器 |
|------|--------|------|-----|--------|
| SDXL | 1024x1024 | 30 | 7.0 | DPM++ 2M Karras |
| Flux | 1024x1024 | 25 | 3.5 | Euler |
| LTX-Video | 1024x512 | 25 | 3.0 | LTXV |
| CogVideoX | 720x480 | 50 | 6.0 | DDIM |

### 4️⃣ 错误自动恢复

- 超时自动重试
- 队列监控
- 失败自动降级（高质量→低质量）

---

## 📁 文件结构

```
markhub-v5/
├── markhub_v5_core.py          # ⭐ 主控制脚本
├── install_v5.sh               # 安装脚本
├── skill_v5.json               # ClawHub 配置
├── SKILL_V5.md                 # 技能说明
├── README_V5.md                # 本文档
└── examples/                   # 使用示例
```

**输出目录：**
```
~/Videos/MarkHub/
├── MarkHub_00001.png
├── MarkHub_00002.png
├── MarkHub_Video_00001.mp4
└── ...
```

---

## 🔧 故障排除

### Q1: 连接失败

**错误：** `连接失败：Connection refused`

**解决：**
1. 检查 ComfyUI 地址是否正确
2. 确认远程服务器是否运行
3. 检查网络连接

```bash
# 测试连接
curl -k https://wp08.unicorn.org.cn:19329/queue
```

### Q2: 节点找不到

**错误：** `Node 'XXX' not found`

**解决：**
1. 远程服务器可能缺少对应插件
2. 使用 `--auto` 模式自动选择可用节点
3. 联系服务器管理员安装插件

### Q3: 生成超时

**解决：**
1. 增加超时时间（编辑脚本，修改 timeout 参数）
2. 降低分辨率或步数
3. 检查服务器队列状态

---

## 💡 提示词技巧

### 高质量提示词结构

```
[主体] + [动作] + [环境] + [风格] + [光照] + [质量词]
```

### 图片示例

```
A beautiful woman with long black hair, traditional Chinese dress, cherry blossoms, soft lighting, cinematic, 4k, highly detailed
```

### 视频示例

```
A beautiful woman dancing gracefully in the rain, flowing dress, slow motion, cinematic lighting, high quality
```

---

## 🔗 相关链接

- **GitHub:** https://github.com/yun520-1/markhub-skill
- **ClawHub:** https://clawhub.ai/yun520-1/markhub
- **ComfyUI:** https://github.com/comfyanonymous/ComfyUI
- **LTX-Video:** https://github.com/Lightricks/LTX-Video

---

## 📊 性能参考

### 图片生成（SDXL）

| 分辨率 | 步数 | 耗时（RTX 4090） |
|--------|------|------------------|
| 512x512 | 20 | ~5 秒 |
| 1024x1024 | 30 | ~15 秒 |

### 视频生成（LTX-Video）

| 分辨率 | 时长 | 耗时（远程） |
|--------|------|--------------|
| 1024x512 | 5 秒 | ~3-5 分钟 |
| 1024x512 | 10 秒 | ~5-10 分钟 |

---

## 🎯 下一步

1. **安装 MarkHub v5.0** - `bash install_v5.sh`
2. **测试连接** - `python3 markhub_v5_core.py -p "test"`
3. **生成第一个作品** - 使用 `--auto` 模式
4. **探索高级功能** - 尝试不同模型和参数

---

**让 AI 创作变得简单智能！** 🎨✨
