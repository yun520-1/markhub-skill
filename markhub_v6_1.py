#!/usr/bin/env python3
"""
MarkHub v6.1 - Local AI Creation System
========================================

Fully local AI image and video generation
No ComfyUI dependency, no legal risks
Uses stable-diffusion-cpp-python for native execution

Author: 1 号小虫子
License: MIT
Version: 6.1.0
"""

import os
import sys
import json
import uuid
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Optional imports
try:
    from stable_diffusion_cpp import StableDiffusion
    from PIL import Image
    import numpy as np
    HAS_SD = True
except ImportError:
    HAS_SD = False
    print("⚠️  stable-diffusion-cpp-python not installed")
    print("   Install: pip install stable-diffusion-cpp-python")


class MarkHubV61:
    """MarkHub v6.1 - Local AI Creation Engine"""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir) if output_dir else Path.home() / "Videos" / "MarkHub"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.models_dir = Path.home() / ".markhub" / "models"
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        self.sd_model = None
        self.current_model = None
        
        # Open source models (no legal risks)
        self.open_source_models = {
            "sd-turbo": {
                "url": "https://huggingface.co/stabilityai/sd-turbo/resolve/main/sd_turbo.safetensors",
                "type": "txt2img",
                "resolution": (512, 512),
                "steps": 1,
                "cfg": 0.0,
                "size_mb": 1400
            },
            "sdxl-turbo": {
                "url": "https://huggingface.co/stabilityai/sdxl-turbo/resolve/main/sd_xl_turbo_1.0_fp16.safetensors",
                "type": "txt2img",
                "resolution": (1024, 1024),
                "steps": 1,
                "cfg": 0.0,
                "size_mb": 6000
            },
            "stable-diffusion-v1-5": {
                "url": "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt",
                "type": "txt2img",
                "resolution": (512, 512),
                "steps": 20,
                "cfg": 7.5,
                "size_mb": 4000
            },
            "stable-diffusion-v2-1": {
                "url": "https://huggingface.co/stabilityai/stable-diffusion-2-1/resolve/main/v2-1_768-ema-pruned.ckpt",
                "type": "txt2img",
                "resolution": (768, 768),
                "steps": 20,
                "cfg": 7.5,
                "size_mb": 5000
            }
        }
        
        print("=" * 70)
        print("🎨 MarkHub v6.1 - Local AI Creation System")
        print("=" * 70)
        print(f"📁 Output: {self.output_dir}")
        print(f"📦 Models: {self.models_dir}")
        print(f"💾 Free Space: {self._get_free_space()}")
        print()
    
    def _get_free_space(self) -> str:
        """Get free disk space"""
        try:
            import shutil
            total, used, free = shutil.disk_usage(self.models_dir)
            return f"{free / (1024**3):.1f} GB"
        except:
            return "Unknown"
    
    def download_model(self, model_name: str) -> Optional[Path]:
        """Download model from HuggingFace"""
        if model_name not in self.open_source_models:
            print(f"❌ Unknown model: {model_name}")
            print(f"   Available: {list(self.open_source_models.keys())}")
            return None
        
        model_info = self.open_source_models[model_name]
        model_path = self.models_dir / f"{model_name}.safetensors"
        
        # Check if already downloaded
        if model_path.exists():
            print(f"✅ Model exists: {model_path}")
            return model_path
        
        # Check disk space
        required_gb = model_info.get("size_mb", 4000) / 1024
        free_gb = float(self._get_free_space().split()[0]) if self._get_free_space() != "Unknown" else 0
        
        if free_gb < required_gb:
            print(f"❌ Insufficient disk space")
            print(f"   Required: {required_gb:.1f} GB")
            print(f"   Available: {free_gb:.1f} GB")
            return None
        
        print(f"📥 Downloading: {model_name}")
        print(f"   URL: {model_info['url']}")
        print(f"   Size: {model_info.get('size_mb', 4000)} MB")
        print(f"   Path: {model_path}")
        
        try:
            def reporthook(blocknum, blocksize, totalsize):
                readsofar = blocknum * blocksize
                if totalsize > 0:
                    percent = readsofar * 100 / totalsize
                    print(f"\r   Progress: {percent:.1f}%", end="")
            
            urllib.request.urlretrieve(
                model_info["url"],
                str(model_path),
                reporthook=reporthook
            )
            print(f"\n✅ Download complete")
            return model_path
            
        except Exception as e:
            print(f"\n❌ Download failed: {e}")
            if model_path.exists():
                model_path.unlink()
            return None
    
    def load_model(self, model_name: str = "sd-turbo") -> bool:
        """Load model"""
        if not HAS_SD:
            print("❌ stable-diffusion-cpp-python not installed")
            print("   Run: pip install stable-diffusion-cpp-python")
            return False
        
        # Download if not exists
        model_path = self.download_model(model_name)
        if not model_path:
            return False
        
        # Unload old model
        if self.sd_model:
            del self.sd_model
            self.sd_model = None
        
        print(f"🔄 Loading model: {model_name}")
        try:
            self.sd_model = StableDiffusion(
                model_path=str(model_path),
                lora_model_dir=None,
                n_threads=-1,
                wtype="f16",
                control_net=None,
                clip_l=None,
                clip_g=None,
                vae_path=None,
                taesd_path=None,
                embeddings_dir=None,
                stacked_id_embeddings_dir=None,
                lora_name_dir=None,
                control_net_path=None,
                upscaler_path=None,
                n_gpu_layers=0,
                rng_type="cuda",
                schedule="karras",
            )
            self.current_model = model_name
            print(f"✅ Model loaded")
            return True
            
        except Exception as e:
            print(f"❌ Model load failed: {e}")
            return False
    
    def generate_image(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 512,
        height: int = 512,
        steps: int = None,
        cfg_scale: float = None,
        seed: int = -1,
        batch_count: int = 1,
        output_path: str = None
    ) -> List[Path]:
        """Generate image"""
        if not self.sd_model:
            print("❌ Model not loaded")
            return []
        
        # Use model defaults
        model_info = self.open_source_models.get(self.current_model, {})
        if steps is None:
            steps = model_info.get("steps", 20)
        if cfg_scale is None:
            cfg_scale = model_info.get("cfg", 7.5)
        
        print(f"\n🎨 Generating image")
        print(f"   Prompt: {prompt[:80]}...")
        print(f"   Size: {width}x{height}")
        print(f"   Steps: {steps}")
        print(f"   CFG: {cfg_scale}")
        print(f"   Count: {batch_count}")
        
        generated_images = []
        
        try:
            for i in range(batch_count):
                print(f"\n   Generating {i+1}/{batch_count}...")
                
                image = self.sd_model.txt2img(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=width,
                    height=height,
                    steps=steps,
                    cfg_scale=cfg_scale,
                    seed=seed if seed >= 0 else int(time.time() * 1000) % (2**31),
                    sample_method="euler_a",
                )
                
                if output_path:
                    save_path = Path(output_path)
                else:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    save_path = self.output_dir / f"MarkHub_{timestamp}_{i+1}.png"
                
                if isinstance(image, np.ndarray):
                    pil_image = Image.fromarray(image)
                else:
                    pil_image = image
                
                pil_image.save(str(save_path), "PNG")
                generated_images.append(save_path)
                print(f"   ✅ Saved: {save_path}")
            
            print(f"\n✅ Complete, {len(generated_images)} images")
            return generated_images
            
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            return []
    
    def generate_video(
        self,
        prompt: str,
        duration: int = 10,
        fps: int = 24,
        width: int = 512,
        height: int = 512,
        output_path: str = None
    ) -> Optional[Path]:
        """Generate video (multi-frame synthesis)"""
        print(f"\n🎬 Generating video")
        print(f"   Prompt: {prompt[:80]}...")
        print(f"   Duration: {duration}s")
        print(f"   FPS: {fps}")
        print(f"   Size: {width}x{height}")
        
        frame_count = duration * fps
        frame_dir = self.output_dir / f"video_frames_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        frame_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n   Generating {frame_count} frames...")
        
        frames = []
        for i in range(frame_count):
            frame_prompt = f"{prompt}, frame {i+1}/{frame_count}"
            
            image = self.sd_model.txt2img(
                prompt=frame_prompt,
                width=width,
                height=height,
                steps=1,
                cfg_scale=0.0,
                seed=int(time.time() * 1000) + i,
                sample_method="euler_a",
            )
            
            frame_path = frame_dir / f"frame_{i:04d}.png"
            if isinstance(image, np.ndarray):
                pil_image = Image.fromarray(image)
            else:
                pil_image = image
            pil_image.save(str(frame_path), "PNG")
            frames.append(frame_path)
            
            if (i + 1) % 10 == 0:
                print(f"   Progress: {i+1}/{frame_count} frames")
        
        # Synthesize video with FFmpeg
        print(f"\n   Synthesizing video...")
        if output_path:
            video_path = Path(output_path)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_path = self.output_dir / f"MarkHub_Video_{timestamp}.mp4"
        
        import subprocess
        cmd = [
            "ffmpeg",
            "-framerate", str(fps),
            "-i", str(frame_dir / "frame_%04d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-y",
            str(video_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Cleanup frames
        import shutil
        shutil.rmtree(frame_dir)
        
        if result.returncode == 0:
            print(f"✅ Video saved: {video_path}")
            return video_path
        else:
            print(f"❌ Video synthesis failed: {result.stderr}")
            return None
    
    def auto_generate(self, prompt: str, is_video: bool = False) -> Optional[Path]:
        """Auto generate (select best model)"""
        print(f"\n🤖 Auto mode")
        
        if is_video:
            model = "sd-turbo"
        else:
            if "portrait" in prompt.lower() or "woman" in prompt.lower() or "man" in prompt.lower():
                model = "sdxl-turbo"
            else:
                model = "sd-turbo"
        
        if not self.load_model(model):
            return None
        
        if is_video:
            return self.generate_video(prompt, duration=10)
        else:
            images = self.generate_image(prompt, batch_count=1)
            return images[0] if images else None


def main():
    parser = argparse.ArgumentParser(
        description="MarkHub v6.1 - Local AI Creation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 markhub_v6_1.py -p "A beautiful woman"
  python3 markhub_v6_1.py -p "Portrait" -m sdxl-turbo
  python3 markhub_v6_1.py -p "Dancing" --video --duration 10
  python3 markhub_v6_1.py -p "Cat" --auto
        """
    )
    parser.add_argument("-p", "--prompt", type=str, required=True, help="Prompt")
    parser.add_argument("-n", "--negative", type=str, default="", help="Negative prompt")
    parser.add_argument("-m", "--model", type=str, default="sd-turbo", help="Model name")
    parser.add_argument("--video", action="store_true", help="Generate video")
    parser.add_argument("--duration", type=int, default=10, help="Video duration (seconds)")
    parser.add_argument("--auto", action="store_true", help="Auto mode")
    parser.add_argument("-o", "--output", type=str, help="Output path")
    parser.add_argument("--width", type=int, default=512, help="Width")
    parser.add_argument("--height", type=int, default=512, help="Height")
    parser.add_argument("--steps", type=int, help="Steps")
    parser.add_argument("--cfg", type=float, help="CFG scale")
    
    args = parser.parse_args()
    
    markhub = MarkHubV61()
    
    if args.auto:
        result = markhub.auto_generate(args.prompt, is_video=args.video)
        if result:
            print(f"\n✅ Complete: {result}")
        else:
            print("\n❌ Failed")
        return
    
    if not markhub.load_model(args.model):
        return
    
    if args.video:
        result = markhub.generate_video(
            args.prompt,
            duration=args.duration,
            output_path=args.output
        )
    else:
        results = markhub.generate_image(
            args.prompt,
            negative_prompt=args.negative,
            width=args.width,
            height=args.height,
            steps=args.steps,
            cfg_scale=args.cfg,
            output_path=args.output
        )
        result = results[0] if results else None
    
    if result:
        print(f"\n✅ Complete: {result}")
    else:
        print("\n❌ Failed")


if __name__ == "__main__":
    main()
