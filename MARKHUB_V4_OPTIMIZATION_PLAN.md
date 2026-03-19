# MarkHub v4 优化计划 - 快速部署增强版

创建时间：2026-03-19
目标：在空白电脑上 5 分钟内完成搭建并生成第一张图片

---

## 📊 当前状态分析

### 现有优势 (v3.1.0)
- ✅ 独立运行，不依赖 ComfyUI 服务器
- ✅ 使用 stable-diffusion-cpp-python
- ✅ Metal 加速优化（Apple Silicon）
- ✅ 本地模型自动检测
- ✅ 跨平台输出路径（~/Pictures/MarkHub/）

### 当前问题
- ❌ 需要手动安装依赖（CMAKE_ARGS 复杂）
- ❌ 需要手动下载模型文件（3 个文件共~11GB）
- ❌ 没有一键安装脚本
- ❌ 缺少模型下载指引
- ❌ 错误提示不够友好
- ❌ 没有预检查机制

---

## 🔍 竞品分析

### 1. Diffusion Bee (macOS)
**优点：**
- 🎯 一键安装包（.dmg）
- 🎯 自动下载模型
- 🎯 GUI 界面友好
- 🎯 支持 SD 1.x/2.x/XL/ControlNet/LoRA

**缺点：**
- ❌ 仅支持 macOS
- ❌ 闭源应用
- ❌ 无法自定义模型

**参考：** https://diffusionbee.com/

---

### 2. Mochi Diffusion (macOS)
**优点：**
- 🎯 Core ML 优化（速度极快）
- 🎯 内存占用低（~150MB）
- 🎯 原生 SwiftUI 界面
- 🎯 支持 FLUX.2 Klein

**缺点：**
- ❌ 仅支持 Apple Silicon
- ❌ 需要手动转换模型为 Core ML 格式

**参考：** https://github.com/MochiDiffusion/MochiDiffusion

---

### 3. StabilityMatrix (跨平台)
**优点：**
- 🎯 多平台支持（Win/Linux/macOS）
- 🎯 包管理器模式
- 🎯 支持多种 UI（ComfyUI/A1111/Fooocus 等）
- 🎯 自动管理 Python/依赖
- 🎯 完全便携

**缺点：**
- ❌ 体积较大
- ❌ 主要针对完整 UI，非轻量级

**参考：** https://github.com/LykosAI/StabilityMatrix

---

## 🚀 MarkHub v4 优化方案

### 方案 A：一键安装脚本（推荐）

**目标：** 一条命令完成所有安装

```bash
# 用户只需执行这一条命令
curl -fsSL https://raw.githubusercontent.com/yun520-1/markhub-skill/main/scripts/install.sh | bash
```

**脚本功能：**
1. ✅ 检查系统环境（Python/cmake/git）
2. ✅ 自动安装缺失的依赖
3. ✅ 检测芯片架构（Apple Silicon/Intel/AMD/NVIDIA）
4. ✅ 自动设置正确的 CMAKE_ARGS
5. ✅ 安装 stable-diffusion-cpp-python
6. ✅ 下载模型文件（带进度条）
7. ✅ 验证模型完整性
8. ✅ 生成测试图片

---

### 方案 B：Docker 容器化

**目标：** 完全隔离环境，跨平台一致

```bash
# 运行容器
docker run -it --rm \
  -v ~/Pictures/MarkHub:/output \
  -v ~/models:/models \
  markhub:latest \
  generate -p "A beautiful woman" -t "beauty"
```

**优点：**
- ✅ 环境完全隔离
- ✅ 跨平台一致性
- ✅ 预装所有依赖和模型

**缺点：**
- ❌ 需要 Docker
- ❌ 镜像体积大（~15GB）
- ❌ GPU 加速配置复杂

---

### 方案 C：Python 包 + 模型下载器

**目标：** 通过 pip 安装，自动下载模型

```bash
# 安装
pip install markhub

# 首次运行自动下载模型
markhub --download-models

# 生成图片
markhub generate -p "A beautiful woman" -t "beauty"
```

**优点：**
- ✅ 符合 Python 生态习惯
- ✅ 易于分发
- ✅ 版本管理清晰

**缺点：**
- ❌ 模型文件较大，pip 不适合打包
- ❌ 需要额外的模型下载逻辑

---

## 📦 推荐实施方案（v4.0.0）

### 阶段 1：一键安装脚本（1-2 天）

