#!/usr/bin/env python3
"""
MarkHub 模型下载器
支持断点续传、进度显示、完整性验证
"""

from huggingface_hub import hf_hub_download
from pathlib import Path
import hashlib
import json
import sys

# 模型配置
MODELS = {
    "unet": {
        "repo": "yun520-1/z-image-turbo",
        "file": "z_image_turbo-Q8_0.gguf",
        "expected_md5": "TODO_FILL_IN",  # 上传后填充
        "size_gb": 6.7,
    },
    "llm": {
        "repo": "yun520-1/z-image-turbo",
        "file": "Qwen3-4B-Q8_0.gguf",
        "expected_md5": "TODO_FILL_IN",
        "size_gb": 4.0,
    },
    "vae": {
        "repo": "yun520-1/z-image-turbo",
        "file": "ae.safetensors",
        "expected_md5": "TODO_FILL_IN",
        "size_gb": 0.3,
    },
}

def calculate_md5(file_path):
    """计算文件 MD5"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def download_model(model_name, model_info):
    """下载单个模型"""
    dest_dir = Path.home() / "Documents/lmd_data_root/apps/ComfyUI/models" / model_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = dest_dir / model_info["file"]
    
    # 检查是否已下载
    if file_path.exists():
        size_gb = file_path.stat().st_size / (1024**3)
        print(f"⏭️  {model_name}: 已存在 ({size_gb:.2f} GB)")
        
        # 验证 MD5（如果有）
        if model_info.get("expected_md5"):
            print("  🔍 验证文件完整性...")
            actual_md5 = calculate_md5(file_path)
            if actual_md5 == model_info["expected_md5"]:
                print(f"  ✅ MD5 验证通过")
                return True
            else:
                print(f"  ⚠️  MD5 不匹配，重新下载...")
        else:
            return True
    
    # 下载
    print(f"📥 下载 {model_name}: {model_info['file']} (约 {model_info['size_gb']:.1f} GB)...")
    
    try:
        downloaded_path = hf_hub_download(
            repo_id=model_info["repo"],
            filename=model_info["file"],
            local_dir=dest_dir,
            resume_download=True,
            force_download=False,
        )
        
        # 验证大小
        downloaded_size = Path(downloaded_path).stat().st_size / (1024**3)
        print(f"  ✅ 下载完成 ({downloaded_size:.2f} GB)")
        
        # 计算并保存 MD5
        actual_md5 = calculate_md5(downloaded_path)
        print(f"  🔐 MD5: {actual_md5}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 下载失败：{e}")
        return False

def download_all():
    """下载所有模型"""
    print("╔════════════════════════════════════════════╗")
    print("║                                            ║")
    print("║        📦 MarkHub 模型下载器                ║")
    print("║                                            ║")
    print("╚════════════════════════════════════════════╝")
    print()
    
    success_count = 0
    total_count = len(MODELS)
    
    for name, info in MODELS.items():
        if download_model(name, info):
            success_count += 1
        print()
    
    # 总结
    print("═══════════════════════════════════════════")
    if success_count == total_count:
        print("✅ 所有模型下载完成！")
        print()
        print(f"📁 模型目录：{Path.home()}/Documents/lmd_data_root/apps/ComfyUI/models")
        print()
        return True
    else:
        print(f"⚠️  下载完成：{success_count}/{total_count}")
        print()
        print("请检查网络连接或稍后重试")
        return False

def save_checksums():
    """保存校验和文件"""
    checksums = {}
    model_root = Path.home() / "Documents/lmd_data_root/apps/ComfyUI/models"
    
    for name, info in MODELS.items():
        file_path = model_root / name / info["file"]
        if file_path.exists():
            md5 = calculate_md5(file_path)
            checksums[info["file"]] = {
                "md5": md5,
                "size": file_path.stat().st_size,
            }
    
    checksum_file = model_root / "checksums.json"
    with open(checksum_file, "w", encoding="utf-8") as f:
        json.dump(checksums, f, indent=2, ensure_ascii=False)
    
    print(f"💾 校验和已保存：{checksum_file}")

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == "--save-checksums":
        save_checksums()
    else:
        if download_all():
            save_checksums()
            sys.exit(0)
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()
