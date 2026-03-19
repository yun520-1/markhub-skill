# MarkHub v3.0 - ClawHub Upload Guide

## 📦 Package Contents (English)

### Required Files for Upload:
```
markhub/
├── SKILL_EN.md           → Rename to SKILL.md before upload
├── skill_en.json         → Rename to skill.json before upload
├── markhub_v3.py         → Main program
├── README_EN.md          → Rename to README.md before upload
├── CHANGELOG.md          → Update log
├── configs/
│   └── sdxl_config.json  → Configuration
├── install_with_mirror.sh → Installation script
└── quick_install_sd_cpp.sh → Quick install script
```

## 🌐 English Description for ClawHub

**Name:** MarkHub v3 - Z-Image Standalone AI Image Generator

**Description:**
Fully standalone AI image generation skill powered by Z-Image model and stable-diffusion-cpp-python. No ComfyUI dependency required. Features Metal acceleration for Apple Silicon, smart CPU/GPU memory separation, and local model auto-detection.

**Key Features:**
- Z-Image-Turbo model support (next-gen image generation)
- stable-diffusion-cpp-python backend
- Metal acceleration (Apple Silicon) / CUDA (Linux)
- Smart memory optimization (CPU/GPU separation)
- Local model auto-detection
- Fast generation (15 steps, ~4 minutes on M1 Pro)
- Smart error resolution (auto-searches GitHub/ClawHub)

**Version:** 3.0.0

**Tags:** image-generation, standalone, z-image, stable-diffusion, ai-art, metal-accel

**License:** MIT-0

**Author:** yun520-1

## 📤 Manual Upload Steps

### Option 1: Web Upload (Recommended)

1. Visit: https://clawhub.ai/upload?updateSlug=markhub
2. Login with your account (yun520-1)
3. Upload the following files:
   - SKILL_EN.md (rename to SKILL.md)
   - skill_en.json (rename to skill.json)
   - markhub_v3.py
   - README_EN.md (rename to README.md)
   - CHANGELOG.md
   - configs/sdxl_config.json
   - install_with_mirror.sh
   - quick_install_sd_cpp.sh
4. Fill in metadata:
   - **Name:** MarkHub v3 - Z-Image Standalone AI Image Generator
   - **Version:** 3.0.0
   - **Description:** (see above)
   - **Tags:** image-generation,standalone,z-image,stable-diffusion,ai-art
   - **Changelog:** Z-Image model support, stable-diffusion-cpp-python backend, Metal acceleration, memory optimization
5. Click "Publish" or "Update"

### Option 2: CLI Upload

```bash
# Login first
npx clawhub@latest login

# Upload (from markhub directory)
cd /Users/apple/.jvs/.openclaw/workspace/skills/markhub

# Publish update
npx clawhub@latest publish . \
  --slug markhub \
  --name "MarkHub v3 - Z-Image Standalone AI Image Generator" \
  --version 3.0.0 \
  --changelog "Z-Image model support, stable-diffusion-cpp-python backend, Metal acceleration, memory optimization" \
  --tags "image-generation,standalone,z-image,stable-diffusion,ai-art,metal-accel"
```

### Option 3: Prepare Package for Upload

```bash
cd /Users/apple/.jvs/.openclaw/workspace/skills/markhub

# Create upload package
rm -rf upload_package
mkdir upload_package
cp SKILL_EN.md upload_package/SKILL.md
cp skill_en.json upload_package/skill.json
cp markhub_v3.py upload_package/
cp README_EN.md upload_package/README.md
cp CHANGELOG.md upload_package/
cp -r configs upload_package/
cp install_with_mirror.sh upload_package/
cp quick_install_sd_cpp.sh upload_package/

# Create zip
cd upload_package
zip -r ../markhub-v3-upload.zip *
cd ..

echo "✅ Upload package ready: markhub-v3-upload.zip"
```

## 📋 Metadata Summary

| Field | Value |
|-------|-------|
| **Slug** | markhub |
| **Name** | MarkHub v3 - Z-Image Standalone AI Image Generator |
| **Version** | 3.0.0 |
| **Author** | yun520-1 |
| **License** | MIT-0 |
| **Main File** | markhub_v3.py |
| **Tags** | image-generation, standalone, z-image, stable-diffusion, ai-art, metal-accel |
| **Description** | Fully standalone AI image generation with Z-Image model and stable-diffusion-cpp-python. Metal acceleration, memory optimized. |

## 🔗 Links

- **Upload Page:** https://clawhub.ai/upload?updateSlug=markhub
- **GitHub:** https://github.com/yun520-1/markhub-skill
- **ClawHub Skill:** https://clawhub.ai/yun520-1/markhub

## ✅ Pre-upload Checklist

- [ ] All files copied to upload package
- [ ] English files renamed correctly (SKILL_EN.md → SKILL.md, etc.)
- [ ] skill.json updated with version 3.0.0
- [ ] Logged into ClawHub
- [ ] Network connection stable
- [ ] Test generation works locally

---

**Guide Created:** 2026-03-18 22:27
**Status:** Ready for upload