#### 1.1 创建安装脚本
```bash
# scripts/install.sh
#!/bin/bash

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🎨 MarkHub v4 安装程序"
echo "======================"

# 1. 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装${NC}"
    echo "请安装 Python 3.8+"
    exit 1
fi

# 2. 检查 cmake
if ! command -v cmake &> /dev/null; then
    echo -e "${YELLOW}⚠️  安装 cmake...${NC}"
    # macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install cmake
    # Linux
    else
        sudo apt-get install cmake
    fi
fi

# 3. 检测硬件加速
if [[ "$OSTYPE" == "darwin"* ]]; then
    CHIP=$(uname -m)
    if [[ "$CHIP" == "arm64" ]]; then
        echo -e "${GREEN}✅ 检测到 Apple Silicon，启用 Metal 加速${NC}"
        export CMAKE_ARGS="-DSD_METAL=ON"
    else
        echo -e "${YELLOW}⚠️  Intel Mac，使用通用版本${NC}"
    fi
fi

# 4. 安装依赖
echo -e "${YELLOW}📦 安装 stable-diffusion-cpp-python...${NC}"
pip3 install ${CMAKE_ARGS:+$CMAKE_ARGS} stable-diffusion-cpp-python

# 5. 下载模型
echo -e "${YELLOW}📥 下载模型文件...${NC}"
mkdir -p ~/Documents/lmd_data_root/apps/ComfyUI/models/{unet,text_encoders,vae}

# 使用 huggingface-cli 下载
pip3 install huggingface-hub

huggingface-cli download \
    yun520-1/z-image-turbo \
    z_image_turbo-Q8_0.gguf \
    --local-dir ~/Documents/lmd_data_root/apps/ComfyUI/models/unet

# ... 其他模型

# 6. 验证安装
echo -e "${GREEN}✅ 安装完成！${NC}"
python3 -c "from markhub_v3 import check_installation; check_installation()"

# 7. 生成测试图片
echo -e "${YELLOW}🎨 生成测试图片...${NC}"
python3 markhub_v3.py -p "A beautiful sunset over mountains" -t "test"
```

---

#### 1.2 创建模型下载器
```python
# scripts/download_models.py
#!/usr/bin/env python3
"""
MarkHub 模型下载器
支持断点续传、进度显示、完整性验证
"""

from huggingface_hub import hf_hub_download
from pathlib import Path
import hashlib

MODELS = {
    "unet": {
        "repo": "yun520-1/z-image-turbo",
        "file": "z_image_turbo-Q8_0.gguf",
        "expected_md5": "abc123...",
    },
    "llm": {
        "repo": "yun520-1/z-image-turbo",
        "file": "Qwen3-4B-Q8_0.gguf",
        "expected_md5": "def456...",
    },
    "vae": {
        "repo": "yun520-1/z-image-turbo",
        "file": "ae.safetensors",
        "expected_md5": "ghi789...",
    },
}

def download_model(model_name, model_info):
    """下载单个模型"""
    dest_dir = Path.home() / "Documents/lmd_data_root/apps/ComfyUI/models" / model_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📥 下载 {model_info['file']}...")
    
    file_path = hf_hub_download(
        repo_id=model_info["repo"],
        filename=model_info["file"],
        local_dir=dest_dir,
        resume_download=True,
    )
    
    # 验证 MD5
    if model_info.get("expected_md5"):
        print("🔍 验证文件完整性...")
        with open(file_path, "rb") as f:
            actual_md5 = hashlib.md5(f.read()).hexdigest()
        if actual_md5 != model_info["expected_md5"]:
            print(f"❌ MD5 不匹配！")
            return False
    
    print(f"✅ {model_name} 下载完成")
    return True

def download_all():
    """下载所有模型"""
    for name, info in MODELS.items():
        if not download_model(name, info):
            print(f"❌ {name} 下载失败")
            return False
    print("\n✅ 所有模型下载完成！")
    return True

if __name__ == "__main__":
    download_all()
```

---

### 阶段 2：交互式安装向导（2-3 天）

