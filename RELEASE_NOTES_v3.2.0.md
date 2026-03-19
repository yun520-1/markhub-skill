# MarkHub v3.2.0 Release Notes

**Release Date:** 2026-03-19  
**Version:** 3.2.0  
**Type:** Major Update - One-Click Installation

---

## 🎉 What's New

### 🚀 One-Click Installer (Major Feature)

**Complete deployment with a single command:**
```bash
curl -fsSL https://raw.githubusercontent.com/yun520-1/markhub-skill/main/install.sh | bash
```

**Features:**
- ✅ **Cross-Platform Support** - macOS / Windows (WSL) / Linux
- ✅ **Auto Hardware Detection** - Intelligently enable Metal/CUDA acceleration
- ✅ **Auto Model Download** - 11GB models with progress bar and resume support
- ✅ **Test Image Generation** - Automatically generate verification image
- ✅ **Smart Error Handling** - User-friendly error messages with solutions
- ✅ **Installation Logging** - Complete log for troubleshooting

**Installation Steps (Automatic):**
1. Check system environment (Python/cmake)
2. Install required dependencies
3. Detect hardware acceleration (Metal/CUDA)
4. Create directory structure
5. Install Python dependencies (stable-diffusion-cpp-python)
6. Download model files (~11GB)
7. Generate test image

**Estimated Time:** 10-30 minutes (mainly depends on network speed)

---

## 📦 Model Auto-Download

**New Download Script:**
```bash
python3 scripts/download_models.py
```

**Features:**
- ✅ Progress bar display
- ✅ Resume support (interrupt and continue)
- ✅ MD5 integrity verification
- ✅ Multi-mirror support (HuggingFace/Aliyun)
- ✅ Size verification

**Models:**
| File | Size | Path |
|------|------|------|
| z_image_turbo-Q8_0.gguf | ~6.7GB | `unet/` |
| Qwen3-4B-Q8_0.gguf | ~4.0GB | `text_encoders/` |
| ae.safetensors | ~0.3GB | `vae/` |

---

## 🌍 Cross-Platform Support

### macOS
- ✅ Apple Silicon (M1/M2/M3) - Metal acceleration
- ✅ Intel Mac - CPU mode
- ✅ Homebrew dependency management

### Linux
- ✅ Ubuntu/Debian - apt package manager
- ✅ CentOS/RHEL - yum package manager
- ✅ NVIDIA GPU - CUDA acceleration
- ✅ CPU-only mode

### Windows
- ✅ WSL (Windows Subsystem for Linux) - Recommended
- ✅ Git Bash support
- ✅ Full compatibility via WSL

---

## 🔧 Improvements

### Error Handling
- ✅ More user-friendly error messages
- ✅ Step-by-step troubleshooting guide
- ✅ Automatic solution suggestions
- ✅ Complete installation logs

### Performance
- ✅ Optimized model loading
- ✅ Better memory management
- ✅ Hardware-specific optimizations

### User Experience
- ✅ Progress bars for long operations
- ✅ Color-coded output
- ✅ Clear installation summary
- ✅ Test image auto-generation

---

## 📝 Documentation Updates

### New Files
- ✅ `README_CN.md` - Complete Chinese documentation
- ✅ `README.md` - Complete English documentation
- ✅ `install.sh` - One-click installation script
- ✅ `scripts/download_models.py` - Model downloader

### Updated Files
- ✅ `SKILL.md` - Updated with v3.2.0 features
- ✅ `skill.json` - Version bump and feature list

---

## 🔗 Quick Links

- **GitHub:** https://github.com/yun520-1/markhub-skill
- **ClawHub:** https://clawhub.ai/yun520-1/markhub
- **HuggingFace:** https://huggingface.co/yun520-1/z-image-turbo
- **Issues:** https://github.com/yun520-1/markhub-skill/issues

---

## 📊 Version Comparison

| Feature | v3.1.0 | v3.2.0 |
|---------|--------|--------|
| One-Click Install | ❌ | ✅ |
| Auto Model Download | ❌ | ✅ |
| Progress Bar | ❌ | ✅ |
| Cross-Platform | Partial | ✅ Full |
| Test Image Auto | ❌ | ✅ |
| Error Messages | Basic | ✅ Enhanced |
| Installation Log | ❌ | ✅ |
| Mirror Support | ❌ | ✅ |

---

## 🐛 Bug Fixes

- Fixed model path detection on Windows WSL
- Improved error handling for failed downloads
- Fixed permission issues on Linux
- Better cmake installation detection

---

## ⚠️ Breaking Changes

**None!** This update is fully backward compatible with v3.1.0.

---

## 🎯 Upgrade Guide

### From v3.1.0

**Option 1: Re-run installer (Recommended)**
```bash
curl -fsSL https://raw.githubusercontent.com/yun520-1/markhub-skill/main/install.sh | bash
```

**Option 2: Manual update**
```bash
# Download new scripts
cd ~/path/to/markhub-skill
git pull  # or download manually

# Run new installer
bash install.sh
```

### From v3.0.0 or Earlier

**Full reinstallation recommended:**
```bash
# Backup your images
cp -r ~/Pictures/MarkHub ~/Pictures/MarkHub_backup

# Run new installer
curl -fsSL https://raw.githubusercontent.com/yun520-1/markhub-skill/main/install.sh | bash
```

---

## 🙏 Acknowledgments

Thanks to:
- All users who provided feedback
- Contributors who tested the new installer
- The stable-diffusion-cpp-python community

---

## 📄 License

MIT-0

---

**Making AI art accessible to everyone!** 🎨✨
