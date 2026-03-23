# MarkHub v6.2.0 Release Notes

## 🦌 DeerFlow 技能集成

MarkHub v6.2.0 集成 6 个 DeerFlow 核心技能，提供完整的内容生成能力。

---

## ✨ 新功能

### 新增技能 (基于 DeerFlow 2.0)

| 技能 | 功能 | 使用场景 |
|------|------|----------|
| **deep-research** | 深度研究方法论 | 内容生成前的资料收集 |
| **image-generation** | 结构化图像生成 | 角色设计、场景、产品 |
| **video-generation** | 视频生成 | 短片、动画 |
| **ppt-generation** | PPT 自动生成 | 演示文稿、报告 |
| **find-skills** | 技能搜索 | 发现能力 |
| **skill-creator** | 技能创建 | 自定义技能 |

---

## 📦 安装

### 一键安装 (推荐)

```bash
curl -fsSL https://raw.githubusercontent.com/yun520-1/markhub-skill/main/install.sh | bash
```

### 依赖

- Python 3.8+
- stable-diffusion-cpp-python
- Pillow
- NumPy
- FFmpeg

---

## 🔧 技术细节

### 技能目录结构

```
skills/
├── LICENSE.deerflow
├── deep-research/
├── image-generation/
├── video-generation/
├── ppt-generation/
├── find-skills/
└── skill-creator/
```

### 路径适配

- 容器路径 → 本地路径
- `/mnt/skills/public/` → `~/.jvs/.openclaw/workspace/skills/markhub/skills/`
- `/mnt/user-data/` → `~/.jvs/.openclaw/workspace/`

---

## ⚖️ 版权和许可证

### DeerFlow (MIT License)

**版权:**
- Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
- Copyright (c) 2025-2026 DeerFlow Authors

**许可证:** MIT License

**合规措施:**
- 每个技能添加 attribution 字段
- 每个技能包含 LICENSE.deerflow 副本
- THIRD_PARTY_NOTICES.md 完整声明
- DEERFLOW_INTEGRATION_COMPLETE.md 集成报告

详见：[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)

---

## 📝 更新日志

### v6.2.0 (2026-03-23)
- 集成 DeerFlow 6 个核心技能
- 新增 skills/ 子目录
- 版权合规文档
- 路径适配优化

### v6.1.0 (2026-03-20)
- 完整文档
- 全面的使用指南

### v6.0.0 (2026-03-20)
- 完全本地版本
- 不依赖 ComfyUI

---

## 🔗 链接

- **GitHub:** https://github.com/yun520-1/markhub-skill
- **DeerFlow:** https://github.com/bytedance/deer-flow
- **ClawHub:** https://clawhub.ai/yun520-1/markhub

---

## 📞 支持

如有问题，请提交 Issue 或联系作者。

**作者:** 1 号小虫子  
**许可证:** MIT  
**发布日期:** 2026-03-23