#### 2.1 创建 TUI 界面
```python
# scripts/install_wizard.py
"""
MarkHub 交互式安装向导
使用 rich 库提供美观的终端界面
"""

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn
from rich.prompt import Confirm
from rich.panel import Panel

console = Console()

def main():
    console.print(Panel.fit("🎨 MarkHub v4 安装向导", style="bold magenta"))
    
    # 1. 系统检查
    console.print("\n[bold blue]步骤 1/5: 检查系统环境[/]")
    # ...
    
    # 2. 选择安装模式
    console.print("\n[bold blue]步骤 2/5: 选择安装模式[/]")
    console.print("1. 快速安装（默认设置）")
    console.print("2. 自定义安装（选择模型/路径）")
    console.print("3. 仅下载模型")
    
    # 3. 下载模型（带进度条）
    console.print("\n[bold blue]步骤 3/5: 下载模型文件[/]")
    with Progress(
        SpinnerColumn(),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.1f}%",
        console=console,
    ) as progress:
        # ...
        pass
    
    # 4. 安装依赖
    # 5. 生成测试图片
    # ...

if __name__ == "__main__":
    main()
```

---

### 阶段 3：预打包模型（可选）

#### 3.1 创建 HuggingFace 模型仓库
- 上传量化后的模型文件
- 提供多个精度版本（Q4/Q6/Q8）
- 添加模型卡片和使用说明

#### 3.2 提供镜像下载
- 国内用户：阿里云 OSS / 腾讯云 COS
- 国际用户：HuggingFace / GitHub Releases

---

## 📋 实施清单

### v4.0.0 (MVP - 1-2 天)
- [ ] 创建一键安装脚本（install.sh）
- [ ] 创建模型下载器（download_models.py）
- [ ] 更新 README.md 安装说明
- [ ] 测试 macOS/Windows/Linux
- [ ] 发布到 GitHub

### v4.1.0 (增强 - 3-5 天)
- [ ] 交互式安装向导（TUI）
- [ ] 断点续传支持
- [ ] 模型完整性验证
- [ ] 多镜像源支持
- [ ] 安装进度保存

### v4.2.0 (高级功能）
- [ ] GUI 安装界面（Tkinter/PyQt）
- [ ] 模型管理界面（查看/删除/切换）
- [ ] 预设模板（多种风格）
- [ ] 批量生成
- [ ] 图片元数据查看

---

## 🎯 5 分钟快速安装流程

### 理想用户体验

```bash
# 用户打开终端，执行一条命令
curl -fsSL https://markhub.ai/install.sh | bash

# 脚本自动执行：
# 1. ✅ 检测系统（macOS ARM64）
# 2. ✅ 安装依赖（cmake, python3）
# 3. ✅ 设置 Metal 加速
# 4. 📦 安装 stable-diffusion-cpp-python (2 分钟)
# 5. 📥 下载模型 (2 分钟，显示进度条)
# 6. ✅ 验证安装
# 7. 🎨 生成测试图片

# 完成后显示：
# 🎉 安装完成！
# 📁 图片已保存到：~/Pictures/MarkHub/markhub_test.png
# 🚀 运行命令：markhub -p "你的提示词"
```

---

## 💡 其他优化建议

### 1. 模型优化
- 提供更小量化版本（Q4_K_M，~4GB）
- 提供 SDXL Turbo 替代方案
- 支持 LoRA 模型扩展

### 2. 性能优化
- 添加模型预热（首次加载后保持）
- 支持批处理生成
- 添加图片预览（低分辨率快速预览）

### 3. 用户体验
- 添加提示词推荐（分类模板）
- 添加负面提示词预设
- 支持图片放大（upscaling）

### 4. 文档优化
- 视频教程（B 站/YouTube）
- 常见问题 FAQ
- 提示词指南（中英文）

---

## 📊 时间估算

| 阶段 | 工作量 | 预计时间 |
|------|--------|----------|
| v4.0.0 (MVP) | 中等 | 1-2 天 |
| v4.1.0 (增强) | 中等 | 3-5 天 |
| v4.2.0 (高级) | 较大 | 1-2 周 |

---

## 🎬 下一步行动

1. **立即执行：**
   - [ ] 创建 GitHub 仓库结构
   - [ ] 编写 install.sh 脚本
   - [ ] 上传模型到 HuggingFace

2. **本周完成：**
   - [ ] 测试跨平台兼容性
   - [ ] 更新文档
   - [ ] 发布 v4.0.0

3. **后续优化：**
   - [ ] 收集用户反馈
   - [ ] 开发 GUI 安装器
   - [ ] 添加更多模型支持

---

**目标：让任何人都能在 5 分钟内开始使用 MarkHub！** 🚀
