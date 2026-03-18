#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MarkHub API 版本
使用 ComfyUI API 作为后端，功能与 markhub.py 相同
"""

import requests
import json
import uuid
import time
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
import threading
import psutil
from PIL import Image
import numpy as np

# ============================================================================
# 配置
# ============================================================================
class Config:
    """MarkHub API 配置"""
    
    # ComfyUI 服务器
    SERVER = "127.0.0.1:8188"
    
    # 路径
    HOME = Path.home()
    OUTPUT_DIR = HOME / "Downloads/markhub_output"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 模型路径
    MODELS_DIR = HOME / "Documents/lmd_data_root/apps/ComfyUI/models"
    
    # 模型文件
    UNET = "z_image_turbo-Q8_0.gguf"
    CLIP = "Qwen3-4B-Q8_0.gguf"
    VAE = "ae.safetensors"
    
    # 默认参数
    DEFAULT_WIDTH = 2048
    DEFAULT_HEIGHT = 1024
    DEFAULT_STEPS = 20
    DEFAULT_CFG = 7.0
    DEFAULT_SAMPLER = "euler"
    DEFAULT_SCHEDULER = "simple"


# ============================================================================
# 资源监控
# ============================================================================
class ResourceMonitor:
    """资源监控"""
    
    def __init__(self):
        self.monitoring = False
        self.stats = []
        self.thread = None
    
    def start(self):
        self.monitoring = True
        self.stats = []
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        print("📊 资源监控已启动")
    
    def stop(self):
        self.monitoring = False
        if self.thread:
            self.thread.join(timeout=2)
        print("📊 资源监控已停止")
    
    def _monitor_loop(self):
        while self.monitoring:
            try:
                cpu = psutil.cpu_percent(interval=1)
                mem = psutil.virtual_memory()
                
                stat = {
                    "timestamp": datetime.now().isoformat(),
                    "cpu": cpu,
                    "memory": mem.percent,
                    "memory_used_gb": mem.used / 1024 / 1024 / 1024
                }
                self.stats.append(stat)
                time.sleep(2)
            except:
                time.sleep(2)
    
    def print_summary(self):
        if not self.stats:
            return
        
        avg_cpu = sum(s["cpu"] for s in self.stats) / len(self.stats)
        avg_mem = sum(s["memory"] for s in self.stats) / len(self.stats)
        
        print("\n" + "="*70)
        print("📊 资源使用摘要")
        print("="*70)
        print(f"  CPU 平均：{avg_cpu:.1f}%")
        print(f"  内存平均：{avg_mem:.1f}%")
        print(f"  采样次数：{len(self.stats)}")
        print("="*70)


# ============================================================================
# 质量验证
# ============================================================================
class QualityValidator:
    """质量验证"""
    
    @staticmethod
    def validate_image(image_path: Path) -> Dict:
        result = {"valid": True, "issues": [], "metrics": {}}
        
        try:
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # 尺寸
            result["metrics"]["width"] = img.width
            result["metrics"]["height"] = img.height
            
            # 亮度
            brightness = np.mean(img_array)
            result["metrics"]["brightness"] = brightness
            if brightness < 20:
                result["issues"].append("图片过暗")
                result["valid"] = False
            if brightness > 240:
                result["issues"].append("图片过亮")
                result["valid"] = False
            
            # 对比度
            contrast = np.std(img_array)
            result["metrics"]["contrast"] = contrast
            if contrast < 30:
                result["issues"].append("对比度过低")
                result["valid"] = False
            
            # 锐度
            if len(img_array.shape) == 3:
                gray = np.mean(img_array, axis=2)
            else:
                gray = img_array
            
            from PIL import ImageFilter
            edges = Image.fromarray(gray.astype(np.uint8)).filter(ImageFilter.FIND_EDGES)
            sharpness = np.std(np.array(edges))
            result["metrics"]["sharpness"] = sharpness
            if sharpness < 10:
                result["issues"].append("锐度不足")
                result["valid"] = False
            
            # 文件大小
            size_mb = image_path.stat().st_size / 1024 / 1024
            result["metrics"]["file_size_mb"] = size_mb
            if size_mb < 0.1:
                result["issues"].append("文件过小")
                result["valid"] = False
            
            result["summary"] = "✅ 质量验证通过" if result["valid"] else f"❌ {len(result['issues'])} 个问题"
            
        except Exception as e:
            result["valid"] = False
            result["issues"].append(str(e))
            result["summary"] = f"❌ 验证失败：{str(e)}"
        
        return result


# ============================================================================
# MarkHub API
# ============================================================================
class MarkHubAPI:
    """MarkHub API 版本"""
    
    def __init__(self):
        self.config = Config()
        self.monitor = ResourceMonitor()
        self.validator = QualityValidator()
        
        print("="*70)
        print("🎨 MarkHub API - 智能媒体生成中心")
        print("="*70)
        print(f"服务器：{self.config.SERVER}")
        print(f"输出：{self.config.OUTPUT_DIR}")
        print()
        
        self._check_server()
        self._check_models()
    
    def _check_server(self):
        """检查服务器"""
        try:
            r = requests.get(f"http://{self.config.SERVER}/system_stats", timeout=5)
            if r.status_code == 200:
                print("✅ ComfyUI 服务器在线")
            else:
                print("❌ ComfyUI 服务器未响应")
        except:
            print("❌ ComfyUI 服务器未运行")
    
    def _check_models(self):
        """检查模型"""
        print("\n📦 模型检查:")
        models = {
            "UNet": self.config.UNET,
            "CLIP": self.config.CLIP,
            "VAE": self.config.VAE
        }
        for name, fname in models.items():
            path = self.config.MODELS_DIR / ("unet" if name == "UNet" else "text_encoders" if name == "CLIP" else "vae") / fname
            if path.exists():
                size = path.stat().st_size / 1024 / 1024 / 1024
                print(f"  ✅ {name}: {fname} ({size:.2f}GB)")
            else:
                print(f"  ❌ {name}: 未找到")
    
    def _create_workflow(self, prompt: str, width: int, height: int, steps: int, cfg: float, seed: int) -> Dict:
        """创建工作流"""
        return {
            "1": {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": self.config.UNET}},
            "2": {"class_type": "CLIPLoaderGGUF", "inputs": {"clip_name": self.config.CLIP, "type": "qwen_image"}},
            "3": {"class_type": "VAELoader", "inputs": {"vae_name": self.config.VAE}},
            "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": prompt}},
            "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": "blurry, low quality, ugly"}},
            "6": {"class_type": "EmptySD3LatentImage", "inputs": {"batch_size": 1, "height": height, "width": width}},
            "7": {"class_type": "KSampler", "inputs": {"cfg": cfg, "denoise": 1.0, "latent_image": ["6", 0], "model": ["1", 0], "negative": ["5", 0], "positive": ["4", 0], "sampler_name": self.config.DEFAULT_SAMPLER, "scheduler": self.config.DEFAULT_SCHEDULER, "seed": seed, "steps": steps}},
            "8": {"class_type": "VAEDecode", "inputs": {"samples": ["7", 0], "vae": ["3", 0]}},
            "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "MarkHub", "images": ["8", 0]}}
        }
    
    def generate_image(self, prompt: str, title: str = "image",
                      width: int = None, height: int = None,
                      steps: int = None, cfg: float = None,
                      seed: int = None, validate: bool = True) -> Optional[str]:
        """生成图片"""
        width = width or self.config.DEFAULT_WIDTH
        height = height or self.config.DEFAULT_HEIGHT
        steps = steps or self.config.DEFAULT_STEPS
        cfg = cfg or self.config.DEFAULT_CFG
        
        if seed is None:
            seed = int(time.time() * 1000) % 1000000
        
        print(f"\n{'='*70}")
        print(f"🎨 生成：{title}")
        print(f"{'='*70}")
        print(f"提示词：{prompt[:70]}...")
        print(f"分辨率：{width}x{height}")
        print(f"步数：{steps}, CFG: {cfg}")
        print(f"种子：{seed}")
        
        workflow = self._create_workflow(prompt, width, height, steps, cfg, seed)
        
        try:
            # 提交
            client_id = str(uuid.uuid4())
            r = requests.post(f"http://{self.config.SERVER}/prompt",
                            json={"prompt": workflow, "client_id": client_id}, timeout=30)
            
            if r.status_code != 200:
                print(f"❌ 提交失败：{r.status_code}")
                return None
            
            prompt_id = r.json().get("prompt_id")
            print(f"✅ 任务已提交：{prompt_id[:12]}...")
            
            # 等待
            print(f"⏳ 生成中...")
            start = time.time()
            self.monitor.start()
            
            while time.time() - start < 300:
                r = requests.get(f"http://{self.config.SERVER}/history/{prompt_id}", timeout=5)
                if r.status_code == 200:
                    history = r.json()
                    if prompt_id in history:
                        status = history[prompt_id].get("status", {})
                        if status.get("completed"):
                            print(f"✅ 完成！用时：{time.time()-start:.1f}秒")
                            break
                        if status.get("status_str") == "error":
                            print("❌ 失败")
                            self.monitor.stop()
                            return None
                time.sleep(2)
            
            self.monitor.stop()
            self.monitor.print_summary()
            
            # 下载
            r = requests.get(f"http://{self.config.SERVER}/history/{prompt_id}", timeout=10)
            if r.status_code == 200:
                history = r.json()
                if prompt_id in history:
                    for out in history[prompt_id].get("outputs", {}).values():
                        for img in out.get("images", []):
                            fn = img.get("filename")
                            if fn:
                                img_r = requests.get(f"http://{self.config.SERVER}/view?filename={fn}", timeout=60)
                                if img_r.status_code == 200:
                                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                                    filepath = self.config.OUTPUT_DIR / f"{title}_{ts}_{fn}"
                                    with open(filepath, "wb") as f:
                                        f.write(img_r.content)
                                    print(f"✅ 已保存：{filepath}")
                                    
                                    # 验证
                                    if validate:
                                        print("\n🔍 质量验证...")
                                        v = self.validator.validate_image(filepath)
                                        print(f"  {v['summary']}")
                                        if v['metrics']:
                                            print(f"  尺寸：{v['metrics'].get('width', '?')}x{v['metrics'].get('height', '?')}")
                                            print(f"  亮度：{v['metrics'].get('brightness', '?'):.1f}")
                                            print(f"  对比度：{v['metrics'].get('contrast', '?'):.1f}")
                                            print(f"  锐度：{v['metrics'].get('sharpness', '?'):.1f}")
                                    
                                    subprocess.run(["open", str(self.config.OUTPUT_DIR)])
                                    return str(filepath)
            return None
            
        except Exception as e:
            print(f"❌ 错误：{e}")
            self.monitor.stop()
            return None
    
    def auto_generate(self, preset: str = "default"):
        """全自动生成"""
        presets = {
            "default": [{"title": "宇宙女神", "prompt": "A magnificent cosmic goddess floating in deep space, surrounded by nebulae and stars, galaxy dress, cosmic energy, ethereal beauty, divine light, universe background, nebula clouds, stardust, celestial aura, hyperdetailed, cinematic lighting, 8k quality"}],
            "landscape": [{"title": "风景日落", "prompt": "Beautiful landscape, sunset over mountains, lake reflection, golden hour, cinematic, high quality, detailed"}],
            "portrait": [{"title": "人像", "prompt": "Beautiful portrait, professional photography, studio lighting, high quality, detailed"}]
        }
        
        prompts = presets.get(preset, presets["default"])
        print(f"\n🤖 全自动生成：{preset}")
        
        results = []
        for item in prompts:
            result = self.generate_image(item["prompt"], item["title"], validate=True)
            if result:
                results.append(result)
        
        print(f"\n✅ 完成：{len(results)} 张")
        return results


# ============================================================================
# 主函数
# ============================================================================
def main():
    import subprocess
    hub = MarkHubAPI()
    
    # 生成测试图片
    print("\n" + "="*70)
    print("开始生成测试图片")
    print("="*70)
    
    result = hub.generate_image(
        prompt="A magnificent cosmic goddess floating in deep space, surrounded by nebulae and stars, galaxy dress, cosmic energy, ethereal beauty, divine light, universe background, nebula clouds, stardust, celestial aura, hyperdetailed, cinematic lighting, 8k quality",
        title="宇宙女神",
        width=2048,
        height=1024,
        steps=20,
        cfg=7.0,
        validate=True
    )
    
    if result:
        print(f"\n✅ 生成成功：{result}")
    else:
        print(f"\n❌ 生成失败")


if __name__ == "__main__":
    main()
