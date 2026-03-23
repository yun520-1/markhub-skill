# MarkHub 更新日志

## [6.3.0] - 2026-03-23

### 🔧 ComfyUI 开发技能集成

**新增 9 个 ComfyUI 节点开发技能** (来源：@jtydhr88)
- ✅ **comfyui-node-basics** - ComfyUI 节点开发基础
- ✅ **comfyui-node-inputs** - 节点输入参数定义
- ✅ **comfyui-node-outputs** - 节点输出类型定义
- ✅ **comfyui-node-datatypes** - 数据类型系统
- ✅ **comfyui-node-lifecycle** - 节点生命周期管理
- ✅ **comfyui-node-advanced** - 高级功能和优化
- ✅ **comfyui-node-migration** - API 版本迁移
- ✅ **comfyui-node-packaging** - 打包和发布
- ✅ **comfyui-node-frontend** - 前端界面开发

**技能目录**
- ✅ 新增 `skills/comfyui-dev/` 子目录
- ✅ 独立存放 ComfyUI 开发技能
- ✅ 创建 ATTRIBUTION.md 版权归属声明

**版权合规**
- ✅ 更新 THIRD_PARTY_NOTICES.md
- ✅ 明确标注来源和作者
- ✅ 声明使用限制 (原仓库无明确 LICENSE)

**功能增强**
- ✅ 完整的 AI 媒体开发工具链
- ✅ ComfyUI 自定义节点开发支持
- ✅ Claude Code 技能集成

---

## [6.2.0] - 2026-03-23

### 🦌 DeerFlow 技能集成

**新增 6 个核心技能** (基于 DeerFlow 2.0, MIT License)
- ✅ **deep-research** - 深度研究方法论，多角度网络调研
- ✅ **image-generation** - 结构化图像生成工作流
- ✅ **video-generation** - 视频生成和参考图像支持
- ✅ **ppt-generation** - 演示文稿自动生成
- ✅ **find-skills** - 技能发现和搜索工具
- ✅ **skill-creator** - 技能创建和编辑工具

**技能目录**
- ✅ 新增 `skills/` 子目录
- ✅ 路径适配：容器路径 → 本地路径
- ✅ 每个技能包含独立 LICENSE.deerflow

**版权合规**
- ✅ THIRD_PARTY_NOTICES.md - 第三方组件声明
- ✅ DEERFLOW_INTEGRATION_COMPLETE.md - 集成报告
- ✅ 每个技能添加 attribution 字段
- ✅ 完全符合 MIT License 要求

**功能增强**
- ✅ 内容生成前自动深度研究
- ✅ PPT 自动生成能力
- ✅ 技能搜索和创建工具
- ✅ 视频生成工作流优化

---

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
