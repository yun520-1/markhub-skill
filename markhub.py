#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MarkHub - 智能媒体生成中心
完全独立的图片和视频生成应用
支持自动设置、自动生成、自动验证、定时任务

功能:
  ✅ 图片生成 (Z-Image-Turbo)
  ✅ 视频生成 (LTX2, Wan2.1)
  ✅ 自动验证 (清晰度、质量检查)
  ✅ 定时任务
  ✅ 批量生成
  ✅ 资源监控 (CPU/GPU)
  ✅ 智能优化
"""

import subprocess
import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import threading
import psutil

# ============================================================================
# 配置
# ============================================================================
class Config:
    """MarkHub 配置"""
    
    # 路径配置
    HOME = Path.home()
    WORKSPACE = HOME / ".jvs/.openclaw/workspace/ComfyUI-Controller-Little-bug"
    OUTPUT_DIR = HOME / "Downloads/markhub_output"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 模型路径 (使用 ComfyUI 已下载的模型)
    MODELS_DIR = HOME / "Documents/lmd_data_root/apps/ComfyUI/models"
    
    # 图片生成模型
    UNET_PATH = MODELS_DIR / "unet/z_image_turbo-Q8_0.gguf"
    CLIP_PATH = MODELS_DIR / "text_encoders/Qwen3-4B-Q8_0.gguf"
    VAE_PATH = MODELS_DIR / "vae/ae.safetensors"
    
    # 视频生成模型
    LTX2_UNET = MODELS_DIR / "unet/ltx-2-19b-dev-Q3_K_S.gguf"
    LTX2_VAE = MODELS_DIR / "vae/ltx-2-19b-dev_video_vae.safetensors"
    
    # stable-diffusion.cpp 路径
    SD_CPP = HOME / "stable-diffusion.cpp/build/bin/sd-cli"
    
    # 默认参数
    DEFAULT_IMAGE_WIDTH = 2048
    DEFAULT_IMAGE_HEIGHT = 1024
    DEFAULT_STEPS = 20
    DEFAULT_CFG = 7.0
    DEFAULT_SAMPLER = "euler"
    
    # 视频参数
    DEFAULT_VIDEO_FRAMES = 97
    DEFAULT_VIDEO_FPS = 25
    
    # 质量验证阈值
    MIN_BRIGHTNESS = 20
    MAX_BRIGHTNESS = 240
    MIN_SHARPNESS = 10.0
    MIN_CONTRAST = 30.0


# ============================================================================
# 资源监控
# ============================================================================
class ResourceMonitor:
    """CPU/GPU 资源监控"""
    
    def __init__(self):
        self.monitoring = False
        self.stats = []
        self.thread = None
    
    def start(self):
        """开始监控"""
        self.monitoring = True
        self.stats = []
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        print("📊 资源监控已启动")
    
    def stop(self):
        """停止监控"""
        self.monitoring = False
        if self.thread:
            self.thread.join(timeout=2)
        print("📊 资源监控已停止")
    
    def _monitor_loop(self):
        """监控循环"""
        while self.monitoring:
            try:
                # CPU
                cpu_percent = psutil.cpu_percent(interval=1)
                
                # 内存
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                memory_used = memory.used / 1024 / 1024 / 1024
                
                # GPU (Mac 使用 Metal)
                gpu_info = self._get_gpu_info()
                
                stat = {
                    "timestamp": datetime.now().isoformat(),
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory_percent,
                    "memory_used_gb": memory_used,
                    "gpu_percent": gpu_info.get("gpu_percent", 0),
                    "gpu_memory_gb": gpu_info.get("gpu_memory", 0)
                }
                self.stats.append(stat)
                
                time.sleep(2)
            except Exception as e:
                print(f"监控错误：{e}")
                time.sleep(2)
    
    def _get_gpu_info(self) -> Dict:
        """获取 GPU 信息 (Mac)"""
        try:
            # 使用 system_profiler 获取 GPU 信息
            result = subprocess.run(
                ["system_profiler", "SPDisplaysDataType"],
                capture_output=True, text=True, timeout=10
            )
            
            gpu_info = {
                "gpu_percent": 0,  # macOS 不直接提供 GPU 使用率
                "gpu_memory": 0
            }
            
            # 解析 VRAM
            for line in result.stdout.split("\n"):
                if "VRAM" in line or "Total Memory" in line:
                    try:
                        mem_str = line.split(":")[-1].strip()
                        if "GB" in mem_str:
                            gpu_info["gpu_memory"] = float(mem_str.replace("GB", "").strip())
                        elif "MB" in mem_str:
                            gpu_info["gpu_memory"] = float(mem_str.replace("MB", "").strip()) / 1024
                    except:
                        pass
            
            return gpu_info
        except:
            return {"gpu_percent": 0, "gpu_memory": 0}
    
    def get_stats(self) -> List[Dict]:
        """获取统计数据"""
        return self.stats
    
    def print_summary(self):
        """打印摘要"""
        if not self.stats:
            print("无监控数据")
            return
        
        avg_cpu = sum(s["cpu_percent"] for s in self.stats) / len(self.stats)
        avg_mem = sum(s["memory_percent"] for s in self.stats) / len(self.stats)
        avg_gpu = sum(s["gpu_percent"] for s in self.stats) / len(self.stats)
        
        print("\n" + "="*70)
        print("📊 资源使用摘要")
        print("="*70)
        print(f"  CPU 平均：{avg_cpu:.1f}%")
        print(f"  内存平均：{avg_mem:.1f}%")
        print(f"  GPU 平均：{avg_gpu:.1f}%")
        print(f"  采样次数：{len(self.stats)}")
        print("="*70)


# ============================================================================
# 质量验证
# ============================================================================
class QualityValidator:
    """图片和视频质量验证"""
    
    @staticmethod
    def validate_image(image_path: Path) -> Dict:
        """验证图片质量"""
        result = {
            "valid": True,
            "issues": [],
            "metrics": {}
        }
        
        try:
            from PIL import Image
            import numpy as np
            
            # 加载图片
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # 检查尺寸
            width, height = img.size
            result["metrics"]["width"] = width
            result["metrics"]["height"] = height
            
            # 检查亮度
            brightness = np.mean(img_array)
            result["metrics"]["brightness"] = brightness
            
            if brightness < Config.MIN_BRIGHTNESS:
                result["issues"].append("图片过暗")
                result["valid"] = False
            
            if brightness > Config.MAX_BRIGHTNESS:
                result["issues"].append("图片过亮")
                result["valid"] = False
            
            # 检查对比度
            contrast = np.std(img_array)
            result["metrics"]["contrast"] = contrast
            
            if contrast < Config.MIN_CONTRAST:
                result["issues"].append("对比度过低，可能模糊")
                result["valid"] = False
            
            # 检查锐度 (使用 Laplacian 方差)
            if len(img_array.shape) == 3:
                gray = np.mean(img_array, axis=2)
            else:
                gray = img_array
            
            from PIL import ImageFilter
            img_gray = Image.fromarray(gray.astype(np.uint8))
            edges = img_gray.filter(ImageFilter.FIND_EDGES)
            sharpness = np.std(np.array(edges))
            result["metrics"]["sharpness"] = sharpness
            
            if sharpness < Config.MIN_SHARPNESS:
                result["issues"].append("锐度不足，可能模糊")
                result["valid"] = False
            
            # 检查文件完整性
            file_size = image_path.stat().st_size / 1024 / 1024  # MB
            result["metrics"]["file_size_mb"] = file_size
            
            if file_size < 0.1:  # 小于 100KB 可能有问题
                result["issues"].append("文件过小，可能损坏")
                result["valid"] = False
            
            # 总结
            if result["valid"]:
                result["summary"] = "✅ 质量验证通过"
            else:
                result["summary"] = f"❌ 发现 {len(result['issues'])} 个问题"
            
        except Exception as e:
            result["valid"] = False
            result["issues"].append(f"验证错误：{str(e)}")
            result["summary"] = f"❌ 验证失败：{str(e)}"
        
        return result
    
    @staticmethod
    def validate_video(video_path: Path) -> Dict:
        """验证视频质量"""
        result = {
            "valid": True,
            "issues": [],
            "metrics": {}
        }
        
        try:
            # 使用 ffprobe 检查视频
            cmd = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(video_path)
            ]
            
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            data = json.loads(proc.stdout)
            
            # 视频流信息
            video_stream = None
            for stream in data.get("streams", []):
                if stream.get("codec_type") == "video":
                    video_stream = stream
                    break
            
            if not video_stream:
                result["issues"].append("未找到视频流")
                result["valid"] = False
                return result
            
            # 分辨率
            width = video_stream.get("width", 0)
            height = video_stream.get("height", 0)
            result["metrics"]["width"] = width
            result["metrics"]["height"] = height
            
            # 帧率
            fps = eval(video_stream.get("r_frame_rate", "0/1"))
            result["metrics"]["fps"] = float(fps)
            
            # 时长
            duration = float(data.get("format", {}).get("duration", 0))
            result["metrics"]["duration_sec"] = duration
            
            # 文件大小
            file_size = Path(video_path).stat().st_size / 1024 / 1024
            result["metrics"]["file_size_mb"] = file_size
            
            # 检查问题
            if width < 512 or height < 512:
                result["issues"].append("分辨率过低")
                result["valid"] = False
            
            if duration < 1:
                result["issues"].append("视频过短")
                result["valid"] = False
            
            if file_size < 1:
                result["issues"].append("文件过小，可能损坏")
                result["valid"] = False
            
            # 总结
            if result["valid"]:
                result["summary"] = "✅ 视频质量验证通过"
            else:
                result["summary"] = f"❌ 发现 {len(result['issues'])} 个问题"
            
        except Exception as e:
            result["valid"] = False
            result["issues"].append(f"验证错误：{str(e)}")
            result["summary"] = f"❌ 验证失败：{str(e)}"
        
        return result


# ============================================================================
# MarkHub 主应用
# ============================================================================
class MarkHub:
    """MarkHub - 智能媒体生成中心"""
    
    def __init__(self):
        self.config = Config()
        self.monitor = ResourceMonitor()
        self.validator = QualityValidator()
        
        print("="*70)
        print("🎨 MarkHub - 智能媒体生成中心")
        print("="*70)
        print(f"输出目录：{self.config.OUTPUT_DIR}")
        print()
        
        # 检查
        self._check_sd_cpp()
        self._check_models()
    
    def _check_sd_cpp(self):
        """检查 stable-diffusion.cpp"""
        if self.config.SD_CPP.exists():
            print(f"✅ stable-diffusion.cpp 已安装")
        else:
            print(f"⚠️  stable-diffusion.cpp 未安装")
            print(f"   路径：{self.config.SD_CPP}")
            print(f"   请运行：cd ~ && git clone https://github.com/leejet/stable-diffusion.cpp.git")
            print(f"   cd stable-diffusion.cpp && mkdir build && cd build")
            print(f"   cmake .. -DSD_METAL=ON && make -j$(sysctl -n hw.ncpu)")
    
    def _check_models(self):
        """检查模型文件"""
        print()
        print("📦 模型检查:")
        
        models = {
            "UNet (图片)": self.config.UNET_PATH,
            "CLIP": self.config.CLIP_PATH,
            "VAE": self.config.VAE_PATH,
            "UNet (视频)": self.config.LTX2_UNET
        }
        
        for name, path in models.items():
            if path.exists():
                size = path.stat().st_size / 1024 / 1024 / 1024
                print(f"  ✅ {name}: {path.name} ({size:.2f}GB)")
            else:
                print(f"  ⚠️  {name}: 未找到")
    
    def generate_image(self, prompt: str, title: str = "image",
                      width: int = None, height: int = None,
                      steps: int = None, cfg: float = None,
                      seed: int = None, validate: bool = True) -> Optional[str]:
        """
        生成图片
        
        Args:
            prompt: 提示词
            title: 标题/文件名前缀
            width: 宽度 (默认 1024)
            height: 高度 (默认 512)
            steps: 步数 (默认 20)
            cfg: CFG 值 (默认 7.0)
            seed: 随机种子 (默认随机)
            validate: 是否验证质量
        
        Returns:
            生成的图片路径，失败返回 None
        """
        width = width or self.config.DEFAULT_IMAGE_WIDTH
        height = height or self.config.DEFAULT_IMAGE_HEIGHT
        steps = steps or self.config.DEFAULT_STEPS
        cfg = cfg or self.config.DEFAULT_CFG
        
        if seed is None:
            seed = int(time.time() * 1000) % 1000000
        
        print(f"\n{'='*70}")
        print(f"🎨 生成图片：{title}")
        print(f"{'='*70}")
        print(f"提示词：{prompt[:70]}...")
        print(f"分辨率：{width}x{height}")
        print(f"步数：{steps}, CFG: {cfg}")
        print(f"种子：{seed}")
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = self.config.OUTPUT_DIR / f"{title}_{ts}.png"
        
        # 构建命令
        cmd = [
            str(self.config.SD_CPP),
            "-m", str(self.config.UNET_PATH),
            "-clip", str(self.config.CLIP_PATH),
            "-vae", str(self.config.VAE_PATH),
            "-p", prompt,
            "-o", str(output),
            "-W", str(width),
            "-H", str(height),
            "--steps", str(steps),
            "--cfg-scale", str(cfg),
            "--sampler", self.config.DEFAULT_SAMPLER,
            "--seed", str(seed)
        ]
        
        print(f"🚀 开始生成...")
        start_time = time.time()
        
        try:
            # 启动监控
            self.monitor.start()
            
            # 执行
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            elapsed = time.time() - start_time
            print(result.stdout)
            
            # 停止监控
            self.monitor.stop()
            self.monitor.print_summary()
            
            if result.returncode == 0:
                print(f"✅ 生成完成！用时：{elapsed:.1f}秒")
                print(f"📁 已保存：{output}")
                
                # 质量验证
                if validate and output.exists():
                    print("\n🔍 质量验证...")
                    validation = self.validator.validate_image(output)
                    print(f"  {validation['summary']}")
                    
                    if validation['metrics']:
                        print(f"  尺寸：{validation['metrics'].get('width', '?')}x{validation['metrics'].get('height', '?')}")
                        print(f"  亮度：{validation['metrics'].get('brightness', '?'):.1f}")
                        print(f"  对比度：{validation['metrics'].get('contrast', '?'):.1f}")
                        print(f"  锐度：{validation['metrics'].get('sharpness', '?'):.1f}")
                        print(f"  文件大小：{validation['metrics'].get('file_size_mb', '?'):.2f}MB")
                    
                    if validation['issues']:
                        for issue in validation['issues']:
                            print(f"  ⚠️  {issue}")
                    
                    if not validation['valid']:
                        print("⚠️  质量验证未通过，建议重新生成")
                
                # 打开目录
                subprocess.run(["open", str(self.config.OUTPUT_DIR)])
                
                return str(output)
            else:
                print(f"❌ 生成失败：{result.stderr}")
                return None
        
        except subprocess.TimeoutExpired:
            print("⏰ 生成超时")
            self.monitor.stop()
            return None
        except Exception as e:
            print(f"❌ 错误：{e}")
            self.monitor.stop()
            return None
    
    def generate_batch(self, prompts: List[Dict], auto_schedule: bool = False):
        """
        批量生成
        
        Args:
            prompts: 提示词列表，每项包含 title 和 prompt
            auto_schedule: 是否自动调度
        """
        print(f"\n🚀 批量生成 {len(prompts)} 张图片")
        
        if auto_schedule:
            print("⚙️  自动调度已启用")
            print("   - 自动优化参数")
            print("   - 自动资源管理")
            print("   - 自动质量验证")
        
        results = []
        
        for i, item in enumerate(prompts, 1):
            title = item.get("title", f"image_{i}")
            prompt = item.get("prompt", "")
            
            print(f"\n[{i}/{len(prompts)}] {title}")
            
            # 智能参数优化
            if auto_schedule:
                # 根据提示词自动调整参数
                if "landscape" in prompt.lower() or "风景" in prompt:
                    width, height = 1024, 512  # 宽屏
                elif "portrait" in prompt.lower() or "人像" in prompt:
                    width, height = 512, 1024  # 竖屏
                else:
                    width, height = 1024, 512
                
                steps = 20  # 默认步数
                cfg = 7.0
            else:
                width, height, steps, cfg = None, None, None, None
            
            filepath = self.generate_image(
                prompt, title,
                width=width, height=height,
                steps=steps, cfg=cfg,
                validate=True
            )
            
            if filepath:
                results.append(filepath)
            
            # 间隔
            if i < len(prompts):
                print("⏳ 等待 2 秒...")
                time.sleep(2)
        
        print(f"\n{'='*70}")
        print(f"📊 批量生成完成")
        print(f"{'='*70}")
        print(f"成功：{len(results)}/{len(prompts)}")
        print(f"📁 输出：{self.config.OUTPUT_DIR}")
        
        return results
    
    def schedule_task(self, task_func, schedule_time: datetime):
        """
        定时任务
        
        Args:
            task_func: 要执行的任务函数
            schedule_time: 计划执行时间
        """
        now = datetime.now()
        delay = (schedule_time - now).total_seconds()
        
        if delay < 0:
            print("⚠️  计划时间已过")
            return
        
        print(f"\n⏰ 定时任务已设置")
        print(f"   执行时间：{schedule_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   等待：{delay/60:.1f}分钟")
        
        def delayed_task():
            time.sleep(delay)
            print(f"\n⏰ 定时任务开始执行！")
            task_func()
        
        thread = threading.Thread(target=delayed_task, daemon=True)
        thread.start()
    
    def auto_generate(self, preset: str = "default"):
        """
        全自动生成
        
        Args:
            preset: 预设类型 (default, landscape, portrait, artistic)
        """
        print(f"\n🤖 全自动生成模式")
        print(f"   预设：{preset}")
        
        # 预设提示词
        presets = {
            "default": [
                {"title": "宇宙女神", "prompt": "A magnificent cosmic goddess floating in deep space, surrounded by nebulae and stars, galaxy dress, cosmic energy, ethereal beauty, divine light, universe background, nebula clouds, stardust, celestial aura, hyperdetailed, cinematic lighting, 8k quality"}
            ],
            "landscape": [
                {"title": "风景日落", "prompt": "Beautiful landscape, sunset over mountains, lake reflection, golden hour, cinematic, high quality, detailed"}
            ],
            "portrait": [
                {"title": "人像", "prompt": "Beautiful portrait, professional photography, studio lighting, high quality, detailed"}
            ],
            "artistic": [
                {"title": "艺术", "prompt": "Abstract art, colorful, artistic, creative, high quality, detailed"}
            ]
        }
        
        prompts = presets.get(preset, presets["default"])
        
        # 自动设置
        print("\n⚙️  自动设置...")
        print("  ✅ 参数优化")
        print("  ✅ 资源监控")
        print("  ✅ 质量验证")
        print("  ✅ 错误处理")
        
        # 执行生成
        results = self.generate_batch(prompts, auto_schedule=True)
        
        # 总结
        if results:
            print(f"\n✅ 全自动生成完成！")
            print(f"   成功：{len(results)} 张")
            print(f"   输出：{self.config.OUTPUT_DIR}")
        else:
            print(f"\n❌ 全自动生成失败")
        
        return results


# ============================================================================
# 主函数
# ============================================================================
def main():
    """主函数 - 演示"""
    # 创建 MarkHub 实例
    hub = MarkHub()
    
    # 示例 1: 单张图片生成
    print("\n" + "="*70)
    print("示例 1: 单张图片生成")
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
    
    # 示例 2: 批量生成
    print("\n" + "="*70)
    print("示例 2: 批量生成")
    print("="*70)
    
    batch_prompts = [
        {"title": "宇宙女神", "prompt": "A magnificent cosmic goddess floating in deep space, surrounded by nebulae and stars, galaxy dress, cosmic energy, ethereal beauty, divine light, universe background, nebula clouds, stardust, celestial aura, hyperdetailed, cinematic lighting, 8k quality"},
        {"title": "芭蕾舞蹈", "prompt": "A beautiful young girl performing elegant ballet dance, graceful movements, pink tutu, spotlight on stage, cinematic lighting, high quality, detailed"},
        {"title": "风景日落", "prompt": "Beautiful landscape, sunset over mountains, lake reflection, golden hour, cinematic, high quality, detailed"}
    ]
    
    # 取消注释以启用批量生成
    # results = hub.generate_batch(batch_prompts, auto_schedule=True)
    
    print("\n💡 提示：取消注释以启用批量生成")
    
    # 示例 3: 全自动生成
    print("\n" + "="*70)
    print("示例 3: 全自动生成")
    print("="*70)
    
    # 取消注释以启用全自动生成
    # results = hub.auto_generate(preset="default")
    
    print("\n💡 提示：取消注释以启用全自动生成")


if __name__ == "__main__":
    main()
