#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MarkHub - 独立版智能媒体生成中心
不依赖 ComfyUI 服务器，直接使用本地模型生成图片
支持自动下载模型、自动配置、智能错误解决
"""

import subprocess
import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
import threading
import psutil
import hashlib
import shutil

# ============================================================================
# 配置
# ============================================================================
class Config:
    """MarkHub 独立版配置"""
    
    # 路径
    HOME = Path.home()
    BASE_DIR = HOME / ".markhub"
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    OUTPUT_DIR = HOME / "Downloads/markhub_output"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    MODELS_DIR = BASE_DIR / "models"
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    CACHE_DIR = BASE_DIR / "cache"
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    LOG_DIR = BASE_DIR / "logs"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # stable-diffusion.cpp 路径
    SD_CPP_DIR = HOME / "stable-diffusion.cpp"
    SD_CPP_BIN = SD_CPP_DIR / "build" / "bin" / "sd-cli"
    
    # 模型配置
    MODELS = {
        "unet": {
            "filename": "z_image_turbo-Q8_0.gguf",
            "url": "https://huggingface.co/leejet/z_image_turbo-gguf/resolve/main/z_image_turbo-Q8_0.gguf",
            "size_gb": 6.7,
            "required": True
        },
        "clip": {
            "filename": "Qwen3-4B-Q8_0.gguf",
            "url": "https://huggingface.co/leejet/z_image_turbo-gguf/resolve/main/Qwen3-4B-Q8_0.gguf",
            "size_gb": 4.0,
            "required": True
        },
        "vae": {
            "filename": "ae.safetensors",
            "url": "https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors",
            "size_gb": 0.3,
            "required": True
        }
    }
    
    # 默认生成参数
    DEFAULT_WIDTH = 2048
    DEFAULT_HEIGHT = 1024
    DEFAULT_STEPS = 20
    DEFAULT_CFG = 7.0
    DEFAULT_SAMPLER = "euler"
    DEFAULT_SEED = -1  # -1 = 随机


# ============================================================================
# 日志工具
# ============================================================================
class Logger:
    """日志工具"""
    
    def __init__(self):
        self.log_file = Config.LOG_DIR / f"markhub_{datetime.now().strftime('%Y%m%d')}.log"
    
    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] [{level}] {message}"
        print(log_line)
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_line + "\n")
        except:
            pass
    
    def info(self, message: str):
        self.log(message, "INFO")
    
    def error(self, message: str):
        self.log(message, "ERROR")
    
    def success(self, message: str):
        self.log(message, "SUCCESS")
    
    def warning(self, message: str):
        self.log(message, "WARNING")


# ============================================================================
# 模型下载器
# ============================================================================
class ModelDownloader:
    """模型下载器 - 支持断点续传"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
        self.session = None
    
    def _init_session(self):
        if self.session is None:
            try:
                import requests
                self.session = requests.Session()
            except ImportError:
                self.logger.error("requests 库未安装，尝试安装...")
                subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"])
                import requests
                self.session = requests.Session()
    
    def download(self, url: str, dest: Path, model_name: str = "") -> bool:
        """下载模型，支持断点续传"""
        self._init_session()
        
        if dest.exists():
            self.logger.success(f"{model_name} 已存在：{dest.name}")
            return True
        
        try:
            import requests
            
            self.logger.info(f"开始下载 {model_name}...")
            self.logger.info(f"源：{url}")
            self.logger.info(f"目标：{dest}")
            
            # 检查部分下载
            start_pos = 0
            if dest.exists():
                start_pos = dest.stat().st_size
                self.logger.info(f"发现部分下载，从 {start_pos} 字节继续")
            
            headers = {}
            if start_pos > 0:
                headers["Range"] = f"bytes={start_pos}-"
            
            # 开始下载
            response = self.session.get(url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get("content-length", 0))
            if start_pos > 0:
                total_size = start_pos + total_size
            
            mode = "ab" if start_pos > 0 else "wb"
            
            downloaded = start_pos
            chunk_size = 8192
            
            with open(dest, mode) as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # 显示进度
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            mb_downloaded = downloaded / 1024 / 1024
                            mb_total = total_size / 1024 / 1024
                            print(f"\r  进度：{percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end="", flush=True)
            
            print()  # 换行
            self.logger.success(f"{model_name} 下载完成：{dest.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"{model_name} 下载失败：{str(e)}")
            return False


# ============================================================================
# 错误解决器
# ============================================================================
class ErrorSolver:
    """智能错误解决器 - 搜索 GitHub 和 ClawHub"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
        self.session = None
    
    def _init_session(self):
        if self.session is None:
            try:
                import requests
                self.session = requests.Session()
            except:
                pass
    
    def search_github(self, query: str) -> List[Dict]:
        """搜索 GitHub Issues"""
        results = []
        
        try:
            import requests
            url = "https://api.github.com/search/issues"
            params = {
                "q": f"{query} is:issue is:open",
                "sort": "reactions",
                "order": "desc",
                "per_page": 5
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("items", [])[:3]:
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("html_url", ""),
                        "repo": item.get("repository_url", "").split("/")[-2:],
                        "reactions": item.get("reactions", {}).get("+1", 0)
                    })
        except Exception as e:
            self.logger.warning(f"GitHub 搜索失败：{str(e)}")
        
        return results
    
    def search_clawhub(self, query: str) -> List[Dict]:
        """搜索 ClawHub Skills"""
        results = []
        
        try:
            import requests
            # ClawHub 搜索 API（如果有）
            url = f"https://clawhub.ai/skills?q={query}"
            # 简单检查页面
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                results.append({
                    "title": f"在 ClawHub 搜索 '{query}'",
                    "url": url
                })
        except:
            pass
        
        return results
    
    def solve(self, error_message: str, context: str = "") -> List[Dict]:
        """分析错误并提供解决方案"""
        self.logger.info(f"🔍 分析错误：{error_message[:100]}...")
        
        solutions = []
        
        # 提取关键词
        keywords = self._extract_keywords(error_message)
        
        # 搜索 GitHub
        github_results = self.search_github(keywords)
        if github_results:
            solutions.append({
                "source": "GitHub",
                "results": github_results
            })
        
        # 搜索 ClawHub
        clawhub_results = self.search_clawhub(keywords)
        if clawhub_results:
            solutions.append({
                "source": "ClawHub",
                "results": clawhub_results
            })
        
        # 常见错误及解决方案
        common_solutions = self._check_common_errors(error_message)
        if common_solutions:
            solutions.append({
                "source": "常见解决方案",
                "results": common_solutions
            })
        
        return solutions
    
    def _extract_keywords(self, error: str) -> str:
        """从错误信息提取关键词"""
        # 移除常见无意义词
        noise_words = ["error", "failed", "exception", "traceback", "line"]
        words = error.lower().split()
        keywords = [w for w in words if w not in noise_words and len(w) > 3]
        return " ".join(keywords[:5])  # 最多 5 个关键词
    
    def _check_common_errors(self, error: str) -> List[Dict]:
        """检查常见错误"""
        solutions = []
        
        error_lower = error.lower()
        
        if "model not found" in error_lower or "model file" in error_lower:
            solutions.append({
                "title": "模型文件未找到",
                "solution": "运行 'python3 markhub_api.py --download-models' 下载所需模型"
            })
        
        if "out of memory" in error_lower or "memory" in error_lower:
            solutions.append({
                "title": "内存不足",
                "solution": "降低分辨率（--width 1024 --height 512）或减少步数（--steps 10）"
            })
        
        if "sd-cli" in error_lower or "stable-diffusion" in error_lower:
            solutions.append({
                "title": "stable-diffusion.cpp 问题",
                "solution": "运行 'python3 markhub_api.py --install-sd-cpp' 重新安装"
            })
        
        if "permission" in error_lower or "denied" in error_lower:
            solutions.append({
                "title": "权限问题",
                "solution": "检查文件权限：chmod +x ~/.markhub/models/*"
            })
        
        return solutions


# ============================================================================
# 安装管理器
# ============================================================================
class InstallManager:
    """安装管理器 - 自动安装依赖"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def check_sd_cpp(self) -> bool:
        """检查 stable-diffusion.cpp"""
        if Config.SD_CPP_BIN.exists():
            self.logger.success("stable-diffusion.cpp 已安装")
            return True
        
        self.logger.warning("stable-diffusion.cpp 未安装")
        return False
    
    def install_sd_cpp(self) -> bool:
        """安装 stable-diffusion.cpp"""
        self.logger.info("开始安装 stable-diffusion.cpp...")
        
        try:
            # 检查是否已克隆
            if not Config.SD_CPP_DIR.exists():
                self.logger.info("克隆 stable-diffusion.cpp 仓库...")
                result = subprocess.run([
                    "git", "clone",
                    "https://github.com/leejet/stable-diffusion.cpp.git",
                    str(Config.SD_CPP_DIR)
                ], capture_output=True, text=True, timeout=120)
                
                if result.returncode != 0:
                    self.logger.error(f"克隆失败：{result.stderr}")
                    return False
            
            # 编译
            build_dir = Config.SD_CPP_DIR / "build"
            build_dir.mkdir(parents=True, exist_ok=True)
            
            self.logger.info("编译 stable-diffusion.cpp...")
            
            # cmake
            result = subprocess.run([
                "cmake", "..", "-DSD_METAL=ON"
            ], cwd=build_dir, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                self.logger.error(f"cmake 失败：{result.stderr}")
                return False
            
            # make
            result = subprocess.run([
                "make", "-j", str(psutil.cpu_count(logical=False))
            ], cwd=build_dir, capture_output=True, text=True, timeout=600)
            
            if result.returncode != 0:
                self.logger.error(f"make 失败：{result.stderr}")
                return False
            
            self.logger.success("stable-diffusion.cpp 安装完成")
            return True
            
        except Exception as e:
            self.logger.error(f"安装失败：{str(e)}")
            return False
    
    def check_dependencies(self) -> bool:
        """检查 Python 依赖"""
        required = ["PIL", "numpy", "psutil", "requests"]
        missing = []
        
        for pkg in required:
            try:
                __import__(pkg)
            except ImportError:
                missing.append(pkg)
        
        if missing:
            self.logger.warning(f"缺少依赖：{', '.join(missing)}")
            self.logger.info("正在安装...")
            
            subprocess.run([
                sys.executable, "-m", "pip", "install",
                *missing, "-q"
            ])
            
            self.logger.success("依赖安装完成")
        
        return True


# ============================================================================
# MarkHub 主类
# ============================================================================
class MarkHub:
    """MarkHub - 独立版智能媒体生成中心"""
    
    def __init__(self):
        self.logger = Logger()
        self.downloader = ModelDownloader(self.logger)
        self.solver = ErrorSolver(self.logger)
        self.installer = InstallManager(self.logger)
        
        self.logger.info("="*70)
        self.logger.info("🎨 MarkHub - 独立版智能媒体生成中心")
        self.logger.info("="*70)
        
        # 初始化检查
        self._init()
    
    def _init(self):
        """初始化检查"""
        self.logger.info("进行初始化检查...")
        
        # 检查依赖
        self.installer.check_dependencies()
        
        # 检查 stable-diffusion.cpp
        if not self.installer.check_sd_cpp():
            self.logger.warning("stable-diffusion.cpp 未安装，部分功能不可用")
            self.logger.info("运行 'python3 markhub_api.py --install-sd-cpp' 安装")
        
        # 检查模型
        self._check_models()
    
    def _check_models(self):
        """检查模型文件"""
        self.logger.info("📦 检查模型文件...")
        
        all_exist = True
        for model_type, model_info in Config.MODELS.items():
            model_path = Config.MODELS_DIR / model_info["filename"]
            
            if model_path.exists():
                size_gb = model_path.stat().st_size / 1024 / 1024 / 1024
                self.logger.success(f"  ✅ {model_type}: {model_info['filename']} ({size_gb:.2f}GB)")
            else:
                self.logger.warning(f"  ❌ {model_type}: 未找到")
                all_exist = False
        
        if not all_exist:
            self.logger.info("运行 'python3 markhub_api.py --download-models' 下载缺失模型")
        
        return all_exist
    
    def download_all_models(self) -> bool:
        """下载所有模型"""
        self.logger.info("开始下载所有模型...")
        
        success_count = 0
        for model_type, model_info in Config.MODELS.items():
            model_path = Config.MODELS_DIR / model_info["filename"]
            
            if self.downloader.download(
                model_info["url"],
                model_path,
                model_type
            ):
                success_count += 1
        
        self.logger.info(f"下载完成：{success_count}/{len(Config.MODELS)} 个模型")
        return success_count == len(Config.MODELS)
    
    def generate_image(self, prompt: str, title: str = "image",
                      width: int = None, height: int = None,
                      steps: int = None, cfg: float = None,
                      seed: int = None, validate: bool = True) -> Optional[str]:
        """生成图片"""
        
        width = width or Config.DEFAULT_WIDTH
        height = height or Config.DEFAULT_HEIGHT
        steps = steps or Config.DEFAULT_STEPS
        cfg = cfg or Config.DEFAULT_CFG
        
        if seed is None or seed == -1:
            seed = int(time.time() * 1000) % 1000000
        
        self.logger.info("="*70)
        self.logger.info(f"🎨 生成：{title}")
        self.logger.info("="*70)
        self.logger.info(f"提示词：{prompt[:70]}...")
        self.logger.info(f"分辨率：{width}x{height}")
        self.logger.info(f"步数：{steps}, CFG: {cfg}")
        self.logger.info(f"种子：{seed}")
        
        # 检查 stable-diffusion.cpp
        if not Config.SD_CPP_BIN.exists():
            self.logger.error("stable-diffusion.cpp 未安装")
            self.logger.info("运行：python3 markhub_api.py --install-sd-cpp")
            return None
        
        # 检查模型
        for model_type, model_info in Config.MODELS.items():
            model_path = Config.MODELS_DIR / model_info["filename"]
            if not model_path.exists():
                self.logger.error(f"模型未找到：{model_info['filename']}")
                self.logger.info("运行：python3 markhub_api.py --download-models")
                return None
        
        # 生成时间戳
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Config.OUTPUT_DIR / f"{title}_{ts}.png"
        
        # 构建命令
        cmd = [
            str(Config.SD_CPP_BIN),
            "-m", str(Config.MODELS_DIR / Config.MODELS["unet"]["filename"]),
            "-clip", str(Config.MODELS_DIR / Config.MODELS["clip"]["filename"]),
            "-vae", str(Config.MODELS_DIR / Config.MODELS["vae"]["filename"]),
            "-p", prompt,
            "-o", str(output_path),
            "-W", str(width),
            "-H", str(height),
            "--steps", str(steps),
            "--cfg-scale", str(cfg),
            "--sampler", Config.DEFAULT_SAMPLER,
            "--seed", str(seed)
        ]
        
        self.logger.info("🚀 开始生成...")
        start_time = time.time()
        
        try:
            # 执行
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            elapsed = time.time() - start_time
            
            # 记录日志
            if result.stdout:
                self.logger.info(result.stdout)
            if result.stderr:
                self.logger.error(result.stderr)
            
            if result.returncode == 0:
                self.logger.success(f"✅ 生成完成！用时：{elapsed:.1f}秒")
                self.logger.success(f"📁 已保存：{output_path}")
                
                # 验证
                if validate:
                    self._validate_image(output_path)
                
                # 打开目录
                subprocess.run(["open", str(Config.OUTPUT_DIR)])
                
                return str(output_path)
            else:
                self.logger.error(f"❌ 生成失败")
                
                # 尝试解决错误
                if result.stderr:
                    solutions = self.solver.solve(result.stderr)
                    if solutions:
                        self.logger.info("\n💡 建议的解决方案:")
                        for sol in solutions:
                            self.logger.info(f"\n  来自 {sol['source']}:")
                            for item in sol["results"]:
                                if "title" in item:
                                    self.logger.info(f"    - {item['title']}")
                                    if "solution" in item:
                                        self.logger.info(f"      {item['solution']}")
                                    if "url" in item:
                                        self.logger.info(f"      {item['url']}")
                
                return None
        
        except subprocess.TimeoutExpired:
            self.logger.error("⏰ 生成超时")
            return None
        except Exception as e:
            self.logger.error(f"❌ 错误：{str(e)}")
            
            # 尝试解决错误
            solutions = self.solver.solve(str(e))
            if solutions:
                self.logger.info("\n💡 建议的解决方案:")
                for sol in solutions:
                    for item in sol["results"]:
                        if "title" in item:
                            self.logger.info(f"  - {item['title']}")
            
            return None
    
    def _validate_image(self, image_path: Path):
        """验证图片质量"""
        try:
            from PIL import Image
            import numpy as np
            
            img = Image.open(image_path)
            img_array = np.array(img)
            
            brightness = np.mean(img_array)
            contrast = np.std(img_array)
            file_size = image_path.stat().st_size / 1024 / 1024
            
            self.logger.info("\n🔍 质量验证:")
            self.logger.info(f"  尺寸：{img.width}x{img.height}")
            self.logger.info(f"  亮度：{brightness:.1f}")
            self.logger.info(f"  对比度：{contrast:.1f}")
            self.logger.info(f"  文件大小：{file_size:.2f}MB")
            
            if brightness < 20 or brightness > 240:
                self.logger.warning("  ⚠️ 亮度异常")
            if contrast < 30:
                self.logger.warning("  ⚠️ 对比度偏低")
            if file_size < 0.1:
                self.logger.warning("  ⚠️ 文件过小")
            
        except Exception as e:
            self.logger.warning(f"验证失败：{str(e)}")
    
    def auto_generate(self, preset: str = "default"):
        """全自动生成"""
        presets = {
            "default": [
                {"title": "宇宙女神", "prompt": "A magnificent cosmic goddess floating in deep space, surrounded by nebulae and stars, galaxy dress, cosmic energy, ethereal beauty, divine light, universe background, nebula clouds, stardust, celestial aura, hyperdetailed, cinematic lighting, 8k quality"}
            ],
            "landscape": [
                {"title": "风景日落", "prompt": "Beautiful landscape, sunset over mountains, lake reflection, golden hour, cinematic, high quality, detailed"}
            ],
            "portrait": [
                {"title": "人像", "prompt": "Beautiful portrait, professional photography, studio lighting, high quality, detailed"}
            ]
        }
        
        prompts = presets.get(preset, presets["default"])
        
        self.logger.info(f"\n🤖 全自动生成：{preset}")
        
        results = []
        for item in prompts:
            result = self.generate_image(
                item["prompt"],
                item["title"],
                validate=True
            )
            if result:
                results.append(result)
        
        self.logger.info(f"\n✅ 完成：{len(results)} 张")
        return results


# ============================================================================
# 命令行接口
# ============================================================================
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="MarkHub - 独立版智能媒体生成中心")
    parser.add_argument("--download-models", action="store_true", help="下载所有模型")
    parser.add_argument("--install-sd-cpp", action="store_true", help="安装 stable-diffusion.cpp")
    parser.add_argument("--check", action="store_true", help="检查安装状态")
    parser.add_argument("-p", "--prompt", type=str, help="生成图片的提示词")
    parser.add_argument("-t", "--title", type=str, default="image", help="输出文件标题")
    parser.add_argument("-W", "--width", type=int, default=Config.DEFAULT_WIDTH, help="宽度")
    parser.add_argument("-H", "--height", type=int, default=Config.DEFAULT_HEIGHT, help="高度")
    parser.add_argument("-s", "--steps", type=int, default=Config.DEFAULT_STEPS, help="步数")
    parser.add_argument("-c", "--cfg", type=float, default=Config.DEFAULT_CFG, help="CFG 值")
    parser.add_argument("--seed", type=int, default=-1, help="随机种子")
    
    args = parser.parse_args()
    
    hub = MarkHub()
    
    if args.download_models:
        hub.download_all_models()
    elif args.install_sd_cpp:
        hub.installer.install_sd_cpp()
    elif args.check:
        hub._check_models()
        hub.installer.check_sd_cpp()
    elif args.prompt:
        hub.generate_image(
            args.prompt,
            args.title,
            width=args.width,
            height=args.height,
            steps=args.steps,
            cfg=args.cfg,
            seed=args.seed
        )
    else:
        # 默认：自动生成
        hub.auto_generate("default")


if __name__ == "__main__":
    main()
