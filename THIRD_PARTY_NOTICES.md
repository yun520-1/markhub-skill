# 第三方组件声明 (Third Party Notices)

**MarkHub** 包含以下第三方开源组件。我们感谢所有开源贡献者的杰出工作。

---

## DeerFlow Skills

本项目包含基于 **DeerFlow** 框架的技能模块。

### 来源信息
- **项目名称**: DeerFlow (Deep Exploration and Efficient Research Flow)
- **源代码**: https://github.com/bytedance/deer-flow
- **许可证**: [MIT License](skills/LICENSE.deerflow)
- **版本**: 2.0 (2026)

### 版权信息
```
Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
Copyright (c) 2025-2026 DeerFlow Authors
```

### 包含组件

| 技能 | 功能描述 | 原始路径 |
|------|----------|----------|
| **deep-research** | 深度研究方法论，多角度的网络调研 | `skills/public/deep-research/` |
| **image-generation** | 结构化图像生成工作流 | `skills/public/image-generation/` |
| **video-generation** | 视频生成和参考图像支持 | `skills/public/video-generation/` |
| **ppt-generation** | 演示文稿自动生成 | `skills/public/ppt-generation/` |
| **find-skills** | 技能发现和搜索工具 | `skills/public/find-skills/` |
| **skill-creator** | 技能创建和编辑工具 | `skills/public/skill-creator/` |

### 修改说明

为适配 MarkHub 环境，对原始技能进行了以下修改：

1. **路径适配**
   - 容器路径 `/mnt/skills/public/` → 本地路径 `~/.jvs/.openclaw/workspace/skills/markhub/skills/`
   - 容器路径 `/mnt/user-data/workspace/` → 本地路径 `~/.jvs/.openclaw/workspace/`
   - 容器路径 `/mnt/user-data/outputs/` → 本地路径 `~/.jvs/.openclaw/workspace/outputs/`

2. **集成调整**
   - 添加 `attribution` 元数据字段到每个 SKILL.md
   - 在每个技能目录中包含 LICENSE.deerflow 副本
   - 整合到 MarkHub 技能加载系统

3. **功能保留**
   - 所有原始功能保持不变
   - 工作流和方法论完整保留
   - 脚本和工具可正常执行

### 许可证合规

DeerFlow 使用 **MIT 许可证**，这是一个宽松的开源许可证，允许：

✅ 商业使用  
✅ 修改和合并  
✅ 分发  
✅ 子许可  
✅ 私有使用  

**唯一要求**: 保留原始版权声明和许可证文本。

本项目已完全遵守 MIT 许可证要求：
- 所有技能文件包含原始版权声明
- 每个技能目录包含 LICENSE.deerflow 副本
- 本声明文件提供完整的归属信息

### 许可证全文

见：[skills/LICENSE.deerflow](skills/LICENSE.deerflow)

---

## 其他依赖

### stable-diffusion-cpp-python
- **用途**: 本地 AI 图像生成核心库
- **许可证**: MIT License
- **来源**: https://github.com/leejet/stable-diffusion.cpp

### Python 依赖
- **PIL/Pillow**: 图像处理
- **NumPy**: 数值计算
- **Hugging Face Hub**: 模型下载

---

## 声明更新

**最后更新**: 2026-03-23  
**MarkHub 版本**: v3.2+

如需了解 DeerFlow 的更多信息，请访问：
- GitHub: https://github.com/bytedance/deer-flow
- 官网：https://deerflow.tech

---

*本声明文件是 MarkHub 项目的一部分，用于满足第三方开源组件的许可证要求。*
