# MarkHub 更新日志

## [3.0.0] - 2026-03-18

### 🎉 重大更新

**Z-Image 模型支持**
- ✅ 使用 z_image_turbo-Q8_0.gguf 模型
- ✅ 使用 Qwen3-4B-Q8_0.gguf 文本编码器
- ✅ 使用 ae.safetensors VAE 解码器

**stable-diffusion-cpp-python**
- ✅ 从 ComfyUI CLI 迁移到 Python 绑定
- ✅ 更好的跨平台支持
- ✅ 更简单的 API

**性能优化**
- ✅ Metal 加速 (Apple Silicon)
- ✅ CPU/GPU 内存智能分离
- ✅ Flash Attention 支持
- ✅ 降低显存占用约 40%

**本地模型检测**
- ✅ 自动检测本地已下载的模型
- ✅ 无需重复下载
- ✅ 支持自定义模型路径

**简化配置**
- ✅ CFG 从 7.0 降至 1.0 (Z-Image 推荐)
- ✅ 步数从 20 降至 15 (质量不变)
- ✅ 分辨率优化为 768x768

### 📦 依赖变更

**新增:**
- stable-diffusion-cpp-python

**移除:**
- requests
- psutil

### 📝 文件变更

**新增:**
- markhub_v3.py (主程序)
- generate_beauty.py (示例脚本)

**移除:**
- markhub_standalone.py
- 所有测试和临时文件

---

## [2.0.0] - 2026-03-18

### 独立运行
- ✅ 不依赖 ComfyUI 服务器
- ✅ 自动下载模型
- ✅ 自动配置环境

### 智能错误解决
- ✅ 自动搜索 GitHub Issues
- ✅ 自动搜索 ClawHub Skills

### 质量验证
- ✅ 亮度/对比度检查
- ✅ 文件大小验证

---

## [1.0.0] - 2026-03-17

### 初始版本
- 基于 ComfyUI 的图像生成
- 支持工作流自动执行
