#!/usr/bin/env python3
"""
MarkHub v3 - Z-Image 独立版智能媒体生成中心
使用 stable-diffusion-cpp-python，不依赖 ComfyUI
"""

import sys
from pathlib import Path

# 模型路径配置
MODEL_ROOT = Path.home() / "Documents/lmd_data_root/apps/ComfyUI/models"

MODELS = {
    "unet": MODEL_ROOT / "unet/z_image_turbo-Q8_0.gguf",
    "llm": MODEL_ROOT / "text_encoders/Qwen3-4B-Q8_0.gguf",
    "vae": MODEL_ROOT / "vae/ae.safetensors",
}

def check_models():
    """检查模型文件是否存在"""
    print("🔍 检查模型文件...")
    all_exist = True
    for name, path in MODELS.items():
        if path.exists():
            size_gb = path.stat().st_size / (1024**3)
            print(f"  ✅ {name}: {path.name} ({size_gb:.2f} GB)")
        else:
            print(f"  ❌ {name}: {path.name} (未找到)")
            all_exist = False
    if all_exist:
        print("✅ 所有模型文件就绪！\n")
    return all_exist

def check_installation():
    """检查安装状态"""
    try:
        from stable_diffusion_cpp import StableDiffusion
        print("✅ stable-diffusion-cpp-python 已安装\n")
        return True
    except ImportError:
        print("❌ 未安装 stable-diffusion-cpp-python")
        print("\n📦 安装命令：")
        print("  macOS Metal: CMAKE_ARGS=\"-DSD_METAL=ON\" pip3 install stable-diffusion-cpp-python")
        print("  Linux CUDA: CMAKE_ARGS=\"-DSD_CUDA=ON\" pip3 install stable-diffusion-cpp-python")
        print("  通用版本：pip3 install stable-diffusion-cpp-python\n")
        return False

def generate_image(prompt, title="output", width=768, height=768, steps=15, cfg=1.0, seed=-1):
    """生成图片"""
    from stable_diffusion_cpp import StableDiffusion
    
    # 验证模型
    if not check_models():
        return False
    
    # 跨平台输出路径：~/Pictures/MarkHub/
    output_dir = Path.home() / "Pictures" / "MarkHub"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"markhub_{title}.png"
    
    print("🎨 开始生成...")
    print(f"  提示词：{prompt[:60]}...")
    print(f"  分辨率：{width}x{height}")
    print(f"  步数：{steps}, CFG: {cfg}")
    print(f"  输出目录：{output_dir}")
    print(f"  输出文件：{output_path}\n")
    
    try:
        # 初始化
        print("⚙️ 加载模型中...")
        sd = StableDiffusion(
            diffusion_model_path=str(MODELS["unet"]),
            llm_path=str(MODELS["llm"]),
            vae_path=str(MODELS["vae"]),
            vae_decode_only=True,
            offload_params_to_cpu=True,
            keep_clip_on_cpu=True,
            keep_vae_on_cpu=True,
            diffusion_flash_attn=True,
            verbose=True,
        )
        
        print("✨ 生成图像中...")
        output = sd.generate_image(
            prompt=prompt,
            width=width,
            height=height,
            cfg_scale=cfg,
            sample_steps=steps,
            seed=seed,
            batch_count=1,
        )
        
        # 保存
        output[0].save(str(output_path))
        
        file_size = output_path.stat().st_size / (1024**2)
        print(f"\n✅ 生成成功！")
        print(f"  📁 保存位置：{output_path}")
        print(f"  📊 文件大小：{file_size:.2f} MB")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 生成失败：{e}")
        return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MarkHub v3 - Z-Image 图像生成")
    parser.add_argument("-p", "--prompt", type=str, default="A beautiful woman", help="提示词")
    parser.add_argument("-t", "--title", type=str, default="output", help="输出文件名")
    parser.add_argument("-W", "--width", type=int, default=768, help="宽度")
    parser.add_argument("-H", "--height", type=int, default=768, help="高度")
    parser.add_argument("-s", "--steps", type=int, default=15, help="采样步数")
    parser.add_argument("-c", "--cfg", type=float, default=1.0, help="CFG 比例")
    parser.add_argument("--check", action="store_true", help="检查安装状态")
    
    args = parser.parse_args()
    
    if args.check:
        if check_installation():
            check_models()
        return 0
    
    if not check_installation():
        return 1
    
    success = generate_image(
        prompt=args.prompt,
        title=args.title,
        width=args.width,
        height=args.height,
        steps=args.steps,
        cfg=args.cfg,
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
