# ComfyUI Skills 集成计划 - MarkHub

**日期**: 2026-03-23 10:26  
**来源**: https://github.com/jtydhr88/comfyui-custom-node-skills  
**目标**: 集成到 MarkHub v6.2+  

---

## ⚠️ 版权风险评估

### 原仓库状态
- **GitHub**: jtydhr88/comfyui-custom-node-skills
- **LICENSE 文件**: ❌ 未找到
- **README 说明**: 提供安装指南，无明确许可证声明
- **作者**: @jtydhr88

### MarkHub 许可证
- **类型**: MIT License
- **允许**: 商业使用、修改、分发、子许可

### 风险等级
**⚠️ 中等风险** - 原仓库无明确许可证

---

## 🔒 版权合规方案

### 方案 A: 联系作者获取许可 (推荐)
1. 在 GitHub 创建 Issue 询问许可证
2. 等待作者回复确认
3. 获得明确许可后再集成

### 方案 B: 作为独立技能包发布 (保守)
1. 不修改原技能内容
2. 保留完整版权归属
3. 明确标注来源和作者
4. 作为 MarkHub 的"推荐配套技能"

### 方案 C: 仅作为参考文档 (最安全)
1. 不直接集成代码
2. 创建使用指南文档
3. 链接到原仓库

---

## 📋 推荐执行方案 (方案 B)

### 集成方式
- **不修改** 原始 SKILL.md 内容
- **保留** 作者信息和来源链接
- **添加** 版权归属声明
- **独立目录** 存放，不与 MarkHub 核心代码混合

### 目录结构
```
markhub/
├── skills/
│   ├── comfyui-dev/          # ComfyUI 开发技能 (独立)
│   │   ├── comfyui-node-basics/
│   │   ├── comfyui-node-inputs/
│   │   └── ... (9 个技能)
│   │   └── ATTRIBUTION.md    # 版权归属声明
│   └── [其他 MarkHub 技能]
└── THIRD_PARTY_NOTICES.md    # 更新第三方声明
```

### 声明文件
创建 `ATTRIBUTION.md`:
```markdown
# ComfyUI Custom Node Skills - 版权归属

**来源**: https://github.com/jtydhr88/comfyui-custom-node-skills
**作者**: @jtydhr88
**原始许可证**: 未明确声明 (待确认)

本技能包由 MarkHub 项目整理，用于辅助 ComfyUI 自定义节点开发。
原始技能版权归原作者所有。

如有许可证问题，请联系原作者或 MarkHub 维护者。
```

---

## 📦 集成步骤

1. ✅ 复制技能到 markhub/skills/comfyui-dev/
2. ✅ 创建 ATTRIBUTION.md 声明文件
3. ✅ 更新 THIRD_PARTY_NOTICES.md
4. ✅ 更新 README.md 说明
5. ⏳ 更新版本号 (v6.2 → v6.3)
6. ⏳ 提交到 GitHub
7. ⏳ 发布到 ClawHub

---

## ⚠️ 注意事项

1. **不声称原创** - 明确标注来源
2. **不修改内容** - 保持原技能完整性
3. **保留链接** - 指向原仓库
4. **免责声明** - 许可证待确认

---

**下一步**: 执行集成，采用方案 B (保守方案)
