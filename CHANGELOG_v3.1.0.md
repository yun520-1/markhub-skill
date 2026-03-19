# MarkHub v3.1.0 更新日志

**更新日期**: 2026-03-18
**作者**: yun520-1

## 🎉 重大更新

### ✅ 跨平台输出路径

**变更内容**:
- 图片输出路径从工作区改为 `~/Pictures/MarkHub/`
- 支持 Windows / Linux / macOS 所有平台
- 目录不存在时自动创建

**代码变更**:
```python
# 旧代码 (硬编码路径)
output_path = Path(f"/Users/apple/.jvs/.openclaw/workspace/markhub_{title}.png")

# 新代码 (跨平台)
output_dir = Path.home() / "Pictures" / "MarkHub"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / f"markhub_{title}.png"
```

**影响范围**:
- ✅ `skills/markhub/markhub_v3.py`
- ✅ `skills/markhub/upload_package/markhub_v3.py`
- ✅ `skills/markhub/SKILL.md`
- ✅ `skills/markhub/upload_package/SKILL.md`
- ✅ `skills/markhub/skill.json`
- ✅ `skills/markhub/upload_package/skill.json`
- ✅ `skills/markhub/upload_package/README.md`

## 📝 其他更新

### 文档更新
- SKILL.md 添加跨平台输出说明
- skill.json 添加 `output_dir` 配置项
- README.md 添加输出路径说明

### 配置更新
- `config.output_dir`: `~/Pictures/MarkHub`
- `usage.output_path`: `~/Pictures/MarkHub/markhub_<title>.png`

## 🚀 升级说明

### 自动升级
技能安装时自动应用新路径。

### 手动升级
```bash
# 重新安装技能
clawhub install markhub

# 或手动更新
cd ~/.jvs/.openclaw/workspace/skills/markhub
git pull origin main
```

## 📊 版本对比

| 版本 | 输出路径 | 跨平台 |
|------|----------|--------|
| v3.0.0 | `/workspace/` | ❌ |
| v3.1.0 | `~/Pictures/MarkHub/` | ✅ |

## ✅ 测试验证

- [x] 模型检测正常
- [x] 路径逻辑正确
- [x] 目录自动创建
- [x] 文档同步更新

---

**完整变更**: 7 个文件更新，新增跨平台输出功能
